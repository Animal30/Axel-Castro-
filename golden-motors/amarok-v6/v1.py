"""Amarok V6 reel 1 - Alejandro presents. python3 v1.py cut|check N,N|render|cover|final out.mp4"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import kit
from kit import W, H, FPS, GOLD, WHITE, glass_card, draw_caption, chunk, icon_car, icon_pin, ease

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw'); AUD = os.path.join(HERE, 'aud'); TH = os.path.join(HERE, 'thumbs')
OUTRO = '/mnt/project-files/golden-motors/outro-logo/golden-motors-outro-girando-con-sonido.mp4'
FY = 700
GRADE = 'eq=contrast=1.05:saturation=1.07,colorbalance=rs=0.015:bs=-0.015'

# unit: audio (file, a, b, gain_db), voice clip id for captions (or None), video pieces [(clip, start, dur_out, zoom, speed)]
def talk(clip, a, b, z=1.0):
    return dict(aud=(f'v{clip}', a, b, 0), cap=clip, vid=[(clip, a, b - a, z, 1.0)])
UNITS = [
    talk(4481, 0.42, 5.40, 1.0),
    dict(aud=('v4481', 5.40, 11.95, 0), cap=4481, vid=[
        (4481, 5.40, 1.20, 1.12, 1.0),
        (4477, 0.6, 1.25, 1.0, 0.7),
        (4471, 0.3, 1.55, 1.0, 0.7),
        (4469, 0.4, 1.30, 1.0, 0.7),
        (4464, 0.2, 1.25, 1.0, 0.7)]),
    talk(4484, 2.20, 3.80, 1.0),
    dict(aud=('e4484', 8.60, 10.40, 6), cap=None, vid=[(4484, 8.60, 1.80, 1.12, 1.0)]),
    dict(aud=('e4487', 0.30, 2.80, 9), cap=None, vid=[(4487, 0.30, 2.50, 1.0, 1.0)]),
    dict(aud=('e4488', 0.50, 1.80, 9), cap=None, vid=[(4488, 0.50, 1.30, 1.0, 1.0)]),
    talk(4486, 0.55, 3.55, 1.0),
    talk(4486, 3.55, 5.15, 1.12),
    talk(4481, 12.30, 13.72, 1.12),
]

def zoom_vf(z):
    if z == 1.0: return ''
    cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    return f',crop={cw}:{ch}:{int((W - cw) / 2)}:{int(FY - ch * FY / H)},scale={W}:{H}:flags=lanczos'

def make_cut():
    os.makedirs('pieces', exist_ok=True)
    vlist, alist = [], []
    for ui, u in enumerate(UNITS):
        for pi, (c, s, d, z, sp) in enumerate(u['vid']):
            out = f'pieces/v{ui:02d}_{pi}.mp4'
            vf = (f"trim={s}:{s + d * sp + 0.2},setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale={W}:{H}:flags=lanczos"
                  f"{zoom_vf(z)},{GRADE},trim=0:{d},setpts=PTS-STARTPTS,format=yuv420p")
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{RAW}/c{c}.mov', '-an', '-vf', vf, '-frames:v', str(round(d * FPS)),
                            '-c:v', 'libx264', '-crf', '13', '-preset', 'fast', out], check=True)
            vlist.append(out)
        f, a, b, g = u['aud']
        out = f'pieces/a{ui:02d}.wav'
        nfr = sum(round(p[2] * FPS) for p in u['vid']); dur = nfr / FPS
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{AUD}/{f}.wav', '-af',
                        f'atrim={a}:{a + dur},asetpts=PTS-STARTPTS,volume={g}dB,afade=t=in:d=0.02,afade=t=out:st={dur - 0.03:.3f}:d=0.03,apad,atrim=0:{dur}',
                        '-ar', '48000', '-ac', '1', out], check=True)
        alist.append(out)
    open('pieces/v.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in vlist))
    open('pieces/a.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in alist))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'pieces/v.txt', '-f', 'concat', '-safe', '0', '-i', 'pieces/a.txt',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'pcm_s16le', 'cut.mov'], check=True)

FIX = {'cincuenta': '57'}
def unit_starts():
    t, out = 0, []
    for u in UNITS:
        out.append(t); t += sum(round(p[2] * FPS) for p in u['vid']) / FPS
    return out, t

def caption_words():
    starts, _ = unit_starts(); words = []
    for u, t0 in zip(UNITS, starts):
        if not u['cap']: continue
        _, a, b, _ = u['aud']
        d = json.load(open(f"{TH}/tx{u['cap']}.json"))
        for w in d['words']:
            if w['type'] != 'word' or not (a - 0.06 <= w['start'] < b - 0.05): continue
            txt = FIX.get(w['text'], w['text'])
            if words and words[-1][2] == 'V' and txt == 'seis': words[-1][1] = t0 + w['end'] - a; words[-1][2] = 'V6'; continue
            if words and words[-1][2] == '57' and txt in ('y', 'siete'): words[-1][1] = t0 + w['end'] - a; continue
            words.append([t0 + w['start'] - a, t0 + min(w['end'], b) - a, txt])
    return words

def icon_vol(d, x, y):
    k = (12, 12, 12)
    d.rectangle((x - 20, y - 8, x - 10, y + 8), fill=k); d.polygon([(x - 10, y - 8), (x + 2, y - 18), (x + 2, y + 18), (x - 10, y + 8)], fill=k)
    d.arc((x - 2, y - 12, x + 14, y + 12), -60, 60, fill=k, width=4); d.arc((x - 4, y - 20, x + 22, y + 20), -60, 60, fill=k, width=4)
def icon_chat(d, x, y):
    k = (12, 12, 12)
    d.rounded_rectangle((x - 24, y - 20, x + 24, y + 12), 10, fill=k)
    d.polygon([(x - 12, y + 10), (x - 16, y + 24), (x + 2, y + 10)], fill=k)
    for dx in (-11, 0, 11): d.ellipse((x + dx - 4, y - 8, x + dx + 4, y), fill=GOLD)
def icon_check(d, x, y):
    k = (12, 12, 12); d.line((x - 16, y, x - 4, y + 12, x + 18, y - 12), fill=k, width=7)

def render(only=None):
    words = caption_words(); groups = chunk(words)
    st, total = unit_starts()
    def at(word, after=0): return next(w for w in words if w[2].startswith(word) and w[0] >= after)
    T = dict(v6=at('V6', st[1])[0], km=at('57')[0], pm=at('primera')[0], so=at('todos', st[1])[0],
             eng0=st[4], eng1=st[6] - 0.3, cta0=at('tiranos')[0] - 0.2, cta1=st[8] - 0.3, end0=st[8], end1=total)
    cards = [
        ('Amarok V6 2022', 'Volkswagen · 4x4', icon_car, T['v6'] - 0.1, T['km'] - 0.35),
        ('57 mil km', 'Kilómetros reales', icon_check, T['km'] - 0.05, T['pm'] - 0.35),
        ('Primera mano', 'Un solo dueño', icon_check, T['pm'] - 0.05, T['so'] - 0.35),
        ('Services oficiales', 'Todos al día', icon_check, T['so'] - 0.05, st[2] - 0.1),
        ('Subí el volumen', 'Escuchá el V6', icon_vol, T['eng0'], T['eng1']),
        ('Escribinos', 'Te respondemos por mensaje', icon_chat, T['cta0'], T['cta1']),
        ('Octavio Pinto 3181', 'Golden Motors · Córdoba', icon_pin, T['end0'], T['end1']),
    ]
    print({k: round(v, 2) for k, v in T.items()}, round(total, 2))
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

F_H1 = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 100)
F_H2 = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 150)
def cover():
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-ss', '1.6', '-i', f'{RAW}/c4481.mov', '-frames:v', '1',
                                   '-vf', f'scale={W}:{H}:flags=lanczos,{GRADE}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    img = Image.frombytes('RGB', (W, H), raw).convert('RGBA')
    dark = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(dark)
    for y in range(0, 760): dd.line((0, y, W, y), fill=(0, 0, 0, int(165 * (1 - y / 760))))
    img.alpha_composite(dark); d = ImageDraw.Draw(img)
    for txt, font, col, y in [('¿BUSCÁS UNA', F_H1, WHITE, 230), ('AMAROK V6?', F_H2, GOLD, 345)]:
        tw = d.textlength(txt, font=font)
        d.text((W / 2 - tw / 2, y), txt, font=font, fill=col + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255))
    sub = '2022 · 57 mil km · Primera mano'; tw = d.textlength(sub, font=kit.F_HOOK2)
    d.rounded_rectangle((W / 2 - tw / 2 - 30, 545, W / 2 + tw / 2 + 30, 625), 20, fill=(12, 12, 12, 225))
    d.text((W / 2 - tw / 2, 556), sub, font=kit.F_HOOK2, fill=WHITE + (255,))
    img.convert('RGB').save('cover.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', 'cover.png', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-t', '0.5', '-r', str(FPS), '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'cover.mp4'], check=True)

def final(out):
    fc = ('[0:v]setsar=1[c];[1:v]setsar=1[b];[3:v]setsar=1,fps=30[o];'
          '[0:a]aresample=48000[ca];[2:a]aresample=48000,aformat=channel_layouts=stereo,alimiter=limit=0.9[ba];[3:a]aresample=48000[oa];'
          '[c][ca][b][ba][o][oa]concat=n=3:v=1:a=1[v][a]')
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
    elif s == 'words': print(' '.join(w[2] for w in caption_words()), unit_starts())
