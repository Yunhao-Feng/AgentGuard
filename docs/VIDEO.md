# Reproduce the 15-second AgentGuard film

The current film is [agentguard-15s.mp4](../assets/teaser/agentguard-15s.mp4): 1920 × 1080, 30 fps, H.264/AAC, English text, original electronic music, no narration. It is an animated research overview, not a recording of model inference.

## Build

Python 3.10+ and FFmpeg must be installed. From the repository root:

```bash
python3 -m venv .venv-teaser
# macOS / Linux:
source .venv-teaser/bin/activate
# Windows PowerShell: .venv-teaser\Scripts\Activate.ps1
python -m pip install -r scripts/promo/teaser-requirements.txt
python scripts/generate_teaser.py
```

The bundled DM Sans font works across platforms. Override it with `--font /path/to/font.ttf` if needed. Use `--ffmpeg /path/to/ffmpeg` to specify the encoder path.

```bash
python scripts/generate_teaser.py --preview-only --output .qa/teaser-preview
```

Preview mode writes scene start/middle/end frames, the cover, storyboard and subtitle files. Use a separate output directory to preserve the completed video's source manifest.

## Edit

Modify `scripts/promo/teaser.json` to change text, card labels, statistics, source references and contiguous scene timings. The layout is authored for 1920 × 1080. Large copy changes should be checked in the preview frames before rendering the film.

| Time | Message |
| --- | --- |
| 0–3 s | Agents can act. Can we trust the outcome? |
| 3–7.5 s | AgentHazard measures risk; VERA verifies execution |
| 7.5–12 s | BraveGuard, HazardAuditor and AdaGuard: learn, audit, adapt |
| 12–15 s | Explore AgentGuard Team's open research |

The source manifest records the paper versions with SHA-256 hashes. Statistics are paper-reported; there is no new model evaluation. Music is synthesized from code without samples; the font license is included.

Outputs include MP4, poster, storyboard, English VTT/SRT subtitles, transcript, source manifest and original WAV. Run `python scripts/package_teaser.py` to create the downloadable source archive. The archive includes everything required for this renderer, including the two source PDFs used for on-screen statistics and the font license.
