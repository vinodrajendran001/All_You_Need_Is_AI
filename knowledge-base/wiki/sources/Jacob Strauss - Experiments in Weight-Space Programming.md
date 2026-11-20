---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-17-strauss-weight-space-experiments
source_title: "Experiments in Weight-Space Programming"
source_author: "Jacob Strauss"
source_url: "https://jacobstrauss.bearblog.dev/experiments-in-weight-space-programming/"
tags:
  - source/summary
  - weight-editing
  - interpretability
  - replication
source_ids:
  - src-2026-11-17-strauss-weight-space-experiments
status: active
---

# Experiments in Weight-Space Programming

## Summary

Jacob Strauss, a practitioner who says he works with LSTMs in production, runs an independent
follow-up to [[Rikiya Takehi et al - Sparks of Weight-Space Programming]], which he attributes to MIT
CSAIL. Where the original tested GPT-6 Astra, Strauss uses **Claude Opus 5.5** (effort "High") in his own
open harness, plus **Claude Fable 5.2** for one task. He tries six classic small problems: MNIST,
CartPole, IMDB sentiment, Two Spirals, bracket matching and a character-level Shakespeare LSTM. The
agent writes or edits each network's weights in NumPy with no gradient descent.

The results split cleanly. On tasks where a compact, known rule exists (CartPole, Two Spirals,
brackets) the agent reaches perfect or near-perfect scores in minutes. On IMDB it comes within **0.8**
points of gradient descent with a readable sentiment dictionary. On MNIST it reaches **64.1%** by
template matching, far below trained networks. Improving an undertrained Shakespeare LSTM barely
moves it. His conclusion is that WSP "isn't an effective replacement for training loops", but that a
network whose units can each be explained may be worth more than "a few points of accuracy" for small
models, and hand-written weights might make a better initialiser than random ones.

## Key claims

### The harness

- The agent gets a Python interpreter in a Docker container with **no internet** and only Python and
  NumPy installed, to block peeking at validation or test data, using TensorFlow or PyTorch, or looking
  up answers.
- Tools: `samples` (draw a limited number of training examples, "usually a dozen or so"), `commit` and
  `reset` (weight snapshots), `evaluate` (validation scores such as accuracy, loss and a confusion
  matrix, with a capped call count) and `forward` (run examples and store activations), which the agent
  "rarely used". The test set is scored only at the start and end.
- Runs are capped at **50 to 100** turns. Rules include no gradient descent, no self-built dataset and no
  dataset exploitation. Another LLM checked each run's logs and found no rule-breaking. Strauss notes the
  agent could in principle have written gradient descent in NumPy with a loop; an early version banning
  loops was "too restrictive".
- All target models were built in TensorFlow. Strauss chose Claude because he gets free Anthropic API
  credits through a start-up program; he says the harness works with any LLM.

### Results by experiment

| Experiment | Network | Agent result | Comparison given |
| --- | --- | --- | --- |
| MNIST | 2 dense layers (128, 10), **101,770** params, zeroed | **64.1%** test in 8 minutes, by stroke-drawn digit templates with 12 variants each | Gradient descent ">85% in under 20 seconds"; a 2025 paper's 30-reference-digit, no-training construction reported **63%** |
| CartPole | 1 hidden layer of 16 units | Perfect score "in just a few turns" after about **490** tokens of thinking | Described as "the textbook answer": a linear state-feedback controller |
| IMDB | Bag-of-words, 10,000 inputs, one sigmoid output | **86.2%** test in under 3 minutes, changing **663** of **10,001** weights | Same model with gradient descent: **87.0%** |
| Two Spirals | 2 inputs, two 64-unit ReLU layers, **4,417** weights | One evaluation at **99.7%**, then **99.9%** test, about 6 minutes; not told what the data was | Described as tricky for gradient descent; no trained number given |
| Brackets | Recurrent network | **100%** at every string length in under a minute, one evaluation | Skachkova et al. (2018) trained network: **96.6%**, weaker on long strings |
| Shakespeare | Character-level LSTM | From zero: about **34%**. Editing an undertrained model: **39.9% → 40.5%** in 36 minutes | Full training would reach **51.3%**; the gain is "roughly half an epoch" |

Mechanism notes the source gives:

- **MNIST**: the agent drew digits from lines, arcs and ellipses, made slanted and stretched variants,
  and predicted its own ceiling: "Pure template matching probably tops out around 70%".
- **IMDB**: a tiered sentiment dictionary plus priors about reviewers, for example a small negative
  weight on "horror", "zombie", "gore" and "budget". The agent noted a bag-of-words model cannot see
  negation, so it judged the limit to be the model's.
