"""CLI: python -m pidginguard run|eval|export-seeds"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .harness import load_seeds, run_harness, write_results
from .models import resolve_backend


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pidginguard",
        description="PidginGuard multilingual safety red-team harness",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="Run red-team harness on seed prompts")
    run_p.add_argument("--backend", default=None, help="echo | fixture | hf")
    run_p.add_argument("--fixture", default=None, help="JSON map for fixture backend")
    run_p.add_argument("--model-id", default=None, help="HF model id for hf backend")
    run_p.add_argument("--seed-dir", default=None)
    run_p.add_argument("--lang", action="append", dest="languages")
    run_p.add_argument("--category", action="append", dest="categories")
    run_p.add_argument("--limit", type=int, default=None)
    run_p.add_argument("--out", default="data/results")
    run_p.add_argument("--name", default="baseline")

    eval_p = sub.add_parser("eval", help="Score an existing trials JSONL")
    eval_p.add_argument("trials", help="Path to *_trials.jsonl")
    eval_p.add_argument("--out", default=None, help="Optional summary JSON path")

    seeds_p = sub.add_parser("list-seeds", help="Print loaded seed prompt ids")
    seeds_p.add_argument("--seed-dir", default=None)
    seeds_p.add_argument("--lang", action="append", dest="languages")

    export_p = sub.add_parser(
        "export-curator",
        help="Export seeds to a CuratorKIT-friendly JSONL corpus",
    )
    export_p.add_argument("--seed-dir", default=None)
    export_p.add_argument("--out", default="data/curated/raw_corpus.jsonl")

    args = parser.parse_args(argv)

    if args.cmd == "run":
        kwargs = {}
        if args.fixture:
            kwargs["fixture_path"] = args.fixture
        if args.model_id:
            kwargs["model_id"] = args.model_id
        backend = resolve_backend(args.backend, **kwargs)
        trials, summary = run_harness(
            backend,
            seed_dir=args.seed_dir,
            languages=args.languages,
            categories=args.categories,
            limit=args.limit,
        )
        path = write_results(trials, summary, args.out, run_name=args.name)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        print(f"\nWrote {path}", file=sys.stderr)
        return 0

    if args.cmd == "eval":
        from .scoring import Score, aggregate, score_response

        trials_path = Path(args.trials)
        scores = []
        with trials_path.open(encoding="utf-8") as fh:
            for line in fh:
                row = json.loads(line)
                p = row["prompt"]
                scores.append(
                    score_response(
                        prompt_id=p["id"],
                        language=p["language"],
                        category=p["category"],
                        expected_behavior=p["expected_behavior"],
                        response=row["response"],
                    )
                )
        summary = aggregate(scores)
        text = json.dumps(summary, indent=2, ensure_ascii=False)
        print(text)
        if args.out:
            Path(args.out).write_text(text + "\n", encoding="utf-8")
        return 0

    if args.cmd == "list-seeds":
        prompts = load_seeds(args.seed_dir, languages=args.languages)
        for p in prompts:
            print(f"{p.id}\t{p.language}\t{p.category}\t{p.expected_behavior}")
        print(f"# {len(prompts)} prompts", file=sys.stderr)
        return 0

    if args.cmd == "export-curator":
        from .adapters.curatorkit import export_raw_corpus

        out = export_raw_corpus(args.seed_dir, args.out)
        print(out)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
