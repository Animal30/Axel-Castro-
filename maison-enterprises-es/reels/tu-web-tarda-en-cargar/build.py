#!/usr/bin/env python3
"""Tu web tarda en cargar - Maison Enterprises (ES). Business Short Form reel, captions = fitted-stacked-captions overlay.
Times are seconds on the tight cut (~/reel-work/demora/out/cut.mp4)."""
import os
import reel_engine as E
import kit as K

ROOT = os.path.dirname(os.path.abspath(__file__))
DUR = 37.12
FACE = [[1.8332, 7.0884], [24.3974, 28.4431], [33.4481, DUR]]
E.init(ROOT, DUR, FACE, [], caps="captions.json", title="Tu web tarda en cargar")   # engine captions off: fitted overlay on top

# ---------------------------------------------------------------- 00 (split) "Este sitio web que no carga": a browser stuck loading
BROWSER_CSS = """.bw{position:absolute;left:90px;top:10px;width:900px;height:430px;border-radius:30px;background:#F4F2EF;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.6);z-index:5}
    .bt{height:64px;background:#E3E0DC;display:flex;align-items:center;gap:12px;padding:0 24px} .bt i{width:18px;height:18px;border-radius:50%;background:#C9C4BE} .bt i:nth-child(1){background:#FF5F57} .bt i:nth-child(2){background:#FEBC2E} .bt i:nth-child(3){background:#28C840}
    .bt span{margin-left:22px;flex:1;height:40px;border-radius:20px;background:#fff;display:flex;align-items:center;padding:0 22px;font-family:"HelvR",sans-serif;font-size:26px;color:#6b6560}
    .pb{height:8px;background:#E3E0DC} .pb b{display:block;height:100%;width:4%;background:#1A73E8}
    .sk{position:absolute;left:60px;border-radius:12px;background:#E3E0DC}
    .sp{position:absolute;left:390px;top:190px;width:120px;height:120px;border-radius:50%;border:12px solid #E3E0DC;border-top-color:#FF7A1A;box-sizing:border-box}
    .lt{position:absolute;left:0;right:0;top:330px;text-align:center;font-family:"HelvB",sans-serif;font-size:34px;color:#8a837c;letter-spacing:-.02em}"""
BROWSER = """<div id="{ID}-bw" class="bw"><div class="bt"><i></i><i></i><i></i><span>tu-negocio.com</span></div><div class="pb"><b id="{ID}-pb"></b></div>
    <div class="sk" style="top:110px;width:420px;height:34px"></div><div class="sk" style="top:160px;width:300px;height:22px"></div>
    <div id="{ID}-sp" class="sp"></div><div class="lt">Cargando...</div></div>"""
K.raw("s00-load", 0, 1.8332, False, BROWSER, BROWSER_CSS,
      """tl.fromTo(q("sp"), {rotation:0}, {rotation:900, duration:1.9, ease:"none"}, T(0)); tl.fromTo(q("pb"), {width:"4%"}, {width:"14%", duration:1.8, ease:"power2.out"}, T(0));""")
K.ac(0.15, "click", -27)

# ---------------------------------------------------------------- face 1.83-7.09: PARÁ, then the 3-second ring and -50% of the traffic
K.OF.append('<div id="st" class="stop"><b>PARÁ</b></div>')
K.ojs("opop('#st', 1.86); " + " ".join("tl.fromTo('#st', {scale:1.14}, {scale:1, duration:0.18, ease:'power2.out'}, %s);" % t for t in (2.10, 2.30, 2.52)) + " oout('#st', 2.75);")
K.ac(1.86, "impact", -29)
K.OF.append('<div id="tm" class="tm"><svg width="210" height="210" viewBox="0 0 200 200"><circle cx="100" cy="100" r="84" fill="rgba(12,10,9,.9)" stroke="rgba(255,255,255,.22)" stroke-width="14"/>'
            '<circle id="tmr" cx="100" cy="100" r="84" fill="none" stroke="#FF7A1A" stroke-width="14" stroke-linecap="round" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="0" transform="rotate(-90 100 100)"/></svg><b id="tmn">3s</b></div>')
