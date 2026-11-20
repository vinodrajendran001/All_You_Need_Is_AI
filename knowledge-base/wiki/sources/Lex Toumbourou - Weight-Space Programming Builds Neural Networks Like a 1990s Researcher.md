---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-18-toumbourou-wsp-1990s-researcher
source_title: "Weight-Space Programming builds neural networks like a 1990s researcher"
source_author: "Lex Toumbourou"
source_url: "https://notesbylex.com/weight-space-programming-1990s.html"
tags:
  - source/summary
  - weight-editing
  - interpretability
  - replication
source_ids:
  - src-2026-11-18-toumbourou-wsp-1990s-researcher
status: active
---

# Weight-Space Programming Builds Neural Networks Like a 1990s Researcher

## Summary

Lex Toumbourou, writing on notesbylex.com, asks whether the write-test-edit loop in
[[Rikiya Takehi et al - Sparks of Weight-Space Programming]] is a new way to train networks, which he
nicknames ***LLM Descent***. He runs his own experiment: **Claude Fable 5.2** sets every weight of a
fixed **5,994**-weight MNIST CNN from scratch, over up to **50** steps, seeing only training loss,
accuracy and a confusion matrix after each attempt. Three runs all reach about **90%** on the
held-out test set, close to 50 steps of Adam. Reading the transcripts, he finds the model rebuilding a
1990s handwriting-recognition pipeline: edge filters, hand-drawn templates, loop and corner detectors,
and a naive Bayes-style classifier whose probabilities it **measures through the confusion matrix**.

He then re-reads the original post's Go network and finds the same pattern: a classical rule-based Go
program (liberties, captures, eyes, ko) compiled into weights, tuned through a config of **26**
hand-set numbers. His tentative conclusion, "from these experiments at least", is that LLMs "aren't
so much 'writing in weight-space' as brilliantly chaining together hand-designed techniques". A
harder cats-versus-dogs test shows where that runs out.

This is a third-party commentary and replication on the original Takehi et al. post. It does not cite
[[Jacob Strauss - Experiments in Weight-Space Programming]], published a day earlier; the two are
independent follow-ups that both happen to use MNIST.

## Key claims

### Setup

- A fixed PyTorch CNN (two 5×5 convolutions with 8 and 16 channels, ReLU and max-pooling, then a
  256→10 linear layer), **5,994** weights, starting from none.
- The model's code runs in a sandbox that can import only NumPy, SciPy and math. Rules forbid fitting,
  regression and searching; drawing filters and templates by hand "from formulas or strokes" is
  explicitly allowed. Toumbourou calls this "considerably stricter" than Astra's Go setup: no PyTorch and
  no practice games.
- Feedback each step: loss, accuracy and a confusion matrix on **10,000** images from MNIST's training
  split, plus the history. The 10,000 official test images are never shown; the network with the lowest
  training loss is the one scored on test.
- Fable 5.2 "performed considerably better than Opus 5.5". Opus runs reached at most **74%** test and
  "tended to prefer guessing". Extra feedback for Opus, including example digits, "didn't make much
  difference".

### Results

- All three Fable runs descended for the full 50 steps, "still improving when they run out", landing
  "around 90%" on test. Run 1, the best, finished at **91.3%**, "roughly where 50 steps of training with
  Adam gets us".
- He qualifies the comparison himself: Adam's 50 steps see **64** images each (**3,200** total), while
  Claude gets scores over all **10,000** training images every step.

### What the model actually built (run 1)

| Steps | What happened | Accuracy reported |
| --- | --- | --- |
| 1-3 | Four-angle line detectors ("cousins of the Sobel filter"), hand-drawn stroke templates scored as log-odds with a temperature; then redrawn digits | **71%**, then **77%** |
| 4-9 | Rewires the output layer so each "predicted digit" reports how strongly a loop detector fired, turning confusion-matrix rows into histograms ("like a unit test"); learns it fires on **83%** of 8s | — |
| 10-18 | Corner detectors as features; guessing stalls near **81%**, three measurement steps help more | **83%** by step 18 |
| 19-30 | Measures how often each of **32** stroke features fires per digit, three at a time | **83% → 88%** at step 24 |
| 31-40 | Discards hand-drawn templates; rebuilds a naive Bayes-style classifier from measured rates (32 orientation cells, 8 corner zones, loop detector) | **89%**, then **90%** |
| 41-50 | Hand calibration of evidence weights and confidence; tracks which step will be scored | **91.3%** final |

The 71% is stated as a test-set score; the capture does not say whether the later run-1 percentages
are test or training accuracy. Across runs, each adopted hand-drawn templates at step 1 and log-odds scoring by step 1, 2 or 11, and
spent **22**, **24** and **27** steps on measurement. Toumbourou calls the measurement trick "kinda
cheating" that "doesn't break the rules": the code never runs the network, fits anything or sees an
image, and the test set stays untouched. His own summary of steps 31-40 is "it's fitting a classifier
by hand".

He ties each technique to the pre-deep-learning literature, including LeCun et al. (1998) on
hand-crafted feature extractors, Mori et al. (1992) on template matching, Chow (1957) on Bayesian
character recognition, and Trier et al. and Favata and Srikantan (both 1996) on shape and edge features.

### Cats versus dogs

