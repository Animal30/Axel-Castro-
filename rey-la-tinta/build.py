# Genera el PDF con los guiones de anuncios de Rey La Tinta (HTML -> PDF).
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

ADS = [
    dict(tag="COVER-UP", color="#f59e0b", title="El tatuaje que escondes", angle="Ángulo: problema → solución",
         length="20–30 seg", why="El que más consultas suele generar: le habla a alguien con un problema que ya quiere resolver.",
         beats=[
             ("GANCHO · 0–3 SEG", "Primer plano de un tatuaje viejo, borroso o mal hecho → corte rápido al mismo brazo con el cover-up terminado.",
              "¿Tienes un tatuaje que escondes cada vez que te pones una camisa corta?"),
             ("MENSAJE", "Rey a cámara en el estudio. Intercalar 2 o 3 cover-ups suyos (antes → después).",
              "Un nombre que ya no va, algo que te hiciste a los 18, un trabajo mal hecho… Lo veo todas las semanas. Y casi siempre tiene solución. No lo tapamos por taparlo: lo convertimos en una pieza que vas a querer enseñar."),
             ("LLAMADO A LA ACCIÓN", "Rey señala a cámara. Texto en pantalla: «Mándame una foto».",
              "Mándame una foto de tu tatuaje por mensaje y te digo qué podemos hacer. Sin compromiso."),
         ],
         text="¿Tienes un tatuaje que ya no quieres ver? 👀\n\nNombres, errores de juventud, trabajos mal hechos… casi todo tiene solución.\n\nTransformo tatuajes viejos en piezas que vas a querer enseñar, con realismo en negro y gris y a color.\n\n📍 Florida\n📸 Mándame una foto de tu tatuaje y te digo qué podemos hacer, sin compromiso.",
         headline="Transformamos tu tatuaje viejo",
         note="El antes y después es el gancho: que se vea en el primer segundo, sin intro. Usar cover-ups reales de clientes, con su permiso."),
    dict(tag="EMOCIONAL", color="#a78bfa", title="No es un dibujo, es tu historia", angle="Ángulo: significado y conexión",
         length="25–35 seg", why="Conecta con su estilo (God First: Transformación, Mi Mundo Simbólico) y con el realismo de retratos que hace.",
         beats=[
             ("GANCHO · 0–3 SEG", "Cámara lenta: el cliente se ve el tatuaje terminado por primera vez en el espejo.",
              "Un tatuaje no es un dibujo. Es lo que no sabes decir con palabras."),
             ("MENSAJE", "Recorrido rápido por 4 o 5 piezas: retratos, la bandera, la tortuga a color.",
              "Un hijo, una madre que ya no está, de dónde vienes, lo que superaste… Cada persona que se sienta en mi silla trae una historia. Mi trabajo es escucharla y convertirla en algo que vas a llevar contigo toda la vida. Por eso no copio diseños: cada pieza se hace una sola vez."),
             ("LLAMADO A LA ACCIÓN", "Rey trabajando en el estudio. Texto en pantalla: «Agenda abierta».",
              "Cuéntame tu historia por mensaje y la diseñamos juntos. La agenda de este mes ya está abierta."),
         ],
         text="Un tatuaje no es un dibujo. Es tu historia. 🖤\n\nUn hijo. Una madre. Tu bandera. Lo que superaste.\n\nCada pieza que hago es única: diseño personalizado, realismo en negro y gris y a color, hecho para durar toda la vida.\n\n📍 Florida · Agenda abierta\n💬 Cuéntame tu idea por mensaje y la diseñamos juntos.",
         headline="Tu historia, hecha arte en tu piel",
         note="Tono tranquilo y cercano, voz baja. Música suave de fondo. La reacción real del cliente en el espejo vale más que cualquier frase."),
    dict(tag="AUTORIDAD", color="#f87171", title="El error de muchos", angle="Ángulo: educar y filtrar por calidad",
         length="25–35 seg", why="Sigue un formato que ya usa en su perfil y filtra a quien solo busca precio.",
         beats=[
             ("GANCHO · 0–3 SEG", "Rey a cámara, serio. Texto grande en pantalla: «ERROR DE MUCHOS».",
              "El error que comete casi todo el mundo antes de tatuarse… y del que se arrepiente después."),
             ("MENSAJE", "Cortes entre Rey hablando y primeros planos de detalle de sus trabajos (sombras, piel, ojos).",
              "Elegir por precio. Un tatuaje barato te sale caro: líneas que se abren, sombras que se pierden y, al final, pagar el doble para arreglarlo. Esto es para toda la vida. Fíjate en el detalle, en cómo se ven los trabajos ya sanados, en que el artista entienda lo que quieres."),
             ("LLAMADO A LA ACCIÓN", "Rey extiende la mano a cámara. Texto en pantalla: «Escríbeme».",
              "Si lo vas a hacer, hazlo bien desde la primera vez. Escríbeme y hablamos de tu idea."),
         ],
         text="El error de muchos: elegir su tatuaje por precio. ❌\n\nUn tatuaje barato sale caro: líneas que se abren, sombras que se pierden y pagar el doble para arreglarlo.\n\nEsto es para toda la vida. Hazlo bien desde la primera vez.\n\n✔️ Diseño personalizado\n✔️ Realismo en negro y gris y a color\n✔️ Higiene y materiales profesionales\n\n📍 Florida\n💬 Escríbeme y hablamos de tu idea.",
         headline="Hazlo bien desde la primera vez",
         note="Seguro, sin hablar mal de otros artistas. Mostrar trabajos ya sanados en los primeros planos: es la prueba de calidad."),
]

