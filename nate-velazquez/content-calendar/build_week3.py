# Calendario de contenido de Nate, semana de Thanksgiving (23 al 27 de nov de 2026): 5 videos hablando a cámara. HTML -> PDF.
import html, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
CHROME = "/opt/pw-browsers/chromium"
WPS = 165 / 60  # palabras por segundo al hablar

# (lo que dice Nate, B-roll, texto en pantalla, fuente en pantalla). La última fila es siempre el cierre.
SCRIPTS = [
    dict(day="Mon · Nov 23", title="The Holiday Pound", ending="Comments", scenes=[
        ("The holidays cost you under 1 pound.",
         "Nate in his kitchen, a pie and a dinner plate on the counter behind him.", "UNDER 1 LB", ""),
        ("NIH researchers followed 195 adults through the holidays.",
         "Quick cuts: a holiday table, a pie being sliced.", "195 ADULTS", "Yanovski et al., NEJM 2000"),
        ("A year later, on average, it was still there.",
         "A calendar page going from November to December.", "A YEAR LATER: STILL THERE", ""),
        ("Skip the fear. Make a plan for the big days.",
         "Nate to camera.", "A PLAN FOR THE BIG DAYS", ""),
        ("Pick 2 or 3 meals that matter.",
         "Overhead: a full dinner table.", "PICK 2-3 MEALS", ""),
        ("Decide ahead of time what you'll do at them.",
         "Nate typing a note on his phone.", "DECIDE AHEAD", ""),
        ("Protein first.",
         "Overhead: a plate built protein first, then the sides.", "PROTEIN FIRST", ""),
        ("In a review of 94 studies, people who decided ahead of time reached their goals more often.",
         "Nate counts on his fingers.", "94 STUDIES", "Gollwitzer & Sheeran, 2006"),
        ("Which holiday meal is your hardest?",
         "Nate to camera.", "HARDEST HOLIDAY MEAL?", ""),
        ("Tell me below, and I'll help you plan your holidays.",
         "Nate points down to the comments.", "COMMENT BELOW", ""),
    ]),
    dict(day="Tue · Nov 24", title="Five And A Half Hours", ending="DM “SLEEP”", scenes=[
        ("Sleeping 5.5 hours cost dieters over half their fat loss.",
         "Nate at his desk in the morning, coffee in hand.", "OVER HALF", ""),
        ("10 adults. Same diet. Two weeks.",
         "A calendar with two weeks highlighted.", "SAME DIET · TWO WEEKS", "Nedeltcheva et al., Annals of Internal Medicine 2010"),
        ("Once with 8.5 hours of sleep a night.",
         "Phone alarm set to 11 PM and 7:30 AM.", "8.5 HOURS", ""),
        ("Once with 5.5.",
         "Phone alarm set to 1 AM and 6:30 AM.", "5.5 HOURS", ""),
        ("Same weight lost both times.",
         "A bathroom scale, same number twice.", "SAME WEIGHT LOST", ""),
        ("But on short sleep, a lot less of it was fat.",
         "Simple graphic: two bars, the fat part shrinking.", "LESS FAT LOST", ""),
        ("More came from lean tissue.",
         "Same graphic, lean part growing.", "MORE LEAN TISSUE LOST", ""),
        ("It's a small study, only 10 people, so I won't oversell it.",
         "Nate to camera.", "SMALL STUDY · 10 PEOPLE", ""),
        ("But it's one more reason to protect your sleep, especially when you're working on your health.",
         "Nate to camera, small nod.", "PROTECT YOUR SLEEP", ""),
        ("Sleeping under six hours? DM me the word SLEEP.",
         "Nate points down.", "DM “SLEEP”", ""),
    ]),
    dict(day="Wed · Nov 25", title="66 Days, Not 21", ending="Comments", scenes=[
        ("A habit takes 66 days, not 21.",
         "Calendar page with 21 crossed out and 66 written in.", "66 DAYS, NOT 21", ""),
        ("And one missed day barely matters.",
         "A habit tracker with one empty box.", "ONE MISSED DAY", ""),
        ("University College London tracked 96 people building a new habit, one day at a time, for 84 days.",
         "A habit tracker with daily checkmarks filling in.", "96 PEOPLE · 84 DAYS", "Lally et al., 2010"),
        ("On average, 66 days.",
         "The number 66 on screen.", "AVERAGE: 66 DAYS", ""),
        ("For some, just 18 days. For others, a predicted 250.",
         "Two numbers on screen, one by one.", "FASTEST 18 · SLOWEST 250", ""),
        ("Missing a single day made no real difference.",
         "The tracker: one empty box, the rest still filled.", "ONE MISS ≠ RESET", ""),
        ("The ones who didn't make it stick missed many days.",
         "The tracker with many empty boxes.", "MANY MISSES = NO HABIT", ""),
        ("If you slipped, you didn't ruin it.",
         "Nate to camera.", "YOU DIDN'T RUIN IT", ""),
        ("Do the next one.",
         "Nate to camera, small nod.", "DO THE NEXT ONE", ""),
        ("What habit do you keep restarting? Tell me below.",
         "Nate points down to the comments.", "WHAT HABIT DO YOU KEEP RESTARTING?", ""),
    ]),
    dict(day="Thu · Nov 26 (Thanksgiving)", title="The Milkshake Study", ending="Comments", scenes=[
        ("66% more ice cream. One milkshake cost them the day.",
         "Nate sets a milkshake on the counter and looks at camera.", "66% MORE ICE CREAM", ""),
        ("In 1975, researchers gave people a milkshake. Then all the ice cream they wanted.",
         "A milkshake being poured.", "THE MILKSHAKE STUDY", "Herman & Mack, 1975"),
        ("Strict dieters ate two thirds more. Non-dieters didn't.",
         "Two bowls side by side: a big one and a small one.", "DIETERS: MORE · NON-DIETERS: LESS", ""),
        ("Once they'd broken the rule, the day felt lost.",
         "Nate shakes his head.", "‘I ALREADY BLEW IT’", ""),
        ("A later study of 1,838 adults found that all-or-nothing food rules went with more binge eating.",
         "A crossed-out ‘forbidden foods’ list.", "ALL-OR-NOTHING: MORE BINGES", "Westenhoefer et al., 1999 \u00b7 1,838 adults"),
        ("Flexible rules went with better results.",
         "A balanced plate with a slice of pie on it.", "FLEXIBLE: BETTER RESULTS", ""),
        ("So today, have the pie. One slice is one slice.",
         "Nate cuts a slice of pie and slides it toward the camera.", "HAVE THE PIE", ""),
        ("Deciding you've already blown it is what costs you.",
         "Nate to camera.", "THE REAL COST", ""),
        ("What food would you never give up? Ice cream? Tell me below.",
         "Nate points down to the comments.", "FOOD YOU'D NEVER GIVE UP?", ""),
    ]),
    dict(day="Fri · Nov 27", title="138 Studies", ending="DM “HABIT”", scenes=[
        ("138 studies found a habit that costs you nothing.",
         "Nate at his desk, laptop open.", "138 STUDIES", "Harkin et al., Psychological Bulletin 2016"),
        ("Checking your progress.",
         "A check-in form on screen.", "CHECK YOUR PROGRESS", ""),
        ("People who tracked their progress reached their goals more often than people who didn't.",
         "A notebook with a weekly log.", "TRACKED = MORE GOALS REACHED", ""),
        ("Even better when they wrote it down or told someone.",
         "Hand writing in the notebook, then a message being sent.", "WRITE IT · TELL SOMEONE", ""),
        ("That's why every client sends me a check-in on Sunday.",
         "Screen recording of a check-in (client blurred, with permission).", "SUNDAY CHECK-IN", ""),
        ("I read it myself, send a video back, and we adjust the next week.",
         "Nate recording a video reply on his laptop.", "A VIDEO BACK", ""),
        ("Want help building this habit? DM me HABIT.",
         "Nate points down.", "DM “HABIT”", ""),
    ]),
]

