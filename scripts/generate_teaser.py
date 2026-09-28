#!/usr/bin/env python3
"""Render the AgentGuard 15-second teaser. Python 3.10+, Pillow, NumPy, FFmpeg.
Usage: python scripts/generate_teaser.py [--preview-only] [--font path.ttf]
All copy, timings, data and card labels live in scripts/promo/teaser.json.
"""
import argparse,json,math,subprocess,hashlib,wave,shutil
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--config',type=Path,default=R/'scripts/promo/teaser.json');p.add_argument('--output',type=Path,default=R/'assets/teaser');p.add_argument('--font',type=Path,default=R/'assets/fonts/DM-Sans.ttf');p.add_argument('--preview-only',action='store_true');p.add_argument('--ffmpeg',default='ffmpeg');a=p.parse_args()
C=json.loads(a.config.read_text());OUT=a.output;OUT.mkdir(parents=True,exist_ok=True);W,H=C['size'];FPS=C['fps'];D=C['duration'];SC=C['scenes'];assert SC[0]['start']==0 and SC[-1]['end']==D
for i,s in enumerate(SC):
 assert s['end']>s['start']
 if i:assert SC[i-1]['end']==s['start']
INK='#112333';BLUE='#167fe5';AZURE='#1697e2';PEACH='#fddeb1';WHITE='#f8f8f8';MUTED='#496275';DARK='#102333'
@lru_cache(None)
def font(size,bold=False):
 f=ImageFont.truetype(str(a.font),size)
 try:f.set_variation_by_axes([32,700 if bold else 450])
 except (AttributeError,OSError,ValueError):pass
 return f
def txt(d,x,y,text,size=36,color=INK,bold=False):
 f=font(size,bold);bb=d.textbbox((0,0),text,font=f)
 if x+bb[2]>W-70:raise ValueError(f'Text exceeds safe area: {text}')
 d.text((int(x),int(y)),text,font=f,fill=color)
def center(d,y,text,size=36,color=INK,bold=False):
 f=font(size,bold);length=d.textlength(text,font=f);txt(d,(W-length)/2,y,text,size,color,bold)
def rr(d,rect,fill,radius=25,outline=None):d.rounded_rectangle(tuple(map(int,rect)),radius,fill=fill,outline=outline,width=2)
def ease(t):return 1-(1-max(0,min(1,t)))**3
def arrow(d,x,y,x2,y2,color,width=3):
 d.line((x,y,x2,y2),fill=color,width=width);ang=math.atan2(y2-y,x2-x);d.polygon([(x2,y2),(x2-13*math.cos(ang-.5),y2-13*math.sin(ang-.5)),(x2-13*math.cos(ang+.5),y2-13*math.sin(ang+.5))],fill=color)
def shield(d,cx,cy,size,color):
 points=[(cx,cy-size*.6),(cx+size*.52,cy-size*.4),(cx+size*.43,cy+size*.22),(cx,cy+size*.62),(cx-size*.43,cy+size*.22),(cx-size*.52,cy-size*.4)]
 d.line(points+[points[0]],fill=color,width=5);d.line([(cx-size*.20,cy),(cx-size*.04,cy+size*.17),(cx+size*.23,cy-size*.15)],fill=color,width=5)
def chrome(d,light=True):
 col=MUTED if light else '#b4cbdc';txt(d,96,50,C['team'].upper(),26,col,True);txt(d,1570,50,'RESEARCH / 2026',24,col)
 d.line((96,107,1824,107),fill='#d6e1e7' if light else '#294457',width=2)