On 64×64 Kaggle Dogs vs. Cats with a **24,898**-weight CNN and the same rules, Fable's animal-feature
detectors (pointed ears, an eyes-and-nose triangle) did not work: "The ear probe showed the opposite of
my guess". What worked were photo properties: more green, more texture and more vertical edges in dog
photos. Its best network, at step 9, used only those three; the run stopped at step 17. It scored
**61.6%** on test (coin flip 50%), above 500 Adam steps (**55%**) but below 5,000 Adam steps (**74%**),
and cost **$8.08** for 17 steps.

### Re-reading the original Go network

From the original authors' released logs, Toumbourou describes Astra's 9×9 Go network (**1.5M**
parameters, later "1.48 million weights") as a layered board analysis: liberties, propagation through
connected stones, atari and self-atari flags, capture and rescue scores, then a combination with
connection, territory and eyes. It is driven by a config of **26** hand-set numbers (for example
`"capture": 9.0`, `"eye": 11.0`). Improvement from practice games was "mostly nudging those numbers by
hand", plus five new rules such as a ko-repetition penalty. He says this matches how rule-based Go
programs were built for decades, citing Müller (2002) and Bouzy and Cazenave (2001). He discloses that he
knows little about Go and assembled this section "in consultation with Opus 5.5". He still calls the
result "an incredible feat of engineering: a hand-written program that beats a PPO network trained on
20.5 million games".

## Why it matters

It sharpens what [[Weight-Space Programming]] writes. The original post framed weight-writing as a
fourth route beside optimization, trained hypernetworks and compilers. Toumbourou's evidence places the
from-scratch results closer to the **compiler** route: the model writes a classical algorithm and
compiles it into weights. That is the reading the vault's [[Neural Network Fundamentals]] already
offered for Go, now with an independent MNIST case and a feature-by-feature account.

It also shows a feedback channel acting as a fitting procedure. With full training-set confusion
matrices, the model repurposed the output layer as an instrument and estimated class-conditional
probabilities one feature at a time. No rule was broken, but the "no fitting" constraint did not prevent
fitting by measurement. That is a harness lesson in the family of [[Benchmark Optimization]], and a
cautionary note for [[Automated AI Research]] loops that treat rules in a prompt as constraints.

For [[Mechanistic Interpretability]], the resulting networks are legible because they are built from
named, hand-designed features, not because the LLM reads learned representations.

## Tensions / open questions

- **Three runs, one model, one task family.** No error bars; the Opus comparison is reported in prose,
  and its extra-feedback runs are omitted from the post.
- **The Adam comparison is not like-for-like**, as the author says (3,200 images seen versus full
  training-set metrics every step). Neither side is matched on compute or wall-clock time.
- **The Go reading is secondhand and assisted.** It relies on Opus 5.5 for Go domain knowledge and on the
  released logs, not on a rerun.
- **Opponent size discrepancy.** Toumbourou writes that the Go network beat one PPO network of the same
  size "trained on 20.5 million games". The vault's summary of the original post quotes "trained on 20
  million games". Neither capture settles which figure is right.
- **Win-rate paraphrase.** He says the 50-pass network beat two small PPO networks "in over 80% of games"
  and the same-size one "most of the time". The original summary records chart labels of 84.0, 80.8 and
  74.2 with an inferred mapping, so his paraphrase is consistent but not independently checked.
- **Cost not compared.** Only the cats-versus-dogs run reports cost ($8.08); the MNIST runs report none.
- **Capture quirk.** The capture's footnote section duplicates the steps 1-3 table and the Go conclusion;
  these are clipping artifacts, not extra content. A read-only fetch of the live page shows small wording
  changes since capture (for example "much better" for "considerably better"); this summary follows the
  capture.

## Affected pages

- [[Weight-Space Programming]]
- [[Neural Network Fundamentals]]
- [[Mechanistic Interpretability]]
- [[Automated AI Research]]

## Raw capture

- [[knowledge-base/raw/sources/Weight-Space Programming builds neural networks like a 1990s researcher]]

## Citations

- Canonical URL: <https://notesbylex.com/weight-space-programming-1990s.html> (the captured link carried
  `utm_source=tldrai`, removed here).
- Published 2026-11-18; captured 2026-11-19. The `source_id` date is the publication date.
- **Author recovered.** The capture has no author field. A read-only fetch of the canonical URL on
  2026-11-20 shows the byline "Lex Toumbourou · Nov 18, 2026", consistent with the `lextoumbourou`
  GitHub repository the post links. No web-only figures were used.
- Experiment repository: `github.com/lextoumbourou/weight-space-programming-experiments` (prompts,
  replies, thinking summaries, code and weights per step; not inspected).
- Original post's released logs, as cited: Takehi, Teoh, Zhang and Khattab (2026), commit 4d09ba6.

## Related pages

- [[Weight-Space Programming]]
- [[Rikiya Takehi et al - Sparks of Weight-Space Programming]]
- [[Jacob Strauss - Experiments in Weight-Space Programming]]
- [[Simon Willison - Qwen 3.8 27B on My Laptop Can Interpret Model Weights, Too]]
- [[Neural Network Fundamentals]]
- [[Mechanistic Interpretability]]
- [[Automated AI Research]]
- [[Benchmark Optimization]]
- [[Interpretability Evaluation]]
- [[Divyansh Agrawal - Qwenputer - A Deterministic RISC-V CPU Inside Qwen3.5]]
