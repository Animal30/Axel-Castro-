"""Ford Ka showcase in the style of the '10 car shots' reference reel (cuts + audio of the reference). python3 v3.py build"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw')
FD = '/home/user/Axel-Castro-/golden-motors/fonts/BarlowCondensed-'
W, H, FPS = 1080, 1920, 30
GRADE = 'eq=contrast=1.07:saturation=1.10:gamma=1.06,colorbalance=rs=0.02:bs=-0.02:rh=0.02:bh=-0.03,vignette=PI/8'
CUTS = [0, 3.03, 4.20, 5.30, 6.43, 7.60, 8.70, 9.83, 11.00, 12.10, 13.23, 15.54]   # measured on the reference reel
# clip, src start, speed, label
SHOTS = [('0043', 0.0, 0.65, None),
         ('0038', 0.0, 0.8, 'FARO'), ('0037', 0.7, 0.8, 'LOGO FRONTAL'), ('0039', 0.0, 0.8, 'LLANTA'),
         ('0044', 0.0, 0.8, 'ESPEJO'), ('0050', 0.4, 0.8, 'LOGO KA'), ('0053', 0.0, 0.8, 'FAROL TRASERO'),
         ('0041', 1.3, 0.8, 'LATERAL'), ('0046', 0.4, 0.8, 'INTERIOR'), ('0052', 0.3, 0.8, 'TRASERA'),
         ('0057', 4.0, 0.6, 'EL AUTO COMPLETO')]
def esc(s): return s.replace(':', '\\:').replace("'", '')
def dt(text, size, y, color='white', weight='ExtraBold', bw=5):
    return (f"drawtext=fontfile={FD}{weight}.ttf:text='{esc(text)}':fontsize={size}:fontcolor={color}:borderw={bw}:bordercolor=black@0.85:"
            f"x=(w-text_w)/2:y={y}")
def build():
    os.makedirs('p3', exist_ok=True); lst = []
    for i, (c, s, sp, lab) in enumerate(SHOTS):
        d = CUTS[i + 1] - CUTS[i]
        txt = ''
        if i == 0:
            txt = ',' + dt('FORD KA SEL 2018', 56, 900, 'white', 'Bold', 4) + ',' + dt('10 TOMAS', 250, 940, '0xF2B824', 'ExtraBold', 6)
        else:
            txt = ',' + dt(f'TOMA {i}/10', 46, 1490, 'white', 'Bold', 4) + ',' + dt(lab, 76, 1545, 'white', 'ExtraBold', 5)
        vf = f"trim={s}:{s + d * sp + 0.4},setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale={W}:{H}:flags=lanczos,{GRADE},format=yuv420p{txt}"
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{RAW}/c{c}.mov', '-an', '-vf', vf, '-frames:v', str(round(d * FPS)),
                        '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', f'p3/{i:02d}.mp4'], check=True)
        lst.append(f"file '{os.path.abspath(f'p3/{i:02d}.mp4')}'\n")
    open('p3/list.txt', 'w').write(''.join(lst))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'p3/list.txt', '-i', 'ref_audio_src.mp4', '-map', '0:v', '-map', '1:a',
                    '-t', str(CUTS[-1]), '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', 'v3_body.mp4'], check=True)
if __name__ == '__main__': os.chdir(HERE); build()
