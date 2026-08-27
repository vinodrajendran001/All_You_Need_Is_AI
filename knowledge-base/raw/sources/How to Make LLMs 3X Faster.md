---
title: "How to Make LLMs 3X Faster"
source: "https://blog.bytebytego.com/p/how-to-make-llms-3x-faster?utm_source=post-email-title&publication_id=817132&post_id=212180385&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-08-26
created: 2026-08-27
description: "In this article, we will look at how speculative decoding works."
tags:
  - "clippings"
---
## What is loop engineering? (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!BpoA!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F76c3c864-4eb8-45bb-aee2-76e59bba8856_1200x628.jpeg)

Every agent already runs a loop. Loop engineering adds a loop around the agent itself, enabling it to evaluate its output, try again when the work falls short, and refine its instructions when the same mistakes recur. Today, you perform that role: reviewing the work, diagnosing what went wrong, and prompting the agent again. This article shows how to automate that process with a working example, while exploring where human judgment still belongs.

---

A 70-billion-parameter model requires reading roughly 140 GBs of weights out of the GPU memory. On a modern data center GPU, this transfer can take tens of milliseconds. The actual calculation applied to these weights takes a fraction of that time. This means that the processor’s math units are unused for most of the time taken by the token generation step.

Speculative decoding is a technique that converts this unused capacity into output. A second, much smaller model produces several candidate tokens in advance. The large model evaluates all of them in a single forward pass instead of one pass per token, resulting in 2-3 times faster generation. To make things better, the text produced remains statistically identical to the output of the large model running alone.

In this article, we will look at how speculative decoding works. Here’s what we will cover:

- Why token generation runs one step at a time
- What a GPU spends its time on during generation
- How several candidate tokens are evaluated in a single pass
- The accept and reject loop, and what happens when a candidate is wrong
- Why output quality is preserved exactly
- Acceptance rate, and why it varies by workload
- The four places a draft can come from
- When speculative decoding stops helping

