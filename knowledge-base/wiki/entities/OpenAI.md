---
type: entity
created: 2026-07-03
updated: 2026-07-03
entity_kind: organization
tags:
  - entity
  - organization
  - voice-ai
  - infrastructure
source_ids:
  - src-2026-07-03-bytebytego-openai-voice
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

## Related pages

- [[ByteByteGo - How OpenAI Delivers Low-Latency Voice AI]]
- [[Real-Time Voice AI]]
- [[ML Systems at Scale]]
- [[Coding Agent Harness]]
- [[AI Knowledge Base Overview]]
