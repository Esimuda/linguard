# Linguard GPU SafeGrad / LoRA — Colab / ZeroGPU runbook

Box is CPU-only. Run this on Colab T4/L4 or HF ZeroGPU after claiming Lexsi $20 credits.

```bash
!pip install -q datasets transformers accelerate peft safetune auditkit curatorkit
# or: pip install -e ".[hf,lexsi]" from a clone of Esimuda/pidginguard
import os
os.environ["HF_TOKEN"] = ...  # Esimuda write token
from datasets import load_dataset
ds = load_dataset("Esimuda/linguard-safety", data_files="curated/sft_messages.jsonl", split="train")
# Follow https://safetune.lexsi.ai/ for harden.SafeGradTrainer / LoRA SFT
# Push adapter to Esimuda/linguard-tiny-aya-earth-lora
# Then: python scripts/live_pipeline.py --phase baseline/harden/audit with LINGUARD_MODEL_PATH
```

Also run CircuitKIT refusal-task `discover` per `docs/GPU_PATH.md` §2.