def esc(s): return html.escape(s, quote=False)
total = len(ADS) + 2
foot = lambda n: f'<div class="foot"><span>REY LA TINTA · GUIONES PARA ANUNCIOS</span><span>{n:02d} / {total:02d}</span></div>'
tag = lambda a: f'<span class="tag" style="color:{a["color"]};border-color:{a["color"]}55;background:{a["color"]}1f">{a["tag"]}</span>'

pages = []
rows = "".join(f'<div class="row"><span class="n">{i+1:02d}</span><span class="t">{esc(a["title"])}</span>{tag(a)}<span class="d">{a["length"]}</span></div>' for i, a in enumerate(ADS))
pages.append(f'''<section class="page cover">
  <div class="cv">
    <div class="eyebrow">REY LA TINTA · @REY_LATINTA</div>
    <h1>Guiones para Anuncios</h1>
    <p class="sub">3 anuncios listos para grabar y publicar en Meta.</p>
    <div class="meta">
      <p><b>OBJETIVO</b> — Mensajes por Instagram y WhatsApp</p>
      <p><b>PÚBLICO</b> — 21 a 45 años · 25–40 millas alrededor del estudio · Florida</p>
      <p><b>FORMATO</b> — Video vertical 9:16 · 20–35 seg · Reels, Stories y Feed</p>
    </div>
  </div>
  <div class="list"><div class="lh">ANUNCIOS EN ESTE DOCUMENTO</div>{rows}
    <div class="row"><span class="n">+</span><span class="t">Cómo configurar la campaña</span><span class="tag" style="color:#d4a24c;border-color:#d4a24c55;background:#d4a24c1f">GUÍA</span><span class="d"></span></div>
  </div>
  {foot(1)}
</section>''')

for i, a in enumerate(ADS):
    beats = "".join(f'''<div class="beat"><div class="bh"><em>{j+1:02d}</em>{esc(b[0])}</div>
      <div class="cols"><div><span class="lab">QUÉ SE VE</span><p>{esc(b[1])}</p></div>
      <div><span class="lab">QUÉ DICE REY</span><p class="say">“{esc(b[2])}”</p></div></div></div>''' for j, b in enumerate(a["beats"]))
    adtext = "<br>".join(esc(l) for l in a["text"].split("\n"))
    pages.append(f'''<section class="page">
  <div class="eyebrow">REY LA TINTA · @REY_LATINTA</div>
  <div class="top"><span class="sc"><i></i>ANUNCIO {i+1} DE {len(ADS)}</span>{tag(a)}</div>
  <h2>{esc(a["title"])}</h2>
  <div class="angle">{esc(a["angle"])} · {esc(a["why"])}</div>
  <div class="facts">
    <div><span>DURACIÓN</span><b>{a["length"]}</b></div>
    <div><span>FORMATO</span><b>Video vertical 9:16</b></div>
    <div><span>OBJETIVO</span><b>Mensajes</b></div>
    <div><span>BOTÓN</span><b class="gold">Enviar mensaje</b></div>
  </div>
  <div class="sect">GUION DEL VIDEO</div>
  {beats}
  <div class="two">
    <div class="box adtext"><div class="bh">TEXTO DEL ANUNCIO</div><p>{adtext}</p></div>
    <div class="side">
      <div class="box"><div class="bh">TÍTULO</div><p class="hl">{esc(a["headline"])}</p></div>
      <div class="box note"><div class="bh">NOTA DE GRABACIÓN</div><p>{esc(a["note"])}</p></div>
    </div>
  </div>
  {foot(i+2)}
</section>''')

