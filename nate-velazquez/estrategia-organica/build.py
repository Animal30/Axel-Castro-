# Genera el PDF de estrategia de contenido orgánico de Nate (HTML -> PDF), mismo estilo que el calendario.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
e = lambda s: html.escape(s, quote=False)

PAGES = []
def page(body):
    PAGES.append(body)

def head(n, title, sub):
    return f'''<div class="eyebrow">NATE VELAZQUEZ · ESTRATEGIA ORGÁNICA</div>
  <div class="top"><span class="sc"><i></i>SECCIÓN {n}</span></div>
  <h2>{title}</h2><div class="angle">{sub}</div>'''

# ---------- 1. Portada ----------
page(f'''<section class="page cover">
  <div class="cv">
    <div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
    <h1>Estrategia de<br>Contenido Orgánico</h1>
    <p class="sub">Basada en lo que funciona en la competencia, con números.</p>
  </div>
  <div class="box summary"><div class="bh">RESUMEN EN 30 SEGUNDOS</div>
    <ol>
      <li><b>Analizamos 10 cuentas</b> de nutrición y fitness en tres niveles: competencia directa, cuentas vecinas y cuentas grandes (solo para copiar formatos).</li>
      <li><b>Cinco formatos explican casi todo lo que funciona:</b> experimento visual, opinión anti-dieta, reacción a tendencias, vida real y educación rápida.</li>
      <li><b>Instagram hoy premia</b> que vean el video completo y que lo manden por mensaje. Eso pesa 3 a 5 veces más que los likes.</li>
      <li><b>La meta de Nate:</b> pasar de ~580 vistas por Reel (lo normal para su tamaño) a 1.500 o más, y repetir cada formato que rinda 3 veces su promedio.</li>
      <li><b>El plan:</b> 5 Reels por semana, historias todos los días y 1 carrusel, con un sistema simple para medir y ajustar cada domingo.</li>
    </ol>
  </div>
  <div class="foot"><span>NATE VELAZQUEZ · ESTRATEGIA ORGÁNICA</span><span>01 / 08</span></div>
</section>''')

# ---------- 2. Método ----------
page(f'''<section class="page">
  {head("01", "Cómo hicimos el análisis", "Qué miramos, de dónde salen los números y qué no pudimos ver.")}
  <div class="grid2">
    <div class="box"><div class="bh"><em>01</em>LA MÉTRICA QUE IMPORTA</div>
      <p>No comparamos vistas totales: una cuenta de 4 millones con 400.000 vistas tuvo un día normal; una de 30.000 con 400.000 vistas encontró algo.</p>
      <p>Por eso medimos <b>cuánto rinde cada video contra el promedio de su propia cuenta</b> ("múltiplo"). Más de 3 veces su promedio = formato ganador que vale la pena copiar.</p></div>
    <div class="box"><div class="bh"><em>02</em>LAS TRES CAPAS DE COMPETENCIA</div>
      <p><b>Directa</b> (3): mismo público y oferta, hasta 10 veces el tamaño de Nate. De acá sale el tono y la oferta.</p>
      <p><b>Vecina</b> (3): otro nicho, mismo público. De acá salen formatos que todavía nadie usa en el nicho de Nate.</p>
      <p><b>Grande</b> (4): solo para copiar estructuras y formatos, nunca frecuencia ni tono.</p></div>
  </div>
  <div class="box"><div class="bh"><em>03</em>DE DÓNDE SALEN LOS NÚMEROS</div>
    <p>Bases públicas de analítica de influencers (HypeAuditor, CreatorDB, Social Blade, Modash, Socialveins) y estudios de 2026 sobre Reels (Supgrowth, Socialinsider, Metricool, SocialPilot), consultados en septiembre/octubre de 2026. Los números de seguidores cambian todos los días: se usan como orden de magnitud, no como dato exacto.</p></div>
  <div class="box note"><div class="bh">LIMITACIÓN IMPORTANTE</div>
    <p>Desde este entorno Instagram y YouTube están bloqueados, así que no pudimos medir video por video. El siguiente paso (sección 07) es completar el análisis con capturas de los Reels de estas cuentas y con las estadísticas reales de Nate. Con eso el plan pasa de "lo que funciona en el nicho" a "lo que funciona para Nate".</p></div>
  <div class="stats">
    <div><b>~580</b><span>vistas promedio por Reel en cuentas de 1.000–5.000 seguidores</span></div>
    <div><b>1.000</b><span>vistas promedio en cuentas de 5.000–10.000</span></div>
    <div><b>8,5 s</b><span>tiempo promedio que se mira un Reel en 2026</span></div>
    <div><b>3–5×</b><span>lo que pesa un envío por mensaje frente a un like</span></div>
  </div>
  <div class="foot"><span>NATE VELAZQUEZ · ESTRATEGIA ORGÁNICA</span><span>02 / 08</span></div>
</section>''')

