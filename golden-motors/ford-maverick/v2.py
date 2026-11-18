"""Ford Maverick 2023 reel 2 (stories) - showcase, no talking, cut to the beat. python3 v2.py pieces|render|final"""
import os, subprocess, sys, math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw'); AUD = os.path.join(HERE, 'aud')
OUTRO = '/mnt/project-files/golden-motors/outro-logo/golden-motors-outro-girando-con-sonido.mp4'
W, H, FPS = 1080, 1920, 30
BPM = 120; BEAT = 60 / BPM
GOLD = (242, 184, 36); WHITE = (255, 255, 255)
GRADE = 'eq=contrast=1.09:saturation=1.10:gamma=0.97,colorbalance=rs=0.02:bs=-0.02:rh=0.02:bh=-0.03,vignette=PI/5'
# clip, src start, beats, speed, label (title, sub) or None
SHOTS = [
    (4493, 0.2, 4, 0.6, None),
    (4495, 0.3, 4, 0.6, None),
    (4499, 0.2, 4, 0.6, None),
    (4501, 1.2, 4, 0.6, ('2023', 'Modelo')),
    (4504, 2.6, 4, 0.6, ('Interior', 'Impecable')),
    (4505, 0.5, 4, 0.6, None),
    (4513, 1.5, 4, 0.6, None),
    (4494, 0.3, 6, 0.5, ('$38.000.000', 'Ford Maverick 2023')),
]
FLASH_AT = {2, 4, 6}   # shot indices that start with a soft flash

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

F_T1 = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 150)
F_T1B = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 136)
F_T2 = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 40)
F_L1 = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 96)
F_L2 = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 34)

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
            spaced(d, 300, 'FORD', F_T1, WHITE, 18 - 8 * p, a, 4)
            spaced(d, 460, 'MAVERICK', F_T1B, GOLD, 18 - 8 * p, a, 4)
            y = 650; L = int(120 * p)
            d.line((W / 2 - 70 - L, y + 22, W / 2 - 70, y + 22), fill=GOLD + (a,), width=3)
            d.line((W / 2 + 70, y + 22, W / 2 + 70 + L, y + 22), fill=GOLD + (a,), width=3)
            spaced(d, y, '2023', F_T2, WHITE, 10, a, 2)
    # spec labels
    for i, s in enumerate(SHOTS):
        if not s[4]: continue
        t0, t1 = st[i], st[i] + s[2] * BEAT
        if not (t0 <= t < t1): continue
        p = ease((t - t0 - 0.05) / 0.3); q = 1 - ease((t - (t1 - 0.18)) / 0.15)
        a = int(255 * p * q)
        if a <= 0: continue
        title, sub = s[4]
        y = 1330 + int((1 - p) * 30)
        spaced(d, y, sub.upper(), F_L2, GOLD, 9, a, 2)
        spaced(d, y + 48, title.upper(), F_L1, WHITE, 4, a, 5)
    # end card
    i = len(SHOTS) - 1
    if t >= st[i]:
        p = ease((t - st[i] - 0.2) / 0.6); a = int(255 * p)
        spaced(d, 330, 'GOLDEN MOTORS', F_L1 if False else ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 84), WHITE, 8, a, 5)
        spaced(d, 440, 'OCTAVIO PINTO 3181 · CÓRDOBA', F_L2, GOLD, 6, a, 2)
        spaced(d, 495, 'CONSULTANOS POR MENSAJE', F_L2, WHITE, 6, int(a * 0.9), 2)
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

COVER_SRC = (4493, 3.9)   # straight front, lights on; ceiling-lamp reflection retouched out of the windshield
def cover():
    c, t = COVER_SRC
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-ss', str(t), '-i', f'{RAW}/c{c}.mov', '-frames:v', '1',
                                   '-vf', f'scale={W}:{H}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    im = np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy()
    m = np.zeros((H, W), np.uint8); cv2.ellipse(m, (CX, CY), (RX, RY), 0, 0, 360, 255, -1)
    im = cv2.seamlessClone(np.roll(im, SHIFT, axis=1), im, m, (CX, CY), cv2.NORMAL_CLONE)
    DOWN = 190; im = np.concatenate([im[DOWN - 1::-1], im[:-DOWN]], 0)   # room for the title below the story header
    im = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-i', '-', '-vf', GRADE,
                                       '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], input=im.tobytes(), capture_output=True, check=True).stdout, np.uint8).reshape(H, W, 3)
    img = Image.fromarray(im).convert('RGBA')
    dark = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(dark)
    for y in range(0, 720): dd.line((0, y, W, y), fill=(0, 0, 0, int(225 * (1 - y / 720) ** 0.7)))
    img.alpha_composite(dark); d = ImageDraw.Draw(img)
    for txt, size, col, y in [('FORD', 130, WHITE, 245), ('MAVERICK', 150, GOLD, 385)]:
        f = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', size)
        tw = sum(d.textlength(ch, font=f) for ch in txt) + 10 * (len(txt) - 1); x = W / 2 - tw / 2
        for ch in txt:
            d.text((x, y), ch, font=f, fill=col + (255,), stroke_width=8, stroke_fill=(0, 0, 0, 255)); x += d.textlength(ch, font=f) + 10
    f2 = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', 46)
    sub = '2023 · XLT · 84.500 km'; tw = d.textlength(sub, font=f2)
    d.rounded_rectangle((W / 2 - tw / 2 - 32, 578, W / 2 + tw / 2 + 32, 660), 22, fill=(12, 12, 12, 230), outline=GOLD + (255,), width=3)
    d.text((W / 2 - tw / 2, 590), sub, font=f2, fill=WHITE + (255,))
    img.convert('RGB').save('cover2.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', 'cover2.png', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-t', '0.5', '-r', str(FPS), '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'cover2.mp4'], check=True)
CX, CY, RX, RY, SHIFT = 505, 728, 68, 66, -150

def withcover(body, out):
    fc = '[0:v]setsar=1[c];[1:v]setsar=1[b];[0:a]aresample=48000[ca];[1:a]aresample=48000,aformat=channel_layouts=stereo[ba];[c][ca][b][ba]concat=n=2:v=1:a=1[v][a]'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'cover2.mp4', '-i', body, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)

def final(out):
    st, total = starts()
    fc = (f"[1:a]volume=-3dB,atrim=0:{total},afade=t=out:st={total - 1.0:.2f}:d=1.0,alimiter=limit=0.9,aformat=channel_layouts=stereo[a];"
          f"[0:v]setsar=1,fade=t=out:st={total - 0.6:.2f}:d=0.6[v]")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'body2.mp4', '-i', 'music2.wav',
                    '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)

if __name__ == '__main__':
    os.chdir(HERE)
    a = sys.argv[1]
    if a == 'cover': cover()
    elif a == 'withcover': withcover(sys.argv[2], sys.argv[3])
    else: {'pieces': pieces, 'render': render}.get(a, lambda: final(sys.argv[2]))()
