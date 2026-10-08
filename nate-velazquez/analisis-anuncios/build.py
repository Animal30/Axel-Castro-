# Genera el PDF de análisis de anuncios de la competencia + anuncios nuevos para Nate (HTML -> PDF).
import html, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
exec((HERE / "_css.py").read_text())
e = lambda s: html.escape(s, quote=False)
P = []
TOTAL = 8
foot = lambda n: f'<div class="foot"><span>NATE VELAZQUEZ · ANÁLISIS DE ANUNCIOS</span><span>{n:02d} / {TOTAL:02d}</span></div>'
def head(n, t, sub): return f'<div class="eyebrow">NATE VELAZQUEZ · ANÁLISIS DE ANUNCIOS</div><div class="top"><span class="sc"><i></i>{n}</span></div><h2>{t}</h2><div class="angle">{sub}</div>'

# 1 Portada
P.append(f'''<section class="page cover"><div class="cv">
<div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
<h1>Qué anuncios funcionan<br>en la competencia</h1>
<p class="sub">Análisis de la Biblioteca de Anuncios de Meta (EE. UU.) y 4 anuncios nuevos para Nate.</p></div>
<div class="box summary"><div class="bh">RESUMEN EN 30 SEGUNDOS</div><ol>
<li><b>Hay más de 8.300 anuncios activos</b> de "nutrition coaching" en EE. UU. Revisamos unos 150 de 20 anunciantes del rubro.</li>
<li><b>Lo que funciona se ve en quién escala:</b> D1 Training corre su "6 Week Challenge" en decenas de sucursales; Tyler Toth tiene 8 versiones del mismo anuncio; una nutricionista (BeingBrigid) tiene más de 15.</li>
<li><b>Seis patrones se repiten:</b> plazo fijo, fecha límite, "basta de adivinar", vida real que se desarma, energía en vez de kilos, y la ciudad en el título.</li>
<li><b>Lo que hizo rebotar a Nate</b> (kilos, promesas, cuerpos) también lo usan otros, pero es lo que Meta rechaza: no se copia.</li>
<li><b>4 anuncios nuevos para Nate</b>, cada uno basado en un patrón ganador y escrito para pasar la revisión de Meta.</li></ol></div>
{foot(1)}</section>''')

# 2 Método
P.append(f'''<section class="page">{head("CÓMO LO MEDIMOS", "Cómo saber qué anuncio funciona", "La Biblioteca de Meta no muestra alcance ni gasto en EE. UU. Así lo resolvimos.")}
<div class="grid2">
<div class="box"><div class="bh"><em>01</em>QUÉ NO SE PUEDE VER</div><p>Para anuncios comerciales en EE. UU., Meta <b>no publica</b> alcance, impresiones ni gasto. Eso solo existe para anuncios políticos o de Europa. Nadie (ni herramientas pagas) puede ver cuántas consultas trae el anuncio de otro.</p></div>
<div class="box"><div class="bh"><em>02</em>LA SEÑAL QUE SÍ FUNCIONA</div><p>Nadie invierte en 8 versiones de un anuncio que no vende. Cuando un anunciante <b>duplica el mismo anuncio</b> en varias variantes, sucursales o ciudades, es porque le está dando resultado y lo está escalando.</p><p>Los anuncios que <b>vuelven a aparecer semana tras semana</b> con el mismo título son la otra señal.</p></div></div>
<div class="stats"><div><b>8.358</b><span>anuncios activos de "nutrition coaching" en EE. UU.</span></div><div><b>~150</b><span>anuncios revisados en detalle</span></div><div><b>20</b><span>anunciantes del rubro analizados</span></div><div><b>6</b><span>patrones que se repiten en los que escalan</span></div></div>
<div class="box note"><div class="bh">QUÉ BÚSQUEDAS HICIMOS</div><p>"nutrition coaching", "online nutrition coach apply", "nutrition coach busy" y "personal training Tampa", solo anuncios activos en EE. UU., más una revisión de todos los anuncios activos de los coaches online que aparecieron. Consultado el 8 de octubre de 2026.</p></div>
{foot(2)}</section>''')

