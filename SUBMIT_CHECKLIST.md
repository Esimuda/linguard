# Linguard (was PidginGuard) — Lexsi submit checklist
Updated 3 Nov 2026 WAT · Official: https://hackathon.lexsi.ai/ · Build Nov 1–14 · **Submit by EOD Nov 14** · Registration closes Nov 5 · Shortlist Nov 16 · Demo Day Nov 22

## Done
- [x] Team registered (ticket `#27J8-ENVZ-WV7M`)
- [x] Lexsi Discord joined (user confirmed 1 Nov) — still claim the $20 HF credits in `#hackathon-lexsi`
- [x] HF account `Esimuda`, write token on box (not in repo)
- [x] CohereLabs/tiny-aya-earth licence accepted; weights downloaded
- [x] Real Lexsi kits installed: auditkit 1.1.3, curatorkit 0.1.22, safetune 0.1.10, circuitkit 0.2.0
- [x] Live baseline on Tiny Aya Earth (34 seeds × 5 languages) + AuditKIT evaluate
- [x] CuratorKIT repair dataset (34/34 passed gates) → HF dataset `Esimuda/linguard-safety`
- [x] SafeTune CAA harden (CPU) at strength 0.25 / 0.4 + AuditKIT compare
- [x] Before/after table in README (real numbers)
- [x] HF Space `Esimuda/linguard` (static demo page)
- [x] Renamed user-facing brand to Linguard
- [x] Submitted once (3 Nov) — confirmation email received; latest submission counts
- [x] Human-paragraph abstract drafted at `docs/submit/ABSTRACT.md` (228 words)
- [x] Seed set grown locally 34 → 74; calibration 16 → 32 (`data/seeds`, `data/calibration`) — Hub + re-eval still pending

## Still to do (ranked for judges)
1. [ ] **HF model + dataset collections** (form requires both; currently none on Esimuda). Token `Linguard-Lexsi-2026-11` lacks collection.create (API 403) — create in HF UI or mint token with collection write.
2. [ ] **Claim HF credits → GPU SafeGrad/LoRA** on CuratorKIT set to cut 40% over-refusal — `docs/GPU_PATH.md`; push `Esimuda/linguard-tiny-aya-earth-lora`
3. [ ] **CircuitKIT discover** on GPU (4th kit live) + feed layers into SafeTune
4. [ ] Push grown seeds/calibration to `Esimuda/linguard-safety` and re-run AuditKIT before/after (CPU possible but slow; GPU preferred)
5. [ ] Resubmit with paragraph abstract + collection URLs (`docs/submit/RESUBMIT_PACKAGE.md`)
6. [ ] Optional HF Article; re-record Linguard demo video (not a form field)
7. [ ] Optional: rename GitHub repo to `linguard` (needs owner OK)

## Submit payload (draft)
- Project: **Linguard — guarding language**
- Track: AI Red Teaming / Safety & Alignment (Track 2a+2b; kits: AuditKIT, CuratorKIT, SafeTune; CircuitKIT wired)
- Repo: https://github.com/Esimuda/pidginguard
- Demo: https://huggingface.co/spaces/Esimuda/linguard
- Dataset: https://huggingface.co/datasets/Esimuda/linguard-safety · Vectors: https://huggingface.co/Esimuda/linguard-caa-vectors
- Abstract: `docs/submit/ABSTRACT.md`
- One-liner: Tiny Aya refuses scams in English but helps with them in Hausa/Igbo. Linguard red-teams 5 Nigerian languages, curates repair data with CuratorKIT, hardens with SafeTune, and audits with AuditKIT: ASR 37.5% → 4.2% (over-refusal 0% → 40%, the next fix).
