"""Golden Motors - 'nuevo local + web' reel. python3 build.py [ONLY=frames]"""
import json, os, subprocess, math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src.mp4')
OUTRO = '/mnt/project-files/golden-motors/outro-logo/golden-motors-outro-girando-con-sonido.mp4'
W, H, FPS = 1080, 1920, 30
GOLD = (242, 184, 36); WHITE = (255, 255, 255)
FX, FY = 540, 860  # zoom anchor (faces)

SEGS = [(3.26, 6.42, 1.0), (7.56, 8.98, 1.12), (9.02, 11.32, 1.0), (11.84, 15.70, 1.12),
        (16.14, 16.46, 1.0), (17.12, 21.95, 1.12), (22.34, 23.36, 1.0), (23.60, 27.45, 1.12)]
COVER_T, COVER_Z, COVER_DUR = 18.8, 1.12, 0.5

# ---------- 1. cut ----------
def zoom_filter(z):
    if z == 1.0: return 'null'
    cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    x = int(FX - cw * FX / W); y = int(FY - ch * FY / H)
    return f'crop={cw}:{ch}:{x}:{y},scale={W}:{H}:flags=lanczos'

def make_cut():
    parts, inputs = [], []
    for i, (a, b, z) in enumerate(SEGS):
        parts.append(f'[0:v]trim={a}:{b},setpts=PTS-STARTPTS,{zoom_filter(z)},setsar=1[v{i}];'
                     f'[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={b-a-0.02:.3f}:d=0.02[a{i}];')
    n = len(SEGS)
    fc = ''.join(parts) + ''.join(f'[v{i}][a{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=1[v][a]'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', SRC, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-r', str(FPS), '-c:a', 'pcm_s16le', 'cut.mov'], check=True)

def src_to_cut(t):
    off = 0
    for a, b, z in SEGS:
        if a - 0.05 <= t <= b + 0.05: return off + min(max(t - a, 0), b - a)
        off += b - a
    return None

# ---------- 2. words -> captions ----------
FIX = {'Moto,': 'Motors,'}
DROP = {'Avisá', 'nomás.', 'eh,', 'nue--', 'Los', 'esper--'}
def caption_words():
    d = json.load(open(os.path.join(HERE, 'tx.json')))
    out = []
    for w in d['words']:
        if w['type'] != 'word' or w['text'] in DROP: continue
        a, b = src_to_cut(w['start']), src_to_cut(w['end'])
        if a is None or b is None: continue
        out.append([a, b, FIX.get(w['text'], w['text'])])
    return out

def chunk(words, maxw=3):
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= maxw or w[2][-1] in '.,?!':
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    # merge tiny 1-word groups forward
    res = []
    for g in groups:
        if res and len(g) == 1 and len(res[-1]) < 3 and res[-1][-1][2][-1] not in '.?!': res[-1] += g
        else: res.append(g)
    return res

# ---------- 3. overlay drawing ----------
F_CAP = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf', 74)
F_CARD = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', 58)
F_CARD_S = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Medium.otf', 36)
F_TAG = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', 40)
F_TAG_S = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Medium.otf', 26)
F_HOOK = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 132)
F_HOOK2 = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', 46)
CAP_Y = 1290

def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def back(x):
    x = min(max(x, 0), 1); c = 1.6; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

def draw_caption(img, groups, t):
    g = next((g for g in groups if g[0][0] - 0.05 <= t <= g[-1][1] + 0.12), None)
    if g is None: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    words = [w[2].upper() for w in g]
    sp = 22; widths = [d.textlength(w, font=F_CAP) for w in words]
    total = sum(widths) + sp * (len(words) - 1)
    lines = [list(range(len(words)))]
    if total > 940:  # two lines
        lines = [list(range(len(words) - 1)), [len(words) - 1]] if len(words) > 1 else lines
    pop = back((t - g[0][0] + 0.05) / 0.18)
    cur = max([i for i in range(len(g)) if g[i][0] - 0.03 <= t] or [-1])
    y = CAP_Y - (len(lines) - 1) * 45
    for ln in lines:
        lw = sum(widths[i] for i in ln) + sp * (len(ln) - 1); x = W / 2 - lw / 2
        for i in ln:
            col = GOLD if i == cur else WHITE
            d.text((x, y), words[i], font=F_CAP, fill=col + (255,), stroke_width=7, stroke_fill=(0, 0, 0, 255))
            x += widths[i] + sp
        y += 90
    sh = lay.filter(ImageFilter.GaussianBlur(10)); sa = np.array(sh)[..., 3] * 0.55
    s = 0.85 + 0.15 * pop
    if s != 1:
        lay = lay.resize((int(W * s), int(H * s)), Image.BICUBIC)
        nl = Image.new('RGBA', (W, H)); nl.paste(lay, (int(W / 2 - W * s / 2), int(CAP_Y + 40 - (CAP_Y + 40) * s))); lay = nl
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shadow.putalpha(Image.fromarray(sa.astype(np.uint8)))
    img.alpha_composite(shadow); img.alpha_composite(lay)

