"""CarMax: opciones de logo final (1080x1920). python3 opciones.py outdir"""
import sys, os, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
H=os.path.dirname(os.path.abspath(__file__)); OUT=sys.argv[1]; os.makedirs(OUT,exist_ok=True)
OR=(238,120,14); WH=(245,245,245); GR=(150,150,150)
W,Hh=1080,1920
CAR=lambda s:ImageFont.truetype(f'{H}/baloo-2-latin-800-normal.ttf',s)
SUB=lambda s:ImageFont.truetype(f'{H}/orbitron-latin-700-normal.ttf',s)
THIN=lambda s:ImageFont.truetype(f'{H}/michroma-latin-400-normal.ttf',s)

def bg():
    y,x=np.mgrid[0:Hh,0:W].astype(np.float32)
    r=np.sqrt(((x-W/2)/W)**2+((y-880)/W)**2)
    base=np.full((Hh,W,3),9,np.float32)
    base+=np.exp(-(r/0.45)**2)[...,None]*np.array([34,16,3],np.float32)
    return Image.fromarray(np.clip(base,0,255).astype(np.uint8))

def spaced(d,text,font,y,fill,track,cx=W/2,width=None):
    ws=[d.textlength(c,font=font) for c in text]
    if width: track=(width-sum(ws))/(len(text)-1)
    tot=sum(ws)+track*(len(text)-1)
    x=cx-tot/2
    for c,w in zip(text,ws): d.text((x,y),c,font=font,fill=fill); x+=w+track
    return tot

def center(d,text,font,y,fill):
    w=d.textlength(text,font=font); d.text((W/2-w/2,y),text,font=font,fill=fill); return w

def glow(im,layer):
    g=layer.filter(ImageFilter.GaussianBlur(28)); a=np.asarray(g).astype(np.float32)
    b=np.asarray(im).astype(np.float32); return Image.fromarray(np.clip(b+a*0.35,0,255).astype(np.uint8))

def make(kind):
    im=bg(); L=Image.new('RGB',(W,Hh)); d=ImageDraw.Draw(L)
    if kind=='A':
        center(d,'CarMax',CAR(250),700,OR)
    elif kind=='B':
        wc=center(d,'CarMax',CAR(230),660,OR)
        spaced(d,'AUTOMOTORES',SUB(52),960,WH,14,width=wc-16)
    elif kind=='C':
        wc=center(d,'CarMax',CAR(230),680,OR)
        d.rectangle((W/2-150,975,W/2+150,979),fill=OR)
        spaced(d,'CÓRDOBA',THIN(44),1015,WH,22)
    elif kind=='D':
        wc=center(d,'CarMax',CAR(220),600,OR)
        spaced(d,'AUTOMOTORES',SUB(50),888,WH,13,width=wc-16)
        d.rectangle((W/2-60,1010,W/2+60,1013),fill=OR)
        spaced(d,'CÓRDOBA',THIN(30),1050,GR,14)
    im=glow(im,L)
    m=np.asarray(L).sum(2)>30; out=np.asarray(im).copy(); out[m]=np.asarray(L)[m]
    return Image.fromarray(out)

names={'A':'Solo CarMax','B':'CarMax Automotores','C':'CarMax Córdoba','D':'Automotores + Córdoba'}
frames=[]
for k in 'ABCD':
    f=make(k); f.save(f'{OUT}/opcion-{k}.png'); frames.append(f)
# comparison sheet
s=0.36; tw,th=int(W*s),int(Hh*s); pad=30
sheet=Image.new('RGB',(4*tw+5*pad,th+150),(30,30,30)); d=ImageDraw.Draw(sheet)
for i,(k,f) in enumerate(zip('ABCD',frames)):
    x=pad+i*(tw+pad); sheet.paste(f.resize((tw,th),Image.LANCZOS),(x,90))
    t=f'{k}  {names[k]}'; LF=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf',28); w=d.textlength(t,font=LF); d.text((x+tw/2-w/2,35),t,font=LF,fill=WH)
sheet.save(f'{OUT}/comparacion.png')
