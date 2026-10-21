---
title: "The Thin Orchestrator: How We Made Our AI Agents More Reliable by Giving the Router Less to Do"
source: "https://engineering.fb.com/2026/10/19/ml-applications/thin-orchestrator-ai-agent-architecture/?utm_source=tldrai"
author:
  - "[[Plawan Rath]]"
  - "[[Akhil Jindal]]"
  - "[[Ashwini Verma]]"
published: 2026-10-19
created: 2026-10-21
description: "Sometimes, giving an AI agent all of the knowledge it needs is the wrong approach.  At Meta, we’ve seen notable improvements in efficiency and accuracy by keeping the orchestration layer of o…"
tags:
  - "clippings"
---
- Sometimes, giving an AI agent all of the knowledge it needs is the wrong approach.
- At Meta, we’ve seen notable improvements in efficiency and accuracy by keeping the orchestration layer of our data pipeline agents deliberately thin: It routes work and enforces reliability checks, while specialized agents do the domain reasoning.
- We’re sharing our own process and insights, plus how any team can apply this to their production AI agents.

We built a 1,300-line orchestrator that routes 20+ workflows to 14 specialized AI agents. It performs zero domain work itself. That’s the point.

When we first deployed AI agents to automate data column onboarding across Meta’s recommendation systems — a process spanning three code repositories, three programming languages, and up to six pipeline stages that must stay in sync — we did what most teams do: We built one smart agent that knew everything.

It worked in demos. In production, it started hallucinating.

The fix wasn’t better prompts or a bigger context window. It was giving the central agent less to do. We call this the thin orchestrator pattern: a router that owns sequencing and reliability checks, and leaves every domain decision to specialists.

## The Problem: More Context, Worse Results

Our pipeline is config-as-code: Python configurations drive C++ code generation, which feeds data processing services, which populate analytics systems. Onboarding a single data column requires coordinated changes across configuration registries, backend services, and data pipelines, and each column moves through up to six stages before its data arrives.

Our first approach was a single AI agent loaded with all domain knowledge, configuration schemas, code generation rules, pipeline routing logic, validation requirements, and population patterns for 10+ data sources.

The agent had everything it needed. That was the problem.

