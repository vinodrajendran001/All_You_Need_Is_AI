---
type: source-summary
created: 2026-10-30
updated: 2026-10-30
source_id: src-2026-10-22-agrawal-qwenputer
source_title: "Qwenputer: a fully functioning, deterministic RISC-V CPU inside Qwen3.5"
source_author: Divyansh Agrawal
source_url: https://divagr.com/blog/qwenputer
tags:
  - source/summary
  - architecture
  - memory
  - tool-use
source_ids:
  - src-2026-10-22-agrawal-qwenputer
status: active
---

# Qwenputer: A Deterministic RISC-V CPU Inside Qwen3.5

## Summary

Divyansh Agrawal describes a compiled RISC-V computer attached to Qwen3.5-4B inside the
model's forward-pass computation. The original Qwen weights are unchanged and no training or
post-training is used. It is an architectural/programming construction, not evidence that
ordinary language-model reasoning has learned exact arithmetic.

## Key claims

- **Gated DeltaNet state becomes explicitly addressed memory.** With gate and beta fixed to
  one and one-hot keys/queries, a state row can be exactly overwritten and read. Exactness
  applies to bounded slots under these compiled conditions, not arbitrary history compressed
  by an ordinary learned recurrent model.
- **The computer is additional network machinery.** Eleven layers precede Qwen's 32 layers.
  The CPU implements RV32IM, Zba, and a small bignum unit; ADDR, VAL, and STEP trace tokens
  drive execution through forward passes.
- **Tool-like syntax does not imply an external runtime.** The language model uses a familiar
  tool-call format, but the compiled CPU performs arithmetic internally. A custom **RvChat
  driver is still required** to load firmware and prevent CPU trace tokens from reaching the
  Qwen layers; this is not a plain `generate()` replacement or a software-free system.
- **CPU tests and task accuracy measure different things.** The author reports passing
  riscv-tests/QEMU comparisons and **18 million free-running instructions** without errors,
  with roughly **230,000 output positions** matching. That does not guarantee that the
  language model always selects the right computation.
- **The benchmarks do not show universal superiority to external tools.** The reported four
  DeepMind-task scores are **97.5%, 97.5%, 100%, and 97.5%**, with mixed comparisons against
  Python-tool and base-model baselines. NUPA improves from **48.6% to 100%**, matching
  external Python rather than surpassing it.
- **Persistent explicit data can live inside recurrent state.** An experimental filesystem
  offers **1,024 directory slots**, up to **512 files / about 53,000 tokens**, and state
  saved/restored across chats. Changed-fact recall of **90% versus 30%** for replayed chats
  and a separate **83.3% versus 78.9%** Python-memory-tool comparison are different tests.

## Why it matters

[[Linear Attention and Recurrent Memory]] needs to distinguish learned compression from
compiled addressing. [[Agent Memory]] needs to separate storage location from representation:
state inside the network can hold explicit files rather than opaque learned facts.
[[Tool Use and Function Calling]] likewise cannot infer execution location from the call syntax.
The result belongs to a particular [[Qwen]] derivative, not to unmodified family checkpoints.

## Tensions / open questions

- The checkpoint is **18.8 GB**, roughly twice the base, with much zero padding; it runs on a
  single 24 GB GPU. Calculations take seconds rather than native-CPU milliseconds. Reported
  **3,200 CPU trace tokens/s on an L4** is not ordinary chat-generation throughput.
- Bounded exact memory does not contradict the inability of a fixed-size state to retain
  unbounded arbitrary history. Persistence also depends on saving/restoring that state.
- These are creator-reported tests and small task evaluations. The code was not inspected or
  executed for this ingest, and linked monitoring/hidden-reasoning follow-ups are not evidence
  captured here.
- Raw metadata incorrectly names the author as `Markdown version`; the body BibTeX identifies
  **Divyansh Agrawal**. Attribution is corrected here without changing the raw capture.

## Affected pages

- [[Linear Attention and Recurrent Memory]]
- [[Agent Memory]]
- [[Tool Use and Function Calling]]
- [[Qwen]]

## Raw capture

- [[knowledge-base/raw/sources/Qwenputer a fully functioning, deterministic RISC-V CPU inside Qwen3.5]]

## Citations

- Canonical URL: <https://divagr.com/blog/qwenputer>
- Linked implementation: <https://github.com/divagr18/qwenputer> (not independently inspected).
- Published October 22, 2026 according to capture metadata; captured October 30, 2026.

## Related pages

- [[Qwen]]
- [[Linear Attention and Recurrent Memory]]
- [[Agent Memory]]
- [[Tool Use and Function Calling]]
- [[LLM Reasoning]]
- [[Ali Behrouz and Vahab Mirrokni - The Sleep Framework]]
