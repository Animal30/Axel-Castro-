"""Golden Motors 3 s logo outro. usage: python3 outro.py A|B out_dir"""
import sys, os, math, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

MODE = sys.argv[1]; OUT = sys.argv[2]
W, H, FPS, DUR = 1080, 1920, 30, 3.0
N = int(FPS * DUR)
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(7)

# ---------- palette ----------
G_DARK = np.array([0.36, 0.24, 0.07]); G_MID = np.array([0.83, 0.66, 0.28]); G_LIGHT = np.array([1.0, 0.93, 0.68])
BG = np.array([0.018, 0.016, 0.014])

def ease_out_cubic(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def ease_out_expo(x): x = min(max(x, 0), 1); return 1 if x >= 1 else 1 - 2 ** (-10 * x)
def ease_in_out(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def seg(t, a, b): return min(max((t - a) / (b - a), 0), 1)

# ---------- logo plate (gold, bevelled) ----------
LOGO_H = 600
MASTER = 1.45  # supersample so scale-ups stay sharp
a_full = cv2.imread(os.path.join(HERE, 'logo_alpha.png'), 0).astype(np.float32) / 255
ph = int(LOGO_H * MASTER); pw = int(a_full.shape[1] * ph / a_full.shape[0])
alpha = cv2.resize(a_full, (pw, ph), interpolation=cv2.INTER_AREA)
# bevel lighting from top-left
soft = cv2.GaussianBlur(alpha, (0, 0), 5)
gx = cv2.Sobel(soft, cv2.CV_32F, 1, 0, ksize=5); gy = cv2.Sobel(soft, cv2.CV_32F, 0, 1, ksize=5)
light = -(gx * -0.6 + gy * -0.8); light /= (np.abs(light).max() + 1e-6)
yy, xx = np.mgrid[0:ph, 0:pw].astype(np.float32)
diag = (xx / pw * 0.45 + yy / ph * 0.55)
band = 0.5 + 0.5 * np.sin(diag * 2 * math.pi * 1.15 + 0.6)  # brushed-metal banding
base = G_DARK[None, None] * (1 - band[..., None]) + G_MID[None, None] * band[..., None]
base = base + (G_LIGHT - G_MID)[None, None] * np.clip(light, 0, 1)[..., None] * 0.9
base = base * (1 - 0.45 * np.clip(-light, 0, 1))[..., None]
PLATE = np.clip(base, 0, 1).astype(np.float32)
EDGE_COL = (G_DARK * 0.55).astype(np.float32)

def shine_layer(p):
    """specular sweep, p in 0..1 across the plate diagonally"""
    if p <= 0 or p >= 1: return None
    d = (xx / pw * 0.6 + yy / ph * 0.4) - (-0.25 + 1.5 * p)
    s = np.exp(-(d / 0.06) ** 2) + 0.35 * np.exp(-(d / 0.16) ** 2)
    return s.astype(np.float32)

def plate_rgba(shine_p=-1, tint=1.0):
    rgb = PLATE * tint
    s = shine_layer(shine_p)
    if s is not None: rgb = np.clip(rgb + s[..., None] * np.array([1.0, 0.95, 0.8], np.float32) * 0.85, 0, 1)
    return rgb, alpha

# ---------- background ----------
fy, fx = np.mgrid[0:H, 0:W].astype(np.float32)
CX, CY = W / 2, 800
r = np.sqrt(((fx - CX) / W) ** 2 + ((fy - CY) / W) ** 2)
GLOW_BG = np.exp(-(r / 0.42) ** 2)[..., None] * np.array([0.10, 0.065, 0.02], np.float32)
VIGN = (1 - 0.55 * np.clip((np.sqrt(((fx - W / 2) / W) ** 2 + ((fy - H / 2) / H) ** 2) - 0.25) / 0.5, 0, 1))[..., None]
P_N = 70
P_xy = rng.uniform([0, 200], [W, 1700], (P_N, 2)); P_v = rng.uniform(8, 30, P_N); P_s = rng.uniform(1.0, 3.2, P_N)
P_ph = rng.uniform(0, 6.28, P_N); P_a = rng.uniform(0.15, 0.55, P_N)

def particles(t):
    lay = np.zeros((H, W), np.float32)
    for i in range(P_N):
        x = P_xy[i, 0] + 12 * math.sin(t * 0.8 + P_ph[i]); y = P_xy[i, 1] - P_v[i] * t
        a = P_a[i] * (0.6 + 0.4 * math.sin(t * 3 + P_ph[i]))
        cv2.circle(lay, (int(x), int(y)), int(P_s[i]), a, -1, cv2.LINE_AA)
    lay = cv2.GaussianBlur(lay, (0, 0), 1.6)
    return lay[..., None] * np.array([1.0, 0.8, 0.45], np.float32)

# ---------- compositing helpers ----------
def over(dst, rgb, a):
    dst *= (1 - a[..., None]); dst += rgb * a[..., None]

def place(dst, rgb, a, scale, cy=CY, blur=0, opacity=1.0, glow=0.0):
    s = scale / MASTER
    nw, nh = max(2, int(pw * s)), max(2, int(ph * s))
    interp = cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC
    r_ = cv2.resize(rgb, (nw, nh), interpolation=interp); a_ = cv2.resize(a, (nw, nh), interpolation=interp)
    if blur > 0.3:
        pad = int(blur * 3) + 2
        r_ = cv2.copyMakeBorder(r_, pad, pad, pad, pad, cv2.BORDER_CONSTANT); a_ = cv2.copyMakeBorder(a_, pad, pad, pad, pad, cv2.BORDER_CONSTANT)
        r_ = cv2.GaussianBlur(r_, (0, 0), blur); a_ = cv2.GaussianBlur(a_, (0, 0), blur)
        nh, nw = a_.shape
    x0 = int(CX - nw / 2); y0 = int(cy - nh / 2)
    canvas_a = np.zeros((H, W), np.float32); canvas_r = np.zeros((H, W, 3), np.float32)
    canvas_a[y0:y0 + nh, x0:x0 + nw] = a_; canvas_r[y0:y0 + nh, x0:x0 + nw] = r_
    if glow > 0:
        g = cv2.GaussianBlur(canvas_a, (0, 0), 38)
        dst += g[..., None] * np.array([0.95, 0.68, 0.25], np.float32) * glow
    over(dst, canvas_r, canvas_a * opacity)
    return canvas_a

def project_quad(theta, wz, sc):
    """corners of plate rotated by theta about Y, at depth offset wz (px), focal f"""
    f = 2200.0
    hw, hh = pw / MASTER * sc / 2, ph / MASTER * sc / 2
    pts = []
    for (u, v) in [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]:
        x = u * math.cos(theta) + wz * math.sin(theta)
        z = -u * math.sin(theta) + wz * math.cos(theta)
        k = f / (f + z)
        pts.append((CX + x * k, CY + v * k))
    return np.array(pts, np.float32), (-0 * math.sin(theta) + wz * math.cos(theta))

SRC_Q = np.array([[0, 0], [pw, 0], [pw, ph], [0, ph]], np.float32)

def warp_layer(dst, rgb, a, quad, opacity=1.0):
    M = cv2.getPerspectiveTransform(SRC_Q, quad)
    ra = cv2.warpPerspective(np.dstack([rgb, a]), M, (W, H), flags=cv2.INTER_LINEAR)
    over(dst, ra[..., :3], ra[..., 3] * opacity)
    return ra[..., 3]

def spun_logo(dst, theta, sc, opacity, shine_p, glow):
    depth = 34.0 * sc; L = 14
    layers = []
    for i in range(L + 1):
        wz = -depth / 2 + depth * i / L          # i=0 front face
        q, z = project_quad(theta, wz, sc)
        layers.append((z, i, q))
    layers.sort(key=lambda e: -e[0])              # far first
    lum = 0.55 + 0.45 * abs(math.cos(theta))
    front_rgb, a = plate_rgba(shine_p, lum)
    back_rgb = PLATE * lum * 0.55
    edge = np.broadcast_to(EDGE_COL * (0.7 + 0.6 * abs(math.sin(theta))), PLATE.shape).astype(np.float32)
    if glow > 0:
        q, _ = project_quad(theta, 0, sc)
        M = cv2.getPerspectiveTransform(SRC_Q, q)
        ga = cv2.GaussianBlur(cv2.warpPerspective(a, M, (W, H)), (0, 0), 38)
        dst += ga[..., None] * np.array([0.95, 0.68, 0.25], np.float32) * glow
    for z, i, q in layers:
        rgb = front_rgb if i == 0 else (back_rgb if i == L else edge)
        warp_layer(dst, rgb, a, q, opacity)

# ---------- wordmark ----------
F_BIG = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 66)
F_SM = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Medium.otf', 25)
WM_Y, SUB_Y = 1170, 1268

def text_mask(text, font, y, tracking, letter_alpha):
    img = Image.new('L', (W, H), 0); d = ImageDraw.Draw(img)
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = W / 2 - total / 2
    m = np.zeros((H, W), np.float32)
    for ch, wch, la in zip(text, widths, letter_alpha):
        if la > 0.002 and ch != ' ':
            li = Image.new('L', (W, H), 0); ImageDraw.Draw(li).text((x, y), ch, font=font, fill=255)
            m = np.maximum(m, np.asarray(li, np.float32) / 255 * la)
        x += wch + tracking
    return m, total

TXT_GRAD = (G_MID[None, None] * (1 - (fy / H)[..., None]) + G_LIGHT[None, None] * (fy / H)[..., None])

def wordmark(dst, t, t0):
    p = seg(t, t0, t0 + 0.75)
    if p <= 0: return
    name = 'GOLDEN MOTORS'
    la = [ease_out_cubic(seg(t, t0 + i * 0.035, t0 + i * 0.035 + 0.45)) for i in range(len(name))]
    trk = 30 - 12 * ease_out_cubic(p)
    m, tot = text_mask(name, F_BIG, WM_Y, trk, la)
    col = np.clip(TXT_GRAD * 1.02 + 0.0, 0, 1)
    over(dst, col.astype(np.float32), m)
    # thin lines + CÓRDOBA
    q = ease_out_cubic(seg(t, t0 + 0.35, t0 + 1.0))
    if q > 0:
        sub = 'CÓRDOBA'
        ms, stot = text_mask(sub, F_SM, SUB_Y, 14, [q] * len(sub))
        over(dst, np.broadcast_to(np.array([0.78, 0.68, 0.48], np.float32), (H, W, 3)).copy(), ms * 0.95)
        ln = np.zeros((H, W), np.float32)
        gap = stot / 2 + 26; L = 120 * q; yl = SUB_Y + 17
        cv2.line(ln, (int(W / 2 - gap - L), yl), (int(W / 2 - gap), yl), q, 2, cv2.LINE_AA)
        cv2.line(ln, (int(W / 2 + gap), yl), (int(W / 2 + gap + L), yl), q, 2, cv2.LINE_AA)
        over(dst, np.broadcast_to(G_MID.astype(np.float32), (H, W, 3)).copy(), ln * 0.8)

# ---------- frame ----------
GRAIN = [rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]

def frame(t):
    img = np.broadcast_to(BG.astype(np.float32), (H, W, 3)).copy()
    if MODE == 'A':
        e = ease_out_expo(seg(t, 0.0, 1.15))
        sc = (0.78 + 0.22 * e) * (1 + 0.025 * seg(t, 1.15, 3.0))
        bl = 16 * (1 - ease_out_cubic(seg(t, 0.0, 0.95)))
        op = ease_in_out(seg(t, 0.0, 0.55))
        flare = math.exp(-((t - 1.05) / 0.22) ** 2)
        bgk = 0.25 + 0.75 * ease_in_out(seg(t, 0.1, 1.2)) + 0.5 * flare
        img += GLOW_BG * bgk
        img += particles(t) * (0.3 + 0.7 * seg(t, 0.2, 1.2))
        rgb, a = plate_rgba(seg(t, 1.0, 1.75), 0.35 + 0.65 * ease_in_out(seg(t, 0.0, 1.0)))
        place(img, rgb, a, sc, blur=bl, opacity=op, glow=0.18 + 0.55 * flare)
        wordmark(img, t, 1.35)
    else:
        sp = seg(t, 0.0, 1.55)
        subs = 4 if sp < 0.85 else 1
        acc = np.zeros((H, W, 3), np.float32)
        flare = math.exp(-((t - 1.55) / 0.22) ** 2)
        for k in range(subs):
            tt = t + (k / subs - 0.5) / FPS * 0.9 if subs > 1 else t
            e = ease_out_cubic(seg(tt, 0.0, 1.55))
            theta = math.radians(-450 * (1 - e))
            sc = (0.88 + 0.12 * ease_out_cubic(seg(tt, 0.0, 1.2))) * (1 + 0.02 * seg(tt, 1.55, 3.0))
            op = ease_in_out(seg(tt, 0.0, 0.3))
            base = img.copy()
            base += GLOW_BG * (0.3 + 0.7 * ease_in_out(seg(tt, 0.0, 1.4)) + 0.5 * flare)
            base += particles(t) * (0.3 + 0.7 * seg(t, 0.2, 1.2))
            spun_logo(base, theta, sc, op, seg(tt, 1.6, 2.3), 0.15 + 0.5 * flare)
            acc += base
        img = acc / subs
        wordmark(img, t, 1.5)
    img *= VIGN
    g = cv2.resize(GRAIN[int(t * FPS) % 6], (W, H), interpolation=cv2.INTER_LINEAR)
    img += g[..., None] * 0.012
    return np.clip(img, 0, 1)

os.makedirs(OUT, exist_ok=True)
silent = os.path.join(OUT, f'_silent_{MODE}.mp4')
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', silent], stdin=subprocess.PIPE)
only = os.environ.get('ONLY')
for i in range(N):
    t = i / FPS
    if only and i not in [int(x) for x in only.split(',')]: continue
    f = frame(t)
    b = (f * 255 + 0.5).astype(np.uint8)
    if only: cv2.imwrite(os.path.join(OUT, f'f{MODE}_{i:03d}.png'), b[..., ::-1])
    ff.stdin.write(b.tobytes())
ff.stdin.close(); ff.wait()
print('done', silent)
