#!/usr/bin/env python3
"""La IA no te va a hacer viral - Personal Short Form reel (Maison Enterprises).   python3 build.py
Edit THIS file, never the generated compositions/*.html or index.html. All times are GLOBAL seconds on the cut; frames are frames of the cut.
The creator sits low in the frame, so the face-window graphics live ABOVE the head (y 290-600) and the caption sits under the chin."""
import os
import reel_engine as E, kit as K, psf as P

ROOT = os.path.dirname(os.path.abspath(__file__))
DUR = 54.638
sw = P.sw
# ---- windows in frames of the cut. Big jumps (cut_times.py): 324 361 420 442 587 608 719 919 1057 1162, each one starts or ends a FULL window.
FULLF = [(229, 324), (361, 420), (420, 442), (503, 587), (587, 608), (644, 719), (719, 796), (919, 936), (997, 1057), (1121, 1162)]
FULL = [[sw(a), sw(b)] for a, b in FULLF]
FACE, t = [], 0.0
for a, b in FULL:
    if a > t + 0.01: FACE.append([t, a])
    t = b
FACE.append([t, DUR])
EMPH = {"todos", "equivocado", "clientes", "genérica", "scroll", "revés", "multiplica", "preguntas", "ganchos", "directo", "error", "historia",
        "mejores", "volumen", "nadie", "tarde", "gancho", "exactamente"}
P.setup(ROOT, DUR, FACE, FULL, "La IA no te va a hacer viral", emph=EMPH, keep={"IA", "Internet"}, merge=(("cien", "100"),), cap_y=1222, split_cap_y=905)
W = lambda f: sw(f)

# ================================================================ B-roll windows (hard cuts, the voice carries on)
BR = "assets/broll/"
P.broll("b01-scroll", W(229), W(324), [(BR + "b0.mp4", 229, 95)])            # "...muy genérica y eso no frena el scroll de nadie"
P.broll("b02-escribir", W(644), W(719), [(BR + "b2.mp4", 644, 75)])          # "pedile cinco ganchos específicos para cada una"
P.broll("b03-grabar", W(997), W(1057), [(BR + "b3.mp4", 997, 60)])           # "Vos contás algo que nadie más puede hacerlo"

# ================================================================ full-screen scenes (shared look)
FCSS = """
  .fx-k{position:absolute;left:0;width:1080px;text-align:center;font-family:"HelvB",Helvetica,sans-serif;font-weight:700;letter-spacing:-.045em;color:#F2F0EC;opacity:0}
  .fx-p{font-family:"PlayIt",serif;font-weight:500;color:#FF7A1A;letter-spacing:-.03em}
  .fx-card{position:absolute;width:250px;height:330px;border-radius:30px;background:linear-gradient(180deg,#1C1A18,#0F0E0D);border:2px solid rgba(255,255,255,.22);box-shadow:0 26px 60px rgba(0,0,0,.6);opacity:0;box-sizing:border-box;overflow:hidden}
  .fx-card .th{position:absolute;left:18px;top:18px;right:18px;height:170px;border-radius:18px;background:linear-gradient(135deg,#FF7A1A,#7A2E05)}
  .fx-card .th svg{position:absolute;left:50%;top:50%;margin:-30px 0 0 -30px}
  .fx-card .l1,.fx-card .l2{position:absolute;left:22px;height:18px;border-radius:9px;background:rgba(255,255,255,.55)} .fx-card .l1{top:212px;width:190px} .fx-card .l2{top:246px;width:130px;background:rgba(255,255,255,.3)}
  .fx-pill{position:absolute;left:190px;width:700px;height:120px;border-radius:60px;display:flex;align-items:center;gap:26px;padding-left:34px;box-sizing:border-box;font-family:"HelvB",Helvetica,sans-serif;font-weight:700;font-size:52px;letter-spacing:-.04em;color:#fff;opacity:0}
  .fx-pill b{display:flex;align-items:center;justify-content:center;width:76px;height:76px;border-radius:38px;background:#FF7A1A;color:#120C08;font-size:44px;flex:none}
  .fx-pill.dim{color:rgba(255,255,255,.35)} .fx-pill.dim b{background:rgba(255,255,255,.14);color:rgba(255,255,255,.45)}
"""
PLAY = '<svg width="60" height="60" viewBox="0 0 60 60"><circle cx="30" cy="30" r="29" fill="rgba(0,0,0,.35)"/><path d="M24,18 L42,30 L24,42 Z" fill="#fff"/></svg>'
def card(i, left, top, extra=""):
    return '<div id="{ID}-%s" class="fx-card" style="left:%dpx;top:%dpx;%s"><div class="th">%s</div><i class="l1"></i><i class="l2"></i></div>' % (i, left, top, extra, PLAY)

