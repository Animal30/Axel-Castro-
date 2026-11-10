# Genera el calendario de contenido de Iron Bird Fitness del 10/11/26 (HTML -> PDF), mismo diseño que el calendario del 10/1/26.
# Temas nuevos: no repite los de los calendarios del 10/1/26 ni de la Semana 2.
import html, pathlib, subprocess, sys, glob
HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
OUT = "IronBirdFitness_ContentCalendar11.10.26.pdf"

SCRIPTS = [
    dict(title="Check Your Plate Before You Change Your Workout", angle="Educational · Authority angle", fmt="Educational", length="35-45 sec", kw="PROTEIN",
         hook="If you're training hard and your body still isn't changing, look at your plate before you look at your workout.",
         core=["Most adults I meet eat plenty of food and not nearly enough protein. Coffee for breakfast, a sandwich at lunch, and the only real serving of protein shows up at dinner.",
               "Protein is what your muscles rebuild with after you train. It also keeps you full longer, which is why people who eat enough of it usually snack a lot less.",
               "I'm Sam, owner of Iron Bird Fitness. The first change I make with almost every new client isn't the workout. It's a real portion of protein at every meal, not just the last one.",
               "Train hard, eat like it matters, and the work you're already putting in finally starts to show."],
         cta="DM me PROTEIN. I'll send you the simple way we hit it at every meal."),
    dict(title="Crunches Won't Burn Your Belly Fat", angle="Educational · Myth angle", fmt="Educational", length="30-40 sec", kw="CORE",
         hook="If crunches burned belly fat, everyone doing a hundred a night would have abs by now.",
         core=["You can't pick where your body loses fat. Crunches make the muscles underneath stronger, and that's good, but they don't melt what's sitting on top.",
               "Losing fat around your midsection comes from the full picture: how you eat, how much you move during the day, and training your whole body instead of one spot.",
               "I'm Sam, owner of Iron Bird Fitness. Core work is in every program I write. It's just never the whole plan.",
               "Train your core for strength. Fix your plate and the rest of your week for the fat."],
         cta="DM me CORE. I'll send you my 10-minute midsection workout and the three things that actually move the needle."),
    dict(title="Your Weekends Are Erasing Your Weekdays", angle="Talking Head · Mindset angle", fmt="Talking Head", length="30-40 sec", kw="WEEKEND",
         hook="Monday to Friday you're dialed in. Then Saturday and Sunday quietly undo most of it.",
         core=["Five good days feel like a win. But two loose days of brunch, drinks and whatever's in the fridge can cancel out a big part of your week, and most people never connect the two.",
               "You don't need a perfect weekend. You need a plan before it starts: one meal out you actually enjoy, a walk or a short session on Saturday, and back to normal on Sunday night instead of Monday.",
               "I'm Sam, owner of Iron Bird Fitness. When someone tells me they're stuck, the first thing I ask about isn't their workouts. It's their weekends.",
               "Win the weekend on purpose and the weekdays finally start adding up."],
         cta="DM me WEEKEND. I'll show you the weekend plan my clients use."),
    dict(title="If Stairs Bother Your Knees, Start Here", angle="Educational · Authority angle", fmt="Educational", length="35-45 sec", kw="KNEES",
         hook="If taking the stairs makes your knees ache, your knees probably aren't the whole problem.",
         core=["A lot of knee discomfort comes from what's around the knee. Hips and legs that got weak from sitting all day, so the joint ends up taking the load the muscles should be handling.",
               "Building strength in your glutes, quads and hamstrings, slowly and with good form, takes pressure off the knee instead of adding to it.",
               "I'm Sam, owner of Iron Bird Fitness. Some of the best progress I see doesn't show up on a scale. It's taking the stairs, getting up from the floor or playing with your kids without thinking about your knees. (If pain is sharp or ongoing, see your doctor first.)",
               "Strong legs are how you protect your knees, not what hurts them."],
         cta="DM me KNEES. I'll send you the three movements we start with."),
    dict(title="How To Eat Out And Still Make Progress", angle="Talking Head · Practical angle", fmt="Talking Head", length="35-45 sec", kw="MENU",
         hook="You don't have to stop eating out to get in shape. You just have to order like you have a plan.",
         core=["Work lunches, date night, the kids' games. For most adults, eating out a couple of times a week is just life, and cutting it out completely never lasts.",
               "Three rules that work almost anywhere: build your order around a protein, swap one side for vegetables, and decide before you sit down if tonight is drinks or dessert.",
               "I'm Sam, owner of Iron Bird Fitness. I'd rather teach you how to handle a menu than hand you a diet you'll quit in three weeks.",
               "Real life has restaurants in it. Your plan should too."],
         cta="DM me MENU. I'll send you my go-to orders for the places you already eat."),
]

