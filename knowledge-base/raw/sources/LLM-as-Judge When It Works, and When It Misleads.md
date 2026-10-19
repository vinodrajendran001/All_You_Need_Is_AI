---
title: "LLM-as-Judge: When It Works, and When It Misleads"
source: "https://www.arise-ai.org/blog/llm-as-judge"
author:
  - "[[Sri Polkampally]]"
  - "[[Bhav Jain]]"
  - "[[Cathy Liu]]"
  - "[[Liam G. McCoy]]"
published: 2026-08-02
created: 2026-10-19
description: "When LLM-as-judge works for clinical AI evaluation, when it misleads, and why human-validated baselines are essential for post-deployment monitoring."
tags:
  - "clippings"
---
Most FDA-authorized AI devices arrive in the clinic with remarkably little known about how they perform there. Of roughly a thousand authorized devices, an analysis found that [more than half reported no performance metrics and nearly half described no clinical study at all](https://doi.org/10.1038/s41746-025-02052-9). Once a system is deployed, the question of how to keep evaluating it— continuously, at scale, and on the outcomes that actually matter—has largely gone unanswered.

In response to this regulatory need, the U.S. Food and Drug Administration recently issued a [Request for Public Comment on measuring and evaluating AI-enabled medical-device performance in the real world](https://www.fda.gov/medical-devices/digital-health-center-excellence/request-public-comment-measuring-and-evaluating-artificial-intelligence-enabled-medical-device). Our team at ARISE submitted a [public comment](https://www.regulations.gov/comment/FDA-2025-N-4203-0062) proposing that one technique—LLM-as-judge—could form part of the answer, used carefully and for the right tasks.

That last qualification is the whole point. LLM-as-judge is not a general-purpose oversight system, and treating it as one is the fastest way to get misled. It is a powerful tool under specific conditions, and knowing when not to reach for it matters as much as knowing when to.

## What is LLM-as-judge?

In an LLM-as-judge setup, a language model evaluates a piece of human- or, more commonly, AI-generated text—for example, by reading a note and scoring it against a rubric. At its most useful, the LLM performs a form of *content matching*: deciding whether one piece of text carries the same clinical meaning as a reference, even when the wording is completely different.

This capability is particularly useful in clinical contexts, where there may be many semantically different but clinically equivalent ways to express an answer. A note that records thyroid status as “TSH elevated, free T4 low” is saying the same thing as one that writes “hypothyroidism.” A judge that understands this can match them where older natural-language-processing methods, keyed to surface strings, would fail. The same flexibility lets a judge check [whether a note follows SOAP structure](https://doi.org/10.1056/AIcs2400631), [whether a differential covers the expected diagnoses](https://arxiv.org/abs/2410.12858), or [whether a clinical summary quietly dropped important content](https://doi.org/10.1038/s41746-025-02005-2), such as the medication list. These are matching problems against a known answer, and they are what the technique is good at.

In essence, large language models let us evaluate unstructured clinical text with an ease much closer to the way we have traditionally evaluated structured, organized answers. This has implications for training and evaluating clinical models—and for training and evaluating people. However, a naively implemented LLM judge may introduce more confusion into the evaluation process than it resolves.

## When to use it

LLM-as-judge earns its place when three conditions hold, and they build on one another (Figure 1): a judge you can trust, pointed at a task it can actually do, in a setting where doing it by hand does not scale. Miss any one and the technique stops paying off.

1. **A validated human baseline exists.** This is the primary condition, and everything else rests on it. Before a judge is trusted with anything, its scores are checked against a set of cases that human experts graded independently. That seed set does double duty: it fixes the criteria the judge is meant to apply, and it becomes the standing benchmark the judge is spot-checked against over time. The judge only goes to scale once its agreement with the human graders clears a pre-specified threshold. Human review should then continue on a spot-checked basis.
2. **The task is narrowly scoped.** Scope is a feature here, not a limitation. A judge that reliably catches one common, well-defined failure is worth far more than one asked to pass judgment on everything and trusted on none of it. Two shapes of task fit especially well:
	- **Semantic equivalence:** deciding whether an output carries the same clinical meaning as the reference despite different wording. The thyroid example above is exactly this.
		- **Standardized reasoning:** checking an output against well-established, agreed-upon criteria—for example, whether a note follows SOAP structure or a differential covers the diagnoses the case demands.
3. **The task benefits from scale.** No human panel can read every note written in a health system. Catching that AI-scribe notes are *systematically* dropping medication reconciliation across thousands of encounters is precisely the kind of signal that only surfaces at volume—and precisely the work a validated judge can take on and a manual reviewer cannot.
![Flowchart showing the conditions for reliable LLM-as-judge monitoring: a human-graded seed dataset, a narrow task scope, semantic equivalence or standardized reasoning, and a task that benefits from scale.](https://www.arise-ai.org/_next/image?url=%2Fstatic-posts%2Fllm-as-judge%2Flayers-of-evaluation.png&w=3840&q=75)

Layers of evaluation for AI monitoring. A useful judge begins with a human-graded seed dataset, stays narrowly scoped, and is used where evaluation benefits from scale.

## Good and bad judges

It bears repeating: the line that separates a useful judge from a harmful one is not the model, the prompt, or the rubric. It is whether there is a clearly validated—ideally human-expert—baseline behind it.

An LLM-as-judge system is only as useful as the confidence we can have in it. Simply asking one model to evaluate the quality of another model’s response places us in a “who watches the watchmen?” situation unless we have an evaluation set against which the grader itself can be tested.

A good LLM-as-judge grades against a detailed, human-adjudicated reference: a set of cases that experts scored independently. It has also been checked to confirm that its scores track the human ones—or a true verifier, where one exists. Under those conditions, the model extends the reach of a human standard. It does at scale what a panel of clinicians did on the seed set, with the flexibility to recognize the same clinical meaning in unfamiliar phrasing.

Our comment points to real examples: an LLM-as-judge that reached [human-like agreement with graders on clinical-summary quality](https://doi.org/10.1038/s41746-025-02005-2); pipelines that adjudicate cardiovascular endpoints in [multicenter](https://jamanetwork.com/journals/jamacardiology/fullarticle/2811977) and [global clinical trials](https://pubmed.ncbi.nlm.nih.gov/39549261/); and systems that identify [venous-thromboembolism diagnostic delays](https://pubmed.ncbi.nlm.nih.gov/41058083/) or support [post-deployment monitoring for pulmonary-embolism detection](https://pubmed.ncbi.nlm.nih.gov/40602699/). In each case, the judge is anchored to something that was validated by hand.

A bad LLM-as-judge skips that step and simply asks the model for a verdict. From the outside, the two look almost identical—the same prompt shape and rubric-flavored output—but they are different things entirely. Without a human-adjudicated baseline, you are not measuring anything; you are laundering a model’s opinion into a number and calling it evaluation. Because the thing being graded is usually another model’s output, this creates a **slop cycle**, where errors get scored as correct because the grader shares the generator’s blind spots. The distance between grading against a detailed human answer and simply asking the LLM is the distance between a measurement and a guess in a lab coat.

## Ensuring the grader lasts

Even once you have established a judge you can trust, its usefulness can be taken away. Model deprecation is particularly damaging because a great deal of work may have gone into validating the specific nuances of an autograder for a project. Given the rate at which models are removed from closed-source APIs, numerous projects may become impossible to replicate, leaving high-quality benchmarks stranded without a clear grader.

We recommend using an open-source autograder where possible. In all cases, start *first* by creating the human gold-standard set and comparing the LLM’s performance against it, rather than beginning with LLM outputs and conducting retrospective human grading. The former leaves you with an artifact that can validate future models.

## When not to use it

Even a well-validated judge has a bounded remit. It is the wrong tool in a few important cases:

- **Rare or idiosyncratic presentations.** Judges are trained on common cases, just like the systems they grade, and are least reliable exactly where the clinical stakes are often highest.
- **Case-level conclusions about individual patients.** LLM-as-judge is a population-level instrument. “This group of notes systematically understates pain in older adults” is a signal worth acting on; “this specific patient was undertreated” is beyond what it can support.
- **Contested rubrics.** If experts do not agree on the criteria, the model cannot resolve the disagreement for them. A definable standard is a precondition, not an output.
- **Anything treated as ground truth.** Judge outputs are prompt-sensitive, carry the biases of their training data, and can be confidently wrong while sounding authoritative. Ongoing human spot-checking is not optional.

## Why this belongs in post-deployment monitoring

The reason careful LLM-as-judge is worth the trouble is that the failures worth catching after deployment are mostly not in the algorithm. They are in the human-machine team. A system that performs well in a validation study can degrade in use through automation bias, anchoring on the model’s suggestions, alert fatigue, and the gradual deskilling that comes from offloading judgment to a tool. This is the performance paradox described in our comment: accurate systems can lose ground once real people start relying on them. The effect is concrete. After automated polyp detection was introduced, clinicians’ [unaided adenoma-detection rate fell by six percentage points](https://pubmed.ncbi.nlm.nih.gov/40816301/) within a few months.

Those effects surface in clinical data as patterns: propagated documentation errors, missed diagnostic opportunities, and drift in how a tool gets used. Patterns across large volumes are exactly what a validated judge can surface and manual review cannot. That is the case for building these systems—not to replace human oversight, but to let a human standard, once established, watch far more than any human panel could.

## Case study: AI scribes

Ambient AI scribes are the sharpest illustration of the gap. They are at once the most widely deployed form of generative AI in medicine and among the least evaluated on anything that bears on patient care. The workflow is simple: the scribe listens to the encounter and drafts the note; the clinician reviews and signs it. What deployments commonly measure is operational: time spent in notes, after-hours “pajama time,” clinician satisfaction, and burnout. Studies have focused on [documentation burden and efficiency](https://doi.org/10.1001/jamanetworkopen.2024.60637) or [work burden, burnout, and job satisfaction](https://doi.org/10.1093/jamiaopen/ooaf013). Those numbers come straight out of the EHR, and they answer a genuine question: does the tool reduce documentation burden? What they do not establish is whether the note is any good.

The properties that actually matter clinically—whether the note is accurate, whether it invented a finding that was never discussed, whether it dropped something that was, and whether the assessment is complete—are rarely measured once a scribe is live. They can be. Validated instruments like the PDQI-9 exist, and [research studies have used them to grade AI notes against physician-authored ones](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1691499/full). But that grading happens, when it happens at all, in a one-off validation study—not as ongoing scrutiny of the notes being signed every day in production.

This is not just an incomplete picture; it is a hazardous one, because the scribe sits inside a human-machine loop that operational metrics cannot see. A clinician reviewing a fluent, confident note is exposed to automation bias: a fabricated line—such as a normal exam that was never performed or a symptom that was never reported—is easy to wave through and hard to catch. Once signed, it stops being a draft and becomes part of the permanent record, propagating into every later decision and every model subsequently trained on that record. A dashboard tracking minutes saved is blind to all of it. This is one route by which LLM-generated text can contribute to the [degradation of the medical record](https://www.nejm.org/doi/abs/10.1056/NEJMp2405999).

The problem also drifts. Scribes are built on frontier models that vendors version and retire on their own timelines, and a note pipeline validated against one model can quietly shift behavior when the backend is swapped underneath it. Evaluation performed once, at procurement, cannot catch a regression that appears two versions later. What the setting actually calls for is the reverse: continuous assessment of the note content itself, at the scale of every note written.

That is exactly the shape of task LLM-as-judge fits. “Did this note capture what was said, omit what mattered, or assert what was not there?” is a semantic-matching question against a reference, answerable at a volume no human reviewer could approach. Once again, this only works as long as the judge is anchored to a human-graded sample and checked against it over time. Operational metrics tell you whether clinicians like the tool. A validated judge is how you find out whether it is safe.

## The bottom line

The regulatory gap is widening faster than manual evaluation can close it, and LLM-as-judge is one of the few tools that scales to meet it: for standardized tasks, where a human-graded rubric exists, and where the goal is population-level pattern detection.

However, there are also numerous contexts in which large language models may create false confidence and may be worse than no grading at all. The technology can be highly useful in this role, but it is also easy to misuse. A bad judge is worse than none because it hides the absence of evaluation behind the appearance of it.