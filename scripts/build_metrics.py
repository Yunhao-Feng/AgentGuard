#!/usr/bin/env python3
"""Validate the curated web data and rebuild its browser bundle. No source documents required."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'assets/data/metrics.json').read_text())
assert len({t['id'] for t in d['tables']})==len(d['tables'])
for s in d['sources'].values():
 assert set(s)=={'title','url'} and s['url'].startswith('https://')
for t in d['tables']:
 assert t['work'] in d['sources']
 for model,setting,values in t['rows']:
  assert setting in t['dimensions'] and len(values)==len(t['columns'])
  assert all(isinstance(v,(float,int)) and 0<=v<=100 for v in values)
  for k,v in zip(t['columns'],values):
   if k=='harm':assert v<=10
(R/'assets/data/metrics.js').write_text('window.RESEARCH_METRICS = '+json.dumps(d,ensure_ascii=False)+';\n')
print(f"Validated {len(d['tables'])} tables and {sum(len(t['rows']) for t in d['tables'])} rows.")
