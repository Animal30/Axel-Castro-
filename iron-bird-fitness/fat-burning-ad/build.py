# Genera el guion del anuncio nuevo "10 Minutes. No Gym." armado con escenas del video
# "Sam - 10 Min Fat Burning (2 min) 9x16.mp4" (HTML -> PDF). Uso: python3 build.py [fonts.css]
import html, pathlib, subprocess, sys, glob

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
OUT = "IronBird_10MinNoGym_AdScript.pdf"
SRC = "Sam - 10 Min Fat Burning (2 min) 9x16.mp4"

# (tiempo en el anuncio, clip del video original, lo que se escucha, texto en pantalla, nota de edición)
SCENES = [
    ("0:00 – 0:05", "1:25 – 1:30", "“This is a 10-minute workout that's going to work this whole area. Get your whole body stronger.”",
     "10 MINUTES. NO EQUIPMENT.", "Start on the word “This”. Keep the original 10:00 timer on screen. This is the hook."),
    ("0:05 – 0:13", "0:04 – 0:13 (audio)\n0:06 – 0:15 (visual)", "“First, definitely do your cardio, also do your nutrition, and then get as many reps in that work on the midsection.”",
     "CARDIO + NUTRITION + CORE", "Sam's audio over the formula graphic. Cut before “Basics for your beginner”."),
    ("0:13 – 0:16", "0:18 – 0:21", "Music (no voice)", "01 · KNEES TO WALL · 40–50 REPS", "Fast montage, one cut every 3 seconds, on the beat."),
    ("0:16 – 0:19", "0:33 – 0:36", "Music (no voice)", "02 · PUSH-UPS · 10 REPS", "Use the correct-form shot, not the mistakes."),
    ("0:19 – 0:22", "1:06 – 1:09", "Music (no voice)", "03 · SIT-UPS + CRUNCHES · 10 REPS", ""),
    ("0:22 – 0:25", "1:39 – 1:42", "Music (no voice)", "04 · CORE FINISHER · COBRA + PLANK", ""),
    ("0:25 – 0:30", "1:15 – 1:21 (visual)\n1:18 – 1:23 (audio)", "“Three to five. You're a beginner? Start with one set.”",
     "3–5 ROUNDS · BEGINNER: 1", "Levels graphic (Beginner / Building / Ready) with Sam's voice over it."),
    ("0:30 – 0:39", "1:58 – 2:08", "“As you can see, I didn't use any weights. So please do not say, ‘Oh, I wasn't able to go to the gym.’ The gym is wherever you're at.”",
     "THE GYM IS WHEREVER YOU'RE AT", "Sam talking to camera. Cut on “you're at”, before “Let me know what you think”."),
    ("0:39 – 0:45", "2:12 – 2:16 + new end card", "Music (no voice)",
     "TRAIN SMARTER. NOT LONGER.\nWant Sam to build your full plan?\n12-Week 1-on-1 Coaching · Fresno · Apply below",
     "Original end card with the call-to-action text on top. Optional: Sam records one new line (page 3)."),
]

HOOKS = [
    ("Main (recommended for ads)", "“This is a 10-minute workout that's going to work this whole area. Get your whole body stronger.”", "Clip 1:25 – 1:30"),
    ("Alternate A", "“As you can see, I didn't use any weights. So please do not say, ‘Oh, I wasn't able to go to the gym.’”", "Clip 1:58 – 2:06. Open with the objection, then show the moves."),
    ("Alternate B (organic only)", "“This is a quick workout on how to get rid of the FUPA, the mom pouch, the dad bod, whatever.”", "Clip 0:00 – 0:03. The strongest hook in the original, but it talks about the viewer's body and Meta often rejects that in health ads. Use it in organic Reels, not paid."),
]

OPTIONAL_VO = "“If you want me to build your whole plan, cardio, nutrition and training, tap Apply Now.”"

COPY_NEW = dict(headline="Train Smarter, Not Longer", cta="Apply Now",
    text=["10 minutes. No equipment. Your whole midsection.",
          "1️⃣ Knees to wall · 3–5 sets of 40–50 reps\n2️⃣ Push-ups · 3–5 sets of 10\n3️⃣ Sit-ups + crunches · 3–5 sets of 10\n4️⃣ Core finisher · floor cobra + plank",
          "Beginner? Start with one round.",
          "This workout is one third of the plan. Cardio and nutrition are the other two. If you're in Fresno and want Sam to build all three around your schedule, apply below for his 12-Week 1-on-1 Coaching Program."])

COPY_ORIG = dict(headline="Train Smarter, Not Longer", cta="Apply Now",
    text=["Here's a 10-minute midsection workout you can do anywhere. No equipment needed.",
          "1️⃣ Knees to wall · 3–5 sets of 40–50 reps\n2️⃣ Push-ups · 3–5 sets of 10\n3️⃣ Sit-ups + crunches · 3–5 sets of 10\n4️⃣ Core finisher · floor cobra + plank",
          "Beginner? Start with one round. Save this and try it tonight.",
          "Sam's rule: this workout works best next to cardio and nutrition. If you're in Fresno and want him to build all three around your schedule, apply below for his 12-Week 1-on-1 Coaching Program."])

