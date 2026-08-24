---
type: concept
created: 2026-06-10
updated: 2026-08-24
tags:
  - concept
  - routing
  - inference
  - ai-agents
  - cost
source_ids:
  - src-2026-06-10-bytebytego-token-spend-routing
  - src-2026-06-24-bytebytego-llm-vs-slm
  - src-2026-07-02-alyona-vert-ai-concepts-2026
  - src-2026-07-03-sebastian-raschka-local-coding-agents
  - src-2026-08-19-bytebytego-inkling
  - src-2026-08-24-openai-gpt-5-6-builder-guide
status: active
---

# Model Routing

## Definition

Model routing is the practice of selecting which model, provider, or model tier should handle a given request, task, or step inside a larger workflow. In production agent systems, the goal is usually to satisfy a quality threshold while minimizing cost and latency by sending easy work to cheaper models and reserving frontier models for the hard parts.

## Why it matters

Long-running agents turn model choice into infrastructure. When a system repeatedly resends large contexts through many loop steps, "just use the best model" stops being economically viable. Routing becomes the control layer that decides whether ambitious agent workloads remain affordable at all.

## Current synthesis

- [[ByteByteGo - Token Spend Out of Control - The Case for Smarter Routing]] reframes routing as more than a cost hack. Agent loops repeatedly resend system instructions, history, tool schemas, tool results, and intermediate reasoning, so the bill grows with both **context size** and **number of calls**. Routing is the main remaining lever once those loops are structurally necessary.
- A durable router has two parts:
  - a **gateway** that presents one API while speaking to many model providers underneath
  - a **decision layer** that chooses the model
- There are two main decision strategies:
  - **Route on a known signal** — for example task type, agent mode, or operation class. This is cheap, explainable, and reliable when the signal is trustworthy.
  - **Predict difficulty from the request** — infer how hard the request is and choose the cheapest likely-good model. This is more flexible, but it adds another learned system that must be trained, evaluated, and kept current as models change.
- The strongest production pattern is therefore: **route on the strongest signal you already have**. Kilo's coding agent always knows whether it is planning, debugging, editing, or doing a background chore, so it can route by mode instead of trying to infer difficulty from raw request text.
- Routing usually appears as **tiers**, not as one-off hand tuning:
  - top tier for hard reasoning / planning / debugging
  - balanced tier for routine but still capable work
  - tiny or free tiers for background chores
- Routing and caching are complementary, not substitutes. Kilo reports that even with 80%+ cache reuse on many features, spend stayed high because request volume and uncached context were still large. Caching reduces repeated prefix cost; routing decides which model pays the remaining bill.
- Routing also introduces new failure modes:
  - wrong decisions hurt quality
  - the routing layer adds complexity and latency
  - switching between different model families mid-task can force the system to drop intermediate reasoning because one model's internal "thinking" is not readable by another
- There is a useful vault-level distinction between **inter-model routing** and **intra-model routing**:
  - this page focuses on **inter-model routing** across providers or model tiers
  - [[Mixture of Experts]] and parts of [[On-Device Reasoning]] involve **intra-model routing**, where a router inside one system decides which experts or reasoning paths to activate
- [[ByteByteGo - Large Language Models vs Small Language Models]] adds the small/large composition version of this pattern. [[Small Language Models]] are useful as the fast, cheap, local, or high-volume tier; large models remain necessary for harder reasoning, broader generalization, and richer world knowledge. Production systems therefore use SLMs as:
  - **primary handlers** for common/easy requests;
  - **guardrails** around larger models;
  - **routers** that estimate difficulty or intent;
  - **drafters** for speculative decoding.
- This reframes routing as a capability allocation problem, not only a provider-cost problem. The router must decide when a small model is enough, when to retrieve, when to escalate, and when to block or ask for human review.
- Two 2026 sources widen the cost surface routing optimises. [[Alyona Vert - AI Concepts and Techniques in 2026]] notes inference is **fragmenting by workload** across specialised hardware (rack-scale Vera Rubin, MatX, Taalas "model-as-hardware"), so routing increasingly spans not just model tiers but *hardware* tiers keyed on cost-per-token, latency, and context handling. [[Sebastian Raschka - Using Local Coding Agents]] adds a subtler lever: for agentic work, **token usage is driven by the harness, not the model** — Claude Code re-feeds far more input context per turn than Codex for equal task success — so choosing the [[Coding Agent Harness]] is itself a routing-style efficiency decision.
- [[OpenAI - The Builder's Guide to GPT-5.6]] adds a second routing axis: after selecting a model tier, choose **reasoning effort** based on task risk and complexity. The same guide recommends stronger orchestration with cheaper specialized workers and tool search rather than exposing a large tool schema on every turn.
- [[ByteByteGo - The New American AI Model Designed to Be Customized]] shows the analogous control inside one sparse model. Inkling activates a small subset of experts per layer and exposes an effort parameter, so deployment can route both computation inside the model and reasoning budget across requests.

## Open questions

- How accurate can learned difficulty routers become as model landscapes change month to month?
- At what point does per-step routing degrade quality too much by fragmenting long-horizon reasoning across model families?
- Can routing become fully budget-aware and self-tuning, the way load balancing became background infrastructure?
- What confidence or uncertainty signal is reliable enough to let a small model decide it should escalate?

## Related pages

- [[ByteByteGo - Token Spend Out of Control - The Case for Smarter Routing]]
- [[ByteByteGo - Large Language Models vs Small Language Models]]
- [[Small Language Models]]
- [[Context Engineering]]
- [[AI Agents in Production]]
- [[On-Device Reasoning]]
- [[Mixture of Experts]]
- [[Model Quantization and Efficiency]]
- [[Coding Agent Harness]]
- [[Alyona Vert - AI Concepts and Techniques in 2026]]
- [[Sebastian Raschka - Using Local Coding Agents]]
- [[Sarthak Rastogi - Making an AI Agent Production-Ready]]
- [[ByteByteGo]]
- [[AI Knowledge Base Overview]]
- [[OpenAI - The Builder's Guide to GPT-5.6]]
- [[ByteByteGo - The New American AI Model Designed to Be Customized]]
