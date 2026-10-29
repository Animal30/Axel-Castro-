# Genera el guion del reel del caso Isa Franco Motos (8 a 32 motos en un mes) y su caption (HTML -> PDF).
import html, pathlib, shutil, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

HOOK = "De 8 motos vendidas a 32. En un solo mes. ¿Querés saber cómo lo hicimos?"
ALT_HOOK = "¿Querés saber cómo esta concesionaria pasó de vender 8 motos a 32 en un solo mes?"

# (bloque, toma, líneas habladas)
BEATS = [
    ("GANCHO", "Frente al local, caminando hacia cámara. Placa “8 → 32” desde el primer cuadro.",
     ["De 8 motos vendidas a 32. En un solo mes.", "¿Querés saber cómo lo hicimos?"]),
    ("LA MARCA", "Toma abierta del salón, las motos.",
     ["Esto es Isa Franco Motos."]),
    ("EL PROBLEMA", "Vos al lado de una moto. Cortá a una toma de apoyo a mitad de la línea larga.",
     ["Consultas tenían un montón, pero la mayoría eran curiosos que preguntaban el precio, les respondías y nunca más aparecían.",
      "Horas perdidas."]),
    ("PASO 1 · EL SITIO", "Celular en mano navegando el sitio: ficha de una moto, después el formulario.",
     ["Paso uno: un sitio web hecho para vender.",
      "Cada moto con su ficha y su precio.",
      "Y antes de hablar con un vendedor, el cliente te dice qué moto busca, cómo la piensa pagar y cuándo la quiere.",
      "El curioso se filtra solo.",
      "Al vendedor le llega alguien listo para cerrar."]),
    ("PASO 2 · META", "Pantalla con los anuncios o el administrador de Meta. Un anuncio corriendo en el celular.",
     ["Paso dos: anuncios en Facebook e Instagram.",
      "Directo a la gente que ya está buscando moto.",
      "Presupuesto del mes: 500 mil pesos."]),
    ("RESULTADO", "Vos en el salón, plano medio. Pausa antes del número. Apoyo: entrega de llaves.",
     ["¿Resultado? 32 motos vendidas, cuatro veces más, con el mismo local y el mismo equipo."]),
    ("CIERRE", "Mirando a cámara, plano cerrado.",
     ["¿Tenés una concesionaria? Comentame MOTOS.", "Vemos cómo hacer que tus 8 sean 32."]),
]

CARDS = [
    ("0:00", "8 → 32 MOTOS EN UN MES"),
    ("0:07", "EL PROBLEMA: CURIOSOS"),
    ("0:15", "PASO 1 · SITIO QUE FILTRA"),
    ("0:22", "QUÉ MOTO · CÓMO PAGA · CUÁNDO"),
    ("0:31", "PASO 2 · META ADS"),
    ("0:37", "PRESUPUESTO: $500.000"),
    ("0:41", "32 MOTOS · x4"),
    ("0:48", "COMENTÁ “MOTOS”"),
]

TIPS = [
    "Arrancá ya en movimiento. Nada de “hola” ni presentación: el video empieza en el número.",
    "Cambiá la toma en cada línea larga (problema, filtro del sitio, resultado). Apoyo: motos en detalle, el sitio en el celular, entrega de llaves.",
    "El “32” decilo despacio, con una pausa antes. Es el momento del video.",
    "Tono firme y tranquilo, sin gritar. Lo premium es la seguridad, no la energía.",
    "Placas en la franja del medio: nada arriba de 230 px ni debajo de 1440 px, y libres los 230 px de la derecha.",
]

