---
type: concept
created: 2026-05-21
updated: 2026-06-23
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

## The main lesson

The common pattern is not “let the model do everything.” It is **design an environment where the model can do a few high-value things reliably**. That means specialized agents, narrow tools, token-aware context management, human review, and interfaces that encode domain structure instead of dumping raw data.

## Related pages

- [[Context Engineering]]
- [[Model Routing]]
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
- [[ByteByteGo]]
- [[AI Knowledge Base Overview]]
