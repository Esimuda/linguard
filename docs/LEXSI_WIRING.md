# Lexsi kit wiring (real APIs only)

Sources checked for Linguard adapters (Oct 31, 2026 WAT):

- Hackathon brief: https://hackathon.lexsi.ai/
- CuratorKIT: https://github.com/Lexsi-Labs/CuratorKIT · https://curatorkit.lexsi.ai/
- SafeTune: https://github.com/Lexsi-Labs/SafeTune · https://safetune.lexsi.ai/
- CircuitKIT: https://github.com/Lexsi-Labs/CircuitKIT · https://circuitkit.lexsi.ai/
- AuditKIT: https://github.com/Lexsi-Labs/AuditKIT · https://auditkit.lexsi.ai/

Adapters live under `src/pidginguard/adapters/`. Each supports `dry_run_config_only=True` so CI can print the intended call without importing the kit.

## 1. CuratorKIT → safety dataset

```python
from curatorkit import Curator, CuratorConfig

result = Curator(CuratorConfig(
    dataset="data/curated/raw_corpus.jsonl",
    llm_model="ollama/aya-expanse",          # prefer free/local
    # or openai-compatible local: llm_model="openai/CohereLabs/tiny-aya-earth",
    #                            llm_api_base="http://localhost:8000/v1"
    generation_task="adversarial_preference",
    hallucination_threshold=0.7,
    reward_threshold=0.7,
    export_formats=["alpaca", "sharegpt", "messages"],
    output_split={"train": 0.9, "validation": 0.1},
    output_dir="data/curated/curatorkit_out",
    min_tokens=3,
)).run()

# Hub (after HF account):
# result.push_to_hub("Esimuda/linguard-safety", export_file="sft_alpaca.jsonl")
```

Load export:

```python
from datasets import load_dataset
chat = load_dataset("data/curated/curatorkit_out", "sft_messages")
```

Linguard helper: `python -m pidginguard export-curator` then `adapters.curatorkit.run_curatorkit(...)`.

## 2. SafeTune harden

From CuratorKIT handoff docs:

```python
from datasets import load_dataset
from safetune.runner import harden

# harden.SafeGradTrainer(model, tokenizer).train(
#     load_dataset("data/curated/curatorkit_out", "sft_messages", split="train"),
#     safety_dataset=safety_dataset,
# )
```

Evaluate / attack (SafeTune docs):

```python
from safetune.evaluate import evaluate, AbliterationAttack, BoNAttack
# results = evaluate(model, benchmarks=["harmbench"], tokenizer=tok)
```

CircuitKIT scores: SafeTune reads `*_scores.json` keys `safety_units` / `layer_suggestions` (and can derive them from `node_scores`).

## 3. CircuitKIT

```python
from circuitkit import Pipeline

pipe = Pipeline("CohereLabs/tiny-aya-earth", task="ioi")  # safety task TBD post-kickoff
pipe.discover(algorithm="eap-ig", sparsity=0.3)
pipe.evaluate()
pipe.prune()
pipe.export("./data/results/circuit_checkpoint")
```

Tiny Aya / Aya Expanse are listed as experimental but validated surfaces in CircuitKIT docs. Aya Vision is rejected (no vision tower in TransformerLens).

## 4. AuditKIT before / after

```python
import auditkit as ak

samples = [ak.Sample(input=p, target="REFUSE") for p in attack_prompts]
metrics = ["exact_match", "f1_score"]  # swap to GuardJudge / red-team metrics when configured

base = ak.evaluate(samples, "hf:CohereLabs/tiny-aya-earth", metrics)
tuned = ak.evaluate(samples, "hf:Esimuda/linguard-tiny-aya-earth-lora", metrics)
print(ak.compare(base, tuned).summary())
```

Any `list[str] -> list[str]` callable also works as a model — useful for our echo backend during dry runs.

## Install pins (expected)

```bash
pip install "curatorkit[all]"
pip install safetune
pip install "auditkit[transformers]"
pip install circuitkit
```

Exact versions will be locked in `requirements-lexsi.txt` after Nov 1 kickoff once the hackathon pin list is published.
