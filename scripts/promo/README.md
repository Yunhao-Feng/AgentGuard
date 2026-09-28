# Rebuild the 90-second research film

The film is generated locally with Python + Pillow + NumPy + PyMuPDF + Matplotlib + FFmpeg. No GPU, API key, paid service, cloud upload, or model checkpoint is required. Exact tested versions for Python 3.12 are listed in `requirements-tested.txt`; use that file instead of `requirements.txt` to match the delivered environment.

## Quick start (macOS / Linux / Windows)

1. Install Python 3.10+ and FFmpeg, with `ffmpeg` and `ffprobe` available on PATH.
2. From the project root:

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r scripts/promo/requirements.txt
python scripts/generate_promo.py --preview-only
python scripts/generate_promo.py
```

If FFmpeg is not on PATH, pass `--ffmpeg /absolute/path/to/ffmpeg` (or the path to ffmpeg.exe).

A successful run writes `assets/promo/agent-safety-film.mp4` at 1920×1080, 30 fps, 90 seconds, H.264 video + AAC music, with browser-compatible pixel format and fast-start metadata. The default font is Matplotlib's bundled DejaVu Sans, so there is no hard-coded macOS font dependency.

## Customize

Edit `scripts/promo/storyboard.json`:

- `scenes`: start/end times, chapter titles, subtitles and source labels. Keep times contiguous and update `duration` to match. Scene-specific animation phases are in the renderer.
- `results`: exact chart values, metric definitions and settings. The same data generates the site's `assets/promo/results.js`.
- `sources`: PDF names, 1-based figure pages, PDF-coordinate crop boxes, evidence descriptions and URLs.
- `author`: final credit.

Animation layout is intentionally authored for 1920×1080. To change resolution/aspect ratio, adapt the scene drawing functions; the script refuses an unsupported layout size instead of silently cropping text.

The five source PDFs must remain in the project root, directly above the `scripts/` directory. The downloadable source package includes the five supplied PDFs for reproducibility; the original paper authors retain their rights.

Optional overrides:

```bash
python scripts/generate_promo.py --config scripts/promo/storyboard.json \
  --font /path/to/regular.ttf --bold-font /path/to/bold.ttf \
  --output assets/promo
```

`--preview-only` regenerates figures, captions, provenance, chart exports, poster, and 21 QA frames but does not render video or music. After changes, inspect `.qa/promo/contact.jpg` and the full-sized scene frames before the complete render.

The old `scripts/generate_demo.py` remains unchanged and produces the separate 24-second silent concept animation.

## Outputs

- `agent-safety-film.mp4`: finished film, with burned-in English captions.
- `captions.en.srt` / `captions.en.vtt`: matching editable subtitle files. The website leaves optional subtitle tracks off by default to avoid duplicating the burned-in captions.
- `poster.jpg`: cover image.
- `original-score.wav`: original, uncompressed synthesized score.
- `transcript.en.txt`: chapter transcript and source references.
- `figures/`: unchanged crops of the supplied paper figures.
- `comparison.svg` / `comparison.png`: static 0–100% chart exported with Matplotlib.
- `sources.json`: source hashes, PDF crop coordinates, settings, data, render metadata and film hash.
- `SOURCES.md`: human-readable evidence and resource ledger.
- `.qa/promo/`: start/middle/end previews for each chapter.

Source PDFs are never modified. The film presents published results, not new experiments or recorded live inference. See SOURCES.md for comparison limits.