K.ojs("opop('#tm', 3.0); oout('#tm', 6.85); tl.fromTo('#tmr', {strokeDashoffset:0}, {strokeDashoffset:1000, duration:1.6, ease:'none'}, 4.2);"
      " (function(){ const c={n:3}, el=$o('#tmn'); tl.fromTo(c,{n:3},{n:0,duration:1.6,ease:'none',onUpdate:function(){ el.textContent=Math.ceil(c.n)+'s'; }},4.2); })();"
      " tl.to('#tmr', {stroke:'#E5372B', duration:0.2}, 5.7); tl.to('#tmn', {color:'#FF8A80', duration:0.2}, 5.7);")
K.ac(3.0, "pop", -27)
K.OF.append('<div id="hf" class="half"><b id="hfn">0%</b><span>de tu tráfico</span></div>')
K.ojs("opop('#hf', 5.68); oout('#hf', 6.85); (function(){ const c={n:0}, el=$o('#hfn'); tl.fromTo(c,{n:0},{n:50,duration:0.7,ease:'power2.out',onUpdate:function(){ el.textContent='-'+Math.round(c.n)+'%'; }},5.75); })();")
K.ac(5.75, "impact", -30)

# ---------------------------------------------------------------- 01 (split) 5 seconds before they close it ... "estas tres cosas"
K.raw("s01-five", 7.0884, 12.01, False,
      """<div id="{ID}-rg" class="rg"><svg width="300" height="300" viewBox="0 0 200 200"><circle cx="100" cy="100" r="84" fill="rgba(12,10,9,.9)" stroke="rgba(255,255,255,.18)" stroke-width="12"/>
      <circle id="{ID}-rr" cx="100" cy="100" r="84" fill="none" stroke="#FF7A1A" stroke-width="12" stroke-linecap="round" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="0" transform="rotate(-90 100 100)"/></svg><b id="{ID}-rn">5</b><span>segundos</span></div>
      <div id="{ID}-mw" class="mw"><div class="bt"><i></i><i></i><i></i><span>tu-negocio.com</span><em id="{ID}-x">&#10005;</em></div><div class="sk" style="top:100px;width:260px;height:26px"></div><div class="sk" style="top:146px;width:180px;height:18px"></div><div class="sk" style="top:200px;width:330px;height:110px"></div></div>
      <svg id="{ID}-cur" class="cur" viewBox="0 0 24 24" width="64" height="64"><path d="M4,2 L4,20 L9,15.5 L12.5,22.5 L15.5,21 L12,14 L19,14 Z" fill="#fff" stroke="#120C08" stroke-width="1.4" stroke-linejoin="round"/></svg>
      <div id="{ID}-h3" class="h3"><b>3</b> errores que te cuestan clientes</div>""",
      """.rg{position:absolute;left:90px;top:110px;width:300px;height:300px} .rg svg{position:absolute;inset:0;filter:drop-shadow(0 0 22px rgba(255,122,26,.45))}
      .rg b{position:absolute;left:0;right:0;top:78px;text-align:center;font-family:"HelvB",sans-serif;font-size:120px;line-height:1;color:#F2F0EC;letter-spacing:-.05em} .rg span{position:absolute;left:0;right:0;top:200px;text-align:center;font-family:"HelvB",sans-serif;font-size:26px;color:#9A928A}
      .mw{position:absolute;left:460px;top:70px;width:530px;height:380px;border-radius:26px;background:#F4F2EF;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.6);z-index:5}
      .mw .bt{height:58px;background:#E3E0DC;display:flex;align-items:center;gap:10px;padding:0 20px} .mw .bt i{width:15px;height:15px;border-radius:50%;background:#C9C4BE}
      .mw .bt span{margin-left:14px;flex:1;height:34px;border-radius:17px;background:#fff;display:flex;align-items:center;padding:0 16px;font-family:"HelvR",sans-serif;font-size:22px;color:#6b6560}
      .mw .bt em{font-style:normal;width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-family:"HelvB",sans-serif;font-size:26px;color:#6b6560}
      .mw .sk{position:absolute;left:40px;border-radius:10px;background:#E3E0DC}
      .cur{position:absolute;left:760px;top:330px;z-index:7;opacity:0;filter:drop-shadow(0 6px 10px rgba(0,0,0,.5))}
      .h3{position:absolute;left:0;right:0;top:190px;text-align:center;font-family:"HelvB",sans-serif;font-size:54px;letter-spacing:-.045em;color:#F2F0EC;opacity:0} .h3 b{color:#FF7A1A;font-size:130px;vertical-align:-0.18em;margin-right:14px}""",
      """tl.fromTo(q("rr"), {strokeDashoffset:0}, {strokeDashoffset:1000, duration:3.0, ease:"none"}, T(7.39));
      (function(){ const c={n:5}, el=document.getElementById(ID+"-rn"); tl.fromTo(c,{n:5},{n:0,duration:3.0,ease:"none",onUpdate:function(){ el.textContent=Math.ceil(c.n); }},T(7.39)); })();
      tl.to(q("rr"), {stroke:"#E5372B", duration:0.2}, T(10.2));
      tl.fromTo(q("cur"), {opacity:0, x:-40, y:120}, {opacity:1, x:162, y:-268, duration:0.75, ease:"power2.inOut"}, T(8.3));
      tl.to(q("x"), {background:"#E5372B", color:"#fff", duration:0.12}, T(9.0)); tl.to(q("cur"), {scale:0.86, duration:0.08, yoyo:true, repeat:1}, T(9.0));
      tl.to([q("mw"), q("cur")], {opacity:0, scale:0.7, duration:0.3, ease:"power2.in"}, T(9.2));
      tl.to(q("rg"), {opacity:0, duration:0.3}, T(11.0)); __ft(q("h3"), {opacity:0, scale:1.15, filter:"blur(12px)"}, {opacity:1, scale:1, filter:"blur(0px)", duration:0.45, ease:"expo.out"}, T(11.27));""")
