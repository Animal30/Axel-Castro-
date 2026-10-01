# Genera el calendario de contenido de Nate (HTML -> PDF) con el mismo diseño del calendario anterior.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

TAGS = {
    "CONTRARIAN": ("#fb923c", "rgba(251,146,60,.14)"),
    "MINDSET": ("#c084fc", "rgba(192,132,252,.14)"),
    "EDUCATIONAL": ("#60a5fa", "rgba(96,165,250,.14)"),
    "MYTH": ("#f87171", "rgba(248,113,113,.14)"),
    "ADVICE": ("#2dd4bf", "rgba(45,212,191,.14)"),
    "INSIGHT": ("#4ade80", "rgba(74,222,128,.14)"),
    "OFFER": ("#facc15", "rgba(250,204,21,.14)"),
}

SCRIPTS = [
    dict(tag="CONTRARIAN", day="Mon · Week 2", title="Eating Less Is Why Your Nights Fall Apart",
         angle="Contrarian angle", fmt="Talking Head", length="30-40 sec", kw="FUEL",
         hook="If you're \"good\" all day and then lose it every night, you're not weak. You're hungry.",
         core=["Most busy adults skip breakfast, grab something small at lunch, and call it discipline. Then 8pm hits and the kitchen wins.",
               "That's not a lack of self-control. That's a body that went ten hours on almost nothing, doing exactly what it's designed to do.",
               "The fix isn't eating less at night. It's eating enough during the day, so night never turns into a fight.",
               "I'm Nate. I coach busy adults on nutrition, and the first thing I fix for most clients isn't what they eat at dinner. It's what they didn't eat before it."],
         cta="DM me FUEL and I'll show you how I build a day that doesn't fall apart at night.",
         note="Open almost confessional, like you're letting them in on something. The turn is \"you're not weak, you're hungry\": give it a beat, it's the line people will screenshot. Calm, zero judgment."),
    dict(tag="MINDSET", day="Tue · Week 2", title="Your Weekends Are Undoing Your Weekdays",
         angle="Mindset angle", fmt="Talking Head", length="30-40 sec", kw="WEEKEND",
         hook="Five good days and two \"off\" days isn't a 70% plan. For a lot of people, it's a zero.",
         core=["Monday to Friday you're locked in. Then Friday night turns into Sunday night, and the weekend quietly cancels out everything the week built.",
               "The answer isn't giving up your weekends. It's to stop treating them like a break from the plan, and start making them part of it.",
               "Pick the one meal you're actually looking forward to. Enjoy it fully, no guilt. Keep the rest of the weekend simple.",
               "I'm Nate, nutrition coach for busy adults. My clients don't lose their weekends. They just stop letting two days decide the other five."],
         cta="DM me WEEKEND and I'll send you the exact weekend rules I give my clients.",
         note="Record it on a Friday or Saturday if you can, it feels timely. Light and relatable, not preachy: you love weekends too. Say \"no guilt\" like you mean it."),
    dict(tag="EDUCATIONAL", day="Wed · Week 2", title="The \"Healthy\" Foods Quietly Stalling Your Progress",
         angle="Educational · Authority angle", fmt="Talking Head + B-roll", length="35-45 sec", kw="SWAP",
         hook="You're eating \"healthy\" and nothing's changing. These might be the reason.",
         core=["The smoothie with three fruits, nut butter and honey. The granola that's basically dessert. The salad with half a cup of dressing. The coffee drink that's really a milkshake.",
               "None of these are bad foods. But they're labeled healthy, so nobody counts them, and together they can add up to a whole extra meal every day without you noticing.",
               "I'm Nate. I coach busy adults on nutrition, and I don't take these foods away from my clients. I show them the swaps that keep the taste and cut the hidden extras.",
               "Healthy and helpful aren't always the same thing."],
         cta="DM me SWAP and I'll send you my top 5 swaps.",
         note="Show each food on screen as you name it (B-roll or holding it up in the kitchen). Quick rhythm on the list, then slow down for \"none of these are bad foods\". Never shame the food or the person."),
    dict(tag="MYTH", day="Thu · Week 2", title="You Don't Have To Quit Carbs",
         angle="Myth-busting angle", fmt="Talking Head", length="30-40 sec", kw="CARBS",
         hook="Carbs didn't make you gain weight. And cutting them is why it keeps coming back for so many people.",
         core=["Going no-carb feels great for two weeks, mostly because you're losing water. Then a birthday, a pasta night, a vacation, and it all comes back, plus the guilt.",
               "Carbs were never the problem. Eating them without a plan was.",
               "Rice, potatoes, bread, fruit. My clients eat all of it. The difference is they know how much, and what to pair it with.",
               "I'm Nate, nutrition coach for busy adults. A plan without the foods you love isn't a plan you'll keep. It's just a countdown to quitting."],
         cta="DM me CARBS and I'll show you how my clients eat them and still make progress.",
         note="Confident, slightly playful. Could hold a bowl of rice or a slice of bread for the hook, it stops the scroll. Land \"a countdown to quitting\" slowly and stop there."),
    dict(tag="ADVICE", day="Fri · Week 2", title="How To Eat Out Without Starting Over Monday",
         angle="Advice angle", fmt="Talking Head", length="35-45 sec", kw="MENU",
         hook="You don't have to skip dinner with friends to stay on track. You just need three rules.",
         core=["One: decide before you get there. Check the menu ahead of time, so you're not choosing while you're starving.",
               "Two: pick your one. The drink, the bread, or the dessert. Enjoy one of them fully, not all three halfway.",
               "Three: stop at satisfied, not stuffed. Restaurant portions aren't a challenge you have to finish.",
               "I'm Nate. I coach busy adults on nutrition, and eating out is where most of my clients think they'll fail. It usually ends up being where they feel the most confident."],
         cta="DM me MENU and I'll send you my full dining-out guide.",
         note="Count the rules on your fingers, it keeps people watching to the end. Film at a restaurant table or in the car before dinner if possible. Practical, quick, friendly."),
    dict(tag="INSIGHT", day="Sat · Week 2", title="Your Diet Gets Decided In The Grocery Store",
         angle="Insight angle", fmt="Walk & Talk", length="30-40 sec", kw="LIST",
         hook="Most of your diet gets decided right here, not in your kitchen.",
         core=["If it's in your house, you'll eat it eventually. Not because you're weak. Because you're tired, busy, and it's right there.",
               "Which means the most important nutrition decision of your week happens in about forty minutes, pushing a cart.",
               "My clients shop from one simple list: proteins, easy carbs, fruit and veggies, and two snacks they actually love. So the easy choice at home is already the right one.",
               "I'm Nate, nutrition coach for busy adults. I don't ask my clients to fight the food in their house. I help them change what's waiting for them there."],
         cta="DM me LIST and I'll send you the grocery list template I give my clients.",
         note="Film walking through a grocery store aisle with a cart, phone at chest height. Point at shelves naturally. Relaxed weekend energy, like you're shopping together."),
    dict(tag="OFFER", day="Sun · Week 2", title="What 12 Weeks With Me Actually Looks Like",
         angle="Process + offer angle", fmt="Talking Head", length="40-50 sec", kw="APPLY",
         hook="People keep asking what coaching with me actually looks like. Here's the honest version.",
         core=["Weeks one to four: we build your plan around your schedule and the food you already eat, and lock in the first few habits. Nothing extreme.",
               "Weeks five to eight: we adjust every week based on your check-ins, so nothing stalls and nothing feels forced.",
               "Weeks nine to twelve: we make it yours. How to eat out, travel, and handle a rough week without needing me.",
               "I'm Nate. I coach busy adults on nutrition, and I only take ten new clients a month, so every plan gets real attention."],
         cta="DM me APPLY and let's see if you're a fit for this month.",
         note="The clearest, most structured video of the week: hold up one, two, three fingers or use on-screen text for each phase. Calm and confident, no hype. Pause before the CTA."),
]