# ---------- 3. Competencia ----------
ROWS = [
  ("DIRECTA", "#4ade80", "Kelli Fras", "@rootedlifewellness", "~31K", "Coach de nutrición: mujeres 30+ que dejan las dietas y disfrutan comida real", "Mismo mensaje que Nate. Ver qué ganchos usa para \"dejar de hacer dieta\""),
  ("DIRECTA", "#4ade80", "Mario Tomic", "@mariotomich", "~24K IG · 470K YouTube", "Fitness y nutrición para emprendedores y profesionales ocupados", "El mismo avatar que Nate. Cómo habla de falta de tiempo sin sonar a excusa"),
  ("DIRECTA", "#4ade80", "Laura Thomas, PhD", "@laurathomasnutrition", "~22K", "Nutrición sin dietas, alimentación intuitiva", "Opiniones fuertes contra la cultura de la dieta"),
  ("VECINA", "#60a5fa", "Abbey Sharp (dietista)", "@abbeyskitchen", "180K+", "\"Dietitian reviews\": reacciona a videos de \"what I eat in a day\"", "El formato reacción: aprovecha videos virales ajenos para educar"),
  ("VECINA", "#60a5fa", "Stephanie Kay", "@stephaniekaynutrition", "~121K", "Nutricionista: tips y recetas", "Recetas rápidas con un dato útil = guardados"),
  ("VECINA", "#60a5fa", "Mike Matthews", "@muscleforlifefitness", "~128K", "Fitness basado en evidencia para adultos 30/40+", "Cómo explica ciencia en simple a un público mayor"),
  ("GRANDE", "#facc15", "Will Tennyson", "@willtenny", "~1M · 176K vistas prom.", "Experimentos y desafíos con comida, humor", "Experimentos visuales. 176K vistas promedio ≈ 17% de sus seguidores"),
  ("GRANDE", "#facc15", "Adrian Preuss", "@nourishherbody", "~845K · 1,6M plays prom.", "Científico de nutrición, educación con base científica", "1,6M plays promedio ≈ 1,9× sus seguidores, 15% de engagement: lo más fuerte de la lista"),
  ("GRANDE", "#facc15", "Jordan Syatt", "@syattfitness", "~1,1M", "Pérdida de grasa sostenible, sin vueltas", "Opiniones directas y \"no tenés que dejar los carbohidratos\""),
  ("GRANDE", "#facc15", "Jeff Nippard", "@jeffnippard", "~4,1M · 3,15% eng.", "Ciencia del entrenamiento y la nutrición", "Solo formato: datos + gráficos simples en pantalla"),
]
rows = "".join(f'''<tr><td><span class="tag" style="color:{c};background:{c}22">{t}</span></td><td><b>{e(n)}</b><br><span class="h">{e(h)}</span></td><td class="num">{e(f)}</td><td>{e(w)}</td><td>{e(x)}</td></tr>''' for t,c,n,h,f,w,x in ROWS)
page(f'''<section class="page">
  {head("02", "La competencia, en números", "Diez cuentas en tres niveles. Lo que importa es qué copiar de cada una.")}
  <table class="tbl"><thead><tr><th>Nivel</th><th>Cuenta</th><th>Tamaño</th><th>Qué hace</th><th>Qué le copiamos</th></tr></thead><tbody>{rows}</tbody></table>
  <div class="box note"><div class="bh">LECTURA RÁPIDA</div>
    <p>Las cuentas grandes que más rinden en proporción (Preuss, Tennyson) no son las que dan "tips": son las que <b>muestran algo</b> (un experimento, un dato visual, una comparación). Las directas, del tamaño de Nate, ganan con <b>opinión y postura</b> contra las dietas. La estrategia combina las dos cosas.</p></div>
  <div class="foot"><span>NATE VELAZQUEZ · ESTRATEGIA ORGÁNICA</span><span>03 / 08</span></div>
</section>''')

