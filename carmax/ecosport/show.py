"""Showcase EcoSport Freestyle: solo tomas, cortes a la cuenta de Inner Bloom. python3 show.py cut|cover|final out.mp4 [nomusic]"""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont
from common import *
HERE = os.path.dirname(os.path.abspath(__file__))
# (clip, ss, beats, speed, push, flash)
SHOTS = [('0175', 0.30, 4, 0.75, 0.05, False),   # intro: frente bajo el cartel, antes del drop
         ('0200', 4.20, 4, 0.85, 0.05, True),    # DROP: toma cenital del auto en el salón
         ('0168', 0.40, 4, 0.80, 0.05, False),
         ('0170', 0.15, 2, 0.60, 0.06, False),
         ('0173', 0.50, 4, 0.80, 0.05, False),
         ('0171', 0.30, 2, 0.60, 0.06, False),
         ('0172', 0.70, 4, 0.80, 0.05, False),
         ('0176', 0.20, 4, 0.80, 0.05, False),
         ('0178', 0.05, 2, 0.60, 0.06, False),
         ('0179', 0.00, 4, 0.90, 0.04, False),
         ('0182', 0.30, 4, 0.80, 0.05, False),
         ('0196', 0.60, 4, 0.80, 0.05, False),
         ('0198', 2.40, 4, 0.80, 0.05, False),
         ('0166', 2.90, 6, 0.80, 0.05, False)]   # cierre: el auto se aleja frente al local
VENTO = os.environ.get('VENTO')   # ruta del audio del showcase del Vento blanco de Golden (15.4 s, 120 BPM)
if VENTO:   # versión 15 s con la canción del Vento: 29 beats de 0.5 s, el cierre se alarga 0.4 s hasta el final del tema
    B = 0.5
    SHOTS = [('0175', 0.30, 3, 0.80, 0.05, False), ('0200', 4.20, 3, 0.80, 0.05, True), ('0168', 0.40, 2, 0.70, 0.05, False),
             ('0173', 0.50, 2, 0.70, 0.05, False), ('0170', 0.15, 2, 0.60, 0.06, False), ('0171', 0.30, 2, 0.60, 0.06, False),
             ('0172', 0.70, 2, 0.70, 0.05, False), ('0178', 0.05, 2, 0.60, 0.06, False), ('0179', 0.00, 3, 0.85, 0.04, False),
             ('0196', 0.60, 2, 0.70, 0.05, False), ('0198', 2.40, 2, 0.70, 0.05, False), ('0166', 2.90, 4, 0.60, 0.05, False)]
LEAD = 0.5   # portada
def times():
    t, out, acc = 0, [], 0
    for s in SHOTS:
        a = round(acc * B * FPS); acc += s[2]; b = round(acc * B * FPS); out.append((a, b))
    if VENTO: out[-1] = (out[-1][0], out[-1][1] + 12)   # +0.4 s
    return out
def total(): return times()[-1][1] / FPS
def make_cut():
    os.makedirs('pieces', exist_ok=True); lst = []
    for i, (s, (a, b)) in enumerate(zip(SHOTS, times())):
        o = f'pieces/s{i:02d}.mp4'; lst.append(o)
        piece(o, s[0], s[1], (b - a) / FPS, s[3], s[4], s[5])
    open('pieces/s.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in lst))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'pieces/s.txt', '-c', 'copy', 'body_raw.mp4'], check=True)
F1 = ImageFont.truetype(f'{HERE}/../../golden-motors/fonts/BarlowCondensed-ExtraBold.ttf', 120)
F2 = ImageFont.truetype(f'{HERE}/../../golden-motors/fonts/BarlowCondensed-ExtraBold.ttf', 190)
OR = (238, 120, 14); WH = (255, 255, 255)
def cover(src=None):
    src = src or ('0175', 1.75, 1.0)
    # frame limpio de la toma elegida (misma geometría que el body)
    piece('cov_tmp.mp4', src[0], src[1], 1.5, src[2], 0.0)
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', 'cov_tmp.mp4', '-vf', 'select=eq(n\\,15)', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    img = Image.frombytes('RGB', (W, H), raw).convert('RGBA'); img.convert('RGB').save('cover_clean.png')
    d = ImageDraw.Draw(img)
    for txt, f, col, y in [('FORD ECOSPORT', F1, WH, int(os.environ.get('CY', 600))), ('FREESTYLE', F2, OR, int(os.environ.get('CY', 600)) + 105)]:
        tw = d.textlength(txt, font=f)
        d.text((W / 2 - tw / 2, y), txt, font=f, fill=col + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255))
    img.convert('RGB').save('cover.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', 'cover.png', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-t', str(LEAD), '-r', str(FPS), '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'cover.mp4'], check=True)
def final(out, music=True):
    T = LEAD + total(); s0 = DROP - (LEAD + 4 * B)
    a = (f"-ss {s0:.3f} -t {T:.2f} -i {SONG}").split()
    if VENTO: a = ['-i', VENTO]
    af = f'aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1.5:LRA=11' + ('' if VENTO else f',afade=t=in:d=0.15,afade=t=out:st={T - 1.4:.2f}:d=1.4') if music else 'anull'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', 'cover.mp4', '-i', 'body_raw.mp4'] + a + \
          ['-filter_complex', f'[0:v]setsar=1[c];[1:v]setsar=1[b];[c][b]concat=n=2:v=1:a=0[v];[2:a]{af}[a]' if music else
           '[0:v]setsar=1[c];[1:v]setsar=1[b];[c][b]concat=n=2:v=1:a=0[v];anullsrc=r=48000:cl=stereo[a]',
           '-map', '[v]', '-map', '[a]', '-t', f'{T:.2f}', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p',
           '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True)
if __name__ == '__main__':
    os.chdir(os.environ.get('WORK', f'{SCR}/es/show')); s = sys.argv[1]
    if s == 'cut': make_cut()
    elif s == 'cover': cover()
    elif s == 'final': final(sys.argv[2], len(sys.argv) < 4)
    elif s == 'info': print(total(), times())
