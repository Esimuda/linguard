"""CuratorKIT adapter — real API from https://github.com/Lexsi-Labs/CuratorKIT

Documented surface used here:
  from curatorkit import Curator, CuratorConfig
  Curator(CuratorConfig(...)).run()
  result.push_to_hub(...)
Exports are loadable via datasets.load_dataset(output_dir, "sft_messages").
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..harness import load_seeds


class InstallError(RuntimeError):
    pass


def export_raw_corpus(
    seed_dir: str | Path | None = None,
    out_path: str | Path = "data/curated/raw_corpus.jsonl",
) -> Path:
    """Write seed prompts as a document corpus CuratorKIT can ingest."""
    prompts = load_seeds(seed_dir)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        for p in prompts:
            # CuratorKIT accepts JSONL; we keep provenance fields for later gates.
            row = {
                "id": p.id,
                "text": p.text,
                "language": p.language,
                "category": p.category,
                "expected_behavior": p.expected_behavior,
                "tags": p.tags,
                "source": "pidginguard-seeds",
            }
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return out


def run_curatorkit(
    dataset_path: str | Path,
    output_dir: str | Path = "data/curated/curatorkit_out",
    *,
    llm_model: str = "ollama/aya-expanse",
    generation_task: str = "adversarial_preference",
    export_formats: list[str] | None = None,
    dry_run_config_only: bool = False,
) -> dict[str, Any]:
    """Run CuratorKIT when installed.

    Prefer free/local generators (Ollama / local vLLM). Do not burn paid GPU APIs
    unless the operator explicitly sets llm_model to a paid route.
    """
    config_dict = {
        "dataset": str(dataset_path),
        "llm_model": llm_model,
        "generation_task": generation_task,
        "hallucination_threshold": 0.7,
        "reward_threshold": 0.7,
        "export_formats": export_formats or ["alpaca", "sharegpt", "messages"],
        "output_dir": str(output_dir),
        "output_split": {"train": 0.9, "validation": 0.1},
        "min_tokens": 3,
    }
    if dry_run_config_only:
        return {"status": "config_only", "config": config_dict}

    try:
        from curatorkit import Curator, CuratorConfig  # type: ignore
    except ImportError as exc:
        raise InstallError(
            "CuratorKIT not installed. "
            'pip install "curatorkit[all]" '
            "or pip install 'curatorkit[all] @ git+https://github.com/Lexsi-Labs/CuratorKIT.git'"
        ) from exc

    result = Curator(CuratorConfig(**config_dict)).run()
    summary = {"status": "ok", "output_dir": str(output_dir)}
    if hasattr(result, "print_summary"):
        result.print_summary()
    if hasattr(result, "manifest"):
        summary["manifest"] = result.manifest
    return summary
