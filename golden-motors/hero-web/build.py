"""Golden Motors web hero background. python3 build.py"""
import subprocess, os
H = os.path.dirname(os.path.abspath(__file__))
SPEED = 0.75; XF = 0.6; FPS = 30
# clip, start, end (source s), mobile crop centre (0..1 of width)
SHOTS = [
    ('c4392', 0.3, 3.3, 0.33),   # facade + GOLDEN MOTORS sign
    ('c4391', 3.0, 5.7, 0.55),   # push in: Mini + Amarok at the door
    ('c4393', 0.0, 2.35, 0.40),  # Mini Cooper S close
    ('c4395', 0.0, 2.6, 0.45),   # Audi Q3 + Ford Maverick
    ('c4396', 0.5, 3.0, 0.40),   # showroom: Corolla Cross, Audi, logo
    ('c4399', 0.4, 3.0, 0.50),   # Amarok in studio
    ('c4397', 0.5, 3.0, 0.55),   # Audi + Ka + GM wall
    ('c4398', 2.0, 4.6, 0.55),   # sedans
]
GRADE = "eq=contrast=1.06:saturation=1.08:gamma=0.98,colorbalance=rs=0.02:bs=-0.02:rh=0.02:bh=-0.02,vignette=PI/5"

def seg(i, s, w, h, crop=None):
    c, a, b, cx = s
    vf = f"trim={a}:{b},setpts=(PTS-STARTPTS)/{SPEED},fps={FPS},"
    if crop:
        vf += f"crop=ih*9/16:ih:max(0\\,min(iw-ih*9/16\\,iw*{cx}-ih*9/32)):0,"
    vf += f"scale={w}:{h}:flags=lanczos,{GRADE},format=yuv420p"
    out = f"seg_{crop or 'd'}_{i}.mp4"
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(H, c + '.mov'), '-an', '-vf', vf,
                    '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', out], check=True)
    return out, (b - a) / SPEED

def build(tag, w, h, crop=None):
    parts = [seg(i, s, w, h, crop) for i, s in enumerate(SHOTS)]
    inputs = sum([['-i', p] for p, _ in parts], [])
    fc = ''; prev = '[0:v]'; t = parts[0][1]
    for k in range(1, len(parts)):
        off = t - XF
        fc += f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{k}];"
        prev = f'[x{k}]'; t = off + parts[k][1]
    fc += f"{prev}fade=t=in:st=0:d=0.5,fade=t=out:st={t-0.6:.3f}:d=0.6,format=yuv420p[v]"
    master = f'master_{tag}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex', fc, '-map', '[v]',
                    '-c:v', 'libx264', '-crf', '14', '-preset', 'slow', master], check=True)
    print(tag, round(t, 2), 's')
    return master

if __name__ == '__main__':
    os.chdir(H)
    build('desk', 1920, 1080)
    build('mob', 720, 1280, crop='m')
