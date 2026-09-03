---
type: concept
created: 2026-08-25
updated: 2026-09-03
tags:
  - concept
  - sdlc
  - coding-agents
  - governance
  - enterprise
source_ids:
  - src-2026-08-21-anthropic-ai-native-sdlc
  - src-2026-08-05-aibuilderclub-reviewing-ai-generated-pull-requests
  - src-2026-08-07-avi-chawla-claude-code-cost
  - src-2026-08-22-grok-bot-systems-engineering-working-note
  - src-2026-09-02-paolo-perrone-agentic-testing
status: active
---

# AI-Native Software Development Lifecycle

## Definition

The AI-native SDLC is a rebuilt software development process in which the six familiar stages — plan, design, build, test, deploy, maintain — become a **loop of committed artifacts** rather than a linear chain of documents and sign-offs, with AI embedded at every point and controls enforced as the agent acts rather than at review time.

## Why it matters

Most of this vault's agent material operates at the level of one developer and one harness. This concept is the layer above: what a *company's* process must become when [[Coding Agent Harness|coding agents]] write most of the diff. [[Anthropic - The AI-Native SDLC Playbook]] makes the case bluntly — code is no longer the bottleneck, and three things follow when build collapses to hours:

- The constraint moves to the stages either side of build, which still run at human speed.
- Controls stop matching reality. Reviewing every line by hand made sense when a person wrote it; it cannot keep up once agents do.
- Governance costs *rise*, because exceptions still route through committees that meet weekly or monthly.

The failure mode is therefore not "agents write bad code." It is an organisation that accelerates one stage and leaves the surrounding process to become the bottleneck it was never designed to be.

## The committed artifact is the mechanism

The single structural idea worth carrying: **every stage ends by writing one artifact to version control, and that commit triggers the next stage.**

| Stage | Artifact | Trigger |
| --- | --- | --- |
| Plan | `intent.md` | acceptance triggers requirements and design |
| Design | `spec.md` | approval triggers plan mode |
| Build | `plan.md`, then the diff and its tests | merged PR triggers the pipeline |
| Test | eval results in CI | passing gate allows deploy |
| Deploy | the PR with its review findings | release authorization |
| Maintain | the incident record | a breached control band writes the next `intent.md` |

Two properties make this more than bureaucracy. First, the early artifacts are deliberately Markdown because **a product owner and an agent can both read and act on the same file**; from build onward the artifact is code and its records. Second, the chain of commits *is* the audit trail — who asked for what, what the agent produced, who approved it — so traceability is a by-product of the workflow rather than a separate compliance activity.

This is the same principle [[Grok Bot Systems Engineering Working Note]] arrives at for agent teams generally: pass typed artifacts and evidence pointers, not conversations. Both sources independently reject narrative handoff in favour of a durable, checkable object.

## Where enforcement moves

The deepest shift is **from review-time to act-time governance**.

- **Institutional knowledge becomes versioned files.** `CLAUDE.md` carries commands, conventions, architecture, and — usefully — an explicit "things Claude gets wrong" section. Recurring procedures become [[Agent Skill|skills]] (`.claude/skills/*/SKILL.md`), such as a secure API review.
- **Hooks are guardrails and gates.** The same mechanism enforces conventions at build time and blocks a production deploy without a named release authorization. Policy becomes executable rather than documented.
- **Review is layered, not uniform.** Agentic review passes run first against a committed `REVIEW.md` that defines the passes, states what "important" means, caps the nits, and lists what not to report. Scarce human review is reserved for regulated and critical code.
- **Testing becomes continuous evals in CI** rather than QA gates at stage boundaries — the [[Multi-Turn Evaluation]] argument applied to the pipeline.
- **Maintain closes the loop.** Agents watch live deployments against control bands (a `bands.yaml`), and a breached band is diagnosed and written back as the next `intent.md`.

## Adoption is a dependency graph, not a ladder

The playbook is explicit that stage order and adoption order are different things. Plays with no inbound arrows can be started immediately; every other play names its prerequisites. This matters because it makes the process resistant to the usual "maturity model" failure, where an organisation tries to advance every stage in lockstep. Compare [[Agent Workflow Maturity]], which reaches a compatible conclusion from the operations side: choose the smallest architecture that externalises the *real* bottleneck.

## Tensions

- **The evidence is vendor-supplied and unmeasured.** Every play is expressed in Claude Code primitives, and while each names "how you measure whether it worked," no baselines, control groups, or before/after numbers are reported for any customer.
- **Guardrails need governance too.** Moving policy into hooks means policy now lives in shell scripts inside the repository. Who reviews the guardrails, and what stops an agent from editing them, is unaddressed.
- **The audit trail assumes honest artifacts.** Treating the commit chain as the record of what happened presumes the agent's stated rationale reflects what it actually did — precisely the gap [[Grok Bot Systems Engineering Working Note]] closes with an evidence ladder in which "the bot says it is done" is never sufficient.
- Human accountability is asserted to remain central, but concentrating attention at gates means humans increasingly review *what the agent flagged* rather than the work itself, which relocates rather than removes the trust problem.

## Testing: agents at authoring time, deterministic artifacts in CI

[[Paolo Perrone - What is Agentic Testing]] contributes the vault's most concrete evidence for what agents
deliver inside a real engineering pipeline, and it is consistently **partial**: Meta's TestGen-LLM produced
tests of which **75% compiled, 57% passed reliably, 25% raised coverage**; Uber's AutoCover writes roughly
**1 in 9** of all new tests, with viable pass rates of **20% Java, 40% Go, 80% Python**; Airbnb migrated
**~3,500 files in 6 weeks** against a 1.5-year manual estimate.

Two findings shape how this fits the lifecycle.

**Agent output is usable because it is cheap to filter, not because it is reliable.** Every one of these
systems is a funnel with automated gates. Meta's much-quoted 73% engineer acceptance applies only to tests
that had already survived three of them.

**Capability is language-stratified.** The 20/40/80 spread is direct evidence that agent effectiveness depends
on the ecosystem — tooling, typing, idiom stability — and not only on the model, so a benchmark figure from
one language does not transfer to a polyglot codebase.

The recommended shape is **agent at authoring time, model out of CI**: agents explore, generate and repair
offline; deterministic artifacts run in the pipeline. This is the general principle of this page applied to
testing — agents produce candidates, deterministic systems decide — and it is reinforced by a specific hazard,
that a repair agent's documented give-up condition is to **mark a test skipped**, silently narrowing coverage
while keeping the suite green. See [[Agentic Testing]].

## Open questions

- Which parts survive translation off Claude Code? The artifact loop and act-time enforcement look portable; the specific `CLAUDE.md`/hooks/subagent surface does not.
- What is the actual failure rate of agentic review passes on critical code, and does layered review catch what uniform human review would have?
- How do regulated industries reconcile "governance enforced as the AI acts" with regimes that require a named human reviewer per change?
- Does the artifact chain scale to large organisations, or does it fragment into per-team dialects the way earlier process documentation did?

## Related pages

- [[Anthropic - The AI-Native SDLC Playbook]]
- [[Coding Agent Harness]]
- [[Agent Skill]]
- [[Agent Security and Governance]]
- [[Agent Workflow Maturity]]
- [[AI Agents in Production]]
- [[Multi-Turn Evaluation]]
- [[Context Engineering]]
- [[Loop Engineering]]
- [[Anthropic]]
- [[Agentic Testing]]
- [[Paolo Perrone - What is Agentic Testing]]
