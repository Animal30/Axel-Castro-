# Genera el PDF de preguntas de nutrición más buscadas en 2026 + guiones de respuesta de Nate (HTML -> PDF).
import html, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
exec((HERE / "_css.py").read_text())
e = lambda s: html.escape(s, quote=False)
P = []; TOTAL = 7
foot = lambda n: f'<div class="foot"><span>NATE VELAZQUEZ · PREGUNTAS DE NUTRICIÓN 2026</span><span>{n:02d} / {TOTAL:02d}</span></div>'
def head(n, t, sub): return f'<div class="eyebrow">NATE VELAZQUEZ · PREGUNTAS DE NUTRICIÓN 2026</div><div class="top"><span class="sc"><i></i>{n}</span></div><h2>{t}</h2><div class="angle">{sub}</div>'

# 1 Portada
P.append(f'''<section class="page cover"><div class="cv">
<div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
<h1>Lo que la gente<br>pregunta en 2026</h1>
<p class="sub">Las preguntas de nutrición más buscadas, los formatos que más rinden y las respuestas de Nate listas para grabar.</p></div>
<div class="box summary"><div class="bh">RESUMEN EN 30 SEGUNDOS</div><ol>
<li><b>Los videos que más alcance tienen responden algo que la gente ya está buscando.</b> La demanda existe antes de publicar: el video solo tiene que aparecer.</li>
<li><b>Los temas más calientes de 2026:</b> proteína, "fibermaxxing", aceites de semillas, ultraprocesados, creatina, magnesio y cómo comer con medicamentos GLP-1 (Ozempic).</li>
<li><b>El formato ganador es "pregunta buscada + respuesta directa"</b>, con la pregunta escrita en pantalla y una postura clara. Los temas polémicos (aceites, ultraprocesados, GLP-1) generan debate en comentarios.</li>
<li><b>6 guiones listos</b>, en formato yapping, con la respuesta de Nate a las 6 preguntas con más potencial.</li>
<li><b>Dos de ellos son solo para orgánico</b> (GLP-1 y creatina): Meta restringe anuncios sobre medicamentos y suplementos.</li></ol></div>
{foot(1)}</section>''')

# 2 Formatos
FMT = [
 ("01", "PREGUNTA BUSCADA + RESPUESTA DIRECTA", "La pregunta escrita en pantalla desde el segundo 0 (\"How much protein do you actually need?\") y la respuesta con un número concreto.", "La gente ya está buscando esa respuesta. Instagram también funciona como buscador: el título y el caption con la pregunta exacta hacen que el video aparezca en búsquedas."),
 ("02", "EL COACH REACCIONA", "Pantalla verde o \"stitch\" sobre un video viral con una afirmación de nutrición, y Nate dice qué es cierto y qué no.", "Aprovecha un video que ya está viralizado: el público ya existe, Nate solo suma su opinión. Es el formato más barato de producir."),
 ("03", "MITO O VERDAD", "Arranca con una creencia muy repetida (\"Seed oils are poisoning you\") y la desarma con calma.", "Las aperturas contrarias generan debate en comentarios, y los comentarios le dicen a Instagram que el video interesa."),
 ("04", "RESPONDER UN COMENTARIO", "Usar la función de responder un comentario con video: la pregunta de un seguidor aparece en pantalla.", "Muestra que la gente le pregunta cosas reales a Nate y genera más preguntas, que son ideas para los próximos videos."),
 ("05", "BUENO · MEJOR · EL MEJOR", "El formato de platos que ya están grabando: tres opciones del mismo tipo de comida, de menos a más completa.", "Se guarda para usarlo después. Los guardados son la señal más fuerte de valor en contenido de nutrición."),
]
cards = "".join(f'<div class="box fmt"><div class="bh"><em>{n}</em>{t}</div><p><b>Cómo es:</b> {e(c)}</p><p class="ex"><b>Por qué rinde:</b> {e(w)}</p></div>' for n,t,c,w in FMT)
P.append(f'''<section class="page">{head("QUÉ VIDEOS SE VIRALIZAN", "Los 5 formatos que más rinden en nutrición", "Lo que tienen en común los videos de nutrición que superan las 500–1.000 vistas habituales.")}{cards}
<div class="box note"><div class="bh">LA DIFERENCIA ENTRE 500 Y 50.000 VISTAS</div><p>Los videos que se quedan en 500 vistas suelen ser consejos genéricos que nadie estaba buscando ("eat more veggies"). Los que despegan tienen <b>un tema que ya está en conversación</b> (fibermaxxing, aceites de semillas, Ozempic), <b>una postura clara</b> y <b>un dato concreto</b> en los primeros 3 segundos.</p></div>
{foot(2)}</section>''')