![](https://substackcdn.com/image/fetch/$s_!wEyb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55326d4d-9fd1-4a48-8967-6ed265064e86_2174x1128.png)

*Disclaimer: This post is based on publicly shared details from various sources. References at the end. Please comment if you notice any inaccuracies.*

## Autoregressive Decoding

Text generation works one token at a time.

The model reads everything produced so far, computes a probability distribution over its vocabulary, selects the next token, appends that token to the input, and repeats the cycle. Each cycle is called a forward pass, and every forward pass runs the input through all layers of the model.

For example, token 50 depends on token 49 being present in the input, and token 49 depends on token 48, and so on. Computing them simultaneously would break the dependency chain that makes the output coherent.

The implication is that a 500-token response requires 500 sequential forward passes, each one completing before the next begins. Since the duration of a single pass depends on the size of the model, the total generation time equals the number of output tokens multiplied by the time per forward pass.

This explains why the response speed stays roughly steady whether the answer is a short factual reply or a long block of code, because the per-token cost stays the same either way. It also explains why a larger model produces text more slowly on identical hardware.

Modern inference systems use a KV cache, which stores the attention state for tokens already processed so that each new pass only computes attention for the newest position. This cuts the work done inside each pass to a large extent, though the requirement for one pass per token still remains.

## Memory Bandwidth

Since the number of passes is fixed by how much text we want, it leaves the second half of the equation. What does a single forward pass actually spend its time doing?

To put it simply, a forward pass spends most of its duration moving data rather than performing arithmetic calculations.

Model weights live in the GPU memory, usually called VRAM. To compute anything with those weights, the GPU has to transfer them into the compute units where the multiplication happens. For a 70-billion-parameter model stored at 16-bit precision, this transfer amounts to roughly 140 GBs for every single token.

The arithmetic performed on those 140 GBs is quite small by comparison. One token means one narrow vector flowing through each weight matrix. The GPU loads an enormous matrix out of memory, multiplies it against that vector, discards it, and loads the next one.

The consequence is that during prompt processing, compute utilization is around 90 to 95 percent. However, during token generation, it falls to somewhere between 20 and 40 percent. The math units are unused for most of every step while the memory bus runs near capacity.

The difference is driven by how much work each weight read supports:

- Prompt processing reads the weights once and applies them to thousands of input tokens simultaneously.
- Token generation reads the same weights and applies them to exactly one token.

This is capacity that has already been paid for, but underutilized.

But why does this matter practically?

A GPU with higher memory bandwidth improves generation speed more than one with more raw compute.

![](https://substackcdn.com/image/fetch/$s_!OoLa!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0375236-d679-4861-b070-f7bbb6a0c9cc_2036x1222.png)

However, spare capacity only helps if there is useful work to put into it. The question is whether a single forward pass can produce more than one token’s worth of output.

## Parallel Verification

A single forward pass can evaluate many positions at once.

Transformers process an entire sequence in parallel. When we feed in a sequence of tokens, the model computes a next-token prediction at every position in that sequence during the same pass. For example, a five-token input produces five predictions.

These predictions stay valid because of causal masking. Inside the attention mechanism, position 5 can access positions 1 through 5 while positions 6 and beyond are masked out, and position 3 can access only positions 1 through 3. Each position is therefore conditioned on exactly the tokens preceding it, identical to the conditioning it would have received had we generated the sequence one step at a time.

This is the property that makes prompt processing fast. A 2,000-token prompt runs through the model in one pass rather than 2,000, because all 2,000 positions are computed together.

When applied to verification, the consequence is direct. For example, if we append four candidate tokens to the context and run one forward pass, we receive the model’s own prediction at each of those four positions.

One thing to understand here is that verification and generation are basically the same operation. The target model performs identical work at each position. The cost savings comes from performing that work across several positions in a single pass instead of across one position in each of several passes.

![](https://substackcdn.com/image/fetch/$s_!6PI8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F246605ed-62d9-457b-ae0f-64154ae3b8f4_2584x1268.png)

## Draft and Verify

The complete loop combines a fast source of candidate tokens with the batched evaluation described above.

This setup uses two models:

- The large model we want output from is called the target model
- Running alongside it is a much smaller draft model with 10 to 20 times fewer parameters. It is usually drawn from the same family and uses the same tokenizer.

Each round has three steps:

- The draft model produces K candidate tokens through its own serial loop. Those passes are sequential as well, though each one costs a small fraction of a target model pass.
- The candidates are appended to the context. The target model evaluates the extended sequence in one forward pass.
- Working left to right, each candidate is compared against the target model’s prediction at that position. The matching candidates are kept, and as soon as the first mismatch appears, the remaining candidates are discarded.

The mismatch point plays an important role in this. The verification pass already computed the target model’s prediction at that position, so that token gets used directly. We keep the matching prefix and receive one correct token at no additional cost.

This property places a bound on the downside.

In the worst case, all four candidates might fail to match, but we would still have the one token the target model produced at the first position, which is exactly what plain decoding would have delivered from one forward pass. The wasted effort amounts to just the draft model’s compute and some extra effort in the verification pass. Both are drawn from otherwise available capacity. In a typical case where two of four candidates match, we get to keep two plus the free token, giving three tokens from one target model pass.

Draft length K is a tunable value, which is commonly set between 3 and 5. Larger values raise the ceiling on savings, since a fully accepted draft of eight saves more than a fully accepted draft of three. However, larger values also reduce the odds that later candidates survive, because the draft model conditions on its own unverified output as it moves forward. Past a certain point, the additional candidates get discarded often enough that the extra work outweighs the benefit.

![](https://substackcdn.com/image/fetch/$s_!bNtN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9187572-5dd5-4858-94d6-5f8278947e7b_3486x1978.png)

The question at this point is whether the resulting text is still the text the target model would have produced.

## Lossless Guarantee

Speculative decoding produces text with the same statistical properties as the target model running alone. This is enforced by means of the acceptance rule.

Under greedy decoding, where we always take the highest-probability token, the rule is quite direct. A candidate is kept when it matches the target model’s top choice at that position, and dropped when it fails to match.

However, sampling takes more care, since tokens get picked with some randomness. Both models produce a full set of probabilities across the vocabulary at each position. The rule compares the two sets:

- When the target model gave the candidate at least as much probability as the draft model did, the candidate is kept.
- When the target model gave it less, the candidate is kept part of the time. This is in proportion to how far apart the two numbers were.
- When a candidate is dropped, the replacement gets picked from an adjusted set of probabilities, with the draft model’s own scores subtracted out first.

This last step is critical. If we add up both paths, the candidates kept and the candidates replaced, the odds of any particular token appearing depend exactly on the target model’s own odds for it. This is regardless of what the draft model suggested.

There are two qualifications to this:

- Matching odds still allow different wording, since sampling stays random either way. Running the same prompt twice can give varied text in both setups.
- Computers store these numbers with limited precision, so rounding can flip the winner when two tokens sit almost exactly tied.

## Acceptance Rate

The size of the speed increase in this approach is governed by the acceptance rate, which is largely a property of the workload.

Acceptance rate is the fraction of candidate tokens the target model keeps, and acceptance length is the average number confirmed per verification pass, including the free token at the end.

Different workload types produce different results:

- Structured and repetitive output produces high acceptance. For example, code generation, summarization, extraction, and retrieval-augmented answers reuse large amounts of text from the input, which makes the next token easy to predict from a small model.
- Open-ended output produces low acceptance. Creative writing and open conversation generate text with genuine variety, where a small model diverges from a large one far more often.

Sampling temperature contributes as well. Higher temperature flattens the probability distribution, which increases mismatches between the two models and pushes acceptance down. If the acceptance falls below roughly 50%, the additional work outweighs the savings.

For reference, DeepSeek reported acceptance rates between 80 and 90 percent for the second predicted token in production serving of DeepSeek-V3, which translated to roughly 1.8x generation throughput.

The practical implication is that two teams can deploy the same configuration on the same hardware and get different results, because their users are asking different questions. Ultimately, acceptance depends on the quality of the candidates, which brings us to where candidates come from.

## Candidate or Draft Sources

The key question while choosing candidate or draft sources is where to obtain fast predictions cheaply. There are four answers in common use:

- **A separate small model:** The original approach pairs the target with a smaller sibling, so a 1B model drafting for a 13B target, or a 3B to 8B model drafting for a 70B target. Same family and identical tokenizer are requirements in this approach. The cost is a second checkpoint to deploy and version, plus VRAM that comes out of the KV cache budget, which reduces how many concurrent requests the server can hold.
- **Extra prediction heads on the target model:** Lightweight output heads predict tokens two or three positions ahead using the target model’s internal representations. DeepSeek-V3 trained these during pretraining to improve model quality, then reused them at inference as the draft source. The cost is training, which puts this option out of reach unless we control the model.
- **A cheaper version of the same model:** The draft runs the same weights under a reduced compute budget through quantization, layer skipping, or a compressed KV cache. For example, QuantSpec uses 4-bit weights and a 4-bit KV cache for drafting while verification runs at higher precision, reporting speedups above 1.78x with acceptance above 90 percent. The cost is implementation complexity, since draft and target share hardware and cache structures.
- **A search over existing text:** This approach scans the prompt and previous output for a recent matching sequence, then proposes whatever followed it last time. Memory cost is zero, and a single model is involved. It contributes only when output repeats input, where it reaches 2x to 4x on tasks like document editing and summarization.

Selecting an option depends on the deployment. Also, tokenizer compatibility constrains pairing more tightly than model quality does. A stronger small model with a different vocabulary is unusable as a draft source without additional machinery. All four options depend on spare compute being available. This condition holds under some serving loads better than others.

![](https://substackcdn.com/image/fetch/$s_!kP-g!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e1591d0-cdc6-4ff1-8d58-1d3fd57dda1f_3396x1774.png)

## Concurrency Limits

The increase in speed also depends on the operating regime rather than on the technique alone. The gains shrink as server load rises.

Speculative decoding spends compute capacity that would otherwise go unassigned. When a server handles a single request, this capacity is genuinely available. As concurrent requests accumulate, the same weight read operation serves many requests at once, and the compute units approach saturation. Verification work has to compete with real requests.

One systematic evaluation reported up to 1.96x on a 70B model at batch size 1, declining to 1.21x at batch size 128. Under higher concurrency, the technique can fall below baseline throughput, at which point enabling it costs more than the benefits.

Serving systems try to handle this in different ways. For example, vLLM exposes a flag that disables speculation above a configurable batch size. It supports dynamic adjustment where draft length shrinks as concurrency rises and reaches zero under heavy load. The control signals routine operational tuning rather than an edge case.

Another boundary is that the time to first token stays roughly the same, since speculative decoding applies to generation rather than prompt processing. Therefore, workloads with long prompts and short outputs have relatively little to gain.

DeepSeek documented the tradeoff, describing multi-token prediction as slightly reducing throughput while significantly improving end-to-end generation latency.

![](https://substackcdn.com/image/fetch/$s_!yatq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb6f55d1-ebb2-4220-8032-23beeef8cc63_4136x2440.png)

## Conclusion

Speculative decoding rearranges when the processing happens rather than reducing how much the target model performs. Here are some key points we have understood:

- Token generation is slow because every token requires reading the full set of model weights out of memory, while the arithmetic applied to those weights is comparatively small.
- A transformer computes a prediction at every position in one pass, which makes evaluating several candidate tokens cost about the same as evaluating one.
- A rejected draft truncates rather than wastes, since the verification pass supplies a correct token at the mismatch position regardless.
- Output quality is preserved by the acceptance rule itself, so it holds without tuning.
- The size of the gain depends on how predictable the output is and how much spare compute the server has available.
- The variants differ in where predictions come from and what that source costs.

---

∙