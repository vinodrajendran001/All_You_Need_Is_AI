---
type: source-summary
created: 2026-09-13
updated: 2026-09-13
source_id: src-2026-09-13-adedeji-multi-agent-code-review
source_title: "Agents That Prove, Not Guess: A Multi-Agent Code Review System"
source_author: Ayo Adedeji
source_url: https://medium.com/google-cloud/agents-that-prove-not-guess-a-multi-agent-code-review-system-e2c0a735e994
tags:
  - source/summary
  - ai-agents
  - code-review
  - testing
source_ids:
  - src-2026-09-13-adedeji-multi-agent-code-review
status: active
---

# Ayo Adedeji - Agents That Prove, Not Guess

## Summary

A worked Google ADK tutorial that replaces one opaque code-generation pass with four specialists: a structural analyzer, style checker, executable test runner, and feedback synthesizer. A bounded repair loop then proposes a fix, reruns the evidence-producing stages, and exits either on success or after three attempts. The durable idea is not that four prompts are inherently safer than one; it is that deterministic tools produce evidence and models synthesize it.

## Key claims

- In the demonstrated LeetCode Hard task, Gemini 2.5 Pro's first solution failed **13 cases** because equivalent negative slopes were not canonicalized.
- The analyzer uses Python `ast.parse()` and the style stage uses `pycodestyle`; the reported style score was **90/100**.
- The test agent generated and ran **20 sandboxed tests**. **19 passed and 1 failed**, exposing `(1,-1)` versus `(-1,1)` as different representations of the same slope.
- After repair, all **20** tests passed, moving the demonstrated pass rate from **90% to 100%**. This is one example, not a benchmark, and generated tests are not a proof of general correctness.
- The `LoopAgent` permits at most **3** repair attempts. The example stopped after **2** by setting `tool_context.actions.escalate = True`.
- Shared typed state is the communication layer. Constants for state keys turn handoff typos into failures rather than silent empty reads.
- The reported Cloud Trace lasted **2 min 28 sec**: analyzer **4.7 sec**, style **5.3 sec**, test runner **1 min 28 sec**, synthesizer **47.89 sec**. Testing consumed about **59%** of elapsed time.
- The service can be exposed through A2A or FastMCP; the latter is an integration surface, not additional verification.

## Why it matters

The article provides a concrete boundary between probabilistic and deterministic work. Models decide what evidence means and how to explain it; parsers, linters, and test execution produce the evidence. It also makes orchestration cost visible: decomposition improved inspectability in the example but added calls, state contracts, and more than two minutes of latency.

## Tensions / open questions

- Twenty generated tests can still share the generator's blind spots.
- The sandbox restrictions and trace behavior are product- and configuration-dependent.
- No comparison establishes whether four agents outperform one agent using the same tools and repair budget.
- The phrase "prove, not guess" overstates what example-based testing establishes.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Agentic Testing]]
- [[Agent Observability]]
- [[Agent Frameworks]]
- [[Agent Delegation]]

## Citations

- Ayo Adedeji, "Agents That Prove, Not Guess: A Multi-Agent Code Review System", 2025-10-10.

## Raw capture

- [[2026-09-13 Ayo Adedeji - Agents That Prove, Not Guess]]

## Related pages

- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[Coding Agent Harness]]
- [[AI-Native Software Development Lifecycle]]

