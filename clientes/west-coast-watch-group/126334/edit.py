# Edita los 2 creativos del 126334: textos sobreimpresos (HTML -> PNG transparente), cierre de marca, SFX y export 1080x1920.
# Uso: python3 edit.py  (espera video/raw-01.mp4 y video/raw-02.mp4)
import base64, json, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[2]
FONTS_DIR = ROOT / ".claude/creator-profile/nahuel/assets/fonts"
SFX = ROOT / ".claude/creator-profile/nahuel/assets/sfx"
CHROME = "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome"
OUT = HERE / "video"; TMP = HERE / "_tmp"; TMP.mkdir(exist_ok=True)
W, H, END = 1080, 1920, 2.2  # duración de la placa final

def face(fam, file, w, style):
    b = base64.b64encode((FONTS_DIR / file).read_bytes()).decode()
    return f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{style};src:url(data:font/otf;base64,{b})}}"
FONTS = face("Inter", "Inter-Regular.otf", 400, "normal") + face("Inter", "Inter-Bold.otf", 700, "normal") + \
        face("Playfair", "PlayfairDisplay-Italic.ttf", 400, "italic")
CSS = """*{margin:0;padding:0}body{width:1080px;height:1920px;background:transparent;font-family:Inter,sans-serif;color:#fff}
.t{position:absolute;left:0;right:0;top:%dpx;text-align:center;text-shadow:0 4px 40px rgba(0,0,0,.85)}
.big{font-family:Playfair,serif;font-style:italic;font-size:118px;line-height:1.05}
.small{margin-top:26px;font-size:30px;font-weight:700;letter-spacing:.32em;color:#d7dbe2}
.line{width:90px;height:2px;background:#9fb4d6;margin:30px auto 0}
.end{position:absolute;inset:0;background:#000;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.mark{font-size:30px;font-weight:700;letter-spacing:.5em;color:#9fb4d6;margin-bottom:34px}
.brand{font-family:Playfair,serif;font-style:italic;font-size:104px;line-height:1.05}
.sub{margin-top:34px;font-size:28px;font-weight:700;letter-spacing:.3em;color:#d7dbe2}
.cta{margin-top:90px;padding:26px 58px;border:2px solid #fff;border-radius:999px;font-size:32px;font-weight:700;letter-spacing:.22em}
.legal{position:absolute;bottom:150px;font-size:22px;color:#7d828c;letter-spacing:.06em}"""

def png(name, body, top=300):
    src = TMP / f"{name}.html"
    src.write_text(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{FONTS}{CSS % top}</style></head><body>{body}</body></html>")
    out = TMP / f"{name}.png"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{H}",
                    "--default-background-color=00000000", "--virtual-time-budget=2000", f"--screenshot={out}", str(src)],
                   check=True, stderr=subprocess.DEVNULL)
    return out

def card(big, small, top):
    return f'<div class="t"><div class="big">{big}</div><div class="line"></div><div class="small">{small}</div></div>'

END_CARD = ('<div class="end"><div class="mark">EST. SAN DIEGO</div><div class="brand">West Coast<br>Watch Group</div>'
            '<div class="sub">PRE-OWNED LUXURY WATCHES</div><div class="cta">DM TO SEE IT LIVE</div>'
            '<div class="legal">Independent dealer. Not affiliated with Rolex SA.</div></div>')

# (inicio, fin, grande, chico) para cada creativo; top = altura del bloque de texto
SPOTS = {
    "01-full-set": dict(top=300, cards=[(0.3, 2.7, "Datejust 41", "REF. 126334 · BLUE DIAMOND"),
                                         (2.9, 5.3, "Full set.", "BOX & PAPERS · JUBILEE"),
                                         (5.5, 7.9, "See it live.", "MESSAGE US TODAY")],
                        sfx=[("shine", 0.25, 0.5), ("woosh", 2.85, 0.35), ("shine", 4.2, 0.45), ("woosh", 5.45, 0.35), ("riser", 6.6, 0.4), ("impact", 8.0, 0.5)]),
    "02-macro": dict(top=260, cards=[(0.3, 2.7, "Ten diamonds.", "ONE BLUE DIAL"),
                                      (2.9, 5.3, "18k white gold.", "FLUTED BEZEL · 41 MM"),
                                      (5.5, 7.9, "Datejust 41", "REF. 126334 · JUBILEE")],
                     sfx=[("shine", 0.25, 0.55), ("woosh", 2.85, 0.35), ("shine", 3.6, 0.45), ("woosh", 5.45, 0.35), ("riser", 6.6, 0.4), ("impact", 8.0, 0.5)]),
}

end_png = png("end", END_CARD)
for i, (name, spec) in enumerate(SPOTS.items(), 1):
    raw = OUT / f"raw-{i:02d}.mp4"
    pngs = [png(f"{name}-{k}", card(b, s, spec["top"]), spec["top"]) for k, (_, _, b, s) in enumerate(spec["cards"])]
    inputs = ["-i", str(raw)] + sum([["-loop", "1", "-t", "10", "-i", str(p)] for p in pngs], []) + ["-loop", "1", "-t", str(END), "-i", str(end_png)]
    # base: escala a 1080x1920, leve grade (contraste y viñeta), y se le agrega la placa final al final
    f = [f"[0:v]scale={W}:{H}:flags=lanczos,eq=contrast=1.06:saturation=1.05,vignette=PI/5,format=yuva420p,trim=0:8,setpts=PTS-STARTPTS[base]"]
    last = "base"
    for k, (a, b, _, _) in enumerate(spec["cards"], 1):
        f.append(f"[{k}:v]format=rgba,fade=t=in:st={a}:d=0.45:alpha=1,fade=t=out:st={b-0.4}:d=0.4:alpha=1[o{k}]")
        f.append(f"[{last}][o{k}]overlay=0:0:shortest=1:enable='between(t,{a},{b})'[v{k}]"); last = f"v{k}"
    e = len(spec["cards"]) + 1
    f.append(f"[{last}]fade=t=out:st=7.6:d=0.4,fps=24,format=yuv420p[main]")
    f.append(f"[{e}:v]scale={W}:{H},fps=24,fade=t=in:st=0:d=0.5,fade=t=out:st={END-0.4}:d=0.4,format=yuv420p,setsar=1[endv]")
    f.append("[main][endv]concat=n=2:v=1:a=0[v]")
    # sonido: SFX posicionados, mezclados y normalizados
    a_in = []; a_f = []
    for j, (s, t, vol) in enumerate(spec["sfx"]):
        a_in += ["-i", str(SFX / f"{s}.mp3")]
        idx = e + 1 + j
        a_f.append(f"[{idx}:a]volume={vol},adelay={int(t*1000)}|{int(t*1000)}[a{j}]")
    n = len(spec["sfx"])
    a_f.append("".join(f"[a{j}]" for j in range(n)) + f"amix=inputs={n}:normalize=0,apad,atrim=0:{8+END},alimiter=limit=0.8[a]")
    dst = OUT / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, *a_in, "-filter_complex", ";".join(f + a_f),
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(dst)], check=True)
    print(dst)
