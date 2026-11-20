# Genera los guiones de anuncios de Meta de Nate, versión 5 (HTML -> PDF): 3 ángulos nuevos para campañas a mensajes de Instagram.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
CHROME = "/opt/pw-browsers/chromium"

QUOTE = "“Nate was the first coach who understood me. He didn't judge me, and his accountability changed everything.”"

ADS = [
    dict(
        title="Start Before January",
        angle="Seasonal urgency · Talking head walking + holiday B-roll",
        fmt="Walk-and-talk + B-roll", length="35-40 sec", keyword="HOLIDAY",
        why="Coaches scaling right now are running holiday deadline ads: Level Above Fitness (“Reset Before The Holidays”, “Start Strong Before January”, three variants live) and The Den Training (“Enter The New Year With Momentum”). Nate's version plans the holidays instead of avoiding them, which fits the Flex Week Method and passes Meta's health rules.",
        hook="Don't wait for January. Here's why my clients start before the holidays.",
        alts=["Thanksgiving, work parties, family dinners, New Year's. That's what stands between you and January.",
              "Every January my inbox fills up. The clients who do best messaged me in November.",
              "Six weeks of holidays. Here's how my clients get through them without starting over."],
        scenes=[
            ("0-3s", "Don't wait for January. Here's why my clients start before the holidays.",
             "Nate walking toward camera outside (Tampa street or park), handheld, close.", "DON'T WAIT FOR JANUARY"),
            ("3-9s", "Between now and New Year's you've got Thanksgiving, work parties, family dinners. Most people write the whole season off and say they'll start fresh in January.",
             "Quick cuts: a full holiday table, drinks at an office party, a calendar with December dates filling up.", "THANKSGIVING · PARTIES · NEW YEAR'S"),
            ("9-15s", "Then January comes, and they're starting from further back, at the same time as everyone else.",
             "A packed gym or a crowded grocery aisle. Cut back to Nate, who shrugs.", "STARTING FROM FURTHER BACK"),
            ("15-26s", "My clients plan for those weeks. We pick which dinners matter, what to eat before the party, and what the next morning looks like, so one big night stays one big night.",
             "Nate on his phone reviewing a check-in. Hands building a holiday plate. Morning coffee and a protein shake on the counter.", "PLAN THE BIG NIGHTS"),
            ("26-31s", "So when January gets here, they're already six weeks in.",
             "Back to Nate, walking, smiling at camera.", "JANUARY = WEEK 6"),
            ("31-38s", "I'm taking a few new clients before the holidays. Send me a message with the word HOLIDAY and I'll ask you three quick questions.",
             "Nate stops walking, points down to the button. Keyword appears big on screen.", "DM “HOLIDAY”"),
        ],
        primary="Thanksgiving, work parties, family dinners, New Year's. Most people write off the next six weeks and promise to start in January.\n\nMy clients plan for those weeks instead. We decide which dinners matter, what to eat before the party and what the next morning looks like, so one big night stays one big night.\n\nBy January they're already six weeks in.\n\nI'm taking a few new 1-on-1 clients before the holidays. Send me a message with the word HOLIDAY and I'll ask you 3 quick questions.",
        headline="Start before January",
        audience="Tampa + 30 mi, cold audience, Advantage+ on. Run it now through mid-December, then retire it.",
        notes="Confirm with Nate how many spots he really has before the holidays: the ad says “a few”, so it has to be true.",
    ),
    dict(
        title="You've Seen My Videos",
        angle="Warm audience · Behind the scenes of a real weekly check-in",
        fmt="Desk talking head + screen recording", length="35-40 sec", keyword="COACH",
        why="Nate's organic reach is up, so many people already know his face but have never seen what working with him looks like. This ad turns that attention into conversations. Coaches who run authority and behind-the-scenes ads (Tyler, “Coached by a Pro Card Coach”, five variants live) keep a whole ad set aimed at people who already follow them.",
        hook="You've watched my videos. This is what happens when you actually work with me.",
        alts=["If my videos keep showing up on your feed, this one's for you.",
              "The tips are free. Here's what changes when I'm your coach.",
              "This is a real weekly check-in with one of my clients, start to finish."],
        scenes=[
            ("0-3s", "You've watched my videos. This is what happens when you actually work with me.",
             "Nate seated at his desk, laptop open, natural light. Slow push in.", "WHAT COACHING WITH ME LOOKS LIKE"),
            ("3-8s", "The videos give you the tips. Coaching is where we use them on your actual week.",
             "Fast montage: screen recording scrolling his Instagram grid and two of his most viewed reels.", "THE TIPS → YOUR WEEK"),
            ("8-20s", "Every Sunday you send me a quick check-in: how the week went, your energy, your sleep, what got in the way. I read every one myself and send you back a video with what we change.",
             "Screen recording of a check-in form (client name and photo blurred, with permission). Nate recording a short video reply on his laptop.", "WEEKLY CHECK-IN · PERSONAL VIDEO REPLY"),
            ("20-28s", "Late meeting on Wednesday? We adjust Thursday. Traveling next week? We plan it now.",
             "Phone close-up: a message thread with Nate (blurred). The plan document being edited.", "ADJUSTED EVERY WEEK"),
            ("28-33s", "That's why clients tell me things like this.",
             "Client quote on screen, word by word, over a slow shot of Nate at the desk.", "CLIENT QUOTE (FULL TEXT)"),
            ("33-39s", "If you've been watching for a while, this is the next step. Send me a message with the word COACH.",
             "Nate looks at camera, closes the laptop. Keyword appears big on screen.", "DM “COACH”"),
        ],
        primary="If my videos have been showing up on your feed, thanks for watching.\n\nThe tips are free. Coaching is the part where we use them on your actual week: a check-in every Sunday, a personal video reply from me, and changes to your plan before the next week starts.\n\nOne client put it like this: " + QUOTE + "\n\nSend me a message with the word COACH and I'll ask you 3 quick questions to see if we're a fit.",
        headline="Coaching with me, week by week",
        audience="Warm audience: people who engaged with Nate's Instagram or watched his videos in the last 365 days (custom audiences). Small budget, high intent.",
        notes="The check-in footage needs written OK from the client and every name or face blurred. If there's no real check-in to show, Nate can fill out the form himself as a demo and say so.",
    ),
    dict(
        title="Keep The Food You Love",
        angle="Food demo · B-roll heavy, plate built on camera",
        fmt="Kitchen demo + voiceover", length="30-37 sec", keyword="FOOD",
        why="Ownfitbody is scaling “Keep Your Food. Get a Plan.” with several variants live at once, and trizzlemanfitness runs a “volume eating” workshop: keeping the food people love is the angle the market is buying. The ending copies the conversational pattern of Rad Training (“Tell me your hardest day.”): asking for something personal gets more DMs than “apply now”.",
        hook="Your favorite food stays. Here's how I fit it into a client's week.",
        alts=["Tacos on a Friday night? Still on the plan. Watch.",
              "The first thing new clients ask me is what they have to give up. Usually it's less than they think.",
              "Same tacos, two different plates. Here's the difference."],
        scenes=[
            ("0-3s", "Your favorite food stays. Here's how I fit it into a client's week.",
             "Nate drops a takeout bag on the kitchen counter and pulls out tacos (or a burger). Overhead camera.", "KEEP THE TACOS"),
            ("3-9s", "The first thing new clients ask me is what they have to cut out. For most of them, their favorite food stays.",
             "Nate to camera, leaning on the counter, tacos in front of him.", "WHAT DO I HAVE TO CUT OUT?"),
            ("9-21s", "We look at the rest of the plate instead. Add a protein, add something fresh, keep the amount you'd actually enjoy, and put it on a night that fits your week.",
             "Overhead, fast cuts with a sound on each: grilled chicken added, salad and salsa added, the plate finished. Side by side with the original plate.", "+ PROTEIN · + SOMETHING FRESH · SAME TACOS"),
            ("21-28s", "When the food you love is part of the plan, Friday night stops being the night everything falls apart.",
             "Nate sitting down to eat, relaxed, laughing with someone off camera.", "PART OF THE PLAN"),
            ("28-36s", "Tell me your favorite food. Send me a message with the word FOOD, and I'll show you how it fits into your week.",
             "Nate to camera with the plate, points down to the button. Keyword appears big on screen.", "DM “FOOD”"),
        ],
        primary="The first question almost every new client asks me: what do I have to cut out?\n\nFor most of them, the answer is less than they think. Their favorite food stays. We change what goes around it, how much feels right and which night it lands on.\n\nThat's how a plan survives a Friday night.\n\nSend me a message with the word FOOD and tell me your favorite meal. I'll tell you how it fits into your week.",
        headline="Keep the food you love",
        audience="Tampa + 30 mi, cold audience, Advantage+ on. This one can run long term: it isn't tied to a season.",
        notes="Use food Nate actually eats or recommends. No calorie numbers on screen and no talk about the viewer's body or weight.",
    ),
]

