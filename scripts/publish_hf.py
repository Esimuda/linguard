"""Publish Linguard artifacts to HF Hub under Esimuda/linguard-* (reads HF_TOKEN from env; never prints it)."""
import json, os
from pathlib import Path
from huggingface_hub import HfApi

ROOT = Path(__file__).resolve().parents[1]
api = HfApi(token=os.environ["HF_TOKEN"])
DS, SP, VEC = "Esimuda/linguard-safety", "Esimuda/linguard", "Esimuda/linguard-caa-vectors"

api.create_repo(DS, repo_type="dataset", exist_ok=True)
card = (ROOT / "docs" / "HF_DATASET_CARD.md").read_text()
api.upload_file(path_or_fileobj=card.encode(), path_in_repo="README.md", repo_id=DS, repo_type="dataset")
api.upload_folder(folder_path=str(ROOT / "data" / "seeds"), path_in_repo="seeds", repo_id=DS, repo_type="dataset")
api.upload_folder(folder_path=str(ROOT / "data" / "calibration"), path_in_repo="calibration", repo_id=DS, repo_type="dataset")
api.upload_folder(folder_path=str(ROOT / "data" / "curated" / "curatorkit_out"), path_in_repo="curated", repo_id=DS, repo_type="dataset")
api.upload_folder(folder_path=str(ROOT / "data" / "results" / "live"), path_in_repo="results", repo_id=DS, repo_type="dataset", ignore_patterns=["*.pt"])

api.create_repo(VEC, repo_type="model", exist_ok=True)
api.upload_file(path_or_fileobj=str(ROOT / "data" / "results" / "live" / "caa_vectors.pt"), path_in_repo="caa_vectors.pt", repo_id=VEC)
api.upload_file(path_or_fileobj=(
    "---\nbase_model: CohereLabs/tiny-aya-earth\nlicense: mit\ntags: [safety, steering, safetune, lexsi, linguard]\n---\n"
    "# Linguard CAA steering vectors for Tiny Aya Earth\n\nSafeTune `extract_caa_vectors` on layers 12/16/20 from the held-out "
    "calibration set (`Esimuda/linguard-safety/calibration`). Apply with `safetune.steer.CAAModel(model, torch.load('caa_vectors.pt'), strength=0.25)`.\n"
    "Inference-time harden only (no weight changes). Metrics: https://github.com/Esimuda/pidginguard\n").encode(), path_in_repo="README.md", repo_id=VEC)

api.create_repo(SP, repo_type="space", space_sdk="static", exist_ok=True)
api.upload_folder(folder_path=str(ROOT / "space"), repo_id=SP, repo_type="space")
print("published", DS, VEC, SP)
