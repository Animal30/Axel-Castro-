"""Swap the engine sound after ignition (15.33-20.70 s of v1_nomusic.mp4) with revs from a reference reel (ig/reel.mp4, 0-5.4 s)."""
import numpy as np, soundfile as sf, subprocess
from scipy.signal import butter, sosfilt
SR = 48000; T0, T1 = 15.33, 20.70; D = T1 - T0
o, _ = sf.read('ig/orig.wav')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'ig/reel.mp4', '-t', f'{D + 0.1:.3f}', '-ac', '2', '-ar', str(SR), 'ig/eng_st.wav'], check=True)
e, _ = sf.read('ig/eng_st.wav'); e = e[:int(D * SR)]
# warm bass shelf so it sounds like the V6 in the room, then match the old engine level + 1 dB
low = sosfilt(butter(2, 150, 'low', fs=SR, output='sos'), e, axis=0); e = e + 0.5 * low
seg = o[int(T0 * SR):int(T1 * SR)]
rms = lambda x: np.sqrt(np.mean(x ** 2))
e *= rms(seg) / rms(e) * 10 ** (4 / 20)
e = 0.89 * np.tanh(e / 0.89 * 1.0)  # soft limiter, keeps the rest of the video untouched
print('after lim', round(20*np.log10(rms(e)),1), 'old', round(20*np.log10(rms(seg)),1))
n = len(e); fi = int(0.04 * SR); fo = int(0.15 * SR)
env = np.ones(n); env[:fi] = np.linspace(0, 1, fi); env[-fo:] = np.linspace(1, 0, fo)
out = o.copy(); i0 = int(T0 * SR)
xf = np.ones(n); xf[:fi] = np.linspace(1, 0, fi); xf[fi:] = 0
out[i0:i0 + n] = o[i0:i0 + n] * xf[:, None] + e * env[:, None]
pk = np.abs(out).max(); out = np.clip(out, -0.95, 0.95)
sf.write('ig/new.wav', out.astype(np.float32), SR); print('ok', round(20*np.log10(rms(e)),1), round(pk,2))