def glass_card(img, cx, cy, title, sub, icon, t, t0, t1, accent_title=False):
    if t < t0 or t > t1 + 0.3: return
    p_in = ease((t - t0) / 0.35); p_out = ease((t - t1) / 0.3)
    alpha = p_in * (1 - p_out); dy = (1 - p_in) * 40 - p_out * 20
    d0 = ImageDraw.Draw(img)
    tw = max(d0.textlength(title, font=F_CARD), d0.textlength(sub, font=F_CARD_S) if sub else 0)
    bw, bh = int(tw + 210), 186 if sub else 130
    card = Image.new('RGBA', (bw + 60, bh + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
    d.rounded_rectangle((30, 30, 30 + bw, 30 + bh), 36, fill=(12, 12, 12, 215), outline=GOLD + (230,), width=3)
    # icon disc
    ix, iy = 30 + 30 + 40, 30 + bh // 2
    d.ellipse((ix - 40, iy - 40, ix + 40, iy + 40), fill=GOLD + (255,))
    icon(d, ix, iy)
    tx = ix + 66
    if sub:
        d.text((tx, 30 + 32), title, font=F_CARD, fill=(GOLD if accent_title else WHITE) + (255,))
        d.text((tx, 30 + 114), sub, font=F_CARD_S, fill=(215, 205, 185, 255))
    else:
        d.text((tx, iy - 30), title, font=F_CARD, fill=WHITE + (255,))
    sh = Image.new('RGBA', card.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((30, 40, 30 + bw, 40 + bh), 36, fill=(0, 0, 0, 160))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    sh.alpha_composite(card); card = sh
    a = np.array(card); a[..., 3] = (a[..., 3] * alpha).astype(np.uint8); card = Image.fromarray(a)
    s = 0.9 + 0.1 * back((t - t0) / 0.35)
    card = card.resize((max(1, int(card.width * s)), max(1, int(card.height * s))), Image.BICUBIC)
    img.alpha_composite(card, (int(cx - card.width / 2), int(cy - card.height / 2 + dy)))

def icon_pin(d, x, y):
    d.ellipse((x - 15, y - 24, x + 15, y + 6), fill=(12, 12, 12)); d.polygon([(x - 13, y - 2), (x + 13, y - 2), (x, y + 24)], fill=(12, 12, 12))
    d.ellipse((x - 6, y - 15, x + 6, y - 3), fill=GOLD)
def icon_globe(d, x, y):
    k = (12, 12, 12); d.ellipse((x - 22, y - 22, x + 22, y + 22), outline=k, width=4)
    d.ellipse((x - 9, y - 22, x + 9, y + 22), outline=k, width=4); d.line((x - 22, y, x + 22, y), fill=k, width=4)
def icon_clock(d, x, y):
    k = (12, 12, 12); d.ellipse((x - 22, y - 22, x + 22, y + 22), outline=k, width=5)
    d.line((x, y, x, y - 13), fill=k, width=5); d.line((x, y, x + 10, y + 6), fill=k, width=5)

def name_tag(img, cx, cy, name, t, t0, t1):
    if t < t0 or t > t1 + 0.3: return
    p_in = ease((t - t0) / 0.3); p_out = ease((t - t1) / 0.3); alpha = p_in * (1 - p_out)
    d0 = ImageDraw.Draw(img); tw = d0.textlength(name, font=F_TAG); sw = d0.textlength('SOCIO', font=F_TAG_S)
    bw = int(max(tw, sw) + 64); bh = 104
    lay = Image.new('RGBA', (bw + 40, bh + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((20, 20, 20 + bw, 20 + bh), 22, fill=(12, 12, 12, 220))
    d.rectangle((20, 20, 28, 20 + bh), fill=GOLD + (255,))
    d.text((48, 28), name, font=F_TAG, fill=WHITE + (255,)); d.text((48, 80), 'SOCIO', font=F_TAG_S, fill=GOLD + (255,))
    a = np.array(lay); a[..., 3] = (a[..., 3] * alpha).astype(np.uint8); lay = Image.fromarray(a)
    img.alpha_composite(lay, (int(cx - lay.width / 2 + (1 - p_in) * -30), int(cy)))

def hook(img):
    d = ImageDraw.Draw(img)
    for txt, font, col, y in [('NOS', F_HOOK, WHITE, 250), ('MUDAMOS', F_HOOK, GOLD, 385)]:
        tw = d.textlength(txt, font=font)
        d.text((W / 2 - tw / 2, y), txt, font=font, fill=col + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255))
    sub = 'Conocé el nuevo local de Golden Motors'
    tw = d.textlength(sub, font=F_HOOK2)
    d.rounded_rectangle((W / 2 - tw / 2 - 30, 560, W / 2 + tw / 2 + 30, 640), 20, fill=(12, 12, 12, 225))
    d.text((W / 2 - tw / 2, 572), sub, font=F_HOOK2, fill=WHITE + (255,))

# ---------- 4. render ----------
def render(only=None):
    words = caption_words(); groups = chunk(words)
    wt = {w[2]: w for w in words}
    def at(word): return next(w for w in words if w[2].startswith(word))
    T = {
        'addr0': at('Estamos')[0], 'addr1': at('3181')[1] + 0.5,
        'renzo0': at('Renzo')[0] - 0.4, 'renzo1': at('conoce')[1],
        'ale0': at('Alejandro')[0] - 0.2, 'ale1': at('Alejandro')[1] + 0.9,
        'web0': at('página')[0], 'web1': at('Nuestros')[0] - 0.35,
        'hrs0': at('Nuestros')[0], 'hrs1': at('corrido')[1] + 0.1,
    }
    print({k: round(v, 2) for k, v in T.items()})
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'cut.mov']))
    n = int(dur * FPS)
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', 'cut.mov', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', 'body.mp4'], stdin=subprocess.PIPE)
    for i in range(n):
        raw = dec.stdout.read(W * H * 3)
        if len(raw) < W * H * 3: break
        t = i / FPS
        if only and i not in only: enc.stdin.write(raw); continue
        img = Image.frombytes('RGB', (W, H), raw).convert('RGBA')
        glass_card(img, W / 2, 420, 'Octavio Pinto 3181', 'Nuevo local · Córdoba', icon_pin, t, T['addr0'], T['addr1'])
        name_tag(img, 330, 1010, 'Alejandro', t, T['ale0'], T['ale1'])
        name_tag(img, 760, 1010, 'Renzo', t, T['renzo0'], T['renzo1'])
        glass_card(img, W / 2, 420, 'goldenmotorscba.com', 'Todo el stock online', icon_globe, t, T['web0'], T['web1'], accent_title=True)
        glass_card(img, W / 2, 420, 'Lunes a viernes', '9 a 18 hs · de corrido', icon_clock, t, T['hrs0'], T['hrs1'])
        draw_caption(img, groups, t)
        out = img.convert('RGB')
        if only: out.save(f'chk_{i:04d}.jpg', quality=88)
        enc.stdin.write(out.tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()

def cover():
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-ss', str(COVER_T), '-i', SRC, '-frames:v', '1', '-vf', zoom_filter(COVER_Z),
                                   '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    img = Image.frombytes('RGB', (W, H), raw).convert('RGBA')
    dark = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(dark)
    for y in range(0, 760): dd.line((0, y, W, y), fill=(0, 0, 0, int(150 * (1 - y / 760))))
    img.alpha_composite(dark); hook(img); img.convert('RGB').save('cover.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', 'cover.png', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-t', str(COVER_DUR), '-r', str(FPS), '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'cover.mp4'], check=True)

def final(out):
    body_d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'body.mp4']))
    fc = ('[1:v]setsar=1[b];[0:v]setsar=1[c];[2:v]setsar=1,fps=30[o];'
          '[1:a]aresample=48000,loudnorm=I=-14:TP=-1.5:LRA=11[ba];[0:a]aresample=48000[ca];[2:a]aresample=48000[oa];'
          '[c][ca][b][ba][o][oa]concat=n=3:v=1:a=1[v][a]')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'cover.mp4', '-i', 'body.mp4', '-i', 'cut.mov', '-i', OUTRO,
                    '-filter_complex', fc.replace('[2:v]', '[3:v]').replace('[2:a]', '[3:a]').replace('[1:a]', '[2:a]'),
                    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)

if __name__ == '__main__':
    import sys
    step = sys.argv[1]
    if step == 'cut': make_cut()
    elif step == 'check': render(only=set(int(x) for x in sys.argv[2].split(',')))
    elif step == 'render': render()
    elif step == 'cover': cover()
    elif step == 'final': final(sys.argv[2])
