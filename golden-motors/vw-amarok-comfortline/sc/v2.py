"""Ford Ka SEL showcase - showcase, no talking, cut to the beat. python3 v2.py pieces|render|final"""
import os, subprocess, sys, math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw'); AUD = os.path.join(HERE, 'aud')
OUTRO = '/mnt/project-files/golden-motors/outro-logo/golden-motors-outro-girando-con-sonido.mp4'
W, H, FPS = 1080, 1920, 30
BEAT = 0.5  # beat of the new track (117-120 BPM); body starts 0.5 s into the video, audio = track[0.05:]
GOLD = (242, 184, 36); WHITE = (255, 255, 255)
GRADE = 'eq=contrast=1.07:saturation=1.10:gamma=1.06:brightness=0.0,colorbalance=rs=0.02:bs=-0.02:rh=0.02:bh=-0.03,vignette=PI/8'
# clip, src start, beats, speed, label (title, sub) or None
SHOTS = [
    ('0066', 0.0, 6, 1.0, None),
    ('0064', 0.2, 2, 0.7, None),
    ('0067', 0.3, 2, 0.7, (['2.0 TDI', '180 CV'], None)),
    ('0068', 0.2, 2, 0.7, (['CUBIERTAS', 'ALL TERRAIN'], None)),
    ('0069', 0.2, 2, 0.7, None),
    ('0073', 0.3, 2, 0.7, ('4X4', 'Tracción integral')),
    ('0072', 0.3, 2, 0.7, None),
    ('0077', 2.0, 2, 0.7, (['CAJA MANUAL', '6 MARCHAS'], None)),
    ('0075', 0.2, 2, 0.7, None),
    ('0081', 0.3, 2, 0.7, None),
    ('0071', 4.4, 5.8, 0.9, None),
]
FLASH_AT = {2, 4, 6, 8}   # shot indices that start with a soft flash

def starts():
    t, out = 0.0, []
    for s in SHOTS:
        out.append(t); t += s[2] * BEAT
    return out, t

def pieces():
    os.makedirs('p2', exist_ok=True)
    for i, (c, s, beats, sp, _) in enumerate(SHOTS):
        d = beats * BEAT
        vf = f"trim={s}:{s + d * sp + 0.3},setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale={W}:{H}:flags=lanczos,{GRADE},format=yuv420p"
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{RAW}/c{c}.mov', '-an', '-vf', vf, '-frames:v', str(round(d * FPS)),
                        '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', f'p2/{i:02d}.mp4'], check=True)
    open('p2/list.txt', 'w').write(''.join(f"file '{os.path.abspath(f'p2/{i:02d}.mp4')}'\n" for i in range(len(SHOTS))))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'p2/list.txt', '-c', 'copy', 'cut2.mp4'], check=True)

BF = lambda w, z: ImageFont.truetype('/home/user/Axel-Castro-/golden-motors/fonts/BarlowCondensed-' + w + '.ttf', z)
F_T1 = BF('ExtraBold', 250)
F_T2 = BF('Bold', 70)
F_L1 = BF('ExtraBold', 190)
F_L2 = BF('SemiBold', 44)

def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3

def spaced(d, xy_center_y, text, font, fill, tracking, alpha=255, stroke=0):
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1); x = W / 2 - total / 2
    for ch, w in zip(text, widths):
        d.text((x, xy_center_y), ch, font=font, fill=fill + (alpha,), stroke_width=stroke, stroke_fill=(0, 0, 0, int(alpha * 0.8)))
        x += w + tracking
    return total

def text_layer(t, st, total):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # opening title
    if t < st[1] + 0.2:
        p = ease((t - 0.25) / 0.7); q = 1 - ease((t - (st[1] - 0.25)) / 0.35)
        a = int(255 * p * q)
        if a > 0:
            f = F_T1
            while sum(d.textlength(ch, font=f) for ch in 'AMAROK') + 4 * 6 > 900: f = BF('ExtraBold', f.size - 4)
            spaced(d, 250, 'AMAROK', f, WHITE, 4 + 8 * (1 - p), a, 3)
            spaced(d, 560, 'VW COMFORTLINE 4X4 · 2021', F_T2, GOLD, 10, a, 2)
    # spec labels
    for i, s in enumerate(SHOTS):
        if not s[4]: continue
        t0, t1 = st[i], st[i] + s[2] * BEAT
        if not (t0 <= t < t1): continue
        p = ease((t - t0 - 0.05) / 0.3); q = 1 - ease((t - (t1 - 0.18)) / 0.15)
        a = int(255 * p * q)
        if a <= 0: continue
        title, sub = s[4]
        y = 1250 + int((1 - p) * 30)
        lines = title if sub is None else [title.upper()]
        for k, ln in enumerate(lines):
            sz = 190 if sub is not None else 165
            f = BF('ExtraBold', sz)
            while sum(d.textlength(ch, font=f) for ch in ln) + 2 * (len(ln) - 1) > 940: sz -= 4; f = BF('ExtraBold', sz)
            spaced(d, y, ln, f, WHITE if k == 0 else GOLD, 2, a, 3); y += int(sz * 1.12)
        if sub is not None: spaced(d, y + 6, sub.upper(), F_L2, GOLD, 14, a, 2)
    # end card
    i = len(SHOTS) - 1
    if t >= st[i]:
        p = ease((t - st[i] - 0.2) / 0.6); a = int(255 * p)
        spaced(d, 270, 'GOLDEN MOTORS', BF('ExtraBold', 150), WHITE, 6, a, 4)
        spaced(d, 450, 'OCTAVIO PINTO 3181 · CÓRDOBA', F_L2, GOLD, 8, a, 2)
        spaced(d, 510, 'CONSULTANOS POR MENSAJE', F_L2, WHITE, 8, int(a * 0.9), 2)
    sh = lay.filter(ImageFilter.GaussianBlur(12)); sa = np.array(sh)[..., 3].astype(np.float32) * 0.5
    return lay, sa

