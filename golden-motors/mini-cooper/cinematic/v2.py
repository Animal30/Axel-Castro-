"""Mini Cooper S JCW cinematic showcase. 60 fps source in slow motion, cuts land on the accents of the music.
python3 v2.py pieces|render|cover|final v2_body.mp4|withcover v2_body.mp4 out.mp4"""
import os, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw')
W, H, FPS = 1080, 1920, 30
GOLD = (242, 184, 36); WHITE = (255, 255, 255)
GRADE = 'eq=contrast=1.08:saturation=1.06:gamma=1.05,colorbalance=rs=-0.02:bs=0.03:rh=0.02:bh=-0.02,vignette=PI/7'
# accents of the music (video time) 4.44 9.43 14.44 19.44 24.43 -> body time = video - 0.5 (cover is 0.5 s)
# clip, source start, output seconds, speed, label (lines, sub) or None
SHOTS = [
    ('4573', 0.0, 8.93, 0.57, None),                                  # badge pulls back to the whole car
    ('4560', 0.3, 5.01, 0.70, (['192 CV', 'CAJA AUTOMÁTICA'], None)), # steering wheel pull back, dash
    ('4572', 0.5, 2.50, 0.70, None),
    ('4568', 0.2, 2.49, 0.70, (['JOHN COOPER', 'WORKS'], None)),
    ('4571', 1.0, 4.99, 0.70, (['2016', '93.000 KM'], None)),
    ('2320', 32.6, 3.97, 1.00, None),                                 # walk round to the whole car, finale with the end card
]
TITLE_T0, TITLE_T1 = 3.80, 8.60
FLASH_AT = {1, 2, 4, 5}

def starts():
    t, out = 0.0, []
    for s in SHOTS:
        out.append(t); t += s[2]
    return out, t

def pieces():
    os.makedirs('p2', exist_ok=True)
    for i, (c, s, d, sp, _) in enumerate(SHOTS):
        vf = (f"trim={s}:{s + d * sp + 0.4},setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale={W}:{H}:flags=lanczos,{GRADE},format=yuv420p")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{RAW}/c{c}.mov', '-an', '-vf', vf, '-frames:v', str(round(d * FPS)),
                        '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', f'p2/{i:02d}.mp4'], check=True)
    open('p2/list.txt', 'w').write(''.join(f"file '{os.path.abspath(f'p2/{i:02d}.mp4')}'\n" for i in range(len(SHOTS))))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'p2/list.txt', '-c', 'copy', 'cut2.mp4'], check=True)

BF = lambda w, z: ImageFont.truetype('/home/user/Axel-Castro-/golden-motors/fonts/BarlowCondensed-' + w + '.ttf', z)
F_T2 = BF('Bold', 66); F_L2 = BF('SemiBold', 44)
def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3

def spaced(d, y, text, font, fill, tracking, alpha=255, stroke=0):
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1); x = W / 2 - total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill + (alpha,), stroke_width=stroke, stroke_fill=(0, 0, 0, int(alpha * 0.8)))
        x += w + tracking
    return total

def fit(d, text, size, maxw, tracking):
    f = BF('ExtraBold', size)
    while sum(d.textlength(ch, font=f) for ch in text) + tracking * (len(text) - 1) > maxw: size -= 4; f = BF('ExtraBold', size)
    return f

