---
type: raw-source
source_id: src-2026-08-20-liquid-ai-production-loops
title: Designing Loops for Production-Grade Work
author: Liquid AI
url: https://www.liquid.ai/blog/agent-loops
published: 2026-08-18
captured: 2026-08-20
status: immutable
tags:
  - source/raw
  - agents
  - loop-engineering
  - evaluation
---

> Preserve the source body below this line as the canonical capture.
In late 2025, we ran an experiment to answer one question: *“Can coding agents autonomously solve a production-grade problem from scratch on their own?”*

For this, we tasked two agents with the (at that time) best publicly available coding models with a real problem and a real deadline. The result of this experiment is a tokenizer trainer called `toktoktok`, and is now open source on [GitHub](https://github.com/Liquid4All/toktoktok).

In this article, we share what we learned about designing effective loops that allow agents to autonomously solve production-grade problems: how to specify a goal for multi-domain experts and how to set up the verification infrastructure.

## Why testing autonomy needs a real target

As part of [our research on the impact of vocabulary size on edge LLMs](https://www.liquid.ai/blog/tokenizer-expansion), we needed a byte-pair encoding (BPE) tokenizer trainer that could run trillions of tokens on a single machine. However, the tokenizer training landscape is thin:`sentencepiece` was optimized for non-BPE tokenizers and is slow, Hugging Face `tokenizers` ran out of memory on our corpora, and `tiktoken` has no training capability at all.

That’s why we needed to **build a production-grade BPE tokenizer trainer**. From our experience with existing libraries, we also knew **memory size was the real bottleneck**, and they were missing two features we needed: a warm start from an existing tokenizer (vocabulary extension) and a per-language vocabulary budget. This gave us a concrete task, with a real deadline, and an effective way to answer whether coding agents are reliable enough to autonomously solve a task, because it met the following criteria:

**Production-grade.** How agents are commonly used to autonomously solve a problem can't answer this question. First, they are often used for prototyping and never held to a production bar. Second, they reimplement something already existing in a different language, such as “Port SQLite to Rust” or “write a C compiler in Zig,” which is a translation of something the model has likely seen during pretraining. Unlike either of these, ours had a clear ship-to-production goal, and because BPE tokenizer training is recent enough with few public reference implementations, it made an ideal “test distribution” problem sample.

**Multi-domain expertise.** At Liquid AI, our experts run deep, but each in a single domain. Our ML researchers can tell you from memory why OpenAI’s cl100k reserves ranks for every three-digit number, but they’ve never written a line of Rust. Our Rust engineers write exactly the kind of memory-aware, multi-threaded systems code this problem needs, but they’ve never trained a tokenizer.

These are two disjoint sets of people, and neither can solve this problem alone. Both human workarounds are lossy: either one of them learns the other’s half first, or we staff it as a collaboration and pay the coordination overhead instead. This is the gap we pointed the agent at: “C *an it cover a span of expertise no single one of our engineers has?*"

**Externally verifiable.** The artifact must load in tiktoken and Hugging Face tokenizers. Because of this interoperability with third-party software, the work can be checked by code the agent can’t modify. Success isn’t self-reported but rather whether two third-party libraries either produce the right tokens or not.

While the [details of what had to be built](https://github.com/Liquid4All/toktoktok) are interesting on their own, what matters for this article is that a task that is real production-grade, hard for our single-domain experts, and externally verifiable is the only honest way to answer whether an agent can do the job without any human oversight.

## Setting up the experiment

For this experiment, we chose Claude Opus 4.5 and Codex with GPT-5.2, the two strongest publicly available coding models in late 2025, as the coding agents and let both work in their planning modes. Before either agent wrote a single line of code, we set up two things around it: a goal to aim at, and a way to verify whether it had gotten there.

![Experiment setup](https://www.liquid.ai/_next/image?url=https%3A%2F%2Faypchzzf9pftwuto.public.blob.vercel-storage.com%2Fpasted-image-2NLk3YRs8pp7FJL5igHxyM2VAVC1gl.png&w=3840&q=75)

Experiment setup

The **goal** is described in a specification file. It's a single `AGENTS.md` / `CLAUDE.md` document written by the operator, describing the outcome and its constraints, not an implementation: The primary architectural constraint is memory. The design spends its complexity budget on memory, so a corpus far larger than RAM stays fairly represented. Compute and I/O are secondary and get straightforward treatment: a system-level programming language (Rust) and multi-threading should be sufficient.

To **verify** whether the agent has reached the specified goal, we gave it two things it couldn’t influence:

- **Production data**:We gave the agents sandboxed access to our production training dataset and a machine capable of handling it, specifically an AMD EPYC 9755 with 128 cores, 256 threads, and 2 TB of memory.
- **External verification harness**: The trained vocabulary had to be loaded by `tiktoken` and Hugging Face `tokenizers`, and checked both for encode and decode round trips and for ID-level agreement between the two, across multiple languages, numbers, currency formatting, tabs, CRLF line endings, and source code.

With these components in place, the agent could work toward the specified goal.

## What happened when we ran it

We ran the experiment with both coding agents. The operator monitored from the outside, reading only the harness but never a single line of code.

### Both zero-shot the toy trainer

**Both agents produced a working trainer within 30 minutes**.They parsed the config, walked the corpus, applied the hardcoded merges, ran the BPE training, and emitted a valid`.tiktoken` file that passed their own unit tests.

**Both could successfully train toy tokenizers on a few megabytes**.The artifacts loaded in `tiktoken`. All tests passed. If we stopped the evaluation at this point, the conclusion would be both runs are a success.

### Neither scaled to production without loops

However, neither trainer survived the full production dataset. In the first run, every unit test passed at every stage, because a few megabytes of clean text triggers none of the following:

| **What had to be discovered** | **How it announced itself** | **What caught it** | **Effort to fix** |
| --- | --- | --- | --- |
| **File encodings.** Parquet permits several encodings for the same logical column. | Files that read fine in testing are silently mishandled in the corpus | real corpus files | hours |
| **Memory awareness.** Per-document Vec overhead swamps the payload | Out of memory at roughly 1% of the target corpus | full scale run | two to three days: chunk batching, sentinels, multi-segment iteration |
| **Improper parallelization.** Parallelizing part of the critical path leaves the rest sequential | Every core busy, throughput still unacceptable | full scale run | one to two days |
| **Pre-tokenization speed.** `\s+(?!\S)` forces a backtracking regex engine | Profiler shows pre-tokenization dominating; adversarial whitespace goes quadratic | full scale run | hours, plus a correctness judgment call |
| **Rank ordering.** `tiktoken` derives merge order from rank order, so ranks must be contiguous | Vocabulary loads without complaint and encodes differently than intended | external harness | hours |
| **Duplicate merges.** A trained merge can duplicate an existing token and collapse the vocabulary | Vocabulary is short by N and every later rank shifts | external harness | hours |
| **Number encoding.** Rust's regex crate reparses `{1,3}+` as `({1,3})+` | `tokenizers` and `tiktoken` agree on everything except numbers | external harness | one line |

Then, we let the agents loop against the real data: execute, hit a wall, report the symptom, let the agent diagnose and fix, run again.

After more than five iterations with little progress, we stopped work on the Codex/GPT-5.2 track, which was still struggling with training throughput. That was a resourcing decision: one operator, a real deadline, and by that point the Claude Opus 4.5 track was further along after the same number of turns. Our read was that Claude's first version started from a better place by picking up the nuances of the specification and the intent behind the constraints more reliably than GPT-5.2.

Claude Opus 4.5 closed out the remaining issues over a handful of further iterations and produced a trainer that ran the full production configuration: trillions of tokens of multilingual and code data, multi-phase, on a single machine, completing in a few days. The output passed the external harness cleanly.

## Why the loop was necessary

We ran this experiment to answer the question, *“Can coding agents solve a production-grade problem from scratch on their own?”* It's tempting to read "neither agent zero-shot it" as a story about model capability, but this is the wrong conclusion. By the bar we had set at the start, **the experiment succeeded**. However, what got it there was not any single clever turn but the loop.

![Closing the loop](https://www.liquid.ai/_next/image?url=https%3A%2F%2Faypchzzf9pftwuto.public.blob.vercel-storage.com%2Fpasted-image-1P2VxXqqASGGPB3S9CvXY4DMlcOSvd.png&w=3840&q=75)

Closing the loop

The two thousand lines in this repository aren't an artifact of a zero-shot response but the residue of an iterative process. Almost every non-obvious line is cheap to write once you know it needs writing, and the expensive part is knowing that it needs writing at all.

That means whether or not an agent can successfully achieve a goal without human oversight depends on having an iteration loop that converges against the constraints of the real environment. This allows the agent to iteratively discover and experience the messiness of the real world.

## Lessons from running an autonomous loop

From this experiment we learned that coding agents are able to autonomously solve a task with a loop, but more importantly, we learned two valuable lessons on how to design effective loops, which have become everyday practice on our engineering team today.

### Specify goals for multi-domain experts

From the experiment, we learned that coding agents are multi-domain experts, covering a span of expertise none of our engineers have. Turns out it knew OpenAI's cl100k regex, and it knew Rust’s `rayon`. Nobody we could have staffed on this knew both. This changes how we can specify the goals because it feels more like talking to a colleague from the other team who happens to also know your team's material.

Consider what it would actually take to hand this problem to a strong software engineer with no tokenizer background. The obvious answer is to write them a detailed spec. This is the classic bind of expertise transfer: Write the spec too short, and the engineer has to discover all of it the slow way. Write it long enough to be genuinely actionable, and you have written pseudocode, at which point you needed the domain knowledge yourself and could nearly have done the work.

An LLM isn't in that bind, because it arrives with the background already installed. That changes what a specification is. Ours was short. It stated outcomes and constraints rather than mechanisms.

Take a real example from our spec: *“reserve vocabulary for all two- and three-digit numbers before training starts”*. To an engineer without the background, this is an arbitrary requirement. They can implement it literally and still get it wrong, because the sentence doesn’t carry its own motivation. It’s about giving the model a consistent numeric representation so arithmetic doesn’t depend on which digit pairs happened to be frequent in the corpus, e.g., think of GPT-2’s tokenizer that has a unique *2019* token but not a *2029* one due to frequency in the training data. Not knowing that, they can’t tell which parts of the instruction are critical, where in the pipeline it belongs, or what else in their design it implies.

![Specification for multi-domain experts](https://www.liquid.ai/_next/image?url=https%3A%2F%2Faypchzzf9pftwuto.public.blob.vercel-storage.com%2Fpasted-image-bAULSNt4wPezQMEhOKrsgh43wTTQIe.png&w=3840&q=75)

Specification for multi-domain experts

### Verify against the constrains to the real world

Our operator never read a line of the produced code. This was only acceptable because the success criteria were something the agent couldn’t manipulate. A common mistake we see in loop design is weak verification, run against toy-scale data or open to the agent’s influence, such as editing its own unit tests.

The main lesson is to design a loop that converges against the constraints of reality with the following components:

1. **Iterate against real production data at scale.** The failures that mattered were invisible in a test suite and only discoverable in full-scale production data.
2. **Verify with an external harness.** This is what makes autonomy acceptable. The operator never read the code, and that was tolerable only because correctness was defined by tiktoken and Hugging Face tokenizers, software the agent did not write and could not influence. Had we accepted its own test suite as evidence, we would have had two implementations that passed their tests and produced quietly different vocabularies. Structure the problem so a third party can judge the artifact.

## What’s routine today and looking ahead

These are the results and lessons from an experiment we ran in late 2025: Yes, coding agents can solve a production-grade problem from scratch on their own, without any human oversight, but only when they run inside a loop.

The lessons we learned have become everyday practice on our engineering team today. Half a year on, specifying the goal is the part we spend the most care on, and building loops with real data and external verification have become standard practice.

Today we run loops well beyond one-off builds like the tokenizer trainer, which had a clear, verifiable end goal the loop converged toward. Many of the loops we run now are open-ended instead, hill-climbing toward an objective with no single right answer: tuning a kernel, watching continuous integration, triaging incoming pull requests, or scanning production logs for anomalies. In each, we check the metric instead of the code.

Today's models are meaningfully better, but what made this routine is that they got reliable enough to hand the whole loop to. **If that generalizes, it's a bigger shift in how ML and software engineering get done than any change in raw coding ability.**

## Availability

toktoktok is open source under Apache 2.0 at [https://github.com/Liquid4All/toktoktok](https://github.com/Liquid4All/toktoktok). It trains tiktoken-compatible BPE vocabularies from scratch or extends existing ones, reads.txt and.parquet, allocates vocabulary budget across languages and domains through multi-phase training, and stays inside a memory budget you declare. Conversion scripts for Hugging Face go both directions and verify equivalence before writing anything.

Every line of it was written by an agent, and none of it has been read by us.

## Acknowledgements

Written by Mathias Lechner, with contributions from Leonie Monigatti.

We are grateful to AMD for the partnership that made the hardware for this experiment available.

## Citation

Please cite this article as:

Liquid AI, "Designing Loops for Production-Grade Work", Liquid AI Blog, Aug 2026.

```
@article{liquidAI2026loops,
  author  = {Liquid AI},
  title   = {Designing Loops for Production-Grade Work},
  journal = {Liquid AI Blog},
  year    = {2026},
  note    = {www.liquid.ai/blog/agent-loops},
}
```