#!/usr/bin/env python3
"""Dejá de tocar el botón azul - Maison Enterprises (ES), guion viral 4. Visual essay reel (black + orange), no Maison logo.
All times are GLOBAL seconds on the cut timeline (~/reel-work/boton/edit.txt). The presenter's head top sits at y 860,
so the wall used here is y 230-840."""
import os
import essay_engine as E

ROOT = os.path.dirname(os.path.abspath(__file__))
E.init(ROOT)
DUR = E.P["dur"]
E.ZONE = (65, 230, 1015, 840)
MK = "stand-in rebuilt in HTML (generic account 'tu.marca'), Meta/Instagram UI wording"
REY = "/mnt/project-files/maison-enterprises-es/anuncios-rey/rey-resultados.jpg (Rey La Tinta's real Meta Ads results, sent by Nahuel)"
CHIP = """.chp{position:absolute;opacity:0} .chp div{height:92px;padding:0 30px;border-radius:46px;background:rgba(14,12,11,.92);border:2px solid rgba(255,255,255,.28);
  display:flex;align-items:center;gap:16px;font-family:"HelvB",sans-serif;font-weight:700;font-size:40px;letter-spacing:-.04em;color:#F2F0EC;white-space:nowrap;box-shadow:0 18px 40px rgba(0,0,0,.55)}
  .chp i{font-style:normal;width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px;color:#fff;flex:none}
  .chp.ok div{border-color:rgba(47,166,90,.8);box-shadow:0 0 34px rgba(47,166,90,.35)} .chp.ok i{background:#2FA65A}
  .chp.no div{border-color:rgba(229,55,43,.9);box-shadow:0 0 34px rgba(229,55,43,.4)} .chp.no i{background:#E5372B}
  .winl{display:inline-block;padding:16px 30px;border-radius:40px;background:#2FA65A;color:#06140B;font:700 36px "HelvB",sans-serif;letter-spacing:-.03em;opacity:0;box-shadow:0 0 40px rgba(47,166,90,.5)}"""
def chip(i, x, y, text, kind="ok"):
    return f'<div id="{i}" class="chp {kind}" style="left:{x}px;top:{y}px"><div><i>{"&#10003;" if kind == "ok" else "&#10005;"}</i>{text}</div></div>'

E.glow(0, "bottom")

# 1  "dejar de tocar el botón azul de promocionar": the Instagram post with its blue button; it gets an X
with E.scene(0.0, 2.45) as s:
    s.card("assets/media/post.png", (540, 240, 700, 470), t=0.0, how="cut", origin=MK, mock=True)
    s.raw('<div style="position:absolute;left:715px;top:580px"><div id="bx1" class="bx">&#10005;</div></div>',
          css=CHIP + """.bx{width:110px;height:110px;border-radius:50%;background:#E5372B;color:#fff;font:700 64px/110px "HelvB",sans-serif;text-align:center;box-shadow:0 0 50px rgba(229,55,43,.85);opacity:0}""",
          js='pop("#bx1",1.87,0.2);', ids=["bx1"])
E.sfx(1.87, "impact", -30)

# 2  "le estás regalando la plata a Instagram": coins fly into the Instagram icon
IG = ('<svg viewBox="0 0 48 48" width="300" height="300"><defs><radialGradient id="igg" cx="30%" cy="107%" r="150%"><stop offset="0" stop-color="#FEDA75"/><stop offset=".25" stop-color="#FA7E1E"/>'
      '<stop offset=".5" stop-color="#D62976"/><stop offset=".75" stop-color="#962FBF"/><stop offset="1" stop-color="#4F5BD5"/></radialGradient></defs><rect x="2" y="2" width="44" height="44" rx="12" fill="url(#igg)"/>'
      '<rect x="12" y="12" width="24" height="24" rx="7" fill="none" stroke="#fff" stroke-width="3.4"/><circle cx="24" cy="24" r="5.6" fill="none" stroke="#fff" stroke-width="3.4"/><circle cx="32.6" cy="15.4" r="2" fill="#fff"/></svg>')
