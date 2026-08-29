---
type: linkedin-post
created: 2026-08-29
updated: 2026-08-29
tags:
  - post
pages_used:
  - "[[Reward Design for RL]]"
  - "[[IBM Granite Team - Granite 4.2 LLMs How They're Built]]"
  - "[[Group Relative Policy Optimization]]"
  - "[[Staged Reinforcement Learning Curriculum]]"
topics:
  - reward design
  - kl divergence
  - verifiable vs preference rewards
  - post-training recipes
covers_from: 2026-08-26
covers_through: 2026-08-29
status: ready
---

# 2026-08-29 KL Should Follow the Reward

## Post

Most teams tune the KL penalty in RLHF by feel. IBM's Granite 4.2 build report suggests it shouldn't be tuned at all. It should be looked up.

They published the hyperparameters for every reinforcement learning stage of the model. And the KL coefficient — the knob controlling how far the model is allowed to drift from where it started — doesn't track stage difficulty or model size. It tracks one thing: whether the reward can be verified.

Math with a checkable answer. Code that has to pass hidden tests. KL = 0. No leash at all. Passing the test is sufficient proof the model behaved.

Preference tuning and safety? KL = 0.05, the highest value in the pipeline.

The reasoning is sharp. When you can't verify the outcome, you can't tell real improvement from reward hacking. So you stop trusting the destination and start constraining the distance travelled.

A leash isn't a safety feature. It's an admission that you can't check where the dog went.

It isn't perfectly binary — the agentic stages sit at 0.01 — and this is a first-party report with self-reported numbers and no ablations, so nothing proves the schedule is load-bearing. But it's the rare hyperparameter with an actual reason behind it.

Where else are we tuning by feel, because we can't measure the outcome?

(Source: "Granite 4.2 LLMs: How They're Built", IBM Granite Team — https://huggingface.co/blog/ibm-granite/granite-4-2)

#ReinforcementLearning #LLMTraining #RewardDesign #GRPO #OpenModels

## Hook variants

1. **The number.** "IBM published the KL coefficient for every training stage of Granite 4.2. The interesting part isn't the value — it's that it drops to zero, and you can predict exactly when."
2. **The analogy.** "A leash isn't a safety feature. It's an admission that you can't check where the dog went. That's also, it turns out, how you should set your KL penalty."
3. **The myth-correction.** "Most teams tune the KL penalty in RLHF by feel. IBM's Granite 4.2 build report suggests it shouldn't be tuned at all — it should be looked up."

**Recommended:** 3. It names a habit the reader recognizes in themselves and immediately contradicts it, which earns the click-through on a truncated feed. Variant 2 is stronger writing but spends the analogy before the reader knows what it's for, and the post needs that line at the end. Variant 1 is the most honest framing but assumes the reader already cares about KL coefficients.

## Why this topic

Window: 2026-08-26 → 2026-08-29. Four ingests, two lint passes.

| Candidate | Surprise | Concrete | Reach | Fresh | Total |
|---|---|---|---|---|---|
| **KL follows the reward type** (Granite 4.2) | 5 | 5 | 4 | 5 | **19** |
| "3X faster" speculative decoding, real range 1.21×–2× | 4 | 5 | 4 | 5 | 18 |
| Reasoning traces as an unsanitisable secrets surface (328 of 6,708 trajectories leaking) | 4 | 5 | 3 | 5 | 17 |
| Speculative tool execution gates on purity but not authority | 4 | 3 | 2 | 5 | 14 |
| Five attributes of a reportable benchmark number (Wafer) | 2 | 4 | 3 | 5 | 14 |

Chose the KL rule because it is a *derived* insight rather than a reported fact: the source publishes a table, and
the vault is what noticed the table has a rule in it. It also carries a working analogy, a memorable pair of
numbers, and a takeaway that transfers to readers who will never run GRPO — the general form is "when you can't
measure the outcome, constrain the process instead."

The speculative-decoding debunk is held as the strongest backup and remains unposted; it scores nearly as high and
is untouched by this post's cooldown.

## Fact check

| Claim in post | Traced to | Verdict |
|---|---|---|
| IBM published per-stage RL hyperparameters for Granite 4.2 | [[IBM Granite Team - Granite 4.2 LLMs How They're Built]], "The 30B stage table" | ✅ prompts/step, gens/prompt, seq len, rollout turns, KL, LR given per stage |
| Verifiable-reward stages run at KL = 0 | Same, stage table: RLVR ×3 KL 0, IF booster KL 0, SWE 2 KL 0 | ✅ verbatim |
| Preference/safety stage runs at KL = 0.05, the pipeline's highest | Same: RLHF KL 0.05; code booster also 0.05; no stage exceeds it | ✅ "highest" is accurate as a maximum, not a unique value |
| Code that must pass hidden tests trains at KL 0 | Same: RLVR uses competitive coding checked against hidden tests in a sandbox (KL 0); SWE 2, rewarded on hidden tests, KL 0 | ✅ |
| "Not perfectly binary — the agentic stages sit at 0.01" | Same: SWE 1, Terminal, Search all KL 0.01 | ✅ included precisely because the clean version of the story would have been false |
| Rationale: unverifiable reward ⇒ drift and reward hacking are indistinguishable | [[Reward Design for RL]], "KL as a reward-type-dependent parameter" | ✅ vault's own framing, not invented for the post |
| First-party report, self-reported benchmarks, no ablations | [[IBM Granite Team - Granite 4.2 LLMs How They're Built]], "Tensions / open questions" | ✅ hedged in the post body, not only here |
| Author attribution "IBM Granite Team" | Same, `source_author` | ✅ matches; the post is signed by the team, not the four capture-byline individuals |
| URL | Same, `source_url` | ✅ |

**Cut during fact-check:**

- An earlier draft said the KL rule was "IBM's recommendation." The source never frames it as advice — it reports
  what was done. Rewritten to "the report suggests," and the no-ablations caveat kept in the body.
- A line claiming the schedule "is why Granite scores well on SWE-Bench" was cut outright. The vault records no
  ablation, so no causal claim about the schedule is supportable.
- "Every verifiable stage runs at KL 0" was cut and replaced with the explicit 0.01 exception, since SWE 1, Terminal,
  and Search are outcome-rewarded yet non-zero.

## Attribution

- **IBM Granite Team**, *Granite 4.2 LLMs: How They're Built* — https://huggingface.co/blog/ibm-granite/granite-4-2
- Credited inline in the post body, not only here.

## Hashtags

`#ReinforcementLearning #LLMTraining #RewardDesign #GRPO #OpenModels`

Deliberately avoided `#AI`, `#MachineLearning`, and `#Innovation` — too broad to reach the people this lands for.

## Related pages

- [[Reward Design for RL]] - spine page; the KL-follows-reward-type rule lives here
- [[IBM Granite Team - Granite 4.2 LLMs How They're Built]] - source summary the post draws on
- [[Group Relative Policy Optimization]] - the optimizer whose KL term this concerns
- [[Staged Reinforcement Learning Curriculum]] - why the pipeline has separable stages to set KL per stage
- [[Post Archive]] - ledger of posts and spine-page cooldowns
