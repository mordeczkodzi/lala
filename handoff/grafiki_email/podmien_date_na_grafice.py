import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
F='/tmp/claude-0/-home-user-lala/9af5c72f-959d-5981-b926-47b34d7272d6/scratchpad/fonts/'
img=Image.open('hero_orig.jpg').convert('RGB'); A=np.array(img).astype(np.float32)
def render(txt,font,track,col,W,H,x,y):  # zwraca maskę i obraz tekstu z odstępem między literami
    L=Image.new('L',(W,H),0); d=ImageDraw.Draw(L); cx=x
    for ch in txt: d.text((cx,y),ch,font=font,fill=255); cx+=font.getlength(ch)+track
    return np.array(L).astype(np.float32)/255.0
def fit_and_replace(box,old,new,fontnames,thr,bg_fill=None):
    x0,y0,x1,y1=box; pad=6
    reg=A[y0-pad:y1+pad,x0-pad:x1+pad]; lum=reg.sum(2)
    mask=(lum>thr).astype(np.float32)
    bgl=np.percentile(lum,30); fgl=np.percentile(lum[lum>thr],90); soft=np.clip((lum-bgl)/(fgl-bgl),0,1)
    ys,xs=np.where(mask>0); tx0,ty0=xs.min(),ys.min()
    col=reg[mask>0].reshape(-1,3); col=col[col.sum(1)>np.percentile(col.sum(1),70)].mean(0)
    best=None
    for fontname in fontnames:
     for size in np.arange(18,34,0.5):
        f=ImageFont.truetype(F+fontname+'.ttf',int(round(size*4)))
        for track in np.arange(-1,6.5,0.5):
            m=render(old,f,track*4,None,reg.shape[1]*4,reg.shape[0]*4,0,0)
            m=cv2.resize(m,(reg.shape[1],reg.shape[0]),interpolation=cv2.INTER_AREA)
            yy,xx=np.where(m>0.4)
            if len(xx)==0: continue
            sh=np.zeros_like(m); dx=tx0-xx.min(); dy=ty0-yy.min()
            M=np.float32([[1,0,dx],[0,1,dy]]); m2=cv2.warpAffine(m,M,(m.shape[1],m.shape[0]))
            err=-((m2-soft)**2).mean()
            if best is None or err>best[0]: best=(err,size,track,dx,dy,fontname)
    iou,size,track,dx,dy,fontname=best; print(old,'->',new,'err',round(-iou,4),'size',size,'track',track,fontname)
    # wyczyść stary tekst
    clear=cv2.dilate((mask>0).astype(np.uint8),np.ones((5,5),np.uint8))
    full=np.zeros(A.shape[:2],np.uint8); full[y0-pad:y1+pad,x0-pad:x1+pad]=clear
    out=np.array(img).copy()
    if bg_fill is not None: out[full>0]=bg_fill
    else: out=cv2.inpaint(out,full,5,cv2.INPAINT_TELEA)
    # nowy tekst, wyśrodkowany w miejscu starego, ta sama linia bazowa
    f=ImageFont.truetype(F+fontname+'.ttf',int(round(size*4)))
    def width(t): return sum(f.getlength(c)+track*4 for c in t)-track*4
    S=4; Wb,Hb=(x1-x0+80)*S,(y1-y0+2*pad)*S
    mo=render(old,f,track*S,None,Wb,Hb,0,0); yy,xx=np.where(mo>0.4)
    mn=render(new,f,track*S,None,Wb,Hb,0,0); yn,xn=np.where(mn>0.4)
    oc=(xx.min()+xx.max())/2/S; nc=(xn.min()+xn.max())/2/S
    m=cv2.resize(mn,(Wb//S,Hb//S),interpolation=cv2.INTER_AREA)
    ox=x0-pad+tx0-xx.min()/S + (oc-nc); oy=y0-pad+ty0-yy.min()/S
    M=np.float32([[1,0,ox],[0,1,oy]]); big=cv2.warpAffine(m,M,(A.shape[1],A.shape[0]))[...,None]
    out=(out.astype(np.float32)*(1-big)+col*big).clip(0,255).astype(np.uint8)
    return Image.fromarray(out)
img=fit_and_replace((293,21,350,43),'15.11','25.11',['Poppins-Medium','Poppins-SemiBold','Poppins-Bold'],500,bg_fill=(123,31,44)); A=np.array(img).astype(np.float32)
img=fit_and_replace((581,978,633,1008),'15.11,','25.11,',['Poppins-Regular','Poppins-Medium'],560)
img.save('winterly-dzis11-hero-25-11.jpg',quality=95)
img.crop((0,0,1200,90)).save('_top_new.png'); img.crop((300,940,900,1020)).resize((1200,160)).save('_kod_new.png')
