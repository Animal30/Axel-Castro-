#!/usr/bin/env python3
"""¿Por qué tus anuncios no funcionan? - Maison Enterprises (ES). Business Short Form reel, captions = fitted-stacked-captions overlay.
Camera = Nahuel's tight cut with Rey La Tinta's ad hook spliced in at 13.3864-20.4768 (edit.mp4). Times are GLOBAL seconds on that edit."""
import os
import reel_engine as E
import kit as K

ROOT = os.path.dirname(os.path.abspath(__file__))
DUR = 42.625
FACE = [[0, 2.4588], [2.4588, 7.0467], [7.0467, 12.5522], [12.5522, 13.3864], [13.3864, 20.4768],
        [30.5702, 34.324], [34.324, 35.9923], [35.9923, 39.4124], [39.4124, DUR]]
FULL = [[23.6049, 27.4421]]
E.init(ROOT, DUR, FACE, FULL, caps="captions.json", title="Por qué tus anuncios no funcionan")   # engine captions off: fitted overlay on top
P = "assets/proof/"

K.raw("s00", 0, 20.25, False, "", "", "")

# 01 (split) mismo cliente, mismo objetivo, dos anuncios: the real Meta Ads screen of Rey La Tinta
K.raw("s01-meta", 20.25, 23.6049, True and False, """<div id="{ID}-win" class="win"><img class="hd" src="assets/proof/head.jpg"/>
      <div id="{ID}-c0" class="cc"><img src="assets/proof/first.jpg"/><span class="tg">Anuncio 1</span></div>
      <div id="{ID}-c1" class="cc"><img src="assets/proof/sec.jpg"/><span class="tg">Anuncio 2</span></div></div>""",
    """.win{position:absolute;left:50px;top:20px;width:980px;height:500px;border-radius:34px;overflow:hidden;background:#1C2530;border:2px solid rgba(255,255,255,.22);box-shadow:0 30px 70px rgba(0,0,0,.6);z-index:5}
    .hd{display:block;width:980px;height:150px;object-fit:cover;object-position:0 0}
    .cc{position:absolute;top:180px;width:455px;height:229px;border-radius:20px;overflow:hidden;opacity:0;box-shadow:0 14px 34px rgba(0,0,0,.5)} .cc img{width:100%;height:100%;display:block}
    #s01-meta-c0{left:24px} #s01-meta-c1{left:501px}
    .tg{position:absolute;left:0;right:0;bottom:-58px;text-align:center;font-family:"HelvB";font-size:34px;color:#F2F0EC;letter-spacing:-.03em}
    .cc{overflow:visible} .cc img{border-radius:20px}""",
    """tl.fromTo(q("c0"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(22.85)); tl.fromTo(q("c1"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(23.15));""")
K.ac(20.5, "swoosh", -24); K.ac(22.85, "pop", -25); K.ac(23.15, "pop", -25)

# 02 (FULL) el primero: 1 conversación a $37 (red) ... el segundo (green card arrives)
K.raw("s02-vs", 23.6049, 27.4421, True, """<div id="{ID}-a" class="big"><img src="assets/proof/first.jpg"/><i id="{ID}-ra" class="ring"></i><span class="lb">Anuncio 1</span></div>
    <div id="{ID}-b" class="big"><img src="assets/proof/sec.jpg"/><i id="{ID}-rb" class="ring"></i><span class="lb">Anuncio 2</span></div>
    <div id="{ID}-x" class="chip red">$37 por conversación</div>""",
    """.big{position:absolute;left:150px;width:780px;height:393px;border-radius:28px;z-index:5;opacity:0;box-shadow:0 30px 70px rgba(0,0,0,.6)} .big img{width:100%;height:100%;display:block;border-radius:28px}
    #s02-vs-a{top:250px} #s02-vs-b{top:760px}
    .ring{position:absolute;inset:-6px;border-radius:34px;border:6px solid transparent}
    .lb{position:absolute;left:24px;top:-56px;font-family:"HelvB";font-size:36px;color:#F2F0EC;letter-spacing:-.03em}
    .chip{position:absolute;left:290px;top:668px;width:500px;height:72px;border-radius:36px;display:flex;align-items:center;justify-content:center;font-family:"HelvB";font-size:34px;letter-spacing:-.03em;opacity:0;z-index:7}
    .chip.red{background:#B3261E;color:#fff;box-shadow:0 0 46px rgba(179,38,30,.6)}""",
    """tl.fromTo(q("a"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(23.4));
    __tt(q("ra"), {borderColor:"#B3261E", boxShadow:"0 0 60px rgba(179,38,30,.6)", duration:0.35}, T(25.3)); __ft(q("x"), {opacity:0, scale:1.2}, {opacity:1, scale:1, duration:0.35, ease:"power3.out"}, T(25.4));
    __tt([q("a"), q("x")], {opacity:0.4, duration:0.4}, T(26.6));
    tl.fromTo(q("b"), {opacity:0, y:40}, {opacity:1, y:0, duration:0.5}, T(26.75)); __tt(q("rb"), {borderColor:"#2FA65A", boxShadow:"0 0 60px rgba(47,166,90,.6)", duration:0.35}, T(26.85));""")
