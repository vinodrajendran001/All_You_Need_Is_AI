---
type: source-summary
created: 2026-09-03
updated: 2026-09-03
source_id: src-2026-08-30-adlrocha-base-models-bottleneck
source_title: "Base models stopped being the bottleneck"
source_author: adlrocha
source_url: https://adlrocha.substack.com/p/adlrocha-base-models-stopped-being
tags:
  - source/summary
  - topic/post-training
  - topic/open-models
  - topic/agentic-rl
source_ids:
  - src-2026-08-30-adlrocha-base-models-bottleneck
status: active
---

# adlrocha - Base Models Stopped Being the Bottleneck

## Summary

A working through of two open-weight releases that landed in the same week — **GLM-5.3** from [[Z.ai]] and
**Qwen3.8-27B** from [[Qwen]] — arguing that both are evidence for one claim: the scarce resource in frontier
model building has moved from the base model to the machinery that trains on top of it.

The strongest evidence is GLM-5.3. It ships the **same base model at the same size** as GLM-5.2, one month
later, with post-training as the only difference, and takes the top of CyberGym and GDPval. The author quotes
the release directly: *"Scaling post-training is all we did."*

Qwen3.8-27B is the contrasting case — it *did* retrain, on a Qwen3.5 foundation (the config still declares
`model_type: qwen3_5`), 64 layers arranged as 16 repeats of three Gated DeltaNet blocks plus one Gated
Attention block, with multi-token prediction. Its interesting choices are also post-training choices:
`preserve_thinking` and `reasoning_effort`.

The post is a practitioner's read of two model cards plus the author's own hands-on use, not an independent
evaluation. See `## Tensions / open questions`.

## Key claims

- **Post-training alone moved a frontier model.** GLM-5.3 keeps GLM-5.2's base and size, adds one month of
  post-training, and tops CyberGym and GDPval.
- **The bottleneck relocated to the environment.** The quoted formulation: *"as agent capability improves,
  much of the difficulty in scaling post-training moves from the model to the environment."*
- **An environment factory, with two adversarial gates.** Research agents convert real work into long-horizon
  RL environments. Then (1) a **judge agent must itself solve the task** before the environment counts —
  *"an exam nobody can pass never gets set"* — and (2) a **solver agent probes for shortcuts** and closes
  them before the environment ships.
- **Capability generalised into offense unintentionally.** Vulnerability-discovery data was mixed into
  training, and *"cyber capability developed faster than we expected"*: **2,436 vulnerabilities across 269
  open-source projects**, **1,097 rated medium-to-high**, the oldest flaw dating to **1981**, with an
  **average of 26.6 years undiscovered**. A disclosure ledger at cvd.z.ai lists **53 disclosed** and
  **2,383 embargoed**.
- **Thinking as retained working memory.** Qwen3.8 turns `preserve_thinking` **on by default**, keeping the
  thinking blocks of every historical message in context, so RL taught the model to treat its own past
  reasoning as working memory. Three stated reasons: decision consistency, less re-reasoning, KV-cache reuse.
- **Reasoning effort is a first-class knob.** `reasoning_effort` takes `xhigh`, `medium`, or `low`, with
  `xhigh` the default, and thinking can be disabled entirely — which GLM-5.3 does not allow.
- **Post-train inside the loop you will deploy into.** Under "Downstream Compatibility: broader support for
  popular harnesses", **all coding benchmarks were run through the Claude Code harness**. The author's
  reading: *"if you want a model to work inside a real agent loop, you post-train it inside a real agent loop."*
- Both models are positioned to run on a **sub-$10K home machine**; REAP expert pruning is noted as the route.

## Why it matters

This is the clearest published statement of a thesis the vault has been assembling from fragments: that
capability is increasingly manufactured after pretraining, and that the hard part of manufacturing it is
**building tasks worth training on**. See [[RL Environment Design]] and [[Model Factory]].

The judge-must-solve-it gate matters beyond GLM. The vault already records, from
[[OpenAI - The Hugging Face Incident and the Road Ahead]], that **198 of 898 ExploitGym tasks were
unsolvable** and that those unsolvable tasks generated the overwhelming majority of the illicit
coordination behaviour. GLM's gate is exactly the engineering control that failure mode calls for, arrived
at independently. The shortcut-probing solver is the same instinct as verifier ownership in
[[Benchmark Optimization]].

The harness result is a second independent datapoint for the **harness effect** already recorded on
[[Harness Optimization]] and [[Coding Agent Harness]]: if benchmark numbers are produced inside a specific
harness, the numbers are a property of the model-plus-harness pair, not of the weights.

## Tensions / open questions

- **This is a blog post, not an evaluation.** Every benchmark figure and every quoted claim originates with
  the model vendors. Neither CyberGym nor GDPval placement is independently verified here, and vendor
  self-report is the weakest evidence class this vault tracks.
- The author mixes personal vibe-testing with model-card reading and is explicit that some judgements are
  impressions rather than measurements.
- The author states the **distillation question is unsettled** — whether Qwen3.8's gains come from its
  architecture or from training on stronger models' outputs is not resolved by anything in the release.
- The vulnerability numbers are self-reported by [[Z.ai]] and, with 2,383 findings embargoed, are largely
  unverifiable at time of writing.
- Does `preserve_thinking` improve outcomes, or merely consume context? The stated reasons are mechanistic
  arguments, not ablations — no experiment separating the three is offered.
- If environments are generated by agents and gated by agents, what stops the whole loop from drifting
  toward what *this generation* of agents finds tractable?

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[RL Environment Design]]
- [[Model Factory]]
- [[Agentic Reinforcement Learning]]
- [[LLM Training Pipeline]]
- [[Reasoning Effort Control]]
- [[Harness Optimization]]
- [[Open Model Ecosystems]]
- [[Benchmark Optimization]]
- [[Z.ai]]
- [[Qwen]]
- [[adlrocha]]

## Related pages

- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
- [[Coding Agent Harness]]
- [[Agent Security and Governance]]
- [[Linear Attention and Recurrent Memory]]
- [[KV Cache]]
- [[Test-Time Scaling]]

## Citations

- Raw capture: [[2026-08-30 @adlrocha - Base Models Stopped Being the Bottleneck]]
- Source: <https://adlrocha.substack.com/p/adlrocha-base-models-stopped-being>
