---
type: concept
created: 2026-11-20
updated: 2026-11-20
tags:
  - concept
  - weight-editing
  - interpretability
  - neural-networks
source_ids:
  - src-2026-11-02-takehi-weight-space-programming
  - src-2026-11-03-willison-qwen-interprets-weights
  - src-2026-11-17-strauss-weight-space-experiments
  - src-2026-11-18-toumbourou-wsp-1990s-researcher
status: active
---

# Weight-Space Programming

## Definition

Weight-space programming (WSP) means having a language model read, write or edit a neural network's
parameters directly, by reasoning about what each part should compute, instead of producing them by
gradient descent on data. The term comes from
[[Rikiya Takehi et al - Sparks of Weight-Space Programming]], which places it beside three existing
writers of weights: optimization, trained hypernetworks and compilers from formal programs. Follow-ups
use the name both for writing networks from zero and for editing a trained one. Lex Toumbourou calls
the iterative write-test-edit loop "*LLM Descent*".

## Why it matters

- It is a route to parameters other than the training loop that [[Neural Network Fundamentals]]
  describes, so it tests what that loop is actually needed for.
- Networks written this way can be legible by construction. That is a different claim from reading
  learned weights, which is what [[Mechanistic Interpretability]] and [[Interpretability Evaluation]]
  care about, and the two are easy to conflate.
- Weights become one more artifact an agent loop can edit ([[Automated AI Research]]), with the same
  harness questions about feedback channels and rules.

## Current synthesis

### The original claims are first-party and preliminary

Takehi et al. ran eight experiments with one model, GPT-6 Astra, and call the results "very early".
Writing: a MinAtar Breakout network written from zeros scored **517.4**, against **25.3** for PPO at
500 million steps, and a 9×9 Go network of **1,480,274** weights was written with no forward passes in
a single **336**-line run. Reading: Astra found every copying head in small transformers, but on Gemma
3 270M sycophant/honest pairs it **failed all four attempts from weights alone** and succeeded only with
an attention probe. Editing: on Qwen3.5-0.8B it removed a loop direction from **131,072** weights
(**0.016%**), and MATH-500 rose **7.9 → 48.1**, against **+1.6** points for a norm-matched
random-direction control.

### Reading small networks does not need a frontier model

[[Simon Willison - Qwen 3.8 27B on My Laptop Can Interpret Model Weights, Too]] reran the four no-tools
game prompts. Qwen 3.8 27B, running locally on a laptop, named three of the four games and missed
Freeway; each answer with a reported time took 46 minutes to over an hour. Kimi K3.1 Pro, via
OpenRouter, named Breakout, the only game it was given. It was one run per game, with no repeats or
guess-rate baseline.

### Writing works where a compact algorithm exists

[[Jacob Strauss - Experiments in Weight-Space Programming]] tested writing with Claude Opus 5.5 on six
small networks. Tasks with a compact known rule went well: CartPole perfect "in just a few turns", Two
Spirals **99.9%**, bracket matching **100%** at every length. Data-heavy tasks did not: IMDB **86.2%**
against **87.0%** with gradient descent, MNIST **64.1%** by stroke-drawn templates, and an undertrained
Shakespeare LSTM moved **39.9% → 40.5%**. Strauss concludes WSP "isn't an effective replacement for
training loops".

### The writer compiles known techniques, and rich feedback becomes fitting

[[Lex Toumbourou - Weight-Space Programming Builds Neural Networks Like a 1990s Researcher]] gave
Claude Fable 5.2 a fixed **5,994**-weight CNN and loss, accuracy and a confusion matrix over **10,000**
training images each step. Three runs reached "around 90%" on test, the best **91.3%**. The transcripts
show a 1990s handwriting pipeline: edge filters, templates, loop and corner detectors, then a naive
Bayes-style classifier whose probabilities the model measured through the confusion matrix ("it's
fitting a classifier by hand"). The metric, not the code, did the fitting (compare
[[Benchmark Optimization]]). Re-reading Astra's Go network, Toumbourou finds a classical rule-based
Go program driven by **26** hand-set numbers. On cats versus dogs, where the model's hand-designed
animal detectors did not work, the approach reached **61.6%**, between 500 Adam steps (**55%**) and
5,000 (**74%**).

### What the evidence supports

Across the four sources, success tracks whether a compact, human-known algorithm exists: a controller,
a counting rule, a geometric construction, rule-based Go, template-and-feature OCR. Where performance
depends on many statistical regularities (IMDB, Shakespeare, cats versus dogs) gradient descent ties or
wins. This supports reading WSP as the model compiling algorithms it already knows into weights, closer
to the compiler route than to a new learning method. *Vault inference from four sources.*

The two MNIST results differ widely (**64.1%** and about **90%**) but also differ in model,
architecture (dense versus CNN), feedback (a dozen or so samples and capped validation versus full
training-set metrics every step) and budget, so the cause of the gap is not isolated. All four sources
are blog posts with single or few runs and no seeds, and baselines range from same-architecture
training to none.

## Open questions

- Does writing from scratch scale past small networks? The largest written-from-zero network recorded
  here is the **1,480,274**-weight Go network; the 0.8B result is an edit of a trained model.
- How much of the MNIST gap comes from feedback richness rather than model or architecture?
- Where should a harness draw the line between writing and fitting, when a confusion matrix over the
  full training set lets the model estimate class-conditional rates feature by feature?
- Are hand-written weights a better initialiser than random ones, as Strauss hypothesizes? Untested.
- Do weight-reading claims beat a behavior-only baseline, the test [[Interpretability Evaluation]]
  asks for? Not yet run in any source.
- The Go opponent is described as trained on "20 million games" (Takehi et al., as summarized) and
  "20.5 million games" (Toumbourou). Which is right is unresolved.

## Related pages

- [[Rikiya Takehi et al - Sparks of Weight-Space Programming]]
- [[Simon Willison - Qwen 3.8 27B on My Laptop Can Interpret Model Weights, Too]]
- [[Jacob Strauss - Experiments in Weight-Space Programming]]
- [[Lex Toumbourou - Weight-Space Programming Builds Neural Networks Like a 1990s Researcher]]
- [[Neural Network Fundamentals]]
- [[Mechanistic Interpretability]]
- [[Interpretability Evaluation]]
- [[Automated AI Research]]
- [[Parameter-Efficient Fine-Tuning]]
- [[Benchmark Optimization]]
- [[Qwen]]
