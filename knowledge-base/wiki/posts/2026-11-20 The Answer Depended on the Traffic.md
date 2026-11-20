---
type: social-post
created: 2026-11-20
updated: 2026-11-20
tags:
  - post
  - inference
  - reproducibility
platforms:
  - linkedin
  - x
pages_used:
  - "[[Inference Determinism]]"
  - "[[Nathan Barry - Eliminating Nondeterminism in LLM Inference with Integer-Only Arithmetic]]"
  - "[[Weight-Space Programming]]"
  - "[[Lex Toumbourou - Weight-Space Programming Builds Neural Networks Like a 1990s Researcher]]"
  - "[[Jacob Strauss - Experiments in Weight-Space Programming]]"
  - "[[OpenRouter - MCP vs CLI vs Skills - What Each Costs in Context]]"
  - "[[Will DePue - Chinese Frontier Models Carry Blackwell GPU Fingerprints]]"
  - "[[Thinking Machines - End-to-End 4-Bit Training]]"
  - "[[Ashish Subedi - Why Antigravity Eats Weekly Quota Fast]]"
topics:
  - inference determinism
  - floating-point reproducibility
  - batch-dependent outputs
  - single-run evaluation
covers_from: 2026-11-13
covers_through: 2026-11-20
status: ready
---

# The Answer Depended on the Traffic

## LinkedIn post

Turn an AI model's randomness all the way down and ask it the same question twice. You would expect the same answer twice. You may not get it, and the cause can be other people's traffic on the server rather than the model.

Models do their maths with decimals stored at limited precision, called floating point. Every addition rounds a little, so order matters: (a + b) + c and a + (b + c) can round differently.

A model adds up thousands of numbers for every word it writes. The cause is mostly not random timing inside the chip: most of these calculations return the same bits when repeated on the same inputs. What changes is the batch. A shared server processes your request alongside other people's, and the maths library splits the sums differently depending on batch size. As Nathan Barry puts it, "your output depends on traffic you can't see or control."

How big is the effect? Barry relays a result from the AI lab Thinking Machines: one prompt sent 1,000 times with randomness off returned 80 different answers. Their fix forces one fixed order. All 1,000 then matched, at about a 20% slowdown in the core calculation, but only on one type of chip running their code.

Barry's proof of concept, DetLLM, is blunter: drop decimals. Whole-number addition is exact, so order cannot matter. He ran a small open model, Qwen3-0.6B, entirely in whole numbers and tested one prompt in nine setups: different batch sizes, different prompt chunking, two NVIDIA GPUs, and CPUs from AMD, Intel and Apple. Every whole-number run produced the same fingerprint of the model's internal scores. The usual 16-bit decimal runs produced nine different ones.

The twist: eight of those nine decimal runs still wrote the same 512 tokens (word pieces). The model picks its top-scoring option, so drift matters only when two options are close. At the first step, drift was at most 0.094 against a 2.66 lead, a cushion Barry calls unusually generous. Later, 45 of the 512 steps had leads under 0.5, and at step 457 one run hit an exact tie and the text forked. The variation was hidden, not absent, and longer answers give it more chances.

The limits: one author, one small model, one prompt. Reading the prompt still runs at about 0.13 times the 16-bit speed, and converting a model to whole numbers is not itself reproducible, so the guarantee covers one prepared copy. The 80-in-1,000 figure is secondhand.

So treat "randomness off" as removing the dice, not the drift. When an evaluation or incident replay rests on one run, re-run it and record the exact setup, because a single run partly measures the server.

Where would a different answer to the same input hurt you most?

Source: Nathan Barry, "Eliminating Nondeterminism in LLM Inference with Integer-Only Arithmetic"
https://nathan.rs/posts/detllm/

#Reproducibility #LLMInference #MLOps

## X post

Counts include spaces and punctuation; each URL counts as 23 characters under X's link
weighting. Number labels, counts, and code fences are outside the copy-ready text.

**A) Standalone** (274 chars):

```text
AI randomness off, same prompt, different answers: rounding depends on addition order, and server batch size changes that order. Nathan Barry ran a small model in whole numbers: 9 setups, 1 identical result (one prompt). Re-run before trusting a run. https://nathan.rs/posts/detllm/
```

