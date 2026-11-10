# Genera el guion del anuncio "10 Minutes. No Gym." (HTML -> PDF), con el mismo formato que
# NateVelazquez_MetaAdScripts_v4.pdf. Armado con escenas de "Sam - 10 Min Fat Burning (2 min) 9x16.mp4";
# Sam graba las frases nuevas y el B-roll sale de ese video. Uso: python3 build.py [fonts.css]
import html, pathlib, subprocess, sys, glob

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
OUT = "IronBird_10MinNoGym_AdScript.pdf"

ADS = [
    dict(title="10 Minutes. No Gym.", angle="Talking Head + B-roll · Value-first angle",
         fmt="Talking Head + B-roll", length="30-45 sec",
         hook="You don't need a gym to work your core. You need ten minutes and a wall.",
         alts=["Give me ten minutes and I'll give you a workout you can do anywhere.",
               "Busy week? This is the workout I'd do if I only had ten minutes.",
               "Four moves, ten minutes, zero equipment."],
         core=["Here's the order: knees to the wall, push-ups, sit-ups with crunches, and a plank to finish.",
               "Three to five rounds. If you're just starting, one round is enough. Do it right before you do it fast.",
               "But this workout is only one piece. Real results show up when your training, your nutrition and how much you move during the day all line up.",
               "I'm Sam, owner of Iron Bird Fitness, and that's exactly what I build with my clients here in Fresno: a plan around your schedule, one-on-one."],
         cta="Want me to build that plan for you? Tap 'Apply Now' below and my team will reach out."),
]

e = lambda s: html.escape(s, quote=False)
N = len(ADS)
pages = []
for i, a in enumerate(ADS):
    core = "".join(f"<p>{e(p)}</p>" for p in a["core"])
    pages.append(f'''<section class="page">
  <div class="eyebrow">IRON BIRD FITNESS · @IRONBIRDFIT</div>
  <div class="top"><span class="sc"><i></i>AD {i+1} OF {N}</span><span class="tag">PAID AD</span></div>
  <div class="vs">META AD SCRIPT</div>
  <h2>{e(a["title"])}</h2>
  <div class="angle">{e(a["angle"])}</div>
  <div class="facts">
    <div><span>FORMAT</span><b>{e(a["fmt"])}</b></div>
    <div><span>LENGTH</span><b>{a["length"]}</b></div>
    <div><span>CHANNEL</span><b>Meta Ads (IG + FB)</b></div>
    <div><span>OBJECTIVE</span><b class="kw">Lead Gen</b></div>
  </div>
  <div class="box"><div class="bh"><em>01</em>THE HOOK</div><p class="hook">“{e(a["hook"])}”</p>
    <div class="alts"><span>ALTERNATE HOOKS · SAME VIDEO, TEST THE FIRST 3 SECONDS</span>{"".join(f"<p>“{e(h)}”</p>" for h in a["alts"])}</div></div>
  <div class="box"><div class="bh"><em>02</em>CORE MESSAGE</div><div class="core">{core}</div></div>
  <div class="box cta"><div class="bh"><em>03</em>CALL TO ACTION</div><p class="hook">“{e(a["cta"])}”</p></div>
  <div class="foot"><span>IRON BIRD FITNESS · META AD SCRIPT</span><span>{i+1:02d} / {N:02d}</span></div>
</section>''')

CSS = """
@page { size: 8.5in 11in; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0b0b0f; font-family: Inter, Arial, sans-serif; color: #f3f3f5; }
.page { width: 8.5in; height: 11in; padding: .62in .61in; position: relative; overflow: hidden; break-after: page; background: #0b0b0f; }
.page:last-child { break-after: auto; }
.eyebrow { font-size: 7.4pt; font-weight: 700; letter-spacing: .1em; color: #5b7cff; }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 16pt; }
.sc { font-size: 7.4pt; font-weight: 700; letter-spacing: .1em; color: #5b7cff; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #5b7cff; display: inline-block; }
.tag { font-size: 6.6pt; font-weight: 700; letter-spacing: .1em; color: #f5c518; background: #2b2812; border-radius: 9pt; padding: 3.5pt 8pt; }
.vs { font-size: 7.2pt; font-weight: 700; letter-spacing: .08em; color: #74747e; margin-top: 10pt; }
h2 { font-size: 21.5pt; font-weight: 800; line-height: 1.2; margin-top: 5pt; letter-spacing: -.01em; }
.angle { color: #a2a2ac; font-size: 10pt; margin-top: 4pt; }
.facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin-top: 14pt; }
.facts div { background: #131318; border: .75pt solid #26262e; border-radius: 5pt; padding: 10pt 10pt 13pt; }
.facts span { display: block; font-size: 6.4pt; letter-spacing: .08em; color: #74747e; margin-bottom: 9pt; }
.facts b { font-size: 9.6pt; font-weight: 700; }
.kw { color: #5b7cff; font-weight: 700; }
.box { background: #131318; border: .75pt solid #26262e; border-radius: 6pt; padding: 13pt 13pt 15pt; margin-top: 9pt; }
.bh { font-size: 7.2pt; font-weight: 700; letter-spacing: .08em; color: #74747e; margin-bottom: 8pt; }
.bh em { font-style: normal; color: #5b7cff; font-size: 9.5pt; margin-right: 8pt; }
.hook { font-size: 10.4pt; font-weight: 700; line-height: 1.45; }
.alts { border-top: .75pt solid #26262e; margin-top: 11pt; padding-top: 10pt; }
.alts span { display: block; font-size: 6.4pt; font-weight: 700; letter-spacing: .08em; color: #74747e; margin-bottom: 5pt; }
.alts p { font-size: 8.6pt; color: #b9b9c2; line-height: 1.6; }
.core p { font-size: 8.3pt; color: #a2a2ac; line-height: 1.7; }
.core p + p { margin-top: 6pt; }
.box.cta { background: #10142a; border-color: #2a3466; }
.foot { position: absolute; left: .61in; right: .61in; bottom: .4in; border-top: .75pt solid #1d1d24; padding-top: 7pt; display: flex; justify-content: space-between; font-size: 6.4pt; letter-spacing: .08em; color: #5a5a64; }
"""
doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Iron Bird Fitness · Meta Ad Script</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
chrome = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome"))[-1]
subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000",
                f"--print-to-pdf={HERE/OUT}", str(src)], check=True, stderr=subprocess.DEVNULL)
src.unlink(); print(HERE/OUT)
