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
NOZOOM = {'0434', '0435'}   # insignias (Strada F.L.G., Working 1.4): ni zoom ni estabilizador, para no comerse letras en los bordes
def fx_piece(src, dst, d, in_t, out_t, full, size, nozoom=False):
    """transicion segun el golpe: grave = golpe de zoom + destello, agudo = entrada suave; las tomas del auto entero no recortan al salir"""
    w, h = size; a, b = FX[in_t], FX[out_t]; ai = 0 if nozoom else a['ai'] * (0.3 if full else 1); ao = 0 if (full or nozoom) else b['ao']; do = b['do']
    z = f"(1+{ai}*pow(max(0,1-t/{a['di']}),2)+{ao}*pow(max(0,(t-({d}-{do}))/{do}),2))"
    vf = f"scale=w='trunc({w}*{z}/2)*2':h=-2:eval=frame:flags=bicubic,crop={w}:{h}"
    if a['fl']: vf += f",eq=brightness='{a['fl']}*max(0,1-t/0.14)':eval=frame"
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vf', vf + ',format=yuv420p', '-an', '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-r', str(FPS), dst], check=True)
STRADA2 = [('0428', 10.0, 10.9), ('0434', 1.9, 2.85), ('0435', 0.45, 2.5), ('0441', 0.2, 3.0), ('0443', 2.2, 4.7),
           ('0444', 2.0, 5.0), ('0436', 5.0, 8.0), ('0429', 3.4, 6.1)]   # sin 0438 (casi igual a la ultima); insignias completas
def auto_plan(wav, shots, offset, end, lead=(1.0, 1.9)):
    """cortes sobre los golpes de la cancion (desde `offset`, `end` segundos): reparte las tomas segun su fuente, elige el golpe
    mas fuerte cerca de cada punto y clasifica cada corte: drop / B (grave) / T (agudo) / soft, para la transicion."""
    import librosa, numpy as np
    y, sr = librosa.load(wav, sr=22050, offset=offset, duration=end + 0.5)
    n, hop = 2048, 256; S = np.abs(librosa.stft(y, n_fft=n, hop_length=hop)); fr = librosa.fft_frequencies(sr=sr, n_fft=n)
    def band(lo, hi):
        b = S[(fr >= lo) & (fr < hi)].sum(0); d = np.diff(b, prepend=0).clip(0); return d / (d.max() + 1e-9)
    low, high = band(20, 180), band(3000, 9000)
    full = librosa.onset.onset_strength(S=librosa.amplitude_to_db(S), sr=sr, hop_length=hop); full /= full.max()
    sc = 0.5 * low + 0.5 * full; t = librosa.frames_to_time(np.arange(len(sc)), sr=sr, hop_length=hop)
    pk = librosa.util.peak_pick(sc, pre_max=8, post_max=8, pre_avg=24, post_avg=24, delta=0.06, wait=30)
    H = [(float(t[i]), float(sc[i]), float(low[max(0, i - 3):i + 4].max()), float(high[max(0, i - 3):i + 4].max())) for i in pk if 0.9 < t[i] < end - 1.5]
    src = [1.3] + [min(3.6, max(2.0, (se - ss) / 0.9)) for _, ss, se in shots[1:]]; tot = sum(src); cuts = []; types = []; prev = 0.0
    first = [h for h in H if lead[0] <= h[0] <= lead[1]]
    for i in range(len(shots) - 1):
        ideal = (end * sum(src[:i + 1]) / tot) if i else (max(first, key=lambda h: h[1])[0] if first else 1.4)
        room = 1.3 * (len(shots) - 2 - i) + 1.6
        cand = [h for h in H if h[0] > prev + 1.1 and h[0] < end - room]
        if i == 0 and first: cand = first
        best = max(cand, key=lambda h: h[1] - 0.5 * abs(h[0] - ideal)) if cand else (ideal, 0, 0, 0)
        cuts.append(round(best[0] * FPS) / FPS); prev = cuts[-1]
        ty = 'drop' if best[2] > 0.8 and best[1] > 0.5 else 'B' if best[2] >= max(best[3], 0.25) else 'T' if best[3] > 0.15 else 'soft'
        types.append(ty)
    return dict(wav=wav, offset=offset, end=end, cuts=cuts, types=types, shots=shots)
