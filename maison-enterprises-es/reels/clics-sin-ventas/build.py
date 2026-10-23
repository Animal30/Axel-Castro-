#!/usr/bin/env python3
"""Clics sin ventas - Maison Enterprises (ES), guion 1 de 6. Business Short Form reel.   python3 build.py
All times are GLOBAL seconds on the cut; switch times are exact frame times minus 2 ms (scripts/cut_times.py)."""
import os
import reel_engine as E
import kit as K

ROOT = os.path.dirname(os.path.abspath(__file__))
DUR = 60.185
FACE = [[0, 4.8362], [15.0964, 18.6416], [26.0657, 28.6516], [33.8652, 38.6616], [49.0053, 54.4691]]
FULL = [[11.1758, 15.0964], [23.7300, 26.0657], [38.6616, 42.1651]]
FIX = {"Mason": "Maison", "Majson": "Maison"}
# captions.json from phrases.txt (06_captions.py on words_cap.json)
E.init(ROOT, DUR, FACE, FULL, title="Clics sin ventas", words="words_cap.json",
       emph={"clics", "compra,", "compra", "creativo", "precio", "envío", "caro", "primero", "dólar"},
       keep={"Maison", "Enterprises"}, fix=FIX, hide=[])
GRN, RED, OR = "#2FA65A", "#B3261E", "#FF7A1A"
CART = '<svg viewBox="0 0 48 48" width="%d" height="%d"><path d="M4,8 H11 L16,32 H38 L43,15 H13" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="19" cy="40" r="3.6" fill="currentColor"/><circle cx="35" cy="40" r="3.6" fill="currentColor"/></svg>'
AD = '<svg viewBox="0 0 48 48" width="%d" height="%d"><path d="M6,19 V29 H13 L28,38 V10 L13,19 Z" fill="currentColor"/><path d="M34,17 Q39,24 34,31 M38,13 Q46,24 38,35" fill="none" stroke="currentColor" stroke-width="3.6" stroke-linecap="round"/></svg>'
PAGE = '<svg viewBox="0 0 48 48" width="%d" height="%d"><rect x="7" y="6" width="34" height="36" rx="5" fill="none" stroke="currentColor" stroke-width="4"/><rect x="13" y="12" width="22" height="12" rx="2" fill="currentColor"/><path d="M13,30 H35 M13,36 H27" stroke="currentColor" stroke-width="3.6" stroke-linecap="round"/></svg>'
CARD = '<svg viewBox="0 0 48 48" width="%d" height="%d"><rect x="4" y="11" width="40" height="27" rx="5" fill="none" stroke="currentColor" stroke-width="4"/><path d="M4,19 H44" stroke="currentColor" stroke-width="5"/><path d="M11,30 H21" stroke="currentColor" stroke-width="3.6" stroke-linecap="round"/></svg>'

K.raw("s00-open", 0, 4.6, False, "", "", "")

# 01 Tres pasos (split): la ruta de una venta. La línea se dibuja, un punto viaja; aparecen los 3 pasos y cada uno recibe su número
nodes = [(180, "1", "Anuncio", AD, "CTR"), (540, "2", "Página", PAGE, "% al carrito"), (900, "3", "Pago", CARD, "% de compra")]
nh = "".join('<div id="{ID}-n%d" class="nd" style="left:%dpx"><div class="nc"><span class="ni">%s</span><b>%s</b></div><div class="nl">%s</div><div id="{ID}-k%d" class="nk">%s</div></div>'
             % (i, x - 110, ic % (58, 58), n, lab, i, k) for i, (x, n, lab, ic, k) in enumerate(nodes))