def esc(s): return html.escape(s, quote=False)
def paras(s): return "".join(f"<p>{esc(p)}</p>" for p in s.split("\n\n"))
N = len(ADS)

cards = "".join(f'''<div class="ov"><div class="ovn">0{i+1}</div><div><h3>{esc(a["title"])}</h3>
  <p class="ova">{esc(a["angle"])}</p><p class="ovh">“{esc(a["hook"])}”</p>
  <p class="ovk">DM keyword: <b>{a["keyword"]}</b> · {a["length"]}</p></div></div>''' for i, a in enumerate(ADS))

pages = [f'''<section class="page">
  <div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
  <div class="top"><span class="sc"><i></i>META AD SCRIPTS · V5</span><span class="tag">NOVEMBER 2026</span></div>
  <h1>3 new ads for Instagram DMs</h1>
  <p class="lead">Nate's videos are reaching more people than ever. These three ads use that moment with angles the account hasn't tested yet. Every ad ends with a different word to send by DM, so each conversation tells us which ad it came from.</p>
  {cards}
  <div class="box note"><div class="bh"><em>!</em>RULES FOR ALL THREE</div>
    <p>Vertical 9:16, with captions on screen and all text kept in the middle of the frame (away from the top 14% and bottom 35%, where Instagram puts its buttons). The first 3 seconds must show something moving and the hook written on screen. No talk about the viewer's body or weight, no promised results, no before-and-after photos. Already-tested angles we're not repeating: “Monday restart”, “every diet worked”, “busy day of eating”, “busy professionals in Tampa”.</p></div>
  <div class="foot"><span>NATE VELAZQUEZ · META AD SCRIPTS V5</span><span>00 / {N:02d}</span></div>
</section>''']

