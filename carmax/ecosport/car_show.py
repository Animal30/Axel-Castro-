"""Showcase 15.4 s con la musica del Vento (beat 0.5 s) para cualquier auto: python3 car_show.py <auto> cut|cover|final out.mp4 [nomusic]
Clips de hoy (26/11) en RAW=<scratch>/new/raw. Tomas = (clip, ss, beats, speed, push, flash)."""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont
SCRN = '/tmp/claude-0/-home-user/74e478c3-632a-51d9-acc1-5b85b595e003/scratchpad'
os.environ.setdefault('RAW', f'{SCRN}/new/raw')
import common
from common import *
import json as _json
ORIENT = _json.load(open(f'{SCRN}/new/orient.json'))
def piece_any(out, clip, ss, d, speed=1.0, push=0.05, flash=False, grade=True):
    if ORIENT.get(clip) != 'L': return common.piece(out, clip, ss, d, speed, push, flash, grade)
    nf = round(d * FPS); D = nf / FPS
    vf = (f"trim={ss}:{ss + d * speed + 0.3},setpts=(PTS-STARTPTS)/{speed},fps={FPS},format=yuv420p,split[a][b];"
          f"[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:6,eq=brightness=-0.10:saturation=0.9[bg];"
          f"[b]scale=w='trunc(1080*(1+{push}*min(t/{D},1))/2)*2':h=-2:eval=frame:flags=bicubic,crop=1080:ih[fg];"
          f"[bg][fg]overlay=(W-w)/2:(H-h)/2," + (common.GRADE + ',' if grade else '') +
          (f"eq=brightness='0.30*max(0,1-t/0.16)':eval=frame," if flash else '') + "format=yuv420p[vout]")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{RAW}/{clip}.mp4', '-filter_complex', vf, '-map', '[vout]', '-an',
                    '-frames:v', str(nf), '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-r', str(FPS), out], check=True)
HERE = os.path.dirname(os.path.abspath(__file__))
VENTO = f'{SCR}/es/gm/vento_audio.wav'; B = 0.5; LEAD = 0.5
CARS = {
 'trailblazer': dict(t=('CHEVROLET', 'TRAILBLAZER'), cover=('0347', 3.9), cy=640, shots=[
   ('0347', 0.3, 3, .75, .05, False), ('0349', 0.5, 3, .80, .05, True), ('0353', 0.4, 2, .70, .05, False), ('0350', 0.3, 2, .70, .05, False),
   ('0352', 0.3, 2, .70, .05, False), ('0356', 0.3, 2, .70, .05, False), ('0354', 0.6, 2, .70, .05, False), ('0358', 0.5, 3, .80, .04, False),
   ('0357', 0.3, 2, .70, .05, False), ('0359', 2.0, 2, .70, .05, False), ('0361', 0.8, 2, .70, .05, False), ('0362', 1.0, 4, .60, .05, False)]),
 'amarok-plata': dict(t=('VOLKSWAGEN', 'AMAROK'), cover=('0371', 6.0), cy=640, shots=[
   ('0371', 0.3, 3, .75, .05, False), ('0380', 0.4, 3, .80, .05, True), ('0373', 0.3, 2, .70, .05, False), ('0377', 0.2, 2, .60, .05, False),
   ('0378', 0.3, 2, .70, .05, False), ('0374', 0.3, 2, .70, .05, False), ('0379', 0.4, 2, .70, .05, False), ('0382', 0.3, 3, .80, .04, False),
   ('0381', 0.2, 2, .60, .04, False), ('0384', 0.3, 2, .70, .05, False), ('0385', 0.3, 2, .70, .05, False), ('0387', 3.0, 4, .60, .05, False)]),
 'hilux': dict(t=('TOYOTA', 'HILUX 4X4'), cover=('0398', 7.0), cy=330, shots=[
   ('0392', 0.3, 3, .75, .05, False), ('0394', 0.5, 3, .80, .05, True), ('0398', 1.0, 2, .70, .05, False), ('0401', 0.3, 2, .60, .05, False),
   ('0404', 1.0, 2, .70, .05, False), ('0402', 1.0, 2, .70, .05, False), ('0405', 1.0, 2, .70, .05, False), ('0408', 0.2, 2, .60, .04, False),
   ('0409', 0.2, 3, .70, .04, False), ('0410', 0.3, 2, .70, .05, False), ('0411', 1.5, 2, .70, .05, False), ('0407', 2.0, 4, .60, .05, False)]),
 'saveiro': dict(t=('VOLKSWAGEN', 'SAVEIRO'), cover=('0414', 8.8), cy=640, shots=[
   ('0414', 0.4, 3, .75, .05, False), ('0419', 0.4, 3, .80, .05, True), ('0415', 0.5, 2, .70, .05, False), ('0418', 0.3, 2, .70, .05, False),
   ('0417', 1.0, 2, .70, .05, False), ('0420', 0.5, 2, .70, .05, False), ('0421', 2.0, 2, .70, .05, False), ('0426', 1.0, 3, .80, .05, False),
   ('0422', 0.5, 2, .70, .05, False), ('0423', 0.3, 2, .70, .05, False), ('0424', 2.0, 2, .70, .05, False), ('0427', 2.0, 4, .60, .05, False)]),
 'strada': dict(t=('FIAT', 'STRADA'), cover=('0428', 9.0), cy=640, shots=[
   ('0428', 4.6, 3, .75, .05, False), ('0429', 0.4, 3, .80, .05, True), ('0438', 1.0, 2, .70, .05, False), ('0437', 0.5, 2, .70, .05, False),
   ('0436', 1.5, 2, .70, .05, False), ('0429', 3.5, 2, .70, .05, False), ('0437', 3.5, 2, .70, .05, False), ('0444', 1.0, 3, .80, .05, False),
   ('0440', 0.2, 2, .60, .04, False), ('0443', 1.0, 2, .70, .05, False), ('0439', 1.0, 2, .70, .05, False), ('0428', 6.0, 4, .60, .05, False)]),
 'amarok-blanca': dict(t=('VOLKSWAGEN', 'AMAROK'), cover=('0446', 3.0), cy=330, shots=[
   ('0445', 0.3, 3, .75, .05, False), ('0446', 0.5, 3, .80, .05, True), ('0454', 1.0, 2, .70, .05, False), ('0450', 0.3, 2, .60, .05, False),
   ('0453', 2.0, 2, .70, .05, False), ('0447', 5.0, 2, .70, .05, False), ('0448', 1.0, 2, .70, .05, False), ('0449', 1.0, 3, .80, .05, False),
   ('0456', 1.0, 2, .70, .05, False), ('0458', 0.3, 2, .60, .04, False), ('0461', 0.3, 2, .60, .04, False), ('0462', 2.0, 4, .60, .05, False)]),
}
assert all(sum(s[2] for s in c['shots']) == 29 for c in CARS.values())
def times(shots):
    out, acc = [], 0
    for s in shots:
        a = round(acc * B * FPS); acc += s[2]; b = round(acc * B * FPS); out.append((a, b))
    out[-1] = (out[-1][0], out[-1][1] + 12); return out
