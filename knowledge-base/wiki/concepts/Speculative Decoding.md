---
type: concept
created: 2026-07-06
updated: 2026-10-16
tags:
  - concept
  - inference
  - speculative-decoding
  - serving
  - efficiency
source_ids:
  - src-2026-07-06-mayank-pratap-singh-speculative-decoding
  - src-2026-08-14-changyi-yang-mla-mtp-arithmetic-intensity
  - src-2026-08-25-jacob-peake-ai-chip-architectures
  - src-2026-08-23-wafer-ai-performance-engineering-resources
  - src-2026-08-26-alex-zhang-speculative-programmatic-tool-calling
  - src-2026-08-26-bytebytego-how-to-make-llms-3x-faster
  - src-2026-09-02-baseten-efficient-frontier-inference
  - src-2026-09-21-bytebytego-big-model-cheap-hardware
  - src-2026-10-11-samarin-speculative-decoding
status: active
---

# Speculative Decoding

## Definition

Speculative decoding proposes several future tokens with a cheap drafter and checks them with
a target model in a parallel verification pass. Exact variants preserve the target's output
distribution through the verification rule; this does not require seed-identical sampled text.
Approximate acceptance variants need a separate quality contract. The drafter can be an
auxiliary module or a lookup procedure, not necessarily a second standalone language model.

## Why it matters

In low-batch, weight-bandwidth-bound [[LLM Inference]], one weight load can verify multiple
positions while using otherwise spare arithmetic. Long-context cache traffic can create a
different opportunity to amortize reads. Neither regime guarantees a win: draft cost,
verification kernels, memory, and scheduling determine whether fewer target passes actually
reduce latency or increase throughput.

## Current synthesis

[[Mayank Pratap Singh - Speculative Decoding in vLLM]] builds the technique end to end.

### The mechanism

- A drafter `M_q` proposes K tokens for target `M_p`. Under greedy matching, verification
  commits the matching prefix and a target correction at the first mismatch. Under stochastic
  rejection sampling, acceptance is probabilistic and the correction comes from a residual
  distribution. If every proposal is accepted, the round can supply a bonus target token.
  Only the committed history becomes target [[KV Cache]] state; rejected work may inform later
  proposals without becoming accepted history. A round can advance by only one token while
  costing more than an ordinary step, so token progress is not a latency guarantee.

### Why it is exact

- Exact rejection sampling (Leviathan 2023; Chen 2023) accepts a draft token with probability
  `min(1, p(x)/q(x))` and, on rejection, samples from normalized `(p-q)+`, reconstructing
  the target distribution. At one position, `alpha = sum min(p, q) = 1 - TV(p, q)`.
  This protects the target's sampling distribution, not the factual correctness of its answers.
- [[Aleksandr Samarin - Speculative Decoding - The Art of Guessing Well]] distinguishes that
  result from reproducibility. Shared, position-consistent Gumbel noise can instead match the
  target's sampled path across drafters, with a different acceptance coupling. Correct causal
  masks, cache bookkeeping, and sampling transformations remain implementation requirements.

### The economics: α, τ, K

- **α (acceptance rate)** — the probability a proposed token survives; important but insufficient
  without the cost of producing and checking it.
- **τ (committed tokens per round)** — under constant conditional acceptance,
  `τ = (1 − α^{K+1}) / (1 − α)`, including the correction/bonus token. For K=5, α=0.30
  yields about 1.43 and α=0.85 about 4.15; at α=1 the limit is K+1. Real prefixes have
  position-dependent survival. Some papers count only accepted draft tokens, so check the
  convention before comparing their reported acceptance lengths.
- **K (lookahead)** — how far to guess. Tune expected prefix survival against measured
  verification and drafting cost, rather than maximizing length or using target entropy alone.

### When it wins and when it loses

- **The bottleneck determines the opportunity.** Low-batch weight-bound decode is the classic
  favorable case. At compute saturation, extra verification and drafting can hurt; batching
  and variable accepted lengths also create scheduling costs. The earlier vLLM/ByteByteGo
  accounts motivate reducing speculation under load, but Samarin adds long-context,
  cache-bound large-batch exceptions. Batch size is a useful signal, not a universal on/off rule.
- **System tax vs token math.** Fixed per-step overheads (kernel launches, KV-cache lookups) drag a 2.5× token-math win down to ~1.8× measured. As batch grows, target verification's share of the step climbs (52%→74%) and the draft's collapses (24%→10%), so the recoverable headroom shrinks with batching.
- **Constraints:** the direct tokenwise algorithm assumes proposals in the target's token
  space; auxiliary weights, private cache, workspace, and rejected computation can compete
  with target serving. A rejection ends the committed draft prefix, not necessarily all useful
  proposal information.

