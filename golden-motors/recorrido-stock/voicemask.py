"""Isolate Alejandro's voice on the ORIGINAL audio: the ElevenLabs stem is used only as a guide to build a
time-frequency mask, so the voice keeps the original recording's clarity (no mp3 artifacts, no EQ/compression)."""
import sys, numpy as np, soundfile as sf
from scipy.signal import stft, istft, fftconvolve
from scipy.ndimage import uniform_filter
FLOOR_DB = -24
def run(orig, iso, out):
    x, sr = sf.read(orig, always_2d=True); g, _ = sf.read(iso, always_2d=True); g = g.mean(1)
    a = x.mean(1)[int(2 * sr):int(8 * sr)]; b = g[int(2 * sr):int(8 * sr)]
    lag = np.argmax(fftconvolve(b, a[::-1], 'full')) - (len(a) - 1)          # align the stem to the original
    g = np.roll(g, -lag)[:len(x)] if lag else g[:len(x)]
    if len(g) < len(x): g = np.pad(g, (0, len(x) - len(g)))
    n = 2048
    _, _, G = stft(g, sr, nperseg=n, noverlap=n * 3 // 4)
    _, _, M = stft(x.mean(1), sr, nperseg=n, noverlap=n * 3 // 4)
    V = np.abs(G) ** 2; N = np.maximum(np.abs(M) ** 2 - V, 0)
    V = uniform_filter(V, (3, 3)); N = uniform_filter(N, (3, 5))
    mask = V / (V + N + 1e-12)
    mask = np.maximum(mask, 10 ** (FLOOR_DB / 20))
    y = np.zeros_like(x)
    for c in range(x.shape[1]):
        _, _, X = stft(x[:, c], sr, nperseg=n, noverlap=n * 3 // 4)
        _, yc = istft(X * mask, sr, nperseg=n, noverlap=n * 3 // 4); y[:, c] = yc[:len(x)]
    sf.write(out, y, sr, subtype='PCM_24'); print(out, 'lag', lag)
run('aud/origa_fix.wav', 'aud/isoa.wav', 'aud/vma.wav')
run('aud/origb.wav', 'aud/isob.wav', 'aud/vmb.wav')
