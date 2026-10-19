---
type: source-summary
created: 2026-10-19
updated: 2026-10-19
source_id: src-2026-08-02-arise-llm-as-judge
source_title: "LLM-as-Judge: When It Works, and When It Misleads"
source_author: "Sri Polkampally, Bhav Jain, Cathy Liu, Liam G. McCoy"
source_url: https://www.arise-ai.org/blog/llm-as-judge
tags: [source/summary, llm-as-judge, evaluation, clinical-ai, post-deployment-monitoring, medical-devices]
source_ids: [src-2026-08-02-arise-llm-as-judge]
status: active
---

# Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads

## Summary

A blog post by four authors writing for ARISE that explains the team's public comment to the
U.S. Food and Drug Administration's Request for Public Comment on measuring and evaluating
real-world performance of AI-enabled medical devices. The comment proposes LLM-as-judge as one
part of post-deployment monitoring, "used carefully and for the right tasks," and the post spends
as much effort on when the technique misleads as on when it helps.

Its central claim is that the line between a useful and a harmful judge is "not the model, the
prompt, or the rubric" but whether a clearly validated, ideally human-expert baseline stands
behind it. Anchored to such a baseline, a judge extends a human standard to volumes no panel can
read. Without one, it is "laundering a model's opinion into a number and calling it evaluation."

This is an argued position from a clinical-AI evaluation group. It cites validation studies and a
clinician-performance result, but reports no agreement statistics, thresholds, or experiments of
its own.

## Key claims

### The gap the comment addresses

- Of roughly a thousand FDA-authorized AI devices, a cited analysis found that more than half
  reported no performance metrics and nearly half described no clinical study. How to keep
  evaluating a deployed system "continuously, at scale, and on the outcomes that actually matter"
  is described as largely unanswered.
- LLM-as-judge is "not a general-purpose oversight system." Its most useful form is **content
  matching**: deciding whether a text carries the same clinical meaning as a reference despite
  different wording. A note recording "TSH elevated, free T4 low" says the same thing as one that
  writes "hypothyroidism." The same flexibility supports checking SOAP structure, whether a
  differential covers the expected diagnoses, or whether a summary dropped content such as the
  medication list.

### Three conditions that build on one another

| Condition | What the authors require |
| --- | --- |
| Validated human baseline (primary) | Experts independently grade a seed set that fixes the criteria and remains the standing benchmark. The judge goes to scale only after its agreement with the human graders clears a **pre-specified threshold**; spot-checked human review then continues. |
| Narrow scope | One common, well-defined failure, in two shapes: **semantic equivalence** to a reference, or **standardized reasoning** against agreed criteria. |
| Benefit from scale | Signals that surface only at volume, such as AI-scribe notes systematically dropping medication reconciliation across thousands of encounters. |

"Miss any one and the technique stops paying off." The post specifies no threshold value,
agreement statistic, or seed-set size.

### Good judges, bad judges, and the slop cycle

- A good judge grades against a detailed, human-adjudicated reference and has been checked to
  confirm that its scores track the human ones, "or a true verifier, where one exists." The cited
  examples are human-like agreement on clinical-summary quality, cardiovascular-endpoint
  adjudication in multicenter and global trials, detection of venous-thromboembolism diagnostic
  delays, and post-deployment monitoring for pulmonary-embolism detection. The capture links these
  studies but reproduces none of their figures.
- A bad judge looks almost identical from outside, with the same prompt shape and rubric-flavored
  output, but has no human-adjudicated baseline. Because it usually grades another model's output,
  it creates a **slop cycle**: errors get scored as correct because the grader shares the
  generator's blind spots. The authors call the result "a guess in a lab coat."

### A validated grader has to last

- Model deprecation on closed-source APIs can make projects impossible to replicate and leave
  "high-quality benchmarks stranded without a clear grader." The authors recommend an open-source
  autograder where possible.
- In all cases, build the human gold-standard set **first** and compare the LLM against it,
  rather than starting from LLM outputs and adding retrospective human grading. The former leaves
  an artifact that can validate future models.

### When not to use it

- **Rare or idiosyncratic presentations**, where judges trained on common cases are least reliable
  and the clinical stakes are often highest.
- **Case-level conclusions about individual patients.** The technique is a "population-level
  instrument": "This group of notes systematically understates pain in older adults" is actionable;
  "this specific patient was undertreated" is beyond what it can support.
