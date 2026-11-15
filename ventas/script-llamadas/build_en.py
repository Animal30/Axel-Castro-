"""English version of SCRIPT-10KTeamClosers (same layout as the Word original).
Usage: python build_en.py <dir-with-Aptos.ttf-and-Aptos-Bold.ttf>
Aptos is a Microsoft font (free download from Microsoft); it is not stored in the repo.
"""
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).resolve()

# (kind, text): h=title, s=section heading, b=bold line, p=paragraph, li=bullet, hr=rule
DOC = [
("h", "SCRIPT — CAR DETAILER CALLS"),
("s", "OPENING"),
("p", "— Hi, good morning! Am I speaking with [BUSINESS NAME]?"),
("p", "— Yes, hi, good morning, go ahead."),
("p", "— Good morning, my name is Nahuel/Nico/Axel. Who am I speaking with?"),
("p", "— Darío. How’s it going?"),
("p", "— All good, Darío. Look, I’m calling because your services were recommended to me. I’m from the north side, I looked you up on Google, saw you on Maps and on Instagram, but I couldn’t find a website with more information about the shop. I wasn’t sure if you were open or taking clients."),
("p", "— Yes, yes, Nahuel, we’re working."),
("p", "— Great, perfect."),
("hr", ""),
("s", "PITCH TRANSITION"),
("p", "— Look, Darío, I build sales funnel systems for car detailers and dealerships in Argentina."),
("p", "— Since I saw you didn’t have a website, I took the initiative and put together a premium website for the brand."),
("p", "— It’s going to serve you specifically for:"),
("li", "client management"), ("li", "sales"), ("li", "inquiries"), ("li", "and brand perception"),
("p", "— Are you working on your own or do you have a team?"),
("hr", ""),
("s", "RAPPORT BUILDING"),
("p", "(IF HE SAYS HE WORKS ALONE)"),
("p", "— Ah, nice, nice."),
("p", "— How long have you been in detailing, Darío?"),
("p", "— Uhh, it’s been about 5 years since I started."),
("p", "— That’s a long time!"),
("p", "— First, let me tell you everything looks amazing. I loved what you’ve been building, and I thought it was the right moment to show you what I put together for you."),
("hr", ""),
("s", "DIAGNOSIS"),
("p", "— Right now, are you running any kind of ads?"),
("p", "— There’s a girl who handles the Instagram."),
("p", "— Perfect."),
("p", "— Roughly how many inquiries are you getting per day?"),
("p", "— Uhh, around 10, let’s say, but they’re just browsing."),
("p", "— Right."),
("p", "— And out of those 10, how many turn into serious clients?"),
("p", "— 2."),
("p", "— And how much are you investing in ads?"),
("p", "— About 150 thousand pesos."),
("hr", ""),
("s", "SPOTTING THE OPPORTUNITY"),
("p", "— Look, honestly, with the level of work you have, you should be getting more than 15 to 20 inquiries a day."),
("p", "— And today the problem usually isn’t the service."),
("p", "— The problem tends to be:"),
("li", "brand perception"), ("li", "follow-up"), ("li", "and how the inquiries come in"),
("p", "— Because most people come in through Instagram, ask for the price and disappear."),
("hr", ""),
("s", "BUSINESS CAPACITY"),
("p", "— And today, how many clients could you handle per day?"),
("p", "— How many cars fit in the shop, Darío?"),
("p", "— We can take about 8 cars, so yes, I have room."),
("p", "— Perfect, so there’s room to scale."),
("hr", ""),
("s", "PRESENTING THE SOLUTION"),
("p", "— Well, look, for the businesses I work with I build:"),
("li", "the entire sales funnel"), ("li", "the advertising"), ("li", "the websites"), ("li", "and the inquiry system"),
("p", "— The idea is to increase the number of SERIOUS inquiries and improve how the business is perceived."),
("p", "— That’s why I’d like to show it to you on a video call, a Google Meet, if that works for you."),
("hr", ""),
("s", "CLOSE"),
("p", "— Sure, let’s do it."),
("p", "— Perfect, Darío. Right now I’m heading to an in-person meeting with a dealership."),
("p", "— I’m free after 2 in the afternoon."),
("p", "— Around 3, does that work for you?"),
("p", "— Perfect."),
("p", "— Then I’ll send you a WhatsApp with the link."),
("hr", ""),
("s", "KEY PHRASES FOR THE TEAM"),
("s", "IMPORTANT"),
("li", "“I’ll be quick so I don’t take up your time.”"),
("li", "“Your services were recommended to me.”"),
("li", "“I took the initiative.”"),
("li", "“Everything looks amazing.”"),
("li", "“Brand perception.”"),
("li", "“Serious inquiries.”"),
("li", "“Sales funnel.”"),
("li", "“Inquiry system.”"),
("hr", ""),
("s", "OBJECTIONS"),
("b", "“I’m not interested”"),
("p", "— Totally, I understand."),
("p", "— Still, before we hang up, let me ask you something quick:"),
("p", "— Right now, do most of your inquiries come in through Instagram?"),
("hr", ""),
("b", "“I already have someone handling marketing”"),
("p", "— Perfect."),
("p", "— Then you’ll probably get what I put together right away, because it’s focused specifically on conversion and serious inquiries."),
("hr", ""),
("b", "“I don’t need a website”"),
("p", "— Yes, a lot of detailers start out thinking that, because everything comes in through Instagram."),
("p", "— But the problem usually isn’t getting inquiries."),
("p", "— The problem is converting better clients and improving how the business is perceived."),
("hr", ""),
("b", "“I don’t have time”"),
("p", "— Totally, that’s exactly why I’m suggesting something super short."),
("p", "— 10 or 15 minutes max and I’ll show you everything quickly."),
]