CAPTION = """¿Tenés una concesionaria y te escriben muchos curiosos? Comentá MOTOS y te cuento cómo lo resolvimos acá.

Isa Franco Motos vendía 8 motos por mes. Consultas tenían, pero la mayoría preguntaba el precio y desaparecía.

Hicimos dos cosas. Un sitio web pensado para captar clientes, donde antes de hablar con un vendedor la persona cuenta qué moto busca, cómo la piensa pagar y cuándo la quiere. Y anuncios en Meta, en Facebook e Instagram, llevando a esa gente directo al sitio.

Presupuesto del mes: 500 mil pesos. Resultado: 32 motos vendidas. Mismo local, mismo equipo.

Si querés este sistema de marketing para concesionarias en tu negocio, comentá MOTOS y te escribo.

#marketingparaconcesionarias #concesionaria #motos #metaads"""

def esc(s): return html.escape(s, quote=False)
def kw(s): return s.replace("MOTOS", '<span class="kw">MOTOS</span>')

beats = "".join(f'''<div class="beat"><div class="bl"><b>{esc(b)}</b><span>{esc(t)}</span></div>
  <div class="br">{"".join(f"<p>{kw(esc(l))}</p>" for l in ls)}</div></div>''' for b, t, ls in BEATS)
cards = "".join(f"<div class='card'><span>{t}</span><b>{esc(c)}</b></div>" for t, c in CARDS)
tips = "".join(f"<li>{esc(t)}</li>" for t in TIPS)
caption = "".join(f"<p>{kw(esc(p))}</p>" for p in CAPTION.split("\n\n"))

head = '''<div class="eyebrow">ISA FRANCO MOTOS · CASO DE ÉXITO</div>'''
foot = lambda n: f'<div class="foot"><span>NAHUEL CASARTELLI · MARKETING PARA CONCESIONARIAS</span><span>{n:02d} / 02</span></div>'

page1 = f'''<section class="page">{head}
  <div class="top"><span class="sc"><i></i>GUION DE REEL</span><span class="tag">IG + FACEBOOK</span></div>
  <h2>De 8 a 32 motos en un mes</h2>
  <div class="angle">Sitio web que filtra curiosos + anuncios en Meta · grabado en el local</div>
  <div class="facts">
    <div><span>FORMATO</span><b>Reel 9:16, a cámara</b></div>
    <div><span>DURACIÓN</span><b>45-50 seg</b></div>
    <div><span>PRESUPUESTO</span><b>$500.000 / mes</b></div>
    <div><span>PALABRA CLAVE</span><b class="kw">MOTOS</b></div>
  </div>
  <div class="box"><div class="bh"><em>01</em>EL GANCHO</div><p class="hook">“{esc(HOOK)}”</p>
    <div class="alts"><span>GANCHO ALTERNATIVO · PARA PROBAR</span><p>“{esc(ALT_HOOK)}”</p></div></div>
  <div class="box"><div class="bh"><em>02</em>GUION COMPLETO</div>{beats}</div>
  {foot(1)}
</section>'''

page2 = f'''<section class="page">{head}
  <div class="top"><span class="sc"><i></i>PANTALLA, GRABACIÓN Y CAPTION</span><span class="tag">IG + FACEBOOK</span></div>
  <div class="box"><div class="bh"><em>03</em>TEXTO EN PANTALLA · 6 PALABRAS MÁX.</div><div class="cards">{cards}</div></div>
  <div class="box"><div class="bh"><em>04</em>CÓMO GRABARLO PARA QUE SE VEA PREMIUM</div><ul>{tips}</ul></div>
  <div class="box cta"><div class="bh"><em>05</em>CAPTION · LISTO PARA PEGAR</div><div class="cap">{caption}</div></div>
  {foot(2)}
</section>'''

