---
type: concept
created: 2026-11-13
updated: 2026-11-13
tags:
  - concept
  - drug-discovery
  - scientific-ai
  - training-data
source_ids:
  - src-2026-11-06-koller-data-grow-in-dish
  - src-2026-07-30-teaching-open-model-science
status: active
---

# AI Drug Discovery

## Definition

AI drug discovery is the use of machine learning to find and justify therapeutic hypotheses: which
biological mechanism to target, what evidence supports it, and which experiments to run next. In
this vault it covers both the generation of biological training data and the training of models
that gather and reason over biomedical evidence. Clinical development lies beyond anything the
sources here measure.

## Why it matters

Drug discovery tests a claim that recurs across the vault: that progress in a domain is limited by
the data and verification available, not only by model capacity. Biology adds two complications.
The relevant data often does not exist yet. And the outcome that matters, benefit to patients, sits
far downstream of anything a model or a lab assay can score.

## Current synthesis

### Two layers, two kinds of evidence

The vault's two sources work at different layers, and their results should not be pooled.

- **Data generation.** [[Daphne Koller - Getting Data to Grow in a Dish]] argues that the data
  needed to learn causal human biology "did not exist" and cannot be derived *in silico* from first
  principles. insitro therefore built a wet-lab "data factory". Its POSH screens produce "one row
  per cell", linking a CRISPR perturbation to an imaged phenotype across millions of cells per
  screen. The reported payoff is target discovery: an ALS programme yielded **three** novel targets,
  including ALS-1, the target of insitro's CTRO-2018 programme.
- **Evidence-seeking agents.** [[Bojan Jakimovski - Teaching an Open Model to Do Science]]
  post-trains Arcee's Trinity Mini with GRPO in two verifiable environments. Drug Tool teaches the
  model to choose and call biomedical tools covering PubMed, GEO, KEGG, UniProt, and STRING. Its
  supervised-fine-tuning prompts came from Loka's drug-discovery application. The held-out Drug
  Tool score rose from **70.8%** to **81.2%**. See [[Agentic Reinforcement Learning]].

The first source produces new measurements of biology. The second teaches a model to retrieve and
synthesize existing records. A gain in one says nothing about the other.

### Both stop short of the clinic, and say so

The sources share an explicit boundary. Koller writes that "a change in a cultured cell does not
establish that an intervention will benefit a patient". A screen yields a mechanistic hypothesis to
align with clinical data and test in other models. The Jakimovski results "are not claims about
clinical validity, wet-lab performance, or success across an entire drug program". Neither source
reports a clinical outcome. In this vault, AI drug discovery is evidenced only at the hypothesis
and evidence-gathering stages, and the ALS targets are first-party, pre-clinical claims.

### Reliable data is a process-engineering result

Koller's main lesson is an order of work: measure the process, stabilize it, optimize it, and only
then scale. Reference cells and synthesized barcoded beads measure the platform separately from
the biology, and statistical process control separates ordinary variation from real change. After
stabilization, barcode efficiency averaged **47%**, and its standard deviation fell from **11.2** to
**2.5** percentage points. Later chemistry and software changes raised efficiency above **71%**. The
essay's later spread figure, "a reliable 7 percentage points", is left unreconciled with the
earlier **2.5**; see the source page.

The underlying risk is that a model "has no way to tell biology from experimental drift", so an
unmeasured change "can masquerade as a discovery". On the vault's reading, this is the wet-lab
counterpart of a reward signal that tracks the wrong thing ([[Reward Design for RL]]). Training
data is only as trustworthy as the measurement process behind it.

### The data has to be manufactured, as in robotics

This comparison is the vault's reading, not either source's. Biology resembles
[[Robot Training Data]] more than LLM text. Neither field has a large existing public stock of data
that links an intervention to its outcome, so both manufacture it physically, and both face a
fidelity question about cheaper substitutes. They part on simulation. Koller rejects
first-principles generation for biology, while robotics uses simulation where physics is well
characterized. Both differ from the [[Synthetic Data Flywheel]], whose model-generated data starts
from material that already exists.

### AI inside the data pipeline

Models also help build the platform. insitro's convolutional base caller raised the share of cells
with valid barcodes from **66.6%** to **78.8%**, a different metric from barcode efficiency. Its
active-learning segmentation loop cut annotation time "more than fiftyfold". Agentic QC uses
multimodal language models to review images. It agrees with expert reviewers **82%** of the time and
raised coverage more than **eightyfold**, while scientists set the standards and decide what to do
with each flag. That is [[LLM-as-a-Judge]] applied to lab images rather than text, without a
reported inter-expert baseline.

## Open questions

- How do a lab's data-quality metrics, such as barcode efficiency or agreement with expert QC,
  relate to downstream target success? Neither source connects them.
- Do evidence-seeking agents trained in verifiable environments improve experiment choice in a
  real programme, or only environment scores?
- How much of the claimed advantage comes from the platform rather than from the particular targets
  found?
- Which biological questions admit synthetic or simulated data, given Koller's claim that biology
  cannot be reasoned to from first principles?

## Related pages

- [[Daphne Koller - Getting Data to Grow in a Dish]]
- [[Bojan Jakimovski - Teaching an Open Model to Do Science]]
- [[Agentic Reinforcement Learning]]
- [[Robot Training Data]]
- [[Synthetic Data Flywheel]]
- [[LLM-as-a-Judge]]
- [[Reward Design for RL]]
- [[Automated AI Research]]