# ---------- 4. Qué funciona ----------
FMT = [
  ("01", "EXPERIMENTO VISUAL", "Will Tennyson, Adrian Preuss", "Se entiende sin sonido (la mayoría mira en silencio), se mira hasta el final para ver el resultado y se manda por mensaje: \"mirá esto\". Es exactamente lo que el algoritmo premia más.", "Mismas calorías, dos platos · La cucharada de mantequilla de maní · Lo que tiene de verdad un batido \"saludable\""),
  ("02", "OPINIÓN ANTI-DIETA", "Jordan Syatt, Laura Thomas, Kelli Fras", "Genera comentarios (gente a favor y en contra) y posiciona a Nate como alguien con criterio, no como otro coach más. Es su diferencial: \"sin dietas restrictivas\".", "\"Eat clean\" es el peor consejo · No hace falta dejar los carbohidratos · Por qué \"guilt-free\" es una trampa"),
  ("03", "REACCIÓN A TENDENCIAS", "Abbey Sharp", "Usa videos que ya se están viralizando: el público ya existe, Nate solo agrega su mirada. Es el formato más barato de producir.", "Coach reacciona a \"what I eat in a day\" de 800 calorías · A la última dieta de moda · A un mito viral"),
  ("04", "VIDA REAL", "Abbey Sharp (\"random day as a busy dietitian\")", "La gente está cansada del día perfecto. Mostrar un día ocupado y real genera identificación y seguidores: \"él es como yo\".", "Lo que como en un mal día · Mi almuerzo en 5 minutos · Qué pido en la estación de servicio"),
  ("05", "EDUCACIÓN EN 20 SEGUNDOS", "Jeff Nippard, Mike Matthews, Stephanie Kay", "Un solo dato útil, con texto en pantalla, que la gente guarda para después. Los guardados le dicen a Instagram que el contenido tiene valor duradero.", "3 desayunos con 30 g de proteína · El error de pesarte después de un viaje · Cómo leer una etiqueta en 10 segundos"),
]
cards = "".join(f'''<div class="box fmt"><div class="bh"><em>{n}</em>{t}</div>
  <p class="ref">Lo hacen: {e(r)}</p><p><b>Por qué funciona:</b> {e(w)}</p><p class="ex"><b>Para Nate:</b> {e(x)}</p></div>''' for n,t,r,w,x in FMT)
page(f'''<section class="page">
  {head("03", "Los 5 formatos que funcionan", "Lo que tienen en común los videos que más rinden en el nicho, y por qué.")}
  {cards}
  <div class="foot"><span>NATE VELAZQUEZ · ESTRATEGIA ORGÁNICA</span><span>04 / 08</span></div>
</section>''')

