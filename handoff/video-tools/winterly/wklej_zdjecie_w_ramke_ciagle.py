# Wkleja CIĄGŁE zdjęcie przed/po (jeden dom, podział pionowy) w ramkę zwycięzcy Black Week.
import sys, math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
TPL='/home/user/lala/handoff/grafiki_black_week/winterly_black_week_balkon_4x5.png'
SRC,OUT=sys.argv[1],sys.argv[2]
YS=int(sys.argv[3]) if len(sys.argv)>3 else 360          # górna krawędź kadru w źródle
DARK=float(sys.argv[4]) if len(sys.argv)>4 else 0.9      # przyciemnienie lewej połowy ("przed")
tpl=Image.open(TPL).convert('RGB'); src=Image.open(SRC).convert('RGB')
X0,Y0,X1,Y1=18,276,1104,878; W,H=X1-X0,Y1-Y0; R=15; SS=4
SX0,SX1,SEAM=48,1232,639.5
s=W/(SX1-SX0); sh=H/s
photo=src.crop((SX0,YS,SX1,int(round(YS+sh)))).resize((W,H),Image.LANCZOS)
seam=(SEAM-SX0)*s
if DARK<1:
    lp=photo.crop((0,0,int(seam),H)); lp=ImageEnhance.Brightness(lp).enhance(DARK); photo.paste(lp,(0,0))
d=ImageDraw.Draw(photo); d.rectangle([int(seam)-3,0,int(seam)+3,H],fill=(250,246,238))
rm=Image.new('L',(W*SS,H*SS),0); ImageDraw.Draw(rm).rounded_rectangle([0,0,W*SS-1,H*SS-1],radius=R*SS,fill=255)
rm=rm.resize((W,H),Image.LANCZOS)
out=tpl.copy(); out.paste(photo,(X0,Y0),rm)
SEAM_T=X0+seam
def capsule(w,h,inset=1):
    mm=Image.new('L',(w*SS,h*SS),0); ImageDraw.Draw(mm).rounded_rectangle([inset*SS,inset*SS,(w-inset)*SS-1,(h-inset)*SS-1],radius=(h/2-inset)*SS,fill=255)
    return mm.resize((w,h),Image.LANCZOS)
def put_pill(box,dest_xy,scale=1.0):
    x0,y0,x1,y1=box; patch=tpl.crop(box); m=capsule(x1-x0,y1-y0)
    if scale!=1.0:
        nw,nh=int((x1-x0)*scale),int((y1-y0)*scale); patch=patch.resize((nw,nh),Image.LANCZOS); m=m.resize((nw,nh),Image.LANCZOS)
    w,h=patch.size; dx,dy=dest_xy
    shd=Image.new('L',out.size,0); ImageDraw.Draw(shd).rounded_rectangle([dx,dy+4,dx+w,dy+h+4],radius=h/2,fill=110)
    out.paste((0,0,0),(0,0),shd.filter(ImageFilter.GaussianBlur(6))); out.paste(patch,(dx,dy),m)
LB=(38,800,293,851); RB=(432,794,1007,863)
put_pill(LB,(38,811))
rs=0.88; rw=int((RB[2]-RB[0])*rs); rh=int((RB[3]-RB[1])*rs)
put_pill(RB,(int(SEAM_T+(X1-SEAM_T-rw)/2),862-rh),rs)
AX=[int(v) for v in sys.argv[5].split(',')] if len(sys.argv)>5 else [470,470,625,400]
def arrow_layer(x0,y0,x1,y1):
    S=SS; L=Image.new('RGBA',(out.width*S,out.height*S),(0,0,0,0)); d=ImageDraw.Draw(L)
    cx,cy=x0+(x1-x0)*0.25,y1-10
    pts=[]
    for i in range(41):
        t=i/40; pts.append(((1-t)**2*x0+2*(1-t)*t*cx+t*t*x1,(1-t)**2*y0+2*(1-t)*t*cy+t*t*y1,t))
    def shape(grow):
        pl=[];pr=[]
        for i,(bx,by,t) in enumerate(pts[:-6]):
            nx,ny=pts[i+1][0]-bx,pts[i+1][1]-by; n=math.hypot(nx,ny); nx,ny=nx/n,ny/n; th=(4+15*t)+grow
            pl.append(((bx-ny*th)*S,(by+nx*th)*S)); pr.append(((bx+ny*th)*S,(by-nx*th)*S))
        bx,by,_=pts[-7]; ex,ey,_=pts[-1]; dx,dy=ex-bx,ey-by; n=math.hypot(dx,dy); dx,dy=dx/n,dy/n
        hw=34+grow; tip=(ex+dx*(10+grow*1.4),ey+dy*(10+grow*1.4))
        return pl+pr[::-1],[((bx-dy*hw)*S,(by+dx*hw)*S),(tip[0]*S,tip[1]*S),((bx+dy*hw)*S,(by-dx*hw)*S)]
    for grow,col in [(9,(0,0,0,70)),(4,(222,190,120,255)),(0,(18,72,48,255))]:
        body,head=shape(grow); d.polygon(body,fill=col); d.polygon(head,fill=col)
    return L.resize(out.size,Image.LANCZOS)
out=Image.alpha_composite(out.convert('RGBA'),arrow_layer(*AX)).convert('RGB')
out.save(OUT,quality=94); print('OK',OUT,'seam',round(SEAM_T,1))
