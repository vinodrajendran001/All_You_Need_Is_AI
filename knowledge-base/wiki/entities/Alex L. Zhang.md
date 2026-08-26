---
type: entity
entity_kind: person
created: 2026-08-26
updated: 2026-08-26
tags:
  - entity
  - person
  - agent-harness
  - programmatic-tool-calling
source_ids:
  - src-2026-08-26-alex-zhang-speculative-programmatic-tool-calling
status: active
---

# Alex L. Zhang

## Who they are

A researcher writing on agent harness design, publishing at `alexzhang13.github.io`. Advised by Omar Khattab. Author of work on **Recursive Language Models (RLMs)** — harnesses in which a model's tools include calls to sub-models — and of the harness-design writing this vault draws on.

## Why they matter here

Zhang holds a strong and unusually explicit position: **code in a REPL is the only tool a system needs, and all other tools should be functions in that code.** That claim is the seed of [[Programmatic Tool Calling]] in this vault, and it is a genuine alternative to the JSON-schema contract described in [[Tool Use and Function Calling]].

[[Alex L. Zhang - Speculative Programmatic Tool Calling]] then draws the consequence: once the action space is a program, the harness can optimize it like a compiler. That proposal seeds [[Speculative Tool Execution]] and gives the vault its first treatment of speculation *above* the token level — a level up from [[Speculative Decoding]].

## Notes

- The writing is a personal research blog with accompanying open implementations rather than peer-reviewed work. It should be cited as an engineering proposal with measurements, not as a paper.
- **Reports conservative numbers.** The sPTC post gives 1–1.2× speedups and states plainly that exact speedups are near-impossible to estimate; a more favourable "deterministic" benchmark suite was deliberately omitted as too specific. That is unusual candour for a technique proposal and raises rather than lowers the credibility of the reported figure.
- Positions his own ideas against prior art explicitly, naming Conveyor, Speculative Interaction Agents, and AsyncFC, including an objection to the last.
- Compute for the experiments was provided by Laude.

## Related pages

- [[Alex L. Zhang - Speculative Programmatic Tool Calling]]
- [[Programmatic Tool Calling]]
- [[Speculative Tool Execution]]
- [[Coding Agent Harness]]
- [[Tool Use and Function Calling]]
- [[Speculative Decoding]]
- [[Agent Planning]]
- [[AI Knowledge Base Overview]]
