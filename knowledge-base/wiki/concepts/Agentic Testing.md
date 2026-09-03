---
type: concept
created: 2026-09-03
updated: 2026-09-03
tags:
  - concept
  - evaluation
  - testing
  - agents
  - software-engineering
source_ids:
  - src-2026-09-02-paolo-perrone-agentic-testing
  - src-2026-06-02-bytebytego-doordash-testing-system
  - src-2026-08-05-aibuilderclub-how-to-evaluate-ai-agents
  - src-2026-08-31-bytebytego-chatbot-request-lifecycle
status: active
---

# Agentic Testing

## Definition

Agentic testing points an agent at software with a **goal** rather than a script. The distinction drawn by
[[Paolo Perrone - What is Agentic Testing]] is that a scripted test is a **recorded route** while an agentic
test is a **destination**: the script freezes a **locator** (how to find the element) and an **oracle** (what
counts as correct), whereas the agent freezes only the goal and runs a loop of *look, act, look again*.

Note the direction of this page. It is about **agents testing software**. Evaluating agents themselves is
[[Multi-Turn Evaluation]] and [[LLM-as-a-Judge]].

## Why it matters

Testing is where the vault can observe agent capability against a task with an unusually honest scoreboard:
a generated test either compiles and passes repeatedly or it does not, and several companies have published
their hit rates. The resulting numbers are the most concrete evidence available for what agents actually
deliver in a production engineering loop — and they are consistently **partial**.

## Three jobs, and what the interface has to expose

Agents are given three distinct roles: **explore** an application to discover what should be tested,
**generate** tests, and **repair** tests that break.

The enabling detail is that these agents read **structured interfaces** — the accessibility tree, the API
schema, the call graph — **not screenshots**. This is why the approach is tractable at all, and it sets its
boundary: an interface exposing no structure gives the agent nothing to reason over. See
[[Vision-Language Grounding]] for the harder case.

## The published numbers, and what they say

| System | Result |
|---|---|
| Meta **TestGen-LLM** | 75% of generated tests compiled, 57% passed reliably, 25% raised coverage; of survivors, engineers accepted 73% |
| Uber **AutoCover** | ~1 in 9 of all new tests written at Uber; viable pass rate **20% Java, 40% Go, 80% Python** |
| Airbnb **Enzyme migration** | ~3,500 files in 6 weeks against a 1.5-year manual estimate; 75% in 4 hours, 97% within 4 days |

Three readings matter more than the headlines.

**The funnel is the finding, not the acceptance rate.** Meta's 73% acceptance applies only to tests that had
already survived compilation, reliability and coverage filters. Agent output is usable here because it is
**cheap to filter automatically**, not because it is reliable.

**Capability is language-stratified.** Uber's 20/40/80 spread across Java, Go and Python is the vault's first
direct evidence that agent success depends on the ecosystem — tooling, type system, idiom stability, training
data volume — and not only on the model. A single-language benchmark number does not transfer.

**The long tail is where the cost is.** Airbnb's most files took under 10 attempts, but the tail ran 50–100
attempts, with prompts growing to 100k tokens and up to 50 files supplied as context. The median case and the
tail case are different economic propositions; see [[Context Engineering]].

## pass@k is the wrong metric; report pass^k

The most portable idea on this page. **pass@k** asks whether a system succeeded **at least once** in k
attempts. **pass^k** asks whether it succeeded **every time**.

The worked example: five checks over three runs gives **pass@3 = 0.6** but **pass^3 = 0.4**. The instruction
is blunt — *"Report pass^k."* A test that passes sometimes is not a test.

This has reach well beyond testing, because most agent capability figures the vault holds are pass@k-shaped.
It also pairs with a serving fact from
[[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]]: **temperature 0 is not
deterministic**, because numerics depend on batch composition, and 1,000 identical prompts produced roughly
**80 distinct completions**. If the inference stack alone injects that much variance, a single-run pass@1 is
partly measuring the serving configuration. See [[Multi-Turn Evaluation]].

## The failure modes are quiet ones

Both documented failures degrade the *signal* rather than the code, which makes them hard to notice.

**The repair agent's give-up condition is to mark the test skipped.** Coverage narrows and the suite stays
green. *"Nobody decided to drop that flow from your coverage. The agent did."* This is the benign instance of
the environment-modification pattern collected on [[Self-Replicating Agents]] — an agent removing a check
standing between it and its objective, with no adversarial intent anywhere.

**Self-healing locators can go green over broken features.** An agent that re-finds a moved element will also
route around a feature that genuinely regressed. Robustness to refactoring and blindness to regression are the
same mechanism.

Both point the same way as the vault's existing evaluation guidance: in
[[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]], the LLM works best as a **narrow
verifier** with binary policy checks and human calibration, not as a general generator; and
[[AI Builder Club - How to Evaluate AI Agents - What Works in 2026]] insists that production and acceptance be
performed by different parties. A repair agent that can silently retire its own acceptance criterion violates
that separation.

## The recommended shape

**Agent at authoring time, model out of CI.** Use agents to explore, generate and repair offline, then run
deterministic artifacts in the pipeline. This keeps the agent's variance out of the release gate while
retaining its throughput — and it is the same conclusion the vault reaches for
[[AI-Native Software Development Lifecycle]] generally: agents produce candidates, deterministic systems
decide.

## Open questions

- If the model is kept out of CI, what maintains the suite as the application drifts? The repair loop is
  exactly what the recommendation excludes, and skipped-test behaviour is a reason to want it excluded.
- What drives the 20/40/80 language spread — static typing, framework conventions, or training data volume?
  Nothing in the source separates these, and the answer determines whether the gap closes.
- What is the correct k for pass^k, and who pays for k runs of an expensive agent?
- All three case studies are company blog posts and talks with no controlled comparison; Airbnb's 1.5-year
  baseline is an **estimate**. How much of the speedup is the agent and how much is the forcing function of a
  migration project?
- Should a repair agent ever be permitted to skip a test, or should give-up always escalate to a human?

## Related pages

- [[Paolo Perrone - What is Agentic Testing]]
- [[Multi-Turn Evaluation]]
- [[LLM-as-a-Judge]]
- [[Benchmark Optimization]]
- [[AI-Native Software Development Lifecycle]]
- [[Coding Agent Harness]]
- [[Agent Security and Governance]]
- [[Self-Replicating Agents]]
- [[Context Engineering]]
- [[Agentic Loop]]
- [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]]
