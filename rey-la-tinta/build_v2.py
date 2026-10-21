# Genera los guiones de anuncios de Meta de Rey La Tinta (HTML -> PDF), mismo formato que el de Nate.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

ADS = [
    dict(title="No Sabes Qué Tatuarte", angle="Talking Head + B-roll · Tatuajes con significado", length="30-40 seg",
         hook="Nunca elijas tu tatuaje de un catálogo. Dime 3 cosas que te importan.",
         core=["Me llamo Rey, soy tatuador en Coral Springs, y casi nadie llega a mi estudio con el diseño listo. Llegan con algo que les importa.",
               "El nombre de un hijo. El lugar donde creciste. Una canción. Un animal que significa algo para ti.",
               "Con esas 3 cosas empiezo. Me cuentas la historia, hago el boceto y lo ajustamos juntos hasta que sea tuyo.",
               "Lo ves puesto en tu piel antes de empezar, y solo entonces lo tatuamos.",
               "Un catálogo te da el tatuaje de cualquiera. Esto te da uno que nadie más va a tener."],
         cta="Toca el botón y escríbeme por WhatsApp esas 3 cosas. Te digo qué haría con ellas, o te espero en el estudio en Coral Springs para hablarlo en persona.",
         note="A cámara en la mesa de dibujo. Muestra cada paso mientras lo dices: la charla con el cliente, el boceto a lápiz o en la tablet, el stencil puesto en la piel y el tatuaje terminado. Cierra con el cliente viendo su pieza por primera vez."),
    dict(title="La Foto Guardada En Tu Celular", angle="Talking Head + B-roll · Idea de referencia", length="30-40 seg",
         hook="¿Esa foto de tatuaje que guardaste en el celular? Ya la tiene otra persona. Haz esto.",
         core=["Una captura de Instagram, algo de Pinterest, un tatuaje que le viste a alguien. Si la copias tal cual, llevas el tatuaje de otro.",
               "Yo no la copio. La uso para entender lo que te gusta: el estilo, el tamaño, la zona.",
               "Después le agrego lo tuyo: una fecha, un detalle, algo de tu historia. Y la dibujo para tu cuerpo, no para el de otra persona.",
               "Te enseño el boceto, lo cambiamos las veces que haga falta y lo ves puesto antes de empezar.",
               "Esa foto deja de ser de otro y se convierte en tu tatuaje."],
         cta="Toca el botón y mándame esa foto por WhatsApp. O tráela al estudio en Coral Springs y la vemos juntos, sin compromiso.",
         note="Abre con el celular en la mano, pasando capturas de tatuajes. Después, pantalla dividida: la foto de referencia de un cliente a un lado y el tatuaje final que le hiciste al otro. Muestra 2 o 3 ejemplos así."),
    dict(title="Algún Día", angle="Talking Head · Ángulo decisión", length="30-40 seg",
         hook="¿Llevas 5 años con la misma idea de tatuaje? Te falta un paso que nadie te cuenta.",
         core=["La idea la tienes clara. Lo que falta es lo demás: con quién, cuánto, por dónde empezar. Y así pasan los años.",
               "El paso que falta no es sentarte en la silla. Es sentarte a hablar.",
               "Vienes al estudio, me cuentas la idea, ves mis trabajos de cerca y te explico cómo lo haríamos, cuánto tiempo lleva y dónde quedaría mejor.",
               "Sin presión. Si te convence, armamos el diseño juntos y separamos tu fecha.",
               "Cinco años pensándolo. Una conversación para empezar."],
         cta="Toca el botón, escríbeme por WhatsApp y te reservo un rato en el estudio en Coral Springs para que nos conozcamos.",
         note="A cámara, cercano, en el estudio. En «y así pasan los años», muestra el celular con una nota vieja que diga «tatuaje». Mientras explicas la visita, recorre el estudio: la entrada, la mesa de dibujo, el portafolio y la silla. Que se vea limpio y acogedor."),
]