# ---------- 5. Algoritmo + reglas ----------
page(f'''<section class="page">
  {head("04", "Cómo decide Instagram a quién mostrarle un Reel", "Las reglas de 2026, en orden de importancia, y qué significan para cada video de Nate.")}
  <div class="rank">
    <div><b>1</b><div><h4>Que lo miren hasta el final</h4><p>El tiempo de visualización sigue siendo la señal más fuerte, y los primeros segundos pesan más que el resto. <b>Regla:</b> el gancho dice o muestra el tema en menos de 2 segundos. Nada de "hola, hoy les quiero hablar de…".</p></div></div>
    <div><b>2</b><div><h4>Que lo manden por mensaje</h4><p>Los envíos por mensaje pesan 3 a 5 veces más que un like para llegar a gente que no te sigue. <b>Regla:</b> cada video tiene que tener un motivo para mandárselo a alguien ("esto sos vos", "mirá este dato").</p></div></div>
    <div><b>3</b><div><h4>Que lo guarden</h4><p>En fitness y nutrición los guardados son la señal más fuerte de valor duradero. <b>Regla:</b> los educativos llevan el dato escrito en pantalla, para que valga la pena guardarlo.</p></div></div>
    <div><b>4</b><div><h4>La duración justa</h4><p>Entre 7 y 30 segundos se logra la mayor tasa de videos vistos completos. Las historias y tutoriales funcionan mejor entre 30 y 90. <b>Regla:</b> 20–35 segundos por defecto; más largo solo si cuenta una historia.</p></div></div>
    <div><b>5</b><div><h4>Que sea original</h4><p>Instagram baja el alcance del contenido reciclado o con marca de agua de otra app. <b>Regla:</b> se copia la estructura, nunca el video. Nada con logo de TikTok.</p></div></div>
  </div>
  <div class="box note"><div class="bh">QUÉ SIGNIFICA PARA NATE</div>
    <p>Con 3.200 seguidores, lo normal es ~580 vistas por Reel. Las cuentas chicas llegan proporcionalmente a más gente que las grandes: un buen gancho puede multiplicar eso varias veces. No hace falta tener más seguidores para llegar lejos; hace falta que la gente mire hasta el final y lo comparta.</p></div>
  <div class="foot"><span>NATE VELAZQUEZ · ESTRATEGIA ORGÁNICA</span><span>05 / 08</span></div>
</section>''')

# ---------- 6. La estrategia ----------
PIL = [("ALCANCE", "40%", "#60a5fa", "Experimentos visuales y reacciones", "Traer gente nueva que no conoce a Nate"),
       ("POSTURA", "25%", "#f87171", "Opiniones anti-dieta", "Que lo recuerden y lo elijan por cómo piensa"),
       ("CONFIANZA", "20%", "#4ade80", "Vida real y resultados de clientes", "Que lo vean como alguien real y que funciona"),
       ("VENTA", "15%", "#facc15", "Cómo es trabajar con él, a quién no acepta", "Convertir seguidores en conversaciones por mensaje")]
pil = "".join(f'<div class="pil"><span class="pct" style="color:{c}">{p}</span><h4 style="color:{c}">{n}</h4><p><b>{e(f)}</b></p><p>{e(o)}</p></div>' for n,p,c,f,o in PIL)
page(f'''<section class="page">
  {head("05", "La estrategia para Nate", "Cuatro pilares, cuánto de cada uno y cómo se conectan con la venta.")}
  <div class="pils">{pil}</div>
  <div class="grid2">
    <div class="box"><div class="bh"><em>01</em>FRECUENCIA</div><ul>
      <li><b>5 Reels por semana</b> (lunes a viernes, o 7 si puede).</li>
      <li><b>Historias todos los días</b>: 3 a 5, con una encuesta o caja de preguntas.</li>
      <li><b>1 carrusel por semana</b>: el dato educativo que más guardados tuvo, ampliado.</li></ul></div>
    <div class="box"><div class="bh"><em>02</em>CÓMO SE CONVIERTE EN CLIENTES</div><ul>
      <li>Los Reels de alcance traen seguidores. <b>No llevan pedido de venta.</b></li>
      <li>Las historias invitan a escribir ("respondé con FIT").</li>
      <li>1 video por semana de venta suave, con palabra clave por mensaje.</li>
      <li>El perfil (fijados, bio, destacados) termina de convencer.</li></ul></div>
  </div>
  <div class="box"><div class="bh"><em>03</em>REGLAS DE CADA VIDEO</div>
    <div class="rules">
      <p><b>Gancho en menos de 2 s</b>, con texto en pantalla de 3–5 palabras.</p>
      <p><b>Subtítulos siempre.</b> La mayoría mira sin sonido.</p>
      <p><b>Un solo mensaje</b> por video.</p>
      <p><b>Final que vuelve al inicio</b>, para que lo miren dos veces.</p>
      <p><b>Portada con texto</b>, para que la grilla se entienda.</p>
      <p><b>Caption con la frase clave</b> en las primeras 125 letras.</p></div></div>
  <div class="foot"><span>NATE VELAZQUEZ · ESTRATEGIA ORGÁNICA</span><span>06 / 08</span></div>
</section>''')

