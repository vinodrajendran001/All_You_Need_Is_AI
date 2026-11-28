---
title: "From Model Compression to Looped Transformers"
source: "https://shiweiliuiiiiiii.github.io/blog/2026/from-model-compression-to-looped-transformers/?utm_source=tldrai"
author:
  - "[[Shiwei Liu]]"
published: 2026-11-26
created: 2026-11-28
description: "How the Curse of Depth Changed My Perspective on Efficient AI"
tags:
  - "clippings"
---
At first glance, moving from model compression to Looped Transformers may seem like a big leap, but once you see the Curse of Depth as the thread connecting them, I believe the journey makes sense.

For years, I tried to make neural networks smaller. Eventually, that work made me question why we were making them deeper.

Before the current LLM era, much of my research was about model compression: pruning weights, reducing precision, and finding ways to preserve performance with fewer resources. I became used to asking which parts of a convolutional network we could afford to remove.<sup><a href="#ref-1" aria-label="Reference 1">1</a></sup><sup>,</sup><sup><a href="#ref-2" aria-label="Reference 2">2</a></sup>

When I started working on LLMs, a familiar pattern reappeared. Layers were not equally sensitive to compression. Often, we could compress substantial parts of the deeper network more aggressively than the early layers.

At first, that looked like good news. It gave us a useful way to allocate a compression budget. But the longer I thought about it, the more it bothered me.

**If the deeper layers are so easy to remove, what did we gain by putting them there?**

That question gradually changed the direction of my research. It led from LLM pruning to the Curse of Depth, from normalization to residual connections, and eventually to Looped Transformers. Looking back, these projects feel like different stages of the same investigation: how do we make additional computation actually matter?

This is a personal account of that journey, rather than a survey. I use “I” for the questions that motivated me and “we” for the research carried out with my collaborators.

## 1\. A useful compression trick becomes an uncomfortable question

Compression teaches you to look at a model differently. Instead of taking its architecture at face value, you start probing it. Remove some weights. Reduce their precision. Observe where the model breaks—and where it barely notices.

A model may look uniform on paper: the same block, repeated many times. Its sensitivity to these interventions can be anything but uniform.

