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
def sp(c, a, b, z=1.0): return (c, a, round(b - a, 3), z, 1.0)
def br(c, s0, d): return (c, s0, d, 1.0, 1.0)
def U(clip, a, b, pieces):
    assert abs(sum(p[2] for p in pieces) - (b - a)) < 0.02, (clip, a, b, sum(p[2] for p in pieces))
    return dict(aud=(f'{AUDSRC}{clip}', a, b), cap=clip, vid=pieces)
UNITS = [
    U('0105', 0.30, 4.70, [sp('0105', 0.30, 4.70)]),                                                # bueno que tenemos aca, rey de la ruta, es un Vento
    U('0105', 5.25, 11.20, [sp('0105', 5.25, 6.05), br('0094', 0.2, 1.2), sp('0105', 7.25, 9.25, 1.1), br('0102', 0.2, 1.95)]),
    U('0105', 11.66, 14.95, [sp('0105', 11.66, 14.95)]),                                            # la autonomia es impresionante
    U('0105', 15.32, 19.75, [sp('0105', 15.32, 16.92, 1.1), br('0097', 1.5, 1.7), sp('0105', 18.62, 19.75)]),
    U('0105', 19.98, 23.06, [sp('0105', 19.98, 23.06, 1.1)]),
    U('0105', 23.48, 28.80, [sp('0105', 23.48, 25.0), sp('0105', 25.0, 28.8, 1.12)]),
    U('0106', 0.00, 3.45, [sp('0106', 0.00, 3.45)]),
    U('0106', 3.95, 9.60, [sp('0106', 3.95, 6.0, 1.1), sp('0106', 6.0, 9.6)]),
    U('0106', 10.00, 12.45, [sp('0106', 10.0, 12.45, 1.12)]),
    U('0106', 12.75, 18.40, [sp('0106', 12.75, 14.4), br('0101', 4.8, 1.8), sp('0106', 16.2, 18.4, 1.1)]),
    U('0106', 19.10, 20.15, [sp('0106', 19.10, 20.15)]),
    U('0106', 20.40, 24.55, [sp('0106', 20.40, 24.55, 1.1)]),
    U('0106', 24.45, 24.85, [br('e001', 12.0, 0.4)]),                                                # placeholder tail, extended below
]
# end beat: 2.4 s of car with the address card (silence, music carries it)
UNITS[-1] = dict(aud=('clean0106', 24.45, 24.85), cap='0106', vid=[br('e001', 11.8, 2.4)])

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
FIX = {'$4': '4', 'cuatro': '4', 'Bento': 'Vento', 'viajas': 'viajás', 'amas.': 'amás.'}
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
        ('VW Vento TDI 2.0', 'Luxury · 2013 · 225.000 km', icon_car, max(0.0, at('Vento')[0] - 0.25), at('caja')[0] - 0.25),
        ('Caja DSG', 'De 6 velocidades', icon_check, at('caja')[0] - 0.2, at('sexta')[1] + 0.35),
        ('Autonomía increíble', 'Unos 1.000 km con un tanque', icon_check, at('autonomía')[0] - 0.2, at('kilómetros')[1] + 0.3),
        ('Viajes largos', 'A Buenos Aires con 1/4 de tanque', icon_check, at('Buenos')[0] - 0.2, at('tanque')[1] + 0.3),
        ('Mantenimiento al día', 'Siempre bien cuidado', icon_check, at('hice')[0] - 0.2, at('gusto')[1] + 0.3),
        ('Súper económico', 'Consumo ideal para andar', icon_check, at('súper')[0] - 0.2, at('andar')[1] + 0.3),
        ('Sin impuesto de rentas', 'Por ser modelo 2013', icon_tag, at('2013', st[11] - 0.1)[0] - 0.2, st[12] - 0.05),
        ('Octavio Pinto 3181', 'Golden Motors · Córdoba', icon_pin, st[12] + 0.15, total - 0.05),
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
COVER = ('e001', 17.0)
def cover():
    c, t = COVER
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-ss', str(t), '-i', f'{RAW}/c{c}.mov', '-frames:v', '1',
                                   '-vf', f'scale={W}:{H}:flags=lanczos,{GRADE}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    img = Image.frombytes('RGB', (W, H), raw).convert('RGBA')
    d = ImageDraw.Draw(img)   # no dark band (Nahuel 2026-11-18); text above the roof inside the feed safe zone
    F1 = ImageFont.truetype(F_H1.path, 132); F3 = ImageFont.truetype(F_H1.path, 70)
    p1, p2 = 'EL REY DE LA ', 'RUTA'
    tw = d.textlength(p1 + p2, font=F1); x = W / 2 - tw / 2
    for txt, col in ((p1, WHITE), (p2, GOLD)):
        d.text((x, 300), txt, font=F1, fill=col + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255)); x += d.textlength(txt, font=F1)
    t3 = 'VENTO TDI 2.0 · 2013 · 225.000 KM'; tw = d.textlength(t3, font=F3)
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
