# Carrusel 01 de la agencia: "5 errores que hacen que tus anuncios de Meta quemen plata".
# Genera 1080x1350 PNG por slide (Chrome headless) con la marca de Nahuel: naranja sobre negro, Inter + Playfair italic.
import base64, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[2]
FONTS_DIR = ROOT / ".claude/creator-profile/nahuel/assets/fonts"
CHROME = "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome"
HANDLE = "NAHUEL CASARTELLI · MARKETING"

def face(fam, file, w, style):
    b = base64.b64encode((FONTS_DIR / file).read_bytes()).decode()
    return f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{style};src:url(data:font/otf;base64,{b})}}"
FONTS = face("Inter", "Inter-Regular.otf", 400, "normal") + face("Inter", "Inter-Bold.otf", 700, "normal") + \
        face("Playfair", "PlayfairDisplay-Italic.ttf", 400, "italic")

# (tipo, título, cuerpo). En el título, *palabra* va en Playfair italic naranja.
SLIDES = [
    ("cover", "Tus anuncios están *quemando* plata", "5 errores que veo en casi todas las cuentas de Meta que reviso."),
    ("stake", "Antes de subir el presupuesto, *revisá esto.*", "Cada uno de estos errores se paga todos los días que el anuncio sigue prendido."),
    ("err", "Usás el botón *Promocionar*", "Promocionar optimiza para likes y alcance. Si querés mensajes o ventas, armá la campaña en el Administrador de anuncios con ese objetivo."),
    ("err", "Tenés *un solo* anuncio", "Meta decide a quién mostrarte según el creativo. Con uno solo no tiene nada para probar. Subí de 3 a 6 versiones con ganchos distintos."),
    ("err", "Segmentás *demasiado* fino", "\"Mujeres de 32 a 34 que aman el yoga en Miami\" le ata las manos al algoritmo. Abrí el público y dejá que el anuncio filtre."),
    ("err", "No tenés Píxel ni *API de conversiones*", "Si Meta no ve quién te compra o te escribe, optimiza a ciegas. Configurá los dos y verificá que los eventos lleguen."),
    ("err", "Lo tocás *todos* los días", "Cada cambio grande reinicia el aprendizaje. Dale una semana y unas 50 conversiones antes de decidir si funciona."),
    ("recap", "Guardalo y *revisá tu cuenta*", ["Nada de Promocionar: objetivo real", "De 3 a 6 anuncios distintos", "Público abierto", "Píxel + API de conversiones", "Una semana sin tocar"]),
    ("cta", "¿Querés que *revise* los tuyos?", "Comentá AUDIT y te digo cuál de los 5 te está costando más plata."),
]
N = len(SLIDES)

def title(t):
    parts = t.split("*")
    return "".join(f'<em>{p}</em>' if i % 2 else p for i, p in enumerate(parts))

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#050505;color:#f5f5f5;font-family:Inter,Arial,sans-serif;overflow:hidden}
.s{position:absolute;inset:0;padding:150px 120px 140px;display:flex;flex-direction:column}
.glow{position:absolute;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(255,122,26,.20),transparent 62%);right:-380px;top:-360px}
.top{display:flex;justify-content:space-between;font-size:26px;font-weight:700;letter-spacing:.14em;color:#8a8a8a}
.top b{color:#ff7a1a}
h1{font-weight:700;letter-spacing:-.02em;line-height:1.02}
h1 em{font-family:Playfair,Georgia,serif;font-style:italic;font-weight:400;color:#ff7a1a;letter-spacing:0}
.cover h1{font-size:132px;margin-top:auto}
.cover p{font-size:40px;color:#bdbdbd;line-height:1.4;margin-top:44px;max-width:780px}
.swipe{margin-top:70px;font-size:28px;font-weight:700;letter-spacing:.14em;color:#ff7a1a}
.mid h1{font-size:96px;margin-top:auto}
.mid p{font-size:40px;color:#c8c8c8;line-height:1.5;margin-top:48px;margin-bottom:auto}
.num{font-size:250px;font-weight:700;color:transparent;-webkit-text-stroke:3px #ff7a1a;line-height:1;margin-top:70px}
.err h1{font-size:84px;margin-top:30px}
.err p{font-size:38px;color:#c8c8c8;line-height:1.5;margin-top:44px}
.recap h1{font-size:80px;margin-top:60px}
.recap ol{list-style:none;margin-top:60px}
.recap li{font-size:40px;padding:26px 0;border-bottom:2px solid #1f1f1f;display:flex;gap:30px;align-items:baseline}
.recap li span{color:#ff7a1a;font-weight:700;font-size:34px}
.cta h1{font-size:104px;margin-top:auto}
.cta p{font-size:42px;color:#c8c8c8;line-height:1.45;margin-top:48px}
.kw{display:inline-block;margin-top:56px;margin-bottom:auto;padding:26px 54px;border-radius:999px;background:#ff7a1a;color:#050505;font-size:46px;font-weight:700;letter-spacing:.08em;align-self:flex-start}
.foot{position:absolute;left:120px;right:120px;bottom:80px;display:flex;justify-content:space-between;font-size:24px;letter-spacing:.12em;color:#5c5c5c;font-weight:700}
"""

out = HERE / "slides"; out.mkdir(exist_ok=True)
for i, (kind, t, body) in enumerate(SLIDES, 1):
    top = f'<div class="top"><span>META ADS</span><b>{i}/{N}</b></div>'
    if kind == "cover":
        inner = f'<h1>{title(t)}</h1><p>{body}</p><div class="swipe">DESLIZÁ →</div>'; cls = "cover"
    elif kind in ("stake",):
        inner = f'<h1>{title(t)}</h1><p>{body}</p>'; cls = "mid"
    elif kind == "err":
        inner = f'<div class="num">{i-2:02d}</div><h1>{title(t)}</h1><p>{body}</p>'; cls = "err"
    elif kind == "recap":
        lis = "".join(f"<li><span>{k:02d}</span>{x}</li>" for k, x in enumerate(body, 1))
        inner = f'<h1>{title(t)}</h1><ol>{lis}</ol>'; cls = "recap"
    else:
        inner = f'<h1>{title(t)}</h1><p>{body}</p><div class="kw">AUDIT</div>'; cls = "cta"
    html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{FONTS}{CSS}</style></head><body><div class='glow'></div><div class='s {cls}'>{top}{inner}</div><div class='foot'><span>{HANDLE}</span><span>{'GUARDALO' if kind=='recap' else ''}</span></div></body></html>"
    src = out / f"_s{i}.html"; src.write_text(html)
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--window-size=1080,1350",
                    "--virtual-time-budget=3000", f"--screenshot={out / f'slide-{i:02d}.png'}", str(src)], check=True, stderr=subprocess.DEVNULL)
    src.unlink()
print(out)
