#!/usr/bin/env python3
"""Instagram no es tu negocio (video "deja de promocionar") - Maison Enterprises (ES). Depth UI reel, no Maison logo anywhere.
Times are seconds on the tight cut (~/reel-work/promo/cut.mp4, 37.87 s)."""
import json, os, sys
ROOT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ROOT)
import depth_engine as D
DUR = 37.87
W = json.load(open(os.path.join(ROOT, "words.json")))
for w in W:
    if w[2] == "diez": w[2] = "10"
    w[2] = w[2].replace(":", "").replace("¿", "").replace("?", "")
D.init(ROOT, W, DUR, fps="24000/1001", title="Instagram no es tu negocio", emph={"alquilado", "desaparece", "propio", "reales"})
print("captions:", " | ".join(D.captions()))
RL = lambda ns: [f"assets/reels/r{n:02d}.jpg" for n in ns]
G, R, A = D.GREEN, D.RED, D.ACCENT
IG = ('<svg viewBox="0 0 48 48" width="%d" height="%d"><defs><radialGradient id="igG%s" cx="30%%" cy="107%%" r="150%%"><stop offset="0" stop-color="#FEDA75"/><stop offset=".25" stop-color="#FA7E1E"/>'
      '<stop offset=".5" stop-color="#D62976"/><stop offset=".75" stop-color="#962FBF"/><stop offset="1" stop-color="#4F5BD5"/></radialGradient></defs><rect x="2" y="2" width="44" height="44" rx="12" fill="url(#igG%s)"/>'
      '<rect x="12" y="12" width="24" height="24" rx="7" fill="none" stroke="#fff" stroke-width="3.4"/><circle cx="24" cy="24" r="5.6" fill="none" stroke="#fff" stroke-width="3.4"/><circle cx="32.6" cy="15.4" r="2" fill="#fff"/></svg>')
ig = lambda s, u: IG % (s, s, u, u)
CHK = '<svg viewBox="0 0 40 40" width="%d" height="%d"><circle cx="20" cy="20" r="19" fill="#2FA65A"/><path d="M11,21 L17.5,27 L29,14" fill="none" stroke="#06140B" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
XX = '<svg viewBox="0 0 40 40" width="%d" height="%d"><circle cx="20" cy="20" r="19" fill="#E5372B"/><path d="M13,13 L27,27 M27,13 L13,27" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>'
LOCK = '<svg viewBox="0 0 24 24" width="26" height="26"><rect x="5" y="10" width="14" height="10" rx="2" fill="#2FA65A"/><path d="M8,10 V7 A4,4 0 0 1 16,7 V10" fill="none" stroke="#2FA65A" stroke-width="2.4"/></svg>'
HOUSE = '<svg viewBox="0 0 48 48" width="%d" height="%d"><path d="M6,22 L24,7 L42,22 V42 H6 Z" fill="none" stroke="currentColor" stroke-width="3.6" stroke-linejoin="round"/><rect x="19" y="28" width="10" height="14" rx="1.5" fill="currentColor"/></svg>'
ICO = {
 "mail": '<svg viewBox="0 0 48 48" width="58" height="58"><rect x="5" y="10" width="38" height="28" rx="6" fill="none" stroke="currentColor" stroke-width="3.6"/><path d="M8,14 L24,27 L40,14" fill="none" stroke="currentColor" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "grid": '<svg viewBox="0 0 48 48" width="58" height="58"><rect x="6" y="6" width="15" height="15" rx="3" fill="currentColor"/><rect x="27" y="6" width="15" height="15" rx="3" fill="currentColor"/><rect x="6" y="27" width="15" height="15" rx="3" fill="currentColor"/><rect x="27" y="27" width="15" height="15" rx="3" fill="currentColor"/></svg>',
 "card": '<svg viewBox="0 0 48 48" width="58" height="58"><rect x="4" y="11" width="40" height="27" rx="5" fill="none" stroke="currentColor" stroke-width="3.6"/><path d="M4,19 H44" stroke="currentColor" stroke-width="5"/><path d="M11,30 H21" stroke="currentColor" stroke-width="3.6" stroke-linecap="round"/></svg>'}
