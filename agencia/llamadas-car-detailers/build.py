# Guion de llamadas en frío a car detailers de EE.UU. (inglés + español) -> PDF.
# Uso: python3 build.py
import html, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
ME, THEM, NOTE = "YOU", "THEM", "NOTE"

# Cada sección: (título EN, título ES, [(quién, inglés, español)])
SECTIONS = [
    ("Opening", "Apertura", [
        (ME, "Hi, good morning! Is this [BUSINESS NAME]?", "Hola, buen día. ¿Hablo con [NOMBRE DEL NEGOCIO]?"),
        (THEM, "Yeah, this is them. How can I help you?", "Sí, qué tal, buen día, decime."),
        (ME, "Good morning! My name is Nahuel. Who am I speaking with?", "Buen día, mi nombre es Nahuel, ¿con quién tengo el gusto?"),
        (THEM, "This is Mike. How's it going?", "Darío, mi nombre, ¿cómo va?"),
        (ME, "Doing great, Mike, thanks. I'll be quick so I don't take up your time. I came across your shop on Google, saw you on Maps and on Instagram, but I couldn't find a website to learn more about you guys. I wasn't even sure if you were open or taking new clients.",
             "Todo bien Darío. Te llamo rápido así no te robo tiempo. Los busqué por Google, los vi en Maps y en Instagram, pero no encontré un sitio web para ver más información. No estaba seguro de si estaban abiertos o tomando clientes."),
        (THEM, "Yeah, yeah, we're open.", "Sí sí, estamos trabajando."),
        (ME, "Awesome, perfect.", "Bien, perfecto."),
    ]),
    ("Transition to the pitch", "Transición al pitch", [
        (ME, "So Mike, what I do is build sales funnel systems for car detailers and dealerships here in the US.",
             "Yo me dedico a crear sistemas de embudos de ventas para car detailers y concesionarias de Estados Unidos."),
        (ME, "Since I noticed you didn't have a website, I took the initiative and put together a premium website for your brand.",
             "Como vi que no tenían sitio web, tomé la iniciativa y les preparé un sitio web premium para la marca."),
        (ME, "It's built specifically for: managing your clients, sales, inquiries, and how people see your brand.",
             "Les va a servir exclusivamente para: gestión de clientes, ventas, consultas y percepción de la marca."),
        (ME, "Are you running the shop by yourself, or do you have a team?", "¿Están trabajando solos o tienen un equipo?"),
    ]),
    ("Building rapport", "Construcción de relación", [
        (NOTE, "If he works alone:", "Si dice que trabaja solo:"),
        (ME, "Oh, nice, nice. How long have you been doing detailing, Mike?", "Ah, bien bien. ¿Hace cuánto te dedicás al detailing?"),
        (THEM, "Man, about five years now.", "Yyy, ya hace como 5 años que empecé."),
        (ME, "That's a long time!", "¡Un montón de tiempo!"),
        (ME, "First of all, let me just say your work looks amazing. I love what you've been building, and I thought it was the right time to show you what I put together for you.",
             "Primero dejame decirte que todo se ve espectacular. Me encantó lo que vienen armando y me pareció oportuno mostrarte lo que preparé para ustedes."),
    ]),
    ("Diagnosis", "Diagnóstico", [
        (ME, "Right now, are you running any kind of ads?", "Actualmente, ¿están corriendo algún tipo de anuncios?"),
        (THEM, "There's a girl who handles our Instagram.", "Hay una chica que se hace cargo del Instagram."),
        (ME, "Got it.", "Perfecto."),
        (ME, "Roughly how many inquiries are you getting per day?", "¿Cuántas consultas están teniendo por día más o menos?"),
        (THEM, "Hmm, maybe ten, but most of them are just shopping around.", "Yyy, unas 10 ponele, pero son curiosos."),
        (ME, "Right.", "Claro."),
        (ME, "And out of those ten, how many turn into serious customers?", "¿Y de esos 10 cuántos se convierten en clientes serios?"),
        (THEM, "Two.", "2."),
        (ME, "And how much are you spending on ads?", "¿Y cuánto están invirtiendo en anuncios?"),
        (THEM, "About fifteen hundred bucks a month.", "Unos 150 mil pesos."),
    ]),
    ("Spotting the opportunity", "Detección de oportunidad", [
        (ME, "Honestly, with the quality of work you're putting out, you should be getting fifteen to twenty inquiries a day.",
             "Sinceramente, con el nivel de trabajos que tienen deberían estar teniendo más de 15 a 20 consultas diarias."),
        (ME, "And usually the problem isn't the service.", "Y normalmente el problema no es el servicio."),
        (ME, "The problem is usually: how people see your brand, the follow-up, and how the inquiries come in.",
             "El problema suele ser: la percepción de la marca, el seguimiento y cómo llegan las consultas."),
        (ME, "Because most people come in through Instagram, ask for a price, and then ghost you.",
             "Porque la mayoría entra por Instagram, pregunta precio y desaparece."),
    ]),
    ("Business capacity", "Capacidad del negocio", [
        (ME, "And right now, how many clients could you handle per day? How many cars fit in the shop, Mike?",
             "¿Cuántos clientes podrían manejar por día? ¿Cuántos autos entran en el taller?"),
        (THEM, "We can fit about eight cars, so yeah, I've got room.", "Entran unos 8 autos, así que sí tengo espacio."),
        (ME, "Perfect, so there's room to scale.", "Perfecto, entonces hay margen para escalar."),
    ]),
    ("Presenting the solution", "Presentación de la solución", [
        (ME, "So here's the deal. With the businesses I work with, I set up the whole sales funnel, the advertising, the website, and the inquiry system.",
             "Con los negocios que trabajo armo todo el embudo de ventas, la publicidad, los sitios web y el sistema de consultas."),
        (ME, "The goal is to get you more SERIOUS inquiries and level up how people see your business.",
             "La idea es aumentar la cantidad de consultas SERIAS y mejorar la percepción del negocio."),
        (ME, "That's why I'd love to show it to you on a quick video call, a Google Meet, if that works for you.",
             "Por eso me gustaría mostrártelo por videollamada, un Google Meet si te parece bien."),
    ]),
    ("Close", "Cierre", [
        (THEM, "Yeah, sure.", "Sí dale."),
        (ME, "Perfect, Mike. I'm heading into a meeting with a dealership right now, and I'm free after 2 PM.",
             "Perfecto. Ahora me estoy yendo a una reunión con una concesionaria. Me desocupo después de las 2 de la tarde."),
        (ME, "How about 3 PM your time? Does that work?", "¿Tipo 3, hora tuya, te queda bien?"),
        (THEM, "Sounds good.", "Perfecto."),
        (ME, "Great. What's the best number to text you the link? I'll send it over right now.",
             "Genial. ¿A qué número te mando el link por mensaje? Te lo mando ya."),
    ]),
]

