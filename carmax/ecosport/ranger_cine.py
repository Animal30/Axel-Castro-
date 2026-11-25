"""Ranger Black showcase cinemático con la canción de Nahuel (bass hits). python3 ranger_cine.py cut|final out.mp4
Cortes = golpes de bajo detectados (banda 30-130 Hz): en la sección 35-46.5 s los golpes fuertes, en 47-54.4 s cada golpe (0.5 s)."""
import os, sys, subprocess
import common
from common import *
SONGF = os.environ.get('SONGF', '/root/.claude/uploads/74e478c3-632a-51d9-acc1-5b85b595e003/e4457091-audio_6b077186600075.44177573.mp3')
common.GRADE = ('eq=contrast=1.12:saturation=0.93:gamma=0.98,colorbalance=rs=-0.02:bs=0.03:rh=0.03:bh=-0.02,'
                'vignette=PI/6,noise=alls=5:allf=t')
T0 = 34.99                    # primer golpe fuerte tras el silencio
HITS = [34.99, 36.99, 38.92, 39.34, 39.83, 40.23, 41.99, 44.24, 46.50] + [47.03 + 0.5 * i for i in range(15)] + [54.40]
# (clip, ss, speed, flash)
SH = [('0208', 0.30, 0.60, True), ('0201', 12.00, 0.60, False), ('0209', 0.50, 0.55, False), ('0207', 0.00, 0.55, False),
      ('0210', 0.30, 0.55, False), ('0206', 0.30, 0.60, False), ('0202', 0.20, 0.60, True), ('0211', 0.10, 0.60, True),
      # final: un corte por golpe, 0.5 s
      ('0213', 0.00, 0.55, True), ('0205', 0.10, 0.55, False), ('0212', 0.20, 0.55, False), ('0214', 0.10, 0.55, False),
      ('0217', 0.00, 0.55, False), ('0217', 1.50, 0.55, False), ('0215', 1.30, 0.55, False), ('0218', 5.00, 0.55, False),
      ('0220', 1.80, 0.55, False), ('0220', 4.00, 0.55, False), ('0233', 0.30, 0.55, False), ('0233', 1.60, 0.55, False),
      ('0204', 0.30, 0.55, False), ('0209', 2.00, 0.55, False), ('0208', 3.40, 0.55, False), ('0201', 15.50, 0.55, False)]
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
    T = LEAD + total(); s0 = T0 - LEAD
    fc = ('[0:v]setsar=1[c];[1:v]setsar=1[b];[c][b]concat=n=2:v=1:a=0[v];'
          f'[2:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={T - 0.7:.2f}:d=0.7[a]')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'cover.mp4', '-i', 'body_raw.mp4', '-ss', f'{s0:.3f}', '-t', f'{T:.2f}', '-i', SONGF,
                    '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', f'{T:.2f}', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow',
                    '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '192k',
                    '-movflags', '+faststart', out], check=True)
if __name__ == '__main__':
    os.chdir(os.environ.get('WORK', f'{SCR}/es/ranger_cine')); os.makedirs('.', exist_ok=True)
    if sys.argv[1] == 'cut': cut()
    elif sys.argv[1] == 'final': final(sys.argv[2])
    elif sys.argv[1] == 'info': print(total(), frames())