NB = lambda i, top, ttl, body, icon: (f'<div id="{i}" class="nb" style="top:{top}px"><div class="nbi">{icon}</div><div class="nbt"><b>{ttl}</b><span>{body}</span></div><em>ahora</em></div>')
D.css(""".nb{left:80px;width:920px;height:150px;border-radius:44px;background:rgba(36,36,40,.9);-webkit-backdrop-filter:blur(30px);backdrop-filter:blur(30px);border:1px solid rgba(255,255,255,.14);box-shadow:0 24px 60px rgba(0,0,0,.55);display:flex;align-items:center;gap:26px;padding:0 34px;box-sizing:border-box;opacity:0}
 .nbi{width:84px;height:84px;flex:none;display:flex;align-items:center;justify-content:center} .nbt{flex:1;line-height:1.2} .nbt b{display:block;font-size:34px;font-weight:600;letter-spacing:-.03em} .nbt span{display:block;font-size:32px;color:#e2e2e2;font-weight:500;letter-spacing:-.02em}
 .nb em{position:absolute;right:34px;top:30px;font-style:normal;font-size:26px;color:#9a9a9a}
 .card{left:150px;width:780px;border-radius:36px;background:rgba(15,15,15,.94);border:1.5px solid rgba(255,255,255,.14);box-shadow:0 18px 50px rgba(0,0,0,.55);opacity:0;box-sizing:border-box}
 .pill{height:84px;border-radius:42px;padding:0 34px;display:flex;align-items:center;gap:16px;font-family:"HelvB",sans-serif;font-size:36px;letter-spacing:-.03em;box-sizing:border-box;opacity:0}""")

# camera: step on the sentence cuts
D.camera([(0, 4.8, 1.0, 1.035), (4.8, 9.716, 1.075, 1.095), (9.716, 12.093, 1.0, 1.02), (12.093, 18.391, 1.08, 1.10), (18.391, 21.3, 1.0, 1.03),
          (21.3, 27.734, 1.07, 1.09), (27.734, 32.614, 1.0, 1.035), (32.614, DUR, 1.08, 1.10)])

# 1  "10 mil seguidores y no tener un sitio web ... terreno alquilado": Instagram profile card on the chest, link row turns red, a 'Alquilado' sign behind
D.front(f'<div id="pf" class="card" style="top:1270px;height:220px;padding:26px 32px"><div class="pfr"><div class="pav">{ig(96, "a")}</div>'
        '<div class="pst"><div><b id="pf-n">0</b><span>seguidores</span></div><div><b>312</b><span>publicaciones</span></div></div></div>'
        f'<div id="pf-l" class="pfl"><span>&#128279; Sitio web</span><i>no tiene</i>{XX % (40, 40)}</div></div>')
D.css(""".pfr{display:flex;align-items:center;gap:40px} .pav{width:110px;height:110px;border-radius:50%;background:#1d1d1d;display:flex;align-items:center;justify-content:center;border:3px solid rgba(255,255,255,.2)}
 .pst{display:flex;gap:60px} .pst div{text-align:center} .pst b{display:block;font-family:"HelvB",sans-serif;font-size:56px;letter-spacing:-.05em;line-height:1} .pst span{font-size:24px;color:#a8a8a8}
 .pfl{margin-top:18px;height:56px;border-radius:16px;background:#1f1f1f;display:flex;align-items:center;gap:16px;padding:0 18px;font-size:28px;color:#dcdcdc;opacity:.35}
 .pfl i{font-style:normal;color:#ff8f86;margin-left:auto} .pfl svg{opacity:0}""")