def esc(s): return html.escape(s, quote=False)

def tag_html(t):
    c, bg = TAGS[t]
    return f'<span class="tag" style="color:{c};background:{bg}">{t}</span>'

total = len(SCRIPTS) + 1
pages = []
rows = "".join(
    f'<div class="row"><span class="n">{i+1:02d}</span><span class="t">{esc(s["title"])}</span>{tag_html(s["tag"])}<span class="d">{s["day"]}</span></div>'
    for i, s in enumerate(SCRIPTS))
pages.append(f'''<section class="page cover">
  <div class="cv">
    <div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
    <h1>Content Calendar</h1>
    <p class="sub">{len(SCRIPTS)} scripts. Ready to record. Built to convert.</p>
    <div class="meta">
      <p><b>TARGET</b> — Busy adults 30+ who've tried restrictive diets and want a sustainable way to eat</p>
      <p><b>STYLE</b> — Direct, personal, coach-to-camera. No hype, no shame.</p>
      <p><b>FORMAT</b> — 30–50 sec · Talking Head · Instagram Reels</p>
    </div>
  </div>
  <div class="list"><div class="lh">SCRIPTS IN THIS DOCUMENT</div>{rows}</div>
  <div class="foot"><span>NATE VELAZQUEZ · CONTENT CALENDAR</span><span>01 / {total:02d}</span></div>
</section>''')

