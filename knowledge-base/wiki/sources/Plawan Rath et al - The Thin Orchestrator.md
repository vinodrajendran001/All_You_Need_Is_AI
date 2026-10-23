---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-19-rath-thin-orchestrator
source_title: "The Thin Orchestrator: How We Made Our AI Agents More Reliable by Giving the Router Less to Do"
source_author: Plawan Rath, Akhil Jindal, Ashwini Verma
source_url: https://engineering.fb.com/2026/10/19/ml-applications/thin-orchestrator-ai-agent-architecture/
tags:
  - source/summary
  - agent-architecture
  - orchestration
  - context-engineering
source_ids:
  - src-2026-10-19-rath-thin-orchestrator
status: active
---

# Plawan Rath et al - The Thin Orchestrator

## Summary

Meta Engineering's account of rebuilding a data-onboarding agent after a single agent holding all domain
knowledge **worked in demos and hallucinated in production**. The replacement is a deliberately
knowledge-free router: roughly **1,300 lines** coordinating **20+ workflows** across **14 specialist
agents**, performing no domain work itself.

The design principle is a hard boundary: **"Deterministic decisions stay deterministic."** Routing,
sequencing, input gathering, reliability checks, and error handling are ordinary code; only delegated
domain reasoning uses a model.

## Key claims

### What broke

- One agent held schemas, code-generation rules, routing logic, validation requirements, and patterns
  for **more than 10 data sources**. The authors report it **cross-contaminated concepts** between
  subsystems and hallucinated in production.
- Their diagnosis is stated bluntly: **"The agent had everything it needed. That was the problem."**
  More context degraded performance through interference.
- The onboarding process spans **three code repositories, three programming languages, and up to six
  pipeline stages**.

### The replacement

- The orchestrator's fixed protocol: read the relevant subagent instructions → check for duplicates →
  gather required user fields → auto-discover inferable facts (repository type, existing configuration)
  → check warnings and required reviewers → delegate with full context → handle results and surface
  errors.
- It **generates no configurations, does not reason about code, and does not touch the codebase**.
- Specialists are isolated subagents owning schema management, population and code generation,
  validation, and other domain reasoning, each with its own knowledge, execution steps, discovery
  patterns, and troubleshooting mappings.
- **Workflow templates** are deterministic state machines sequencing the same 14 agents: column
  onboarding (Schema → Validation → Population → Testing), event onboarding (Schema → Population →
  Validation → Testing → Event Processing), and pipeline migration (Assessment → Planning → Population
  → Validation → Monitoring).
- **25+ knowledge files**, typically a few thousand tokens each, are loaded **at runtime by specialists**
  rather than embedded in the orchestrator, so updates take effect in later sessions without orchestrator
  changes.
- Context isolation is intentional: **"No agent sees the full picture. That's the feature, not the bug."**
  A specialist failure triggers retry or escalation and is meant not to corrupt other contexts.

### Reported results — all self-reported

- A single-agent alternative achieved **70-80%** success **with manual prompt engineering per task**,
  falling to **10-20%** without it. Workload and sample size unspecified.
- Process duration across successive versions: manual preparation **three to four days** → earlier
  config-driven system **about a day** → thin orchestrator **under an hour**.
- **"About two-thirds"** of system changes land without significant human edits. Denominator and the
  meaning of "significant" are not specified.
- A **15th subagent** would need no new structural design, since it follows the same template. This is an
  architectural claim, not a measurement.
- **[Third-party]** A cited Mount Sinai preprint reported orchestrated multiagent systems at **65.3%**
  accuracy versus **16.6%** for single agents on **80-task batches**, with token usage reduced
  **up to 65-fold**. The benchmark details are not reproduced.

## Why it matters

[[Agent Delegation]] and [[Context Engineering]] in this vault have accumulated the claim that context
interference degrades agents. This source supplies an **architectural response** to it that is unusually
specific about where the boundary runs: not "use subagents", but *the router must contain no domain
knowledge at all*, and everything the router does must be expressible as deterministic code.

It also inverts the usual framing for [[Model Routing]]. Most routing material in the vault is about
choosing a model; here the router chooses a **specialist and a workflow phase**, and the reliability
gain is attributed to the router **reasoning less**. The closing line — "The most important component in
our AI agent system is the one that does the least work" — is the thesis.

The runtime knowledge-loading pattern is also notable for [[Agent Frameworks]]: domain knowledge lives in
files owned by specialists, so updating behavior means editing a knowledge file, not redeploying a router.

## Tensions / open questions

- **No ablation.** The article does not separate the effects of deterministic routing, context
  isolation, workflow templates, and runtime knowledge loading. Any of them could carry the benefit.
- No failure rates, retry counts, escalation rates, or controlled baseline experiment for the thin
  orchestrator itself are reported.
- "Under an hour" has no controlled design or exact workload definition, and compares against **earlier
  versions of their own process** — improvements may come from many simultaneous changes.
- "Two-thirds landing without significant edits" is not a formal quality or correctness metric.
- The cited **65.3% vs 16.6%** result is third-party evidence for a related design on a different
  workload; it does not validate Meta's deployment.
- The authors' own caveats: specialization trades generality for depth, each specialist lacks the full
  picture by design, a new workflow may require careful reuse and sequencing, and the proposed
  continuous-improvement loop is **future work gated by human review**.
- Nothing establishes that thin orchestrators generally improve reliability across domains.

## Affected pages

- [[Agent Delegation]]
- [[Context Engineering]]
- [[Model Routing]]
- [[Agent Frameworks]]
- [[Meta]]

## Raw capture

- [[The Thin Orchestrator How We Made Our AI Agents More Reliable by Giving the Router Less to Do]]

## Citations

- Raw capture: [[The Thin Orchestrator How We Made Our AI Agents More Reliable by Giving the Router Less to Do]]
- Canonical URL: <https://engineering.fb.com/2026/10/19/ml-applications/thin-orchestrator-ai-agent-architecture/>
- Published 2026-10-19; captured 2026-10-22.
- Cites a Mount Sinai multiagent preprint, not read during this ingest.

## Related pages

- [[Multi-Tenant Agent Architecture]]
- [[Agentic Loop]]
- [[Agent Workflow Maturity]]
- [[Graph Engineering]]
- [[AI Agents in Production]]
- [[Harness State Authority]]
- [[Agent Skill]]