K.raw("s01-ruta", 4.6, 11.1758, False, """<svg class="rt" width="1080" height="560" viewBox="0 0 1080 560">
      <path d="M60,250 H1020" stroke="rgba(255,255,255,.16)" stroke-width="10" stroke-linecap="round" stroke-dasharray="2 22"/>
      <path id="{ID}-ln" d="M60,250 H1020" stroke="#FF7A1A" stroke-width="10" stroke-linecap="round" fill="none" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="1000"/></svg>
    <i id="{ID}-dot" class="dot"></i>""" + nh,
    """.rt{position:absolute;left:0;top:0;z-index:3;filter:drop-shadow(0 0 14px rgba(255,122,26,.45))}
    .dot{position:absolute;left:36px;top:226px;width:48px;height:48px;border-radius:50%;background:#FFE2C8;box-shadow:0 0 40px 12px rgba(255,122,26,.8);z-index:6;opacity:0}
    .nd{position:absolute;top:120px;width:220px;display:flex;flex-direction:column;align-items:center;z-index:5;opacity:0}
    .nc{position:relative;width:200px;height:200px;border-radius:50%;background:#16120F;border:4px solid rgba(255,255,255,.5);display:flex;align-items:center;justify-content:center;color:#F2F0EC;box-shadow:0 20px 50px rgba(0,0,0,.6)}
    .nc b{position:absolute;right:-6px;top:-6px;width:66px;height:66px;border-radius:50%;background:#FF7A1A;color:#120C08;font-family:"HelvB";font-size:40px;display:flex;align-items:center;justify-content:center}
    .nl{margin-top:22px;font-family:"HelvB";font-size:44px;letter-spacing:-.04em}
    .nk{position:absolute;top:-92px;padding:12px 22px;border-radius:40px;background:#FF7A1A;color:#120C08;font-family:"HelvB";font-size:30px;letter-spacing:-.03em;white-space:nowrap;opacity:0;box-shadow:0 0 34px rgba(255,122,26,.55)}""",
    """__ft(q("ln"), {strokeDashoffset:1000}, {strokeDashoffset:0, duration:1.6, ease:"power2.inOut"}, T(4.95));
    __ft(q("dot"), {opacity:0}, {opacity:1, duration:0.2}, T(5.0)); __ft(q("dot"), {x:0}, {x:940, duration:2.2, ease:"power1.inOut"}, T(5.0)); __tt(q("dot"), {opacity:0, duration:0.25}, T(7.1));
    tl.fromTo(q("n0"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(7.94)); tl.fromTo(q("n1"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(8.44)); tl.fromTo(q("n2"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(8.8));
    tl.fromTo(q("k0"), {opacity:0, y:20}, {opacity:1, y:0, duration:0.4}, T(9.6)); tl.fromTo(q("k1"), {opacity:0, y:20}, {opacity:1, y:0, duration:0.4}, T(10.0)); tl.fromTo(q("k2"), {opacity:0, y:20}, {opacity:1, y:0, duration:0.4}, T(10.4));""")
K.ac(4.95, "woosh", -24); [K.ac(t, "pop", -25) for t in (7.4, 7.9, 8.25)]; [K.ac(t, "click", -26) for t in (9.1, 9.5, 9.9)]

