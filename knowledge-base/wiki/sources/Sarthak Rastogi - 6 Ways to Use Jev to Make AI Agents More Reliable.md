---
type: source-summary
created: 2026-09-30
updated: 2026-09-30
source_id: src-2026-09-25-rastogi-6-ways-jev-agents-reliable
source_title: "6 Ways to Use Jev to Make AI Agents More Reliable"
source_author: Sarthak Rastogi
source_url: https://sarthakai.substack.com/p/6-ways-to-use-jev-to-make-ai-agents
tags: [source/summary, decision-models, ai-agents, routing, governance]
source_ids: [src-2026-09-25-rastogi-6-ways-jev-agents-reliable]
status: active
---

# Sarthak Rastogi - 6 Ways to Use Jev to Make AI Agents More Reliable

## Summary

Sarthak Rastogi writes an adoption guide for placing a typed decision model at the bounded choice
points of an agent while leaving reasoning and prose to an LLM. Six patterns are given: intent
routing, model routing, malicious-intent screening, tool-call gating, confidence-based escalation, and
UI-action selection. The more durable content is the surrounding discipline - narrow context, explicit
schemas, arithmetic in code rather than in the model, shadow-mode rollout, and thresholds chosen after
labelling rather than before. The performance figures are repeated vendor claims, not new evidence.

## Key claims

- Jev returns typed answers with probabilities and **generates no text**; the three primitives are
  `Choice`, `Noul`, and `Score`. A `Noul` of **0.5** means the model cannot tell, not "medium".
- Repeated vendor figures: launched **September 15, 2026**, about **100 milliseconds** response time,
  **$0.042 per million input tokens** with **output tokens free**, and **40x to 200x faster** and
  **up to 400x cheaper** than frontier LLMs on decision-shaped work.
- Routing context: LiteLLM reported **43% savings** and RouteLLM claims up to **85%** from model
  routing, while LLM-as-judge routers add **1 to 5 seconds per request** - the argument for moving the
  routing decision itself off a generative model.
- The tool-call gate sees the task and the pending action but not tool outputs, which Rastogi likens
  to Claude Code's deliberately reasoning-blind classifier. Shipyard is cited as reporting users
  approve about **93% of permission prompts**, which is the case for gating rather than prompting.
- Guardrail pattern: one request per message carrying `Noul` questions for jailbreak, harmful request,
  medical advice, and self-harm, plus a `Score`, attributed to TypeSafe's cookbook using **`jev-1.12`**.
- Rollout discipline: **week 0** pick one simple decision, **week 1** shadow mode, **week 2** label
  **100 to 200 cases**, **week 3** automate only the measured paths. The intent-routing example sends
  anything below **0.6 confidence** to a person, and Rastogi is explicit that the threshold should be
  chosen after measurement.
- Calibration is stated plainly: if Jev says **0.9**, it should be right about **90% of the time**.
- Claimed weaknesses: arithmetic, counting, date logic, images, audio, and video; text only. Named
  open-source alternatives: Kev, openjev, NanoJev, and Laya.

## Why it matters

This is the first source in the vault's typed-decision thread written as an operations guide rather
than an announcement or an explanation, and its sequencing is the contribution: shadow first, label
second, automate third, with thresholds derived from the labels. It also draws the boundary the
category tends to blur - a typed screening model is a filter, not a security boundary, because it does
not treat its input as hostile and adversarial state can move the answer. Least-privilege controls
remain necessary behind it.

## Tensions and caveats

The article adds no benchmark or controlled comparison; its performance numbers restate vendor claims
and are not comparable with the other figures the vault records for the same product - **70-500 ms**,
**20-200x**, **200x/400x**, **193.6x faster**, and **444.6x cheaper** - because none of them travel
with a workload
definition. The TypeSafe cookbook results are vendor-provided and described only as having worked
"pretty well", with no dataset, denominator, confusion matrix, or replication. The recommended
thresholds are advice, not demonstrated calibration. Claims that such a model "cannot hallucinate" do
not survive contact with the distinction between schema validity and semantic correctness. Rastogi
himself advises against the pattern for low-volume, high-consequence decisions.

## Raw capture

- [[2026-09-25 Sarthak Rastogi - 6 Ways to Use Jev to Make AI Agents More Reliable]]

## Affected pages

- [[Typed Probabilistic Decision Models]]
- [[Model Routing]]
- [[Agent Security and Governance]]
- [[Agent Delegation]]
- [[TypeSafe AI]]

## Related pages

- [[LLM-as-a-Judge]]
- [[Tool Use and Function Calling]]
- [[Agentic Loop]]
- [[AI Agents in Production]]
- [[Agent Observability]]
