# Guiones de anuncios de Meta de Nate, versión 7 (HTML -> PDF): versión simple para grabar. Solo guion, B-roll y texto en pantalla.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
CHROME = "/opt/pw-browsers/chromium"

CTA = "Tap Apply Now below, answer three quick questions, and I'll call you within 24 hours."

# (tiempo, lo que dice Nate, B-roll, texto en pantalla, fuente en pantalla)
ADS = [
    dict(title="Start Before January", length="38-42 sec", scenes=[
        ("0-3s", "NIH researchers weighed 195 adults before and after the holidays. Here's what they found.",
         "Nate walking toward camera outside, handheld.", "195 ADULTS. ONE HOLIDAY SEASON.", "Yanovski et al., NEJM 2000"),
        ("3-11s", "The weight people put on over the holidays was small, less than a pound on average. But a year later, it was still there.",
         "Holiday table, a pie being sliced, a calendar with late December dates.", "SMALL. BUT IT STAYED.", "NIH follow-up, 1 year later"),
        ("11-18s", "Most people plan to fix it in January. Researchers at Wharton call that the fresh start effect: we wait for a new week, a new month or a new year to begin.",
         "A calendar flips to January 1. A packed gym.", "THE FRESH START EFFECT", "Dai, Milkman & Riis, 2014"),
        ("18-29s", "What works better is a plan you make ahead of time. In a review of 94 studies, people who decided in advance, like ‘at the party, I eat protein first’, reached their goals more often than people who only set the goal.",
         "Nate typing a plan on his phone. Overhead: a plate built protein first.", "IF-THEN PLANS", "Gollwitzer & Sheeran, 2006 · 94 studies"),
        ("29-34s", "That's what I build with my clients for every big night between now and New Year's.",
         "Nate on a call with a client (phone or screen).", "A PLAN FOR EVERY BIG NIGHT", ""),
        ("34-41s", CTA, "Nate stops walking and points down to the button.", "TAP APPLY NOW", ""),
    ]),
    dict(title="The Habit In 138 Studies", length="38-42 sec", scenes=[
        ("0-3s", "138 studies. Almost 20,000 people. One habit kept showing up in the people who reached their goals.",
         "Nate at his desk, laptop open. Slow push in.", "138 STUDIES · 19,951 PEOPLE", "Harkin et al., Psychological Bulletin 2016"),
        ("3-11s", "Researchers looked at goals like eating better and getting healthier. The people who tracked their progress reached their goals more often.",
         "Close-up of a check-in form on screen. A notebook with a weekly log.", "TRACKING PROGRESS", ""),
        ("11-17s", "And it worked even better when they reported that progress to someone else.",
         "Phone: a message being sent to Nate (name blurred).", "EVEN BETTER WHEN SOMEONE SEES IT", ""),
        ("17-28s", "That's the part my videos can't do for you. With coaching, you send me a check-in every Sunday. I read it myself and send you back a video with what we change for next week.",
         "Screen recording of a check-in (client blurred, with permission). Nate recording a video reply.", "WEEKLY CHECK-IN · VIDEO REPLY", ""),
        ("28-33s", "That's why clients tell me things like this.",
         "Client quote typed out on screen, over a slow shot of Nate.", "“Nate was the first coach who understood me. He didn't judge me, and his accountability changed everything.”", ""),
        ("33-42s", "If you've been watching my videos for a while, this is the next step. " + CTA,
         "Nate looks at camera and closes the laptop.", "TAP APPLY NOW", ""),
    ]),
    dict(title="The Milkshake Study", length="38-42 sec", scenes=[
        ("0-3s", "In a classic study, strict dieters drank a milkshake. Then they ate more ice cream, not less.",
         "Nate sets a milkshake on the kitchen counter and looks at camera.", "ONE MILKSHAKE. THEN WHAT?", "Herman & Mack, 1975"),
        ("3-12s", "Researchers gave people a milkshake, then all the ice cream they wanted. Strict dieters ate about two thirds more after the milkshake. Once the rule was broken, the day felt lost.",
         "Ice cream tub, a spoon digging in. Nate shakes his head.", "‘I ALREADY BLEW IT’", ""),
        ("12-20s", "A later study of almost 2,000 people found the same pattern. All-or-nothing food rules went with more binge eating. Flexible rules went with better results.",
         "Split screen: a crossed-out ‘forbidden foods’ list next to a balanced plate.", "ALL-OR-NOTHING VS. FLEXIBLE", "Westenhoefer et al., 1999 · 1,838 adults"),
        ("20-30s", "So my clients keep the food they love. We build the plate around it. Protein first, about 25 to 30 grams, which helps you feel full. Then something fresh. And the tacos stay.",
         "Overhead, fast cuts: grilled chicken added, salad and salsa added, tacos on the plate.", "+ 25-30 g PROTEIN · + SOMETHING FRESH · SAME TACOS", "Leidy et al., Am J Clin Nutr 2015"),
        ("30-39s", CTA + " We'll start with your favorite food.",
         "Nate to camera with the plate, points down to the button.", "TAP APPLY NOW", ""),
    ]),
]