K.ac(9.0, "click", -24); K.ac(9.2, "swish", -30); K.ac(11.27, "pop", -26)

# ---------------------------------------------------------------- 02 (split) the three errors
K.stack("s02-tres", 12.01, 16.9, False, [("1", "Una web que tarda en cargar"), ("2", "Un texto que no se entiende"), ("3", "Se ve rota en el celular")],
        [12.14, 13.44, 14.92], solid=True, bad=[(0, 12.6), (1, 14.3), (2, 15.8)])
K.ac(12.14, "pop", -28); K.ac(13.44, "pop", -28); K.ac(14.92, "pop", -28)

# ---------------------------------------------------------------- 03 (split) "casi todo tu tráfico viene de celular"
PH = '<svg viewBox="0 0 24 24" width="58" height="58"><rect x="6" y="1.5" width="12" height="21" rx="2.6" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10.5,19 H13.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
PC = '<svg viewBox="0 0 24 24" width="58" height="58"><rect x="2" y="3" width="20" height="13" rx="1.8" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8,21 H16 M12,16 V21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
K.raw("s03-movil", 16.9, 19.5, False,
      """<div class="tt">¿Desde dónde entran a tu web?</div>
      <div class="br" style="top:170px"><i style="color:#FF7A1A">%s</i><span>Celular</span><div class="bb"><b id="{ID}-b0" style="background:#FF7A1A;box-shadow:0 0 40px rgba(255,122,26,.55)"></b></div></div>
      <div class="br" style="top:330px"><i style="color:#9A928A">%s</i><span>Computadora</span><div class="bb"><b id="{ID}-b1" style="background:#5A544E"></b></div></div>""" % (PH, PC),
      """.tt{position:absolute;left:0;right:0;top:40px;text-align:center;font-family:"HelvB",sans-serif;font-size:48px;letter-spacing:-.04em;color:#F2F0EC}
      .br{position:absolute;left:90px;width:900px;height:120px} .br i{position:absolute;left:0;top:30px} .br span{position:absolute;left:78px;top:8px;font-family:"HelvB",sans-serif;font-size:36px;color:#F2F0EC;letter-spacing:-.03em}
      .bb{position:absolute;left:78px;right:0;top:62px;height:44px;border-radius:22px;background:rgba(255,255,255,.08);overflow:hidden} .bb b{display:block;height:100%;width:0;border-radius:22px}""",
      """tl.fromTo(q("b0"), {width:"0%"}, {width:"88%", duration:0.9, ease:"power3.out"}, T(17.4)); tl.fromTo(q("b1"), {width:"0%"}, {width:"14%", duration:0.6, ease:"power3.out"}, T(17.6));""")
