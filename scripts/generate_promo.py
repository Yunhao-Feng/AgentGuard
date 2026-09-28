#!/usr/bin/env python3
"""Reproducible 90-second research film. CPU only; FFmpeg required.

python scripts/generate_promo.py --preview-only
python scripts/generate_promo.py
python scripts/generate_promo.py --font /path/font.ttf --bold-font /path/bold.ttf

The original generate_demo.py is intentionally preserved.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, shutil, subprocess, sys, tempfile, wave
from functools import lru_cache
from pathlib import Path
import numpy as np
import pymupdf
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
P=argparse.ArgumentParser(description=__doc__)
P.add_argument('--config',type=Path,default=ROOT/'scripts/promo/storyboard.json')
P.add_argument('--output',type=Path,default=ROOT/'assets/promo')
P.add_argument('--font',type=Path);P.add_argument('--bold-font',type=Path)
P.add_argument('--preview-only',action='store_true')
P.add_argument('--ffmpeg',default='ffmpeg')
ARGS=P.parse_args()
CFG=json.loads(ARGS.config.read_text());OUT=ARGS.output.resolve();OUT.mkdir(parents=True,exist_ok=True)
W,H=CFG['size'];FPS=CFG['fps'];DURATION=CFG['duration'];SCENES=CFG['scenes']
assert (W,H)==(1920,1080),'This layout is authored at 1920 x 1080.'
assert SCENES[0]['start']==0 and SCENES[-1]['end']==DURATION
for i,s in enumerate(SCENES):
 assert s['end']>s['start']
 if i:assert s['start']==SCENES[i-1]['end'],'Scene times must be contiguous.'
# Matplotlib ships DejaVu fonts on every supported OS. Explicit font paths override.
import matplotlib
from matplotlib import font_manager
FONT=ARGS.font or Path(font_manager.findfont('DejaVu Sans'))
BOLD=ARGS.bold_font or Path(font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans',weight='bold')))
for path in [FONT,BOLD]:
 if not path.is_file():raise FileNotFoundError(path)
@lru_cache(None)
def font(size,bold=False):return ImageFont.truetype(str(BOLD if bold else FONT),size)
NAVY='#0b1428';BLUE='#2563eb';INK='#111827';MUTED='#59667b';PALE='#eef3fc';LINE='#dbe4f0';WHITE='#ffffff';TEAL='#087f71';ORANGE='#ba4a21'
def ease(x):x=max(0,min(1,x));return 1-(1-x)**3

def text(d,xy,s,size=30,fill=INK,bold=False,maxw=None):
 f=font(size,bold)
 if maxw:
  while d.textbbox((0,0),s,font=f)[2]>maxw and size>14:size-=1;f=font(size,bold)
 d.text(xy,s,font=f,fill=fill,stroke_width=0)

def box(d,rect,fill=WHITE,outline=LINE,r=18,width=2):d.rounded_rectangle(rect,radius=r,fill=fill,outline=outline,width=width)

def arrow(d,x,y,x2,y2,color=BLUE,width=4):
 d.line((x,y,x2,y2),fill=color,width=width)
 a=math.atan2(y2-y,x2-x)
 d.polygon([(x2,y2),(x2-14*math.cos(a-.45),y2-14*math.sin(a-.45)),(x2-14*math.cos(a+.45),y2-14*math.sin(a+.45))],fill=color)

# Extract original figures without recoloring, retouching, or removing scientific content.
figures={};manifest={'title':CFG['title'],'sources':{},'results':CFG['results'],'transformations':['Figure-only PDF crops at 3x PDF-point resolution; no recoloring or retouching.','Charts redraw published point estimates on 0–100% axes. No uncertainty was supplied; none invented.','Opening and policy examples are explanatory reconstructions, not recorded inference.'],'audio':{'type':'original procedural synthesis','seed':20260928,'sample_rate':48000,'narration':False}}
(OUT/'figures').mkdir(exist_ok=True)
for key,source in CFG['sources'].items():
 source_path=ROOT/source['file'];doc=pymupdf.open(source_path)
 pix=doc[source['figure_page']-1].get_pixmap(matrix=pymupdf.Matrix(3,3),clip=pymupdf.Rect(source['crop']),alpha=False)
 path=OUT/'figures'/f'{key}.png';pix.save(path)
 figures[key]=Image.open(path).convert('RGB')
 manifest['sources'][key]={**source,'sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),'asset':f'figures/{key}.png'}
(OUT/'sources.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
(OUT/'results.js').write_text('window.PAPER_RESULTS = '+json.dumps(CFG['results'])+';\n')
shutil.copyfile(ARGS.config,OUT/'storyboard.json') if ARGS.config.resolve()!= (OUT/'storyboard.json').resolve() else None

@lru_cache(None)
def fitted(key,width,height):
 im=figures[key].copy();im.thumbnail((width,height),Image.Resampling.LANCZOS);return im

def place_figure(im,key,rect,label=True):
 d=ImageDraw.Draw(im);x,y,x2,y2=rect;box(d,rect,WHITE,LINE)
 f=fitted(key,x2-x-32,y2-y-54)
 im.paste(f,(x+(x2-x-f.width)//2,y+14+(y2-y-54-f.height)//2))
 if label:text(d,(x+20,y2-32),f"ORIGINAL PAPER FIGURE  /  {CFG['sources'][key]['figure']}",16,MUTED)

BASE={}
for dark in [False,True]:
 im=Image.new('RGB',(W,H),NAVY if dark else '#f7f9fd');d=ImageDraw.Draw(im)
 for x in range(88,1900,64):
  for y in range(124,946,64):d.ellipse((x,y,x+2,y+2),fill='#21314c' if dark else '#dfe7f3')
 d.line((88,99,1832,99),fill='#2c3c59' if dark else LINE,width=2)
 text(d,(88,47),'YUNHAO FENG  /  AGENT SAFETY RESEARCH',23,'#b6c8e5' if dark else MUTED,bold=True)
 text(d,(1470,47),'RESEARCH FILM  ·  2026',22,'#b6c8e5' if dark else MUTED)
 BASE[dark]=im

def chrome(scene,t,dark):
 im=BASE[dark].copy();d=ImageDraw.Draw(im);fg=WHITE if dark else INK
 text(d,(88,136),scene['chapter'],23,'#8cb6ff' if dark else BLUE,bold=True)
 if scene['id'] not in ['hook','outro']:
  text(d,(88,176),scene['title'],72,fg,bold=True)
  text(d,(90,264),scene['second'],35,'#c7d4e8' if dark else MUTED)
 # Permanent labels are intentionally separate from the subtitle area.
 d.rectangle((0,938,W,1080),fill=NAVY if dark else '#f7f9fd')
 text(d,(88,954),scene['source'],19,'#9cb0cd' if dark else MUTED,maxw=1740)
 box(d,(88,993,1832,1053),'#152441' if dark else '#e7eefb',None,r=10)
 caption=scene['caption']
 text(d,(118,1006),caption,25,'#eff5ff' if dark else INK,maxw=1680)
 d.rectangle((0,1073,W,1079),fill='#233754' if dark else '#d9e4f5')
 d.rectangle((0,1073,round(W*t/DURATION),1079),fill='#72a8ff' if dark else BLUE)
 for s in SCENES[1:]:
  x=round(W*s['start']/DURATION);d.line((x,1073,x,1079),fill=WHITE,width=3)
 return im

def hook(im,l):
 d=ImageDraw.Draw(im)
 text(d,(88,216),'A harmless step.',86,WHITE,True)
 text(d,(88,321),'A harmful trajectory.',86,'#83b2ff',True)
 text(d,(91,459),'Risk can emerge when actions are composed.',34,'#b6c8e5')
 labels=[('Inspect','workspace'),('Prepare','a hook'),('Access','sensitive data'),('Attempt','external transfer')]
 for j,(a,b) in enumerate(labels):
  x=88+j*445;active=l>.8+j*.8;c=('#ffb293' if j==3 else '#82b2ff') if active else '#536783'
  box(d,(x,599,x+405,788),'#13233e',c,width=2)
  text(d,(x+25,620),f'0{j+1}',23,c,True);text(d,(x+25,662),a,35,WHITE,True);text(d,(x+25,716),b,27,'#c3d2e8')
  if j<3:arrow(d,x+411,694,x+439,694,'#6686b2')
 text(d,(91,841),'SAFETY IS A PROPERTY OF THE TRAJECTORY.',27,'#b9d3ff',True)

def agenthazard(im,l):
 d=ImageDraw.Draw(im);place_figure(im,'agenthazard',(620,344,1832,892))
 text(d,(91,349),'THE BENCHMARK',23,BLUE,True)
 p=ease(l/2)
 text(d,(86,393),f"{round(CFG['results']['agenthazard']['instances']*p):,}",110,INK,True)
 text(d,(94,522),'executable risk instances',27,MUTED)
 for j,(v,lab) in enumerate([(str(CFG['results']['agenthazard']['risks']),'risk categories'),(str(CFG['results']['agenthazard']['attacks']),'attack strategies')]):
  y=593+j*121;text(d,(90,y),v,56,BLUE,True);text(d,(190,y+23),lab,26,MUTED)
 # The source is retained in full. A moving border points to the construction stage.
 stage=min(2,int(l/4.4));labels=['Taxonomy → executable tasks','Execution-based filtering','Human-reviewed benchmark']
 text(d,(642,905),labels[stage],21,BLUE,True)

def vera(im,l):
 d=ImageDraw.Draw(im)
 # Show the original stages at a readable size before highlighting their purposes.
 place_figure(im,'vera',(88,344,1260,831))
 stage=min(2,int(l/4.34));names=['Discover','Construct','Verify'];subs=['Literature-grounded risks','Executable safety cases','Observable outcomes']
 for j,(a,b) in enumerate(zip(names,subs)):
  y=358+j*119;active=j==stage
  box(d,(1300,y,1832,y+100),'#e6efff' if active else WHITE,BLUE if active else LINE)
  text(d,(1325,y+10),f'0{j+1} / {a}',30,BLUE if active else INK,True);text(d,(1325,y+57),b,22,MUTED)
 text(d,(94,865),f"{CFG['results']['vera']['cases']:,} executable cases",35,BLUE,True)
 text(d,(700,865),f"{CFG['results']['vera']['risks']} risk categories",35,BLUE,True)
 text(d,(1304,752),'STATE + TOOL EVIDENCE',21,BLUE,True)
 text(d,(1304,798),'Beyond model self-report.',25,INK,maxw=520)

def braveguard(im,l):
 d=ImageDraw.Draw(im)
 if l<5.0:
  place_figure(im,'braveguard',(88,338,1058,913))
  labels=['Discover emerging threats','Collect realistic trajectories','Train trajectory-aware guards','Feed validation failures back']
  for j,lab in enumerate(labels):
   y=375+j*126;active=l>.2+j*.6
   text(d,(1110,y),f'0{j+1}',24,BLUE if active else MUTED,True)
   text(d,(1110,y+36),lab,28,INK,maxw=700)
   if j<3:arrow(d,1123,y+80,1123,y+107,BLUE,3)
 else:
  r=CFG['results']['braveguard'];p=ease((l-5)/1.8)
  text(d,(89,343),'AgentHazard-Strongest  /  Accuracy (%)',28,INK,True)
  x0=625;xend=1705
  for tick in range(0,101,25):
   x=x0+(xend-x0)*tick/100;d.line((x,423,x,743),fill=LINE,width=2);text(d,(x-14,758),str(tick),22,MUTED)
  for j,(lab,val,c) in enumerate([('Off-the-shelf guards',r['baseline'],'#657b9d'),('BraveGuard-trained',r['trained'],BLUE)]):
   y=452+j*150;text(d,(93,y+14),lab,32,INK,True,maxw=510);d.rectangle((x0,y,x0+(xend-x0)*val/100*p,y+66),fill=c)
   text(d,(x0+(xend-x0)*val/100*p+18,y+12),f'{val:.2f}%',36,c,True)
  text(d,(92,832),'GPT-5.5 / OpenClaw 3.11 trajectories',27,INK,True)
  text(d,(92,878),'Model-group averages; not a paired single-model improvement.',24,MUTED)

def hazard(im,l):
 d=ImageDraw.Draw(im);r=CFG['results']['hazardauditor']
 if l<4:
  place_figure(im,'hazardauditor',(88,343,1150,903))
  text(d,(1210,376),'GuardPO',54,BLUE,True)
  text(d,(1210,462),'Execution evidence',29,INK,True)
  arrow(d,1240,522,1240,565)
  text(d,(1210,582),'Rationale + verdict',29,INK,True)
  arrow(d,1240,642,1240,685)
  text(d,(1210,703),'One safety decision',29,BLUE,True)
  text(d,(1210,790),'Balance the training signal.',23,MUTED)
  text(d,(1210,834),'Across agent frameworks.',23,MUTED)
  return
 p=ease((l-4)/2.5)
 # Labels and patterned baseline bars carry meaning without relying on color.
 text(d,(88,330),'CUA-EXEC  /  Accuracy (%)',27,INK,True)
 text(d,(970,335),'////  BraveGuard-Qwen3-Guard-8B',20,'#586e91',True)
 text(d,(1510,335),'■  HazardAuditor',22,BLUE,True)
 x0=450;xend=1670;top=426;bottom=844
 for tick in range(0,101,25):
  x=x0+(xend-x0)*tick/100;d.line((x,top-17,x,bottom),fill=LINE,width=2);text(d,(x-14,bottom+10),str(tick),20,MUTED)
 for j,name in enumerate(r['frameworks']):
  y=top+j*103
  spotlight=min(3,int(max(0,l-8)/2)) if l>=8 else -1
  if j==spotlight:box(d,(76,y-8,1832,y+76),'#eaf0fc',None,r=8)
  text(d,(90,y+12),name,29,INK,True)
  for k,(val,color) in enumerate([(r['baseline'][j],'#7187aa'),(r['auditor'][j],BLUE)]):
   yy=y+k*37;right=x0+(xend-x0)*val/100*p
   d.rectangle((x0,yy,right,yy+27),fill=color)
   if k==0:
    for xx in range(x0,int(right)-7,18):d.line((xx,yy+25,min(xx+7,right),yy+3),fill='#ccd6e6',width=2)
   text(d,(right+12,yy-4),f'{val:.2f}',24,color,True)
 text(d,(90,900),'100 safe + 100 unsafe trajectories per framework  ·  Same-table comparison',23,MUTED)
 if l>=8:
  j=min(3,int((l-8)/2));gain=r['auditor'][j]-r['baseline'][j]
  text(d,(1450,191),f'+{gain:.1f} pp',43,BLUE,True)
  text(d,(1450,249),r['frameworks'][j]+' accuracy',21,MUTED)

def ada(im,l):
 d=ImageDraw.Draw(im)
 box(d,(88,349,1832,499),WHITE,LINE)
 text(d,(114,369),'RECORDED ACTION',20,BLUE,True)
 text(d,(114,404),'send_email(external, public_report)',37,INK,True)
 text(d,(114,458),'Observed outcome: delivery successful.',24,MUTED)
 for j,(title,rule,verdict,c) in enumerate([('POLICY A','Public reports may be sent externally.','NR  /  NO VIOLATION',TEAL),('POLICY B','No files may be sent externally.','R1  /  POLICY VIOLATION',ORANGE)]):
  x=88+j*892;box(d,(x,543,x+852,765),WHITE,LINE)
  text(d,(x+28,561),title,22,BLUE,True);text(d,(x+28,610),rule,27,INK,maxw=795)
  if l>2+j*2:
   box(d,(x+25,669,x+827,740),'#e8f5f1' if j==0 else '#fff0e8',None,r=10)
   text(d,(x+44,683),verdict,29,c,True)
 if l<9:
  text(d,(91,827),'Only the policy changes.',42,BLUE,True)
  text(d,(94,888),'Explanatory reconstruction of AdaGuard Figure 1; no live inference.',23,MUTED)
 else:
  text(d,(91,812),f"{CFG['results']['adaguard']['accuracy']:.2f}%",74,BLUE,True)
  text(d,(465,822),CFG['results']['adaguard']['model']+'  /  '+CFG['results']['adaguard']['dataset'],31,INK,True)
  text(d,(465,872),f"Binary accuracy · {CFG['results']['adaguard']['samples']:,} test examples · Paper-reported result",24,MUTED)

def outro(im,l):
 d=ImageDraw.Draw(im)
 text(d,(88,218),'Build more capable agents.',78,WHITE,True,maxw=1750)
 text(d,(88,324),'Make every action accountable.',78,'#85b4ff',True,maxw=1750)
 labels=['AgentHazard','VERA','BraveGuard','HazardAuditor','AdaGuard']
 for j,lab in enumerate(labels):
  x=88+j*352;box(d,(x,532,x+328,624),'#152642','#3c5a89',r=14)
  text(d,(x+20,558),lab,27,WHITE,True,maxw=290)
 text(d,(91,686),CFG['author'],30,'#c5d5ec')
 text(d,(91,751),'github.com/Yunhao-Feng',40,WHITE,True)
 text(d,(91,817),'huggingface.co/datasets/Yunhao-Feng/AgentHazard',29,'#91baff')
 text(d,(91,870),'Models: huggingface.co/Yunhao-Feng',26,'#91baff')

DRAW={'hook':hook,'agenthazard':agenthazard,'vera':vera,'braveguard':braveguard,'hazardauditor':hazard,'adaguard':ada,'outro':outro}
def scene_frame(scene,t):
 dark=scene['id'] in ['hook','outro'];im=chrome(scene,t,dark);local=t-scene['start'];DRAW[scene['id']](im,local)
 cut={'braveguard':5.0,'hazardauditor':4.0}.get(scene['id'])
 if cut is not None and cut<=local<cut+.3:
  before=chrome(scene,t,dark);DRAW[scene['id']](before,cut-.01);im=Image.blend(before,im,ease((local-cut)/.3))
 return im

def frame(t):
 i=next(i for i,s in enumerate(SCENES) if s['start']<=t<s['end'])
 s=SCENES[i];im=scene_frame(s,t);local=t-s['start']
 if i and local<.38:
  prev=scene_frame(SCENES[i-1],s['start']-1/FPS)
  im=Image.blend(prev,im,ease(local/.38))
 return im

# Captions match the burned-in English captions; a clean transcript is also distributed.
def stamp(t,sep='.'):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}{sep}{ms%1000:03}'
vtt='WEBVTT\n\n';srt='';transcript=[]
for i,s in enumerate(SCENES):
 vtt+=f"{stamp(s['start'])} --> {stamp(s['end'])}\n{s['caption']}\n\n"
 srt+=f"{i+1}\n{stamp(s['start'],',')} --> {stamp(s['end'],',')}\n{s['caption']}\n\n"
 transcript.append(f"{stamp(s['start'])}  {s['title']} {s['second']}\n{s['caption']}\nSource: {s['source']}\n")
(OUT/'captions.en.vtt').write_text(vtt);(OUT/'captions.en.srt').write_text(srt);(OUT/'transcript.en.txt').write_text('\n'.join(transcript))
# Poster uses the finished typography; no fake player chrome.
poster=BASE[True].copy();d=ImageDraw.Draw(poster)
text(d,(88,153),'FIVE WORKS. ONE RESEARCH DIRECTION.',25,'#88b6ff',True)
text(d,(88,254),'From Agent Risks',104,WHITE,True)
text(d,(88,384),'to Adaptive Defenses',104,'#85b4ff',True)
text(d,(92,568),'Measure risk. Verify behavior. Learn to protect.',37,'#c5d5ec')
for j,name in enumerate(['AgentHazard','VERA','BraveGuard','HazardAuditor','AdaGuard']):
 x=88+j*352;box(d,(x,714,x+328,813),'#162845','#3d5e8e',r=14);text(d,(x+20,744),name,26,WHITE,True,maxw=290)
text(d,(92,934),'90 SECONDS  /  ENGLISH  /  RESEARCH RESULTS + METHOD ANIMATIONS',23,'#b8cdea')
poster.save(OUT/'poster.jpg',quality=95)
# Save scene start, midpoint and final frame for explicit layout review.
qa=ROOT/'.qa/promo';qa.mkdir(parents=True,exist_ok=True)
for s in SCENES:
 for label,t in [('start',s['start']+.5),('middle',(s['start']+s['end'])/2),('end',s['end']-1/FPS)]:
  frame(t).save(qa/f"{s['id']}-{label}.jpg",quality=93)
contact=Image.new('RGB',(960,7*180),'#ccd5e0')
for row,s in enumerate(SCENES):
 for col,label in enumerate(['start','middle','end']):
  a=Image.open(qa/f"{s['id']}-{label}.jpg");a.thumbnail((320,180));contact.paste(a,(col*320,row*180))
contact.save(qa/'contact.jpg',quality=95)

# Standard static plotting export for the website and independent checking of values.
import matplotlib.pyplot as plt
r=CFG['results']['hazardauditor']
with plt.rc_context({'font.family':'DejaVu Sans','font.size':12,'svg.fonttype':'none'}):
 fig,ax=plt.subplots(figsize=(11,6.4));fig.subplots_adjust(left=.17,right=.94,top=.76,bottom=.20);y=np.arange(4)
 a=ax.barh(y-.18,r['baseline'],height=.32,color='#7187aa',hatch='///',label='BraveGuard-Qwen3-Guard-8B')
 b=ax.barh(y+.18,r['auditor'],height=.32,color=BLUE,label='HazardAuditor')
 ax.bar_label(a,fmt='%.2f',padding=5,fontsize=11);ax.bar_label(b,fmt='%.2f',padding=5,fontsize=11)
 ax.set_yticks(y,r['frameworks']);ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xticks([0,25,50,75,100]);ax.set_xlabel('Accuracy (%)');ax.set_title('CUA-EXEC · Same-table comparison',loc='left',pad=58,fontweight='bold')
 ax.spines[['top','right','left']].set_visible(False);ax.set_axisbelow(True);ax.grid(axis='x',color='#e2e8f0');ax.legend(loc='lower left',bbox_to_anchor=(0,1.01),ncol=2,frameon=False,fontsize=10)
 fig.text(.17,.055,'100 safe + 100 unsafe trajectories per framework. Accuracy endpoint.',fontsize=9,color='#536174')
 fig.text(.17,.025,'Source: supplied HazardAuditor manuscript, Table 1, PDF p. 8. See paper for recall/F1 trade-offs.',fontsize=8,color='#536174')
 fig.savefig(OUT/'comparison.svg');fig.savefig(OUT/'comparison.png',dpi=180);plt.close(fig)
if ARGS.preview_only:
 print('Preview frames, figures, poster, chart, captions and provenance ready.',flush=True);sys.exit(0)
if not shutil.which(ARGS.ffmpeg):raise SystemExit('FFmpeg not found; install it or supply --ffmpeg /path/to/ffmpeg')

def music(path):
 sr=48000;n=round(DURATION*sr);t=np.arange(n,dtype=np.float64)/sr;rng=np.random.default_rng(20260928)
 # Four slow, original chord voicings. No samples or copyrighted recordings.
 audio=np.zeros((n,2),dtype=np.float32)
 chords=[[146.832,220,293.665,349.228],[130.813,196,261.626,329.628],[164.814,220,329.628,391.995],[110,164.814,220,293.665]]
 for start in range(0,DURATION,8):
  i0=int(start*sr);i1=min(n,int((start+8)*sr));tt=np.arange(i1-i0)/sr
  env=np.minimum(tt/1.3,1)*np.minimum((len(tt)/sr-tt)/1.6,1)
  for k,freq in enumerate(chords[start//8%4]):
   for channel,detune in enumerate([.999,1.001]):
    audio[i0:i1,channel]+=(.020*env*(np.sin(2*np.pi*freq*detune*tt)+.22*np.sin(2*np.pi*2*freq*tt))).astype(np.float32)
 # Quiet pulse and arpeggio at 96 BPM, with exponential note envelopes.
 beat=60/96
 for beat_i in range(int(DURATION/beat)):
  start=beat_i*beat;i0=int(start*sr);i1=min(n,i0+int(sr*.45));tt=np.arange(i1-i0)/sr
  if beat_i%2==0:
   kick=.038*np.sin(2*np.pi*(52*tt+15*(1-np.exp(-tt*25))/25))*np.exp(-tt*16)
   audio[i0:i1]+=kick[:,None].astype(np.float32)
  freq=chords[int(start)//8%4][beat_i%4]*2
  note=.018*np.sin(2*np.pi*freq*tt)*np.exp(-tt*9)*(1-np.exp(-tt*80))
  audio[i0:i1,beat_i%2]+=note.astype(np.float32)
 for s in SCENES[1:]:
  i0=int((s['start']-.2)*sr);i1=min(n,i0+int(.6*sr));tt=np.arange(i1-i0)/sr
  sweep=.012*np.sin(2*np.pi*(390*tt+600*tt**2))*np.sin(np.pi*tt/.6)**2
  audio[i0:i1]+=sweep[:,None].astype(np.float32)
 env=(np.minimum(t/2,1)*np.minimum((DURATION-t)/3,1)).astype(np.float32);audio*=env[:,None]
 peak=float(np.max(np.abs(audio)));audio*=.38/max(peak,.001)
 with wave.open(str(path),'wb') as w:
  w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((audio*32767).astype('<i2').tobytes())
 manifest['audio'].update({'peak_before_encoding':float(np.max(np.abs(audio))),'rms_before_encoding':float(np.sqrt(np.mean(audio**2)))})

with tempfile.TemporaryDirectory(prefix='agent-promo-') as tmp:
 tmp=Path(tmp);music(tmp/'music.wav');silent=tmp/'silent.mp4'
 cmd=[ARGS.ffmpeg,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',str(silent)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for i in range(round(DURATION*FPS)):
   proc.stdin.write(frame(i/FPS).tobytes())
   if i%(FPS*5)==0:print(f'Rendered {i/FPS:.0f} / {DURATION}s',flush=True)
 finally:proc.stdin.close()
 if proc.wait()!=0:raise RuntimeError('FFmpeg video encoding failed')
 subprocess.run([ARGS.ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(silent),'-i',str(tmp/'music.wav'),'-c:v','copy','-c:a','aac','-b:a','192k','-af','loudnorm=I=-20:TP=-2:LRA=7','-ar','48000','-t',str(DURATION),'-movflags','+faststart',str(OUT/'agent-safety-film.mp4')],check=True)
 shutil.copyfile(tmp/'music.wav',OUT/'original-score.wav')
manifest.update({'render':{'size':[W,H],'fps':FPS,'duration':DURATION,'font':FONT.name,'bold_font':BOLD.name,'pillow':Image.__version__,'python':sys.version.split()[0]},'film_sha256':hashlib.sha256((OUT/'agent-safety-film.mp4').read_bytes()).hexdigest()})
(OUT/'sources.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
print('Finished: '+str(OUT/'agent-safety-film.mp4'),flush=True)