- **Contested rubrics.** "A definable standard is a precondition, not an output."
- **Anything treated as ground truth.** Judge outputs are prompt-sensitive, carry training-data
  biases, and can be confidently wrong. "Ongoing human spot-checking is not optional."

### Why post-deployment monitoring needs it

- The failures worth catching after deployment are mostly "in the human-machine team": automation
  bias, anchoring on the model's suggestions, alert fatigue, and gradual deskilling. The comment
  calls this the **performance paradox**: accurate systems can lose ground once people rely on them.
  A cited study found that after automated polyp detection was introduced, clinicians' **unaided
  adenoma-detection rate fell by six percentage points** within a few months.
- **AI scribes** are the sharpest case: described as the most widely deployed form of generative
  AI in medicine and among the least evaluated "on anything that bears on patient care." Deployments commonly
  measure time in notes, after-hours "pajama time," clinician satisfaction, and burnout. Those
  answer whether documentation burden fell, not whether the note is any good.
- Accuracy, fabrication, omission, and assessment completeness are rarely measured once a scribe is
  live. Validated instruments such as PDQI-9 have graded AI notes against physician-authored ones,
  but in one-off validation studies rather than ongoing production scrutiny.
- A fabricated line in a fluent note, such as an exam never performed, is easy to wave through
  under automation bias. Once signed, it becomes part of the permanent record and propagates into
  later decisions and into models trained on that record.
- Scribes run on frontier models that vendors version and retire on their own timelines, so a
  pipeline validated against one model can shift when the backend is swapped. Procurement-time
  evaluation "cannot catch a regression that appears two versions later." The proposed remedy is
  continuous assessment of note content at the scale of every note, by a judge anchored to, and
  checked over time against, a human-graded sample.
- Closing claim: "A bad judge is worse than none because it hides the absence of evaluation behind
  the appearance of it."

## Why it matters

[[LLM-as-a-Judge]] already requires golden-set calibration. This source adds the conditions under
which a calibrated judge should not be used, an explicit unit of inference (populations, not
individual cases), the order of construction (human gold set before automation), and grader
durability as a reproducibility problem. It gives [[Embedded Evaluation]] a regulated-deployment
instance of evaluation that expires when the evaluated system changes. It also gives
[[LLM Application Resilience]] and [[Agent Observability]] a domain where semantic failures pass
every operational dashboard and also pass the human signer.

## Tensions / open questions

- The primary safeguard is an agreement threshold the post never quantifies. Agreement measured on
  a common-case seed set says little about the rare presentations the authors exclude, and the
  human graders' own inter-rater agreement is not discussed.
- Scale assumes a reference to match against. For production scribe notes, the capture does not
  say what the reference is, how it is produced, or how its own errors are handled.
- Population-level monitoring finds systematic patterns; it does not identify which signed note is
  wrong. Correcting an individual note still depends on reviewers the post describes as exposed to
  automation bias.
- The open-source recommendation answers deprecation, not grader quality. The capture compares
  neither open and closed graders on clinical tasks nor states what must be archived for a grader
  to remain reproducible.
- The polyp result concerns clinician performance after detection assistance was introduced. It
  motivates monitoring the human-machine team; it is not evidence that an LLM judge detects
  deskilling.
- The public comment is a submission to an FDA request for comment, not an adopted requirement.

## Affected pages

- [[LLM-as-a-Judge]]
- [[Embedded Evaluation]]
- [[LLM Application Resilience]]
- [[Open Model Ecosystems]]
- [[Benchmark Optimization]]
- [[Agent Observability]]

## Raw capture

- [[LLM-as-Judge When It Works, and When It Misleads]]

## Citations

- Canonical article: <https://www.arise-ai.org/blog/llm-as-judge>
- Published August 2, 2026; captured October 19, 2026. Authors per the capture's metadata: Sri
  Polkampally, Bhav Jain, Cathy Liu, and Liam G. McCoy. The body attributes the comment to "our
  team at ARISE" and does not expand the name.
- Public comment explained by the post: <https://www.regulations.gov/comment/FDA-2025-N-4203-0062>.
  Neither the comment nor the linked studies were read separately for this summary.
- Device-reporting analysis cited in the opening: <https://doi.org/10.1038/s41746-025-02052-9>.

## Related pages

- [[LLM-as-a-Judge]]
- [[Embedded Evaluation]]
- [[LLM Application Resilience]]
- [[Open Model Ecosystems]]
- [[Benchmark Optimization]]
- [[Agent Observability]]
- [[Sycophancy]]
- [[Apollo Research - Principles for Embedded Evaluations]]