D.blur_in("#pf", 0.1, y=60, d=0.4, b=18)
D.js("(function(){const c={n:0}, el=document.querySelector('#pf-n'); tl.fromTo(c,{n:0},{n:10000,duration:1.0,ease:'power2.out',onUpdate:function(){el.textContent=Math.round(c.n).toLocaleString('es-AR');}},0.35);})();")
D.js(f"tl.to('#pf-l', {{opacity:1, background:'rgba(229,55,43,.28)', duration:0.3}}, 1.55); tl.to('#pf-l svg', {{opacity:1, duration:0.2}}, 1.6);")
D.shake("#pf-l", 1.7); D.blur_out("#pf", 3.2, y=80, d=0.3)
D.ev("pf", "graphic", 0.1, 3.5, "Instagram profile card: 10.000 seguidores ticks up, 'Sitio web: no tiene' goes red (generic profile)")
D.behind(f'<div id="sign" class="sign"><div class="spost"></div><div class="sbd">{HOUSE % (64, 64)}<b>ALQUILADO</b><span>No es tuyo</span></div></div>')
D.css(""".sign{left:760px;top:260px;width:260px;height:420px;opacity:0} .spost{position:absolute;left:122px;top:120px;width:16px;height:300px;background:linear-gradient(90deg,#5a4636,#8a6c52);border-radius:4px}
 .sbd{position:absolute;left:0;top:0;width:260px;height:190px;border-radius:20px;background:#E5372B;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;box-shadow:0 0 50px rgba(229,55,43,.6),0 20px 40px rgba(0,0,0,.5);transform-origin:50% 0%}
 .sbd b{font-family:"HelvB",sans-serif;font-size:40px;letter-spacing:-.03em} .sbd span{font-size:24px;opacity:.9}""")
D.blur_in("#sign", 3.3, y=-300, d=0.5); D.js("tl.fromTo('#sign .sbd', {rotation:-7}, {rotation:4, duration:0.9, ease:'sine.inOut', yoyo:true, repeat:1}, 3.8);"); D.blur_out("#sign", 4.75)
D.ev("sign", "graphic", 3.3, 5.1, "'ALQUILADO' sign beside the head")

# 2  "si mañana se cae Instagram, cuántos clientes pierdo": his own reels grid behind the head, it goes down (grey + red + X)
D.behind(D.ig_grid("igf", RL([1, 5, 9, 2, 6, 10, 3, 7, 11, 4, 8, 12, 1, 5, 9])))
D.blur_in("#igf", 4.95, y=520, d=0.55); D.drift("#igf-in", 4.95, 4.7, -230)
D.js("tl.to('#igf-in', {filter:'grayscale(1) brightness(.5)', duration:0.3}, 7.6); tl.fromTo('#igf-red', {opacity:0}, {opacity:1, duration:0.3}, 7.6);")
D.pop("#igf-x", 7.7, 0.3); D.shake("#igf", 7.75); D.blur_out("#igf", 9.6, y=620, d=0.3)
D.front('<div id="err" class="pill" style="left:240px;top:1290px;width:600px;justify-content:center;background:rgba(15,15,15,.94);border:2px solid #E5372B;color:#fff;box-shadow:0 0 40px rgba(229,55,43,.5)">'
        '<i class="dot"></i>Instagram no disponible</div>')
D.css(".dot{width:18px;height:18px;border-radius:50%;background:#E5372B;box-shadow:0 0 14px #E5372B;display:block}")
D.blur_in("#err", 7.85, y=50, d=0.35, b=14); D.blur_out("#err", 9.55, y=60, d=0.25)
D.ev("igf", "graphic", 4.95, 9.9, "Instagram reels grid (Maison's own reel covers) goes grey, red, X + 'Instagram no disponible'")

# 3  "si la respuesta es todos, tenés un problema": clients round the head, all turn red
PTS = [(150, 420), (190, 640), (130, 860), (935, 420), (900, 640), (950, 860)]
D.behind(D.people("cl", PTS, label=None))
for k in range(6): D.pop(f"#cl{k}", round(9.75 + k * 0.07, 2), 0.26)
D.js(f"tl.to(['#cl0','#cl1','#cl2','#cl3','#cl4','#cl5'], {{background:'rgba(229,55,43,.85)', borderColor:'#ff8f86', boxShadow:'0 0 40px rgba(229,55,43,.8)', duration:0.25, stagger:0.04}}, 10.74);")
D.js("tl.to(['#cl0','#cl1','#cl2','#cl3','#cl4','#cl5'], {opacity:0, scale:0.6, filter:'blur(10px)', duration:0.3, stagger:0.03}, 11.75);")
D.ev("cl", "graphic", 9.75, 12.1, "Client icons round the head, all turn red on 'todos'")

