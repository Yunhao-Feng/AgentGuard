# Yunhao Feng · Agent Safety Research

A static research website for GitHub Pages, with English/Chinese language switching, light/dark themes, a 90-second English research film, original paper figures, evidence-bounded comparisons, and a policy playground.

## Preview

```bash
python3 scripts/serve.py
```

Open http://localhost:4173. The included preview server supports HTTP byte ranges so video seeking and chapter navigation work locally. No JavaScript package installation or build is needed. English and light mode are the first-visit defaults. Language and theme selections are stored locally when browser storage is available. The site works without third-party fonts or scripts.

## Research film

- Watch: `assets/promo/agent-safety-film.mp4`
- Source: `scripts/generate_promo.py`
- Editable data/timeline: `scripts/promo/storyboard.json`
- Full build instructions: [scripts/promo/README.md](scripts/promo/README.md)
- Evidence and links: [assets/promo/SOURCES.md](assets/promo/SOURCES.md)

1920×1080, 30 fps, 90 seconds. English burned-in captions, original procedural music, no narration. Results are from the supplied papers. Animated examples are clearly marked reconstructions, not live inference. No A100 server or model execution is used.

The complete downloadable reproduction package is `assets/promo/promo-source.zip`. The previous 24-second concept video and `scripts/generate_demo.py` are preserved separately.

## Website editing

- `index.html`: semantic page structure, video player and dialogs.
- `site-content.js`: complete English/Chinese copy, project resource links and BibTeX citations.
- `app.js`: language/theme controls, interactive policy case, evidence table, chapters and dialogs.
- `style.css`: responsive design and HazardArena-inspired white/gray/blue theme.
- `assets/promo/results.js`: generated from the film's source data; regenerate with the video script after changing numerical results.

Paper figures can be opened at full size with keyboard-accessible dialogs. Experimental charts have exact-value tables and source files. Film chapter buttons seek to the corresponding research contribution. Both project and community resources link to their actual published locations; unavailable AdaGuard weights are not represented as downloadable models.

## GitHub Pages (prepared, not published)

1. Push this directory to the `main` branch of your chosen GitHub repository.
2. In Settings → Pages → Build and deployment, select **GitHub Actions**.
3. Run the included Pages workflow, or push an update.

The workflow copies only public website files, assets and the five paper PDFs. Relative paths support both root domains and `/repository/` project deployments. The rendering environment, QA files and intermediate scripts are not deployed except for the intentional downloadable source ZIP. No repository has been configured or uploaded by this task.

## Evidence boundaries

AgentHazard and VERA statistics, BraveGuard group means, HazardAuditor CUA-EXEC accuracy and AdaGuard AdaptiveSafety results retain their original settings. The CUA-EXEC chart compares methods within one table, not across unrelated papers or datasets. The page includes the accuracy-vs-recall/F1 caveat. HazardAuditor bibliographic links now point to its public September 2026 release; numerical evidence still identifies the supplied PDF version. See the source ledger for details.
