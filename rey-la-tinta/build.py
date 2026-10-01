# Genera los guiones de anuncios de Meta de Rey La Tinta (HTML -> PDF), mismo formato que el de Nate.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

ADS = [
    dict(title="El Tatuaje Que Escondes", angle="Talking Head · Ángulo cover-up", length="20-30 seg",
         hook="¿Tienes un tatuaje que escondes cada vez que te pones una camisa corta?",
         core=["Me llamo Rey, y soy tatuador aquí en Florida.",
               "Un nombre que ya no va. Algo que te hiciste a los 18. Un trabajo mal hecho.",
               "Lo veo todas las semanas, y casi siempre tiene solución.",
               "No lo tapamos por taparlo. Lo convertimos en una pieza que vas a querer enseñar.",
               "Realismo en negro y gris y a color, diseñado para tu piel y para lo que ya tienes."],
         cta="Mándame una foto de tu tatuaje por mensaje y te digo qué podemos hacer. Sin compromiso.",
         note="Abre con el tatuaje viejo en primer plano y corta rápido al cover-up terminado: el antes y después es el gancho, tiene que verse en el primer segundo. Después, a cámara en el estudio, seguro y tranquilo. Intercala 2 o 3 cover-ups reales."),
    dict(title="No Es Un Dibujo, Es Tu Historia", angle="Talking Head + B-roll · Ángulo emocional", length="25-35 seg",
         hook="Un tatuaje no es un dibujo. Es lo que no sabes decir con palabras.",
         core=["Me llamo Rey.",
               "Un hijo. Una madre que ya no está. De dónde vienes. Lo que superaste.",
               "Cada persona que se sienta en mi silla trae una historia.",
               "Mi trabajo es escucharla y convertirla en algo que vas a llevar contigo toda la vida.",
               "Por eso no copio diseños. Cada pieza se hace una sola vez."],
         cta="Cuéntame tu historia por mensaje y la diseñamos juntos. La agenda de este mes ya está abierta.",
         note="Abre en cámara lenta con un cliente viéndose el tatuaje terminado en el espejo. Voz baja y cercana, sin prisa. Mientras hablas, muestra 4 o 5 piezas: retratos, la bandera, la tortuga a color. Música suave de fondo."),
    dict(title="El Error De Muchos", angle="Talking Head · Ángulo autoridad", length="25-35 seg",
         hook="El error que comete casi todo el mundo antes de tatuarse… y del que se arrepiente después.",
         core=["Elegir por precio.",
               "Un tatuaje barato te sale caro: líneas que se abren, sombras que se pierden y, al final, pagar el doble para arreglarlo.",
               "Me llamo Rey, soy tatuador aquí en Florida, y esto es para toda la vida.",
               "Fíjate en el detalle. En cómo se ven los trabajos ya sanados. En que el artista entienda lo que quieres.",
               "Diseño personalizado, realismo en negro y gris y a color, y materiales profesionales."],
         cta="Si lo vas a hacer, hazlo bien desde la primera vez. Escríbeme y hablamos de tu idea.",
         note="A cámara, serio, a la altura de los ojos, con «ERROR DE MUCHOS» grande en pantalla. Haz una pausa después de «elegir por precio». Intercala primeros planos de trabajos sanados. Seguro, sin hablar mal de otros artistas."),
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
    <div><span>OBJETIVO</span><b class="kw">Mensajes</b></div>
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
pdf = HERE / "ReyLaTinta_MetaAdScripts.pdf"
subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
