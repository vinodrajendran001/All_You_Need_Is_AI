---
type: source-summary
created: 2026-09-03
updated: 2026-09-03
source_id: src-2026-09-02-paolo-perrone-agentic-testing
source_title: "What is Agentic Testing"
source_author: Paolo Perrone
source_url: https://theaiengineer.substack.com/p/what-is-agentic-testing-fa2
tags:
  - source/summary
  - topic/evaluation
  - topic/agents
source_ids:
  - src-2026-09-02-paolo-perrone-agentic-testing
status: active
---

# Paolo Perrone - What is Agentic Testing

## Summary

The clean distinction this post makes: **a scripted test is a recorded route, an agentic test is a
destination.** A scripted test freezes two things — a **locator** (how to find the element) and an **oracle**
(what counts as correct). An agentic test freezes only the goal and lets an agent run a loop of *look, act,
look again* until it gets there.

Three jobs are given to agents in practice: **explore** an application to find what should be tested,
**generate** tests, and **repair** tests that break. Crucially, the agents read **structured interfaces** —
the accessibility tree, the API schema, the call graph — **not screenshots**.

The post is unusually disciplined about what this does and does not buy, and its conclusion is a warning:
**"Agentic testing does not remove the check. It moves who writes it."**

## Key claims

- **Three production results, all partial:**
  - **Meta TestGen-LLM** — **75%** of generated tests compiled, **57%** passed reliably, **25%** raised
    coverage; of the tests that survived all filters, engineers accepted **73%**.
  - **Uber AutoCover** — roughly **1 in 9** of all new tests written at Uber; viable pass rates varied sharply
    by language: **20% Java, 40% Go, 80% Python**.
  - **Airbnb Enzyme migration** — about **3,500 files** migrated in **6 weeks** against a **1.5-year** manual
    estimate; **75% done in 4 hours**, **97% within 4 days**. Most files took **under 10 attempts**, with a
    long tail of **50–100**, prompts growing to **100k tokens** and **up to 50 files** supplied as context.
- **pass@k is the wrong metric and pass^k is the right one.** The worked example: 5 checks over 3 runs gives
  **pass@3 = 0.6** (passed at least once) but **pass^3 = 0.4** (passed every time). The instruction is blunt:
  **"Report pass^k."** A test that passes sometimes is not a test.
- **The repair agent's give-up condition is the buried lede.** When a repair agent cannot fix a test, its
  documented behaviour is to **mark the test skipped**. The post's line: *"Nobody decided to drop that flow
  from your coverage. The agent did."*
- **Self-healing locators can go green over broken features.** An agent that re-finds a moved element will
  also happily re-find its way around a feature that genuinely regressed.
- **Structured interfaces, not pixels.** Reading the accessibility tree or schema is why these agents are
  tractable at all; it also means the approach degrades on interfaces that expose no structure.
- **Recommended shape: agent at authoring time, model out of CI.** Use agents to write and repair tests
  offline, then run deterministic artifacts in the pipeline.

## Why it matters

**pass^k is the item with the widest blast radius, and it is new to this vault.** Nearly every agent
capability number the vault holds is a pass@k-style figure, and the gap between 0.6 and 0.4 in a five-check,
three-run example is the size of the correction. It is also the natural pairing for the finding in
[[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]] that **temperature 0 is
not deterministic** because batch composition changes numerics — if the serving stack alone produces ~80
distinct completions from 1,000 identical prompts, then single-run pass@1 is measuring luck. See
[[Multi-Turn Evaluation]].

**The skip-on-failure behaviour is a governance finding, not a testing detail.** It is an agent silently
narrowing a safety property — coverage — with no human in the decision. That is the same shape as the
blacklist rewrite in [[derelict5432 - Adaptive Agentic Worms Are Here]]: an agent modifying the constraint
system rather than satisfying it. In one case the objective is replication; here it is "make the suite green".

The three case studies also give the vault its first **language-stratified** agent success rates
(20/40/80 by language), which is direct evidence that agent capability is a property of the ecosystem's tooling
and type system, not only of the model.

## Tensions / open questions

- The three case studies are **company blog posts and conference talks**, reported secondhand here. None are
  controlled comparisons, and Airbnb's 1.5-year manual baseline is an **estimate**, not a measured control.
- Uber's 20/40/80 spread is reported without an explanation; the post does not establish whether the driver
  is language typing, test-framework conventions, or training-data volume.
- "Engineers accepted 73%" is a survivorship figure — it applies to tests that already passed three filters,
  so it is not a 73% acceptance rate for generated tests overall.
- If the recommendation is to keep the model out of CI, what maintains the tests as the application drifts?
  The repair loop is exactly what the recommendation excludes.
- No cost figures. 100k-token prompts across 3,500 files is a large bill nobody quantifies.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Agentic Testing]]
- [[Multi-Turn Evaluation]]
- [[AI-Native Software Development Lifecycle]]
- [[Paolo Perrone]]

## Related pages

- [[Benchmark Optimization]]
- [[LLM-as-a-Judge]]
- [[Coding Agent Harness]]
- [[Agent Security and Governance]]
- [[Agentic Loop]]
- [[Context Engineering]]
- [[derelict5432 - Adaptive Agentic Worms Are Here]]

## Citations

- Raw capture: [[2026-09-02 Paolo Perrone - What is Agentic Testing]]
- Source: <https://theaiengineer.substack.com/p/what-is-agentic-testing-fa2>
