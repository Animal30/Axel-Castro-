"""CarMax 2 s logo outro (opción D: CarMax / AUTOMOTORES / línea / CÓRDOBA).
usage: python3 outro.py A|B out.mp4      A = barrido de luz (faro), B = impacto
Writes a silent video; audio is muxed by make.sh."""
import sys, os, math, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

MODE, OUT = sys.argv[1], sys.argv[2]
W, H, FPS, DUR = 1080, 1920, 30, 2.0
N = int(FPS * DUR); SUB = 3  # motion-blur subframes
HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, '..', 'logo-opciones')
rng = np.random.default_rng(11)

OR = np.array([238, 120, 14], np.float32) / 255
WH = np.array([0.96, 0.96, 0.96], np.float32)
GR = np.array([0.62, 0.62, 0.62], np.float32)
HOT = np.array([1.0, 0.86, 0.62], np.float32)

def clamp(x): return min(max(x, 0.0), 1.0)
def seg(t, a, b): return clamp((t - a) / (b - a))
def sstep(x): x = clamp(x); return x * x * (3 - 2 * x)
def eo3(x): x = clamp(x); return 1 - (1 - x) ** 3
def eoexpo(x): x = clamp(x); return 1.0 if x >= 1 else 1 - 2 ** (-10 * x)
def eoback(x, s=1.9): x = clamp(x) - 1; return 1 + (s + 1) * x ** 3 + s * x ** 2

# ---------- layout (option D, block centred on screen) ----------
DY = 95
CAR = ImageFont.truetype(f'{FD}/baloo-2-latin-800-normal.ttf', 220)
AUT = ImageFont.truetype(f'{FD}/orbitron-latin-700-normal.ttf', 50)
COR = ImageFont.truetype(f'{FD}/michroma-latin-400-normal.ttf', 30)

def mask_text(text, font, x, y):
    im = Image.new('L', (W, H)); ImageDraw.Draw(im).text((x, y), text, font=font, fill=255)
    return np.asarray(im, np.float32) / 255

tmp = ImageDraw.Draw(Image.new('L', (1, 1)))
wc = tmp.textlength('CarMax', font=CAR)
M_CAR = mask_text('CarMax', CAR, W / 2 - wc / 2, 600 + DY)
ys, xs = np.nonzero(M_CAR > 0.5)
CAR_BOX = (xs.min(), ys.min(), xs.max(), ys.max()); CAR_CY = (ys.min() + ys.max()) / 2

# AUTOMOTORES letters, tracked to CarMax width
txt = 'AUTOMOTORES'; ws = [tmp.textlength(c, font=AUT) for c in txt]
target = wc - 16; track = (target - sum(ws)) / (len(txt) - 1)
x = W / 2 - target / 2; LET = []
for c, w in zip(txt, ws):
    LET.append((mask_text(c, AUT, 0, 888 + DY), x)); x += w + track
# CÓRDOBA
txt2 = 'CÓRDOBA'; ws2 = [tmp.textlength(c, font=COR) for c in txt2]; tr2 = 14
tot2 = sum(ws2) + tr2 * (len(txt2) - 1); x = W / 2 - tot2 / 2
im = Image.new('L', (W, H)); d = ImageDraw.Draw(im)
for c, w in zip(txt2, ws2): d.text((x, 1050 + DY), c, font=COR, fill=255); x += w + tr2
M_COR = np.asarray(im, np.float32) / 255
LINE_Y = 1010 + DY

# ---------- background ----------
fy, fx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.sqrt(((fx - W / 2) / W) ** 2 + ((fy - (880 + DY)) / W) ** 2)
GLOW = np.exp(-(r / 0.45) ** 2)[..., None] * np.array([0.13, 0.062, 0.012], np.float32)
VIG = (1 - 0.5 * np.clip((np.sqrt(((fx - W / 2) / W) ** 2 + ((fy - H / 2) / H) ** 2) - 0.25) / 0.5, 0, 1))[..., None]
BASE = (np.full((H, W, 3), 0.035, np.float32) + GLOW) * VIG

P_N = 90
P_xy = rng.uniform([0, 300], [W, 1650], (P_N, 2)); P_v = rng.uniform(10, 40, P_N); P_s = rng.uniform(1.2, 3.5, P_N)
P_a = rng.uniform(0.15, 0.6, P_N)
# sparks for B
S_N = 70
S_ang = rng.uniform(0, 2 * math.pi, S_N); S_spd = rng.uniform(500, 1900, S_N); S_len = rng.uniform(20, 70, S_N)

def blur(m, s): return cv2.GaussianBlur(m, (0, 0), s) if s > 0.3 else m

def xform(m, scale=1.0, dx=0.0, dy=0.0, cx=W / 2, cy=CAR_CY):
    if abs(scale - 1) < 1e-4 and dx == 0 and dy == 0: return m
    A = np.float32([[scale, 0, cx - scale * cx + dx], [0, scale, cy - scale * cy + dy]])
    return cv2.warpAffine(m, A, (W, H), flags=cv2.INTER_LINEAR)

def shift_letter(m, x):
    return np.roll(m, int(round(x)), axis=1) if False else cv2.warpAffine(m, np.float32([[1, 0, x], [0, 1, 0]]), (W, H))

def over(img, mask, col, a=1.0):
    m = (mask * a)[..., None]; return img * (1 - m) + col[None, None] * m

def add(img, mask, col, a=1.0): return img + mask[..., None] * col[None, None] * a

