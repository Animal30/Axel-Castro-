"""Honda Civic EXS reel 1 - Alejandro sells it. python3 v1.py cut|check N,N|render|cover|final out.mp4"""
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
    return dict(aud=(f'iso{clip}', a, b), cap=clip, vid=cut or [(clip, a, b - a, z, 1.0)])
UNITS = [
    talk(4532, 1.08, 5.98, 1.0),                                   # hook: Vento Corolla Focus -> Honda Civic
    talk(4532, 6.52, 10.14, 1.0),                                  # el más full de todos, EXS automático
    talk(4532, 12.24, 14.92, cut=[(4532, 12.24, 1.70, 1.12, 1.0), (4527, 2.4, 0.98, 1.0, 0.7)]),   # 120 mil km, techo, cuero
    talk(4532, 15.04, 18.86, cut=[(4532, 15.04, 2.20, 1.0, 1.0), (4529, 5.4, 1.62, 1.0, 0.7)]),    # lo que le pidas... cámara marcha atrás
    talk(4534, 1.24, 4.48, 1.0),                                   # control de estabilidad, modo eco
    talk(4534, 10.46, 11.58, 1.12),                                # velocidad crucero
    talk(4534, 12.20, 12.76, cut=[(4530, 2.6, 0.56, 1.0, 0.7)]),   # el control
    talk(4534, 13.32, 15.64, cut=[(4530, 3.0, 2.32, 1.0, 0.7)]),   # para hablar por teléfono y manejar la radio
    talk(4534, 16.06, 18.90, 1.0),                                 # viene re completo para ser un 2016
    talk(4535, 1.80, 9.00, 1.0),                                   # vení con tu novia... ovni
    talk(4532, 19.40, 21.62, cut=[(4523, 1.2, 2.22, 1.0, 0.7)]),  # garantía de que es un Honda (rear badge)
    talk(4536, 5.04, 8.96, 1.0),                                   # 23 millones y medio, no busques más
]

def zoom_vf(z):
    if z == 1.0: return ''
    cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    return f',crop={cw}:{ch}:{int((W - cw) / 2)}:{int(FY - ch * FY / H)},scale={W}:{H}:flags=lanczos'

def nframes(u): return sum(round(p[2] * FPS) for p in u['vid'])

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
                        f'atrim={a}:{a + dur},asetpts=PTS-STARTPTS,highpass=f=80,equalizer=f=3000:t=q:w=1.2:g=2,'
                        f'acompressor=threshold=0.1:ratio=3:attack=10:release=150:makeup=1.5,'
                        f'afade=t=in:d=0.02,afade=t=out:st={dur - 0.04:.3f}:d=0.04,apad,atrim=0:{dur}',
                        '-ar', '48000', '-ac', '1', out], check=True)
        alist.append(out)
    open('pieces/v.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in vlist))
    open('pieces/a.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in alist))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'pieces/v.txt', '-f', 'concat', '-safe', '0', '-i', 'pieces/a.txt',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'pcm_s16le', 'cut.mov'], check=True)

# STT heard "City": the car is a Honda Civic EXS
FIX = {'City.': 'Civic', 'pidás': 'pidas', 'Veintitrés': '23', 'ciento': '120', 'OVNI,': 'OVNI'}
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
            if words and words[-1][2] == '120' and txt == 'veinte': words[-1][1] = t0 + w['end'] - a; continue
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
        ('Honda Civic EXS', '2016 · Automático', icon_car, at('EXS')[0] - 0.15, st[2] - 0.15),
        ('132.000 km', 'Techo solar · Cuero', icon_check, st[2] + 0.05, st[3] - 0.15),
        ('Cámara de retroceso', 'Full equipo', icon_check, at('Cámara')[0] - 0.1, st[4] - 0.15),
        ('Control de estabilidad', 'Modo ECO', icon_check, st[4] + 0.05, st[5] - 0.15),
        ('Velocidad crucero', 'Comandos al volante', icon_check, st[5] + 0.05, st[8] - 0.15),
        ('Techo solar', 'Para ver las estrellas', icon_check, at('Acá', st[9])[0] - 0.1, st[10] - 0.15),
        ('$23.500.000', 'Golden Motors · Córdoba', icon_tag, st[11] + 0.05, at('No', st[11])[0] - 0.1),
        ('Escribinos', 'Te respondemos por mensaje', icon_chat, at('No', st[11])[0], total),
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
COVER = (4532, 2.5)
def cover():
    c, t = COVER
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-ss', str(t), '-i', f'{RAW}/c{c}.mov', '-frames:v', '1',
                                   '-vf', f'scale={W}:{H}:flags=lanczos,{GRADE}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    img = Image.frombytes('RGB', (W, H), raw).convert('RGBA')
    dark = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(dark)
    for y in range(0, 760): dd.line((0, y, W, y), fill=(0, 0, 0, int(170 * (1 - y / 760))))
    img.alpha_composite(dark); d = ImageDraw.Draw(img)
    for txt, font, col, y in [('¿BUSCÁS UN', F_H1, WHITE, 200), ('SEDÁN FULL?', F_H2, GOLD, 315)]:
        tw = d.textlength(txt, font=font)
        d.text((W / 2 - tw / 2, y), txt, font=font, fill=col + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255))
    sub = 'Honda Civic EXS · 2016 · 132.000 km'; tw = d.textlength(sub, font=kit.F_HOOK2)
    d.rounded_rectangle((W / 2 - tw / 2 - 30, 520, W / 2 + tw / 2 + 30, 600), 20, fill=(12, 12, 12, 225), outline=GOLD + (255,), width=3)
    d.text((W / 2 - tw / 2, 531), sub, font=kit.F_HOOK2, fill=WHITE + (255,))
    img.convert('RGB').save('cover.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', 'cover.png', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-t', '0.5', '-r', str(FPS), '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'cover.mp4'], check=True)

def final(out):
    fc = ('[0:v]setsar=1[c];[1:v]setsar=1[b];[3:v]setsar=1,fps=30[o];'
          '[0:a]aresample=48000,aformat=channel_layouts=stereo[ca];[2:a]aresample=48000,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo[ba];'
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