K.ac(17.4, "riser", -34); K.ac(18.4, "shine", -28)

# ---------------------------------------------------------------- 04 (split) "pensada para una computadora ... un cliente que ya no existe"
GHOST = '<svg viewBox="0 0 24 24" width="190" height="190"><circle cx="12" cy="7.6" r="4.3" fill="none" stroke="#9A928A" stroke-width="1.1" stroke-dasharray="1.6 1.2"/><path d="M3.2,22 C4.2,15.2 19.8,15.2 20.8,22" fill="none" stroke="#9A928A" stroke-width="1.1" stroke-dasharray="1.6 1.2"/></svg>'
K.raw("s04-pc", 19.5, 24.3974, False,
      """<div id="{ID}-pc" class="pc"><div class="scr"><div class="nav"><i></i><i></i><i></i><i></i></div><div class="hero"></div><div class="cols"><i></i><i></i><i></i></div></div><div class="ft"></div><div class="bs"></div></div>
      <div id="{ID}-gh" class="gh">%s</div><div id="{ID}-tg" class="tg">Este cliente ya no existe</div>""" % GHOST,
      """.pc{position:absolute;left:110px;top:40px;width:470px;height:420px} .scr{position:absolute;left:0;top:0;width:470px;height:300px;border-radius:18px;background:#F4F2EF;border:12px solid #2A2724;box-sizing:border-box;overflow:hidden}
      .nav{display:flex;gap:10px;padding:14px} .nav i{width:60px;height:12px;border-radius:6px;background:#D6D1CB} .hero{margin:0 14px;height:110px;border-radius:10px;background:linear-gradient(135deg,#FFB27A,#AE3C00)}
      .cols{display:flex;gap:10px;padding:12px 14px} .cols i{flex:1;height:54px;border-radius:8px;background:#E3E0DC}
      .ft{position:absolute;left:210px;top:300px;width:50px;height:70px;background:#2A2724} .bs{position:absolute;left:140px;top:366px;width:190px;height:16px;border-radius:8px;background:#2A2724}
      .gh{position:absolute;left:680px;top:90px;width:190px;height:190px;opacity:0}
      .tg{position:absolute;left:580px;top:320px;width:440px;padding:16px 0;border-radius:40px;background:#B3261E;color:#fff;text-align:center;font-family:"HelvB",sans-serif;font-size:32px;letter-spacing:-.03em;box-shadow:0 0 40px rgba(179,38,30,.55);opacity:0}""",
      """tl.fromTo(q("pc"), {opacity:0.0, y:20}, {opacity:1, y:0, duration:0.5, ease:"power2.out"}, T(20.9));
      tl.fromTo(q("gh"), {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.4}, T(22.84)); tl.to(q("gh"), {opacity:0.25, duration:0.8, ease:"power2.in"}, T(23.4));
      __ft(q("tg"), {opacity:0, scale:1.2}, {opacity:1, scale:1, duration:0.35, ease:"power3.out"}, T(23.5)); tl.to(q("pc"), {opacity:0.5, duration:0.4}, T(23.5));""")
K.ac(20.95, "pop", -28); K.ac(23.5, "impact", -30)

# ---------------------------------------------------------------- face 24.40-28.44: the test (pills under the caption)
for k, (tx, hot, t) in enumerate([("Abrí tu web en el celular", "", 25.41), ("Con datos móviles", "", 26.75), ("Contá hasta 5", "hot", 27.47)]):
    K.OF.append('<div id="pr%d" class="crow%s" style="top:%dpx">%s</div>' % (k, " hot" if hot else "", 1290 + k * 92, tx))
    K.ojs("opop('#pr%d', %s); oout('#pr%d', 28.3);" % (k, t, k)); K.ac(t, "pop" if not hot else "shine", -28 if not hot else -26)