# 4  "te bloquea la cuenta, cambia el algoritmo o te baja el alcance, tu negocio desaparece": three real-style notifications stack on the chest
N1 = NB("n1", 1270, "Instagram", "Tu cuenta fue suspendida", ig(80, "b"))
N2 = NB("n2", 1270, "Instagram", "Cambió el algoritmo", ig(80, "c"))
N3 = NB("n3", 1270, "Instagram", "Tu alcance bajó", ig(80, "d"))
D.front(N3 + N2 + N1)
D.js("tl.fromTo('#n1', {opacity:0, y:-60, filter:'blur(14px)'}, {opacity:1, y:0, filter:'blur(0px)', duration:0.4, ease:'power3.out'}, 13.05);")
D.js("tl.to('#n1', {opacity:0, y:-50, filter:'blur(12px)', duration:0.3}, 14.25); tl.fromTo('#n2', {opacity:0, y:-60, filter:'blur(14px)'}, {opacity:1, y:0, filter:'blur(0px)', duration:0.4, ease:'power3.out'}, 14.3);")
D.js("tl.to('#n2', {opacity:0, y:-50, filter:'blur(12px)', duration:0.3}, 15.9); tl.fromTo('#n3', {opacity:0, y:-60, filter:'blur(14px)'}, {opacity:1, y:0, filter:'blur(0px)', duration:0.4, ease:'power3.out'}, 15.95);")
D.js("tl.to(['#n3'], {opacity:0, y:120, filter:'blur(18px)', duration:0.4, ease:'power2.in', stagger:0.05}, 17.45);")
D.ev("notifs", "graphic", 13.05, 17.9, "Three Instagram notifications: cuenta suspendida, cambió el algoritmo, tu alcance bajó (generic labels)")

# 5  "un sitio web es un terreno propio": a browser window behind the head (url bar readable) + 'Terreno propio' tag
D.behind('<div id="br" class="panel br" style="top:150px"><div class="bbar"><i></i><i></i><i></i><div class="url">' + LOCK + '<b>tumarca.com</b></div></div>'
         '<div class="bhero"><small>TU MARCA</small><h2>Lo que vendés,<br/>en tu propio sitio.</h2><div class="bbtn">Comprar ahora</div></div></div>')
D.css(""".br{background:#F6F3EF;color:#141210} .bbar{height:84px;background:#E4DED7;display:flex;align-items:center;gap:14px;padding:0 26px} .bbar i{width:18px;height:18px;border-radius:50%;background:#C9C2BA}
 .url{margin-left:20px;flex:1;height:50px;border-radius:25px;background:#F6F3EF;display:flex;align-items:center;gap:12px;padding-left:20px;font-size:28px} .url b{font-weight:600;color:#141210;letter-spacing:-.02em}
 .bhero{padding:60px 50px} .bhero small{font-size:26px;letter-spacing:.2em;color:#8a847e} .bhero h2{margin:16px 0 30px;font-family:"HelvB",sans-serif;font-size:72px;line-height:1;letter-spacing:-.05em}
 .bbtn{display:inline-block;padding:22px 40px;border-radius:40px;background:#FF7A1A;color:#120C08;font-family:"HelvB",sans-serif;font-size:32px}""")
D.blur_in("#br", 18.45, y=-520, d=0.55); D.drift("#br", 19.0, 2.5, -40)
D.front(f'<div id="own" class="pill" style="left:270px;top:1290px;width:540px;justify-content:center;background:#2FA65A;color:#06140B;box-shadow:0 0 46px rgba(47,166,90,.55)">{HOUSE % (46, 46)}Terreno propio</div>')
D.css("#own svg{color:#06140B}")
D.blur_in("#own", 20.35, y=50, d=0.35, b=14); D.blur_out("#own", 21.3, y=60, d=0.25)
D.ev("br", "graphic", 18.45, 21.6, "Browser window 'tumarca.com' behind the head + green 'Terreno propio' tag (generic site)")

