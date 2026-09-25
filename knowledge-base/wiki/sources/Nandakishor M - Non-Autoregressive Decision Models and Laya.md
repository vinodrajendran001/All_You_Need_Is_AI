---
type: source-summary
created: 2026-09-25
updated: 2026-09-25
source_id: src-2026-09-18-nandakishor-nonautoregressive-decisions
source_title: "I Built Non-Autoregressive Decision Models a Year Ago. Then a Frontier Lab Called It a Breakthrough"
source_author: Nandakishor M
source_url: https://dev.to/nandakishor_m_6cc0adfde9f/i-built-non-autoregressive-decision-models-a-year-ago-then-a-frontier-lab-called-it-a-18me
tags: [source/summary, decision-models, reinforcement-learning, calibration]
source_ids: [src-2026-09-18-nandakishor-nonautoregressive-decisions]
status: active
---

# Nandakishor M - Non-Autoregressive Decision Models and Laya

## Summary

Nandakishor M presents Laya as an open, approximately 421M-parameter typed decision model and argues
that his earlier work predates TypeSafe AI's Jev. He claims it combines a bidirectional encoder,
typed questions, reinforcement learning intended to improve calibration, and an explicit
act-versus-escalate policy.

## Key claims

- Laya combines a **395M** ModernBERT-large backbone with decision components for about **421M**
  parameters and evaluates multiple choice, score, and binary questions in one forward pass.
- Its reward combines logarithmic, spherical, and ranked-probability scores across eight noisy
  samples; the Act/Escalate rewards imply acting only above **0.625** estimated correctness.
- The author reports **33-38 ms** GPU latency, **83.8%** macro accuracy and **0.060 ECE** across
  23,024 in-task questions, and **65.1% / 0.207 ECE** on 2,400 zero-shot questions.
- At 50% coverage the reported accuracy is **92.2%**. Confidence uses normalized Shannon entropy.

## Why it matters

Typed probabilistic decisions are a broader design pattern than one vendor product. Laya also makes
selective automation explicit: a system intended to automate selectively can use an escalation
action in addition to a label.

## Tensions and caveats

The priority claim, Laya benchmarks, and comparison with Jev are self-reported by Laya's builder.
There is no controlled cross-system benchmark or independent reproduction. "Same core idea" does
not establish copied implementation, and calibration metrics do not establish correctness in new domains.

## Raw capture

- [[2026-09-18 Nandakishor M - Non-Autoregressive Decision Models and Laya]]

## Affected pages

- [[Typed Probabilistic Decision Models]]
- [[Inference Efficiency Frontier]]
- [[LLM-as-a-Judge]]
- [[TypeSafe AI]]

## Related pages

- [[Diogo Almeida - Introducing System One Models and Jev]]
- [[Reinforcement Learning]]
- [[Agent Security and Governance]]
