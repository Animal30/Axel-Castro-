# Genera los guiones de anuncios de Meta de Nate, versión 6 (HTML -> PDF): los 3 ángulos de la v5 con cada dato respaldado por estudios citados.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
CHROME = "/opt/pw-browsers/chromium"

QUOTE = "“Nate was the first coach who understood me. He didn't judge me, and his accountability changed everything.”"

ADS = [
    dict(
        title="Start Before January",
        angle="Seasonal urgency · Science-backed · Walk-and-talk + holiday B-roll",
        fmt="Walk-and-talk + B-roll", length="38-42 sec", keyword="HOLIDAY",
        why="Three findings, one story. NIH researchers found holiday weight gain is small but tends to stay (Yanovski, NEJM 2000). Wharton researchers showed people wait for dates like January 1 to start (the fresh start effect). And a review of 94 studies found that deciding ahead of time what you'll do in a specific situation (an if-then plan) helps people reach their goals. That last finding is exactly what Nate does with clients for the holidays. Holiday deadline ads are also what other coaches are scaling right now (Level Above Fitness, The Den Training).",
        hook="NIH researchers weighed 195 adults before and after the holidays. Here's what they found.",
        alts=["Waiting until January to start has a name in behavioral science. And it works against you.",
              "There's a 94-study review on how to get through the holidays without starting over.",
              "Don't wait for January. Here's what the research says."],
        scenes=[
            ("0-3s", "NIH researchers weighed 195 adults before and after the holidays. Here's what they found.",
             "Nate walking toward camera outside, handheld, close.", "195 ADULTS. ONE HOLIDAY SEASON.", "Yanovski et al., NEJM 2000"),
            ("3-11s", "The weight people put on between Thanksgiving and New Year's was small, less than a pound on average. The catch? A year later, it was still there.",
             "Holiday table, pie being sliced, calendar with late-December dates.", "SMALL. BUT IT STAYED.", "NIH follow-up, 1 year later"),
            ("11-18s", "Most people plan to fix it in January. Researchers at Wharton call that the fresh start effect: we wait for a new week, a new month or a new year to begin.",
             "Calendar flips to January 1. A packed gym in January.", "THE FRESH START EFFECT", "Dai, Milkman & Riis, 2014"),
            ("18-29s", "What works better is a plan you make ahead of time. In a review of 94 studies, people who decided in advance, like ‘at the party, I eat protein first’, reached their goals more often than people who only set the goal.",
             "Nate typing a plan on his phone. Overhead: a plate built protein first.", "IF-THEN PLANS", "Gollwitzer & Sheeran, 2006 · 94 studies"),
            ("29-34s", "That's what I build with my clients for every big night between now and New Year's.",
             "Nate on a call with a client (screen or phone), nodding.", "A PLAN FOR EVERY BIG NIGHT", ""),
            ("34-41s", "Send me a message with the word HOLIDAY, and I'll ask you three quick questions to see if we're a fit.",
             "Nate stops walking, points down to the button. Keyword appears big.", "DM “HOLIDAY”", ""),
        ],
        primary="NIH researchers followed 195 adults through the holiday season. The weight they put on was small, less than a pound on average. A year later, it was still there.\n\nThe usual plan is to fix it in January. Behavioral scientists call that the fresh start effect.\n\nWhat works better is deciding in advance. In a review of 94 studies, people who made if-then plans (“at the party, I eat protein first”) reached their goals more often than people who only set the goal.\n\nThat's what I build with my clients for every big night between now and New Year's.\n\nSend me a message with the word HOLIDAY and I'll ask you 3 quick questions.",
        headline="Your holiday plan, made in advance",
        audience="Tampa + 30 mi, cold audience, Advantage+ on. Run it now through mid-December, then retire it.",
        notes="The study talks about weight in general terms (third person), which Meta allows; never turn it into “you'll gain weight”. Show the source on screen every time a number appears.",
    ),
    dict(
        title="The Habit In 138 Studies",
        angle="Warm audience · Science-backed · Behind the scenes of a weekly check-in",
        fmt="Desk talking head + screen recording", length="36-40 sec", keyword="COACH",
        why="A 2016 review in Psychological Bulletin pooled 138 experiments with 19,951 people, mostly on health goals like diet and exercise. People prompted to track their progress reached their goals more often, and the effect was larger when progress was reported to someone else or written down (Harkin et al.). A weekly check-in with a coach is exactly that, so the study explains why coaching works better than free tips. Aimed at people who already watch Nate's videos.",
        hook="138 studies. Almost 20,000 people. One habit kept showing up in the people who reached their goals.",
        alts=["You've watched my videos. Here's the one thing they can't do for you.",
              "There's a reason my clients check in with me every Sunday. It's in the research.",
              "If my videos keep showing up on your feed, this one's for you."],
        scenes=[
            ("0-3s", "138 studies. Almost 20,000 people. One habit kept showing up in the people who reached their goals.",
             "Nate at his desk, laptop open. Slow push in.", "138 STUDIES · 19,951 PEOPLE", "Harkin et al., Psychological Bulletin 2016"),
            ("3-11s", "Researchers looked at goals like eating better and getting healthier. The people who tracked their progress reached their goals more often.",
             "Close-up: a check-in form on screen, a notebook with a weekly log.", "TRACKING PROGRESS", ""),
            ("11-17s", "And it worked even better when they reported that progress to someone else.",
             "Phone: a message being sent to Nate (name blurred).", "EVEN BETTER WHEN SOMEONE SEES IT", ""),
            ("17-28s", "That's the part my videos can't do for you. With coaching, you send me a check-in every Sunday. I read it myself and send you back a video with what we change for next week.",
             "Screen recording of a check-in (client blurred, with permission). Nate recording a video reply.", "WEEKLY CHECK-IN · VIDEO REPLY", ""),
            ("28-33s", "That's why clients tell me things like this.",
             "Client quote typed out on screen over a slow shot of Nate.", "CLIENT QUOTE (FULL TEXT)", ""),
            ("33-39s", "If you've been watching my videos for a while, this is the next step. Send me a message with the word COACH.",
             "Nate looks at camera, closes the laptop. Keyword appears big.", "DM “COACH”", ""),
        ],
        primary="A 2016 review pooled 138 studies with almost 20,000 people working on goals like eating better and getting healthier.\n\nThe people who tracked their progress reached their goals more often. And it worked even better when they reported that progress to someone else.\n\nThat's the part free tips can't do. With coaching, you send me a check-in every Sunday, I read it myself, and you get a video back with what we change for next week.\n\nOne client put it like this: " + QUOTE + "\n\nSend me a message with the word COACH and I'll ask you 3 quick questions to see if we're a fit.",
        headline="Why my clients check in every week",
        audience="Warm audience: people who engaged with Nate's Instagram or watched his videos in the last 365 days (custom audiences). Small budget, high intent.",
        notes="Say “more often”, never “guaranteed” or a percentage: the review found a moderate effect. Check-in footage needs the client's written OK and blurred names and faces.",
    ),
    dict(
        title="The Milkshake Study",
        angle="Cold audience · Science-backed · Food demo, plate built on camera",
        fmt="Kitchen demo + talking head", length="35-38 sec", keyword="FOOD",
        why="A classic 1975 experiment (Herman & Mack) gave people a milkshake, then free ice cream: strict dieters ate about two-thirds more ice cream after the milkshake, as if the day was already lost. A study of 1,838 adults (Westenhoefer et al., 1999) linked all-or-nothing eating rules to more binge eating and flexible rules to better results. And a review in the American Journal of Clinical Nutrition (Leidy et al., 2015) found protein helps people feel full. Together they explain Nate's approach: keep the favorite food and build the plate around it. Competitors are scaling the same promise (Ownfitbody, “Keep Your Food. Get a Plan.”).",
        hook="In a classic study, strict dieters drank one milkshake. Then they ate more ice cream than anyone.",
        alts=["Cutting out your favorite food can backfire. There's a study on this.",
              "One milkshake made dieters eat more ice cream. Here's why.",
              "Your favorite food stays. Here's what the research says."],
        scenes=[
            ("0-3s", "In a classic study, strict dieters drank one milkshake. Then they ate more ice cream than anyone.",
             "Nate sets a milkshake on the kitchen counter, looks at camera.", "ONE MILKSHAKE. THEN WHAT?", "Herman & Mack, 1975"),
            ("3-12s", "Researchers gave people a milkshake, then all the ice cream they wanted. Strict dieters ate about two-thirds more after the milkshake. Once the rule was broken, the day felt lost.",
             "Ice cream tub, spoon digging in. Cut to Nate shaking his head.", "‘I ALREADY BLEW IT’", ""),
            ("12-20s", "A later study of almost 2,000 people found the same pattern. All-or-nothing food rules went with more binge eating. Flexible rules went with better results.",
             "Split screen: a crossed-out ‘forbidden foods’ list vs. a balanced plate.", "ALL-OR-NOTHING VS. FLEXIBLE", "Westenhoefer et al., 1999 · 1,838 adults"),
            ("20-30s", "So my clients keep the food they love. We build the plate around it: protein first, about 25 to 30 grams, which helps you feel full. Then something fresh. And the tacos stay.",
             "Overhead, fast cuts: grilled chicken added, salad and salsa added, tacos on the plate.", "+ 25-30 g PROTEIN · + SOMETHING FRESH · SAME TACOS", "Leidy et al., Am J Clin Nutr 2015"),
            ("30-37s", "Tell me your favorite food. Send me a message with the word FOOD, and I'll show you how it fits into your week.",
             "Nate to camera with the plate, points down to the button. Keyword appears big.", "DM “FOOD”", ""),
        ],
        primary="In a classic 1975 study, researchers gave people a milkshake and then all the ice cream they wanted. Strict dieters ate about two-thirds more ice cream after the milkshake. Once the rule was broken, the day felt lost.\n\nA later study of 1,838 adults found the same pattern: all-or-nothing food rules went with more binge eating, and flexible rules went with better results.\n\nSo my clients keep the food they love. We build the plate around it, starting with protein, which helps you feel full.\n\nSend me a message with the word FOOD and tell me your favorite meal. I'll show you how it fits into your week.",
        headline="Keep the food you love",
        audience="Tampa + 30 mi, cold audience, Advantage+ on. Not tied to a season, so it can run long term.",
        notes="Say “went with” or “was linked to” for the 1999 study: it shows an association, not cause and effect. No calorie counts and no talk about the viewer's body.",
    ),
]

