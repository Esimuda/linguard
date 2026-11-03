# Linguard SafeGrad / LoRA stub (Colab / ZeroGPU)

> Stub only — run on a GPU runtime. Do not commit HF tokens.

```python
# !pip install -e ".[hf,lexsi]" peft accelerate bitsandbytes
import os
from datasets import load_dataset
# from safetune import harden  # see https://safetune.lexsi.ai/

assert os.environ.get("HF_TOKEN"), "export HF_TOKEN with write access to Esimuda/*"

ds = load_dataset(
    "Esimuda/linguard-safety",
    data_files="curated/sft_messages.jsonl",
    split="train",
)
print(ds)

# TODO on GPU:
# 1. Load CohereLabs/tiny-aya-earth
# 2. harden.SafeGradTrainer(...).train(ds, safety_dataset=ds)  OR LoRA SFT on messages
# 3. Push adapter → Esimuda/linguard-tiny-aya-earth-lora
# 4. Re-run: LINGUARD_MODEL_PATH=... python scripts/live_pipeline.py --phase baseline
# 5. AuditKIT compare vs CPU CAA 0.25 (target: keep ASR low, cut over-refusal from 40%)
```

Also see `docs/GPU_PATH.md`.
