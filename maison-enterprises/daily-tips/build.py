# Builds the Maison Enterprises Daily Marketing Tips playbook (research + hook bank + 30 scripts), HTML -> PDF.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""

from tips import TIPS

def esc(s): return html.escape(s, quote=False)
N = len(TIPS)
EYEBROW = '<div class="eyebrow">MAISON ENTERPRISES · DAILY MARKETING TIPS</div>'
def foot(right): return f'<div class="foot"><span>MAISON ENTERPRISES · DAILY MARKETING TIPS</span><span>{right}</span></div>'

FORMATS = [
    ("Marketing psychology", "“The trick brands use on you.” Studies and pricing tricks everyone has felt. Interesting to people who aren't marketers too, so it travels far and gets sent.", "Sends · reach"),
    ("Brand breakdown", "“How Costco / Liquid Death / Spotify did X.” Famous brands make people curious in the first second and work on cold audiences.", "Sends · new followers"),
    ("One tactic, do it today", "One specific thing to change today, with a real example. The format buyers save, and the one that builds trust with future clients.", "Saves · leads"),
    ("Myth / contrarian", "“Stop doing X.” Goes against a common belief, backed by a reason. Gets debate going in the comments.", "Comments"),
    ("Platform insider", "A feature or rule on Instagram or Meta that most people don't know. Feels like a secret, so people save it and come back.", "Saves · follows"),
    ("The series itself", "“Marketing Tip #12.” Numbering every video and ending with “tomorrow…” gives people a reason to follow instead of just watching once.", "Follows"),
]

HOOKS = [
    ("Hidden reason", "Costco hasn't raised this price since 1985. It's not generosity."),
    ("Weird result", "This option nobody bought almost tripled sales of the expensive one."),
    ("Stop doing", "Stop collecting testimonials that say 'amazing service'."),
    ("It's not X, it's Y", "Your emails aren't being ignored. Your subject lines are."),
    ("Free secret", "You can see every ad your competitor is running. For free."),
    ("Specific number", "One word got 94% of people to say yes."),
    ("Callout", "If you have a local business, this matters more than your website."),
    ("Myth bust", "9.99 still works, and it's not because people are dumb."),
    ("Unexpected brand", "This company sells water in a can. It's worth a billion."),
    ("Before you…", "Before you raise your ad budget, do this math."),
    ("The one most miss", "There are three ways to do this. The third one, nobody does."),
    ("Hidden feature", "Instagram has a button that tests your reel on strangers first."),
    ("You're doing it…", "You're still picking interests in your ads like it's 2019."),
    ("Your ___ is hiding", "Your best ad copy is hiding in your one-star reviews."),
    ("Story start", "A car burned down, and a cup brand had its best week."),
    ("What X won't do", "Posting every day won't make you viral. Here's what it will do."),
    ("Comparison", "Same offer, different words, way more people take it."),
    ("Ownership", "Your next 30 videos are already in your comments."),
    ("Cost", "Fake countdown timers are quietly killing your brand."),
    ("Insider question", "Why does everyone say 'comment GUIDE' at the end of their videos?"),
]

SOURCES = [
    "Instagram ranking signals (watch time, likes and sends per reach), Adam Mosseri, as reported in: dataslayer.ai/blog/instagram-algorithm-2025-complete-guide-for-marketers · highstyle.ai/insights/instagram-reels-algorithm-2026",
    "Short-form trends and hook timing: rightblogger.com/blog/short-form-video-tips · blog.mean.ceo/short-form-video-marketing-trends-june-2026 · vidiq.com/blog/post/viral-video-hooks-youtube-shorts",
    "Educational formats and goal-based scoring (sends / saves / comments): viral.app/blog/guides/how-to-make-a-reel-go-viral · influish.com/blog/viral-content-reel-ideas-for-2026-formats-hooks-and-strategies",
    "Talking-head editing and pacing: viberoll.questera.ai/learn/talking-head-video-editing-checklist · opus.pro/blog/video-editing-tips",
    "Meta Andromeda and creative-led targeting: segwise.ai/blog/meta-andromeda-update-creative-strategy-2026 · flighted.co/blog/meta-ads-strategy-for-dtc-brands",
]

