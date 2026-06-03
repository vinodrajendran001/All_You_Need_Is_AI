---
type: raw-source
source_id: src-2026-06-03-fareed-khan-train-llm-from-scratch
title: Train LLM From Scratch
author: Fareed Khan
url: https://github.com/FareedKhan-dev/train-llm-from-scratch
captured: 2026-06-03
repo_owner: FareedKhan-dev
repo_name: train-llm-from-scratch
inspected_commit: f3524df6413b66145d6a91b151d412807a442632
inspected_commit_date: 2026-05-22
license: MIT
asset_readme: 2026-06-03 Fareed Khan - Train LLM From Scratch README.md
asset_readme_sha256: 1688fec7660f901ae606a7a5fc5b4d6c2792f7e1115095c00a7009eba46a2440
asset_readme_size_bytes: 60650
status: immutable
tags:
  - source/raw
  - github-repo
  - llm
  - transformer
  - pytorch
---

> Canonical local capture:
> - [README snapshot](../assets/2026-06-03%20Fareed%20Khan%20-%20Train%20LLM%20From%20Scratch%20README.md)

# Train LLM From Scratch

## Metadata

- **Author / owner:** Fareed Khan (`FareedKhan-dev`)
- **Repository URL:** https://github.com/FareedKhan-dev/train-llm-from-scratch
- **Inspected commit:** `f3524df6413b66145d6a91b151d412807a442632`
- **License:** MIT

## Root layout

- `README.md`
- `config/config.py`
- `data_loader/data_loader.py`
- `scripts/data_download.py`
- `scripts/data_preprocess.py`
- `scripts/train_transformer.py`
- `scripts/generate_text.py`
- `src/models/attention.py`
- `src/models/mlp.py`
- `src/models/transformer_block.py`
- `src/models/transformer.py`
- `sft_rlhf_guide.ipynb`

## Capture notes

- The local raw capture for this source is the repository README pinned to the inspected commit.
- The README describes an end-to-end workflow around The Pile dataset: download raw shards, preprocess them into tokenized HDF5 files with `tiktoken`, train a decoder-only Transformer with PyTorch, and generate text from saved checkpoints.
- The repository structure also shows a separate `sft_rlhf_guide.ipynb` notebook at the root, indicating that the project extends beyond base pretraining into post-training topics.
