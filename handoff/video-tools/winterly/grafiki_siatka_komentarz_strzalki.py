import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import numpy as np
S='/tmp/claude-0/-home-user-lala/9af5c72f-959d-5981-b926-47b34d7272d6/scratchpad/'
F=S+'fonts/'; LA=S+'la/'
TPL='/home/user/lala/handoff/grafiki_black_week/winterly_black_week_balkon_4x5.png'
DOM='/home/user/lala/handoff/grafiki_black_week/winterly_black_week_dom_4x5.jpg'
def font(n,s): return ImageFont.truetype(F+n+'.ttf',s)
W,H=1080,1350
GOLD=(214,178,108); CREAM=(250,243,228); GREEN=(14,52,38); RED=(196,26,32)
tpl=Image.open(TPL).convert('RGB')
# transparent gold logo keyed from template cream
def logo(height):
    c=tpl.crop((455,8,672,158)); a=np.array(c).astype(float)
    cream=np.array([252,240,226.]); dist=np.clip(((cream-a).sum(2)-45)/160.0,0,1)
    rgba=np.zeros((a.shape[0],a.shape[1],4),np.uint8); rgba[...,:3]=a.astype(np.uint8); rgba[...,3]=(dist*255).astype(np.uint8)
    im=Image.fromarray(rgba,'RGBA'); bb=im.getbbox(); im=im.crop(bb)
    # boost to gold-ish on dark bg
    r,g,b,al=im.split(); im=Image.merge('RGBA',(r.point(lambda v:min(255,int(v*1.15)+20)),g.point(lambda v:min(255,int(v*1.1)+15)),b,al))
    return im.resize((int(im.width*height/im.height),height),Image.LANCZOS)
def ctext(d,y,txt,f,fill,W=W,shadow=None,x0=0):
    w=d.textlength(txt,font=f); x=x0+(W-w)/2
    if shadow: d.text((x+3,y+3),txt,font=f,fill=shadow)
    d.text((x,y),txt,font=f,fill=fill); return w
def cover(im,w,h,cx=0.5,cy=0.5):
    r=max(w/im.width,h/im.height); im=im.resize((int(im.width*r+0.5),int(im.height*r+0.5)),Image.LANCZOS)
    x=int((im.width-w)*cx); y=int((im.height-h)*cy); return im.crop((x,y,x+w,y+h))
def sharpen(im): return im.filter(ImageFilter.UnsharpMask(radius=1.6,percent=70,threshold=2))
def pill_text(d,xy,txt,f,bg,fg,padx=22,pady=10,r=None):
    x,y=xy; w=d.textlength(txt,font=f); bb=f.getbbox(txt); h=bb[3]-bb[1]
    r=r if r is not None else (h+2*pady)//2
    d.rounded_rectangle([x,y,x+w+2*padx,y+h+2*pady],radius=r,fill=bg)
    d.text((x+padx,y+pady-bb[1]),txt,font=f,fill=fg); return w+2*padx,h+2*pady
def save(im,name): im.convert('RGB').save(LA+name,quality=94); print('OK',name)

# ---------- 1) GRID: Jedna kurtyna. Co wieczór inny wzór.
dom=Image.open(DOM).convert('RGB')
tiles=[(Image.open(LA+'p_balwan_6.0.png'),(0,640,1080,1330),'Bałwanek'),
       (Image.open(LA+'p_choinka_0.4.png'),(0,560,1080,1250),'Choinka'),
       (Image.open(LA+'p_sanie_2.5.png'),(0,880,1080,1570),'Sanie Mikołaja'),
       (Image.open(LA+'p_snieg_8.0.png'),(0,620,1080,1310),'Śnieżynki'),
       (Image.open(LA+'snow_0.5.png'),(250,620,930,1055),'Mikołaj'),
       (dom,(860,790,1560,1235),'Zimowa wioska')]
