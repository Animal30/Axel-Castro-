"""Alfa Romeo GTV 1979 - Alejandro voice-over. python3 v1.py cut|check N,N|render|cover|final out.mp4"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import kit
from kit import W, H, FPS, GOLD, WHITE, glass_card, draw_caption, chunk, icon_car, icon_pin

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw'); AUD = os.path.join(HERE, 'aud'); TX = os.path.join(HERE, 'tx')
OUTRO = '/mnt/project-files/golden-motors/outro-logo/golden-motors-outro-girando-con-sonido.mp4'
FY = 700
AUDSRC = os.environ.get('AUDSRC', 'clean')
GRADE = 'eq=contrast=1.08:saturation=1.08:gamma=1.06,colorbalance=rs=0.02:bs=-0.02:rh=0.02:bh=-0.03,vignette=PI/8'

# unit: audio (file, a, b), caption clip (or None), video pieces [(clip, start, dur_out, zoom, speed)]
def talk(clip, a, b, z=1.0, cut=None):
    return dict(aud=(f'{AUDSRC}{clip}', a, b), cap=clip, vid=cut or [(clip, a, b - a, z, 1.0)])
UNITS = [
    talk(4613, 1.15, 3.80, cut=[(4605, 0.0, 2.65, 1.0, 0.6)]),                                   # es un Alfa Romeo del 1979
    talk(4613, 3.85, 6.10, cut=[(4607, 0.3, 2.25, 1.0, 0.6)]),                                   # es una GTV dos litros
    talk(4613, 6.25, 7.85, cut=[(4603, 0.2, 1.60, 1.0, 0.6)]),                                   # un clasico de la epoca
    talk(4613, 9.20, 10.85, cut=[(4606, 0.3, 1.65, 1.0, 0.6)]),                                  # el estado de conservacion es como se ve
    talk(4613, 11.60, 13.55, cut=[(4598, 0.3, 1.95, 1.0, 0.6)]),                                 # se restauro en el 2021
    talk(4613, 13.60, 17.55, cut=[(4600, 0.2, 2.00, 1.0, 0.6), (4602, 1.0, 1.95, 1.0, 0.6)]),   # mejoras en el motor, pistones forjados
    talk(4613, 17.90, 19.10, cut=[(4601, 0.3, 1.20, 1.0, 0.6)]),                                 # aros NPR
    talk(4613, 19.75, 21.70, cut=[(4601, 1.5, 1.95, 1.0, 0.6)]),                                 # levas Colombo, se le hicieron las mejoras
    talk(4613, 21.70, 24.75, cut=[(4596, 2.5, 3.05, 1.0, 0.6)]),                                 # se usaba para correr carreras de regularidad
    talk(4613, 26.25, 27.95, cut=[(4610, 0.3, 1.70, 1.0, 0.6)]),                                 # si lo quieren venir a ver
    talk(4613, 28.95, 31.55, cut=[(4611, 5.0, 2.60, 1.0, 0.6)]),                                 # con gusto recibimos consultas
    talk(4613, 31.80, 32.85, cut=[(4612, 6.6, 1.05, 1.0, 0.6)]),                                 # y bueno esta a la vista
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
                        f'atrim={a}:{a + dur},asetpts=PTS-STARTPTS,volume={unit_gain(u):.2f}dB,'   # original audio, static level match only
                        f'afade=t=in:d=0.02,afade=t=out:st={dur - 0.04:.3f}:d=0.04,apad,atrim=0:{dur}',
                        '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s24le', out], check=True)
        alist.append(out)
    open('pieces/v.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in vlist))
    open('pieces/a.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in alist))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'pieces/v.txt', '-f', 'concat', '-safe', '0', '-i', 'pieces/a.txt',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'pcm_s16le', 'cut.mov'], check=True)

# STT heard "City": the car is a Honda Civic EXS
FIX = {'GTB,': 'GTV', 'colombos,': 'Colombo'}
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
            if txt == 'la' and words and words[-1][2] == 'está': txt = 'a la'
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
        ('Alfa Romeo GTV', '1979 · 2.0 litros', icon_car, at('Alfa')[0] - 0.1, st[3] - 0.15),
        ('Restaurado en 2021', 'Clásico de colección', icon_check, st[3] + 0.05, st[5] - 0.15),
        ('Motor preparado', 'Pistones forjados · Aros NPR', icon_check, st[5] + 0.05, st[7] - 0.15),
        ('Levas Colombo', 'Mejoras de competición', icon_check, st[7] + 0.05, st[8] - 0.15),
        ('Carreras de regularidad', 'Auto de competición', icon_check, st[8] + 0.05, st[9] - 0.15),
        ('Escribinos', 'Te respondemos por mensaje', icon_chat, st[9] + 0.05, total),
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

F_H1 = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 90)
F_H2 = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf', 134)
COVER = (4612, 8.8)
def cover():
    c, t = COVER
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-ss', str(t), '-i', f'{RAW}/c{c}.mov', '-frames:v', '1',
                                   '-vf', f'scale={W}:{H}:flags=lanczos,{GRADE}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    img = Image.frombytes('RGB', (W, H), raw).convert('RGBA')
    d = ImageDraw.Draw(img)   # no dark band (Nahuel 2026-11-18)
    for txt, font, col, y in [('ALFA ROMEO GTV', F_H1, WHITE, 200), ('DE CARRERAS', F_H2, GOLD, 315)]:
        tw = d.textlength(txt, font=font)
        d.text((W / 2 - tw / 2, y), txt, font=font, fill=col + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255))
    sub = '1979 · 2.0 · Restaurado en 2021'; tw = d.textlength(sub, font=kit.F_HOOK2)
    d.rounded_rectangle((W / 2 - tw / 2 - 30, 520, W / 2 + tw / 2 + 30, 600), 20, fill=(12, 12, 12, 225), outline=GOLD + (255,), width=3)
    d.text((W / 2 - tw / 2, 531), sub, font=kit.F_HOOK2, fill=WHITE + (255,))
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
