# Builds the English recording copy PDF (shooting guide + only the lines to say for each script), large type.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

from scripts import ADS

GUIDE = [
    ("CAMERA", [
        "Phone on a tripod, <b>vertical (9:16)</b>, at eye level and about three feet away.",
        "Shoot in <b>4K at 30 fps</b> with a fixed frame rate (not auto). Lock focus and exposure on your face.",
        "Framing: mid-chest up, head centered with a little room above. The edit switches between a close-up and a panel at the bottom, so stay in the center of the frame and don't lean in or back.",
    ]),
    ("LIGHT AND BACKGROUND", [
        "Light always <b>in front of you</b>, slightly above eye level: a window or a soft light. Never a window behind you.",
        "A tidy background, three to six feet behind you. Wear a color that's different from the wall: the edit cuts you out so your head rises above the panel, and contrast keeps the cut-out clean.",
        "Plain clothes, no thin stripes or big logos. Change outfits every two scripts so it doesn't look like it was all shot on the same day.",
    ]),
    ("AUDIO", [
        "This matters most. Use a <b>lavalier mic</b> (wireless or wired to the phone).",
        "Record in a room with furniture or curtains so there's no echo. Turn off the AC and the fan.",
    ]),
    ("HOW TO SHOOT THE TAKES", [
        "<b>One file per script.</b> Hit record, say the whole script and stop at the end. Don't stop recording between lines.",
        "Go <b>paragraph by paragraph</b>: read the block, look at the lens and say it. The silences between blocks get cut in the edit.",
        "If you mess up, pause for two seconds and <b>repeat the whole sentence from the start</b>. The edit keeps the last complete take.",
        "Record <b>the main hook and the two alternates</b> back to back at the start. Same video, three openings to test.",
        "Talk to the lens, not the screen, with a bit more energy than normal. When you say “step one, two, three,” count it with your hand.",
        "Say the lines with numbers (1%, 25%, 30 vs. 40 dollars) more slowly: that's where the animations land.",
        "Before moving to the next script, watch 10 seconds of the take with headphones to check audio and focus.",
    ]),
    ("EDIT", [
        "Recommended template: <b>Glass Explainer Reel</b>. It switches between close-ups and a panel with you at the bottom and each step's animation building above, with real screenshots and numbers. No B-roll needed.",
    ]),
]

def esc(s): return html.escape(s, quote=False)
N = len(ADS)

guide = "".join(f'<div class="gs"><h3>{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></div>' for t, items in GUIDE)
pages = [f'''<section class="page">
  <div class="eyebrow">MAISON ENTERPRISES · AI MARKETING</div>
  <h1>Shooting guide</h1>
  <div class="sub">Talking head · {N} scripts · Vertical format for Reels, TikTok and Meta ads</div>
  {guide}
  <div class="foot"><span>MAISON ENTERPRISES · RECORDING COPY</span><span>GUIDE</span></div>
</section>''']

for i, a in enumerate(ADS):
    cta_html = esc(a["cta"]).replace(a["kw"], '<span class="kw">' + a["kw"] + '</span>', 1)
    core = "".join(f"<p>{esc(p)}</p>" for p in a["core"])
    pages.append(f'''<section class="page">
  <div class="eyebrow">MAISON ENTERPRISES · AI MARKETING</div>
  <div class="top"><span class="sc"><i></i>SCRIPT {i+1} OF {N}</span><span class="tag">{a["length"]} · {esc(a["pillar"])}</span></div>
  <h2>{esc(a["title"])}</h2>
  <div class="lbl">HOOK</div>
  <p class="hook">{esc(a["hook"])}</p>
  <div class="alt">{"".join(f"<p><em>ALT {j+1}</em>{esc(h)}</p>" for j, h in enumerate(a["alts"]))}</div>
  <div class="lbl">MESSAGE</div>
  <div class="core">{core}</div>
  <div class="lbl">CLOSE</div>
  <p class="cta">{cta_html}</p>
  <div class="foot"><span>MAISON ENTERPRISES · RECORDING COPY</span><span>{i+1:02d} / {N:02d}</span></div>
</section>''')

CSS = """
@page { size: letter; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0b0b0d; font-family: Inter, Arial, sans-serif; color: #f5f3ef; }
.page { width: 8.5in; height: 11in; padding: 0.6in 0.65in 0.6in; position: relative; overflow: hidden; break-after: page; background: #0b0b0d; }
.page:last-child { break-after: auto; }
.eyebrow { font-size: 8.2pt; font-weight: 700; letter-spacing: .12em; color: #d4b06a; }
.foot { position: absolute; left: .65in; right: .65in; bottom: .42in; display: flex; justify-content: space-between; border-top: .75pt solid #22201c; padding-top: 10pt; font-size: 7.1pt; letter-spacing: .06em; color: #6c6860; }
h1 { font-size: 26pt; font-weight: 800; margin-top: 16pt; }
.sub { color: #aaa69d; font-size: 10pt; margin-top: 4pt; margin-bottom: 6pt; }
.gs { background: #141311; border: .75pt solid #26231e; border-radius: 7pt; padding: 10pt 13pt; margin-top: 8pt; }
.gs h3 { font-size: 7.9pt; font-weight: 700; letter-spacing: .08em; color: #d4b06a; margin-bottom: 5pt; }
.gs ul { padding-left: 12pt; }
.gs li { font-size: 8.7pt; color: #aaa69d; line-height: 1.55; margin-top: 2.5pt; }
.gs li b { color: #f5f3ef; }
.gs:last-of-type { background: #1a160e; border-color: #4a3d22; }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 15pt; }
.sc { font-size: 8.2pt; font-weight: 700; letter-spacing: .08em; color: #d4b06a; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #d4b06a; display: inline-block; }
.tag { font-size: 7.3pt; font-weight: 700; letter-spacing: .1em; padding: 3pt 9pt; border-radius: 10pt; color: #f5f3ef; background: rgba(212,176,106,.16); text-transform: uppercase; }
h2 { font-size: 22pt; font-weight: 800; margin-top: 8pt; line-height: 1.2; }
.lbl { font-size: 7.6pt; font-weight: 700; letter-spacing: .1em; color: #6c6860; margin-top: 15pt; margin-bottom: 6pt; }
.hook { font-size: 17pt; font-weight: 700; line-height: 1.4; color: #f5f3ef; }
.core p { font-size: 12.8pt; line-height: 1.48; color: #dcd8cf; }
.core p + p { margin-top: 8pt; }
.cta { font-size: 14.5pt; font-weight: 700; line-height: 1.45; padding: 12pt 14pt; background: #1a160e; border: .75pt solid #4a3d22; border-radius: 7pt; }
.kw { color: #d4b06a; }
.alt { margin-top: 7pt; }
.alt p { font-size: 11.5pt; font-weight: 600; line-height: 1.4; color: #aaa69d; margin-top: 4pt; }
.alt em { font-style: normal; font-size: 7.4pt; font-weight: 700; letter-spacing: .08em; color: #d4b06a; margin-right: 8pt; }
"""

doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Maison Enterprises Recording Copy</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp_copies_en.html"; src.write_text(doc)
pdf = HERE / "MaisonEnterprises_RecordingCopy_EN.pdf"
subprocess.run(["/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
