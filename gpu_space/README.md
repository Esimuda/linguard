---
title: Linguard GPU LoRA harden
emoji: 🛡️
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---
One-shot GPU job for Linguard (Lexsi AI Safety hackathon): baseline vs SafeTune CAA vs LoRA safety SFT on Tiny Aya Earth,
evaluated on 120 held-out multilingual seeds (EN/PCM/YO/HA/IG). Pushes adapter to Esimuda/linguard-tiny-aya-earth-lora, then tries CircuitKIT discover.
Code: https://github.com/Esimuda/linguard