pages.append(f'''<section class="page guide">
  <div class="eyebrow">REY LA TINTA · @REY_LATINTA</div>
  <div class="top"><span class="sc"><i></i>GUÍA</span></div>
  <h2>Cómo configurar la campaña</h2>
  <div class="angle">Para que los anuncios se conviertan en citas.</div>
  <div class="grid">
    <div class="box"><div class="bh"><em>01</em>CAMPAÑA</div><ul>
      <li><b>Objetivo: Mensajes</b> (Instagram + WhatsApp). En tatuajes, la conversación es la venta.</li>
      <li><b>Ubicación:</b> 25–40 millas alrededor del estudio.</li>
      <li><b>Edad:</b> 21 a 45 años, con Advantage+ activado.</li>
      <li><b>Ubicaciones:</b> Reels, Stories y Feed de Instagram y Facebook.</li>
      <li>En español, Meta lo muestra solo a quienes usan Facebook en ese idioma.</li></ul></div>
    <div class="box"><div class="bh"><em>02</em>PRUEBA</div><ul>
      <li>Publicar <b>los 3 anuncios a la vez</b>, en el mismo conjunto de anuncios.</li>
      <li>A los <b>4–5 días</b>, apagar el que tenga el costo por conversación más caro.</li>
      <li>Al ganador, darle más presupuesto poco a poco.</li></ul></div>
    <div class="box"><div class="bh"><em>03</em>RESPUESTAS AUTOMÁTICAS</div>
      <p class="q">“¡Gracias por escribir! ¿Qué te quieres tatuar?”</p>
      <p class="q">“¿En qué parte del cuerpo y de qué tamaño, más o menos?”</p>
      <p class="q">“¿Tienes una foto de referencia?”</p></div>
    <div class="box"><div class="bh"><em>04</em>CONVERTIR LA CONSULTA EN CITA</div><ul>
      <li>Responder <b>rápido</b>: idealmente en menos de 15 minutos.</li>
      <li>Con la idea, el lugar y el tamaño, dar el rango de precio y <b>ofrecer 2 fechas concretas</b>.</li>
      <li>Pedir el depósito para reservar.</li></ul></div>
    <div class="box wide"><div class="bh"><em>05</em>MATERIAL QUE MÁS VENDE</div><ul>
      <li><b>Tatuajes ya sanados</b>, no solo recién hechos: dan mucha más confianza.</li>
      <li><b>Reacciones reales</b> de clientes viendo su tatuaje terminado (con su permiso).</li>
      <li>Buena luz y piel limpia en los primeros planos: el detalle es lo que vende.</li></ul></div>
  </div>
  {foot(total)}
</section>''')