That was the starting point of our work on [Outlier Weighed Layerwise Sparsity, or OWL](https://arxiv.org/abs/2310.05175). Rather than assigning the same sparsity to every layer, OWL uses the layerwise distribution of outliers to allocate different pruning ratios. Layers with more outliers are treated more conservatively.

![OWL Figure 1: nonuniform sparsity allocations and layerwise outlier distributions in LLaMA models.](https://shiweiliuiiiiiii.github.io/assets/img/blog/from-model-compression-to-looped-transformers/01_owl.png)

Figure 1. A model's repeated architecture hides an uneven compression budget. OWL assigns different sparsity ratios across depth. Many later interior layers receive more pruning than early layers, but the pattern is not strictly monotonic: the final layers can be sensitive again. Reproduced from OWL, Figure 1.

For a compression researcher, this is an opportunity. At a given overall sparsity, preserving sensitive layers and pruning less sensitive ones more heavily can produce a better model than treating every layer identically.

But I began to see the same observation from the opposite direction.

Imagine that compression is no longer your main concern. You are designing and training the original model. You pay for those deeper layers during training and inference. You expect them to perform additional transformations—to refine a representation, develop a useful feature, or carry out another stage of computation.

If substantial parts of that depth can be removed with little consequence, perhaps the model is not using its architecture as effectively as we hoped.

Of course, compressibility alone does not prove that a layer is useless. Redundancy can be helpful, and removing weights is not the same experiment as removing an entire block. But it gives us a reason to investigate.

The question I wanted to answer had changed. I was no longer satisfied with knowing **where we could compress more**. I wanted to understand **why there was so much room to compress in the first place**.

## 2\. The Curse of Depth: a deep network can behave less deeply than it looks

After thinking about this for a few days, I kept returning to something that initially seemed like a small architectural detail: where normalization sits relative to the residual connection.

Pre-LN and Post-LN arrange almost the same components differently. Writing one residual sublayer schematically:

Pre-LN: x<sub>ℓ+1</sub> = x<sub>ℓ</sub> + F<sub>ℓ</sub>(LN(x<sub>ℓ</sub>))  
Post-LN: x<sub>ℓ+1</sub> = LN(x<sub>ℓ</sub> + F<sub>ℓ</sub>(x<sub>ℓ</sub>))

In Pre-LN, the branch receives normalized input, but the accumulated residual stream bypasses that normalization. In Post-LN, normalization acts after the addition.

We compared their behavior. In controlled models, the contrast was striking: deeper Post-LN layers became more distinct and more consequential, whereas deeper Pre-LN layers tended to change the representation less. [Our Curse of Depth paper](https://arxiv.org/abs/2502.05795) investigated this empirically and theoretically.

![Controlled Post-LN versus Pre-LN comparison, showing representation changes and the effect of removing individual layers.](https://shiweiliuiiiiiii.github.io/assets/img/blog/from-model-compression-to-looped-transformers/02_pre_post_ln.png)

Figure 2. The comparison that made normalization placement hard to ignore. In controlled LLaMA-130M experiments, Post-LN and Pre-LN exhibit contrasting depth-utilization patterns. The top panels show angular distances; the bottom panels show the performance impact of removing individual layers. Reproduced from The Curse of Depth, Figure 3.

The mechanism centers on residual-stream variance. As its scale grows, the normalized residual branch can become less influential relative to the identity path. Under the analyzed growth conditions, the block Jacobian approaches the identity:

J<sub>ℓ</sub> = I + J<sub>F<sub>ℓ</sub></sub> J<sub>LN</sub> ≈ I.

This is a subtle failure mode. Information can still pass through the network, but later blocks contribute progressively less transformation. A near-identity Jacobian is a statement about local sensitivity; it does not, by itself, mean the block output is exactly its input. The layer-removal and representation analyses provide complementary evidence of underused depth.

We called this phenomenon the **Curse of Depth**.

The phrase captures the distinction that had been bothering me since the pruning experiments: architectural depth is easy to count; useful computational depth has to be earned.

Our first response was [LayerNorm Scaling](https://arxiv.org/abs/2502.05795): scale the normalized branch input by 1/√ℓ. This controls variance growth and improves depth utilization while retaining the Pre-LN structure.

What stayed with me was the broader lesson. The residual pathway is part of the computation. Its design influences whether the next layer meaningfully changes anything.

## 3\. Attention Residuals: changing how a model reads its own depth

By this point, I had become increasingly interested in residual connections themselves. We had found a way to improve their behavior through scaling. But I wanted to know how much more could change if we reconsidered the way information moves across depth.

Then Kimi’s [Attention Residuals](https://arxiv.org/abs/2603.15031) appeared.

For me, it was a game changer conceptually. Standard residual addition accumulates previous updates with fixed unit weights. Attention Residuals lets a layer selectively combine earlier representations using learned, input-dependent weights.

The idea shifts attention toward the history of computation inside the model. A layer can choose which earlier representations to read, rather than relying entirely on one accumulated sum. Full AttnRes keeps access to preceding outputs; Block AttnRes groups them to reduce overhead.

This connected directly to the question that compression had raised for me. Perhaps deeper layers were underperforming partly because of the way we delivered information to them. Changing that delivery mechanism could change what additional depth was worth.

We wanted to test this systematically. In [DepthBench](https://arxiv.org/abs/2609.32534), we compared residual and normalization designs while varying the width–depth tradeoff under approximately fixed parameter budgets and a shared pretraining recipe.

![DepthBench validation loss versus width-to-depth aspect ratio under a roughly fixed 400M parameter budget, alongside model shape comparisons.](https://shiweiliuiiiiiii.github.io/assets/img/blog/from-model-compression-to-looped-transformers/03_depthbench.png)

Figure 3. The value of depth depends on the residual architecture. On the left, moving left means deeper and narrower models under an approximately fixed 400M parameter budget. Full AttnRes and HC benefit from these deeper shapes much more consistently than standard Pre-LN. The right panel contextualizes the shape preferences. Reproduced from DepthBench, Figure 1.

The results made the distinction concrete. In the tested settings, standard Pre-LN and many normalization or scaling variants gained little—or became worse—as models became deeper and narrower. Full Attention Residuals and Hyper-Connections benefited much more consistently.

This was also a useful reminder of the limits of our earlier solution. LayerNorm Scaling addressed an identified pathology, but that did not mean it solved every challenge of depth scaling. DepthBench pushed us to ask a harder question: which architectures make a greater allocation of capacity to depth worthwhile?

There are qualifications. Fixed parameters and a shared training recipe do not make all costs identical. Full AttnRes and Block AttnRes also behaved differently in this benchmark. The result is evidence for particular architectures and settings, rather than a claim that every attention-based residual design will always win.

Still, my interpretation was clear: **the residual connection helps determine whether depth is a productive scaling axis at all.**

## 4\. Looped Transformers: the same question, with shared weights

Around this stage, Looped Transformers became a natural next direction for me.

An ordinary deep Transformer applies different blocks in sequence. A looped model repeatedly applies shared blocks. It offers another way to increase computational depth without duplicating the main backbone parameters.

That is an appealing proposition for someone who came from compression. Instead of asking how much of a large model we can remove, we can ask how much computation we can obtain from a smaller set of weights.

But parameter reuse does not automatically imply useful computation reuse.

Each additional loop needs to do something worthwhile. If it mostly preserves the previous state, repeats an unhelpful update, or pushes the representation farther from what the task needs, we have increased the computation without getting the benefit we wanted.

Weight sharing also makes recurrence a demanding setting for residual design. The same transformations act repeatedly on their own evolving outputs. In our experiments, uncontrolled residual accumulation amplified variance growth and representation drift. For MoE models, we also observed a separate problem: shared routers could repeatedly choose similar experts, limiting diversity across loops.

This is the connection to the Curse of Depth. Looping gives us more architectural computation; it does not guarantee that the model can use it.

### Carry useful history without keeping all of it

Attention Residuals suggested a compelling direction: allow later computation to reuse earlier representations more selectively. But retaining and attending over an ever-growing history becomes expensive as the number of iterations increases.

For straightforward full-history attention over T depth steps, the history grows with T, and the total aggregation work grows quadratically in T. Blockwise strategies reduce that burden, but the question of how to manage a long computational history remains.

This led us toward a loop-friendly alternative in [LOOM](https://arxiv.org/abs/2610.01153): a Looping Residual based on a normalized exponential moving average.

Instead of retaining every output, maintain an accumulator and its normalization:

N ← βN + o D ← βD + 1 r = N / D.

Here, o is the current scaled attention output. The resulting summary weights past outputs exponentially by recency. LOOM uses a fixed decay β = 0.5, with a global memory across layers and loops and a local memory that resets each loop.

![A current output and a previous summary update a normalized EMA memory; LOOM keeps one global memory and one memory reset each loop.](https://shiweiliuiiiiiii.github.io/assets/img/blog/from-model-compression-to-looped-transformers/04_memory.svg)

Figure 4. Keep a running summary instead of an expanding list of depth outputs. LOOM's global and local memories follow the same normalized EMA update, but have different reset boundaries. This is an explanatory schematic, not an experimental result.

I think of this as carrying a central motivation of Attention Residuals into a recurrent setting: give subsequent computation access to useful history. The mechanism is different, though. A fixed-decay EMA is not content-dependent softmax attention, nor an exact replacement for it. It trades flexible retrieval of individual past states for a compact recurrent summary.

A fixed decay is only a starting point. **I believe we can do better by learning how quickly the model should forget.** A learned decay factor would let the model choose its own memory timescale: a larger β retains earlier contributions for longer, while a smaller β emphasizes recent computation. A simple extension would learn a separate β = sigmoid(θ) for each memory; a more expressive version could make the decay depend on the current state, allowing retention to adapt as computation unfolds.

The appeal is that we can learn this forgetting behavior while retaining the same compact accumulator structure. We pursue this idea in InfiLoop, discussed below, combining learned temporal decay with content-based weighting. LOOM’s fixed-decay EMA and InfiLoop’s learned attention residual are distinct designs; the learned-memory results come from InfiLoop’s reasoning experiments, rather than the LOOM comparison shown next.

That tradeoff matters if our ambition is to keep looping. The additional summary state does not grow with the number of loops, and each memory update uses elementwise operations. This statement concerns the residual memory specifically; it does not make the entire model’s compute, KV cache, or training memory constant.

### Beating Non-Looped Transformers Under Matched FLOPs

The result that matters most to me is that **LOOM can outperform a non-looped Transformer under a near-matched FLOP budget.** This asks whether recurrent depth is a better way to spend a given amount of computation—a direct continuation of the efficiency question that motivated my compression research.

In our 700M-parameter comparison, all models are trained on 10B tokens. We keep the backbone dimensions fixed and reduce the number of activated experts per pass as we increase the number of loops, keeping the estimated per-token compute approximately constant. At five loops, LOOM reduces validation perplexity from **18.36 to 16.54** and improves average zero-shot accuracy from **38.84% to 39.53%** relative to the non-looped baseline. The four-loop model also reaches **39.53%** accuracy, with perplexity **16.58**, while matching the baseline’s per-token FLOP proxy exactly; the five-loop configuration uses about 7% more under that proxy.

For me, this is evidence that **how we organize computation matters, even when its budget is held approximately fixed.** In this comparison, spending that budget on successive passes through shared weights is more effective than spending it on more active experts in a single pass. The scope is this tested MoE baseline and compute accounting; it does not establish superiority over every possible non-looped architecture.

LOOM combines residual memory with residual scaling, embedding re-injection, and loop-specific routers. These gains belong to the complete recipe, rather than to EMA alone.

![LOOM results: best performance near five loops under near-matched FLOPs for 700M, and near nine loops without FLOP matching for 1.7B.](https://shiweiliuiiiiiii.github.io/assets/img/blog/from-model-compression-to-looped-transformers/05_loom.png)

Figure 5. Beating the non-looped baseline with a near-matched compute budget. Left: looped 700M models outperform the one-pass baseline, with the lowest perplexity near five loops under the near-iso-FLOP comparison. Right: the 1.7B model peaks near nine loops when additional loops are allowed additional compute. These are finite tested regimes, not evidence of unlimited improvement. Reproduced from LOOM, Figure 1.

The left panel supports the central efficiency claim: recurrent depth can deliver better performance at approximately the same compute budget. The right panel addresses a complementary question: how much further can performance improve when we allow additional computation? Keeping these comparisons separate makes clear what looping buys us in each setting.

### Latent Overthinking: When More Loops Undo Earlier Progress

There is another reason why useful depth matters: additional computation can actively make a model worse.

In [our InfiLoop paper](https://arxiv.org/abs/2610.11570), we observed a phenomenon we call **latent overthinking**. A looped model can reach a correct intermediate deduction—or even a complete solution—and then overwrite it in subsequent iterations. More computation becomes an opportunity to lose progress.

This made the limitation of the usual “carry-last” rule especially clear to me. When every new recurrent output becomes the next state, the model has to preserve everything useful through that latest output. A noisy update can damage what earlier iterations worked to establish. The newest state is not necessarily the best state to carry forward.

![InfiLoop Figure 1: TRM accuracy declines after peaking, while InfiLoop improves; post-solution state changes and solution retention show InfiLoop preserving correct solutions.](https://shiweiliuiiiiiii.github.io/assets/img/blog/from-model-compression-to-looped-transformers/06_latent_overthinking.png)

Figure 6. Latent overthinking on Sudoku-Extreme. TRM peaks at 62.2% exact accuracy at 468 executed layers, then falls to 58.1% at 1,872 layers; InfiLoop reaches 90.9% at that depth. In the post-solution analysis, TRM loses 19.7% of solutions after 36 further updates, while InfiLoop retains all of them over the measured window. The horizontal axis on the left counts executed layers, not outer loops. Reproduced from InfiLoop, Figure 1.

Our answer is to change the connection between iterations. **InfiLoop’s loop-native attention residual learns what to retain from earlier computation and how strongly to accept a new update.** It combines content scores with learned temporal decay in a running summary, so later iterations can build on useful history without storing every past state.

Writing the current candidate as z<sub>t</sub> and its positive content weight as e<sub>t</sub>, the aggregation has an exact streaming form:

N<sub>t</sub> = βN<sub>t−1</sub> + e<sub>t</sub>z<sub>t</sub>  
D<sub>t</sub> = βD<sub>t−1</sub> + e<sub>t</sub>  
h<sub>t</sub> = N<sub>t</sub> / D<sub>t</sub>

Here, β is learned. Unlike LOOM’s fixed-decay EMA, this update also weights candidates by their content. The resulting adaptive residual can suppress unreliable proposals and preserve a useful state instead of accepting every new output in full. Its persistent aggregation memory stays constant with loop count.

**This addresses the observed latent-overthinking failure:** in the reported post-solution window, InfiLoop preserves the solutions that the carry-last baseline can lose. In longer Sudoku-Extreme evaluations, it continues improving beyond 20,000 effective steps, measured as executed Transformer layers. These experiments demonstrate much longer useful recurrence; they do not establish unlimited improvement on every task.

For me, this adds another requirement to depth scaling. A model needs to make progress, but it also needs to protect that progress. Learning when to preserve a good state is part of learning how to reason for longer.

## Looking back—and forward

I did not start with a plan to move from pruning to recurrent architectures. I started with a practical question about efficiency, and an observation that became increasingly difficult to ignore.

Compression showed me where a model could afford to lose capacity. The Curse of Depth made me ask why that capacity was underused. Attention Residuals and DepthBench made the information pathway itself a central object of study. Looped Transformers brought the question back to efficiency: can a compact set of parameters support a much longer sequence of useful computation?

I still care about making models smaller. But I now see another side of the same goal: making the computation we retain more valuable.

The question that connects this journey is simple:

**How can we continue to improve a model’s capacity when resources are limited?**

Several questions now guide how I think about the next steps.

**How can we reduce the computational cost of Looped Transformers?** Weight sharing saves parameters, but executing another loop still costs computation and latency. Our [FlashLoop](https://arxiv.org/abs/2609.29812) work takes a step toward addressing this: it exploits redundancy across loops through token-sparse updates, loop-aware sparse attention, and KV-residual quantization, without additional training. Across the evaluated models, it achieves up to **1.64× end-to-end speedup** and roughly **6× KV-cache memory reduction**, while largely preserving accuracy. This brings the story back to compression: once we make recurrent depth useful, we can ask which computations and stored states do not need to be repeated in full.

I am also interested in **combining looping with diffusion-style parallel decoding**. Could a looped diffusion language model refine multiple token positions together, with additional loops reserved for positions that still need work? Another possibility is to use shallow loops to produce parallel drafts and deeper loops to verify or correct them. The key is to coordinate recurrent depth with denoising steps and reuse intermediate computation, so that parallel generation reduces latency rather than simply multiplying two iterative costs. These are directions to explore: the goal is to preserve the benefits of deeper computation while generating more tokens per unit of time, at comparable output quality.

**How should a model decide where to spend additional computation?** Different inputs—and different tokens within an input—may need different amounts of reasoning. Can a model allocate loops adaptively and stop when further computation is unlikely to help, without stopping before a difficult problem is solved?

**What should a compact recurrent memory retain, and when should it forget?** Learned decay and content weighting give us a starting point. Can a state-dependent memory better preserve important deductions while discarding misleading updates, under a fixed memory budget?

**How should we divide a limited budget between parameters and recurrent depth?** Given a training budget, memory limit, and inference-latency target, when should we build a wider model, add distinct layers, or reuse existing layers through more loops? I want to understand these tradeoffs across model scales and tasks.

**Can compression and recurrence be designed together?** Pruning and quantization could make each loop cheaper, but repeatedly applying shared weights may also compound approximation errors. Can we co-design compressed weights and loop-native residuals so that efficiency gains survive long recurrence?

These questions bring me back to where I started: how to get more capability from the resources we have.

---