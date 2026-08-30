---
type: concept
created: 2026-06-05
updated: 2026-08-30
tags:
  - concept
  - context-engineering
  - prompt-engineering
  - ai-agents
  - production-ai
source_ids:
  - src-2026-06-05-systemdesign42-system-design-academy
  - src-2026-06-10-bytebytego-token-spend-routing
  - src-2026-06-22-cameron-wolfe-agentic-rl-frameworks
  - src-2026-06-22-alphasignal-agent-skill-optimization
  - src-2026-08-05-aibuilderclub-context-engineering-guide
  - src-2026-08-05-aibuilderclub-rag-vs-long-context-vs-fine-tuning
  - src-2026-08-05-aibuilderclub-prompt-context-harness-evolution
  - src-2026-08-07-avi-chawla-claude-code-cost
  - src-2026-08-26-alex-zhang-speculative-programmatic-tool-calling
  - src-2026-08-25-bytebytego-stealing-reasoning-traces
  - src-2026-07-16-lilian-weng-harness-engineering
  - src-2026-08-30-addy-osmani-audit-agent-files
status: active
---

# Context Engineering

## Definition

Context engineering is the discipline of managing what goes into an LLM's context window at inference time. It is distinct from prompt engineering: prompt engineering is about crafting individual instruction phrasings to elicit desired output styles; context engineering is about the information architecture of the complete input — deciding *what* to include, *how much*, in *what order*, and what to leave out.

## Why it matters

LLM performance at inference time is determined by the content of the context window far more than by per-call prompt crafting. The context window contains system prompts, conversation history, retrieved documents, tool results, memory promotions, and any compressed summaries of prior state. Managing that window poorly — overloading it, leaving irrelevant content, failing to retrieve the right documents — is a primary source of production failures in deployed AI systems. As context windows grow longer (100K–1M tokens), the problem does not go away: longer windows increase cost, introduce lost-in-the-middle failures, and make token budget management more consequential.

## Current synthesis

### Context engineering vs. prompt engineering

| | Prompt engineering | Context engineering |
|-|-------------------|-------------------|
| **Focus** | How you phrase one instruction | What information populates the whole input |
| **Scope** | Single turn, one message | Full context window across turns |
| **Key skill** | Wording, instruction format | Information selection, compression, budget allocation |
| **Failure mode** | Wrong output format or style | Missing context, overloaded context, wrong retrieval |
| **When it matters most** | Few-shot examples, chain-of-thought elicitation | Long conversations, agentic systems, RAG pipelines |

Prompt engineering is a subset of context engineering — once you have the right context architecture, prompt phrasing matters less than what information is present.

### Skill files as optimizable context artifacts

[[Alpha Signal - How your agents can write and optimize their own skills]] adds a concrete artifact type to this page: the [[Agent Skill|skill file]]. A skill file is a standalone markdown operating procedure that enters the agent's context and tells it how to perform a task family, use tools, format outputs, and recover from failures.

The source's important shift is from one-off prompt tweaking to **text-space optimization**. SkillOpt, GEPA, and EvoSkill treat these text artifacts as external state that can be improved through rollouts, verifiers, reflection over trajectories, bounded edits, held-out validation, and rejected-edit buffers. This is context engineering becoming an optimization loop rather than a manual writing exercise.

The caveat is that this only works when the task has a verifiable feedback signal. For subjective or poorly specified work, automated skill-file optimization can overfit to weak evals or introduce hidden regressions.

### Context rules during agentic RL

[[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]] adds a training-time version of context engineering. In [[Agentic Reinforcement Learning]], the full rollout may contain many steps of generated text, tool calls, observations, rewards, and environment state. But the model-visible context at the next step does not have to be a naive append-only transcript.

Agent-R1-style frameworks store the full step-level trajectory, then apply an environment-specific context rule that can preserve, summarize, remove, or transform past steps before the next action. This matters because append-only context can create **context rot**: verbose tool outputs or irrelevant reasoning history crowd out useful state. The source reports that sliding-window context can outperform append-only and summarization strategies in some environments, reinforcing that "more context" is not always better.

### What context engineering manages

1. **System prompt** — role definition, capability boundaries, output format rules, tool schemas. Should be stable, concise, and written to survive position bias (models attend less to middle-of-context content).
2. **Conversation history** — which prior turns to include. Naive approaches include all history; engineering approaches apply sliding windows, summarization of older turns, or importance-weighted retention.
3. **Retrieved content (RAG)** — what documents to include and how many. The quality of retrieval is a context engineering problem, not just a retrieval problem: wrong documents in the window cost tokens and actively mislead the model.
4. **Tool and function call results** — output from tool executions can be large. Truncating, summarizing, or filtering tool results before including them in the context is context engineering.
5. **Memory promotions** — facts promoted from long-term storage ([[Agent Memory]]) into the active context must be selected for relevance to the current query, not included wholesale.
6. **Token budget allocation** — on constrained systems ([[On-Device Reasoning]]), token budgets must be explicitly partitioned across system prompt, history, retrieval, and output reservation.