def render():
    st, total = starts(); n = int(round(total * FPS))
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', 'cut2.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-crf', '15', '-preset', 'medium', '-pix_fmt', 'yuv420p', 'body2.mp4'], stdin=subprocess.PIPE)
    only = os.environ.get('ONLY'); only = set(int(x) for x in only.split(',')) if only else None
    for f in range(n):
        raw = dec.stdout.read(W * H * 3)
        if len(raw) < W * H * 3: break
        t = f / FPS
        if only and f not in only: enc.stdin.write(raw); continue
        img = np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(np.float32)
        i = max(k for k in range(len(SHOTS)) if st[k] <= t + 1e-6)
        p = (t - st[i]) / (SHOTS[i][2] * BEAT)
        z = 1.0 + 0.05 * p if i != len(SHOTS) - 1 else 1.0 + 0.04 * p
        if i in FLASH_AT and t - st[i] < 0.12:  # punch-in on the beat
            z += 0.05 * (1 - (t - st[i]) / 0.12)
        if z > 1.0:
            cw, ch = int(W / z), int(H / z); x0, y0 = (W - cw) // 2, (H - ch) // 2
            img = cv2.resize(img[y0:y0 + ch, x0:x0 + cw], (W, H), interpolation=cv2.INTER_LINEAR)
        if i in FLASH_AT and t - st[i] < 0.1:
            k = 1 - (t - st[i]) / 0.1; img = img * (1 - 0.45 * k) + 255 * 0.45 * k
        if t < 0.35: img *= t / 0.35
        lay, sa = text_layer(t, st, total)
        la = np.array(lay).astype(np.float32); a = la[..., 3:4] / 255
        img = img * (1 - sa[..., None] / 255) ; img = img * (1 - a) + la[..., :3] * a
        out = np.clip(img, 0, 255).astype(np.uint8)
        if only: Image.fromarray(out).save(f'c2_{f:04d}.jpg', quality=88)
        enc.stdin.write(out.tobytes())
    enc.stdin.close(); enc.wait(); dec.stdout.close(); dec.kill(); dec.wait()
    print('total', round(total, 2))

COVER_SRC = ('0065', 3.4)
def cover():
    c, t = COVER_SRC
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-ss', str(t), '-i', f'{RAW}/c{c}.mov', '-frames:v', '1',
                                   '-vf', f'scale={W}:{H}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    im = np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy()
    tmp = subprocess.run(['ffmpeg', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-i', '-', '-vf', GRADE,
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], input=im.tobytes(), capture_output=True, check=True).stdout
    img = Image.frombytes('RGB', (W, H), tmp).convert('RGBA')
    # no dark band: only a soft shadow behind the letters
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    bigs = BF('ExtraBold', 200)
    _d = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
    while sum(_d.textlength(ch, font=bigs) for ch in 'AMAROK') + 12 * 7 > 900: bigs = BF('ExtraBold', bigs.size - 4)
    for txt, y in [('AMAROK', 285)]:
        tw = sum(sd.textlength(ch, font=bigs) for ch in txt) + 12 * (len(txt) - 1); x = W / 2 - tw / 2
        for ch in txt:
            sd.text((x + 4, y + 10), ch, font=bigs, fill=(0, 0, 0, 170), stroke_width=10, stroke_fill=(0, 0, 0, 170)); x += sd.textlength(ch, font=bigs) + 12
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); d = ImageDraw.Draw(img)
    big = bigs
    for txt, col, y in [('AMAROK', WHITE, 285)]:
        tw = sum(d.textlength(ch, font=big) for ch in txt) + 12 * (len(txt) - 1); x = W / 2 - tw / 2
        for ch in txt:
            d.text((x, y), ch, font=big, fill=col + (255,), stroke_width=8, stroke_fill=(0, 0, 0, 255)); x += d.textlength(ch, font=big) + 12
    f2 = BF('SemiBold', 62)
    sub = 'COMFORTLINE 4X4 · 2021 · 110.000 km'; tw = d.textlength(sub, font=f2)
    d.rounded_rectangle((W / 2 - tw / 2 - 34, 490, W / 2 + tw / 2 + 34, 570), 22, fill=(12, 12, 12, 230), outline=GOLD + (255,), width=3)
    d.text((W / 2 - tw / 2, 494), sub, font=f2, fill=WHITE + (255,))
    img.convert('RGB').save('cover2.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', 'cover2.png', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-t', '0.5', '-r', str(FPS), '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'cover2.mp4'], check=True)

def withcover(body, out):
    fc = '[0:v]setsar=1[c];[1:v]setsar=1[b];[0:a]aresample=48000[ca];[1:a]aresample=48000,aformat=channel_layouts=stereo[ba];[c][ca][b][ba]concat=n=2:v=1:a=1[v][a]'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'cover2.mp4', '-i', body, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)

def final(out):
    st, total = starts()
    fc = (f"[1:a]volume=-3dB,atrim=0:{total},afade=t=out:st={total - 1.0:.2f}:d=1.0,alimiter=limit=0.9,aformat=channel_layouts=stereo[a];"
          f"[0:v]setsar=1[v]")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'body2.mp4', '-i', 'music2.wav',
                    '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)

if __name__ == '__main__':
    os.chdir(HERE)
    a = sys.argv[1]
    if a == 'cover': cover()
    elif a == 'withcover': withcover(sys.argv[2], sys.argv[3])
    else: {'pieces': pieces, 'render': render}.get(a, lambda: final(sys.argv[2]))()
