"""Captions estilo 'kinetic italic' (referencia captionstyle.mp4): Inter Extra Bold Italic, Title Case, palabras clave grandes y conectores chicos,
numeros enormes, aparecen palabra por palabra con subida suave, blanco con sombra suave."""
import os
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

# ---------------- letra "vidriada" (referencia de Nahuel 27/11) ----------------
FSB = '/usr/share/fonts/opentype/inter/Inter-BoldItalic.otf'
GLASS_STYLES = {
    # tono sobre fondo oscuro, tono sobre fondo claro, peso del tono, opacidad, degradado abajo, brillo borde, usa inversion
    'white':  dict(lt=(246, 247, 250), dk=(62, 64, 68), tm=0.7, op=0.85, fade=0.8, rim=28, inv=True),
    'clear':  dict(lt=(250, 251, 253), dk=(58, 60, 64), tm=0.62, op=0.7, fade=0.62, rim=50, inv=True),
    'orange': dict(lt=(255, 146, 52), dk=(140, 58, 8), tm=1.0, op=0.72, fade=0.62, rim=50, inv=False),
}
def glass_composite(img, mask, strength=None, blur=1.0, style=None):
    """mask: PIL 'L' del texto. Vidrio: el fondo se ve a traves de las letras (con su textura), invertido en luminosidad
    (claro sobre fondo oscuro, oscuro sobre fondo claro), mas transparente hacia abajo de cada letra, con un brillo fino en el borde."""
    rgb = np.array(img.convert('RGB')).astype(np.float32)
    bl = np.array(img.convert('RGB').filter(ImageFilter.GaussianBlur(1.5))).astype(np.float32)
    soft = np.array(img.convert('RGB').filter(ImageFilter.GaussianBlur(10))).astype(np.float32)
    lum = (soft[..., 0] * .299 + soft[..., 1] * .587 + soft[..., 2] * .114) / 255.0
    # inversion tipo "diferencia": el fondo se ve invertido a traves de la letra (con su textura)
    inv = 255 - bl
    # empujar a blanco sobre oscuro y a gris oscuro sobre claro (sin llegar a negro)
    st = GLASS_STYLES[style or os.environ.get('GLASS_STYLE', 'white')]
    if strength is None: strength = st['op']
    t = np.clip((lum - 0.36) / 0.18, 0, 1)[..., None]
    tone = np.array(st['lt'], np.float32) * (1 - t) + np.array(st['dk'], np.float32) * t
    if st['inv']: glass = tone * st['tm'] + inv * (1 - st['tm'])
    else: glass = tone + (bl - soft) * 0.9          # vidrio de color: el tono con la textura del fondo
    rimc = np.array(st['lt'], np.float32) * 0.5 + 127
    m = np.array(mask).astype(np.float32) / 255.0
    # transparencia vertical dentro de cada letra: arriba mas solido, abajo deja ver mas
    rows = np.where(m.max(1) > 0)[0]
    if len(rows):
        g = np.ones(H, np.float32)
        lab = np.zeros(H, np.int32)
        # degradado por bloque de lineas contiguas
        start = rows[0]; prev = rows[0]
        blocks = []
        for r in rows[1:]:
            if r != prev + 1: blocks.append((start, prev)); start = r
            prev = r
        blocks.append((start, prev))
        for a0, b0 in blocks:
            g[a0:b0 + 1] = np.linspace(1.0, st['fade'], b0 - a0 + 1)
        m = m * g[:, None]
    m = (m * strength)[..., None]
    out = rgb * (1 - m) + glass * m
    mk = mask.filter(ImageFilter.MinFilter(3))
    edge = np.clip(np.array(mask).astype(np.float32) - np.roll(np.roll(np.array(mk).astype(np.float32), 2, 0), 2, 1), 0, 255) / 255.0
    out = out + edge[..., None] * (st['rim'] / 255.0) * rimc * (1 - t)
    img.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), 'RGB').convert('RGBA'))
def glass_lines(img, lines, cx=W / 2, y=640, gap=6, strength=None, fade_bottom=False):
    """lines: [(texto, fuente)], centrado. Devuelve nada; modifica img."""
    lay = Image.new('L', (W, H), 0); d = ImageDraw.Draw(lay); yy = y
    for txt, f in lines:
        tw = d.textlength(txt, font=f); d.text((cx - tw / 2, yy), txt, font=f, fill=255); yy += f.size + gap
    glass_composite(img, lay, strength)
