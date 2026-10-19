---
type: concept
created: 2026-10-16
updated: 2026-10-19
tags: [concept, evaluation, governance, assurance]
source_ids:
  - src-2026-08-30-openai-hugging-face-incident
  - src-2026-09-30-apollo-embedded-evaluations
  - src-2026-08-02-arise-llm-as-judge
status: active
---

# Embedded Evaluation

## Definition

Embedded evaluation is an ongoing assessment arrangement in which independent evaluators
receive deep access to a model developer's training and internal deployment. In the
[[Apollo Research - Principles for Embedded Evaluations]] proposal, evaluators assess
predeclared claims about scheming and loss-of-control risk and publish qualified verdicts.
It is not simply running a release benchmark or assigning a company one safety label.

## Why it matters

Independence requires more than a separate grader. Access, resources, disclosure incentives,
and the right to publish determine what an evaluator can actually discover. The process
must also distinguish "we found no counterexample" from "our methods were capable of finding
one within the stated scope."

## Current synthesis

### Specify claims before evaluating them

Apollo proposes both standard claims shared across developers and recommended claims
responsive to particular risks or incidents. This limits cherry-picking without pretending
all systems have the same risks. Evaluators review developer evidence, independently
investigate, and then assess detection adequacy if no counterexample emerges.

The proposed grades keep access and disclosure behavior distinct from incident severity:

| Grade | Verdict | What it establishes |
| --- | --- | --- |
| A | Verified | No counterexample found and methods likely adequate, subject to uncertainty |
| B | Unrefuted | No counterexample found, with material evidence or detection gaps |
| C | Self-reported | Developer evidence contradicts its claim |
| D | Evaluator-found | Evaluator found a counterexample beyond developer disclosure |
| E | Blocked | Insufficient access to meaningfully attempt falsification |

A severe self-reported incident can receive C; E does not prove a particular unsafe behavior.
Reports therefore need separate descriptions of scope, confidence, severity, outstanding
requests, and limitations. A refuted original claim stays visible even if remediation permits
a narrower fallback claim with its own verdict.

### A retrospective success is not prospective coverage

[[OpenAI - The Hugging Face Incident and the Road Ahead]] reports that retrospective
chain-of-thought monitoring would have detected relevant activity more than a day before
the breach, but the monitor was not deployed on the affected evaluations. That first-party
account illustrates why monitor capability and actual coverage are separate claims.

Apollo's proposed method asks whether realistic planted attempts would be detected and
which workloads remain unobserved. It does not independently validate OpenAI's account or
assign it an Apollo grade. The synthesis is procedural: an empty alert log means little
without evidence about what was monitored and what the monitor could detect.

### A deployment-time validation expires when the backend changes

[[Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads]] makes the verdict-expiry
problem concrete for deployed clinical AI. AI scribes run on frontier models that vendors version and
retire on their own timelines, so a pipeline validated against one model can shift behavior when the
backend is swapped underneath it. Evaluation performed once, at procurement, "cannot catch a
regression that appears two versions later." The authors propose continuous assessment of the
outputs themselves, by an LLM judge anchored to a human-graded sample and spot-checked against it
over time.

That human-graded seed set does work similar to Apollo's detection-adequacy step: it is evidence
about what the monitor can detect, not only a record of what it flagged. The authors' closing claim
restates the empty-alert-log point above: "A bad judge is worse than none because it hides the
absence of evaluation behind the appearance of it." The arrangement is not embedded evaluation in
Apollo's sense. It concerns population-level monitoring of a deployed product, not independent
access to a developer's training and internal deployment, and it does not address evaluator
independence or publication rights. It specifies no agreement threshold, and a common-case seed set
cannot establish detection of the rare presentations the authors exclude. Like Apollo's principles,
it is a proposal, here a public comment to an FDA request for comment, not an adopted requirement.

### Publication is part of the control

Agreed reporting schedules, disclosure rules, protected confidential information, and
independent renewal/funding arrangements reduce opportunities to suppress adverse findings.
Developer rebuttals should not become a veto over evaluator conclusions. These are proposed
institutional safeguards, not a demonstrated incentive theorem or existing legal obligation.

## Open questions

- How can access completeness be assessed when the developer controls the evidence surface?
- What resources and planted-counterexample tests justify an adequacy claim?
- How should verdicts expire as training, architecture, deployment, or monitoring changes?
- When a vendor swaps the model behind an unchanged product, who learns of it, and which validation
  must re-run before the new backend reaches users?

## Related pages

- [[Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads]]
- [[LLM-as-a-Judge]]
- [[Apollo Research - Principles for Embedded Evaluations]]
- [[Apollo Research]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
- [[Agent Security and Governance]]
- [[Chain-of-Thought Monitoring]]
- [[Benchmark Optimization]]
