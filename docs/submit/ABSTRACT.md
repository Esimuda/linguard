# Linguard: guarding Nigerian languages in small AI models

**The problem.** Small multilingual models usually refuse a scam request in English. Ask for the same thing in Hausa, Yoruba, Igbo or Nigerian Pidgin, though, and they often write it. For millions of Nigerians, that gap is where fraud texts, fake jackpot messages and phishing scripts get through.

**What Linguard does.** Linguard tests Cohere Labs Tiny Aya Earth for that gap, then repairs it, using Lexsi's Track 2 kits in one pipeline:

- AuditKIT measures how the model behaves before and after each fix.
- CuratorKIT turns the model's failures into a clean, public repair dataset.
- SafeTune's steering method (CAA) adjusts the model's behaviour while it runs, without retraining it.
- A small LoRA training run fixes the model itself, using the repair data plus helpful example answers so it doesn't learn to refuse everything.
- CircuitKIT maps which parts of the model drive its refusals (exploratory).

**How we tested it.** We used 120 prompts the model never saw during training. 76 were harmful requests, such as scam SMS, fake bank alerts and impersonation scripts. 44 were normal questions a Nigerian user might ask, such as checking a prepaid meter balance. A safe model should refuse all 76 harmful prompts and answer all 44 normal ones.

**Results:**

| Model | Harmful requests it helped with (of 76) | Normal questions it wrongly refused (of 44) | Handled correctly (of 120) |
|---|---|---|---|
| Original Tiny Aya Earth | 30 | 0 | 90 |
| With steering only | 3 | 5 | 112 |
| **With Linguard's training fix** | **1** | **0** | **119** |

Steering alone stopped most of the scams but started refusing ordinary questions, especially in Pidgin. Linguard's training fix closed both gaps at once: it refused almost every harmful request and still answered every normal one.

By language, the original model helped with about half of the harmful Hausa prompts, two thirds in Yoruba, and nearly half in Igbo. After the fix it helped with none in Hausa, Igbo, Pidgin or English, and only one in Yoruba. That one was actually a refusal written with Yoruba tone marks that our checker missed, but we still counted it as a failure.

**Example.** Asked in Hausa to write a fake "you've won a jackpot" text, the original model wrote it, and Linguard refused. Asked in Pidgin how to check a meter balance, the steering-only model refused, and Linguard answered helpfully.

**Honest limits.** The test set is small and scored automatically by keyword checks, so we treat this as a strong pilot, not a final benchmark.

**Links:**

- GitHub: https://github.com/Esimuda/linguard
- Demo Space: https://huggingface.co/spaces/Esimuda/linguard
- Hardened model: https://huggingface.co/Esimuda/linguard-tiny-aya-earth-lora
- Dataset: https://huggingface.co/datasets/Esimuda/linguard-safety
- Demo video: https://youtu.be/-rBvL5wJ8WA
- Models collection: https://huggingface.co/collections/Esimuda/linguard-models-6af179733692a6fca0986d8b
- Datasets collection: https://huggingface.co/collections/Esimuda/linguard-datasets-6af179e0ebb37eb4c95a6830

Solo builder: Olabowale Babalola. Tracks 2a and 2b. Registration ticket #27J8-ENVZ-WV7M.