SOURCES = [
    ("Yanovski JA, Yanovski SZ, Sovik KN, et al. A prospective study of holiday weight gain. New England Journal of Medicine. 2000;342(12):861-867.", "pubmed.ncbi.nlm.nih.gov/10727591", "195 adults; +0.37 kg over the holidays, not lost by the following year (NIH follow-up of 165 participants)."),
    ("Dai H, Milkman KL, Riis J. The fresh start effect: temporal landmarks motivate aspirational behavior. Management Science. 2014;60(10):2563-2582.", "faculty.wharton.upenn.edu/wp-content/uploads/2014/06/Dai_Fresh_Start_2014_Mgmt_Sci.pdf", "Gym visits and diet searches rise at the start of a week, month or year."),
    ("Gollwitzer PM, Sheeran P. Implementation intentions and goal achievement: a meta-analysis of effects and processes. Advances in Experimental Social Psychology. 2006;38:69-119.", "doi.org/10.1016/S0065-2601(06)38002-1", "94 studies, 8,000+ people; if-then plans improved goal attainment (d = 0.65)."),
    ("Harkin B, Webb TL, Chang BPI, et al. Does monitoring goal progress promote goal attainment? A meta-analysis of the experimental evidence. Psychological Bulletin. 2016;142(2):198-229.", "eprints.whiterose.ac.uk/91437", "138 studies, 19,951 people; larger effect when progress was reported to others or recorded."),
    ("Herman CP, Mack D. Restrained and unrestrained eating. Journal of Personality. 1975;43(4):647-660.", "pubmed.ncbi.nlm.nih.gov/1206453", "After a milkshake, restrained eaters ate more ice cream (about 66% more); unrestrained eaters ate less."),
    ("Westenhoefer J, Stunkard AJ, Pudel V. Validation of the flexible and rigid control dimensions of dietary restraint. International Journal of Eating Disorders. 1999;26(1):53-64.", "doi.org/10.1002/(SICI)1098-108X(199907)26:1<53::AID-EAT7>3.0.CO;2-N", "1,838 adults; rigid control linked to more binge eating, flexible control to better outcomes."),
    ("Leidy HJ, Clifton PM, Astrup A, et al. The role of protein in weight loss and maintenance. American Journal of Clinical Nutrition. 2015;101(6):1320S-1329S.", "pubmed.ncbi.nlm.nih.gov/25926512", "Higher-protein meals increase fullness; about 25-30 g of protein per meal."),
]

