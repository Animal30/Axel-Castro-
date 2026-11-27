"""Piezas de video compartidas (CarMax EcoSport Freestyle). Todo vertical 1080x1920 @30."""
import os, subprocess
W, H, FPS = 1080, 1920, 30
SCR = '/tmp/claude-0/-home-user/74e478c3-632a-51d9-acc1-5b85b595e003/scratchpad'
RAW = os.environ.get('RAW', f'{SCR}/pres/raw'); TX = os.environ.get('TX', f'{SCR}/pres/tx')
SONG = '/mnt/project-files/uploads/hearth/ea66fe5b-dbfb-4626-b006-504a099de555'   # Inner Bloom (mp3)
OUTRO = '/mnt/project-files/carmax/outro-logo/carmax-logo-barrido-con-musica.mp4'
GRADE = 'eq=contrast=1.07:saturation=1.08:gamma=1.02,colorbalance=rs=0.012:bs=-0.012:rh=0.02:bh=-0.02,vignette=PI/9'
ROT = {'0166', '0200'}          # estos dos clips quedaron guardados girados (sin metadata)
B = 0.48847; DROP = 64.111      # Inner Bloom: periodo de beat y primer golpe del drop (s de la canción)

def piece(out, clip, ss, d, speed=1.0, push=0.05, flash=False, grade=True):
    """clip ss..ss+d*speed -> d segundos de salida, empuje suave de cámara, flash blanco opcional."""
    nf = round(d * FPS); D = nf / FPS
    rot = 'transpose=2,' if clip in ROT else ''
    vf = (f"trim={ss}:{ss + d * speed + 0.3},setpts=(PTS-STARTPTS)/{speed},fps={FPS},{rot}"
          f"scale=1242:2208:force_original_aspect_ratio=increase:flags=lanczos,crop=1242:2208,"
          f"scale=w='trunc(1242*(1+{push}*min(t/{D},1))/2)*2':h=-2:eval=frame:flags=bicubic,crop={W}:{H},"
          + (GRADE + ',' if grade else '') +
          (f"eq=brightness='0.30*max(0,1-t/0.16)':eval=frame," if flash else '') + "format=yuv420p")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{RAW}/{clip}.mp4', '-map', '0:v:0', '-vf', vf, '-an',
                    '-frames:v', str(nf), '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-r', str(FPS), out], check=True)
