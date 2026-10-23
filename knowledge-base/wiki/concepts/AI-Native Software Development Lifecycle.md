---
type: concept
created: 2026-08-25
updated: 2026-10-23
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
  - src-2026-10-05-faik-ai-native-software-factory
  - src-2026-09-27-willison-llms-2026-so-far
  - src-2026-10-15-osmani-claude-code-review
  - src-2026-10-14-maevyn-decoherence-trap
status: active
---

# AI-Native Software Development Lifecycle

## Definition

The AI-native SDLC redesigns software development around agent-produced artifacts, feedback, and
runtime controls. The vault's anchor Anthropic playbook turns plan, design, build, test, deploy, and
maintain into a **loop of committed artifacts** rather than a linear chain of documents and sign-offs.
That is one concrete operating model, not the definition of every AI-assisted software factory.

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

- **The anchor playbook's evidence is vendor-supplied and unmeasured.** Every play is expressed in Claude Code primitives, and while each names "how you measure whether it worked," no baselines, control groups, or before/after numbers are reported for any customer.
- **Guardrails need governance too.** Moving policy into hooks means policy now lives in shell scripts inside the repository. Who reviews the guardrails, and what stops an agent from editing them, is unaddressed.
- **The audit trail assumes honest artifacts.** Treating the commit chain as the record of what happened presumes the agent's stated rationale reflects what it actually did — precisely the gap [[Grok Bot Systems Engineering Working Note]] closes with an evidence ladder in which "the bot says it is done" is never sufficient.
- Human accountability is asserted to remain central, but concentrating attention at gates means humans increasingly review *what the agent flagged* rather than the work itself, which relocates rather than removes the trust problem. [[Addy Osmani - How the Claude Code Team Does Code Review]] now supplies a first-party admission of the second-order cost: Anthropic reports **no formal method for preserving team-wide codebase understanding** once humans stop reading trivial diffs, and substitutes agent-generated explainers and visual artifacts.

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

## Measure the constrained stage before building a factory

[[Adam Faik - How to Build an AI-Native Software Factory]] adds operational reporting to the
playbook's prescriptions. Its proposal is to measure the bottleneck, run a bought agent on
verifiable toil in shadow mode, and build only the repository context, warm environments, workflow
blueprints, and gates needed by that workload. Review and CI can absorb all of a code-generation
gain. Cost per accepted outcome with quality retained is therefore more useful than token volume.

The strongest counterexample to indiscriminate agent use is an Uber JUnit migration: generative AI
did not work well, while deterministic Shepherd automation produced **5,000+ diffs** and moved
**75,000+ test classes in four months**, with AI helping failures. This is secondary company
reporting, not a controlled comparison, but it keeps deterministic transformation in the baseline
set rather than making "agentic" the success criterion.

[[Simon Willison - 2026 in LLMs (so far)]] reaches a compatible limit through personal experiments:
generating a game-shaped artifact did not supply a compelling game. He presents StrongDM's
no-human-writing/no-human-code-review rules as an experienced team's alternative assurance
experiment, not a universal removal of review. Specification, product judgment, and verification
remain work even when implementation gets cheaper.

Faik's survey is mostly large-company self-reports and explicitly lacks a demonstrated
300-engineer laptop-to-factory rollout. Its illustrative 200-PR PostHog sample also changes
dramatically when bot reviews count. Neither it nor Willison's keynote establishes a general
productivity multiplier or a universally appropriate autonomy level.

## The change sets the tier, not the author

[[Addy Osmani - How the Claude Code Team Does Code Review]] reports an operating model for the Deploy
stage that this page described structurally but never saw instantiated with a rule. A classifier
assigns each change a **low, medium, or high** risk tier, requiring **0, 1, or 2** human approvals
respectively, with sensitive paths, CI workflows, and designated owner paths always requiring a
person. Two constraints make it more than a triage heuristic: **"The change sets the tier, not the
author"**, and **"An agent's approval never counts as a person's."** Whoever prompted an agent-written
change is accountable for it and counts as a required reviewer.

This is the sharpest available answer to the control-mismatch problem stated at the top of this page.
Reviewing every line made sense when a person wrote every line; the common replacement instinct — scrutinise
agent output *more* because an agent produced it — indexes scrutiny on authorship, which is exactly
the variable the risk tier discards. Blast radius is a property of the diff. Everything downstream
follows the same logic: a merge queue reruns checks against the latest `main`, changes ship behind
flags to employees then `latest` then `stable`, and telemetry plus flag-disable and revert supply the
recovery path that makes a low-risk zero-approval merge defensible in the first place.

**The numbers are Anthropic's own and carry no controlled comparison.** Claude is said to write
**"about 90 percent"** of Claude Code's code; monorepo changes rose from **about 2,500 in May to more
than 30,000 in September**; from June to September merged Claude Code pull requests **more than
doubled** while the share requiring reversion **fell by more than 40 percent**, with no counts,
denominator, incident definition, or confidence interval supplied. The stated optimisation target —
at most one human in the loop for most pull requests, with revert and incident rates as guardrails —
is also, by the authors' own admission, **unenforced**: there are no circuit breakers that tighten
approval automatically when those guardrail metrics worsen. The June-to-September comparison does not
isolate the effect of agentic review from simultaneous changes in staffing, workload, and release
controls.