Past a certain context threshold, additional knowledge *degraded* rather than improved performance. The agent would cross-contaminate concepts, applying field naming conventions from one subsystem to another, or using a code generation pattern meant for one data source when populating from a different one. A [preprint from the Windreich Department of Artificial Intelligence](https://www.nature.com/articles/s44401-026-00077-0) and Human Health at Mount Sinai found that orchestrated multiagent systems held 65.3% accuracy at 80-task batches where single agents fell to 16.6%, while reducing token usage up to 65-fold. The authors attribute this to the design’s isolation of tasks, which prevented context interference. We were experiencing the inverse, a single agent drowning in its own knowledge.

We also evaluated an alternative single-agent approach. Its success rate was 70-80% *with* manual prompt engineering per task: An engineer had to craft a custom system prompt for each specific job. Without that handholding, success dropped to 10-20%. This wasn’t a prompt engineering problem. It was an architectural one.

## The Approach: A Thin Router With Specialist Workers

We split the system into two layers:

1. **A deterministic orchestrator** that performs zero domain work. It classifies intent, gathers required fields, runs reliability checks, and delegates to the right specialist. It never reasons about code, never generates configurations, and never touches the codebase. It’s a router.
2. **Fourteen specialized subagents**, each a complete domain expert with isolated context. A schema management agent knows configuration registries. A population agent knows how to generate code for each of 10 data sources. A validation agent knows build systems and quality checks. No agent sees the full picture. That’s the feature, not the bug.

The orchestrator follows a fixed 7-step protocol for every request:

1. **Read** the relevant subagent’s instruction file.
2. **Check** if the target already exists (prevent duplicates).
3. **Gather** required fields from the user.
4. **Auto-discover** what can be inferred (repository type, existing configurations).
5. **Reliability gate** check for active warnings or required reviewers.
6. **Delegate** to the subagent with full context.
7. **Handle** results and surface errors, confirm success.

Steps 1–5 and 7 are deterministic. Only step 6 involves large language model (LLM) reasoning, and it happens inside an isolated subagent with only its domain knowledge loaded.

## What We Built: Workflow Templates, Not New Agents

![](https://engineering.fb.com/wp-content/uploads/2026/10/Meta-Thin-Orchestrator-workflow.jpg)

One architectural insight was separating *what* needs to happen from *how* each step is performed. The orchestrator defines phase ordering through workflow templates — deterministic state machines that constrain the LLM’s decision space:

- **Column Onboarding:** Schema → Validation → Population → Testing
- **Event Onboarding:** Schema → Population → Validation → Testing → Event Processing
- **Pipeline Migration:** Assessment → Planning → Population → Validation → Monitoring

Each workflow template reuses the same pool of 14 subagents in different sequences. When we needed to support pipeline migration, a completely new use case, we didn’t build new agents. We wrote a new workflow template that sequenced existing agents differently. Zero new agent code. Full production capability.

Each subagent follows a standardized structure:

- **Knowledge sources:** which domain files to load at runtime (typically a few thousand tokens each).
- **Pre-gathering checklist:** what the orchestrator must collect before delegation.
- **Step-by-step workflow:** the domain-specific execution plan.
- **Discovery patterns:** how to find relevant code patterns in the monorepo.
- **Troubleshooting:** error-to-resolution mappings for common failures.

This uniformity means adding a new subagent is templated work, not greenfield engineering. The 15th subagent looks structurally identical to the first.

Knowledge files are loaded on demand at subagent execution time, not embedded in the orchestrator. We maintain 25+ knowledge files organized by workflow domain. When a knowledge file is updated, the next session automatically uses the latest version — no orchestrator changes required. The same knowledge files serve multiple platform implementations of our agent.

## Results

![](https://engineering.fb.com/wp-content/uploads/2026/10/Meta-Thin-Orchestrator-results.png) Configuration prep for a new column took three to four days by hand and about a day with our earlier config-driven system. The thin orchestrator system does it in under an hour.

For broader context: About two-thirds of the system’s changes land without significant human edits. It gets there by trading generality for deep domain knowledge, a deliberate architectural choice. The orchestrator is general; the subagents are specialists.

## Why This Works (And Why Heavyweight Orchestrators Don’t)

The conventional approach is to make the orchestrator the smartest component — give it all the context and let it reason about what to do and how to do it. This works until it doesn’t, and it stops working exactly when you need it most — at scale, with complex multi-step workflows, across heterogeneous subsystems.

The thin orchestrator works because it aligns architectural boundaries with computational boundaries:

- **Deterministic decisions stay deterministic.** “Which subagent handles this?” is a routing decision, not a reasoning task. Don’t use an LLM for it.
- **Context isolation prevents cross-contamination.** The population agent for data source A never sees data source B’s patterns. It can’t hallucinate the wrong one.
- **Failures are contained.** If a subagent fails, the orchestrator retries or escalates. The failure doesn’t corrupt the orchestrator’s state or other subagents’ contexts.
- **The system improves at every layer independently.** A better model improves all 14 subagents simultaneously. A knowledge file update takes effect immediately. A new workflow template unlocks new capabilities without touching agents. No single component carries the full weight.

## How to Apply This to Your AI Agents

This pattern isn’t specific to data pipelines. Any team building production AI agents can benefit:

1. **Separate routing from reasoning.** If your orchestrator is making domain decisions, it’s doing too much. Routing should be deterministic: keyword matching, intent classification, field gathering. Push all domain reasoning into isolated subagents.
2. **Design subagents as structurally uniform specialists.** Every subagent should have the same structure: knowledge sources, required inputs, execution steps, error handling. This makes adding new capabilities templated work rather than architecture changes.
3. **Use workflow templates, not new agents, to scale.** When you need a new use case, first ask: Can I sequence existing agents differently? If you can’t reuse agents across workflows, your agents are too coupled to specific use cases.
4. **Load knowledge at runtime, not at build time.** Embed knowledge in the orchestrator and every update requires redeployment. Load it on demand and updates take effect immediately, across all platforms.
5. **Draw the deterministic/probabilistic boundary explicitly.** For every component, decide: Is this a routing decision (deterministic) or a reasoning task (probabilistic)? The orchestrator should be on one side, the subagents on the other. Don’t mix them.

The strongest argument for a thin orchestrator is the failure mode of the alternative. When a heavyweight orchestrator hallucinates, the error spreads to everything downstream: it routes to the wrong agent, gathers the wrong fields, or skips reliability checks. A thin orchestrator leaves little room for hallucination because its routing and reliability steps don’t rely on LLM reasoning. It follows a fixed protocol. The creativity happens downstream, in isolated, domain-scoped contexts where hallucination risk is minimized and failures are contained.

## What’s Next

We’re scaling this architecture to handle an increase in data columns across new pipeline domains. The compositional thesis predicts this will work because scaling means adding workflow templates and knowledge files, not rebuilding agents. We’re also exploring how the system can continuously improve from production usage, using automated feedback loops to identify failure patterns and propose targeted improvements to subagent knowledge, with human review always gating any changes.

The counterintuitive lesson: the most important component in our AI agent system is the one that does the least work. Keep your orchestrator thin and your specialists deep, and the whole system becomes more reliable.

## Acknowledgements

*This work was a team effort. Some other people who contributed to this effort include:* *Mani Bhushan, Rahul Maliakkal, Jae Ha, Chakrapani Kumar, Vivek Tiwari, and Amanda Yin.*