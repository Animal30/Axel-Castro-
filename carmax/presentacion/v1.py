"""CarMax - video de presentación (Nahuel a cámara frente al local).
python3 v1.py cut|check N,N|render|cover|music|final out.mp4
Env: RAW (DJI talking clips 0155..0160.mp4), BROLL (vertical IMG_46xx.MOV), WEB (phone screenshots f0000.png..)."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import kit
from kit import W, H, FPS, GOLD, WHITE, glass_card, draw_caption, chunk, icon_pin, icon_globe, icon_car

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = '/tmp/claude-0/-home-user/74e478c3-632a-51d9-acc1-5b85b595e003/scratchpad'
RAW = os.environ.get('RAW', f'{SCR}/pres/raw'); BROLL = os.environ.get('BROLL', f'{SCR}/raw')
WEB = os.environ.get('WEB', f'{SCR}/pres/web'); TX = os.environ.get('TX', f'{SCR}/pres/tx')
OUTRO = '/mnt/project-files/carmax/outro-logo/carmax-logo-barrido-con-musica.mp4'
GRADE = 'eq=contrast=1.06:saturation=1.06:gamma=1.02,colorbalance=rs=0.015:bs=-0.015:rh=0.02:bh=-0.02,vignette=PI/8'
S = 0.6  # b-roll slow motion

# unit: audio (talk clip, a, b) + video pieces [(kind, clip, start, dur_out, speed)]
def talk(clip, a, b, vid=None):
    return dict(aud=(clip, a, b), vid=vid or [('T', clip, a, b - a, 1.0)])
UNITS = [   # v2 (Nahuel 2026-11-25): web line removed, address moved to the end
    talk('0160', 0.00, 6.25),                                    # gancho: si estás en Córdoba... visitá CarMax, flota de usados
    talk('0156', 0.45, 4.70, [('T', '0156', 0.45, 1.90, 1.0),     # en nuestro catálogo de usados seleccionados
                               ('B', 'IMG_4663', 3.4, 1.20, S),   # pickups
                               ('B', 'IMG_4673', 0.3, 1.15, S)]), # salón por dentro
    talk('0158', 0.22, 3.95, [('W', None, 0, 2.45, 1.0),          # deslizá y podrás ver todo nuestro catálogo completo
                               ('T', '0158', 2.67, 1.28, 1.0)]),  # no dudes en consultarnos
    talk('0155', 2.98, 5.30),                                    # estamos en Octavio Pinto al 2585
]

def nframes(u): return sum(round(p[3] * FPS) for p in u['vid'])

def make_cut():
    os.makedirs('pieces', exist_ok=True); vlist, alist = [], []
    for ui, u in enumerate(UNITS):
        for pi, (k, c, s, d, sp) in enumerate(u['vid']):
            out = f'pieces/v{ui:02d}_{pi}.mp4'; vlist.append(out); nf = str(round(d * FPS))
            if k == 'W':
                cmd = ['-framerate', str(FPS), '-start_number', str(s), '-i', f'{WEB}/f%04d.png', '-vf', f'scale={W}:{H}:flags=lanczos,format=yuv420p']
            else:
                src = f'{RAW}/{c}.mp4' if k == 'T' else f'{BROLL}/{c}.MOV'
                vf = (f"trim={s}:{s + d * sp + 0.3},setpts=(PTS-STARTPTS)/{sp},fps={FPS},"
                      f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},{GRADE},format=yuv420p")
                cmd = ['-i', src, '-map', '0:v:0', '-vf', vf]
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *cmd, '-an', '-frames:v', nf,
                            '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-r', str(FPS), out], check=True)
        c, a, b = u['aud']; dur = nframes(u) / FPS; out = f'pieces/a{ui:02d}.wav'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{RAW}/{c}.mp4', '-map', '0:a:0', '-af',
                        f'atrim={a}:{a + dur},asetpts=PTS-STARTPTS,highpass=f=80,'
                        f'afade=t=in:d=0.02,afade=t=out:st={dur - 0.04:.3f}:d=0.04,apad,atrim=0:{dur}',
                        '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s24le', out], check=True)
        alist.append(out)
    open('pieces/v.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in vlist))
    open('pieces/a.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in alist))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'pieces/v.txt', '-f', 'concat', '-safe', '0',
                    '-i', 'pieces/a.txt', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'pcm_s16le', 'cut.mov'], check=True)

FIX = {'Carmax.': 'CarMax', 'Carmax': 'CarMax'}
def unit_starts():
    t, out = 0, []
    for u in UNITS: out.append(t); t += nframes(u) / FPS
    return out, t

def caption_words():
    starts, _ = unit_starts(); words = []
    for u, t0 in zip(UNITS, starts):
        c, a, b = u['aud']; dur = nframes(u) / FPS
        for w in json.load(open(f'{TX}/{c}.json'))['words']:
            if w['type'] != 'word' or not ((w['end'] > a + 0.05 or w['start'] >= a) and w['start'] < a + dur - 0.02): continue
            words.append([t0 + max(w['start'], a) - a, t0 + min(w['end'], a + dur) - a, FIX.get(w['text'], w['text'])])
    return words

def render(only=None):
    words = caption_words(); groups = chunk(words); st, total = unit_starts()
    def at(word, after=0): return next(w for w in words if w[2].startswith(word) and w[0] >= after)
    cards = [
        ('Octavio Pinto 2585', 'Córdoba', icon_pin, st[3] + 0.1, total - 0.05),
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

F_H1 = ImageFont.truetype(f'{HERE}/../../golden-motors/fonts/BarlowCondensed-ExtraBold.ttf', 112)
F_H2 = ImageFont.truetype(f'{HERE}/../../golden-motors/fonts/BarlowCondensed-ExtraBold.ttf', 150)
COVER = ('0160', 1.57); COVER_FRAME = 53   # Nahuel's pick: frame 53 of cut.mov (mouth slightly open, hands in triangle)
def cover():
    c, t = COVER
    # v5: exact frame of the edit that Nahuel pointed at (cut.mov frame 53 = 1.767 s, matched against his screenshot)
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', 'cut.mov', '-map', '0:v:0', '-vf', f'select=eq(n\\,{COVER_FRAME})',
                                   '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    img = Image.frombytes('RGB', (W, H), raw).convert('RGBA'); d = ImageDraw.Draw(img)
    for txt, font, col, y in [('BUSCANDO UN AUTO', F_H1, WHITE, 500), ('EN CÓRDOBA', F_H2, GOLD, 600)]:   # v4 (Nahuel): statement, no ¿?, no address line
        while d.textlength(txt, font=font) > 940: font = ImageFont.truetype(font.path, font.size - 4)
        tw = d.textlength(txt, font=font)
        d.text((W / 2 - tw / 2, y), txt, font=font, fill=col + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255))
    img.convert('RGB').save('cover.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', 'cover.png', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-t', '0.5', '-r', str(FPS), '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'cover.mp4'], check=True)

def music():
    _, total = unit_starts()
    subprocess.run([sys.executable, f'{HERE}/music.py', 'music.wav', f'{total + 0.5 + 1.0:.2f}'], check=True)

def final(out, with_music=True):
    """cover + body (voice, music bed ducked under it) + logo outro with its own sting."""
    _, total = unit_starts(); body = 0.5 + total
    if with_music:
        mus = (f'[3:a]aresample=48000,aformat=channel_layouts=stereo,volume=-16dB,afade=t=out:st={body - 0.6:.2f}:d=0.6,atrim=0:{body}[m];'
               '[m2][v0]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[md];[md][vv]amix=inputs=2:normalize=0[mix];')
        pre = '[vx]asplit=2[v0][vv];[m]anull[m2];'
    else:
        mus = '[vx]anull[mix];'; pre = ''
    fc = ('[0:v]setsar=1[c];[1:v]setsar=1[b];[4:v]setsar=1,fps=30,format=yuv420p[o];[c][b]concat=n=2:v=1:a=0[cb];[cb][o]concat=n=2:v=1:a=0[v];'
          '[0:a]aresample=48000,aformat=channel_layouts=stereo[ca];[2:a]aresample=48000,aformat=channel_layouts=stereo[ba];'
          '[ca][ba]concat=n=2:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[vx];' + pre + mus +
          '[4:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1.5,aresample=48000[oa];[mix][oa]concat=n=2:v=0:a=1[a]')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'cover.mp4', '-i', 'body.mp4', '-i', 'cut.mov', '-i', 'music.wav', '-i', OUTRO,
                    '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow',
                    '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)

if __name__ == '__main__':
    os.chdir(os.environ.get('WORK', HERE))
    s = sys.argv[1]
    if s == 'cut': make_cut()
    elif s == 'check': render(set(int(x) for x in sys.argv[2].split(',')))
    elif s == 'render': render()
    elif s == 'cover': cover()
    elif s == 'music': music()
    elif s == 'final': final(sys.argv[2], os.environ.get('NOMUSIC') is None)
    elif s == 'words': print(' | '.join(f'{w[2]}@{w[0]:.2f}' for w in caption_words()), [round(x, 2) for x in unit_starts()[0]])