CP = [(90, 300), (140, 560), (110, 720), (260, 420), (230, 640)]
coins = "".join(f'<div style="position:absolute;left:{x}px;top:{y}px"><div id="cn{k}" class="coin">$</div></div>' for k, (x, y) in enumerate(CP))
with E.scene(2.5, 4.35) as s:
    s.raw(f'<div style="position:absolute;left:620px;top:330px"><div id="igb" style="opacity:0;filter:drop-shadow(0 0 60px rgba(214,41,118,.55))">{IG}</div></div>' + coins,
          css=""".coin{width:96px;height:96px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#FFE9A8,#E8B53A 60%,#9C7316);color:#5a3d00;font:700 56px/96px "HelvB",sans-serif;text-align:center;opacity:0;box-shadow:0 10px 30px rgba(0,0,0,.6)}""",
          js='pop("#igb",2.55,0.22);' + "".join(f'tl.fromTo("#cn{k}",{{opacity:0,x:0,y:0,scale:1}},{{opacity:1,duration:0.12}},{2.75 + k * 0.12:.2f}); tl.to("#cn{k}",{{x:{720 - x},y:{430 - y},scale:0.35,opacity:0,duration:0.55,ease:"power2.in"}},{2.87 + k * 0.12:.2f});'
                                             for k, (x, y) in enumerate(CP)),
          ids=["igb"] + [f"cn{k}" for k in range(5)])
E.sfx(2.75, "swish", -27)

# 3  "pensado para darte likes y visitas al perfil, no clientes": the boost goal screen + what it gets you
with E.scene(4.37, 8.62) as s:
    s.card("assets/media/boost.png", (330, 270, 560, 400), t=4.49, origin=MK, mock=True, source="Promocionar publicación (Instagram)")
    s.raw(chip("c1", 650, 300, "Likes") + chip("c2", 650, 420, "Visitas") + chip("c3", 650, 560, "Clientes", "no"),
          js='pop("#c1",6.37,0.2); pop("#c2",6.91,0.2); pop("#c3",8.03,0.2);', ids=["c1", "c2", "c3"])
E.sfx(8.03, "impact", -31)

# 4  "¿Por qué?": straight to camera
E.solo(8.69, 9.85); E.punch(8.69, 1.1, hold=1.1)

# 5  "no podés elegir bien el objetivo, no podés probar varios anuncios y saber qué funcionó"
with E.scene(9.89, 14.2) as s:
    s.raw(chip("l1", 230, 300, "Elegir el objetivo", "no") + chip("l2", 230, 430, "Probar varios anuncios", "no") + chip("l3", 230, 560, "Saber qué funcionó", "no"),
          js='pop("#l1",10.43,0.2); pop("#l2",11.81,0.2); pop("#l3",13.53,0.2);', ids=["l1", "l2", "l3"])

# 6  "desde el administrador de anuncios ... mensajes o ventas"
E.glow(14.2, "low-left")
E.punch(14.2, 1.06, hold=1.25)
with E.scene(14.2, 19.4) as s:
    s.card("assets/media/obj.png", (360, 270, 600, 450), t=15.52, origin=MK, mock=True, source="Administrador de anuncios (Meta)")
    s.raw(chip("o1", 690, 380, "Mensajes") + chip("o2", 690, 510, "Ventas"), js='pop("#o1",18.19,0.2); pop("#o2",18.99,0.2);', ids=["o1", "o2"])
E.sfx(15.52, "woosh", -26); E.sfx(18.99, "shine", -25)

# 7  "probás tres versiones al mismo tiempo y Meta le da la plata al que mejor convierte"
ads = ""
for k, lab in enumerate("ABC"):
    ads += (f'<div style="position:absolute;left:{120 + k * 290}px;top:250px"><div id="ad{k}" class="adv"><div class="adi">Anuncio {lab}</div>'
            f'<div class="bb"><i id="bf{k}"></i></div><b id="bp{k}">33%</b></div></div>')
