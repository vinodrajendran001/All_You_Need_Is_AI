---
type: source-summary
created: 2026-09-25
updated: 2026-09-25
source_id: src-2026-09-22-bytebytego-openai-gpt-live
source_title: "How OpenAI Built GPT-Live"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-openai-built-gpt-live
tags: [source/summary, voice-ai, real-time, inference]
source_ids: [src-2026-09-22-bytebytego-openai-gpt-live]
status: active
---

# ByteByteGo - How OpenAI Built GPT-Live

## Summary

This secondary account describes GPT-Live as a full-duplex voice system that continuously consumes
and emits audio rather than waiting for explicit turn boundaries. It separates a millisecond-sensitive
live voice model from slower asynchronous reasoning and tool work.

## Key claims

- Full duplex learns endpointing and interruption behavior from the audio stream, including silence,
  rather than placing a turn detector before the model.
- Separate live and asynchronous serving paths keep tool latency from blocking the conversational
  stream; conversation state stays resident so only new audio frames need processing.
- WARP reportedly reduces WebRTC setup from six round trips to one. A **60 ms** mobile round trip
  makes the six-round-trip path exceed **0.3 seconds**, but that is an illustrative calculation.
- Warm handoff transfers a session to another model instance during scaling, failure, or context
  compaction. OpenAI reportedly engineers around **p999**, not only p95/p99.

## Why it matters

Real-time voice is a continuously scheduled stateful stream, not ordinary request/response inference.
Its architecture must isolate the speaking loop while allowing slower reasoning to proceed in parallel.

## Tensions and caveats

ByteByteGo relies partly on conversations with OpenAI engineers. GPT-Live behavior, WARP, the p999
practice, and a reported CPU-side launch bottleneck are not accompanied by public latency, quality,
cost, concurrency, or reliability datasets.

## Raw capture

- [[2026-09-22 ByteByteGo - How OpenAI Built GPT-Live]]

## Affected pages

- [[Real-Time Voice AI]]
- [[OpenAI]]
- [[ByteByteGo]]

## Related pages

- [[LLM Inference]]
- [[Agent Delegation]]
- [[Context Engineering]]
