"""Showcases cinematicos lentos con canciones de IG de Nahuel (27/11).
python3 cine_show.py <auto> [cover|final]   -> WORK=<scratch>/cine/<auto>
Cada toma termina cuando el movimiento de camara llega a su remate (auto entero, volante entero) y los cortes caen
en los golpes fuertes de la cancion (medidos con librosa: onset + graves). Tomas = (clip, ss, fin_en_cancion).
La velocidad sale sola: (fuente) / (duracion en la cancion)."""
import os, sys, subprocess
SCRN = '/tmp/claude-0/-home-user/74e478c3-632a-51d9-acc1-5b85b595e003/scratchpad'
os.environ.setdefault('RAW', f'{SCRN}/new/raw')
import numpy as np
from PIL import Image
import car_show as cs
from common import GRADE, FPS

IG = f'{SCRN}/ig'
# (clip, ss, se): se = segundo de la fuente donde termina el remate; cada toma va hasta el siguiente golpe
CARS = {
 'trailblazer': dict(song='Df3SZtAC5Kf', t=('CHEVROLET', 'TRAILBLAZER'), cy=560, end=14.30, cuts=[1.10, 3.53, 5.97, 9.59, 12.02], shots=[
    ('0347', 3.9, None), ('0356', 0.3, 2.6), ('0352', 0.0, 2.3), ('0358', 0.5, 4.1), ('0361', 2.0, 4.3), ('0349', 5.6, 8.0)]),
 'amarok-plata': dict(song='Dfn4MAiCtLd', t=('VOLKSWAGEN', 'AMAROK'), cy=560, end=12.17, cuts=[2.35, 4.88, 7.01, 8.80, 10.57], shots=[
    ('0371', 6.0, None), ('0378', 0.3, 2.6), ('0383', 0.5, 2.8), ('0385', 0.3, 2.2), ('0377', 0.0, 1.7), ('0380', 0.0, 0.9)]),
 'hilux': dict(song='Df52ZovM1tT', t=('TOYOTA', 'HILUX 4X4'), cy=235, tscale=0.8, end=8.70, cuts=[2.17, 4.44, 7.02], land=True, shots=[
    ('0392', 0.5, None), ('0406', 1.6, 4.0), ('0413', 0.5, 3.3), ('0398', 4.6, 6.4)]),
 'saveiro': dict(song='De26CPsCWn6', t=('VOLKSWAGEN', 'SAVEIRO'), cy=560, end=11.80, cuts=[1.37, 2.95, 4.53, 6.88, 9.25], shots=[
    ('0414', 8.8, None), ('0420', 0.3, 2.0), ('0418', 1.6, 3.3), ('0422', 0.3, 3.0), ('0423', 0.5, 3.0), ('0417', 5.0, 7.7)]),
 'strada': dict(song='DfOMM6QiEPz', t=('FIAT', 'STRADA'), cy=640, end=12.90, cuts=[2.39, 4.78, 7.49, 10.36], shots=[
    ('0428', 9.0, None), ('0434', 0.0, 2.6), ('0441', 0.2, 3.0), ('0443', 2.2, 4.7), ('0429', 3.4, 6.1)]),
 'amarok-blanca': dict(song='Dbwa5lPC002', t=('VOLKSWAGEN', 'AMAROK'), cy=235, tscale=0.8, land=True, end=13.15, cuts=[2.80, 5.98, 8.44, 11.03], shots=[
    ('0446', 4.4, None), ('0451', 0.0, 2.8), ('0447', 5.5, 8.0), ('0461', 0.3, 3.0), ('0448', 4.5, 6.8)]),
}

def land_piece(out, clip, ss, d, speed, push=0.04):
    """salida horizontal 1920x1080 (Hilux)"""
    nf = round(d * FPS); D = nf / FPS
    vf = (f"trim={ss}:{ss + d * speed + 0.3},setpts=(PTS-STARTPTS)/{speed},fps={FPS},format=yuv420p,"
          f"scale=2112:1188:flags=lanczos,scale=w='trunc(2112*(1+{push}*min(t/{D},1))/2)*2':h=-2:eval=frame:flags=bicubic,"
          f"crop=1920:1080,{GRADE},format=yuv420p")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{cs.RAW}/{clip}.mp4', '-map', '0:v:0', '-vf', vf, '-an',
                    '-frames:v', str(nf), '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-r', str(FPS), out], check=True)