g=Image.new('RGB',(W,H),GREEN)
# subtle radial vignette
yy,xx=np.mgrid[0:H,0:W]; v=1-0.35*np.clip(np.hypot((xx-W/2)/W,(yy-H/2)/H)*1.6,0,1)
g=Image.fromarray((np.array(g)*v[...,None]).astype(np.uint8))
d=ImageDraw.Draw(g)
ctext(d,36,'Jedna kurtyna.',font('PlayfairDisplay-Bold',84),CREAM)
ctext(d,130,'Co wieczór inny wzór.',font('PlayfairDisplay-Bold',84),GOLD)
M,G,TW=48,24,0; TW=(W-2*M-G)//2; TH=int(TW*0.58); Y0=252
fc=font('Montserrat-Bold',24)
for i,(im,box,cap) in enumerate(tiles):
    c=sharpen(cover(im.crop(box),TW,TH)); x=M+(i%2)*(TW+G); y=Y0+(i//2)*(TH+G)
    g.paste(c,(x,y)); d.rectangle([x-3,y-3,x+TW+2,y+TH+2],outline=GOLD,width=3)
    pill_text(d,(x+14,y+TH-56),cap,fc,(250,243,228),(20,40,30),padx=16,pady=9)
yb=Y0+3*TH+2*G+24
fp=font('Montserrat-ExtraBold',30)
txt='BLACK WEEK  •  DRUGA KURTYNA −40%'
tw=d.textlength(txt,font=fp); px=(W-tw-60)//2
pill_text(d,(px,yb),txt,fp,RED,(255,255,255),padx=30,pady=14)
lg=logo(60); ly=yb+76
d.line([(W/2-300,ly+40),(W/2-lg.width/2-24,ly+40)],fill=GOLD,width=2); d.line([(W/2+lg.width/2+24,ly+40),(W/2+300,ly+40)],fill=GOLD,width=2)
g.paste(lg,(int(W/2-lg.width/2),ly),lg)
save(g,'winterly_bw_siatka_wzorow_4x5.jpg')

# ---------- 2) KOMENTARZ + TAŚMA (kurtyna odsłonięta)
k=Image.new('RGB',(W,H),(10,10,12)); d=ImageDraw.Draw(k)
ctext(d,58,'„Chcę!”',font('Montserrat-ExtraBold',116),(255,255,255))
ctext(d,212,'Komentarz pod naszą reklamą',font('Montserrat-SemiBold',30),GOLD)
PH=690; py=318
photo=sharpen(cover(tpl.crop((418,282,1100,872)),W,PH,cy=0.2)); k.paste(photo,(0,py))
fade=Image.new('L',(W,PH),255); fd=ImageDraw.Draw(fade)
for i in range(50): fd.line([(0,i),(W,i)],fill=int(255*i/50)); fd.line([(0,PH-1-i),(W,PH-1-i)],fill=int(255*i/50))
k.paste(Image.new('RGB',(W,PH),(10,10,12)),(0,py),ImageOps.invert(fade))
def tape(img,y,ang,txt='BLACK WEEK  •  ',hgt=76,fs=38):
    f=font('Montserrat-ExtraBold',fs); L=2200; T=Image.new('RGBA',(L,hgt),(242,194,48,255)); td=ImageDraw.Draw(T)
    x=-40
    while x<L: td.text((x,(hgt-fs)//2-4),txt,font=f,fill=(15,15,15)); x+=td.textlength(txt,font=f)
    T=T.rotate(ang,expand=True,resample=Image.BICUBIC)
    sh=Image.new('RGBA',T.size,(0,0,0,0)); sh.putalpha(T.split()[3].point(lambda a:int(a*0.5))); sh=sh.filter(ImageFilter.GaussianBlur(8))
    img.paste(sh,((W-T.width)//2+4,y-T.height//2+10),sh); img.paste(T,((W-T.width)//2,y-T.height//2),T)
tape(k,py+8,-3); tape(k,py+PH-6,2.5)
bx,by,R=905,py+PH-118,100
bd=Image.new('RGBA',(2*R+40,2*R+40),(0,0,0,0)); dd=ImageDraw.Draw(bd)
dd.ellipse([20,20,20+2*R,20+2*R],fill=RED); dd.ellipse([29,29,11+2*R,11+2*R],outline=(255,255,255),width=3)
f1=font('Montserrat-ExtraBold',60); f2=font('Montserrat-SemiBold',22)
w=dd.textlength('−40%',font=f1); dd.text((20+R-w/2,20+R-60),'−40%',font=f1,fill='white')
for j,t in enumerate(['na drugą','kurtynę']):
    w=dd.textlength(t,font=f2); dd.text((20+R-w/2,20+R+14+j*25),t,font=f2,fill='white')
bd=bd.rotate(-8,resample=Image.BICUBIC); k.paste(bd,(bx-R-20,by-R-20),bd)
d=ImageDraw.Draw(k)
ctext(d,1072,'Setki animowanych wzorów, sterowanych z telefonu',font('Montserrat-SemiBold',33),(255,255,255))
ctext(d,1122,'Płatność przy odbiorze  •  30 dni na zwrot',font('Montserrat-SemiBold',28),(200,200,200))
lg=logo(80); k.paste(lg,(int(W/2-lg.width/2),1208),lg)
save(k,'winterly_bw_komentarz_chce_4x5.jpg')

# ---------- 3) ZDJĘCIE Z OPISAMI (strzałki)
src=Image.open(LA+'p_sanie_0.4.png').convert('RGB')
a=sharpen(cover(src.crop((0,300,1080,1920)),W,H,cy=0.35)); 
grad=Image.new('L',(1,H)); 
for y in range(H):
    v=0.9*max(0,min(1,(y-H*0.62)/(H*0.3))) if y>H*0.62 else 0.75*max(0,(H*0.2-y)/(H*0.2))
    grad.putpixel((0,y),int(255*v))
grad=grad.resize((W,H)); a.paste(Image.new('RGB',(W,H),(5,8,14)),(0,0),grad)
d=ImageDraw.Draw(a)
ctext(d,58,'Wzór zmieniasz',font('Montserrat-ExtraBold',72),(255,255,255),shadow=(0,0,0))
ctext(d,140,'jednym kliknięciem.',font('Montserrat-ExtraBold',72),(255,255,255),shadow=(0,0,0))


def hand_ellipse(img,cx,cy,rx,ry,rot,col=(255,255,255),w=6):
    SS=3; L=Image.new('RGBA',(img.width*SS,img.height*SS),(0,0,0,0)); dl=ImageDraw.Draw(L)
    for k,(dr,dw,ph) in enumerate([(0,w,0.0),(7,w-2,0.6)]):
        pts=[]
        for i in range(0,374):
            t=math.radians(i)+ph*0.05; r1=rx+dr*math.sin(t*2+ph); r2=ry+dr*math.cos(t*3+ph)
            x=r1*math.cos(t); y=r2*math.sin(t); c,sn=math.cos(math.radians(rot)),math.sin(math.radians(rot))
            pts.append(((cx+x*c-y*sn)*SS,(cy+x*sn+y*c)*SS))
        dl.line(pts,fill=col+(255,),width=dw*SS,joint='curve')
    L=L.resize(img.size,Image.LANCZOS); img.paste(L,(0,0),L)
def hand_arrow(img,p0,p1,bend=0.25,col=(255,255,255),w=5):
    SS=3; L=Image.new('RGBA',(img.width*SS,img.height*SS),(0,0,0,0)); dl=ImageDraw.Draw(L)
    (x0,y0),(x1,y1)=p0,p1; mx,my=(x0+x1)/2,(y0+y1)/2; nx,ny=-(y1-y0),(x1-x0); cx,cy=mx+nx*bend,my+ny*bend
    pts=[(((1-t)**2*x0+2*(1-t)*t*cx+t*t*x1)*SS,((1-t)**2*y0+2*(1-t)*t*cy+t*t*y1)*SS) for t in [i/40 for i in range(41)]]
    dl.line(pts,fill=col+(255,),width=w*SS,joint='curve')
    ex,ey=pts[-1]; bx,by=pts[-5]; ang=math.atan2(ey-by,ex-bx)
    for da in (2.6,-2.6):
        dl.line([(ex,ey),(ex+math.cos(ang+da)*26*SS,ey+math.sin(ang+da)*26*SS)],fill=col+(255,),width=w*SS)
    L=L.resize(img.size,Image.LANCZOS); img.paste(L,(0,0),L)
def shadow_text(img,xy,txt,f,fill=(255,255,255)):
    L=Image.new('RGBA',img.size,(0,0,0,0)); dl=ImageDraw.Draw(L); dl.text((xy[0]+2,xy[1]+3),txt,font=f,fill=(0,0,0,200))
    L=L.filter(ImageFilter.GaussianBlur(3)); img.paste(L,(0,0),L); ImageDraw.Draw(img).text(xy,txt,font=f,fill=fill)
hand_ellipse(a,597,552,405,205,-3)
fh=font('Caveat-Bold',58)
shadow_text(a,(700,250),'Setki wzorów',fh); hand_arrow(a,(790,318),(860,392),bend=-0.25)
shadow_text(a,(36,775),'Pilot w zestawie',fh); hand_arrow(a,(200,772),(292,690),bend=-0.3)
shadow_text(a,(585,780),'Aplikacja iOS i Android',fh); hand_arrow(a,(760,776),(700,712),bend=0.3)
d=ImageDraw.Draw(a)
d.text((60,972),'BLACK WEEK',font=font('Montserrat-ExtraBold',74),fill=(255,255,255))
d.text((62,1068),'Druga kurtyna −40%',font=font('Montserrat-Bold',38),fill=(242,194,48))
d.text((62,1122),'Płatność przy odbiorze  •  30 dni na zwrot',font=font('Montserrat-SemiBold',28),fill=(225,225,225))
R=118; bd=Image.new('RGBA',(2*R+40,2*R+40),(0,0,0,0)); dd=ImageDraw.Draw(bd)
dd.ellipse([20,20,20+2*R,20+2*R],fill=(10,10,12,235)); dd.ellipse([30,30,10+2*R,10+2*R],outline=(255,255,255),width=3)
f1=font('Montserrat-ExtraBold',68); f2=font('Montserrat-SemiBold',24)
w=dd.textlength('−40%',font=f1); dd.text((20+R-w/2,20+R-66),'−40%',font=f1,fill='white')
for j,t in enumerate(['na drugą','kurtynę']):
    w=dd.textlength(t,font=f2); dd.text((20+R-w/2,20+R+18+j*28),t,font=f2,fill='white')
a.paste(bd,(905-R-20,1060-R-20),bd)
lg=logo(70); a.paste(lg,(60,1220),lg)
save(a,'winterly_bw_opisy_strzalki_4x5.jpg')

# ---------- 4) BAŁWAN, KTÓRY NIE TOPNIEJE (nasze ujęcie)
b=Image.open(LA+'balwan_3.0.png').convert('RGB')
b=sharpen(b.crop((0,400,1080,1750)))
grad=Image.new('L',(1,H))
for y in range(H):
    v=0.92*max(0,min(1,(y-H*0.64)/(H*0.26))) if y>H*0.64 else 0.8*max(0,(H*0.24-y)/(H*0.24))
    grad.putpixel((0,y),int(255*v))
b.paste(Image.new('RGB',(W,H),(5,8,14)),(0,0),grad.resize((W,H)))
d=ImageDraw.Draw(b)
ctext(d,44,'Bałwan, który',font('Montserrat-ExtraBold',84),(255,255,255),shadow=(0,0,0))
ctext(d,138,'nie topnieje.',font('Montserrat-ExtraBold',84),(255,255,255),shadow=(0,0,0))
ctext(d,250,'Kurtyna LED Winterly – setki wzorów z telefonu',font('Montserrat-SemiBold',31),(235,235,235),shadow=(0,0,0))
d.text((60,972),'BLACK WEEK',font=font('Montserrat-ExtraBold',74),fill=(255,255,255))
d.text((62,1068),'Druga kurtyna −40%',font=font('Montserrat-Bold',38),fill=(242,194,48))
d.text((62,1122),'Płatność przy odbiorze  •  30 dni na zwrot',font=font('Montserrat-SemiBold',28),fill=(225,225,225))
R=118; bd=Image.new('RGBA',(2*R+40,2*R+40),(0,0,0,0)); dd=ImageDraw.Draw(bd)
dd.ellipse([20,20,20+2*R,20+2*R],fill=RED); dd.ellipse([30,30,10+2*R,10+2*R],outline=(255,255,255),width=3)
f1=font('Montserrat-ExtraBold',68); f2=font('Montserrat-SemiBold',24)
w=dd.textlength('−40%',font=f1); dd.text((20+R-w/2,20+R-66),'−40%',font=f1,fill='white')
for j,t in enumerate(['na drugą','kurtynę']):
    w=dd.textlength(t,font=f2); dd.text((20+R-w/2,20+R+18+j*28),t,font=f2,fill='white')
bd=bd.rotate(-8,resample=Image.BICUBIC); b.paste(bd,(905-R-20,1060-R-20),bd)
lg=logo(70); b.paste(lg,(60,1220),lg)
save(b,'winterly_bw_balwan_4x5.jpg')
