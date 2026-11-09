# Linguard: guarding language across Nigerian multilingual prompts

**Lexsi AI Safety & Alignment Hackathon · Tracks 2a + 2b · Solo · Ticket `#27J8-ENVZ-WV7M`**

Small multilingual models can refuse a scam in English and still help with the same intent in Hausa, Igbo, Yoruba, or Nigerian Pidgin. Linguard red-teams that gap on [CohereLabs/tiny-aya-earth](https://huggingface.co/CohereLabs/tiny-aya-earth), curates repair data, hardens with SafeTune, and proves the change with AuditKIT.

## Pipeline

1. **Seeds** — EN · PCM · YO · HA · IG scam / social-eng / harmful / jailbreak / benign controls  
2. **AuditKIT** — live baseline + before/after compare  
3. **CuratorKIT** — gated repair export → [`Esimuda/linguard-safety`](https://huggingface.co/datasets/Esimuda/linguard-safety)  
4. **SafeTune** — CAA steering vectors → [`Esimuda/linguard-caa-vectors`](https://huggingface.co/Esimuda/linguard-caa-vectors)  
5. **CircuitKIT** — `linguard_refusal` task registered; GPU `discover` next  

## Live metrics (CPU, 1 Nov 2026, n=34 pilot)

| Run | ASR ↓ | Over-refusal ↓ | Accuracy |
|---|---|---|---|
| Baseline | 37.5% | 0% | 73.5% |
| CAA 0.25 | **4.2%** | 40% | 85.3% |

AuditKIT `linguard_attack_success`: **0.2647 → 0.0294 (−88.9% rel)**.

The 40% over-refusal is the honest next problem — GPU SafeGrad/LoRA on the CuratorKIT set is meant to keep ASR low while restoring benign helpfulness.

## Links

- Code: [github.com/Esimuda/linguard](https://github.com/Esimuda/linguard)  
- Demo Space: [Esimuda/linguard](https://huggingface.co/spaces/Esimuda/linguard)  
- Abstract (paste-ready): `docs/submit/ABSTRACT.md` in the repo  

Builder: **Olabowale Babalola** ([@Esimuda](https://huggingface.co/Esimuda)).

*Paste this markdown into a new Hugging Face Article on your profile when ready; then put the article URL in the Lexsi form “Hugging Face article” field.*