- **Two Spirals**: layer 1 drew a fan of rays from the centre, layer 2 marked spiral edges, and the
  output counted edges crossed.
- **Brackets**: the agent switched from tracking the first opened bracket to a shortcut. Since only the
  last bracket is removed, it counts open-minus-closed per bracket type and picks the one equal to 1,
  with four 16-unit counters.
- **Shakespeare**: the agent "found nothing" to fix and called the model "simply undertrained". Fable
  5.2 tried a more elaborate strategy, compressing part of the network by hand to fit a tree of common
  word beginnings, and ended "in almost exactly the same place".

### Conclusion

Strauss argues gradient descent captures patterns *implicitly* while the agent realises them
*explicitly*, so its weights can be followed. Gradient descent is still "cheaper, faster and in many
cases, results in more accurate models". The agent "seems better at deciding what a network should
look like than at choosing its exact numbers". He ends with a hypothesis, not a test: hand-written
weights as an initialiser.

## Why it matters

It is the vault's second third-party test of [[Weight-Space Programming]] after
[[Simon Willison - Qwen 3.8 27B on My Laptop Can Interpret Model Weights, Too]], and the first on the
*writing* side with a different model family. It supports a narrower reading than the original
post's framing. Writing weights works where the model already knows a compact algorithm (a
textbook controller, a counting rule, a geometric construction). It is weak where performance depends
on many small statistical regularities learned from data, which is the part gradient descent handles.
That bears on [[Neural Network Fundamentals]], whose page already asks whether reasoning-written
weights compete mostly against weak baselines. Here, the comparisons are against the same architecture
trained normally, and the agent loses or ties on the data-heavy tasks. For [[Mechanistic Interpretability]],
Strauss's interpretability claim is about networks built to be legible, not about reading trained ones.

## Tensions / open questions

- **Single runs, one author, one main model.** Each experiment is reported once with no seeds or
  variance. The rule-compliance check was done by another LLM.
- **Cheap feedback shapes the result.** The agent saw "a dozen or so" samples and a capped number of
  validation scores. [[Lex Toumbourou - Weight-Space Programming Builds Neural Networks Like a 1990s Researcher]]
  gave a CNN's writer full training-set metrics for 50 steps and got about **90%** on MNIST. The two
  setups differ in model, architecture, feedback and budget, so neither isolates why. *Vault inference.*
- **Baselines vary in strength.** MNIST is compared against gradient descent "in under 20 seconds" at
  ">85%"; the trained IMDB and Shakespeare comparisons use the same architectures; Two Spirals has no
  trained number. CartPole needs no learning, as Strauss says.
- **Provenance of the original.** Strauss calls the Takehi et al. post an MIT CSAIL publication. The
  vault's summary of that post records no affiliation in its capture, so this attribution is
  secondhand.
- **Shortcut versus task.** The brackets solution exploits the dataset's construction (only the last
  bracket is missing). Strauss treats this as good reasoning and notes he "could make the task
  harder"; the 100% reflects that construction, and the capture does not show whether the paper's
  96.6% was measured on an identically constructed set.
- **Typo in capture.** The IMDB section ends "why each weight is there.xw"; the stray characters are a
  capture or source typo.

## Affected pages

- [[Weight-Space Programming]]
- [[Neural Network Fundamentals]]
- [[Mechanistic Interpretability]]

## Raw capture

- [[knowledge-base/raw/sources/Experiments in Weight-Space Programming]]

## Citations

- Canonical URL: <https://jacobstrauss.bearblog.dev/experiments-in-weight-space-programming/> (the
  captured link carried `utm_source=tldrai`, removed here).
- Published 2026-11-17; captured 2026-11-19. The `source_id` date is the publication date.
- **Author recovered.** The capture has no author field. A read-only fetch of the blog's home page,
  `jacobstrauss.bearblog.dev`, on 2026-11-20 shows "Partial derivatives of Jacob Strauss" with a GitHub
  link to `jda5`, the account hosting the harness code cited in the post. No other web content was used.
- Harness code: `github.com/jda5/wsp-experiments` (linked from the post; not inspected).

## Related pages

- [[Weight-Space Programming]]
- [[Rikiya Takehi et al - Sparks of Weight-Space Programming]]
- [[Lex Toumbourou - Weight-Space Programming Builds Neural Networks Like a 1990s Researcher]]
- [[Simon Willison - Qwen 3.8 27B on My Laptop Can Interpret Model Weights, Too]]
- [[Neural Network Fundamentals]]
- [[Mechanistic Interpretability]]
- [[Interpretability Evaluation]]
- [[Automated AI Research]]
- [[Benchmark Optimization]]
