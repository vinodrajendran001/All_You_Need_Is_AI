---
type: inbox-source
title: "Why MLA and MTP Fight Each Other: Attention Through Arithmetic Intensity"
source: "https://www.linkedin.com/pulse/why-mla-mtp-fight-each-other-attention-through-arithmetic-yang-npr9c/"
author:
published: 2001-08-14
created: 2026-08-15
updated: 2026-08-24
tags:
  - source/inbox
status: pending
---
> **Strongly recommend check this site for better format!** Originally published at [https://changyi.fun/posts/attention-](https://changyi.fun/posts/attention-) [arithmetic-intensity/](https://changyi.fun/posts/attention-arithmetic-intensity/)

I was reading [this post by Su Jianlin](https://kexue.fm/archives/11848) when one sentence stopped me:

> Besides the KV cache, decoding now has another variable — MTP, or speculative decoding, whose idea is to trade compute for speed. But MLA behaves during decoding like an MQA with head\_dims=512+, and has already consumed most of the compute up front, so "MLA+MTP" tends to lose out.

My first reaction was: **what does that mean? Why would MLA "consume compute up front" during decode? And why should it conflict with MTP that its decode FLOPs come out equivalent to a head-dim-512+ MHA?**

Following the question down led to something classic, but unusually pretty when applied to attention: **arithmetic intensity** — FLOPs per byte moved.

And the answer turns out to be surprisingly clean (everything below assumes a BF16 KV cache):

- Reduce MHA all the way down and its AI comes out to **exactly 1**;
- GQA and MQA are just as clean — they depend on **nothing but head counts**. Context length and head dim cancel out completely;
- **MLA has the same shape again**, independent of the latent dim too, just with a constant of a little under 2 in front.

Lined up, here is the AI of the attention core for a single-token decode:

Sections 2 and 4 derive those four rows. The first three are the same formula with different KV head counts; the constant on the last row comes from somewhere else entirely.

And that constant of a little under 2 is just enough to move attention decode on many current GPUs from clearly memory-bound to sitting near the roofline knee. Stack MTP on top and the workload tips over into compute-bound — which is exactly why Su says MLA is unfriendly to MTP.

This post works through the whole derivation.

> *This one is written out in detail — starting from how you count FLOPs in a matmul, with every matrix shape spelled out. If you already know the structure of attention and what decode computes, section 2 can be skimmed down to the result in 2.5, then jump to section 3.*

---

### 1\. What arithmetic intensity is

The definition is simple:

$$ \\boxed{ AI = \\frac{\\text{FLOPs}}{\\text{HBM Bytes}} } $$

That is: **for every byte pulled in from HBM, how many floating-point operations do you get out of it.**

Low AI means the GPU spends most of its time moving data. High AI means each piece of data gets reused for a lot of arithmetic once it arrives.

The hardware has a matching threshold:

$$ \\boxed{ AI\_{\\text{hardware}} = \\frac{\\text{Peak Compute}}{\\text{HBM Bandwidth}} } $$

In the idealized roofline model:

$$ AI\_{\\text{workload}} < AI\_{\\text{hardware}} \\quad\\Rightarrow\\quad \\text{memory-bound} $$

and

$$ AI\_{\\text{workload}} > AI\_{\\text{hardware}} \\quad\\Rightarrow\\quad \\text{compute-bound} $$

Using dense BF16 tensor-core throughput, the theoretical balance points of a few common cards:

Sources: [NVIDIA H100](https://www.nvidia.com/en-us/data-center/h100/), [NVIDIA H200](https://www.nvidia.com/en-au/data-center/h200/), [NVIDIA HGX B200](https://www.nvidia.com/en-sg/data-center/hgx/), [NVIDIA DGX B200](https://www.nvidia.com/en-au/data-center/dgx-b200/).

No real kernel saturates peak FLOPs and peak bandwidth simultaneously, so treat these as a roofline upper bound for building intuition rather than a line you would see in a profiler. "A few hundred FLOP/B" is the magnitude to remember; it gets compared against later.

One caveat worth stating up front: **AI is a ratio. It answers "which side of the roofline are you on", not "which approach is faster."** Numerator and denominator can both grow and leave AI untouched while everything gets slower. Section 5 has a concrete case: two algorithms computing the same thing, where the one with the *higher* AI does 120× the FLOPs.

What follows only counts the KV-related part of attention:

> **For one decoded token: from its hidden state, compute Q, K and V, read in the KV cache, and carry through to this layer's attention output.**

Softmax is small next to the two big matmuls and is left out. The goal is not to estimate whole-layer latency; it is to isolate one question: **what does changing the attention structure do to the arithmetic intensity of that stretch?**

Sections 2 through 4 handle **decode** only (one token at a time, history read from cache). **Prefill** — computing an entire sequence at once — waits until section 5, where it turns out the same model wants the opposite algorithm in the two phases.

> *PS: why not count the final W\_{O} too? Because it has nothing to do with which attention structure you picked. W\_{O} always receives the concatenated per-head outputs, whose width depends only on H\_{q} and d\_{v} — how the KV side is organized is invisible to it, and MHA, GQA, MQA and MLA all hand it something the same width. Like the Q/K/V projections it is a weight-times-vector: it never touches the KV cache, does not grow with L, and at batch = 1 its AI is fixed at 2/b. Including it adds the same constant to every structure and dilutes the comparison. Same for the MLP and for communication.*

---

### 2\. One formula for MHA / GQA / MQA

### 2.1 How to count FLOPs

An (m × k) matrix times a (k × n) matrix takes m·n·k multiply-accumulates (MACs). One MAC is a multiply plus an add, so 2 FLOPs:

$$ \\text{FLOPs} = 2mnk $$

### 2.2 MHA, briefly

The most basic attention is MHA: split the hidden state into heads, let each head compute its own Query, Key and Value, run attention independently, then concatenate.

Start with the shapes. The layer receives the current token's hidden state:

$$ h \\in \\mathbb{R}^{1 \\times d\_{\\text{model}}} $$

Three projections turn it into Query, Key and Value. In MHA all three have the same head count, but GQA and MQA later reduce the K/V head count, so it gets its own symbol: H\_{q} query heads, H\_{kv} KV heads, with **MHA being the case H\_{kv} = H\_{q}**.

One thing to settle here: the Key head count and the Value head count are **not required by the math to match** — 8 groups of K and 4 of V would work fine on paper. But no real model is built that way: K and V are cached in **pairs**, and storing a position's k always means storing its v. This post follows that convention and calls both H\_{kv}.

As for head dims: Query and Key must match, or q and k cannot be dotted — call it d\_{k}. The Value dimension may differ; call it d\_{v}.

$$ W^Q \\in \\mathbb{R}^{d\_{\\text{model}} \\times H\_q d\_k}, \\quad W^K \\in \\mathbb{R}^{d\_{\\text{model}} \\times H\_{kv} d\_k}, \\quad W^V \\in \\mathbb{R}^{d\_{\\text{model}} \\times H\_{kv} d\_v} $$

Per head:

$$ q\_h \\in \\mathbb{R}^{1\\times d\_k}, \\qquad k\_h \\in \\mathbb{R}^{1\\times d\_k}, \\qquad v\_h \\in \\mathbb{R}^{1\\times d\_v} $$

The new k and v are appended to the KV cache. With history length L, the layer's cache is:

$$ K \\in \\mathbb{R}^{L \\times H\_{kv} \\times d\_k}, \\qquad V \\in \\mathbb{R}^{L \\times H\_{kv} \\times d\_v} $$

Then each query head does three steps. Write g(h) for the KV head that query head h uses (in MHA, g(h) = h):

**One — score.** Dot the current query against all L cached keys, a (1 × d\_{k}) by (d\_{k} × L) product:

$$ s\_h = q\_h K\_{g(h)}^\\top \\in \\mathbb{R}^{1\\times L} $$

**Two — normalise.** Softmax turns scores into weights; the shape does not change:

$$ p\_h = \\operatorname{softmax}(s\_h) \\in \\mathbb{R}^{1\\times L} $$

**Three — weighted sum.** Multiply the weights into Value, a (1 × L) by (L × d\_{v}) product:

$$ o\_h = p\_h V\_{g(h)} \\in \\mathbb{R}^{1\\times d\_v} $$

The H\_{q} per-head outputs concatenate into the layer's attention output.

### 2.3 FLOPs

Three parts, each with shapes substituted into 2mnk.

**One — compute this token's Q, K, V.** Three (1 × d\_{model}) by (d\_{model} × ·) products, so m = 1:

$$ F\_{\\text{proj}} = 2d\_{\\text{model}}\\left(H\_q d\_k + H\_{kv} d\_k + H\_{kv} d\_v\\right) $$

**Two — score.** Per query head, one (1 × d\_{k}) by (d\_{k} × L) product, times H\_{q} heads:

$$ F\_{QK} = 2H\_q L d\_k $$

**Three — weighted sum.** Per query head, one (1 × L) by (L × d\_{v}) product:

$$ F\_{PV} = 2H\_q L d\_v $$

All three together are the layer's attention arithmetic:

$$ F = F\_{\\text{proj}} + 2H\_q L (d\_k + d\_v) $$

The two terms behave completely differently: **F\_{proj} is independent of history length L**, since it only handles the current token, while **the second term is proportional to L**, because it sweeps the whole history. Their ratio, to an order of magnitude:

$$ \\frac{F\_{\\text{proj}}}{2H\_q L (d\_k+d\_v)} \\;\\sim\\; \\frac{d\_{\\text{model}}}{L} $$

(Substituting MHA's H\_{kv} = H\_{q} and d\_{k} = d\_{v} gives exactly 1.5 d\_{model}/L.)

That ratio is not as small as it sounds. With d\_{model} = 7168 it is 10752/L: at L = 8K the projections cost **more** than attention (1.3×), at 32K they are 33%, and it takes over a hundred thousand tokens to drop below 10%.

So dropping F\_{proj} is not justified by its being small. What justifies it is that **it is irrelevant to the comparison** — F\_{proj} is a weight-times-vector, reading weights rather than the KV cache, with AI fixed at 2/b whichever attention structure you choose. F\_{attn} is the only term that grows with L and the only one the structure changes. The AI below keeps just that:

$$ \\boxed{ F\_{\\text{attn}} = 2H\_q L (d\_k + d\_v) } $$

That said, do not forget the F\_{proj} path itself. Section 3 shows that what MLA does is precisely **to move work that would have been multiplied by L back onto that L-independent path**.

### 2.4 HBM bytes

Let each element take b bytes; BF16 means b = 2.

The cache holds H\_{kv} keys and H\_{kv} values, each position's key d\_{k} wide and value d\_{v} wide, across L positions:

$$ \\boxed{ B\_{KV} = bLH\_{kv}(d\_k + d\_v) } $$

This assumes a fused attention that does not write the L-length score/probability matrix back to HBM.

> The three projection weights are read from HBM too, of course. But they are weights rather than KV cache, and at batch = 1 a matrix-times-vector has AI fixed at 2/b regardless of attention structure, so they do not affect the comparison between structures below.

### 2.5 Divide

Keeping only the part that grows with L:

$$ AI = \\frac{2H\_qL(d\_k+d\_v)}{bLH\_{kv}(d\_k+d\_v)} $$

L cancels, and (d\_{k} + d\_{v}) cancels as a block:

$$ \\boxed{ AI\_{\\text{MHA/GQA/MQA}} = \\frac{2}{b}\\frac{H\_q}{H\_{kv}} } $$

With BF16, b = 2:

$$ \\boxed{ AI\_{\\text{BF16}} = \\frac{H\_q}{H\_{kv}} } $$

Here is the pretty part: **context length L and both head dims cancel out entirely.**

One quantity is left:

> **how many query heads reuse a single KV head**

### 2.6 Three special cases

MHA, GQA and MQA differ only in what H\_{kv} is:

So MHA → GQA → MQA is one formula with H\_{kv} sliding: **FLOPs do not drop when KV heads are removed, but the history read from HBM does, because one KV is reused by more query heads.**

That is the first layer of data reuse.

### 2.7 Real models

For example:

- [Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B/blob/main/config.json): H\_{q} = 28, H\_{kv} = 4;
- [Mixtral-8x7B](https://huggingface.co/mistralai/Mixtral-8x7B-v0.1/blob/main/config.json): H\_{q} = 32, H\_{kv} = 8;
- [Falcon-7B](https://huggingface.co/tiiuae/falcon-7b/blob/main/config.json): 71 query heads with multi\_query=true, i.e. true MQA.

So for BF16 single-token decode, the AI of this part is roughly:

At this point MQA has taken cross-head KV reuse as far as it goes: every query head shares one K and one V, and AI equals the query head count.

Which is also where it gets stuck: **MQA's AI ceiling is the query head count, and that number does not grow.** Common models have 32, 64 or 128 query heads; Falcon-7B's 71 is already on the high side, and the count is fixed by the architecture — you cannot simply add heads to buy AI. Against the few-hundred FLOP/B balance points from section 1, **piling on query heads alone cannot get there.**

And note the last few words:

> **one K, and one V.**

K and V are still two separate pieces of data.

That is what MLA changes next.

---

### 2.8 What about prefill?

Everything above was decode. What do the same formulas give for prefill?

Prefill computes the whole input at once. Let the input length be L (the same symbol as above — in decode it is the history, in prefill it is the input length itself). Every token attends to all tokens before it, so each K and V gets used by roughly L query tokens — the reuse is free. Dividing the same way:

$$ AI\_{\\text{prefill}} \\approx \\frac{H\_q}{H\_{kv}}\\cdot\\frac{L}{b} $$

That is **the decode AI multiplied by L/b**. Against H100's 295 FLOP/B:

**In prefill even plain MHA is compute-bound** — past six hundred or so tokens it is over the line, and GQA/MQA cross within a few dozen. There is no memory-bound problem to discuss in prefill at all.

Worth noting too: **GQA and MQA do not change prefill FLOPs whatsoever**, because FLOPs depend on H\_{q} and not H\_{kv}. They only push an already-over-the-line AI higher, and shrink the cache.

So:

> **The whole MHA → GQA → MQA → MLA line is a decode story.** Reuse in prefill is free and there is nothing to fix; these structures exist because decode has exactly one query token and therefore no reuse at all.

### 3\. MLAs latent cache

> *Editor's note: to keep the core structure clear,* ***the next few sections ignore RoPE****. It does not change the conclusion; putting it back is covered in appendix A at the end.*

What MLA changes is not attention's final form:

$$ \\operatorname{softmax}(QK^\\top)V $$

but the parameterization of the cached K and V.

For history token j, the hidden state is first compressed into a KV latent shared by all heads. The **D stands for down-projection**: W^{DKV} is the matrix that takes the d\_{model}-wide hidden state down to a much narrower d\_{c}:

$$ \\boxed{ c\_j=W^{DKV}h\_j } $$

where:

$$ c\_j\\in\\mathbb{R}^{d\_c} $$

Head h's K and V both expand out of that one latent:

$$ k\_{j,h}=W\_h^Kc\_j $$

$$ v\_{j,h}=W\_h^Vc\_j $$

So what used to be cached,

$$ K\_j, V\_j $$

now only needs to be:

$$ \\boxed{c\_j} $$

Put Kimi K3's numbers in: 96 heads, K and V head dims both 128, so **one KV is 128 + 128 = 256 numbers**. How much you store per token per layer is then just how many copies you keep:

48× smaller than MHA and 4× smaller than 8-group GQA — but **twice as large as MQA**.

So MLA's selling point was never "smallest cache"; on cache size alone it loses to MQA. What it buys is something else: that one latent plays the role of both K and V, whereas MQA's 256 is 128 of K and 128 of V doing separate jobs. Section 4 prices what that is worth.

But it immediately raises a problem: if every generated token re-expands all L cached latents through W^{K} and W^{V}, you have traded an HBM problem for an enormous compute one.

The clever part of MLA at decode is **matrix absorption / reassociation**.

### 3.1 K-side absorption

The original content score:

$$ q\_h^Tk\_{j,h} $$

Substituting:

$$ q\_h^TW\_h^Kc\_j $$

By associativity of matrix multiplication this can be rewritten:

$$ \\boxed{ q\_h^TW\_h^Kc\_j = \\left((W\_h^K)^Tq\_h\\right)^Tc\_j } $$

Which means there is no need to generate K for each of the L cached latents.

Instead, transform **the single current query token** once, pulling it into latent space — the resulting q̃\_{h} can be read as "the query, in latent space":

$$ \\tilde q\_h=(W\_h^K)^Tq\_h $$

then dot it against the whole history directly in latent space:

$$ \\tilde q\_h^Tc\_j $$

The direction is reversed: instead of expanding every cached latent into a K and comparing the query against it, the query is moved into latent space once and compared against the latents as stored. The scores are identical, but the second way never touches the history.

### 3.2 V-side absorption

Likewise, the original attention output:

$$ o\_h = \\sum\_jp\_{h,j}v\_{j,h} $$

Substituting v\_{j,h} = W\_{h}^{V} c\_{j}:

$$ o\_h = \\sum\_jp\_{h,j}W\_h^Vc\_j $$

Pulling the constant matrix outside the sum:

$$ \\boxed{ o\_h = W\_h^V \\left( \\sum\_jp\_{h,j}c\_j \\right) } $$

So PV can also happen entirely in latent space:

$$ P\_hC $$

with a single W\_{h}^{V} projection applied to the **one** latent output at the end.

### 3.3 Why the projection did not get expensive

This is the part I misread at first.

Without absorption, every generated token has to re-expand every cached c\_{j} — computing k\_{j,h} = W\_{h}^{K} c\_{j} and v\_{j,h} = W\_{h}^{V} c\_{j} for each head. The longer the history, the more times you do it, so the cost carries a factor of L:

$$ O(Ld\_cd\_kH) $$

After absorption, the extra K-side and V-side projections only touch the current query or the final output:

$$ O(Hd\_cd\_k)+O(Hd\_cd\_v) $$

They are **no longer multiplied by context length L**.

The part that grows with history becomes:

$$ O(HLd\_c) $$

So at long context, those few projections on the current token shrink steadily relative to reading the whole history.

Put another way:

> **MLA does not make the projection disappear. It changes the order of association, moving an expensive projection off the sequence's O(L) dimension and leaving it on the O(1) current-token path of each decode step.**

Same result, very different compute graph.

---

### 4\. Why MLAs AI doubles

Per section 3, each cached token stores one latent.

In MLA all query heads share that latent, so there is no "KV head count" dimension left; a single head count suffices, denoted H, which is the earlier H\_{q}.

Per cached token:

$$ c\_j\\in\\mathbb{R}^{d\_c} $$

### 4.1 FLOPs

**One — the parts independent of history length.** This one new token has to: compress its hidden state into a latent (2d\_{model} d\_{c}), compute its own query (2d\_{model} H d\_{k}), fold W^{K} into that query (the absorption of 3.1, 2H d\_{k} d\_{c}), and project the latent output back per head (2H d\_{c} d\_{v}). All of it applies to the current token only; call it F\_{fixed}.

**Two — the parts that sweep the history.** After absorption both the scoring and the weighted sum run on the latent, width d\_{c}:

$$ F\_{QK} = 2HLd\_c, \\qquad F\_{PV} = 2HLd\_c $$

Together:

$$ F = F\_{\\text{fixed}} + 4HLd\_c $$

For DeepSeek-V3 (d\_{model} = 7168, H = 128, d\_{c} = 512, d\_{k} = d\_{v} = 128), F\_{fixed} ≈ 276 MFLOP versus 0.26 MFLOP × L — a ratio of about 1052/L, so 13% at L = 8K and 3% at 32K.

Dropping F\_{fixed} is justified as before: it does not vary with L and does not participate in what is being compared. Keeping only the part that grows with L:

$$ \\boxed{ F\_{\\text{MLA}}=4HLd\_c } $$

### 4.2 HBM bytes

Here is the crux.

The history no longer has separate K and V caches, only one:

$$ C\\in\\mathbb{R}^{L\\times d\_c} $$

so under a fused kernel:

$$ \\boxed{ B\_{\\text{MLA}}=bLd\_c } $$

Note there is **no factor of 2 for K plus V** in the denominator.

Once that latent is read from HBM it:

1. takes part in QK;
2. takes part in PV.

So:

$$ AI\_{\\text{MLA}} = \\frac{4HLd\_c}{bLd\_c} $$

giving:

$$ \\boxed{ AI\_{\\text{MLA}} = \\frac{4H}{b} } $$

With BF16, b = 2:

$$ \\boxed{ AI\_{\\text{MLA,BF16}}=2H } $$

As in 2.5, the latent dim d\_{c} cancels here too: **the AI has nothing to do with how wide the latent is**, only with the head count. Widening the latent rank from 512 to 1024 doubles the KV cache and leaves this AI untouched.

The whole MLA AI story in one paragraph:

> **MQA already had every query head share the KV, reaching AI = H. MLA goes further and compresses what used to be two separate historical representations, K and V, into one latent. Once that latent arrives from HBM, both the K-side and the V-side computation use it — the same data consumed twice — and AI picks up another factor of 2.**

To be clear, this does not mean "MLA's cache is necessarily half of MQA's".

A plain MQA with d\_{k} = d\_{v} = 128 stores a KV width of:

$$ 128+128=256 $$

per cached token, whereas DeepSeek/Kimi's typical latent rank is 512 — the actual cache is wider.

The 2× comes from:

> **one latent serving as both K and V**

not from bytes mechanically halving.

There is also an implementation condition. If the kernel reads the latent once for QK, discards it, then re-reads it from HBM for PV, this reuse is lost and AI falls back toward H. The result assumes FlashAttention/FlashMLA-style fused, streaming execution, where the same latent tile serves both computations on chip.

Substituting AI = 2H into two real models: DeepSeek-V3 / R1 has 128 heads, giving **256 FLOP/B**; Kimi K3's MLA layer has 96 heads, giving **192 FLOP/B**.

Against the few-hundred FLOP/B balance points from section 1 — a batch-of-one decode is already sitting near the roofline knee.

---

### 5\. One MLA, two algorithms

Section 3 put it this way: re-expanding all L cached latents into K and V on every generated token would trade the HBM problem for an enormous compute one — and absorption is what avoids that expansion.

There is a premise hiding in that sentence: **"on every generated token."** Decode computes exactly one query token, so the expanded K and V are used once and thrown away, and there is **no other query token to share the cost with**. Avoiding it is pure profit.

Prefill is a different situation entirely. It computes thousands of query tokens at once, and the expanded K and V are **the same** for all of them — a cost that used to be discarded after a single use is suddenly divided among thousands. Whether it is still worth avoiding is no longer obvious.

The conclusion is a little counterintuitive: **the same MLA model, the same weights, wants opposite algorithms in decode and in prefill.** This section works out both and finds where the boundary is.

### 5.1 One product, two bracketings

Back to the expression from 3.1. For **one** query head and **one** cached token, the content score is three things multiplied:

$$ q\_h^{\\top} W\_h^{K} c\_j $$

Whichever way you bracket it gives the same value (associativity), but a completely different algorithm:

$$ \\underbrace{q\_h^{\\top} \\left( W\_h^{K} c\_j \\right)}\_{\\text{expand}} \\qquad\\text{vs.}\\qquad \\underbrace{\\left( (W\_h^{K})^{\\top} q\_h \\right)^{\\top} c\_j}\_{\\text{absorb}} $$

On the left, expand the cached latent into a K first, then dot with the query. On the right, fold W^{K} into the query first, then dot against the latent directly. The V side is the same idea in the other direction (section 3.2).

**First difference: which side the projection lands on.**

- expand: W^{K} c\_{j} is done per **cached token** — once each, shared by every query token in the batch;
- absorb: (W^{K})^{ op} q\_{h} is done per **query token** — once each, shared across the whole history.

The widths involved:

- d\_{c}: the latent width, section 3's c\_{j} — this is how wide each cached token is;
- d\_{k}: each head's K after expanding;
- d\_{v}: each head's V after expanding.

**Second difference: how wide the remaining dot product is.** For one query-token × cached-token pair, both paths do two multiply-accumulates — one to score, one to accumulate. The shapes make it clear.

**After expanding:**

- score: q\_{h} (1 × d\_{k}) dotted with k\_{j,h} (1 × d\_{k}), giving a scalar — d\_{k} MACs;
- weighted sum: the scalar p\_{h,j} times v\_{j,h} (1 × d\_{v}), accumulated into o\_{h} (1 × d\_{v}) — d\_{v} MACs.

Total d\_{k} + d\_{v}.

**After absorbing:**

- score: q̃\_{h} (1 × d\_{c}) dotted with c\_{j} (1 × d\_{c}) — d\_{c} MACs;
- weighted sum: the scalar p\_{h,j} times c\_{j} (1 × d\_{c}), accumulated into a d\_{c}-wide latent output — d\_{c} MACs.

Total 2d\_{c}.

The scoring difference is obvious (d\_{k} against d\_{c}). **The accumulation is the one that is easy to miss**: after expanding you accumulate a d\_{v}-wide v, while absorbing accumulates a d\_{c}-wide latent.

Worth stating plainly: **both paths emit the same o\_{h}**, both d\_{v} wide. That is exactly section 3.2's step — multiplying by W^{V} before the sum and after the sum are equal:

$$ \\sum\_j p\_j \\left( W\_h^{V} c\_j \\right) \\;=\\; W\_h^{V} \\left( \\sum\_j p\_j c\_j \\right) $$

The only difference is which side of the sum W^{V} is applied on. Expanding applies it **first**, once per cached token, so the accumulation is naturally d\_{v} wide. Absorbing applies it **last**, so the accumulation stays on the d\_{c}-wide latent and one final W^{V} brings it back to d\_{v} — and that one runs **once per query token**, not once per pair.

It is the same fact as the K side above: **bracketing changes the cost, not the answer.**

Substituting Kimi K3 (d\_{c} = 512, d\_{k} = d\_{v} = 128): expanding gives 128 + 128 = **256**, absorbing gives 2 × 512 = **1024**.

**For the same query/history pair, absorbing does 4× the arithmetic.** The latent is wide, and dotting against it costs more — that intuition is correct.

The two paths in one sentence: **expanding charges the projection to the history and gets a narrower dot product per pair; absorbing charges it to the query and pays for a wide latent on every pair.**

### 5.2 One query token against one cached token

5.1 only counted the dot products. Each path also has its one projection, and adding it in is what shows who is cheaper at one-to-one.

**Expanding:** turning this cached token's latent into K and V costs d\_{c}(d\_{k} + d\_{v}).

**Absorbing:** folding W^{K} into the query and projecting the output back for this head also costs d\_{c}(d\_{k} + d\_{v}) — **exactly the same**.

For K3 (d\_{c} = 512, d\_{k} = d\_{v} = 128; DeepSeek-V3 has identical widths and only differs at 128 heads instead of 96), both projections come to 512 × 256 = 131072:

**So at one-to-one the outcome is decided entirely by the dot-product column** — 5.1's 4×. The projection column is identical and cancels.

At this point expanding looks like a free win.

### 5.3 Scaling up to S queries and L cached tokens

One-to-one cannot settle it, because in reality the two columns **scale by different factors**.

The dot-product column is straightforward: every query-token × cached-token pair pays it, so it scales with S·L.

The projection column is 5.1's point — **whichever side it lands on is the side whose count it is billed by**:

- expand: W^{K} c\_{j} is done per cached token, **once each**, shared by all query tokens in the batch → scales with L;
- absorb: (W^{K})^{ op} q\_{h} is done per query token, **once each**, shared across the whole history → scales with S.

One clarification: **W^{K} is per head**, not shared across heads — in implementations the up-projection's output dimension is H × (d\_{k} + d\_{v}) (in sglang, kv\_b\_proj is kv\_lora\_rank → num\_heads \* (qk\_nope\_head\_dim + v\_head\_dim)). Expanding one cached token therefore has to be done **once per head**, with no sharing between heads.

But absorbing is per head too: (W^{K})^{ op} q\_{h} is also computed once per head. **Both paths bill their projection per head, so H treats them equally** — which is why arguing on a single head is not biased, and why H cancels out of the crossover later.

Multiplying through by H heads:

$$ F\_{\\text{MHA}} = 2H\\left\[\\, L\\,d\_c(d\_k+d\_v) \\;+\\; S\\,L\\,(d\_k+d\_v) \\,\\right\] $$

$$ F\_{\\text{MLA}} = 2H\\left\[\\, S\\,d\_c(d\_k+d\_v) \\;+\\; S\\,L\\,\\cdot 2d\_c \\,\\right\] $$

The difference is the first term: **expanding multiplies by L, absorbing multiplies by S.** Which is cheaper depends on whether S or L is larger in this forward pass — and decode and prefill sit at opposite ends of that question.

### 5.4 Decode: the MLA algorithm wins outright

In decode S = 1, one new token, and that projection has **nothing to amortize against**.

Substituting Kimi K3's parameters into the two formulas above (96 heads, d\_{c} = 512, d\_{k} = d\_{v} = 128), per **layer**:

**The MLA algorithm wins on both axes**: 120× fewer FLOPs and 71× fewer bytes.

Nor is there room for "use the other one at short sequences". Setting the two equal at S = 1 puts the crossing at L ≈ 1.006 — the MHA algorithm edges ahead only when the history contains a single token, and **from L ≥ 2 onward the MLA algorithm wins throughout**. The reason is plain: a longer L only scales that 120× gap up, it cannot reverse it.

### 5.5 Prefill: the other way around

Prefill computes a large batch of tokens at once, so S equals the sequence length, and the expansion is amortized across thousands of query tokens.

Same K3 parameters, same per layer:

**There is no crossover in prefill — the MHA algorithm wins at every length.** The reason is rather neat: when S = L, the per-token one-off cost is algebraically identical on both paths, 2HL·d\_{c}(d\_{k}+d\_{v}) — the MLA algorithm spends it folding W^{K} into every query and projecting every output back, the MHA algorithm spends it expanding every cached token into K and V. They cancel, leaving only the ratio of the quadratic terms:

$$ \\frac{2d\_c}{d\_k+d\_v} = \\frac{1024}{256} = 4 $$

Longer sequences approach that 4×; shorter ones only shrink the advantage (3× at 2048) without reversing it.

### 5.6 So how large does S have to be?

The previous two sections each computed an extreme: decode at S = 1, where absorbing wins by 128×, and prefill at S in the thousands, where expanding wins by 4×. What about in between — how large does S have to get before you should switch?

The question has a definite answer. In 5.3's two formulas the MLA one grows with S and the MHA one barely does, so there must be some S at which they tie; **that S is the switch point**, and solving F\_{MLA} = F\_{MHA} is how you find it.

First, what it looks like. With K3's parameters and history length fixed at L = 32768, dividing one path's FLOPs by the other — the x-axis is S, the y-axis is the **ratio**, and crossing 1 is where they tie:

At the left end, decode's ratio is only 0.008 — absorbing is more than 100× cheaper. The ratio climbs with S because both of the MLA path's terms carry S, so every extra query token repeats the work, while the MHA path's dominant term is the expansion, which carries only L — extra query tokens are nearly free. The curve crosses 1 at **S ≈ 170**.

Actually solving it shows H cancelling (both paths bill their projection per head, as 5.3 noted), leaving the crossing determined by a few head dims:

$$ S^{\*} = \\frac{a L}{a + (c-e)L}, \\qquad a = d\_c(d\_k+d\_v),\\; c = 2d\_c,\\; e = d\_k+d\_v $$

Substituting in, taking L from 512 up to 128K moves S^{\*} only from 128 to **171**. In other words:

> **what decides the algorithm is how many query tokens this pass computes, not how long the history is**

And because H cancels, DeepSeek-V3 (128 heads) and Kimi K3 (96 heads) have **exactly the same** crossover.

The three vertical lines say the rest: **decode at S = 1 and MTP at 2–8 are pinned far to the left**, while prefill, in the thousands, sits well to the right. Both regimes stay on their own side and almost nothing lands in between — so in practice this is never a "compute it and decide" question, but a straight dispatch on decode versus prefill.

### 5.7 Which is also where AI misleads

Section 1 left a thread hanging: AI only tells you which side of the roofline you are on. Here is the counterexample.

Look again at the decode rows in 5.4's table: **the MHA algorithm's AI is 503, the MLA algorithm's is 193.** Read AI alone and you would pick the MHA algorithm — which in fact does 120× the FLOPs and touches 71× the bytes, both an order of magnitude or two worse. Its AI is higher precisely because **the numerator exploded**, not because it is a better deal.

Prefill fails differently: both paths land at AI in the 10⁵–10⁶ range, so AI only says "both deeply compute-bound" and **cannot discriminate at all**.

One gives the wrong answer, the other gives no answer. So:

> **AI is a ratio; it answers which side of the roofline you are on. To judge which path is faster, you have to put the absolute FLOPs and bytes side by side.**

### 5.8 sglang dispatches exactly this way

This is not a paper exercise. The DeepSeek attention dispatch in [sglang](https://github.com/sgl-project/sglang) (python/sglang/srt/models/deepseek\_common/attention\_backend\_handler.py) switches on forward mode:

- **prefill** goes to MHA\_ONE\_SHOT / MHA\_CHUNKED\_KV, the expanding path;
- **decode, and speculative decoding's verify / draft**, go to MLA, the absorbing path.

Notably, **the decode path does not branch on L at all**: the only place in the dispatch function that looks at sequence length is gated behind the prefill branch. That matches 5.4 — on the decode side there was never a window worth switching in.

---

### 6\. Sparse attention reverses the direction

Section 5's conclusion rests on one premise: attention looks at **all** L cached tokens. DeepSeek-V3.2's DSA, and GLM's equivalent, challenge exactly that premise — a lightweight selector scores the cached tokens and only the top-k actually participate. In V3.2's config that k is index\_topk = 2048.

This is **not symmetric** between the two algorithms:

- **The MLA algorithm benefits from sparsity.** The cache holds individual latents, so whichever 2048 are selected are gathered by index, and the scoring and weighted sum only run over those. The cost goes from L to k.
- **The MHA algorithm does not.** It has to expand the history into K and V and hand it to a dense GEMM — and the operators on that path only offer a dense GEMM, with no selective GEMM that runs on just the chosen tokens. So the expansion is still billed across the whole L.

The longer L gets, the more absurd the gap. With DeepSeek-V3's parameters (128 heads), decode, per layer:

**The sparse path is flat past k; the dense one stays linear.**

So once sparsity is in play, the direction of the choice flips relative to section 5: dense says "the longer the sequence, the more you want the MHA algorithm", sparse says "the longer the sequence, the more you want the MLA algorithm". sglang's DSA dispatch (dsa\_backend.py) confirms it — the MHA algorithm is used only when max\_kv\_len is under a threshold, above which it uses sparse MLA, and decode / verify always go to MLA.

That threshold defaults to **2048** — **exactly** index\_topk. The meaning is clear: below 2048 the top-k selects everything, sparsity buys nothing, and the faster dense kernel is preferable; above it, sparsity finally starts saving something real.

---

### 7\. The four structures side by side

Everything below is BF16, single-token decode, counting only the attention core's one pass over the cached KV, assuming a fused kernel and ignoring softmax / projections / output projection as lower-order terms.

Compressed into a single line:

$$ \\boxed{ 1 \\rightarrow \\frac{H\_q}{H\_{kv}} \\rightarrow H\_q \\rightarrow \\sim2H\_q } $$

I find this view more unifying than "how much KV cache does variant X save":

> **A large part of how attention architectures have evolved is the design of data reuse. GQA and MQA reuse KV across query heads; MLA goes further and has one latent serve as both K and V.**

---

### 8\. Why MLA and MTP fight each other

Now the opening quote can be revisited.

Ordinary autoregressive decode has one query token per step. The systems intuition behind MTP and speculative decoding is: since the KV cache has already been dragged in from HBM, can it serve several candidate tokens at once?

Say one verification step uses the same cached history to serve S query positions. To a very rough approximation the HBM traffic does not grow proportionally with S while the QK/PV computation scales nearly linearly with it, so:

$$ AI(S)\\approx S\\cdot AI(S=1) $$

For plain MQA:

$$ AI\_{\\text{MQA}}\\approx SH $$

and for MLA:

$$ AI\_{\\text{MLA}} \\approx SH\\frac{2d\_c+d\_s}{d\_c+d\_s} $$

This also answers a question in passing: MTP lifts the query token count from 1 to S, so does it push past section 5's crossover and switch to the MHA algorithm? **No.** Speculation windows are typically 2 to 8, at most a few dozen, nowhere near 171. So MTP **stays on the MLA-algorithm side** — every query token still runs against the wide latent. Which is exactly why its AI climbs faithfully with S.

In other words, **MTP and MLA are spending the same resource: the GPU compute left idle by a memory-bound decode.**

- MLA spends extra compute to buy stronger cache reuse;
- MTP spends extra speculative / verification compute to buy fewer serial decoding steps.

If the workload were a low-AI MQA, say AI ≈ 70–100, the GPU is far from the roofline knee and MTP's extra arithmetic is largely using tensor cores that were idle anyway.

But DeepSeek-style MLA already reaches, at a single query:

$$ 256\\ \\text{FLOP/B} $$

and Kimi K3's MLA layer:

$$ 192\\ \\text{FLOP/B} $$

Against the theoretical balance points above — H200 at ~206 FLOP/B, H100 and B200 in the two-to-three-hundred range.

So at S = 1 MLA has already moved decode from clearly memory-bound to roughly the compute/memory balance point. Take S to 2:

$$ \\text{DeepSeek: }256\\rightarrow512 $$

$$ \\text{Kimi K3: }192\\rightarrow384 $$

and it sails past the roofline knee into compute-bound territory.

At that point MTP's extra arithmetic is no longer using otherwise idle compute; it starts costing real latency.

So the opening claim — that MLA behaves during decoding like an MQA with head\_dims=512+ and has already consumed most of the compute — reduces, as I now understand it, to:

> **MLA and MTP are both making a compute-for-bandwidth / compute-for-latency trade. MLA has already spent a large part of decode's idle compute headroom, leaving less of it free for MTP.**

Mathematically, MLA's AI is "only" a constant factor under 2 above MQA's. Systems-wise, that constant is exactly enough to push the workload across the roofline.

Which is the part I find most interesting.

### Acknowledgements

Thanks to [Yangmin](https://yamy1234.github.io/) for the insights and discussion on MLA inference.

After finishing this I found that Zyphra's [Compressed Convolutional Attention](https://arxiv.org/abs/2510.04476) (arXiv:2510.04476) states the same thing independently, in nearly the same terms:

> MLA has an arithmetic intensity of 2n\_heads at inference time, which is very large, and targets the ridge of the roofline plot on a H100 for a single query.... The arithmetic intensity required to breach the ridge of the roofline for an Nvidia H100 under bfloat16 is 295 FLOPs per byte. Deepseek seemingly chose their number of heads for the DeepseekV3 model to accordingly saturate the roofline to approach compute bound inference at batch size 1.... This falls short in cases where speculative decoding is utilized such that the arithmetic intensity passes the roofline.

AI = 2H, 295 FLOP/B, and "DeepSeek picked their head count against the roofline" — all three line up. It also raises an angle this post does not cover: **MLA also loses under tensor parallelism**, because the shared KV has to be replicated per TP rank, which gives back the reuse MQA had bought.

One more line from that paper, which closes section 5's observation about AI nicely:

> while MLA is capable of better compute utilization on decode, the increase in FLOPs that would otherwise go unused does not automatically result in victory. Model quality and latency, not SM utilization, is the end goal.

---

### Appendix A: putting RoPE back

The AI = 2H above is the cleanest form of the result, but it rests on ignoring RoPE. Here it comes back.

The problem is at 3.1's absorption step, which relies on associativity to move W^{K} over to the query side. RoPE is a **position-dependent** rotation sitting between query and key, and the two sides are rotated by different angles, so that regrouping no longer works — with RoPE in place you cannot score against the latent directly.

DeepSeek's answer is a division of labor: the latent part is absorbed as usual and carries no RoPE, while a separate small segment of RoPE-carrying key is kept, shared by all heads and stored in the cache alongside the latent. That segment only participates in scoring, not in the final weighted sum (it has no corresponding Value).

Writing its width as:

$$ d\_s $$

each cached token's real width is:

$$ d\_c+d\_s $$

the QK contraction width is:

$$ d\_c+d\_s $$

and the PV contraction width is still only:

$$ d\_c $$

so:

$$ F = 2HL(d\_c+d\_s)+2HLd\_c $$

that is:

$$ \\boxed{ F=2HL(2d\_c+d\_s) } $$

HBM traffic:

$$ \\boxed{ B=bL(d\_c+d\_s) } $$

giving:

$$ \\boxed{ AI\_{\\text{MLA}} = \\frac{2H}{b} \\frac{2d\_c+d\_s}{d\_c+d\_s} } $$

and with BF16:

$$ \\boxed{ AI\_{\\text{MLA,BF16}} = H \\frac{2d\_c+d\_s}{d\_c+d\_s} } $$

When d\_{s} ≪ d\_{c} the factor naturally approaches:

$$ 2H $$

### A.1 DeepSeek V3 / R1

From the [DeepSeek-V3 config](https://huggingface.co/deepseek-ai/DeepSeek-V3/blob/main/config.json):

$$ H=128,\\quad d\_c=512,\\quad d\_s=64 $$

so:

$$ AI = 128\\times\\frac{2\\times512+64}{512+64} $$

$$ \\boxed{ AI\_{\\text{DeepSeek MLA}}\\approx241.8\\ \\text{FLOP/B} } $$

### A.2 Kimi K3

From the [Kimi K3 config](https://huggingface.co/moonshotai/Kimi-K3/blob/main/config.json) 's MLA layer:

$$ H=96,\\quad d\_c=512,\\quad d\_s=64 $$

so:

$$ AI = 96\\times\\frac{1088}{576} $$

$$ \\boxed{ AI\_{\\text{Kimi K3 MLA}}\\approx181.3\\ \\text{FLOP/B} } $$

K3 has an implementation quirk: the config keeps the qk\_rope\_head\_dim=64 layout but also sets mla\_use\_nope=true, so those 64 dims are not actually doing RoPE. That does not affect the derivation here — all we need is that it is likewise a small segment **shared by all heads, participating only in scoring and not in the weighted sum**, 64 wide, substituted into the formulas above.

---

### A.3 Section 5s numbers

Section 5's comparison of the two algorithms used the same simplification. Adding the segment back:

The expansion is unchanged, because the segment is shared across heads and does not need expanding per head. Both per-pair costs widen, so the ratio drops from 4 to 3.4, and the MHA algorithm's prefill advantage drops from about 3.9× to about 3.3×.

**The crossover does not move at all**: it is the expansion divided by the per-pair *difference*, and that difference is 1024 − 256 = 768 before and 1088 − 320 = 768 after — identical. So S^{\*} ≈ 171 is unaffected.