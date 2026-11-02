"""Genera el PDF de una propuesta comercial de Maison Enterprises.

Uso:
    python propuestas/build.py propuestas/clientes/<cliente>/datos.json

El diseño vive en _plantilla/propuesta.html.j2 y no se toca por cliente.
Cada cliente tiene su datos.json (textos, precios, servicios) y el PDF
sale en la misma carpeta con el nombre de "archivo".
"""
import base64, json, os, pathlib, shutil, subprocess, sys, tempfile

from jinja2 import Environment, FileSystemLoader, ChainableUndefined

HERE = pathlib.Path(__file__).parent
TPL = HERE / "_plantilla"

FONTS = [
    ("Inter", 400, "normal", "Inter-Regular.woff2"),
    ("Inter", 600, "normal", "Inter-SemiBold.woff2"),
    ("Inter", 700, "normal", "Inter-Bold.woff2"),
    ("Inter", 800, "normal", "Inter-ExtraBold.woff2"),
    ("Newsreader", 400, "italic", "Newsreader-Italic.woff2"),
]

ICONS = {
    "meta":  '<svg viewBox="0 0 24 24"><path d="M6 20v-6M12 20V8M18 20v-9"/></svg>',
    "web":   '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>',
    "crm":   '<svg viewBox="0 0 24 24"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>',
    "video": '<svg viewBox="0 0 24 24"><path d="m16 13 5.2 3.5a.5.5 0 0 0 .8-.4V7.9a.5.5 0 0 0-.8-.4L16 11"/><rect x="2" y="6" width="14" height="12" rx="2"/></svg>',
    "chat":  '<svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "mail":  '<svg viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
    "star":  '<svg viewBox="0 0 24 24"><path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>',
    "search": '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>',
    "camera": '<svg viewBox="0 0 24 24"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3z"/><circle cx="12" cy="13" r="3"/></svg>',
    "users": '<svg viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/></svg>',
}


def chrome_path():
    for c in (os.environ.get("CHROME"), "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome",
              shutil.which("chromium"), shutil.which("google-chrome"), shutil.which("chrome"),
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"):
        if c and pathlib.Path(c).exists():
            return c
    sys.exit("No encontré Chrome/Chromium. Indicá la ruta con la variable CHROME.")


def font_css():
    out = []
    for fam, w, st, f in FONTS:
        b64 = base64.b64encode((TPL / "fonts" / f).read_bytes()).decode()
        out.append(f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};'
                   f'src:url(data:font/woff2;base64,{b64}) format("woff2");}}')
    return "\n".join(out)


def render(datos_path, keep_html=False):
    datos_path = pathlib.Path(datos_path)
    d = json.loads(datos_path.read_text(encoding="utf-8"))
    env = Environment(loader=FileSystemLoader(TPL), undefined=ChainableUndefined, autoescape=False)
    html = env.get_template("propuesta.html.j2").render(d=d, fonts=font_css(), icons=ICONS)

    out_pdf = datos_path.parent / f"{d['archivo']}.pdf"
    with tempfile.TemporaryDirectory() as tmp:
        src = pathlib.Path(tmp) / "propuesta.html"
        src.write_text(html, encoding="utf-8")
        if keep_html:
            (datos_path.parent / "_preview.html").write_text(html, encoding="utf-8")
        subprocess.run([chrome_path(), "--headless", "--no-sandbox", "--disable-gpu",
                        "--no-pdf-header-footer", "--virtual-time-budget=5000",
                        f"--print-to-pdf={out_pdf}", src.as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_pdf


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    print(render(sys.argv[1], keep_html="--html" in sys.argv))
