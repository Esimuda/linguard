# Schedule — Nov 1–14 2026 (Africa/Lagos · WAT)

Official build window: **Nov 1–14** (submit by end of Nov 14). Demo Day Nov 22 for shortlisted teams.  
Hard personal push: **visible early package before Nov 3 WAT**.

| Date (WAT) | Milestone |
|------------|-----------|
| Oct 31 | Kickoff talk; publish Linguard early package (this repo) |
| Nov 1 | Install Lexsi kits; accept Tiny Aya Hub licence; first live baseline |
| Nov 2–3 | Expand seeds; CuratorKIT dry-run → first curated export; HF dataset draft |
| Nov 4–5 | SafeTune harden v0 on `tiny-aya-earth`; log train provenance |
| Nov 6–7 | CircuitKIT safety-oriented discover; feed scores into SafeTune if applicable |
| Nov 8–9 | AuditKIT before/after table; abliteration / BoN stress tests |
| Nov 10–11 | Fix regressions (over-refusal); multilingual qualitative review |
| Nov 12 | Hub push: dataset + adapter + eval logs; polish README metrics |
| Nov 13 | Demo recording (harness + metrics); dry-run submission checklist |
| Nov 14 | **Submit** (do not claim done before this window) |

## Risks

- Gated Tiny Aya access delay → keep `echo`/`fixture` path green; document HF wait  
- GPU scarcity → prefer SafeTune inference-time steer / small LoRA; CircuitKIT CPU quickstarts where possible  
- Kit API drift post-kickoff → adapters isolated under `adapters/`; pin versions when announced  
