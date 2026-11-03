# Linguard (was PidginGuard) — Lexsi submit checklist
Updated 3 Nov 2026 WAT · Official: https://hackathon.lexsi.ai/ · Build Nov 1–14 · **Submit by EOD Nov 14** · Registration closes Nov 5 · Shortlist Nov 16 · Demo Day Nov 22

## Done
- [x] Team registered (ticket `#27J8-ENVZ-WV7M`)
- [x] Lexsi Discord joined (user confirmed 1 Nov) — still claim the $20 HF credits in `#hackathon-lexsi`
- [x] HF account `Esimuda`, write token on box (not in repo)
- [x] CohereLabs/tiny-aya-earth licence accepted; weights downloaded
- [x] Real Lexsi kits installed: auditkit 1.1.3, curatorkit 0.1.22, safetune 0.1.10, circuitkit 0.2.0
- [x] Live baseline on Tiny Aya Earth (initial 34 seeds × 5 languages) + AuditKIT evaluate
- [x] CuratorKIT repair dataset (34/34 passed gates) → HF dataset `Esimuda/linguard-safety`
- [x] SafeTune CAA harden (CPU) at strength 0.25 / 0.4 + AuditKIT compare
- [x] Before/after table in README (real numbers)
- [x] HF Space `Esimuda/linguard` (static demo page)
- [x] Renamed user-facing brand to Linguard
- [x] Official form submitted (latest submission counts; confirmation email to babalolabowale01@gmail.com)
- [x] Seeds grown to ~29–36 / language (154 total across EN/PCM/YO/HA/IG)
- [x] Calibration grown to 112 prompts (55 harmful / 57 harmless), held out from eval seeds
- [x] Human-paragraph abstract at [`docs/LEXSI_ABSTRACT.md`](docs/LEXSI_ABSTRACT.md) (<500 words)
- [ ] HF Collections: script ready (`scripts/create_hf_collections.py`) but **HF 429 rate limit** (new-user 6 creations/day) blocked create on 3 Nov — retry in ~24h WAT
- [x] CircuitKIT `linguard_refusal` registration script (`scripts/register_linguard_circuit_task.py`)

## Still to do
- [ ] Claim HF credits → GPU run: SafeTune SafeGrad/LoRA on CuratorKIT set (fix 40% over-refusal) — `docs/GPU_PATH.md` · stub `notebooks/linguard_safeggrad_lora_stub.md`
- [ ] CircuitKIT: GPU `discover` after registration; push `Esimuda/linguard-circuit`; feed layers into SafeTune
- [ ] Re-run live Tiny Aya baseline + CAA + AuditKIT on the **grown** seed set (needs HF weights / time; CPU live pass was on n=34)
- [ ] Optional: grow calibration toward 100+/class for stronger CAST; optional LLM-judge (AuditKIT GuardJudge)
- [ ] Re-record demo video with the Linguard name + live before/after (old video shows offline harness)
- [ ] Optional: rename GitHub repo to `linguard` (needs owner OK)
- [ ] Optional resubmit form with cleaned abstract paragraphs if Lexsi UI still strips newlines in the confirmation email

## Submit payload
- Project: **Linguard — guarding language**
- Track: AI Red Teaming / Safety & Alignment (Track 2a+2b kits: AuditKIT, CuratorKIT, SafeTune; CircuitKIT wired)
- Repo: https://github.com/Esimuda/pidginguard
- Demo: https://huggingface.co/spaces/Esimuda/linguard
- Dataset: https://huggingface.co/datasets/Esimuda/linguard-safety · Vectors: https://huggingface.co/Esimuda/linguard-caa-vectors
- Collections: Models + Datasets under https://huggingface.co/Esimuda (created by `scripts/create_hf_collections.py`)
- Abstract: [`docs/LEXSI_ABSTRACT.md`](docs/LEXSI_ABSTRACT.md)
- One-liner: Tiny Aya refuses scams in English but helps with them in Hausa/Igbo. Linguard red-teams 5 Nigerian languages, curates repair data with CuratorKIT, hardens with SafeTune, and audits with AuditKIT: ASR 37.5% → 4.2% (over-refusal 0% → 40%, the next fix).
- Form notes: Lexsi submission page has **no dedicated demo-video upload field** in the public form; latest submission replaces prior. Demo is the HF Space URL (+ optional video link in write-up if re-submitted).
- Note: rules say projects must be built during the hackathon — pre-Nov-1 commits are scaffolding; all model work is dated 1 Nov 2026+.
