"""Golden Motors title style (Nahuel 2026-11-27, covers + openings of showcases and presentation reels):
small tracked brand line with thin side lines, huge Barlow Condensed Black model name with a gold gradient and soft shadow.
layer = title_layer(W, H, 'VOLKSWAGEN', 'AMAROK', y=300, alpha=1.0)  -> RGBA layer to alpha_composite over a frame."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
GOLD_TOP, GOLD_BOT = (255, 211, 78), (217, 154, 16)

def _f(name, size): return ImageFont.truetype(os.path.join(FONTS, f'BarlowCondensed-{name}.ttf'), size)

def title_layer(W, H, brand, model, y=300, alpha=1.0, max_w=820, size=205, brand_size=74):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    a = int(255 * alpha)
    # brand: tracked white with thin side lines
    fb = _f('SemiBold', brand_size); tr = 18
    ws = [d.textlength(c, font=fb) for c in brand]; tw = sum(ws) + tr * (len(brand) - 1); x = W / 2 - tw / 2
    for c, w in zip(brand, ws):
        d.text((x, y), c, font=fb, fill=(255, 255, 255, a)); x += w + tr
    ly = y + int(brand_size * 0.62); gap, ln = 30, 120
    d.line((W / 2 - tw / 2 - gap - ln, ly, W / 2 - tw / 2 - gap, ly), fill=(255, 255, 255, int(a * 0.85)), width=3)
    d.line((W / 2 + tw / 2 + gap, ly, W / 2 + tw / 2 + gap + ln, ly), fill=(255, 255, 255, int(a * 0.85)), width=3)
    # model: Black with gold gradient
    fm = _f('Black', size)
    while d.textlength(model, font=fm) > max_w: size -= 4; fm = _f('Black', size)
    my = y + int(brand_size * 0.95)
    mw = d.textlength(model, font=fm); mx = W / 2 - mw / 2
    mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).text((mx, my), model, font=fm, fill=255)
    bb = mask.getbbox()
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shadow.putalpha(mask.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.6 * alpha)))
    sh2 = Image.new('RGBA', (W, H), (0, 0, 0, 255)); sh2.putalpha(shadow.getchannel('A'))
    lay.alpha_composite(sh2, (0, 10))
    grad = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(grad)
    y0, y1 = bb[1], bb[3]
    for yy in range(y0, y1 + 1):
        k = (yy - y0) / max(1, y1 - y0); gd.line((0, yy, W, yy), fill=tuple(int(GOLD_TOP[i] + (GOLD_BOT[i] - GOLD_TOP[i]) * k) for i in range(3)) + (255,))
    ol = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ol).text((mx, my), model, font=fm, fill=(40, 26, 0, int(150 * alpha)), stroke_width=3, stroke_fill=(40, 26, 0, int(150 * alpha)))
    lay.alpha_composite(ol)
    grad.putalpha(mask.point(lambda v: int(v * alpha))); lay.alpha_composite(grad)
    return lay, (bb[3] if bb else my + size)   # bottom of the model letters