**B) Thread:**

1. (199 chars)

```text
Turn an AI model's randomness to zero ("temperature 0") and send the same prompt again. You can still get a different answer, and the cause can be other people's traffic on the server, not the model.
```

2. (267 chars)

```text
Why: models do maths in limited-precision decimals. Each addition rounds, so (a+b)+c and a+(b+c) can round differently. Servers batch your request with others, and batch size changes how the sums are split. New order, new rounding, occasionally a different next word.
```

3. (264 chars)

```text
How often? Nathan Barry relays a Thinking Machines result: one prompt sent 1,000 times with randomness off gave 80 different answers. Their fix pins the order: all 1,000 matched, at about a 20% slower core calculation, but only on one chip type running their code.
```

4. (271 chars)

```text
Barry's DetLLM drops decimals: whole-number addition is exact, so order can't matter. A small model (Qwen3-0.6B), one prompt, nine setups: batch sizes, chunking, 2 NVIDIA GPUs, 3 CPUs. Whole numbers: one identical fingerprint of the model's scores. 16-bit decimals: nine.
```

5. (243 chars)

```text
Twist: 8 of the 9 decimal runs still wrote the same 512 tokens. The model picks its top option, so drift matters only in close calls. 45 of 512 steps were close, and at step 457 one run hit an exact tie and the text forked. Hidden, not absent.
```

6. (249 chars)

```text
Limits: one author, one small model, one prompt. Reading the prompt runs at about 0.13x the 16-bit speed, and the guarantee covers only one converted copy of the model, because the conversion isn't reproducible. The 80-in-1,000 figure is secondhand.
```

7. (217 chars)

```text
So "randomness off" removes the dice, not the drift. If an eval or incident replay rests on one run, re-run it and record the exact setup: a single run partly measures the server. Nathan Barry: https://nathan.rs/posts/detllm/
```

**Ship:** Thread. It defines "randomness off" before the surprise, explains rounding and
batching before any number, separates Thinking Machines' secondhand 80-in-1,000 result
from Barry's own nine-setup test, and keeps the one-model, one-prompt, speed, and
per-copy caveats in the penultimate post. The standalone keeps the situation, the
rounding-order mechanism, the batch cause, the nine-setup result with its one-prompt
scope, and the action, but drops the 80-in-1,000 scale, the latent-tie twist, and the
speed cost.

## Hook variants

1. **Plain situation:** Turn an AI model's randomness all the way down and ask it the same question twice. You may not get the same answer, and the cause can be other people's traffic on the server.
2. **Concrete number:** One prompt, sent 1,000 times with randomness off, came back as 80 different answers.
3. **Myth correction:** "Temperature 0" removes the dice, not the drift.

**Recommended:** The plain situation for LinkedIn and X post 1: it starts from an expectation
every reader shares and names the unexpected cause before any jargon. The number is kept for
the third paragraph and post 3 because it is secondhand and needs its attribution beside it;
the myth correction closes both variants as the takeaway.

## Why this topic

**Window:** 2026-11-13 through 2026-11-20, inclusive, anchored to the newest active ready
post's `covers_through`. The November 13 ingest and lint entries precede that post in the
log and were scored in the previous run. Two entries follow it: the November 20 "Derived
Kernels, 4-Bit Training, and Weights Written by Reasoning" ingest (30 sources) and the
November 20 "Scoped Claims, Restored Hedges, and a Team Byline" lint pass, which added no
source. The Git cross-check covered 18 commits and 41 changed source-summary paths since
the previous run: 24 November 13 summaries and 17 older ones that gained only links or
lint corrections. The 30 November 20 summaries are in the uncommitted working tree. No
unlogged source summary appeared.

Four ByteByteGo items were excluded before scoring: EP233 on Kubernetes, the overthinking
explainer, the Instacart query-understanding article, and the Shankar and Husain Evals
excerpt that ByteByteGo published. The off-domain smart-TV capture has no summary. That
left 26 eligible sources.

Scores are editorial judgments, 1-5. Clarity and completeness must each be at least 4;
a high total cannot override either gate.