W3 = (12, 18, 70)
with E.scene(19.45, 23.55) as s:
    s.raw(ads + '<div style="position:absolute;left:0;width:1080px;top:650px;text-align:center"><span id="win" class="winl">Más presupuesto al que convierte</span></div>',
          css=""".adv{width:260px;height:360px;border-radius:26px;background:rgba(14,12,11,.92);border:2px solid rgba(255,255,255,.25);box-shadow:0 20px 50px rgba(0,0,0,.55);opacity:0;padding:20px;box-sizing:border-box}
          .adi{height:165px;border-radius:16px;background:radial-gradient(80% 80% at 50% 35%,#3A2A1E,#17120E);display:flex;align-items:center;justify-content:center;color:#F2F0EC;font:700 34px "HelvB",sans-serif;letter-spacing:-.03em}
          .bb{margin-top:26px;height:22px;border-radius:11px;background:rgba(255,255,255,.12);overflow:hidden} .bb i{display:block;height:100%;width:33%;background:#FF7A1A;border-radius:11px}
          .adv b{display:block;margin-top:16px;text-align:center;font:700 54px "HelvB",sans-serif;color:#F2F0EC;letter-spacing:-.04em}""",
          js='pop("#ad0",19.83,0.2); pop("#ad1",19.95,0.2); pop("#ad2",20.07,0.2);'
             + "".join(f'tl.to("#bf{k}",{{width:"{w}%",duration:0.8,ease:"power2.inOut"}},21.93);' for k, w in enumerate(W3))
             + "".join(f'(function(){{const c={{n:33}},el=document.querySelector("#bp{k}");tl.to(c,{{n:{w},duration:0.8,ease:"power2.inOut",onUpdate:function(){{el.textContent=Math.round(c.n)+"%";}}}},21.93);}})();' for k, w in enumerate(W3))
             + 'tl.to("#ad2",{borderColor:"#2FA65A",boxShadow:"0 0 50px rgba(47,166,90,.55)",duration:0.3},22.61); tl.to("#bf2",{background:"#2FA65A",duration:0.3},22.61);'
             + 'tl.to(["#ad0","#ad1"],{opacity:0.45,duration:0.3},22.61); pop("#win",22.61,0.2);',
          ids=["ad0", "ad1", "ad2", "win"])
E.sfx(21.93, "riser", -33); E.sfx(22.61, "shine", -24)

# 8  "mismo presupuesto, pero con un resultado completamente distinto": a real client's two ads in Meta Ads
E.glow(23.55, "bottom")
with E.scene(23.55, 26.88) as s:
    a, b = (430, 250, 640, 322), (650, 440, 640, 322)
    s.card("assets/media/first.jpg", a, t=23.85, label="Anuncio 1", origin=REY, source="Campaña real de un cliente")
    s.card("assets/media/sec.jpg", b, t=24.99, label="Anuncio 2", origin=REY)
    s.raw('<div style="position:absolute;left:60px;top:596px"><span id="x3" class="winl" style="font-size:38px;display:inline-block;transform:rotate(-3deg)">3 veces más barato</span></div>',
          js='pop("#x3",25.61,0.2);', ids=["x3"])
E.sfx(24.99, "pop", -25); E.sfx(25.61, "impact", -30)

# 9  CTA "escribime BOTÓN y te lo explico": the keyword, then the DM arriving
E.glow(26.9, "behind", 0.9)
IG2 = IG.replace('width="300" height="300"', 'width="76" height="76"').replace('id="igg"', 'id="igg2"').replace("url(#igg)", "url(#igg2)")
with E.scene(26.9, DUR) as s:
    s.text("Escribime", 540, 330, t=28.31, size=56)
    s.text("*BOTÓN*", 540, 400, t=28.79, size=150)
    s.raw('<div style="position:absolute;left:90px;top:640px"><div id="dm" class="dmb"><div class="dmi">' + IG2
          + '</div><div class="dmt"><b>tu.cliente</b><span>BOTÓN</span></div><em>ahora</em></div></div>',
          css=""".dmb{width:900px;height:140px;border-radius:42px;background:rgba(36,36,40,.92);border:1px solid rgba(255,255,255,.14);box-shadow:0 24px 60px rgba(0,0,0,.55);display:flex;align-items:center;gap:24px;padding:0 30px;box-sizing:border-box;opacity:0;position:relative}
          .dmt b{display:block;font:700 34px "HelvB",sans-serif;color:#fff;letter-spacing:-.03em} .dmt span{display:block;font-size:32px;color:#e2e2e2;letter-spacing:0} .dmb em{position:absolute;right:30px;top:28px;font-style:normal;font-size:26px;color:#9a9a9a;letter-spacing:0}""",
          js='rise("#dm",29.33,0.25);', ids=["dm"])
E.sfx(28.79, "shine", -24); E.sfx(29.33, "pop", -22)

E.build()