### Context window as information architecture

The clearest framing: the context window is a **fixed-size database** that the model reads entirely at each inference step. Context engineering is database engineering for that fixed-size store: schema design (system prompt structure), query selection (what to retrieve), cache management (history truncation), and cost optimization (fewer tokens = lower latency and cost).

### Relationship to agent memory

[[Agent Memory]] distinguishes short-term context (the window) from long-term persistent storage. Context engineering operates at the boundary: deciding what to promote from long-term storage into the short-term window, how to represent it compactly, and when to evict. This makes context engineering the operational layer of memory management for agents.

### Relationship to on-device reasoning

[[On-Device Reasoning]] operates under hard token budget constraints on mobile-class hardware. Every byte of context competes with reasoning trace length and output. The Qualcomm paper's budget-forcing mechanism is a form of context engineering applied to the *reasoning* portion of the context specifically.

### Routing is the economic complement to context engineering

[[ByteByteGo - Token Spend Out of Control - The Case for Smarter Routing]] adds an important systems correction: even when you compress history, trim tool results, and retrieve more selectively, long-loop agents still have to resend large contexts many times. Context engineering controls **how many tokens** get sent; [[Model Routing]] controls **which model pays for them**.

The practical synthesis is:

1. **Reduce the context where you can** — summarize, filter, stage retrieval, reserve generation headroom.
2. **Measure token spend by feature/task** — context cost is often dominated by a few heavy workflows rather than by the highest request count.
3. **Route on the strongest trustworthy signal you already have** — if the system already knows the task mode (planning vs editing vs background chore), do not infer difficulty from scratch.

Kilo's production numbers are useful here because they show the limit of "just cache more." Even with high cache reuse, spend stayed high because request volume and uncached context were still large. That makes routing and context engineering complementary infrastructure layers rather than competing techniques.

### Production failure modes that context engineering addresses

- **Lost-in-the-middle**: models attend poorly to content in the middle of long contexts. Solution: place critical information at start or end.
- **Context overload**: too many retrieved documents degrade generation quality even if each individually is relevant. Solution: rank and select rather than include all.
- **History drift**: long conversations accumulate stale context that conflicts with current state. Solution: progressive summarization of older turns.
- **Tool result bloat**: tool calls return verbose JSON that fills the window with low-density information. Solution: structured summarization of tool outputs before reinsertion.
- **Token exhaustion**: the context fills before the model can generate a response. Solution: explicit token budget partitioning with headroom reserved for generation.

### AI Builder Club's four operating strategies

[[AI Builder Club - Context Engineering - The Complete Guide (2026)]] consolidates the operational playbook into four strategies: **offload** detailed artifacts to external storage, **retrieve** them just in time, **isolate** specialist work in separate contexts, and **compress** history while preserving future constraints. It also names poisoning, distraction, confusion, and clash as context failure modes.

The collection adds a cache-level implication: stable prefixes and append-only histories can preserve prefix reuse, while dynamic material placed early invalidates it. Context design therefore affects quality, latency, and cost together.

### Cost attribution confirms the replay tax

[[Avi Chawla - 86 Percent of Your Claude Code Bill Has Nothing to Do With Your Prompts]] reports a vendor-associated team analysis in which visible user prompts accounted for only 14% of input tokens. The larger categories were system and skill instructions, MCP schemas, tool results, and prior assistant context. The exact percentages need independent replication, but the mechanism is durable: caching discounts repeated prefixes without removing their volume, and every retained tool result raises the cost of later turns.

## Two additions: code as context economy, and traces as leaked context

[[Programmatic Tool Calling]] ([[Alex L. Zhang - Speculative Programmatic Tool Calling]]) offers a structural answer to a problem this page usually attacks with summarization and retrieval. When the agent's action is a program, a large intermediate result can be processed *in the interpreter* and only its conclusion returned. Under a JSON tool-call contract that result must pass through the context window to be acted on at all. Filtering, aggregation, and fan-out become interpreter work rather than context work.

