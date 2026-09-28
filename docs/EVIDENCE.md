# Evidence and comparison settings

All metrics are drawn from the five supplied paper PDFs. `assets/data/metrics.json` records their filenames and SHA-256 hashes, the source table/page for each view, metric labels, evaluation settings and exact values. `scripts/build_metrics.py` extracts decimal table rows and checks the expected row counts. VERA's Table IV and dataset statistics are transcribed explicitly in that script.

| View | Source | What is measured |
| --- | --- | --- |
| AgentHazard | Table 2, PDF p. 6 | Attack success (%) and harmfulness (0–10); full trajectories judged by an LLM |
| VERA | Table IV, PDF p. 8 | Execution success by agent framework and execution mode |
| BraveGuard | Table 1, PDF p. 7 | Accuracy, recall and F1 on AgentHazard-Strongest, with four OpenClaw 3.11 backends |
| HazardAuditor | Table 1, PDF p. 8 | Accuracy and macro metrics on balanced CUA-EXEC across four frameworks |
| AdaGuard binary | Table 1, PDF p. 7 | Accuracy, precision, recall and F1 on AdaptiveSafety and DynaBench |
| AdaGuard rules | Table 2, PDF p. 8 | Exact rule-set accuracy and rule-level micro-F1 |

The statistics cards cite AgentHazard Table 1 (p. 6), VERA § V (pp. 6–7), BraveGuard Table 4 (p. 13), HazardAuditor Table 1 (p. 8), and the AdaGuard abstract. The 800 CUA-EXEC total is derived transparently as four framework subsets × 200 trajectories. Dataset counts describe distinct artifacts and are not summed.

BraveGuard model-group means are labeled as averages. They compare different model groups, rather than a paired single-model change. AdaGuard's binary and rule-level outcomes are separate views. Higher attack-mode ESR in VERA means more harmful outcomes verified; higher benign ESR means more legitimate tasks completed. Neither is interchangeable with guard detection accuracy.

Bar lengths always start at zero. Harmfulness uses a 0–10 axis; percentage metrics use 0–100. The selected tables do not supply confidence intervals, so none are invented. Full table entries, including strong baselines and outcomes where our models do not lead, remain visible.

The overview film uses only AgentHazard and VERA size statistics; model performance belongs in the interactive metrics explorer where evaluation conditions remain readable.

Research links and all seven user-provided HF endpoints were checked on 2026-09-28. AgentImages contains execution environment images, while VERA's evaluation cases have a separate repository link. AdaGuard's three model entries point directly to their supplied HF pages.
