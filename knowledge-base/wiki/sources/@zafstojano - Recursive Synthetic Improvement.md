---
type: source-summary
created: 2026-09-11
updated: 2026-09-11
source_id: src-2026-09-09-zafstojano-recursive-synthetic-improvement
source_title: "Recursive Synthetic Improvement"
source_author: "@zafstojano"
source_url: https://x.com/zafstojano/status/2097689256961466486
tags:
  - source/summary
  - training
  - synthetic-data
  - reinforcement-learning
source_ids:
  - src-2026-09-09-zafstojano-recursive-synthetic-improvement
status: active
---

# @zafstojano - Recursive Synthetic Improvement

## Summary

A long survey arguing that **"recursive self-improvement" is happening, but not in the form the term
usually implies** — the acronym "might as well stand for **Recursive Synthetic Improvement**." The loop is
not a model rewriting its own weights; it is that "a human-generated artifact gets replaced by a
model-generated one, which trains better models, which then generate better artifacts."

The structure is the paper's main contribution: **five parts of the training stack that have each flipped
from human-produced to model-produced** — the **Judge**, the **Corpus**, the **Teacher**, the
**Curriculum**, and the **Environment**. Each section traces the same arc from a human bottleneck through
a partial automation to a self-sustaining generator, and each ends somewhere different in that arc.

The author is the creator of Reasoning Gym, which appears in the Environment section, and closes with a
caveat that undercuts the whole framing: the apparent exponential is "mostly an artifact of just how
little these labs disclose."

## Key claims

### The Judge

**LLM-as-a-judge reached human-level agreement in 2023.** Zheng et al. found GPT-4 agreeing with human
raters at **roughly 80%**, "roughly equal to inter-human agreement" — the threshold past which paying for
human preference labels became optional for most purposes. The path runs InstructGPT's three phases →
Constitutional AI and RLAIF → LLM-as-judge.

**Kimi K2 folded the judge back into the policy**, using the model as its own rubric-guided critic
rather than a separate reward model.

**The human-preference layer became a business.** Chatbot Arena's commercial arm reached
**$100M ARR eight months after launch, on a $150M Series A.**

### The Corpus

**Filtering discards ~98% of the web.** Common Crawl exceeds **10 PB**; DCLM keeps about **3.8T tokens out
of 240T extracted**, and only about **1T of those 3.8T are unique**. Sutskever's "fossil fuel of AI"
framing is the backdrop.

**Model-based filtering replaced heuristic filtering.** FineWeb-Edu ran Llama-3-70B-Instruct over ~500k
documents to label educational quality, trained a classifier on those labels, and filtered **15T tokens
down to 1.3T**.

**Synthetic pretraining data works, and the early proof was small.** TinyStories trained sub-10M-parameter
models on GPT-3.5/4-generated children's stories. "Textbooks Are All You Need" took **phi-1 from 29% to
51% on HumanEval** over its base, "outperforming baselines 10× its size."

**Model collapse requires *replacing* real data, not adding to it.** Gerstgrasser et al. (2024) showed
accumulation avoids the collapse that replacement causes — the distinction that makes the rest of the
section viable.

**Rephrasing gives large speedups without new information.** WRAP rephrases C4 in four styles
(Easy, Medium, Hard, Q-A) mixed 1:1 with real data for **up to 3× training speedup**. Nemotron-CC
reaches **6.3T tokens — 4.4T real unique plus 1.9T synthetic**. Muennighoff et al. (2023) put the ceiling
on the alternative: repeating pretraining data past **4 epochs** gives diminishing returns.

**BeyondWeb isolates *why* rephrasing works, and the answer is not knowledge transfer.** It converges
**2.7× faster than Nemotron-Synth**, and the gains "come from per-token information density, not the
generator's knowledge" — **rephraser size barely matters past 3B**. FinePhrase ran **333
train-and-evaluate experiments over 90 rephrasing configurations** to pin this down.

**The practice has reached production user data.** Aidan Gomez is quoted on the industry position: the
promise is only not to train on exactly the data you put in — "rewritten data is fair game."

### The Teacher

**The off-policy/on-policy distinction is a divergence choice.** Off-policy distillation minimises forward
KL and is **mode-covering**; on-policy minimises reverse KL and is **mode-seeking**.

