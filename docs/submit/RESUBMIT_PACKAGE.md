# Linguard resubmit package (draft)

Latest Lexsi submission counts. Use this for a clean re-submit before Nov 14 AoE.

## Form answers (fill on https://hackathon.lexsi.ai/submission/)

- Registered email: babalolabowale01@gmail.com (registration ticket #27J8-ENVZ-WV7M)
- Abstract: paste `docs/submit/ABSTRACT.md` (human paragraphs; under 500 words)
- Discord username: esimuda
- Tracks: Track 2a + Track 2b (and matching problem statements: multilingual/code-mixed safety; adversarial/safety eval set; inference-time safety steering; repairing safety drift / locating safety)
- Repos used: CuratorKIT, SafeTune, CircuitKIT, AuditKIT
- Models used: Tiny Aya Earth (primary)
- GitHub: https://github.com/Esimuda/pidginguard
- Demo / public link: https://huggingface.co/spaces/Esimuda/linguard
- Dataset: https://huggingface.co/datasets/Esimuda/linguard-safety
- Model/vectors: https://huggingface.co/Esimuda/linguard-caa-vectors
- Write-up: GitHub README (HF Article still missing)

## Still create before ideal resubmit

1. Public HF **model collection** including `Esimuda/linguard-caa-vectors` (+ future LoRA adapter)
2. Public HF **dataset collection** including `Esimuda/linguard-safety`
   - Current write token `Linguard-Lexsi-2026-11` is fine-grained and **cannot create collections** (API 403). Need a token with collection write, or create collections in the HF UI while signed in as Esimuda.
3. Optional HF Article summarizing metrics + pipeline
4. GPU SafeGrad/LoRA adapter pushed to Hub, then added to model collection
5. Re-recorded Linguard-named demo video (not a form field; useful for Demo Day / README)

## Confirmed: no dedicated demo-video field

Tally form `o9E0Ve` HTML has VIDEO block count 0 and FILE_UPLOAD 0.
