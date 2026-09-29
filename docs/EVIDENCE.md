# Research evidence

The website renders curated numerical data and original conceptual diagrams. It does not distribute source document attachments or document metadata. Research provenance is expressed through work titles, public resource links, evaluation tables and experimental settings.

`assets/data/metrics.json` is the editable source of numerical results. Run `python3 scripts/build_metrics.py` to validate its schema and regenerate the browser bundle. New source values must be reviewed before inclusion; the script validates shape and ranges, not scientific correctness.

| View | Research source | Evaluation |
| --- | --- | --- |
| AgentHazard | AgentHazard, Table 2 | Attack success and harmfulness by framework and backend |
| VERA | VERA, Table IV | Execution success by framework and execution mode |
| BraveGuard | BraveGuard, Table 1 | Accuracy, recall and F1 on AgentHazard-Strongest |
| HazardAuditor | HazardAuditor, Table 1 | Accuracy and macro metrics on balanced CUA-EXEC |
| AdaGuard binary | AdaGuard, Table 1 | AdaptiveSafety and DynaBench binary outcomes |
| AdaGuard rules | AdaGuard, Table 2 | Exact rule-set accuracy and rule micro-F1 |
| AdaGuard API comparison | AdaGuard, Table A1 | API and local-model binary outcomes on the same examples |
| AdaGuard API rules | AdaGuard, Table A2 | Complete rule-set and micro-level outcomes |
| HazardAuditor transfer | HazardAuditor, Table 2 | AgentHazard outcomes by agent backend |

Public research links: [AgentHazard](https://arxiv.org/abs/2604.02947), [VERA](https://arxiv.org/abs/2607.01793), [BraveGuard](https://arxiv.org/abs/2606.01166), [HazardAuditor](https://arxiv.org/abs/2609.15134), [AdaGuard](https://arxiv.org/abs/2609.34241).

The statistics cards use AgentHazard Table 1, VERA's evaluation setup, BraveGuard Table 4, HazardAuditor Table 1, and the AdaGuard dataset description. CUA-EXEC's 800 total is derived as four subsets × 200 trajectories. Different datasets are not added together.

## Jev comparison

The comparison page selects Jev, HazardAuditor, BraveGuard and AdaGuard rows only where a shared evaluation reports them. No scores are joined across studies into a unified ranking.

CUA-EXEC contains 100 safe and 100 unsafe trajectories per framework. Its F1, recall and precision are macro-averaged. AgentHazard uses unsafe trajectories as the positive class and reports binary recall and F1.

AdaptiveSafety uses 1,000 test examples; DynaBench uses 543. Jev and AdaGuard see the same examples but use different interfaces and inference budgets. Jev's probability is evaluated separately for each rule, with a threshold of 0.5; its selected rule set is serialized in policy order. AdaGuard emits an explanation and ordered rule identifiers. Jev's evaluated identifier is `typesafe/jev-1.13-20260917`; its server-side context handling is unknown. Local AdaGuard uses greedy BF16 decoding, a 16,000-token prompt budget and 512-token output budget. Invalid outputs count as errors.

For rule identification, exact match requires the entire valid violation set. The micro metrics pool rule decisions as specified by the evaluation; failed predictions contribute an empty set to the micro counts and never count as exact. Binary detection and rule identification are distinct endpoints.

Jev leads AdaGuard-8B on DynaBench accuracy, binary F1, exact rule-set accuracy and rule micro-F1; on AdaptiveSafety Jev has higher binary recall while AdaGuard-8B has higher accuracy and F1. These trade-offs remain visible. No equal-budget latency, cost or compute claim is made. Product-level descriptions refer to [TypeSafe's own overview](https://typesafe.ai/), not third-party performance claims.

## Rendering

All bars start at zero. Percentage metrics use 0–100; harmfulness uses 0–10. No uncertainty intervals were supplied for these selected tables, so none are invented. The method diagrams are original conceptual redrawings created by `scripts/generate_methods.py`; they are not screenshots of documents.