def frame(t):
    img = BASE.copy()
    # drifting dust
    pm = np.zeros((H, W), np.float32)
    for (x0, y0), v, s, a in zip(P_xy, P_v, P_s, P_a):
        cv2.circle(pm, (int(x0), int(y0 - v * t)), int(s), float(a), -1, cv2.LINE_AA)
    img = add(img, blur(pm, 1.2), OR, 0.35)

    push = 1.0 + 0.035 * eo3(t / DUR)  # slow camera push-in over whole outro
    shake = (0, 0)

    # ---- CarMax entrance ----
    if MODE == 'A':
        sx = -150 + (W + 300) * sstep(seg(t, 0.0, 0.32))
        reveal = np.clip((sx - fx) / 40 + 0.5, 0, 1) if t < 0.32 else 1.0
        car = M_CAR * reveal
        flash = math.exp(-max(t - 0.30, 0) / 0.09) if t >= 0.22 else 0
        car_s = push
    else:
        p = seg(t, 0.0, 0.24)
        car_s = (2.4 - 1.4 * (p ** 2.2)) * push if t < 0.24 else push
        car = M_CAR * clamp(t / 0.12)
        flash = math.exp(-max(t - 0.24, 0) / 0.08) if t >= 0.24 else 0
        if t >= 0.24:
            k = math.exp(-(t - 0.24) / 0.09) * 26
            shake = (k * math.sin(t * 95), k * math.cos(t * 83))
    car = xform(car, car_s, *shake)
    # glow + body
    img = add(img, blur(car, 34), OR, 0.42 + 0.9 * flash)
    img = add(img, blur(car, 10), OR, 0.35 + 0.6 * flash)
    col = OR * (1 - flash) + HOT * flash
    img = over(img, car, col)

    # shine sweep across CarMax (1.0 - 1.4 s)
    sp = seg(t, 1.0, 1.4)
    if 0 < sp < 1:
        x0, y0, x1, y1 = CAR_BOX
        dd = (fx - x0) / (x1 - x0) + (fy - y0) / (x1 - x0) * 0.5 - (-0.3 + 1.8 * sp)
        sh = np.exp(-(dd / 0.05) ** 2)
        img = add(img, car * sh, HOT, 0.75)

    # light streak (A) / shockwave + sparks (B)
    if MODE == 'A' and t < 0.45:
        sx = -150 + (W + 300) * sstep(seg(t, 0.0, 0.32))
        fade = 1 - seg(t, 0.32, 0.45)
        streak = np.exp(-((fy - CAR_CY) / 5) ** 2) * np.exp(-((fx - sx) / 420) ** 2)
        core = np.exp(-((fy - CAR_CY) / 70) ** 2) * np.exp(-((fx - sx) / 60) ** 2)
        img = add(img, streak, HOT, 1.6 * fade); img = add(img, core, HOT, 0.9 * fade)
    if MODE == 'B' and 0.24 <= t < 0.75:
        q = (t - 0.24) / 0.5
        rad = 80 + 900 * eo3(q)
        rr = np.sqrt((fx - W / 2) ** 2 + ((fy - CAR_CY) * 1.15) ** 2)
        ring = np.exp(-((rr - rad) / (8 + 30 * q)) ** 2) * max(1 - q, 0) ** 1.5
        img = add(img, ring, OR, 1.2)
        sm = np.zeros((H, W), np.float32)
        for a, s, L in zip(S_ang, S_spd, S_len):
            d0 = s * (t - 0.24) * (1 - 0.5 * q); dx, dy = math.cos(a), math.sin(a)
            x0, y0 = W / 2 + dx * (120 + d0), CAR_CY + dy * (60 + d0 * 0.8)
            cv2.line(sm, (int(x0), int(y0)), (int(x0 + dx * L), int(y0 + dy * L)), float(max(1 - q, 0)), 2, cv2.LINE_AA)
        img = add(img, blur(sm, 1.0), HOT, 1.0)
    # global flash
    img = img + flash * 0.035 * HOT[None, None]

    # ---- AUTOMOTORES: letters collapse in from wide tracking ----
    pa = seg(t, 0.34, 0.80)
    if pa > 0:
        e = eoexpo(pa); lm = np.zeros((H, W), np.float32)
        for i, (m, x) in enumerate(LET):
            off = (i - (len(LET) - 1) / 2) * 70 * (1 - e)
            lm = np.maximum(lm, shift_letter(m, x + off))
        lm = blur(lm, 6 * (1 - e)) * clamp(pa * 2.2)
        lm = xform(lm, push)
        img = over(img, lm, WH)
    # ---- line draws from centre ----
    pl = eo3(seg(t, 0.62, 0.92))
    if pl > 0:
        half = 60 * pl; lm = np.zeros((H, W), np.float32)
        cv2.rectangle(lm, (int(W / 2 - half), LINE_Y), (int(W / 2 + half), LINE_Y + 3), 1.0, -1)
        lm = xform(lm, push); img = add(img, blur(lm, 6), OR, 0.8); img = over(img, lm, OR)
    # ---- CÓRDOBA ----
    pc = eo3(seg(t, 0.80, 1.12))
    if pc > 0:
        m = xform(M_COR, push, 0, 18 * (1 - pc)); img = over(img, m, GR, pc)

    # film grain
    img = img + rng.normal(0, 0.012, (H // 4, W // 4)).repeat(4, 0).repeat(4, 1)[..., None]
    return np.clip(img, 0, 1)

cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
       '-c:v', 'libx264', '-crf', '12', '-preset', 'slow', '-pix_fmt', 'yuv420p',
       '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', OUT]
pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for i in range(N):
    acc = np.zeros((H, W, 3), np.float32)
    for s in range(SUB): acc += frame((i + s / SUB) / FPS)
    pr.stdin.write((acc / SUB * 255).astype(np.uint8).tobytes())
pr.stdin.close(); pr.wait()
