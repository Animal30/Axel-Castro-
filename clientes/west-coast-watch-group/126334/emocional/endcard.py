# Placa final v2 de West Coast Watch Group: más sobria y exclusiva.
# Capas PNG transparentes (Chrome) animadas con ffmpeg: aparición escalonada, línea dorada que se dibuja,
# leve acercamiento y grano fino. Salida: video/_endcard.mp4 (1080x1920, 24 fps, 3.4 s, sin audio).
import base64, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[3]
FONTS_DIR = ROOT / ".claude/creator-profile/nahuel/assets/fonts"
CHROME = "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome"
TMP = HERE / "_tmp_end"; TMP.mkdir(exist_ok=True)
OUT = HERE / "video/_endcard.mp4"
W, H, D = 1080, 1920, 3.4
GOLD = "#c9b27c"

def face(fam, file, w, style):
    b = base64.b64encode((FONTS_DIR / file).read_bytes()).decode()
    return f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{style};src:url(data:font/otf;base64,{b})}}"
FONTS = face("Inter", "Inter-Regular.otf", 400, "normal") + face("Inter", "Inter-Bold.otf", 700, "normal") + \
        face("Playfair", "PlayfairDisplay-Italic.ttf", 400, "italic")
BASE = f"""*{{margin:0;padding:0}}body{{width:{W}px;height:{H}px;background:transparent;font-family:Inter,sans-serif;color:#f4f1ea}}
.c{{position:absolute;left:0;right:0;text-align:center}}"""

LAYERS = {
    # fondo: negro con un halo azul noche muy sutil (eco del dial) y marco fino dorado
    "bg": (f"""body{{background:radial-gradient(ellipse at 50% 46%,#0d1726 0%,#05070b 55%,#000 100%)}}
.f{{position:absolute;inset:70px;border:1.5px solid {GOLD};opacity:.28}}""", '<div class="f"></div>'),
    "mono": (f".c{{top:640px;font-size:24px;font-weight:700;letter-spacing:.9em;padding-left:.9em;color:{GOLD}}}",
             '<div class="c">W · C · W · G</div>'),
    "word": (""".a{top:720px;font-family:Playfair,serif;font-style:italic;font-size:150px;line-height:1}
.b{top:900px;font-size:34px;font-weight:700;letter-spacing:.62em;padding-left:.62em}""",
             '<div class="c a">West Coast</div><div class="c b">WATCH GROUP</div>'),
    "line": (f".l{{position:absolute;top:1000px;left:390px;width:300px;height:1.5px;background:{GOLD}}}", '<div class="l"></div>'),
    "sub": (".c{top:1046px;font-size:25px;letter-spacing:.34em;padding-left:.34em;color:#cfcac0}",
            '<div class="c">PRIVATE VIEWINGS · SAN DIEGO</div>'),
    "cta": (f""".c{{top:1250px;font-family:Playfair,serif;font-style:italic;font-size:46px;color:#f4f1ea}}
.u{{display:inline-block;padding-bottom:10px;border-bottom:1.5px solid {GOLD}}}""",
            '<div class="c"><span class="u">Message us to arrange a viewing</span></div>'),
    "legal": (".c{top:1700px;font-size:20px;letter-spacing:.08em;color:#6f6c66}",
              '<div class="c">Independent dealer. Not affiliated with Rolex SA.</div>'),
}

def png(name, css, body):
    src = TMP / f"{name}.html"
    src.write_text(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{FONTS}{BASE}{css}</style></head><body>{body}</body></html>")
    out = TMP / f"{name}.png"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{H}",
                    "--default-background-color=00000000", "--virtual-time-budget=2000", f"--screenshot={out}", str(src)],
                   check=True, stderr=subprocess.DEVNULL)
    return out

files = {k: png(k, css, body) for k, (css, body) in LAYERS.items()}
# (capa, inicio del fundido, duración del fundido, desplazamiento vertical inicial en px)
ANIM = [("mono", 0.25, 0.7, 14), ("word", 0.45, 0.9, 22), ("sub", 1.35, 0.7, 10), ("cta", 1.75, 0.8, 12), ("legal", 2.1, 0.6, 0)]
ins = ["-f", "lavfi", "-i", f"color=black:s={W}x{H}:r=24:d={D}", "-loop", "1", "-t", str(D), "-i", str(files["bg"]),
       "-loop", "1", "-t", str(D), "-i", str(files["line"])]
for name, *_ in ANIM:
    ins += ["-loop", "1", "-t", str(D), "-i", str(files[name])]
f = [f"[1:v]format=rgba,fade=t=in:st=0:d=0.6:alpha=1[bg]", "[0:v][bg]overlay=0:0[v0]",
     # la línea dorada se dibuja del centro hacia afuera
     "[2:v]format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='alpha(X,Y)*lte(abs(X-540),min(150,max(0,(T-1.05)*210)))'[ln]",
     "[v0][ln]overlay=0:0[v1]"]
last = "v1"
for k, (name, st, d, dy) in enumerate(ANIM, 3):
    f.append(f"[{k}:v]format=rgba,fade=t=in:st={st}:d={d}:alpha=1[l{k}]")
    y = f"'{dy}*max(0,1-(t-{st})/{d})'" if dy else "0"
    f.append(f"[{last}][l{k}]overlay=x=0:y={y}:shortest=1[o{k}]"); last = f"o{k}"
# leve acercamiento continuo y grano fino de película
f.append(f"[{last}]scale=iw*1.04:ih*1.04,zoompan=z='1+0.025*on/({D}*24)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=24,"
         f"noise=alls=5:allf=t,format=yuv420p[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(f), "-map", "[v]", "-t", str(D),
                "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", str(OUT)], check=True)
print(OUT)
