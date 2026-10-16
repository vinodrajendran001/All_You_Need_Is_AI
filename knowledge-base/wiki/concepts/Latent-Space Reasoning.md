---
type: concept
created: 2026-05-18
updated: 2026-10-16
tags:
  - concept
  - reasoning
  - architecture
source_ids:
  - src-2026-05-18-alphasignal-return-of-recursion
  - src-2026-06-04-progressive-thought-encoding
  - src-2026-06-04-reasoncache
  - src-2026-07-02-arora-llm-reasoning-advances
  - src-2026-09-02-raschka-astra-looped-transformers
  - src-2026-09-09-raschka-astra-looped-hidden-reasoning
  - src-2026-10-12-bytebytego-energy-based-reasoning
  - src-2026-10-14-dickson-kv-cache-handoffs
status: active
---

# Latent-Space Reasoning

## Definition

Latent-space reasoning is the use of continuous internal representations for intermediate computation instead of generating explicit natural-language tokens for every reasoning step. Rather than “thinking out loud” in text, a model iterates over compressed hidden states and produces language only when it needs to expose a final answer.

## Why it matters

Reasoning in latent space can be faster, cheaper, and more compact than token-space reasoning because the model avoids repeatedly decoding long intermediate chains of text. That reduces token costs, lowers memory pressure, and lets the system spend compute on recursive internal updates instead of serial text generation. It is especially attractive for deterministic tasks where the main bottleneck is structured computation rather than broad world knowledge.

## Token-space contrast

In a standard [[Agentic Loop]] or chain-of-thought workflow, the model often externalizes intermediate reasoning as text tokens, then rereads those tokens to continue. That can improve performance, but it is slow and inefficient because every extra reasoning step expands the visible sequence. Latent-space reasoning keeps those intermediate steps compressed inside the model's state, trading inspectability for speed and compute efficiency.

## Representative implementations

- **HRM** uses coupled recurrent modules so a high-level planner can guide a fast low-level solver in latent space.
- **TRM** simplifies the idea to a tiny weight-sharing recursive network, suggesting that the recursive loop itself is the key ingredient.
- **RecursiveMAS** applies the same principle to multi-agent systems, with agents exchanging latent representations instead of text messages until final output time.

## Training implications

Making latent recursive systems work well still depends on training, optimization, and evaluation choices that overlap with [[Reinforcement Learning]] and related post-training methods. Even when these models are not trained with RL directly, the broader problem is similar: how to allocate computation over multiple steps, assign credit across reasoning trajectories, and optimize for accuracy under latency and cost constraints.

## Compression-oriented bridges

The newer efficient-reasoning batch adds two adjacent examples that are not full recursive latent reasoners but still push in the same direction:

- [[Training Large Reasoning Models Efficiently via Progressive Thought Encoding]] progressively compresses intermediate reasoning into fixed-size vectors so RL training and inference can run under bounded cache budgets.
- [[ReasonCACHE - Teaching LLMs To Reason Without Weight Updates]] distills demonstrations into a reusable key-value cache, letting the model learn reasoning skills without storing every step as long visible text or modifying the base weights in the usual way.

These methods reinforce the same general lesson: useful reasoning state does not always need to survive as a long explicit token trace.

[[Akhil Arora et al - Current Advances in LLM Reasoning]] gives this its broader framing.
Under the frozen-θ view, verifier-free [[Test-Time Scaling|test-time search]] can surface
learned reasoning paths rather than change weights. Keeping intermediate work in representations
is a distinct lever within [[LLM Reasoning]], but the absence of a token trace removes an
observable channel; it does not establish faithful or safe computation. The earlier version
of this page understated that oversight cost by treating the missing trace as less of a concern.

## Layer reuse is not latent reasoning

[[Sebastian Raschka - OpenAI Astra and Looped Transformers]] draws a boundary this page needs. Looped
transformers are frequently listed as latent-reasoning architectures, but reusing a layer stack is *"just reusing
layers in the transformer block"* — it adds computation in hidden states before the next token is emitted,
**exactly as ordinary layers do.** By that standard every transformer reasons latently, and the label stops
distinguishing anything.

The distinction that survives is quantitative rather than architectural. More computation available per token
means a model *may* need fewer explicit intermediate tokens to reach the same answer, shifting work into
activations that cannot be read as text. Raschka's crucial qualification is that this follows from capacity, not
from recurrence: **"we would get the same effect if we were scaling up the model size."** Latent reasoning, on
this reading, is a continuum every capability increase moves along, not a design choice a lab makes.

