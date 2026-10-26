#!/usr/bin/env python3
"""El error de las webs - Maison Enterprises (ES). YouTube Clips vertical style on the business-reel engine:
one-line 1-3 word captions (emphasis word in Playfair italic orange), three modes switching on cuts, few quiet SFX.
All times are GLOBAL seconds on the tight cut (cut.mp4, 38.91 s)."""
import os
import reel_engine as E
import kit as K

ROOT = os.path.dirname(os.path.abspath(__file__))
DUR = 38.91
FACE = [[0, 4.70], [9.25, 12.1], [27.4838, 29.62], [35.033, DUR]]
FULL = [[15.3467, 19.1421], [21.1024, 23.3964], [25.6486, 27.4838], [32.2385, 35.033]]
E.init(ROOT, DUR, FACE, FULL, caps="captions.json", title="El error de las webs")
GRN, RED, OR = "#2FA65A", "#B3261E", "#FF7A1A"
CHK = '<svg viewBox="0 0 40 40" width="%d" height="%d"><circle cx="20" cy="20" r="19" fill="#2FA65A"/><path d="M11,21 L17.5,27 L29,14" fill="none" stroke="#06140B" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
XX = '<svg viewBox="0 0 40 40" width="%d" height="%d"><circle cx="20" cy="20" r="19" fill="#B3261E"/><path d="M13,13 L27,27 M27,13 L13,27" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>'
PERSON = '<svg viewBox="0 0 40 48" width="%d" height="%d"><circle cx="20" cy="14" r="10" fill="currentColor"/><path d="M2,48 Q2,28 20,28 Q38,28 38,48 Z" fill="currentColor"/></svg>'
CURSOR = '<svg viewBox="0 0 32 40" width="64" height="80"><path d="M3,2 L3,32 L11,25 L17,38 L23,35 L17,22 L28,22 Z" fill="#fff" stroke="#120C08" stroke-width="2.5" stroke-linejoin="round"/></svg>'
BAR = '<div class="bbar"><i></i><i></i><i></i><span>%s</span></div>'
WINCSS = """.win{position:absolute;border-radius:30px;overflow:hidden;background:#F6F3EF;color:#141210;box-shadow:0 30px 70px rgba(0,0,0,.6);z-index:5;font-family:-apple-system,"HelvR",sans-serif}
    .bbar{height:58px;background:#E4DED7;display:flex;align-items:center;gap:12px;padding:0 22px} .bbar i{width:16px;height:16px;border-radius:50%;background:#C9C2BA}
    .bbar span{margin-left:16px;flex:1;height:34px;border-radius:17px;background:#F6F3EF;font-size:20px;color:#8A847E;display:flex;align-items:center;padding-left:18px}
    .nb1{position:absolute;width:84px;height:84px;border-radius:50%;background:#FF7A1A;color:#120C08;font-family:"HelvB";font-size:50px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 40px rgba(255,122,26,.6);z-index:8}"""

K.raw("s00", 0, 4.70, False, "", "", "")

