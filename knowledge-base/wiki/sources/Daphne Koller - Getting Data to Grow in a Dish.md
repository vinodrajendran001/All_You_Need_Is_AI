---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-06-koller-data-grow-in-dish
source_title: Getting Data to Grow in a Dish
source_author: Daphne Koller
source_url: https://deepphenotype.substack.com/p/getting-data-to-grow-in-a-dish
tags:
  - source/summary
  - drug-discovery
  - training-data
  - lab-automation
  - quality-control
source_ids:
  - src-2026-11-06-koller-data-grow-in-dish
status: active
---

# Getting Data to Grow in a Dish

## Summary

Daphne Koller's third essay in a series on AI drug discovery describes how insitro built a wet-lab
"data factory". The motivating claim is that the data AI needs to learn causal human biology "did
not exist", and cannot be generated *in silico* from first principles, so the company had to
produce it. The essay centres on POSH, a pooled CRISPR imaging screen. It argues that reliable
data at scale needs process engineering in a fixed order: **measure, stabilize, then optimize**.
Only then should a process be scaled. Its examples are failures that were silent, then caught.
They also include chemistry and hardware choices made according to where information is lost, and
a split of work between AI models and scientists. Koller writes in the first person as part of
insitro, so the account is first-party and promotional in places.

## Key claims

### The data had to be manufactured

insitro began building its lab in 2018. The name blends *in silico* and *in vitro*. Koller's
argument is that biology "is the product of billions of years of evolution, with no designer and no
documentation". To learn what a cell does when a gene is perturbed, "we have to perform the
experiment and look". The essay's evidence of reward is an ALS programme. insitro produced **six
billion** motor neurons from the genetic backgrounds of a diverse population of people with ALS. It
characterized them by imaging and transcriptomics and used AI to find "a new axis of ALS biology".
That work led to **three** novel targets, including ALS-1, the target of its CTRO-2018 programme.

### POSH turns each cell into one labelled row

In POSH (Pooled Optical Screening in Human cells), millions of cells grow in one pool. Each cell
receives a CRISPR guide, usually a knockout, and a molecular barcode that identifies the guide.
Cells are stained, partly with Cell Painting, and imaged. The barcode is then read *in situ* over
roughly **thirteen** rounds of sequencing chemistry. A plate goes on and off the microscope more than
a dozen times and yields more than **200,000** images. The output is "one row per cell: what we did
to it, and what happened". There are millions of cells per screen and dozens of screens a year.

Koller says imaging costs about **100x** less per cell than other high-content single-cell
measurements. Pooling reduces batch effects because perturbations share one environment: "in an
arrayed screen, your N is a well; in a pooled screen, your N is a cell". She also states the limit:
"A change in a cultured cell does not establish that an intervention will benefit a patient". It
yields a mechanistic hypothesis to align with clinical data and test in other models.

### The worst failures are silent

A robot arm threw plates across the deck. The cause was adhesive from a new sealer, which had been
introduced to stop **170**-micron coverslip glass from cracking. A plate may go through more than
**100** heating and cooling cycles and **200** robotic handling steps in a screen. Other failures
gave no warning. Sequencing stopped working because of a mislabeled primer, which took weeks to
find. A faulty USB port froze imaging. A third-party camera driver shifted successive images by
one frame. The lesson is to "make silent failures loud before they entered the dataset".

### Measure, stabilize, optimize, then scale

- **Measure.** The lab used cameras, timestamped logs, temperature records, and scales that weigh
  plates throughout the workflow. It tracks guide-library representation and checks every chemistry
  change against both readouts. Reference cells and synthesized barcoded beads measure the platform
  independently of the biology. Much early variation "came from the platform itself".
- **Stabilize.** Checks were added at every handoff, along with preventive maintenance and software
  that coordinates instruments. Pyxscope, insitro's acquisition package, now captures more than
  **95%** of imaging data. Each imaging system can generate about **80 MB** of raw data per
  second. Pyxcell is the analysis platform. With end-to-end records, the lab adopted statistical
  process control.
- **Results.** Barcode efficiency, the share of cells whose perturbation can be identified, ranged
  from about **25% to 50%**, averaging **34%**. After stabilization the average was **47%** and the
  standard deviation fell from **11.2** to **2.5** percentage points. After a base-calling artifact
  fix and barcode-amplifying chemistry, efficiency rose above **71%**, "with the standard deviation
  remaining at a reliable 7 percentage points".