### The method families

Drafts can come from a separate model, n-gram prompt lookup, or target-conditioned modules.
**Medusa** adds prediction heads and tree verification; exactness depends on its acceptance
variant. Original **EAGLE** uses feature prediction, while **EAGLE-3** fuses multiple target-layer
features and drops the feature-regression objective in favor of token training. These are
different training designs, not interchangeable names for one feature-space method.

### It is a bet

- The honest lesson: on Llama-3.1-8B on a single saturated 48 GB Ada GPU, EAGLE3 came out **slower in both regimes** — acceptance length τ=1.81 was the one-glance tell. The win grows with **model size** and **acceptance**; a small model on a fast, saturated GPU is the losing case. Always A/B on your own hardware before shipping.

## Relationship to neighbouring levers

[[Model Quantization and Efficiency|Quantization]] cuts representation size and
[[KV Cache|cache compression]] cuts history traffic; speculation amortizes target work over
more committed tokens. Their gains need not multiply. Exact speculation aims to serve the
**same output distribution** more efficiently, whereas [[Test-Time Scaling]] changes the
inference procedure to seek better answers.

## The headroom speculation depends on can already be spent

The strongest constraint on this page comes from [[Changyi Yang - Why MLA and MTP Fight Each Other]], and it is not about acceptance rate at all. Speculation works because a memory-bound decode leaves GPU compute idle; verifying K drafted tokens in one pass costs arithmetic that was going to waste. Formally, HBM traffic barely grows with the number of verified query positions S while QK/PV compute scales nearly linearly, so `AI(S) ≈ S · AI(S=1)` — speculation is a device for climbing the roofline (see [[Arithmetic Intensity and the Roofline Model]]).

That only pays while there is roofline left. **Attention architectures that maximise cache reuse have already spent it.** DeepSeek-style MLA reaches ~256 FLOP/B at a single query and Kimi K3's MLA layer ~192 FLOP/B, against balance points of ~206 FLOP/B on H200 and the two-to-three-hundred range on H100/B200. Taking S to 2 gives 512 and 384 — past the knee, where the extra verification arithmetic stops being free and **starts costing real latency**. On a low-intensity MQA workload at AI ≈ 70–100 the same speculation is nearly free.

Two corollaries:

- MLA and multi-token prediction are **not independent optimisations**. Both can spend the same
  compute-for-bandwidth headroom. This also applies to self-drafting MTP: avoiding a second
  full language model does not eliminate auxiliary parameters, state, or workspace.
- Typical speculation windows of 2–8 (at most a few dozen) stay well below the S ≈ 171 crossover at which the dense-GEMM attention algorithm would take over, so speculation does not change which attention kernel is dispatched.

[[Jacob Peake - AI Chip Architectures]] describes the same mechanism from the hardware side: speculative decoding and multi-token prediction exist to promote decode GEMVs back into GEMMs, alongside continuous batching — which means batch size and speculation are also competing for the same headroom, not stacking on it.

## Where the technique comes from

[[Wafer - AI Performance Engineering Resources]] supplies the lineage this page has been describing through a single vLLM implementation write-up. The method was introduced independently by Leviathan et al. (*Fast Inference from Transformers via Speculative Decoding*) and Chen et al. (*Accelerating Large Language Model Decoding with Speculative Sampling*), both establishing the property that makes it safe to deploy: the accept/reject rule preserves the target model's output distribution exactly.

Later work replaces a separate general-purpose draft model with target-conditioned components.
**Medusa** adds heads and **EAGLE** uses target features. This can reduce the serving burden,
but auxiliary checkpoints, training, and alignment with a particular target version remain
operational responsibilities; self-drafting does not make them disappear.

## The same idea, one layer up

[[Speculative Tool Execution]] ([[Alex L. Zhang - Speculative Programmatic Tool Calling]]) applies this page's pattern above the token level: a harness parses tool calls out of a *partially generated* program and pre-launches them, so that if the finished program invokes them they return from cache. Guessing actions instead of tokens.

The structural analogy is close — cheap speculative work overlapped with an expensive serial process, discarded when wrong — but two properties do not carry over. There is **no distributional guarantee**: token speculation is provably lossless because the accept/reject rule preserves the target distribution, while a speculated tool call is either used or wasted, and a wasted one has already consumed money, tokens, and rate limit. And the wrong-guess cost is external rather than internal: a mispredicted draft token costs idle compute, a mispredicted sub-agent call clogs a serving engine other requests are waiting on.