e = lambda s: html.escape(s, quote=False).replace("\n", "<br>")
foot = lambda n, t: f'<div class="foot"><span>IRON BIRD FITNESS · AD SCRIPT</span><span>{n:02d} / {t:02d}</span></div>'
T = 4

p1 = f'''<section class="page">
  <div class="eyebrow">IRON BIRD FITNESS · @IRONBIRDFIT</div>
  <div class="sc"><i></i>NEW AD · EDITED FROM EXISTING FOOTAGE</div>
  <h1>10 Minutes.<br><span>No Gym.</span></h1>
  <div class="angle">Value-first ad built only from clips of “10 Min Fat Burning”. No new filming needed.</div>
  <div class="facts">
    <div><span>FORMAT</span><b>Workout montage + talking head</b></div><div><span>LENGTH</span><b>40–45 sec</b></div>
    <div><span>PLACEMENT</span><b>Reels + Stories (9:16)</b></div><div><span>CTA</span><b class="kw">Apply Now · Lead form</b></div>
  </div>
  <div class="box"><div class="bh"><em>01</em>THE IDEA</div><div class="core">
    <p>The original video is 2:16: great value, too long for an ad. This cut keeps the strongest 45 seconds: a promise in the first line, the formula, the 4 moves in a fast montage, the “no excuses” line, and a clear call to action.</p>
    <p>It gives away the workout first and sells the coaching second. People who save the workout but want results faster are exactly the leads Sam closes.</p></div></div>
  <div class="box"><div class="bh"><em>02</em>HOOKS · TEST THE FIRST 3 SECONDS</div>
    {"".join(f'<div class="hk"><span>{e(n)}</span><p class="hook">{e(h)}</p><small>{e(note)}</small></div>' for n, h, note in HOOKS)}</div>
  {foot(1, T)}
</section>'''

rows = "".join(f'<tr><td class="t">{e(a)}</td><td class="src">{e(b)}</td><td>{e(c)}</td><td class="sup">{e(d)}</td><td class="note">{e(n)}</td></tr>' for a, b, c, d, n in SCENES)
p2 = f'''<section class="page">
  <div class="eyebrow">IRON BIRD FITNESS · @IRONBIRDFIT</div>
  <div class="sc"><i></i>SCENE BY SCENE</div>
  <h2>Edit map</h2>
  <table><thead><tr><th>AD TIME</th><th>CLIP (ORIGINAL)</th><th>AUDIO</th><th>ON-SCREEN TEXT</th><th>EDIT NOTE</th></tr></thead><tbody>{rows}</tbody></table>
  {foot(2, T)}
</section>'''

p3 = f'''<section class="page">
  <div class="eyebrow">IRON BIRD FITNESS · @IRONBIRDFIT</div>
  <div class="sc"><i></i>EDIT NOTES</div>
  <h2>How to cut it</h2>
  <div class="box"><div class="bh"><em>01</em>STYLE</div><div class="core">
    <p>Keep the original look: black and dark red, the white “Iron Bird” tank, the red section titles. Same caption style as the original, bottom third, white text.</p>
    <p>Montage cuts every 2–3 seconds on the beat. Talking-head parts stay on one shot so Sam's voice carries them.</p>
    <p>Low music bed under the whole ad, ducked under Sam's voice. Quiet sound effects only on the 4 exercise titles, not on every cut.</p></div></div>
  <div class="box"><div class="bh"><em>02</em>OPTIONAL NEW LINE FOR SAM · 10 SECONDS TO RECORD</div>
    <p class="hook">{e(OPTIONAL_VO)}</p><div class="core"><p>Same setup as the original talking head (Iron Bird tank, same corner of the gym). If he records it, it replaces the music in the last scene. Without it, the ad still works with the text CTA.</p></div></div>
  <div class="box"><div class="bh"><em>03</em>SOURCE FILE</div><div class="core"><p>{e(SRC)} · Drive folder “November Folder”. Every timestamp in this script refers to that file.</p></div></div>
  <div class="box"><div class="bh"><em>04</em>META POLICY CHECKS</div><div class="core">
    <p>No body-shaming hook in paid ads (“FUPA”, “mom pouch”, “dad bod”): keep those for organic posts.</p>
    <p>No promised results or timeframes (“lose X lbs in 10 days”). The ad sells a 10-minute routine and the coaching, nothing else.</p>
    <p>No before/after shots in this cut.</p></div></div>
  {foot(3, T)}
</section>'''

def copyblock(title, c):
    paras = "".join(f"<p>{e(p)}</p>" for p in c["text"])
    return f'''<div class="box"><div class="bh"><em>{title[0]}</em>{e(title[1])}</div>
    <div class="facts two"><div><span>HEADLINE</span><b>{e(c["headline"])}</b></div><div><span>BUTTON</span><b class="kw">{e(c["cta"])}</b></div></div>
    <div class="core copy">{paras}</div></div>'''

