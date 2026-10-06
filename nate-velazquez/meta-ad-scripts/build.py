# Genera los guiones de anuncios de Meta de Nate (HTML -> PDF), versión que cumple las políticas de salud de Meta.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

ADS = [
    dict(title="Same Calories, Two Very Different Days", angle="Visual Demo · Pattern-interrupt angle", length="25-35 sec",
         hook="These two breakfasts have the same calories. Only one of them gets you to lunch without raiding the snack drawer.",
         core=["Left: a muffin and a vanilla latte. Gone in four minutes.",
               "Right: eggs, toast, fruit and Greek yogurt. Same calories. Way more food.",
               "My name's Nate. I've been coaching busy professionals here in Tampa for over 10 years, and this is what most people are never shown.",
               "It's not about eating less. It's about knowing what to put on the plate, so your day runs on food instead of willpower.",
               "That's what I build with my clients: a plan around the food you already like and the schedule you actually have."],
         cta="If you want a plan built around your real life, tap the link and let's talk.",
         note="Open on the two plates side by side, overhead, no intro. Put the calorie number on each plate on screen (weigh them so they truly match). Then cut to Nate at eye level. Show food only: no bodies, no scale, no measuring tape."),
    dict(title="You Don't Need Another Diet", angle="Talking Head · Contrarian angle", length="25-35 sec",
         hook="Unpopular opinion from a nutrition coach: another diet is the last thing you need.",
         core=["Every diet works for about three weeks. Then a work dinner, a birthday, a busy Tuesday… and it's over.",
               "That's not a discipline problem. Diets aren't built for real life.",
               "I'm Nate. I coach busy professionals here in Tampa, and I don't hand out meal plans you'll quit by Friday.",
               "We build habits around your schedule, your family and the food you enjoy, with a weekly check-in so you never figure it out alone.",
               "No foods off the table. Just a plan you can actually keep."],
         cta="If you're done starting over every Monday, tap the link and we'll talk.",
         note="Say the hook straight into the lens with a half-smile, like you know it's a bold take. Pause after \"real life.\" Kitchen or clean office background. Talk about habits and food, never about weight or body changes."),
    dict(title="What A Busy Day Of Eating Actually Looks Like", angle="Day-in-the-life · Relatable angle", length="30-40 sec",
         hook="Back-to-back meetings, no time to cook… here's how my clients still eat well on days like this.",
         core=["7am: coffee and a protein shake in the car. Done.",
               "Lunch between calls: a grocery-store wrap and a piece of fruit. Five minutes.",
               "4pm: the snack that keeps you from ordering takeout at 9.",
               "Dinner: something you actually like, ready in fifteen minutes.",
               "I'm Nate, nutrition coach for busy professionals in Tampa. No perfect days needed. Just a simple plan that works on the messy ones."],
         cta="Want a plan like this built for your schedule? Tap the link and let's talk.",
         note="Quick cuts every 2-3 seconds, real locations (car, office, grocery store, kitchen), phone in hand, time on screen for each moment. Food and hands only, no body shots. Close on Nate to camera for the last line."),
]

def esc(s): return html.escape(s, quote=False)
N = len(ADS)
pages = []
for i, a in enumerate(ADS):
    core = "".join(f"<p>{esc(p)}</p>" for p in a["core"])
    pages.append(f'''<section class="page">
  <div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
  <div class="top"><span class="sc"><i></i>AD {i+1} OF {N}</span><span class="tag">PAID AD</span></div>
  <div class="vs">META AD SCRIPT</div>
  <h2>{esc(a["title"])}</h2>
  <div class="angle">{esc(a["angle"])}</div>
  <div class="facts">
    <div><span>FORMAT</span><b>{esc(a["angle"].split(" · ")[0])}</b></div>
    <div><span>LENGTH</span><b>{a["length"]}</b></div>
    <div><span>CHANNEL</span><b>Meta Ads (IG + FB)</b></div>
    <div><span>OBJECTIVE</span><b class="kw">Lead Gen</b></div>
  </div>
  <div class="box"><div class="bh"><em>01</em>THE HOOK</div><p class="hook">“{esc(a["hook"])}”</p></div>
  <div class="box"><div class="bh"><em>02</em>CORE MESSAGE</div><div class="core">{core}</div></div>
  <div class="box cta"><div class="bh"><em>03</em>CALL TO ACTION</div><p class="hook">“{esc(a["cta"])}”</p></div>
  <div class="box note"><div class="bh">DIRECTOR'S NOTE</div><p>{esc(a["note"])}</p></div>
  <div class="foot"><span>NATE VELAZQUEZ · META AD SCRIPT</span><span>{i+1:02d} / {N:02d}</span></div>
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

doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Nate Velazquez Meta Ad Scripts</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "NateVelazquez_MetaAdScripts_v2.pdf"
subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
