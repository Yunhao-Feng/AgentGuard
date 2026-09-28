"""Create an illustrative research walkthrough. Requires Pillow and ffmpeg."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess, math
ROOT=Path(__file__).resolve().parents[1]
W,H,FPS=1280,720,24
font='/System/Library/Fonts/Supplemental/Arial.ttf'
bold='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def f(n,b=False):return ImageFont.truetype(bold if b else font,n)
bg=(9,16,20); mint=(172,255,215); grey=(148,171,166)
scenes=[('01 / IDENTIFY','AgentHazard','When plausible steps compose into harm.',['USER TASK','TOOL CALLS','COMPOSED RISK']),('02 / VERIFY','VERA','Safety verdicts grounded in execution evidence.',['DISCOVER','EXECUTE','VERIFY']),('03 / LEARN','Three complementary guards','Learn from trajectories. Align decisions. Adapt policies.',['BraveGuard','HazardAuditor','AdaGuard']),('04 / ADAPT','Same action. Different policy.','Recorded action: send a public report externally.',['POLICY A: ALLOW','POLICY B: DENY','CONTEXT MATTERS'])]
proc=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'assets/research-demo.mp4')],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
for frame in range(24*FPS):
 t=frame/FPS; idx=min(int(t//6),3); local=t%6; stage,title,sub,labels=scenes[idx]
 im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
 for x in range(35,W,30):
  for y in range(35,H,30):d.ellipse((x,y,x+1,y+1),fill=(32,54,48))
 d.text((65,42),'YUNHAO FENG  /  AGENT SAFETY RESEARCH',font=f(17),fill=grey)
 d.text((990,42),'CONCEPT DEMO',font=f(17),fill=mint)
 d.line((65,84,1215,84),fill=(51,75,66))
 d.text((65,131),stage,font=f(20),fill=mint)
 d.text((65,190),title,font=f(57,True),fill=(234,246,239))
 d.text((65,277),sub,font=f(25),fill=grey)
 for j,label in enumerate(labels):
  x=65+j*398; active=local>=j*1.2; c=mint if active else (63,87,79)
  d.rounded_rectangle((x,379,x+354,509),radius=9,fill=(18,33,29),outline=c,width=2)
  d.text((x+22,399),f'0{j+1}',font=f(17),fill=grey)
  d.text((x+22,444),label,font=f(22,True),fill=c)
  if j<2:d.text((x+365,425),'>',font=f(25),fill=grey)
 if idx==3:
  d.text((65,544),'NR / NO VIOLATION',font=f(21),fill=mint)
  d.text((463,544),'R1 / POLICY VIOLATION',font=f(21),fill=(255,183,151))
 else:
  captions=['Trajectory-level safety benchmark','Executable cases + observable outcomes','Complementary research directions; not one integrated system']
  d.text((65,548),captions[idx],font=f(21),fill=grey)
 d.text((65,633),'ILLUSTRATIVE ANIMATION / NOT A LIVE MODEL RUN',font=f(14),fill=grey)
 d.text((1130,633),f'{int(t):02d} / 24',font=f(16),fill=mint)
 d.rectangle((65,677,1215,680),fill=(40,60,52)); d.rectangle((65,677,65+1150*t/24,680),fill=mint)
 if frame==8*FPS:im.save(ROOT/'assets/demo-poster.jpg',quality=94)
 proc.stdin.write(im.tobytes())
proc.stdin.close()
if proc.wait()!=0:raise RuntimeError('ffmpeg failed')
print('Generated 24-second H.264 video and poster')