KEY_PHRASES = [
    ("I'll be quick so I don't take up your time.", "Te llamo rápido así no te robo tiempo."),
    ("I took the initiative.", "Tomé la iniciativa."),
    ("Your work looks amazing.", "Todo se ve espectacular."),
    ("How people see your brand / brand perception.", "La percepción de marca."),
    ("Serious inquiries / qualified leads.", "Consultas serias."),
    ("Sales funnel.", "Embudo de ventas."),
    ("Inquiry system / lead system.", "Sistema de consultas."),
]

OBJECTIONS = [
    ("“I'm not interested.”", "“No me interesa”", [
        ("Totally, I get it.", "De una, entiendo."),
        ("Before I let you go, just one quick question: are most of your inquiries coming in through Instagram right now?",
         "Igual antes de cortar te hago una consulta rápida: ¿hoy la mayoría de las consultas les llegan por Instagram?"),
    ]),
    ("“I already have someone doing my marketing.”", "“Ya tengo alguien que maneja marketing”", [
        ("Perfect.", "Perfecto."),
        ("Then you'll get what I put together really fast, because it's focused specifically on conversions and serious inquiries.",
         "Entonces seguramente vas a entender rápido lo que preparé porque está enfocado en conversión y consultas serias."),
    ]),
    ("“I don't need a website.”", "“No necesito página web”", [
        ("Yeah, a lot of detailers think that at first, because everything comes in through Instagram.",
         "Sí, muchos detailers arrancan pensando eso porque todo entra por Instagram."),
        ("But the problem usually isn't getting inquiries. It's turning them into better customers and leveling up how people see your business.",
         "Pero el problema normalmente no es recibir consultas. Es convertir mejores clientes y mejorar la percepción del negocio."),
    ]),
    ("“I don't have time.”", "“No tengo tiempo”", [
        ("Totally, that's exactly why I'm suggesting something super short.", "De una, por eso mismo te propongo algo súper corto."),
        ("Ten, fifteen minutes max, and I'll walk you through everything.", "10 o 15 minutos máximo y te muestro todo rápido."),
    ]),
]

