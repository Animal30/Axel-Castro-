import numpy as np, soundfile as sf, subprocess, sys
sys.argv=['x']; import importlib.util
spec=importlib.util.spec_from_file_location('v1','v1.py'); v1=importlib.util.module_from_spec(spec); spec.loader.exec_module(v1)
SR=48000; COVER=0.5
cuts=[]; t=0
for u in v1.UNITS:
    for p in u['vid']:
        cuts.append(t); t+=p[2]
cuts=[c+COVER for c in cuts[1:]]
cards=[5.28,10.44,17.01,24.77,32.7,44.77]
cards=[c+COVER for c in cards]
total=t+COVER
print('cuts',[round(c,2) for c in cuts]); 
rng=np.random.default_rng(7)
def bp(x,lo,hi):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X[(f<lo)|(f>hi)]=0; return np.fft.irfft(X,len(x))
def whoosh(d=0.38):
    n=int(d*SR); x=rng.standard_normal(n); tt=np.linspace(0,1,n)
    # sweep: crossfade filtered bands low->high
    lo=bp(x,200,900); hi=bp(x,1500,6000)
    y=lo*(1-tt)+hi*tt
    env=np.sin(np.pi*tt)**2
    y=y*env; y/=np.abs(y).max()+1e-9
    return y*0.5
def pop(d=0.5):
    n=int(d*SR); tt=np.arange(n)/SR
    thump=np.sin(2*np.pi*(110-60*tt/d)*tt)*np.exp(-tt*14)
    tick=np.sin(2*np.pi*1800*tt)*np.exp(-tt*60)*0.35
    sh=bp(rng.standard_normal(n),3000,9000)*np.exp(-tt*10)*0.25
    y=thump*0.8+tick+sh; return y/np.abs(y).max()*0.6
out=np.zeros(int((total+1)*SR))
def put(w,at,gain_db):
    i=int(at*SR); g=10**(gain_db/20); out[i:i+len(w)]+=w[:len(out)-i]*g
last=-9
for c in cuts:
    if c-last<0.7: continue
    put(whoosh(),max(c-0.16,0),-17); last=c
for c in cards: put(pop(),c,-14)
stereo=np.stack([out,out],1)
sf.write('sfx_track.wav',stereo,SR,subtype='PCM_24')
print('total',total)
