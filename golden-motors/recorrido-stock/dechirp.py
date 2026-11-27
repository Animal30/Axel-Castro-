"""Remove the chair squeak (harmonic whine ~683 Hz) in take A, 37.85-38.68 s, with narrow notches only there."""
import soundfile as sf, numpy as np
from scipy.signal import iirnotch, filtfilt
x, sr = sf.read('aud/origa.wav')
T0, T1, XF = 37.86, 38.56, 0.05
F = [682, 1354, 2055, 2747, 3423, 4059, 4733, 5445, 6189, 6905, 7600]
i0, i1 = int((T0 - 0.2) * sr), int((T1 + 0.2) * sr)
seg = x[i0:i1].copy()
for f in F:
    b, a = iirnotch(f, f / 70, sr)
    for _ in range(2): seg = filtfilt(b, a, seg, axis=0)
from scipy.signal import butter, sosfiltfilt
hi = sosfiltfilt(butter(4, 4000, 'high', fs=sr, output='sos'), seg, axis=0)
seg = seg - hi * (1 - 10 ** (-12 / 20))   # squeak's noisy top end: -12 dB above 4 kHz, only in this window
w = np.zeros(i1 - i0); t = (np.arange(i1 - i0) / sr) + (T0 - 0.2)
w = np.clip(np.minimum((t - T0) / XF + 1, (T1 - t) / XF + 1), 0, 1)
x[i0:i1] = x[i0:i1] * (1 - w[:, None]) + seg * w[:, None]
sf.write('aud/origa_fix.wav', x, sr, subtype='PCM_24')
