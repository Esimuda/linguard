Linguard ("guarding language") is a Nigerian multilingual safety project for the Lexsi AI Safety and Alignment Hackathon.

Small open multilingual models often refuse scam and social-engineering requests in English, then comply when the same intent is asked in Hausa, Igbo, Yoruba, or Nigerian Pidgin. Linguard attacks that gap on Cohere Labs Tiny Aya Earth and turns the failures into a repair loop.

We chain Lexsi Track 2 kits into one pipeline. AuditKIT scores a live baseline on red-team seeds across five languages. CuratorKIT quality-gates those failures into a public repair dataset (Esimuda/linguard-safety). SafeTune applies CAA inference-time steering from a held-out calibration set. AuditKIT then compares before and after on the same samples. CircuitKIT is wired for refusal-circuit discovery once GPU is available.

On Tiny Aya Earth (CPU live run, 1 Nov 2026), attack success fell from 37.5% to 4.2% at CAA strength 0.25. AuditKIT linguard_attack_success moved from 0.2647 to 0.0294 (−88.9% relative). Overall accuracy rose from 73.5% to 85.3%. Over-refusal on benign prompts rose from 0% to 40%, which is the trade-off the next GPU SafeGrad/LoRA harden on the CuratorKIT set is meant to reduce.

Public artifacts: GitHub Esimuda/linguard, demo Space Esimuda/linguard, dataset Esimuda/linguard-safety, CAA vectors Esimuda/linguard-caa-vectors. Solo builder Olabowale Babalola. Registration ticket #27J8-ENVZ-WV7M. Model work dated 1 Nov 2026+ inside the hackathon window. Tracks: 2a (multilingual/code-mixed safety; adversarial eval set) and 2b (inference-time safety steering; safety repair).