| Angle and source | Clarity | Completeness | Surprise | Concreteness | Reach | Freshness | Total | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| With randomness off, the same prompt can still change answers because server batching changes the order of rounded additions; whole-number arithmetic removes it - [[Nathan Barry - Eliminating Nondeterminism in LLM Inference with Integer-Only Arithmetic]] | 5 | 5 | 5 | 5 | 4 | 5 | 29 | Selected: one test with a plain mechanism (rounding order), one memorable twist (a hidden tie at step 457), limits stated by the author, and a direct practical consequence for evaluation. |
| Asked to write a network's weights by hand, a model rebuilt a 1990s handwriting pipeline; writing works where a compact known algorithm exists - [[Lex Toumbourou - Weight-Space Programming Builds Neural Networks Like a 1990s Researcher]], with [[Jacob Strauss - Experiments in Weight-Space Programming]] | 4 | 4 | 5 | 4 | 4 | 5 | 26 | Eligible runner-up; a cold reader first needs weights and gradient descent, and the "metric did the fitting" point is subtle. |
| Reaching GitHub through a standard tool server cost 59,417 input tokens where the command line cost 1,421 - [[OpenRouter - MCP vs CLI vs Skills - What Each Costs in Context]] | 4 | 4 | 4 | 5 | 4 | 3 | 24 | Eligible but weaker: a vendor post, "one server on one task", a promotional Tool Search section, and context-cost territory close to the September 5, September 18, and October 30 posts. |
| Six open models' starting weights match Blackwell GPUs - [[Will DePue - Chinese Frontier Models Carry Blackwell GPU Fingerprints]] | 3 | 3 | 5 | 4 | 4 | 5 | 24 | Rejected by both gates: the initialization fingerprint needs specialist explanation, and the report itself does not establish where the chips were or whether export controls were violated. |
| A theoretical 3x speedup became 8% in pretraining and 20% in RL - [[Thinking Machines - End-to-End 4-Bit Training]] | 3 | 3 | 4 | 4 | 3 | 5 | 22 | Rejected by both gates: 4-bit and 8-bit formats and expert layers need explaining, the 3x applies only to one theoretical pass, and the first-party post gives no model size or ablation. |
| A coding agent's weekly quota drains when the provider's cache expires during pauses - [[Ashish Subedi - Why Antigravity Eats Weekly Quota Fast]] | 4 | 4 | 4 | 4 | 4 | 2 | 22 | Not selected: its natural spine, [[KV Cache]], is in cooldown until 2026-11-27, and the October 16 and October 30 posts covered cache reuse. |

The selected spine is [[Inference Determinism]], a new concept page created on 2026-11-20.
It is mixed-source: its "roughly 80 distinct completions" sentence cites a ByteByteGo article
first and Barry second. The public copy relies only on Barry's capture, which states the
1,000-prompt, 80-answer result itself with its Thinking Machines attribution; no ByteByteGo
page supports any public sentence.

**Anti-repeat:** No earlier post used this spine or covered inference determinism. The
September 11 post concerned how serving benchmarks are normalized, not whether the same
request is reproducible. The archive's "temperature 0 is not deterministic" candidate was
listed with pass@k under [[Multi-Turn Evaluation]] but never drafted, and its 80-completions
support there is ByteByteGo-sourced; this post replaces that support with Barry's direct
account and his new test, so the old candidate is retired.

## Reader check

**Passed:** reread the LinkedIn body, standalone, and connected thread without relying
on these notes. Each preserves the situation, claim, example, mechanism, limit, and action.

| Cold-reader question | LinkedIn and thread | Standalone |
|---|---|---|
| What is the situation? | Asking an AI model the same question with randomness turned off and expecting the same answer. | The same, in one clause. |
| What is the single claim? | Answers can still differ because rounding depends on addition order, and other people's requests in the same server batch change that order. | Rounding depends on addition order, and batch size changes it. |
| What example supports it? | Thinking Machines' 80 answers from 1,000 sends (secondhand); Barry's nine setups giving one fingerprint in whole numbers and nine in 16-bit decimals; the tie at step 457. | Barry's nine setups and one identical result. |
| Why did it happen? | Decimal additions round, so order matters; servers split sums differently by batch size; small drift changes a word only when the top two options are nearly tied. | Rounding plus batch-dependent order. |
| What is the limit? | One author, one small model, one prompt; slow prompt reading; a guarantee for one prepared copy; the 80-in-1,000 figure is secondhand. | "(one prompt)". |
| What should change? | Treat "randomness off" as not reproducible; re-run single-run evaluations or replays and record the setup. | Re-run before trusting a run. |

