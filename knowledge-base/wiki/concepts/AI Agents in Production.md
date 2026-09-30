---
type: concept
created: 2026-05-21
updated: 2026-09-30
tags:
  - concept
  - ai-agents
  - production
  - productivity
source_ids:
  - src-2026-05-21-bytebytego-batch
  - src-2026-05-18-rag-architecture-comparison
  - src-2026-06-02-alphasignal-look-past-rag-pipeline
  - src-2026-06-03-liquid-ai-lfm2-5-8b-a1b
  - src-2026-06-03-nvidia-locateanything
  - src-2026-06-04-efficient-reasoning-edge
  - src-2026-06-05-pguso-agents-from-scratch
  - src-2026-06-05-systemdesign42-system-design-academy
  - src-2026-06-10-bytebytego-token-spend-routing
  - src-2026-06-22-cameron-wolfe-agentic-rl-frameworks
  - src-2026-06-22-djfarrelly-agent-loop-architecture
  - src-2026-06-22-alphasignal-agent-skill-optimization
  - src-2026-06-24-bytebytego-llm-vs-slm
  - src-2026-07-06-sarthak-rastogi-production-agent
  - src-2026-07-30-teaching-open-model-science
  - src-2026-08-05-aibuilderclub-ai-agents-101-part-5
  - src-2026-08-05-aibuilderclub-harness-six-components
  - src-2026-08-05-aibuilderclub-how-to-evaluate-ai-agents
  - src-2026-08-05-aibuilderclub-ai-agent-runaway-cost
  - src-2026-08-05-aibuilderclub-agent-tool-permissions-canary
  - src-2026-08-05-aibuilderclub-who-owns-your-ai-agents
  - src-2026-08-07-zach-lloyd-computer-use-verification
  - src-2026-08-07-avi-chawla-claude-code-cost
  - src-2026-08-07-rllm-realtime-rl-agents
  - src-2026-08-12-yoko-li-loop-convergence
  - src-2026-08-12-alyona-vert-agent-frameworks-sdks
  - src-2026-08-22-grok-bot-systems-engineering-working-note
  - src-2026-08-21-anthropic-ai-native-sdlc
  - src-2026-08-25-bytebytego-stealing-reasoning-traces
  - src-2026-09-06-rastogi-agent-observability
  - src-2026-09-07-bytebytego-llm-error-handling
  - src-2026-09-13-weinmeister-build-ai-agents-google-cloud
  - src-2026-09-13-nevsky-gemini-multi-agent-system
  - src-2026-09-13-rahmat-adk-gemini-enterprise
  - src-2026-09-13-prabhulal-production-rag-adk
  - src-2026-09-13-virinchi-google-cloud-mcp-security
  - src-2026-09-13-tessier-gcp-model-armor
  - src-2026-09-27-fd-agent-muse-compute-demand
  - src-2026-09-28-bytebytego-agents-can-pay
status: active
---

# AI Agents in Production

Production AI agents are not just prompts wrapped around tools. They are controlled workflows that manage state, context budgets, tool boundaries, risk levels, and human review. The Grab and Figma articles are useful because they describe real agent deployments where the hard part is operational design rather than model novelty.

## Brain, hands, and orchestration

Grab describes a clean production pattern: **decouple the brain from the hands**. The LLM handles reasoning, while specialized agents and tools fetch metadata, trace data lineage, run SQL, inspect pipeline health, or prepare code changes. This is a concrete enterprise implementation of the [[Agentic Loop]]: the loop becomes a routed workflow across multiple specialists rather than a single model repeatedly calling a single tool.

The same pattern appears in Figma’s design workflows. The coding agent does not directly “understand Figma” on its own. It relies on an MCP server that exposes a carefully shaped set of tools and structured context. The agent reasons about which tool to call; the surrounding system defines what data is exposed and how it is transformed.

## Tool use only works when the interface is shaped for the model

Both Grab and Figma show that raw access is usually the wrong product surface.

- Grab learned that too many tools with verbose descriptions degrade both speed and quality.
- Figma learned that raw screenshots lack precision and raw JSON overwhelms the context window.

The production answer in both cases is the same: expose **fewer, better, more model-legible interfaces**. That is exactly the systems layer described by [[Tool Use and Function Calling]] and standardized, in Figma’s case, by [[Model Context Protocol]].