- **Payoff.** A whole-genome screen now takes **4** FTE-weeks instead of **52**, **10** plates
  instead of **27.5**, and **$50,000** in reagents instead of **$200,000**.

### Use the tool that fits where information is lost

The robot returns a plate only to within about **100** microns. Instead of submicron robotics, every
acquisition includes a nuclear stain that software uses for alignment. Focus is different, because
detail that was never recorded cannot be recovered by software. The lab therefore combines **five**
autofocus routines per well with an infrared sensor. The standard mitochondrial stain interfered
with base calling, so insitro designed MitoProbe. Guide libraries are built so every barcode pair
differs in at least **three** positions. A single misread then still maps correctly, recovering
**5%–35%** more cells.

### AI inside the lab, scientists at the judgement points

- A small convolutional base caller, trained first on the older method's filtered predictions,
  raised the share of cells assigned a valid barcode from **66.6%** to **78.8%** (Sivanandan et al.,
  *Nature Communications*, 2025).
- iALDE, an active-learning loop for cell segmentation, asks experts to correct only uncertain
  cases. Annotation time fell "more than fiftyfold", and a segmentation model that took six to
  twelve months now takes about a month.
- Agentic QC uses multimodal language models to review images. Two engineers took it to production
  in about **six weeks**. It evaluates **seven** failure modes, explains its assessments, and agrees
  with expert reviewers **82%** of the time. It raised coverage more than **eightyfold**, and it
  caught the camera-driver bug the evening the images were acquired.
- Scientists "define the standards, qualify the system, and decide what to do with its findings".
  The explanation attached to each flag gives them a basis for judging it.

## Why it matters

[[AI Drug Discovery]] gets its first source on the data-generation layer: the claim that useful
biological training data must be manufactured, and the process discipline that makes it
trustworthy. The argument parallels [[Robot Training Data]], where action data also has to be
produced rather than scraped; that parallel is the vault's reading, not Koller's. Agentic QC
supplies [[LLM-as-a-Judge]] with a non-text reviewer that has a reported expert-agreement figure and
a bounded human role.

## Tensions / open questions

- This is a first-party essay by an insitro author about insitro's platform. It references Virtual
  Human™ and the CTRO-2018 programme, so commercial interest is evident. Koller's title at the
  company is not stated in the capture.
- The ALS targets are evidence of target discovery, not of clinical benefit, and the essay itself
  says a cell-level change does not establish patient benefit. No clinical results are given.
- **Spread inconsistency.** Stabilization is credited with cutting the standard deviation to
  **2.5** percentage points. After optimization, it is described as "remaining at a reliable 7
  percentage points". That is wider than 2.5, not unchanged. The chart caption gives a mean of
  **71%** over three and a half years of A549 plates. The essay does not reconcile these figures.
- Two barcode metrics should not be conflated: barcode efficiency (**34% → 71%+**) and the base
  caller's valid-barcode share (**66.6% → 78.8%**).
- Agentic QC's **82%** agreement has no stated baseline for inter-expert agreement, sample size, or
  per-failure-mode rates.
- The whole-genome screen comparison does not give the "before" date or what else changed between
  the two screens.
- Koller says the platform cannot address every disease, since tractability depends on what can be
  measured.
- Only the POSH-cited *Nature Communications* paper is named; it was not read by this ingest.

## Affected pages

- [[AI Drug Discovery]]
- [[LLM-as-a-Judge]]

## Raw capture

- [[knowledge-base/raw/sources/Getting Data to Grow in a Dish]]

## Citations

- Canonical URL: <https://deepphenotype.substack.com/p/getting-data-to-grow-in-a-dish> (tracking
  parameter removed).
- By Daphne Koller on the deepphenotype Substack, published November 6, 2026; captured November 10,
  2026. It is the third essay in her series; the first two are referenced but not captured.
- Named paper: Sivanandan et al., *Nature Communications*, 2025.

## Related pages

- [[AI Drug Discovery]]
- [[LLM-as-a-Judge]]
- [[Robot Training Data]]
- [[Synthetic Data Flywheel]]
- [[Agentic Reinforcement Learning]]
- [[Bojan Jakimovski - Teaching an Open Model to Do Science]]
- [[NVIDIA - GR00T 2 - Scaling Robot Foundation Models for Generalization, Dexterity, and Adaptation]]
