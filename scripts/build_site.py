#!/usr/bin/env python3
"""Package a static site from an explicit list of public assets."""
from pathlib import Path
from zipfile import ZipFile
import argparse,re,shutil
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=R/'_site');a=p.parse_args();out=a.output.resolve()
assert out!=R
FILES=['index.html','metrics.html','jev.html','style.css','metrics.css','jev.css','app.js','metrics.js','jev.js','site-content.js','.nojekyll','assets/favicon.svg','assets/promo/results.js','assets/promo/comparison.svg','docs/EVIDENCE.md']
DIRS=['assets/brand','assets/data','assets/fonts','assets/methods','assets/teaser']
private=re.compile(r'\biclr\b|under review as a conference paper|anonymous authors|submission\s+(?:id|number)\s*[:#]?\s*\d+',re.I)
def inspect(name,data):
 if name.lower().endswith(('.pdf','.doc','.docx')) or data.lstrip().startswith(b'%PDF-'):raise ValueError('Document attachment rejected: '+name)
 if name.lower().endswith(('.html','.js','.json','.md','.svg','.txt','.srt','.vtt','.py','.css','.yml')):
  text=data.decode('utf-8',errors='replace')
  if private.search(text):raise ValueError('Private document metadata rejected: '+name)
 if name.lower().endswith('.zip'):
  from io import BytesIO
  with ZipFile(BytesIO(data)) as z:
   for item in z.infolist():
    if not item.is_dir():inspect(item.filename,z.read(item))
files=[R/f for f in FILES]+[f for d in DIRS for f in (R/d).rglob('*') if f.is_file()]
for f in files:inspect(str(f.relative_to(R)),f.read_bytes())
# Never clean arbitrary directories. Only this script's known output folders are accepted.
assert out==R/'_site' or out.is_relative_to(R/'.qa'),'Use _site or a directory beneath .qa.'
if out.exists():shutil.rmtree(out)
for f in files:
 target=out/f.relative_to(R);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,target)
print(f'Packaged {len(files)} reviewed public assets into {out.name}.')