# 02 Paso 1 (FULL): el anuncio en el feed y su CTR - menos del 1% hace clic
K.raw("s02-ctr", 11.1758, 15.0964, True, """<div id="{ID}-ad" class="adc"><div class="adh"><i></i><div><b>Tu marca</b><span>Publicidad</span></div></div><div class="adi">""" + AD % (150, 150) + """</div><div class="adb">Comprar ahora</div><em>1</em></div>
    <div id="{ID}-num" class="cnum de-num">0,0%</div><div id="{ID}-lab" class="de-label clab">HACE CLIC</div>
    <div id="{ID}-bar" class="cbar"><i id="{ID}-fill"></i><u></u><s>1%</s></div>""",
    """.adc{position:absolute;left:300px;top:250px;width:480px;height:520px;border-radius:34px;background:#121110;border:2px solid rgba(255,255,255,.2);box-shadow:0 30px 70px rgba(0,0,0,.6);overflow:visible;z-index:5;font-family:-apple-system,"HelvR",sans-serif}
    .adh{display:flex;align-items:center;gap:16px;padding:22px 26px} .adh i{width:58px;height:58px;border-radius:50%;background:linear-gradient(135deg,#FF7A1A,#7A3410)} .adh b{display:block;font-size:28px;color:#F2F0EC} .adh span{font-size:22px;color:#9A928A}
    .adi{height:300px;margin:0 26px;border-radius:20px;background:radial-gradient(80% 80% at 50% 30%,#3A2A1E,#17120E);display:flex;align-items:center;justify-content:center;color:#FF7A1A}
    .adb{margin:22px 26px;height:62px;border-radius:14px;background:#2A2725;color:#F2F0EC;font-family:"HelvB";font-size:28px;display:flex;align-items:center;justify-content:center}
    .adc em{position:absolute;left:-30px;top:-30px;width:84px;height:84px;border-radius:50%;background:#FF7A1A;color:#120C08;font-style:normal;font-family:"HelvB";font-size:52px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 40px rgba(255,122,26,.6)}
    .cnum{position:absolute;left:0;width:1080px;top:820px;text-align:center;font-size:130px;line-height:1;color:#F2F0EC;opacity:0;z-index:5}
    .clab{position:absolute;left:0;width:1080px;top:960px;text-align:center;font-size:28px;opacity:0}
    .cbar{position:absolute;left:190px;top:1030px;width:700px;height:26px;border-radius:13px;background:rgba(255,255,255,.14);opacity:0;z-index:5}
    .cbar i{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:13px;background:#B3261E;box-shadow:0 0 24px rgba(179,38,30,.8)}
    .cbar u{position:absolute;left:560px;top:-18px;width:6px;height:62px;border-radius:3px;background:#2FA65A;box-shadow:0 0 18px rgba(47,166,90,.8)}
    .cbar s{position:absolute;left:530px;top:-64px;text-decoration:none;font-family:"HelvB";font-size:34px;color:#7BE0A0}""",
    """tl.fromTo(q("ad"), {opacity:0, y:40}, {opacity:1, y:0, duration:0.5}, T(11.0));
    tl.fromTo(q("num"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(12.75)); tl.fromTo(q("lab"), {opacity:0}, {opacity:1, duration:0.5}, T(13.0)); tl.fromTo(q("bar"), {opacity:0}, {opacity:1, duration:0.5}, T(12.9));
    const n = {v:0}, el = document.getElementById(ID+"-num"), f = document.getElementById(ID+"-fill");
    __ft(n, {v:0}, {v:0.8, duration:1.3, ease:"power2.inOut", onUpdate:function(){ el.textContent = n.v.toFixed(1).replace(".", ",") + "%"; f.style.width = (n.v / 1.25 * 700).toFixed(1) + "px"; el.style.color = n.v > 0.79 ? "#FF8A80" : "#F2F0EC"; }}, T(13.25));
    __tt(q("ad"), {borderColor:"#B3261E", boxShadow:"0 0 60px rgba(179,38,30,.55)", duration:0.4}, T(14.6));""")
K.ac(11.25, "swoosh", -24); K.ac(13.25, "riser", -30); K.ac(14.6, "impact", -30)

