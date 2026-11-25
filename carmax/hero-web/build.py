"""CarMax web hero background (same steps as golden-motors/hero-web).
python3 build.py RAW_DIR OUT_DIR
Horizontal 4K clips -> desktop 1920x1080, vertical 4K clips -> phone 720x1280.
0.75x slow-mo, light grade, crossfades, fade in/out, muted. MP4 + WebM + posters."""
import subprocess, os, sys
RAW, OUT = sys.argv[1], sys.argv[2]
SPEED = 0.75; XF = 0.6; FPS = 30
CRF = {'d': '25', 'm': '25'}; MAXR = {'d': '2600k', 'm': '1400k'}
GRADE = "eq=contrast=1.06:saturation=1.08:gamma=0.98,colorbalance=rs=0.02:bs=-0.02:rh=0.02:bh=-0.02,vignette=PI/5"
DESK = [  # clip, start, end (source s)
    ('IMG_4659', 0.4, 3.6),   # low angle: CarMax sign against the sky
    ('IMG_4652', 0.3, 3.5),   # facade + red car + fleet at the door
    ('IMG_4660', 8.3, 11.3),  # fleet row along the street
    ('IMG_4661', 4.0, 7.0),   # pickups: Amarok, Hilux
    ('IMG_4658', 7.5, 10.5),  # VW Nivus at the door
    ('IMG_4672', 1.0, 4.4),   # showroom inside
    ('IMG_4656', 12.6, 15.6), # fleet on the street + Corolla, closing
]
MOB = [
    ('IMG_4664', 0.3, 3.6),   # CarMax sign + red car
    ('IMG_4667', 0.0, 3.2),   # CarMax AUTOMOTORES + Jeep
    ('IMG_4663', 3.2, 6.4),   # pickups
    ('IMG_4671', 0.0, 3.0),   # Nivus side detail
    ('IMG_4673', 0.0, 3.6),   # showroom inside, CarMax wall
    ('IMG_4670', 8.4, 11.4),  # street fleet, closing
]

def seg(i, s, w, h, tag):
    c, a, b = s
    vf = (f"trim={a}:{b},setpts=(PTS-STARTPTS)/{SPEED},fps={FPS},"
          f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h},{GRADE},format=yuv420p")
    out = f"/tmp/carmax_seg_{tag}_{i}.mp4"
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(RAW, c + '.MOV'), '-an', '-vf', vf,
                    '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', out], check=True)
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out],
                             capture_output=True, text=True).stdout)
    assert abs(d - (b - a) / SPEED) < 0.1, f'{c}: segment shorter than asked ({d:.2f}s)'
    return out, (b - a) / SPEED

def build(tag, shots, w, h, name):
    parts = [seg(i, s, w, h, tag) for i, s in enumerate(shots)]
    inputs = sum([['-i', p] for p, _ in parts], [])
    fc = ''; prev = '[0:v]'; t = parts[0][1]
    for k in range(1, len(parts)):
        off = t - XF
        fc += f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{k}];"
        prev = f'[x{k}]'; t = off + parts[k][1]
    fc += f"{prev}fade=t=in:st=0:d=0.5,fade=t=out:st={t-0.6:.3f}:d=0.6,format=yuv420p[v]"
    base = os.path.join(OUT, name)
    tagc = ['-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709']
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex', fc, '-map', '[v]',
                    '-c:v', 'libx264', '-crf', CRF[tag], '-maxrate', MAXR[tag], '-bufsize', MAXR[tag], '-preset', 'slow', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
                    *tagc, '-movflags', '+faststart', '-an', base + '.mp4'], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', base + '.mp4', '-c:v', 'libvpx-vp9', '-crf', '38',
                    '-b:v', MAXR[tag], '-row-mt', '1', '-deadline', 'good', '-cpu-used', '2', '-an', base + '.webm'], check=True)
    poster = base.replace('hero-', 'hero-poster-').rsplit('-', 1)[0] + '.jpg'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '1.6', '-i', base + '.mp4', '-frames:v', '1',
                    '-q:v', '3', poster], check=True)
    print(name, round(t, 2), 's')

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[3] if len(sys.argv) > 3 else 'both'
    if which in ('both', 'desk'): build('d', DESK, 1920, 1080, 'hero-escritorio-1920x1080')
    if which in ('both', 'mob'): build('m', MOB, 720, 1280, 'hero-celular-720x1280')
