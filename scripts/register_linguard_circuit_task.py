#!/usr/bin/env python3
"""Register CircuitKIT task `linguard_refusal` from local Linguard seeds.

CPU-safe: registration only. GPU discover is documented / gated behind --discover
and will refuse to fake results on CPU-only hosts.

Usage:
  python scripts/register_linguard_circuit_task.py              # register + print plan
  python scripts/register_linguard_circuit_task.py --discover    # needs CUDA + Tiny Aya
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "data" / "seeds"


def load_harmful_rows(max_records: int | None = None) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(SEEDS.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("expected_behavior") != "refuse":
                continue
            # SafetyPromptAdapter looks for prompt/goal/instruction columns
            rows.append(
                {
                    "id": row["id"],
                    "prompt": row["text"],
                    "category": row.get("category", ""),
                    "language": row.get("language", ""),
                    "target": "Sure, here is how:",
                }
            )
            if max_records and len(rows) >= max_records:
                return rows
    return rows


def load_benign_controls() -> list[str]:
    out: list[str] = []
    for path in sorted(SEEDS.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("expected_behavior") == "answer":
                out.append(row["text"])
    return out or [
        "How do I check my prepaid meter balance on the official app?",
        "What documents do I need to open a savings account in Nigeria?",
    ]


def register_task(max_records: int = 128, pairing_mode: str = "harmful_vs_benign") -> dict:
    from circuitkit.data.adapters.safety_prompt import SafetyPromptAdapter
    from circuitkit.data.normalized_task import NormalizedTaskSpec
    from circuitkit.tasks.registry import is_task_registered, register_task

    task_name = "linguard_refusal"
    raw = load_harmful_rows(max_records=max_records)
    if len(raw) < 8:
        raise SystemExit(f"need more refuse seeds, got {len(raw)}")
    ds = SafetyPromptAdapter().adapt(
        raw,
        name=task_name,
        source=str(SEEDS),
        max_records=max_records,
        pairing_mode=pairing_mode,
        benign_controls=load_benign_controls(),
    )
    if not ds.fully_paired:
        raise SystemExit(f"adapter produced {ds.n_paired}/{len(ds)} paired records")
    if is_task_registered(task_name):
        # Re-register by replacing is not supported; report existing
        status = "already_registered"
    else:
        register_task(NormalizedTaskSpec(ds, name=task_name))
        status = "registered"
    return {
        "status": status,
        "task": task_name,
        "n_records": len(ds),
        "n_paired": ds.n_paired,
        "pairing_mode": pairing_mode,
    }


def maybe_discover(n_examples: int, hub_repo: str | None) -> dict:
    import torch

    if not torch.cuda.is_available():
        return {
            "status": "skipped_no_gpu",
            "note": "CircuitKIT discover needs CUDA. See docs/GPU_PATH.md — do not fabricate results.",
        }
    import circuitkit as ck

    info = register_task(max_records=max(n_examples, 32))
    model = ck.load_model("CohereLabs/tiny-aya-earth", dtype="bfloat16", device="cuda")
    circuit = ck.discover(
        model,
        "linguard_refusal",
        algorithm="eap-ig",
        n_examples=n_examples,
    )
    out_dir = ROOT / "data" / "results" / "circuit_checkpoint"
    out_dir.mkdir(parents=True, exist_ok=True)
    ck.export_checkpoint(
        model,
        circuit,
        str(out_dir / "linguard-circuit"),
        push_to_hub=bool(hub_repo),
        hub_repo=hub_repo,
        hub_private=False,
    )
    return {"status": "ok", "task_info": info, "export_dir": str(out_dir)}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--discover", action="store_true", help="Run GPU discover (requires CUDA)")
    p.add_argument("--n-examples", type=int, default=34)
    p.add_argument("--hub-repo", default=None, help="Optional HF repo to push circuit checkpoint")
    p.add_argument("--max-records", type=int, default=128)
    p.add_argument(
        "--pairing-mode",
        default="harmful_vs_benign",
        choices=["answer_contrastive", "harmful_vs_benign", "benign_vs_harmful"],
    )
    args = p.parse_args(argv)

    if args.discover:
        result = maybe_discover(args.n_examples, args.hub_repo)
    else:
        result = register_task(max_records=args.max_records, pairing_mode=args.pairing_mode)
        result["gpu_next"] = (
            "On a CUDA host: python scripts/register_linguard_circuit_task.py --discover "
            "--n-examples 34 --hub-repo Esimuda/linguard-circuit"
        )
    print(json.dumps(result, indent=2))
    return 0 if result.get("status") in {"registered", "already_registered", "ok", "skipped_no_gpu"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
