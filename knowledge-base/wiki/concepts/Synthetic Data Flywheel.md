---
type: concept
created: 2026-09-11
updated: 2026-09-11
tags:
  - concept
  - topic/training
  - topic/synthetic-data
source_ids:
  - src-2026-09-09-zafstojano-recursive-synthetic-improvement
status: active
---

# Synthetic Data Flywheel

## Definition

The loop in which a human-generated artifact in the training stack is replaced by a model-generated one,
which trains better models, which generate better artifacts.
[[@zafstojano - Recursive Synthetic Improvement]] proposes this as the literal content of "recursive
self-improvement" in current practice — the acronym "might as well stand for **Recursive Synthetic
Improvement**" — and identifies **five parts of the stack that have each flipped**: the **Judge**, the
**Corpus**, the **Teacher**, the **Curriculum**, and the **Environment**.

The reframing matters because it makes the claim checkable. Each of the five can be independently
examined for whether the human has actually been removed, and each sits at a different point on that arc.

## Why it matters

It reinterprets [[Recursive Self-Improvement]] as something less dramatic and more measurable than a
model rewriting its own weights. The recursion runs through **artifacts** — labels, corpora, teachers,
task distributions, environments — and each stage has published evidence and published limits.

It also identifies where the binding constraint has moved. **GLM-5.3 is a controlled experiment by
accident**: the same base, the same architecture, the same total and activated parameters as GLM-5.2,
with one month of scaling long-horizon environments and RL, and gains that are "not marginal." Jie Tang's
gloss is that "the dials do not have to be turned together." Set against Noam Shazeer's older
formulation — **"FLOPs were intelligence; parameters were knowledge"** — this is the clearest available
evidence that [[RL Environment Design]] is now the scaling axis rather than parameter count.

## Current synthesis

### The Judge

InstructGPT's three phases → Constitutional AI and RLAIF → LLM-as-a-judge. The threshold result is Zheng
et al. (2023): **GPT-4 agreeing with human raters at roughly 80%, about equal to inter-human agreement**
— past which paying for human preference labels became optional for most purposes. Kimi K2 folded the
judge back into the policy as its own rubric-guided critic. The residual human-preference layer became a
business: Chatbot Arena's commercial arm reached **$100M ARR eight months after launch on a $150M Series
A**. See [[LLM-as-a-Judge]].

### The Corpus

**Filtering discards ~98% of the web.** Common Crawl exceeds 10 PB; DCLM keeps about **3.8T tokens of
240T extracted**, of which only ~1T are unique. Model-based filtering replaced heuristics: FineWeb-Edu
labelled ~500k documents with Llama-3-70B-Instruct, trained a classifier on those labels, and cut **15T
tokens to 1.3T**.

**Synthetic pretraining data works.** TinyStories trained sub-10M-parameter models on generated
children's stories; "Textbooks Are All You Need" took **phi-1 from 29% to 51% on HumanEval**,
outperforming baselines 10× its size.

**Collapse requires replacement, not addition.** Gerstgrasser et al. (2024) showed that *accumulating*
synthetic data alongside real data avoids the collapse that *replacing* real data causes — the finding
the whole corpus programme depends on.

**Rephrasing gives speedups without new information, and the mechanism is now understood.** WRAP
rephrases C4 in four styles mixed 1:1 with real data for **up to 3× training speedup**; Nemotron-CC
reaches **6.3T tokens (4.4T real unique + 1.9T synthetic)**. **BeyondWeb converges 2.7× faster than
Nemotron-Synth, and its gains come from per-token information density rather than the generator's
knowledge — rephraser size barely matters past 3B.** FinePhrase ran **333 train-and-evaluate experiments
over 90 rephrasing configurations** to establish this. The alternative is capped: Muennighoff et al.
(2023) put diminishing returns on repeating real pretraining data at about **4 epochs**.

### The Teacher

Off-policy distillation minimises forward KL and is **mode-covering**; on-policy minimises reverse KL and
is **mode-seeking**. The 2023 cohort established how cheap it is: Self-Instruct bootstrapped ~82k
instances from **175 seed tasks**; **Alpaca** produced 52k pairs for ~$500 of API calls plus ~$100 of
compute in three hours on 8×A100; **Vicuna** reached "~90% of ChatGPT quality" on 70k ShareGPT
conversations for **$300**; Orca used ~5M ChatGPT traces plus 1M from GPT-4.

**DeepSeek R1's distills are the most-used artifacts of the trend** — six sizes from ~800k samples
(~600k rejection-sampled reasoning, 200k non-reasoning), with **the 1.5B and 7B distills alone downloaded
over 35M times as of September 2026**.

**OpenThoughts3 (1000+ controlled experiments) produced three counterintuitive results**: sampling
multiple answers per question gives ≥16× the data *and* better results; **QwQ-32B is a stronger teacher
than DeepSeek-R1 despite being the weaker model**; difficulty filtering helps but **answer filtering does
not**. The middle finding breaks the assumption that distillation quality is bounded by teacher
capability. At the extreme of data efficiency, **s1 matched o1-preview from 1,000 curated questions**.