# 15.05 - 17.52  "Vos nos das el contenido y la IA lo multiplica": one real piece in the middle, then the copies fan out around it
cards = card("c0", 415, 520, "z-index:3;border:3px solid #FF7A1A;box-shadow:0 0 70px rgba(255,122,26,.55),0 26px 60px rgba(0,0,0,.6)")
spots = [(80, 330), (750, 330), (80, 760), (750, 760), (415, 930), (415, 130)]
cards += "".join(card("m%d" % k, x, y, "transform:scale(.8)") for k, (x, y) in enumerate(spots[:5]))
body = cards + '<div id="{ID}-t1" class="fx-k" style="top:330px;font-size:64px">tu <span class="fx-p">contenido</span></div>' \
              '<div id="{ID}-t2" class="fx-k" style="top:340px;font-size:120px;line-height:1"><span class="fx-p">&times;10</span></div>'
js = ('tl.set(q("t1"), {opacity:1}, 0); pop(tl, "c0", %s, {from:.7, d:.5, e:"power3.out"});' % (W(361) + 0.02) +
      'out(tl, "t1", 16.3, .25);' +
      "".join('__ft(q("m%d"), {opacity:0, x:%d, y:%d, scale:.4}, {opacity:1, x:0, y:0, scale:.8, duration:.55, ease:"power3.out"}, T(%s));' % (k, 415 - x, 520 - y, round(16.78 + k * 0.06, 3)) for k, (x, y) in enumerate(spots[:5])) +
      '__ft(q("t2"), {opacity:0, scale:.6}, {opacity:1, scale:1, duration:.45, ease:"power3.out"}, T(16.95));')
K.raw("a01-multiplica", W(361), W(420), True, body, FCSS, js)
K.ac(16.78, "shine", -22)

# step cards = the reel's transitions: big orange numeral, a line that wipes across, the label
def step(sid, a, b, num, label):
    body = ('<div id="{ID}-n" class="fx-k fx-p" style="top:420px;font-size:330px;line-height:1">%s</div>'
            '<div id="{ID}-ln" style="position:absolute;left:340px;top:820px;width:400px;height:6px;border-radius:3px;background:#FF7A1A;box-shadow:0 0 30px rgba(255,122,26,.8);transform:scaleX(0);transform-origin:0 50%%"></div>'
            '<div id="{ID}-lb" class="fx-k" style="top:870px;font-size:72px;letter-spacing:.2em;margin-left:.1em">%s</div>') % (num, label)
    js = ('__ft(q("n"), {opacity:0, scale:1.25, filter:"blur(20px)"}, {opacity:1, scale:1, filter:"blur(0px)", duration:.45, ease:"expo.out"}, 0);'
          '__ft(q("ln"), {scaleX:0}, {scaleX:1, duration:.4, ease:"power3.inOut"}, .08);'
          '__ft(q("lb"), {opacity:0, y:20}, {opacity:1, y:0, duration:.35, ease:"power3.out"}, .16);')
    K.raw(sid, a, b, True, body, FCSS + "#{ID}-in{opacity:1 !important;filter:none !important}", js)
    K.ac(a + 0.02, "impact", -27)
step("st1", W(420), W(442), "01", "PASO UNO")
step("st2", W(587), W(608), "02", "PASO DOS")
step("st3", W(919), W(936), "03", "PASO TRES")

# 20.98 - 24.48  "ya sea por mensaje, por llamada, en los comentarios": the client on her phone, the real questions dropping in
PHONE = '<svg width="50" height="50" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#34C759"/><path d="M15,12 c2,-1 4,0 5,2 l2,4 c1,2 0,3 -1,4 l-2,1 c1,4 4,7 8,8 l1,-2 c1,-1 2,-2 4,-1 l4,2 c2,1 3,3 2,5 c-1,3 -4,4 -7,3 c-9,-2 -16,-9 -18,-18 c-1,-3 0,-6 2,-8 z" fill="#fff"/></svg>'
nb = lambda i, top, title, text: K.banner(i, top, title, text)
body = (K.clip("assets/broll/b1.mp4", 0, round(W(587) - W(503), 3), "position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:1") +
        '<div style="position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,.15) 40%,rgba(0,0,0,0) 60%)"></div>'
        '<div style="position:absolute;inset:0;z-index:3">' + nb("a", 330, "lu.boutique", "Te envió un mensaje: &iquest;cu&aacute;nto sale?") +
        nb("b", 330, "Llamada perdida", "Cliente nuevo &middot; hace 1 min").replace(K.igicon("{ID}b"), PHONE) +
        nb("c", 330, "marce.ok", "coment&oacute;: &iquest;esto sirve para mi negocio?") + '</div>')