# ---------------------------------------------------------------- 05 (split) 5 seconds on the phone: what do they sell, how do I buy, gone
K.raw("s05-test", 28.4431, 33.4481, False,
      """<div id="{ID}-ph" class="ph"><div class="psc"><div class="pn"></div><div class="ph1"></div><div class="ph2"></div><div class="ph3"></div><div id="{ID}-red" class="red">Cerró tu web</div></div></div>
      <div id="{ID}-ct" class="ct"><b id="{ID}-cn">5</b></div>
      <div id="{ID}-q0" class="qq" style="top:200px">¿Qué vende?</div><div id="{ID}-q1" class="qq" style="top:320px">¿Cómo compro?</div>""",
      """.ph{position:absolute;left:150px;top:10px;width:240px;height:470px;border-radius:44px;background:#111;padding:12px;box-sizing:border-box;box-shadow:0 30px 70px rgba(0,0,0,.65),0 0 0 3px #2A2724}
      .psc{position:relative;width:100%;height:100%;border-radius:34px;overflow:hidden;background:#F4F2EF}
      .pn{position:absolute;left:50%;top:10px;width:80px;height:22px;margin-left:-40px;border-radius:11px;background:#111}
      .ph1{position:absolute;left:-30px;top:60px;width:300px;height:110px;background:linear-gradient(135deg,#FFB27A,#AE3C00);transform:rotate(-4deg)}
      .ph2{position:absolute;left:20px;top:200px;width:320px;height:22px;border-radius:8px;background:#D6D1CB} .ph3{position:absolute;left:20px;top:240px;width:150px;height:150px;border-radius:12px;background:#E3E0DC}
      .red{position:absolute;inset:0;background:#B3261E;color:#fff;display:flex;align-items:center;justify-content:center;text-align:center;font-family:"HelvB",sans-serif;font-size:34px;letter-spacing:-.03em;opacity:0}
      .ct{position:absolute;left:470px;top:20px;width:150px;height:150px;border-radius:50%;background:#FF7A1A;display:flex;align-items:center;justify-content:center;box-shadow:0 0 50px rgba(255,122,26,.6)}
      .ct b{font-family:"HelvB",sans-serif;font-size:96px;line-height:1;color:#120C08;letter-spacing:-.05em}
      .qq{position:absolute;left:470px;width:480px;height:86px;border-radius:43px;background:#1B1917;border:3px solid rgba(255,255,255,.34);display:flex;align-items:center;justify-content:center;font-family:"HelvB",sans-serif;font-size:40px;color:#F2F0EC;letter-spacing:-.03em;opacity:0}""",
      """(function(){ const c={n:5}, el=document.getElementById(ID+"-cn"); tl.fromTo(c,{n:5},{n:1,duration:3.2,ease:"none",onUpdate:function(){ el.textContent=Math.ceil(c.n); }},T(29.0)); })();
      [29.64,30.44,31.24,32.04].forEach(function(t){ tl.fromTo(q("ct"), {scale:1.12}, {scale:1, duration:0.25, ease:"power2.out"}, T(t)); });
      tl.fromTo(q("q0"), {opacity:0, y:20}, {opacity:1, y:0, duration:0.35}, T(30.58)); tl.fromTo(q("q1"), {opacity:0, y:20}, {opacity:1, y:0, duration:0.35}, T(31.38));
      tl.to(q("red"), {opacity:1, duration:0.2}, T(32.36)); tl.to(q("ct"), {background:"#B3261E", boxShadow:"0 0 50px rgba(179,38,30,.6)", duration:0.2}, T(32.36)); tl.to(q("cn"), {color:"#fff", duration:0.2}, T(32.36));
      tl.to([q("q0"), q("q1")], {opacity:0.35, duration:0.3}, T(32.36));""")
K.ac(30.58, "pop", -28); K.ac(31.38, "pop", -28); K.ac(32.36, "impact", -28)

