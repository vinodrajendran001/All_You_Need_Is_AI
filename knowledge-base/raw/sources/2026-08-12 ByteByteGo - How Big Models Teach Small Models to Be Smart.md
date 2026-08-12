---
type: raw-source
source_id: src-2026-08-12-bytebytego-knowledge-distillation
title: How Big Models Teach Small Models to Be Smart
author: ByteByteGo
url: https://blog.bytebytego.com/p/how-big-models-teach-small-models
published: 2026-08-05
captured: 2026-08-12
status: immutable
tags:
  - source/raw
  - knowledge-distillation
  - small-language-models
---

> Preserve the source body below this line as the canonical capture.

## \[Webinar\] Can you prove AI is working? (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!6jwZ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f4b0dd6-9113-47e7-bed8-5a03a5a9764a_1600x900.png)

AI is in your engineering workflow. While the token spend shows it, the throughput doesn’t. The human is very much still in the loop, and that’s a context problem.

[Join live on Aug 19 (FREE)](https://getunblocked.link/NwybmZ3) to learn:

- The 4 metrics to measure where AI gains leak out before production.
- The 8 stages of context maturity, the specific walls capping your metrics, and a free tool to pinpoint where your team is
- Why more MCPs and bigger context windows aren’t enough, and what it takes to get real value from your agents.

---

The most capable AI models are also the most expensive to run. They need specialized hardware, they consume large amounts of memory, and they add cost and delay to every request they handle.

These traits make them hard to deploy in places where resources are limited, such as a mobile device or a service that handles heavy traffic and needs fast and low-cost responses.

There is also a second fact that sounds backward at first. A small model can sometimes match or beat a much larger model on a specific task, even when the small model learned everything it knows from the larger one. On an intuitive level, a model trained on another model’s output would seem to inherit a ceiling rather than break through it, yet the results are different. The method that makes this work is called knowledge distillation, and it has become a standard part of how production AI systems get built.

In this article, we will walk through the idea from the ground up. The main points we will cover are as follows:

- What distillation is, and how it differs from compression.
- Why learning from a model’s output can beat learning from raw labels.
- The three main methods, and which one dominates?
- What distilled models achieve in practice.
- Where the method breaks down, and where it is heading next.

![](https://substackcdn.com/image/fetch/$s_!bE0b!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffcc59983-2437-4519-a9b7-d05bc6c145fa_3790x1040.png)

## Distillation

Distillation trains a new, smaller model to copy the behavior of a larger one. The setup involves two models:

- The first is a large, capable model called the teacher.
- The second is a smaller model called the student, which is trained to reproduce the teacher’s outputs.

Once training finishes, the student runs on its own, and the teacher steps out of the picture.

A common assumption is that the student is the teacher in compressed form. The reality, however, is different.

Compression methods such as quantization and pruning start with one model and reduce its footprint by storing its numbers at lower precision or removing parts that contribute little to the result. The model stays the same model, smaller and lighter.

Distillation, on the other hand, produces a genuinely separate model, with its own parameters and often a different design, whose goal during training is to behave like the teacher.

One operation shrinks an existing model. The other trains a fresh one. The payoff is practical, since a small student can run inside a single service or on a phone, respond in less time, and cost far less for each request, and in some cases, it can run on the device itself without sending data elsewhere.

![](https://substackcdn.com/image/fetch/$s_!-6lk!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F965d38d3-6df4-4c28-9ccf-33ac300a4c93_3490x1768.png)

This method is now standard practice. For example, Google’s Gemma models are built using distillation during training, drawing on a larger model in the Gemini family. The two ideas also work together in sequence. A model is often distilled first to produce a smaller capable model, then quantized to shrink that model further for a specific device.

Keeping the distinction clear matters because it affects how we understand further concepts. A compressed model carries a copy of the original inside it. A distilled model is a separate thing that was trained to act like the original, which is exactly why it can sometimes behave in ways the original would not.

If the student only copies the teacher, why does copying work so well?

The answer is in what the teacher hands over.

## Soft Labels

Learning from a model’s output beats learning from raw data because the output carries more information than a plain answer.

Standard training data gives one answer per example. An image of a cat carries the label “cat,” and the model is rewarded for producing “cat” and penalized for anything else. A teacher model offers something richer. Instead of a single answer, its output is a set of probabilities across the options, such as cat at 0.70, dog at 0.25, and fox at 0.05. That full set of probabilities is called a soft label, in contrast to the single hard label found in ordinary data.

The extra numbers carry additional information. They show that the teacher’s output ranks dog as a plausible alternative and fox as a distant one, which says something about how the categories relate to each other. Researchers sometimes call this dark knowledge, meaning the structure hidden in a model’s confidence that a bare label leaves out.

![](https://substackcdn.com/image/fetch/$s_!QYdZ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94194471-983e-47d3-bf09-b4b33aecc0e6_3170x1764.png)

During training, the student works to match this distribution. It is scored on how far its own probabilities sit from the teacher’s, and training pushes it to close that gap. In other words, the student learns the teacher’s whole pattern of confidence rather than a single right answer, and that pattern is a stronger training signal than a one-word label.

This is the core reason distillation works as well as it does. A single correct label discards the relationships between options, and soft labels keep them.

An early result showed the practical payoff, since a student could reach good performance from far fewer examples when trained on soft targets, because each example now carried more than a single answer. The original 2015 work added a control called temperature for exactly this purpose, where a higher temperature spreads the probabilities out and exposes more of that fine structure for the student to learn.

With the mechanism clear, the next question is how this gets done in practice, which has more than one answer.

## Methods

Distillation comes in three main forms, and they differ in what the student copies:

- **Output distillation:** The student matches the teacher’s final outputs, including the soft labels described above. This is the original form from 2015 and the most direct one.
- **Feature distillation:** The student matches the teacher’s internal representations, meaning the intermediate values a model computes while processing an input, before it settles on a final answer. The aim is a similar internal picture, not only a similar output. Google’s EmbeddingGemma is trained this way, learning to produce internal representations close to those of a larger Gemini model.
- **Synthetic data distillation:** The teacher generates a dataset of examples, and the student is fine-tuned on that dataset the same way it would be trained on any ordinary data. Stanford’s Alpaca was an early case, fine-tuned on examples produced by an existing large model to improve how well it followed instructions.

![](https://substackcdn.com/image/fetch/$s_!J7A5!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa027195-54cd-4957-aceb-65cf4e8e05ec_3624x1830.png)

The third form has become the most common approach in practice, and part of the reason comes down to access.

Many strong models are reachable only through an interface that returns text, with their internal values and probabilities kept private. When those internals are out of reach, generating data is the route that still works.

The three forms also differ in what they require. Output distillation needs the teacher’s probabilities, feature distillation needs access to its internal values, and synthetic data distillation needs only the text the teacher produces, which is why it travels the furthest across closed models.

These methods can also be combined. A single training run might use a generated dataset alongside soft labels, and newer methods mix teacher and student generation during training.

These methods are not only theoretical. The next section shows what they produce.

## Results

The results in practice are strong, with one important qualifier.

A clear example came in early 2025 from a lab called DeepSeek. It used a large reasoning model to generate a set of training examples, then fine-tuned several existing smaller models on those examples. One result stood out.

A 7-billion-parameter student scored higher than a 32-billion-parameter model on a competition mathematics benchmark, even though it was produced by plain fine-tuning on the larger model’s outputs. The released family of distilled models ran from 1.5 billion parameters up to 70 billion, and the smaller ones were compact enough to run on a single graphics card, which is part of why the release drew so much attention. The practical effect was that strong performance on these narrow tasks became something a small team could run locally and cheaply, rather than only through a large hosted model.

The qualifier matters as much as the headline.

These wins tend to appear on narrow, well-defined tasks such as mathematics and code. On those tasks, a small distilled model can perform at a level its size would not suggest. Across broader measures of general knowledge, the same small models still trail the larger ones. For example, a model can become excellent at competition mathematics through distillation while remaining weaker at wide-ranging questions about the world. Therefore, a claim that a small model beats a large one is usually true in a specific, narrow sense.

![](https://substackcdn.com/image/fetch/$s_!Frkv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7eb9b517-2532-443a-a60a-2db39b265f17_3790x1442.png)

If the results are this good, the natural question is where the method falls short, which the next section takes on directly.

## Limits

Distillation has clear limits, and they matter when deciding whether it fits a given problem.

- **A ceiling effect from the teacher:** A student trained on a teacher’s output tends to stay at or below the teacher’s level on the kind of data they saw. When the teacher produces a wrong answer, the student learns that wrong answer along with the right ones. The teacher’s quality sets the bar, which makes the choice of teacher one of the most consequential decisions in the process.
- **A wider gap can hurt:** A larger, stronger teacher does not always produce a better student. When the gap between teacher and student is very wide, transfer can degrade, because the student has too little capacity to absorb everything that a much larger model expresses. Research on this capacity gap has found that the strongest available teacher is sometimes a poor choice. A set of methods exists to bridge wide gaps by adding a middle step, where the teacher trains a mid-sized model and that model trains the small student, so each handoff spans a smaller distance.
- **Architecture can outweigh size:** The design of the base model can matter more than its parameter count. In one study, a 32-billion-parameter student outperformed a 70-billion-parameter student on the same task, because the smaller one was built on a stronger base architecture. Size alone is a weak predictor of how well distillation will go.
- **The teacher can pass on more than the task:** In a 2025 study later published in Nature, a teacher model with a particular trait, a tendency to favor owls, was used to generate training data made up only of number sequences. A student trained on those numbers picked up the same preference for owls, even after the data was filtered to remove any visible trace of the trait. The same effect appeared with more serious behaviors, and it occurred only when the teacher and student shared the same base model. The takeaway is that distillation can carry across more than the task being taught, and that filtering the visible data is sometimes too coarse to stop it.

![](https://substackcdn.com/image/fetch/$s_!fwPc!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf27c451-2af1-4161-a50f-8829a0e45d7e_2488x1596.png)

These limits set the boundaries, and within them, the method keeps advancing. The next section covers where it is heading.

## Automation

The newest direction in distillation reduces the manual effort by automating the whole process.

In this setup, the large model runs the full loop on its own. It generates training data, fine-tunes the student, evaluates the student against a held-out set of examples it also generates, and repeats the cycle, adjusting what it produces until the student stops improving. The human role shrinks to defining the task and the success criteria at the start, with a final check on real data at the end.

![](https://substackcdn.com/image/fetch/$s_!Jfpl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd280c4e-90ed-4064-8225-741c922327b6_2952x2006.png)

Recent work in 2026 applied this to a detection task and found that it worked well, with one finding worth keeping in mind.

The choice of teacher model had a large effect on the outcome. Different teachers, given the same loop and the same student, produced students of noticeably different quality. So automation removes manual effort while making the initial choice of teacher more consequential, since that choice now drives an entire self-running process rather than a single training pass.

The same loop also points toward less hand-built pipeline work over time, as more of the data generation and evaluation moves to the model itself. For a team, the appeal is building a small, task-specific model without assembling a large hand-labeled dataset first, since the teacher supplies both the training examples and the data used to score them.

## Conclusion

Distillation is a method for training a small, deployable model to copy the behavior of a large, expensive one. It produces a separate model rather than a compressed version of the original, and that distinction explains most of how it behaves.

It works because a model’s output carries more information than a plain label, in the form of soft labels that show a full pattern of confidence across the options.

In practice, the most common form has the teacher generate a training set that the student learns from, and the results can be strong, though usually on narrow tasks.

The limits are real:

- The teacher sets a ceiling,
- A wider size gap can hurt rather than help,
- Architecture can outweigh size
- The process can carry across traits that were never intended.

Taken together, distillation tends to be a good fit when the task is well defined and a capable teacher is available, and a weaker fit when the goal is broad, open-ended capability.

**References:**

- [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531)
- [DeepSeek-R1](https://arxiv.org/abs/2501.12948)
- [Gemma 3 Technical Report](https://arxiv.org/abs/2503.19786)
- [EmbeddingGemma architecture and recipe](https://developers.googleblog.com/en/gemma-explained-embeddinggemma-architecture-and-recipe/)
- [Alpaca](https://crfm.stanford.edu/2023/03/13/alpaca.html)
- [Improved Knowledge Distillation via Teacher Assistant](https://arxiv.org/abs/1902.03393)
- [Explainable Sentiment Analysis with DeepSeek-R1](https://arxiv.org/abs/2503.11655)
- [Language models transmit behavioural traits through hidden signals in data](https://www.nature.com/articles/s41586-026-10319-8)
- [Anthropic summary](https://alignment.anthropic.com/2025/subliminal-learning/).
- [Agentic Knowledge Distillation](https://arxiv.org/abs/2602.10869)