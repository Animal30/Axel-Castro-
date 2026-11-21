"""Ford Ka SEL 2018 - Alejandro voice-over. python3 v1.py cut|check N,N|render|cover|final out.mp4"""
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
    talk('0055', 0.00, 3.30, cut=[('0034', 0.0, 3.30, 1.0, S)]),                                    # estas buscando un primer auto...
    talk('0055', 3.48, 12.40, cut=[('0037', 0.3, 2.12, 1.0, S), ('0041', 0.5, 1.00, 1.0, S), ('0046', 1.2, 1.00, 1.0, S),
                                   ('0044', 0.3, 1.15, 1.0, S), ('0047', 0.3, 1.85, 1.0, S), ('0048', 0.3, 1.80, 1.0, S)]),
    talk('0054', 0.25, 1.25, cut=[('0050', 0.2, 1.00, 1.0, S)]),                                    # es un Ka
    talk('0054', 1.42, 9.00, cut=[('0053', 0.2, 2.60, 1.0, S), ('0040', 0.3, 3.40, 1.0, S), ('0039', 0.2, 1.58, 1.0, S)]),
    talk('0054', 9.24, 12.29, cut=[('0043', 2.5, 1.50, 1.0, S), ('0038', 2.0, 1.55, 1.0, S)]),       # antiniebla, llantas
    talk('0054', 12.53, 21.15, cut=[('0049', 0.1, 1.87, 1.0, S), ('0048', 2.5, 2.90, 1.0, S), ('0045', 0.3, 1.70, 1.0, S),
                                    ('0047', 1.5, 2.15, 1.0, S)]),
    talk('0054', 21.54, 27.27, cut=[('0046', 0.0, 2.76, 1.0, S), ('0054', 24.3, 2.97, 1.0, 1.0)]),  # tablero, computadora
    talk('0054', 27.82, 30.40, cut=[('0057', 3.0, 2.58, 1.0, S)]),
    talk('0056', 0.45, 5.28, cut=[('0058', 0.3, 2.40, 1.0, S), ('0052', 0.0, 2.43, 1.0, S)]),
    talk('0056', 5.52, 6.65, cut=[('0051', 0.0, 1.13, 1.0, S)]),
    talk('0056', 6.85, 12.70, cut=[('0043', 3.4, 2.60, 1.0, S), ('0042', 0.0, 3.25, 1.0, 0.58)]),
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
FIX = {'4K,': 'Ka', 'estacionado': 'estacionás', 'comandantes': 'comandos', 'cuentas': 'cuentavueltas', 'una': 'un', 'tienes': 'tenés', 'llegas': 'llegás', 'cuatro': '4'}
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
            if w['type'] != 'word' or not (w['end'] > a + 0.05 and w['start'] < a + dur - 0.02): continue
            txt = FIX.get(w['text'], w['text'])
            if words and words[-1][2] == 'cuentavueltas' and txt.strip(',.') in ('de', 'revoluciones'): words[-1][1] = t0 + w['end'] - a; continue
            if words and words[-1][2].lower().strip(',.') == txt.lower().strip(',.') and t0 + w['start'] - a - words[-1][1] < 0.6: words[-1][1] = t0 + w['end'] - a; continue  # stutter (lo lo)
            words.append([t0 + max(w['start'], a) - a, t0 + min(w['end'], a + dur) - a, txt])
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
        ('Ford Ka SEL', '2018 · 90.000 km', icon_car, st[2] + 0.05, at('Tiene')[0] - 0.15),
        ('4 cubiertas nuevas', 'Antiniebla · Llantas de aleación', icon_check, at('Tiene')[0] - 0.05, st[5] - 0.15),
        ('Confort total', 'Comandos al volante · Espejos eléctricos', icon_check, st[5] + 0.05, at('aire')[0] - 0.15),
        ('Aire acondicionado', 'Dirección asistida', icon_check, at('aire')[0] - 0.05, st[6] - 0.15),
        ('Computadora de a bordo', 'Tablero completo', icon_check, st[6] + 0.05, st[8] - 0.15),
        ('Tomamos tu usado', 'De menor valor', icon_tag, at('tenés')[0] - 0.1, at('también')[0] - 0.15),
        ('Financiamos hasta 50%', 'Escribinos por mensaje', icon_chat, at('también')[0] - 0.05, total),
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
COVER = ('0043', 4.8)
def cover():
    c, t = COVER
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-ss', str(t), '-i', f'{RAW}/c{c}.mov', '-frames:v', '1',
                                   '-vf', f'scale={W}:{H}:flags=lanczos,{GRADE}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    img = Image.frombytes('RGB', (W, H), raw).convert('RGBA')
    d = ImageDraw.Draw(img)   # no dark band (Nahuel 2026-11-18)
    for txt, font, col, y in [('¿BUSCÁS TU', F_H1, WHITE, 315), ('PRIMER AUTO?', F_H2, GOLD, 420)]:
        while d.textlength(txt, font=font) > 940: font = ImageFont.truetype(font.path, font.size - 4)
        tw = d.textlength(txt, font=font)
        d.text((W / 2 - tw / 2, y), txt, font=font, fill=col + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255))
    sub = 'Ford Ka SEL · 2018 · 90.000 km'; tw = d.textlength(sub, font=kit.F_HOOK2)
    d.rounded_rectangle((W / 2 - tw / 2 - 30, 590, W / 2 + tw / 2 + 30, 670), 20, fill=(12, 12, 12, 225), outline=GOLD + (255,), width=3)
    d.text((W / 2 - tw / 2, 601), sub, font=kit.F_HOOK2, fill=WHITE + (255,))
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
