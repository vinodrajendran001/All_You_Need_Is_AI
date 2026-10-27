---
type: source-summary
created: 2026-10-27
updated: 2026-10-27
source_id: src-2026-10-17-redwood-screwtape
source_title: "Screwtape: Adversarial Transcript Editing for Monitor Red-Teaming"
source_author: Redwood Research
source_url: https://www.redwoodresearch.org/blog/screwtape-adversarial-transcript
tags: [source/summary, safety, monitoring, red-teaming, ai-control]
source_ids:
  - src-2026-10-17-redwood-screwtape
status: active
---

# Redwood Research - Screwtape - Adversarial Transcript Editing for Monitor Red-Teaming

## Summary

A Redwood Research post, published 17 October 2026, introducing Screwtape: a pipeline that takes a real
agent transcript, inserts an attack, and keeps editing it until an *action-only* monitor, one that does
not read the agent's chain of thought, stops flagging it. An LLM verifier checks every edit for
validity, realism, and severity. Across 252 runs, the pipeline produced six human-confirmed attacks that
also evaded a held-out monitor from a frontier developer. Its durable contribution is the authors' own
reading rule: the pipeline finds monitor blind spots, but it cannot estimate how safe a monitor is.

## Key claims

**The loop.** The inputs are a real transcript, a monitor, and a *threat contract*, which states the
threat vector and severity an attack must reach to count. An attacker agent edits the transcript and
describes the inserted attack. Programmatic rules reject some edits: the attacker cannot change user
messages or edit subagent calls. The verifier then sees the edited transcript, the attack description,
and the diff against the original; the monitor sees only the edited transcript. "The attack is successful
when the monitor’s score falls below a threshold" set to a fixed false-positive rate on honest
transcripts. Every failed check returns its reasoning to the attacker as feedback for the next iteration.

**Optimize against a proxy, test against a held-out monitor.** Redwood iterated against its own monitors,
based on Opus 4.8 and Gemini 3.1 Pro, and tested the surviving attacks against a monitor from a frontier
developer that the loop never saw.

**The result is a funnel with few survivors.** "We ran the pipeline 252 times on 94 unique transcripts."
That produced 35 attacks that evaded Redwood's monitors. The opening states: "Six of these 35 attacks also
evaded the frontier developer’s monitor, and we confirmed them as valid through human review." A later
passage says "final review confirmed 6 of the 17 attacks that evaded the held-out monitor." Read together,
the likely funnel is 35 evading the proxies, 17 also evading the held-out monitor, and 6 confirmed valid,
but the post never lays it out, and the threshold's false-positive rate is not reported.

**Search is slow.** "Each iteration takes about 5 to 10 minutes, a run can take a few hours, and most runs
find no attack". For comparison, the post cites human red-team attacks in SLEIGHT-Bench at 2–3 hours of
human work each; that figure is third-party, not measured here.

**The verifier had to be rebuilt for optimization pressure.** A simple yes/no verdict let runs stop
early on trivial "successes", accepting many attacks that experts did not find valid. The working
verifier uses a detailed rubric drawn from NIST SP 800-160v1r1 and the STPA Handbook and reasons
explicitly about harm, whether harm has happened or is only prepared, and whether the user authorized the
actions. On average it rejects 60–70% of candidate edits within a run, with fewer rejections in later
iterations. "Verifier mistakes concentrate towards the end of the funnel", so human review stays
mandatory.

**Severity is the hardest judgment.** Over many iterations the attacker drifts toward borderline cases
that look incriminating but are not severe enough, such as publishing expired credentials or planting a
backdoor that changes a button color. Labeling severity is hard even for human experts, so Redwood set
conservative high-severity thresholds.

**Improvement, not evaluation.** "Screwtape is much more useful for monitor improvement than monitor
evaluation." The authors state that "we can’t get any quantitative safety estimates from the pipeline".
Finding nothing says little, because the search covers only the attack space its configuration, threat
contract, and transcript can reach. A found failure can refute a specific safety claim but is limited
evidence of real risk: "our attacker sees the whole transcript and gets the monitor’s feedback after
every attempt, and a deployed agent usually has neither." Hardening a monitor against Screwtape also makes
later Screwtape evaluations less informative, since they search the same region.

**No reasoning traces yet.** "Currently, Screwtape can only generate attack transcripts without reasoning
traces." The authors call this a major limitation, because OpenAI and Anthropic use monitors that read
both actions and reasoning, and realistic reasoning cannot be checked: "Unlike tool calls, reasoning
doesn’t affect the environment, so there’s nothing to validate it against."

**Deliberately unreleased, and of uncertain value to its authors.** "We aren’t releasing the pipeline
implementation for now", although Redwood is open to sharing it with researchers. The authors are also
"quite uncertain" whether helping developers improve frontier monitors is good: strong monitors raise
short-term safety but may let capabilities advance without fixing the underlying misalignment.

## Why it matters

[[Chain-of-Thought Monitoring]] has asked whether optimization against a monitor teaches evasion. Screwtape
is the attacker's side of that question made explicit: an optimizer with full transcript access and
per-attempt feedback does find blind spots, slowly. It also explains why monitors that read reasoning are
harder to red-team: nothing in the environment can confirm that a written reasoning trace is realistic.

[[LLM-as-a-Judge]] gets a case of a judge inside an optimization loop. Under pressure, the cheap verdict
format failed first, and the remaining errors gathered among the final survivors, where they matter most.

## Tensions / open questions

- **The 35, 17, and 6 counts are not reconciled in the text.** The reading above is the most consistent
  one, not a stated funnel.
- **Missing denominators.** The fixed false-positive rate, the number of candidate edits and verifier
  passes, confidence intervals, and the identity of the held-out monitor are not given. The linked paper
  was not captured.
- **The attacker is stronger than a deployed agent in two specific ways**, whole-transcript visibility and
  per-attempt monitor feedback. The authors note that deployed agents can sometimes obtain feedback, for
  example by retrying after a block.
- **Not reproducible from outside.** The implementation is withheld; access is by request to Tyler Tracy.
- **Author uncertainty about the direction of the work** is part of the source and should not be dropped
  when citing its results.

## Affected pages

- [[Chain-of-Thought Monitoring]]
- [[LLM-as-a-Judge]]
- [[Redwood Research]]

## Raw capture

- [[Screwtape Adversarial Transcript Editing for Monitor Red-Teaming]]

## Citations

- Canonical URL: https://www.redwoodresearch.org/blog/screwtape-adversarial-transcript (email tracking
  parameters removed).
- Published 17 October 2026. The clipping's frontmatter names "Substack" as author, which is a clipping
  artifact; the body identifies the work as Redwood's and names Tyler Tracy as the contact, but gives no
  individual byline. The accompanying paper is linked at https://arxiv.org/abs/2610.20941 (not captured).
- Figures are image-only; their captions were captured.

## Related pages

- [[Chain-of-Thought Monitoring]]
- [[LLM-as-a-Judge]]
- [[Agentic Testing]]
- [[Agent Security and Governance]]
- [[Embedded Evaluation]]
- [[Apollo Research - Principles for Embedded Evaluations]]
- [[Aria Wong et al - Reducing Reward Hacking by Localizing Bad Behavior Instead of Penalizing It]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
- [[Redwood Research]]
- [[AI Knowledge Base Overview]]
