# Demo walkthrough plan

Goal: ≤90s clip of the **real harness** (terminal), not slides. Prefer after HF access; early package can ship offline.

## Script (Israel on camera / voice optional; captions OK)

1. `pwd` → show `linguard` repo + `git log -1 --oneline`
2. `python -m pidginguard list-seeds | tail` — show Yo/Ha/Ig/PCM ids
3. `python -m pidginguard run --backend echo --name demo --limit 12` — live scroll of summary JSON (ASR, by_language)
4. `head -n 2 data/results/demo_trials.jsonl` — one attack refusal + one benign answer
5. Open `docs/LEXSI_WIRING.md` briefly — CuratorKIT → SafeTune → AuditKIT chain
6. Closing card: repo URL + ticket `#27J8-ENVZ-WV7M` + track

## Capture

- Tooling: simple terminal recording (`script` / asciinema / OBS)
- Output path: `docs/demo/linguard-walkthrough.mp4` (or `.cast`)
- Keep under ~2 minutes; silent + captions acceptable if TTS blocked

## Status

- [x] Plan written (early package)
- [ ] Offline echo demo recorded
- [ ] Live Tiny Aya demo recorded (post HF gate)
