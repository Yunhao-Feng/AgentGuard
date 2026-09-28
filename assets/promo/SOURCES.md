# From Agent Risks to Adaptive Defenses — source ledger

Created for Yunhao Feng and collaborators, September 28, 2026.

## What the film is

A 90-second English research overview combining animations, original paper figures, and published experimental results. It contains original procedural music, English on-screen captions, and no narration. The opening and policy examples are **reconstructions**, not recordings of live model inference. The five projects are complementary research contributions, not presented as one integrated deployment.

## Evidence and transformations

| Segment | Supplied source | Exact evidence | Presentation |
|---|---|---|---|
| 00:00–00:08 | AgentHazard, `2604.02947v2.pdf` | Figure 1, PDF p. 2 | Simplified animated sequence; no operational attack commands |
| 00:08–00:21 | AgentHazard, same PDF | Abstract, Section 3; Figure 2, PDF p. 4 | 2,653 instances; 10 risk categories; 10 attack strategies; original pipeline crop |
| 00:21–00:34 | VERA, `2607.01793v2.pdf` | Abstract; Figure 1, PDF p. 3 | 1,600 VERA-Bench cases; 124 risk categories; original method crop |
| 00:34–00:47 | BraveGuard, `2606.01166v2.pdf` | Figure 2, PDF p. 4; Table 1, PDF p. 7 | 38.79% vs 82.38% accuracy, **model-group averages**, GPT-5.5 / OpenClaw 3.11, AgentHazard-Strongest |
| 00:47–01:04 | HazardAuditor, `379_HazardAuditor_From_Executa.pdf` | Figure 1, PDF p. 2; Table 1, PDF p. 8 | CUA-EXEC paired model comparison across four frameworks |
| 01:04–01:21 | AdaGuard, `AdaGuard__Arxiv_.pdf` | Figure 1, PDF p. 2; Table 1, PDF p. 7 | Policy-counterfactual reconstruction; AdaGuard-4B 89.30% accuracy on 1,000 AdaptiveSafety test examples |
| 01:21–01:30 | Project resources below | Verified resource identities | Papers, code, datasets, and released weights |

Figures are cropped from the original PDFs at 3× PDF-point resolution and scaled to fit their display areas. No scientific content has been recolored, erased, or retouched. The source PDFs are preserved. Exact crop coordinates and PDF SHA-256 hashes are recorded in `sources.json`.

Charts use published point estimates on linear axes starting at 0 and ending at 100. No runs have been performed for this film. No uncertainty intervals are invented. Visual reveal/counting transitions are animation, not time-series measurements. Derived gains are arithmetic percentage-point differences.

### CUA-EXEC comparison

Each framework subset contains 100 safe and 100 unsafe trajectories. Metric: Accuracy (%). Baseline: **BraveGuard-Qwen3-Guard-8B**, not an average over BraveGuard variants.

| Framework | BraveGuard-Qwen3-Guard-8B | HazardAuditor | Difference (pp) |
|---|---:|---:|---:|
| Claude Code | 81.50 | 94.00 | 12.50 |
| Codex | 91.50 | 95.50 | 4.00 |
| Hermes | 77.00 | 86.50 | 9.50 |
| OpenClaw | 71.00 | 87.50 | 16.50 |

This is a selected accuracy endpoint, not a claim of dominance on every benchmark or metric. HazardAuditor Table 2 shows that BraveGuard retains higher recall and F1 in the GPT-5.5 setting. AdaGuard's policy-conditioned results are kept separate from this trajectory-classification comparison. No universal improvement claim is made for SafePO.

## Resource register

Verified September 28, 2026. Resource availability can change after this date.

- AgentHazard: [paper](https://arxiv.org/abs/2604.02947), [project](https://yunhao-feng.github.io/AgentHazard/), [code](https://github.com/Yunhao-Feng/AgentHazard), [Hugging Face dataset](https://huggingface.co/datasets/Yunhao-Feng/AgentHazard).
- VERA: [paper](https://arxiv.org/abs/2607.01793), [code](https://github.com/Yunhao-Feng/Vera), [VERA-Bench](https://github.com/Yunhao-Feng/Vera/tree/main/evaluation_bench).
- BraveGuard: [paper](https://arxiv.org/abs/2606.01166), [code](https://github.com/Yunhao-Feng/BraveGuard), [model collection](https://huggingface.co/Yunhao-Feng/BraveGuard). Checkpoints are in subfolders; consult the actual model files before inference.
- HazardAuditor: [arXiv](https://arxiv.org/abs/2609.15134), [project](https://yunhao-feng.github.io/HazardAuditor/), [code](https://github.com/Yunhao-Feng/HazardAuditor), [weights](https://huggingface.co/Yunhao-Feng/HazardAuditor). Film numbers refer to the supplied manuscript; public bibliographic metadata follows the project page.
- AdaGuard: [code](https://github.com/Yunhao-Feng/AdaGuard). The source release does not distribute the original dataset or trained weights. Local paper metadata is used; no arXiv identifier is invented.

Website colors reference [HazardArena](https://hazardarena-team.github.io/): white/light gray, dark text, and #2563eb blue, with a navy dark theme. This is visual inspiration, not a claim of partnership.

## Music and fonts

The score is synthesized from sine-wave chords, pulses, and short transition tones by the supplied Python code. It uses no external audio recordings or samples. The original PCM score is in `original-score.wav`; the video includes an AAC version normalized to a target of -20 LUFS with a -2 dBTP ceiling. No human or cloned voice is used.

The renderer defaults to Matplotlib's DejaVu Sans / DejaVu Sans Bold and supports explicit font files through command-line flags. The website uses platform fonts and loads no third-party font service.
