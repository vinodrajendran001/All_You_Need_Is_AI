---
type: concept
created: 2026-08-12
updated: 2026-10-23
tags:
  - concept
  - ai-agents
  - frameworks
  - sdks
source_ids:
  - src-2026-08-12-alyona-vert-agent-frameworks-sdks
  - src-2026-06-05-systemdesign42-system-design-academy
  - src-2026-08-18-harry0703-moneyprinterturbo
  - src-2026-09-13-adedeji-multi-agent-code-review
  - src-2026-09-13-weinmeister-build-ai-agents-google-cloud
  - src-2026-09-13-nevsky-gemini-multi-agent-system
  - src-2026-09-13-rahmat-adk-gemini-enterprise
  - src-2026-10-19-rath-thin-orchestrator
status: active
---

# Agent Frameworks

## Definition

Agent frameworks are reusable runtimes and architectural toolkits for coordinating model calls, tools, state, memory, workflows, human approval, tracing, and deployment. They sit above model APIs and often overlap with SDKs, which primarily simplify access to lower-level platform operations.

## Why it matters

A framework can remove large amounts of plumbing, but it also establishes state models, context behavior, failure semantics, security boundaries, and migration costs. Framework selection is therefore an architectural choice, not merely a package preference.

## Current synthesis

### Selection dimensions

Choose based on the system being built:

- **Control-flow model:** free loop, event workflow, state machine, or graph.
- **Durability:** in-memory turns versus checkpointed long-running execution.
- **Language and type system:** Python, TypeScript, .NET, and structured validation needs.
- **Data plane:** general tools versus document/RAG-centered processing.
- **Interaction modality:** text, computer use, or real-time voice/multimodal sessions.
- **Multi-agent needs:** explicit handoffs, role-based crews, simulations, or fan-out/fan-in.
- **Operations:** tracing, evaluations, human approval, deployment, storage, and access control.
- **Abstraction cost:** context overhead, debugging opacity, lock-in, and migration surface.

### Ecosystem families

[[Alyona Vert - 13 Frameworks and SDKs for Building AI Agents]] maps representative families:

- stateful graph runtimes such as LangGraph, Google ADK, and Microsoft Agent Framework;
- typed general-purpose runtimes such as Pydantic AI;
- role-based multi-agent systems such as CrewAI and CAMEL-AI;
- data-centric systems such as LlamaIndex;
- lightweight code-action libraries such as smolagents;
- TypeScript-native stacks such as Mastra;
- voice/multimodal infrastructure such as LiveKit Agents.

### Frameworks do not remove core design work

A framework supplies mechanics, not a trustworthy objective or verifier. Teams still need [[Context Engineering]], [[Agent Security and Governance]], [[Multi-Turn Evaluation]], and explicit failure handling. A hand-written loop remains preferable when the task is small and framework features would add more state and context than value.

## Integration breadth as its own architecture

[[harry0703 - MoneyPrinterTurbo]] is a useful counterexample to this page's framework-selection axes, because its value is not in any of them. It turns a keyword into a finished short video by orchestrating script generation, stock or local footage, speech synthesis, subtitles, music, rendering, and optional publishing, exposed through agent, web, API, and CLI surfaces over one workflow — and its architectural contribution is **provider abstraction plus deterministic media stages**, not a new control flow or learning algorithm.

The pattern worth extracting: model-generated content sits in the middle of a pipeline whose surrounding stages are conventional and deterministic. The model writes the script; ffmpeg renders the video. Frameworks are usually compared on how they orchestrate model calls, but a large share of real agent systems are mostly *not* model calls, and the abstraction that matters is the one over providers — hosted APIs, gateways, and local Ollama-compatible models behind one interface.

The caveats are the ones any repository README invites: it reports capabilities rather than controlled quality or reliability evidence, and "one click" conceals substantial configuration, licensing, stock-media rights, provider cost, and auto-publishing policy questions.

## The Google Cloud stack makes the framework boundary visible

Four Google Cloud publication sources separate layers that vendor diagrams often collapse.
[[Karl Weinmeister - Build AI Agents Your Way on Google Cloud]] places the framework beside, not
inside, the model, tool protocol, grounding system, inter-agent protocol, and runtime. In its map,
ADK, CrewAI, or LangGraph structure logic; Gemini or Gemma supplies the model; MCP supplies tools;
A2A supplies cross-system interoperability; and Agent Engine, Cloud Run, or GKE supplies execution.

The implementation articles make those boundaries concrete:

- [[Ayo Adedeji - Agents That Prove, Not Guess]] uses ADK to coordinate four reviewers, while
  Python AST parsing, `pycodestyle`, and sandboxed execution remain ordinary deterministic tools.
