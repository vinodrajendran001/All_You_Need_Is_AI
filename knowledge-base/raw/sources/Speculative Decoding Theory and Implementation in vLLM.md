---
title: "Speculative Decoding: Theory and Implementation in vLLM"
source: "https://vizuara.substack.com/p/speculative-decoding-theory-and-implementation?utm_source=post-email-title&publication_id=3466476&post_id=205325757&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[Mayank Pratap Singh]]"
published: 2026-07-06
created: 2026-07-06
description: "From why LLM generation is slow to a working EAGLE3 implementation in vLLM: the theory, the economics, the method families, and an honest benchmark where speculation did not pay off"
tags:
  - "clippings"
---
![](https://substackcdn.com/image/fetch/$s_!EyEo!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fadc64081-e1b4-4828-ae80-f61f5197154d_960x540.gif)

Large language models are slow when they generate text, and the reason catches most people off guard. It is not that the math is hard. The problem is that the model has to read its entire multi-hundred-gigabyte brain out of memory once for every single word, and it cannot start the next word until the current one is finished. Speculative decoding is the trick that breaks this one-word-at-a-time barrier, and it does so without changing the model’s output at all.

This post builds the idea up from the ground, then puts it into production. I start with why generation is slow, work out the core “guess-and-verify” mechanism, prove it is mathematically exact, dig into the economics that decide how much speedup you actually get, walk the method families (n-gram lookup, Medusa, EAGLE), and finish *by actually deploying EAGLE3 on vLLM* and reading the speedup off a real GPU.

## Table of Contents

**1\. Why generation is slow**

**2\. The core idea: draft, then verify**

**3\. Why it’s exact: the correctness guarantee**

**4\. The economics: alpha, tau, and K**

**5\. System realities and limitations**

**6\. The landscape of methods**

**7\. Putting it in production: EAGLE3 on vLLM**

**8\. Takeaways**

**9\. What I didn’t cover**

Code Repo

[https://github.com/Mayankpratapsingh022/LLM-Inference-Playbook](https://github.com/Mayankpratapsingh022/LLM-Inference-Playbook)

> Speculative decoding makes a large model generate **2–3× faster** while producing the **exact same text** it would have written anyway. It is close to a free lunch, paid for with spare compute the GPU was already wasting, but it is a **bet**, and Section 7 shows a real run where it did not pay off.

## 1\. Why generation is slow

## 1.1 Generation happens one token at a time

An LLM generates text **autoregressively**: it predicts one token, appends it to the input, and runs the whole model again for the next one. There is no shortcut here. Each new word literally depends on the one before it.

![](https://substackcdn.com/image/fetch/$s_!yr4V!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3606a4a5-6e0c-4919-81ab-daf712811632_1476x1085.png)

*Figure 1: In autoregressive decoding, the large model predicts only the next word, which is then appended to the context. The model runs again to predict the subsequent word, and this process repeats many times to generate the complete sequence.*

Notice what this costs. To produce the phrase “a small red,” the giant model runs **three separate times**. To write a 500-token answer, it runs 500 times, strictly in order. Every run is a full forward pass through every layer of the network.

## 1.2 Training is parallel, inference is sequential

This sequential bottleneck is unique to *generation*. During training, the model already knows the whole target sentence, so it can score every position at once in a single parallel forward pass. During inference, the future words do not exist yet, so the model is stuck in a step-by-step loop.

![](https://substackcdn.com/image/fetch/$s_!QSX-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F39dedb1d-103d-4d87-9e03-eaa72ebf617f_1515x1698.png)

*Figure 2: A comparison of Transformer processing modes during training and inference. During training (Panel A), the full sentence is known, enabling the model to score multiple positions simultaneously in a single parallel forward pass. In contrast, during inference (Panel B), future words are missing, forcing the system into a sequential, step-by-step generation loop where each new token must be predicted one at a time.*

The transformer is perfectly capable of massive parallelism. We just cannot use it at generation time, because we are missing the very thing we are trying to produce.

## 1.3 The autoregressive barrier

Here is another way to see the problem. At any moment, the model has a valid **KV cache** for everything it has already written (the past), and a complete **blind spot** for everything it has not (the future). It can generate exactly one token to push the boundary forward, and only then can it look one step further.

![](https://substackcdn.com/image/fetch/$s_!udPe!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a58e778-dee3-4092-8981-d7b624b0ccd3_1443x667.png)

*Figure 3: An illustration of the autoregressive barrier during LLM inference. Because the model cannot see future words, it uses past context to actively generate the immediate next token, and must complete this step before moving to the next slot. Speculative decoding attempts to bypass this strict sequential bottleneck by filling the future unknown slots with rapid guesses.*

That last sentence is the whole thesis of this post in one line:

what if we could fill those blind-spot slots with cheap guesses, and then check them all at once?

## 1.4 The real culprit is memory bandwidth, not compute

Here is the part that trips people up. Each generation step is slow not because the GPU is busy doing math. It is slow because the GPU has to physically stream the model’s *entire* set of weights, every single parameter, out of high-bandwidth memory (HBM) and into the compute cores, and it does this for every token it produces.

![](https://substackcdn.com/image/fetch/$s_!yQ4f!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b2ff9f8-d482-44a4-af04-47b81b8dfd87_1599x2176.png)

*Figure 4: Key system observations highlight the inefficiencies of autoregressive decoding, noting that every new word necessitates another full pass through the large model. Because the same massive weights are repeatedly loaded, each additional word incurs another computationally expensive step, ultimately causing long answers to generate slowly.*

For a 70B-parameter model, that is roughly **140 GB read from memory per token**. Three tokens means moving **420 GB**. The arithmetic units, meanwhile, sit mostly idle. They finish long before the next batch of weights even shows up. This is what people mean when they say generation is **memory-bandwidth bound**.

This one fact is the foundation of everything that follows:

*Generation is **memory-bound**, not compute-bound. The GPU's math units sit starving while they wait on weights. That means there is **spare compute to burn**, if only we could feed it more tokens at once.*

And we can feed it more tokens at once. Remember Figure 4, Panel A: verifying many tokens in parallel costs almost the same as generating a single one, because either way you pay to load the weights exactly once. That asymmetry, where one weight-load can check many tokens, is the gap speculative decoding pries open.

## 2\. The core idea: draft, then verify

## 2.1 A small model guesses, a large model checks

Speculative decoding adds a second, much smaller **draft model** (*M <sub>q</sub>*) alongside the big **target model** (*M <sub>p</sub>*). The draft model is cheap to run, so it can rattle off several guesses for the next few tokens very quickly. The target model then verifies all of those guesses in a single parallel pass, the same pass that in normal decoding would have produced just one token.

![](https://substackcdn.com/image/fetch/$s_!zZ7q!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F409b5223-a049-434c-ae3d-b6d5676fd272_1416x1475.png)

*Figure 5: In the speculative decoding pipeline, a small model (*M <sub>q</sub>*) rapidly guesses future tokens while a large model (*M <sub>p</sub>*) verifies those guesses in parallel. Correct guesses are committed to the KV Cache, and rejected ones are corrected to preserve* M <sub>p</sub> *'s exact distribution.*

The draft model produces *K* candidate tokens in roughly *4×T <sub>fast</sub>* (its drafting latency). Then the target model spends one expensive pass, *T <sub>slow</sub>*, confirming the whole batch instead of producing a single token. When the guesses are good, you get several tokens for the price of one big step.

## 2.2 Verification accepts a prefix, then corrects

How does verification decide what to keep? The target model scores the drafted sequence left to right and accepts tokens **until the first mismatch**. Everything before the mismatch is committed. The mismatched token is replaced with the target model’s own correct token. Everything after it is thrown away.

![](https://substackcdn.com/image/fetch/$s_!1Bqf!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc41c6f1e-5f11-4671-bda8-8647a14ef6f6_1512x816.png)

*Figure 6: The token verification process. The target model evaluates the drafted sequence sequentially from left to right. It successfully verifies and accepts "a" and "small". However, upon rejecting the token "blue", all subsequent guesses in the drafted sequence are automatically discarded.*

This "first mismatch wins" rule is what keeps the output identical to plain decoding. The moment a guess strays from what the big model would have said, we stop trusting the draft and hand control back to the target. And notice the worst case: even if every single guess is wrong, the verification pass still hands back one correct token (the corrected one), so we never do worse than plain autoregressive decoding.

## 2.3 The speedup, in numbers

Let me put concrete costs on it. Say one big-model pass costs 100 units and one draft pass costs 10.

Standard decoding of five tokens is five serial big passes: 5×100=500

![](https://substackcdn.com/image/fetch/$s_!1vOv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7efa7626-663d-42e4-8975-f3224f2fc40a_1646x1825.png)

*Figure 7: Cost comparison and best-case performance of speculative decoding versus standard autoregressive decoding. Standard decoding requires paying for five large, sequential passes to generate five tokens, resulting in a baseline cost of 500. Conversely, speculative decoding employs a computationally cheap draft model to guess five words simultaneously. In an ideal scenario where the draft model guesses all words correctly, the target model verifies the entire block once in parallel, which reduces the total operational cost from 500 to 150.*

In the best case, speculative decoding pays for five cheap draft guesses plus one verification pass: (5×10)+100=150. Same five tokens, less than a third of the cost. The catch, which the rest of this post is really about, is that this best case only shows up when the draft model guesses well. How often it does is the whole game.

## 3\. Why it’s exact: the correctness guarantee

The most important property of speculative decoding is that it is **not an approximation**. The text you get out is drawn from *exactly* the same probability distribution as if the target model had generated every token itself. This is what separates it from lossy tricks like just using a smaller model directly.

The mechanism is a clever twist on **rejection sampling**, introduced for this setting by **[Leviathan et al. (2023)](https://arxiv.org/abs/2211.17192)** and **[Chen et al. (2023)](https://arxiv.org/abs/2302.01318)**. Let *q(x)* be the draft model’s probability for a proposed token *x*, and *p* (*x*) the target model’s probability for that same token. We accept the draft token with probability:

$$
p_{\text{accept}} = min \left(1 , \frac{p \left(x\right)}{q \left(x\right)}\right)
$$

Read it intuitively. If the target likes the token at least as much as the draft did (p≥q), we keep it outright. If the target likes it less, we keep it only proportionally, and sometimes reject it, so we do not over-represent tokens the draft was too eager about.

When a token *is* rejected, we do not just resample blindly. We sample the replacement from the **normalized residual distribution**, which fills in exactly the probability mass the acceptance step left out:

Together, the accept rule and the residual-resample rule provably rebuild the target distribution *p*, token for token. The draft model only ever affects speed. It never affects what actually gets written.

*The draft model is a **guesser, not a decider**. Rejection sampling guarantees the final text matches the target model's distribution exactly. A wrong guess costs you time, never correctness.*

## 4\. The economics: alpha, tau, and K

Speculative decoding is only as good as its guesses. Three quantities decide how much real speedup you see: the **acceptance rate** *α*, the **expected accepted tokens per round** *τ*, and the **lookahead budget** *K*.

## 4.1 Alpha (α): how often guesses are accepted

**Alpha** is the probability that any given drafted token survives verification. It is the single most important efficiency number, because rejected tokens are wasted work.

![](https://substackcdn.com/image/fetch/$s_!hduJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd8d28e0-244f-49c6-ae25-f7e563be3026_1422x984.png)

Figure 8: The Role of Alpha (α) in Speculative Execution. Alpha serves as the fundamental efficiency metric in speculative decoding, quantifying the rate at which the target model accepts drafted tokens. High α values indicate strong distribution alignment and yield significant inference acceleration. Conversely, low α values reflect computational waste, as misaligned draft tokens trigger early rejections and serial fallbacks.

When *α* is high, the draft and target models "think alike," long runs of guesses get accepted, and you approach that ideal 150-cost case. When *α* is low, you reject early and often, and most of your drafting effort goes in the bin.

## 4.2 Tau (τ): expected tokens per verification

So how many tokens do you actually commit per round, on average? If each of the *K* drafted tokens is independently accepted with probability *α*, the expected number of accepted tokens per round is a geometric series:

$$
\tau = \frac{1 - \alpha^{K + 1}}{1 - \alpha}
$$

![](https://substackcdn.com/image/fetch/$s_!tIYX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6e98c7d-3835-42e4-9a3c-45d92f8e2bbb_1659x834.png)

*Figure 9: With K=5 as the lookahead budget for the number of draft tokens proposed during each validation step, the variable α defines the independent probability that a draft token matches the target distribution, which determines τ, the estimated average of accepted tokens per round. Achieving a larger τ is beneficial because it reduces the frequency of costly target-model runs, directly lowering system latency.*

The numbers tell the story. A weak drafter (*α* =0.30) commits only about 1.43 tokens per expensive pass, barely better than plain decoding. A strong drafter (*α* =0.85) commits about 4.15 tokens per pass, and that is where the real speedups come from. Acceptance compounds across slots, which is why the bars decay from left to right. To get slot 5 right, slots 1 through 4 all have to be right first.

## 4.3 Lookahead K (γ): how far to guess

*K* (sometimes written *γ*) is how many tokens the draft model proposes before each verification. It is a balance, not a “bigger is better” dial.

![](https://substackcdn.com/image/fetch/$s_!p3rP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27e6ad31-62a3-495f-a676-66b60a95d41a_1665x780.png)

*Figure 10: The parameter K determines the number of tokens drafted per step. A value too small limits speedup, while a value too large wastes compute on discarded tokens. To maximize efficiency, optimal systems dynamically tune K based on the token acceptance rate.*

If *K* is too small, you verify too often and leave easy speedup unclaimed. If *K* is too large, you draft far past the first inevitable mismatch and burn compute on tokens you will only throw away. The sweet spot depends on *α*: confident drafters can afford a deeper lookahead.

## 4.4 Adaptive K: tune the lookahead to the text

Since the ideal *K* depends on how predictable the upcoming text is, good systems do not fix it. They use an **adaptive controller** that reads the local difficulty of the stream, usually through the entropy *H* (*x*) of the model’s distribution, and sets the lookahead to match.

$$
K_{\text{opt}} = clamp \left(\right. f \left(H \left(x\right)\right) , K_{min} , K_{max} \left.\right)
$$

![](https://substackcdn.com/image/fetch/$s_!wV6K!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99c1ed7b-9efc-4855-b644-cac7fbea1505_1224x687.png)

*Figure 11: Dynamic lookahead overcomes the limitations of a static K budget by adjusting draft length based on textual confidence, allowing farther drafts for easy text and shorter drafts for hard text, to minimize wasted compute and memory bandwidth.*

On boilerplate or highly predictable text ("in the logs we found a critical error in the system"), the controller drafts far ahead, because the guesses will mostly be accepted. On genuinely uncertain text ("therefore the proof…"), it drafts cautiously, because deep guessing would just produce garbage to discard.

## 5\. System realities and limitations

Speculative decoding looks like a clean win on paper. In a real serving system it comes with sharp edges worth knowing about before you reach for it.

## 5.1 The two models run in lockstep

The draft and target models do not work at the same time. They take turns. While the draft model is busy proposing, the expensive target model sits **idle**. While the target verifies, the draft model sits **idle**.

![](https://substackcdn.com/image/fetch/$s_!IZAh!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcabe059d-af89-43f3-9d87-cf024b6aa12e_1509x675.png)

*Figure 12: Speculative decoding's sequential workflow. In Phase 1, the large, expensive target model sits idle while the draft model generates its guesses one by one. In Phase 2, the bigger issue, drafting stops entirely while the draft model waits for the slow target model to finish its verification.*

This back-and-forth is why naive implementations sometimes fall short of their theoretical speedup. There is real "bubble" time where one of the two models is doing nothing at all.

## 5.2 It only helps when the GPU has spare compute

Remember that the whole trick leans on **spare compute** (Section 1.4). That spare capacity exists at low batch sizes, when one or a few requests leave the GPU’s math units idle. At high batch sizes, many requests already saturate the GPU, and speculation’s extra drafting work just *steals* memory bandwidth away from useful generation.

![](https://substackcdn.com/image/fetch/$s_!RAn-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef1188e6-ab3b-4092-8359-c51476c4bda2_1626x953.png)

*Figure 13: Because speculative decoding only reduces latency when GPUs have spare compute, and actively steals memory bandwidth under high load, modern serving engines dynamically toggle the feature based on real-time queue depth to maximize overall system throughput.*

This is why production serving stacks treat speculation as a **latency optimization for light load**, switching it off automatically when the queue fills up and the system flips into throughput-maximizing mode.

## 5.3 Limitation 1: the tokenizers must match

Because verification compares the draft’s token against the target’s token, both models have to speak the **exact same vocabulary**. A draft model that splits “active” into `[act]` and `[-ive]` cannot be checked against a target that emits a single `[active]` token. The two sequences would never line up.

![](https://substackcdn.com/image/fetch/$s_!K1IW!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbc8cf55-c328-4a02-8bff-24f15f5308fb_864x456.png)

*Figure 14: Limitation 1, tokenizer identity. The draft and target models must share an identical tokenizer and vocabulary; otherwise their token sequences cannot be aligned during verification.*

In practice this means your draft model is usually a smaller member of the *same model family* as the target (say, a 7B drafting for a 70B with a shared tokenizer), which limits your options.

## 5.4 Limitation 2: you pay for a second model in VRAM

Speculative decoding puts two models on the GPU at once. The draft model is small, but it is not free, and the memory it takes up is memory you cannot hand to the KV cache or to bigger batches.

![](https://substackcdn.com/image/fetch/$s_!dUQC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6bf4b1d-253e-4718-a838-0b2acb490c60_723x408.png)

*Figure 15: Limitation 2, dual-model VRAM overhead. Co-locating both models in VRAM (for example ~14 GB for a 7B draft plus ~140 GB for a 70B target) severely reduces the capacity left for KV caches and high batch sizes.*

## 5.5 Limitation 3: rejection triggers a serial fallback

When a drafted token is rejected, every guess after it gets discarded and the system falls back to generating that step the slow way. On hard text, rejections come often, so you keep re-drafting and re-verifying, and the speedup for that step evaporates.

![](https://substackcdn.com/image/fetch/$s_!AJpv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdeec9c1d-cfe5-4350-bce4-0d499fa58c8a_1080x711.png)

*Figure 16: Limitation 3, distribution alignment and the rejection loop. When the draft and target distributions diverge, proposals get rejected and discarded, and the system falls back to a serial re-drafting loop that erases the speedup for that step.*

All three limitations point back to the same truth: speculative decoding is a **bet**. It pays off handsomely when the draft is well-aligned and the GPU has room to spare, and it quietly costs you when those conditions fail.

## 6\. The landscape of methods

“Speculative decoding” is now a *family* of techniques, not a single algorithm. They differ mainly in **where the draft tokens come from**.

![](https://substackcdn.com/image/fetch/$s_!tdei!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9630af9c-d9d7-4f13-866f-7b5eec598153_1596x963.png)

*Figure 17: A timeline of speculative decoding methods, including the separate vanilla draft model, model-free n-gram lookup, and single-model multi-head drafting (Medusa).*

I will focus on the three most foundational and widely used approaches:

1. **Vanilla draft-target** (Section 2): two separate models, where the draft proposes and the target verifies. This is the classic formulation.
2. **N-gram prompt lookup** (6.1): no draft model at all. The drafts are copied from repeated text in the prompt.
3. **Medusa** (6.2): a single model grows extra heads that predict several future tokens at once.

The figure also shows **Eagle** (feature-level tree drafting), **self-speculation** (drafting by skipping the target's own middle layers), and **streaming overlap** (pipelining draft and verify). I introduce the core idea behind **EAGLE** in 6.3, because it is the method that now dominates production serving; its tree-based refinements (EAGLE-2/EAGLE-3), self-speculation, and streaming overlap are more advanced and belong to a future post.

## 6.1 Deep dive: n-gram prompt lookup

The simplest drafter is **no model at all**. In a lot of real tasks (summarization, document Q&A, code editing, retrieval-augmented generation) the output copies long spans verbatim from the input. **[Prompt Lookup Decoding](https://github.com/apoorvumang/prompt-lookup-decoding)** (Saxena, 2023) takes advantage of this directly.

![](https://substackcdn.com/image/fetch/$s_!lUh0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F87070b82-9610-426f-b7d1-3f042644464d_1578x1179.png)

*Figure 18: N-gram prompt lookup. Instead of a neural drafter, the system scans the past context for a repeat of the most recent n-gram suffix and proposes the tokens that followed it last time. The target model verifies these guesses in a single pass. This is model-free and adds zero VRAM, but its hit rate falls on creative, non-repetitive text.*

The mechanism is just **string matching**:

1. Take the last few generated tokens (the active n-gram suffix, say `if key in`).
2. **Scan backward** through the prompt and prior output for an earlier occurrence of that same n-gram.
3. If you find one, propose the tokens that followed it last time (`cache: return`) as the draft.
4. Verify those proposals with the target model exactly as before.

Because no neural network is involved in drafting, this approach uses **zero extra VRAM**, which sidesteps Limitation 2 completely, and it works with any decoder model out of the box. The trade-off is that its hit rate is only as good as the repetition in your text. It shines on structured, input-grounded generation (2–4× speedups are common) and does almost nothing for open-ended creative writing.

## 6.2 Deep dive: Medusa

**[Medusa](https://arxiv.org/abs/2401.10774)** (Cai et al., 2024) takes a different route. Instead of a *separate* draft model, it bolts **extra decoding heads** onto the target model itself. One backbone pass produces several future-token predictions at once, and they all get verified together. No second model, no separate tokenizer to babysit.

### Multiple heads predict multiple positions

A normal LLM has one “LM head” that predicts the very next token (position +1). Medusa adds extra heads on top: head 1 predicts position +2, head 2 predicts +3, head 3 predicts +4. All of them read from the **same backbone hidden state**, computed in a single forward pass.

![](https://substackcdn.com/image/fetch/$s_!_5gP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf99fac2-7b93-4d11-928c-0ff1f5957cfb_1044x549.png)

*Figure 19: Medusa augments a model with extra decoding heads. After the backbone runs once, the original LM head predicts the next position while each added Medusa head predicts a position further out, and each head keeps its top-2 candidates.*

Because each head keeps its **top-2** candidates, the heads together describe many possible continuations, not just one. That branching is handled by a tree.

### Tree attention verifies many candidates at once

With each head offering 2 candidates, the continuations form a small **tree**. Two heads give 2×2=4 candidate paths, and a third head would give 8. Medusa packs all these paths into a single sequence and uses a specially shaped **tree attention mask**, so each candidate token only attends to its own ancestors. The branches stay logically separate even though they ride through one shared forward pass.

![](https://substackcdn.com/image/fetch/$s_!gUbr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0dcf598d-612b-4580-9b74-7953cf40101c_1464x627.png)

*Figure 20: Medusa’s candidate tree and tree-attention mask. The top-2 outputs of each head combine into multiple candidate paths (top-2 × top-2 = 4, or 8 with a third head). The attention mask ensures each row attends only to its ancestors and itself, so independent branches do not contaminate each other.*

Here is the payoff. All of these candidate paths get checked in **one backbone pass**. The target verifies the whole tree at once and commits the longest path that survives, and that committed path immediately seeds the next tree.

![](https://substackcdn.com/image/fetch/$s_!LX_Y!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c792ad8-f667-420a-984b-95e6641194a5_744x633.png)

*Figure 21: A single backbone pass with tree attention verifies every candidate path at once. Here the path "returned · the · cached" is accepted, 3 tokens committed in one pass, and it seeds the next round's tree.*

### Two training recipes: Medusa-1 vs Medusa-2

How you train those heads decides the trade-off between quality and speed.

![](https://substackcdn.com/image/fetch/$s_!5jaT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c114036-114c-4a1c-9782-370a5790af60_1587x1197.png)

*Figure 22: Medusa's two training procedures. In Medusa-1 the backbone is frozen and only the heads are trained, so accepted tokens match the original model exactly (lossless). In Medusa-2 the backbone is fine-tuned alongside the heads using a careful recipe (a combined loss, split learning rates, and warming up the heads first), which yields more accurate heads and higher speedup while keeping quality intact.*

- **Medusa-1** freezes the backbone and trains only the heads. Since the backbone is never touched, the verified output is **lossless**, identical to the original model. It is cheap to train (one GPU) and a safe default.
- **Medusa-2** fine-tunes the backbone and heads together. This makes the heads more accurate, so more tokens are accepted per step, but it risks degrading the base model, which is why it needs the careful recipe shown above.

The lever that connects training to speed is simple:

**better heads → more tokens accepted per step → higher speedup**.

![](https://substackcdn.com/image/fetch/$s_!6RIV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22adaf3e-11d7-4e63-8010-0a3e3b4d111d_1560x1206.png)

*Figure 23: Why Medusa-2 is faster comes down to one lever, head accuracy. More accurate heads get more tokens accepted, which means more tokens per step and higher speedup. Numbers from Cai et al. (2024), Vicuna-7B on MT-Bench, both variants trained on the same ShareGPT data for 2 epochs.*

## 6.3 EAGLE: drafting features, not tokens

Everything so far, vanilla draft-target, n-gram lookup, Medusa, shares one habit: the drafter guesses **raw tokens**, and verification compares those exact tokens against the target’s. That is fine on predictable text. It falls apart exactly where language is hardest.

### Why token-level guessing stalls

Recall from Section 4 that speedup lives and dies by the acceptance rate *α*. The trouble is that *α* is not a constant, it collapses in **high-entropy** contexts, the moments where many different next tokens are all reasonable.

![](https://substackcdn.com/image/fetch/$s_!hsbC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8027f409-cefb-4a43-92b4-084555170b94_1578x792.png)

*Figure 24: In a high-entropy context, several next tokens are plausible at once. The target's distribution p favours "the" while the smaller draft's q favours "a". Because verification accepts only up to the first token-level mismatch, this single disagreement rejects the draft early and cuts the accepted prefix short.*

Look at what happens. The target model spreads its probability *p* across `returned`, `caused`, `the`, and more, landing on **"the"**. The little draft model, working with a coarser view of the world, puts its mass *q* on **"a"**. Neither is "wrong", both are grammatical, but the *exact-token* verifier does not care about that. The first token-level mismatch ends the accepted run right there.

The cost compounds through the same geometry seen in Section 4. If entropy pushes per-token acceptance down to, say, α=0.4, then with a lookahead of *K* =5:

$$
\tau = \frac{1 - \alpha^{K + 1}}{1 - \alpha} = \frac{1 - 0.4^{6}}{1 - 0.4} \approx 1.66
$$

Barely more than one token committed per expensive verification pass. **The more the draft's distribution diverges from the target's, the shorter the accepted prefix, and the smaller the real speedup.** Guessing the *exact word* is simply too brittle a target when many words are plausible.

### EAGLE’s fix: predict the feature, not the word

**[EAGLE](https://github.com/SafeAILab/EAGLE)** (Li et al.) makes one deceptively simple change. Instead of training the drafter to predict the next **token**, it trains a lightweight module to predict the target model’s next **feature**, the hidden state from the layer just below the LM head. Features are continuous, smooth, and far more predictable than the discrete lottery of exact tokens, so the drafter agrees with the target much more often.

![](https://substackcdn.com/image/fetch/$s_!c3lG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbd4d33c-efe7-4fc8-b484-00538a028525_1659x1137.png)

*Figure 25: EAGLE drafts at the feature level. It takes the target's own hidden feature (Layer N−1 output) plus the embedding of the token that actually followed, concatenates them, and runs a tiny autoregressive head (one FC layer + one decoder layer) to predict the next feature. That predicted feature loops back in as the next input, and is also decoded to a draft token through the frozen target LM head. The target model itself is never modified.*

Read the pipeline left to right:

1. **Reuse the target’s features (left).** The target model is **frozen**. EAGLE taps the hidden state from its second-to-last layer, the “feature” that summarises everything the model knows right after the word `is`. Nothing about the big model changes.
2. **Anchor each guess with the real next word (middle).** EAGLE feeds the drafter the feature *and* the embedding of the token that actually came next (`is` → `blue`). That next word is what tells the drafter **which branch of reality actually happened** (`blue`, not `falling`), so its predictions stay grounded instead of drifting.
3. **Autoregress on features (right).** A tiny head, one fully-connected layer plus a single decoder layer, takes the concatenation \[featis; emb(blue)\] and predicts the **next feature**. That predicted feature loops straight back in as the input for the following step (this is the autoregressive part), and in parallel it is pushed through the **frozen target LM head** to read off an actual draft token (`today`).

Because the drafter learned to imitate the target's own internal trajectory, its proposals line up with what the target would have produced, so acceptance climbs and *τ* with it. And crucially, since draft tokens are still decoded through the target's real LM head and verified the usual way, EAGLE keeps the **exactness guarantee** from Section 3 intact. The feature trick buys speed, never correctness.

*EAGLE stops guessing the **exact word** and starts predicting the target's own **internal feature**. Smoother targets are easier to hit, so acceptance α rises, and α is the very quantity that governs speedup.*

> **From theory to deployment. EAGLE's descendant, EAGLE3, is exactly what I deploy in Section 7 of this post, on a real Llama-3.1-8B with vLLM. If you want the flags, benchmarks, and measured numbers, jump to 7.**

## 6.4 The production reality: where the speedup goes

The clean 1150-vs-500 arithmetic from Section 2 is the *theoretical* story. On a real serving stack, two things bend those numbers: fixed per-step **system overheads**, and the **batch size** the GPU is running at. This section is the honest accounting.

### Ideal vs measured: the system tax

Even in the friendliest case, a single request at batch 1 with every drafted token accepted, you do not get the speedup the token math promises. Real engines pay fixed costs the idealized picture ignores.

![](https://substackcdn.com/image/fetch/$s_!EfHv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb39dde8-4c20-4259-8700-514430242ad8_1662x846.png)

*Figure 26: The gap between the paper speedup and the measured one, at batch 1. The theoretical ideal (left) accepts all four drafted tokens for a 2.5× win. The production timeline (right) inserts real per-step costs, kernel-launch overhead and KV-cache lookups, that the token arithmetic never counted, dragging the effective speedup down to roughly 1.8×. (Illustrative numbers.)*

The extra blocks on the right, kernel-launch overhead and KV-cache lookup, are the "system tax." They are largely **fixed per step**, so they do not shrink just because your draft was good. A 2.5× algorithm becomes a 1.8× system. This is why a speedup you can *prove* on your own hardware is worth more than any number on a slide.

*The token math sets the **ceiling**. Fixed per-step overheads, kernel launches, cache lookups, scheduling, set the **floor**. The speedup you actually ship lives in between, and only a benchmark tells you where.*

### Batch size decides everything

Section 5.2 made the claim that speculation only helps when the GPU has spare compute. Here is the mechanism, drawn out across the two regimes.

![](https://substackcdn.com/image/fetch/$s_!MRvq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fddfa4dc1-b9a7-4c8b-9f17-12d9218fd859_1617x933.png)

*Figure 27: The same speculative machinery in two regimes. At batch 1 (latency-bound) the GPU is mostly idle, so the draft model's extra work hides inside that idle time and verification is nearly free, this is where speculation shines. At batch 128 (throughput-bound) the GPU is already saturated, drafting kernels serialize and compete for bandwidth, and the step is held hostage by its slowest request (the straggler effect), leaving effective speedup somewhere between −5% and +10%.*

The two lanes could not be more different:

- **Lane 1, batch 1 (latency-bound).** The compute engine sits mostly idle waiting on memory. Drafting slots into that idle time for free, and verification overlaps without adding wall-clock. Spare compute is exactly the currency speculation spends, and here it is abundant.
- **Lane 2, batch 128 (throughput-bound).** Now 128 requests already saturate compute and memory bandwidth. Every extra drafting kernel is no longer free, it *serializes* and steals bandwidth from useful generation. Worse, a batched step only finishes when its **slowest** member finishes, so one request that rejects and re-drafts (the **straggler**) stalls the whole batch. Net effect: anywhere from a small loss to a modest gain.

This is precisely why production stacks toggle speculation **on at light load and off under saturation**, the dynamic switch introduced in Section 5.2.

### Following one decoding step’s clock

One more view makes the batch-size story concrete: take a single full decoding step, call it 100% of its wall-clock time, and watch how that time redistributes as the batch grows.

![](https://substackcdn.com/image/fetch/$s_!Y4o7!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F297cfb18-db7d-4703-9077-078d70ad9ab4_1650x1038.png)

*Figure 28: The composition of one decoding step's wall-clock time at three batch sizes. As the batch grows from 1 to 128, target verification's share climbs (52% → 63% → 74%) while the draft model's share shrinks (24% → 17% → 10%). (Illustrative numbers.)*

The trend is the whole point. At batch 1, the draft forward pass is a real slice of the step (24%), so making it cheap or making its guesses land pays off handsomely. By batch 128, verification dominates (74%) and drafting is a rounding error (10%). **As the batch grows, verification eats the step and the draft’s share collapses, so the headroom speculation can possibly recover shrinks right along with it.**

*Speculative decoding is fundamentally a **low-load latency optimization**. Its win is largest exactly where the GPU has idle compute to burn, and it fades as batching fills that idle time with real work.*

## 7\. Putting it in production: EAGLE3 on vLLM

Everything above was the idea. Now I run it. I deploy the method that won production, **EAGLE3**, on **vLLM**, serving **Llama-3.1-8B** on a single 48 GB GPU, and measure the speedup against a real baseline. Same model, same prompts, one flag flipped.

***This half is also a notebook. Every command below is a runnable cell in the companion vLLM notebook.***

Code Repo

[https://github.com/Mayankpratapsingh022/LLM-Inference-Playbook](https://github.com/Mayankpratapsingh022/LLM-Inference-Playbook)

***The subsection numbers (7.1, 7.4 and so on) match the notebook, so you can read a part here and run the same thing there. Spin up the pod from 7.2, upload the notebook into the pod's JupyterLab, and step through it cell by cell while you read along. I tried hard to make it as simple as it can possibly be: open it, run each cell, and read the numbers off.***

I use an 8B target on one affordable card so you can reproduce it for about a dollar. Fair warning, and it is the honest point of 7.7: on this small-model, single-GPU setup the speedup did **not** materialize, and that section explains exactly why.

## 7.1 What we are building

The experiment is deliberately simple to reason about:

- **Target model:** `meta-llama/Llama-3.1-8B-Instruct`.
- **Hardware:** a single 48 GB RunPod GPU (an A40, L40S, RTX 6000 Ada, or A6000). One card is plenty, see the memory note in 7.2.
- **Engine:** **vLLM**, the most widely deployed open inference server.
- **Method:** **EAGLE3**, the current state-of-the-art (7.3 explains why I don’t bother with the rest).
- **What we toggle:** a **baseline** run with plain autoregressive decoding, then the *same* model with **EAGLE3** turned on. That’s the whole A/B.
- **Workload:** chat traffic (ShareGPT-style), which is decode-heavy and the most common production shape.
- **What we measure:** output throughput, acceptance length, latency percentiles, and cost per million tokens.

## 7.2 Renting the server on RunPod

**[RunPod](https://www.runpod.io/)** rents GPU pods by the minute, which makes it ideal for a benchmark you will tear down afterward.

You can use any service, maybe [Massedcompute](https://massedcompute.com/) or my personal favourite [Modal](https://modal.com/).

Before you start the clock, here is roughly how long the whole experiment takes on a single 48 GB card, running baseline vs EAGLE3 on vLLM. **Plan for about 45 to 60 minutes end to end.** A single 48 GB GPU on RunPod runs about $0.40 to $0.90 per hour, so the whole run costs roughly **$1**.

![](https://substackcdn.com/image/fetch/$s_!nByC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd4b697e3-0b54-4d57-a2b1-41c5a9c43c11_2306x1269.png)

The weights download only once and live on the `/workspace` persistent volume, so if you come back later that day you skip the ~10-minute download. Your two biggest sources of variance are HuggingFace download speed and whether you benchmark at `--request-rate inf` (fast) or a finite rate (slower).

### A memory reality check (read this first)

Llama-3.1-8B in `bf16` is about **16 GB of weights**. Add the KV cache, activations, CUDA graphs, and the small EAGLE3 draft head (only a percent or two of the base model), and the whole thing still sits well under **48 GB**. That means one card does the job, with no tensor parallelism and no quantization to fuss over.

Any of these single 48 GB GPUs on RunPod work:

- **A40 (48 GB)** is the cheapest option and the one this guide assumes by default.
- **L40S, RTX 6000 Ada, or A6000 (48 GB)** all work too and are a bit faster; pick whichever is available and affordable.

*8B in* `bf16` *is a **single-GPU** job. One 48 GB card holds the weights, the KV cache, and the EAGLE3 head at once, so every command below uses* `-tp 1` *and no quantization.*

The commands in this guide all use `-tp 1` (a single card). If you happen to be on a smaller 24 GB GPU like a 4090 or L4, add `--quantization fp8` to fit, at a small quality cost.

### Spin up the pod

![](https://substackcdn.com/image/fetch/$s_!nBMR!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0bbfd973-1197-4d07-a7e1-5c27d9392920_1000x563.gif)

*RunPod pod configuration. Pick a single 48 GB card (A40 by default, or L40S / RTX 6000 Ada / A6000) with the GPU count set to 1. Then choose a recent CUDA/PyTorch template, a large enough container disk, a persistent volume for the model weights, and an exposed HTTP port for the inference server.*

1. In the RunPod console, go to **Pods → Deploy**, select a **48 GB GPU** (an **A40** by default, or an L40S / RTX 6000 Ada / A6000), and leave the GPU count at **1**. As the memory check above explains, 8B fits on one card, so there is no tensor parallelism to set up.
2. Choose a recent **PyTorch / CUDA** template (or a vLLM template from the RunPod Hub).
3. Give it a **persistent volume** of ~60 GB mounted at `/workspace` so the 8B weights survive a restart, and set container disk to ~40 GB.
4. Under **Expose HTTP Ports**, add `8000` (vLLM’s default).
5. Deploy, then connect via the **web terminal** or **SSH**.

### One-time setup inside the pod

```markup
# Hugging Face access (Llama is a gated model, so accept the license on HF first)
pip install -U "huggingface_hub[cli]"
huggingface-cli login   # paste your HF token

# Keep all downloads on the persistent volume
export HF_HOME=/workspace/hf
mkdir -p "$HF_HOME"
```

Now you are ready to install an engine and serve the model.

## 7.3 Why EAGLE3 is the one to deploy

The theory above introduced a whole family of speculative decoding methods. In production today, **EAGLE3** is the default choice, and the others are mostly of historical or niche interest. Here is the honest comparison so you know *why* we are skipping them rather than just being told to.

![](https://substackcdn.com/image/fetch/$s_!so5_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9fef607c-efda-4b66-af44-43d9aed7cf50_2623x1175.png)

**EAGLE3** wins on every axis that matters in production. It reaches the **highest acceptance rates**, so you get the most tokens per verification pass. It costs almost **no extra VRAM**, because it’s a small head rather than a second model. It has **no tokenizer-matching problem**. And, best of all for our purposes, **pre-trained EAGLE3 heads are published** for popular targets including Llama-3.1-8B, so there is nothing to train. Reported speedups reach roughly **2.4×** on 8B (and up to **~4×** on larger models) without changing the output.

### What a “pre-trained EAGLE3 head” actually is

Every command in this guide points at two model names: the **target** I serve, and a **draft head**. It’s worth being clear about what that second name is, because it looks like a model but behaves very differently.

A draft head is a small checkpoint hosted on Hugging Face, named in the usual `owner/name` form.

Three things follow from that name, and they are the whole reason EAGLE3 is easy to deploy:

- **It is tiny, not a second model.** The head is only a percent or two of the target’s size. It’s the *guesser*, and the engine downloads it and bolts it onto the frozen target for you. That’s why speculation here costs almost no extra VRAM.
- **It is tied to one specific target.** An EAGLE3 head is trained against a single model and only works with that model, because it learned to predict *that* model’s internal features. `EAGLE3-LLaMA3.1-Instruct-8B` works with Llama-3.1-8B and nothing else. This is exactly why, when this guide moved from a 70B target to 8B, the draft head had to change too.
- **“Pre-trained” means you skip the hard part.** Someone already trained this head and published it, so you just reference it by name. If no head existed for your model, you would train one yourself (the **[EAGLE](https://github.com/SafeAILab/EAGLE)** repo has recipes), but for Llama-3.1-8B one already ships, so there is nothing to do but point at it.

*I deploy **exactly one technique: EAGLE3**. It is the current state of the art for production speculative decoding, and pre-trained heads exist for the model I'm using, so there is nothing to train.*

### The workflow I’ll follow

I deploy on vLLM (7.4) and follow one simple loop so the comparison is honest:

1. **Deploy the model** ***without*** **speculation** and benchmark it. This is your **reference**: the plain tokens/sec and latency of the model as-is. (7.4 to deploy, 7.6 to benchmark.)
2. **Re-deploy** ***with*** **EAGLE3** and run the *identical* benchmark. (7.4.)
3. **Compare.** The ratio of step-2 throughput to step-1 throughput is your speedup; the acceptance length tells you whether EAGLE3 is actually working. (7.7.)

*The golden rule of this whole page: **measure the baseline first.** A "2.5× speedup" only means something against a number you actually recorded on your hardware, with the same model, prompts, and benchmark.*

## 7.4 vLLM implementation

Install vLLM:

```markup
pip install -U vllm
```

vLLM enables speculation through a single `--speculative-config` JSON blob (offline, the equivalent `speculative_config={...}` dict). Everything else about serving stays the same.

### Baseline (no speculation)

This is the run every speedup is measured against. **Deploy it and benchmark it first** (7.6) before you touch EAGLE3.

```markup
VLLM_USE_V1=1 vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --seed 42 \
  -tp 1 \
  --gpu-memory-utilization 0.90
```

The server exposes an OpenAI-compatible API at

`http://localhost:8000/v1`.

### Turning on EAGLE3

Now the same model, same flags, plus one `--speculative-config`. EAGLE3 attaches a small draft head that reuses the target model’s internal features:

```markup
VLLM_USE_V1=1 vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --seed 42 \
  -tp 1 \
  --speculative-config '{"model": "yuhuili/EAGLE3-LLaMA3.1-Instruct-8B", "num_speculative_tokens": 3, "method": "eagle3"}'
```

Each field in that JSON maps to a speculative-decoding idea:

- `method: "eagle3"` picks the drafting algorithm. It tells vLLM the draft head predicts the target’s internal *features* instead of raw tokens (the EAGLE idea from 6.3), which is what pushes acceptance so high.
- `model` is the pre-trained EAGLE3 draft head, the small network that does the guessing. The target model is never touched.
- `num_speculative_tokens: 3` is how many tokens the head drafts ahead before the target verifies them. This is the lookahead `K` from 4, and it is the one dial you actually tune. Bigger is not automatically better: acceptance compounds, so each extra drafted token lands less often. Red Hat measured acceptance dropping off past two or three tokens on 8B (about 45% at 2 drafts, down to 28% at 4), so three is the sweet spot.

vLLM keeps this simple: you set how far to draft with this one number, and it sizes the draft tree (its depth, branching, and per-pass token budget) for you internally.

Two practical notes:

- On a single card there is nothing to shard, so the draft head runs alongside the target on the same GPU. On a multi-GPU box you would add `"draft_tensor_parallel_size": 1` to keep the tiny head on one card.
- An alternative draft checkpoint is `RedHatAI/Llama-3.1-8B-Instruct-speculator.eagle3`.

Benchmark this exactly as you benchmarked the baseline (7.6), then compare.

### Offline (Python) equivalent

If you would rather drive vLLM from Python instead of the server, the same config is a dict:

```markup
from vllm import LLM, SamplingParams

llm = LLM(
    model="meta-llama/Llama-3.1-8B-Instruct",
    tensor_parallel_size=1,
    speculative_config={
        "method": "eagle3",
        "model": "yuhuili/EAGLE3-LLaMA3.1-Instruct-8B",
        "num_speculative_tokens": 3,
    },
)

out = llm.generate(
    ["Explain speculative decoding in one paragraph."],
    SamplingParams(temperature=0, max_tokens=256),
)
print(out[0].outputs[0].text)
```

***On a smaller 24 GB card (a 4090 or L4), add*** `quantization="fp8"` ***(Python) or*** `--quantization fp8` ***(CLI) to fit;*** `-tp 1` ***stays the same.***

### Smoke test

Check the server is answering before you benchmark it:

```markup
import openai

client = openai.Client(base_url="http://127.0.0.1:8000/v1", api_key="None")
resp = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "List 3 countries and their capitals."}],
    temperature=0,
    max_tokens=64,
)
print(resp.choices[0].message.content)
```

If this returns sensible text, your server is up and you can benchmark it.

## 7.5 How to benchmark it honestly

A speedup number means nothing without saying *what* you measured. Four metrics tell the whole story.

- **Output throughput (tokens/sec).** The headline. How many tokens the system produces per second under load. This is where EAGLE3 shows up biggest.
- **Acceptance length,** ***τ*** **(and acceptance rate,** ***α*****).** From 4: *τ* is the average number of drafted tokens committed per verification pass, and *α* is the per-token acceptance probability. If *τ* is near 1, speculation is doing nothing; if it is 3–4, you are winning. **This is the single best diagnostic**, and vLLM reports it.
- **Latency: TTFT and TPOT/ITL.** *Time to first token* (TTFT) measures responsiveness; *time per output token* / *inter-token latency* (TPOT/ITL) measures how fast the stream flows. Report p50 and a tail percentile (vLLM prints p99).
- **Cost per 1M tokens.** The business case. Derived from throughput and the pod’s hourly price:

$$
\text{cost per 1M tokens} = \frac{\left(\text{pod }\$/\text{hr}\right) \times 10^{6}}{\left(\text{tokens}/\text{sec}\right) \times 3600}
$$

**Why chat?** Chat is *decode-heavy*: short prompts, long answers. That is exactly the regime where generation is memory-bound and speculation has spare compute to exploit. On prefill-heavy workloads (huge unique prompts, short answers) the win shrinks.

## 7.6 Running the benchmark

vLLM ships its own load generator. Run the **baseline first**, record the numbers, then re-launch the server with EAGLE3 and re-run the *identical* benchmark command.

### The load test

Grab the ShareGPT dataset once:

```markup
wget https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/ShareGPT_V3_unfiltered_cleaned_split.json \
  -O /workspace/sharegpt.json
```

With the server running, point the benchmark at it:

```markup
vllm bench serve \
  --backend vllm \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --endpoint /v1/completions \
  --dataset-name sharegpt \
  --dataset-path /workspace/sharegpt.json \
  --num-prompts 500 \
  --request-rate inf
```

`--request-rate inf` floods the server to measure peak throughput; set a finite rate (e.g. `--request-rate 8`) and `--max-concurrency` to simulate steady traffic. The summary reports throughput, TTFT, and TPOT; vLLM's server logs/metrics report the **acceptance length** for the EAGLE3 run.

***A trap worth knowing before you read your numbers.*** `--request-rate inf` ***fires all 500 prompts at once, so the GPU runs at ~500 concurrent requests, fully saturated. That is the throughput-bound regime, where speculation has no spare compute and can come out slower than baseline. To measure the latency regime, where EAGLE3 actually helps, add*** `--max-concurrency 1 --temperature 0` ***(one request at a time, greedy). Our result in 7.7 shows exactly this split.***

### A minimal sanity script (optional)

For an intuition check before the heavy tooling, time tokens/sec from a single streamed request:

```markup
import time, openai

client = openai.Client(base_url="http://127.0.0.1:8000/v1", api_key="None")
prompt = "Write a 400-word explanation of how a CPU cache works."

t0 = time.time()
n = 0
stream = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": prompt}],
    temperature=0, max_tokens=512, stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        n += 1
dt = time.time() - t0
print(f"{n} tokens in {dt:.2f}s = {n/dt:.1f} tok/s")
```

Run it against the baseline server, then against the EAGLE3 server. The difference in tok/s is your speedup (or, as 7.7 found, sometimes a slowdown) in one number. Use the real benchmark tools for anything you report.

## 7.7 Results

Here are the numbers from an actual run: Llama-3.1-8B on a single 48 GB Ada GPU, baseline vs EAGLE3, same prompts. I am reporting them exactly as they came out, because the honest result is more useful than a flattering one: **on this setup, EAGLE3 was slower in both regimes.** The tables show it, and the acceptance number explains it.

**Table A: Single request (batch 1, greedy** `temperature=0`**)**, the latency regime where speculation is *supposed* to win

![](https://substackcdn.com/image/fetch/$s_!m3Mn!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feedb2752-88b9-40f6-b47c-0c90d08a4f62_1695x462.png)

**Table B: Under load (500 prompts,** `--request-rate inf`**, ~500 concurrent)**, the throughput regime

![](https://substackcdn.com/image/fetch/$s_!5-wN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff46ce771-65eb-4342-8b45-bb3049f685e2_1803x462.png)

**Table C:** Acceptance (the diagnostic, from the EAGLE3 benchmark)

![](https://substackcdn.com/image/fetch/$s_!b987!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10792206-9eb7-4587-9afd-40b16eec9e1c_1623x543.png)

Table D: Latency under load

![](https://substackcdn.com/image/fetch/$s_!NGiO!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb16e134-4445-40e4-9550-aa18519d2faa_1948x462.png)

**Table C is the whole story.** Acceptance length came out at **1.81**, barely above 1 and nowhere near the 3–4 you need for a win. When fewer than two of every three drafted tokens survive verification, the cost of drafting and verifying isn’t paid back, so throughput drops and latency rises. **This is not a bug; it is speculation losing its bet,** and the diagnostic tells you *why*, not just *whether*.

Three things drove acceptance down, and they are worth internalizing because they generalize:

1. **A small target on a fast GPU is the hard case for speculation.** An 8B model already decodes quickly (45 tok/s single-stream here), so the memory-bandwidth headroom that speculation trades compute for is small, and the draft head’s own forward pass eats most of any gain. EAGLE3’s economics are far better on **large** targets (70B), where each decode step is expensive and the draft is comparatively cheap. The published ~2.4× for 8B and ~4× for 70B come from bigger, more favorable setups than a single mid-range card.
2. **The load benchmark ran non-greedy.** vLLM’s benchmark no longer forces `temperature=0`, and stochastic sampling lowers acceptance because the target’s samples diverge from the draft’s guesses more often.
3. `--request-rate inf` **saturated the GPU.** At ~500 concurrent requests the card is compute-bound, so speculation’s extra work steals cycles from useful generation (7.8).

*This is what "speculative decoding is a **bet** " means in practice. Modest acceptance, a small model, and a saturated GPU stacked up, and the bet did not pay. The number that told me in one glance was **acceptance length (*****τ=1.81*****)**. Read it first, always.*

**Could I make it win?** Probably, but not for free. You would push acceptance up and stay in the latency regime: benchmark with `--max-concurrency 1 --temperature 0`, try `num_speculative_tokens: 2` (shorter drafts fail less often), and confirm the draft head is actually attached (the acceptance line in the server log). The biggest lever, though, is the target size: run EAGLE3 against a **70B** model and the same machinery usually comes out well ahead. On an 8B, expect the fight to be close, and sometimes a loss.

## 7.8 When speculation helps, and when it hurts

EAGLE3 is excellent, but it is still a bet, not a free switch, and 7.7 is proof. From the production literature (Red Hat’s gpt-oss and EAGLE3 studies, ) plus my own run:

**It helps most when:**

- The workload is **decode-heavy** (short prompts, long responses), like chat, reasoning, and agents.
- The **target model is large** (say 70B). Each decode step is expensive, so a cheap draft that lands even half its tokens is a clear win. This is the single biggest factor, and the one my 8B run was missing.
- Acceptance is **high** (τ≳3), which needs a well-matched draft head and, ideally, greedy or low-temperature decoding.

**It hurts or does nothing when:**

- The **target is small and the GPU is fast** (my case): baseline decoding is already quick, so there is little bandwidth headroom to buy back, and the draft’s own forward pass eats the gain.
- The GPU is already **compute-saturated** (high concurrency), so speculation’s extra drafting steals cycles from useful work. Some studies report gains even at ~200 concurrent requests, but my 500-concurrent run lost, so do not assume it, measure it.
- The workload is **prefill-heavy** (long unique prompts, little cache reuse), because the decode phase is too short to amortize the drafting.

This is why modern serving stacks treat speculation as a **dynamic** feature, on at light/medium load, automatically off when the queue saturates.

## 8\. Takeaways

**The idea:**

- **The problem is memory bandwidth.** Generation is slow because the GPU re-reads the model’s entire weights for every token, leaving its math units idle. There is spare compute sitting there unused.
- **The idea is guess-and-verify.** A cheap drafter proposes several tokens, the expensive target verifies them all in one parallel pass, accepting a prefix and correcting the first mismatch.
- **It is exact, not approximate.** Modified rejection sampling (accept with min⁡(1,p/q), resample from the residual) guarantees the output matches the target distribution token for token. The draft only affects speed.
- **The economics come down to** ***α*****,** ***τ*****, and** ***K*****.** High acceptance (*α*) and well-tuned, adaptive lookahead (*K*) push you toward the best-case speedup. Mismatched drafts and a bad *K* waste compute.
- **Pick the drafter that fits your text.** Use **n-gram lookup** for repetitive, input-grounded tasks with zero extra VRAM, **Medusa** for a single self-contained model, and **EAGLE** when you want the highest acceptance by drafting features instead of tokens.
- **The real speedup depends on batch size.** Fixed per-step overheads and, above all, GPU saturation erode the paper speedup: speculation is a low-load latency win, and its headroom collapses as verification comes to dominate each step.

**The deployment:**

- **In production, deploy one method: EAGLE3.** It ships with pre-trained heads for popular targets (including Llama-3.1-8B), and it is **one flag** in vLLM (`--speculative-config`), not a rewrite.
- **8B is a single-GPU job.** One 48 GB card runs the target, KV cache, and EAGLE3 head at once, with no tensor parallelism or quantization.
- **Read acceptance length first.** *τ* tells you whether EAGLE3 is working before throughput does. My run’s *τ* =1.81 predicted the slowdown in one glance.
- **It is conditional, and it can lose.** A small model on a fast, saturated GPU is the hard case, and ours came out slower. The win grows with model size and acceptance. Measure your own A/B before you ship it.

*The lesson under all of it: when a system is bottlenecked on one resource, you can spend a **cheap, abundant** resource to relieve the **expensive, scarce** one. Speculative decoding spends idle compute to buy back memory bandwidth. When the draft aligns and the GPU has room, it hands you faster text for free; when it does not, the **acceptance length** tells you so at a glance.*

## 9\. What I didn’t cover

This post covered the foundations and a working deployment. Several powerful ideas were mentioned only in passing or left out entirely, worth a look if you want to go deeper:

- **EAGLE-2 / EAGLE-3: dynamic candidate trees.** Section 6.3 introduced EAGLE’s core idea, drafting at the *hidden-feature* level. The refinements build a *dynamic* candidate tree on top of those features, plus training-time tricks that push acceptance rates (and speedups) well past the vanilla EAGLE drafter.
- **Self-speculation (layer-skipping / early-exit drafting).** Turning the target model into its own drafter by skipping its middle layers, so you get drafts with no second model and no extra VRAM, sidestepping the dual-model cost from 5.4.
- **Streaming / overlapped execution.** Pipelining the draft and verify phases so the two models stop sitting idle in lockstep, closing the “bubble” time described in 5.1.
- **Tree-based verification beyond Medusa** (e.g. SpecInfer, Sequoia): smarter token trees, how to shape and size them, and how tree depth trades off against verification cost.
- **Speculation at high batch sizes.** How newer methods keep speculation useful in the throughput-bound regime instead of being toggled off the moment the GPU saturates.
- **Designing and training the draft model.** Distilling and aligning a drafter to maximize the acceptance rate *α*, and how draft–target alignment is actually engineered.
- **Adjacent ways to break the autoregressive barrier**, such as multi-token prediction (MTP), lookahead / Jacobi decoding, and how they relate to classic speculative decoding.
- **Other serving stacks.** How TensorRT-LLM and SGLang implement and auto-tune all of this (SGLang in particular has strong EAGLE3 support once you are on a compatible CUDA build).

That is where I am going to stop for today. There is clearly more here: dynamic EAGLE trees, self-speculation, streaming overlap, and now this semi-autoregressive line from DeepSeek. Maybe, if there is appetite for it, I will do a Part 2 that actually works through those. But this post is already long, and I would rather end it clean than stretch it thin.

If you liked the way this one reads, I have more in the same style on the way, and I think you will enjoy those just as much.

**This is Part 1 of a longer run I am planning on LLM inference optimization, with more coming on CUDA, Triton.**

Alongside the writing, I’m also building Audio Deep Learning projects and LLM projects, sharing and discussing them on LinkedIn and Twitter. If you’re someone curious about these topics, I’d love to connect with you all!

**Mayank Pratap Singh**

**LinkedIn**: [www.linkedin.com/in/mayankpratapsingh022](https://www.linkedin.com/in/mayankpratapsingh022/)

**Twitter/X**: [x.com/Mayank\_022](https://x.com/Mayank_022).