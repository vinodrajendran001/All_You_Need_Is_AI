---
type: concept
created: 2026-10-16
updated: 2026-10-27
tags: [concept, evaluation, governance, assurance]
source_ids:
  - src-2026-08-30-openai-hugging-face-incident
  - src-2026-09-30-apollo-embedded-evaluations
  - src-2026-08-02-arise-llm-as-judge
  - src-2026-10-20-guan-beyond-gmean-squared
  - src-2026-10-17-redwood-screwtape
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

## A low bad-output rate can mean the system rarely deployed anything

This page's recurring claim is that an empty alert log is not evidence.
[[Melody Guan et al - Complementary Metrics for Monitorability]] supplies the quantitative version of
the same trap, inside a developer's own re-analysis of its monitoring evaluations.

Its **post-control** metric scores the arrangement rather than the detector: sample up to **K** outputs,
reject the ones a monitor flags, deploy the first accepted output. It reports three quantities, and the
authors insist all three be read together — **B(K)**, the probability of deploying a bad output;
**A(K)**, the probability of deploying anything at all; and **B(K)/A(K)**, the bad fraction among
deployed outputs. A low B(K) is ambiguous between "the gate works" and "the gate almost never passes
anything", and only A(K) separates them. Outcome risk is additionally **base-rate dependent**: a model
that rarely misbehaves can post low post-control risk while being poorly monitorable. For process
evaluations only positive rollouts are scored, so the number is a **positive escape rate** rather than
deployment risk under the model's full output mixture.

Two scoping rules follow, and both are the kind of thing an assurance report has to state rather than
imply. Headline estimates used **K=1** and **K=4**; K=1 required at least **1** valid rollout per
instance and K=4 at least **4**, and a configuration was reported only when at least **5** instances
qualified — so the two retry budgets can rest on **different eligible instance sets** and are not
directly comparable. The retry budget is itself part of the measurement: the recommended reporting set
is dataset-level g-mean², magnitude-aware pair estimates with confidence intervals or HodgeRank
residuals, and the bad-output, deployment, and conditional-bad-output probabilities **with K stated**.

The provenance belongs in the record too. This is **first-party re-scoring by the developer** of its own
existing system-card evaluations — **7** agent-model configurations, GPT-5 at high reasoning effort as
monitor, **500** deterministic hierarchical bootstrap replicates — not independent evaluation under an
access agreement, and **GPT-6 Astra was excluded** because it used a different monitor. In Apollo's
vocabulary this is developer evidence to be reviewed, not a verdict, and nothing here assesses detection
adequacy against planted counterexamples. Its value for this page is narrower and real: a developer
publishing the **reading rules** that stop its own headline number from being over-read is the
disclosure behavior the grade table above is designed to reward. The deployment scheme is also
**hypothetical** — the authors state OpenAI does not deploy current models this way — so it is a
proposed measurement of a proposed arrangement, not a report on a shipped control.

## Open questions

- How can access completeness be assessed when the developer controls the evidence surface?
- What resources and planted-counterexample tests justify an adequacy claim? [[Redwood Research - Screwtape - Adversarial Transcript Editing for Monitor Red-Teaming]] gives a reading rule for the search side: a found attack can refute a specific safety claim, but "the absence of found attacks provides little information about safety".
- How should verdicts expire as training, architecture, deployment, or monitoring changes?
- When a vendor swaps the model behind an unchanged product, who learns of it, and which validation
  must re-run before the new backend reaches users?
- If a developer publishes B(K) without A(K), what does an evaluator ask for, and who checks the
  eligible instance sets behind different retry budgets?
- The post-control metric is simulated with non-adaptive retries on an arrangement its authors say is
  not deployed. It establishes nothing about risk under a live gate, and it is not reported for
  intervention evaluations at all, because the data cannot identify which positive outcome the
  intervention caused.
- The source does not say which of its three metrics a verdict should rest on. It keeps dataset-level
  g-mean² primary and treats disagreement among metrics as a prompt to investigate rather than as a
  decision rule, which leaves the adequacy question this page asks unanswered.

## Related pages

- [[Melody Guan et al - Complementary Metrics for Monitorability]]
- [[Interpretability Evaluation]]
- [[OpenAI]]

- [[Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads]]
- [[LLM-as-a-Judge]]
- [[Apollo Research - Principles for Embedded Evaluations]]
- [[Apollo Research]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
- [[Agent Security and Governance]]
- [[Chain-of-Thought Monitoring]]
- [[Benchmark Optimization]]
- [[Redwood Research - Screwtape - Adversarial Transcript Editing for Monitor Red-Teaming]]