# 01 (split) lo que hace la mayoría: "Bienvenidos a nuestra empresa" + foto del equipo
team = "".join('<span style="color:%s">%s</span>' % (c, PERSON % (74, 88)) for c in ("#B7A99A", "#A08E7C", "#C4B6A6", "#8F7D6B", "#B0A190"))
K.raw("s01-mayoria", 4.70, 9.25, False, """<div id="{ID}-w" class="win" style="left:110px;top:24px;width:860px;height:500px">""" + BAR % "tuempresa.com" + """
      <div class="nav"><b>LOGO</b><span>Inicio</span><span>Nosotros</span><span>Servicios</span><span>Contacto</span></div>
      <div id="{ID}-h" class="h1">Bienvenidos a nuestra empresa</div>
      <div id="{ID}-t" class="team">""" + team + """<em>Nuestro equipo</em></div></div>""",
    WINCSS + """.nav{display:flex;gap:26px;align-items:center;padding:18px 34px;font-size:22px;color:#6F6862} .nav b{font-family:"HelvB";color:#141210;margin-right:auto;letter-spacing:.08em}
    .h1{margin:26px 34px 0;font-family:"HelvB";font-size:52px;letter-spacing:-.04em;line-height:1.05;clip-path:inset(0 100% 0 0)}
    .team{position:absolute;left:34px;right:34px;bottom:30px;height:190px;border-radius:20px;background:linear-gradient(160deg,#EADFD3,#D4C2AF);display:flex;align-items:flex-end;justify-content:center;gap:6px;opacity:0;overflow:hidden}
    .team span{display:block;margin-bottom:-6px} .team em{position:absolute;left:20px;top:14px;font-style:normal;font-size:20px;color:#6F6862}""",
    """tl.fromTo(q("w"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(4.8));
    __ft(q("h"), {clipPath:"inset(0 100% 0 0)"}, {clipPath:"inset(0 0% 0 0)", duration:1.0, ease:"none"}, T(6.9));
    tl.fromTo(q("t"), {opacity:0, y:24}, {opacity:1, y:0, duration:0.45}, T(8.55));
    __tt(q("w"), {boxShadow:"0 0 0 6px #B3261E, 0 0 60px rgba(179,38,30,.55)", duration:0.3}, T(9.0));""")
K.ac(8.55, "pop", -25)

# 02 (split) al lector no le interesa tu empresa: le interesa lo que vos podés ofrecer
K.raw("s02-lector", 12.1, 15.3467, False, """<div id="{ID}-p0" class="lp2"><span>Tu empresa</span><i id="{ID}-x" class="sx2"></i><u>""" + XX % (54, 54) + """</u></div>
    <div id="{ID}-p1" class="lp2 ok"><span>Tu contenido</span><u>""" + CHK % (54, 54) + """</u></div>
    <div id="{ID}-p2" class="lp2 ok"><span>Lo que podés ofrecer</span><u>""" + CHK % (54, 54) + """</u></div>""",
    """.lp2{position:absolute;left:150px;width:780px;height:120px;border-radius:60px;background:rgba(18,16,14,.92);border:3px solid rgba(255,255,255,.4);display:flex;align-items:center;justify-content:center;font-family:"HelvB";font-size:52px;color:#F2F0EC;letter-spacing:-.04em;opacity:0;z-index:5;box-shadow:0 16px 40px rgba(0,0,0,.5)}
    .lp2 u{position:absolute;right:34px;top:33px;opacity:0} .lp2.ok{border-color:#2FA65A;box-shadow:0 0 40px rgba(47,166,90,.4)}
    #s02-lector-p0{top:60px} #s02-lector-p1{top:220px} #s02-lector-p2{top:380px}
    .sx2{position:absolute;left:150px;right:150px;top:50%;height:8px;margin-top:-4px;border-radius:4px;background:#B3261E;transform:scaleX(0);transform-origin:0 50%;box-shadow:0 0 14px rgba(179,38,30,.8)}""",
    """tl.fromTo(q("p0"), {opacity:0, y:24}, {opacity:1, y:0, duration:0.45}, T(12.12));
    __ft(q("x"), {scaleX:0}, {scaleX:1, duration:0.3, ease:"power2.out"}, T(12.6)); tl.to(q("p0") + " u", {opacity:1, duration:0.2}, T(12.6)); __tt(q("p0"), {opacity:0.45, duration:0.3}, T(12.9));
    tl.fromTo(q("p1"), {opacity:0, y:24}, {opacity:1, y:0, duration:0.45}, T(13.45)); tl.to(q("p1") + " u", {opacity:1, duration:0.2}, T(13.8));
    tl.fromTo(q("p2"), {opacity:0, y:24}, {opacity:1, y:0, duration:0.45}, T(14.35)); tl.to(q("p2") + " u", {opacity:1, duration:0.2}, T(14.7)); sweep(tl, "p2", 14.75);""")
K.ac(12.6, "impact", -31); K.ac(14.7, "shine", -25)

