"""AuditKIT adapter — real API from https://github.com/Lexsi-Labs/AuditKIT

Documented surfaces:
  import auditkit as ak
  samples = [ak.Sample(input=..., target=...)]
  base = ak.evaluate(samples, "hf:CohereLabs/tiny-aya-earth", metrics)
  tuned = ak.evaluate(samples, "hf:<you>/pidginguard-hardened", metrics)
  print(ak.compare(base, tuned).summary())
Also: any list[str] -> list[str] callable works as a model.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from ..harness import load_seeds


class InstallError(RuntimeError):
    pass


def build_samples_from_seeds(seed_dir: str | Path | None = None) -> list[dict[str, str]]:
    """Build AuditKIT-like sample dicts (input/target) without requiring AuditKIT."""
    samples = []
    for p in load_seeds(seed_dir):
        target = "REFUSE" if p.expected_behavior == "refuse" else "ANSWER_HELPFULLY"
        samples.append(
            {
                "id": p.id,
                "input": p.text,
                "target": target,
                "language": p.language,
                "category": p.category,
            }
        )
    return samples


def run_auditkit_before_after(
    before_model: str | Callable[[list[str]], list[str]],
    after_model: str | Callable[[list[str]], list[str]],
    *,
    seed_dir: str | Path | None = None,
    metrics: list[str] | None = None,
    dry_run_config_only: bool = False,
) -> dict[str, Any]:
    samples_raw = build_samples_from_seeds(seed_dir)
    plan = {
        "n_samples": len(samples_raw),
        "before_model": before_model if isinstance(before_model, str) else "callable",
        "after_model": after_model if isinstance(after_model, str) else "callable",
        "metrics": metrics or ["exact_match", "f1_score"],
        "note": "For safety judges prefer AuditKIT red-team / GuardJudge metrics when available.",
    }
    if dry_run_config_only:
        return {"status": "config_only", "plan": plan, "samples_preview": samples_raw[:3]}

    try:
        import auditkit as ak  # type: ignore
    except ImportError as exc:
        raise InstallError(
            "AuditKIT not installed. pip install auditkit "
            'or pip install "auditkit[transformers]" '
            "see https://github.com/Lexsi-Labs/AuditKIT"
        ) from exc

    samples = [ak.Sample(input=s["input"], target=s["target"]) for s in samples_raw]
    metric_list = metrics or ["exact_match", "f1_score"]
    base = ak.evaluate(samples, before_model, metric_list)
    tuned = ak.evaluate(samples, after_model, metric_list)
    comparison = ak.compare(base, tuned)
    return {
        "status": "ok",
        "plan": plan,
        "before": base.summary() if hasattr(base, "summary") else str(base),
        "after": tuned.summary() if hasattr(tuned, "summary") else str(tuned),
        "compare": comparison.summary() if hasattr(comparison, "summary") else str(comparison),
    }


def dump_sample_manifest(out_path: str | Path, seed_dir: str | Path | None = None) -> Path:
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {"samples": build_samples_from_seeds(seed_dir)}
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out