"Floating point" is introduced after its plain meaning. "Tokens" is glossed as word pieces.
"Temperature 0" appears only on X, defined on first use as randomness set to zero. The
fingerprint is described as a fingerprint of the model's internal scores; "hash", "logits",
"batch invariance", "kernels", "greedy decoding", "prefill", and "quantization" are not used.
GPU and CPU are left as common hardware names. The LinkedIn conclusion completes the argument
before the closing question.

## Fact check

**Passed:** checked every public factual sentence against Barry's raw capture,
[[Nathan Barry - Eliminating Nondeterminism in LLM Inference with Integer-Only Arithmetic]], and [[Inference Determinism]]. LinkedIn has 477 words including attribution and
hashtags, above the usual 450 because the twist and the limits paragraph were kept rather
than cut. The X standalone is 274 characters; the seven thread posts are
199, 267, 264, 271, 243, 249, and 217 characters under the
declared link weighting. The public copy is ASCII.

| Public claim group | Direct support and boundary |
|---|---|
| With randomness off (temperature 0), a model picks its most likely next token, yet one prompt sent 1,000 times gave 80 different answers | Raw opening: "at temperature 0 a model always picks its single most likely next token ... when they sent one prompt 1,000 times, they got 80 different answers." Credited in both variants as Thinking Machines' result relayed by Barry, and labelled secondhand in both. |
| Decimal (floating-point) addition rounds, so (a + b) + c and a + (b + c) can round differently; a model adds thousands of numbers per word | Raw: "floating-point addition is not associative. (a + b) + c and a + (b + c) can round differently. A GPU sums thousands of numbers for every token." "Word" is the plain-language stand-in for token. |
| The cause is mostly not random timing; most calculations repeat bit-for-bit; what changes is the batch | Raw: atomic-add races are "mostly not what goes on in an LLM forward pass ... Most inference kernels are run-to-run deterministic. What they aren't is batch invariant." The hedge "mostly" is kept on LinkedIn; X states only the batch cause. |
| A shared server batches your request with others, and the maths library splits sums differently by batch size; quote | Raw cuBLAS paragraph ("picks one based on the problem's shape"; small batches split the reduction) and the verbatim quotation "your output depends on traffic you can't see or control." Prompt chunking and cache splitting are further causes in the raw; the post mentions chunking only as a test setup. |
| Thinking Machines' fix forces one order; all 1,000 then matched at about a 20% slowdown in the core calculation, only on one chip type with their code | Raw: "batch-invariant kernels fix every reduction's order ... at about a 20% matmul slowdown, and all 1,000 of their completions came back identical" and "That works, but only on that GPU with those kernels." "Core calculation" glosses matrix multiplication. Secondhand. |
| DetLLM drops decimals; whole-number addition is exact so order cannot matter; Qwen3-0.6B entirely in whole numbers | Raw: "Integer addition is associative"; "DetLLM runs Qwen3-0.6B with exact integer arithmetic for every operation between the input ids and the int32 logits." Overflow is bounded in advance per the raw, so "exact" is the author's claim as stated. |
| One prompt, nine setups: batch sizes, prompt chunking, two NVIDIA GPUs, CPUs from AMD, Intel and Apple; whole numbers gave one fingerprint, 16-bit decimals nine | Raw demo paragraph and table: batch 1, batch 8 with seven random co-prompts, split prefill then token-by-token, CPU-only; A100, H100, AMD EPYC 7J13, Intel Xeon 8480+, Apple M1 Pro; all int8 runs `64430dd985f8`, nine distinct fp16 hashes. The fingerprint is the chain hash of the logits at every step. |
| Eight of nine decimal runs still wrote the same 512 tokens; drift matters only when the top two options are close; 0.094 against a 2.66 lead at the first step, "unusually generous"; 45 of 512 steps under 0.5; an exact tie at step 457 forked the text; hidden, not absent; longer answers give more chances | Raw twist paragraphs, numbers verbatim; "Float nondeterminism is usually latent, not absent"; "the longer the generation, the more likely it forks." The tie is on the M1 Pro; the post does not name the device. |
| Limits: one author, one small model, one prompt | Summary "Scale" tension; all results are the author's own. |
| Reading the prompt runs at about 0.13 times the 16-bit speed | Raw footnote 10: int8 prefill "still runs at about 0.13x fp16". The decode speedups are omitted because the author calls that comparison "Not an apples-to-apples comparison". |
| Converting to whole numbers is not itself reproducible, so the guarantee covers one prepared copy | Raw: "The guarantee is tied to one prepared artifact, since the float-to-int conversion isn't itself reproducible." |
| Treat randomness off as not reproducible; re-run single-run evaluations or replays and record the setup, because a single run partly measures the server | The post's conclusion from Barry's quotation that output depends on server traffic. It is presented as practical advice, not a measured finding; it does not rest on the ByteByteGo-sourced single-run sentence on [[Multi-Turn Evaluation]]. |

