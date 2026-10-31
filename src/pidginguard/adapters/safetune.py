"""SafeTune adapter — real API from https://github.com/Lexsi-Labs/SafeTune

Documented surfaces used here (from CuratorKIT handoff + SafeTune docs):
  from safetune.runner import harden
  harden.SafeGradTrainer(model, tokenizer).train(
      load_dataset("output/", "sft_messages", split="train"),
      safety_dataset=safety_dataset,
  )
  from safetune.evaluate import evaluate, AbliterationAttack, BoNAttack
CircuitKIT score files: load_circuit_info_from_file / get_circuit_info.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class InstallError(RuntimeError):
    pass


def run_safetune_harden(
    model_id: str,
    curated_dir: str | Path,
    *,
    dataset_config: str = "sft_messages",
    safety_dataset: Any = None,
    dry_run_config_only: bool = False,
) -> dict[str, Any]:
    """Harden a model with SafeTune using a CuratorKIT export folder."""
    plan = {
        "model_id": model_id,
        "train_dataset": str(curated_dir),
        "dataset_config": dataset_config,
        "method": "SafeGradTrainer",
        "notes": (
            "Call harden.SafeGradTrainer(model, tokenizer).train("
            "load_dataset(curated_dir, dataset_config, split='train'), "
            "safety_dataset=safety_dataset)"
        ),
    }
    if dry_run_config_only:
        return {"status": "config_only", "plan": plan}

    try:
        from datasets import load_dataset  # type: ignore
        from safetune.runner import harden  # type: ignore
        from transformers import AutoModelForCausalLM, AutoTokenizer  # type: ignore
    except ImportError as exc:
        raise InstallError(
            "SafeTune (+ datasets, transformers) not installed. "
            "See https://safetune.lexsi.ai/ and https://github.com/Lexsi-Labs/SafeTune"
        ) from exc

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    train_ds = load_dataset(str(curated_dir), dataset_config, split="train")
    trainer = harden.SafeGradTrainer(model, tokenizer)
    trainer.train(train_ds, safety_dataset=safety_dataset)
    return {"status": "ok", "plan": plan}


def run_safetune_eval(model: Any, tokenizer: Any, benchmarks: list[str] | None = None) -> Any:
    """Thin wrapper around safetune.evaluate.evaluate when available."""
    try:
        from safetune.evaluate import evaluate  # type: ignore
    except ImportError as exc:
        raise InstallError(
            "SafeTune evaluate not available. pip install safetune"
        ) from exc
    return evaluate(model, benchmarks=benchmarks or ["harmbench"], tokenizer=tokenizer)
