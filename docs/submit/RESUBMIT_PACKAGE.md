# Linguard resubmit package (draft)

Latest Lexsi submission counts. Deadline: end of day **14 Nov 2026 AoE**.
Form: https://hackathon.lexsi.ai/submission/ (Tally `o9E0Ve`).

## Form fields (from live Tally HTML 3 Nov 2026)

| Field | Type | Notes |
|---|---|---|
| Your team | section | |
| Registered email | email | required — use registration email |
| Abstract | textarea | required — under 500 words |
| Discord username | text | present (optional in parse) |
| Hugging Face model collection | link | required — public collection URL |
| Hugging Face dataset collection | link | required — public collection URL |
| Hugging Face article | link | required on form; site text also allows GitHub README as write-up |
| GitHub repo | link | required |
| Which repos did you use? | checkboxes | CuratorKIT, AlignTune, AgentTune, SafeTune, CircuitKIT, AuditKIT |
| Which other repos? | text | hidden unless needed |
| Which models did you use? | checkboxes | Tiny Aya / Aya Expanse family |
| Which other models? | text | hidden unless needed |
| Which track does the submission fall under? | checkboxes | Track 1 / 2a / 2b / 3 |
| Problem statements Track 1/2a/2b/3 | checkboxes | shown for selected tracks |
| **Demo video** | — | **NOT present** (VIDEO=0, FILE_UPLOAD=0) |

## Values to paste

- Registered email: `babalolabowale01@gmail.com` (ticket `#27J8-ENVZ-WV7M`)
- Abstract: `docs/submit/ABSTRACT.md` (228 words, paragraphs)
- Discord: `esimuda`
- Tracks: **2a + 2b**
- Repos: CuratorKIT, SafeTune, CircuitKIT, AuditKIT
- Models: Tiny Aya Earth
- GitHub: https://github.com/Esimuda/pidginguard
- Demo/public: https://huggingface.co/spaces/Esimuda/linguard (put in article/demo-related links as applicable; Space is live)
- Dataset repo: https://huggingface.co/datasets/Esimuda/linguard-safety
- Model repo: https://huggingface.co/Esimuda/linguard-caa-vectors
- Write-up / article field: GitHub README URL until an HF Article exists

## Blockers before ideal resubmit

1. **HF collections missing** — Esimuda has **0** collections. `create_collection` hit **429** “6 per day” new-user rate limit on 3 Nov ~13:32 Africa/Lagos; retry ~24h later or create in HF UI if quota allows.
2. GPU SafeGrad/LoRA + CircuitKIT discover (box is CPU-only; need Lexsi $20 HF credits / Colab).
3. Re-eval on expanded 74 seeds after GPU/harden (seeds already on Hub).

## Prior confirmation abstract issue

Email “Lexsi Hackathon: submission received” (3 Nov 2026, 12:23 Africa/Lagos) pasted the abstract as **one wall-of-text paragraph** (Tally/email formatting). Content was otherwise complete. Resubmit with `ABSTRACT.md` for human paragraphs in the form field.