# 03 (FULL) una web que vende: 3 cosas en los primeros 5 segundos
K.raw("s03-cinco", 15.3467, 19.1421, True, """<div id="{ID}-hd" class="hd3">Una web que <em>vende</em></div>
    <div class="sl3">""" + "".join('<div id="{ID}-s%d" class="slot"><b>%d</b></div>' % (i, i + 1) for i in range(3)) + """</div>
    <div id="{ID}-tm" class="tm3"><svg width="300" height="300" viewBox="0 0 200 200"><circle cx="100" cy="100" r="84" fill="rgba(12,10,9,.9)" stroke="rgba(255,255,255,.2)" stroke-width="12"/>
      <circle id="{ID}-r" cx="100" cy="100" r="84" fill="none" stroke="#FF7A1A" stroke-width="12" stroke-linecap="round" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="0" transform="rotate(-90 100 100)"/></svg><b id="{ID}-n">5s</b></div>""",
    """.hd3{position:absolute;left:0;width:1080px;top:260px;text-align:center;font-family:"HelvB";font-size:84px;color:#F2F0EC;letter-spacing:-.05em;opacity:0}
    .hd3 em{font-family:"PlayIt";font-style:normal;color:#FF7A1A;font-size:100px}
    .sl3{position:absolute;left:150px;width:780px;top:430px;display:flex;justify-content:space-between}
    .slot{width:220px;height:220px;border-radius:40px;background:#16120F;border:3px dashed rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center;opacity:0}
    .slot b{font-family:"HelvB";font-size:110px;color:#FF7A1A;letter-spacing:-.05em}
    .tm3{position:absolute;left:390px;top:720px;width:300px;height:300px;opacity:0} .tm3 svg{position:absolute;inset:0;filter:drop-shadow(0 0 22px rgba(255,122,26,.45))}
    .tm3 b{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:"HelvB";font-size:100px;color:#F2F0EC;letter-spacing:-.05em}""",
    """tl.fromTo(q("hd"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(15.4));
    [0, 1, 2].forEach(function(i){ tl.fromTo(q("s" + i), {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.4, ease:"back.out(1.6)"}, T(17.1 + i * 0.16)); });
    tl.fromTo(q("tm"), {opacity:0, scale:0.85}, {opacity:1, scale:1, duration:0.4}, T(18.2));
    __ft(q("r"), {strokeDashoffset:0}, {strokeDashoffset:1000, duration:0.9, ease:"none"}, T(18.3));
    const c = {n:5}, el = document.getElementById(ID + "-n"); __ft(c, {n:5}, {n:0, duration:0.9, ease:"none", onUpdate:function(){ el.textContent = Math.ceil(c.n) + "s"; }}, T(18.3));""")
K.ac(15.4, "woosh", -25); K.ac(18.3, "riser", -33)

# 04 (split) 1 - muestra qué problema resuelve
K.raw("s04-uno", 19.1421, 21.1024, False, """<div id="{ID}-w" class="win" style="left:150px;top:40px;width:780px;height:460px">""" + BAR % "tuweb.com" + """
      <div class="hp"><small>Para dueños de negocio</small><div>Tu problema,<br/><em>resuelto.</em></div></div></div><div id="{ID}-b" class="nb1" style="left:110px;top:6px">1</div>
    <div id="{ID}-k" class="tg4">Qué problema resolvés</div>""",
    WINCSS + """.hp{padding:40px 50px} .hp small{font-size:26px;color:#8A847E} .hp div{margin-top:14px;font-family:"HelvB";font-size:76px;line-height:1;letter-spacing:-.05em} .hp em{font-family:"PlayIt";font-style:normal;color:#E0600C}
    .tg4{position:absolute;left:240px;top:430px;width:600px;height:80px;border-radius:40px;background:#FF7A1A;color:#120C08;display:flex;align-items:center;justify-content:center;font-family:"HelvB";font-size:38px;letter-spacing:-.03em;opacity:0;z-index:9;box-shadow:0 0 40px rgba(255,122,26,.5)}""",
    """tl.fromTo(q("w"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.45}, T(19.2)); tl.fromTo(q("b"), {opacity:0, scale:1.4}, {opacity:1, scale:1, duration:0.35}, T(19.3));
    tl.fromTo(q("k"), {opacity:0, y:20}, {opacity:1, y:0, duration:0.4}, T(19.75));""")
