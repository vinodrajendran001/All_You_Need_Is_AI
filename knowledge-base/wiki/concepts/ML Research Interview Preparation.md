---
type: concept
created: 2026-06-30
updated: 2026-06-30
tags:
  - concept
  - interview-prep
  - careers
  - llm
source_ids:
  - src-2026-06-30-alisa-liu-ai-research-job-search
  - src-2026-06-30-alisa-liu-book-of-llms
  - src-2026-06-30-alisa-liu-math-notes
  - src-2026-05-21-leetcode-templates
  - src-2026-05-18-hanfang-pytorch-practice
  - src-2026-06-10-itsreallyvivek-frontier-ai-labs
status: active
---

# ML Research Interview Preparation

## Definition

ML research interview preparation is the process of getting ready for the hiring loop for Research Scientist / Member of Technical Staff / ML engineer roles. Unlike generic software interviews, it spans a wider surface: ML coding, general coding, technical discussion, research discussion, behavioral, math, and a job talk — backed by a deliberate, full-time study effort.

## Why it matters

The vault already has the *components* of interview prep ([[Algorithm Templates for Interviews]] for DSA, [[Han Fang - PyTorch Practice]] for ML implementation), but lacked the connective tissue: which interview types exist, how they differ, and how to study for them. This page is that hub. It is also where the technical concept pages double as exam material — interview prep is one of the strongest reasons this whole knowledge base exists.

## The interview-type taxonomy

From [[Alisa Liu - The AI Research Job Search]] (one candidate's 11 companies / 57 interviews). A repeated meta-point: **technical skills and knowledge are evaluated much more than research experience**, even though research experience is usually what earns the interview.

1. **ML coding** — *the most common type.* Implement an architecture, a decoding strategy, or a classic ML algorithm. PyTorch fluency is mandatory; occasionally pure numpy for a from-scratch backward pass. Practice via [[Han Fang - PyTorch Practice]]; the recurring "implement/debug a transformer" task (Stanford CS336 HW1) should become muscle memory.
2. **General coding** — LeetCode-style; see [[Algorithm Templates for Interviews]] and [[Universal LeetCode Templates]]. Strong foundations here also help in ML coding.
3. **Technical discussion** — no coding, two flavors: an **extended experiment-design** discussion (tests *how you think* — design choices, hypothetical results, follow-up experiments) or **rapid-fire breadth** questions (tests *what you know* — e.g. "ways of encoding positional information," "5D parallelism," "PPO vs GRPO"). The breadth flavor is exactly what [[Alisa Liu - Book of LLMs]] is built to cover.
4. **Research discussion** — narrate a past project and defend it; expect questions on other CV papers. Prepare *why* you worked on things, insights/opinions developed, and promising future directions; tailor the pitch and hit the right keywords.
5. **Behavioral** — textbook STAR, plus occasional AI-safety/societal-impact questions. Pre-map memorable project stories to common questions so you can retrieve anecdotes instantly. (Easy to fail by under-preparing.)
6. **Math** — probability, linear algebra, calculus; from logic puzzles to pen-and-paper derivations. Covered by [[Alisa Liu - Math Notes]].
7. **Job talk** — shorter than an academic talk, focused on a single paper or direction.

## Preparation methodology

- **"There is truly no better use of your time than studying for interviews."** Treat the search as a full-time job.
- **Map first, then deep-dive.** Start with Stanford **CS336 (Language Modeling from Scratch)** to organize scattered concepts into one picture, then study concepts one at a time (papers, blogs, talking to ChatGPT/Claude, implementing from scratch).
- **Build study references.** [[Alisa Liu - Book of LLMs]] (the technical map) and [[Alisa Liu - Math Notes]] (the probability/stats map) model how to consolidate the field. The vault's own concept pages serve the same role.
- **Make the transformer muscle memory.** Implementing/debugging a transformer recurs constantly; CS336 HW1 is the canonical drill.
- **Practice with AI assistance fully off** to mimic interview conditions — otherwise you underestimate your reliance.
- **Per-interview cram.** "Each interview is a slightly different math or CS class, you never went to lectures, and now you have ~3 days to cram for the midterm." Swap the most relevant knowledge in for each company.
- **Logistics.** Sleep beats last-minute cramming on the day; record notes afterward. Use a few companies for practice but guard your stamina; company headcount and which teams are hiring can matter more than prep.

## Beyond the loop: what labs actually select for

[[itsreallyvivek - some notes on getting into frontier ai labs]] adds a productive counter-frame: the interview *loop* rewards technical breadth, but the deeper ability frontier labs select for is **judgment and abstraction under uncertainty** — forming hypotheses and building useful abstractions when no complete map exists (see [[Automated AI Research]]). Both are true at once: study to pass the loop, but the durable edge is research judgment.

## Negotiation

A distinct, hard skill that **cannot be solved by studying** (per [[Alisa Liu - The AI Research Job Search]]). Initial offers are designed to be negotiated; a few weeks of effort can equal years of work at the initial offer. Lean on friends to calibrate asks, pre-script what you will/won't share, and anticipate recruiter questions. Watch for "exploding" offers.

## Open questions

- How much does this NLP-PhD → research-scientist account generalize to MLE/SWE roles, non-PhD candidates, or different hiring years?
- What is the right balance between breadth cramming (to pass loops) and depth/judgment (the durable research skill)?
- Which vault concept pages most need an "interview-ready" summary layer to serve double duty as study material?

## Related pages

- [[Alisa Liu - The AI Research Job Search]]
- [[Alisa Liu - Book of LLMs]]
- [[Alisa Liu - Math Notes]]
- [[Algorithm Templates for Interviews]]
- [[Universal LeetCode Templates]]
- [[Han Fang - PyTorch Practice]]
- [[itsreallyvivek - some notes on getting into frontier ai labs]]
- [[Automated AI Research]]
- [[Neural Network Fundamentals]]
- [[Transformer Architecture]]
- [[Alisa Liu]]
- [[AI Knowledge Base Overview]]
