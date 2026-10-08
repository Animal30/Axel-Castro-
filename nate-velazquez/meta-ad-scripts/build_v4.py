# Genera los guiones de anuncios de Meta de Nate (HTML -> PDF), versión que cumple las políticas de salud de Meta.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

CTA = "Tap 'Apply Now' below. Answer 3 quick questions and I'll call you within 24 hours."
ADS = [
    dict(title="The Monday Restart", angle="Talking Head + B-roll · Relatable angle", length="25-35 sec",
         hook="Monday: \u2018This week I'm eating better.\u2019 Friday: takeout on the couch. Sound familiar?",
         alts=["If every Monday feels like starting over, this is for you.",
               "Sunday night: \u2018Tomorrow I start.\u2019 We've all been there.",
               "Almost every client I coach started exactly here."],
         core=["Monday you're all in. Wednesday a late meeting hits. Friday it's takeout, and Sunday night it's \u201cI'll start again Monday.\u201d",
               "If that's your week, you're not lazy and you're not alone. Almost every person I coach started right there.",
               "I'm Nate, and I coach people whose calendars run their lives, here in Tampa.",
               "With the Flex Week Method, we stop planning for the perfect week. We plan for Wednesday's late meeting and Friday's takeout, so one rough day never turns into starting over.",
               "Every week we check in and adjust. You're never figuring it out alone.",
               "A client said it best: \u201cNate was the first coach who made me feel understood, not judged. The accountability changed everything.\u201d"],
         cta=CTA),
    dict(title="Every Diet You've Tried Worked", angle="Talking Head + B-roll · Reframe angle", length="25-35 sec",
         hook="Every diet you've tried worked. That's the problem.",
         alts=["I stopped giving my clients meal plans. Here's why.",
               "Three weeks in, every diet falls apart. Here's why.",
               "Most diets are built for a perfect week. Nobody I coach has one."],
         core=["It worked for three weeks, because it was built for a perfect week. Nobody I coach has one.",
               "Then a work dinner, a birthday, a busy Tuesday… and you're back to square one.",
               "It's not you. It's what you were handed.",
               "I'm Nate, and I coach people whose calendars run their lives, here in Tampa.",
               "With the Flex Week Method, nothing is off the table: we start with the food you already eat, adjust every week, and when the week falls apart, you're not figuring it out alone.",
               "In a client's words: \u201cBest coach I've ever had. For the first time, I didn't quit. The accountability made it stick.\u201d"],
         cta=CTA),
    dict(title="What A Busy Day Of Eating Actually Looks Like", angle="Day-in-the-life · Relatable angle", length="30-40 sec",
         hook="Back-to-back meetings, no time to cook… here's how my clients still eat well on days like this.",
         alts=["7:02 AM. No time for breakfast. Here's what my clients do instead.",
               "If your calendar runs your life, this is what eating well actually looks like.",
               "No meal prep. No perfect days. Here's a real day of eating for my clients."],
         core=["7:02 AM: coffee and a protein shake in the car. Done.",
               "12:30: lunch between calls. A grocery-store wrap and a piece of fruit. Five minutes.",
               "4:00: the snack that keeps you from ordering takeout at 9.",
               "7:30: a dinner you actually like, ready in fifteen minutes.",
               "I'm Nate, nutrition coach in Tampa. No perfect days needed. This is what my clients' weekly check-ins look like.",
               "And in their words: \u201cNate kept me accountable every single week. I finally stayed consistent.\u201d"],
         cta=CTA),
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
  <div class="box"><div class="bh"><em>01</em>THE HOOK</div><p class="hook">“{esc(a["hook"])}”</p>
    <div class="alts"><span>ALTERNATE HOOKS · SAME VIDEO, TEST THE FIRST 3 SECONDS</span>{"".join(f"<p>“{esc(h)}”</p>" for h in a["alts"])}</div></div>
  <div class="box"><div class="bh"><em>02</em>CORE MESSAGE</div><div class="core">{core}</div></div>
  <div class="box cta"><div class="bh"><em>03</em>CALL TO ACTION</div><p class="hook">“{esc(a["cta"])}”</p></div>
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
.alts { margin-top: 9pt; padding-top: 8pt; border-top: .75pt solid #22222b; }
.alts span { display: block; font-size: 6.8pt; font-weight: 700; letter-spacing: .08em; color: #67666f; margin-bottom: 4pt; }
.alts p { font-size: 8.8pt; color: #a6a6b3; line-height: 1.6; }
.box.note p { font-size: 8.2pt; color: #a6a6b3; font-style: italic; line-height: 1.7; }
"""

doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Nate Velazquez Meta Ad Scripts</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "NateVelazquez_MetaAdScripts_v4.pdf"
subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