# Extra: lo que te pueden preguntar en EE.UU. y no está en el guion original.
QUESTIONS = [
    ("“How much does it cost?”", "¿Cuánto sale?",
     "Great question. It depends on what your shop needs, which is exactly why I want to show you on the call. I'll walk you through the options and the pricing there, no pressure.",
     "Depende de lo que necesite el taller; justamente por eso te lo quiero mostrar en la llamada. Ahí te paso opciones y precios, sin compromiso."),
    ("“Where are you calling from?” / “Where are you based?”", "¿De dónde llamás?",
     "I'm based in Argentina, and I work remotely with detailers and dealerships in the US. Everything's done online, so it works just the same.",
     "Estoy en Argentina y trabajo a distancia con detailers y concesionarias de EE.UU. Todo es online, funciona igual."),
    ("“How did you get my number?”", "¿De dónde sacaste mi número?",
     "It's the number listed on your Google Business profile.", "Es el número que figura en su perfil de Google."),
    ("“Is this a sales call?”", "¿Es una llamada de venta?",
     "Kind of, yeah. I'll be honest with you, but I already built something for your shop and I just want to show it to you. If you don't like it, no hard feelings.",
     "Más o menos, sí, te soy sincero. Pero ya armé algo para tu taller y solo te lo quiero mostrar. Si no te gusta, no pasa nada."),
    ("“Just send me an email.”", "Mandame un mail.",
     "Sure, what's the best email? I'll also send a quick preview of the website. And would it be okay if I follow up on Thursday to see what you think?",
     "Dale, ¿cuál es el mejor mail? Te mando también una vista previa del sitio. ¿Te parece si te escribo el jueves para ver qué te pareció?"),
    ("“Can you send me the website now?”", "¿Me lo podés mandar ahora?",
     "I'd rather show it to you live, because I want to explain how the whole system works, not just the design. It only takes fifteen minutes.",
     "Prefiero mostrártelo en vivo, porque te quiero explicar cómo funciona todo el sistema, no solo el diseño. Son 15 minutos."),
    ("“Do you have any results / examples?”", "¿Tenés resultados o ejemplos?",
     "Yes, I'll show you real examples on the call, so you can see exactly what it looks like.",
     "Sí, en la llamada te muestro ejemplos reales para que veas cómo queda."),
    ("“Call me back later.”", "Llamame más tarde.",
     "No problem. What time works best for you, morning or afternoon?", "Sin problema. ¿Qué horario te queda mejor, mañana o tarde?"),
    ("“Sorry, I didn't catch that.” / “Can you repeat that?”", "No te entendí.",
     "Sure, no worries. Let me say that again.", "Sí, tranqui, te lo repito."),
]

TIPS = [
    ("Time zones: confirm the time in THEIR zone (“3 PM Eastern?”). Florida and New York are Eastern; Texas is Central; California is Pacific.",
     "Husos horarios: confirmá la hora en SU zona (“3 PM Eastern?”). Florida y Nueva York son Eastern; Texas, Central; California, Pacific."),
    ("In the US they use text messages more than WhatsApp: ask “Can I text you the link?”",
     "En EE.UU. usan más el SMS que WhatsApp: preguntá “Can I text you the link?”."),
    ("Don't say “they recommended you” unless it's true: if they ask who, the call is over. “I came across your shop on Google” works just as well.",
     "No digas “me recomendaron” si no es verdad: si te preguntan quién, se cae la llamada. “Los encontré en Google” funciona igual de bien."),
    ("Speak a little slower than feels natural and smile while you talk. Your accent is fine: clarity matters more than sounding American.",
     "Hablá un poco más lento de lo que te sale y sonriendo. El acento no es problema: importa más que se entienda que sonar yanqui."),
    ("Call the business number from Google Maps, by hand. Don't use an auto-dialer or robocalls to cell phones (TCPA law).",
     "Llamá al número del negocio que figura en Maps, a mano. No uses marcador automático ni mensajes grabados a celulares (ley TCPA)."),
]

def e(s): return html.escape(s, quote=False)