K.ac(23.65, "woosh", -24); K.ac(25.4, "impact", -30); K.ac(26.85, "shine", -24)

# 03 (split) el segundo: 12-14 conversaciones a $12 - zoom on the winning card, the cost lights green, then "3x más barato"
K.raw("s03-win", 27.4421, 30.5702, False, """<div id="{ID}-w" class="wc"><img src="assets/proof/sec.jpg"/><i id="{ID}-h1" class="hl" style="left:10px;top:180px;width:170px;height:90px"></i><i id="{ID}-h2" class="hl" style="left:180px;top:180px;width:250px;height:90px"></i></div>
    <div id="{ID}-k" class="chip grn">3 veces más barato</div>""",
    """.wc{position:absolute;left:140px;top:10px;width:800px;height:403px;border-radius:28px;z-index:5;box-shadow:0 0 70px rgba(47,166,90,.5),0 30px 70px rgba(0,0,0,.6);border:5px solid #2FA65A} .wc img{width:100%;height:100%;display:block;border-radius:24px}
    .hl{position:absolute;border-radius:18px;border:5px solid #2FA65A;box-shadow:0 0 30px rgba(47,166,90,.8);opacity:0}
    .chip{position:absolute;left:290px;top:440px;width:500px;height:76px;border-radius:38px;display:flex;align-items:center;justify-content:center;font-family:"HelvB";font-size:36px;letter-spacing:-.03em;opacity:0;z-index:7}
    .chip.grn{background:#2FA65A;color:#06140B;box-shadow:0 0 46px rgba(47,166,90,.6)}""",
    """tl.fromTo(q("h1"), {opacity:0, scale:1.2}, {opacity:1, scale:1, duration:0.35}, T(27.75)); tl.fromTo(q("h2"), {opacity:0, scale:1.2}, {opacity:1, scale:1, duration:0.35}, T(29.4));
    tl.fromTo(q("k"), {opacity:0, y:20}, {opacity:1, y:0, duration:0.45}, T(30.05)); sweep(tl, "k", 30.1);""")
K.ac(27.75, "pop", -24); K.ac(29.4, "pop", -24); K.ac(30.05, "shine", -23)

K.raw("s04", 30.5702, DUR, False, "", "", "")

# ---------------------------------------------------------------- on the creator (top band, above the head; fitted captions sit under the chin)
K.hook("¿Querés saber por qué", "tus anuncios no funcionan?", 2.4)
# +1.000 anuncios
K.OF.append('<div id="k1" class="topc"><b id="k1n" class="de-num">0</b><span>anuncios lanzados</span></div>')
K.ojs("opop('#k1', 3.9); oout('#k1', 6.95); (function(){ const c={n:0}, el=$o('#k1n'); tl.fromTo(c,{n:0},{n:1000,duration:1.0,ease:'power2.inOut',onUpdate:function(){ el.textContent='+'+Math.round(c.n).toLocaleString('es-AR'); }},4.2); })();")
K.ac(3.9, "woosh", -25); K.ac(4.2, "riser", -33); K.ac(5.2, "shine", -25)
# the 3-second ring: drains while he says "más de tres segundos"
K.OF.append('<div id="tm" class="tm"><svg width="200" height="200" viewBox="0 0 200 200"><circle cx="100" cy="100" r="84" fill="rgba(12,10,9,.88)" stroke="rgba(255,255,255,.22)" stroke-width="14"/>'
            '<circle id="tmr" cx="100" cy="100" r="84" fill="none" stroke="#FF7A1A" stroke-width="14" stroke-linecap="round" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="0" transform="rotate(-90 100 100)"/></svg><b id="tmn">3s</b></div>')
K.ojs("opop('#tm', 7.5); oout('#tm', 12.45); tl.fromTo('#tmr', {strokeDashoffset:0}, {strokeDashoffset:1000, duration:2.4, ease:'none'}, 9.2);"
      " (function(){ const c={n:3}, el=$o('#tmn'); tl.fromTo(c,{n:3},{n:0,duration:2.4,ease:'none',onUpdate:function(){ el.textContent=Math.ceil(c.n)+'s'; }},9.2); })();"
      " tl.to('#tmr', {stroke:'#B3261E', duration:0.2}, 11.5); tl.to('#tmn', {color:'#FF8A80', duration:0.2}, 11.5);")