def text_layer(t, st, total):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if TITLE_T0 <= t < TITLE_T1:      # opening title lands on the first accent
        p = ease((t - TITLE_T0) / 0.6); q = 1 - ease((t - (TITLE_T1 - 0.4)) / 0.4); a = int(255 * p * q)
        if a > 0:
            f = fit(d, 'MINI COOPER S', 230, 940, 6)
            spaced(d, 300 + int((1 - p) * 20), 'MINI COOPER S', f, WHITE, 6 + 10 * (1 - p), a, 3)
            spaced(d, 300 + int(f.size * 1.02), 'JOHN COOPER WORKS · 2016', F_T2, GOLD, 9, a, 2)
    for i, s in enumerate(SHOTS):
        if not s[4]: continue
        t0, t1 = st[i], st[i] + s[2]
        if not (t0 <= t < t1): continue
        p = ease((t - t0 - 0.08) / 0.35); q = 1 - ease((t - (t1 - 0.3)) / 0.25); a = int(255 * p * q)
        if a <= 0: continue
        y = 1260 + int((1 - p) * 26)
        for k, ln in enumerate(s[4][0]):
            f = fit(d, ln, 150, 940, 2)
            spaced(d, y, ln, f, WHITE if k == 0 else GOLD, 2, a, 3); y += int(f.size * 1.1)
    i = len(SHOTS) - 1
    if t >= st[i] + 0.6:
        p = ease((t - st[i] - 0.6) / 0.7); a = int(255 * p)
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
        if i in FLASH_AT and t - st[i] < 0.1:
            k = 1 - (t - st[i]) / 0.1; img = img * (1 - 0.35 * k) + 255 * 0.35 * k
        if t < 0.4: img *= t / 0.4
        lay, sa = text_layer(t, st, total)
        la = np.array(lay).astype(np.float32); a = la[..., 3:4] / 255
        img = img * (1 - sa[..., None] / 255); img = img * (1 - a) + la[..., :3] * a
        out = np.clip(img, 0, 255).astype(np.uint8)
        if only: Image.fromarray(out).save(f'c2_{f:04d}.jpg', quality=88)
        enc.stdin.write(out.tobytes())
    enc.stdin.close(); enc.wait(); dec.stdout.close(); dec.kill(); dec.wait()
    print('total', round(total, 2))

COVER_SRC = ('2320', 36.0); SHIFT_X = 34
def cover():
    c, t = COVER_SRC
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-ss', str(t), '-i', f'{RAW}/c{c}.mov', '-frames:v', '1',
                                   '-vf', f'scale={W}:{H}:flags=lanczos,{GRADE}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    arr = np.frombuffer(raw, np.uint8).reshape(H, W, 3)
    M = np.float32([[1, 0, SHIFT_X], [0, 1, 0]])   # nudge the car to the middle, mirror-fill the thin strip that opens on the left
    arr = cv2.warpAffine(arr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    img = Image.fromarray(arr).convert('RGBA'); d = ImageDraw.Draw(img)
    f = fit(d, 'MINI COOPER S', 210, 900, 8)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    spaced(sd, 305, 'MINI COOPER S', f, (0, 0, 0), 8, 170, 10)
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); d = ImageDraw.Draw(img)
    spaced(d, 300, 'MINI COOPER S', f, WHITE, 8, 255, 8)
    f2 = BF('SemiBold', 62); sub = 'JOHN COOPER WORKS · 2016 · 93.000 km'; tw = d.textlength(sub, font=f2)
    y0 = 300 + int(f.size * 1.02) + 40
    d.rounded_rectangle((W / 2 - tw / 2 - 34, y0, W / 2 + tw / 2 + 34, y0 + 80), 22, fill=(12, 12, 12, 230), outline=GOLD + (255,), width=3)
    d.text((W / 2 - tw / 2, y0 + 4), sub, font=f2, fill=WHITE + (255,))
    img.convert('RGB').save('cover2.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', 'cover2.png', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-t', '0.5', '-r', str(FPS), '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'cover2.mp4'], check=True)

def withcover(body, out):
    fc = ('[0:v]setsar=1[c];[1:v]setsar=1[b];[0:a]aresample=48000,aformat=channel_layouts=stereo[ca];[1:a]aresample=48000,aformat=channel_layouts=stereo[ba];'
          '[c][ca][b][ba]concat=n=2:v=1:a=1[v][a]')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'cover2.mp4', '-i', body, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)

def final(out):   # body with silent track; the music is laid over the whole video afterwards
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'body2.mp4', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', out], check=True)

if __name__ == '__main__':
    os.chdir(HERE); a = sys.argv[1]
    if a == 'cover': cover()
    elif a == 'withcover': withcover(sys.argv[2], sys.argv[3])
    elif a == 'final': final(sys.argv[2])
    else: {'pieces': pieces, 'render': render}[a]()