K.ac(19.3, "pop", -24)

# 05 (FULL) 2 - cómo lo resolvió en otras personas (prueba)
cards = "".join('<div id="{ID}-c%d" class="tc" style="top:%dpx"><span class="av">%s</span><div><b>&#9733;&#9733;&#9733;&#9733;&#9733;</b><i></i><i style="width:62%%"></i></div></div>'
                % (i, 470 + i * 190, PERSON % (54, 64)) for i in range(3))
K.raw("s05-dos", 21.1024, 23.3964, True, """<div id="{ID}-hd" class="hd5"><span class="nb1" style="position:relative;display:inline-flex;margin-right:22px;vertical-align:middle">2</span>Casos reales</div>""" + cards,
    WINCSS + """.hd5{position:absolute;left:0;width:1080px;top:300px;text-align:center;font-family:"HelvB";font-size:72px;color:#F2F0EC;letter-spacing:-.05em;opacity:0}
    .tc{position:absolute;left:170px;width:740px;height:160px;border-radius:34px;background:#16120F;border:2px solid rgba(255,255,255,.22);display:flex;align-items:center;gap:28px;padding:0 34px;box-sizing:border-box;opacity:0;box-shadow:0 18px 40px rgba(0,0,0,.5)}
    .av{width:96px;height:96px;border-radius:50%;background:#2A2420;color:#9A8572;display:flex;align-items:flex-end;justify-content:center;overflow:hidden;flex:none}
    .tc div{flex:1} .tc b{display:block;color:#FFB020;font-size:36px;letter-spacing:4px;margin-bottom:12px} .tc i{display:block;height:16px;border-radius:8px;background:rgba(255,255,255,.18);margin-top:10px}""",
    """tl.fromTo(q("hd"), {opacity:0, y:24}, {opacity:1, y:0, duration:0.45}, T(21.15));
    [0, 1, 2].forEach(function(i){ tl.fromTo(q("c" + i), {opacity:0, x:-60}, {opacity:1, x:0, duration:0.45, ease:"power3.out"}, T(21.7 + i * 0.3)); });""")

# 06 (split) 3 - te muestra qué hacer ahora: un botón, un clic
K.raw("s06-tres", 23.3964, 25.6486, False, """<div id="{ID}-b" class="nb1" style="left:190px;top:40px">3</div><div id="{ID}-hd" class="hd6">Qué hacer ahora</div>
    <div id="{ID}-btn" class="cta6">Agendá tu llamada &rarr;</div><div id="{ID}-cur" class="cur6">""" + CURSOR + "</div>",
    WINCSS + """.hd6{position:absolute;left:0;width:1080px;top:150px;text-align:center;font-family:"HelvB";font-size:64px;color:#F2F0EC;letter-spacing:-.05em;opacity:0}
    .cta6{position:absolute;left:190px;top:280px;width:700px;height:150px;border-radius:75px;background:#FF7A1A;color:#120C08;display:flex;align-items:center;justify-content:center;font-family:"HelvB";font-size:54px;letter-spacing:-.04em;opacity:0;box-shadow:0 0 60px rgba(255,122,26,.55);z-index:5}
    .cur6{position:absolute;left:760px;top:520px;opacity:0;z-index:7}""",
    """tl.fromTo(q("b"), {opacity:0, scale:1.4}, {opacity:1, scale:1, duration:0.35}, T(23.45)); tl.fromTo(q("hd"), {opacity:0, y:20}, {opacity:1, y:0, duration:0.4}, T(23.5));
    tl.fromTo(q("btn"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.45}, T(23.8));
    tl.fromTo(q("cur"), {opacity:0, x:120, y:120}, {opacity:1, x:0, y:0, duration:0.6, ease:"power2.out"}, T(24.25));
    __tt(q("btn"), {scale:0.94, duration:0.1, yoyo:true, repeat:1}, T(24.9)); sweep(tl, "btn", 24.95);""")
