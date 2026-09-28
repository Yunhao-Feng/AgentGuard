# Website maintenance

The public research landing page is [README.md](../README.md); its Chinese counterpart is [README.zh-CN.md](../README.zh-CN.md).

## Local preview

```bash
python3 scripts/serve.py
```

Open http://localhost:4173. The server supports byte-range requests for video seeking. The website is static HTML/CSS/JavaScript, with no build step or backend.

## Publish with GitHub Pages

1. In `Yunhao-Feng/AgentGuard` → **Settings → Pages → Build and deployment**, choose **GitHub Actions**.
2. Commit and push changes to `main`.
3. Check **Actions → Deploy research website to GitHub Pages** for deployment status.

The workflow lives in `.github/workflows/pages.yml`. It copies the public pages, style sheets, scripts, paper PDFs, and assets into `_site`. Preview tooling, the rendering environment, and QA intermediates are excluded. Public URL: https://yunhao-feng.github.io/AgentGuard/.

## Edit the site

| File | Purpose |
| --- | --- |
| `index.html` | Homepage sections, research map, video, policy case |
| `site-content.js` | English/Chinese homepage copy, paper links and citations |
| `app.js` | Homepage interactions, translation, theme and resource lists |
| `style.css` | Shared responsive identity and homepage styling |
| `metrics.html`, `metrics.css`, `metrics.js` | Bilingual metrics explorer |
| `assets/data/metrics.json` | Table data, settings, PDF pages and SHA-256 hashes |
| `scripts/build_metrics.py` | Re-extract selected tables from the supplied PDFs |
| `scripts/promo/teaser.json` | 15-second video's text, timeline and evidence |
| `scripts/generate_teaser.py` | CPU-only rendering and original music synthesis |

Keep both languages in sync. Language and theme preferences persist locally and carry across both pages. Publication model names, dataset names and the English video remain in their original language.

Rebuild numerical data with `python scripts/build_metrics.py` in an environment with PyMuPDF installed. Review changed table rows and source page numbers before committing. Headline data for homepage cards also lives in `scripts/promo/storyboard.json` and `assets/promo/results.js` from the original film. Keep matching values consistent when updating paper versions.

## Assets

The main video is `assets/teaser/agentguard-15s.mp4`; the 90-second film remains in `assets/promo/` as an archival artifact. The original 24-second concept generator is also retained. The main site and README promote only the new 15-second video.

DM Sans is self-hosted in `assets/fonts/` with its SIL Open Font License. No third-party font request, analytics, or runtime framework is required.