def esc(s): return html.escape(s, quote=False)
N = len(ADS)
pages = []
for i, a in enumerate(ADS):
    core = "".join(f"<p>{esc(p)}</p>" for p in a["core"])
    pages.append(f'''<section class="page">
  <div class="eyebrow">REY LA TINTA · @REY_LATINTA</div>
  <div class="top"><span class="sc"><i></i>ANUNCIO {i+1} DE {N}</span><span class="tag">ANUNCIO PAGADO</span></div>
  <div class="vs">GUION DE ANUNCIO META</div>
  <h2>{esc(a["title"])}</h2>
  <div class="angle">{esc(a["angle"])}</div>
  <div class="facts">
    <div><span>FORMATO</span><b>{esc(a["angle"].split(" · ")[0])}</b></div>
    <div><span>DURACIÓN</span><b>{a["length"]}</b></div>
    <div><span>CANAL</span><b>Meta Ads (IG + FB)</b></div>
    <div><span>OBJETIVO</span><b class="kw">WhatsApp</b></div>
  </div>
  <div class="box"><div class="bh"><em>01</em>EL GANCHO</div><p class="hook">“{esc(a["hook"])}”</p></div>
  <div class="box"><div class="bh"><em>02</em>MENSAJE PRINCIPAL</div><div class="core">{core}</div></div>
  <div class="box cta"><div class="bh"><em>03</em>LLAMADO A LA ACCIÓN</div><p class="hook">“{esc(a["cta"])}”</p></div>
  <div class="box note"><div class="bh">NOTA DE DIRECCIÓN</div><p>{esc(a["note"])}</p></div>
  <div class="foot"><span>REY LA TINTA · GUION DE ANUNCIO META</span><span>{i+1:02d} / {N:02d}</span></div>
</section>''')

CSS = """
@page { size: letter; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0b0b0f; font-family: Inter, Arial, sans-serif; color: #f4f4f7; }
.page { width: 8.5in; height: 11in; padding: 0.62in 0.62in 0.6in; position: relative; overflow: hidden; break-after: page; background: #0b0b0f; }
.page:last-child { break-after: auto; }
.eyebrow { font-size: 8.2pt; font-weight: 700; letter-spacing: .1em; color: #5b7cfa; }
.foot { position: absolute; left: .62in; right: .62in; bottom: .42in; display: flex; justify-content: space-between; border-top: .75pt solid #1f1f27; padding-top: 10pt; font-size: 7.1pt; letter-spacing: .06em; color: #67666f; }
.tag { font-size: 7.3pt; font-weight: 700; letter-spacing: .1em; padding: 3pt 9pt; border-radius: 10pt; color: #facc15; background: rgba(250,204,21,.14); }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 16pt; }
.sc { font-size: 8.2pt; font-weight: 700; letter-spacing: .08em; color: #5b7cfa; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #5b7cfa; display: inline-block; }
.vs { font-size: 7.9pt; font-weight: 700; letter-spacing: .08em; color: #67666f; margin-top: 12pt; }
h2 { font-size: 20.2pt; font-weight: 800; margin-top: 4pt; line-height: 1.2; }
.angle { color: #a6a6b3; font-size: 10.1pt; margin-top: 4pt; }
.facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin-top: 14pt; }
.facts div { background: #131318; border: .75pt solid #22222b; border-radius: 6pt; padding: 10pt 10pt 12pt; }
.facts span { display: block; font-size: 7.1pt; letter-spacing: .06em; color: #67666f; margin-bottom: 8pt; }
.facts b { font-size: 9.6pt; font-weight: 700; }
.kw { color: #5b7cfa; font-weight: 700; }
.box { background: #131318; border: .75pt solid #22222b; border-radius: 7pt; padding: 12pt 13pt; margin-top: 9pt; }
.bh { font-size: 7.9pt; font-weight: 700; letter-spacing: .08em; color: #67666f; margin-bottom: 8pt; }
.bh em { font-style: normal; color: #5b7cfa; font-size: 9.8pt; margin-right: 7pt; }
.hook { font-size: 10.6pt; font-weight: 700; line-height: 1.45; }
.core p { font-size: 8.9pt; color: #a6a6b3; line-height: 1.75; }
.core p + p { margin-top: 5pt; }
.box.cta { background: #10142a; border-color: #2a3778; }
.box.note p { font-size: 8.2pt; color: #a6a6b3; font-style: italic; line-height: 1.7; }
"""

doc = f"<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><title>Rey La Tinta Meta Ad Scripts</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "ReyLaTinta_MetaAdScripts_v2.pdf"
subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
