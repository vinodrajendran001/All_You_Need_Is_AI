---
type: source-summary
created: 2026-06-03
updated: 2026-06-03
source_id: src-2026-06-03-fareed-khan-train-llm-from-scratch
source_title: Train LLM From Scratch
source_author: Fareed Khan
source_url: https://github.com/FareedKhan-dev/train-llm-from-scratch
tags:
  - source-summary
  - llm
  - transformer
  - pytorch
  - code-first
source_ids:
  - src-2026-06-03-fareed-khan-train-llm-from-scratch
status: active
---

# Fareed Khan - Train LLM From Scratch

## Overview

This source is a code-first GitHub repository for training a small GPT-style language model in PyTorch. Its main value for the vault is **end-to-end cohesion**: one repo covers raw-data download, tokenization, HDF5 serialization, batch iteration, decoder-only Transformer implementation, training, checkpointing, and text generation. Instead of explaining LLM training only through isolated tutorials, it shows the whole pipeline as a runnable project.

The repo is also useful as a practical bridge between the vault's existing learning sources. [[The Pocket - PocketFlow Tutorial Docs]] and [[Han Fang - PyTorch Practice]] explain components and training mechanics separately; this repository connects those pieces into a single pretraining workflow grounded in real files and scripts.

## Durable claims

1. The repository uses **The Pile** as its pretraining corpus and frames large-scale language-model training as something that can still be meaningfully explored under constrained hardware by scaling down model size and data volume.
2. Preprocessing uses OpenAI's `tiktoken` with the `r50k_base` tokenizer and appends `<|endoftext|>` delimiters before packing tokens into HDF5 files, turning raw `.jsonl.zst` text into contiguous training arrays.
3. The main model is a **decoder-only Transformer** with learned token embeddings, learned absolute position embeddings, stacked Transformer blocks, final layer normalization, and a linear LM head.
4. Attention is implemented with causal masking via a lower-triangular buffer, then extended from single-head to multi-head attention before being combined with an MLP and residual connections inside each block.
5. Training uses a plain **AdamW** loop with periodic train/dev loss estimation, a fixed learning-rate decay step, and checkpoint saves that include optimizer state plus loss history.
6. The README argues that roughly **13M-parameter** models are where grammatical output starts to become useful on modest hardware, making smaller, domain-specific models a realistic target for private or narrow-use deployments.
7. The repository root also includes a separate `sft_rlhf_guide.ipynb`, indicating that the project extends beyond base pretraining toward post-training topics.

## Content map

- `README.md` — walkthrough of dataset choice, hardware assumptions, code structure, usage, and a line-by-line explanation of the training stack.
- `scripts/data_download.py` — downloads The Pile shards into local train/validation directories.
- `scripts/data_preprocess.py` — tokenizes text with `tiktoken` and stores tokens in HDF5 datasets.
- `data_loader/data_loader.py` — provides batch iterators over tokenized training data.
- `src/models/*.py` — implements MLP, attention, Transformer blocks, and the main Transformer model.
- `scripts/train_transformer.py` — runs the training loop, evaluation, learning-rate decay, and checkpointing.
- `scripts/generate_text.py` — loads a trained checkpoint and generates autoregressive samples.
- `sft_rlhf_guide.ipynb` — separate notebook suggesting the repo's scope expands into supervised fine-tuning and RLHF topics.

## Why it matters

This source strengthens the vault's code-first LLM branch. It is particularly useful for readers who already know the theory but want to see how a minimal pretraining stack is actually wired together across scripts, config, model modules, and data pipelines.

## Affected pages

- [[Transformer Architecture]]
- [[LLM Training Pipeline]]
- [[Neural Network Fundamentals]]
- [[Fareed Khan]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture note: [[2026-06-03 Fareed Khan - Train LLM From Scratch]]
- README snapshot: [local asset](../../raw/assets/2026-06-03%20Fareed%20Khan%20-%20Train%20LLM%20From%20Scratch%20README.md)

## Related pages

- [[Fareed Khan]]
- [[Transformer Architecture]]
- [[LLM Training Pipeline]]
- [[Neural Network Fundamentals]]
- [[Han Fang - PyTorch Practice]]
- [[The Pocket - PocketFlow Tutorial Docs]]
- [[AI Knowledge Base Overview]]