js = K.NJS + 'drop("a", 21.45); drop("b", 22.38); push(["a"], 22.38, 1); drop("c", 23.3); push(["b"], 23.3, 1); push(["a"], 23.3, 2);'
K.raw("n01-preguntas", W(503), W(587), True, body, P.BCSS + K.NBCSS, js)
for t in (21.45, 22.38, 23.3): K.ac(t, "pop", -22)

# 29.99 - 33.20  "Puede ser uno directo, uno con una pregunta,": the kinds of hook, lit as they are named
PILLS = [("1", "Directo"), ("2", "Con una pregunta"), ("3", "Error com&uacute;n"), ("4", "Una historia")]
body = '<div id="{ID}-hd" class="fx-k" style="top:300px;font-size:60px">5 <span class="fx-p">ganchos</span> por pregunta</div>' + "".join(
    '<div id="{ID}-p%d" class="fx-pill mc dim" style="top:%dpx"><b>%s</b>%s</div>' % (k, 470 + k * 160, n, tx) for k, (n, tx) in enumerate(PILLS))
js = 'tl.set(q("hd"), {opacity:1}, 0);' + "".join('__ft(q("p%d"), {opacity:0, y:30}, {opacity:1, y:0, duration:.4, ease:"power3.out"}, T(%s));' % (k, round(W(719) + 0.1 + k * 0.08, 3)) for k in range(4)) + \
     "".join('tl.set(q("p%d"), {background:"#FF7A1A", borderColor:"#FFB27A", color:"#120C08", boxShadow:"0 0 50px rgba(255,122,26,.55)"}, T(%s)); tl.set(q("p%d") + " b", {background:"#120C08", color:"#FF7A1A"}, T(%s));' % (k, t, k, t) for k, t in ((0, 30.7), (1, 31.95)))
K.raw("h01-tipos", W(719), W(796), True, body, FCSS, js)
K.ac(30.7, "click", -24); K.ac(31.95, "click", -24)

# 46.75 - 48.47  "a tener cien ganchos en una tarde": the wall filling with notes, the number on top
body = (K.clip("assets/broll/b4.mp4", 0, round(W(1162) - W(1121), 3), "position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:1") +
        '<div style="position:absolute;inset:0;z-index:2;background:radial-gradient(70% 40% at 50% 40%,rgba(0,0,0,.55),rgba(0,0,0,0))"></div>'
        '<div id="{ID}-n" class="fx-k" style="z-index:3;top:420px;font-size:260px;line-height:1;color:#fff;text-shadow:0 10px 50px rgba(0,0,0,.7)">0</div>'
        '')
js = ('tl.set(q("n"), {opacity:1}, 0); (function(){ const el = document.querySelector(q("n")), c = {n:0};'
      '__ft(c, {n:0}, {n:100, duration:1.0, ease:"power2.out", onUpdate:function(){ el.textContent = Math.round(c.n); }}, T(46.95)); })();')
K.raw("c01-cien", W(1121), W(1162), True, body, P.BCSS + FCSS, js)
K.ac(47.2, "riser", -30)

