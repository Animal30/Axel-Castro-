"""Portada v2 del video presentando: cuadro exacto (cut.mov frame 194) + título EcoSport Freestyle 2019."""
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
FD = '/home/user/Axel-Castro-/golden-motors/fonts/BarlowCondensed-'
OR = (238, 120, 14); WH = (255, 255, 255); W, H = 1080, 1920
raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', 'cut.mov', '-map', '0:v:0', '-vf', 'select=eq(n\\,194)', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
base = Image.frombytes('RGB', (W, H), raw).convert('RGBA'); base.convert('RGB').save('cover2_clean.png')
lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
def txt(s, font, y, col, track=0, stroke=8):
    ws = [d.textlength(c, font=font) for c in s]; tot = sum(ws) + track * (len(s) - 1); x = W / 2 - tot / 2
    for c, w in zip(s, ws):
        d.text((x, y), c, font=font, fill=col + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255)); x += w + track
    return tot
f1 = ImageFont.truetype(FD + 'ExtraBold.ttf', 150); f2 = ImageFont.truetype(FD + 'ExtraBold.ttf', 200); f3 = ImageFont.truetype(FD + 'Bold.ttf', 64)
Y = 1120
txt('ECOSPORT', f1, Y, WH, track=6)
txt('FREESTYLE', f2, Y + 120, OR, track=2)
# 2019 con líneas naranjas a los lados
yy = Y + 345; wy = d.textlength('2019', font=f3) + 4 * 3
tw = txt('2019', f3, yy, WH, track=12, stroke=6)
for sgn in (-1, 1):
    x0 = W / 2 + sgn * (tw / 2 + 28); x1 = W / 2 + sgn * (tw / 2 + 28 + 150)
    d.rectangle((min(x0, x1), yy + 40, max(x0, x1), yy + 46), fill=OR + (255,))
sh = lay.filter(ImageFilter.GaussianBlur(14)); sa = (np.asarray(sh)[..., 3] * 0.55).astype(np.uint8)
shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shadow.putalpha(Image.fromarray(sa))
base.alpha_composite(shadow); base.alpha_composite(lay); base.convert('RGB').save('cover2.png')
