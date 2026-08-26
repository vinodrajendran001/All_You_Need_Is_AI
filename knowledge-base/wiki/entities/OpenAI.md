---
type: entity
created: 2026-07-03
updated: 2026-08-26
entity_kind: organization
tags:
  - entity
  - organization
  - voice-ai
  - infrastructure
source_ids:
  - src-2026-07-03-bytebytego-openai-voice
  - src-2026-08-24-openai-builders-guide-gpt-5-6
  - src-2026-08-25-bytebytego-stealing-reasoning-traces
status: active
---

# OpenAI

## What it is

OpenAI is the AI research and product company behind ChatGPT, the GPT model family, and the Realtime API. Beyond model research, it operates large-scale serving infrastructure, including the WebRTC voice stack that carries real-time spoken conversation to roughly 900 million weekly active users.

## Why it matters here

OpenAI enters the vault as the subject of [[ByteByteGo - How OpenAI Delivers Low-Latency Voice AI]], the clearest production real-time-systems case study currently held here. Its **relay/transceiver** split and **ICE-ufrag first-packet routing** are the transport-infrastructure half of the [[Real-Time Voice AI]] concept, and they illustrate the same data-locality laws catalogued in [[ML Systems at Scale]]. OpenAI's employment of original WebRTC architects (Justin Uberti) and the Pion library maintainer (Sean DuBois) is why the design carries unusual protocol depth.

## Notes

- Also appears indirectly across the vault as a reference point for frontier models (GPT family), agent harnesses (Codex), and post-training recipes.
- The voice architecture is deliberately optimised for 1:1 (user ↔ model) sessions rather than multiparty calls.
- [[OpenAI - The Builder's Guide to GPT-5.6]] adds vendor guidance on selecting model variants and reasoning effort, programmatic tool calling, prompt caching, and orchestrator/worker allocation.

## Reasoning-block exposure

[[ByteByteGo - How to Steal an AI Model's Private Thoughts]] reports that OpenAI returns encrypted reasoning state in a field named `encrypted_content`, and that acceptance is **organised by generation**: the GPT-5.6 series accepted blocks from all earlier generations, while older models accepted only their own. That is a narrower surface than Claude's or Gemini's, though not a closed one.

Extraction from GPT was correspondingly harder — up to 50 candidate extractions per block, with output chunked below roughly 50 tokens to avoid a rejection triggered by verbatim reproduction. GPT-5.6 Sol was also the target in the demonstrated prompt-injection vector, where a block carrying an upload instruction was ported into an unrelated slide-editing conversation and executed. See [[Reasoning Trace Privacy]].

The related finding worth carrying forward: recovered GPT traces are frequently **not fluent English** but compressed telegraphic notes with articles dropped and grammar abandoned — which complicates any oversight scheme that assumes traces are readable.

## Related pages

- [[ByteByteGo - How OpenAI Delivers Low-Latency Voice AI]]
- [[Real-Time Voice AI]]
- [[ML Systems at Scale]]
- [[Coding Agent Harness]]
- [[AI Knowledge Base Overview]]
- [[OpenAI - The Builder's Guide to GPT-5.6]]
- [[Model Routing]]
- [[ByteByteGo - How to Steal an AI Model's Private Thoughts]]
- [[Reasoning Trace Privacy]]
- [[Programmatic Tool Calling]]