The new [[Direct Corpus Interaction]] source adds an important counterpoint: "better interface" does not always mean "higher-level interface." For debugging and code-search agents, hiding the corpus entirely behind vector retrieval can remove the exact strings, paths, and version pins the agent needs. In those tasks, the right production surface may be a bounded terminal-style interface over raw files rather than a prefiltered semantic layer.

## Context management is a first-class production problem

Agents fail when context grows faster than the orchestration layer can compress it.

- Grab tracks token counts, summarizes older turns, and prunes tool outputs between agent handoffs.
- Figma explicitly recommends a **scan, then zoom in** workflow using `get_metadata` before `get_design_context` so agents do not blow through MCP response budgets.

This makes context shaping part of the product design. Production agents need not only the right tools but also the right amount of context at the right time.

DCI sharpens this lesson. Raw `grep` and `find` output can be more faithful than chunk retrieval, but it can also flood the context window or stall the loop with overly broad commands. Production DCI therefore still needs shaping: limits, filters, staged exploration, and interfaces that keep raw access legible.

## Risk-based autonomy beats one-size-fits-all automation

Grab splits read-only investigation from write-heavy enhancement work because the blast radius is different. Investigative flows can run with lighter oversight; code and schema changes stay human-gated. Figma’s design↔code roundtrip is similarly bounded: design structure moves between systems, but business logic and state do not automatically survive, which keeps a human developer in the loop.

This is the same principle that powers safer [[Retrieval-Augmented Generation|Agentic RAG]] systems: give the model more autonomy where the cost of a wrong intermediate action is low, and tighten control when actions mutate production state.

## Persistent memory and workflow state matter

Production agents usually need memory outside the model weights.

- Grab uses Redis for fast session needs and PostgreSQL for conversation history plus agent metadata.
- Figma externalizes design state into the Figma file itself and uses MCP tools as the access boundary.

In both cases, the agent is effective because the surrounding system remembers more than the immediate prompt.

## Local and perceptual agents widen the production surface

The newer sources show that "production agent" no longer means only a cloud workflow over text tools.

- [[Liquid AI - LFM2.5-8B-A1B]] shows a **local/private deployment path**: a sparse model can run an interactive tool loop with dozens of tools and many MCP servers on a single laptop, which makes inference speed and model architecture part of the product surface.
- [[NVIDIA - LocateAnything]] shows a **perceptual deployment path**: GUI agents, document agents, and embodied systems need fast and precise grounding over images and screens, so spatial decoding quality becomes as important as text generation quality.
- [[Efficient Reasoning on the Edge]] adds a **resource-aware local reasoning path**: on-device agents need active control over whether to reason, how long to reason, and how much KV state they can afford. Switcher routing, budget forcing, KV-cache reuse, and verifier-guided parallel decoding become orchestration primitives rather than only model-level tricks.

This broadens the agent-design problem. Production agents need not only reasoning and tools, but sometimes also local privacy guarantees and high-fidelity spatial interfaces to the world they act on.

## Durable orchestration and skill libraries

[[djfarrelly - The Agent Loop Architecture]] adds the execution-layer version of production readiness. A production agent loop cannot be only a long-running process, because crashes, deploys, OOMs, and spot-instance reclamations can make the loop forget which step already ran. The durable requirements are step-level checkpoints, independent retries, failure hooks, guaranteed event delivery, concurrency control, sub-agent lifecycle management, hot deploys, and run history.

The source's useful reframing is: agents are **loops + skills + orchestration**. The LLM and tools sit inside that structure. The loop decides when work is needed; the [[Agent Skill|skill]] is the reusable durable workflow; the orchestrator makes the workflow survivable and observable.

[[Alpha Signal - How your agents can write and optimize their own skills]] adds the text-artifact side of the same pattern. It frames a skill as a markdown operating procedure and surveys SkillOpt, GEPA, and EvoSkill as optimization loops that improve those skill files from task trajectories. This connects directly to production evals: self-optimizing skills require verifiers, representative held-out datasets, rejected-edit buffers or version control, and human-visible review.

The combined production rule is: **do not let agents self-modify unobservably**. If agents can write or optimize skills, those skills need versioned text, durable execution, run traces, eval gates, rollback paths, and developer ownership.

## Evals and telemetry as production requirements

[[pguso - Agents From Scratch]] adds two operational disciplines that are absent from the Grab/Figma treatment but are essential for running agents in production:

**Regression testing via golden datasets (Lesson 11):** A prompt change that improves phrasing can silently break JSON parsing, push structured output outside the context window, or alter routing logic. An eval suite — test cases with known inputs and expected outputs, run before every change — catches these silent regressions. The workflow: make prompt change → run evals → if any golden case fails, fix or revert → commit. This is software engineering applied to prompt changes.

**Runtime observability via structured telemetry (Lesson 12):** Evals prevent bad code from shipping; telemetry shows what shipped code is doing. Each LLM call, tool execution, and memory operation is logged as a span with a trace ID that links all operations in one agent interaction. Metrics (success rate, average latency, retry count) give at-a-glance system health. When something goes wrong, filtering logs by trace ID reveals the exact sequence of events.

The practical consequence: in production, a prompt is not done when it "seems to work" — it is done when it passes a golden dataset suite and is covered by runtime tracing that can diagnose failures after deployment.

## Training production agents with RL

[[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]] adds the training-side mirror of this production picture. If a production agent operates through tools and stateful environments, then [[Agentic Reinforcement Learning]] must train over isolated copies of those environments. Each rollout may need its own filesystem, browser, database, codebase, or simulated tool state so that one trajectory's side effects do not corrupt another's.

This reinforces several production requirements already on this page:

- **Environment isolation** is not only a safety boundary; it is a training requirement.
- **Standard tool/environment APIs** make new tasks pluggable into both serving and RL training.
- **Asynchronous orchestration** is needed because long-running agent trajectories have highly variable duration.
- **Run traces and step boundaries** matter for observability and for policy updates.
- **Context management** is part of the product and the trainer: retaining all tool output can degrade both inference and RL rollouts.

## Agentic design patterns and multi-agent architectures

[[systemdesign42 - System Design Academy]] documents several named patterns and multi-agent frameworks in its AI Engineering section that extend this page's framing:

**Agentic design patterns** — recurring structural solutions for how agents decompose and execute tasks. The most common documented patterns are:
- **ReAct (Reason + Act)**: interleave reasoning steps and tool calls rather than planning fully before acting. Reduces failure scope when environment state is uncertain.
- **Plan-and-Execute**: generate a complete plan first, then execute steps sequentially or in parallel. Better for deterministic workflows where the task scope is known upfront — aligns with [[Agent Planning]]'s AoT approach.
- **Reflection**: run the agent output through a critic (another LLM call or a verifier) before committing. Reduces hallucination in high-stakes outputs. The [[Efficient Reasoning on the Edge]] verifier pattern is a resource-constrained form of this.
- **Tool selection routing**: a lightweight router selects which specialized agent or tool handles each subtask rather than having a single agent call all tools. Mirrors the Grab "decouple brain from hands" pattern.

**Multi-agent architectures** — when the task exceeds the scope, context window, or specialization of a single agent, multiple agents coordinate:
- **Orchestrator–Worker**: one orchestrator agent decomposes tasks and delegates to specialized worker agents. Each worker has a narrow tool set and focused context. The orchestrator synthesizes results. This is the most common production pattern for complex, long-running tasks.
- **Peer-to-peer (Collaborative)**: agents communicate bidirectionally, each contributing domain expertise. Useful for multi-discipline tasks where no single agent has all the needed knowledge.
- **Hierarchical**: nested layers of orchestrators and workers for tasks that require deep decomposition. Complexity cost is high; reserved for tasks where the parallelism gain justifies coordination overhead.

Key production constraint: **context isolation between agents is a reliability requirement**. Each agent should receive only the context it needs for its task. Sharing full conversation history across all agents floods every context window with irrelevant content, degrades specialization, and increases cost. [[Context Engineering]] becomes the discipline for managing what each agent sees.

**Context engineering as an agent-level primitive** — the [[Context Engineering]] framing unifies multiple production patterns already described on this page: Figma's `get_metadata` first / `get_design_context` second workflow is context engineering. Grab's turn summarization and token tracking is context engineering. The On-Device switcher routing that decides whether to reason is context engineering at the inference level. Production agents need context engineering embedded in their orchestration layer, not bolted on afterward.

## Cost governance and model routing

[[ByteByteGo - Token Spend Out of Control - The Case for Smarter Routing]] adds the economic version of the same story. Even a well-designed agent still resends large contexts through many loop steps. Once that is true, production quality depends not only on *what* context is sent, but also on *which model* receives each step.

