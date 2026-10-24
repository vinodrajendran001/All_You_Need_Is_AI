---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-21-databricks-memcurrent
source_title: "MemCurrent: Designing Persistent Memory for Production Agents"
source_author: The Databricks AI Research Team
source_url: https://www.databricks.com/blog/memcurrent-designing-persistent-memory-production-agents
tags:
  - source/summary
  - agent-memory
  - evaluation
  - databricks
source_ids:
  - src-2026-10-21-databricks-memcurrent
status: active
---

# Databricks AI Research - MemCurrent Persistent Memory for Production Agents

## Summary

Databricks' design note for **MemCurrent**, a persistent-memory system for production agents built
around a split between **episodic memory** (append-only raw session traces) and **derived memory**
(mutable, distilled knowledge files), accessed through plugins, tools, and an offline consolidation
pipeline the authors call **"dreaming."**

The opening claim — **"More history is not necessarily better memory"** — is the point, and the
ablations support it: derived memory carries most of the benefit, and episodic memory adds a small
complementary gain.

## Key claims

### Architecture

- **Three access patterns:** a **plugin** that logs or injects memory automatically at fixed session
  points; **tools** (`search_memory`, `fetch_memory`, `add_memory`, `update_memory`, `delete_memory`)
  the agent invokes explicitly; and an **offline "dreaming" pipeline** that consolidates asynchronously.
- **Two memory types:** episodic memory is append-only raw traces; derived memory is mutable structured
  knowledge files holding distilled corrections, preferences, definitions, and workflows.
- An automatically generated **`memory.md` index** describes the available files and their contents, and
  a session-start plugin injects that index.
- Both types live in a production database; derived memory is a **mutable table simulating a
  hierarchical filesystem**.
- The dreaming pipeline extracts implicit learning from new sessions, writes to relevant files,
  **splits oversized files, merges duplicates, and resolves conflicts**.
- Design stance: **"Memory feeds actions, not answers."**

### Evaluation setup

- Open benchmarks: **LoCoMo** (19-32 sessions/sample), **LongMemEval** (38-62 sessions/sample), and a
  **ConvoMem** subset of **500 samples** at **100 sessions/sample**. Comparators were Mem0, PropMem,
  OpenClaw memory, a no-memory floor, and a full-context ceiling, averaged over **LangGraph and OpenAI
  Agents SDK** harnesses and **three repeats**. Agent and memory model: GPT 5.6 luna.
- **Internal Memory Benchmark:** mined from **12K+** Genie sessions down to **3K** candidates, yielding
  **114 test cases**, **29 users**, and **2,233 history sessions**, covering **5 memory types** and
  **11 scenarios**. An adversarial judge checked seven criteria, followed by manual review. Agent model
  Claude Opus 4.6, memory model GPT 5.6 sol, three repeats.

### Reported results — all first-party

- Open benchmarks: MemCurrent **88.1%** versus **87.8%** for full context, at **8.4K versus 103K input
  tokens per question** — roughly **12x fewer** tokens for comparable accuracy.
- Internal benchmark: MemCurrent **68.4%** pass rate at **252s** latency and **418K** tokens per task.
  No-memory floor **22.3%**; gold-memory injection ceiling **78.6%**; Mem0 **43.9%** at higher latency
  and cost.
- Against no memory, MemCurrent **tripled** pass rate (**22.3% → 68.4%**), ran **1.35x faster**, and was
  **1.44x cheaper**, closing **"over 80% of the gap"** to gold injection. The headline **31% fewer
  tokens / 26% faster** figures are relative to the **no-memory baseline** on this benchmark.
- **Memory-type ablation:** episodic alone **35.8%**, derived alone **66.1%**, both **68.4%** — from a
  **22.3%** floor. **"Derived memory does most of the work."**
- **Access-pattern ablation:** offline dreaming alone **63.5%**, online tools alone **53.9%**, combined
  **66.1%**.