# ================================================================ graphics on the creator (above the head, y 290-600)
G = []
def g(html): K.OF.append(html)
GC = """
  .g-k{position:absolute;left:0;width:1080px;text-align:center;font-family:"HelvB",Helvetica,sans-serif;font-weight:700;letter-spacing:-.045em;color:#fff;text-shadow:0 4px 22px rgba(0,0,0,.45);opacity:0}
  .g-card{position:absolute;width:200px;height:250px;border-radius:24px;background:#16130F;border:2px solid rgba(255,255,255,.25);box-shadow:0 20px 50px rgba(0,0,0,.45);box-sizing:border-box;overflow:hidden;opacity:0}
  .g-card .th{position:absolute;left:14px;top:14px;right:14px;height:130px;border-radius:14px;background:linear-gradient(135deg,#8E8A84,#5B5853)}
  .g-card .l1,.g-card .l2{position:absolute;left:16px;height:14px;border-radius:7px;background:rgba(255,255,255,.45)} .g-card .l1{top:164px;width:150px} .g-card .l2{top:192px;width:100px;background:rgba(255,255,255,.25)}
  .g-bub{position:absolute;padding:20px 30px;border-radius:34px;background:rgba(18,16,14,.92);border:2px solid rgba(255,255,255,.22);box-shadow:0 18px 44px rgba(0,0,0,.45);font-family:"HelvB",Helvetica,sans-serif;font-weight:700;font-size:44px;letter-spacing:-.03em;color:#fff;white-space:nowrap;opacity:0}
  .g-bub.me{background:#FF7A1A;border-color:#FFB27A;color:#120C08}
  .g-chip{position:absolute;display:flex;align-items:center;justify-content:center;border-radius:50%;box-sizing:border-box;opacity:0}
"""
# 0 - 2.2 s  HOOK (moved under the top safe line)
K.hook("La IA no te va a", "hacer viral", 2.25)
K.ac(0.02, "riser", -32)
# 2.3 - 3.6  "y le salió igual que el de todos": three identical posts, the same post three times
for k in range(3):
    g('<div id="gc%d" class="g-card" style="left:%dpx;top:330px"><div class="th"></div><i class="l1"></i><i class="l2"></i></div>' % (k, 175 + k * 260))
K.ojs("".join("opop('#gc%d', %s);" % (k, round(2.45 + k * 0.12, 2)) for k in range(3)) + "oout(['#gc0','#gc1','#gc2'], 3.55);")
K.ac(2.45, "pops", -25)
# 3.67 - 5.6  "Eso es porque le pediste lo equivocado": the generic prompt, struck through in red
g('<div id="gp" class="g-bub" style="left:170px;top:420px;width:740px;text-align:center;box-sizing:border-box;font-family:HelvR,Helvetica,sans-serif;font-weight:400">'
  '&ldquo;Escribime un post viral&rdquo;<i id="gps" style="position:absolute;left:24px;right:24px;top:50%;height:7px;margin-top:-3px;border-radius:4px;background:#B3261E;box-shadow:0 0 18px rgba(179,38,30,.8);transform-origin:0 50%"></i></div>')
K.ojs("opop('#gp', 3.75); tl.fromTo('#gps', {scaleX:0}, {scaleX:1, duration:.35, ease:'power3.inOut', immediateRender:true}, 4.5); oout('#gp', 5.55);")
K.ac(4.5, "swish", -26)
# 5.71 - 9.5  "La IA no conoce a tus clientes": the AI on one side, the clients on the other, a question mark between
AV = '<svg viewBox="0 0 24 24" width="62" height="62"><circle cx="12" cy="8" r="4.4" fill="#F2F0EC"/><path d="M3.4,22 C4.4,15.4 19.6,15.4 20.6,22 Z" fill="#F2F0EC"/></svg>'
g('<div id="gai" class="g-chip" style="left:150px;top:350px;width:200px;height:200px;background:#120F0C;border:4px solid #FF7A1A;box-shadow:0 0 50px rgba(255,122,26,.5);font-family:HelvB,Helvetica,sans-serif;font-size:84px;font-weight:700;color:#FF7A1A;letter-spacing:-.04em">IA</div>')
for k, (x, y) in enumerate([(660, 330), (800, 410), (660, 490)]):
    g('<div id="gcl%d" class="g-chip" style="left:%dpx;top:%dpx;width:120px;height:120px;background:#2A2724;border:3px solid rgba(255,255,255,.5)">%s</div>' % (k, x, y, AV))
g('<div id="gq" class="g-k" style="left:380px;width:260px;top:375px;font-size:150px;color:#B3261E">?</div>')
K.ojs("opop('#gai', 5.8);" + "".join("opop('#gcl%d', %s);" % (k, round(6.75 + k * 0.1, 2)) for k in range(3)) +
      "tl.fromTo('#gq', {opacity:0, scale:.5}, {opacity:1, scale:1, duration:.4, ease:'power3.out'}, 7.0);"
      "oout(['#gai','#gcl0','#gcl1','#gcl2','#gq'], 9.25);")
