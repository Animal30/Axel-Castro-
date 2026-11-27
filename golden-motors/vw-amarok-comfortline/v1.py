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
def vo(clip, a, b, shots):  # voice-over unit: Alejandro's audio from clip, picture = b-roll list (clip, start, dur)
    return dict(aud=(f'{AUDSRC}{clip}', a, b), cap=clip, vid=[(c, s, d, 1.0, 1.0) for c, s, d in shots])
UNITS = [
    vo('0082', 0.00, 2.85, [('0064', 0.0, 2.85)]),                                   # es una Amarok Comfortline
    vo('0082', 3.10, 6.70, [('0077', 0.2, 3.6)]),                                    # 4x4 caja manual 6 marchas
    vo('0082', 7.10, 17.70, [('0077', 3.0, 3.0), ('0076', 3.8, 2.4), ('0075', 0.0, 1.7), ('0074', 0.2, 2.0), ('0076', 0.4, 1.5)]),
    vo('0082', 18.50, 23.60, [('0078', 0.5, 2.5), ('0079', 3.8, 2.6)]),              # todo lo que nos acostumbra... Volkswagen
    vo('0083', 0.00, 12.70, [('0066', 0.0, 3.2), ('0068', 0.0, 2.0), ('0072', 0.0, 3.0), ('0081', 0.0, 2.5), ('0071', 3.0, 2.0)]),
    vo('0083', 13.00, 15.45, [('0073', 0.2, 2.45)]),                                  # la 4x4 te salva
    vo('0084', 0.00, 4.55, [('0080', 0.0, 4.55)]),                                   # si tenes otra Amarok...
    vo('0084', 4.85, 9.85, [('0065', 0.0, 2.5), ('0070', 0.0, 2.5)]),                # tirame la consulta, coordinamos visita
    vo('0084', 10.35, 12.50, [('0067', 0.5, 2.15)]),                                 # entregar usado y financiar
    vo('0084', 12.75, 15.05, [('0069', 0.4, 2.3)]),                                  # todo se puede hablar
    vo('0084', 15.05, 17.95, [('0070', 1.6, 2.9)]),                                 # contado, una atencion
    vo('0084', 18.50, 20.75, [('0065', 1.1, 2.25)]),                                 # no dudes en venir
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
FIX = {'$4': '4', 'cuatro': '4', 'Comfort': 'Comfortline', 'AMAR': 'Amarok', 'Médanos,': 'Médanos,'}
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
            if txt.lower().strip(',.') in ('aire', 'acondicionado'): continue      # never mention aire acondicionado
            if txt.lower().startswith('sacristar') and words and words[-1][2].lower() == 'al': words[-1][2] = 'alzacristales'; words[-1][1] = t0 + w['end'] - a; continue
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
        ('VW Amarok Comfortline', '4x4 · Diésel · 2021 · 110.000 km', icon_car, at('Amarok')[0] - 0.25, at('caja')[0] - 0.3),
        ('Caja manual', '6 marchas', icon_check, at('caja')[0] - 0.2, at('marchas')[1] + 0.5),
        ('Climatizador', 'Y velocidad crucero', icon_check, at('climatizador')[0] - 0.2, at('crucero')[1] + 0.25),
        ('Comandos al volante', 'Teléfono y audio', icon_check, at('comando')[0] - 0.2, at('volante')[1] + 0.25),
        ('Todo eléctrico', 'Espejos y alzacristales en las 4 puertas', icon_check, at('espejos')[0] - 0.2, at('puertas')[1] + 0.25),
        ('Tracción 4x4', 'Playa, campo y barro', icon_check, at('4x4', st[4])[0] - 0.3, at('situaciones')[1] + 0.3),
        ('Aceptamos tu usado', 'Financiamos una parte', icon_tag, at('entregar')[0] - 0.2, at('parte')[1] + 0.3),
        ('Octavio Pinto 3181', 'Golden Motors · Córdoba', icon_pin, at('dudes')[0] - 0.3, total - 0.05),
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
COVER = ('0064', 3.25)
def cover():
    c, t = COVER
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-ss', str(t), '-i', f'{RAW}/c{c}.mov', '-frames:v', '1',
                                   '-vf', f'scale={W}:{H}:flags=lanczos,{GRADE}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    img = Image.frombytes('RGB', (W, H), raw).convert('RGBA')
    d = ImageDraw.Draw(img)   # no dark band (Nahuel 2026-11-18); car starts ~y 560 so the text stays above it
    F1 = ImageFont.truetype(F_H1.path, 132); F3 = ImageFont.truetype(F_H1.path, 70)
    p1, p2 = 'ESTA AMAROK ', '4X4'
    tw = d.textlength(p1 + p2, font=F1); x = W / 2 - tw / 2
    for txt, col in ((p1, WHITE), (p2, GOLD)):
        d.text((x, 300), txt, font=F1, fill=col + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255)); x += d.textlength(txt, font=F1)
    t3 = 'COMFORTLINE · 2021 · 110.000 KM'; tw = d.textlength(t3, font=F3)
    d.text((W / 2 - tw / 2, 455), t3, font=F3, fill=WHITE + (255,), stroke_width=5, stroke_fill=(0, 0, 0, 255))
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