p4 = f'''<section class="page">
  <div class="eyebrow">IRON BIRD FITNESS · @IRONBIRDFIT</div>
  <div class="sc"><i></i>AD COPY</div>
  <h2>Primary text</h2>
  {copyblock(("01", "NEW 45-SEC CUT · “10 MINUTES. NO GYM.”"), COPY_NEW)}
  {copyblock(("02", "ORIGINAL 2:16 VIDEO · RUNNING NOW"), COPY_ORIG)}
  {foot(4, T)}
</section>'''

CSS = """
@page { size: 10in 12.5in; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0b0909; font-family: Inter, Arial, sans-serif; color: #f5f2f2; }
.page { width: 10in; height: 12.5in; padding: .62in .67in; position: relative; overflow: hidden; break-after: page;
  background: radial-gradient(120% 60% at 50% 0%, #2a0d0f 0%, #0b0909 60%); }
.page:last-child { break-after: auto; }
.eyebrow { font-size: 8.2pt; font-weight: 700; letter-spacing: .1em; color: #e2231a; }
.sc { font-size: 8.2pt; font-weight: 700; letter-spacing: .08em; color: #e2231a; display: flex; align-items: center; gap: 9pt; margin-top: 24pt; }
.sc i { width: 16pt; height: 1.5pt; background: #e2231a; display: inline-block; }
h1 { font-family: Anton, Inter, sans-serif; font-weight: 400; font-size: 56pt; line-height: .98; margin-top: 12pt; text-transform: uppercase; }
h1 span { color: #e2231a; }
h2 { font-size: 28pt; font-weight: 800; line-height: 1.18; margin-top: 10pt; letter-spacing: -.01em; }
.angle { color: #b3a6a6; font-size: 11.2pt; margin-top: 10pt; }
.facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10pt; margin-top: 18pt; }
.facts.two { grid-template-columns: 1fr 1fr; margin-top: 0; margin-bottom: 12pt; }
.facts div { background: #161012; border: .75pt solid #2b1d1f; border-radius: 5pt; padding: 11pt 12pt 13pt; }
.facts span { display: block; font-size: 7.5pt; letter-spacing: .08em; color: #7a6668; margin-bottom: 6pt; font-weight: 600; }
.facts b { font-size: 10.8pt; font-weight: 700; }
.kw { color: #ff4a3d; font-weight: 700; }
.box { background: #161012; border: .75pt solid #2b1d1f; border-radius: 6pt; padding: 16pt 18pt; margin-top: 13pt; }
.bh { font-size: 8.2pt; font-weight: 700; letter-spacing: .08em; color: #7a6668; margin-bottom: 10pt; }
.bh em { font-style: normal; color: #e2231a; font-size: 10.5pt; margin-right: 9pt; }
.hook { font-size: 13.2pt; font-weight: 700; line-height: 1.42; }
.hk + .hk { margin-top: 11pt; padding-top: 11pt; border-top: .75pt solid #2b1d1f; }
.hk span { display: block; font-size: 7.6pt; letter-spacing: .08em; color: #ff4a3d; font-weight: 700; margin-bottom: 4pt; text-transform: uppercase; }
.hk small { display: block; color: #9a8b8c; font-size: 9pt; margin-top: 4pt; line-height: 1.45; }
.core p { font-size: 10.6pt; color: #b3a6a6; line-height: 1.7; }
.core p + p { margin-top: 7pt; }
.copy p { color: #e9e1e1; }
table { width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 16pt; font-size: 8.6pt; line-height: 1.42; }
th { text-align: left; font-size: 7pt; letter-spacing: .08em; color: #7a6668; font-weight: 700; padding: 0 7pt 7pt; }
td { background: #161012; border-top: .75pt solid #2b1d1f; padding: 9pt 7pt; vertical-align: top; color: #d8cfcf; }
td.t { color: #ff4a3d; font-weight: 700; white-space: nowrap; }
td.src { color: #f5f2f2; font-weight: 600; white-space: nowrap; }
td.sup { font-weight: 700; color: #fff; text-transform: none; }
td.note { color: #9a8b8c; }
th:nth-child(1){width:11%} th:nth-child(2){width:15%} th:nth-child(3){width:29%} th:nth-child(4){width:20%} th:nth-child(5){width:25%}
.foot { position: absolute; left: .67in; right: .67in; bottom: .45in; display: flex; justify-content: space-between; font-size: 7.5pt; letter-spacing: .08em; color: #7a6668; }
"""
doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Iron Bird Fitness · 10 Minutes. No Gym. · Ad Script</title><style>{FONTS}</style><style>{CSS}</style></head><body>{p1}{p2}{p3}{p4}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
chrome = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome"))[-1]
subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000",
                f"--print-to-pdf={HERE/OUT}", str(src)], check=True, stderr=subprocess.DEVNULL)
src.unlink(); print(HERE/OUT)
