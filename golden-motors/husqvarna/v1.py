"""VW Vento 1.4 Comfortline 2017 - Alejandro talking reel. python3 v1.py cut|check N,N|render|cover|final out.mp4"""
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
S = 0.6
UNITS = [
    talk('0113', 0.00, 1.28),                 # arrancan los dias de verano
    talk('0113', 1.89, 3.48),                 # y no te decidiste todavia
    talk('0113', 5.09, 6.78),                 # aca tenes la moto Husqvarna
    talk('0113', 7.64, 20.33),                # premium de KTM, Svartpilen 401, 45 CV, 2022, 4600 km, service
    talk('0113', 20.79, 22.98),               # bateria cambiada
    talk('0113', 23.49, 30.88),               # cubiertas off road, sierra
    talk('0113', 31.64, 38.08),               # sliders, lastima la moto
    talk('0113', 38.79, 40.28),               # frenos Brembo
    talk('0113', 41.19, 42.68),               # quickshift
    talk('0113', 43.34, 45.68),               # iluminacion LED
    talk('0117', 0.00, 6.83),                 # USD 4500, no motos en parte de pago
    talk('0117', 7.29, 9.83),                 # si queres venir a verla, Octavio Pinto
    talk('0117', 10.29, 12.00),               # lunes a viernes de 9 a 18
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
FIX = {'$4': '4', 'cargas': 'cargás', 'cuatro': '4', 'Comfort': 'Comfortline', 'cesta.': 'sexta.', 'viento?': 'Vento?'}
def unit_starts():
    t, out = 0, []
    for u in UNITS:
        out.append(t); t += nframes(u) / FPS
    return out, t

def caption_words():
    starts, _ = unit_starts(); words = []
    for u, t0 in zip(UNITS, starts):
        _, a, b = u['aud']; dur = nframes(u) / FPS
        d = json.load(open(f"{TX}/med{u['cap']}.json"))
        for w in d['words']:
            if w['type'] != 'word' or not (w['end'] > a + 0.05 and w['start'] < a + dur - 0.02): continue
            txt = FIX.get(w['text'], w['text'])
            if txt.lower().startswith('barna') and words and words[-1][2] == 'Uno': words[-1][2] = 'Husqvarna'; words[-1][1] = t0 + w['end'] - a; continue
            if txt.lower().startswith('-road') and words and words[-1][2] == 'off': words[-1][2] = 'off road'; words[-1][1] = t0 + w['end'] - a; continue
            if txt[:1] in '.,' and txt[1:2].isdigit() and words and words[-1][2].isdigit(): words[-1][2] += txt[1:].rstrip('.,'); words[-1][1] = t0 + w['end'] - a; continue
            if txt.startswith('Line'): words[-1][1] = t0 + w['end'] - a; continue      # Comfort + Line -> Comfortline
            if txt.startswith('.4') and words and words[-1][2] == '1': words[-1][2] = '1.4'; words[-1][1] = t0 + w['end'] - a; continue
            if words and words[-1][2].lower().strip(',.') == txt.lower().strip(',.') and t0 + w['start'] - a - words[-1][1] < 0.6: words[-1][1] = t0 + w['end'] - a; continue  # stutter (lo lo)
            words.append([t0 + max(w['start'], a) - a, t0 + min(w['end'], a + dur) - a, txt])
    # Nahuel 2026-11-25: no filler words (bueno) in subtitles; no opening ¿ on the hook (it is a statement); "21 millones 500" stays together
    res = []
    for w in words:
        base = w[2].lower().strip('.,;:¿?!')
        if base == 'bueno':
            if res and res[-1][2].lower().strip('.,;:¿?!') == 'y' and w[0] - res[-1][1] < 0.4: res.pop()
            continue
        res.append(w)
    words = res
    for k in range(len(words) - 1):
        if words[k][2].lower() == 'se' and words[k + 1][2].lower().startswith('decidiste'): words[k][2] = 'te'
    if words and words[0][2].startswith('¿'): words[0][2] = words[0][2].lstrip('¿')
    i = 0
    while i < len(words) - 2:
        if words[i][2] == '21' and words[i + 1][2].lower().startswith('millones') and words[i + 2][2].strip('.,') in ('500', '500.', 'quinientos'):
            words[i:i + 3] = [[words[i][0], words[i + 2][1], '21 millones 500']]
        i += 1
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
        ('Husqvarna Svartpilen 401', '2022 · 4.600 km · 45 CV', icon_car, at('Svartpilen')[0] - 0.25, at('Svartpilen')[0] + 3.3),
        ('Service recién hecho', 'Batería cambiada hace poco', icon_check, at('service')[0] - 0.2, at('poquito')[1] + 0.25),
        ('Cubiertas off road', 'Para animarte a la sierra', icon_check, at('cubiertas')[0] - 0.2, at('cómodamente')[1] + 0.2),
        ('Sliders de protección', 'Por si se cae despacio', icon_check, at('sliders')[0] - 0.2, at('despacio')[1] + 0.3),
        ('Frenos Brembo', 'Equipamiento premium', icon_check, at('frenos')[0] - 0.2, at('quickshift')[0] - 0.3),
        ('Quick shift', 'Cambios sin embrague', icon_check, at('quickshift')[0] - 0.2, at('quickshift')[1] + 1.0),
        ('Iluminación LED', 'En toda la moto', icon_check, at('iluminación')[0] - 0.35, st[10] - 0.1),
        ('USD 4.500', 'Aceptamos auto en parte de pago', icon_tag, st[10] + 0.1, st[11] - 0.1),
        ('Lunes a viernes', '9 a 18 · Octavio Pinto 3181', icon_pin, st[12] - 0.0 - 0.0, total - 0.05),
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

F_H1 = ImageFont.truetype('/home/user/Axel-Castro-/golden-motors/fonts/BarlowCondensed-ExtraBold.ttf', 128)
F_H2 = ImageFont.truetype('/home/user/Axel-Castro-/golden-motors/fonts/BarlowCondensed-ExtraBold.ttf', 196)
COVER = ('0113', 8.4)
def cover():
    c, t = COVER
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-ss', str(t), '-i', f'{RAW}/c{c}.mov', '-frames:v', '1',
                                   '-vf', f'scale={W}:{H}:flags=lanczos,{GRADE}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    img = Image.frombytes('RGB', (W, H), raw).convert('RGBA')
    d = ImageDraw.Draw(img)   # no dark band (Nahuel 2026-11-18)
    for txt, font, col, y in [('¿NO TE DECIDISTE', F_H1, WHITE, 300), ('TODAVÍA?', F_H2, GOLD, 430)]:
        while d.textlength(txt, font=font) > 940: font = ImageFont.truetype(font.path, font.size - 4)
        tw = d.textlength(txt, font=font)
        d.text((W / 2 - tw / 2, y), txt, font=font, fill=col + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255))
    sub = 'Svartpilen 401 · 2022 · 4.600 km'; tw = d.textlength(sub, font=kit.F_HOOK2)
    d.rounded_rectangle((W / 2 - tw / 2 - 34, 640, W / 2 + tw / 2 + 34, 730), 22, fill=(12, 12, 12, 225), outline=GOLD + (255,), width=3)
    d.text((W / 2 - tw / 2, 646), sub, font=kit.F_HOOK2, fill=WHITE + (255,))
    img.convert('RGB').save('cover.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', 'cover.png', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-t', '0.5', '-r', str(FPS), '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'cover.mp4'], check=True)

def final(out):
    fc = ('[0:v]setsar=1[c];[1:v]setsar=1[b];[3:v]setsar=1,fps=30[o];'
          '[0:a]aresample=48000,aformat=channel_layouts=stereo[ca];[2:a]aresample=48000,aformat=channel_layouts=stereo[ba];'
          '[3:a]aresample=48000,aformat=channel_layouts=stereo,volume=0:enable=\'lt(t,1.3)\'[oa];[c][ca][b][ba][o][oa]concat=n=3:v=1:a=1[v][a]')
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
