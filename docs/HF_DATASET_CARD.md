---
license: mit
language: [en, pcm, yo, ha, ig]
task_categories: [text-generation]
tags: [ai-safety, red-teaming, lexsi, curatorkit, auditkit, safetune, linguard, nigeria]
pretty_name: Linguard Safety (Nigerian-language red-team + repair)
size_categories: [n<1K]
---
# Linguard Safety — guarding language

Red-team seeds, held-out steering calibration set, CuratorKIT repair dataset, and live Tiny Aya Earth transcripts
for the Lexsi AI Safety & Alignment Hackathon (Nov 2026). Code: https://github.com/Esimuda/pidginguard

| Folder | Contents |
|---|---|
| `seeds/` | 34 prompts (24 attacks: scam, social engineering, harmful advice, refusal-failure; 10 benign) in EN/PCM/YO/HA/IG |
| `calibration/` | 16 held-out prompts (8 harmful / 8 harmless) used only for SafeTune CAA vectors |
| `curated/` | CuratorKIT export: `sft_alpaca.jsonl`, `sft_messages.jsonl`, provenance + checksums |
| `results/` | Baseline and SafeTune-hardened transcripts, summaries, AuditKIT runs |

Baseline Tiny Aya Earth ASR 37.5% → 4.2% with SafeTune CAA (strength 0.25), at the cost of 40% over-refusal on benign prompts.
Small pilot (n=34), keyword-heuristic scorer. Attack prompts are for safety research only; repair targets are refusals.