CSS = f"""
@font-face {{ font-family: Aptos; font-weight: 400; src: url('{(FONTS/'Aptos.ttf').as_uri()}'); }}
@font-face {{ font-family: Aptos; font-weight: 700; src: url('{(FONTS/'Aptos-Bold.ttf').as_uri()}'); }}
@page {{ size: 612pt 792pt; margin: 72pt; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: Aptos, sans-serif; font-size: 12pt; color: #000; orphans: 2; widows: 2; }}
p, .s, .b, li, .hr {{ line-height: 16.95pt; margin-bottom: 8.05pt; }}
h1 {{ font-size: 15.96pt; font-weight: 700; text-align: center; line-height: 22.6pt; margin-bottom: 8pt; }}
.s, .b {{ font-weight: 700; break-after: avoid; }}
ul {{ list-style: none; }}
li {{ position: relative; padding-left: 36pt; }}
li::before {{ content: "•"; position: absolute; left: 18pt; top: 1pt; font-size: 9.96pt; }}
.hr {{ position: relative; height: 16.95pt; }}
.hr::after {{ content: ""; position: absolute; left: 0; right: 0; top: 10.5pt; height: 1.5pt;
  background: linear-gradient(#a0a0a0 0 1.2pt, #e3e3e3 1.2pt 1.5pt); }}
"""

def build():
    out, in_list = [], False
    for kind, text in DOC:
        t = html.escape(text, quote=False)
        if kind == "li" and not in_list:
            out.append("<ul>"); in_list = True
        if kind != "li" and in_list:
            out.append("</ul>"); in_list = False
        out.append({"h": f"<h1>{t}</h1>", "s": f"<div class='s'>{t}</div>", "b": f"<div class='b'>{t}</div>",
                    "p": f"<p>{t}</p>", "li": f"<li>{t}</li>", "hr": "<div class='hr'></div>"}[kind])
    if in_list: out.append("</ul>")
    doc = f"<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><title>SCRIPT — CAR DETAILER CALLS</title><style>{CSS}</style></head><body>{''.join(out)}</body></html>"
    src = HERE / "_en.html"; src.write_text(doc, encoding="utf-8")
    pdf = HERE / "SCRIPT-10KTeamClosers-EN.pdf"
    subprocess.run(["/opt/pw-browsers/chromium-1243/chrome-linux64/chrome", "--headless", "--no-sandbox", "--disable-gpu",
                    "--no-pdf-header-footer", "--allow-file-access-from-files", "--virtual-time-budget=4000",
                    f"--print-to-pdf={pdf}", src.as_uri()], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    src.unlink()
    print(pdf)

build()
