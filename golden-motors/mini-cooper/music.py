"""Royalty-free chill deep house bed, 118 BPM. python3 music.py out.wav seconds"""
import sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000; BPM = 120; BEAT = 60 / BPM
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 26
N = int(SR * DUR); rng = np.random.default_rng(7)

def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)
def note(m): return 440 * 2 ** ((m - 69) / 12)
def env(n, a, d):
    t = np.arange(n) / SR; e = np.exp(-t / d)
    na = max(1, int(a * SR)); e[:na] *= np.linspace(0, 1, na); return e

L = np.zeros(N); R = np.zeros(N)
def add(buf, x, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(x))
    if i < N: buf[i:j] += x[:j - i] * g
def addst(x, t, g=1.0, pan=0.0):
    add(L, x, t, g * (1 - max(pan, 0))); add(R, x, t, g * (1 + min(pan, 0)))

beats = int(DUR / BEAT) + 1
# ---- kick
kn = int(0.42 * SR); kt = np.arange(kn) / SR
kf = 45 + 85 * np.exp(-kt / 0.035)
kick = np.sin(2 * np.pi * np.cumsum(kf) / SR) * np.exp(-kt / 0.16)
kick += lp(rng.normal(0, 1, kn), 3000) * np.exp(-kt / 0.004) * 0.25
kick = np.tanh(kick * 1.4)
# sidechain envelope
sc = np.ones(N)
for b in range(beats):
    t = b * BEAT; i = int(t * SR); n = int(BEAT * SR)
    seg = 1 - 0.65 * np.exp(-np.arange(n) / SR / 0.11)
    j = min(N, i + n)
    if i < N: sc[i:j] = np.minimum(sc[i:j], seg[:j - i])
for b in range(beats): addst(kick, b * BEAT, 0.9)
# ---- hats
hn = int(0.14 * SR); hat = hp(rng.normal(0, 1, hn), 7000, 4) * env(hn, 0.001, 0.045)
sn = int(0.06 * SR)
for b in range(beats):
    addst(hat, b * BEAT + BEAT / 2, 0.22, 0.15)
    for k in range(4):
        sh = bp(rng.normal(0, 1, sn), 5000, 11000) * env(sn, 0.004, 0.018)
        addst(sh, b * BEAT + k * BEAT / 4, 0.06 if k % 2 else 0.035, -0.3)
# ---- clap on 2 & 4 (from bar 2)
cn = int(0.3 * SR); clap = bp(rng.normal(0, 1, cn), 900, 3500) * env(cn, 0.002, 0.07)
for b in range(4, beats):
    if b % 4 in (1, 3): addst(clap, b * BEAT, 0.28)
# ---- harmony: Am9 - Fmaj9 - Cmaj9 - G6 (2 beats... 1 bar each)
prog = [(50, [57, 60, 64, 65]), (58, [57, 62, 65, 69]), (53, [57, 60, 64, 67]), (48, [55, 60, 62, 64])]
def saw(f, n, det=(0, 0.11, -0.12)):
    t = np.arange(n) / SR; o = 0
    for d in det:
        ff = f * 2 ** (d / 12 / 4); o = o + 2 * ((t * ff + rng.random()) % 1) - 1
    return o / len(det)
bar = 4 * BEAT
stabL = np.zeros(N); stabR = np.zeros(N); bass = np.zeros(N); pad = np.zeros(N)
for bi in range(int(DUR / bar) + 1):
    root, ch = prog[bi % 4]; t0 = bi * bar
    # stabs on the offbeats: 1&, 2&, 3, 4& (classic deep house push)
    for off in (0.5, 1.5, 2.75, 3.5):
        n = int(0.32 * SR)
        s = sum(saw(note(m), n) for m in ch) / len(ch)
        e = env(n, 0.003, 0.11)
        cut = lp(s, 1400) * e
        add(stabL, cut, t0 + off * BEAT, 0.5); add(stabR, cut, t0 + off * BEAT + 0.012, 0.5)
    # pad
    n = int(bar * SR)
    p = sum(np.sin(2 * np.pi * note(m + 12) * np.arange(n) / SR + rng.random() * 6) for m in ch) / len(ch)
    pe = np.minimum(1, np.arange(n) / SR / 0.4) * np.minimum(1, (n - np.arange(n)) / SR / 0.3)
    add(pad, p * pe, t0, 0.12)
    # bass: root on the off-8ths + octave pick-up
    for off, oct_ in ((0.5, 0), (1.5, 0), (2.5, 0), (3.25, 12), (3.5, 0)):
        n = int(0.24 * SR); tt = np.arange(n) / SR; f = note(root - 24 + oct_)
        x = np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt)
        add(bass, np.tanh(x * 1.5) * env(n, 0.005, 0.12), t0 + off * BEAT, 0.55)
# reverb
irn = int(1.6 * SR); ir = rng.normal(0, 1, irn) * np.exp(-np.arange(irn) / SR / 0.45); ir = lp(ir, 6000); ir /= np.abs(ir).sum() ** 0.5 * 6
wetL = fftconvolve(stabL + pad, ir)[:N]; wetR = fftconvolve(stabR + pad, ir[::-1].copy())[:N]
L += (stabL + pad + wetL * 0.5) * sc; R += (stabR + pad + wetR * 0.5) * sc
bassf = lp(bass, 400) * (0.35 + 0.65 * sc); L += bassf; R += bassf
cl = fftconvolve(L * 0, ir)[:N]
mix = np.stack([L, R], 1)
mix = hp(mix.T, 30).T
# fade in 0.3 s, fade out last 2 s
fi = np.minimum(1, np.arange(N) / SR / 0.3); fo = np.minimum(1, (N - np.arange(N)) / SR / 2.0)
mix *= (fi * fo)[:, None]
mix = np.tanh(mix / np.abs(mix).max() * 1.3) * 0.85
sf.write(sys.argv[1], mix.astype(np.float32), SR)
print('ok', DUR)