for i, s in enumerate(SCRIPTS):
    core = "".join(f"<p>{esc(p)}</p>" for p in s["core"])
    cta = esc(s["cta"]).replace(s["kw"], f'<span class="kw">{s["kw"]}</span>', 1)
    pages.append(f'''<section class="page">
  <div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
  <div class="top"><span class="sc"><i></i>SCRIPT {i+1} OF {len(SCRIPTS)}</span>{tag_html(s["tag"])}</div>
  <div class="vs">VIDEO SCRIPT</div>
  <h2>{esc(s["title"])}</h2>
  <div class="angle">{esc(s["angle"])}</div>
  <div class="facts">
    <div><span>FORMAT</span><b>{esc(s["fmt"])}</b></div>
    <div><span>LENGTH</span><b>{s["length"]}</b></div>
    <div><span>CHANNEL</span><b>Instagram Reels</b></div>
    <div><span>DM KEYWORD</span><b class="kw">{s["kw"]}</b></div>
  </div>
  <div class="box"><div class="bh"><em>01</em>THE HOOK</div><p class="hook">“{esc(s["hook"])}”</p></div>
  <div class="box"><div class="bh"><em>02</em>CORE MESSAGE</div><div class="core">{core}</div></div>
  <div class="box cta"><div class="bh"><em>03</em>CALL TO ACTION</div><p class="hook">“{cta}”</p></div>
  <div class="box note"><div class="bh">DIRECTOR'S NOTE</div><p>{esc(s["note"])}</p></div>
  <div class="foot"><span>NATE VELAZQUEZ · CONTENT CALENDAR</span><span>{i+2:02d} / {total:02d}</span></div>
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
.tag { font-size: 7.3pt; font-weight: 700; letter-spacing: .1em; padding: 3pt 9pt; border-radius: 10pt; }
.cover .cv { text-align: center; margin-top: 1.55in; }
.cover h1 { font-size: 34pt; font-weight: 800; margin-top: 12pt; letter-spacing: -.01em; }
.cover .sub { color: #a6a6b3; font-size: 10pt; margin-top: 8pt; }
.cover .meta { margin-top: 26pt; border-top: .75pt solid #1f1f27; border-bottom: .75pt solid #1f1f27; padding: 20pt 0; font-size: 8.6pt; color: #a6a6b3; line-height: 2; }
.cover .meta b { color: #f4f4f7; }
.list { margin-top: 24pt; }
.lh { font-size: 7.6pt; font-weight: 700; letter-spacing: .1em; color: #5b7cfa; margin-bottom: 6pt; }
.row { display: flex; align-items: center; gap: 10pt; padding: 8.5pt 0; border-bottom: .75pt solid #1a1a21; font-size: 9.2pt; }
.row .n { color: #5b7cfa; font-weight: 700; width: 18pt; }
.row .t { flex: 1; }
.row .d { color: #8b8a94; font-size: 8pt; width: 64pt; text-align: right; }
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

doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Nate Velazquez Content Calendar</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
out = HERE / "NateVelazquez_ContentCalendar_Week2.html"
out.write_text(doc)
pdf = HERE / "NateVelazquez_ContentCalendar_Week2.pdf"
subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(out)],
               check=True, stderr=subprocess.DEVNULL)
out.unlink()
print(pdf)
