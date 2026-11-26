"""VW Nivus showcase cinemático con la música del Vento blanco de Golden (cortes cada 1-2 pulsos de 0.5 s, 15.4 s). python3 nivus_cine.py cut|final out.mp4
Cortes = golpes de bajo detectados (banda 30-130 Hz): en la sección 35-46.5 s los golpes fuertes, en 47-54.4 s cada golpe (0.5 s)."""
import os, sys, subprocess
import common
from common import *
SONGF = os.environ.get('SONGF', f'{SCR}/es/gm/vento_audio.wav')
common.GRADE = ('eq=contrast=1.12:saturation=0.93:gamma=0.98,colorbalance=rs=-0.02:bs=0.03:rh=0.03:bh=-0.02,'
                'vignette=PI/6,noise=alls=5:allf=t')
T0 = 0.0
HITS = [float(i) for i in range(9)] + [8.5 + 0.5 * i for i in range(13)] + [14.9]   # 1 s al principio, 0.5 s después
# (clip, ss, speed, flash)
SH = [('0247', 0.30, 0.60, True), ('0251', 1.00, 0.60, False), ('0248', 0.10, 0.55, False), ('0249', 0.00, 0.55, False),
      ('0254', 0.00, 0.50, False), ('0246', 0.40, 0.60, False), ('0250', 0.30, 0.60, True), ('0252', 0.50, 0.60, True),
      # final: un corte por golpe, 0.5 s
      ('0255', 0.10, 0.55, True), ('0253', 0.20, 0.55, False), ('0253', 2.20, 0.55, False), ('0256', 0.30, 0.55, False),
      ('0256', 1.80, 0.55, False), ('0257', 0.50, 0.55, False), ('0257', 3.00, 0.55, False), ('0257', 5.50, 0.55, False),
      ('0260', 0.80, 0.55, False), ('0260', 3.50, 0.55, False), ('0260', 6.00, 0.55, False), ('0266', 1.00, 0.55, False),
      ('0266', 3.00, 0.55, False), ('0246', 2.50, 0.55, False), ('0247', 2.00, 0.55, False), ('0251', 3.50, 0.55, False)]
SH = SH[:len(HITS) - 1]
assert len(SH) == len(HITS) - 1, (len(SH), len(HITS))
LEAD = 0.5
def frames(): return [(round((HITS[i] - T0) * FPS), round((HITS[i + 1] - T0) * FPS)) for i in range(len(SH))]
def total(): return frames()[-1][1] / FPS
def cut():
    os.makedirs('pieces', exist_ok=True); lst = []
    for i, ((c, ss, sp, fl), (a, b)) in enumerate(zip(SH, frames())):
        o = f'pieces/c{i:02d}.mp4'; lst.append(o); piece(o, c, ss, (b - a) / FPS, sp, 0.05, fl)
    open('pieces/c.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in lst))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'pieces/c.txt', '-c', 'copy', 'body_raw.mp4'], check=True)
def final(out):
    T = LEAD + total(); s0 = 0.0
    fc = ('[0:v]setsar=1[c];[1:v]setsar=1[b];[c][b]concat=n=2:v=1:a=0[v];'
          f'[2:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={T - 0.7:.2f}:d=0.7[a]')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'cover.mp4', '-i', 'body_raw.mp4', '-ss', f'{s0:.3f}', '-t', f'{T:.2f}', '-i', SONGF,
                    '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', f'{T:.2f}', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow',
                    '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '192k',
                    '-movflags', '+faststart', out], check=True)
if __name__ == '__main__':
    os.chdir(os.environ.get('WORK', f'{SCR}/es/nivus_cine_vento')); os.makedirs('.', exist_ok=True)
    if sys.argv[1] == 'cut': cut()
    elif sys.argv[1] == 'final': final(sys.argv[2])
    elif sys.argv[1] == 'info': print(total(), frames())
