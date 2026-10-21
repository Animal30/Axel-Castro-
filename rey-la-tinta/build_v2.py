# Genera los guiones de anuncios de Meta de Rey La Tinta (HTML -> PDF), mismo formato que el de Nate.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

ADS = [
    dict(title="Tu Primer Tatuaje", angle="Talking Head · Ángulo primer tatuaje", length="25-35 seg",
         hook="¿Nunca te has tatuado y te dan nervios? Te cuento exactamente lo que pasa en mi silla.",
         core=["Me llamo Rey, soy tatuador aquí en Florida, y casi todos los que llegan por primera vez me preguntan lo mismo: ¿cuánto duele?",
               "Menos de lo que te imaginas. Y nadie empieza sin saber lo que va a pasar.",
               "Primero hablamos de tu idea. Después te enseño el diseño y lo ves puesto en tu piel antes de empezar. Si algo no te convence, lo cambiamos.",
               "Paramos cuando lo necesites, y te vas con las instrucciones para que sane bien.",
               "Tu primer tatuaje tiene que ser una buena experiencia, no un mal recuerdo."],
         cta="Escríbeme por mensaje lo que tienes en mente, aunque todavía no lo tengas claro. Te contesto yo.",
         note="A cámara, cercano y con una sonrisa, como si le hablaras a un amigo nervioso. Mientras explicas los pasos, muestra en planos cortos: la charla con el cliente, el diseño en la pantalla, el stencil puesto en la piel y el cliente mirándose en el espejo."),
    dict(title="El Primer Día No Cuenta", angle="Talking Head + B-roll · Ángulo calidad", length="25-35 seg",
         hook="Cualquier tatuaje se ve bien el primer día. La prueba de verdad es cómo se ve un año después.",
         core=["Recién hecho, con la piel brillando y buena luz, casi todo parece perfecto.",
               "A los meses es cuando se nota: las líneas se abren, el negro se pone gris y el detalle se pierde.",
               "Por eso, antes de elegir artista, pídele fotos de trabajos sanados. No solo de los recién hechos.",
               "Estos son míos, meses después.",
               "Realismo en negro y gris y a color, pensado desde el principio para cómo va a sanar en tu piel."],
         cta="Mándame por mensaje tu idea y en qué parte la quieres, y te digo cómo la haría.",
         note="Abre con pantalla dividida: un tatuaje recién hecho a un lado y el mismo tatuaje sanado al otro (los dos tuyos). En «estos son míos, meses después», corta a 3 o 4 trabajos sanados con luz natural, sin filtros. Sin hablar mal de otros artistas."),
    dict(title="No Sabes Qué Tatuarte", angle="Talking Head · Ángulo diseño personalizado", length="20-30 seg",
         hook="¿Quieres tatuarte pero no sabes qué? Así empiezan muchos de mis mejores trabajos.",
         core=["Casi nadie llega con el diseño listo. Llegan con algo que les importa.",
               "El nombre de un hijo. El lugar donde creciste. Una canción. Un animal que significa algo para ti.",
               "Con eso tengo suficiente. Yo lo convierto en un diseño que nadie más va a tener.",
               "Nada de catálogo ni de copiar algo de Pinterest. Lo hacemos desde cero, contigo."],
         cta="Mándame por mensaje tres cosas que te importan y dónde lo quieres. Te digo qué haría con eso.",
         note="A cámara en la mesa de dibujo. Mientras nombras cada idea, muestra el boceto a lápiz convirtiéndose en el tatuaje terminado (time-lapse del diseño en la tablet si lo tienes). Termina con el cliente viendo su pieza por primera vez."),
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
pdf = HERE / "ReyLaTinta_MetaAdScripts_v2.pdf"
subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
