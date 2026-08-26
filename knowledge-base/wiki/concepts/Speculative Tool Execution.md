---
type: concept
created: 2026-08-26
updated: 2026-08-26
tags:
  - concept
  - ai-agents
  - agent-harness
  - inference-latency
  - speculative-execution
source_ids:
  - src-2026-08-26-alex-zhang-speculative-programmatic-tool-calling
status: active
---

# Speculative Tool Execution

## Definition

**Speculative tool execution** starts running an agent's tool calls before the model has finished deciding to make them — parsing calls out of a partially generated response and launching them, so that if the finished response does invoke them, the results are already available. It is the harness-level analogue of CPU speculative execution and of [[Speculative Decoding]], moved up a layer: instead of guessing tokens, the harness guesses *actions*.

## Why it matters

Agent latency is dominated by two serial waits: the model generating its turn, and the tools then running. Most harnesses execute these strictly in order, an inheritance from JSON tool calling where the overlap was not worth chasing. Speculation collapses the two waits into one — and the effect is largest exactly where agents hurt most, when the tools are themselves slow LLM or sub-agent calls.

There is a second, less obvious win. Model-written programs routinely express independent work sequentially, because writing correct async code is harder than writing straight-line code. A speculating harness recovers that parallelism without the model having to ask for it, acting as a naive JIT compiler over the agent's own actions.

## Why it needs code as the action space

The technique is much weaker under JSON tool calling, for a structural reason: by the time the model has emitted enough tokens to fully specify a JSON call, there is usually little generation left to overlap it with. A program is different — its runtime is unknown, its call structure is rich, and calls can appear early in a long generation. [[Programmatic Tool Calling]] is therefore not just a compatible design but close to a precondition.

## The mechanism

[[Alex L. Zhang - Speculative Programmatic Tool Calling]] implements this with a **shadow REPL**: a deepcopy fork of the real interpreter that executes the partial program as it streams. Tools marked speculatable are swapped, in the shadow namespace, for versions that launch a promise and register it in a store; the real tools later resolve from that store or execute normally if no speculation exists.

Two design decisions carry most of the weight:

- **The speculator never becomes the executor.** Partial code may be malformed or incomplete, so the shadow REPL must not mutate real state. The REPL cell stays the unit of computation.
- **Purity gates everything.** Functions with side effects — `open`, most external libraries — are marked unsafe, and any tool whose *inputs* depend on them is not speculated at all.

## What can and cannot be speculated

The difficulty ladder, from the same source:

| Case | Speculatable? |
| --- | --- |
| Inputs are literals | Yes, parsed immediately without executing anything |
| Inputs depend on other *safe* values | Yes, and chained — a call waits on its dependency, still during streaming |
| Inputs depend on in-memory variables | Only if "peekable" from the shadow namespace |
| Inputs depend on a blocked function | No |
| Calls inside conditionals or loops | Only if the guard can be safely evaluated |

Identical non-deterministic calls must be tracked as distinct instances, or one speculated result would wrongly satisfy all of them — which breaks precisely the majority-vote-over-sub-agents pattern that motivates speculation in the first place.

## What it is worth

Measured speedups were **roughly 1–1.2×** on OOLONG and OOLONG-Pairs with a 30B MoE model on 8×H100 via vLLM. The author is explicit that exact speedups are near-impossible to estimate, since they depend on tool latency, tokens generated, engine load, and the trajectory the harness takes.

The benefit is also regime-dependent in a way that connects to [[Arithmetic Intensity and the Roofline Model]]. On a locally served model the engine is memory-bound decoding the main context, so speculative sub-calls consume compute that was otherwise idle — the speculation is close to free. Behind a high-volume API the batching is abstracted away, so the only gain is the overlap itself.

The worst case is a tool-serving engine clogged with speculated requests that were never needed.

## Prior art

- **Conveyor** (Xu et al., 2024) lets users declare partial-execution opportunities parsed during decoding.
- **Speculative Interaction Agents** (Hooper et al., 2026) formalizes the idea as *speculative tool calling* and targets time-to-first-token by overlapping long thinking chains with invoked tools.
- **AsyncFC** (Feng et al., 2026) wraps function calls in futures without model changes — with the standing objection that this risks diverging from the original harness trajectory.

## Open questions

- **Speculation spends money on discarded work.** Pre-launching sub-agent calls burns tokens and rate limit on branches never taken. The cost side is acknowledged as a queueing concern but is unquantified.
- Purity is analysed; **authority is not**. Executing a partially generated program acts on an intention the model has not finished forming — a distinction [[Agent Security and Governance]] cares about and this line of work has not yet addressed. Should speculation be forbidden for anything that requires approval?
- The allowlist is conservative by necessity. The author's own framing is that the ideal is "a whole pseudo-compiler," which does not exist.
- Does speculation change what the model should be trained to write — for instance, rewarding programs whose calls are speculation-friendly?
- How does this compose with [[Prefill-Decode Disaggregation]] and prefix reuse, where speculated sub-calls contend for the same serving pool as the main generation?

## Related pages

- [[Alex L. Zhang - Speculative Programmatic Tool Calling]]
- [[Programmatic Tool Calling]]
- [[Speculative Decoding]]
- [[Coding Agent Harness]]
- [[Tool Use and Function Calling]]
- [[Agent Security and Governance]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[LLM Inference]]
- [[Inference Serving Engines]]
- [[Agent Planning]]