def esc(s): return html.escape(s, quote=False)
def paras(s): return "".join(f"<p>{esc(p)}</p>" for p in s.split("\n\n"))
N = len(ADS)

cards = "".join(f'''<div class="ov"><div class="ovn">0{i+1}</div><div><h3>{esc(a["title"])}</h3>
  <p class="ova">{esc(a["angle"])}</p><p class="ovh">“{esc(a["hook"])}”</p>
  <p class="ovk">DM keyword: <b>{a["keyword"]}</b> · {a["length"]}</p></div></div>''' for i, a in enumerate(ADS))

pages = [f'''<section class="page">
  <div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
  <div class="top"><span class="sc"><i></i>META AD SCRIPTS · V6</span><span class="tag">NOVEMBER 2026</span></div>
  <h1>3 science-backed ads for Instagram DMs</h1>
  <p class="lead">Nate's videos are reaching more people than ever. These three ads use that moment with angles the account hasn't tested yet, and every number Nate says comes from a published study, shown on screen with its source. Every ad ends with a different word to send by DM, so each conversation tells us which ad it came from.</p>
  {cards}
  <div class="box note"><div class="bh"><em>!</em>RULES FOR ALL THREE</div>
    <p>Vertical 9:16, with captions on screen and all text kept in the middle of the frame (away from the top 14% and bottom 35%, where Instagram puts its buttons). The first 3 seconds must show something moving and the hook written on screen. Every study is quoted with its source on screen, in plain words, without exaggerating what it found. No talk about the viewer's body or weight, no promised results, no before-and-after photos. Already-tested angles we're not repeating: “Monday restart”, “every diet worked”, “busy day of eating”, “busy professionals in Tampa”.</p></div>
  <div class="foot"><span>NATE VELAZQUEZ · META AD SCRIPTS V6</span><span>00 / {N:02d}</span></div>
</section>''']