# 3 Quién escala
ROWS = [
 ("D1 Training", "Decenas de sucursales", "\"6 WEEK CHALLENGE\" · \"8 WEEK CHALLENGE\"", "Plazo fijo y corto. Un título de 3 palabras que dice todo."),
 ("BeingBrigid Functional Nutrition", "15+ variantes", "\"7 days to feel more like yourself again\" · \"7 Days to Less Bloat, More Energy\" · \"Last Chance to Reset Energy & Calm Cravings\"", "Nutrición sin hablar de kilos: energía, antojos, sentirse bien. Pasa la revisión de Meta."),
 ("Hooper Adaptive Coaching", "15+ variantes", "\"Your Week Fell Apart. Your Training Program Didn't.\" · \"Life Changes. Your Plan Should Too.\" · \"Less Time To Train Means Less Time To Waste\"", "Le habla al ocupado: la vida real se desarma y el plan se adapta."),
 ("Tyler Toth (coach online)", "8 variantes", "\"Stop Guessing At Your Physique\"", "\"Basta de adivinar\": el dolor de no saber qué hacer."),
 ("Austin Martin Fitness", "6 variantes", "\"1:1 Online Coaching\"", "Directo y simple. Funciona con buen video."),
 ("Eric Roberts (coach online)", "6+ variantes", "\"Stop Trying on Your Own & Get Accountability\" · \"Free Calorie Calculator…\" · \"our clients lose 10-20lbs in 8 wks\"", "Mezcla acompañamiento, un regalo para captar contactos y… promesa de kilos (no copiar)."),
 ("Burn Boot Camp", "Muchas sucursales", "\"4 WEEKS FOR $69 · ENDS MON 10/12\"", "Fecha límite concreta: crea urgencia real."),
 ("Elevate 360 · Spenga · Allen Elliott", "5 títulos por anuncio", "\"Greenville Men: Feel Strong Again!\" · \"Get Results Before The Holidays\"", "Ciudad en el título y temporada (fiestas, fin de año)."),
 ("Omar Bohorquez (en español)", "Varias", "\"Deja de improvisar. Empieza a entrenar con un plan.\" · botón \"Chatea con nosotros\"", "Anuncio a mensajes: la conversación es la venta."),
]
rows = "".join(f'<tr><td><b>{e(a)}</b></td><td class="num">{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>' for a,b,c,d in ROWS)
P.append(f'''<section class="page">{head("QUIÉN ESTÁ ESCALANDO", "Los anunciantes que más invierten", "Títulos reales de anuncios activos. Cuantas más variantes, más resultado le está dando.")}
<table class="tbl"><thead><tr><th>Anunciante</th><th>Cuánto escala</th><th>Títulos que usa (reales)</th><th>Por qué funciona</th></tr></thead><tbody>{rows}</tbody></table>
{foot(3)}</section>''')

# 4 Patrones
PAT = [
 ("01", "PLAZO FIJO", "\"6 WEEK CHALLENGE\" · \"8-Week Fit Over 30\"", "Un final a la vista baja el miedo a comprometerse \"para siempre\".", "Nate ya tiene 12 semanas: hay que decirlo en el título."),
 ("02", "FECHA LÍMITE REAL", "\"ENDS MON 10/12\" · \"Last Chance\" · \"Before The Holidays\"", "Sin fecha, la gente lo deja para después y se olvida.", "\"Start before the holidays. Enrollment closes Oct 31.\""),
 ("03", "BASTA DE ADIVINAR", "\"Stop Guessing At Your Physique\" · \"Stop Trying on Your Own\" · \"Deja de improvisar\"", "Nombra el dolor real: no saber qué hacer y estar solo.", "\"Stop guessing what to eat.\""),
 ("04", "LA VIDA REAL SE DESARMA", "\"Your Week Fell Apart. Your Program Didn't.\" · \"Life Changes. Your Plan Should Too.\"", "El ocupado se siente visto: su problema no es la voluntad, es el caos.", "\"Your week fell apart. Your eating doesn't have to.\""),
 ("05", "ENERGÍA, NO KILOS", "\"Less Bloat, More Energy\" · \"Calm Cravings\" · \"Feel more like yourself again\"", "Habla de lo que se siente día a día y pasa la revisión de salud de Meta.", "Energía de tarde, antojos de noche, comer sin culpa."),
 ("06", "CIUDAD EN EL TÍTULO", "\"Greenville Men: Feel Strong Again!\" · \"Naples Women: …\"", "La persona siente que es para ella. (Ojo: la edad sí está prohibida; la ciudad no.)", "\"Tampa Professionals: …\""),
]
cards = "".join(f'<div class="box fmt"><div class="bh"><em>{n}</em>{t}</div><p class="ref">Lo usan: {e(x)}</p><p><b>Por qué funciona:</b> {e(w)}</p><p class="ex"><b>Para Nate:</b> {e(a)}</p></div>' for n,t,x,w,a in PAT)
P.append(f'''<section class="page">{head("LOS PATRONES", "Los 6 patrones que se repiten", "Lo que tienen en común los anuncios que más escalan, y cómo lo aplicamos a Nate.")}{cards}{foot(4)}</section>''')