K.ac(24.9, "click", -24)

# 07 (FULL) un solo botón, no cinco
labs = ["Ver más", "Servicios", "Agendá tu llamada", "Contacto", "Nosotros"]
K.raw("s07-boton", 25.6486, 27.4838, True, "".join('<div id="{ID}-b%d" class="b7%s" style="top:%dpx">%s</div>' % (i, " hot" if i == 2 else "", 420 + i * 150, t) for i, t in enumerate(labs))
    + '<div id="{ID}-one" class="one7">1 botón</div>',
    """.b7{position:absolute;left:220px;width:640px;height:110px;border-radius:55px;background:#1B1917;border:3px solid rgba(255,255,255,.35);color:#F2F0EC;display:flex;align-items:center;justify-content:center;font-family:"HelvB";font-size:44px;letter-spacing:-.03em;opacity:0}
    .b7.hot{background:#FF7A1A;border-color:#FF7A1A;color:#120C08;box-shadow:0 0 50px rgba(255,122,26,.5)}
    .one7{position:absolute;left:0;width:1080px;top:270px;text-align:center;font-family:"PlayIt";font-size:110px;color:#FF7A1A;opacity:0;text-shadow:0 0 40px rgba(255,122,26,.5)}""",
    """[0, 1, 2, 3, 4].forEach(function(i){ tl.fromTo(q("b" + i), {opacity:0, y:20}, {opacity:1, y:0, duration:0.3}, T(25.7 + i * 0.09)); });
    [0, 1, 3, 4].forEach(function(i){ __tt(q("b" + i), {opacity:0, scale:0.9, filter:"blur(6px)", duration:0.35}, T(26.75)); });
    __tt(q("b2"), {y:-80, scale:1.12, duration:0.5, ease:"power3.out"}, T(26.85)); tl.fromTo(q("one"), {opacity:0, y:20}, {opacity:1, y:0, duration:0.4}, T(26.9));""")
K.ac(26.9, "shine", -25)

# 08 (split) las consultas se dispararon hasta 5 veces
K.raw("s08-x5", 29.62, 32.2385, False, """<div class="ch8"><div class="col"><div id="{ID}-a" class="bar8"></div><span>Antes</span></div><div class="col"><div id="{ID}-d" class="bar8 g"></div><span>Después</span></div>
      <div id="{ID}-x" class="x8">x5</div><div class="lb8">Consultas</div></div>""",
    """.ch8{position:absolute;left:190px;top:20px;width:700px;height:520px;z-index:5}
    .lb8{position:absolute;left:0;top:0;font-family:"HelvB";font-size:40px;color:#9A928A;letter-spacing:-.03em}
    .col{position:absolute;bottom:0;width:220px;height:460px;display:flex;flex-direction:column;justify-content:flex-end;align-items:center} .col:nth-child(1){left:40px} .col:nth-child(2){left:330px}
    .col span{margin-top:14px;font-family:"HelvB";font-size:36px;color:#F2F0EC;letter-spacing:-.03em}
    .bar8{width:180px;height:70px;border-radius:22px 22px 8px 8px;background:#3A3633;transform-origin:50% 100%;transform:scaleY(0)} .bar8.g{height:350px;background:linear-gradient(180deg,#FFB070,#FF7A1A);box-shadow:0 0 50px rgba(255,122,26,.5)}
    .x8{position:absolute;right:-10px;top:40px;font-family:"PlayIt";font-size:150px;color:#FF7A1A;opacity:0;text-shadow:0 0 40px rgba(255,122,26,.55)}""",
    """__ft(q("a"), {scaleY:0}, {scaleY:1, duration:0.4, ease:"power2.out"}, T(29.75));
    __ft(q("d"), {scaleY:0}, {scaleY:1, duration:1.0, ease:"power3.inOut"}, T(30.35));
    tl.fromTo(q("x"), {opacity:0, scale:1.4}, {opacity:1, scale:1, duration:0.35, ease:"power3.out"}, T(31.3));""")
