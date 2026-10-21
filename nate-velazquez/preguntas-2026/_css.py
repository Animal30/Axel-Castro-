CSS = """
@page { size: letter; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0b0b0f; font-family: Inter, Arial, sans-serif; color: #f4f4f7; }
.page { width: 8.5in; height: 11in; padding: .6in .6in .6in; position: relative; overflow: hidden; break-after: page; background: #0b0b0f; }
.page:last-child { break-after: auto; }
.eyebrow { font-size: 8pt; font-weight: 700; letter-spacing: .1em; color: #5b7cfa; }
.foot { position: absolute; left: .6in; right: .6in; bottom: .42in; display: flex; justify-content: space-between; border-top: .75pt solid #1f1f27; padding-top: 10pt; font-size: 7pt; letter-spacing: .06em; color: #67666f; }
.tag { font-size: 6.6pt; font-weight: 700; letter-spacing: .08em; padding: 2pt 7pt; border-radius: 8pt; white-space: nowrap; }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 14pt; }
.sc { font-size: 8pt; font-weight: 700; letter-spacing: .08em; color: #5b7cfa; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #5b7cfa; display: inline-block; }
h2 { font-size: 20pt; font-weight: 800; margin-top: 8pt; line-height: 1.2; }
.angle { color: #a6a6b3; font-size: 9.6pt; margin-top: 4pt; margin-bottom: 4pt; }
.box { background: #131318; border: .75pt solid #22222b; border-radius: 7pt; padding: 11pt 13pt; margin-top: 9pt; }
.bh { font-size: 7.6pt; font-weight: 700; letter-spacing: .08em; color: #67666f; margin-bottom: 6pt; }
.bh em { font-style: normal; color: #5b7cfa; font-size: 9.4pt; margin-right: 7pt; }
.box p, .box li { font-size: 8.6pt; color: #a6a6b3; line-height: 1.6; }
.box p + p { margin-top: 5pt; }
.box b { color: #f4f4f7; }
.box ul, .box ol { padding-left: 14pt; }
.box li { margin-top: 3pt; }
.box.note { border-color: #2a3778; background: #10142a; }
.cover .cv { text-align: center; margin-top: 1.2in; }
.cover h1 { font-size: 33pt; font-weight: 800; margin-top: 12pt; line-height: 1.12; }
.cover .sub { color: #a6a6b3; font-size: 10.5pt; margin-top: 10pt; }
.summary { margin-top: 40pt; padding: 16pt 18pt; }
.summary li { font-size: 9.4pt; margin-top: 7pt; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 9pt; }
.grid2 .box { margin-top: 9pt; }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin-top: 9pt; }
.stats div { background: #131318; border: .75pt solid #22222b; border-radius: 7pt; padding: 11pt 10pt; }
.stats b { display: block; font-size: 18pt; color: #5b7cfa; font-weight: 800; }
.stats span { font-size: 7.6pt; color: #a6a6b3; line-height: 1.45; display: block; margin-top: 4pt; }
.tbl { width: 100%; border-collapse: collapse; margin-top: 10pt; }
.tbl th { font-size: 6.8pt; letter-spacing: .08em; color: #67666f; text-align: left; padding: 6pt 6pt; border-bottom: 1pt solid #2c2c36; text-transform: uppercase; }
.tbl td { font-size: 7.8pt; color: #a6a6b3; padding: 6.5pt 6pt; border-bottom: .75pt solid #1d1d24; vertical-align: top; line-height: 1.45; }
.tbl td b { color: #f4f4f7; }
.tbl .h { color: #5b7cfa; font-size: 7.2pt; }
.tbl .num { color: #f4f4f7; font-weight: 600; }
.fmt { padding: 9pt 13pt; }
.fmt p { font-size: 8.3pt; }
.fmt .ref { color: #5b7cfa; font-size: 7.6pt; font-weight: 600; }
.fmt .ex { color: #d6d6de; }
.rank > div { display: grid; grid-template-columns: 26pt 1fr; gap: 10pt; background: #131318; border: .75pt solid #22222b; border-radius: 7pt; padding: 11pt 13pt; margin-top: 8pt; }
.rank > div > b { font-size: 20pt; color: #5b7cfa; font-weight: 800; line-height: 1; }
.rank h4 { font-size: 10pt; margin-bottom: 3pt; }
.rank p { font-size: 8.5pt; color: #a6a6b3; line-height: 1.6; }
.rank p b { color: #f4f4f7; }
.pils { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin-top: 10pt; }
.pil { background: #131318; border: .75pt solid #22222b; border-radius: 7pt; padding: 11pt 10pt; }
.pil .pct { font-size: 20pt; font-weight: 800; }
.pil h4 { font-size: 8pt; letter-spacing: .1em; margin: 2pt 0 6pt; }
.pil p { font-size: 7.8pt; color: #a6a6b3; line-height: 1.5; margin-top: 3pt; }
.pil p b { color: #f4f4f7; }
.rules { display: grid; grid-template-columns: 1fr 1fr; gap: 4pt 14pt; }
.wks .box { margin-top: 9pt; }
.wk li { font-size: 8.3pt; }
.src { font-size: 7pt; color: #67666f; line-height: 1.55; margin-top: 12pt; }
"""

