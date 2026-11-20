# Genera la hoja de grabación para Sam del anuncio "10 Minutes. No Gym." (HTML -> PDF),
# con el mismo estilo que IronBird_10MinNoGym_AdScript.pdf. Uso: python3 build_recording.py [fonts.css]
import html, pathlib, subprocess, sys, glob

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
OUT = "IronBird_10MinNoGym_RecordingScript.pdf"

SETUP = ["Wear the Iron Bird tank, same gym corner as the 10-minute workout video.",
         "Phone vertical (9:16), at eye level, good light on your face.",
         "Say each line straight to camera. Short pause between lines; we cut those out in editing.",
         "Do each line 2 or 3 times so we can pick the best take."]

LINES = ["You don't need a gym to work your core. You need ten minutes and a wall.",
         "Here's the order: knees to the wall, push-ups, sit-ups with crunches, and a plank to finish.",
         "Three to five rounds. If you're just starting, one round is enough. Do it right before you do it fast.",
         "But this workout is only one piece. Real results show up when your training, your nutrition and how much you move during the day all line up.",
         "I'm Sam, owner of Iron Bird Fitness, and that's exactly what I build with my clients here in Fresno: a plan around your schedule, one-on-one.",
         "Want me to build that plan for you? Tap “Apply Now” below and my team will reach out."]

HOOKS = ["Give me ten minutes and I'll give you a workout you can do anywhere.",
         "Busy week? This is the workout I'd do if I only had ten minutes.",
         "Four moves, ten minutes, zero equipment."]

e = lambda s: html.escape(s, quote=False)
page = f'''<section class="page">
  <div class="eyebrow">IRON BIRD FITNESS · @IRONBIRDFIT</div>
  <div class="top"><span class="sc"><i></i>FOR SAM</span><span class="tag">RECORDING</span></div>
  <div class="vs">RECORDING SCRIPT</div>
  <h2>10 Minutes. No Gym.</h2>
  <div class="angle">Read the lines in order, straight to camera</div>
  <div class="facts">
    <div><span>FORMAT</span><b>Talking Head</b></div>
    <div><span>LENGTH</span><b>30-45 sec</b></div>
    <div><span>VIDEO</span><b>Vertical 9:16</b></div>
    <div><span>TAKES</span><b class="kw">2-3 per line</b></div>
  </div>
  <div class="box"><div class="bh"><em>01</em>RECORDING SETUP</div><div class="core">{"".join(f"<p>{e(s)}</p>" for s in SETUP)}</div></div>
  <div class="box"><div class="bh"><em>02</em>THE SCRIPT · READ IT IN THIS ORDER</div>
    <ol>{"".join(f"<li><b>{n:02d}</b><p>{e(l)}</p></li>" for n, l in enumerate(LINES, 1))}</ol></div>
  <div class="box cta"><div class="bh"><em>03</em>EXTRA HOOKS · RECORD THESE TOO, TO TEST DIFFERENT OPENINGS</div>
    <div class="alts">{"".join(f"<p>{e(h)}</p>" for h in HOOKS)}</div></div>
  <div class="foot"><span>IRON BIRD FITNESS · RECORDING SCRIPT</span><span>01 / 01</span></div>
</section>'''

CSS = """
@page { size: 8.5in 11in; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0b0b0f; font-family: Inter, Arial, sans-serif; color: #f3f3f5; }
.page { width: 8.5in; height: 11in; padding: .62in .61in; position: relative; overflow: hidden; background: #0b0b0f; }
.eyebrow { font-size: 7.4pt; font-weight: 700; letter-spacing: .1em; color: #5b7cff; }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 16pt; }
.sc { font-size: 7.4pt; font-weight: 700; letter-spacing: .1em; color: #5b7cff; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #5b7cff; display: inline-block; }
.tag { font-size: 6.6pt; font-weight: 700; letter-spacing: .1em; color: #f5c518; background: #2b2812; border-radius: 9pt; padding: 3.5pt 8pt; }
.vs { font-size: 7.2pt; font-weight: 700; letter-spacing: .08em; color: #74747e; margin-top: 10pt; }
h2 { font-size: 21.5pt; font-weight: 800; line-height: 1.2; margin-top: 5pt; letter-spacing: -.01em; }
.angle { color: #a2a2ac; font-size: 10pt; margin-top: 4pt; }
.facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin-top: 12pt; }
.facts div { background: #131318; border: .75pt solid #26262e; border-radius: 5pt; padding: 10pt 10pt 13pt; }
.facts span { display: block; font-size: 6.4pt; letter-spacing: .08em; color: #74747e; margin-bottom: 9pt; }
.facts b { font-size: 9.6pt; font-weight: 700; }
.kw { color: #5b7cff; font-weight: 700; }
.box { background: #131318; border: .75pt solid #26262e; border-radius: 6pt; padding: 13pt 13pt 15pt; margin-top: 9pt; }
.bh { font-size: 7.2pt; font-weight: 700; letter-spacing: .08em; color: #74747e; margin-bottom: 8pt; }
.bh em { font-style: normal; color: #5b7cff; font-size: 9.5pt; margin-right: 8pt; }
.core p { font-size: 8.3pt; color: #a2a2ac; line-height: 1.5; }
.core p + p { margin-top: 1pt; }
ol { list-style: none; }
li { display: flex; gap: 10pt; align-items: baseline; padding: 4pt 0; }
li + li { border-top: .75pt solid #1f1f26; }
li b { color: #5b7cff; font-size: 8.6pt; font-weight: 700; min-width: 14pt; }
li p { font-size: 10.4pt; font-weight: 700; line-height: 1.4; }
.alts p { font-size: 9pt; color: #d6d6de; line-height: 1.6; font-weight: 600; }
.box.cta { background: #10142a; border-color: #2a3466; }
.foot { position: absolute; left: .61in; right: .61in; bottom: .4in; border-top: .75pt solid #1d1d24; padding-top: 7pt; display: flex; justify-content: space-between; font-size: 6.4pt; letter-spacing: .08em; color: #5a5a64; }
"""
doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Iron Bird Fitness · Recording Script</title><style>{FONTS}</style><style>{CSS}</style></head><body>{page}</body></html>"
src = HERE / "_tmp_rec.html"; src.write_text(doc)
chrome = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome"))[-1]
subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000",
                f"--print-to-pdf={HERE/OUT}", str(src)], check=True, stderr=subprocess.DEVNULL)
src.unlink(); print(HERE/OUT)