**Cheap distillation was proven in 2023 and the prices are the point.** Self-Instruct bootstrapped ~82k
instances from **175 seed tasks**; Alpaca produced 52k pairs for **~$500 in API calls plus ~$100 of
compute, three hours on 8×A100**; Vicuna used 70k ShareGPT conversations for **$300** and reached "~90%
of ChatGPT quality"; Orca used ~5M ChatGPT traces plus 1M from GPT-4.

**DeepSeek R1's distills are the most-used artifacts of the whole trend.** Six model sizes from ~800k
samples (~600k rejection-sampled reasoning plus 200k non-reasoning); **the 1.5B and 7B distills alone
have been downloaded over 35M times as of September 2026.**

**OpenThoughts3 ran 1000+ controlled experiments and produced three counterintuitive findings**: sampling
multiple answers per question gives ≥16× the data *and* better results; **QwQ-32B is a stronger teacher
than DeepSeek-R1 despite being the weaker model**; difficulty filtering helps but **answer filtering does
not**.

**s1 matched o1-preview from 1,000 curated questions**, the extreme end of the data-efficiency argument.

**Distillation is now a cost line in frontier pipelines.** Qwen 3's distillation pipeline cost **only 10%
of the GPU compute** of the full multi-stage pipeline and performed better. Nemotron 3 Ultra trained
**10+ domain-specialised teachers** consolidated via MOPD; MAI-Thinking-1 trained three domain
specialists. OPSD and SDPO use the model as its own teacher with privileged information.

### The Curriculum

The lineage runs Schmidhuber (2002) → AlphaGo and AlphaGo Zero → GANs → STaR → Self-Rewarding LMs → SPIN.
**Absolute Zero** is the current form: a proposer and a solver in self-play, the proposer rewarded for
*learnability*, covering abduction, deduction and induction, and **anchored in a code interpreter** so
the self-play cannot drift free of ground truth. PopuLoRA evolves a population of student and teacher
LoRAs paired by TrueSkill.

### The Environment

**SWE-bench's descendants automate progressively more of environment construction**: SWE-bench (12 Python
repos, fail-to-pass plus no regressions) → SWE-bench Verified → SWE-rebench (deriving install recipes
from error logs) → SWE-smith (build the environment first, then synthesise bugs by AST mutation, LM
rewrites, or undoing a PR) → BugPilot (let an agent break things by accident).

**Terminal-Bench is not saturating.** At version 2.0 it had **89 curated hard tasks**; now in its fourth
iteration, **top SOTA models score under 60%.**

**Frontier labs synthesise tool environments rather than integrating real ones.** Kimi K2 combined
**3000+ real MCP tools with synthesised schemas** and τ-bench-style simulated users; Kimi K3 built an
evolving hierarchical knowledge graph plus **mock Slack, Gmail, Notion and Canvas** that "preserve core
semantics without the external API burden." FunReason-MT composes tools into a DAG.

**GLM-5.3 is the cleanest evidence that environments are now the scaling axis.** Same base, same
architecture, same total and activated parameters as GLM-5.2 — **one month of scaling long-horizon
environments and RL**, and "the gains are not marginal." Jie Tang is quoted that "the dials do not have
to be turned together"; Noam Shazeer's older formulation supplies the contrast: **"FLOPs were
intelligence; parameters were knowledge."**

**The environment market repriced accordingly.** Anthropic leadership have reportedly discussed spending
**over $1B on environments in a single year**. Meta's 49% stake in Scale AI (June 2025) drove labs to
alternatives; entrants include Deeptune (acquired by Mercor, July 2026), Turing, Fleet, Vmax, Bespoke
Labs and Mechanize, with Prime Intellect open-sourcing via the Environments Hub. **Mercor is dominant at
roughly $2B gross annualised run rate.**

**Jason Wei's Verifier's law** governs what gets built: "The ease of training AI to solve a task is
proportional to how verifiable the task is."

**Private evals are losing their function.** Florian Brand is quoted that "semi-private evals and evals
with a hold out set are basically dead."