- Kilo's gateway pattern is the cleanest example here: one normalized entry point in front of many providers, plus a routing layer that maps known agent modes (planning, debugging, editing, background work) to model tiers.
- The strongest production rule is **route on the strongest signal you already have**. If the agent already knows it is in planning mode, use that signal instead of trying to infer difficulty from raw prompt text.
- This creates a second form of routing distinct from tool routing:
  - **tool routing** chooses the right tool or specialist agent
  - **model routing** chooses the right model tier for the current step
- Routing also introduces a subtle cross-model failure mode: if one provider's reasoning model hands off to another provider's model mid-task, internal intermediate reasoning may have to be dropped because the formats are not mutually readable.
- The economic lesson is durable: caching helps, but it does not solve high-volume agent spend by itself. Routing and context compression are complementary, and both belong in the production design.
- [[ByteByteGo - Large Language Models vs Small Language Models]] adds three concrete hybrid patterns for production agents:
  - **small-model routing** for common/easy requests with escalation to larger models;
  - **small-model guardrails** before and after expensive model calls;
  - **small-model drafting/speculative decoding** where a fast model proposes candidate tokens and a larger model verifies them (see [[Speculative Decoding]]).

These patterns make [[Small Language Models]] production infrastructure rather than merely weaker substitutes for large models.

## A layered production architecture

[[Sarthak Rastogi - Making an AI Agent Production-Ready]] gives the vault its most concrete end-to-end blueprint, organized around the failure modes a demo ignores: prompt-injection, cost blowups from re-answering identical questions, no observability at 2am, and partial answers to multi-part questions. The durable, tool-agnostic patterns:

- **Guards before the graph; work inside it.** Cheap protections (rate limiting, logging, and a **semantic cache** check) run *before* the agent framework is even invoked — a cache hit should be a pure lookup-and-return. Everything that *is* work (safety, retrieval, generation, validation) is a node in one graph, with **one trace per request** for debuggability.
- **Safety is a dedicated first node:** PII scrubbing plus prompt-**attack detection** (an isolated microservice with its own memory budget), treating untrusted input as hostile by default.
- **Validate the output, not just the input:** run **faithfulness** (hallucination vs retrieved context) and **completeness** (did we answer every part?) checks in parallel — an inline production instance of [[LLM-as-a-Judge]].
- **Resilience is explicit:** retries with backoff, circuit breakers around external dependencies, and resource isolation so a security model can't starve the main app.
- **Evals gate change, not just launch:** a regression suite compares faithfulness + completeness against a baseline on every prompt/model change, and A/B testing routes a fraction of traffic before cutover (see [[Multi-Turn Evaluation]]).

## The main lesson

The common pattern is not “let the model do everything.” It is **design an environment where the model can do a few high-value things reliably**. That means specialized agents, narrow tools, token-aware context management, human review, and interfaces that encode domain structure instead of dumping raw data.

## Scientific application and promotion gates

[[Bojan Jakimovski - Teaching an Open Model to Do Science]] turns those principles into a production-shaped scientific application. A Strands/FastAPI/React harness routes specialist tasks to a promoted LoRA adapter while retaining a larger base model for orchestration. The top-level agent delegates to narrow specialists with explicit tools, sources, and artifact identifiers; Python runs in an isolated sandbox; and plans, reports, and hypotheses are fixed flows rather than unconstrained chat.

The deployment gate is deliberately broader than a benchmark: held-out environment scores, verifier and trace review, and qualitative workflow testing must agree. Review checks whether citations and identifiers are usable, evidence-seeking is purposeful, ambiguity is handled, and uncertainty is acknowledged. This makes evidence provenance and inspectable trajectories first-class production requirements for high-stakes agents.

## Governance is part of the runtime

[[AI Builder Club - Build AI Agents]] adds an operational governance layer to this page. Production readiness includes not only a working graph and eval suite but also a named owner, an inventory of actual credential and tool reach, a kill switch, tested revocation, append-only intent/outcome logs, autonomy levels, and prewritten demotion triggers.

The collection's permission-canary pattern is especially useful: prove that an unguarded route can perform the damaging action, then require the guarded route to preserve the target *and* emit structured denial evidence. Silence is inconclusive. Cost reporting follows the same evidentiary standard—include evaluators, retries, sub-agents, and shared infrastructure, then report cost per successful outcome.

## Behavioral verification, full-cost traces, and learning gates

