# Delivery validation — 2026-09-28

## Current scope

The homepage, metrics explorer and Jev comparison page are static, bilingual pages. Numerical results are rendered as native tables and charts. Ten original English/Chinese SVGs illustrate the five research methods. No source documents or original paper screenshots are included in the current website or downloadable source archive.

## Browser and data checks

- Chrome: three pages × English/Chinese × light/dark × widths 320, 390, 768, 1024 and 1440 pixels. All 60 layouts passed document overflow, translation-key and source-link checks.
- The Jev page passed all 44 combinations of task, setting and chart metric against the curated data. The comparison keeps task settings separate and explains differing interfaces and inference budgets.
- Headline accuracy differences are calculated from the data: AdaGuard-8B leads by 7.10 percentage points on AdaptiveSafety; Jev leads by 6.81 points on DynaBench.
- Nine data tables contain 287 setting-specific rows. Table dimensions, unique identifiers, metric ranges and row shapes pass the data validator. All 77 combinations of setting and chart metric in the full metrics explorer also match the data.
- Jev CSV export, five bilingual method dialogs, language/theme persistence and browser playback to the film ending passed. No JavaScript errors or failed HTTP responses were observed.
- Desktop and mobile Jev screenshots were inspected in light and dark themes. Charts start at zero and retain a 100% maximum. Wider tables scroll within their containers on mobile.
- Local HTML and README file links resolve. Public research URLs replace local document links.

## Media and source archive

The retained 15-second film uses code-rendered text and graphics, with original procedural music. Its previously verified format is H.264, 1920 × 1080, 30 fps, 450 frames, and AAC stereo at 48 kHz. The video itself is unchanged in this revision and contains no paper screenshots.

The rebuilt source ZIP contains the renderer, configuration, font and attribution, with public research links and numerical evidence. An independent extraction and preview rebuild passed without research documents. Archive integrity and nested member checks passed.

## Publication checks

`scripts/build_site.py` packages an explicit list of 52 public assets. It checks every selected file and recursively inspects ZIP members. Synthetic tests confirmed rejection of document filenames, disguised document content, private review metadata and documents nested in archives.

The current working files, publication artifact and source ZIP were scanned for source attachments and private manuscript identifiers. Old document files, original paper screenshots and the legacy video package containing them were removed from the current tree. Original documents are not needed to rebuild the website or current film.

Git history remains unchanged at the user's request. No remote push or online deployment was performed in this revision. Deletions and replacements take effect online after the updated commit is pushed and the Pages workflow succeeds.
