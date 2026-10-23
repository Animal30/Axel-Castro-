# Builds the English Maison Enterprises scripts PDF (HTML -> PDF), same layout as the Spanish one in ../build.py.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

from scripts import ADS

def esc(s): return html.escape(s, quote=False)
N = len(ADS)
pages = []
for i, a in enumerate(ADS):
    cta_html = esc(a["cta"]).replace(a["kw"], '<span class="kw">' + a["kw"] + '</span>', 1)
    core = "".join(f"<p>{esc(p)}</p>" for p in a["core"])
    pages.append(f'''<section class="page">
  <div class="eyebrow">MAISON ENTERPRISES · AI MARKETING</div>
  <div class="top"><span class="sc"><i></i>SCRIPT {i+1} OF {N}</span><span class="tag">ORGANIC + AD</span></div>
  <div class="vs">VIDEO SCRIPT · EDUCATIONAL CONTENT</div>
  <h2>{esc(a["title"])}</h2>
  <div class="angle">{esc(a["angle"])}</div>
  <div class="facts">
    <div><span>FORMAT</span><b>{esc(a["angle"].split(" · ")[0])}</b></div>
    <div><span>LENGTH</span><b>{a["length"]}</b></div>
    <div><span>PILLAR</span><b>{esc(a["pillar"])}</b></div>
    <div><span>DM KEYWORD</span><b class="kw">{a["kw"]}</b></div>
  </div>
  <div class="box"><div class="bh"><em>01</em>THE HOOK</div><p class="hook">“{esc(a["hook"])}”</p>
    <div class="alts"><span>ALTERNATE HOOKS · SAME VIDEO, TEST THE FIRST 3 SECONDS</span>{"".join(f"<p>“{esc(h)}”</p>" for h in a["alts"])}</div></div>
  <div class="box"><div class="bh"><em>02</em>CORE MESSAGE</div><div class="core">{core}</div>
    <div class="alts"><span>WHAT THE VIEWER TAKES AWAY</span><p>{esc(a["learn"])}</p></div></div>
  <div class="box cta"><div class="bh"><em>03</em>CALL TO ACTION</div><p class="hook">“{cta_html}”</p></div>
  <div class="box note"><div class="bh">DIRECTION NOTE</div><p>{esc(a["note"])}</p></div>
  <div class="foot"><span>MAISON ENTERPRISES · CONTENT SCRIPTS</span><span>{i+1:02d} / {N:02d}</span></div>
</section>''')

CSS = """
@page { size: letter; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0b0b0d; font-family: Inter, Arial, sans-serif; color: #f5f3ef; }
.page { width: 8.5in; height: 11in; padding: 0.6in 0.62in 0.6in; position: relative; overflow: hidden; break-after: page; background: #0b0b0d; }
.page:last-child { break-after: auto; }
.eyebrow { font-size: 8.2pt; font-weight: 700; letter-spacing: .12em; color: #d4b06a; }
.foot { position: absolute; left: .62in; right: .62in; bottom: .42in; display: flex; justify-content: space-between; border-top: .75pt solid #22201c; padding-top: 10pt; font-size: 7.1pt; letter-spacing: .06em; color: #6c6860; }
.tag { font-size: 7.3pt; font-weight: 700; letter-spacing: .1em; padding: 3pt 9pt; border-radius: 10pt; color: #f5f3ef; background: rgba(212,176,106,.16); }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 15pt; }
.sc { font-size: 8.2pt; font-weight: 700; letter-spacing: .08em; color: #d4b06a; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #d4b06a; display: inline-block; }
.vs { font-size: 7.9pt; font-weight: 700; letter-spacing: .08em; color: #6c6860; margin-top: 11pt; }
h2 { font-size: 20.2pt; font-weight: 800; margin-top: 4pt; line-height: 1.2; }
.angle { color: #aaa69d; font-size: 10.1pt; margin-top: 4pt; }
.facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin-top: 13pt; }
.facts div { background: #141311; border: .75pt solid #26231e; border-radius: 6pt; padding: 10pt 10pt 12pt; }
.facts span { display: block; font-size: 7.1pt; letter-spacing: .06em; color: #6c6860; margin-bottom: 8pt; }
.facts b { font-size: 9.4pt; font-weight: 700; }
.kw { color: #d4b06a; font-weight: 700; }
.box { background: #141311; border: .75pt solid #26231e; border-radius: 7pt; padding: 11pt 13pt; margin-top: 8pt; }
.bh { font-size: 7.9pt; font-weight: 700; letter-spacing: .08em; color: #6c6860; margin-bottom: 7pt; }
.bh em { font-style: normal; color: #d4b06a; font-size: 9.8pt; margin-right: 7pt; }
.hook { font-size: 10.6pt; font-weight: 700; line-height: 1.45; }
.core p { font-size: 8.6pt; color: #aaa69d; line-height: 1.6; }
.core p + p { margin-top: 4pt; }
.box.cta { background: #1a160e; border-color: #4a3d22; }
.alts { margin-top: 8pt; padding-top: 7pt; border-top: .75pt solid #26231e; }
.alts span { display: block; font-size: 6.8pt; font-weight: 700; letter-spacing: .08em; color: #d4b06a; margin-bottom: 3pt; }
.alts p { font-size: 8.6pt; color: #f5f3ef; line-height: 1.5; }
.box.note p { font-size: 8.1pt; color: #aaa69d; font-style: italic; line-height: 1.65; }
"""

doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Maison Enterprises Scripts</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "MaisonEnterprises_Scripts_EN.pdf"
subprocess.run(["/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
