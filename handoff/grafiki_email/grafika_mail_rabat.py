import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F='/home/user/lala/handoff/video-tools/winterly/fonts/'
TPL='/home/user/lala/handoff/grafiki_black_week/winterly_black_week_balkon_4x5.png'
OUT='/tmp/claude-0/-home-user-lala/9af5c72f-959d-5981-b926-47b34d7272d6/scratchpad/mail/'
font=lambda n,s: ImageFont.truetype(F+n+'.ttf',s)
CREAM=(250,243,228); GREEN=(16,66,44); RED=(190,24,32); GOLD=(201,160,82); INK=(30,26,22)
tpl=Image.open(TPL).convert('RGB')
def logo(h):
    c=tpl.crop((455,8,672,158)); a=np.array(c).astype(float)
    d=np.clip(((np.array([252,240,226.])-a).sum(2)-45)/160.0,0,1)
    rgba=np.zeros((a.shape[0],a.shape[1],4),np.uint8); rgba[...,:3]=a.astype(np.uint8); rgba[...,3]=(d*255).astype(np.uint8)
    im=Image.fromarray(rgba,'RGBA'); im=im.crop(im.getbbox()); return im.resize((int(im.width*h/im.height),h),Image.LANCZOS)
def corners(img):  # gałązki z lampkami z rogów zwycięskiej grafiki
    for box,pos in (((0,0,260,160),(0,0)),((862,0,1122,160),(img.width-260,0))):
        c=tpl.crop(box).convert('RGBA'); a=np.array(c).astype(float)
        d=np.clip(((np.array([252,240,226.])-a[...,:3]).sum(2)-30)/120.0,0,1); a[...,3]=d*255
        img.alpha_composite(Image.fromarray(a.astype(np.uint8),'RGBA'),pos)
    for box,pos in (((0,1240,215,1402),(0,img.height-162)),((905,1240,1122,1402),(img.width-217,img.height-162))):
        c=tpl.crop(box).convert('RGBA'); a=np.array(c).astype(float)
        d=np.clip(((np.array([252,240,226.])-a[...,:3]).sum(2)-30)/120.0,0,1); a[...,3]=d*255
        img.alpha_composite(Image.fromarray(a.astype(np.uint8),'RGBA'),pos)
def ctext(d,W,y,t,f,fill):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill); return w
def photo(w,h,r=26):
    p=tpl.crop((418,300,1100,860)); k=max(w/p.width,h/p.height); p=p.resize((int(p.width*k)+1,int(p.height*k)+1),Image.LANCZOS)
    p=p.crop(((p.width-w)//2,(p.height-h)//2,(p.width-w)//2+w,(p.height-h)//2+h)).filter(ImageFilter.UnsharpMask(1.5,60,2))
    m=Image.new('L',(w*3,h*3),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w*3-1,h*3-1],r*3,fill=255); m=m.resize((w,h),Image.LANCZOS)
    o=Image.new('RGBA',(w,h)); o.paste(p,(0,0)); o.putalpha(m); return o
def make(W,H,name,sc=1.0,story=False):
    img=Image.new('RGBA',(W,H),CREAM+(255,)); corners(img); d=ImageDraw.Draw(img)
    y=int((56 if not story else 190)*sc)
    lg=logo(int(110*sc)); img.alpha_composite(lg,((W-lg.width)//2,y)); y+=lg.height+int(22*sc)
    ctext(d,W,y,'TYLKO DZIŚ • 25.11',font('Montserrat-ExtraBold',int(56*sc)),GREEN); y+=int(66*sc)
    f=font('PlayfairDisplay-Black',int(270*sc)); t='−10%'; w=d.textlength(t,font=f); bb=f.getbbox(t)
    d.text(((W-w)/2,y-bb[1]+int(6*sc)),t,font=f,fill=RED); y+=bb[3]-bb[1]+int(26*sc)
    ctext(d,W,y,'na wszystko',font('PlayfairDisplay-Bold',int(84*sc)),GREEN); y+=int(118*sc)
    pw,ph=int(W*0.86),int((390 if not story else 560)*sc)
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([(W-pw)//2+6,y+14,(W+pw)//2+6,y+ph+14],28,fill=(0,0,0,90))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d.rounded_rectangle([(W-pw)//2-5,y-5,(W+pw)//2+5,y+ph+5],31,fill=GOLD); img.alpha_composite(photo(pw,ph),((W-pw)//2,y)); y+=ph+int(46*sc)
    d=ImageDraw.Draw(img)
    fk=font('Montserrat-SemiBold',int(34*sc)); fc=font('Montserrat-ExtraBold',int(64*sc))
    lab='Twój kod:'; code='DZISIAJ10'; wl=d.textlength(lab,font=fk); wc=d.textlength(code,font=fc)
    bw=int(wl+wc+90*sc); bh=int(104*sc); bx=(W-bw)//2
    d.rounded_rectangle([bx,y,bx+bw,y+bh],int(20*sc),fill=(255,255,255),outline=GREEN,width=max(3,int(4*sc)))
    for x in range(bx+14,bx+bw-14,int(26*sc)): d.line([(x,y+int(10*sc)),(x+int(12*sc),y+int(10*sc))],fill=GOLD,width=2); d.line([(x,y+bh-int(10*sc)),(x+int(12*sc),y+bh-int(10*sc))],fill=GOLD,width=2)
    d.text((bx+int(34*sc),y+(bh-fk.size)/2-int(4*sc)),lab,font=fk,fill=INK)
    d.text((bx+int(34*sc)+wl+int(22*sc),y+(bh-fc.size)/2-int(10*sc)),code,font=fc,fill=RED); y+=bh+int(26*sc)
    ctext(d,W,y,'ważny dziś, 25.11, do 23:59',font('Montserrat-SemiBold',int(34*sc)),GREEN); y+=int(72*sc)
    fb=font('Montserrat-ExtraBold',int(50*sc)); t='ODBIERAM −10%  ›'; w=d.textlength(t,font=fb); bw,bh=int(w+120*sc),int(104*sc); bx=(W-bw)//2
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([bx,y+10,bx+bw,y+bh+10],bh//2,fill=(120,0,0,110)); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d=ImageDraw.Draw(img); d.rounded_rectangle([bx,y,bx+bw,y+bh],bh//2,fill=RED,outline=GOLD,width=max(3,int(4*sc)))
    d.text((bx+(bw-w)/2,y+(bh-fb.size)/2-int(6*sc)),t,font=fb,fill=(255,255,255)); y+=bh+int(34*sc)
    ctext(d,W,y,'Płatność przy odbiorze  •  30 dni na zwrot',font('Montserrat-SemiBold',int(30*sc)),INK)
    img.convert('RGB').save(OUT+name,quality=93); print('OK',name,'dół treści y=',y+int(40*sc),'/',H)
make(1200,1500,'winterly_mail_dzis10_1200x1500.jpg')
make(1080,1920,'winterly_dzis10_story_1080x1920.jpg',sc=0.92,story=True)