- Open-benchmark latency was **4-7 seconds/question** across memory backends.
- **[Illustrative]** One anonymized workflow fell from **11 tool calls, 8 subagents, and nearly six
  minutes** to **2 tool calls, 1 subagent, and 41 seconds** after a workflow was remembered.
- **[Product claim]** Agent Bricks' CLI is advertised as producing an end-to-end sample agent in
  **under 10 minutes**.

## Why it matters

[[Agent Memory]] in this vault has mostly argued *that* agents need persistence. This source is the
first to **measure which kind of persistence pays**, and the answer is lopsided: distilled derived
memory took the internal benchmark from 22.3% to 66.1%, while raw episodic traces alone reached only
35.8% and added just **2.3 points** on top of derived memory.

That reframes memory as a **distillation and consolidation problem** rather than a retrieval problem.
The offline-versus-online ablation points the same way — background consolidation (63.5%) outperformed
agent-invoked memory tools (53.9%), which means the agent deciding what to remember in-session is the
weaker mechanism.

The open-benchmark result is a useful efficiency anchor for [[Context Engineering]]: matching
full-context accuracy at **~12x fewer input tokens** supports the vault's recurring claim that dumping
history into context is expensive rather than thorough.

## Tensions / open questions

- Everything is **first-party**. The internal benchmark is company-created, company-operated, and
  partly **LLM-judged**, with manual review applied only to case construction.
- The internal benchmark is **small — 114 test cases** — and built from Databricks Genie sessions, so
  results may not generalize beyond that workload.
- Results do not isolate memory retrieval from model choice, prompting, harness, or Genie-specific
  infrastructure. The ablations cover memory type and access pattern, **not** indexing, retrieval,
  consolidation, conflict resolution, or memory-file structure.
- "Triples pass rate" is relative to the **no-memory baseline on the internal benchmark**, not a general
  improvement claim. Matching full-context accuracy at lower token use does not show memory is *more*
  accurate than full context everywhere.
- The authors' own caveats: open benchmarks use **synthetic conversations** and may not represent
  enterprise work; offline updates arrive with **delay**; plugins add runtime cost, latency, and
  inflexibility; tool quality depends on agent capability; **distillation can drop details**; episodic
  memory is searched in only about **one-third** of internal test cases; and internal histories were too
  long for full context, forcing gold injection as the ceiling.
- Open-benchmark tool results were **omitted as "strictly dominated"** by plugin-based memory, so the
  tool pathway is evaluated mainly on the internal benchmark.
- Shared memory across agents and models is stated as a **future direction**; no cross-model portability
  experiment is reported.

## Affected pages

- [[Agent Memory]]
- [[Context Engineering]]
- [[Continual Learning for Agents]]
- [[All_You_Need_Is_AI/knowledge-base/wiki/entities/Databricks]]

## Raw capture

- [[MemCurrent Designing Persistent Memory for Production Agents]]

## Citations

- Raw capture: [[MemCurrent Designing Persistent Memory for Production Agents]]
- Canonical URL: <https://www.databricks.com/blog/memcurrent-designing-persistent-memory-production-agents>
- Published 2026-10-21; captured 2026-10-22.
- Full author list in the article: Veronica Lyu, Wenhao Zhan, Sam Havens, Ziyi Yang, Jenny Sun, Qinxin
  Wang, Nihit Desai, Sirui Sun, Ankit Mathur, Jane Zhang, Yi Liu, Jialu Liu, Michael Bendersky, Matei
  Zaharia, Xing Chen.
- Benchmarks referenced but not read during this ingest: LoCoMo, LongMemEval, ConvoMem, Mem0, PropMem.

## Related pages

- [[Institutional Knowledge Agents]]
- [[Agent Observability]]
- [[Retrieval-Augmented Generation]]
- [[Multi-Turn Evaluation]]
- [[AI Agents in Production]]
- [[LLM-as-a-Judge]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Genie Explained]]