From the opposite direction, [[ByteByteGo - How to Steal an AI Model's Private Thoughts]] shows that context management has a disclosure surface. Encrypted reasoning blocks are context the client carries but cannot read — and because they cannot be read, they cannot be sanitised. A scan of 6,708 published agent trajectories recovered API keys, passwords, and private keys from blocks whose visible text had been scrubbed clean. See [[Reasoning Trace Privacy]]. The operational rule is that opaque context artifacts must be **removed** rather than cleaned, and that compaction, forking, and history editing all rest on the same portability that makes the leak possible.

## Context collapse, and why playbooks must be itemized

[[Lilian Weng - Harness Engineering for Self-Improvement]] names a failure mode that any
self-maintaining context file eventually hits. **Context collapse** occurs when a whole context
document is regenerated each round by a model with a brevity bias: accumulated detail erodes round
after round until the playbook is shorter and worse than where it started. The problem is not the
model's judgement about any single item — it is that wholesale rewriting gives every item a fresh
chance to be dropped.

ACE (Agentic Context Engineering) is the structural fix. It splits the work across a **generator**, a
**reflector**, and a **curator**, and stores the evolving playbook as **itemized bullets** added,
edited, or retired one at a time. Updates become local, attributable, and reversible. MCE extends this
to a bi-level loop — meta skill evolution above base context optimization — and Meta-Harness goes a
rung higher by optimizing the optimizer's own code. See [[Harness Optimization]] for the full ladder.

## The null result this page has to answer

[[Addy Osmani - Audit your Agent files]] supplies the sceptical case, with numbers larger than most of
the positive evidence in this area:

- **288 runs across 17 tasks**: the presence of `AGENTS.md` / `CLAUDE.md` made **no clear difference to
  correctness**. It did change behaviour — agents wrote more targeted tests — but the outcome measure
  did not move.
- Anthropic removed **more than 80%** of Claude Code's system prompt with **no measurable eval loss**.
- Across 100 repositories: **lint leakage 62%, context bloat 42%, skill leakage 35%**.
- **Personalized skills performed roughly on par with borrowed ones**, and a generic skill built from
  many developers' practice was **more useful** than a personalized one. (Caveat, flagged by Osmani
  himself: the study used an LLM-based developer simulator.)
- Agents answering behavioural questions from **prose summaries** scored **4/45**; from **source code**,
  **27/45**.

The last finding constrains how context should be written for agents: a summary of behaviour is a poor
substitute for a pointer to the code that implements it. The others invert the default — context
**must justify itself against an eval, and the default action for an unjustified rule is deletion**.
Osmani's mechanics are worth keeping straight: `/doctor` (in-session) audits active configuration
while `claude doctor` (CLI) only runs install diagnostics; `/memory` is a separate review pass; and
skill *listings* are budgeted at roughly **1% of the context window**, with only the invoked skill's
body loading — so a long skill body is cheap until called, but a proliferation of skill names is not
free.

## Open questions

- What is the right abstraction layer for context engineering in multi-agent systems where multiple agents share or read each other's contexts?
- How do very long context windows (1M+ tokens) change the engineering priorities vs. practical retrieval-based approaches?
- Can context engineering be learned and automated (the model manages its own context), or does it require explicit engineering?

## Related pages

- [[Agent Memory]]
- [[Agent Skill]]
- [[Agentic Reinforcement Learning]]
- [[Retrieval-Augmented Generation]]
- [[On-Device Reasoning]]
- [[Model Routing]]
- [[Agentic Loop]]
- [[AI Agents in Production]]
- [[Direct Corpus Interaction]]
- [[Model Context Protocol]]
- [[LLM Training Pipeline]]
- [[ByteByteGo - Token Spend Out of Control - The Case for Smarter Routing]]
- [[Alpha Signal - How your agents can write and optimize their own skills]]
- [[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]]
- [[systemdesign42 - System Design Academy]]
- [[Coding Agent Harness]]
- [[Real-Time Voice AI]]
- [[Sarthak Rastogi - Making an AI Agent Production-Ready]]
- [[AI Knowledge Base Overview]]
- [[AI Builder Club - Build AI Agents]]
- [[Loop Engineering]]
- [[Avi Chawla - 86 Percent of Your Claude Code Bill Has Nothing to Do With Your Prompts]]
- [[Graph Engineering]]
- [[Agent Security and Governance]]
- [[Programmatic Tool Calling]]
- [[Reasoning Trace Privacy]]
- [[ByteByteGo - How to Steal an AI Model's Private Thoughts]]
- [[Alex L. Zhang - Speculative Programmatic Tool Calling]]
- [[Speculative Tool Execution]]
- [[Harness Optimization]]
- [[Lilian Weng]]
- [[Addy Osmani]]
- [[Lilian Weng - Harness Engineering for Self-Improvement]]
- [[Addy Osmani - Audit your Agent files]]
