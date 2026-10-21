# Genera los guiones de anuncios de Meta de Nate (HTML -> PDF), versión que cumple las políticas de salud de Meta.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

ADS = [
    dict(title="Why You're Hungry An Hour After Eating", angle="Talking Head · Yapping · Nutrition", length="30-45 sec", kw="FULL",
         hook="Okay, real talk. If you eat a full meal and you're hungry again an hour later, that's not a willpower thing.",
         alts=["The reason some meals keep you full for five hours and others for one.",
               "Nobody explains this, so let me: why you're always hungry."],
         core=["Most of the time it comes down to two things missing from the meal: protein and fiber.",
               "A bagel and a coffee? Basically no protein, barely any fiber. Your body burns through it fast, and an hour later it's asking for more.",
               "Same amount of food, but with eggs or Greek yogurt and some fruit? Completely different morning.",
               "So before you blame yourself for snacking, look at what was actually on the plate. Most people don't have a hunger problem. They have a meal-building problem.",
               "I'm Nate, nutrition coach, and this is the first thing I look at with almost every new client."],
         cta="Send me a message with the word FULL and tell me what you usually eat in a day. I'll tell you the first thing I'd change."),
    dict(title="Should You Stop Eating After 7pm?", angle="Talking Head · Yapping · Myth", length="30-45 sec", kw="LATE",
         hook="I get asked this every week: ‘Nate, should I stop eating after 7pm?’ Here's my honest answer.",
         alts=["The 7pm rule is one of the most repeated nutrition myths out there.",
               "Eating late isn't the problem. This is."],
         core=["Your body doesn't have a clock that turns food into something worse at 7:01.",
               "What matters way more is how much you eat across the whole day, and what you eat.",
               "Here's what I actually see: people who ‘stop eating at 7’ often barely eat during the day, get home starving, and then the rule falls apart at 9pm anyway.",
               "If your schedule means dinner at 8:30, that's fine. Eat enough earlier in the day, make dinner a real meal, and the late-night grazing usually takes care of itself.",
               "I'm Nate, nutrition coach. I'd rather give my clients a plan that fits their schedule than a rule that fights it."],
         cta="Send me a message with the word LATE and tell me what time you usually eat dinner. I'll tell you how I'd set up your day around it."),
    dict(title="Your Cravings Are Trying To Tell You Something", angle="Talking Head · Yapping · Nutrition", length="30-45 sec", kw="CRAVINGS",
         hook="Cravings aren't a character flaw. Most of the time, they're a signal.",
         alts=["If sweets call your name every night, listen to this first.",
               "Three reasons cravings hit harder than they should, and none of them is willpower."],
         core=["When clients tell me their cravings are out of control, I usually find one of three things.",
               "One: they're not eating enough during the day, so by night their body is basically yelling for quick energy.",
               "Two: they're running on bad sleep. Short nights make sweet and salty food a lot harder to say no to.",
               "Three: they've banned a food completely. And the moment something is off limits, it's all you can think about.",
               "Fix those three, and cravings usually get quieter on their own. No white-knuckling required.",
               "I'm Nate, nutrition coach, and this is a big part of what I work on with my clients."],
         cta="Send me a message with the word CRAVINGS and tell me when they hit you the hardest. I'll tell you what I'd look at first."),
    dict(title="The Snack Mistake Almost Everyone Makes", angle="Talking Head · Yapping · Nutrition", length="25-40 sec", kw="SNACK",
         hook="Most people don't have a snacking problem. They have a snack-choosing problem.",
         alts=["If your afternoon snack is gone in 30 minutes, this is why.",
               "The one thing that turns a snack into something that actually holds you."],
         core=["Here's the mistake: the snack is just carbs on their own. Crackers, a granola bar, a bag of chips. Nothing wrong with them, but they don't last.",
               "What I teach my clients is simple: every snack gets a protein and a fiber.",
               "So instead of just crackers, crackers with cheese. Instead of just an apple, an apple with a cheese stick or some peanut butter.",
               "It's a tiny change, but it's usually the difference between making it to dinner and raiding the pantry at 4pm.",
               "I'm Nate, nutrition coach. Small fixes like this add up faster than any diet."],
         cta="Send me a message with the word SNACK and tell me what you usually grab in the afternoon. I'll give you a better version of it."),
    dict(title="Add, Don't Subtract", angle="Talking Head · Yapping · Mindset + Nutrition", length="25-40 sec", kw="ADD",
         hook="The fastest way to eat better isn't removing foods. It's adding them.",
         alts=["Every diet starts with a list of what you can't eat. That's exactly why they end.",
               "My clients don't give up their favorite meals. Here's what they do instead."],
         core=["Think about every diet you've tried. It started with a list: no carbs, no sugar, no eating out. And it lasted until the first stressful week.",
               "I do the opposite with my clients. We keep what they already eat, and we add to it.",
               "Pizza night stays. We just add a big salad next to it. Pasta stays. We add some protein to it.",
               "When you're not losing anything, there's nothing to rebel against. That's why it sticks.",
               "I'm Nate, nutrition coach. Nothing is off the table with me. We just make the plate work harder."],
         cta="Send me a message with the word ADD and tell me your favorite meal. I'll show you how I'd keep it in your week."),
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
  <div class="vs">NUTRITION TALK · VIDEO SCRIPT</div>
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