def render_scene(idx,t):
 s=SC[idx];u=max(0,t-s['start']);intro=ease(u/.65);offset=round(35*(1-intro));dark=idx in (0,3)
 im=Image.new('RGB',(W,H),DARK if dark else WHITE);d=ImageDraw.Draw(im);chrome(d,not dark)
 # Restrained moving signal field, drawn behind all reading surfaces.
 if dark:
  for r in (190,280,370,460):
   cx,cy=1620,560;d.ellipse((cx-r,cy-r,cx+r,cy+r),outline='#224055',width=2)
  for n in range(7):
   ang=t*.28+n*.9;r=220+n*32;x=1620+math.cos(ang)*r;y=560+math.sin(ang)*r
   d.ellipse((x-5,y-5,x+5,y+5),fill=PEACH if n%2 else AZURE)
  txt(d,96,160,s['label'],23,PEACH,True)
 else:txt(d,96,150,s['label'],23,BLUE,True)
 if idx==0:
  txt(d,96,280+offset,s['lines'][0],104,WHITE,True)
  txt(d,96,401+offset,s['lines'][1],104,WHITE,True)
  txt(d,96,522+offset,s['lines'][2],104,PEACH,True)
  shield(d,1550,460,180,AZURE)
  labels=['REQUEST','ACTION','OUTCOME'];xs=[104,640,1176]
  for i,x in enumerate(xs):
   y=790;rr(d,(x,y,x+410,y+90),'#1c364b',12)
   txt(d,x+30,y+24,labels[i],28,PEACH if i==2 else '#d9e7f2',True)
   if i<2:arrow(d,x+430,y+45,x+510,y+45,AZURE)
   phase=max(0,min(1,(u-.3-i*.25)/1.3));d.rectangle((x,y+88,x+410*phase,y+92),fill=AZURE)
 elif idx==1:
  txt(d,96,204+offset,s['lines'][0],84,INK,True);txt(d,96,302+offset,s['lines'][1],84,BLUE,True)
  rr(d,(96,456,918,882),'#e8f2fc');rr(d,(952,456,1824,882),PEACH)
  ah=C['evidence']['AgentHazard'];ve=C['evidence']['VERA']
  txt(d,132,488,'AgentHazard',45,INK,True);txt(d,992,488,'VERA',45,INK,True)
  txt(d,132,555,f"{ah['instances']:,}",116,BLUE,True);txt(d,992,555,f"{ve['cases']:,}",116,INK,True)
  txt(d,132,698,'benchmark instances',33,MUTED);txt(d,992,698,'executable safety cases',33,MUTED)
  txt(d,132,796,f"{ah['risks']} risks  /  {ah['attacks']} attack strategies",27,INK,True);txt(d,992,796,f"{ve['risks']} risk categories",27,INK,True)
  txt(d,96,912,'Paper-reported statistics  /  AgentHazard, Table 1  ·  VERA, Abstract',22,MUTED)
 elif idx==2:
  txt(d,96,227+offset,s['lines'][0],108,INK,True)
  txt(d,100,373,'Three complementary directions for safer agents.',33,MUTED)
  colors=['#e8f2fc','#d9edfb',PEACH]
  for i,(name,sub,detail) in enumerate(C['guard_cards']):
   x=96+i*586;y=488+round(24*(1-ease((u-i*.10)/.6)));rr(d,(x,y,x+552,y+406),colors[i]);txt(d,x+32,y+30,f'0{i+1}',23,MUTED,True)
   # Evidence to judgment motif, independent of empirical performance.
   if i==0:
    d.arc((x+42,y+95,x+122,y+175),30,325,fill=BLUE,width=4)
    for j in range(3):
     angle=u*.7+j*math.tau/3;px=x+82+40*math.cos(angle);py=y+135+40*math.sin(angle);d.ellipse((px-6,py-6,px+6,py+6),fill=BLUE)
   elif i==1:
    rr(d,(x+46,y+91,x+118,y+180),'#f8f8f8',7)
    for j in range(3):d.line((x+57,y+110+j*21,x+106,y+110+j*21),fill=BLUE,width=4)
    sy=y+100+int((u*.6)%1*66);d.line((x+39,sy,x+128,sy),fill=INK,width=2)
   else:
    for j in range(2):
     rr(d,(x+43,y+102+j*48,x+128,y+132+j*48),'#ead0a8',15)
     px=x+60+int((.5+.5*math.sin(u*1.7+j*math.pi))*48);d.ellipse((px-10,y+107+j*48,px+10,y+127+j*48),fill=BLUE)
   arrow(d,x+164,y+140,x+268,y+140,BLUE);px=x+164+((u*.7)%1)*96;d.ellipse((px-5,y+135,px+5,y+145),fill=INK);shield(d,x+330,y+137,48,INK)
   txt(d,x+32,y+224,name,45,INK,True);txt(d,x+32,y+290,sub,29,MUTED);txt(d,x+32,y+336,detail,25,MUTED)
  txt(d,96,923,'Distinct contributions, connected by execution evidence.',23,MUTED)
 else:
  txt(d,96,256+offset,s['lines'][0],110,WHITE,True);txt(d,96,386+offset,s['lines'][1],110,PEACH,True)
  txt(d,101,552,'MEASURE  →  VERIFY  →  LEARN  →  ADAPT',31,'#b4cbdc',True)
  rr(d,(96,670,1824,785),'#1697e2',18);txt(d,133,698,C['url'],47,'#ffffff',True);txt(d,1725,695,'↗',48,'#ffffff')
  txt(d,100,834,'AgentHazard   ·   VERA   ·   BraveGuard   ·   HazardAuditor   ·   AdaGuard',31,'#cfdeea')
 # Separate readable subtitle and a very thin timeline.
 if idx!=1:
  center(d,982,s['caption'],28,'#c9d9e5' if dark else MUTED)
 else:center(d,982,s['caption'],28,MUTED)
 d.rectangle((0,1074,W,1080),fill='#27455d' if dark else '#dce5ec');d.rectangle((0,1074,W*min(1,t/D),1080),fill=AZURE)
 return im
def frame(t):
 idx=next((i for i,s in enumerate(SC) if s['start']<=t<s['end']),len(SC)-1)
 im=render_scene(idx,t)
 # Blend into each new scene; stable reading time is > 2.5 seconds per scene.
 if idx and t<SC[idx]['start']+.22:
  old=render_scene(idx-1,SC[idx]['start']-.001);im=Image.blend(old,im,ease((t-SC[idx]['start'])/.22))
 return im
