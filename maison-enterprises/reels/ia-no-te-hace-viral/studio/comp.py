import sys, subprocess, numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter, shift
fg_path, bg_path, grad_path, out, t0, n = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]), int(sys.argv[6])
W, H = 1080, 1920
bg = np.asarray(Image.open(bg_path).convert('RGB'), np.float32) / 255
gr = np.asarray(Image.open(grad_path).convert('RGB'), np.float32) / 255
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(t0), "-c:v", "libvpx-vp9", "-i", fg_path, "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE)
enc_args = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "24000/1001", "-i", "-"]
enc_args += (["-frames:v", "1", out] if out.endswith(".png") else ["-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out])
enc = subprocess.Popen(enc_args, stdin=subprocess.PIPE)
k = 0
while True:
    buf = dec.stdout.read(W * H * 4)
    if len(buf) < W * H * 4: break
    f = np.frombuffer(buf, np.uint8).reshape(H, W, 4).astype(np.float32) / 255
    rgb, a = f[..., :3], f[..., 3]
    a = np.clip((gaussian_filter(a, 0.8) - 0.12) / 0.88, 0, 1)          # choke the matte slightly so no wall shows at the edge
    rgb = rgb.copy(); rgb[..., 1] = np.minimum(rgb[..., 1], np.maximum(rgb[..., 0], rgb[..., 2]) * 1.02)   # green-wall spill off                                   # soften the matte edge a touch
    # relight: warm key from the upper left, falloff to the right; slight contrast
    # the yellow gaming-chair panels become dark charcoal leather (studio chair)
    mx = rgb.max(-1); mn = rgb.min(-1); sat = (mx - mn) / (mx + 1e-4)
    hue = np.zeros_like(mx); d = mx - mn + 1e-6; r_, g_, b_ = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    hue = np.where(mx == r_, ((g_ - b_) / d) % 6, np.where(mx == g_, (b_ - r_) / d + 2, (r_ - g_) / d + 4)) * 60
    ym = np.clip((sat - 0.22) / 0.15, 0, 1) * np.clip(1 - np.abs(hue - 52) / 22, 0, 1) * (gaussian_filter(np.clip((sat - 0.4) / 0.2, 0, 1) * (np.abs(hue - 52) < 18), 12) > 0.08)
    ym = gaussian_filter(ym, 1.5)[..., None]
    rgb = rgb * (1 - ym) + (rgb.mean(-1, keepdims=True) * 0.22) * ym
    a = a * (1 - np.clip(ym[..., 0] * 1.6, 0, 1))      # and drop out of the matte entirely
    # edge decontamination: in the soft edge, take the colour from the solid interior next to it (no light fringe from the old wall)
    inner = (a > 0.96).astype(np.float32); small = slice(None, None, 2)
    num = gaussian_filter(rgb[small, small] * inner[small, small, None], (3, 3, 0)); den = gaussian_filter(inner[small, small], 3)[..., None]
    col = np.repeat(np.repeat(num / np.maximum(den, 1e-3), 2, 0), 2, 1)[:H, :W]
    band = np.clip((0.96 - a) / 0.3, 0, 1)[..., None] * (np.repeat(np.repeat(den, 2, 0), 2, 1)[:H, :W] > 0.02)
    rgb = rgb * (1 - band) + col * band
    lit = np.clip(rgb * gr, 0, 1); lit = np.clip((lit - 0.5) * 1.06 + 0.5 - 0.01, 0, 1)
    # contact shadow on the wall, down and to the right of the subject
    sh = gaussian_filter(a[::4, ::4], (6, 10)); sh = np.kron(sh, np.ones((4, 4), np.float32))[:H, :W]
    sh = shift(sh, (22, 40), order=0, mode='constant') * 0.5
    base = bg * (1 - sh[..., None])
    # light wrap: a little of the background's colour bleeds onto the edge
    edge = np.clip(a - gaussian_filter(a, 6), 0, 1)[..., None] * 0.0
    out_rgb = base * (1 - a[..., None]) + lit * a[..., None]
    enc.stdin.write((np.clip(out_rgb, 0, 1) * 255).astype(np.uint8).tobytes()); k += 1
enc.stdin.close(); enc.wait(); print(k, "frames")
