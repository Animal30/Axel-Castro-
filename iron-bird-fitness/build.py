# Genera el calendario de contenido de Iron Bird Fitness (HTML -> PDF), mismo diseño que el calendario del 10/1/26.
import html, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
OUT = "IronBirdFitness_ContentCalendar_Week2.pdf"

SCRIPTS = [
    dict(title="The Weight On The Bar Is Lying To You", angle="Talking Head · Contrarian angle", fmt="Talking Head", length="30-40 sec", kw="FORM",
         hook="The heaviest weight you've ever lifted might be the reason you stopped making progress.",
         core=["Most people judge a workout by the number on the bar. More plates, better session. Except half of those reps are being lifted by momentum, a swinging back and a range of motion that's been quietly cut in half.",
               "Your muscles don't know what's written on the plate. They only know how much tension they're under, and for how long.",
               "The fastest progress I've seen came right after someone dropped the weight and fixed the rep.",
               "Lighter and controlled beats heavy and sloppy. Every time, for every goal."],
         cta="DM me FORM. I'll show you the three cues I fix first with every new client."),
    dict(title="You Don't Need More Time. You Need Three Sessions.", angle="Talking Head · Mindset angle", fmt="Talking Head", length="30-40 sec", kw="THREE",
         hook="‘I don't have time’ usually means ‘I don't have a plan that fits the time I have.’",
         core=["Most people think getting in shape means an hour a day, six days a week. So they wait for a season of life that has that kind of time. It never comes.",
               "Three focused sessions a week, forty-five minutes each, is less than two and a half hours. That's less than one evening of scrolling.",
               "The clients with the busiest calendars are often the most consistent ones, because their sessions are short, planned and non-negotiable.",
               "You don't need more hours. You need fewer, better ones, already on the calendar."],
         cta="DM me THREE. I'll show you what a three-day week actually looks like."),
    dict(title="Your Back Doesn't Hurt Because You're Getting Older", angle="Educational · Authority angle", fmt="Educational", length="35-45 sec", kw="BACK",
         hook="If your back gets stiff every time you sit for too long, age is probably not the real reason.",
         core=["Eight hours in a chair, a long commute, then the couch. Day after day, the muscles that are supposed to support your spine slowly stop doing their job.",
               "For a lot of people, it isn't age. It's what happens to a body that sits all day and never gets asked to get strong.",
               "Some of the biggest changes I see aren't on the scale. They're people who can pick up their kids, sit through a meeting or play a round of golf without thinking about their back.",
               "Strength isn't the thing you build after you feel better. Very often, it's how you start feeling better. (If pain is sharp or ongoing, see your doctor first.)"],
         cta="DM me BACK. I'll send you the four movements we start with."),
    dict(title="Progress Is Boring On Purpose", angle="Talking Head · Mindset angle", fmt="Talking Head", length="30-40 sec", kw="TRACK",
         hook="If your workouts feel exciting every single week, you're probably not progressing.",
         core=["New exercises, new routines, a different video every Monday. It feels like progress because it feels new. But your body can't adapt to something it only does once.",
               "Real progress looks boring on paper: the same lifts, a little more weight or one more rep than last week, written down so you can see it.",
               "Every one of my clients has a log, because the clients who track are the ones who can prove they're getting stronger.",
               "Exciting keeps you entertained. Boring and tracked keeps you improving."],
         cta="DM me TRACK. I'll show you exactly how we log every session."),
    dict(title="You're Comparing Your Week One To Their Year Five", angle="Talking Head · Mindset angle", fmt="Talking Head", length="30-40 sec", kw="LANE",
         hook="The guy next to you at the gym isn't your competition. He's year five. You're week one.",
         core=["Everybody does it: you look at someone stronger, leaner or more experienced and decide you're behind. Then the comparison quietly turns into a reason to stop.",
               "You're not seeing their first year. The bad form, the missed weeks, the plateaus. You're only seeing the result of all of it.",
               "The only number I care about for my clients is how they compare to themselves four weeks ago.",
               "Stay in your lane long enough and you become the person somebody else is comparing themselves to."],
         cta="DM me LANE. Let's set a starting point you can actually beat."),
    dict(title="Strength Is The Most Underrated Thing After 30", angle="Educational · Authority angle", fmt="Educational", length="35-45 sec", kw="STRONG",
         hook="If you only do cardio to stay in shape, you're skipping the part that matters most the older you get.",
         core=["Cardio is great for your heart. But muscle is what keeps your metabolism up, protects your joints and decides how well you move at fifty, sixty and beyond.",
               "Most adults slowly lose muscle every decade they don't train for it. You don't notice it happening. You notice it when stairs, bags and kids start feeling heavier.",
               "Every program we build starts with strength, and cardio supports it, not the other way around.",
               "Lift now for the person you want to be in twenty years."],
         cta="DM me STRONG. I'll show you how we build strength into a busy week."),
    dict(title="The Gym Isn't The Hard Part. Walking In Is.", angle="Talking Head · Personal story angle", fmt="Talking Head", length="30-40 sec", kw="START",
         hook="The hardest rep you'll ever do is opening the door the first day.",
         core=["Not knowing where to start. Feeling like everyone is watching. Not wanting to look like you don't belong. That's what keeps most people out, not the workout itself.",
               "Here's the truth: nobody in a good gym is judging the new person. They remember being that person.",
               "My job on day one isn't to push you. It's to make sure you know exactly what to do, so walking in feels easy the second time.",
               "The workout gets easier with practice. So does walking through the door."],
         cta="DM me START. Let's make your first session the easy part."),
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
subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={HERE/OUT}", str(src)], check=True, stderr=subprocess.DEVNULL)
src.unlink(); print(HERE/OUT)
