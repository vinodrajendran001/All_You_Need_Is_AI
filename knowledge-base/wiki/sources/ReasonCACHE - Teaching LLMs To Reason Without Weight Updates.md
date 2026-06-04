---
type: source-summary
created: 2026-06-04
updated: 2026-06-04
source_id: src-2026-06-04-reasoncache
source_title: "ReasonCACHE: Teaching LLMs To Reason Without Weight Updates"
source_author: Sharut Gupta et al.
source_url: https://arxiv.org/abs/2602.02366
tags:
  - source-summary
  - reasoning
  - icl
  - prefix-tuning
source_ids:
  - src-2026-06-04-reasoncache
status: active
---

# ReasonCACHE: Teaching LLMs To Reason Without Weight Updates

## Summary

ReasonCACHE asks whether reasoning skill can be learned without modifying model weights at all. Its answer is a prefix-tuning style mechanism that distills demonstrations into a fixed key-value cache, creating a middle ground between in-context learning and in-weight learning. Instead of stuffing many demonstrations into a growing context window, the model reasons through a reusable cache injected directly into attention.

## Key claims

- Standard ICL breaks down when scaled to many reasoning demonstrations because context length, attention cost, and shallow learning all become limiting.
- Prefix-tuning-style fixed KV caches can teach reasoning without conventional weight updates.
- ReasonCACHE can outperform naive ICL and match or exceed some in-weight learning approaches on hard reasoning benchmarks.
- The method is argued to be efficient across data, trainable-parameter count, and inference cost, while also being more expressive than low-rank weight updates in a specific theoretical sense.

## Why it matters

This source expands the vault's efficient-reasoning branch beyond token shortening. It shows that some of the same goals—fewer tokens, less context growth, less training overhead—can be achieved by **repackaging reasoning into attention state** rather than compressing visible text alone.

## Tensions / open questions

- How broadly does fixed-cache reasoning generalize beyond benchmark-heavy reasoning tasks?
- When is a distilled KV cache better than a small learned adapter or low-rank update?
- How interpretable and controllable are reasoning skills encoded this way?

## Affected pages

- [[Reasoning Compression]]
- [[Latent-Space Reasoning]]
- [[LLM Training Pipeline]]

## Citations

- Raw capture note: `knowledge-base/raw/sources/2026-06-04 Sharut Gupta et al - ReasonCACHE - Teaching LLMs To Reason Without Weight Updates.md`
- Local PDF: [2026-06-04 Sharut Gupta et al - ReasonCACHE - Teaching LLMs To Reason Without Weight Updates.pdf](../../raw/sources/2026-06-04%20Sharut%20Gupta%20et%20al%20-%20ReasonCACHE%20-%20Teaching%20LLMs%20To%20Reason%20Without%20Weight%20Updates.pdf)

## Related pages

- [[Reasoning Compression]]
- [[Latent-Space Reasoning]]
- [[LLM Training Pipeline]]
- [[On-Device Reasoning]]