K.ac(7.5, "pop", -25); K.ac(11.6, "impact", -31)
# Rey's ad: a tag so the viewer knows it is a real client ad
K.OF.append('<div id="rt" class="rtag"><i></i>Anuncio real &middot; @rey_latinta</div>')
K.ojs("opop('#rt', 13.5); oout('#rt', 20.3);"); K.ac(13.39, "swoosh", -24)
# Meta igual, presupuesto igual, el anuncio cambió
rows = [("Meta", "igual", "", 30.7), ("Presupuesto", "igual", "", 31.65), ("El anuncio", "cambió", "hot", 32.95)]
for i, (a, b, hot, t) in enumerate(rows):
    K.OF.append('<div id="cr%d" class="crow%s" style="top:%dpx"><span>%s</span><b>%s</b></div>' % (i, " hot" if hot else "", 285 + i * 86, a, b))
    K.ojs("opop('#cr%d', %s); oout('#cr%d', 34.2);" % (i, t, i)); K.ac(t, "pop" if not hot else "shine", -25 if not hot else -23)
# no es el algoritmo / son los primeros segundos
K.OF.append('<div id="al" class="crow" style="top:300px"><span>El algoritmo</span><i id="alx" class="sx"></i></div><div id="ps" class="crow grn" style="top:400px"><span>Los primeros segundos</span></div>')
K.ojs("opop('#al', 36.1); tl.fromTo('#alx', {scaleX:0}, {scaleX:1, duration:0.3, ease:'power2.out'}, 36.75); tl.to('#al', {opacity:0.45, duration:0.3}, 37.0); oout('#al', 39.3); opop('#ps', 38.3); oout('#ps', 39.3);")
K.ac(36.1, "pop", -25); K.ac(36.75, "impact", -31); K.ac(38.3, "shine", -23)
# CTA: the DM arrives
K.OF.append(K.banner("X", 290, "tu.marca", "ANUNCIO").replace("{ID}-nX", "dm1").replace("{ID}X", "dm1"))
K.OF.append(K.banner("Y", 290, "Maison Enterprises", "Mandanos el anuncio y lo revisamos &#128064;", me=True).replace("{ID}-nY", "dm2").replace("{ID}Y", "dm2"))
K.ojs("opop('#dm1', 39.9); oout('#dm1', 41.2, 0.2); opop('#dm2', 41.3); oout('#dm2', 42.5);")
K.ac(39.9, "pop", -22); K.ac(41.3, "pop", -21)
K.flush("""#hk2{background:#FF7A1A !important;color:#120C08 !important} .ntm{font-size:0 !important} .ntm::after{content:"ahora";font-size:30px}
    .topc{position:absolute;left:290px;top:280px;width:500px;height:200px;border-radius:40px;background:rgba(12,10,9,.9);border:3px solid rgba(255,255,255,.45);display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 14px 34px rgba(0,0,0,.5);opacity:0}
    .topc b{font-family:"HelvB",sans-serif;font-size:96px;line-height:1;color:#FF7A1A;letter-spacing:-.05em} .topc span{font-family:"HelvB",sans-serif;font-size:34px;color:#F2F0EC;letter-spacing:-.03em;margin-top:6px}
    .tm{position:absolute;left:440px;top:290px;width:200px;height:200px;opacity:0} .tm svg{position:absolute;inset:0;filter:drop-shadow(0 0 18px rgba(255,122,26,.45))}
    .tm b{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:"HelvB",sans-serif;font-size:66px;color:#F2F0EC;letter-spacing:-.05em}
    .rtag{position:absolute;left:250px;top:290px;width:580px;height:76px;border-radius:38px;background:rgba(12,10,9,.88);border:2px solid rgba(255,122,26,.7);display:flex;align-items:center;justify-content:center;gap:14px;font-family:"HelvB",sans-serif;font-size:34px;color:#F2F0EC;letter-spacing:-.03em;opacity:0}
    .rtag i{width:16px;height:16px;border-radius:50%;background:#FF3B30;box-shadow:0 0 12px #FF3B30}
    .crow{position:absolute;left:250px;width:580px;height:72px;border-radius:36px;background:rgba(12,10,9,.9);border:3px solid rgba(255,255,255,.45);display:flex;align-items:center;justify-content:space-between;padding:0 34px;box-sizing:border-box;font-family:"HelvB",sans-serif;font-size:36px;color:#F2F0EC;letter-spacing:-.03em;opacity:0}
    .crow b{color:#9A928A} .crow.hot{background:#FF7A1A;border-color:#FF7A1A;color:#120C08;box-shadow:0 0 46px rgba(255,122,26,.55)} .crow.hot b{color:#120C08}
    .crow.grn{justify-content:center;background:#2FA65A;border-color:#2FA65A;color:#06140B;box-shadow:0 0 46px rgba(47,166,90,.55)} #al{justify-content:center}
    .sx{position:absolute;left:8%;right:8%;top:50%;height:7px;margin-top:-3px;border-radius:4px;background:#B3261E;transform:scaleX(0);transform-origin:0 50%;box-shadow:0 0 14px rgba(179,38,30,.8)}""")
E.build()
