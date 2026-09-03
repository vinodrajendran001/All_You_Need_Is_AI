---
type: entity
entity_kind: organization
created: 2026-09-03
updated: 2026-09-03
tags: [entity, open-models, china, post-training, agentic-rl]
source_ids:
  - src-2026-08-30-adlrocha-base-models-bottleneck
status: active
---

# Z.ai

The lab behind the **GLM** family of open-weight models. Within this vault it is known primarily through
GLM-5.3, and through the unusual amount its release disclosed about *how* the model was made.

## Why it matters to this vault

Z.ai supplies the vault's single strongest datapoint for the claim that post-training has become the binding
constraint on frontier capability. Per [[adlrocha - Base Models Stopped Being the Bottleneck]], **GLM-5.3
keeps GLM-5.2's base model at the same size**, adds one month of post-training and nothing else, and reaches
the top of CyberGym and GDPval. The lab's own summary: *"Scaling post-training is all we did."*

The mechanism disclosed alongside it is the **environment factory** — research agents converting real work
into long-horizon RL environments, gated by a judge agent that must itself solve each task before it counts,
and a solver agent that probes for shortcuts and closes them. That construction is the anchor of
[[RL Environment Design]], and its judge gate is an independently-arrived-at answer to the unsolvable-task
failure documented in [[OpenAI - The Hugging Face Incident and the Road Ahead]].

Z.ai is also the vault's clearest case of **capability generalising into offense unintentionally**. After
vulnerability-discovery data was mixed into training, the lab reported that *"cyber capability developed
faster than we expected"*, subsequently publishing **2,436 vulnerabilities across 269 open-source projects**,
**1,097 rated medium-to-high**, the oldest dating to **1981**, with an **average of 26.6 years undiscovered**.
A disclosure ledger at cvd.z.ai lists **53 disclosed** against **2,383 embargoed**. This is a substantial
contribution to [[Self-Replicating Agents]] and [[Agent Security and Governance]] — offensive capability
arriving as a byproduct of a general training decision rather than as a target.

GLM-5.3 does **not** allow thinking to be disabled, in contrast to [[Qwen]]'s approach — a live comparison for
[[Reasoning Effort Control]]. GLM models also appear as the worked serving example in
[[Philip Kiely - The Efficient Frontier of LLM Inference]] and in the LLM expansion of
[[Baseten - Agentic Kernels in Production]], which places the family firmly inside the vault's inference
coverage as well.

## Caveats

Everything above originates in Z.ai's own release materials, read secondhand through a blog post. Benchmark
placements are self-reported and not independently verified here, and with 2,383 vulnerability findings under
embargo the headline security numbers are largely unverifiable at time of writing.

## Related pages

- [[adlrocha - Base Models Stopped Being the Bottleneck]]
- [[RL Environment Design]]
- [[Model Factory]]
- [[Open Model Ecosystems]]
- [[Qwen]]
- [[Reasoning Effort Control]]
- [[Agentic Reinforcement Learning]]
- [[Self-Replicating Agents]]
- [[LLM Training Pipeline]]
