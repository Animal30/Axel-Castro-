"""Amarok V6 reel 2 - showcase, no talking, cut to the beat. python3 v2.py pieces|render|final"""
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
    (4462, 0.0, 4, 0.6, None),
    (4477, 0.5, 2, 0.6, None),
    (4464, 0.1, 2, 0.6, ('V6', 'Motor')),
    (4466, 0.2, 2, 0.6, ('4x4', 'Tracción')),
    (4465, 0.3, 2, 0.8, None),
    (4470, 0.4, 2, 0.6, ('2022', 'Modelo')),
    (4467, 0.3, 2, 0.6, None),
    (4468, 0.4, 2, 0.7, None),
    (4476, 2.0, 2, 1.0, None),
    (4475, 0.3, 2, 0.8, None),
    (4474, 1.0, 2, 1.0, ('Primera mano', 'Un solo dueño')),
    (4471, 0.2, 2, 0.6, ('57 mil km', 'Reales')),
    (4472, 0.4, 2, 0.8, ('Automática', 'Caja')),
    (4473, 0.4, 2, 0.8, None),
    (4489, 0.3, 2, 0.8, None),
    (4487, 0.5, 2, 1.0, ('Services', 'Oficiales')),
    (4490, 0.3, 2, 0.8, None),
    (4478, 0.4, 2, 0.6, None),
    (4477, 1.6, 4, 0.6, None),
]
FLASH_AT = {1, 4, 8, 11, 14, 17, 18}   # shot indices that start with a soft flash

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
            spaced(d, 300, 'AMAROK', F_T1, WHITE, 18 - 8 * p, a, 4)
            spaced(d, 465, 'V6', F_T1, GOLD, 18 - 8 * p, a, 4)
            y = 650; L = int(140 * p)
            d.line((W / 2 - 40 - L, y + 22, W / 2 - 40, y + 22), fill=GOLD + (a,), width=3)
            d.line((W / 2 + 40, y + 22, W / 2 + 40 + L, y + 22), fill=GOLD + (a,), width=3)
            spaced(d, y, '2022', F_T2, WHITE, 10, a, 2)
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
        z = 1.0 + 0.07 * p if i != len(SHOTS) - 1 else 1.0 + 0.04 * p
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

def final(out):
    st, total = starts()
    i = [s[0] for s in SHOTS].index(4487); te = st[i]
    # music + engine growl under shot 4487/4490, then outro
    fc = (f"[1:a]volume=-3dB,afade=t=out:st={total - 0.8:.2f}:d=0.8,atrim=0:{total}[m];"
          f"[2:a]atrim=0.4:{0.4 + 2 * BEAT * 2:.2f},asetpts=PTS-STARTPTS,volume=10dB,afade=t=in:d=0.1,afade=t=out:st={2 * BEAT * 2 - 0.3:.2f}:d=0.3,adelay={int(te * 1000)}|{int(te * 1000)},apad,atrim=0:{total}[e];"
          f"[m][e]amix=2:normalize=0,alimiter=limit=0.9,aformat=channel_layouts=stereo[ba];"
          f"[0:v]setsar=1[b];[3:v]setsar=1,fps=30[o];[3:a]aresample=48000[oa];[b][ba][o][oa]concat=n=2:v=1:a=1[v][a]")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'body2.mp4', '-i', 'music2.wav', '-i', f'{AUD}/e4487.wav', '-i', OUTRO,
                    '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)

if __name__ == '__main__':
    os.chdir(HERE)
    {'pieces': pieces, 'render': render}.get(sys.argv[1], lambda: final(sys.argv[2]))()
