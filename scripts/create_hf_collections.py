#!/usr/bin/env python3
"""Idempotent: create public HF collections for Linguard models + datasets.

Reads HF_TOKEN from the environment (never prints it). Re-running is safe:
collections are created with exists_ok semantics via list+create, and items
use exists_ok=True on add_collection_item.
"""
from __future__ import annotations

import os
import sys
from typing import Optional

from huggingface_hub import HfApi
from huggingface_hub.errors import HfHubHTTPError


OWNER = "Esimuda"
MODELS_TITLE = "Linguard Models"
DATASETS_TITLE = "Linguard Datasets"
MODELS_DESC = (
    "Linguard (Lexsi AI Safety hackathon) — SafeTune CAA steering vectors and "
    "related model artifacts for Tiny Aya Earth multilingual Nigerian-language safety. "
    "Demo Space: https://huggingface.co/spaces/Esimuda/linguard · "
    "Repo: https://github.com/Esimuda/linguard"
)
DATASETS_DESC = (
    "Linguard safety datasets — multilingual red-team seeds (EN/PCM/YO/HA/IG), "
    "held-out CAA calibration, CuratorKIT repair exports, and live eval transcripts. "
    "Repo: https://github.com/Esimuda/linguard"
)


def _find_collection(api: HfApi, title: str) -> Optional[object]:
    for col in api.list_collections(owner=OWNER):
        if getattr(col, "title", None) == title:
            return col
    return None


def _ensure_collection(api: HfApi, title: str, description: str) -> str:
    description = description[:150]
    existing = _find_collection(api, title)
    if existing is not None:
        slug = existing.slug
        # Keep description fresh when re-run
        try:
            api.update_collection_metadata(
                collection_slug=slug,
                description=description,
                private=False,
            )
        except Exception:
            pass
        return slug
    col = api.create_collection(
        title=title,
        namespace=OWNER,
        description=description,
        private=False,
        exists_ok=True,
    )
    return col.slug


def main() -> int:
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if not token:
        print("HF_TOKEN (or HUGGING_FACE_HUB_TOKEN) required", file=sys.stderr)
        return 2
    api = HfApi(token=token)
    who = api.whoami()
    if who.get("name") != OWNER:
        print(f"warning: authenticated as {who.get('name')!r}, expected {OWNER!r}", file=sys.stderr)

    try:
        models_slug = _ensure_collection(api, MODELS_TITLE, MODELS_DESC)
        datasets_slug = _ensure_collection(api, DATASETS_TITLE, DATASETS_DESC)
    except HfHubHTTPError as exc:
        msg = str(exc)
        if '403' in msg:
            print('BLOCKED: token lacks collection write permission. Use an HF token with "Write access to collections" (or a classic write token).', file=sys.stderr)
            return 4
        if '429' in msg or 'rate limit' in msg.lower():
            print('BLOCKED: HF collection creation rate limit (new-user ~6/day). Retry in ~24h.', file=sys.stderr)
            print('Expected URLs once created:')
            print('  https://huggingface.co/collections/Esimuda/linguard-models')
            print('  https://huggingface.co/collections/Esimuda/linguard-datasets')
            print('(exact slug may include a numeric suffix; script prints real URLs on success)')
            return 3
        raise

    api.add_collection_item(
        models_slug,
        item_id=f"{OWNER}/linguard-caa-vectors",
        item_type="model",
        note="SafeTune CAA steering vectors for Tiny Aya Earth (inference-time harden).",
        exists_ok=True,
    )
    for repo, note in (
        ("linguard-tiny-aya-earth-lora", "LoRA safety adapter: ASR 39.5% -> 1.3%, over-refusal 0% on 120 held-out seeds."),
        ("linguard-circuit", "CircuitKIT EAP-IG refusal-circuit pruned checkpoint (exploratory, not evaluated)."),
    ):
        try:
            api.add_collection_item(models_slug, item_id=f"{OWNER}/{repo}", item_type="model", note=note, exists_ok=True)
        except Exception as exc:
            print(f"note: could not add {repo}: {exc}", file=sys.stderr)
    # Space as a related artifact on the models collection
    try:
        api.add_collection_item(
            models_slug,
            item_id=f"{OWNER}/linguard",
            item_type="space",
            note="Public demo Space for Linguard before/after metrics.",
            exists_ok=True,
        )
    except Exception as exc:
        print(f"note: could not add Space to models collection: {exc}", file=sys.stderr)

    api.add_collection_item(
        datasets_slug,
        item_id=f"{OWNER}/linguard-safety",
        item_type="dataset",
        note="Seeds, calibration, CuratorKIT repair set, live transcripts.",
        exists_ok=True,
    )

    models_url = f"https://huggingface.co/collections/{models_slug}"
    datasets_url = f"https://huggingface.co/collections/{datasets_slug}"
    print("models_collection", models_url)
    print("datasets_collection", datasets_url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