# 6  "capturás contactos, mostrás cosas, cobrás": three checks down the right column, the browser stays behind
for k, (key, lab, t) in enumerate([("mail", "Contactos", 21.75), ("grid", "Catálogo", 22.95), ("card", "Cobros", 24.15)]):
    D.behind(f'<div id="ft{k}" class="ft" style="top:{330 + k * 200}px"><div class="fti">{ICO[key]}</div><span>{lab}</span><u>{CHK % (40, 40)}</u></div>')
    D.pop(f"#ft{k}", t, 0.32)
D.css(""".ft{left:800px;width:220px;height:170px;border-radius:30px;background:rgba(15,15,15,.92);border:2px solid rgba(47,166,90,.7);box-shadow:0 0 34px rgba(47,166,90,.35);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;opacity:0;color:#fff}
 .ft span{font-size:28px;font-weight:600;letter-spacing:-.03em} .ft u{position:absolute;right:-12px;top:-12px}""")
D.js("tl.to(['#ft0','#ft1','#ft2'], {opacity:0, x:120, filter:'blur(14px)', duration:0.3, stagger:0.04}, 25.3);")
D.blur_out("#br", 25.35, y=-520)
D.ev("ft", "graphic", 21.75, 25.6, "Contactos / Catálogo / Cobros cards with checks, right of the head")

# 7  "y aparecés en Google cuando alguien busca lo que vendés": a Google search box on the chest, the query types, your site is first
D.front('<div id="gg" class="card" style="top:1265px;height:240px;padding:24px 30px"><div class="gq"><b class="gl"><i style="color:#4285F4">G</i><i style="color:#EA4335">o</i><i style="color:#FBBC05">o</i><i style="color:#4285F4">g</i><i style="color:#34A853">l</i><i style="color:#EA4335">e</i></b>'
        '<div class="gbox"><span id="gg-q">lo que vendés</span></div></div><div id="gg-r" class="gres"><em>1</em><div><small>tumarca.com</small><b>Tu marca &middot; Lo que vendés</b></div></div></div>')
D.css(""".gq{display:flex;align-items:center;gap:22px} .gl{font-family:"HelvB",sans-serif;font-size:46px;letter-spacing:-.03em} .gl i{font-style:normal}
 .gbox{flex:1;height:68px;border-radius:34px;background:#fff;color:#202124;display:flex;align-items:center;padding:0 26px;font-size:30px;overflow:hidden} #gg-q{white-space:nowrap;clip-path:inset(0 100% 0 0)}
 .gres{margin-top:20px;display:flex;align-items:center;gap:20px;opacity:0} .gres em{font-style:normal;width:62px;height:62px;border-radius:50%;background:#2FA65A;color:#06140B;font-family:"HelvB",sans-serif;font-size:36px;display:flex;align-items:center;justify-content:center}
 .gres small{display:block;font-size:22px;color:#9fd3a9} .gres b{display:block;font-size:32px;font-weight:600;color:#8ab4f8;letter-spacing:-.02em}""")
D.blur_in("#gg", 25.6, y=60, d=0.4, b=18)
D.js("tl.fromTo('#gg-q', {clipPath:'inset(0 100% 0 0)'}, {clipPath:'inset(0 0% 0 0)', duration:0.9, ease:'none'}, 26.3);")
D.js("tl.fromTo('#gg-r', {opacity:0, y:20}, {opacity:1, y:0, duration:0.35}, 27.2);"); D.blur_out("#gg", 27.65, y=80, d=0.3)
D.ev("gg", "graphic", 25.6, 27.95, "Google search: 'lo que vendés', tumarca.com first (generic)")

# 8  "las redes captan la atención, pero tu sitio web convierte vistas en clientes reales": attention vs clients, behind the head
D.behind(f'<div id="fl" class="fl"><div id="fl-a" class="fc"><div class="fci">{ig(70, "e")}</div><span>Redes</span><b>Atención</b></div>'
         f'<div id="fl-arr" class="farr"></div><div id="fl-b" class="fc win"><div class="fci">{LOCK.replace("26", "64")}</div><span>Sitio web</span><b>Clientes</b></div></div>')