# 3 Banco de preguntas
Q = [
 ("PROTEÍNA", "How much protein do I actually need a day?", "Aparece entre las preguntas de salud más buscadas en Google en 2026 (Soliant Health)", "Guion 1"),
 ("PROTEÍNA", "Are protein powders worth it?", "\"Protein powders\": ~673.000 búsquedas al mes, +174% vs. el año anterior (Rising Trends)", "Idea"),
 ("FIBRA", "What is fibermaxxing? Is it healthy?", "La tendencia de nutrición más citada de 2026 (MyFitnessPal, Nutrition Insight, We Eat Live Do Well)", "Guion 2"),
 ("ACEITES", "Are seed oils actually bad for you?", "Uno de los mitos más repetidos en redes; varios dietistas lo desmienten en 2026", "Guion 3"),
 ("SUPLEMENTOS", "Should I take creatine? Is it only for lifters?", "\"Creatine\": entre ~368.000 y ~673.000 búsquedas al mes según la fuente", "Guion 4 · solo orgánico"),
 ("SUPLEMENTOS", "Is magnesium glycinate worth it for sleep?", "\"Magnesium glycinate\": ~1.000.000 de búsquedas al mes, +22% (Rising Trends)", "Idea"),
 ("GLP-1", "What should I eat on Ozempic / a GLP-1?", "Gran motor de las tendencias de 2026: cómo comer cuando baja el apetito", "Guion 5 · solo orgánico"),
 ("PROCESADOS", "Are ultra-processed foods really that bad?", "Pregunta frecuente de 2026, con definiciones que se contradicen", "Guion 6"),
 ("PROCESADOS", "Is beef tallow healthier than oil?", "En la revisión de controversias de nutrición de 2026 (NCBI)", "Idea"),
 ("PROCESADOS", "Are food dyes dangerous?", "Tema repetido en redes y en la prensa en 2026", "Idea"),
 ("CLÁSICOS", "Are carbs bad for me?", "Pregunta que aparece todos los años en las listas de dietistas", "Ya tiene guion (no repetir)"),
 ("CLÁSICOS", "Can you eat too much fruit?", "Pregunta frecuente en sitios de salud (British Heart Foundation)", "Idea"),
 ("CLÁSICOS", "Is intermittent fasting worth it?", "Entre las dietas más mencionadas en las encuestas de 2026 (IFIC)", "Idea"),
 ("CLÁSICOS", "Is full-fat dairy actually healthy?", "En la revisión de controversias de nutrición de 2026 (NCBI)", "Idea"),
]
rows = "".join(f'<tr><td><span class="tag" style="color:#5b7cfa;background:#5b7cfa22">{e(t)}</span></td><td><b>{e(q)}</b></td><td>{e(d)}</td><td class="num">{e(u)}</td></tr>' for t,q,d,u in Q)
P.append(f'''<section class="page">{head("LAS PREGUNTAS", "Las preguntas de nutrición más buscadas en 2026", "Ordenadas por tema. Las 6 con más potencial ya tienen guion; el resto queda como banco de ideas para las próximas semanas.")}
<table class="tbl"><thead><tr><th>Tema</th><th>Pregunta (como la busca la gente)</th><th>Señal de demanda</th><th>Uso</th></tr></thead><tbody>{rows}</tbody></table>
<div class="box note"><div class="bh">CÓMO LEER ESTOS NÚMEROS</div><p>Los volúmenes de búsqueda salen de herramientas de palabras clave y artículos de tendencias de 2026, no de Google directamente. Sirven para saber <b>qué temas tienen demanda</b>, no como cifras exactas.</p></div>
{foot(3)}</section>''')