def li(items): return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

pages = []
pages.append(f'''<section class="page">
  {EYEBROW}
  <h1>Daily Marketing Tips</h1>
  <div class="sub">One tip a day · 25-40 seconds · Talking head · English · 30-day playbook</div>
  <div class="box note"><div class="bh">THE IDEA</div><p>A daily series where Maison Enterprises teaches one marketing idea per video: a psychology trick, a famous brand's move, or a tactic people can use today. It's built to reach people who don't follow us yet (sends), earn the trust of business owners (saves), and turn viewers into followers (the series). It runs alongside the longer educational and ad scripts.</p></div>
  <div class="bh2">WHAT THE ALGORITHM REWARDS RIGHT NOW</div>
  <div class="grid3">
    <div class="box"><b class="big">01</b><h4>Watch time</h4><p>How much of the video people watch, and whether they rewatch it. Short, tight videos that end before people expect win here.</p></div>
    <div class="box"><b class="big">02</b><h4>Sends per reach</h4><p>Reported as the strongest signal for reaching non-followers. A DM share tells Instagram “show this to strangers.”</p></div>
    <div class="box"><b class="big">03</b><h4>Likes per reach</h4><p>Matters most with people who already follow. Saves and follows confirm the account is worth seeing again.</p></div>
  </div>
  <div class="bh2">THE FORMATS THAT PULL THE MOST VIEWS IN MARKETING</div>
  <table class="tbl"><tr><th>Format</th><th>Why it works</th><th>Built for</th></tr>
  {"".join(f"<tr><td><b>{a}</b></td><td>{esc(b)}</td><td class='h'>{c}</td></tr>" for a, b, c in FORMATS)}
  </table>
  <div class="box"><div class="bh">THE MIX FOR THE 30 DAYS</div><p>About <b>40% psychology and brand breakdowns</b> (reach and new followers), <b>45% tactics and platform insider tips</b> (saves and trust from buyers), and <b>15% comment or DM prompts</b> (conversations and leads). No two videos from the same category on consecutive days.</p></div>
  {foot("STRATEGY")}
</section>''')

pages.append(f'''<section class="page">
  {EYEBROW}
  <h1 class="h1s">Anatomy of a daily tip</h1>
  <div class="steps">
    <div><b>0-2s</b><h4>Hook</h4><p>Spoken line, on-screen text (max 6 words) and a strong first image, all saying the same thing. No “hi, I'm…”, no logo intro.</p></div>
    <div><b>2-6s</b><h4>Stakes</h4><p>Why it matters: a number, a famous brand or a mistake they're making. Open a loop that the end closes.</p></div>
    <div><b>6-30s</b><h4>One idea</h4><p>One example with real names and numbers, then the “do this” line. One idea per video, never a list of ten.</p></div>
    <div><b>Last 3s</b><h4>Close</h4><p>One ask that matches the goal: send, save, follow or comment. Rotate them. End before people expect it.</p></div>
  </div>
  <div class="grid2">
    <div class="box"><div class="bh">EDITING · RECOMMENDED TEMPLATE</div><p><b>Cutout Backdrop Reel</b> (the “green screen” style). You're cut out and placed over full-screen images that change with every idea: the Economist ad, the Costco hot dog, the Spotify Wrapped screens. It's the look the most-watched brand breakdown creators use, it needs no B-roll and no green screen, and the real brands on screen do the hooking.</p>
      <p>It also keeps the daily tips looking different from the longer <b>Glass Explainer</b> videos, so the feed has two series people recognize.</p></div>
    <div class="box"><div class="bh">EDITING · SPECS</div>{li([
      "<b>25-40 seconds</b>. Every silence and breath between sentences cut.",
      "A <b>new backdrop every idea</b>, roughly every 3-5 seconds. Real images, no watermarks.",
      "<b>Captions</b> 3-6 words, always in the same spot, the key word in gold.",
      "<b>Series label</b> “MARKETING TIP #01” in the corner of the first frame, the same on every video.",
      "Quiet sound effects on reveals. No music, or music very low under the voice.",
    ])}</div>
  </div>
  <div class="grid2">
    <div class="box"><div class="bh">RECORDING</div>{li([
      "Same set-up as the other scripts (vertical, 4K, lav mic, light in front).",
      "For the cut-out: a <b>plain wall</b>, nothing dark touching your outline, and a top that <b>isn't black</b>.",
      "<b>Batch it:</b> record 7-10 tips in one session, one file per tip. Same outfit is fine, it's a series.",
      "Say the numbers slowly and look at the lens on the hook.",
    ])}</div>
    <div class="box"><div class="bh">POSTING AND REVIEW</div>{li([
      "Same time every day. The series label and the time make it a habit.",
      "Use <b>Trial Reels</b> for the riskier hooks before sharing to followers.",
      "After 48 hours, log each tip: 3-second hold, average watch time, sends, saves, follows.",
      "Every Sunday: make more of the top three topics, drop the bottom three.",
    ])}</div>
  </div>
  {foot("PLAYBOOK")}
</section>''')