def make_cut(car):
    shots = CARS[car]['shots']; os.makedirs('pieces', exist_ok=True); lst = []
    for i, (s, (a, b)) in enumerate(zip(shots, times(shots))):
        o = f'pieces/s{i:02d}.mp4'; lst.append(o); piece_any(o, s[0], s[1], (b - a) / FPS, s[3], s[4], s[5])
    open('pieces/s.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in lst))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'pieces/s.txt', '-c', 'copy', 'body_raw.mp4'], check=True)
F1 = ImageFont.truetype(f'{HERE}/../../golden-motors/fonts/BarlowCondensed-ExtraBold.ttf', 120)
FS = ImageFont.truetype(f'{HERE}/../../golden-motors/fonts/BarlowCondensed-ExtraBold.ttf', 190)
OR = (238, 120, 14); WH = (255, 255, 255)
def cover(car):
    c = CARS[car]; cc, ct = os.environ.get('CC', c['cover'][0]), float(os.environ.get('CT', c['cover'][1]))
    piece_any('cov_tmp.mp4', cc, ct, 1.5, 1.0, 0.0)
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', 'cov_tmp.mp4', '-vf', 'select=eq(n\\,15)', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    img = Image.frombytes('RGB', (W, H), raw).convert('RGBA'); img.convert('RGB').save('cover_clean.png'); d = ImageDraw.Draw(img)
    y0 = int(os.environ.get('CY', c['cy'])); l1, l2 = c['t']
    f2 = FS
    while d.textlength(l2, font=f2) > 960: f2 = ImageFont.truetype(f'{HERE}/../../golden-motors/fonts/BarlowCondensed-ExtraBold.ttf', f2.size - 10)
    if os.environ.get('GLASS') == '1':
        import kinetic
        f2 = kinetic.font(kinetic.FSB, 230)
        while d.textlength(l2.title(), font=f2) > 980: f2 = kinetic.font(kinetic.FSB, f2.size - 10)
        kinetic.glass_lines(img, [(l1.title(), kinetic.font(kinetic.FM, 86)), (l2.title(), f2)], y=y0)
    else:
      for txt, f, col, y in [(l1, F1, WH, y0), (l2, f2, OR, y0 + 105)]:
        tw = d.textlength(txt, font=f); d.text((W / 2 - tw / 2, y), txt, font=f, fill=col + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255))
    img.convert('RGB').save('cover.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', 'cover.png', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-t', str(LEAD), '-r', str(FPS), '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'cover.mp4'], check=True)
def final(car, out, music=True):
    T = LEAD + times(CARS[car]['shots'])[-1][1] / FPS
    af = 'aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1.5:LRA=11'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', 'cover.mp4', '-i', 'body_raw.mp4', '-i', VENTO,
           '-filter_complex', f'[0:v]setsar=1[c];[1:v]setsar=1[b];[c][b]concat=n=2:v=1:a=0[v];[2:a]{af}[a]' if music else
           '[0:v]setsar=1[c];[1:v]setsar=1[b];[c][b]concat=n=2:v=1:a=0[v];anullsrc=r=48000:cl=stereo[a]',
           '-map', '[v]', '-map', '[a]', '-t', f'{T:.2f}', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p',
           '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True)
if __name__ == '__main__':
    car, s = sys.argv[1], sys.argv[2]
    wd = os.environ.get('WORK', f'{SCR}/new/{car}'); os.makedirs(wd, exist_ok=True); os.chdir(wd)
    if s == 'cut': make_cut(car)
    elif s == 'cover': cover(car)
    elif s == 'final': final(car, sys.argv[3], len(sys.argv) < 5)
