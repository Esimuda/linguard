from pidginguard.harness import load_seeds, run_harness
from pidginguard.models import EchoBackend
from pidginguard.adapters.curatorkit import export_raw_corpus, run_curatorkit
from pidginguard.adapters.auditkit import build_samples_from_seeds, run_auditkit_before_after
from pidginguard.adapters.safetune import run_safetune_harden
from pidginguard.adapters.circuitkit import discover_safety_circuit


def test_load_seeds_all_langs():
    prompts = load_seeds()
    langs = {p.language for p in prompts}
    assert langs >= {"en", "pcm", "yo", "ha", "ig"}
    assert len(prompts) >= 30


def test_echo_harness_runs():
    trials, summary = run_harness(EchoBackend(), limit=10)
    assert len(trials) == 10
    assert summary["n"] == 10
    assert summary["backend"] == "echo"


def test_export_and_dry_runs(tmp_path):
    out = export_raw_corpus(out_path=tmp_path / "raw.jsonl")
    assert out.exists()
    assert run_curatorkit(out, dry_run_config_only=True)["status"] == "config_only"
    assert run_safetune_harden("CohereLabs/tiny-aya-earth", out, dry_run_config_only=True)[
        "status"
    ] == "config_only"
    assert discover_safety_circuit(dry_run_config_only=True)["status"] == "config_only"
    assert run_auditkit_before_after("echo", "echo", dry_run_config_only=True)["status"] == "config_only"
    samples = build_samples_from_seeds()
    assert samples and "input" in samples[0]