pages.append(f'''<section class="page">
  {EYEBROW}
  <h1 class="h1s">Hook bank</h1>
  <div class="sub">20 formulas that work in the marketing niche, with an example for each. Mix them with any tip.</div>
  <table class="tbl tight"><tr><th>#</th><th>Formula</th><th>Example</th></tr>
  {"".join(f"<tr><td class='h'>{i+1:02d}</td><td><b>{a}</b></td><td>“{esc(b)}”</td></tr>" for i, (a, b) in enumerate(HOOKS))}
  </table>
  <div class="src"><b>Research sources.</b> Most public guidance on the algorithm comes from Instagram's head Adam Mosseri as reported by marketing outlets; specific percentages from those outlets are directional, not official.<br>{"<br>".join(esc(s) for s in SOURCES)}</div>
  {foot("HOOKS")}
</section>''')

for i, t in enumerate(TIPS):
    body = "".join(f"<p>{esc(p)}</p>" for p in t["body"])
    pages.append(f'''<section class="page">
  {EYEBROW}
  <div class="top"><span class="sc"><i></i>MARKETING TIP #{i+1:02d}</span><span class="tag">DAY {i+1} OF {N}</span></div>
  <h2>{esc(t["title"])}</h2>
  <div class="facts">
    <div><span>CATEGORY</span><b>{esc(t["cat"])}</b></div>
    <div><span>LENGTH</span><b>25-40 sec</b></div>
    <div><span>BUILT FOR</span><b class="kw">{t["goal"]}</b></div>
    <div><span>ON-SCREEN TEXT</span><b>{esc(t["screen"])}</b></div>
  </div>
  <div class="lbl">HOOK</div>
  <p class="hook">{esc(t["hook"])}</p>
  <div class="lbl">SCRIPT</div>
  <div class="core">{body}</div>
  <div class="lbl">CLOSE</div>
  <p class="cta">{esc(t["cta"])}</p>
  <div class="box note"><div class="bh">BACKDROPS FOR THE EDIT</div><p>{esc(t["visuals"])}</p></div>
  {foot(f"{i+1:02d} / {N:02d}")}
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
h1 { font-size: 30pt; font-weight: 800; margin-top: 16pt; line-height: 1.1; }
h1.h1s { font-size: 24pt; }
.sub { color: #aaa69d; font-size: 10pt; margin-top: 5pt; }
.bh2 { font-size: 7.9pt; font-weight: 700; letter-spacing: .1em; color: #d4b06a; margin-top: 16pt; }
.box { background: #141311; border: .75pt solid #26231e; border-radius: 7pt; padding: 10pt 13pt; margin-top: 8pt; }
.box p, .box li { font-size: 8.5pt; color: #aaa69d; line-height: 1.55; }
.box p + p { margin-top: 5pt; }
.box b { color: #f5f3ef; }
.box ul { padding-left: 12pt; }
.box li { margin-top: 2.5pt; }
.box.note { background: #1a160e; border-color: #4a3d22; }
.bh { font-size: 7.6pt; font-weight: 700; letter-spacing: .08em; color: #d4b06a; margin-bottom: 5pt; }
.grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8pt; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8pt; }
.grid3 h4, .steps h4 { font-size: 10pt; margin: 2pt 0 4pt; }
.big { font-size: 18pt; color: #d4b06a; font-weight: 800; display: block; }
.tbl { width: 100%; border-collapse: collapse; margin-top: 8pt; }
.tbl th { font-size: 6.8pt; letter-spacing: .08em; color: #6c6860; text-align: left; padding: 5pt 6pt; border-bottom: 1pt solid #2c2a25; text-transform: uppercase; }
.tbl td { font-size: 8.2pt; color: #aaa69d; padding: 6pt 6pt; border-bottom: .75pt solid #1d1c19; vertical-align: top; line-height: 1.45; }
.tbl td b { color: #f5f3ef; }
.tbl.tight td { padding: 4.2pt 6pt; }
.tbl .h { color: #d4b06a; font-weight: 700; white-space: nowrap; }
.steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8pt; margin-top: 14pt; }
.steps > div { background: #141311; border: .75pt solid #26231e; border-radius: 7pt; padding: 10pt 11pt; border-top: 2pt solid #d4b06a; }
.steps b { font-size: 9pt; color: #d4b06a; }
.steps p { font-size: 8.2pt; color: #aaa69d; line-height: 1.5; }
.src { font-size: 6.9pt; color: #6c6860; line-height: 1.55; margin-top: 12pt; }
.src b { color: #aaa69d; }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 15pt; }
.sc { font-size: 8.4pt; font-weight: 700; letter-spacing: .08em; color: #d4b06a; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #d4b06a; display: inline-block; }
.tag { font-size: 7.3pt; font-weight: 700; letter-spacing: .1em; padding: 3pt 9pt; border-radius: 10pt; color: #f5f3ef; background: rgba(212,176,106,.16); }
h2 { font-size: 22pt; font-weight: 800; margin-top: 8pt; line-height: 1.2; }
.facts { display: grid; grid-template-columns: 1fr 1fr 1fr 1.6fr; gap: 7pt; margin-top: 12pt; }
.facts div { background: #141311; border: .75pt solid #26231e; border-radius: 6pt; padding: 9pt 10pt 11pt; }
.facts span { display: block; font-size: 7pt; letter-spacing: .06em; color: #6c6860; margin-bottom: 7pt; }
.facts b { font-size: 9.4pt; font-weight: 700; }
.kw { color: #d4b06a; }
.lbl { font-size: 7.6pt; font-weight: 700; letter-spacing: .1em; color: #6c6860; margin-top: 16pt; margin-bottom: 6pt; }
.hook { font-size: 17pt; font-weight: 700; line-height: 1.4; }
.core p { font-size: 13pt; line-height: 1.5; color: #dcd8cf; }
.core p + p { margin-top: 8pt; }
.cta { font-size: 14pt; font-weight: 700; line-height: 1.45; padding: 11pt 14pt; background: #141311; border: .75pt solid #4a3d22; border-radius: 7pt; }
.box.note p { font-style: italic; }
"""

doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Maison Enterprises Daily Marketing Tips</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "MaisonEnterprises_DailyMarketingTips.pdf"
subprocess.run(["/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--disable-gpu",
                "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)],
               check=True, stderr=subprocess.DEVNULL)
src.unlink()
print(pdf)