preview=OUT/'frames';preview.mkdir(exist_ok=True)
for i,s in enumerate(SC):
 for tag,t in [('start',s['start']),('middle',(s['start']+s['end'])/2),('end',s['end']-1/FPS)]:frame(t).save(preview/f'{i+1:02}-{tag}.jpg',quality=94)
# Cover deliberately uses the closing visual with complete brand and call to action.
frame(13.8).save(OUT/'poster.jpg',quality=96)
thumbs=[]
for t in [1.5,5.2,9.7,13.8]:
 im=frame(t);im.thumbnail((768,432));thumbs.append(im)
contact=Image.new('RGB',(1536,864));
for i,im in enumerate(thumbs):contact.paste(im,((i%2)*768,(i//2)*432))
contact.save(OUT/'storyboard.jpg',quality=94)
def stamp(t,sep='.'):
 return f'{int(t)//3600:02}:{int(t)%3600//60:02}:{int(t)%60:02}{sep}{round((t%1)*1000):03}'
vtt='WEBVTT\n\n';srt='';transcript=[]
for i,s in enumerate(SC):
 vtt+=f"{stamp(s['start'])} --> {stamp(s['end'])}\n{s['caption']}\n\n";srt+=f"{i+1}\n{stamp(s['start'],',')} --> {stamp(s['end'],',')}\n{s['caption']}\n\n";transcript.append(f"{stamp(s['start'])} — {stamp(s['end'])}\n"+' '.join(s['lines'])+'\n'+s['caption'])
(OUT/'captions.en.vtt').write_text(vtt);(OUT/'captions.en.srt').write_text(srt);(OUT/'transcript.en.txt').write_text('\n\n'.join(transcript)+'\n');shutil.copyfile(a.config,OUT/'storyboard.json')
manifest={'title':C['title'],'team':C['team'],'duration':D,'fps':FPS,'size':[W,H],'type':'Animated research overview; no recorded model inference','sources':{},'audio':'Original procedural electronic score. No third-party samples or narration.','font':'DM Sans, SIL Open Font License 1.1; bundled license in assets/fonts/OFL.txt'}
for k,e in C['evidence'].items():manifest['sources'][k]=dict(e)
if not a.preview_only:
 sr=48000;N=int(sr*D);t=np.arange(N)/sr;music=np.zeros((N,2),np.float64);rng=np.random.default_rng(42)
 chords=[[146.832,220,293.665,369.994],[130.813,195.998,261.626,329.628],[164.814,246.942,329.628,391.995],[146.832,220,293.665,440]]
 for j,start in enumerate(np.arange(0,D,3.75)):
  end=min(D,start+4.2);a0=int(start*sr);n=int((end-start)*sr);tt=np.arange(n)/sr;env=np.minimum(1,tt/.4)*np.minimum(1,(end-start-tt)/.8)
  for k,f in enumerate(chords[j%4]):
   tone=(np.sin(2*np.pi*f*tt)+.22*np.sin(2*np.pi*f*2*tt))*.032*env
   music[a0:a0+n,0]+=tone;music[a0:a0+n,1]+=np.sin(2*np.pi*f*1.001*tt)*.036*env
 for beat,start in enumerate(np.arange(0,D,.5)):
  a0=int(start*sr);n=min(N-a0,int(sr*.38));tt=np.arange(n)/sr
  kick=np.sin(2*np.pi*(48*tt+1.7*(1-np.exp(-tt*32))))*np.exp(-tt*17)*.12
  f=chords[min(3,int(start/3.75))][beat%4]*4;tone=np.sin(2*np.pi*f*tt)*np.exp(-tt*11)*np.minimum(1,tt/.009)*.048
  music[a0:a0+n]+=np.stack([kick+tone,kick+tone*.8],axis=1)
  if beat%2:
   noise=rng.normal(0,1,n);hat=(noise-np.roll(noise,1))*np.exp(-tt*65)*.009;music[a0:a0+n]+=hat[:,None]
 envelope=np.minimum(1,t/.35)*np.minimum(1,(D-t)/.65);music*=envelope[:,None];music*=.65/max(.65,np.max(np.abs(music)))
 with wave.open(str(OUT/'original-score.wav'),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes((music*32767).astype('<i2').tobytes())
 cmd=[a.ffmpeg,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(OUT/'original-score.wav'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-af','loudnorm=I=-18:TP=-2:LRA=8','-ar','48000','-movflags','+faststart','-t',str(D),str(OUT/'agentguard-15s.mp4')]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for n in range(round(D*FPS)):
   proc.stdin.write(frame(n/FPS).tobytes())
   if n%90==0:print(f'Rendering {n}/{round(D*FPS)}',flush=True)
 finally:proc.stdin.close()
 if proc.wait():raise RuntimeError('FFmpeg encoding failed')
 manifest['video_sha256']=hashlib.sha256((OUT/'agentguard-15s.mp4').read_bytes()).hexdigest()
(OUT/'sources.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Complete:',OUT,flush=True)
