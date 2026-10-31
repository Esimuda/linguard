"""Adapters that call real Lexsi toolkit APIs when installed.

Interfaces below are taken from published Lexsi-Labs docs/READMEs
(CuratorKIT, SafeTune, CircuitKIT, AuditKIT). We do not invent APIs.
If a package is missing, helpers raise a clear InstallError.
"""

from .auditkit import run_auditkit_before_after
from .circuitkit import discover_safety_circuit
from .curatorkit import export_raw_corpus, run_curatorkit
from .safetune import run_safetune_harden

__all__ = [
    "export_raw_corpus",
    "run_curatorkit",
    "run_safetune_harden",
    "discover_safety_circuit",
    "run_auditkit_before_after",
]
