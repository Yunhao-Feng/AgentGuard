# Delivery validation — 2026-09-28

## Scope

AgentGuard Team homepage, independent metrics page, English/Chinese README, seven supplied Hugging Face resources, a 15-second promotional film, reusable rendering source and GitHub Pages packaging. The site remains static, with no model server or new GPU experiment.

## Browser and content checks

- Chrome: both pages × English/Chinese × light/dark × widths 320, 390, 768, 1024 and 1440 pixels. No document-level horizontal overflow in 40 layouts.
- All 49 combinations of table, evaluation setting and visualized metric checked against the source data. Six table views contain 185 setting-specific rows. All bars use zero baselines; percentage axes end at 100 and harmfulness at 10.
- Language/theme persistence, cross-page navigation, study deep links, search, empty results, CSV download, policy switching, figure dialogs and citation dialogs checked.
- All five original method figures decode successfully. Scientific content remains unchanged. English and Chinese README layouts rendered and inspected.
- All seven supplied Hugging Face URLs, the five code repositories, four arXiv links and existing project pages returned HTTP 200. OWASP's foundation project page is used for its community link.
- Every local page and README link resolves to a file; PDF source hashes and the video hash match their manifests.
- Reduced-motion preference pauses the animated homepage research map.

## Film checks

- H.264 video, 1920 × 1080, 30 fps, exactly 450 frames and 15.000 seconds; AAC stereo, 48 kHz.
- Scene start/middle/end frames inspected across all four scenes; subtitle timing covers the complete film.
- Full encoded video decoded by FFmpeg without errors. Browser playback through the ending and chapter seeking checked.
- Original music has no full-scale clipping; encoded peak measured at approximately −5.9 dBFS. Audio fades in and out.
- Downloadable source ZIP passed archive integrity and an independent extracted preview rebuild with the bundled font and source PDFs.

## Deployment boundary

`.github/workflows/pages.yml` packages both pages, scripts, styles, PDFs and assets. A local copy of that artifact is tested under a project subdirectory, including video byte-range responses. No remote push or online deployment was performed in this round. The intended public site URL will become available after GitHub Pages is enabled and the updated repository is pushed.
