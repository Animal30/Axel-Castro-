# Arma el PDF y el markdown de los guiones de @iamaegene por embudo, a partir de data.py.
import html, pathlib, subprocess, sys
from data import S, FUNNEL, CAROUSELS, STORIES, TOFU, MOFU, BOFU

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
CHROME = "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome"
COLOR = {TOFU: "#74acdf", MOFU: "#f6b40e", BOFU: "#5ee0a0"}

def esc(s): return html.escape(s, quote=False)
def ph(s): return esc(s).replace("{{", '<b class="adj">{{').replace("}}", "}}</b>")

N = len(S)
rows = "".join(f'<div class="fc" style="border-color:{COLOR[k]}"><span style="color:{COLOR[k]}">{k} · {v["es"].upper()}</span>'
               f'<b>{esc(v["goal"])}</b><p>Mide: {esc(v["metric"])}</p><p>Ritmo: {v["mix"]} · {sum(s["funnel"] == k for s in S)} guiones</p></div>'
               for k, v in FUNNEL.items())
car = "".join(f'<p><b style="color:{COLOR[f]}">{f.split()[0]}</b> {esc(t)}<br><i>{esc(d)}</i></p>' for f, t, d in CAROUSELS)
sto = "".join(f"<p>{esc(x)}</p>" for x in STORIES)
cover = f'''<section class="page">
  <div class="eyebrow">@IAMAEGENE · CONTENIDO POR EMBUDO</div>
  <h1>How to learn<br><span>any language</span></h1>
  <p class="lead">{N} guiones de reels ordenados por embudo, con hooks probados con el puntaje de ig-reel y pasados por el detector de IA. Se hablan en inglés, con tu voz: frases cortas, contracciones, humor. Lo marcado <b class="adj">{{{{así}}}}</b> es un dato tuyo que falta: completalo con lo real antes de grabar.</p>
  <div class="funnel">{rows}</div>
  <div class="box"><div class="bh"><em>!</em>CÓMO SE ARMA LA SEMANA</div><div class="core">
    <p>4 reels de alcance + 2 de confianza + 1 de conversión + 2 carruseles. Historias todos los días.</p>
    <p>El alcance trae gente nueva, la confianza hace que te guarden y te sigan, la conversión los lleva al DM, al ROADMAP y a la comunidad. Sin alcance no hay a quién convertir; sin conversión los seguidores no se transforman en nada.</p>
  </div></div>
  <div class="foot"><span>@IAMAEGENE · GUIONES POR EMBUDO</span><span>00 / {N:02d}</span></div>
</section>'''
extra = f'''<section class="page">
  <div class="eyebrow">@IAMAEGENE · CARRUSELES E HISTORIAS</div>
  <h2>Carruseles</h2><div class="box"><div class="core car">{car}</div></div>
  <h2>Historias</h2><div class="box"><div class="core">{sto}</div></div>
  <div class="foot"><span>@IAMAEGENE · GUIONES POR EMBUDO</span><span>EXTRA</span></div>
</section>'''
pages = [cover]
for i, s in enumerate(S):
    c = COLOR[s["funnel"]]
    body = "".join(f"<p>{ph(p)}</p>" for p in s["body"])
    scr = "".join(f"<i>{ph(t)}</i>" for t in s["screen"])
    pages.append(f'''<section class="page">
  <div class="eyebrow">@IAMAEGENE · HOW TO LEARN ANY LANGUAGE</div>
  <div class="top"><span class="sc"><i></i>SCRIPT {i+1} OF {N}</span><span class="tag" style="color:{c};background:{c}22">{s["funnel"]} · {FUNNEL[s["funnel"]]["es"].upper()}</span></div>
  <h2>{esc(s["title"])}</h2>
  <div class="facts">
    <div><span>EDICIÓN</span><b>{esc(s["edit"])}</b></div>
    <div><span>DURACIÓN</span><b>{s["length"]}</b></div>
    <div><span>FÓRMULA</span><b>{esc(s["formula"])}</b></div>
    <div><span>KEYWORD</span><b class="kw">{s["kw"] or "—"}</b></div>
  </div>
  <div class="box"><div class="bh"><em>01</em>HOOK · 0-2 S</div><p class="hook">“{ph(s["hook"])}”</p>
    <p class="hs">EN PANTALLA: {ph(s["hook_screen"])}</p>
    <div class="alts"><span>HOOKS ALTERNATIVOS</span>{"".join(f"<p>“{ph(h)}”</p>" for h in s["alts"])}</div></div>
  <div class="box"><div class="bh"><em>02</em>CUERPO</div><div class="core">{body}</div></div>
  <div class="box"><div class="bh"><em>03</em>TEXTO EN PANTALLA</div><div class="scr">{scr}</div></div>
  <div class="box cta"><div class="bh"><em>04</em>CTA</div><p class="hook">“{ph(s["cta"])}”</p></div>
  <div class="box note"><div class="bh"><em>✎</em>DIRECCIÓN</div><p>{ph(s["note"])}</p></div>
  <div class="foot"><span>@IAMAEGENE · {s["funnel"]}</span><span>{i+1:02d} / {N:02d}</span></div>
</section>''')
pages.append(extra)