for i, a in enumerate(ADS):
    rows = "".join(f'<tr><td class="t">{esc(t)}</td><td class="say">“{esc(s)}”</td><td>{esc(b)}</td><td class="ost">{esc(o)}{f'<span class="src">{esc(r)}</span>' if r else ''}</td></tr>' for t, s, b, o, r in a["scenes"])
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
  <div class="foot"><span>NATE VELAZQUEZ · META AD SCRIPTS V6</span><span>{i+1:02d}A / {N:02d}</span></div>
</section>''')
    pages.append(f'''<section class="page">
  <div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
  <div class="top"><span class="sc"><i></i>AD {i+1} OF {N} · AD COPY</span><span class="tag">PAID AD · IG DMs</span></div>
  <h2>{esc(a["title"])}</h2>
  <div class="box"><div class="bh"><em>03</em>THE SCIENCE BEHIND IT</div><p class="body">{esc(a["why"])}</p></div>
  <div class="box"><div class="bh"><em>04</em>PRIMARY TEXT</div><div class="copy">{paras(a["primary"])}</div></div>
  <div class="facts two">
    <div><span>HEADLINE</span><b>{esc(a["headline"])}</b></div>
    <div><span>BUTTON</span><b>Send message</b></div>
  </div>
  <div class="box cta"><div class="bh"><em>05</em>CALL TO ACTION (SPOKEN)</div><p class="hook">“{esc(a["scenes"][-1][1])}”</p></div>
  <div class="box"><div class="bh"><em>06</em>AUDIENCE</div><p class="body">{esc(a["audience"])}</p></div>
  <div class="box note"><div class="bh"><em>!</em>BEFORE RECORDING</div><p>{esc(a["notes"])}</p></div>
  <div class="foot"><span>NATE VELAZQUEZ · META AD SCRIPTS V6</span><span>{i+1:02d}B / {N:02d}</span></div>