# 5 Qué no copiar
P.append(f'''<section class="page">{head("QUÉ NO COPIAR", "Lo que también usan, pero hace rebotar el anuncio", "Algunos competidores corren anuncios que Meta todavía no frenó. Para Nate no vale el riesgo: ya le rechazaron uno.")}
<table class="tbl"><thead><tr><th>Lo que vimos</th><th>Ejemplo real</th><th>Por qué no</th><th>Qué hacer en su lugar</th></tr></thead><tbody>
<tr><td><b>Kilos y plazos</b></td><td>"our clients lose 10-20lbs in 8 wks on avg"</td><td>Promesa de resultado de peso: es lo que hizo rebotar a Nate.</td><td class="num">Hablar del proceso: 12 semanas, plan, acompañamiento</td></tr>
<tr><td><b>Edad o género + cuerpo</b></td><td>"LOGANVILLE WOMEN 35+" · "Ready To Lose 10+ Pounds?"</td><td>Meta prohíbe afirmar características de la persona (edad, peso, salud).</td><td class="num">Ciudad y situación: "Tampa professionals", "busy weeks"</td></tr>
<tr><td><b>Antes y después</b></td><td>Fotos de transformación en el video</td><td>Prohibido en anuncios de pérdida de peso.</td><td class="num">Comida, manos, Nate a cámara, testimonios hablados</td></tr>
<tr><td><b>Entrada barata</b></td><td>"$1 to Join" · "4 weeks for $69" · "Free month"</td><td>Funciona para gimnasios de volumen; para un 1:1 de $697+ trae curiosos que no compran.</td><td class="num">Regalo de valor (guía) o llamada de diagnóstico</td></tr>
</tbody></table>
<div class="box note"><div class="bh">LA REGLA SIMPLE PARA NATE</div><p>Si la frase habla del <b>cuerpo o del peso de la persona</b>, se cambia. Si habla de <b>su semana, su comida, su energía o el proceso</b>, va.</p></div>
{foot(5)}</section>''')

