"""VW Nivus presentada por Nahuel (voz + b-roll + Inner Bloom + logo final).
python3 talk.py cut|render|cover|final out.mp4 [nomusic]|words"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
import kit
from kit import chunk, draw_caption, GOLD, WHITE
from common import *
HERE = os.path.dirname(os.path.abspath(__file__))
# unit: aud = [(clip, a, b)...] concatenadas; vid = [(clip, ss, dur_out, speed, push)] (el video no tiene por qué ser continuo con el audio)
def U(aud, vid): return dict(aud=aud, vid=vid)
UNITS = [
  U([('0242', 0.50, 4.25)], [('0242', 0.50, 1.80, 1.0, 0.02), ('0247', 0.40, 0.95, 0.70, 0.05), ('0242', 3.25, 1.00, 1.0, 0.02)]),          # Volkswagen Nivus 2020, caja automática. Vení que te muestro el interior
  U([('0245', 3.20, 4.95), ('0245', 5.35, 9.45)], [('0260', 1.00, 1.75, 0.80, 0.04), ('0253', 0.30, 1.15, 0.80, 0.04),
                                                    ('0256', 0.20, 0.95, 0.80, 0.04), ('0257', 5.0, 2.00, 0.80, 0.04)]),             # tope de gama, cuero, pantalla, tablero digital, arranca con botón
  U([('0266', 3.26, 5.85)], [('0266', 0.65, 2.59, 1.0, 0.03)]),                                                                       # motor, 15.000 km, services oficiales
  U([('0238', 0.28, 4.40)], [('0246', 0.20, 1.40, 0.80, 0.05), ('0250', 0.30, 1.50, 0.80, 0.05), ('0238', 3.16, 1.22, 1.0, 0.02)]),   # si tenés 28.900.000 este auto puede ser para vos
  U([('0264', 0.45, 5.25)], [('0264', 0.45, 4.80, 1.0, 0.02)]),                                                                       # si tenés uno usado... escribinos
]
FIX = {'115': '115.000', '28': '28.900.000', '15': '15.000', 'sub,': 'SUV', '"service"': 'services'}; SKIP = {'000', '900'}
def udur(u): return sum(round(p[2] * FPS) for p in u['vid']) / FPS
def starts():
    t, out = 0, []
    for u in UNITS: out.append(t); t += udur(u)
    return out, t
def make_cut():
    os.makedirs('pieces', exist_ok=True); vl, al = [], []
    for ui, u in enumerate(UNITS):
        for pi, (c, ss, d, sp, pu) in enumerate(u['vid']):
            o = f'pieces/v{ui:02d}_{pi}.mp4'; vl.append(o); piece(o, c, ss, d, sp, pu)
        dur = udur(u); parts = []
        for si, (c, a, b) in enumerate(u['aud']):
            o = f'pieces/a{ui:02d}_{si}.wav'; parts.append(o); n = b - a
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{RAW}/{c}.mp4', '-map', '0:a:0', '-af',
                            f'atrim={a}:{b},asetpts=PTS-STARTPTS,highpass=f=80,' + ('afftdn=nr=10:nf=-40,loudnorm=I=-17:TP=-2:LRA=7,' if c == 'km3' else '') + f'afade=t=in:d=0.02,afade=t=out:st={n - 0.04:.3f}:d=0.04',
                            '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s24le', o], check=True)
        open(f'pieces/a{ui:02d}.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
        o = f'pieces/a{ui:02d}.wav'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'pieces/a{ui:02d}.txt', '-af', f'apad,atrim=0:{dur}',
                        '-ar', '48000', '-c:a', 'pcm_s24le', f'pieces/ac{ui:02d}.wav'], check=True)
        al.append(f'pieces/ac{ui:02d}.wav')
    open('pieces/v.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in vl))
    open('pieces/a.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in al))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'pieces/v.txt', '-f', 'concat', '-safe', '0',
                    '-i', 'pieces/a.txt', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'pcm_s16le', 'cut.mov'], check=True)
def caption_words():
    st, _ = starts(); words = []
    for u, t0 in zip(UNITS, st):
        off = 0
        for c, a, b in u['aud']:
            for w in json.load(open(f'{TX}/{c}.json'))['words']:
                if w['type'] != 'word' or w['text'] in SKIP or w['text'] in {'000'}: continue
                if w['start'] < a - 0.03 or w['end'] > b + 0.05: continue
                words.append([t0 + off + w['start'] - a, t0 + off + min(w['end'], b) - a, FIX.get(w['text'], w['text'])])
            off += b - a
    for i in range(len(words) - 3):   # "ciento quince mil kilometros" -> "115.000 KM"
        if words[i][2].lower() == 'ciento' and words[i + 3][2].lower().startswith('kil'):
            words[i:i + 4] = [[words[i][0], words[i + 2][1], '115.000'], [words[i + 3][0], words[i + 3][1], 'KM']]; break
    for i, w in enumerate(words):   # sin "pesos": el numero se queda en pantalla hasta la palabra siguiente
        if w[2] == '28.900.000' and i + 2 < len(words) and words[i + 1][2].startswith('pesos'):
            w[1] = words[i + 2][0] - 0.02; del words[i + 1]; break
    return words
def render():
    words = caption_words(); groups = chunk(words); _, total = starts(); n = round(total * FPS)
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', 'cut.mov', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', 'body.mp4'], stdin=subprocess.PIPE)
    for i in range(n):
        raw = dec.stdout.read(W * H * 3)
        if len(raw) < W * H * 3: break
        img = Image.frombytes('RGB', (W, H), raw).convert('RGBA'); draw_caption(img, groups, i / FPS)
        enc.stdin.write(img.convert('RGB').tobytes())
    enc.stdin.close(); enc.wait(); dec.stdout.close(); dec.kill(); dec.wait()
F1 = ImageFont.truetype(f'{HERE}/../../golden-motors/fonts/BarlowCondensed-ExtraBold.ttf', 120)
F2 = ImageFont.truetype(f'{HERE}/../../golden-motors/fonts/BarlowCondensed-ExtraBold.ttf', 190)
F3 = ImageFont.truetype(f'{HERE}/../../golden-motors/fonts/BarlowCondensed-ExtraBold.ttf', 270)
COVER = (os.environ.get('CC', '0238'), float(os.environ.get('CT', 0.3)))
def cover():
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', 'cut.mov', '-map', '0:v:0', '-vf', 'select=eq(n\\,' + os.environ.get('CF', '485') + ')', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    img = Image.frombytes('RGB', (W, H), raw).convert('RGBA'); img.convert('RGB').save('cover_clean.png'); d = ImageDraw.Draw(img)
    y0 = int(os.environ.get('CY', 345))
    for txt, f, col, y in [('VOLKSWAGEN', F1, WHITE, y0), ('NIVUS', F3, GOLD, y0 + 110)]:
        tw = d.textlength(txt, font=f); d.text((W / 2 - tw / 2, y), txt, font=f, fill=col + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255))
    img.convert('RGB').save('cover.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', 'cover.png', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-t', '0.5', '-r', str(FPS), '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'cover.mp4'], check=True)
def final(out, music=True):
    st, total = starts(); body = 0.5 + total; drop_at = 0.5 + st[1]; s0 = DROP - drop_at
    mus = (f'[3:a]aresample=48000,aformat=channel_layouts=stereo,volume=-15dB,afade=t=in:d=0.3,afade=t=out:st={body - 0.7:.2f}:d=0.7[m];'
           '[vx]asplit=2[v0][vv];[m][v0]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[md];[md][vv]amix=inputs=2:normalize=0[mix];') if music else '[vx]anull[mix];'
    fc = ('[0:v]setsar=1[c];[1:v]setsar=1[b];[4:v]setsar=1,fps=30,format=yuv420p[o];[c][b]concat=n=2:v=1:a=0[cb];[cb][o]concat=n=2:v=1:a=0[v];'
          '[0:a]aresample=48000,aformat=channel_layouts=stereo[ca];[2:a]aresample=48000,aformat=channel_layouts=stereo[ba];'
          '[ca][ba]concat=n=2:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[vx];' + mus +
          '[4:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1.5,aresample=48000[oa];[mix][oa]concat=n=2:v=0:a=1[a]')
    inp = ['-i', 'cover.mp4', '-i', 'body.mp4', '-i', 'cut.mov', '-ss', f'{s0:.3f}', '-t', f'{body + 1:.2f}', '-i', SONG, '-i', OUTRO]
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '17', '-preset', 'slow',
                    '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)
if __name__ == '__main__':
    os.chdir(os.environ.get('WORK', f'{SCR}/es/nivus_talk')); os.makedirs('.', exist_ok=True); s = sys.argv[1]
    if s == 'cut': make_cut()
    elif s == 'render': render()
    elif s == 'cover': cover()
    elif s == 'final': final(sys.argv[2], len(sys.argv) < 4)
    elif s == 'words': print(' | '.join(f'{w[2]}@{w[0]:.2f}' for w in caption_words()), starts())