K.ac(5.8, "pop", -25); K.ac(7.0, "pop", -24)
# 13.51 - 15.05  "Nosotros lo hacemos al revés": the arrow turns round
g('<div id="gr" class="g-chip" style="left:440px;top:330px;width:200px;height:200px;background:#FF7A1A;box-shadow:0 0 60px rgba(255,122,26,.6)">'
  '<svg id="grs" width="120" height="120" viewBox="0 0 120 120"><path d="M20,60 L96,60 M72,34 L98,60 L72,86" fill="none" stroke="#120C08" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
K.ojs("opop('#gr', %s); tl.to('#grs', {rotation:180, duration:.55, ease:'power3.inOut'}, 14.35); oout('#gr', %s);" % (W(324) + 0.03, W(361) - 0.25))
K.ac(14.35, "swirl", -27)
# 18.43 - 20.98  "buscá las preguntas que más te hacen tus clientes": the questions, in their words
for k, (tx, x, y, t) in enumerate([("&iquest;Cu&aacute;nto sale?", 150, 300, 18.95), ("&iquest;C&oacute;mo empiezo?", 470, 420, 19.45), ("&iquest;Sirve para m&iacute;?", 200, 540, 19.95)]):
    g('<div id="gq%d" class="g-bub" style="left:%dpx;top:%dpx">%s</div>' % (k, x, y, tx))
    K.ojs("opop('#gq%d', %s);" % (k, t)); K.ac(t, "pop", -26)
K.ojs("oout(['#gq0','#gq1','#gq2'], %s);" % (W(503) - 0.3))
# 25.36 - 26.86  "pasale esas preguntas y pedile": the request typed to the AI
g('<div id="gm" class="g-bub me" style="left:160px;top:380px;width:760px;white-space:normal;line-height:1.15;box-sizing:border-box;font-size:46px">Dame 5 ganchos para:<br><span style="font-family:HelvR,Helvetica,sans-serif;font-weight:400">&ldquo;&iquest;Cu&aacute;nto sale?&rdquo;</span></div>')
K.ojs("opop('#gm', %s); oout('#gm', %s);" % (W(608) + 0.05, W(644) - 0.28)); K.ac(W(608) + 0.1, "click", -24)
# 33.20 - 38.33  "uno con un error común, una con una historia que lleve la contraria": the last two kinds, then the audience growing
g('<div id="ge1" class="g-bub" style="left:120px;top:330px;border-color:#B3261E;background:#B3261E">3 &middot; Error com&uacute;n</div>')
g('<div id="ge2" class="g-bub" style="left:470px;top:470px;border-color:#FF7A1A">4 &middot; <span style="font-family:PlayIt,serif;font-weight:500;color:#FF7A1A">Una historia</span></div>')
g('<svg id="gup" width="560" height="200" viewBox="0 0 560 200" style="position:absolute;left:260px;top:360px;opacity:0;overflow:visible"><path id="gupl" d="M10,180 L170,120 L300,140 L540,20" fill="none" stroke="#2FA65A" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="800" stroke-dashoffset="800" style="filter:drop-shadow(0 0 16px rgba(47,166,90,.7))"/>'
  '<path d="M500,14 L544,18 L536,62" fill="none" stroke="#2FA65A" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg>')
K.ojs("opop('#ge1', 33.7); opop('#ge2', 35.1); oout(['#ge1','#ge2'], 37.05);"
      "tl.set('#gup', {opacity:1}, 37.25); tl.to('#gupl', {strokeDashoffset:0, duration:.6, ease:'power2.inOut'}, 37.25); oout('#gup', %s);" % (W(919) - 0.25))
K.ac(33.7, "pop", -25); K.ac(35.1, "pop", -25); K.ac(37.3, "shine", -24)
# 39.05 - 41.59  "elegís los mejores y la IA le pone el volumen": five hooks, two kept, then the volume goes up
for k in range(5):
    g('<div id="gh%d" style="position:absolute;left:%dpx;top:300px;width:150px;height:84px;border-radius:20px;background:rgba(18,16,14,.9);border:2px solid rgba(255,255,255,.25);box-sizing:border-box;opacity:0;display:flex;align-items:center;justify-content:center;font-family:HelvB,Helvetica,sans-serif;font-weight:700;font-size:40px;color:#fff">%d</div>' % (k, 150 + k * 162, k + 1))
K.ojs("".join("opop('#gh%d', %s);" % (k, round(W(936) + 0.05 + k * 0.06, 2)) for k in range(5)) +
      "tl.to(['#gh1','#gh3'], {background:'#FF7A1A', borderColor:'#FF7A1A', color:'#120C08', scale:1.1, boxShadow:'0 0 40px rgba(255,122,26,.6)', duration:.35, ease:'power2.inOut'}, 39.7);"
      "tl.to(['#gh0','#gh2','#gh4'], {opacity:.3, duration:.35, ease:'power2.inOut'}, 39.7);")
K.ac(39.7, "click", -24)
for k in range(9):
    g('<i id="gv%d" style="position:absolute;left:%dpx;top:405px;width:44px;height:120px;border-radius:12px;background:linear-gradient(180deg,#FFB27A,#FF7A1A);box-shadow:0 0 24px rgba(255,122,26,.55);transform-origin:50%% 100%%;opacity:0"></i>' % (k, 290 + k * 58))
K.ojs("tl.set([%s], {opacity:1}, 40.6);" % ",".join("'#gv%d'" % k for k in range(9)) +
      "".join("tl.fromTo('#gv%d', {scaleY:.08}, {scaleY:%s, duration:.45, ease:'power3.out', immediateRender:true}, %s);" % (k, round(0.35 + 0.65 * (k + 1) / 9, 2), round(40.75 + k * 0.04, 2)) for k in range(9)) +
      "oout([%s], %s);" % (",".join(["'#gh%d'" % k for k in range(5)] + ["'#gv%d'" % k for k in range(9)]), W(997) - 0.25))
K.ac(40.75, "riser", -28)
# 44.09 - 46.75  "De esta manera, pasás de no saber publicar": the empty post with the cursor waiting
g('<div id="gx" style="position:absolute;left:340px;top:310px;width:400px;height:260px;border-radius:28px;background:rgba(18,16,14,.92);border:2px dashed rgba(255,255,255,.4);box-sizing:border-box;opacity:0">'
  '<div style="position:absolute;left:0;right:0;top:56px;text-align:center;font-family:HelvB,Helvetica,sans-serif;font-weight:700;font-size:40px;color:rgba(255,255,255,.55)">Nueva publicaci&oacute;n</div>'
  '<i id="gxc" style="position:absolute;left:198px;top:130px;width:5px;height:66px;border-radius:3px;background:#FF7A1A"></i></div>')
K.ojs("opop('#gx', %s); tl.fromTo('#gxc', {opacity:1}, {opacity:0, duration:.35, ease:'steps(1)', repeat:5, yoyo:true}, 44.6); oout('#gx', %s);" % (W(1057) + 0.05, W(1121) - 0.28))
# 48.47 - end  CTA: the word GANCHO sent by DM, then the reply from Maison
g('<div id="gd" style="position:absolute;left:150px;top:330px;width:780px;height:120px;border-radius:60px;background:rgba(18,16,14,.94);border:2px solid rgba(255,255,255,.28);box-sizing:border-box;opacity:0;display:flex;align-items:center;padding:0 16px 0 40px;gap:20px;box-shadow:0 20px 50px rgba(0,0,0,.45)">'
  '<span id="gdt" style="flex:1;font-family:HelvB,Helvetica,sans-serif;font-weight:700;font-size:54px;letter-spacing:.06em;color:#fff;white-space:nowrap;overflow:hidden"></span>'
  '<i id="gdb" style="display:flex;align-items:center;justify-content:center;width:92px;height:92px;border-radius:46px;background:#3B82F6;font-style:normal">'
  '<svg width="44" height="44" viewBox="0 0 24 24"><path d="M3,11 L21,3 L13,21 L11,13 Z" fill="#fff"/></svg></i></div>')
g(K.banner("X", 330, "maison.enterprises", "Te mandamos lo que usamos", me=True).replace("{ID}-nX", "gdr").replace("{ID}X", "gdr"))
K.ojs("opop('#gd', %s);" % (W(1162) + 0.05) +
      "(function(){ const el = document.querySelector('#gdt'), w = 'GANCHO', c = {n:0}; tl.fromTo(c, {n:0}, {n:6, duration:.5, ease:'none', onUpdate:function(){ el.textContent = w.slice(0, Math.round(c.n)); }}, 49.45); })();"
      "tl.to('#gdb', {scale:1.18, duration:.12, yoyo:true, repeat:1, ease:'power2.inOut'}, 50.55); tl.to('#gd', {y:-20, opacity:0, duration:.35, ease:'power2.in'}, 51.3);"
      "opop('#gdr', 51.6);")
K.ac(49.45, "click", -26); K.ac(50.55, "swoosh", -25); K.ac(51.6, "pop", -22)

P.finish(css=GC + """
  .hk1{top:300px !important} .hk2w{top:398px !important}
  #gdr{transform:scale(.88);transform-origin:540px 0}
""")