for i, a in enumerate(ADS):
    rows = "".join(f'<tr><td class="t">{esc(t)}</td><td class="say">“{esc(s)}”</td><td>{esc(b)}</td><td class="ost">{esc(o)}</td></tr>' for t, s, b, o in a["scenes"])
    pages.append(f'''<section class="page">
  <div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
  <div class="top"><span class="sc"><i></i>AD {i+1} OF {N}</span><span class="tag">PAID AD · IG DMs</span></div>
  <h2>{esc(a["title"])}</h2>
  <div class="angle">{esc(a["angle"])}</div>
  <div class="facts">
    <div><span>FORMAT</span><b>{esc(a["fmt"])}</b></div>
    <div><span>LENGTH</span><b>{a["length"]}</b></div>
    <div><span>OBJECTIVE</span><b>Instagram DMs</b></div>
    <div><span>DM KEYWORD</span><b class="kw">{a["keyword"]}</b></div>
  </div>
  <div class="box"><div class="bh"><em>01</em>THE HOOK</div><p class="hook">“{esc(a["hook"])}”</p>
    <div class="alts"><span>ALTERNATE HOOKS · SAME VIDEO, RECORD ALL FOUR OPENINGS AND TEST THE FIRST 3 SECONDS</span>{"".join(f"<p>“{esc(h)}”</p>" for h in a["alts"])}</div></div>
  <div class="box"><div class="bh"><em>02</em>SCRIPT · SCENE BY SCENE</div>
    <table><tr><th>TIME</th><th>NATE SAYS</th><th>B-ROLL / VISUAL</th><th>ON-SCREEN TEXT</th></tr>{rows}</table></div>
  <div class="foot"><span>NATE VELAZQUEZ · META AD SCRIPTS V5</span><span>{i+1:02d}A / {N:02d}</span></div>
</section>''')
    pages.append(f'''<section class="page">
  <div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
  <div class="top"><span class="sc"><i></i>AD {i+1} OF {N} · AD COPY</span><span class="tag">PAID AD · IG DMs</span></div>
  <h2>{esc(a["title"])}</h2>
  <div class="box"><div class="bh"><em>03</em>WHY THIS ANGLE</div><p class="body">{esc(a["why"])}</p></div>
  <div class="box"><div class="bh"><em>04</em>PRIMARY TEXT</div><div class="copy">{paras(a["primary"])}</div></div>
  <div class="facts two">
    <div><span>HEADLINE</span><b>{esc(a["headline"])}</b></div>
    <div><span>BUTTON</span><b>Send message</b></div>
  </div>
  <div class="box cta"><div class="bh"><em>05</em>CALL TO ACTION (SPOKEN)</div><p class="hook">“{esc(a["scenes"][-1][1])}”</p></div>
  <div class="box"><div class="bh"><em>06</em>AUDIENCE</div><p class="body">{esc(a["audience"])}</p></div>
  <div class="box note"><div class="bh"><em>!</em>BEFORE RECORDING</div><p>{esc(a["notes"])}</p></div>
  <div class="foot"><span>NATE VELAZQUEZ · META AD SCRIPTS V5</span><span>{i+1:02d}B / {N:02d}</span></div>
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
h1 { font-size: 26pt; font-weight: 800; margin-top: 18pt; line-height: 1.15; }
.lead { color: #a6a6b3; font-size: 10.4pt; line-height: 1.6; margin-top: 10pt; }
.ov { display: flex; gap: 14pt; background: #131318; border: .75pt solid #22222b; border-radius: 7pt; padding: 13pt 14pt; margin-top: 10pt; }
.ovn { font-size: 20pt; font-weight: 800; color: #5b7cfa; line-height: 1; }
.ov h3 { font-size: 12.5pt; font-weight: 800; }
.ova { font-size: 8.6pt; color: #a6a6b3; margin-top: 3pt; }
.ovh { font-size: 9.6pt; font-weight: 700; margin-top: 7pt; line-height: 1.45; }
.ovk { font-size: 8.2pt; color: #67666f; margin-top: 6pt; }
.ovk b { color: #5b7cfa; }
h2 { font-size: 20.2pt; font-weight: 800; margin-top: 12pt; line-height: 1.2; }
.angle { color: #a6a6b3; font-size: 10.1pt; margin-top: 4pt; }
.facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin-top: 12pt; }
.facts.two { grid-template-columns: 1fr 1fr; margin-top: 9pt; }
.facts div { background: #131318; border: .75pt solid #22222b; border-radius: 6pt; padding: 10pt 10pt 12pt; }
.facts span { display: block; font-size: 7.1pt; letter-spacing: .06em; color: #67666f; margin-bottom: 8pt; }
.facts b { font-size: 9.6pt; font-weight: 700; }
.kw { color: #5b7cfa; font-weight: 700; }
.box { background: #131318; border: .75pt solid #22222b; border-radius: 7pt; padding: 12pt 13pt; margin-top: 9pt; }
.bh { font-size: 7.9pt; font-weight: 700; letter-spacing: .08em; color: #67666f; margin-bottom: 8pt; }
.bh em { font-style: normal; color: #5b7cfa; font-size: 9.8pt; margin-right: 7pt; }
.hook { font-size: 10.6pt; font-weight: 700; line-height: 1.45; }
.body { font-size: 8.9pt; color: #a6a6b3; line-height: 1.7; }
.copy p { font-size: 9.6pt; color: #e4e4ea; line-height: 1.65; }
.copy p + p { margin-top: 7pt; }
.box.cta { background: #10142a; border-color: #2a3778; }
.alts { margin-top: 9pt; padding-top: 8pt; border-top: .75pt solid #22222b; }
.alts span { display: block; font-size: 6.8pt; font-weight: 700; letter-spacing: .08em; color: #67666f; margin-bottom: 4pt; }
.alts p { font-size: 8.8pt; color: #a6a6b3; line-height: 1.6; }
.box.note p { font-size: 8.2pt; color: #a6a6b3; font-style: italic; line-height: 1.7; }
table { width: 100%; border-collapse: collapse; }
th { font-size: 6.6pt; letter-spacing: .08em; color: #67666f; text-align: left; padding: 0 6pt 6pt 0; font-weight: 700; }
td { font-size: 7.7pt; color: #a6a6b3; line-height: 1.5; padding: 6pt 6pt 6pt 0; border-top: .75pt solid #22222b; vertical-align: top; }
td.t { color: #5b7cfa; font-weight: 700; white-space: nowrap; width: 9%; }
td.say { color: #f4f4f7; width: 38%; }
td.ost { color: #facc15; font-weight: 700; width: 20%; }
"""

doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Nate Velazquez Meta Ad Scripts V5</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "NateVelazquez_MetaAdScripts_v5.pdf"
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
