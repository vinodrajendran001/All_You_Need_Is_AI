---
type: entity
created: 2026-11-13
updated: 2026-11-13
entity_kind: organization
tags:
  - entity
  - organization
  - evaluation
  - safety
source_ids:
  - src-2026-11-09-zvi-ai-rd-acceleration-rsi
  - src-2026-11-09-tillman-two-kinds-test-time-scaling
  - src-2026-08-30-openai-hugging-face-incident
  - src-2026-09-30-apollo-embedded-evaluations
status: active
---

# METR

## What it is

An AI evaluation organization that publishes model evaluation reports (the vault's captures link to
them under `metr.org/evaluations`). The captures never spell out the name. Staff who appear in the
vault, labeled "(METR)" in Zvi Mowshowitz's capture, include Ajeya Cotra, Charles Foster, and Ryan
Greenblatt. The vault has no METR-authored capture. Every METR claim here reaches the vault through
another author.

## Why it matters here

METR appears in three different roles, and each needs its own reading rule.

**Deep-access assessor of a lab's AI R&D speed-up.**
[[Zvi Mowshowitz - AI R&D Is Accelerating Towards Potential RSI in 2027]] quotes METR's November 2026
assessment of AI R&D acceleration at [[Anthropic]]. METR concludes, as quoted, that Anthropic is likely
improving capabilities on well-specified tasks at around twice its earlier rate. It adds that it
"would not be surprised" if the true figure were closer to 1.3x or 3x, and it attributes a majority,
"perhaps ≈80%", of the acceleration to AI. The benchmark figure behind this is **1.9x** on AECI,
Anthropic's version of the [[Epoch AI]] Capabilities Index, with a **95% CI of 1.5-2.8x**. It falls
to **1.4x** when non-Anthropic models are included. METR saw about ten categories of internal
evidence and interviewed about **15** key staff. In return Anthropic could redact anything, and it
removed "a majority of the evidence we found most informative". This is the vault's main
quantitative input to [[Recursive Self-Improvement]].

**Model evaluator.** [[James Tillman - Two Kinds of Test-Time Scaling]] cites METR's report that
compaction does not increase GPT-5.1-Codex-Max's time horizon. Tillman calls the evidence for that
model ambiguous, because it also shows a large efficiency gain from further chain-of-thought on the
UK AISI chart (see [[Test-Time Scaling]]).

**Incident investigator.** [[OpenAI - The Hugging Face Incident and the Road Ahead]] reports that
METR and [[Redwood Research]] published an independent investigation of the incident's alignment
issues on the same day as OpenAI's report. That investigation is not captured.

## Notes

### Independence under negotiated access

The vault has a yardstick for METR's Anthropic report.
[[Apollo Research - Principles for Embedded Evaluations]] proposes that public reports state
requested, granted, and denied access. It says redactions should identify the kind and importance of
withheld information without suppressing the overall conclusion, and that a developer may rebut but
should not veto. As quoted by Zvi, METR's public report partly fits:

- **Where it fits.** It publishes a conclusion, lists what it saw, and names the categories that were
  redacted, such as forecasts for a future model and the breakdown into compute, data, and algorithms.
- **Where it falls short.** METR says the public version does not achieve "transparency about
  evidence".
- **Independence.** Anthropic cofounder Sam McCandlish says METR had complete independence to form
  its own conclusions.

Zvi suspects that METR's need for continued cooperation from labs pushes it toward *under*reporting.
That is his inference, not something METR says. See [[Embedded Evaluation]].

### Its own staff disagree in public

Staff commentary is not the report:

- Cotra uses a simple economic model to argue that doubling overall progress needs about a 4-9x labor
  speed-up.
- Greenblatt, working from public information only, gives a very rough estimate of **~4.5x**.
- Foster explains that each ECI point multiplies a model's odds of success.

Zvi also notes that METR's team "did not expect substantial acceleration". Greenblatt had expected
only **1.15x-1.3x** for 2026.

## Boundaries

All three appearances are secondhand. Zvi's capture quotes the Anthropic report selectively and
argues for a strong conclusion. Tillman cites the Codex-Max finding in one sentence. The Hugging Face
investigation is only mentioned. The vault does not record METR's methods, its funding, or how it
defines time horizon beyond Foster's remark that **5** ECI points have historically corresponded to
roughly a doubling. Do not merge the 1.9x AECI figure, the "around twice" conclusion, the 1.4x
all-developer figure, and staff estimates into one number.

## Related pages

- [[Anthropic]]
- [[Redwood Research]]
- [[Apollo Research]]
- [[Epoch AI]]
- [[OpenAI]]
- [[Embedded Evaluation]]
- [[Recursive Self-Improvement]]
- [[Automated AI Research]]
- [[Benchmark Optimization]]
- [[Test-Time Scaling]]
- [[Zvi Mowshowitz - AI R&D Is Accelerating Towards Potential RSI in 2027]]
- [[James Tillman - Two Kinds of Test-Time Scaling]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
- [[Apollo Research - Principles for Embedded Evaluations]]
