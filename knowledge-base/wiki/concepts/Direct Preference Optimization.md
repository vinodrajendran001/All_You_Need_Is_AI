---
type: concept
created: 2026-06-05
updated: 2026-06-05
tags:
  - concept
  - alignment
  - post-training
  - dpo
  - preference-optimization
source_ids:
  - src-2026-05-18-pocketflow-tutorial-docs
  - src-2026-06-05-dharma-ai-dpo-beyond-chatbots
status: active
---

# Direct Preference Optimization

## Definition

Direct Preference Optimization (DPO) is a post-training method that adjusts a language model's behaviour using preference pairs (a chosen and a rejected output for the same input) without training a separate reward model or running an RL optimization loop. It directly optimizes the policy by raising the relative likelihood of chosen outputs and lowering the relative likelihood of rejected ones, anchored to a reference model to prevent the policy from drifting too far.

## Why it matters

DPO is one of two main routes (alongside RLHF + PPO) for making a model prefer good outputs over bad ones after SFT. It is simpler to implement than full RLHF — no separate reward model training, no PPO rollout infrastructure — and has been shown to achieve competitive results on alignment benchmarks. The vault's DPO coverage now extends into a second non-chat domain (structured OCR), which reveals the method's generality.

## Current synthesis

### The canonical chat-alignment framing

In the `LLM Training Pipeline` standard recipe, DPO comes after SFT:
1. **SFT** teaches the model to follow instructions and produce task-appropriate responses.
2. **DPO** then uses human preference rankings (chosen vs rejected responses to the same prompt) to nudge the distribution toward preferred outputs.

The key insight is that DPO re-parameterizes the RL objective so the optimal policy can be expressed in closed form in terms of the preference data — no explicit reward model required. The training signal is pairwise: the model learns "output A is better than output B for this input" rather than "output A scores X on the reward scale."

### What DPO actually fixes vs what SFT fixes

[[Dharma-AI - Direct Preference Optimization Beyond Chatbots]] adds a mechanistic distinction that the standard framing glosses over:

| Stage | What it fixes | What it does NOT fix |
|-------|--------------|---------------------|
| **SFT** | Closes the distance between a generalist model and the task domain | Does not penalize specific failure modes — its token-level loss has no completion-level term |
| **DPO** | Moves the distribution away from identifiable failure geometries (attractor regions) | Does not increase capability toward the task domain |

Critically, SFT and DPO are **not interchangeable operations at different intensities** — they address orthogonal dimensions of model behaviour. Applying DPO after SFT improves reliability in ways SFT alone cannot achieve regardless of training volume.

### DPO beyond chat: self-rejection pairs for structured outputs

The DharmaOCR case shows a generalisation of DPO that does not require human annotators at all:

1. Run the SFT model at inference on training inputs.
2. Score candidate outputs with an automated LLM judge.
3. **Treat the model's own failure outputs as the rejected examples** — not filter them as noise. Degenerate completions (e.g., repetition loops in OCR) are the most direct signal of where the distribution should not go.
4. Pair them with the judge's top-scored correct outputs as chosen examples.
5. Run DPO on these self-generated preference pairs.

Result across five OCR model families: **59.4% average reduction in text degeneration** (best case 87.6%), with no loss in extraction quality.

### Three conditions for self-rejection DPO

The approach requires:
1. **Categorically distinct failure mode** — the failure must be behaviorally recognizable as a class (not just "lower quality"). Repetition loops are categorical; a response that misses a word is not.
2. **Automated scoring without human annotation** — an LLM judge or rule-based mechanism must reliably separate chosen from rejected at the completion level.
3. **Sufficient inference volume** — enough samples to build a preference dataset with meaningful quality variance.

### Why completion-level training matters

Text degeneration is a self-reinforcing attractor: once a token dominates its own conditional distribution, every sampling step deepens the loop. SFT's token-level loss cannot target this — it penalizes each token in isolation and has no concept of a "degenerate completion." DPO's completion-level signal can explicitly point the distribution away from these attractors.

## Open questions

- Does the self-rejection approach generalise beyond OCR to other structured generation tasks (code, SQL, JSON schema compliance)?
- How should the LLM judge be calibrated to produce preference pairs with consistent quality gaps (avoiding noisy pairs that degrade training)?
- At what point does DPO shift from fixing failure modes to degrading general capability?

## Related pages

- [[LLM Training Pipeline]]
- [[Reward Design for RL]]
- [[Group Relative Policy Optimization]]
- [[Reinforcement Learning]]
- [[Dharma-AI - Direct Preference Optimization Beyond Chatbots]]
- [[The Pocket - PocketFlow Tutorial Docs]]
- [[AI Knowledge Base Overview]]
