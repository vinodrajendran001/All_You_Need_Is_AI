---
type: source-summary
created: 2026-08-03
updated: 2026-10-19
source_id: src-2026-07-29-bytebytego-chatgpt-agent-loop-optimization
source_title: "How ChatGPT Optimizes its Agent Loop: Harness, API, and Inference"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-chatgpt-optimizes-its-agent-loop
tags: [source/summary, ai-agents, inference, caching]
source_ids: [src-2026-07-29-bytebytego-chatgpt-agent-loop-optimization]
status: active
---

# ByteByteGo - How ChatGPT Optimizes its Agent Loop

## Summary

A ByteByteGo explainer based on conversations with OpenAI engineers who shipped efficiency work
into Codex and ChatGPT Work. It splits an agentic application into three layers: the **harness**
on the user's machine, which holds the conversation record, runs the loop, and executes tool calls
under approval policies in a sandbox; the **API layer**, a CPU service for validation, rate limits,
tokenization, and safety checks; and the **inference layer**, the GPU fleet. The unifying principle is avoiding repeated work:
preserve cacheable prefixes, transmit state deltas, tokenize only new input, overlap independent
work, and route requests toward reusable state.

The framing metric is **cost per successful task**. The evidence is secondary reporting of
first-party practice: techniques are described, but almost no before/after measurements are
given. A sponsored section is excluded.

## Key claims

### Why the loop repeats work

- A turn can contain many model calls. Heavy tasks "could in theory repeat more than 100 times,"
  and one extra second per call adds "roughly half a minute to a long task." Under stateless HTTP,
  each iteration resends history, retokenizes text, and reprocesses the prompt.

### Harness

- **Persistent WebSockets and incremental requests.** One connection per turn removes repeated
  TCP and TLS setup, and the harness sends only new items with a `previous_response_id`; the
  server rebuilds the full context from state it kept.
- **Stable prompt prefixes.** Prompt caching matches the prefix token by token, so one changed
  token near the front forces recomputation of everything after it. Codex once kept MCP tool
  definitions in a hash map, so the same tools serialized in varying order and tasks completed
  "just more expensively." The fix: append-only history, with volatile state such as approval
  settings enforced by the harness rather than written into the prompt.
- **Deferred tool discovery.** Of the hundreds of tools a session can expose, the prompt carries
  core tools plus a `tool_search` tool; BM25 lexical search loads other definitions on demand.
  Schema and conversation compaction also keep context small.
- **Code Mode.** The model writes a program, run in an embedded JavaScript runtime where tools are
  functions, that can fan out independent calls in parallel and return only the compact result.

### API layer

- **Tokenizing only the delta.** With a WebSocket, the API keeps the tokenized conversation in
  memory and tokenizes only new items, so per-call tokenization becomes "closer to O(1)" in the
  marginal input instead of growing with conversation length.
- **Safety checks in parallel with inference.** Prompt classifiers (for cyberoffense or bioweapon
  content, for example) run while the model processes the prompt. Some models stream immediately
  and cut the stream if a check fails; more sensitive models hold output until checks pass.
- **Routing to newer CPUs.** Behind the same machine labels OpenAI found older Broadwell and newer
  Ice Lake processors. The older ones served the same traffic with "roughly 20% worse time to first
  token, while using about twice as much CPU," so traffic shifted toward newer machines and CPU
  generation became a capacity-planning factor. This concerns the API layer's CPUs, not the GPUs.

### Inference layer

- **Cache-aware routing** weighs even load against returning a conversation to the machine holding
  its cache; load-balancing improvements alone "dramatically reduced" serving cost, with no figure.
- **KV cache management** tests eviction policies against production traces of which state is
  needed again, and optimizes movement between memory tiers.
- **Speculative decoding** is judged by average acceptance length, with output quality said not to
  change. **Prefill/decode separation** runs compute-heavy prefill and memory-heavy decode on
  separately configured machines and ships the KV cache between them.

### Lessons the engineers drew

- Keep designs simple (lexical tool search, one compaction path); use the agent on its own stack
  (Codex wrote much of the migration of the API that serves Codex, turning "years of rewrite work
  into months for a couple of engineers"); and optimize end to end with production traffic shapes,
  since offline wins can hurt in real traffic.

## Why it matters

Reuse is cross-layer: a harness that keeps prefixes stable is what lets [[KV Cache]] reuse and
cache-aware routing pay off on the GPUs, which makes cache-awareness a constraint on how
[[Agentic Loop]] code builds prompts. Deferred discovery and Code Mode connect to
[[Tool Roster Economics]] and [[Programmatic Tool Calling]].

## Tensions / open questions

- The CPU-generation comparison is the only quantified operational result, without workload or
  measurement-window details.
- The cost-per-task framing cites a vendor comparison (GPT 5.6 Sol with max reasoning above Fable 5
  on the Artificial Analysis Coding Agent Index at less than half the cost), linked to OpenAI's
  announcement rather than measured here.
- Server-held conversation state saves payload and tokenization work, but its expiry and failover
  are not discussed.
- Streaming before safety checks finish lets some tokens reach a user before a failing verdict; the
  article gives no exposure data.
- The claim that "the output quality does not change" under speculative decoding depends on the
  verification rule, which the article does not specify. Compute-heavy prefill and memory-heavy
  decode are common regimes, not fixed properties of every workload; see [[LLM Inference]].

## Affected pages

- [[Agentic Loop]]
- [[KV Cache]]

## Raw capture

- [[2026-07-30 ByteByteGo - How ChatGPT Optimizes its Agent Loop Harness, API, and Inference|How ChatGPT Optimizes its Agent Loop Harness, API, and Inference]]

## Citations

- Canonical URL: <https://blog.bytebytego.com/p/how-chatgpt-optimizes-its-agent-loop>
- Published July 29, 2026; captured July 30, 2026. The OpenAI engineers are credited by first
  name only. A sponsored section for Crusoe Serverless Fine-Tuning is excluded.

## Related pages

- [[Coding Agent Harness]]
- [[Agentic Loop]]
- [[Context Engineering]]
- [[LLM Inference]]
- [[KV Cache]]
- [[Tool Roster Economics]]
- [[Programmatic Tool Calling]]
- [[Prefill-Decode Disaggregation]]
- [[Speculative Decoding]]
- [[Inference Serving Engines]]
- [[Harness State Authority]]
- [[OpenAI]]
- [[ByteByteGo]]
