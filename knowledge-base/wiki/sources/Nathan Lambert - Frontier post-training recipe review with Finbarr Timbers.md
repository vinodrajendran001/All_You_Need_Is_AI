---
type: source-summary
created: 2026-06-17
updated: 2026-06-17
source_id: src-2026-06-17-nathan-lambert-frontier-post-training-recipe-review
source_title: Frontier post-training recipe review with Finbarr Timbers
source_author: Nathan Lambert with Finbarr Timbers
source_url: https://www.interconnects.ai/p/frontier-post-training-recipe-review
tags:
  - source-summary
  - post-training
  - rl
  - distillation
  - frontier-models
source_ids:
  - src-2026-06-17-nathan-lambert-frontier-post-training-recipe-review
status: active
---

# Nathan Lambert - Frontier post-training recipe review with Finbarr Timbers

## Summary

An Interconnects interview / technical-summary post by [[Nathan Lambert]] with [[Finbarr Timbers]] reviewing how frontier post-training recipes evolved from InstructGPT-style RLHF into 2026 multi-specialist recipes. The source is valuable because it provides a compact historical map of post-training recipes and identifies **Multi-teacher On-Policy Distillation (MOPD)** as the emerging 2026 frontier pattern.

## Recipe timeline

- **2022-2023: InstructGPT / early RLHF** — SFT on human demonstrations, reward model on human comparisons, PPO against the reward model.
- **2023: Llama 2** — iterative RLHF with rejection sampling and PPO, plus separate helpfulness and safety reward models.
- **2024: Llama 3** — more complex multi-round post-training, but still offline-heavy: reward model, sample K responses, rejection sampling, SFT, then DPO across multiple rounds.
- **2024: Tulu 3** — curated prompts, SFT, DPO, then RLVR. This formalizes the SFT -> DPO -> RLVR pattern in open recipes.
- **2025: DeepSeek R1** — RL becomes the centerpiece. R1-Zero uses pure GRPO-style RL on the base model to seed reasoning behavior, then cold-start SFT, reasoning RL, rejection-sampling SFT, final RL, and dense distillation.
- **2026: MiMo Flash V2 / DeepSeek V4 / Nemotron 3 Ultra** — recipes fragment into many domain-specialist teachers that are merged into a general student through MOPD or related distillation stages.

## Key claims

- The shape of post-training changed more in the last year than in the prior three.
- 2026 frontier recipes are no longer one monolithic SFT -> preference -> RL run. They increasingly train **many domain-specialist teachers** and consolidate them into one general model.
- **MOPD pattern:** train domain-specialist teachers, have the final student sample its own trajectories, route each rollout to the relevant teacher, and minimize reverse KL to that teacher's token distribution.
- MOPD emerged because large mixed-domain RL is expensive and conflict-prone: math, code, safety, and agentic tool-use objectives can trade off against each other inside one run.
- Specialist teachers are organizationally scalable: separate teams can train math, code, search-agent, safety, and other teachers in parallel.
- DPO appears to be less central in the leading 2026 recipes, not necessarily because it is useless, but because more industrialized on-policy RL / distillation pipelines can smooth rough edges earlier. DPO still looks useful for bootstrapping smaller or more open recipes.
- The field is now constrained by both technical and organizational complexity. The source repeatedly notes that modern post-training is partly about "wrangling an org chart."

## MOPD caveats

- Teacher/student distribution mismatch is a real failure mode. Nemotron 3 Ultra reports that teachers trained with substantially different pipelines cannot be naively merged through straightforward on-policy distillation.
- Cross-teacher alignment becomes a new research and organizational problem: if each teacher learns different reasoning behaviors or output distributions, the student-generated trajectories can be out-of-distribution for the teachers.
- It is still unclear how much on-policy distillation beats trace-distillation SFT in final performance; the source treats this as an open empirical question.
- Some 2026 models do not use MOPD (or do not report it): MAI-Thinking-1 uses specialist RL climbs plus trace-distillation SFT and a final RL climb; Kimi K2.5 and GLM-5 use staged RL / agentic / multimodal recipes without the same explicit MOPD framing.

## Why it matters

This source materially updates the vault's [[LLM Training Pipeline]] page: the post-training pipeline is no longer well summarized as SFT -> RLHF/PPO or SFT -> DPO. Frontier post-training is becoming an industrial multi-stage process combining specialist RL, distillation, on-policy sampling, verifiable rewards, and teacher consolidation.

## Affected pages

- [[Multi-Teacher On-Policy Distillation]]
- [[LLM Training Pipeline]]
- [[Direct Preference Optimization]]
- [[Reward Design for RL]]
- [[Automated AI Research]]
- [[Nathan Lambert]]
- [[Finbarr Timbers]]
- [[AI Knowledge Base Overview]]

## Raw capture

- `knowledge-base/raw/sources/Frontier post-training recipe review with Finbarr Timbers.md`

## Related pages

- [[Multi-Teacher On-Policy Distillation]]
- [[LLM Training Pipeline]]
- [[Direct Preference Optimization]]
- [[Reward Design for RL]]
- [[Automated AI Research]]
- [[Nathan Lambert]]
- [[Finbarr Timbers]]
- [[AI Knowledge Base Overview]]