**Reward hacking is the practical failure, and simpler rewards fixed it.** In *Training to Paint with
Code*, an elaborate multi-criterion reward collapsed to "the same flat clip-art flower with five rounded
petals" because the judge's criteria were highly correlated and the length term saturated; the shipped
reward was much simpler.

### The distillation dispute

**Anthropic accused Moonshot of exfiltrating 3.4 million exchanges.** Separately, Panfilov et al.
disclosed *Stealing Reasoning Traces from Proprietary LLM APIs*: encrypted traces are interchangeable
across sessions, users and models within a provider's ecosystem, so passing a strong model's trace to a
weaker one makes it repeat the hidden reasoning verbatim. The evidence that Kimi K3 was prefilled with
decoded Opus 4.8 reasoning is **suggestive but explicitly inconclusive** — a stylistic shift toward
Claude.

**The counter-argument is that RL does not distil.** RL's Razor (SFT forgets more than RL), *Retaining by
Doing*, and *SFT Memorizes, RL Generalizes* all point the same way, and Kimi K3 has served almost **2T
tokens through OpenRouter alone**. Nathan Lambert's formulation closes it: **"One does not simply
'distill' RL environments, infrastructure to run them at scale, or algorithms to mix them together
effectively."**

## Why it matters

This is the most complete map the vault has of where training data now comes from, and it reframes
[[Recursive Self-Improvement]] in a way that is both less dramatic and more testable. The recursion is
real but it runs through **artifacts**, not weights — and each of the five stages can be checked
independently for whether the human has actually been removed.

Three findings deserve to outlive the survey. **BeyondWeb's** result that rephrasing gains come from
per-token information density rather than the generator's knowledge, with rephraser size irrelevant past
3B, is a mechanism claim that constrains how far the corpus flywheel can spin. **OpenThoughts3's**
finding that a weaker model (QwQ-32B) can be the better teacher breaks the assumption that distillation
is bounded by teacher capability. And **GLM-5.3** is a controlled experiment by accident: identical
architecture and parameter count, one month of environment work, non-marginal gains — the strongest
available evidence that [[RL Environment Design]] is now the binding constraint rather than scale.

The Verifier's law and the reward-collapse anecdote together explain the shape of what gets built, and
connect directly to [[Reward Design for RL]]: correlated judge criteria plus a saturating length term
produced a reward that was maximised by a single degenerate output.

## Tensions / open questions

- The author's own closing caveat is the most important one: the exponential appearance "is mostly an
  artifact of just how little these labs disclose." Most of the timeline is assembled from technical
  reports written by the parties with an interest in the narrative.
- The survey documents automation of five stages but never establishes that the loop *compounds*.
  Better judges improving corpora improving teachers is asserted by arrangement, not measured.
- Model collapse is dismissed via the accumulate-versus-replace distinction, but Nemotron-CC is already
  30% synthetic and the 4-epoch repetition ceiling limits how much real data can be reused. The two
  constraints are presented separately and never put together.
- The Kimi K3 distillation evidence is stylistic and the author says it is inconclusive. It sits beside
  strong counter-evidence that RL does not distil, and the section resolves to no verdict.
- The environment market figures ($1B, $2B run rate) are reported second-hand and describe spending
  intent rather than delivered capability.
- Reasoning Gym is the author's own project, and it is cited as a component of Olmo 3 and Nemotron 3
  Super training mixes.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Synthetic Data Flywheel]]
- [[Recursive Self-Improvement]]
- [[Knowledge Distillation]]
- [[Multi-Teacher On-Policy Distillation]]
- [[RL Environment Design]]
- [[LLM-as-a-Judge]]
- [[LLM Training Pipeline]]
- [[Automated AI Research]]
- [[Reward Design for RL]]
- [[@zafstojano]]

## Related pages

- [[Reinforcement Learning]]
- [[Benchmark Optimization]]
- [[Open Model Ecosystems]]
- [[Direct Preference Optimization]]
- [[Agentic Reinforcement Learning]]
- [[Model Factory]]
- [[Nathan Lambert]]

## Citations

- Raw capture: [[2026-09-09 @zafstojano - Recursive Synthetic Improvement]]
- Source: <https://x.com/zafstojano/status/2097689256961466486>