def esc(s): return html.escape(s, quote=False)

def timed(scenes):
    """Devuelve (tiempo, fila, total) calculando cuándo entra cada fila a 165 palabras por minuto."""
    out, t = [], 0.0
    for say, b, o, r in scenes:
        d = max(1.8, len(say.split()) / WPS)
        out.append((f"{int(t)}-{int(t + d + .5)}s", say, b, o, r)); t += d
    return out, int(t + .5)

def build():
    n = len(SCRIPTS)
    rows = "".join(f'<div class="row"><span class="n">{i+1:02d}</span><span class="t">{esc(s["title"])}</span><span class="e">{esc(s["ending"])}</span><span class="d">{esc(s["day"])}</span></div>' for i, s in enumerate(SCRIPTS))
    pages = [f'''<section class="page cover">
  <div class="cv"><div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
  <h1>Content Calendar</h1><p class="sub">Thanksgiving week · 5 talking-head videos · Nov 23-27</p></div>
  <div class="list"><div class="lh">THIS WEEK</div>{rows}</div>
  <div class="foot"><span>NATE VELAZQUEZ · CONTENT CALENDAR</span><span>01 / {n+1:02d}</span></div>
</section>''']
    for i, s in enumerate(SCRIPTS):
        sc, total = timed(s["scenes"])
        trs = []
        for j, (t, say, b, o, r) in enumerate(sc):
            cls = ' class="cta"' if j == len(sc) - 1 else ""
            src = f'<span class="src">{esc(r)}</span>' if r else ""
            trs.append(f'<tr{cls}><td class="t">{esc(t)}</td><td class="say">{esc(say)}</td><td>{esc(b)}</td><td class="ost">{esc(o)}{src}</td></tr>')
        pages.append(f'''<section class="page">
  <div class="eyebrow">NATE VELAZQUEZ · @_NATEVELAZQUEZ</div>
  <div class="top"><span class="sc"><i></i>{esc(s["day"].upper())}</span><span class="len">~{total} SEC</span></div>
  <h2>{esc(s["title"])}</h2>
  <table><tr><th>TIME</th><th>NATE SAYS</th><th>B-ROLL</th><th>ON-SCREEN TEXT</th></tr>{"".join(trs)}</table>
  <div class="foot"><span>NATE VELAZQUEZ · CONTENT CALENDAR</span><span>{i+2:02d} / {n+1:02d}</span></div>
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
.cover .cv { text-align: center; margin-top: 1.4in; }
.cover h1 { font-size: 34pt; font-weight: 800; margin-top: 12pt; }
.cover .sub { color: #a6a6b3; font-size: 10pt; margin-top: 8pt; }
.list { margin-top: 40pt; }
.lh { font-size: 7.6pt; font-weight: 700; letter-spacing: .1em; color: #5b7cfa; margin-bottom: 6pt; }
.row { display: flex; align-items: center; gap: 10pt; padding: 11pt 0; border-bottom: .75pt solid #1a1a21; font-size: 10pt; }
.row .n { color: #5b7cfa; font-weight: 700; width: 18pt; }
.row .t { flex: 1; font-weight: 600; }
.row .e { color: #facc15; font-size: 8pt; font-weight: 700; }
.row .d { color: #8b8a94; font-size: 8pt; width: 130pt; text-align: right; }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 16pt; }
.sc { font-size: 8.2pt; font-weight: 700; letter-spacing: .08em; color: #5b7cfa; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #5b7cfa; display: inline-block; }
.len { font-size: 8.2pt; font-weight: 700; letter-spacing: .08em; color: #67666f; }
h2 { font-size: 24pt; font-weight: 800; margin: 6pt 0 14pt; line-height: 1.2; }
table { width: 100%; border-collapse: collapse; }
th { font-size: 7pt; letter-spacing: .08em; color: #67666f; text-align: left; padding: 0 8pt 8pt 0; font-weight: 700; }
td { font-size: 8.6pt; color: #a6a6b3; line-height: 1.5; padding: 8pt 8pt 8pt 0; border-top: .75pt solid #22222b; vertical-align: top; }
td.t { color: #5b7cfa; font-weight: 700; white-space: nowrap; width: 8%; }
td.say { color: #f4f4f7; font-size: 10pt; font-weight: 500; width: 40%; line-height: 1.5; }
td.ost { color: #facc15; font-weight: 700; width: 24%; }
.src { display: block; color: #67666f; font-weight: 400; font-size: 6.8pt; margin-top: 4pt; font-style: italic; }
tr.cta td { background: #10142a; border-top: .75pt solid #2a3778; }
tr.cta td:first-child { padding-left: 8pt; }
tr.cta td.say { color: #fff; font-weight: 700; }
"""

if __name__ == "__main__":
    doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Nate Velazquez Content Calendar</title><style>{CSS}</style></head><body>{build()}</body></html>"
    src = HERE / "_tmp.html"; src.write_text(doc)
    pdf = HERE / "NateVelazquez_ContentCalendar_Week3.pdf"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)], check=True, stderr=subprocess.DEVNULL)
    src.unlink()
    print(pdf)