The August 7 sources add three production controls. Computer-use verifiers can reproduce and verify user-visible behavior with video evidence, but do not replace architectural and security review. Token attribution must include replayed tool results, schemas, memory, and prior context, not only user prompts. Continually trained agents need a promotion boundary: production trajectories may feed training, but updated checkpoints should pass held-out regressions and staged rollout before serving users.

The August 12 sources add two further controls: convergence must include impossibility and diminishing-return exits, and framework adoption must be evaluated as a runtime/governance decision rather than a shortcut around context, evaluation, or security design.

## Operations: state, evidence, and recovery

The architecture material above answers *how to build* a production agent. [[Grok Bot Systems Engineering Working Note]] answers the neglected other half — *how to run one* — and names the specific way deployments fail: if any operational invariant is missing, **the human quietly becomes the memory layer or the recovery system**. Naming five bots does not create a team if the user still copies context, chooses every next step, and checks every result.

Four contributions extend this page directly:

- **Six invariants** every production workflow needs — one current owner, explicit state, a durable artifact, observable evidence, a bounded retry policy, and a clear approval boundary — reducible to a minimum record of `task_id`, `owner`, `status`, `artifact`, `evidence`, `next_deadline`.
- **Typed handoffs instead of conversation.** A handoff is an interface between owners carrying a named artifact, a single named next owner, an evidence pointer, and the next acceptance test. Correspondingly, **"done," "looks good," and "I handled it" must not advance a workflow** — if the producer cannot point to evidence, the task stays in verifying or blocked. This is a sharper version of the "brain and hands" decoupling above: what crosses the boundary is a checkable object, not a summary.
- **An evidence ladder gating autonomy**, in which level 0 — the agent asserting completion — is never sufficient, and level 5 is an independent verifier pass. Producer and verifier must be separate, and the verifier must not silently repair the artifact.
- **The manager owns state, not work.** A router that repeatedly performs specialist work fills its context with execution detail and destroys the role boundary; deterministic routing rules come first, model classification only above a confidence threshold, a human above a risk threshold.

Its **architecture decision rule** is the useful counterweight to this page's accumulating patterns: choose the smallest architecture that externalises the *real* bottleneck — one agent for execution, a skill for repeatability, a routine for continuity, a specialist for durable expertise or permissions, a manager for routing, a verifier for trust — and add parallel workers only after inputs and convergence are stable. Two operational rules round it out: routines need idempotency keys so a retry cannot duplicate an external effect, and **silence is not success**, so a scheduled run that produces nothing must still emit a heartbeat. Developed in [[Agent Workflow Maturity]].

[[Anthropic - The AI-Native SDLC Playbook]] arrives at the same handoff conclusion from the software-organization side, where the typed artifact is a committed `intent.md`, `spec.md`, or `plan.md` and the commit chain doubles as the audit trail. Two independent sources converging on "pass artifacts and evidence, not transcripts" makes it the strongest operational claim in this cluster. See [[AI-Native Software Development Lifecycle]].

## Published traces are an unsanitisable secrets surface