def esc(s): return html.escape(s, quote=False)

def build():
    pages = []
    for i, a in enumerate(ADS):
        rows = []
        for j, (t, s, b, o, r) in enumerate(a["scenes"]):
            cls = ' class="cta"' if j == len(a["scenes"]) - 1 else ""
            src = f'<span class="src">{esc(r)}</span>' if r else ""
            rows.append(f'<tr{cls}><td class="t">{esc(t)}</td><td class="say">{esc(s)}</td><td>{esc(b)}</td><td class="ost">{esc(o)}{src}</td></tr>')
        pages.append(f'''<section class="page">
  <div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
  <div class="top"><span class="sc"><i></i>AD {i+1} OF {len(ADS)}</span><span class="len">{a["length"]}</span></div>
  <h2>{esc(a["title"])}</h2>
  <table><tr><th>TIME</th><th>NATE SAYS</th><th>B-ROLL</th><th>ON-SCREEN TEXT</th></tr>{"".join(rows)}</table>
  <div class="foot"><span>NATE VELAZQUEZ · META AD SCRIPTS</span><span>{i+1:02d} / {len(ADS):02d}</span></div>
</section>''')
    return "".join(pages)

CSS = """
@page { size: letter; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0b0b0f; font-family: Inter, Arial, sans-serif; color: #f4f4f7; }
.page { width: 8.5in; height: 11in; padding: 0.62in 0.62in 0.6in; position: relative; overflow: hidden; break-after: page; background: #0b0b0f; }
.page:last-child { break-after: auto; }
.eyebrow { font-size: 8.2pt; font-weight: 700; letter-spacing: .1em; color: #5b7cfa; }
.foot { position: absolute; left: .62in; right: .62in; bottom: .42in; display: flex; justify-content: space-between; border-top: .75pt solid #1f1f27; padding-top: 10pt; font-size: 7.1pt; letter-spacing: .06em; color: #67666f; }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 16pt; }
.sc { font-size: 8.2pt; font-weight: 700; letter-spacing: .08em; color: #5b7cfa; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #5b7cfa; display: inline-block; }
.len { font-size: 8.2pt; font-weight: 700; letter-spacing: .08em; color: #67666f; }
h2 { font-size: 24pt; font-weight: 800; margin: 6pt 0 18pt; line-height: 1.2; }
table { width: 100%; border-collapse: collapse; }
th { font-size: 7pt; letter-spacing: .08em; color: #67666f; text-align: left; padding: 0 8pt 8pt 0; font-weight: 700; }
td { font-size: 8.8pt; color: #a6a6b3; line-height: 1.55; padding: 11pt 8pt 11pt 0; border-top: .75pt solid #22222b; vertical-align: top; }
td.t { color: #5b7cfa; font-weight: 700; white-space: nowrap; width: 8%; }
td.say { color: #f4f4f7; font-size: 10pt; font-weight: 500; width: 42%; line-height: 1.6; }
td.ost { color: #facc15; font-weight: 700; width: 22%; }
.src { display: block; color: #67666f; font-weight: 400; font-size: 6.8pt; margin-top: 4pt; font-style: italic; }
tr.cta td { background: #10142a; border-top: .75pt solid #2a3778; }
tr.cta td:first-child { padding-left: 8pt; }
tr.cta td.say { color: #fff; font-weight: 700; }
"""

if __name__ == "__main__":
    doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Nate Velazquez Meta Ad Scripts</title><style>{CSS}</style></head><body>{build()}</body></html>"
    src = HERE / "_tmp.html"; src.write_text(doc)
    pdf = HERE / "NateVelazquez_MetaAdScripts_v7.pdf"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)], check=True, stderr=subprocess.DEVNULL)
    src.unlink()
    print(pdf)