AB2 = [('0446', 4.4, 5.4), ('0450', 0.0, 2.2), ('0448', 0.0, 1.9), ('0452', 0.0, 2.4), ('0458', 1.0, 3.2), ('0461', 0.3, 3.0),
       ('0462', 3.5, 7.0), ('0447', 2.0, 4.5), ('0448', 4.5, 6.8)]   # 0448 dos veces: rueda sola al principio y cierre con la camioneta entera
AB2_FULL = {'0446', '0450', '0452', '0462', '0448'}                  # tomas sin recorte (auto entero / insignias)
ROT_INTRO = f'{SCRN}/cine/rot/rot_es.mp4'
def rot_wrap(src, dst, intro_s=2.6):
    """video horizontal -> vertical 9:16 girado 90 grados horario (se ve derecho al girar el celular a la izquierda),
    con el reel de 'please rotate your phone' al principio; la musica arranca cuando entra la portada"""
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-t', f'{intro_s}', '-i', ROT_INTRO, '-i', src, '-f', 'lavfi', '-t', f'{intro_s}', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-filter_complex', "[0:v]setsar=1,fps=30,scale=1080:1920,format=yuv420p[a];[1:v]transpose=1,setsar=1,fps=30,scale=1080:1920,format=yuv420p[b];[a][b]concat=n=2:v=1:a=0[v];"
                    "[2:a]aresample=48000,aformat=channel_layouts=stereo[sa];[1:a]aresample=48000,aformat=channel_layouts=stereo[ma];[sa][ma]concat=n=2:v=0:a=1[a]",
                    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '17', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709',
                    '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', dst], check=True)
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
            full_piece(pr, f'{cs.RAW}/{nm}.mp4', d, size, z0=1.0 if (i == 0 or clip in NOZOOM) else 1.045); open(pf + '.ok', 'w').close()
        elif land: C.land_piece(pr, nm, 0.0, d, 1.0, 0.03)  # primeros planos (si no estan en FULL)
        else: cs.piece_any(pr, nm, 0.0, d, 1.0, 0.03)
        os.remove(f'{cs.RAW}/{nm}.mp4')
        if types:
            fx_piece(pr, pf, d, None if i == 0 else types[i - 1], types[i] if i < len(types) else None, full, size, nozoom=clip in NOZOOM); os.remove(pr)
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
    if len(sys.argv) > 2 and sys.argv[2] == 'auto':
        wav, off, end = sys.argv[3], float(sys.argv[4]), float(sys.argv[5]); shots = STRADA2 if car == 'strada' else AB2 if car == 'amarok-blanca' else SHOTS[car]
        P = auto_plan(wav, shots, off, end); PLANS[car] = P; SHOTS[car] = shots
        if car == 'strada': C.CARS['strada']['cy'] = 520
        FULL.setdefault(car, set()); FULL[car] |= NOZOOM if car == 'strada' else set(); FULL[car] = AB2_FULL if car == 'amarok-blanca' else FULL[car]; NOZOOM.update({'0450', '0452'} if car == 'amarok-blanca' else set()); print(P['cuts'], P['types'])
        if len(sys.argv) > 6 and sys.argv[6] == 'plan': sys.exit()
    wd = os.environ.get('WORK', f'{LONG}/{car}'); os.makedirs(wd, exist_ok=True); os.chdir(wd); build(car)
    if car == 'amarok-blanca' and os.environ.get('ROT') == '1':
        for n in ('con', 'sin'): rot_wrap(f'{n}.mp4', f'rot_{n}.mp4')
