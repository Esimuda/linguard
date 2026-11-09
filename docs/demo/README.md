# docs/demo

**Demo video (1:50):** https://youtu.be/er5yVB2xrWY

Earlier offline clip:

- **`pidginguard-walkthrough.mp4`** — ~58s, 1280×720 H.264, silent with caption overlays. Real terminal output of the offline harness (frames rendered from actual command output, ffmpeg-assembled):
  1. Title card — Linguard — Lexsi AI Safety 2026 / Israel
  2. `git log` + repo layout
  3. `list-seeds` — Pidgin / Yoruba / Hausa / Igbo seed ids (34 total)
  4. `run --backend echo` — baseline: n=34, refusal 0.706, ASR 0.042, over-refusal 0.10, per-language scores
  5. `eval` — re-score saved trials JSONL
  6. Pidgin scam probes (`pcm-scam-001/002`) with scored refusals
  7. End card — github.com/Esimuda/linguard
- `offline-harness-transcript.txt` — text transcript of the harness run.

See [`../../DEMO_WALKTHROUGH.md`](../../DEMO_WALKTHROUGH.md) for the shot list.
