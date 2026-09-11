---
type: source-summary
created: 2026-09-11
updated: 2026-09-11
source_id: src-2026-09-09-raschka-astra-looped-hidden-reasoning
source_title: "GPT-6 Astra, Looped Transformers, and Hidden Reasoning"
source_author: Sebastian Raschka
source_url: https://magazine.sebastianraschka.com/p/gpt-6-astra-looped-transformers-and
tags:
  - source/summary
  - architecture
  - reasoning
  - ai-agents
source_ids:
  - src-2026-09-09-raschka-astra-looped-hidden-reasoning
status: active
---

# Sebastian Raschka - GPT-6 Astra, Looped Transformers, and Hidden Reasoning

## Summary

The long-form version of the argument Raschka sketched a week earlier in
[[Sebastian Raschka - OpenAI Astra and Looped Transformers]]. That piece was a short note rebutting press
coverage; this is a full article covering three subjects the note only gestured at — what Astra's
benchmarks actually show, what the looped-transformer literature has established, and whether looping
causes the loss of monitorable reasoning traces.

The short note's conclusions survive intact and are not restated here. What this source adds is the
evidence: **three open-weight looped models with their exact loop arithmetic**, five research results
including two from late 2026, a direct quote from OpenAI's Chief Scientist on monitorability, and an
argument that **computer use, not architecture, is the important thing about Astra**.

Raschka's central negative claim about the hidden-reasoning story is a counterexample rather than an
argument: **GPT-5.6 Luna uses about 80% more tokens than Sol at similar performance, and nobody concludes
from this that Sol is less interpretable than Luna.** Token count alone does not establish a
monitorability regression.

## Key claims

**Astra's headline benchmark result is real but narrow.** It scores **99.9% on ARC-AGI-3, against 7.8%
for GPT-5.6 Sol** — a jump Raschka does not dispute. On the Artificial Analysis Coding Agent Index v1.4
it leads, but "doesn't pull ahead by leaps and bounds." The tension between those two readings is left
standing.

**Independent evaluations are more trustworthy than vendor ones, but carry a systematic bias against the
vendor.** GDPval-AA and AA-Briefcase run on the open-source minimal **Stirrup** harness, Terminal-Bench
v2.1 on **Terminus 2**, and τ³-Banking on the τ-Bench harness. Because "models are usually developed with
one primary harness in mind", agentic scores measured on a neutral harness may *underestimate* a model
in its own. This cuts against the usual assumption that independent numbers are conservative.

**Stale agent configuration may now hurt.** Raschka suggests archiving old `AGENTS.md` and `SKILL.md`
content, since newer models "may be over-constrained by it."

**Computer use is the substantive advance, and the training story is the interesting part.** OpenAI
bought tens of thousands of Mac Minis and Mac Studios — "not for training compute" but as **reinforcement
learning environments**. The loop is seven steps: prompt, screenshots, predicted mouse and keyboard
actions, execution, new screenshots, repeat, verifier reward. Raschka frames it as the GUI analogue of
RLVR. NVIDIA's CEO separately said Astra was trained on roughly **100,000 Grace Blackwell GPUs**.

**Looping's compute cost is not offset by a KV cache saving, and one team tried.** Nanbeige4.2-3B applies
the same **22-layer stack twice, for 44 block applications**, roughly halving transformer-block
parameters — but compute is similar to 44 distinct blocks because backpropagation runs through all 44.
On memory: **each pass needs its own KV entries, so there is no KV-cache saving.** "Nanbeige tried
sharing the KV cache across loops and halving it, and the model performed worse." Embedding and output
layers are about 25% of the 3B total, so the parameter saving is smaller than the layer count suggests.
Training from scratch beat upcycling an existing model, and two passes remained their preferred
trade-off.

**The idea is eight years old.** **Universal Transformers (2018)** repeat a single block with adaptive
halting, driven by a learned halting probability and a threshold.

**Deeper loops exist but their implementations lag their designs.** **Ouro-Thinking 2.6B** applies a
48-block stack four times — 192 block applications — with a learned exit gate; but Raschka notes the
released Hugging Face implementation "computes all four passes and then selects", so the advertised early
exit does not yet buy compute.

**Mixture-of-Recursions reverses its own conclusion at small scale.** MoR routes per token, and the paper
compares expert-choice against token-choice routing. MoR wins at larger scale and smaller compute
budgets — but **"the 135M model shows the opposite conclusion"**, which Raschka draws out as a general
methodological point about "the importance of running some experiments at scale."

**Hidden chain of thought is not new for end users.** "OpenAI has hidden the traces since o1", so nothing
changes for them; the concern is for developers who relied on the traces.

**The token-efficiency evidence does not support the monitorability story.** Astra does not use fewer
tokens overall than Sol, only fewer at fixed accuracy. And the Luna comparison — 80% more tokens at
similar performance — shows that token count and interpretability are not the same axis.