def cs_dur(clip):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{cs.RAW}/{clip}.mp4']))
def slow_src(name, clip, ss, d, speed, land):
    """camara lenta suave (interpolacion de movimiento) para velocidades < 0.9: genera un clip intermedio a velocidad 1"""
    L = land or cs.ORIENT.get(clip) == 'L'; sc = '1920:1080' if L else '1242:2208'
    vf = (f"trim={ss}:{ss + d * speed + 0.2},setpts=(PTS-STARTPTS)/{speed},scale={sc}:flags=lanczos,"
          f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,format=yuv420p")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{cs.RAW}/{clip}.mp4', '-map', '0:v:0', '-vf', vf, '-an', '-t', f'{d + 0.15:.3f}',
                    '-c:v', 'libx264', '-crf', '10', '-preset', 'fast', f'{cs.RAW}/{name}.mp4'], check=True)
    cs.ORIENT[name] = 'L' if L else 'V'
def plan(car):
    c = CARS[car]; b = [0.0] + c['cuts'] + [c['end']]
    # duraciones en frames enteros para que los cortes caigan exactos
    fr = [round(x * FPS) for x in b]; out = []
    for i, (clip, ss, se) in enumerate(c['shots']):
        d = (fr[i + 1] - fr[i]) / FPS
        if se is None: speed = min(0.85, (cs_dur(clip) - 0.15 - ss) / d)
        else: speed = (se - ss) / d
        out.append((clip, ss, d, round(speed, 3)))
    return out

def title_layer(car, size):
    c = CARS[car]; lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    cs.refined_title(lay, c['t'][0], c['t'][1], 300)
    bb = lay.getbbox(); sc = c.get('tscale', 1.0)
    t = lay.crop((max(0, bb[0] - 40), max(0, bb[1] - 40), min(1080, bb[2] + 40), min(1920, bb[3] + 40)))
    off = 300 - (bb[1] - 40)
    if sc != 1.0: t = t.resize((round(t.width * sc), round(t.height * sc)), Image.LANCZOS); off = off * sc
    full = Image.new('RGBA', size, (0, 0, 0, 0)); full.alpha_composite(t, ((size[0] - t.width) // 2, round(c['cy'] - off)))
    return full

def build(car, music=True, only_cover=False):
    c = CARS[car]; land = c.get('land'); size = (1920, 1080) if land else (1080, 1920)
    P = plan(car); os.makedirs('p', exist_ok=True)
    for i, (clip, ss, d, sp) in enumerate(P):
        if only_cover and i: break
        if not music and os.path.exists(f'p/{i:02d}.mp4'): continue
        print(car, i, clip, ss, f'd={d:.2f} speed={sp}')
        if sp < 0.9:
            nm = f'slow_{car}_{i}'; slow_src(nm, clip, ss, d, sp, land); clip, ss, sp = nm, 0.0, 1.0
        (land_piece if land else lambda o, cl, s, dd, spd: cs.piece_any(o, cl, s, dd, spd, 0.04))(f'p/{i:02d}.mp4', clip, ss, d, sp)
    title_layer(car, size).save('title.png')
    # portada = primer cuadro + titulo
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', 'p/00.mp4', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    im = Image.frombytes('RGB', size, raw).convert('RGBA'); im.alpha_composite(Image.open('title.png')); im.convert('RGB').save('cover.png')
    if only_cover: return
    with open('list.txt', 'w') as f:
        for i in range(len(P)): f.write(f"file 'p/{i:02d}.mp4'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'body.mp4'], check=True)
    d0 = P[0][2]; total = sum(p[2] for p in P)
    # titulo: visible desde el cuadro 0 (portada) y se desvanece antes del primer corte
    fo = max(0.3, d0 - 0.45)
    vf = f"[1:v]format=rgba,fade=t=out:st={fo:.2f}:d=0.35:alpha=1[t];[0:v][t]overlay=0:0:eof_action=pass,format=yuv420p[v]"
    aud = (['-i', f'{IG}/{c["song"]}.mp4'], f";[2:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={total - 0.35:.3f}:d=0.35,"
           "aresample=48000,loudnorm=I=-14:TP=-1.5,aresample=48000[a]") if music else \
          (['-f', 'lavfi', '-t', f'{total:.3f}', '-i', 'anullsrc=r=48000:cl=stereo'], ';[2:a]anull[a]')
    out = 'con.mp4' if music else 'sin.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'body.mp4', '-loop', '1', '-t', f'{total:.3f}', '-i', 'title.png'] + aud[0] +
                   ['-filter_complex', vf + aud[1], '-map', '[v]', '-map', '[a]', '-t', f'{total:.3f}', '-c:v', 'libx264', '-crf', '16',
                    '-preset', 'slow', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)

if __name__ == '__main__':
    car = sys.argv[1]; mode = sys.argv[2] if len(sys.argv) > 2 else 'final'
    wd = os.environ.get('WORK', f'{SCRN}/cine/{car}'); os.makedirs(wd, exist_ok=True); os.chdir(wd)
    if mode == 'cover': build(car, only_cover=True)
    else: build(car, True); build(car, False)
