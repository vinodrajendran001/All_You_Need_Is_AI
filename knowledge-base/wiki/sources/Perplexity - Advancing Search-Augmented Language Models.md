---
type: source-summary
source_id: src-2026-04-22-perplexity-search-augmented-lm
source_title: "Advancing Search-Augmented Language Models"
source_author: Perplexity Research
source_url: "https://research.perplexity.ai/articles/advancing-search-augmented-language-models"
created: 2026-05-13
updated: 2026-05-13
tags: [search, rl, sft, agents, tool-use, perplexity, grpo, reward-design]
status: active
---

# Perplexity - Advancing Search-Augmented Language Models

## Summary

A Perplexity Research article (published 2026-04-22) describing their post-training pipeline for building state-of-the-art web search agents on top of open-source models (Qwen3.5 family). The core insight is that **data curation and reward design must be co-designed** when training search agents, because optimising any single dimension (accuracy, efficiency, user preference) in isolation degrades the others.

## Key claims

1. **Two-stage pipeline (SFT → RL)** — Supervised Fine-Tuning first establishes deployment-critical behaviours (guardrails, instruction following, language consistency), then on-policy RL improves search accuracy and tool-use efficiency without regressing on SFT-stage behaviours.

2. **Why two stages?** — RL-only training improves search but underperforms on deployment guardrails; SFT-only improves compliance at the cost of search performance. Separating them lets each stage focus on its objective.

3. **GRPO for RL** — They use Group Relative Policy Optimization (GRPO) with token-level Importance Sampling to correct for training-inference mismatch, finding this sufficient to prevent training collapse.

4. **Synthetic verifiable QA** — Multi-hop QA data is constructed via sequential expansion: seed entity → multi-hop chain → name-free question synthesis → verification by independent web-enabled solvers. No curated knowledge graph needed.

5. **Rubric-based general chat** — Non-verifiable queries (rewriting, planning, open-ended assistance) are included in RL training by converting deployment requirements into atomic, objectively checkable rubrics. A pass@4 calibration filter keeps rubric difficulty informative.

6. **Gated reward aggregation** — Correctness is a necessary gate before preference credit is applied, preventing reward hacking where strong preference signals compensate for factual failures. The composite reward combines: baseline correctness + Bradley-Terry preference score + anchored efficiency penalty.

7. **Anchored efficiency penalties** — Tool-call and response-length penalties are group-relative (compared to successful solutions within the same GRPO group), avoiding the problem of unconditional penalties that suppress necessary exploration.

8. **90/10 prompt mixture** — 90% verifiable QA, 10% rubric-based data, to balance gradient variance across the harder QA signal and the easier rubric signal.

9. **Results** — `Qwen3.5-Large-SFT-RL` matches or exceeds GPT-5.4 on FRAMES and Facts Open benchmarks while using comparable tool budgets. At budget=4 on FRAMES: 73.9% accuracy at $0.02/query vs GPT-5.4's 67.8% at $0.085/query (+6 points at 4× lower cost).

10. **Open questions** — Training-inference KL divergence drift at extended training steps; scaling to multi-tool workflows with long-horizon trajectories; credit assignment for partial rollouts.

## Methods and techniques referenced

- [[Group Relative Policy Optimization]] (GRPO)
- Bradley-Terry preference framework
- Token-level Importance Sampling
- Sequential expansion for synthetic QA
- Rubric-based reward design
- Gated reward aggregation

## Affected pages

- [[Search-Augmented Language Models]] — new concept page
- [[Reward Design for RL]] — new concept page
- [[Perplexity]] — new entity page
- [[Reinforcement Learning]] — updated with search-agent RL connections
- [[Tool Use and Function Calling]] — cross-linked with efficiency-aware tool use
- [[Agentic Loop]] — cross-linked

## Raw capture

`knowledge-base/raw/sources/Advancing Search-Augmented Language Models.md`

## Related pages

- [[AI Knowledge Base Overview]]
- [[Search-Augmented Language Models]]
- [[Reward Design for RL]]
- [[Reinforcement Learning]]
- [[Tool Use and Function Calling]]
- [[Agentic Loop]]
- [[Perplexity]]