- [[Alex Nevsky - Building a Multi-Agent AI System with Gemini 3 and Google Cloud]] uses AutoFlow
  for transfer and Pydantic schemas for handoffs. Those contracts, not the agent labels, make the
  topology debuggable.
- [[Roushanak Rahmat - From ADK to Gemini Enterprise]] separates ADK logic from Agent Engine
  execution and Gemini Enterprise discovery. A chat surface is therefore not the runtime or the
  authorization layer.

These are vendor-authored tutorials, not comparative evidence that ADK is better than another
framework. Their durable contribution is the decomposition: **framework, runtime, and distribution
plane are different portability boundaries.**

## A 1,300-line in-house router is one answer to the build-versus-adopt question

This page's open question about building on a framework versus extracting a small internal harness now
has a worked data point on the "extract" side. [[Plawan Rath et al - The Thin Orchestrator]] reports a
Meta Engineering system in which the coordinating layer is **roughly 1,300 lines** handling **20+
workflows** across **14 specialist agents**, and its distinguishing property is that the coordinator
performs **no domain work at all** — no configuration generation, no reasoning about code, no contact
with the codebase. On this page's selection dimensions, the control-flow model is a **state machine**
and the authors keep it in ordinary code rather than expressing it through a framework abstraction
over model calls.

Two patterns transfer independently of whether a team writes its own runtime.

**Runtime knowledge loading relocates the extension point.** The system maintains **25+ domain
knowledge files**, typically a few thousand tokens each, loaded **at runtime by the specialists** that
need them rather than embedded in the coordinator. Changing agent behaviour is therefore editing a
knowledge file, with updates taking effect in later sessions and no coordinator change or redeploy.
Where this page's Google Cloud material separates framework, runtime, and distribution plane as
portability boundaries, this adds a fourth: **the knowledge plane**, which can be versioned and shipped
on a different cadence from the code that routes.

**A uniform specialist template is what makes the roster extensible.** Each specialist carries its own
domain knowledge, execution steps, discovery patterns, and troubleshooting mappings in the same shape,
and the authors state that a **15th subagent** would require no new structural design. That is an
**architectural claim about their template, not a measured result** — nothing in the source adds an
agent and reports the cost.

The evidential limits are substantial and apply to the whole design. All operational figures are
Meta's own, and the article reports **no ablation** separating deterministic routing, context
isolation, workflow templates, and runtime knowledge loading, so no individual pattern above is shown
to carry the benefit. The authors' recommendations — deterministic routing, uniform specialists,
workflow templates, runtime knowledge loading, an explicit deterministic/probabilistic boundary — are
**proposals**, as is their expectation that scaling will mean adding templates and knowledge files
rather than rebuilding agents. Their continuous-improvement loop is stated as **future work gated by
human review**, not a shipped capability. And the tradeoff is acknowledged: specialization buys depth
at the cost of generality, and a genuinely new workflow still requires careful reuse and sequencing of
existing agents.

## Open questions

- Which framework behaviors can be compared under equivalent end-to-end tasks?
- How portable are traces, state, tools, and workflows across runtimes?
- When should teams build on a framework versus extract a small internal harness?
- How should rapidly changing feature claims and project maturity be evaluated?
- A 1,300-line router is small because its domain is enumerable: a fixed specialist roster and a known
  set of workflows. What is the equivalent size, and the equivalent coupling cost, for a domain whose
  intents cannot be listed in advance?
- Runtime knowledge loading makes behaviour editable without redeploying. Nothing reported says how
  those files are reviewed, versioned, or regression-tested, which is the governance question this page
  already asks of framework-managed state.
- No source yet compares a hand-written deterministic state machine against the same workflow expressed
  in a graph framework such as LangGraph or ADK on one task.

## Related pages

- [[Plawan Rath et al - The Thin Orchestrator]]
- [[Meta]]
- [[Agent Delegation]]
- [[Context Engineering]]
- [[Coding Agent Harness]]
- [[Graph Engineering]]
- [[Agentic Loop]]
- [[AI Agents in Production]]
- [[Real-Time Voice AI]]
- [[Alyona Vert - 13 Frameworks and SDKs for Building AI Agents]]
- [[harry0703 - MoneyPrinterTurbo]]
- [[Model Routing]]
- [[Ayo Adedeji - Agents That Prove, Not Guess]]
- [[Karl Weinmeister - Build AI Agents Your Way on Google Cloud]]
- [[Alex Nevsky - Building a Multi-Agent AI System with Gemini 3 and Google Cloud]]
- [[Roushanak Rahmat - From ADK to Gemini Enterprise]]
- [[Google Cloud]]