# 4-6 Guiones
S = [
 ("01", "PROTEÍNA", "How Much Protein Do You Actually Need?", "Feed + anuncio",
  "The most Googled nutrition question this year: how much protein do you actually need? Here's the real number.",
  "Most people eat less protein than they think. Here's how to check in 10 seconds.",
  ["The official number, about 0.8 grams per kilo of body weight, is the minimum to avoid a deficiency. It's not the amount that keeps you full and protects your muscle.", "For most active adults, research points closer to 1.2 to 1.6 grams per kilo.", "In real life, I tell clients: 25 to 40 grams per meal, three or four times a day. A palm of chicken or fish, or a big bowl of Greek yogurt.", "And here's the pattern I see the most: plenty of protein at dinner, almost none at breakfast. That's the gap.", "I'm Nate, nutrition coach."],
  "Send me a message with the word PROTEIN and tell me what you eat for breakfast. I'll tell you how to hit your number.", "PROTEIN"),
 ("02", "FIBRA", "Is Fibermaxxing Actually Healthy?", "Feed + anuncio",
  "Fibermaxxing is all over your feed. As a nutrition coach, here's what I actually think.",
  "The 2026 nutrition trend I actually agree with, with one big warning.",
  ["Good news first: it's one of the few trends I actually like. Most adults get around half the fiber they need.", "The target is roughly 25 grams a day for women and about 30 to 38 for men.", "But here's where people mess it up: they go from 10 grams to 50 overnight and spend the next two days bloated and miserable.", "Go up slowly, a few grams a week, and drink more water as you do it. Beans, berries, oats, chia, veggies. Not a powder in every drink.", "I'm Nate, nutrition coach."],
  "Send me a message with the word FIBER and tell me what a normal day of eating looks like. I'll tell you where I'd add it first.", "FIBER"),
 ("03", "ACEITES", "Are Seed Oils Actually Bad For You?", "Feed + anuncio",
  "Are seed oils actually poisoning you? Let's talk about it, because this one is everywhere.",
  "Everyone cutting seed oils says they feel better. Here's the real reason.",
  ["Short answer: the research doesn't back the fear. Studies that swap saturated fat for oils like canola or soybean tend to show better cholesterol, not worse.", "So why do people feel better when they cut seed oils? Because they also cut fries, chips, fast food and packaged snacks.", "The problem was never the bottle of canola oil in your kitchen. It was the deep fryer.", "Cooking at home with canola or olive oil? You're fine. Look at how often you eat fried and packaged food instead.", "I'm Nate, nutrition coach."],
  "Send me a message with the word OILS and tell me what you cook with at home. I'll tell you if I'd change anything.", "OILS"),
 ("04", "SUPLEMENTOS", "Should You Take Creatine?", "Solo orgánico",
  "Creatine isn't just for bodybuilders anymore. Honestly, it never should have been.",
  "The most researched supplement out there, and the most misunderstood.",
  ["It's one of the most studied supplements that exists. Most research uses 3 to 5 grams a day, every day. No loading phase needed.", "It helps your muscles recover and perform, and people of all ages are using it now, not just lifters.", "It's not a steroid, it's not a fat burner and it's not magic. Some people see the scale go up a little at first: that's water in the muscle, not fat.", "If you have kidney issues or take medication, talk to your doctor first.", "I'm Nate, nutrition coach."],
  "Send me a message with the word CREATINE and tell me what supplements you take right now. I'll tell you which ones I'd actually keep.", "CREATINE"),
 ("05", "GLP-1", "Eating On A GLP-1 Like Ozempic", "Solo orgánico",
  "On a GLP-1 like Ozempic? Then what you eat matters more, not less.",
  "Nobody tells you this part about eating on Ozempic.",
  ["These medications turn your appetite way down. That sounds great, until you realize you're barely eating protein or fiber.", "That's when people feel tired, lose muscle and struggle when they come off it.", "Three things I focus on: protein at every meal, even if it's small. Fiber and water, because digestion slows down. And strength training, so you keep your muscle.", "Your doctor handles the medication. My job is making sure the food side is working.", "I'm Nate, nutrition coach."],
  "Send me a message with the word GLP and tell me what a day of eating looks like for you right now.", "GLP"),
 ("06", "PROCESADOS", "Are Ultra-Processed Foods Really That Bad?", "Feed + anuncio",
  "‘Ultra-processed’ is the scariest word in nutrition right now. But a protein bar and a donut aren't the same thing.",
  "You don't need to cut every processed food. Here's what to do instead.",
  ["The label basically means made in a factory with ingredients you wouldn't have at home. That covers soda and candy, but also some whole-grain breads, flavored Greek yogurt and protein bars.", "They're not all equal.", "Instead of trying to eat zero processed food, which almost nobody can do with a job and a family, aim for most of your plate to be real food.", "And when you do buy packaged stuff, pick the options that bring protein or fiber with them. Better most of the time beats perfect for two weeks.", "I'm Nate, nutrition coach."],
  "Send me a message with the word REAL and tell me the packaged foods you buy every week. I'll tell you which ones I'd keep and which I'd swap.", "REAL"),
]
def card(n, tag, title, use, hook, alt, core, cta, kw):
    c = "".join(f"<p>{e(x)}</p>" for x in core)
    color = "#facc15" if "orgánico" in use else "#4ade80"
    ct = e(cta).replace(kw, f'<span class="kw">{kw}</span>', 1)
    return f'''<div class="box ad"><div class="adh"><span class="adn">GUION {n} · {tag}</span><span class="tag" style="color:{color};background:{color}22">{e(use).upper()}</span></div>
<h3>{e(title)}</h3><div class="sg"><span class="lab">GANCHO</span><p class="hk">“{e(hook)}”</p><span class="lab">GANCHO ALTERNATIVO</span><p class="alt">“{e(alt)}”</p>
<span class="lab">RESPUESTA</span>{c}<span class="lab">LLAMADO A LA ACCIÓN · DM {kw}</span><p class="hk cta">“{ct}”</p></div></div>'''
P.append(f'''<section class="page">{head("LOS GUIONES", "Respuestas de Nate (1 y 2)", "Formato yapping: Nate a cámara, con la pregunta escrita en pantalla desde el segundo 0. 30–45 segundos.")}{card(*S[0])}{card(*S[1])}{foot(4)}</section>''')
P.append(f'''<section class="page">{head("LOS GUIONES", "Respuestas de Nate (3 y 4)", "El guion 4 es solo para publicación orgánica: Meta restringe los anuncios que hablan de suplementos.")}{card(*S[2])}{card(*S[3])}{foot(5)}</section>''')
P.append(f'''<section class="page">{head("LOS GUIONES", "Respuestas de Nate (5 y 6)", "El guion 5 es solo orgánico: los anuncios que mencionan medicamentos con receta (como Ozempic) están restringidos en Meta.")}{card(*S[4])}{card(*S[5])}{foot(6)}</section>''')

