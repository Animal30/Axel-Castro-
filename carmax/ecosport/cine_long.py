"""Showcases cinematicos LARGOS (~2x) con la cancion del reel extendida por compases (27/11, pedido de Nahuel):
mas tomas (ruedas, capo, costados, detalles), todas estabilizadas (vidstab), cada toma completa y cortes en golpes.
python3 cine_long.py <auto>   -> WORK=<scratch>/cine/long/<auto>   (con.mp4, sin.mp4, cover.png)
Cancion extendida + golpes: <scratch>/cine/long/<song>.wav y hits.json (ver extend en el historial del hilo)."""
import os, sys, json, subprocess
SCRN = '/tmp/claude-0/-home-user/74e478c3-632a-51d9-acc1-5b85b595e003/scratchpad'
os.environ.setdefault('RAW', f'{SCRN}/new/raw')
from PIL import Image
import car_show as cs
import cine_show as C
from common import FPS

LONG = f'{SCRN}/cine/long'
SHOTS = {
 'trailblazer': [('0347', 3.9, None), ('0356', 0.3, 2.6), ('0352', 0.0, 2.3), ('0354', 2.0, 4.9),
                 ('0358', 0.5, 4.1), ('0359', 3.0, 6.1), ('0357', 1.0, 3.1), ('0361', 2.0, 4.3), ('0362', 2.5, 5.5), ('0349', 5.6, 8.0)],
 'amarok-plata': [('0371', 6.0, None), ('0373', 0.0, 1.6), ('0372', 0.3, 2.8), ('0378', 0.3, 2.6), ('0379', 1.2, 3.7), ('0375', 1.5, 4.1),
                  ('0383', 0.5, 2.8), ('0381', 0.8, 2.2), ('0384', 1.5, 3.1), ('0385', 0.3, 2.2), ('0377', 0.0, 1.7), ('0380', 0.0, 0.9)],
 'hilux': [('0392', 0.5, None), ('0393', 0.5, 4.0), ('0401', 0.0, 1.6), ('0413', 0.5, 3.3), ('0404', 2.5, 5.0), ('0409', 0.2, 2.2),
           ('0410', 0.5, 2.8), ('0398', 4.6, 6.4)],
 'saveiro': [('0414', 8.8, None), ('0415', 0.3, 3.0), ('0420', 0.3, 2.0), ('0416', 2.0, 5.0), ('0421', 2.0, 5.0),
             ('0422', 0.3, 3.0), ('0423', 0.5, 3.0), ('0424', 4.5, 7.0), ('0427', 1.5, 4.0), ('0417', 5.0, 7.7)],
 'strada': [('0428', 9.0, None), ('0434', 0.0, 2.6), ('0435', 0.0, 2.8), ('0441', 0.2, 3.0), ('0443', 2.2, 4.7),
            ('0439', 2.5, 4.6), ('0444', 2.0, 5.0), ('0436', 5.0, 8.0), ('0438', 5.5, 8.8), ('0429', 3.4, 6.1)],
 'amarok-blanca': [('0446', 4.4, None), ('0450', 0.0, 2.2), ('0449', 2.0, 5.0), ('0452', 0.0, 2.4), ('0458', 1.0, 3.2), ('0461', 0.3, 3.0),
                   ('0462', 3.0, 6.5), ('0447', 5.5, 8.0), ('0454', 7.0, 9.6), ('0448', 4.5, 6.8)],
}

# tomas que terminan mostrando el auto entero: sin estabilizador ni zoom que recorte; abren apenas cerradas
# y terminan en el cuadro completo, asi nunca se corta la rueda (pedido de Nahuel 27/11)
FULL = {'trailblazer': {'0347', '0362', '0349'}, 'amarok-plata': {'0371', '0379', '0380'}, 'hilux': {'0392', '0404', '0398'},
        'saveiro': {'0414', '0415', '0421', '0417'}, 'strada': {'0428', '0436', '0438', '0429'},
        'amarok-blanca': {'0446', '0462', '0447', '0454', '0448'}}
def full_piece(out, src, d, size, z0=1.045):
    nf = round(d * FPS); D = nf / FPS; w, h = size
    vf = (f"fps={FPS},scale=w='trunc({w}*({z0}-({z0}-1)*min(t/{D},1))/2)*2':h=-2:eval=frame:flags=bicubic,crop={w}:{h},"
          f"{C.GRADE},format=yuv420p")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vf', vf, '-an', '-frames:v', str(nf), '-c:v', 'libx264',
                    '-crf', '12', '-preset', 'fast', '-r', str(FPS), out], check=True)
def valid(p, d):
    try:
        n = int(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries',
                                         'stream=nb_read_frames', '-of', 'csv=p=0', p]).strip())
        return n == round(d * FPS)
    except Exception: return False