Distillation is now a line item in frontier pipelines: Qwen 3's distillation pipeline cost **10% of the
GPU compute** of the full multi-stage pipeline and performed better; Nemotron 3 Ultra trained **10+
domain-specialised teachers** consolidated via MOPD; MAI-Thinking-1 trained three. OPSD and SDPO use the
model as its own teacher with privileged information. See [[Knowledge Distillation]] and
[[Multi-Teacher On-Policy Distillation]].

### The Curriculum

Schmidhuber (2002) → AlphaGo and AlphaGo Zero → GANs → STaR → Self-Rewarding LMs → SPIN. **Absolute Zero**
is the current form: a proposer and solver in self-play, the proposer rewarded for *learnability*,
covering abduction, deduction and induction, and **anchored in a code interpreter** so the self-play
cannot drift away from ground truth. PopuLoRA evolves a population of student and teacher LoRAs paired by
TrueSkill.

### The Environment

The SWE-bench lineage automates progressively more of environment construction: SWE-bench (12 Python
repos) → SWE-bench Verified → SWE-rebench (install recipes derived from error logs) → SWE-smith (build
the environment first, then synthesise bugs by AST mutation, LM rewrite, or undoing a PR) → BugPilot (let
an agent break things by accident). **Terminal-Bench is not saturating**: 89 curated hard tasks at v2.0,
now in its fourth iteration with **top SOTA models under 60%**.

Frontier labs now synthesise tool environments rather than integrating real ones: **Kimi K2** combined
**3000+ real MCP tools with synthesised schemas** and τ-bench-style simulated users; **Kimi K3** built an
evolving hierarchical knowledge graph plus mock Slack, Gmail, Notion and Canvas preserving core semantics
without the external API burden. FunReason-MT composes tools into a DAG.

**The market repriced accordingly.** Anthropic leadership have reportedly discussed spending **over $1B
on environments in a single year**; Meta's 49% stake in Scale AI (June 2025) pushed labs to alternatives;
entrants include Deeptune (acquired by Mercor, July 2026), Turing, Fleet, Vmax, Bespoke Labs and
Mechanize, with Prime Intellect open-sourcing through the Environments Hub. **Mercor is dominant at
roughly $2B gross annualised run rate.**

**Jason Wei's Verifier's law** governs what gets built at all: "The ease of training AI to solve a task is
proportional to how verifiable the task is." And reward hacking is the recurring practical failure — in
*Training to Paint with Code*, an elaborate multi-criterion reward collapsed to "the same flat clip-art
flower with five rounded petals" because the judge's criteria were highly correlated and the length term
saturated; the shipped reward was much simpler. See [[Reward Design for RL]].

### The distillation dispute

Anthropic accused Moonshot of exfiltrating **3.4 million exchanges**. Separately, Panfilov et al.
disclosed *Stealing Reasoning Traces from Proprietary LLM APIs*: encrypted traces are interchangeable
across sessions, users and models within a provider's ecosystem, so passing a strong model's trace to a
weaker one makes it repeat the hidden reasoning verbatim. Evidence that Kimi K3 was prefilled with
decoded Opus 4.8 reasoning is **suggestive but explicitly inconclusive** — a stylistic shift. The
counter-argument is that RL does not distil: RL's Razor (SFT forgets more than RL), *Retaining by Doing*,
and *SFT Memorizes, RL Generalizes* all point the same way, and Nathan Lambert's formulation closes it —
**"One does not simply 'distill' RL environments, infrastructure to run them at scale, or algorithms to
mix them together effectively."**

## Open questions

- The survey documents five automated stages but never establishes that the loop **compounds**. Better
  judges improving corpora improving teachers is asserted by arrangement, not measured.
- The author's own closing caveat is the strongest objection to the framing: the apparent exponential "is
  mostly an artifact of just how little these labs disclose."
- Collapse is avoided by accumulating rather than replacing — but Nemotron-CC is already ~30% synthetic
  and the 4-epoch repetition ceiling limits how far real data can be stretched. The two constraints are
  never put together.
- If BeyondWeb's gains come from information density rather than generator knowledge, there should be a
  ceiling on rephrasing once density saturates. Nobody has located it.
- QwQ-32B being a better teacher than DeepSeek-R1 is unexplained. Whatever makes a good teacher is not
  capability, and is not characterised.
- Private evals are reportedly "basically dead" (Florian Brand), which removes the measurement apparatus
  the flywheel would need to verify its own progress.

## Related pages

- [[Recursive Self-Improvement]]
- [[Knowledge Distillation]]
- [[Multi-Teacher On-Policy Distillation]]
- [[RL Environment Design]]
- [[LLM-as-a-Judge]]
- [[LLM Training Pipeline]]
- [[Reward Design for RL]]
- [[Reinforcement Learning]]
- [[Automated AI Research]]
- [[Benchmark Optimization]]
- [[Model Factory]]
- [[@zafstojano - Recursive Synthetic Improvement]]