D.css(""".fl{left:0;top:200px;width:1080px;height:600px} .fc{position:absolute;width:250px;height:300px;border-radius:36px;background:rgba(15,15,15,.92);border:2px solid rgba(255,255,255,.3);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;opacity:0;color:#fff}
 #fl-a{left:60px;top:80px} #fl-b{left:770px;top:80px} .fc span{font-size:28px;color:#bdbdbd;font-weight:500} .fc b{font-family:"HelvB",sans-serif;font-size:40px;letter-spacing:-.04em}
 .fc.win{border-color:#2FA65A;box-shadow:0 0 50px rgba(47,166,90,.45)} .fc.win b{color:#7BE0A0}
 .farr{position:absolute;left:330px;top:220px;width:420px;height:10px;border-radius:5px;background:linear-gradient(90deg,rgba(255,122,26,.2),#FF7A1A);transform-origin:0 50%;transform:scaleX(0);box-shadow:0 0 24px rgba(255,122,26,.7)}""")
D.pop("#fl-a", 27.95, 0.35); D.js("tl.fromTo('#fl-arr', {scaleX:0}, {scaleX:1, duration:1.0, ease:'power2.inOut'}, 29.3);")
D.pop("#fl-b", 30.3, 0.35); D.js("tl.to('#fl-b', {scale:1.08, duration:0.25, yoyo:true, repeat:1}, 31.4);")
D.js("tl.to('#fl', {opacity:0, filter:'blur(16px)', duration:0.3}, 32.45);")
D.ev("fl", "graphic", 27.95, 32.75, "Redes = atención -> Sitio web = clientes")

# 9  CTA "si tenés redes pero todavía no tenés un sitio web, escribime": checklist on the chest, then the DM arrives
D.front(f'<div id="ck" class="card" style="top:1265px;height:200px;padding:20px 34px"><div id="ck0" class="ckr"><span>{ig(48, "f")} Redes</span>{CHK % (48, 48)}</div>'
        f'<div id="ck1" class="ckr"><span>{LOCK.replace("26", "48")} Sitio web</span><i>todavía no</i>{XX % (48, 48)}</div></div>')
D.css(""".ckr{height:80px;display:flex;align-items:center;justify-content:space-between;font-size:38px;font-weight:600;letter-spacing:-.03em;opacity:0} .ckr span{display:flex;align-items:center;gap:16px}
 .ckr i{font-style:normal;font-size:28px;color:#ff8f86;margin-left:auto;margin-right:18px;font-weight:500} #ck0{border-bottom:1.5px solid rgba(255,255,255,.12)}""")
D.blur_in("#ck", 33.0, y=60, d=0.4, b=18)
D.js("tl.fromTo('#ck0', {opacity:0, x:-30}, {opacity:1, x:0, duration:0.3}, 33.25); tl.fromTo('#ck1', {opacity:0, x:-30}, {opacity:1, x:0, duration:0.3}, 34.5);")
D.blur_out("#ck", 35.55, y=80, d=0.3)
D.front(NB("dm", 1270, "tu.cliente", "Hola! Quiero mi sitio web &#128588;", ig(80, "g")))
D.js("tl.fromTo('#dm', {opacity:0, y:-60, filter:'blur(14px)'}, {opacity:1, y:0, filter:'blur(0px)', duration:0.4, ease:'power3.out'}, 35.75);")
D.ev("cta", "graphic", 33.0, DUR, "Checklist Redes ok / Sitio web todavía no, then a DM 'Quiero mi sitio web' (generic)")
D.write()

# sound: a few quiet effects on the key moments only
SFX = [(0.35, "riser", -34), (1.6, "impact", -31), (3.35, "swoosh", -26), (7.65, "impact", -29), (10.74, "pop", -25), (13.05, "pop", -24),
       (14.3, "pop", -25), (15.95, "pop", -25), (18.45, "woosh", -26), (20.35, "shine", -24), (27.2, "click", -25), (30.3, "shine", -24), (35.75, "pop", -21)]
json.dump({"glides": [], "accents": SFX, "dur": DUR}, open(os.path.join(ROOT, "sfx.json"), "w"))
