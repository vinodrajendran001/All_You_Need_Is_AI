---
type: concept
created: 2026-10-16
updated: 2026-10-16
tags: [concept, evaluation, governance, assurance]
source_ids:
  - src-2026-08-30-openai-hugging-face-incident
  - src-2026-09-30-apollo-embedded-evaluations
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

### Publication is part of the control

Agreed reporting schedules, disclosure rules, protected confidential information, and
independent renewal/funding arrangements reduce opportunities to suppress adverse findings.
Developer rebuttals should not become a veto over evaluator conclusions. These are proposed
institutional safeguards, not a demonstrated incentive theorem or existing legal obligation.

## Open questions

- How can access completeness be assessed when the developer controls the evidence surface?
- What resources and planted-counterexample tests justify an adequacy claim?
- How should verdicts expire as training, architecture, deployment, or monitoring changes?

## Related pages

- [[Apollo Research - Principles for Embedded Evaluations]]
- [[Apollo Research]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
- [[Agent Security and Governance]]
- [[Chain-of-Thought Monitoring]]
- [[Benchmark Optimization]]