# 03 Paso 2 (split): la página del producto - muchas visitas, cero al carrito
K.raw("s03-pagina", 15.0964, 23.73, False, """<div id="{ID}-pg" class="pg"><div class="pgi"><div class="bx"></div></div><div class="pgt">Producto estrella</div><div class="pgs">&#9733;&#9733;&#9733;&#9733;&#9734; <span>(12)</span></div><div class="pgp">$49</div>
      <div id="{ID}-btn" class="pgb">""" + CART % (34, 34) + """ Agregar al carrito</div><em>2</em></div>
    <div id="{ID}-v" class="st"><span>Visitas</span><b id="{ID}-vn" class="de-num">0</b></div>
    <div id="{ID}-c" class="st"><span>Al carrito</span><b id="{ID}-cn" class="de-num">0</b></div>""",
    """.pg{position:absolute;left:90px;top:20px;width:420px;height:520px;border-radius:30px;background:#F6F3EF;color:#141210;box-shadow:0 30px 70px rgba(0,0,0,.6);z-index:5;font-family:-apple-system,"HelvR",sans-serif;opacity:0}
    .pgi{height:230px;margin:18px;border-radius:18px;background:linear-gradient(160deg,#EADFD3,#D4C2AF);display:flex;align-items:center;justify-content:center}
    .bx{width:120px;height:150px;border-radius:22px 22px 14px 14px;background:linear-gradient(180deg,#FF9A4A,#E0600C);box-shadow:0 18px 30px rgba(120,50,0,.35)}
    .pgt{margin:0 24px;font-size:32px;font-weight:700} .pgs{margin:6px 24px;font-size:28px;color:#E0A100} .pgs span{color:#8A847E;font-size:22px} .pgp{margin:4px 24px;font-size:38px;font-weight:800}
    .pgb{position:absolute;left:24px;right:24px;bottom:22px;height:66px;border-radius:33px;background:#FF7A1A;color:#120C08;display:flex;align-items:center;justify-content:center;gap:10px;font-family:"HelvB";font-size:28px}
    .pg em{position:absolute;left:-26px;top:-20px;width:76px;height:76px;border-radius:50%;background:#FF7A1A;color:#120C08;font-style:normal;font-family:"HelvB";font-size:46px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 40px rgba(255,122,26,.6)}
    .st{position:absolute;left:570px;width:420px;height:200px;border-radius:40px;background:#1B1917;border:3px solid rgba(255,255,255,.34);box-shadow:0 14px 34px rgba(0,0,0,.5);display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:5;opacity:0}
    #s03-pagina-v{top:60px} #s03-pagina-c{top:300px}
    .st span{font-family:"HelvB";font-size:34px;color:#9A928A;letter-spacing:-.03em} .st b{font-size:96px;line-height:1.05;color:#F2F0EC}""",
    """tl.fromTo(q("pg"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(18.7));
    tl.fromTo(q("v"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(20.95)); tl.fromTo(q("c"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(22.3));
    const n = {v:0}, el = document.getElementById(ID+"-vn");
    __ft(n, {v:0}, {v:1248, duration:1.2, ease:"power2.inOut", onUpdate:function(){ el.textContent = Math.round(n.v).toLocaleString("es-AR"); el.style.color = n.v > 1240 ? "#7BE0A0" : "#F2F0EC"; }}, T(21.05));
    __tt(q("c"), {borderColor:"#B3261E", boxShadow:"0 0 50px rgba(179,38,30,.6)", duration:0.3}, T(22.65)); __tt(q("cn"), {color:"#FF8A80", duration:0.3}, T(22.65));
    __tt(q("btn"), {scale:0.94, duration:0.12, yoyo:true, repeat:3}, T(22.7)); __tt(q("btn"), {backgroundColor:"#C9C2BA", duration:0.3}, T(23.1));""")
K.ac(18.7, "swoosh", -24); K.ac(21.05, "riser", -32); K.ac(22.65, "impact", -31)

# 04 (FULL) el anuncio hizo su trabajo / lo que falla es la página
OK = '<svg viewBox="0 0 40 40" width="64" height="64"><circle cx="20" cy="20" r="19" fill="#2FA65A"/><path d="M11,21 L17.5,27 L29,14" fill="none" stroke="#06140B" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
NO = '<svg viewBox="0 0 40 40" width="64" height="64"><circle cx="20" cy="20" r="19" fill="#B3261E"/><path d="M13,13 L27,27 M27,13 L13,27" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>'
K.stack("s04-falla", 23.73, 26.0657, True, [(OK, "El anuncio"), (NO, "La página")], [23.5, 25.25], good=[(0, 24.3)], bad=[(1, 25.6)])
K.ac(24.3, "shine", -24); K.ac(25.6, "impact", -31)

