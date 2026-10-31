"""Multilingual red-team harness for PidginGuard seed prompts."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .models import ModelBackend, resolve_backend
from .scoring import Score, aggregate, score_response


DEFAULT_SEED_DIR = Path(__file__).resolve().parents[2] / "data" / "seeds"


@dataclass
class Prompt:
    id: str
    language: str
    category: str
    expected_behavior: str
    text: str
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> "Prompt":
        return cls(
            id=str(row["id"]),
            language=str(row["language"]),
            category=str(row["category"]),
            expected_behavior=str(row.get("expected_behavior", "refuse")),
            text=str(row["text"]),
            tags=list(row.get("tags") or []),
        )


@dataclass
class Trial:
    prompt: Prompt
    response: str
    score: Score

    def to_dict(self) -> dict[str, Any]:
        return {
            "prompt": asdict(self.prompt),
            "response": self.response,
            "score": self.score.to_dict(),
        }


def load_seeds(
    seed_dir: str | Path | None = None,
    *,
    languages: Iterable[str] | None = None,
    categories: Iterable[str] | None = None,
) -> list[Prompt]:
    root = Path(seed_dir) if seed_dir else DEFAULT_SEED_DIR
    lang_filter = set(languages) if languages else None
    cat_filter = set(categories) if categories else None
    prompts: list[Prompt] = []
    for path in sorted(root.glob("*.jsonl")):
        with path.open(encoding="utf-8") as fh:
            for line_no, line in enumerate(fh, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{line_no}: invalid JSON") from exc
                p = Prompt.from_dict(row)
                if lang_filter and p.language not in lang_filter:
                    continue
                if cat_filter and p.category not in cat_filter:
                    continue
                prompts.append(p)
    return prompts


def run_harness(
    backend: ModelBackend | None = None,
    *,
    seed_dir: str | Path | None = None,
    languages: Iterable[str] | None = None,
    categories: Iterable[str] | None = None,
    limit: int | None = None,
) -> tuple[list[Trial], dict[str, Any]]:
    model = backend or resolve_backend()
    prompts = load_seeds(seed_dir, languages=languages, categories=categories)
    if limit is not None:
        prompts = prompts[:limit]

    trials: list[Trial] = []
    for p in prompts:
        response = model.generate(p.text, language=p.language)
        score = score_response(
            prompt_id=p.id,
            language=p.language,
            category=p.category,
            expected_behavior=p.expected_behavior,
            response=response,
        )
        trials.append(Trial(prompt=p, response=response, score=score))

    summary = aggregate([t.score for t in trials])
    summary["backend"] = getattr(model, "name", type(model).__name__)
    summary["model_id"] = getattr(model, "model_id", None)
    return trials, summary


def write_results(
    trials: list[Trial],
    summary: dict[str, Any],
    out_dir: str | Path,
    *,
    run_name: str = "baseline",
) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    trials_path = out / f"{run_name}_trials.jsonl"
    summary_path = out / f"{run_name}_summary.json"
    with trials_path.open("w", encoding="utf-8") as fh:
        for t in trials:
            fh.write(json.dumps(t.to_dict(), ensure_ascii=False) + "\n")
    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return summary_path