# ---------------------------------------------------------------- face 33.45-end: CTA, the DM arrives, then the checklist
K.OF.append(K.banner("X", 1290, "tu.cliente", "CINCO").replace("{ID}-nX", "dm1").replace("{ID}X", "dm1"))
K.ojs("opop('#dm1', 34.05); oout('#dm1', 34.85, 0.2);"); K.ac(34.05, "pop", -24)
CK = '<i>&#10003;</i>'
K.OF.append('<div id="cl" class="cl"><div class="ch">Checklist web</div><div class="cr">%sCarga en menos de 3 segundos</div><div class="cr">%sSe entiende en 5 segundos</div><div class="cr">%sSe ve perfecta en el celular</div></div>' % (CK, CK, CK))
K.ojs("opop('#cl', 34.91); " + " ".join("tl.fromTo('#cl .cr:nth-of-type(%d) i', {scale:0}, {scale:1, duration:0.25, ease:'back.out(2)'}, %s);" % (k + 2, 35.2 + k * 0.35) for k in range(3)))
K.ac(34.91, "shine", -26)

K.flush(""".ntm{font-size:0 !important} .ntm::after{content:"ahora";font-size:30px}
    .stop{position:absolute;left:420px;top:250px;width:240px;height:240px;opacity:0;display:flex;align-items:center;justify-content:center;background:#E5372B;clip-path:polygon(29% 0,71% 0,100% 29%,100% 71%,71% 100%,29% 100%,0 71%,0 29%);filter:drop-shadow(0 0 30px rgba(229,55,43,.7))}
    .stop b{font-family:"HelvB",sans-serif;font-size:66px;color:#fff;letter-spacing:-.03em}
    .tm{position:absolute;left:90px;top:300px;width:210px;height:210px;opacity:0} .tm svg{position:absolute;inset:0;filter:drop-shadow(0 0 18px rgba(255,122,26,.45))}
    .tm b{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:"HelvB",sans-serif;font-size:70px;color:#F2F0EC;letter-spacing:-.05em}
    .half{position:absolute;left:730px;top:300px;width:280px;height:210px;border-radius:40px;background:rgba(12,10,9,.92);border:3px solid rgba(229,55,43,.8);display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 0 40px rgba(229,55,43,.35);opacity:0}
    .half b{font-family:"HelvB",sans-serif;font-size:92px;line-height:1;color:#FF6B5E;letter-spacing:-.05em} .half span{font-family:"HelvB",sans-serif;font-size:30px;color:#F2F0EC;letter-spacing:-.03em;margin-top:8px}
    .crow{position:absolute;left:190px;width:700px;height:78px;border-radius:39px;background:rgba(12,10,9,.9);border:3px solid rgba(255,255,255,.45);display:flex;align-items:center;justify-content:center;font-family:"HelvB",sans-serif;font-size:38px;color:#F2F0EC;letter-spacing:-.03em;opacity:0}
    .crow.hot{background:#FF7A1A;border-color:#FF7A1A;color:#120C08;box-shadow:0 0 46px rgba(255,122,26,.55)}
    .cl{position:absolute;left:140px;top:1260px;width:800px;padding:26px 40px 30px;border-radius:40px;background:rgba(12,10,9,.92);border:3px solid rgba(255,122,26,.75);box-shadow:0 0 50px rgba(255,122,26,.3);box-sizing:border-box;opacity:0}
    .ch{font-family:"HelvB",sans-serif;font-size:32px;color:#FF7A1A;letter-spacing:.02em;text-transform:uppercase;margin-bottom:12px}
    .cr{display:flex;align-items:center;gap:20px;font-family:"HelvB",sans-serif;font-size:38px;color:#F2F0EC;letter-spacing:-.03em;margin-top:12px}
    .cr i{flex:none;width:46px;height:46px;border-radius:50%;background:#2FA65A;color:#06140B;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:28px;font-weight:700}""")
K.GL.clear()
import json; json.dump({"glides": [], "accents": sorted(K.AC), "dur": DUR}, open(os.path.join(ROOT, "sfx.json"), "w"))
E.build()