Both techniques exploit the same underlying slack, though, which is worth noting: on a locally served model the engine is memory-bound decoding the main context, so speculative sub-calls consume compute that would otherwise sit idle — the argument on [[Arithmetic Intensity and the Roofline Model]], applied to agent harnesses.

## A fourth draft family, and what production actually reports

[[ByteByteGo - How to Make LLMs 3X Faster]] adds a draft source the taxonomy above does not cover:
**a degraded copy of the target model itself**. The draft runs the same weights under a reduced
compute budget — quantization, layer skipping, or a compressed KV cache — while verification runs
at full precision. QuantSpec drafts with 4-bit weights and a 4-bit KV cache and reports above
**1.78× with acceptance above 90%**.

This reuses the target's weights rather than training an independent general-purpose drafter.
Unlike learned auxiliary heads, the described degraded-weight approach needs no separate
drafter training, but quantized copies, scales, cache formats, and workspace still depend on
the implementation. Draft and target share hardware and cache structures. It also makes [[Model Quantization and Efficiency|quantization]]
do double duty: the same 4-bit machinery that cuts bytes per weight becomes the mechanism for
generating cheap drafts.

The same source supplies the first **production** acceptance figure on this page. DeepSeek reported
**80–90% acceptance for the second predicted token when serving DeepSeek-V3**, worth roughly 1.8×
generation throughput. Everything else here comes from benchmarks or single-GPU experiments, so a
sustained production number is a different class of evidence — and it lands near the top of the α
range the economics section models, which is what makes self-drafting MTP heads attractive despite
their training cost.

## Acceptance depends jointly on the drafter and workload

The earlier workload-centered account explains why identical deployments can behave differently
on different traffic. Samarin's overlap formula adds the other half: acceptance depends on
both target and draft distributions, hence on model pairing, training, prefix, task, and sampling.

Structured or repetitive output can favor a suitable drafter; task labels alone do not determine
agreement. Temperature changes both distributions and their overlap, so acceptance need not
decrease monotonically with temperature.

The operational consequence is uncomfortable. Two teams can deploy the identical configuration on
identical hardware and get different results, because their traffic differs. Speculative decoding is
therefore not a setting that can be validated once and shipped as a default; it has to be measured
against the actual request distribution, and re-measured when that distribution shifts.

## No direct prefill acceleration is not unchanged TTFT

Speculation targets generation rather than directly accelerating prompt processing. End-to-end
time to first token can still change through draft initialization, queueing, scheduling, and
resource competition; unchanged prefill work does not imply unchanged TTFT.
Workloads with long prompts and short outputs — classification, extraction over large documents,
routing — have almost nothing to gain no matter how well they draft. DeepSeek stated the tradeoff in
the same direction: multi-token prediction *slightly reduces* throughput while significantly
improving end-to-end generation latency. That is a reported operating-point tradeoff, not a
universal law that speculation must reduce aggregate capacity.

## From concurrency-only switching to acceptance-aware scheduling

This page has stood with an open question about whether serving stacks could predict α online well
enough to auto-tune K and the on/off switch per request. Shipped code gives a partial answer, and it
works by **sidestepping prediction entirely**.

vLLM exposes a flag that disables speculation above a configurable batch size, and supports dynamic
adjustment in which **draft length shrinks as concurrency rises and reaches zero under heavy load**.
Rather than estimating acceptance, it keys draft length to *observed concurrency* — a directly
measurable proxy for whether spare compute exists at all. [[ByteByteGo - How to Make LLMs 3X Faster]]
frames this as routine operational tuning rather than an edge case.

That addresses resource pressure, not request-specific prefix survival. The earlier account's
measured shape is stark: one systematic evaluation reported **up to 1.96× on a 70B model at batch
size 1, declining to 1.21× at batch size 128**, and falling below baseline under higher concurrency.

The October 16 ingest updates the earlier claim that no described system predicts draftability.
[[Aleksandr Samarin - Speculative Decoding - The Art of Guessing Well]] describes **DSpark**
combining predicted conditional acceptance with the engine's profiled step rate to allocate
draft lengths across a batch. This is model- and engine-specific evidence, not proof that every
vLLM deployment implements that controller or that confidence generalizes to shifted traffic.

## Has speculation changed category?

This page frames speculation as spending headroom that could be spent elsewhere — a tradeoff. [[Philip Kiely - The Efficient Frontier of LLM Inference]] argues the category boundary has moved, and the disagreement is
worth keeping visible rather than resolving.