K.ac(30.35, "riser", -32); K.ac(31.3, "impact", -29)

# 09 (FULL) sin invertir ni un peso más en publicidad
K.raw("s09-cero", 32.2385, 35.033, True, """<div id="{ID}-c" class="cd9"><span>Inversión extra en publicidad</span><b id="{ID}-n" class="de-num">$0</b></div>
    <div id="{ID}-g" class="g9">""" + CHK % (60, 60) + """<span>Solo cambió la web</span></div>""",
    """.cd9{position:absolute;left:150px;top:470px;width:780px;height:360px;border-radius:50px;background:#16120F;border:3px solid rgba(255,255,255,.35);display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0;box-shadow:0 20px 50px rgba(0,0,0,.5)}
    .cd9 span{font-family:"HelvB";font-size:38px;color:#9A928A;letter-spacing:-.03em} .cd9 b{font-size:190px;line-height:1.05;color:#F2F0EC;letter-spacing:-.05em}
    .g9{position:absolute;left:240px;top:880px;width:600px;height:100px;border-radius:50px;background:#2FA65A;color:#06140B;display:flex;align-items:center;justify-content:center;gap:18px;font-family:"HelvB";font-size:40px;letter-spacing:-.03em;opacity:0;box-shadow:0 0 46px rgba(47,166,90,.55)}
    .g9 svg circle{fill:#06140B} .g9 svg path{stroke:#2FA65A}""",
    """tl.fromTo(q("c"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.45}, T(32.3));
    __tt(q("n"), {color:"#7BE0A0", scale:1.08, duration:0.25, yoyo:true, repeat:1}, T(33.55));
    tl.fromTo(q("g"), {opacity:0, y:20}, {opacity:1, y:0, duration:0.4}, T(34.0));""")
K.ac(33.55, "pop", -24)

K.raw("s10", 35.033, DUR, False, "", "", "")

# ---------------------------------------------------------------- on the creator (above the head; captions under the chin)
K.hook("El 90% de las webs", "tiene el mismo problema", 4.55)
K.ac(0.15, "woosh", -26)
K.OF.append('<div id="rt" class="rtag"><i></i>Caso real &middot; cliente de Maison</div>')
K.ojs("opop('#rt', 28.5); oout('#rt', 29.55);")
K.OF.append(K.banner("X", 300, "tu.marca", "WEB").replace("{ID}-nX", "dm1").replace("{ID}X", "dm1"))
K.OF.append(K.banner("Y", 300, "Maison Enterprises", "Mandame tu web y la reviso &#128064;", me=True).replace("{ID}-nY", "dm2").replace("{ID}Y", "dm2"))
K.ojs("opop('#dm1', 36.9); oout('#dm1', 37.75, 0.2); opop('#dm2', 37.85);")
K.ac(36.9, "pop", -22); K.ac(37.85, "pop", -22)
K.GL.clear()      # sound only on the key moments above (no whoosh on every scene)
K.flush("""#hk2{background:#FF7A1A !important;color:#120C08 !important} .ntm{font-size:0 !important} .ntm::after{content:"ahora";font-size:30px}
    .cap-f span{top:1300px !important; font-size:70px !important}
    .cap-a span{top:1520px !important; font-size:66px !important}
    .cap .em{font-family:"PlayIt",serif;font-style:normal;font-weight:500;color:#FF7A1A;font-size:1.12em;letter-spacing:-.03em}
    .cap .nm{color:#FF7A1A}
    .rtag{position:absolute;left:230px;top:300px;width:620px;height:76px;border-radius:38px;background:rgba(12,10,9,.88);border:2px solid rgba(255,122,26,.7);display:flex;align-items:center;justify-content:center;gap:14px;font-family:"HelvB",sans-serif;font-size:34px;color:#F2F0EC;letter-spacing:-.03em;opacity:0}
    .rtag i{width:16px;height:16px;border-radius:50%;background:#2FA65A;box-shadow:0 0 12px #2FA65A}""")
E.build()