CSS = """
@page { size: letter; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0a0a0b; font-family: Inter, Arial, sans-serif, 'Noto Color Emoji'; color: #f5f3ef; }
.page { width: 8.5in; height: 11in; padding: .58in .6in .6in; position: relative; overflow: hidden; break-after: page; background: radial-gradient(ellipse at 100% 0%, #1d1608 0%, #0a0a0b 45%); }
.page:last-child { break-after: auto; }
.eyebrow { font-size: 8.2pt; font-weight: 700; letter-spacing: .12em; color: #d4a24c; }
.foot { position: absolute; left: .6in; right: .6in; bottom: .4in; display: flex; justify-content: space-between; border-top: .75pt solid #24221e; padding-top: 9pt; font-size: 7pt; letter-spacing: .08em; color: #6f6b64; }
.tag { font-size: 7.2pt; font-weight: 700; letter-spacing: .1em; padding: 3pt 9pt; border-radius: 10pt; border: .75pt solid; }
.cover .cv { text-align: center; margin-top: 1.5in; }
.cover h1 { font-size: 34pt; font-weight: 800; margin-top: 12pt; letter-spacing: -.01em; }
.cover .sub { color: #a8a39a; font-size: 10.5pt; margin-top: 8pt; }
.cover .meta { margin-top: 26pt; border-top: .75pt solid #24221e; border-bottom: .75pt solid #24221e; padding: 20pt 0; font-size: 8.8pt; color: #a8a39a; line-height: 2; }
.cover .meta b { color: #f5f3ef; }
.list { margin-top: 26pt; }
.lh { font-size: 7.6pt; font-weight: 700; letter-spacing: .12em; color: #d4a24c; margin-bottom: 6pt; }
.row { display: flex; align-items: center; gap: 10pt; padding: 9pt 0; border-bottom: .75pt solid #1c1b18; font-size: 9.6pt; }
.row .n { color: #d4a24c; font-weight: 700; width: 18pt; }
.row .t { flex: 1; }
.row .d { color: #8a857c; font-size: 8pt; width: 58pt; text-align: right; }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 14pt; }
.sc { font-size: 8.2pt; font-weight: 700; letter-spacing: .1em; color: #d4a24c; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #d4a24c; display: inline-block; }
h2 { font-size: 21pt; font-weight: 800; margin-top: 8pt; line-height: 1.2; }
.angle { color: #a8a39a; font-size: 8.8pt; margin-top: 4pt; line-height: 1.5; }
.facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin-top: 12pt; }
.facts div { background: #141312; border: .75pt solid #26241f; border-radius: 6pt; padding: 8pt 10pt 10pt; }
.facts span { display: block; font-size: 6.8pt; letter-spacing: .08em; color: #6f6b64; margin-bottom: 6pt; }
.facts b { font-size: 9.2pt; }
.gold { color: #d4a24c; }
.sect { font-size: 7.6pt; font-weight: 700; letter-spacing: .12em; color: #d4a24c; margin: 14pt 0 2pt; }
.beat, .box { background: #141312; border: .75pt solid #26241f; border-radius: 7pt; padding: 10pt 12pt; margin-top: 7pt; }
.bh { font-size: 7.6pt; font-weight: 700; letter-spacing: .09em; color: #6f6b64; margin-bottom: 6pt; }
.bh em { font-style: normal; color: #d4a24c; font-size: 9.4pt; margin-right: 7pt; }
.cols { display: grid; grid-template-columns: 1fr 1.55fr; gap: 14pt; }
.lab { display: block; font-size: 6.6pt; letter-spacing: .1em; color: #6f6b64; margin-bottom: 3pt; }
.cols p { font-size: 8.4pt; color: #a8a39a; line-height: 1.55; }
.cols p.say { color: #f5f3ef; font-weight: 600; font-size: 8.8pt; }
.two { display: grid; grid-template-columns: 1.25fr 1fr; gap: 9pt; }
.two .box { margin-top: 9pt; }
.adtext p { font-size: 8.3pt; color: #d9d5ce; line-height: 1.55; }
.side { display: flex; flex-direction: column; }
.hl { font-size: 10.5pt; font-weight: 700; }
.note p { font-size: 8pt; color: #a8a39a; font-style: italic; line-height: 1.6; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 9pt; margin-top: 14pt; }
.grid .box { margin-top: 0; padding: 12pt 13pt; }
.grid .wide { grid-column: 1 / -1; }
.grid ul { list-style: none; }
.grid li { font-size: 8.7pt; color: #a8a39a; line-height: 1.55; padding-left: 11pt; position: relative; margin-top: 4pt; }
.grid li::before { content: ""; position: absolute; left: 0; top: 6pt; width: 4pt; height: 4pt; border-radius: 50%; background: #d4a24c; }
.grid li b { color: #f5f3ef; }
.q { font-size: 9pt; font-weight: 600; margin-top: 6pt; padding: 7pt 10pt; background: #1b1915; border-radius: 6pt; border-left: 2pt solid #d4a24c; }
"""

doc = f"<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><title>Rey La Tinta · Guiones para Anuncios</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "ReyLaTinta_GuionesAnuncios.pdf"
subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
