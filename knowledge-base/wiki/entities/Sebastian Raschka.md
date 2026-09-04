---
type: entity
created: 2026-07-03
updated: 2026-09-04
entity_kind: person
tags:
  - entity
  - person
  - educator
  - local-llm
  - coding-agents
source_ids:
  - src-2026-07-03-sebastian-raschka-local-coding-agents
  - src-2026-07-20-raschka-reasoning-effort
  - src-2026-09-02-raschka-astra-looped-transformers
status: active
---

# Sebastian Raschka

## What it is

Sebastian Raschka (PhD) is an AI researcher and educator, author of the *Build a Large Language Model (From Scratch)* and *Build a Reasoning Model (From Scratch)* books and the *Ahead of AI* / *Sebastian Raschka Magazine* newsletter. He is known for from-scratch, implementation-first explanations of LLM internals, training, and reasoning models.

## Why it matters here

Raschka is the author of [[Sebastian Raschka - Using Local Coding Agents]], the vault's most practical guide to running open-weight models in local coding harnesses. His perspective — implement the stack yourself to understand it, then choose the serving engine, harness, and permission model deliberately — anchors the [[Coding Agent Harness]] concept and connects the local-model side ([[Small Language Models]], [[On-Device Reasoning]]) to the agent-tooling side ([[Agentic Loop]], [[Tool Use and Function Calling]]).

## Notes

- Uses a Mac Mini (M4) and an NVIDIA DGX Spark as his local hardware, alternating Codex and Claude Code as daily drivers while testing local setups.
- Publishes reproducible evaluation code (e.g., the `local-coding-agent-evals` repository) alongside his articles.

## Reasoning effort as a training artifact

[[Sebastian Raschka - Controlling Reasoning Effort in LLMs]] extends his role in this vault from
practical local-model guidance into post-training mechanics. The post surveys how six models
(DeepSeek V4, Nemotron 3 Ultra, Kimi K2.5, GLM-5, Qwen3, Inkling) install low/medium/high effort
controls, and establishes for this vault that **`<think>` tags are cosmetic** — delimiters learned
from a format reward, not a reasoning mechanism. It anchors [[Reasoning Effort Control]].

Characteristically, he marks the boundary of his own evidence: GPT-5.6's internals are unknown, and
his proposed diagram is labelled "a possible implementation, not a confirmed description." That
labelling discipline is why his posts are usable as reference material in this vault.

## Debunking as a contribution

[[Sebastian Raschka - OpenAI Astra and Looped Transformers]] is a different kind of post from his usual
implementation-first explainers, and useful to this vault for that reason: it is a **short corrective written
against press coverage.** The claim under repair was that OpenAI's Astra uses a "recurrent depth" technique that
obscures the model's chain of thought. His reply separates two things the coverage had merged — that looping is
*"just reusing layers,"* and that reducing legible reasoning is a consequence of capacity rather than of
recurrence, since *"we would get the same effect if we were scaling up the model size."*

The characteristic discipline is intact. He states what he is reasoning from (published models described
similarly, not Astra itself), relays Nanbeige's **~75% token-efficiency retention at two passes** as the
publisher's figure rather than as verified, allows that the journalist may have meant a different technique, and
labels the latent-computation account as *"the only plausible interpretation"* rather than as fact. His verdict
is proportionate rather than dismissive: *"Astra may be a really good model, but this shouldn't be about this
'looped transformer aspect,' which is just a tiny architectural tweak."*

He anchors [[Recursive Architectures]] with this vault's first shipped configuration for layer reuse, and
supplies the correction that reframes [[Chain-of-Thought Monitoring]].

## Related pages

- [[Sebastian Raschka - Using Local Coding Agents]]
- [[Coding Agent Harness]]
- [[Small Language Models]]
- [[On-Device Reasoning]]
- [[AI Knowledge Base Overview]]
- [[Reasoning Effort Control]]
- [[Reasoning Compression]]
- [[Test-Time Scaling]]
- [[Sebastian Raschka - Controlling Reasoning Effort in LLMs]]
- [[Sebastian Raschka - OpenAI Astra and Looped Transformers]]
- [[Recursive Architectures]]
- [[Chain-of-Thought Monitoring]]
- [[Latent-Space Reasoning]]