The concrete numbers are worth carrying: Nanbeige4.2-3B runs a **22-layer stack twice**, and its technical report
found **two passes optimal, retaining ~75% of token efficiency**, with more passes giving *"barely any gains."*
If extra latent passes were straightforwardly substituting for explicit reasoning tokens, one would expect the
benefit to continue; it does not. See [[Recursive Architectures]].

## Looped depth adds reasoning capacity specifically, and saturates where reasoning is not needed

[[Sebastian Raschka - GPT-6 Astra, Looped Transformers, and Hidden Reasoning]] supplies a mechanism for what latent computation buys, in place of the general claim
that more compute helps.

**"Beyond Parameters: Virtual Logic Depth"** (June 2025) reports that looping **leaves memorization
capacity nearly unchanged but improves multi-step math**. Latent depth is therefore not a substitute for
parameters; it is a different resource, and it is spent on computation rather than on storage.

**Geiping et al.** show where it saturates. Their 3.5B model, trained on 800B tokens with 4 shared blocks
sandwiched between 2 prelude and 2 coda blocks, randomised loop counts during training and an adaptive
KL-divergence stopping criterion at inference, exhibits a clean split: **HellaSwag levels off after about
8 loops, while GSM8K and HumanEval keep benefiting.** Tasks that need multi-step computation use the extra
depth; commonsense completion does not.

**The token-efficiency evidence is narrower than usually reported.** Astra does not use fewer tokens than
GPT-5.6 Sol overall, only at fixed accuracy. And the counterexample that breaks the inference from token
count to hidden reasoning: **GPT-5.6 Luna uses about 80% more tokens than Sol at similar performance**,
and nobody concludes that Sol is therefore less interpretable than Luna.

A negative result worth keeping: the **full-bandwidth transformer** (August 2026) uses latent feedback to
shorten MATH500 traces in a 1B base model, "but the effect disappears after instruction tuning" — latent
computation displacing visible reasoning is not yet a stable phenomenon.

## Energy optimization is not simply another recurrent forward pass

[[ByteByteGo - How to Build Models Without Language]] illustrates optimizing continuous
candidate or latent states against a learned energy function while weights remain fixed.
This separates the learned score, the search procedure, and the final constraint check.
It is a different mechanism from merely reusing Transformer layers.

Low energy or local convergence does not prove a valid decoded answer. The article's generic
walkthrough is also explicitly not Kona's implementation. [[Energy-Based Model]] keeps the
reported vendor Sudoku demonstration distinct from a universal reasoning advantage or a claim
that language models cannot use search and checkers.

## Sharing hidden state is a communication optimization

[[Ben Dickson - Cross-Model KV Cache Handoffs]] describes calibrated session conversion and
trained C2C fusion. The first avoids receiver session re-prefill; the second retains both
initial prefills and avoids intermediate text-message generation and reprocessing.
Neither makes caches universally interchangeable.

These are adjacent to latent reasoning, not proof that every hidden-state transfer performs
better search. Reported C2C gains depend on the tested models and tasks, and its exploratory
text-plus-fusion result suggests that readable messages and representations may complement
one another. Latent communication does not inherently carry an inspectable explanation,
provenance, or authority contract.

## Related pages

- [[ByteByteGo - How to Build Models Without Language]]
- [[Ben Dickson - Cross-Model KV Cache Handoffs]]
- [[Energy-Based Model]]

- [[Recursive Architectures]]
- [[Agentic Loop]]
- [[Reinforcement Learning]]
- [[Reasoning Compression]]
- [[On-Device Reasoning]]
- [[Training Large Reasoning Models Efficiently via Progressive Thought Encoding]]
- [[ReasonCACHE - Teaching LLMs To Reason Without Weight Updates]]
- [[LLM Reasoning]]
- [[Test-Time Scaling]]
- [[Akhil Arora et al - Current Advances in LLM Reasoning]]
- [[Alpha Signal - The Return of Recursion]]
- [[Sebastian Raschka - OpenAI Astra and Looped Transformers]]
- [[Chain-of-Thought Monitoring]]
- [[Sebastian Raschka]]
- [[Sebastian Raschka - GPT-6 Astra, Looped Transformers, and Hidden Reasoning]]
