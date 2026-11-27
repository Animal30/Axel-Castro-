"""Captions estilo 'kinetic italic' (referencia captionstyle.mp4): Inter Extra Bold Italic, Title Case, palabras clave grandes y conectores chicos,
numeros enormes, aparecen palabra por palabra con subida suave, blanco con sombra suave."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1080, 1920
FB = '/usr/share/fonts/opentype/inter/Inter-ExtraBoldItalic.otf'; FM = '/usr/share/fonts/opentype/inter/Inter-MediumItalic.otf'
_f = {}
def font(path, size):
    k = (path, size)
    if k not in _f: _f[k] = ImageFont.truetype(path, size)
    return _f[k]
CONN = {'a', 'y', 'e', 'o', 'de', 'del', 'el', 'la', 'lo', 'los', 'las', 'con', 'en', 'que', 'te', 'por', 'para', 'si', 'un', 'una', 'uno', 'es', 'este', 'esta', 'tiene', 'al', 'se', 'me', 'mi', 'tu', 'su', 'vos', 'vení'}
def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def style(w):
    s = w.strip('.,;:?!"')
    if any(c.isdigit() for c in s): return s, font(FB, 150), 1.0
    if s.lower() in CONN: return s.lower() if s.lower() != 'vení' else 'Vení', font(FM, 60), 0.88
    return (s if s.isupper() and len(s) > 1 else s[:1].upper() + s[1:]), font(FB, 112), 1.0
BASE_Y = 1300
def draw_caption(img, groups, t):
    g = next((g for g in groups if g[0][0] - 0.02 <= t <= g[-1][1] + 0.14), None)
    if g is None: return
    items = [style(w[2]) for w in g]
    d0 = ImageDraw.Draw(Image.new('RGBA', (4, 4)))
    ws = [d0.textlength(s, font=f) for s, f, _ in items]; sp = 26
    lines, cur, cw = [], [], 0
    for i, w in enumerate(ws):
        add = w + (sp if cur else 0)
        if cur and cw + add > 900: lines.append(cur); cur, cw = [i], w
        else: cur.append(i); cw += add
    if cur: lines.append(cur)
    out = max(0, min(1, (g[-1][1] + 0.14 - t) / 0.12))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    lh = [max(items[i][1].size for i in ln) for ln in lines]
    total_h = sum(lh) + 8 * (len(lines) - 1); y = BASE_Y - total_h / 2
    for ln, h in zip(lines, lh):
        lw = sum(ws[i] for i in ln) + sp * (len(ln) - 1); x = W / 2 - lw / 2
        for i in ln:
            s, f, op = items[i]; a = ease((t - g[i][0] + 0.02) / 0.16) * out
            if a > 0:
                rise = (1 - ease((t - g[i][0] + 0.02) / 0.16)) * 16
                d.text((x, y + h - f.size * 1.0 + rise), s, font=f, fill=(255, 255, 255, int(255 * a * op)))
            x += ws[i] + sp
        y += h + 8
    sh = lay.filter(ImageFilter.GaussianBlur(12)); a = np.array(sh); a[..., :3] = 0; a[..., 3] = (a[..., 3] * 0.6).astype(np.uint8)
    img.alpha_composite(Image.fromarray(a, 'RGBA')); img.alpha_composite(lay)