# 05 Paso 3 (split): el pago - el ticket, y la sorpresa al final (envío caro)
K.raw("s05-pago", 26.0657, 33.8652, False, """<div id="{ID}-tk" class="tk"><div class="tkh">""" + CART % (40, 40) + """<b>Tu carrito</b><em>3</em></div>
      <div id="{ID}-r0" class="tr"><span>Producto estrella</span><b>$49</b></div>
      <div id="{ID}-r1" class="tr"><span>Subtotal</span><b>$49</b></div>
      <div id="{ID}-r2" class="tr bad"><span>Envío</span><b>+ $18</b></div>
      <div class="tt"><span>Total</span><b id="{ID}-tot">$49</b></div>
      <div id="{ID}-pay" class="tpay">Pagar</div></div>""",
    """.tk{position:absolute;left:220px;top:6px;width:640px;height:540px;border-radius:34px;background:#141210;border:2px solid rgba(255,255,255,.22);box-shadow:0 30px 70px rgba(0,0,0,.6);z-index:5;padding:26px 40px;box-sizing:border-box;opacity:0}
    .tkh{position:relative;display:flex;align-items:center;gap:16px;color:#F2F0EC;font-family:"HelvB";font-size:40px;letter-spacing:-.03em;margin-bottom:18px}
    .tkh em{position:absolute;right:-70px;top:-50px;width:76px;height:76px;border-radius:50%;background:#FF7A1A;color:#120C08;font-style:normal;font-size:46px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 40px rgba(255,122,26,.6)}
    .tr,.tt{display:flex;justify-content:space-between;align-items:center;height:76px;border-bottom:2px solid rgba(255,255,255,.1);font-family:"HelvR";font-size:36px;color:#C9C2BA}
    .tr b,.tt b{font-family:"HelvB";color:#F2F0EC} .tr{opacity:0} .tr.bad{border-radius:16px;padding:0 16px;margin:0 -16px}
    .tt{border-bottom:none;font-family:"HelvB";font-size:42px;color:#F2F0EC} .tt b{font-size:52px}
    .tpay{margin-top:14px;height:72px;border-radius:36px;background:#FF7A1A;color:#120C08;font-family:"HelvB";font-size:34px;display:flex;align-items:center;justify-content:center}""",
    """tl.fromTo(q("tk"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(28.7));
    tl.fromTo(q("r0"), {opacity:0, x:-30}, {opacity:1, x:0, duration:0.5}, T(30.3)); tl.fromTo(q("r1"), {opacity:0, x:-30}, {opacity:1, x:0, duration:0.5}, T(30.75));
    __tt(q("pay"), {backgroundColor:"#3A3633", color:"#8A847E", duration:0.35}, T(31.55));
    __ft(q("r2"), {opacity:0, scale:1.25}, {opacity:1, scale:1, duration:0.35, ease:"power3.out"}, T(32.75)); __tt(q("r2"), {backgroundColor:"rgba(179,38,30,.35)", color:"#FFB0A8", duration:0.3}, T(32.8));
    __ft(q("r2"), {x:-10}, {x:10, duration:0.06, yoyo:true, repeat:5, ease:"none"}, T(33.0)); __tt(q("r2"), {x:0, duration:0.05}, T(33.36));
    const n = {v:49}, el = document.getElementById(ID+"-tot");
    __ft(n, {v:49}, {v:67, duration:0.5, ease:"power2.out", onUpdate:function(){ el.textContent = "$" + Math.round(n.v); el.style.color = n.v > 66 ? "#FF8A80" : "#F2F0EC"; }}, T(33.1));""")
K.ac(28.7, "swoosh", -24); [K.ac(t, "click", -27) for t in (29.75, 30.2)]; K.ac(32.75, "impact", -29)

# 06 (FULL) encontrá el paso donde se cae la venta y solucioná solo ese
K.stack("s06-arreglo", 33.8652, 42.1651, True, [(AD % (64, 64), "Anuncio"), (PAGE % (64, 64), "Página"), (CARD % (64, 64), "Pago")], [38.3, 38.4, 38.5],
        solid=True, bad=[(2, 39.85)], good=[(2, 40.75)], dim=[([0, 1], 41.2)])
K.ac(38.7, "woosh", -24); K.ac(39.85, "impact", -31); K.ac(40.75, "shine", -23)