# ---------- 7. Plan 4 semanas ----------
W = [
 ("SEMANA 1", "Calendario ya entregado", ["Mismas calorías, dos platos", "\"Eat clean\" es el peor consejo", "Lo que como en un mal día", "La cucharada de mantequilla de maní", "La voz de la dieta vs. tu coach", "Cosas que nunca hago", "A quién no acepto (venta)"]),
 ("SEMANA 2", "Nuevas ideas", ["El batido \"saludable\" que tiene más calorías que una hamburguesa", "Reacción: \"what I eat in a day\" de 900 calorías", "Por qué \"guilt-free\" es una trampa", "Mi almuerzo en 5 minutos entre reuniones", "El error de pesarte el lunes después de un fin de semana"]),
 ("SEMANA 3", "Nuevas ideas", ["Lo que pedí en Chipotle / Starbucks, como coach", "Reacción a la dieta de moda del mes", "No necesitás fuerza de voluntad, necesitás una heladera distinta", "Lo que comí en un viaje de trabajo", "Cómo es trabajar conmigo, semana por semana (venta)"]),
 ("SEMANA 4", "Nuevas ideas", ["Le di a mi cliente su comida favorita todos los días: esto pasó (caso real)", "3 desayunos con 30 g de proteína en menos de 3 minutos", "Lo que nadie te dice del \"cheat day\"", "Respondo comentarios de la semana", "Mito o verdad con comida real sobre la mesa"]),
]
wk = "".join(f'<div class="box wk"><div class="bh"><em>{n}</em>{e(s).upper()}</div><ol>' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ol></div>" for n,s,items in W)
page(f'''<section class="page">
  {head("06", "Plan de 4 semanas", "La semana 1 es el calendario ya entregado. Las siguientes son ideas para guionar con el mismo método.")}
  <div class="grid2 wks">{wk}</div>
  <div class="box note"><div class="bh">CÓMO SE ARMA CADA SEMANA</div>
    <p>Cada semana mezcla los 4 pilares: 2 de alcance, 1 de postura, 1 de confianza y 1 de venta suave. Las ideas de las semanas 2 a 4 se guionan en detalle (gancho, desarrollo, final y nota de grabación) igual que el calendario actual, y se ajustan según lo que muestren los números de la semana anterior.</p></div>
  <div class="foot"><span>NATE VELAZQUEZ · ESTRATEGIA ORGÁNICA</span><span>07 / 08</span></div>
</section>''')

# ---------- 8. Medición + próximos pasos ----------
page(f'''<section class="page">
  {head("07", "Cómo medimos y ajustamos", "Un sistema de 15 minutos por semana para saber qué repetir y qué dejar de hacer.")}
  <table class="tbl"><thead><tr><th>Métrica</th><th>Qué dice</th><th>Meta para Nate</th></tr></thead><tbody>
    <tr><td><b>Vistas vs. su promedio</b></td><td>Si el video funcionó para su cuenta</td><td class="num">Repetir todo formato que rinda 3× su promedio</td></tr>
    <tr><td><b>Envíos por mensaje</b></td><td>Si llega a gente nueva</td><td class="num">1 envío cada 100 vistas</td></tr>
    <tr><td><b>Guardados</b></td><td>Si tiene valor duradero</td><td class="num">1–2 cada 100 vistas en educativos</td></tr>
    <tr><td><b>Retención a los 3 s</b></td><td>Si el gancho funciona</td><td class="num">60% o más</td></tr>
    <tr><td><b>Seguidores por video</b></td><td>Si el perfil convence</td><td class="num">Crecer semana a semana</td></tr>
    <tr><td><b>Mensajes con palabra clave</b></td><td>Si el contenido vende</td><td class="num">5+ por semana</td></tr>
  </tbody></table>
  <div class="grid2">
    <div class="box"><div class="bh"><em>01</em>CADA DOMINGO</div><ul>
      <li>Nate manda captura de las estadísticas de los Reels de la semana.</li>
      <li>Ordenamos por rendimiento contra su promedio.</li>
      <li>El formato ganador se repite la semana siguiente con otro tema.</li>
      <li>El que rindió menos de la mitad del promedio se deja de hacer.</li></ul></div>
    <div class="box"><div class="bh"><em>02</em>PRÓXIMOS PASOS</div><ul>
      <li><b>Arreglar el perfil</b> (ya entregado): fijados, bio, grilla.</li>
      <li><b>Pasar las estadísticas</b> de sus últimos 15 Reels para calcular su promedio real.</li>
      <li><b>Capturas de 10–12 Reels</b> de las cuentas directas y vecinas, con vistas, para afinar los ganchos.</li>
      <li><b>Guionar la semana 2</b> con este método.</li></ul></div>
  </div>
  <div class="src"><b>Fuentes:</b> HypeAuditor (Jeff Nippard, sept. 2026) · CreatorDB · Social Blade · Modash (Adrian Preuss) · Socialveins / HypeAuditor (Will Tennyson) · Supgrowth y Socialinsider (vistas promedio por tamaño de cuenta, 2026) · SocialPilot, Socialync, Creatorflow y Upgrow (algoritmo de Reels 2026) · perfiles públicos de Instagram (seguidores).</div>
  <div class="foot"><span>NATE VELAZQUEZ · ESTRATEGIA ORGÁNICA</span><span>08 / 08</span></div>
</section>''')

CSS = """
@page { size: letter; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0b0b0f; font-family: Inter, Arial, sans-serif; color: #f4f4f7; }
.page { width: 8.5in; height: 11in; padding: .6in .6in .6in; position: relative; overflow: hidden; break-after: page; background: #0b0b0f; }
.page:last-child { break-after: auto; }
.eyebrow { font-size: 8pt; font-weight: 700; letter-spacing: .1em; color: #5b7cfa; }
.foot { position: absolute; left: .6in; right: .6in; bottom: .42in; display: flex; justify-content: space-between; border-top: .75pt solid #1f1f27; padding-top: 10pt; font-size: 7pt; letter-spacing: .06em; color: #67666f; }
.tag { font-size: 6.6pt; font-weight: 700; letter-spacing: .08em; padding: 2pt 7pt; border-radius: 8pt; white-space: nowrap; }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 14pt; }
.sc { font-size: 8pt; font-weight: 700; letter-spacing: .08em; color: #5b7cfa; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #5b7cfa; display: inline-block; }
h2 { font-size: 20pt; font-weight: 800; margin-top: 8pt; line-height: 1.2; }
.angle { color: #a6a6b3; font-size: 9.6pt; margin-top: 4pt; margin-bottom: 4pt; }
.box { background: #131318; border: .75pt solid #22222b; border-radius: 7pt; padding: 11pt 13pt; margin-top: 9pt; }
.bh { font-size: 7.6pt; font-weight: 700; letter-spacing: .08em; color: #67666f; margin-bottom: 6pt; }
.bh em { font-style: normal; color: #5b7cfa; font-size: 9.4pt; margin-right: 7pt; }
.box p, .box li { font-size: 8.6pt; color: #a6a6b3; line-height: 1.6; }
.box p + p { margin-top: 5pt; }
.box b { color: #f4f4f7; }
.box ul, .box ol { padding-left: 14pt; }
.box li { margin-top: 3pt; }
.box.note { border-color: #2a3778; background: #10142a; }
.cover .cv { text-align: center; margin-top: 1.2in; }
.cover h1 { font-size: 33pt; font-weight: 800; margin-top: 12pt; line-height: 1.12; }
.cover .sub { color: #a6a6b3; font-size: 10.5pt; margin-top: 10pt; }
.summary { margin-top: 40pt; padding: 16pt 18pt; }
.summary li { font-size: 9.4pt; margin-top: 7pt; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 9pt; }
.grid2 .box { margin-top: 9pt; }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin-top: 9pt; }
.stats div { background: #131318; border: .75pt solid #22222b; border-radius: 7pt; padding: 11pt 10pt; }
.stats b { display: block; font-size: 18pt; color: #5b7cfa; font-weight: 800; }
.stats span { font-size: 7.6pt; color: #a6a6b3; line-height: 1.45; display: block; margin-top: 4pt; }
.tbl { width: 100%; border-collapse: collapse; margin-top: 10pt; }
.tbl th { font-size: 6.8pt; letter-spacing: .08em; color: #67666f; text-align: left; padding: 6pt 6pt; border-bottom: 1pt solid #2c2c36; text-transform: uppercase; }
.tbl td { font-size: 7.8pt; color: #a6a6b3; padding: 6.5pt 6pt; border-bottom: .75pt solid #1d1d24; vertical-align: top; line-height: 1.45; }
.tbl td b { color: #f4f4f7; }
.tbl .h { color: #5b7cfa; font-size: 7.2pt; }
.tbl .num { color: #f4f4f7; font-weight: 600; }
.fmt { padding: 9pt 13pt; }
.fmt p { font-size: 8.3pt; }
.fmt .ref { color: #5b7cfa; font-size: 7.6pt; font-weight: 600; }
.fmt .ex { color: #d6d6de; }
.rank > div { display: grid; grid-template-columns: 26pt 1fr; gap: 10pt; background: #131318; border: .75pt solid #22222b; border-radius: 7pt; padding: 11pt 13pt; margin-top: 8pt; }
.rank > div > b { font-size: 20pt; color: #5b7cfa; font-weight: 800; line-height: 1; }
.rank h4 { font-size: 10pt; margin-bottom: 3pt; }
.rank p { font-size: 8.5pt; color: #a6a6b3; line-height: 1.6; }
.rank p b { color: #f4f4f7; }
.pils { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin-top: 10pt; }
.pil { background: #131318; border: .75pt solid #22222b; border-radius: 7pt; padding: 11pt 10pt; }
.pil .pct { font-size: 20pt; font-weight: 800; }
.pil h4 { font-size: 8pt; letter-spacing: .1em; margin: 2pt 0 6pt; }
.pil p { font-size: 7.8pt; color: #a6a6b3; line-height: 1.5; margin-top: 3pt; }
.pil p b { color: #f4f4f7; }
.rules { display: grid; grid-template-columns: 1fr 1fr; gap: 4pt 14pt; }
.wks .box { margin-top: 9pt; }
.wk li { font-size: 8.3pt; }
.src { font-size: 7pt; color: #67666f; line-height: 1.55; margin-top: 12pt; }
"""

doc = f"<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><title>Nate Velazquez · Estrategia de Contenido Orgánico</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(PAGES)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "NateVelazquez_EstrategiaOrganica.pdf"
subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
