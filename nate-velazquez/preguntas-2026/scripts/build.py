# Genera los guiones de anuncios de Meta de Nate (HTML -> PDF), versión que cumple las políticas de salud de Meta.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

ADS = [
    dict(title="How Much Protein Do You Actually Need?", angle="Talking Head · Yapping · Most-searched question", length="30-45 sec", kw="PROTEIN", use="FEED + AD",
         hook="Hungry by 10am? You're making the most common protein mistake there is.",
         alts=[],
         core=["Here it is: plenty of protein at dinner, almost none at breakfast. A bagel and a coffee gets you maybe 10 grams, and by mid-morning your body is asking for food again.",
               "The number you usually see, about 0.8 grams per kilo of body weight, is just the minimum to avoid a deficiency. For most active adults, the research points closer to 1.2 to 1.6.",
               "In real life, I keep it simple for my clients: 25 to 40 grams per meal, three or four times a day.",
               "Start with breakfast. Eggs, Greek yogurt, cottage cheese or a protein shake, and watch how different your morning feels.",
               "I'm Nate, nutrition coach."],
         cta="Send me a message with the word PROTEIN and tell me what you eat for breakfast. I'll tell you exactly how to hit your number."),
    dict(title="Is Fibermaxxing Actually Healthy?", angle="Talking Head · Yapping · 2026 trend", length="30-45 sec", kw="FIBER", use="FEED + AD",
         hook="Fibermaxxing works. But start it like most people do and you'll regret it by tomorrow.",
         alts=[],
         core=["Good news first: this is one of the few trends I actually like. Most adults only get about half the fiber they need.",
               "The target is roughly 25 grams a day for women and about 30 to 38 for men.",
               "Here's where people get it wrong: they go from 10 grams to 50 overnight, and spend the next two days bloated and miserable.",
               "Go up slowly, a few grams a week, and drink more water as you do it. Beans, berries, oats, chia, veggies. Real food, not a powder in every drink."],
         cta="Send me a message with the word FIBER and tell me what a normal day of eating looks like for you. I'll tell you where I'd add it first."),
    dict(title="Are Seed Oils Actually Bad For You?", angle="Talking Head · Yapping · Myth vs. truth", length="30-45 sec", kw=None, use="ORGANIC",
         hook="You cut seed oils and felt better. The oil wasn't the reason.",
         alts=[],
         core=["When people cut seed oils, they also cut fries, chips, fast food and packaged snacks. That's what actually changed.",
               "The research on the oil itself doesn't back the fear. Studies that swap saturated fat for oils like canola or soybean tend to show better cholesterol, not worse.",
               "The problem was never the bottle of canola oil in your kitchen. It was the deep fryer.",
               "Cooking at home with canola or olive oil? You're fine. Watch how often you're eating fried and packaged food instead."],
         cta="So be honest: when you cut seed oils, what else did you cut? Tell me in the comments."),
    dict(title="Should You Take Creatine?", angle="Talking Head · Yapping · Supplements", length="30-45 sec", kw=None, use="ORGANIC ONLY",
         hook="If you only take one supplement this year, make it this one. Here's why.",
         alts=[],
         core=["It's creatine. And no, it's not just for bodybuilders.",
               "It's one of the most studied supplements in the world. It helps your muscles recover and perform, and people of every age are using it now.",
               "How to take it: 3 to 5 grams of creatine monohydrate a day, every day. No loading phase, no special timing.",
               "One heads-up: the scale might go up a little at first. That's water in your muscles, not fat.",
               "If you have kidney issues or take medication, check with your doctor before you start."],
         cta="Are you already taking creatine, or is something holding you back? Tell me in the comments and I'll answer every one."),
    dict(title="Are Ultra-Processed Foods Really That Bad?", angle="Talking Head · Yapping · Myth vs. truth", length="30-45 sec", kw="REAL", use="FEED + AD",
         hook="Cut every ultra-processed food and you'll quit in two weeks. Do this instead.",
         alts=[],
         core=["Trying to eat zero processed food sounds healthy. But with a job and a family, almost nobody can keep it up.",
               "And the label covers more than you think: soda and candy, but also some whole-grain breads, flavored Greek yogurt and protein bars. A protein bar and a donut are not the same food.",
               "So instead of zero, aim for most of your plate to be real food.",
               "And when you do buy packaged food, pick the options that bring protein or fiber with them. Better most of the time beats perfect for two weeks."],
         cta="Send me a message with the word REAL and tell me the packaged foods you buy every week. I'll tell you which ones I'd keep and which I'd swap."),
]

def esc(s): return html.escape(s, quote=False)
N = len(ADS)
pages = []
for i, a in enumerate(ADS):
    if a["kw"]:
        cta_html = esc(a["cta"]).replace(a["kw"], '<span class="kw">' + a["kw"] + '</span>', 1)
        last_fact = '<div><span>DM KEYWORD</span><b class="kw">' + a["kw"] + '</b></div>'
        cta_label, channel = 'CALL TO ACTION', 'IG Feed + Meta Ads'
    else:
        cta_html = esc(a["cta"])
        last_fact = '<div><span>GOAL</span><b>Comments</b></div>'
        cta_label, channel = 'QUESTION FOR THE AUDIENCE', 'IG Feed (organic)'
    core = "".join(f"<p>{esc(p)}</p>" for p in a["core"])
    pages.append(f'''<section class="page">
  <div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
  <div class="top"><span class="sc"><i></i>SCRIPT {i+1} OF {N}</span><span class="tag">{a["use"]}</span></div>
  <div class="vs">NUTRITION Q&amp;A · VIDEO SCRIPT</div>
  <h2>{esc(a["title"])}</h2>
  <div class="angle">{esc(a["angle"])}</div>
  <div class="facts">
    <div><span>FORMAT</span><b>{esc(a["angle"].split(" · ")[0])}</b></div>
    <div><span>LENGTH</span><b>{a["length"]}</b></div>
    <div><span>CHANNEL</span><b>{channel}</b></div>
    {last_fact}
  </div>
  <div class="box"><div class="bh"><em>01</em>THE HOOK</div><p class="hook">“{esc(a["hook"])}”</p></div>
  <div class="box"><div class="bh"><em>02</em>CORE MESSAGE</div><div class="core">{core}</div></div>
  <div class="box cta"><div class="bh"><em>03</em>{cta_label}</div><p class="hook">“{cta_html}”</p></div>
  <div class="foot"><span>NATE VELAZQUEZ · NUTRITION Q&amp;A</span><span>{i+1:02d} / {N:02d}</span></div>
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

doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Nate Velazquez Top Questions</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "NateVelazquez_TopQuestions_Scripts.pdf"
subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
