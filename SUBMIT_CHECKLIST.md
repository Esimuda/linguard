# Linguard (was PidginGuard) — Lexsi submit checklist
Updated 1 Nov 2026 WAT · Official: https://hackathon.lexsi.ai/ · Build Nov 1–14 · **Submit by EOD Nov 14** · Registration closes Nov 5 · Shortlist Nov 16 · Demo Day Nov 22

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

## Still to do
- [ ] Claim HF credits → GPU run: SafeTune SafeGrad/LoRA on CuratorKIT set (fix 40% over-refusal) — `docs/GPU_PATH.md`
- [ ] CircuitKIT: register refusal task + `discover` on GPU; feed layers into SafeTune (4th kit live)
- [ ] Grow calibration + seed sets (target 100+/class) and re-run; optional LLM-judge (AuditKIT GuardJudge)
- [ ] Re-record demo video with the Linguard name + live before/after (old video shows offline harness)
- [ ] Optional: rename GitHub repo to `linguard` (needs owner OK)
- [ ] Submit via official form on hackathon.lexsi.ai (needs owner OK)

## Submit payload (draft)
- Project: **Linguard — guarding language**
- Track: AI Red Teaming / Safety & Alignment (Track 2 kits: AuditKIT, CuratorKIT, SafeTune; CircuitKIT wired)
- Repo: https://github.com/Esimuda/pidginguard
- Demo: https://huggingface.co/spaces/Esimuda/linguard
- Dataset: https://huggingface.co/datasets/Esimuda/linguard-safety · Vectors: https://huggingface.co/Esimuda/linguard-caa-vectors
- One-liner: Tiny Aya refuses scams in English but helps with them in Hausa/Igbo. Linguard red-teams 5 Nigerian languages, curates repair data with CuratorKIT, hardens with SafeTune, and audits with AuditKIT: ASR 37.5% → 4.2% (over-refusal 0% → 40%, the next fix).
- Note: rules say projects must be built during the hackathon — pre-Nov-1 commits are scaffolding; all model work is dated 1 Nov 2026+.
