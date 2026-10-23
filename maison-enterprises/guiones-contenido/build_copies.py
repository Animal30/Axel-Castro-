# Genera el PDF de copies para grabar (guía de grabación + solo el texto a decir de cada guion), letra grande.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

from guiones import ADS

GUIDE = [
    ("CÁMARA", [
        "Celular en trípode, en <b>vertical (9:16)</b>, a la altura de los ojos y a un metro de distancia.",
        "Graba en <b>4K a 30 fps</b> con los fotogramas fijos (no en automático). Bloquea el enfoque y la exposición en tu cara.",
        "Encuadre: de la mitad del pecho hacia arriba, cabeza centrada y un poco de aire arriba. La edición te pone a veces en primer plano y a veces en un panel abajo, así que quédate en el centro del cuadro y no te acerques ni te alejes.",
    ]),
    ("LUZ Y FONDO", [
        "La luz siempre <b>delante tuyo</b>, un poco por encima de los ojos: una ventana o una luz suave. Nunca una ventana detrás.",
        "Fondo ordenado, a uno o dos metros detrás tuyo. Usa ropa de un color distinto al de la pared: la edición te recorta para que la cabeza salga por encima del panel, y el contraste hace que el recorte quede limpio.",
        "Ropa lisa, sin rayas finas ni logos grandes. Cambia de ropa cada dos guiones para que no parezca todo grabado el mismo día.",
    ]),
    ("AUDIO", [
        "Es lo más importante. Usa un <b>micrófono de solapa</b> (inalámbrico o con cable al celular).",
        "Graba en un cuarto con muebles o cortinas para que no haya eco. Apaga el aire acondicionado y el ventilador.",
    ]),
    ("CÓMO GRABAR LAS TOMAS", [
        "<b>Un archivo por guion.</b> Dale a grabar, di el guion completo y corta al final. No pares la grabación entre frases.",
        "Ve <b>párrafo por párrafo</b>: lee el bloque, mira a la lente y dilo. Los silencios entre bloques los quito en la edición.",
        "Si te equivocas, haz una pausa de dos segundos y <b>repite la frase entera desde el principio</b>. En la edición me quedo con la última toma completa.",
        "Graba el <b>gancho tres veces seguidas</b>, con energía distinta cada vez. Elijo el mejor.",
        "Habla a la lente, no a la pantalla, con un poco más de energía de lo normal. Cuando digas «paso uno, dos, tres», marca los números con la mano.",
        "Las frases con números (1%, 25%, 30 contra 40 dólares) dilas más despacio: ahí entran las animaciones.",
        "Antes de pasar al siguiente guion, mira 10 segundos de la toma con auriculares para revisar audio y foco.",
    ]),
    ("EDICIÓN", [
        "Plantilla recomendada: <b>Glass Explainer Reel</b>. Alterna primeros planos con un panel donde apareces abajo y arriba se arman las animaciones de cada paso, con capturas reales y números. No necesita B-roll.",
    ]),
]

def esc(s): return html.escape(s, quote=False)
N = len(ADS)

guide = "".join(f'<div class="gs"><h3>{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></div>' for t, items in GUIDE)
pages = [f'''<section class="page">
  <div class="eyebrow">MAISON ENTERPRISES · MARKETING CON IA</div>
  <h1>Guía de grabación</h1>
  <div class="sub">Talking head · 6 guiones · Formato vertical para Reels, TikTok y anuncios de Meta</div>
  {guide}
  <div class="foot"><span>MAISON ENTERPRISES · COPIES PARA GRABAR</span><span>GUÍA</span></div>
</section>''']

for i, a in enumerate(ADS):
    cta_html = esc(a["cta"]).replace(a["kw"], '<span class="kw">' + a["kw"] + '</span>', 1)
    core = "".join(f"<p>{esc(p)}</p>" for p in a["core"])
    pages.append(f'''<section class="page">
  <div class="eyebrow">MAISON ENTERPRISES · MARKETING CON IA</div>
  <div class="top"><span class="sc"><i></i>GUION {i+1} DE {N}</span><span class="tag">{a["length"]} · {esc(a["pillar"])}</span></div>
  <h2>{esc(a["title"])}</h2>
  <div class="lbl">GANCHO · GRÁBALO 3 VECES</div>
  <p class="hook">{esc(a["hook"])}</p>
  <div class="lbl">MENSAJE</div>
  <div class="core">{core}</div>
  <div class="lbl">CIERRE</div>
  <p class="cta">{cta_html}</p>
  <div class="foot"><span>MAISON ENTERPRISES · COPIES PARA GRABAR</span><span>{i+1:02d} / {N:02d}</span></div>
</section>''')

CSS = """
@page { size: letter; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0b0b0d; font-family: Inter, Arial, sans-serif; color: #f5f3ef; }
.page { width: 8.5in; height: 11in; padding: 0.6in 0.65in 0.6in; position: relative; overflow: hidden; break-after: page; background: #0b0b0d; }
.page:last-child { break-after: auto; }
.eyebrow { font-size: 8.2pt; font-weight: 700; letter-spacing: .12em; color: #d4b06a; }
.foot { position: absolute; left: .65in; right: .65in; bottom: .42in; display: flex; justify-content: space-between; border-top: .75pt solid #22201c; padding-top: 10pt; font-size: 7.1pt; letter-spacing: .06em; color: #6c6860; }
h1 { font-size: 26pt; font-weight: 800; margin-top: 16pt; }
.sub { color: #aaa69d; font-size: 10pt; margin-top: 4pt; margin-bottom: 6pt; }
.gs { background: #141311; border: .75pt solid #26231e; border-radius: 7pt; padding: 10pt 13pt; margin-top: 8pt; }
.gs h3 { font-size: 7.9pt; font-weight: 700; letter-spacing: .08em; color: #d4b06a; margin-bottom: 5pt; }
.gs ul { padding-left: 12pt; }
.gs li { font-size: 8.7pt; color: #aaa69d; line-height: 1.55; margin-top: 2.5pt; }
.gs li b { color: #f5f3ef; }
.gs:last-of-type { background: #1a160e; border-color: #4a3d22; }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 15pt; }
.sc { font-size: 8.2pt; font-weight: 700; letter-spacing: .08em; color: #d4b06a; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #d4b06a; display: inline-block; }
.tag { font-size: 7.3pt; font-weight: 700; letter-spacing: .1em; padding: 3pt 9pt; border-radius: 10pt; color: #f5f3ef; background: rgba(212,176,106,.16); text-transform: uppercase; }
h2 { font-size: 22pt; font-weight: 800; margin-top: 8pt; line-height: 1.2; }
.lbl { font-size: 7.6pt; font-weight: 700; letter-spacing: .1em; color: #6c6860; margin-top: 18pt; margin-bottom: 6pt; }
.hook { font-size: 17pt; font-weight: 700; line-height: 1.4; color: #f5f3ef; }
.core p { font-size: 13.2pt; line-height: 1.5; color: #dcd8cf; }
.core p + p { margin-top: 9pt; }
.cta { font-size: 14.5pt; font-weight: 700; line-height: 1.45; padding: 12pt 14pt; background: #1a160e; border: .75pt solid #4a3d22; border-radius: 7pt; }
.kw { color: #d4b06a; }
"""

doc = f"<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><title>Maison Enterprises Copies</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp_copies.html"; src.write_text(doc)
pdf = HERE / "MaisonEnterprises_Copies_Para_Grabar.pdf"
subprocess.run(["/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
