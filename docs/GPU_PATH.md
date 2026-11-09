# Linguard — GPU path (Colab / HF ZeroGPU)

The box that produced the live numbers in the README is **CPU-only** (8 vCPU, 15 GB RAM).
Everything that fits on CPU ran live (Tiny Aya Earth bf16 inference, AuditKIT, CuratorKIT, SafeTune CAA steering).
These steps need a GPU (Colab T4/L4/A100, or HF ZeroGPU via the Lexsi $20 HF credits):

## Done 9 Nov 2026
- LoRA harden + CAA re-run on 120 held-out seeds: `gpu_space/train.py` on HF Space `Esimuda/linguard-gpu-train` (A10G, ~5 min per run). Adapter: `Esimuda/linguard-tiny-aya-earth-lora`. Results: README "GPU results".
- CircuitKIT discover: same Space with `MODE=circuit` on A100 → `Esimuda/linguard-circuit` (exploratory pruned checkpoint).
- Not done: SafeTune `SafeGradTrainer` itself (the adapter is plain LoRA SFT with self-distilled helpful targets).

## 1. SafeTune weight-level harden (SafeGrad / LoRA SFT)
```bash
pip install -e ".[hf,lexsi]"
export HF_TOKEN=...   # Esimuda write token (never commit)
python - <<'PY'
from datasets import load_dataset
from safetune import harden
ds = load_dataset("Esimuda/linguard-safety", data_files="curated/sft_messages.jsonl", split="train")
# harden.SafeGradTrainer(model, tokenizer).train(ds, safety_dataset=ds)  -- see https://safetune.lexsi.ai/
PY
python scripts/live_pipeline.py --phase baseline   # re-run on the hardened checkpoint via LINGUARD_MODEL_PATH
```
Push the adapter to `Esimuda/linguard-tiny-aya-earth-lora`.

## 2. CircuitKIT safety-circuit discovery

## CircuitKIT registration (CPU-safe) → GPU discover

```bash
# Registers task `linguard_refusal` from data/seeds/*.jsonl (refuse vs answer)
python scripts/register_linguard_circuit_task.py

# GPU only — will no-op with a clear skip on CPU-only hosts (does not fake metrics)
python scripts/register_linguard_circuit_task.py --discover --n-examples 34 \
  --hub-repo Esimuda/linguard-circuit
```


CircuitKIT `discover()` needs a TransformerLens `HookedTransformer` and a registered task. Built-in tasks
(`ioi`, `wmdp`, `truthfulqa`, ...) do not include multilingual refusal, so register a Linguard refusal task
(`ck.register_task(spec)`) from `data/seeds/*.jsonl` (harmful = refuse, benign = answer), then:
```python
import circuitkit as ck
m = ck.load_model("CohereLabs/tiny-aya-earth", dtype="bfloat16", device="cuda")
circuit = ck.discover(m, "linguard_refusal", algorithm="eap-ig", n_examples=34)
ck.export_checkpoint(m, circuit, "./linguard-circuit", push_to_hub=True, hub_repo="Esimuda/linguard-circuit")
```
Feed `circuit` layer suggestions back into SafeTune `target_layers` (CPU run used layers 12/16/20 by hand).

## 3. Bigger calibration for conditional steering (SafeTune CAST)
`fit_cast_condition` on 8+8 calibration prompts gave F1=0.8 and mis-gated benign Hausa prompts.
Calibration is grown past 50+/class in `data/calibration/caa_calibration.jsonl` (held out from eval seeds). Aim for 100+/class before relying on CAST in production; current size is enough for stronger CAST pilots.
