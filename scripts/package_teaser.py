#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json
R=Path(__file__).resolve().parents[1];c=json.loads((R/'scripts/promo/teaser.json').read_text())
paths=['scripts/generate_teaser.py','scripts/package_teaser.py','scripts/promo/teaser.json','scripts/promo/teaser-requirements.txt','assets/fonts/DM-Sans.ttf','assets/fonts/OFL.txt','docs/VIDEO.md','assets/teaser/sources.json']+sorted({s['pdf'] for s in c['evidence'].values()})
with ZipFile(R/'assets/teaser/teaser-source.zip','w',ZIP_DEFLATED) as z:
 for path in paths:z.write(R/path,'agentguard-teaser/'+path)
 z.writestr('agentguard-teaser/README.md','# AgentGuard film source\n\nSee docs/VIDEO.md for installation, rendering and editing instructions.\n')
with ZipFile(R/'assets/teaser/teaser-source.zip') as z:assert z.testzip() is None
print('Source archive verified.')