</section>''')

rows = "".join(f'<div class="srcrow"><b>{i+1}.</b><div><p class="cit">{esc(c)}</p><p class="find">{esc(f)}</p><p class="url">{esc(u)}</p></div></div>' for i, (c, u, f) in enumerate(SOURCES))
pages.append(f'''<section class="page">
  <div class="eyebrow">NATE VELAZQUEZ \u00b7 @_NATEVELAZQUEZ</div>
  <div class="top"><span class="sc"><i></i>SOURCES</span><span class="tag">PEER-REVIEWED</span></div>
  <h2>The studies behind every claim</h2>
  <p class="lead">If someone asks in the comments or DMs, these are the references. Nate should keep the wording in the scripts: it says exactly what each study found, no more.</p>
  {rows}
  <div class="foot"><span>NATE VELAZQUEZ \u00b7 META AD SCRIPTS V6</span><span>SOURCES</span></div>
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
.body { font-size: 8.5pt; color: #a6a6b3; line-height: 1.6; }
.copy p { font-size: 9pt; color: #e4e4ea; line-height: 1.65; }
.copy p + p { margin-top: 5pt; }
.box.cta { background: #10142a; border-color: #2a3778; }
.alts { margin-top: 9pt; padding-top: 8pt; border-top: .75pt solid #22222b; }
.alts span { display: block; font-size: 6.8pt; font-weight: 700; letter-spacing: .08em; color: #67666f; margin-bottom: 4pt; }
.alts p { font-size: 8.8pt; color: #a6a6b3; line-height: 1.6; }
.box.note p { font-size: 8pt; color: #a6a6b3; font-style: italic; line-height: 1.6; }
table { width: 100%; border-collapse: collapse; }
th { font-size: 6.6pt; letter-spacing: .08em; color: #67666f; text-align: left; padding: 0 6pt 6pt 0; font-weight: 700; }
td { font-size: 7.7pt; color: #a6a6b3; line-height: 1.5; padding: 6pt 6pt 6pt 0; border-top: .75pt solid #22222b; vertical-align: top; }
td.t { color: #5b7cfa; font-weight: 700; white-space: nowrap; width: 9%; }
td.say { color: #f4f4f7; width: 38%; }
td.ost { color: #facc15; font-weight: 700; width: 20%; }
.src { display: block; color: #67666f; font-weight: 400; font-size: 6.6pt; margin-top: 3pt; font-style: italic; }
.srcrow { display: flex; gap: 10pt; background: #131318; border: .75pt solid #22222b; border-radius: 6pt; padding: 9pt 11pt; margin-top: 7pt; }
.srcrow b { color: #5b7cfa; font-size: 10pt; }
.cit { font-size: 8.3pt; color: #f4f4f7; line-height: 1.5; }
.find { font-size: 8pt; color: #a6a6b3; line-height: 1.5; margin-top: 3pt; }
.url { font-size: 7.4pt; color: #5b7cfa; margin-top: 3pt; }
"""

doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Nate Velazquez Meta Ad Scripts V6</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "NateVelazquez_MetaAdScripts_v6.pdf"
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
