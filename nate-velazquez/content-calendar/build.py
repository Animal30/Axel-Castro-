# Genera el calendario de contenido de Nate (HTML -> PDF) con el mismo diseño del calendario anterior.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

TAGS = {
    "EXPERIMENT": ("#60a5fa", "rgba(96,165,250,.14)"),
    "HOT TAKE": ("#f87171", "rgba(248,113,113,.14)"),
    "REAL LIFE": ("#4ade80", "rgba(74,222,128,.14)"),
    "SKIT": ("#c084fc", "rgba(192,132,252,.14)"),
    "LIST": ("#2dd4bf", "rgba(45,212,191,.14)"),
    "SOFT OFFER": ("#facc15", "rgba(250,204,21,.14)"),
}

SCRIPTS = [
    dict(tag="EXPERIMENT", day="Mon · Week 2", title="Same Calories. Two Very Different Plates.",
         angle="Visual experiment", fmt="Table-top demo", length="20-30 sec", goal="Shares + saves",
         onscreen="SAME CALORIES ↓",
         hook="These two plates have the exact same calories. Only one of them keeps you full until 3pm.",
         core=["Left: a blueberry muffin and a vanilla latte. Gone in four minutes. Hungry again by 10.",
               "Right: eggs, toast, a pile of fruit, Greek yogurt, and a chicken sausage. Same number. You'll struggle to finish it.",
               "Your stomach doesn't count calories. It counts volume and protein. That's the whole trick.",
               "Nobody's telling you to never eat the muffin. Just know what you're trading when you do."],
         ending="Slide the muffin plate off frame. End on the full plate, no words. Let people rewatch to compare.",
         note="Weigh every food and put the real calorie number on each plate on screen; adjust portions until they truly match. Overhead or 45° angle, clean table, good light. The visual does 80% of the work, keep talking to a minimum."),
    dict(tag="HOT TAKE", day="Tue · Week 2", title="\"Eat Clean\" Is The Worst Advice On The Internet",
         angle="Unpopular opinion", fmt="Talking Head", length="25-35 sec", goal="Comments",
         onscreen="UNPOPULAR OPINION",
         hook="Unpopular opinion from a nutrition coach: \"eat clean\" is the worst advice on the internet.",
         core=["Nobody can tell you what it actually means. Is bread clean? Pasta? A burger you made at home?",
               "What it really does is split food into good and bad. And once a food is \"bad,\" eating it doesn't feel like a meal. It feels like failing.",
               "That's how one cookie turns into the whole sleeve. Not hunger. Guilt.",
               "Food isn't clean or dirty. It's more filling or less filling, more protein or less. That's it. Everything else is marketing."],
         ending="\"Change my mind.\" Then stop. People will try in the comments.",
         note="Say the hook straight into the lens with a half-smile, like you know you're about to start something. Reply to the best comments with video replies, that's where the second wave of views comes from."),
    dict(tag="REAL LIFE", day="Wed · Week 2", title="What I Eat On A Bad Day As A Nutrition Coach",
         angle="Day-in-the-life, flipped", fmt="Vlog · quick cuts", length="35-45 sec", goal="Watch time + follows",
         onscreen="NOT A PERFECT DAY",
         hook="Everyone shows you their perfect day of eating. Here's my bad one.",
         core=["Overslept. Coffee in the car, a protein shake I found in the gym bag. Not cute.",
               "Lunch is a gas station: a turkey sandwich, a cheese stick, a banana. Fine.",
               "3pm, back-to-back calls, I grab a handful of whatever's in the office. Happens.",
               "Dinner at 8:30. Frozen stir-fry and microwave rice. Ten minutes.",
               "Not perfect. But every meal had something that kept me full, and nothing turned into a free-for-all. That's the real skill. Not the perfect days. The bad ones."],
         ending="Last clip: you eating dinner on the couch. \"That's it. That's the secret.\"",
         note="Film it on a genuinely busy day, real locations, phone in hand, no polish. Cut every 2-3 seconds. Honesty is the hook here: the less staged it looks, the better it performs."),
    dict(tag="EXPERIMENT", day="Thu · Week 2", title="I Asked People To Pour One Tablespoon Of Peanut Butter",
         angle="Street / home experiment", fmt="Interactive challenge", length="25-35 sec", goal="Shares",
         onscreen="POUR 1 TBSP",
         hook="I asked three people to pour one tablespoon of peanut butter. Nobody got close.",
         core=["Person one: two and a half tablespoons. Person two: almost three. Person three just laughed.",
               "A real, level tablespoon is around 90 to 100 calories. What most people call \"a spoonful\" is two or three times that.",
               "Peanut butter isn't the problem. Eyeballing it every day for a year is.",
               "You don't need to measure forever. Just do it once, so your eyes learn what one actually looks like."],
         ending="Hand the jar to the camera: \"Your turn.\"",
         note="Use friends, family or gym regulars (get their OK to post). Show the measuring spoon reveal on a kitchen scale for each person, the gap is the punchline. Keep reactions in, they're the reason people share it."),
    dict(tag="SKIT", day="Fri · Week 2", title="The Diet Voice vs. Your Coach At A Birthday Party",
         angle="Two-character skit", fmt="Skit · you play both", length="25-35 sec", goal="Shares + tags",
         onscreen="DIET VOICE vs. COACH",
         hook="The voice in your head at a birthday party vs. what I'd actually tell you.",
         core=["DIET VOICE: \"Don't touch the cake. You already had pizza. Today's ruined anyway, so just go for it.\"",
               "COACH: \"Have the slice. Sit down, enjoy it, talk to people.\"",
               "DIET VOICE: \"But what about tomorrow?\"",
               "COACH: \"Tomorrow you eat breakfast like normal. That's it. One slice of cake never ruined anyone. The 'I already ruined it' part does.\""],
         ending="Diet voice takes a bite, shrugs: \"...okay this is good.\" Cut.",
         note="Change one detail per character (hat, hoodie, side of the frame) so it reads instantly with no sound. Captions on screen are a must. Have fun with it, this is the one that shows Nate's personality."),
    dict(tag="LIST", day="Sat · Week 2", title="Things I'll Never Do As A Nutrition Coach",
         angle="Fast-cut list", fmt="Quick cuts · on-screen text", length="20-30 sec", goal="Saves + comments",
         onscreen="I'LL NEVER…",
         hook="Things I'll never do as a nutrition coach. Number four surprises people.",
         core=["One: skip breakfast to \"save calories\" for a big dinner.",
               "Two: buy anything that says \"guilt-free\" on the label.",
               "Three: drink my calories without noticing. Looking at you, caramel cold brew.",
               "Four: weigh myself the morning after a vacation. That number lies for about a week.",
               "Five: eat dinner standing over the kitchen counter."],
         ending="\"Which one are you guilty of? Number in the comments.\"",
         note="One cut per item, a quick visual for each (empty plate, label close-up, the coffee, a scale with a towel thrown over it, the counter). On-screen number for each one. Fast and punchy, the whole thing should feel like 15 seconds."),
    dict(tag="SOFT OFFER", day="Sun · Week 2", title="Who I Won't Coach",
         angle="Reverse pitch", fmt="Talking Head", length="30-40 sec", goal="Leads", kw="FIT",
         onscreen="I WON'T COACH YOU IF…",
         hook="I only take ten new clients a month. So here's who I'm not taking.",
         core=["If you want to lose twenty pounds by your vacation next week, I'm not your guy.",
               "If you want a meal plan you'll follow for three days and throw away, there are free ones online.",
               "If you think you have to give up pizza forever to get results, I'll spend twelve weeks proving you wrong. But you have to let me.",
               "But if you're busy, you're tired of starting over, and you want something that actually fits your life... that's exactly who I built this for."],
         ending="\"If that's you, DM me FIT.\"",
         note="Calm and a little blunt, not arrogant. Disqualifying people makes the right ones lean in. This is the only video this week with a call to action: keep it soft, one line, then stop."),
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
    <p class="sub">{len(SCRIPTS)} scripts. Built for reach, not just leads.</p>
    <div class="meta">
      <p><b>TARGET</b> — Busy adults 30+ who've tried restrictive diets and want a sustainable way to eat</p>
      <p><b>STYLE</b> — Visual, surprising, real. Things people stop scrolling for, not another coach tip.</p>
      <p><b>FORMAT</b> — 20–45 sec · Experiments, skits, real life &amp; hot takes · Instagram Reels</p>
    </div>
  </div>
  <div class="list"><div class="lh">SCRIPTS IN THIS DOCUMENT</div>{rows}</div>
  <div class="foot"><span>NATE VELAZQUEZ · CONTENT CALENDAR</span><span>01 / {total:02d}</span></div>
</section>''')

for i, s in enumerate(SCRIPTS):
    core = "".join(f"<p>{esc(p)}</p>" for p in s["core"])
    kw = s.get("kw")
    last = (f'<div><span>DM KEYWORD</span><b class="kw">{kw}</b></div>' if kw
            else f'<div><span>GOAL</span><b>{esc(s["goal"])}</b></div>')
    ending = esc(s["ending"])
    if kw: ending = ending.replace(kw, f'<span class="kw">{kw}</span>', 1)
    pages.append(f'''<section class="page">
  <div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
  <div class="top"><span class="sc"><i></i>SCRIPT {i+1} OF {len(SCRIPTS)}</span>{tag_html(s["tag"])}</div>
  <div class="vs">VIDEO SCRIPT</div>
  <h2>{esc(s["title"])}</h2>
  <div class="angle">{esc(s["angle"])}</div>
  <div class="facts">
    <div><span>FORMAT</span><b>{esc(s["fmt"])}</b></div>
    <div><span>LENGTH</span><b>{s["length"]}</b></div>
    <div><span>ON-SCREEN TEXT</span><b>{esc(s["onscreen"])}</b></div>
    {last}
  </div>
  <div class="box"><div class="bh"><em>01</em>THE HOOK</div><p class="hook">“{esc(s["hook"])}”</p></div>
  <div class="box"><div class="bh"><em>02</em>THE BEATS</div><div class="core">{core}</div></div>
  <div class="box{' cta' if kw else ''}"><div class="bh"><em>03</em>{'CALL TO ACTION' if kw else 'THE ENDING'}</div><p class="hook">{ending}</p></div>
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
