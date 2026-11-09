# Linguard: guarding language across Nigerian multilingual prompts

**Lexsi AI Safety & Alignment Hackathon · Tracks 2a + 2b · Solo · Ticket `#27J8-ENVZ-WV7M`**

Small multilingual models can refuse a scam in English and still help with the same intent in Hausa, Igbo, Yoruba, or Nigerian Pidgin. Linguard red-teams that gap on [CohereLabs/tiny-aya-earth](https://huggingface.co/CohereLabs/tiny-aya-earth), curates repair data, hardens it with SafeTune steering and a LoRA adapter, and proves the change with AuditKIT.

## Pipeline

1. **Seeds** — EN · PCM · YO · HA · IG scam / social-eng / harmful / jailbreak / benign controls  
2. **AuditKIT** — live baseline + before/after compare  
3. **CuratorKIT** — gated repair export → [`Esimuda/linguard-safety`](https://huggingface.co/datasets/Esimuda/linguard-safety)  
4. **SafeTune** — CAA steering vectors → [`Esimuda/linguard-caa-vectors`](https://huggingface.co/Esimuda/linguard-caa-vectors)  
5. **LoRA harden** — weight-level fix on GPU → [`Esimuda/linguard-tiny-aya-earth-lora`](https://huggingface.co/Esimuda/linguard-tiny-aya-earth-lora)  
6. **CircuitKIT** — EAP-IG `discover` on the `linguard_refusal` task → [`Esimuda/linguard-circuit`](https://huggingface.co/Esimuda/linguard-circuit) (exploratory, not evaluated)  

## GPU results (9 Nov 2026, 120 held-out seeds)

76 attacks and 44 benign controls across EN · PCM · YO · HA · IG that no training step saw. Greedy decoding, same scorer for every run.

| Run | Attack success ↓ | Over-refusal ↓ | Accuracy |
|---|---|---|---|
| Baseline Tiny Aya Earth | 39.5% | 0% | 75.0% |
| SafeTune CAA 0.25 | 3.9% | 11.4% | 93.3% |
| **Linguard LoRA** | **1.3%** | **0%** | **99.2%** |

AuditKIT `linguard_attack_success`: **0.2500 → 0.0083 (−96.7% rel)** for the LoRA adapter.

Steering stopped most attacks, but it also refused ordinary questions, up to 30% of Pidgin controls. The LoRA adapter keeps attack success low and answers every benign control. It learned refusals in each language from a held-out calibration set and the CuratorKIT repair data. Its helpful answers are the base model's own answers, so it did not learn to refuse everything.

Hausa attack success went from 53.3% to 0%, Yoruba from 66.7% to 6.7%, and Igbo from 46.7% to 0%.

Limits: the judge is a keyword heuristic, the sample is small, and one person wrote the prompts. The one remaining "attack success" is a Yoruba refusal with tone marks that the scorer misses.

## CPU pilot (1 Nov 2026, n=34)

| Run | ASR ↓ | Over-refusal ↓ | Accuracy |
|---|---|---|---|
| Baseline | 37.5% | 0% | 73.5% |
| CAA 0.25 | 4.2% | 40% | 85.3% |

## Links

- Code: [github.com/Esimuda/linguard](https://github.com/Esimuda/linguard)  
- Demo Space: [Esimuda/linguard](https://huggingface.co/spaces/Esimuda/linguard)  
- LoRA adapter: [Esimuda/linguard-tiny-aya-earth-lora](https://huggingface.co/Esimuda/linguard-tiny-aya-earth-lora)  
- Dataset: [Esimuda/linguard-safety](https://huggingface.co/datasets/Esimuda/linguard-safety)  
- Abstract (paste-ready): `docs/submit/ABSTRACT.md` in the repo  

Builder: **Olabowale Babalola** ([@Esimuda](https://huggingface.co/Esimuda)).

*Paste this markdown into a new Hugging Face Article on your profile when ready; then put the article URL in the Lexsi form “Hugging Face article” field.*