**Astra's own system card does report a monitorability regression**, mostly shorter and less informative
traces. Raschka accepts the finding but not the causal attribution: nothing in it establishes that
looping is the cause.

**Jakub Pachocki, OpenAI's Chief Scientist, is quoted as saying the opposite of the press framing.**
*"I want to prevent a race into unmonitorability kicked off by confused reporting. The depth of the
computation graph for our present frontier models, including Astra, is within a factor of two of GPT-4...
I do think it is fragile and unfortunately trending in a negative direction, for reasons not contingent
on architecture changes."* Both halves matter: the architecture claim is denied, and the underlying
concern is confirmed.

**Geiping et al.'s latent-reasoning model shows where looping helps and where it saturates.** A 3.5B model
trained on 800B tokens, with 4 shared blocks sandwiched between 2 prelude and 2 coda blocks, the loop
count randomised during training and an adaptive KL-divergence stopping criterion at inference. The
result is task-dependent: **HellaSwag levels off after about 8 loops, while GSM8K and HumanEval keep
benefiting.** Reasoning tasks use the extra depth; commonsense completion does not.

**"Beyond Parameters: Virtual Logic Depth" (June 2025)** finds that looping "leaves memorization capacity
nearly unchanged but improves multi-step math" — the cleanest statement of what looped depth actually
buys.

**SMELT (September 2026)** is the strongest efficiency result cited: compute-matched MoE looped
transformers up to 54B non-embedding parameters needing **6.8–18% less training compute for the same
validation loss**.

**A negative result is reported alongside.** The **full-bandwidth transformer (August 2026)** uses latent
feedback to shorten MATH500 reasoning traces in a 1B base model, "but the effect disappears after
instruction tuning."

## Why it matters

This is the vault's best-sourced treatment of [[Recursive Architectures]], and it changes what the vault
can claim about them. The earlier note left "looping trades compute for parameters" as the summary; this
source shows the trade is worse than that — **no KV-cache saving, compute proportional to unrolled depth,
and a failed attempt to fix it by sharing the cache.** SMELT's 6.8–18% compute saving at fixed loss is
the first result that makes looping look like a win rather than a wash, and it is recent enough to be
unreplicated.

The Geiping saturation finding and the "Beyond Parameters" result together give a mechanism for
[[Latent-Space Reasoning]]: looped depth adds *reasoning* capacity specifically, not memorisation, and
saturates on tasks that do not need multi-step computation. That is a sharper claim than "more compute
helps."

For [[Chain-of-Thought Monitoring]], the Pachocki quote is the most important item in this batch. It
separates two things the coverage merged: the architecture is not the cause, *and* monitorability is
genuinely degrading anyway. Preserving both halves is the point — dropping the second would make this a
debunking, which it is not.

The computer-use material also opens ground the vault has not covered: RL environments built from
physical consumer hardware, with a verifier supplying reward over screenshots. That is the same
environment-scarcity story that [[Synthetic Data Flywheel]] documents from the training-data side, seen
from the procurement side.

## Tensions / open questions

- Raschka never reconciles 99.9% on ARC-AGI-3 with "doesn't pull ahead by leaps and bounds" elsewhere.
  Either the other benchmarks are saturated, or ARC-AGI-3 measures something the coding indices do not.
- The harness caveat is genuinely double-edged and is left unresolved: neutral harnesses may understate a
  model, vendor harnesses overstate it, and there is no proposed way to measure the gap.
- SMELT's 6.8–18% is compute-matched at fixed validation loss, which is not the same as fixed downstream
  capability, and is a single September 2026 result.
- Ouro-Thinking's early-exit gate is described as a design the released implementation does not realise.
  Its reported efficiency numbers therefore need care about which version produced them.
- The MoR scale reversal is reported as a caution but not explained. If 135M and larger models disagree
  about routing strategy, the mechanism behind the crossover is unknown.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Recursive Architectures]]
- [[Latent-Space Reasoning]]
- [[Chain-of-Thought Monitoring]]
- [[Computer Use Agents]]
- [[Transformer Architecture]]
- [[KV Cache]]
- [[Sebastian Raschka]]
- [[OpenAI]]

## Related pages

- [[Sebastian Raschka - OpenAI Astra and Looped Transformers]]
- [[LLM Reasoning]]
- [[Reasoning Compression]]
- [[Reasoning Trace Privacy]]
- [[Test-Time Scaling]]
- [[Benchmark Optimization]]
- [[Mixture of Experts]]

## Citations

- Raw capture: [[2026-09-09 Sebastian Raschka - GPT-6 Astra, Looped Transformers, and Hidden Reasoning]]
- Source: <https://magazine.sebastianraschka.com/p/gpt-6-astra-looped-transformers-and>
