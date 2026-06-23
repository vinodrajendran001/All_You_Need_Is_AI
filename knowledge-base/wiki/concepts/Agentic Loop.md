---
type: concept
created: 2026-05-13
updated: 2026-06-23
tags: [agents, llm, tool-use, loop]
source_ids:
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
  - src-2026-05-18-rag-architecture-comparison
  - src-2026-05-21-bytebytego-batch
  - src-2026-06-02-dwarkesh-eric-jang-alphago
  - src-2026-06-05-pguso-agents-from-scratch
  - src-2026-06-22-cameron-wolfe-agentic-rl-frameworks
  - src-2026-06-22-djfarrelly-agent-loop-architecture
  - src-2026-06-22-alphasignal-agent-skill-optimization
status: active
---

# Agentic Loop

The iterative cycle by which an LLM-powered application plans, acts, observes, and responds — potentially over multiple rounds of tool calls within a single user request. [[Search-Augmented Language Models]] are a concrete case where this loop becomes a trained search policy rather than a one-off interaction pattern.

## How it works

1. **User prompt** arrives with a list of available tool definitions.
2. The **model reasons** about whether it can answer directly or needs external information.
3. If it needs a tool, it generates a **structured function call** (JSON) instead of a final answer.
4. The **application layer** validates and executes the call, returning results as a new message.
5. The model **incorporates the result** and either produces a final response or issues another tool call.
6. Steps 3–5 repeat as needed.

This multi-step looping is the foundation of **AI agents** — systems where the model autonomously plans and executes complex tasks by chaining multiple tool calls in sequence.

[[Retrieval-Augmented Generation|Agentic RAG]] is a direct example: the loop becomes a multi-step retrieval policy in which the model plans a search, calls retrieval tools, inspects the evidence, and decides whether another retrieval step is needed before answering.

## Production form

Grab’s analytics-support assistant shows what the loop looks like in a real enterprise workflow. A classifier routes a Slack question to specialist agents for data inspection, code search, and on-call health checks; a summarizer then integrates the findings; and higher-risk enhancement requests move to a separate human-gated path. The core loop is still plan → act → observe, but in production it often spans **multiple specialist agents, tool boundaries, and approval steps** rather than a single model repeatedly calling one tool.

The Eric Jang interview adds a research-facing version of the same idea: an **autoresearch loop** where models help implement experiments, run them, and tune hyperparameters across iterations. The limit, for now, is not looping itself but research navigation — deciding which question to investigate next and knowing when a line of attack is a dead end.

## Durable loop architecture

[[djfarrelly - The Agent Loop Architecture]] adds the missing runtime layer: a loop is not just `while not done`. In production, a loop is a trigger or schedule plus a decision-maker plus durable execution steps. The source's three-layer model is:

1. **Loop** — cron or event trigger plus LLM decision-maker.
2. **Skill** — reusable durable workflow that can fetch data, call models, invoke tools, retry, and return a result.
3. **Orchestrator** — execution engine that checkpoints steps, manages retries, enforces concurrency, stores run history, and survives deploys or crashes.

This reframes the agentic loop from a control-flow pattern into an infrastructure problem. A basic process can restart, but it cannot know which LLM call already happened, whether a Slack message was already sent, or whether a child agent is still running. Durable orchestration prevents duplicate side effects and wasted token spend by resuming from the last successful step.

The Alpha Signal skill-optimization source extends this into **loop engineering**: design repeatable cycles with verifiable goals, memory, metrics, and exit conditions, then let the system optimize the skill artifacts inside that loop. See [[Agent Skill]].

## Agentic RL view

[[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]] treats the loop as the rollout generator for [[Agentic Reinforcement Learning]]. Each loop step can include generated text, a structured tool call, an observation from the environment, reward feedback, and updates to external state. This turns the loop into a multi-turn MDP rather than a pure application-control pattern.

The important training implication is that loop traces must preserve which tokens came from the agent, which observations came from tools, where step boundaries occurred, and when termination happened. Those details determine action masks, reward assignment, context construction, and whether the policy update actually matches what happened during rollout.

## Example

A user asks: *"Find me flights to Tokyo and check the weather there."*

1. Model calls `search_flights(destination="Tokyo")` → gets flight options.
2. Model calls `get_weather(location="Tokyo")` → gets current conditions.
3. Model synthesises both results into a single natural-language response.

## Why the separation matters

The model decides *what* should happen. The application layer decides *whether* it happens. This boundary allows:
- **Access control** — restrict which tools are available.
- **Validation** — check arguments before execution.
- **Human-in-the-loop** — require approval for high-stakes actions.

## Ground-up anatomy (from pguso - Agents From Scratch)

[[pguso - Agents From Scratch]] provides the most explicit ground-level treatment of the loop in this vault. Key additions to the above model:

- **An agent is not a clever prompt.** It is a loop with state. The prompt is the least important part; the loop and state machinery around it are what produce multi-step behaviour.
- **State is explicit.** An `AgentState` object (step count, done flag, current plan) is a plain Python object you can inspect at any time — not a hidden conversation history.
- **Termination is a first-class design decision.** The loop must have at least one termination condition: the model signals `"action": "done"`, a `max_steps` limit is hit, or a specific goal is achieved. Infinite loops are a bug, not a feature.
- **Structure beats clever prompting.** Reliability in the loop comes from forcing structured JSON outputs and retrying on validation failure, not from crafting more elaborate prompts.
- **Premature autonomy is dangerous.** Agency should be added incrementally: first the model responds; then it decides; then it requests actions; only finally does the system execute with less oversight.

The full agent-building progression this source teaches:
1. Structured output (reliable JSON with validation + retries) — the reliability foundation
2. Decisions (finite choice spaces) — how the model routes rather than generates
3. Tool request/execute separation — where safety lives
4. State + loop — what makes the system an agent rather than a chatbot
5. Memory → planning → atomic actions → dependency graphs — the intelligence stack
6. Evals + telemetry — the observability stack without which production operation is guesswork

See [[Agent Planning]] for the planning/execution branch and [[Agent Memory]] for the memory branch.

## Related pages

- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[AI Agents in Production]]
- [[Agent Planning]]
- [[Agent Memory]]
- [[Agent Skill]]
- [[Search-Augmented Language Models]]
- [[Retrieval-Augmented Generation]]
- [[Reward Design for RL]]
- [[Agentic Reinforcement Learning]]
- [[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]]
- [[pguso - Agents From Scratch]]
- [[djfarrelly - The Agent Loop Architecture]]
- [[Alpha Signal - How your agents can write and optimize their own skills]]
- [[ByteByteGo - Connecting LLMs to the Real World]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[ByteByteGo]]
- [[Automated AI Research]]
- [[Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]]
