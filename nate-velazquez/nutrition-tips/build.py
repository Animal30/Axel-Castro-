# Genera los guiones de anuncios de Meta de Nate (HTML -> PDF), versión que cumple las políticas de salud de Meta.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

ADS = [
    dict(title="The Hand Portion Rule", angle="Talking Head + B-roll · Nutrition tip", length="30-40 sec", kw="PLATE",
         hook="You don't need a food scale. You already have one at the end of your arm.",
         alts=["The easiest way to build a balanced plate, anywhere, in 5 seconds.",
               "No counting, no apps. Here's how my clients portion every meal."],
         core=["Protein: one palm. Chicken, fish, eggs, Greek yogurt, tofu.",
               "Veggies: one fist, or two if you can. Raw, roasted, frozen, it all counts.",
               "Carbs: one cupped hand. Rice, potatoes, pasta, fruit, bread.",
               "Fats: one thumb. Olive oil, avocado, cheese, nuts.",
               "That's it. It works at home, at a restaurant or at a work lunch, and your hands come with you everywhere.",
               "I'm Nate, nutrition coach. This is the first thing I teach clients who are tired of weighing and logging every bite."],
         cta="Send me a message with the word PLATE and I'll send you the one-page guide I give my clients."),
    dict(title="The Nutrient Almost Nobody Gets Enough Of", angle="Educational · Nutrition tip", length="30-40 sec", kw="FIBER",
         hook="Hungry an hour after eating? Look at this before you blame yourself.",
         alts=["Most adults get about half the fiber they need. Here's the easy fix.",
               "It's not protein. It's the other thing that keeps you full."],
         core=["Fiber. Most adults get roughly half of what they need every day, and it's one of the biggest reasons meals don't keep you full.",
               "The fix is small additions, not a new diet:",
               "Berries or chia in your yogurt. Beans or lentils in your bowl. Oats instead of cereal. A piece of fruit with lunch.",
               "Add it slowly and drink water with it, so your stomach has time to adjust.",
               "I'm Nate, nutrition coach. When clients tell me they're hungry all the time, this is one of the first places I look."],
         cta="Send me a message with the word FIBER and I'll send you my list of 10 easy high-fiber swaps."),
    dict(title="How To Build A Snack That Actually Holds You", angle="Talking Head + B-roll · Nutrition tip", length="25-35 sec", kw="SNACK",
         hook="A snack that leaves you hungry 30 minutes later isn't a snack. It's a warm-up.",
         alts=["The 2-part snack formula my clients use every afternoon.",
               "Why the 3pm snack doesn't work, and the one change that fixes it."],
         core=["Most snacks are just carbs on their own: crackers, a granola bar, chips. They're gone fast, and so is the energy.",
               "The formula is simple: one protein plus one fiber.",
               "An apple and a cheese stick. Greek yogurt and berries. Hummus and baby carrots. Turkey slices and a handful of grapes.",
               "Protein keeps you full, fiber slows it all down, and together they get you to dinner without raiding the pantry.",
               "I'm Nate, nutrition coach. Fixing the afternoon snack is one of the fastest wins I see with busy clients."],
         cta="Send me a message with the word SNACK and I'll send you 15 combos you can grab in under 2 minutes."),
    dict(title="Meal Prep Without Spending Your Whole Sunday", angle="Kitchen Demo · Nutrition tip", length="35-45 sec", kw="PREP",
         hook="Stop meal prepping meals. Prep ingredients instead.",
         alts=["30 minutes on Sunday. Easy lunches all week. Here's the system.",
               "Why most people quit meal prep by week two, and what to do instead."],
         core=["Eating the same chicken and rice five days in a row is why most people quit meal prep.",
               "So don't cook meals. Cook building blocks:",
               "Two proteins, like chicken thighs and ground turkey. One carb, like rice or potatoes. One tray of roasted veggies. One sauce you actually love.",
               "Then every day you mix them differently: a bowl on Monday, tacos on Tuesday, a wrap on Wednesday. Same 30 minutes of work, a different meal every day.",
               "I'm Nate, nutrition coach. This is how my clients eat well on weeks when there's no time to cook."],
         cta="Send me a message with the word PREP and I'll send you my 30-minute Sunday prep list."),
    dict(title="Add, Don't Subtract", angle="Talking Head · Nutrition tip", length="25-35 sec", kw="ADD",
         hook="The fastest way to eat better isn't removing foods. It's adding them.",
         alts=["Keep the pizza. Just add this.",
               "My clients don't give up their favorite meals. They do this instead."],
         core=["Every diet starts with a list of things you can't have. That's why every diet ends.",
               "Try the opposite: keep what you already eat, and add one protein and one fruit or veggie to it.",
               "Pizza night? Add a big side salad. Cereal in the morning? Add Greek yogurt. Pasta? Add chicken and a bag of frozen broccoli.",
               "You end up eating better without feeling like you lost anything, and that's what makes it stick.",
               "I'm Nate, nutrition coach. Nothing is off the table with my clients. We just make the plate work harder."],
         cta="Send me a message with the word ADD and I'll send you 10 easy add-ons for the meals you already love."),
]

def esc(s): return html.escape(s, quote=False)
N = len(ADS)
pages = []
for i, a in enumerate(ADS):
    cta_html = esc(a["cta"]).replace(a["kw"], '<span class="kw">' + a["kw"] + '</span>', 1)
    core = "".join(f"<p>{esc(p)}</p>" for p in a["core"])
    pages.append(f'''<section class="page">
  <div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
  <div class="top"><span class="sc"><i></i>SCRIPT {i+1} OF {N}</span><span class="tag">FEED + AD</span></div>
  <div class="vs">NUTRITION TIP · VIDEO SCRIPT</div>
  <h2>{esc(a["title"])}</h2>
  <div class="angle">{esc(a["angle"])}</div>
  <div class="facts">
    <div><span>FORMAT</span><b>{esc(a["angle"].split(" · ")[0])}</b></div>
    <div><span>LENGTH</span><b>{a["length"]}</b></div>
    <div><span>CHANNEL</span><b>IG Feed + Meta Ads</b></div>
    <div><span>DM KEYWORD</span><b class="kw">{a["kw"]}</b></div>
  </div>
  <div class="box"><div class="bh"><em>01</em>THE HOOK</div><p class="hook">“{esc(a["hook"])}”</p>
    <div class="alts"><span>ALTERNATE HOOKS · TEST THE FIRST 3 SECONDS</span>{"".join(f"<p>“{esc(h)}”</p>" for h in a["alts"])}</div></div>
  <div class="box"><div class="bh"><em>02</em>CORE MESSAGE</div><div class="core">{core}</div></div>
  <div class="box cta"><div class="bh"><em>03</em>CALL TO ACTION</div><p class="hook">“{cta_html}”</p></div>
  <div class="foot"><span>NATE VELAZQUEZ · NUTRITION TIPS</span><span>{i+1:02d} / {N:02d}</span></div>
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

doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Nate Velazquez Nutrition Tips</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "NateVelazquez_NutritionTips_Scripts.pdf"
subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
