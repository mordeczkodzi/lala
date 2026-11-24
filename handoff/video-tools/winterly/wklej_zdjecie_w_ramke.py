# Wkleja zdjęcie przed/po (np. z grafiki AI z błędnymi napisami) w ramkę zwycięskiej grafiki Black Week.
# Użycie: python3 wklej_zdjecie_w_ramke.py ZRODLO.jpg WYNIK.jpg [przesuniecie_plakietki_x] ["x0,y0,x1,y1" strzałki] [split_x_dol] [y_startu_kadru_prawego]
# Współrzędne kadrów w źródle są ustawione pod grafikę 1280x1589 (lewe zdjęcie x 47-636, prawe x 642-1234).
import sys, math
from PIL import Image, ImageDraw, ImageFilter
TPL='/home/user/lala/handoff/grafiki_black_week/winterly_black_week_balkon_4x5.png'
SRC=sys.argv[1]; OUT=sys.argv[2]
tpl=Image.open(TPL).convert('RGB'); src=Image.open(SRC).convert('RGB')
X0,Y0,X1,Y1=18,276,1104,878; W,H=X1-X0,Y1-Y0; R=15
TTOP,TBOT=(int(sys.argv[5])+84,int(sys.argv[5])) if len(sys.argv)>5 else (554,470)      # split line x at top / bottom (template coords)
SS=4
# --- photo panels
from PIL import ImageEnhance
lw=TTOP-X0; lsh=589*H/lw
left=src.crop((47,345,636,int(345+lsh))).resize((lw,H),Image.LANCZOS)
left=ImageEnhance.Color(ImageEnhance.Brightness(left).enhance(0.8)).enhance(0.85)
rsc=(X1-TBOT)/592.0; rh=H/rsc; ry0=int(sys.argv[6]) if len(sys.argv)>6 else 430
right=src.crop((642,ry0,1234,int(ry0+rh))).resize((X1-TBOT,H),Image.LANCZOS)
photo=Image.new('RGB',(W,H)); photo.paste(left,(0,0))
m=Image.new('L',(W*SS,H*SS),0); ImageDraw.Draw(m).polygon([((TTOP-X0)*SS,0),(W*SS,0),(W*SS,H*SS),((TBOT-X0)*SS,H*SS)],fill=255)
m=m.resize((W,H),Image.LANCZOS)
rp=Image.new('RGB',(W,H)); rp.paste(right,(TBOT-X0,0)); photo.paste(rp,(0,0),m)
# white split line
lm=Image.new('L',(W*SS,H*SS),0); ImageDraw.Draw(lm).line([((TTOP-X0)*SS,-10),((TBOT-X0)*SS,H*SS+10)],fill=255,width=8*SS)
lm=lm.resize((W,H),Image.LANCZOS); photo.paste((250,246,238),(0,0),lm)
# paste into template with rounded corners
rm=Image.new('L',(W*SS,H*SS),0); ImageDraw.Draw(rm).rounded_rectangle([0,0,W*SS-1,H*SS-1],radius=R*SS,fill=255)
rm=rm.resize((W,H),Image.LANCZOS)
out=tpl.copy(); out.paste(photo,(X0,Y0),rm)
# --- copy label pills from template (capsule masks)
def capsule(box,inset=1):
    x0,y0,x1,y1=box; w,h=x1-x0,y1-y0
    mm=Image.new('L',(w*SS,h*SS),0); ImageDraw.Draw(mm).rounded_rectangle([inset*SS,inset*SS,(w-inset)*SS-1,(h-inset)*SS-1],radius=(h/2-inset)*SS,fill=255)
    return mm.resize((w,h),Image.LANCZOS)
def shadow(img,box,dx,dy):
    x0,y0,x1,y1=box; w,h=x1-x0,y1-y0
    sh=Image.new('L',img.size,0); ImageDraw.Draw(sh).rounded_rectangle([x0+dx,y0+dy+4,x1+dx,y1+dy+4],radius=h/2,fill=110)
    sh=sh.filter(ImageFilter.GaussianBlur(6)); img.paste((0,0,0),(0,0),sh)
LB=(38,800,293,851); RB=(432,794,1007,863)
RDX=int(sys.argv[3]) if len(sys.argv)>3 else 70
for box,dx in [(LB,0),(RB,RDX)]:
    shadow(out,box,dx,0)
    patch=tpl.crop(box); out.paste(patch,(box[0]+dx,box[1]),capsule(box))
# --- arrow (dark green with gold outline), drawn supersampled
AX=[int(v) for v in sys.argv[4].split(',')] if len(sys.argv)>4 else [430,560,600,470]
def arrow_layer(x0,y0,x1,y1):
    S=SS; L=Image.new('RGBA',(out.width*S,out.height*S),(0,0,0,0)); d=ImageDraw.Draw(L)
    cx,cy=x0+(x1-x0)*0.25,y1-10
    pts=[]
    for i in range(41):
        t=i/40; bx=(1-t)**2*x0+2*(1-t)*t*cx+t*t*x1; by=(1-t)**2*y0+2*(1-t)*t*cy+t*t*y1; pts.append((bx,by,t))
    def shape(grow):
        poly_l=[];poly_r=[]
        for i,(bx,by,t) in enumerate(pts[:-6]):
            nx,ny=pts[i+1][0]-bx,pts[i+1][1]-by; n=math.hypot(nx,ny); nx,ny=nx/n,ny/n
            th=(4+15*t)+grow
            poly_l.append(((bx-ny*th)*S,(by+nx*th)*S)); poly_r.append(((bx+ny*th)*S,(by-nx*th)*S))
        bx,by,_=pts[-7]; ex,ey,_=pts[-1]; dx,dy=ex-bx,ey-by; n=math.hypot(dx,dy); dx,dy=dx/n,dy/n
        hw=34+grow; tip=(ex+dx*(10+grow*1.4),ey+dy*(10+grow*1.4))
        head=[((bx-dy*hw)*S,(by+dx*hw)*S),(tip[0]*S,tip[1]*S),((bx+dy*hw)*S,(by-dx*hw)*S)]
        return poly_l+poly_r[::-1], head
    for grow,col in [(9,(0,0,0,70)),(4,(222,190,120,255)),(0,(18,72,48,255))]:
        body,head=shape(grow); d.polygon(body,fill=col); d.polygon(head,fill=col)
    L=L.resize(out.size,Image.LANCZOS)
    return L
al=arrow_layer(*AX)
# soften the shadow layer: blur alpha of first pass approximated by slight blur of whole layer bottom
out=Image.alpha_composite(out.convert('RGBA'),al).convert('RGB')
out.save(OUT,quality=94)
print('OK',OUT,out.size)