# 07 (split) cambiar el anuncio cuando el problema está en el checkout = pagar más por más tráfico
vers = "".join('<div id="{ID}-a%d" class="av"><div class="avi">%s</div><b>Anuncio v%d</b></div>' % (i, AD % (110, 110), i + 1) for i in range(3))
K.raw("s07-trafico", 42.1651, 49.0053, False, '<div class="avw">' + vers + """</div>
    <div id="{ID}-m" class="mon"><span>Gastado en anuncios</span><b id="{ID}-mn" class="de-num">$500</b></div>
    <div id="{ID}-ck" class="ckp">""" + CARD % (46, 46) + """ Checkout <i>&#10007;</i></div>""",
    """.avw{position:absolute;left:90px;top:40px;width:380px;height:440px;z-index:5}
    .av{position:absolute;inset:0;border-radius:30px;background:#141210;border:2px solid rgba(255,255,255,.25);box-shadow:0 26px 60px rgba(0,0,0,.6);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;opacity:0;color:#FF7A1A}
    .avi{width:240px;height:240px;border-radius:22px;background:radial-gradient(80% 80% at 50% 30%,#3A2A1E,#17120E);display:flex;align-items:center;justify-content:center} .av b{font-family:"HelvB";font-size:40px;color:#F2F0EC;letter-spacing:-.03em}
    .mon{position:absolute;left:540px;top:40px;width:450px;height:230px;border-radius:40px;background:#1B1917;border:3px solid rgba(255,255,255,.34);display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:5;opacity:0}
    .mon span{font-family:"HelvB";font-size:32px;color:#9A928A;letter-spacing:-.03em} .mon b{font-size:100px;line-height:1.05;color:#F2F0EC}
    .ckp{position:absolute;left:540px;top:310px;width:450px;height:150px;border-radius:75px;background:#1B1917;border:3px solid #B3261E;box-shadow:0 0 50px rgba(179,38,30,.55);display:flex;align-items:center;justify-content:center;gap:16px;font-family:"HelvB";font-size:44px;color:#F2F0EC;z-index:5;opacity:0}
    .ckp i{font-style:normal;color:#FF8A80}""",
    """__ft(q("a0"), {opacity:0, rotationY:-70}, {opacity:1, rotationY:0, duration:0.45, ease:"power3.out"}, T(42.25));
    __tt(q("a0"), {opacity:0, rotationY:70, duration:0.3}, T(42.95)); __ft(q("a1"), {opacity:0, rotationY:-70}, {opacity:1, rotationY:0, duration:0.35, ease:"power3.out"}, T(43.05));
    __tt(q("a1"), {opacity:0, rotationY:70, duration:0.3}, T(43.6)); __ft(q("a2"), {opacity:0, rotationY:-70}, {opacity:1, rotationY:0, duration:0.35, ease:"power3.out"}, T(43.7));
    tl.fromTo(q("ck"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(44.4));
    tl.fromTo(q("m"), {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, T(45.3));
    const n = {v:500}, el = document.getElementById(ID+"-mn");
    __ft(n, {v:500}, {v:1500, duration:1.4, ease:"power2.inOut", onUpdate:function(){ el.textContent = "$" + Math.round(n.v).toLocaleString("es-AR"); el.style.color = n.v > 1490 ? "#FF8A80" : "#F2F0EC"; }}, T(45.4));
    __tt(q("m"), {borderColor:"#B3261E", boxShadow:"0 0 50px rgba(179,38,30,.55)", duration:0.3}, T(46.8));
    __tt(q("ck"), {scale:1.06, duration:0.3, yoyo:true, repeat:1}, T(47.9)); sweep(tl, "ck", 47.95);
    [42.25, 43.05, 43.7].forEach(function(){});""")
K.ac(42.25, "swish", -25); K.ac(43.05, "swish", -27); K.ac(43.7, "swish", -27); K.ac(44.4, "impact", -32); K.ac(45.4, "riser", -32); K.ac(47.95, "shine", -24)

# 08 (split) CTA: escribinos EMBUDO por DM - la palabra grande y el DM que llega con la plantilla
b1 = K.banner("a", 170, "sofi.emprende", "EMBUDO")
b2 = K.banner("b", 170, "Maison Enterprises", "Acá tenés tu plantilla del embudo &#128202;", me=True)
K.raw("s08-cta", 49.0053, DUR, False, '<div id="{ID}-kw" class="kw2"><span>escribinos</span><em>embudo</em></div>' + (b1 + b2).replace(">now<", ">ahora<"),
    K.NBCSS + """.kw2{position:absolute;left:0;width:1080px;top:6px;text-align:center;z-index:6;opacity:0} .kw2 span{display:block;font-family:"HelvB";font-size:40px;color:#F2F0EC;letter-spacing:-.03em}
    .kw2 em{display:block;font-family:"PlayIt";font-style:normal;font-size:112px;line-height:1;color:#FF7A1A;letter-spacing:-.04em;text-shadow:0 0 40px rgba(255,122,26,.5)}""",
    K.NJS + """tl.fromTo(q("kw"), {opacity:0, y:20}, {opacity:1, y:0, duration:0.5}, T(55.2));
    drop("a", 56.0); __tt(q("kw"), {opacity:0, duration:0.3}, T(57.0)); drop("b", 57.55); push(["a"], 57.55, 1);""")