CSS = """
@page { size: letter; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0b0d12; font-family: Inter, Arial, sans-serif; color: #f4f5f8; }
.page { width: 8.5in; height: 11in; padding: .55in .6in .6in; position: relative; overflow: hidden; break-after: page; background: #0b0d12; }
.page:last-child { break-after: auto; }
.eyebrow { font-size: 8pt; font-weight: 700; letter-spacing: .1em; color: #74acdf; }
.foot { position: absolute; left: .6in; right: .6in; bottom: .38in; display: flex; justify-content: space-between; border-top: .75pt solid #1e222c; padding-top: 9pt; font-size: 7pt; letter-spacing: .06em; color: #646a78; }
.tag { font-size: 7.3pt; font-weight: 700; letter-spacing: .1em; padding: 3pt 9pt; border-radius: 10pt; }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 14pt; }
.sc { font-size: 8pt; font-weight: 700; letter-spacing: .08em; color: #74acdf; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #74acdf; display: inline-block; }
h1 { font-size: 44pt; font-weight: 800; line-height: 1.05; margin-top: .9in; }
h1 span { color: #74acdf; font-family: 'Playfair Display', Georgia, serif; font-style: italic; font-weight: 600; }
.lead { font-size: 11pt; color: #a7adbb; line-height: 1.6; margin-top: 16pt; max-width: 6.3in; }
.funnel { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8pt; margin-top: 22pt; }
.fc { border: .75pt solid; border-radius: 7pt; padding: 11pt; background: #13161d; }
.fc span { display: block; font-size: 7pt; font-weight: 700; letter-spacing: .08em; margin-bottom: 7pt; }
.fc b { display: block; font-size: 9.6pt; line-height: 1.35; margin-bottom: 6pt; }
.fc p { font-size: 7.8pt; color: #a7adbb; line-height: 1.5; }
h2 { font-size: 19pt; font-weight: 800; margin-top: 8pt; line-height: 1.2; }
.facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin-top: 12pt; }
.facts div { background: #13161d; border: .75pt solid #222733; border-radius: 6pt; padding: 9pt 10pt 10pt; }
.facts span { display: block; font-size: 6.8pt; letter-spacing: .06em; color: #646a78; margin-bottom: 6pt; }
.facts b { font-size: 8.8pt; font-weight: 700; }
.kw { color: #74acdf; font-weight: 700; }
.adj { color: #f6b40e; font-weight: 600; }
.box { background: #13161d; border: .75pt solid #222733; border-radius: 7pt; padding: 10pt 12pt; margin-top: 8pt; }
.bh { font-size: 7.6pt; font-weight: 700; letter-spacing: .08em; color: #646a78; margin-bottom: 6pt; }
.bh em { font-style: normal; color: #74acdf; font-size: 9.6pt; margin-right: 7pt; }
.hook { font-size: 10.6pt; font-weight: 700; line-height: 1.42; }
.hs { font-size: 7.6pt; color: #a9cdee; letter-spacing: .04em; margin-top: 5pt; font-weight: 700; }
.core p { font-size: 8.6pt; color: #b3b8c4; line-height: 1.6; }
.core p + p { margin-top: 4pt; }
.car p + p { margin-top: 8pt; }
.car i { color: #8a90a0; }
.scr { display: flex; flex-wrap: wrap; gap: 5pt; }
.scr i { font-style: normal; font-size: 7.6pt; font-weight: 700; letter-spacing: .03em; padding: 3pt 7pt; border-radius: 4pt; background: rgba(116,172,223,.12); color: #a9cdee; }
.box.cta { background: #0f1a2a; border-color: #29507a; }
.alts { margin-top: 7pt; padding-top: 7pt; border-top: .75pt solid #222733; }
.alts span { display: block; font-size: 6.6pt; font-weight: 700; letter-spacing: .08em; color: #646a78; margin-bottom: 3pt; }
.alts p { font-size: 8.5pt; color: #b3b8c4; line-height: 1.5; }
.box.note p { font-size: 8.1pt; color: #a7adbb; font-style: italic; line-height: 1.6; }
"""

doc = f"<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><title>iamaegene Guiones por Embudo</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "iamaegene_Guiones_Embudo.pdf"
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)], check=True, stderr=subprocess.DEVNULL)
src.unlink()

md = ["# @iamaegene · Guiones por embudo", "",
      "Se hablan en inglés. `{{...}}` = dato tuyo que falta. Ritmo semanal: 4 de alcance, 2 de confianza, 1 de conversión, 2 carruseles.", ""]
for k, v in FUNNEL.items():
    md += [f"- **{k} ({v['es']})**: {v['goal']}. Mide: {v['metric']}."]
md.append("")
for i, s in enumerate(S):
    md += [f"## {i+1}. {s['title']}  ·  {s['funnel']}", "",
           f"**Fórmula:** {s['formula']} · **Edición:** {s['edit']} · **Duración:** {s['length']}" + (f" · **Keyword:** `{s['kw']}`" if s["kw"] else ""), "",
           f"**Hook:** \"{s['hook']}\"  ", f"**En pantalla:** {s['hook_screen']}", "", "**Alternativos:**"] + [f"- \"{h}\"" for h in s["alts"]] + \
          ["", "**Cuerpo:**", ""] + [f"> {p}\n>" for p in s["body"]] + \
          ["", "**Texto en pantalla:** " + " · ".join(f"`{t}`" for t in s["screen"]), "",
           f"**CTA:** \"{s['cta']}\"", "", f"*Dirección: {s['note']}*", "", "---", ""]
md += ["## Carruseles", ""] + [f"- **{f}** · {t}. {d}" for f, t, d in CAROUSELS] + ["", "## Historias", ""] + [f"- {x}" for x in STORIES]
(HERE / "guiones-embudo.md").write_text("\n".join(md) + "\n")
print(pdf)