e = lambda s: html.escape(s, quote=False)
N = len(SCRIPTS); pages = []
for i, s in enumerate(SCRIPTS):
    core = "".join(f"<p>{e(p)}</p>" for p in s["core"])
    cta = e(s["cta"]).replace(s["kw"], f'<span class="kw">{s["kw"]}</span>', 1)
    pages.append(f'''<section class="page">
  <div class="eyebrow">IRON BIRD FITNESS · @IRONBIRDFIT</div>
  <div class="sc"><i></i>SCRIPT {i+1} OF {N}</div>
  <h2>{e(s["title"])}</h2>
  <div class="angle">{e(s["angle"])}</div>
  <div class="facts">
    <div><span>FORMAT</span><b>{e(s["fmt"])}</b></div><div><span>LENGTH</span><b>{s["length"]}</b></div>
    <div><span>CHANNEL</span><b>Instagram Reels</b></div><div><span>DM KEYWORD</span><b class="kw">{s["kw"]}</b></div>
  </div>
  <div class="box"><div class="bh"><em>01</em>THE HOOK</div><p class="hook">“{e(s["hook"])}”</p></div>
  <div class="box"><div class="bh"><em>02</em>CORE MESSAGE</div><div class="core">{core}</div></div>
  <div class="box cta"><div class="bh"><em>03</em>CALL TO ACTION</div><p class="hook">“{cta}”</p></div>
  <div class="foot"><span>IRON BIRD FITNESS · CONTENT CALENDAR</span><span>{i+1:02d} / {N:02d}</span></div>
</section>''')

CSS = """
@page { size: 10in 12.5in; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0a0b0f; font-family: Inter, Arial, sans-serif; color: #f3f5f8; }
.page { width: 10in; height: 12.5in; padding: .62in .67in; position: relative; overflow: hidden; break-after: page; background: #0a0b0f; }
.page:last-child { break-after: auto; }
.eyebrow { font-size: 8.2pt; font-weight: 700; letter-spacing: .1em; color: #5b8cff; }
.sc { font-size: 8.2pt; font-weight: 700; letter-spacing: .08em; color: #5b8cff; display: flex; align-items: center; gap: 9pt; margin-top: 26pt; }
.sc i { width: 16pt; height: 1.5pt; background: #5b8cff; display: inline-block; }
h2 { font-size: 28.5pt; font-weight: 800; line-height: 1.18; margin-top: 12pt; max-width: 6.2in; letter-spacing: -.01em; }
.angle { color: #98a2b3; font-size: 11.2pt; margin-top: 8pt; }
.facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10pt; margin-top: 20pt; }
.facts div { background: #10131a; border: .75pt solid #1d222c; border-radius: 5pt; padding: 12pt 12pt 14pt; }
.facts span { display: block; font-size: 7.5pt; letter-spacing: .08em; color: #565f70; margin-bottom: 7pt; font-weight: 600; }
.facts b { font-size: 11.2pt; font-weight: 700; }
.kw { color: #5b8cff; font-weight: 700; }
.box { background: #10131a; border: .75pt solid #1d222c; border-radius: 6pt; padding: 18pt 18pt; margin-top: 14pt; }
.bh { font-size: 8.2pt; font-weight: 700; letter-spacing: .08em; color: #565f70; margin-bottom: 11pt; }
.bh em { font-style: normal; color: #5b8cff; font-size: 10.5pt; margin-right: 9pt; }
.hook { font-size: 14.2pt; font-weight: 700; line-height: 1.45; }
.core p { font-size: 10.9pt; color: #98a2b3; line-height: 1.75; }
.core p + p { margin-top: 8pt; }
.box.cta { background: #121729; border-color: #2a3560; }
.foot { position: absolute; left: .67in; right: .67in; bottom: .45in; display: flex; justify-content: space-between; font-size: 7.5pt; letter-spacing: .08em; color: #565f70; }
"""
doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Iron Bird Fitness · 7-Video Content Calendar</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
subprocess.run([sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome"))[-1], "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={HERE/OUT}", str(src)], check=True, stderr=subprocess.DEVNULL)
src.unlink(); print(HERE/OUT)