VACUO = dict(wav=f'{SCRN}/cine/vacuo/song.wav', offset=15.1, end=27.5,
             cuts=[1.40, 4.16, 6.91, 9.65, 13.08, 15.84, 18.59, 19.96, 22.02, 24.08, 25.46],
             shots=[('0371', 6.0, None), ('0373', 0.0, 2.4), ('0372', 0.3, 2.8), ('0378', 0.3, 2.6), ('0379', 0.3, 3.6), ('0375', 1.0, 4.0),
                    ('0383', 0.5, 2.8), ('0381', 0.8, 2.2), ('0384', 1.5, 3.1), ('0385', 0.3, 2.2), ('0377', 0.0, 1.7), ('0380', 0.0, 0.9)])
# Trailblazer v2 (27/11): "vacuo (super slowed)" de NIKO, ultima parte (drop en 99.66 s de la cancion), transiciones por tipo de golpe
# tipos de corte: drop (golpe grave fuerte), B (grave), T (agudo/hi-hat), soft. Cada uno cambia la transicion del video.
TB2 = dict(wav=f'{SCRN}/cine/vacuo/song.wav', offset=98.4, end=25.0,
           cuts=[1.26, 4.01, 6.07, 8.50, 11.26, 15.54, 18.14, 20.87, 23.00],
           types=['drop', 'B', 'B', 'T', 'T', 'T', 'B', 'T', 'soft'],
           shots=[('0347', 4.65, 5.15), ('0356', 0.3, 2.6), ('0350', 0.0, 1.5), ('0352', 0.0, 2.3), ('0354', 2.0, 4.9), ('0358', 0.5, 4.1),
                  ('0357', 1.0, 3.1), ('0361', 2.0, 4.3), ('0362', 3.0, 5.5), ('0349', 5.9, 8.0)])
PLANS = {}
if os.environ.get('VACUO') == '1': PLANS['amarok-plata'] = VACUO
if os.environ.get('TB2') == '1': PLANS['trailblazer'] = TB2
for _k, _p in PLANS.items(): SHOTS[_k] = _p['shots']
USE_VACUO = 'amarok-plata' in PLANS
FX = {'drop': dict(ai=0.16, di=0.35, fl=0.35, ao=0.06, do=0.10), 'B': dict(ai=0.10, di=0.25, fl=0.22, ao=0.05, do=0.10),
      'T': dict(ai=0.05, di=0.30, fl=0.0, ao=0.0, do=0.10), 'soft': dict(ai=0.03, di=0.30, fl=0.0, ao=0.0, do=0.10), None: dict(ai=0, di=0.3, fl=0, ao=0, do=0.1)}
def fx_piece(src, dst, d, in_t, out_t, full, size):
    """transicion segun el golpe: grave = golpe de zoom + destello, agudo = entrada suave; las tomas del auto entero no recortan al salir"""
    w, h = size; a, b = FX[in_t], FX[out_t]; ai = a['ai'] * (0.3 if full else 1); ao = 0 if full else b['ao']; do = b['do']
    z = f"(1+{ai}*pow(max(0,1-t/{a['di']}),2)+{ao}*pow(max(0,(t-({d}-{do}))/{do}),2))"
    vf = f"scale=w='trunc({w}*{z}/2)*2':h=-2:eval=frame:flags=bicubic,crop={w}:{h}"
    if a['fl']: vf += f",eq=brightness='{a['fl']}*max(0,1-t/0.14)':eval=frame"
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vf', vf + ',format=yuv420p', '-an', '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-r', str(FPS), dst], check=True)
def assign(car):
    if car in PLANS: return PLANS[car]['cuts'], PLANS[car]['end']
    """elige los cortes: para cada toma, el golpe mas cercano a donde terminaria a velocidad ~1 (0.8-1.25)"""
    c = C.CARS[car]; H = json.load(open(f'{LONG}/hits.json'))[c['song']]; end = H['dur'] - 0.05
    hits = [t for t, s in H['hits'] if s > 0.2 and 0.8 < t < end - 1.0]
    shots = SHOTS[car]; t = 0.0; cuts = []
    rem_src = lambda k: sum((se - ss) for _, ss, se in shots[k:] if se)
    for i, (clip, ss, se) in enumerate(shots[:-1]):
        # repartir el tiempo restante en proporcion a la fuente que queda
        left = end - t; src = (se - ss) if se else 1.8; share = left * src / (rem_src(i) + (0 if se else 1.8))
        want = t + max(1.3, share)
        cand = [h for h in hits if t + 1.1 < h < end - 1.4 * (len(shots) - 1 - i)]
        nxt = min(cand, key=lambda h: abs(h - want)) if cand else want
        cuts.append(nxt); t = nxt
    return cuts, end