**Attribution and exclusion:** The LinkedIn source line and the final X post name Nathan
Barry, matching the summary's `source_author`, and use the canonical URL without the
capture's tracking parameter. Thinking Machines is credited for its own result, as Barry
credits it. The raw capture is Barry's own blog post and contains no ByteByteGo reference.
All nine `pages_used` entries are tracked and outside `wiki/queries/`; the seven unselected
pages support only the editorial shortlist.

**Claims cut rather than compressed:**

- Quality on two text-prediction tests (one slightly better, one 0.4% worse): true, but it
  needs the perplexity metric explained and does not change the argument.
- Decode speedups (0.8 to 106.3 tokens per second): the author says the baseline is not
  comparable.
- The 79-test suite: the CPU rows rest on the hash table rather than the suite.
- The "first pipeline" novelty claim: self-assessed "to my knowledge".
- The NeurIPS workshop papers, the hackathon origin, and the bug-fix footnote: not needed.
- DeepSeek's deterministic engine setting and Cam Pedersen's accuracy gate on
  [[Inference Determinism]]: a second and third system would dilute the one example.

**Compression check:** The standalone keeps "(one prompt)" and presents the result as a
small model's test, not a general guarantee, and does not repeat the secondhand
80-in-1,000 figure. The thread keeps "relays", the 20% cost and its one-chip limit, the
"8 of the 9" qualifier, and every limit in post 6. No version claims that the tie occurs
often in real workloads; the vault records that as unmeasured.

**Comprehension check:** Each version explains why rounding order matters and why other
people's traffic changes it before giving any result. The thread's sequence is situation,
mechanism, scale, test, twist, limits, and action. No number needs these notes to make
sense.

## Attribution

Public example and all empirical claims: **Nathan Barry**, "Eliminating Nondeterminism in
LLM Inference with Integer-Only Arithmetic" - https://nathan.rs/posts/detllm/

Thinking Machines' 1,000-prompt result and 20% cost are credited to Thinking Machines as
relayed by Barry; their original post is not in the vault.

Direct source: [[Nathan Barry - Eliminating Nondeterminism in LLM Inference with Integer-Only Arithmetic]].
Primary capture: [[knowledge-base/raw/sources/Eliminating Nondeterminism in LLM Inference with Integer-Only Arithmetic]].
Wiki synthesis: [[Inference Determinism]].

The other source pages in `pages_used` document the scored editorial alternatives.
They are not additional public examples or evidence.

## Hashtags

LinkedIn: `#Reproducibility #LLMInference #MLOps`

X: none.

## Related pages

- [[Post Archive]]
- [[Inference Determinism]]
- [[Nathan Barry - Eliminating Nondeterminism in LLM Inference with Integer-Only Arithmetic]]
- [[Weight-Space Programming]]
- [[Lex Toumbourou - Weight-Space Programming Builds Neural Networks Like a 1990s Researcher]]
- [[Jacob Strauss - Experiments in Weight-Space Programming]]
- [[OpenRouter - MCP vs CLI vs Skills - What Each Costs in Context]]
- [[Will DePue - Chinese Frontier Models Carry Blackwell GPU Fingerprints]]
- [[Thinking Machines - End-to-End 4-Bit Training]]
- [[Ashish Subedi - Why Antigravity Eats Weekly Quota Fast]]
