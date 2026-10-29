# Edita los 2 spots emocionales ("The Drive" y "The Milestone"): tomas de Kling + macro verificada, crossfades,
# una línea de texto por toma, placa de marca y SFX. Salida 1080x1920 (reel) en video/.
import base64, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[3]
FONTS_DIR = ROOT / ".claude/creator-profile/nahuel/assets/fonts"
SFX = ROOT / ".claude/creator-profile/nahuel/assets/sfx"
CHROME = "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome"
CLIPS, OUT, TMP = HERE / "clips", HERE / "video", HERE / "_tmp"
OUT.mkdir(exist_ok=True); TMP.mkdir(exist_ok=True)
MACRO = HERE.parent / "video/raw-02.mp4"
W, H, X = 1080, 1920, 0.4  # X = duración del crossfade

def face(fam, file, w, style):
    b = base64.b64encode((FONTS_DIR / file).read_bytes()).decode()
    return f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{style};src:url(data:font/otf;base64,{b})}}"
FONTS = face("Inter", "Inter-Bold.otf", 700, "normal") + face("Playfair", "PlayfairDisplay-Italic.ttf", 400, "italic")
CSS = """*{margin:0;padding:0}body{width:1080px;height:1920px;background:transparent;font-family:Inter,sans-serif;color:#fff}
.t{position:absolute;left:0;right:0;top:1130px;text-align:center;text-shadow:0 4px 50px rgba(0,0,0,.9),0 0 18px rgba(0,0,0,.6)}
.big{font-family:Playfair,serif;font-style:italic;font-size:104px;line-height:1.08}
.small{margin-top:24px;font-size:28px;font-weight:700;letter-spacing:.32em;color:#e3e6ec}
.end{position:absolute;inset:0;background:#000;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.mark{font-size:28px;font-weight:700;letter-spacing:.5em;color:#9fb4d6;margin-bottom:34px}
.brand{font-family:Playfair,serif;font-style:italic;font-size:104px;line-height:1.05}
.sub{margin-top:34px;font-size:26px;font-weight:700;letter-spacing:.3em;color:#d7dbe2}
.cta{margin-top:90px;padding:26px 58px;border:2px solid #fff;border-radius:999px;font-size:30px;font-weight:700;letter-spacing:.22em}
.legal{position:absolute;bottom:150px;font-size:22px;color:#7d828c;letter-spacing:.06em}"""

def png(name, body):
    src = TMP / f"{name}.html"
    src.write_text(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{FONTS}{CSS}</style></head><body>{body}</body></html>")
    out = TMP / f"{name}.png"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{H}",
                    "--default-background-color=00000000", "--virtual-time-budget=2000", f"--screenshot={out}", str(src)],
                   check=True, stderr=subprocess.DEVNULL)
    return out

END_CARD = ('<div class="end"><div class="mark">EST. SAN DIEGO</div><div class="brand">West Coast<br>Watch Group</div>'
            '<div class="sub">PRE-OWNED LUXURY WATCHES</div><div class="cta">DM TO SEE IT LIVE</div>'
            '<div class="legal">Independent dealer. Not affiliated with Rolex SA.</div></div>')

