# Delivery validation — September 28, 2026

## Film

- 90.000 seconds; 2,700 frames; 1920×1080; 30 fps.
- H.264 / yuv420p video; stereo AAC at 48 kHz; fast-start MP4.
- Entire encoded video decoded without FFmpeg errors.
- Start, midpoint and final frames of all seven chapters inspected from the encoded MP4 (21 frames), in addition to renderer previews.
- Integrated music loudness measured at approximately -19.9 LUFS; true peak approximately -8.5 dBFS. No clipping detected. Original soundtrack is 48 kHz PCM and contains no narration.
- Chart endpoint values checked against the supplied paper tables. Bars start at zero; no uncertainty intervals fabricated. Source ledger records benchmark settings and model-group versus paired comparisons.
- English captions span 00:00–01:30 without gaps. Captions are burned in; optional VTT and SRT files match the chapter timeline.

## Website

- English/light first-visit defaults; English/Chinese and light/dark preference persistence checked.
- Layout checked at 320, 360, 390, 768, 1024 and 1440 px in both languages; no document-level horizontal overflow. The exact-data table has intentional local scrolling on small screens.
- Policy decisions switch correctly in both languages. Language changes preserve the selected policy.
- All five paper-figure dialogs and all five citation dialogs open and close; keyboard activation, Escape dismissal and focus restoration checked.
- Reduced-motion preference pauses the SVG animation on initial load and when the preference changes.
- Browser storage failures are handled; language and theme still work within the current page.
- Local paper, video, subtitle, chart, transcript, provenance and source-package downloads resolve.
- Video playback and chapter seeking work through the included range-capable preview server.
- An equivalent deployment artifact was tested under `/research/`; assets and chapter seeking work with a GitHub Pages-style project prefix.
- No application JavaScript errors or failed static resource responses found during final interaction checks.

## Resources and reproduction

- 26 distinct external resource links inspected from the rendered website. 25 returned HTTP 200 to direct requests. The OWASP GenAI site blocks the automated request with HTTP 403; its official page is retained rather than treated as a nonexistent resource.
- ZIP archive integrity verified. Source package extracted to an independent temporary directory and successfully regenerated figures, captions, poster, static chart and QA previews.
- The original five PDFs and 24-second generator remain unchanged.
- No server experiment, model inference, repository upload or online deployment performed.