def lines(rows):
    out = []
    for who, en, es in rows:
        if who == NOTE:
            out.append(f'<div class="note">{e(en)} <span>· {e(es)}</span></div>')
            continue
        out.append(f'<div class="line {who.lower()}"><div class="who">{who}</div><div><p class="en">{e(en)}</p><p class="es">{e(es)}</p></div></div>')
    return "".join(out)

body = ['<header><div class="eyebrow">AGENCIA · COLD CALL SCRIPT · US</div><h1>Car Detailers Call Script</h1>'
        '<p class="sub">Inglés de EE.UU. arriba, original en español abajo. Los nombres (Mike) y números son ejemplos.</p></header>']
for i, (t_en, t_es, rows) in enumerate(SECTIONS, 1):
    body.append(f'<section><h2><em>{i:02d}</em>{e(t_en)} <span>· {e(t_es)}</span></h2>{lines(rows)}</section>')

body.append('<section class="break"><h2><em>★</em>Key phrases <span>· Frases clave</span></h2>' + "".join(
    f'<div class="kp"><p class="en">{e(en)}</p><p class="es">{e(es)}</p></div>' for en, es in KEY_PHRASES) + '</section>')

obj = []
for q_en, q_es, rows in OBJECTIONS:
    obj.append(f'<div class="obj"><h3>{e(q_en)} <span>· {e(q_es)}</span></h3>{lines([(ME, en, es) for en, es in rows])}</div>')
body.append('<section><h2><em>!</em>Objections <span>· Objeciones</span></h2>' + "".join(obj) + '</section>')

qs = "".join(f'<div class="obj"><h3>{e(q)} <span>· {e(qe)}</span></h3>{lines([(ME, a, ae)])}</div>' for q, qe, a, ae in QUESTIONS)
body.append('<section class="break"><h2><em>?</em>Questions they might ask <span>· Preguntas que te pueden hacer</span></h2>' + qs + '</section>')

body.append('<section><h2><em>i</em>Calling the US <span>· Para llamar a EE.UU.</span></h2>' + "".join(
    f'<div class="kp"><p class="en">{e(en)}</p><p class="es">{e(es)}</p></div>' for en, es in TIPS) + '</section>')

CSS = """
@page { size: letter; margin: 0.55in 0.6in; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: Inter, Arial, sans-serif; color: #15151a; font-size: 10pt; }
header { border-bottom: 1.5pt solid #15151a; padding-bottom: 10pt; margin-bottom: 6pt; }
.eyebrow { font-size: 7.8pt; font-weight: 700; letter-spacing: .1em; color: #2f55e4; }
h1 { font-size: 22pt; font-weight: 800; margin-top: 4pt; }
.sub { color: #6b6b76; font-size: 9pt; margin-top: 3pt; }
section { margin-top: 14pt; }
section.break { break-before: page; margin-top: 0; }
h2 { font-size: 13pt; font-weight: 800; margin-bottom: 7pt; break-after: avoid; }
h2 em { font-style: normal; color: #2f55e4; margin-right: 8pt; }
h2 span, h3 span, .note span { color: #8a8a95; font-weight: 500; }
h3 { font-size: 10.5pt; font-weight: 700; margin-bottom: 4pt; break-after: avoid; }
.line { display: grid; grid-template-columns: 38pt 1fr; gap: 8pt; padding: 5pt 0; border-top: .5pt solid #ececf0; break-inside: avoid; }
.who { font-size: 6.8pt; font-weight: 800; letter-spacing: .08em; padding-top: 3pt; color: #2f55e4; }
.them .who { color: #9a9aa5; }
.en { font-size: 10.6pt; font-weight: 600; line-height: 1.4; }
.them .en { font-weight: 400; color: #4a4a55; font-style: italic; }
.es { font-size: 8.4pt; color: #8a8a95; line-height: 1.4; margin-top: 2pt; }
.note { break-after: avoid; font-size: 8.6pt; font-weight: 700; color: #b4540a; padding: 5pt 0 2pt; }
.kp { padding: 6pt 0; border-top: .5pt solid #ececf0; break-inside: avoid; }
.obj { background: #f6f7fb; border-radius: 6pt; padding: 9pt 11pt 5pt; margin-bottom: 8pt; break-inside: avoid; }
.obj .line { border-top: none; padding: 3pt 0; }
"""

doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Car Detailers Call Script</title><style>{CSS}</style></head><body>{''.join(body)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "Script_CarDetailers_EN-ES.pdf"
subprocess.run(["/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={pdf}", str(src)], check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
