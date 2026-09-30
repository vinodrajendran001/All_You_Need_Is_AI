---
type: concept
created: 2026-09-03
updated: 2026-09-30
tags:
  - concept
  - evaluation
  - testing
  - ai-agents
  - software-engineering
source_ids:
  - src-2026-09-02-paolo-perrone-agentic-testing
  - src-2026-06-02-bytebytego-doordash-testing-system
  - src-2026-08-05-aibuilderclub-how-to-evaluate-ai-agents
  - src-2026-08-31-bytebytego-chatbot-request-lifecycle
  - src-2026-09-03-github-ai-coding-cost-efficient
  - src-2026-09-13-adedeji-multi-agent-code-review
  - src-2026-09-14-bytebytego-llm-judge-health
  - src-2026-09-09-mistral-legacy-code-modernization
  - src-2026-09-28-martin-automating-eval-design-hillclimbing
  - src-2026-09-29-bytebytego-why-do-llms-lie
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

## Prompt behaviour is untested surface

[[GitHub - How We Make AI Coding More Cost Efficient]] contributes a category of test this page did not cover:
**tests over prompt-induced behaviour.** A meta-prompting loop halved a task-tool prompt and, without anyone
noticing, converted cautious parallelism guidance into a hard scheduling policy that **serialised independent
agents**. Offline evaluation passed. The regression appeared only in production, and the fix was to restore a
single sentence.

The lesson is stated as a rule and deserves to be treated as one: *"Prompt behavior needs tests. If a behavior is
not tested, a shorter prompt can remove it without anyone noticing."* Every prompt sentence is an untested
assertion about behaviour until something exercises it, which makes prompt compression a refactor without a
safety net — and prompt compression is now routinely done by models.

A second contribution is a cheap evaluation signal for output-shaping changes: **the recovery path is the test.**
When an aggressive output compressor removed detail, agents reopened files and re-ran commands to recover it. No
human judgement was needed to detect the regression — the agent's own recovery behaviour was the measurement.
Where a change removes information, instrument whether the agent goes and fetches it again.

The same source is a caution about test-suite portability: a file-tool change that reduced cost in a code-review
agent **increased** it in a CLI agent. A behavioural suite validated on one product does not license the change
on another.

## Executable evidence is stronger than synthesis, but it is not proof

[[Ayo Adedeji - Agents That Prove, Not Guess]] supplies a compact worked example of the
recommended shape on this page. Four agents separate structural analysis, style checking, test
execution, and synthesis; the evidence-producing stages are deterministic tools (`ast.parse`,
`pycodestyle`, and sandboxed execution), while the models interpret and communicate the result.

The example is useful precisely because it is not clean. Gemini 2.5 Pro's first solution failed
**13 cases**. The generated suite then ran **20 tests**, with **19 passing and 1 failing**, and a
bounded repair loop reached **20/20** after **2 iterations**. That is evidence for the tested cases,
not the article title's stronger promise to "prove": generated tests can share the generator's
blind spots, and one LeetCode task is not a benchmark.

The durable rule is narrower: **make the acceptance evidence inspectable and executable outside the
model, then bound the repair loop.** The source caps repair at **3 attempts** and exits through an
explicit escalation action rather than letting the model decide indefinitely that another try is
warranted.

## Evaluation is a loop, not one score

[[ByteByteGo - LLMs as a Judge - How to Know if Your LLM Is Healthy]] proposes a stack from
deterministic validators through golden datasets, model judges, human calibration, and production
monitoring. The durable practice is that every live failure becomes a regression case, while
development and holdout sets remain separate so prompt tuning does not optimize the test away.

## Characterization before migration

[[Mistral - Modernizing Complex Legacy Code with AI Agents]] builds tests from intermediate legacy
state rather than from translated code. This reduces shared-error risk: generated C++ must match
observable Fortran behavior before refactoring or cleanup changes the structure.

## The grader and the answer space are untested surface too

This page already argues that prompt behaviour is untested surface. Two new sources extend the same
argument to the measuring apparatus itself.
[[Lance Martin - Automating Eval Design and Hillclimbing with Claude]] makes grader noise a first-class
diagnostic: before any improvement work begins, the baseline run executes **the grader twice on the same
output**, alongside checks for timeouts, API errors, and truncated responses, and reports a confidence
interval plus one full transcript per case. A suite that cannot separate its own run-to-run variance from
the system's cannot attribute anything — the same complaint this page makes about pass@k, aimed at a
different target.

The four properties Martin requires of a usable evaluation read as a construction checklist: a
production-like task distribution, scores that rise with stronger models and more effort, frontier
performance with **headroom below 100%**, and low run-to-run variance. The third has a rule attached — the
diagnostic **warns when the baseline is about 95% or higher**, on the grounds that quality hillclimbing is
then uninformative and cost or latency should become the objective. Cases are sampled in a fixed order of
preference: production transcripts, then bug reports and support tickets, then **five to ten**
hand-written cases, then cases synthesized from the codebase — real traffic first, synthesis last. All of
this is Anthropic-reported on an Anthropic workflow, with no independent reproduction and no released
evaluation data; see [[Anthropic]].

[[ByteByteGo - Why Do LLMs Lie]] supplies the other half, and it is the sharper contribution: an
evaluation should measure **correctness, support, appropriate abstention, and unnecessary refusal** as
four separate things. Right/wrong scoring cannot distinguish a system that learned to say "I don't know"
from one that learned to refuse, because both register as non-answers. That has a direct reading on this
page's most uncomfortable finding. The repair agent's give-up condition — mark the test skipped — is
precisely an abstention that a two-valued scoreboard records as a green suite, and no amount of pass^k
reporting separates a justified skip from an evaded one.

Both sources also pull against this page's recommended shape. "Agent at authoring time, model out of CI"
keeps model variance out of the release gate; Martin's loop keeps a judge in the measurement path
throughout and concedes that a misconfigured judge still requires a human to read scored transcripts, and
ByteByteGo's verification stage is itself a model that can be wrong. Neither retires the
deterministic-artifacts recommendation — both say the artifact deciding *what counts as passing* is harder
to make deterministic than the artifact that runs in CI. ByteByteGo is a secondary explainer with
sponsored sections and reports no hallucination rates or controlled comparisons, so its four-way
scoreboard is a design proposal rather than a measured improvement.

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
- Does a skipped test count as appropriate abstention or as unnecessary refusal? ByteByteGo names the
  distinction but nothing says how a suite would classify its own repair agent's give-up events.
- Martin's roughly-95% warning assumes a high baseline means a saturated system. How would a team tell
  that apart from a task distribution that was sampled too easy in the first place?

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
- [[Tool Roster Economics]]
- [[GitHub - How We Make AI Coding More Cost Efficient]]
- [[GitHub]]
- [[Ayo Adedeji - Agents That Prove, Not Guess]]
- [[Lance Martin - Automating Eval Design and Hillclimbing with Claude]]
- [[ByteByteGo - Why Do LLMs Lie]]
- [[ByteByteGo]]
- [[Anthropic]]
- [[Harness Optimization]]