Teams publish agent trajectories for reproducibility, debugging, and evaluation — practices this page and [[Multi-Turn Evaluation]] both encourage. [[ByteByteGo - How to Steal an AI Model's Private Thoughts]] shows the cost. Encrypted reasoning blocks travel inside those traces, they contain whatever the agent read while working, and **the publisher cannot inspect them**.

A scan of 6,708 public agent trajectories from GitHub and Hugging Face decoded 315,320 blocks and found, from genuine user sessions, 62 API keys, 33 passwords, 24 access tokens, 7 private keys, and 30 personal email addresses. 328 sessions leaked at least one item. Perfect scrubbing of the visible text would have removed **none** of it, because sanitisation operates on plaintext only.

Two operational rules follow, and they belong alongside the invariants above:

- **Strip opaque provider artifacts from any trace before publishing.** They cannot be cleaned, only removed.
- **Treat a resumed public run as untrusted input.** An instruction planted inside a block executes as prior context when the session resumes, and no one in the chain can read the payload.

The credential example is not hypothetical for this audience: an agent asked to remove hardcoded secrets from a repository must read those secrets, so they enter the trace before any answer exists. See [[Reasoning Trace Privacy]].

## The production gate is reconstructability, and the new failure category is semantic

Two September 2026 sources converge on what has to be true before an agent takes real traffic.

[[Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]] states the gate operationally: if nobody can answer *what did the agent do, why did
it do that, and what did it cost* for any single run from the last 30 days, the system **"does not touch
production traffic."** This is not evals — those judge whether the chain was good — and it is not logging,
since "a team can have TBs of logs and still have zero observability." It is the ability to reconstruct a
**causal chain**. Across 73 production agent incidents from January to May 2026, incidents without
decision-trace logging averaged **4.2 hours** to resolve against **under an hour** with full tracing, and
tool-call failures were the most common entry point, cascading into planning failures and wrong answers
before reaching a human. See [[Agent Observability]].

[[ByteByteGo - How to Deal With Errors and Failures in LLM-Powered Applications]] supplies the failure taxonomy that explains why ordinary monitoring misses this.
LLM applications fail in two categories: **technical failures**, where the operation cannot complete, and
**semantic failures**, where it completes perfectly and the result is still wrong, unsafe, irrelevant or
unusable. "A successful API request to an LLM doesn't guarantee that the response we receive is correct or
even usable." Conventional error handling covers only the first, because no exception is raised for the
second. See [[LLM Application Resilience]].

Three findings from the pair are worth holding as production rules.

**A near-zero fallback-response rate is a defect signal.** If an agent's `fallback_response_rate` is close
to zero, "that's not a good sign, it just means your agent has never met an ambiguous situation it didn't
confidently answer anyway."

**Guardrails need their own tests.** Feeding known-bad input on a schedule — *sabotage validation* — is
the only way to know a check still fires; one team running it found **67 checks silently no-op'ing for
months**.

**Retries multiply side effects at a computable rate.** 20,000 runs/day × 6 tool calls × 0.5% failure × 3
attempts is roughly **1,800 retried calls daily**, each a chance to fire a refund or a write twice. Both
sources reach the same requirement from opposite directions: tool calls need idempotency keys, and the
trace needs `retry_count`, or a retry storm and a prompt-injection campaign are indistinguishable.

A cautionary data point on buying rather than building: adoption metrics ship early because they are easy
and sell internally, while step-level reasoning traces and cost-per-task attribution arrive late.

## Production is a stack of control planes, not a deployment command

The Google Cloud cluster maps a production agent into replaceable planes:

1. **Logic and contracts** — ADK or another framework.
2. **Models** — Gemini, Gemma, or a model reached through another API layer.
3. **Tools and grounding** — MCP, APIs, connectors, search, vector stores, or RAG.
4. **Runtime and state** — Agent Engine, Cloud Run, or GKE.
5. **Identity and authority** — service identities, end-user identity, IAM, confirmation, and
   tool-side authorization.
6. **Distribution** — an application, A2A endpoint, or Gemini Enterprise catalogue.
7. **Evidence and recovery** — traces, evaluations, logs, backups, time travel, and versioning.

[[Karl Weinmeister - Build AI Agents Your Way on Google Cloud]] supplies the broad map.
[[Roushanak Rahmat - From ADK to Gemini Enterprise]] makes runtime and distribution separate.
[[Alex Nevsky - Building a Multi-Agent AI System with Gemini 3 and Google Cloud]] makes one action
agent the sole writer, puts confirmation on refunds and escalates amounts over **$500**.
[[Arjun Prabhulal - Production-Grade RAG with ADK and Vertex AI RAG Engine]] adds deployment
scaffolding and traces, but no retrieval-quality evidence — a deployed RAG agent is not thereby
production-ready.

The security sources close the loop. [[Virinchi T - Google Cloud MCP Security Framework]] adds
dedicated identities, recurring tool inventory, deny policies, tenant-separated state, and recovery.
[[David Tessier - GCP Model Armor]] adds centrally enforced pre- and post-model content inspection.
Both are vendor-authored and neither makes probabilistic filtering an authorization boundary.

## Capacity planning is a chain of ratios, and every architecture choice on this page moves it

This page answers how to build and run an agent; it has never costed one at scale.
[[FD - Agent Muse Compute Demand]] supplies that layer for a hypothetical consumer deployment, and the
framing matters more than the totals: it is a **bottom-up scenario estimate built on assumptions**,
not a measurement of Meta's infrastructure, and the **100M DAU** premise is hypothetical - the post
does not establish Meta's actual deployment scale.

The useful artifact is the chain, because each link is an assumption a team can replace with its own
measurement. **100M DAU** x **two active hours per day** / 24 = **~8M average simultaneous active
VMs**; a **2.5x peak-to-average ratio** gives **~20M peak**; **~20% capacity headroom** gives **~25M
provisioned live VMs**, or roughly **25% of DAU live at once**. The separation that makes the chain
work is *logical versus physical*: the observed per-user sandbox advertises **2 vCPUs, ~8 GB of RAM,
and ~100 GB of persistent logical storage**, but none of that is a physical reservation.
Oversubscription is anchored on DeepSeek's DSec paper - **~30,000 physical cores**, **250 TB of
DRAM**, **~160 nodes**, peak concurrency above **380,000 sandboxes**, about **800 microVMs per node**
on roughly **188 physical cores**, or **~0.23 physical cores per live VM**. Muse is assumed *less*
efficient at **0.3-0.75**, base case **0.5**, giving **12.5M physical cores** (**~50K CPUs** at 256
cores, **~$800M**); memory extrapolated from a **single** observed instance at **~3 GB** gives **75
PB** (range **~75-100 PB**, **~$2B**).

The structural finding is the one worth carrying into design reviews. The entire sandbox/VM layer -
all the isolation, all the environments, all the tool execution surface - comes to an estimated
**~0.1 GW**, while total average power lands at **~1-2 GW**. Inference is the rest: **50
reasoning-equivalent events per DAU per day** at **5 Wh** each is **25 GWh/day**, or **~1.0 GW**. The
per-event energy is itself derived - a Microsoft study's median of **~0.31 Wh per normal query**, a
long reasoning query at roughly **15x the tokens** using about **13x the energy** (**~4 Wh**), widened
to an assumed **5-10 Wh**. The **3-4 GW** figure that travels with this analysis is a *sensitivity
conclusion under higher reasoning demand, not a forecast*.

That reframes most of the controls recommended above as capacity decisions. Reflection passes,
independent verifier runs, faithfulness and completeness checks in parallel, retries with backoff,
sabotage validation, orchestrator-worker fan-out - each adds reasoning-equivalent events per task, and
FD's scaling asymmetry is that **demand tracks reasoning-equivalent events per user, not user count**.
An agent that deliberates more raises compute demand with zero new users. Nothing here argues against
those controls; it argues that a production plan which counts users, requests, or sandboxes is
counting the wrong thing, and that the evidence ladder and the capacity model should be filled in
together.

The caveats are load-bearing. Active hours, peak ratio, headroom, oversubscription, memory residency,
events per user, energy per event, and hardware prices are all assumed rather than measured; the
**~3 GB** observation is a single instance and cannot establish fleet working-set behaviour; DSec's
sandbox workload may differ materially from Muse's; and the dollar figures exclude networking,
storage, orchestration, redundancy, facilities, cooling, depreciation, and operations. Treat the chain
as a template to instrument, not a result to cite. See [[Multi-Tenant Agent Architecture]] for the
isolation side of the same estimate and [[Tool Roster Economics]] for the per-turn side.

## Buying at runtime makes settlement a production dependency

The capacity chain above prices the compute an agent consumes; the other bill is what the agent buys
from third parties mid-loop. [[ByteByteGo - AI Agents Can Think, Now They Can Pay]] describes Machine
Payments Protocol, launched **18th March 2026** and co-authored by Stripe and Tempo, which keeps that
purchase on ordinary HTTP: an unpaid request returns **402** with a challenge (ID, amount, currency,
recipient, payment method, validity window), the agent authorizes and retries with a credential, and the
server returns the resource plus a **receipt**. The receipt matters operationally more than the protocol
does — it is a per-request cost record for external purchases, which the cost-governance material above
has only ever had for tokens.

Session mode is where production constraints bite. A single web search may be worth **just a cent** while
per-transaction fees exceed the payment itself, so the agent reserves funds and signs an **IOU per
request** — the article's example is **a tenth of a cent** — verified in **the few milliseconds a
signature check takes** and settled in one batched transaction. That is the amortization pattern this
page already records for batching and caching, applied to trust, and it adds two runtime dependencies an
agent loop did not previously have: a funded reserve, without which the loop stalls, and a settlement
path whose failure is invisible at request time because every individual request already succeeded.

The failure taxonomy is usable directly. A failed verification returns **another 402, not a 401**, with a
fresh challenge and a structured reason — `payment-insufficient`, `payment-expired`,
`verification-failed`, `invalid-challenge` — which lets the loop separate "top up and retry" from "not
permitted", the retriable-versus-terminal distinction that [[LLM Application Resilience]] treats as the
core error question. Two invariants belong in the runbook beside it: **unpaid requests must not cause
side effects**, so a payment failure is safe to retry, and **payment proofs are single-use**.

What it does not give a production owner is recourse. Payment proves **control of a key, not customer
identity**; reputation, abuse prevention, refunds, and disputes are explicitly out of scope; and there is
**no defined refund flow for one-off charges**. A spending cap therefore delivers a bounded loss, not a
correct purchase, and an operator who wants dispute handling has to build it outside the protocol. The
piece is a secondary explainer rather than a production measurement, and the Cloudflare figure it cites —
roughly **57.5% of HTTP requests to web content** — covers **all automated systems, not AI agents
specifically**. See [[Agent Payment Protocols]].

## Related pages

- [[Grok Bot Systems Engineering Working Note]]
- [[Anthropic - The AI-Native SDLC Playbook]]
- [[Agent Workflow Maturity]]
- [[AI-Native Software Development Lifecycle]]
- [[Grok Bot]]
- [[Context Engineering]]
- [[Model Routing]]
- [[Small Language Models]]
- [[ByteByteGo - Large Language Models vs Small Language Models]]
- [[Agent Skill]]
- [[Agentic Reinforcement Learning]]
- [[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]]
- [[djfarrelly - The Agent Loop Architecture]]
- [[Alpha Signal - How your agents can write and optimize their own skills]]
- [[Inngest]]
- [[ByteByteGo - Token Spend Out of Control - The Case for Smarter Routing]]
- [[systemdesign42 - System Design Academy]]
- [[Agentic Loop]]
- [[Tool Use and Function Calling]]
- [[Agent Planning]]
- [[Agent Memory]]
- [[Model Context Protocol]]
- [[Direct Corpus Interaction]]
- [[Retrieval-Augmented Generation]]
- [[Alpha Signal - As AI agents evolve, we need to look past the RAG pipeline]]
- [[Liquid AI - LFM2.5-8B-A1B]]
- [[Efficient Reasoning on the Edge]]
- [[NVIDIA - LocateAnything]]
- [[Mixture of Experts]]
- [[On-Device Reasoning]]
- [[Vision-Language Grounding]]
- [[Qualcomm AI Research]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[Coding Agent Harness]]
- [[Sarthak Rastogi - Making an AI Agent Production-Ready]]
- [[Speculative Decoding]]
- [[ByteByteGo]]
- [[AI Knowledge Base Overview]]
- [[Bojan Jakimovski - Teaching an Open Model to Do Science]]
- [[Loop Engineering]]
- [[Graph Engineering]]
- [[Agent Security and Governance]]
- [[AI Builder Club - Build AI Agents]]
- [[Zach Lloyd - The computer use verification skill that every agent needs]]
- [[Avi Chawla - 86 Percent of Your Claude Code Bill Has Nothing to Do With Your Prompts]]
- [[Continual Learning for Agents]]
- [[Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge]]
- [[Agent Frameworks]]
- [[ByteByteGo - How to Steal an AI Model's Private Thoughts]]
- [[Reasoning Trace Privacy]]
- [[Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]]
- [[ByteByteGo - How to Deal With Errors and Failures in LLM-Powered Applications]]
- [[Agent Observability]]
- [[LLM Application Resilience]]
- [[Sarthak Rastogi]]
- [[Karl Weinmeister - Build AI Agents Your Way on Google Cloud]]
- [[Alex Nevsky - Building a Multi-Agent AI System with Gemini 3 and Google Cloud]]
- [[Roushanak Rahmat - From ADK to Gemini Enterprise]]
- [[Arjun Prabhulal - Production-Grade RAG with ADK and Vertex AI RAG Engine]]
- [[Virinchi T - Google Cloud MCP Security Framework]]
- [[David Tessier - GCP Model Armor]]
- [[Google Cloud]]
- [[FD - Agent Muse Compute Demand]]
- [[Multi-Tenant Agent Architecture]]
- [[Tool Roster Economics]]
- [[Test-Time Scaling]]
- [[Meta]]
- [[DeepSeek]]
- [[ByteByteGo - AI Agents Can Think, Now They Can Pay]]
- [[Agent Payment Protocols]]
