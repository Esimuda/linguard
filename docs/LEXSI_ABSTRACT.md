# Linguard — Lexsi submission abstract

Small multilingual models often look safe in English and then slip when people speak Nigerian Pidgin, Yoruba, Hausa, or Igbo. Scammers already work in those languages — OTP phishing, romance scripts, fake bank agents — so a red-team that only probes English misses the real gap. Linguard is a solo build for the Lexsi AI Safety & Alignment hackathon that closes that gap for Cohere Labs Tiny Aya Earth.

The pipeline chains four Lexsi kits end to end. AuditKIT scores the same multilingual seed set before and after harden. CuratorKIT turns attack and repair pairs into a gated safety dataset with provenance. SafeTune applies inference-time CAA steering on held-out calibration prompts (and leaves a clear GPU path for SafeGrad / LoRA weight harden). CircuitKIT is wired with a registerable `linguard_refusal` task so GPU hosts can discover refusal circuits and feed layer suggestions back into SafeTune.

On the live CPU run, attack success rate fell from 37.5% to 4.2% with CAA strength 0.25. AuditKIT reported `linguard_attack_success` moving from 0.2647 to 0.0294 (−88.9% relative), with accuracy rising as several Hausa and Igbo failures flipped to correct refusals. The honest trade-off is over-refusal: benign controls went from 0% to 40% at strength 0.25. The next fix is the GPU SafeGrad / LoRA path on the CuratorKIT set so the model can stay helpful on ordinary meter, BVN, and SIM questions while still refusing scams.

Artifacts are public: GitHub `Esimuda/linguard`, demo Space `Esimuda/linguard`, dataset `Esimuda/linguard-safety`, and CAA vectors `Esimuda/linguard-caa-vectors`. Built solo by Olabowale Babalola, ticket `#27J8-ENVZ-WV7M`.