# 6-7 Anuncios
ADS = [
 ("01", "PATRÓN 02 + 01 · FECHA LÍMITE + PLAZO", "Before The Holidays",
  "Most people start eating better in January. My clients start in October and walk into the holidays already ahead.",
  ["I'm Nate. I coach busy professionals here in Tampa on nutrition.", "In 12 weeks we build a way of eating around your schedule and the food you like, with a weekly check-in so you're never doing it alone.", "No diets. No foods off the table. Just a plan you actually keep through Thanksgiving, Christmas and New Year's."],
  "I'm taking 10 new clients before October 31. Tap the link to apply.",
  "Most people wait until January. My clients start now. 🦃🎄\n\n12 weeks of 1:1 nutrition coaching built around your schedule and the food you enjoy, with weekly check-ins so you stay on track through the holidays.\n\nEnrollment closes October 31 · 10 spots.\nTap \"Apply Now\" to book a call.",
  "Start Before The Holidays · 10 Spots"),
 ("02", "PATRÓN 04 · LA VIDA REAL SE DESARMA", "Your Week Fell Apart",
  "Your week fell apart. Your eating doesn't have to.",
  ["Late meeting, kid's practice, no time to cook. That's when every plan you've tried falls apart.", "I'm Nate, nutrition coach for busy professionals in Tampa. My clients get a plan that bends instead of breaks:", "a 10-minute dinner, a drive-thru order that still works, and a weekly check-in where we adjust to the week you actually had."],
  "If you want a plan built for messy weeks, tap the link and let's talk.",
  "Your week fell apart. Your eating doesn't have to.\n\n1:1 nutrition coaching for busy professionals: a plan that adapts to late meetings, travel and family dinners, with a weekly check-in to adjust it.\n\nNo diets. No foods off the table.\nTap \"Apply Now\" to book a call.",
  "A Nutrition Plan Built For Busy Weeks"),
 ("03", "PATRÓN 03 · BASTA DE ADIVINAR", "Stop Guessing What To Eat",
  "If you've ever stood in front of the fridge with no idea what to eat… this is for you.",
  ["Most people don't need more information. They need someone to tell them exactly what works for their day.", "I'm Nate. I coach busy professionals here in Tampa.", "You get a plan built around food you already like, simple swaps, and a weekly check-in with me. No guessing, no starting over, no figuring it out alone."],
  "Tap the link and let's build your plan together.",
  "Stop guessing what to eat. 🍽️\n\n1:1 nutrition coaching for busy professionals in Tampa: a simple plan built around the food you like, plus a weekly check-in so you never figure it out alone.\n\nTap \"Apply Now\" to book a call.",
  "Stop Guessing What To Eat"),
 ("04", "PATRÓN 05 + 06 · ENERGÍA + CIUDAD", "Tampa Professionals: The 3pm Crash",
  "Tampa professionals: if 3pm hits and you're reaching for the vending machine, it's probably not your willpower.",
  ["It's usually lunch. Too small, too fast, or skipped.", "I'm Nate. I coach busy professionals on nutrition, and fixing the middle of the day is where we start: more steady energy, fewer cravings at night, meals that take minutes.", "Then we build the rest around your schedule, with a weekly check-in so it actually sticks."],
  "If you want more energy without another diet, tap the link and let's talk.",
  "Tampa professionals: tired of the 3pm crash? ⚡\n\n1:1 nutrition coaching built around your workday: steadier energy, fewer late-night cravings and meals that take minutes, not hours.\n\nNo diets. Weekly check-ins.\nTap \"Apply Now\" to book a call.",
  "More Energy. No Diets. 1:1 Coaching"),
]
def adcard(n, tag, title, hook, core, cta, prim, hl):
    c = "".join(f"<p>{e(x)}</p>" for x in core)
    pt = "<br>".join(e(l) for l in prim.split("\n"))
    return f'''<div class="box ad"><div class="adh"><span class="adn">ANUNCIO {n}</span><span class="tag" style="color:#facc15;background:#facc1522">{tag}</span></div>
<h3>{e(title)}</h3>
<div class="adg"><div><span class="lab">GANCHO DEL VIDEO (0–3 s)</span><p class="hk">“{e(hook)}”</p>
<span class="lab">MENSAJE</span>{c}<span class="lab">LLAMADO A LA ACCIÓN</span><p class="hk cta">“{e(cta)}”</p></div>
<div class="pt"><span class="lab">TEXTO DEL ANUNCIO</span><p>{pt}</p><span class="lab">TÍTULO</span><p class="hk">{e(hl)}</p><span class="lab">BOTÓN</span><p class="hk">Apply Now</p></div></div></div>'''
P.append(f'''<section class="page">{head("ANUNCIOS PARA NATE", "4 anuncios nuevos (1 y 2)", "Cada uno toma un patrón ganador de la competencia. Guion del video + texto + título, en inglés y listos para Meta.")}{adcard(*ADS[0])}{adcard(*ADS[1])}{foot(6)}</section>''')
P.append(f'''<section class="page">{head("ANUNCIOS PARA NATE", "4 anuncios nuevos (3 y 4)", "Grabación: Nate a cámara o comida/manos en pantalla. Nunca cuerpos, balanzas ni antes y después.")}{adcard(*ADS[2])}{adcard(*ADS[3])}{foot(7)}</section>''')

