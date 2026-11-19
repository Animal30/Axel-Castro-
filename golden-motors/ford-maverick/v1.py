"""Ford Maverick 2023 reel 1 - Alejandro presents it (feed). python3 v1.py cut|check N,N|render|cover|final out.mp4"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import kit
from kit import W, H, FPS, GOLD, WHITE, glass_card, draw_caption, chunk, icon_car, icon_pin

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw'); AUD = os.path.join(HERE, 'aud'); TX = os.path.join(HERE, 'tx')
OUTRO = '/mnt/project-files/golden-motors/outro-logo/golden-motors-outro-girando-con-sonido.mp4'
FY = 700
GRADE = 'eq=contrast=1.06:saturation=1.08:gamma=0.98,colorbalance=rs=0.015:bs=-0.015'

# unit: audio (file, a, b), caption clip (or None), video pieces [(clip, start, dur_out, zoom, speed)]
def talk(clip, a, b, z=1.0, cut=None):
    return dict(aud=(f'orig{clip}', a, b), cap=clip, vid=cut or [(clip, a, b - a, z, 1.0)])
# Nahuel 2026-11-19: use BOTH takes complete and in order, only trim the silence at the start/end of each.
# Audio runs continuously; cutaways only cover the picture.
UNITS = [
    talk(4516, 1.30, 15.50, cut=[(4516, 1.30, 2.10, 1.12, 1.0), (4516, 3.40, 2.00, 1.0, 1.0), (4495, 0.4, 1.00, 1.0, 0.7),
                                 (4505, 0.6, 1.10, 1.0, 0.7), (4516, 7.50, 3.30, 1.0, 1.0), (4516, 10.80, 1.50, 1.12, 1.0),
                                 (4501, 1.3, 1.20, 1.0, 0.7), (4516, 13.50, 2.00, 1.0, 1.0)]),
    talk(9001, 1.05, 18.62, cut=[(9001, 1.05, 2.45, 1.0, 1.0), (9001, 3.50, 3.10, 1.12, 1.0), (4504, 2.6, 1.40, 1.0, 0.7),
                                 (9001, 8.00, 3.40, 1.0, 1.0), (9001, 11.40, 2.40, 1.12, 1.0), (9001, 13.80, 2.80, 1.0, 1.0),
                                 (9001, 16.60, 2.02, 1.12, 1.0)]),
]

def zoom_vf(z):
    if z == 1.0: return ''
    cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    return f',crop={cw}:{ch}:{int((W - cw) / 2)}:{int(FY - ch * FY / H)},scale={W}:{H}:flags=lanczos'

def nframes(u): return sum(round(p[2] * FPS) for p in u['vid'])

def unit_gain(u, target=-21.5):
    import soundfile as sf
    f, a, b = u['aud']; x, sr = sf.read(f'{AUD}/{f}.wav'); seg = x[int(a * sr):int(b * sr)].mean(1)
    fr = seg[:len(seg) // 2400 * 2400].reshape(-1, 2400); r = np.sort(np.sqrt((fr ** 2).mean(1)))[len(fr) // 2:]
    lvl = 20 * np.log10(np.sqrt((r ** 2).mean()))
    pk = 20 * np.log10(np.abs(x[int(a * sr):int(b * sr)]).max())
    return float(np.clip(min(target - lvl, -1.0 - pk), -12, 14))

def make_cut():
    os.makedirs('pieces', exist_ok=True)
    vlist, alist = [], []
    for ui, u in enumerate(UNITS):
        for pi, (c, s, d, z, sp) in enumerate(u['vid']):
            out = f'pieces/v{ui:02d}_{pi}.mp4'; vlist.append(out)
            if os.environ.get('KEEP') and os.path.exists(out): continue
            vf = (f"trim={s}:{s + d * sp + 0.2},setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale={W}:{H}:flags=lanczos"
                  f"{zoom_vf(z)},{GRADE},trim=0:{d},setpts=PTS-STARTPTS,format=yuv420p")
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{RAW}/c{c}.mov', '-an', '-vf', vf, '-frames:v', str(round(d * FPS)),
                            '-c:v', 'libx264', '-crf', '13', '-preset', 'fast', out], check=True)
        f, a, b = u['aud']; dur = nframes(u) / FPS
        out = f'pieces/a{ui:02d}.wav'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{AUD}/{f}.wav', '-af',
                        f'atrim={a}:{a + dur},asetpts=PTS-STARTPTS,volume={unit_gain(u):.2f}dB,'   # original sound, only a static level match (Nahuel 2026-11-18)
                        f'afade=t=in:d=0.02,afade=t=out:st={dur - 0.04:.3f}:d=0.04,apad,atrim=0:{dur}',
                        '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s24le', out], check=True)
        alist.append(out)
    open('pieces/v.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in vlist))
    open('pieces/a.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in alist))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'pieces/v.txt', '-f', 'concat', '-safe', '0', '-i', 'pieces/a.txt',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'pcm_s16le', 'cut.mov'], check=True)

# STT heard "City": the car is a Honda Civic EXS
FIX = {'Treinta': '38', 'treinta': '38', 'veintitrés.': '2023'}
def unit_starts():
    t, out = 0, []
    for u in UNITS:
        out.append(t); t += nframes(u) / FPS
    return out, t

def caption_words():
    starts, _ = unit_starts(); words = []
    for u, t0 in zip(UNITS, starts):
        _, a, b = u['aud']; dur = nframes(u) / FPS
        d = json.load(open(f"{TX}/tx{u['cap']}.json"))
        for w in d['words']:
            if w['type'] != 'word' or not (a - 0.06 <= w['start'] < a + dur - 0.05): continue
            txt = FIX.get(w['text'], w['text'])
            if txt == 'hacemos' and words and words[-1][2] == 'le': words[-1][2] = 'lo'
            if txt.startswith('Nahuel'):   # never show Nahuel's name on screen (audio stays untouched)
                if words and words[-1][2] == 'a': words.pop()
                continue
            if words and words[-1][2] == '38' and txt.strip('.,') in ('y', 'ocho'): words[-1][1] = t0 + w['end'] - a; continue
            if words and words[-1][2] == 'veinte' and txt in ('2021', '2023'): words[-1][1] = t0 + w['end'] - a; words[-1][2] = txt; continue
            if words and words[-1][2] in ('4', 'cuatro') and txt == 'mil': words[-1][2] = '4'
            if words and words[-1][2] == 'cuatro' and txt == 'por': words[-1][2] = '4x4'; words[-1][1] = t0 + w['end'] - a; continue
            if words and words[-1][2] == '4x4' and txt == 'cuatro': words[-1][1] = t0 + w['end'] - a; continue
            words.append([t0 + w['start'] - a, t0 + min(w['end'], a + dur) - a, txt])
    return words

def icon_chat(d, x, y):
    k = (12, 12, 12)
    d.rounded_rectangle((x - 24, y - 20, x + 24, y + 12), 10, fill=k)
    d.polygon([(x - 12, y + 10), (x - 16, y + 24), (x + 2, y + 10)], fill=k)
    for dx in (-11, 0, 11): d.ellipse((x + dx - 4, y - 8, x + dx + 4, y), fill=GOLD)
def icon_check(d, x, y):
    k = (12, 12, 12); d.line((x - 16, y, x - 4, y + 12, x + 18, y - 12), fill=k, width=7)
def icon_tag(d, x, y):
    k = (12, 12, 12)
    d.polygon([(x - 22, y - 6), (x - 6, y - 22), (x + 22, y - 22), (x + 22, y + 6), (x + 6, y + 22)], fill=k)
    d.ellipse((x + 6, y - 15, x + 15, y - 6), fill=GOLD)

def render(only=None):
    words = caption_words(); groups = chunk(words)
    st, total = unit_starts()
    def at(word, after=0): return next(w for w in words if w[2].startswith(word) and w[0] >= after)
    cards = [
        ('$38.000.000', 'Golden Motors · Córdoba', icon_tag, 0.05, at('tenemos')[0] - 0.1),
        ('Ford Maverick 2023', 'XLT · 84.500 km', icon_car, at('Ford')[0] - 0.1, at('Estás')[0] - 0.15),
        ('Punto intermedio', 'Mismas funciones', icon_check, at('punto')[0] - 0.1, st[1] - 0.15),
        ('Caja de 8 velocidades', 'Como la Ford Bronco', icon_check, at('caja')[0] - 0.1, at('toda')[0] - 0.1),
        ('Conectividad total', 'La de los autos 2023', icon_check, at('toda')[0] - 0.05, at('Voy')[0] - 0.1),
        ('Consultá por mensaje', 'Hay un precio especial', icon_chat, at('unos')[0] - 0.1, total + 0.5),
    ]
    print([(c[0], round(c[3], 2), round(c[4], 2)) for c in cards], round(total, 2))
    n = int(round(total * FPS))
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', 'cut.mov', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', 'body.mp4'], stdin=subprocess.PIPE)
    for i in range(n):
        raw = dec.stdout.read(W * H * 3)
        if len(raw) < W * H * 3: break
        t = i / FPS
        if only and i not in only: enc.stdin.write(raw); continue
        img = Image.frombytes('RGB', (W, H), raw).convert('RGBA')
        for title, sub, ic, t0, t1 in cards:
            glass_card(img, W / 2, 330, title, sub, ic, t, t0, t1, accent_title=True)
        draw_caption(img, groups, t)
        out = img.convert('RGB')
        if only: out.save(f'chk_{i:04d}.jpg', quality=88)
        enc.stdin.write(out.tobytes())
    enc.stdin.close(); enc.wait(); dec.stdout.close(); dec.kill(); dec.wait()

F_H1 = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 104)
F_H2 = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 150)
F_H3 = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 118)
COVER = (4516, 2.5)
def cover():
    c, t = COVER
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-ss', str(t), '-i', f'{RAW}/c{c}.mov', '-frames:v', '1',
                                   '-vf', f'scale={W}:{H}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    import cv2
    im = np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy(); m = np.zeros((H, W), np.uint8)
    cv2.ellipse(m, (457, 876), (70, 64), 0, 0, 360, 255, -1)   # ceiling lamp reflected on the windshield
    im = cv2.seamlessClone(np.roll(im, 170, axis=1), im, m, (457, 876), cv2.NORMAL_CLONE)
    im = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-i', '-', '-vf', GRADE,
                                       '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], input=im.tobytes(), capture_output=True, check=True).stdout, np.uint8).reshape(H, W, 3)
    img = Image.fromarray(im).convert('RGBA')
    d = ImageDraw.Draw(img)   # no dark band (Nahuel 2026-11-18)
    def fit(txt, size, maxw=980):
        while True:
            f = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', size)
            if d.textlength(txt, font=f) <= maxw: return f
            size -= 4
    for txt, font, col, y in [('¿TE QUEDA GRANDE', fit('¿TE QUEDA GRANDE', 104), WHITE, 190), ('UNA HILUX?', fit('UNA HILUX?', 160), GOLD, 300)]:
        tw = d.textlength(txt, font=font)
        d.text((W / 2 - tw / 2, y), txt, font=font, fill=col + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255))
    sub = 'Ford Maverick 2023 · $38.000.000'; tw = d.textlength(sub, font=kit.F_HOOK2)
    d.rounded_rectangle((W / 2 - tw / 2 - 30, 505, W / 2 + tw / 2 + 30, 585), 20, fill=(12, 12, 12, 225), outline=GOLD + (255,), width=3)
    d.text((W / 2 - tw / 2, 516), sub, font=kit.F_HOOK2, fill=WHITE + (255,))
    img.convert('RGB').save('cover.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', 'cover.png', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-t', '0.5', '-r', str(FPS), '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'cover.mp4'], check=True)

def final(out):
    fc = ('[0:v]setsar=1[c];[1:v]setsar=1[b];[3:v]setsar=1,fps=30[o];'
          '[0:a]aresample=48000,aformat=channel_layouts=stereo[ca];[2:a]aresample=48000,aformat=channel_layouts=stereo[ba];'
          '[3:a]aresample=48000,aformat=channel_layouts=stereo[oa];[c][ca][b][ba][o][oa]concat=n=3:v=1:a=1[v][a]')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'cover.mp4', '-i', 'body.mp4', '-i', 'cut.mov', '-i', OUTRO,
                    '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)

if __name__ == '__main__':
    os.chdir(HERE)
    s = sys.argv[1]
    if s == 'cut': make_cut()
    elif s == 'check': render(set(int(x) for x in sys.argv[2].split(',')))
    elif s == 'render': render()
    elif s == 'cover': cover()
    elif s == 'final': final(sys.argv[2])
    elif s == 'words': print(' | '.join(f'{w[2]}@{w[0]:.2f}' for w in caption_words()), [round(x, 2) for x in unit_starts()[0]])
