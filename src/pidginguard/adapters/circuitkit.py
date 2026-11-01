"""CircuitKIT adapter — real API from https://github.com/Lexsi-Labs/CircuitKIT

Documented surfaces:
  from circuitkit import Pipeline
  pipe = Pipeline(model_id, task=...)
  pipe.discover(algorithm="eap-ig", sparsity=0.3)
  pipe.evaluate(); pipe.prune(); pipe.export("./checkpoint")

  import circuitkit as ck
  model = ck.load_model("CohereLabs/tiny-aya-earth")
  circuit = ck.discover(model, "ioi", n_examples=32)
  ck.export_checkpoint(model, circuit, "./out")
Score JSONs expose safety_units / layer_suggestions for SafeTune.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class InstallError(RuntimeError):
    pass


def discover_safety_circuit(
    model_id: str = "CohereLabs/tiny-aya-earth",
    *,
    task: str = "ioi",
    algorithm: str = "eap-ig",
    sparsity: float = 0.3,
    export_dir: str | Path = "data/results/circuit_checkpoint",
    dry_run_config_only: bool = False,
) -> dict[str, Any]:
    plan = {
        "model_id": model_id,
        "task": task,
        "algorithm": algorithm,
        "sparsity": sparsity,
        "export_dir": str(export_dir),
        "note": (
            "For Linguard we will swap `task` to a safety-oriented probe "
            "once CircuitKIT task registry options for refusal/safety are confirmed "
            "post-kickoff. Tiny Aya is listed as experimental but validated in CircuitKIT."
        ),
    }
    if dry_run_config_only:
        return {"status": "config_only", "plan": plan}

    try:
        from circuitkit import Pipeline  # type: ignore
    except ImportError as exc:
        raise InstallError(
            "CircuitKIT not installed. "
            "pip install circuitkit "
            "or see https://github.com/Lexsi-Labs/CircuitKIT"
        ) from exc

    pipe = Pipeline(model_id, task=task)
    pipe.discover(algorithm=algorithm, sparsity=sparsity)
    pipe.evaluate()
    pipe.prune()
    pipe.export(str(export_dir))
    return {"status": "ok", "plan": plan, "export_dir": str(export_dir)}