# (archivo, inicio dentro del clip, duración, texto grande, texto chico)
SPOTS = {
    "03-the-drive": [("A1.mp4", 0.3, 3.0, "The road.", ""),
                     ("A2.mp4", 0.0, 2.4, "The details.", ""),
                     ("A3.mp4", 0.3, 3.2, "The arrival.", ""),
                     (str(MACRO), 1.2, 3.0, "Datejust 41", "REF. 126334 · BLUE DIAMOND")],
    "04-the-milestone": [("B1.mp4", 0.2, 3.2, "The deal.", ""),
                         ("B2.mp4", 0.3, 3.0, "The toast.", ""),
                         ("B3.mp4", 1.4, 3.6, "The moment you keep.", ""),
                         (str(MACRO), 1.2, 3.0, "Datejust 41", "REF. 126334 · BLUE DIAMOND")],
    # anuncio completo: las dos historias, el full set (confianza) y la macro, en un solo spot
    "05-anuncio-completo": [("A1.mp4", 0.3, 3.0, "The road.", ""),
                            ("A2.mp4", 0.0, 2.4, "The details.", ""),
                            ("A3.mp4", 0.3, 3.2, "The arrival.", ""),
                            ("B1.mp4", 0.2, 3.2, "The deal.", ""),
                            ("B2.mp4", 0.3, 3.0, "The toast.", ""),
                            ("B3.mp4", 1.4, 3.6, "The moment you keep.", ""),
                            (str(HERE.parent / "video/raw-01.mp4"), 2.0, 2.8, "Full set.", "BOX & PAPERS · JUBILEE"),
                            (str(MACRO), 1.2, 3.0, "Datejust 41", "REF. 126334 · BLUE DIAMOND")],
}
END = 3.4

end_png = png("end", END_CARD)
for name, shots in SPOTS.items():
    seq = shots + [("END", 0, END, "", "")]
    ins, f = [], []
    for k, (src, ss, d, big, small) in enumerate(seq):
        if src == "END":
            ins += ["-i", str(OUT / "_endcard.mp4")]  # placa final animada (endcard.py)
            f.append(f"[{k}:v]scale={W}:{H},fps=24,format=yuv420p,setsar=1[s{k}]")
        else:
            p = pathlib.Path(src) if "/" in src else CLIPS / src
            ins += ["-ss", str(ss), "-t", str(d), "-i", str(p)]
            f.append(f"[{k}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=24,"
                     f"eq=contrast=1.05:saturation=1.04,vignette=PI/5,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[s{k}]")
    # crossfades encadenados
    last, t = "s0", seq[0][2]
    starts = [0.0]
    for k in range(1, len(seq)):
        off = t - X
        f.append(f"[{last}][s{k}]xfade=transition=fade:duration={X}:offset={off:.3f}[x{k}]")
        starts.append(off); last = f"x{k}"; t = off + seq[k][2]
    total = t
    # una línea de texto por toma
    n_in = len(seq)
    for k, (src, ss, d, big, small) in enumerate(seq):
        if not big: continue
        body = f'<div class="t"><div class="big">{big}</div>' + (f'<div class="small">{small}</div>' if small else "") + "</div>"
        ins += ["-loop", "1", "-t", f"{total:.2f}", "-i", str(png(f"{name}-{k}", body))]
        a, b = starts[k] + 0.35, starts[k] + d - 0.45
        f.append(f"[{n_in}:v]format=rgba,fade=t=in:st={a:.2f}:d=0.5:alpha=1,fade=t=out:st={b-0.35:.2f}:d=0.35:alpha=1[o{k}]")
        f.append(f"[{last}][o{k}]overlay=0:0:shortest=1:enable='between(t,{a:.2f},{b:.2f})'[t{k}]"); last = f"t{k}"; n_in += 1
    f.append(f"[{last}]format=yuv420p[v]")
    # SFX: woosh en cada corte, brillo en la macro, impacto en la placa
    cues = [("woosh", s - 0.15, 0.3) for s in starts[1:-1]] + [("shine", starts[-2] + 0.3, 0.5), ("riser", starts[-1] - 1.4, 0.35), ("impact", starts[-1] + 0.05, 0.45)]
    a_f = []
    for j, (s, at, vol) in enumerate(cues):
        ins += ["-i", str(SFX / f"{s}.mp3")]
        ms = int(max(at, 0) * 1000)
        a_f.append(f"[{n_in + j}:a]volume={vol},adelay={ms}|{ms}[a{j}]")
    a_f.append("".join(f"[a{j}]" for j in range(len(cues))) + f"amix=inputs={len(cues)}:normalize=0,apad,atrim=0:{total:.2f},alimiter=limit=0.8[a]")
    dst = OUT / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(f + a_f), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", str(dst)], check=True)
    print(dst, f"{total:.1f}s")
