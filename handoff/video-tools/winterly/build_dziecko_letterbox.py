"""Film „Dziecko boi się ciemności” – wersja z klipów 16:9: klip na środku (1080x608) na rozmytym tle 9:16."""
import json, subprocess, numpy as np
from PIL import Image, ImageFilter
S='/tmp/claude-0/-home-user-lala/9af5c72f-959d-5981-b926-47b34d7272d6/scratchpad/'; SRC=S+'src_f2/'
T=json.load(open(S+'vo/dz1_fast_times.json')); r=lambda v: round(v,3); cut=lambda k: r(T[k][0]-0.06)
END=r(T['L'][1]+0.1); TOTAL=r(END+3.4); FPS=30
segs=[('k1.mp4',20.5,cut('B'),None,1.0),('k2.mp4',0.4,cut('C')-cut('B'),None,1.0),('k3.mp4',0.3,cut('D')-cut('C'),None,1.0),
      ('k4.mp4',0.0,cut('H')-cut('D'),None,None),(SRC+'s20.mp4',3.0,cut('I')-cut('H'),676,1.0),(SRC+'s16.mp4',3.75,cut('J')-cut('I'),420,1.0),
      ('C6',0,cut('K')-cut('J'),None,1.0),(SRC+'s18.mp4',1.0,TOTAL-cut('K'),640,1.0)]
VF_LB="[0:v]split[a][b];[a]{bgsrc}scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=38,eq=brightness=-0.16[bg];[b]{fgsrc}scale=1080:608:flags=lanczos,unsharp=5:5:0.6[fg];[bg][fg]overlay=0:656,fps=30,format=yuv420p"
names=[]; acc=0.0
for i,(f,st,dur,cy,spd) in enumerate(segs):
    nfr=int(round((acc+dur)*FPS))-int(round(acc*FPS)); acc+=dur; out=f'seg{i}.mp4'
    if f=='C6':
        im=Image.open('c6_screen.png').convert('RGB').crop((0,26,440,540))
        bg=im.resize((1080,int(im.height*1080/im.width)),Image.LANCZOS).resize((1080,1920),Image.LANCZOS).filter(ImageFilter.GaussianBlur(38))
        bg=Image.eval(bg,lambda v:int(v*0.84))
        enc=subprocess.Popen(['ffmpeg','-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        bh=int(440*608/1080)
        for k in range(nfr):
            p=k/max(1,nfr-1); e=p*p*(3-2*p); y0=int(95+e*(im.height-bh-95-20)); z=1.0+0.05*e
            cw,ch=int(440/z),int(bh/z); x0=(440-cw)//2
            fg=im.crop((x0,y0,x0+cw,y0+ch)).resize((1080,608),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,70,2))
            fr=bg.copy(); fr.paste(fg,(0,656)); enc.stdin.write(fr.tobytes())
        enc.stdin.close(); enc.wait()
    else:
        srcdur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
        if spd is None: spd=min(1.0,(srcdur-st-0.05)/dur)
        pts=f'setpts=PTS/{spd},' if spd!=1.0 else ''
        fgsrc=pts+(f'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,crop=1080:608:0:{cy},' if cy is not None else '')
        bgsrc=pts
        vf=VF_LB.format(bgsrc=bgsrc,fgsrc=fgsrc)+',tpad=stop_mode=clone:stop_duration=1'
        subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(st),'-t',f'{dur*spd+0.3:.3f}','-i',f,'-an','-filter_complex',vf,'-frames:v',str(nfr),'-c:v','libx264','-crf','17','-preset','fast',out],check=True)
    names.append(out); print(i,f.split('/')[-1],st,round(dur,3),nfr)
open('lst.txt','w').writelines(f"file '{n}'\n" for n in names)
subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-f','concat','-safe','0','-i','lst.txt','-c','copy','dziecko_lb.mp4'],check=True)
cfg={"out":"dziecko_lb_end.mp4","emoji_dir":S+"emo/pkg/package/img/google/64","punch":False,"dissolve":0,"badge_from":999,
     "hook":{"lines":[],"until":0},"stickers":[],"end_dur":3.4,"logo":"/home/user/lala/handoff/video-tools/winterly/logo_winterly_zlote.png","logo_w":400,
     "end":{"pill":"BLACK MONTH • do −35%","pill_emoji":"1f525","lines":["Zamów na","*winterly.pl*"],"button":"KUP TERAZ","small":"Drugi zestaw 50 zł taniej • 30 dni na zwrot"},
     "beats":[{"dur":TOTAL,"segs":[["dziecko_lb.mp4",0.0,TOTAL]],"subs":[]}]}
json.dump(cfg,open('cfg_dziecko_end.json','w'),ensure_ascii=False,indent=1)
s=lambda k: r(T[k][0]-0.02)
n={"in":"dziecko_lb_end.mp4","out":"dziecko_napisy.mp4","emoji_dir":S+"emo/pkg/package/img/google/64","sub_y":0.725,
   "hook":{"lines":["Moja córka","bała się ciemności"],"emoji":"1f97a","until":cut('B'),"y":0.2},
   "subs":[[s('B'),cut('C'),"„Mamo, nie gaś światła…”"],[s('C'),cut('D'),"Więc powiesiłam w jej oknie kurtynę LED."],
           [s('D'),s('E'),"Teraz przed snem"],[s('E'),s('F'),"razem wybieramy w telefonie,"],[s('F'),s('G'),"co ma świecić:"],
           [s('G'),s('H'),"bałwanek,"],[s('H'),s('I'),"gwiazdki"],[s('I'),s('J'),"albo Mikołaj."],[s('J'),s('K'),"Zasypia z uśmiechem…"],
           [s('K'),END,"a z zewnątrz to najpiękniejsze okno na osiedlu."]],
   "end":{"from":999,"lines":["-"]}}
json.dump(n,open('napisy_dziecko.json','w'),ensure_ascii=False,indent=1)
print('END',END,'TOTAL',TOTAL)