# 7 Cómo usarlo + fuentes
P.append(f'''<section class="page">{head("CÓMO USARLO", "Cómo grabarlos y publicarlos", "Lo que hace que una respuesta llegue a gente nueva y no se quede en los seguidores.")}
<div class="grid2">
<div class="box"><div class="bh"><em>01</em>GRABACIÓN</div><ul>
<li><b>La pregunta escrita en pantalla</b> desde el primer cuadro, grande y en el centro.</li>
<li>Nate a cámara, una sola toma, tono de charla. Subtítulos siempre.</li>
<li><b>El número o la respuesta corta antes del segundo 5</b> ("25 to 40 grams per meal").</li>
<li>Terminar con una frase que invite a comentar o a escribir.</li></ul></div>
<div class="box"><div class="bh"><em>02</em>PUBLICACIÓN</div><ul>
<li><b>Caption que empiece con la pregunta exacta</b> como la busca la gente: así aparece en el buscador de Instagram.</li>
<li>Portada del Reel con la pregunta en 4–6 palabras.</li>
<li>Responder los comentarios con video: cada pregunta nueva es el próximo guion.</li>
<li>Los que más guardados tengan pasan a anuncio (salvo los de solo orgánico).</li></ul></div></div>
<div class="box note"><div class="bh">ANTES DE PUBLICAR</div><p>Las respuestas usan rangos generales de las guías y la investigación más citadas. Son información educativa, no un consejo médico individual. En creatina y GLP-1, Nate recomienda hablar con el médico, como dicen los guiones.</p></div>
<div class="src"><b>Fuentes consultadas (octubre 2026):</b> We Eat Live Do Well, "4 Nutrition Questions Everyone's Asking in 2026" · Soliant Health, "2026 Most Popular Medical Questions Americans Google" · Rising Trends, "Nutrition Trends 2026" y "Supplement Trends 2026" · MyFitnessPal, "2026 Nutrition Trends" · Nutrition Insight, tendencias 2026 · Lincoln Land Community College, "Protein and fiber lead 2026 nutrition trends" · NCBI, "A Clinician's Guide for Trending Cardiovascular Nutritional Controversies in 2026" · British Heart Foundation, "Ask the expert" · MyFitnessPal y Yahoo Health sobre aceites de semillas · The Social Content Factory y Eliro, formatos de Reels 2026. No se tuvo acceso a Google Trends ni a estadísticas internas de Instagram: los volúmenes son estimaciones de terceros.</div>
{foot(7)}</section>''')

EXTRA = """
.ad { padding: 12pt 14pt; }
.adh { display: flex; justify-content: space-between; align-items: center; }
.adn { font-size: 7.6pt; font-weight: 700; letter-spacing: .1em; color: #5b7cfa; }
.ad h3 { font-size: 13.5pt; margin: 4pt 0 2pt; }
.lab { display: block; font-size: 6.6pt; letter-spacing: .1em; color: #67666f; margin: 7pt 0 2pt; font-weight: 700; }
.ad p { font-size: 8.3pt; line-height: 1.5; }
.ad .hk { color: #f4f4f7; font-weight: 600; font-size: 8.8pt; }
.ad .alt { color: #a6a6b3; font-style: italic; }
.ad .cta { color: #c9d3ff; }
.kw { color: #5b7cfa; font-weight: 700; }
"""
doc = f"<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><title>Nate Velazquez · Preguntas de Nutrición 2026</title><style>{FONTS}</style><style>{CSS}{EXTRA}</style></head><body>{''.join(P)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "NateVelazquez_PreguntasNutricion2026.pdf"
subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)], check=True, stderr=subprocess.DEVNULL)
src.unlink(); print(pdf)