# 8 Plan de prueba
P.append(f'''<section class="page">{head("CÓMO LOS CORREMOS", "Plan de prueba de 7 días", "Para saber con datos cuál de los 4 trae más consultas por menos plata.")}
<div class="grid2">
<div class="box"><div class="bh"><em>01</em>LA CONFIGURACIÓN</div><ul>
<li><b>1 campaña</b> de clientes potenciales, con formulario de Meta (ya armada).</li>
<li><b>Los 4 anuncios</b> en el mismo conjunto, para que Meta reparta el presupuesto.</li>
<li><b>$20–30 por día</b> durante 7 días.</li>
<li><b>Tampa + 25–30 millas</b>, 25–65 años, sin intereses (Advantage+).</li></ul></div>
<div class="box"><div class="bh"><em>02</em>LA REGLA PARA DECIDIR</div><ul>
<li><b>Día 3:</b> apagar el que tenga el costo por consulta más alto, si ya gastó más de $30 sin consultas.</li>
<li><b>Día 7:</b> quedarse con los 2 mejores y subir el presupuesto 20% cada 3 días.</li>
<li><b>Cada 2 semanas:</b> sumar un anuncio nuevo con el patrón ganador y un gancho distinto.</li></ul></div></div>
<table class="tbl"><thead><tr><th>Métrica</th><th>Qué dice</th><th>Referencia para arrancar</th></tr></thead><tbody>
<tr><td><b>Retención a 3 s</b></td><td>Si el gancho frena el scroll</td><td class="num">30% o más</td></tr>
<tr><td><b>Clic en el anuncio (CTR)</b></td><td>Si el mensaje interesa</td><td class="num">1% o más</td></tr>
<tr><td><b>Costo por consulta</b></td><td>Cuánto cuesta cada formulario</td><td class="num">Bajar semana a semana; comparar entre los 4</td></tr>
<tr><td><b>Consultas que agendan</b></td><td>Si la consulta es de calidad</td><td class="num">Llamar en menos de 1 hora</td></tr></tbody></table>
<div class="box note"><div class="bh">LO QUE MÁS MUEVE LAS CONSULTAS (MÁS QUE EL ANUNCIO)</div><p><b>Responder rápido.</b> Una consulta contactada en los primeros 5–10 minutos convierte varias veces más que una contactada al día siguiente. Las preguntas del formulario (una sobre disposición a invertir) filtran a los curiosos.</p></div>
<div class="src"><b>Fuente:</b> Biblioteca de Anuncios de Meta (búsquedas de anuncios activos en EE. UU., 8 de octubre de 2026). Los títulos citados son reales; el texto completo y el video de cada anuncio se pueden ver en la Biblioteca. Las referencias de métricas son puntos de partida orientativos, no garantías.</div>
{foot(8)}</section>''')

EXTRA = """
.ad { padding: 12pt 14pt; }
.adh { display: flex; justify-content: space-between; align-items: center; }
.adn { font-size: 7.6pt; font-weight: 700; letter-spacing: .1em; color: #5b7cfa; }
.ad h3 { font-size: 13pt; margin: 4pt 0 6pt; }
.adg { display: grid; grid-template-columns: 1.15fr 1fr; gap: 14pt; }
.lab { display: block; font-size: 6.6pt; letter-spacing: .1em; color: #67666f; margin: 6pt 0 2pt; font-weight: 700; }
.ad p { font-size: 8pt; line-height: 1.5; }
.ad .hk { color: #f4f4f7; font-weight: 600; font-size: 8.4pt; }
.ad .cta { color: #8fa6ff; }
.pt { background: #0f0f14; border: .75pt solid #22222b; border-radius: 6pt; padding: 4pt 10pt 8pt; }
"""
doc = f"<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><title>Nate Velazquez · Análisis de Anuncios</title><style>{FONTS}</style><style>{CSS}{EXTRA}</style></head><body>{''.join(P)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "NateVelazquez_AnalisisAnuncios.pdf"
subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)], check=True, stderr=subprocess.DEVNULL)
src.unlink(); print(pdf)
