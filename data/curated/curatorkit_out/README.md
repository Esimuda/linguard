---
tags:
- curatorkit
configs:
- config_name: sft_alpaca
  default: true
  description: curatorkit sft_alpaca export, sha256 eff64fe4c3d8a179b80477705c9ed0661cc3f2dc5764651cc7f8b63e372874b5
  data_files:
  - split: train
    path: sft_alpaca.jsonl
- config_name: sft_messages
  description: curatorkit sft_messages export, sha256 68cd26b4f51a6337e58bcac5ac91f24276533b09c8bf69210ec5f7fa52fc68e1
  data_files:
  - split: train
    path: sft_messages.jsonl
---

# Dataset Card: linguard_repair

## Summary

- **Run timestamp**: 2026-11-01T15:43:57.994116Z
- **Wall clock time**: 0.0s
- **Pipeline config hash**: `1d7e37eddaffe26c`

## Source Documents

  - Unknown

## Pipeline Stages

| Step | Input | Passed | Recovered | Rejected | Forward |
|------|-------|--------|-----------|----------|---------|
| JSONLReader | 34 | 34 | — | 0 | 34 |
| SchemaGate | 34 | 34 | 0 | 0 | 34 |
| ExactDeduplicator | 34 | 34 | — | — | 34 |
| TextCleaner | 34 | 34 | — | — | 34 |
| AlpacaExporter | — | 34 | — | — | 34 |
| MessagesExporter | — | 34 | — | — | 34 |

## Gate Pass Rates and Rejection Breakdown

- **JSONLReader**: 34/0 passed (N/A), 0 rejected
- **SchemaGate**: 34/34 passed (100.0%), 0 rejected


**Rejection reasons:**
  - None

## Deduplication

  - exact_duplicates_removed: 0

## Known Limitations

- No MinHash deduplication applied.
- Table extraction requires `extract_tables: true` on the PDF reader and MinerU with GPU support. Disabled by default.
- Token counting uses a whitespace tokenizer by default. For exact LLM context window
  enforcement, enable `use_tiktoken: true` in the SchemaGate config.
- Both within-run (MinHash/Diversity) and cross-run (EmbeddingDeduplicator) deduplication
  are available. Cross-run dedup persists an embedding index across runs; use
  `embedding_reset_index: true` to start fresh.

## Reproduction

```bash
pip install curatorkit
curatorkit run pipeline.yaml --output-dir ./out/
```

## Tool Versions

- **curatorkit**: 0.1.22
- **python**: 3.13.5

## Configs

Load one with `datasets.load_dataset("<this folder or Hub repo>", "<config>")`.

| Config | Splits (rows) | Columns |
|--------|---------------|---------|
| `sft_alpaca` | train (34) | `instruction`: string<br>`input`: string (empty when there is no input)<br>`output`: string |
| `sft_messages` | train (34) | `messages`: list of {role, content}; role is system, user or assistant |
