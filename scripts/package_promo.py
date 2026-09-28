#!/usr/bin/env python3
"""Bundle the rendering source and supplied PDFs for an independent rebuild."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json
ROOT=Path(__file__).resolve().parents[1]
config=json.loads((ROOT/'scripts/promo/storyboard.json').read_text())
files=[ROOT/'scripts/generate_promo.py',ROOT/'scripts/generate_demo.py',ROOT/'scripts/package_promo.py']
files+=sorted((ROOT/'scripts/promo').glob('*.*'))
files += [ROOT/s['file'] for s in config['sources'].values()]
files += [ROOT/'assets/promo/SOURCES.md',ROOT/'assets/promo/sources.json']
output=ROOT/'assets/promo/promo-source.zip'
with ZipFile(output,'w',ZIP_DEFLATED,compresslevel=6) as z:
 for path in files:
  z.write(path,Path('agent-promo-source')/path.relative_to(ROOT))
 z.write(ROOT/'scripts/promo/README.md','agent-promo-source/README.md')
with ZipFile(output) as z:
 assert z.testzip() is None,'Corrupt archive'
 print(f'{len(z.namelist())} files; {output.stat().st_size/1024/1024:.2f} MiB; ZIP integrity passed')