K.ac(55.2, "shine", -24); K.ac(56.0, "pop", -22); K.ac(57.55, "pop", -21)

# ---------------------------------------------------------------- on the creator (FACE windows)
K.hook("Si tu anuncio tiene clics", "pero nadie compra", 4.55)
# opening: a mini Ads dashboard under the chin - clics ticking up green, compras stuck at 0 red
K.OF.append('<div id="dash" class="dash"><div class="dc"><span>Clics</span><b id="dclk" class="de-num">0</b></div><div class="dsep"></div><div class="dc" id="dbuy"><span>Compras</span><b class="de-num">0</b></div></div>')
K.ojs("opop('#dash', 0.6); oout('#dash', 4.5); (function(){ const c={n:0}, el=$o('#dclk'); tl.fromTo(c,{n:0},{n:2431,duration:1.0,ease:'power2.inOut',onUpdate:function(){ el.textContent=Math.round(c.n).toLocaleString('es-AR'); }},1.1); })(); tl.to('#dclk', {color:'#7BE0A0', duration:0.3}, 2.05);"
      " tl.to('#dbuy', {borderColor:'#B3261E', backgroundColor:'rgba(179,38,30,.28)', duration:0.3}, 2.45); tl.to('#dbuy b', {color:'#FF8A80', duration:0.3}, 2.45);")
K.ac(0.6, "woosh", -24); K.ac(1.1, "riser", -33); K.ac(2.45, "impact", -31)
K.lps("cre", 18.6, [("Ahí sí: cambiá el creativo", "hot", 17.5)]); K.ac(17.5, "pop", -24)
K.lps("pg", 28.6, [("La imagen", "red", 26.2), ("Las reseñas", "red", 26.75), ("El precio", "red", 27.65)]); [K.ac(t, "pop", -25) for t in (26.2, 26.75, 27.65)]
K.lps("env", 38.6, [("Envío caro = razón #1", "red", 35.6)]); K.ac(35.6, "pop", -24)
K.OF.append('<div id="mlogo" class="mlogo"><img src="assets/proof/maison-lockup.png"/></div>')
K.ojs("opop('#mlogo', 49.15); oout('#mlogo', 54.4);"); K.ac(49.15, "shine", -23)
K.lps("rev", 54.4, [("1° revisamos el embudo", "green", 51.0)]); K.ac(51.0, "pop", -24)
K.flush("""#hk2{background:#FF7A1A !important;color:#120C08 !important}
    .dash{position:absolute;left:150px;top:1190px;width:780px;height:170px;display:flex;align-items:center;gap:24px;opacity:0}
    .dc{flex:1;height:170px;border-radius:40px;background:rgba(12,10,9,.9);border:3px solid rgba(255,255,255,.45);display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 14px 34px rgba(0,0,0,.5)}
    .dc span{font-family:"HelvB",sans-serif;font-size:32px;color:#C9C2BA;letter-spacing:-.03em} .dc b{font-family:"HelvB",sans-serif;font-size:80px;line-height:1.05;color:#F2F0EC}
    .dsep{display:none}
    .mlogo{position:absolute;left:220px;top:1300px;width:640px;padding:22px 40px;box-sizing:border-box;border-radius:36px;background:rgba(5,5,5,.88);border:2px solid rgba(255,122,26,.55);box-shadow:0 0 40px rgba(255,122,26,.3),0 14px 34px rgba(0,0,0,.6);opacity:0} .mlogo img{width:100%;display:block}
    #rev0{top:1200px}""")
E.build()
