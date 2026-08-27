---
type: source-summary
source_id: src-2026-08-26-alex-zhang-speculative-programmatic-tool-calling
source_title: "Speculative Programmatic Tool Calling"
source_author: Alex L. Zhang
source_url: https://alexzhang13.github.io/blog/2026/spec-ptc/
created: 2026-08-26
updated: 2026-08-26
tags:
  - source/summary
  - programmatic-tool-calling
  - agent-harness
  - speculative-execution
  - inference-latency
status: active
---

# Alex L. Zhang - Speculative Programmatic Tool Calling

## Summary

A harness-design proposal: when an agent's action space is **code in a REPL** rather than JSON tool calls, the harness can start executing tool calls it finds in the *partially generated* code, before the model has finished streaming. If the finished program does call them, they return immediately from cache. The author calls this **speculative programmatic tool calling (sPTC)** and positions it as the code-execution analogue of CPU speculative execution and of [[Speculative Decoding]].

The premise is stated up front and is a strong one: code in a REPL is the only tool a system needs, and every other tool should be a function inside that code. The article is written from the author's Recursive Language Model (RLM) work, where the functions being speculated are themselves sub-LLM calls.

## Key claims

- **Two distinct savings exist.** First, overlapping tool execution with token streaming — most harnesses wait for the entire generation to finish before executing anything, an inheritance from JSON tool calling where waiting cost little. Second, acting as a **naive JIT compiler**: programs routinely contain independent sub-agent calls written synchronously that could have run in parallel.
- **Speculation is worth more for code than for JSON.** With standard tool calling, by the time enough tokens exist to fully specify the call there is usually little generation left to overlap with. A program's runtime is unknown and its call structure is far richer, so there is much more room.
- **The mechanism is a shadow REPL.** A deepcopy fork of the real REPL executes the partial program as it streams. Speculatable tools are replaced in a shadowed namespace with versions that launch a promise and register it; the real tools later draw from that store. Functions with side effects (`open`, most external libraries) are marked unsafe, and any tool whose inputs depend on them is not speculated.
- **The speculator is deliberately not the executor.** Partial code may be error-prone or incomplete, so the shadow REPL never mutates real state — the REPL cell stays the unit of computation.
- **Four speculation cases, in increasing difficulty:** literal inputs parse immediately; inputs with *safe* dependencies are speculated and chained (a call waits on the call it depends on, still during streaming); some in-memory dependencies are "peekable" from the shadow namespace and some are not; and anything depending on a blocked function is refused.
- **Non-deterministic identical calls must be tracked separately**, or a single speculated result would wrongly route to every copy — which matters directly for majority-vote-over-sub-agents patterns.
- **Measured speedups are modest: roughly 1–1.2×** on OOLONG (trec-coarse, 132k) and OOLONG-Pairs (32k), with `Qwen3-30B-A3B-Instruct-0527` on 8×H100 via vLLM, 5 runs each at 4 and 8 concurrent runs, tested at both temperature 0.7 and 0.0.
- **The benefit is regime-dependent.** For locally run models the engine is memory-bound decoding the main context, so speculation raises [[Arithmetic Intensity and the Roofline Model|arithmetic intensity]]. For high-volume API serving the batching is abstracted away, so the gain comes purely from overlap.
- **Overhead is small but the failure mode is not.** Parsing is cheap and the deepcopy is cheap relative to REPL data. The worst case is a tool serving engine clogged with speculated requests that were never needed.

## Why it matters

This is the vault's first source on **programmatic tool calling as a paradigm** rather than as a vendor feature, and its first on speculation *above* the token level. It also supplies a prior-art map the vault had none of: Conveyor (2024) for tool partial execution during decoding, Speculative Interaction Agents (2026) which formalizes speculative tool calling and targets TTFT, and AsyncFC (2026) for future-based async wrappers — with the author's caveat that AsyncFC risks diverging from the original harness trajectory.

The deeper point for agent design is that **the action space determines the optimization surface.** JSON tool calling offers almost no overlap; code offers a compiler's worth. Choosing code as the action space buys latency headroom that did not previously exist.

## Tensions and open questions

- **The measured gains are small and the author says so plainly** — 1–1.2×, with an explicit warning that exact speedups are near-impossible to estimate because they depend on tool latency, token count, engine load, and the trajectory the harness happens to take. A separate "more deterministic" suite showing better numbers was omitted as too specific, which means the reported figure is the conservative one but also that the favourable case is unpublished.
- Single-author blog post with an accompanying implementation, not peer-reviewed. The evaluation is one model family on two datasets from one paper.
- **Speculating sub-agent calls spends real money and real tokens on work that may be discarded.** The article treats this as a queueing concern; it is also a cost and a rate-limit concern that goes unquantified.
- The safety analysis covers *purity* (side effects on local state) but not *authority*. Speculatively executing a partially generated program means acting on an intention the model has not finished forming — a governance question [[Agent Security and Governance]] would ask and this source does not.
- The allowlist approach ("most external libraries marked unsafe") is conservative today; the author notes the ideal is "a whole pseudo-compiler," which is unbuilt.
- Language and harness coverage is currently `{Python, bash, Bun} × {coding harness, RLM, game agent}` — portability is asserted, not demonstrated.

## Affected pages

- [[Agent Security and Governance]]
- [[Alex L. Zhang]] - new
- [[Coding Agent Harness]]
- [[Context Engineering]]
- [[LLM Inference]]
- [[Programmatic Tool Calling]] - new
- [[Speculative Decoding]]
- [[Speculative Tool Execution]] - new
- [[Tool Use and Function Calling]]

## Raw capture

- [[2026-08-26 Alex L. Zhang - Speculative Programmatic Tool Calling]]

## Citations

- Implementation: `github.com/alexzhang13/spec-ptc`
- Xu et al. (2024), *Conveyor: Efficient Tool-aware LLM Serving with Tool Partial Execution*, arXiv:2406.00059
- Hooper et al. (2026), *Speculative Interaction Agents: Building Real-Time Agents with Asynchronous I/O and Speculative Tool Calling*, arXiv:2605.13360
- Feng et al. (2026), *Concurrency without Model Changes: Future-based Asynchronous Function Calling for LLMs*, arXiv:2605.15077
- Recursive Language Models, arXiv:2512.24601
- OOLONG, arXiv:2511.02817
- Compute provided by Laude; idea proofread by the author's advisor Omar Khattab.

## Related pages

- [[Programmatic Tool Calling]]
- [[Speculative Tool Execution]]
- [[Alex L. Zhang]]
- [[Tool Use and Function Calling]]
- [[Coding Agent Harness]]
- [[Speculative Decoding]]
- [[LLM Inference]]
- [[AI Knowledge Base Overview]]
- [[Arithmetic Intensity and the Roofline Model]]

