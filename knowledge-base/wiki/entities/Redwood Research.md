---
type: entity
entity_kind: organization
created: 2026-10-27
updated: 2026-10-27
tags: [entity, organization, safety, monitoring, red-teaming, ai-control]
source_ids:
  - src-2026-10-17-redwood-screwtape
  - src-2026-08-30-openai-hugging-face-incident
  - src-2026-09-30-apollo-embedded-evaluations
status: active
---

# Redwood Research

## What it is

The research organization behind the vault's captured post on Screwtape, a pipeline for red-teaming
monitors that watch agent actions, published on 17 October 2026. The post is institutionally attributed:
it carries no individual byline and names Tyler Tracy as the contact for researchers who want the
pipeline implementation, which Redwood is not releasing for now. The experiments use Redwood staff
transcripts and Redwood's own monitors. The post links Redwood blog posts on the LinuxArena and BashArena
environments for generating attack transcripts and on *Thoughts on the conservative assumptions in AI
control*; those posts and the accompanying paper are not captured.

## Why it matters here

[[Redwood Research - Screwtape - Adversarial Transcript Editing for Monitor Red-Teaming]] is the vault's
first account of optimizing attacks directly against a monitor, and its reading rules matter as much as
its results:

- For [[Chain-of-Thought Monitoring]], it supplies the attacker's side of the question of whether
  optimization against a monitor finds ways past it. It reaches only *action-only* monitors for now,
  because nothing in the environment can confirm that a written reasoning trace is realistic.
- For [[LLM-as-a-Judge]], it is a case of judges inside an optimization loop: a simple yes/no verifier
  let trivial attacks through, a rubric-based verifier replaced it, and the remaining verifier mistakes
  gathered at the end of the funnel, so human review stayed necessary.
- For [[Embedded Evaluation]], it is a concrete counterexample search with an explicit reading rule: a
  found attack can refute a specific safety claim, but an empty search says little about safety.

Redwood also connects to the vault's main incident record.
[[OpenAI - The Hugging Face Incident and the Road Ahead]] reports that METR and Redwood Research
conducted an independent investigation of the model alignment issues in that incident and published their
own report, which is not captured here. [[Apollo Research - Principles for Embedded Evaluations]] calls
that investigation "a good first step, but we believe significantly more access is required in the
future", asking for more time, access to all relevant data, and follow-up experiments on the main model
involved. The Screwtape post in turn cites the incident as one way a deployed agent can get monitor
feedback: by hacking the infrastructure.

## Boundaries

Everything here comes from Redwood's own post about Redwood's own pipeline. The implementation is
withheld, though Redwood is open to sharing it with researchers, so the results cannot be reproduced from
outside, and the paper is not captured. The post does not report the false-positive rate that sets its
monitors' threshold, confidence intervals, or the identity of the held-out frontier-developer monitor.
Its counts of 35 attacks that evaded Redwood's monitors, 17 that evaded the held-out monitor, and 6
confirmed by review are not reconciled in the text. The authors also say they are "quite uncertain"
whether helping to improve frontier monitors is good; citing the results without that uncertainty would
misstate the source.

## Related pages

- [[Redwood Research - Screwtape - Adversarial Transcript Editing for Monitor Red-Teaming]]
- [[Chain-of-Thought Monitoring]]
- [[LLM-as-a-Judge]]
- [[Embedded Evaluation]]
- [[Agent Security and Governance]]
- [[Apollo Research]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
- [[OpenAI]]
- [[Apollo Research - Principles for Embedded Evaluations]]