## Throughput is the stage this loop measures; coherence is not

[[The Decoherence Trap]] — an essay published at maevyn.codes with **no author stated anywhere in the
capture** — supplies the counter-case to everything above. Its argument is that the quantity a
faster lifecycle optimises and the quantity that determines future cost are different. **Decoherence**
is proposed as a third category of technical debt, distinct from infrastructure debt (wear) and
technical-advancement debt (the need to upgrade): the accumulation of **locally valid but mutually
incompatible or redundant models** in a system that keeps changing. Each change is defensible on its
own; the interactions between coexisting paradigms are combinatorial, so the cost of the *next* change
rises.

The essay's own simulation is explicitly **illustrative and not evidence about real software** — the
author states that its weights are arbitrary and that it does not prove how complex systems evolve —
so the displayed feature counts should not be read as measurements. What it does carry are three
third-party studies, which together are the most concrete negative evidence this page holds:

| Study, as cited | Reported finding |
| --- | --- |
| Harvard working paper (Chen and Stratton), **718 companies** | Coding agents increased code written by **30%** with no measurable increase in finished work; pull requests took **49% longer** to review and **nearly twice as many** were returned for changes |
| Carnegie Mellon (He et al.), open-source projects adopting Cursor | A large initial velocity increase that **did not last**, with rising code complexity contributing to the later slowdown; **no effect size quoted** |
| Liu et al., **over 300,000** AI-authored commits across **more than 6,000** repositories | Roughly **one in eleven** commits — up to **one in seven** depending on assistant — introduced at least one quality issue, and **nearly a quarter** of those issues remained in the code |

None of these were read during ingest and all concern specific companies, repositories, assistants and
periods, so they establish association for those populations rather than a universal causal effect.

The reading for this page is narrow and useful. Its committed-artifact chain instruments **stage
transitions** — intent accepted, spec approved, plan merged, evals passed, release authorised — and
every one of those is a throughput measure. Decoherence is a property of the *accumulated* system that
no stage gate inspects, which is why a lifecycle can report improving numbers at each gate while the
Harvard pattern holds overall. The essay's "sweet spot" claim is the practical form: it argues both
extremes reduce delivery, so the recommendation is a moderate, actively maintained coherence level
rather than maximum coherence.

**This sits in unresolved tension with the Anthropic report above**, and the vault should keep both.
One organisation reports reverts falling by more than 40 percent while agent-written volume rose; a
Harvard sample of 718 companies reports review time rising 49 percent and finished work flat. They are
different organisations, different measures, and different denominators — neither checks the other.
The honest reading is that Anthropic's result, if real, is evidence about a company with merge queues,
risk classifiers, daily incident-derived evals, feature flags, and rollback culture already in place,
which is not the population the Harvard paper sampled. **Decoherence Collapse** — the end state in
which systems degrade faster than they can be repaired — is the essay's **speculative forecast**, not
an observed condition; the author's estimate that repair could take "years or even decades" is
explicitly qualitative, and nothing in the essay shows any real system has reached it or that agents
cannot repair a highly complex system.

## Open questions

- Which parts survive translation off Claude Code? The artifact loop and act-time enforcement look portable; the specific `CLAUDE.md`/hooks/subagent surface does not.
- What is the actual failure rate of agentic review passes on critical code, and does layered review catch what uniform human review would have?
- How do regulated industries reconcile "governance enforced as the AI acts" with regimes that require a named human reviewer per change?
- Does the artifact chain scale to large organisations, or does it fragment into per-team dialects the way earlier process documentation did?
- A risk classifier decides how much human scrutiny a change receives. Nothing reported measures the
  classifier's own error rate, or what a misclassified high-risk change costs when it merges with zero
  approvals.
- The Anthropic account defines the guardrails (revert rate, incident rate) but has **no circuit
  breaker** wired to them. What should automatically tighten, and at what threshold?
- Decoherence has no fitted growth rate in any production codebase. What would a usable metric for
  accumulated incompatibility even be, and could a stage gate carry it?
- Nothing establishes whether Anthropic's falling revert share and the Harvard sample's rising review
  burden are contradictory or simply describe organisations at different levels of release-control
  maturity. No shared measure exists to compare them.

## Related pages

- [[Addy Osmani - How the Claude Code Team Does Code Review]]
- [[The Decoherence Trap]]
- [[Recursive Self-Improvement]]
- [[Adam Faik - How to Build an AI-Native Software Factory]]
- [[Simon Willison - 2026 in LLMs (so far)]]
- [[Legacy Code Modernization with AI Agents]]
- [[Agent Observability]]
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