The historical framing is granted: speculation *was* a tradeoff technique, because it was expensive, sequences
were short, acceptance rates were low, and it was viable only at small batch sizes. The claim is that
**EAGLE-3, DSpark and DFlash** changed this, because their strength yields efficiency from **skipped forward
passes** in addition to raw latency reduction — a genuine reduction in work rather than a reallocation of it.
That would make speculation **frontier-moving**: gains that can be allocated to latency or throughput at will.

The qualification is retained in the same source: these methods still **compete with the main model loop for
resources**, and so still cap maximum batch size. Code generation benefits most, because output sequences are
relatively predictable — which is also why it is the case most likely to overstate the general result.

Samarin supplies a way to test that claim rather than settle it by category: count all draft,
verification, cache, and scheduling work at a matched serving objective. Cache-bound large-batch
wins qualify the older low-load-only view; below-baseline examples qualify blanket frontier
improvement. See [[Inference Efficiency Frontier]].

## Cheap hardware changes the break-even point

[[ByteByteGo - How to Run a Big Model on Cheap Hardware]] frames speculative decoding as a three-way
trade: draft agreement, target verification cost, and extra draft-model memory. A smaller machine can
lose the latency benefit when the draft model or verification competes for scarce fast memory.

## The verifier, drafter, and scheduler form one optimization problem

[[Aleksandr Samarin - Speculative Decoding - The Art of Guessing Well]] replaces the assumption
of one cheap verification pass with an explicit cost model. For batch B, N draft-tree nodes,
and target step cost T, the idealized speed ratio is
`tau(N) * T(B) / (T(B * (N + 1)) + T_draft)`. Attention, kernel shape, and compaction affect
the denominator as much as acceptance affects the numerator.

Its illustrative alpha=0.8, K=5, c=0.05 example yields about **3.69 committed tokens**,
**2.95x** with serial drafting, and **3.51x** with one parallel pass under cheap verification.
These are calculations, not measurements. A cited Qwen3-4B/GSM8K comparison gives EAGLE-3 and
DFlash the same **tau=4.2**, but **2.1x versus 3.3x** speedups; a separate
Qwen3-8B/MATH500 AMD-vLLM example puts EAGLE-3 at **0.44-0.88x** baseline.

Parallel proposals reduce serial draft work but can combine incompatible output marginals.
The survey describes DFlash as a one-step masked block predictor at inference, and
DSpark/Domino as restoring dependence with lightweight causal heads. Tree verification needs
ancestor-only attention; block verification uses a different joint prefix rule. Reusing
rejected proposals does not authorize committing them to target history.

Training must match that verifier and the prefixes encountered at deployment. Minimizing KL,
maximizing token overlap, maximizing block acceptance, and minimizing sequence-level verification
rounds are different objectives for a limited-capacity drafter; see [[Knowledge Distillation]].
Private drafter cache versus borrowed target state is a separate memory choice, not something
acceptance length measures.

## Open questions

- How well do acceptance predictors such as DSpark's calibrate under traffic or target-model
  changes, and when is their overhead justified over concurrency-only switching?
- Can cross-tokenizer or tokenizer-free speculation relax the same-family constraint?
- Where is the model-size/batch crossover at which speculation reliably pays, and how does it shift with EAGLE-style feature drafting?
- Should a serving stack disable speculation automatically for high-arithmetic-intensity attention architectures, and can the balance point be probed at runtime rather than assumed from the datasheet?

## Related pages

- [[Aleksandr Samarin - Speculative Decoding - The Art of Guessing Well]]
- [[Knowledge Distillation]]
- [[Mayank Pratap Singh - Speculative Decoding in vLLM]]
- [[Changyi Yang - Why MLA and MTP Fight Each Other]]
- [[Jacob Peake - AI Chip Architectures]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[LLM Inference]]
- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[GPU Execution Model]]
- [[Test-Time Scaling]]
- [[Small Language Models]]
- [[AI Knowledge Base Overview]]
- [[Wafer - AI Performance Engineering Resources]]
- [[Serving Benchmarks and Goodput]]
- [[Speculative Tool Execution]]
- [[Programmatic Tool Calling]]
- [[Alex L. Zhang - Speculative Programmatic Tool Calling]]
- [[ByteByteGo - How to Make LLMs 3X Faster]]
- [[Inference Efficiency Frontier]]
- [[Philip Kiely - The Efficient Frontier of LLM Inference]]