CSS = """
@page { size: letter; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0b0b0d; font-family: Inter, Arial, sans-serif; color: #f4f2ee; }
.page { width: 8.5in; height: 11in; padding: 0.62in 0.62in 0.6in; position: relative; overflow: hidden; break-after: page; background: #0b0b0d; }
.page:last-child { break-after: auto; }
.eyebrow { font-size: 8.2pt; font-weight: 700; letter-spacing: .1em; color: #c9a45c; }
.foot { position: absolute; left: .62in; right: .62in; bottom: .42in; display: flex; justify-content: space-between; border-top: .75pt solid #24221e; padding-top: 10pt; font-size: 7.1pt; letter-spacing: .06em; color: #6d6a63; }
.tag { font-size: 7.3pt; font-weight: 700; letter-spacing: .1em; padding: 3pt 9pt; border-radius: 10pt; color: #c9a45c; background: rgba(201,164,92,.14); }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 14pt; }
.sc { font-size: 8.2pt; font-weight: 700; letter-spacing: .08em; color: #c9a45c; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #c9a45c; display: inline-block; }
h2 { font-size: 21pt; font-weight: 800; margin-top: 8pt; line-height: 1.2; }
.angle { color: #a9a59c; font-size: 10pt; margin-top: 4pt; }
.facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin-top: 12pt; }
.facts div { background: #141412; border: .75pt solid #262420; border-radius: 6pt; padding: 9pt 10pt 11pt; }
.facts span { display: block; font-size: 7.1pt; letter-spacing: .06em; color: #6d6a63; margin-bottom: 7pt; }
.facts b { font-size: 9.4pt; font-weight: 700; }
.kw { color: #c9a45c; font-weight: 700; }
.box { background: #141412; border: .75pt solid #262420; border-radius: 7pt; padding: 11pt 13pt; margin-top: 9pt; }
.bh { font-size: 7.9pt; font-weight: 700; letter-spacing: .08em; color: #6d6a63; margin-bottom: 7pt; }
.bh em { font-style: normal; color: #c9a45c; font-size: 9.8pt; margin-right: 7pt; }
.hook { font-size: 11pt; font-weight: 700; line-height: 1.45; }
.alts { margin-top: 8pt; padding-top: 7pt; border-top: .75pt solid #262420; }
.alts span { display: block; font-size: 6.8pt; font-weight: 700; letter-spacing: .08em; color: #6d6a63; margin-bottom: 3pt; }
.alts p { font-size: 8.8pt; color: #a9a59c; line-height: 1.55; }
.beat { display: grid; grid-template-columns: 1.55in 1fr; gap: 12pt; padding: 5pt 0; border-top: .75pt solid #22201c; }
.beat:first-of-type { border-top: 0; padding-top: 0; }
.bl b { display: block; font-size: 7.6pt; letter-spacing: .08em; color: #c9a45c; }
.bl span { display: block; font-size: 7pt; color: #6d6a63; line-height: 1.35; margin-top: 3pt; font-style: italic; }
.br p { font-size: 9.2pt; line-height: 1.42; }
.br p + p { margin-top: 2pt; }
.cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6pt; }
.card { display: flex; gap: 10pt; align-items: baseline; background: #0f0f0e; border: .75pt solid #262420; border-radius: 5pt; padding: 7pt 9pt; }
.card span { font-size: 7.4pt; color: #6d6a63; font-weight: 700; }
.card b { font-size: 9pt; letter-spacing: .03em; }
ul { padding-left: 13pt; }
li { font-size: 9pt; color: #a9a59c; line-height: 1.6; }
li + li { margin-top: 3pt; }
.box.cta { background: #17140d; border-color: #4a3d22; }
.cap p { font-size: 9pt; color: #d9d5cc; line-height: 1.6; }
.cap p + p { margin-top: 6pt; }
"""

doc = f"<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><title>Isa Franco Motos · Caso 8 a 32</title><style>{FONTS}</style><style>{CSS}</style></head><body>{page1}{page2}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "IsaFrancoMotos_Caso8a32_Guion.pdf"
chrome = next((p for p in ["/opt/pw-browsers/chromium/chrome-linux/chrome", "/opt/pw-browsers/chromium",
                           shutil.which("chromium") or "", shutil.which("google-chrome") or ""]
               if p and pathlib.Path(p).is_file()), None)
subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
