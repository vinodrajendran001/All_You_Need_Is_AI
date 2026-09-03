---
type: entity
entity_kind: person
created: 2026-09-03
updated: 2026-09-03
tags: [entity, author, newsletter, open-models]
source_ids:
  - src-2026-08-30-adlrocha-base-models-bottleneck
status: active
---

# adlrocha

The author of a Substack newsletter that reads open-weight model releases closely — model cards, configs and
inference defaults — and works out what the engineering choices imply.

## Why they matter to this vault

[[adlrocha - Base Models Stopped Being the Bottleneck]] is the vault's clearest statement of a thesis it had
been assembling from fragments: that the scarce resource in frontier model building has moved from the base
model to the machinery trained on top of it. The post reads [[Z.ai]]'s GLM-5.3 and [[Qwen]]'s Qwen3.8-27B
against each other and extracts the shared conclusion, and it is the originating source for
[[RL Environment Design]].

The value of this author to the vault is a particular reading habit: noticing that a config still declares
`model_type: qwen3_5`, that `preserve_thinking` is on by default, that coding benchmarks were run through the
Claude Code harness. These are the details that decide what a release actually means, and they are usually
absent from coverage that works from the benchmark table.

## Caveats

This is a practitioner blog, not an evaluation. Benchmark figures and quoted claims originate with the model
vendors and are not independently verified. The author mixes personal vibe-testing with model-card reading and
is explicit about which is which, and is equally explicit that the **distillation question is unsettled**.

## Related pages

- [[adlrocha - Base Models Stopped Being the Bottleneck]]
- [[Z.ai]]
- [[Qwen]]
- [[RL Environment Design]]
- [[Open Model Ecosystems]]
- [[Reasoning Effort Control]]
- [[Harness Optimization]]