def prep(name, clip, ss, d, speed, land, stab=True):
    """fuente intermedia: recorte + velocidad + escala (+ interpolacion si es lenta) + estabilizado vidstab"""
    L = land or cs.ORIENT.get(clip) == 'L'; sc = '1920:1080' if L else '1242:2208'
    mi = f",minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" if speed < 0.9 else f",fps={FPS}"
    tmp = f'{cs.RAW}/{name}_a.mp4'; out = f'{cs.RAW}/{name}.mp4'; trf = f'/tmp/{name}.trf'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{cs.RAW}/{clip}.mp4', '-map', '0:v:0', '-vf',
                    f"trim={ss}:{ss + d * speed + 0.25},setpts=(PTS-STARTPTS)/{speed},scale={sc}:flags=lanczos{mi},format=yuv420p",
                    '-an', '-t', f'{d + 0.2:.3f}', '-c:v', 'libx264', '-crf', '11', '-preset', 'fast', tmp], check=True)
    if not stab:
        os.replace(tmp, out); cs.ORIENT[name] = 'L' if L else 'V'; return
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-vf', f'vidstabdetect=shakiness=6:accuracy=12:result={trf}', '-f', 'null', '-'], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-vf',
                    f'vidstabtransform=input={trf}:smoothing=18:optzoom=1:interpol=bicubic,unsharp=5:5:0.5:5:5:0,format=yuv420p',
                    '-an', '-c:v', 'libx264', '-crf', '11', '-preset', 'fast', out], check=True)
    os.remove(tmp); cs.ORIENT[name] = 'L' if L else 'V'

def build(car):
    c = C.CARS[car]; land = c.get('land'); size = (1920, 1080) if land else (1080, 1920)
    cuts, end = assign(car); b = [0.0] + cuts + [end]; fr = [round(x * FPS) for x in b]
    shots = SHOTS[car]; os.makedirs('p', exist_ok=True); P = []
    for i, (clip, ss, se) in enumerate(shots):
        d = (fr[i + 1] - fr[i]) / FPS
        sp = min(0.85, (C.cs_dur(clip) - 0.2 - ss) / d) if se is None else (se - ss) / d
        P.append((clip, ss, d, sp)); print(car, i, clip, ss, f'{b[i]:.2f}-{b[i + 1]:.2f} d={d:.2f} speed={sp:.2f}', flush=True)
        full = clip in FULL[car]; pf = f'p/{i:02d}.mp4'; types = PLANS.get(car, {}).get('types')
        pr = f'p/r{i:02d}.mp4' if types else pf
        if os.path.exists(pf) and (os.path.exists(pf + '.ok') or not full) and valid(pf, d): continue
        nm = f'st_{car}_{i}'; prep(nm, clip, ss, d, sp, land, stab=not full)
        if full:
            full_piece(pr, f'{cs.RAW}/{nm}.mp4', d, size, z0=1.0 if i == 0 else 1.045); open(pf + '.ok', 'w').close()
        elif land: C.land_piece(pr, nm, 0.0, d, 1.0, 0.03)
        else: cs.piece_any(pr, nm, 0.0, d, 1.0, 0.03)
        os.remove(f'{cs.RAW}/{nm}.mp4')
        if types:
            fx_piece(pr, pf, d, None if i == 0 else types[i - 1], types[i] if i < len(types) else None, full, size); os.remove(pr)
    C.title_layer(car, size).save('title.png')
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', 'p/00.mp4', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    im = Image.frombytes('RGB', size, raw).convert('RGBA'); im.alpha_composite(Image.open('title.png')); im.convert('RGB').save('cover.png')
    with open('list.txt', 'w') as f:
        for i in range(len(P)): f.write(f"file 'p/{i:02d}.mp4'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'body.mp4'], check=True)
    total = sum(p[2] for p in P); fo = max(0.3, P[0][2] - 0.45)
    vf = f"[1:v]format=rgba,fade=t=out:st={fo:.2f}:d=0.35:alpha=1[t];[0:v][t]overlay=0:0:eof_action=pass,format=yuv420p[v]"
    for music in (True, False):
        aud = (['-ss', f'{PLANS[car]["offset"]}', '-i', PLANS[car]['wav']] if car in PLANS else ['-i', f'{LONG}/{c["song"]}.wav'], f";[2:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={total - 0.8:.3f}:d=0.8,"
               "aresample=48000,loudnorm=I=-14:TP=-1.5,aresample=48000[a]") if music else \
              (['-f', 'lavfi', '-t', f'{total:.3f}', '-i', 'anullsrc=r=48000:cl=stereo'], ';[2:a]anull[a]')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'body.mp4', '-loop', '1', '-t', f'{total:.3f}', '-i', 'title.png'] + aud[0] +
                       ['-filter_complex', vf + aud[1], '-map', '[v]', '-map', '[a]', '-t', f'{total:.3f}', '-c:v', 'libx264', '-crf', '18',
                        '-preset', 'slow', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                        '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', 'con.mp4' if music else 'sin.mp4'], check=True)

if __name__ == '__main__':
    car = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == 'plan':
        cuts, end = assign(car); b = [0] + cuts + [end]
        for i, (clip, ss, se) in enumerate(SHOTS[car]):
            d = b[i + 1] - b[i]; print(f'{clip} {b[i]:.2f}-{b[i + 1]:.2f} d={d:.2f} speed={(se - ss) / d if se else 0:.2f}')
        sys.exit()
    wd = os.environ.get('WORK', f'{LONG}/{car}'); os.makedirs(wd, exist_ok=True); os.chdir(wd); build(car)
