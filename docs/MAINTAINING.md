# Website maintenance

## Preview and publish

```bash
python3 scripts/serve.py
```

Open http://localhost:4173. There is no frontend build step or backend. The preview server supports video byte ranges.

For GitHub Pages, choose **Settings → Pages → Source → GitHub Actions**, then push changes to `main`. The workflow runs `python3 scripts/build_site.py`, packages an explicit list of public pages/assets, and deploys `_site`.

## Edit

- `index.html`, `site-content.js`, `app.js`: bilingual homepage, resources, citations and policy case.
- `metrics.html`, `metrics.js`, `metrics.css`: metrics explorer.
- `jev.html`, `jev.js`, `jev.css`: Jev comparison and interpretation.
- `style.css`: shared responsive identity.
- `assets/data/metrics.json`: curated data, public research URLs and evaluation settings.
- `assets/promo/results.js`: homepage headline values; keep consistent with the full dataset.
- `scripts/build_metrics.py`: validate data and regenerate the browser bundle.
- `scripts/generate_methods.py`: draw the bilingual method diagrams.
- `scripts/generate_teaser.py`, `scripts/promo/teaser.json`: generate and edit the 15-second film.

Keep English and Chinese copy synchronized. Language and theme settings are shared across all three pages.

## Public asset policy

Keep source documents outside the public repository. Numerical data, original diagrams and public research links are sufficient to render the site. Do not add document screenshots, document fingerprints or private filenames to metadata. The build rejects document attachments, recursively checks ZIP members, and uses a file/directory allowlist. The source ZIP contains only the film renderer, its configuration, the font/license, documentation and the public source manifest.

Test the actual publication bundle locally with:

```bash
python3 scripts/build_site.py
python3 scripts/serve.py --directory _site --port 4174
```
