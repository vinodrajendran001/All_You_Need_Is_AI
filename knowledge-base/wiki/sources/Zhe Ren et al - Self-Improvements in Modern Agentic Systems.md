---
type: source-summary
created: 2026-08-03
updated: 2026-10-19
source_id: src-2026-07-24-ren-et-al-self-improvements-agentic-systems-survey
source_title: "Self-Improvements in Modern Agentic Systems: A Survey"
source_author: Zhe Ren et al.
source_url: https://arxiv.org/html/2607.13104v1
tags: [source/summary, ai-agents, self-improvement, survey]
source_ids: [src-2026-07-24-ren-et-al-self-improvements-agentic-systems-survey]
status: active
---

# Zhe Ren et al - Self-Improvements in Modern Agentic Systems

## Summary

A survey by twelve authors from Jilin University, KAUST, the University of Alberta, IDSIA, and an
independent researcher, with Jürgen Schmidhuber among them. It models a foundation-model (FM) agent
as a configuration `A_t = (θ_t, Σ_t)`: model parameters plus an operational **scaffold**
`Σ_t = (p_t, m_t, T_t, g_t)` of prompts, memory, tools, and control logic. The survey notes that the
scaffold is also called an agent harness. Self-improvement is a self-induced operator that turns
signals from the agent's own execution into **durable** updates to either component. The
ephemeral execution state (KV caches, intermediate plans, short-term working memory) is not part of
the configuration.

Prior work is organized first by what is updated, then by where the learning signal comes from.
This is a taxonomy and literature review, not a new experiment. Results it mentions belong to the
surveyed papers. The capture ends mid-sentence in section 6.2.1, before the tool, full-scaffold,
application, evaluation, and safety sections.

## Key claims

### Definitions

- **Durable versus transient.** The update operator commits durable changes; for the scaffold,
  changes "intended to endure beyond individual task boundaries." They are "not strictly
  irreversible and may be undone." The operator is history-aware (`θ_1:t`, `Σ_1:t`), which the
  survey says supports validation and rollback of harmful updates.
- **Two modes of self-reference.** In the *distributional* mode, the agent's behavior generates
  data, preferences, or critiques that an update rule consolidates into parameters (foundation-model
  improvement). In the *action-level* mode, the agent directly edits its prompts, memory, tools, or
  control logic (scaffolding improvement). Parameter updates are slower, costlier, and more global.
  Scaffold updates are "typically faster, more reversible, and more context-dependent."
- **A skill is a reusable update, not a substrate.** A skill is a named, retained instance of the
  update operator. It can be serialized into a tool, an instruction or workflow, a memory entry,
  consolidated weights, or control logic. *Object-level* skills act on the task. *Meta-level*
  skills edit the agent's own configuration, so the operator can become part of its own operand.
- **Relation to RL.** Parameter updates are ordinary policy optimization under a fixed decision
  process. Scaffold updates sit outside the standard RL formulation because they reshape the
  effective state-action space and observation processing. They are discrete, inspectable
  artifacts usually changed by search or edits, not gradients.

### Parameter-update signals

| Signal | Forms the survey describes |
| --- | --- |
| Intrinsic generative demonstrations | Self-generated instruction pairs, reasoning traces, and structured trajectories, with self-consistency or unit-test filtering and curriculum generation |
| Intrinsic evaluative feedback | Rubric judging (Constitutional AI, Meta-Rewarding), consistency signals (majority vote, entropy, self-certainty), and critique-and-revision |
| Extrinsic exploratory experience | Grounded environments with programmatic verifiers, learned reward models, or self-generated tasks; and simulated proxies built on learned world models |

### Scaffold updates in the capture

- **Prompts** are grouped by signal richness: scalar scores (APE, OPRO), natural-language critiques
  (Reflexion, ACE), population-based evolution (Promptbreeder, GEPA), and textual gradients (APO,
  TextGrad, MetaTextGrad). Richer signals are associated with less heuristic, more sample-efficient
  updates.
- **Memory** is split into objects, structure, and processing. Explicit objects are processed
  trails, curated raw content, and integrated external knowledge. Implicit objects are latent
  tokens, hidden states, and KV-cache augmentations. Explicit memory is auditable but spends
  context; implicit memory is compact but hard to inspect and prone to drift.

### Failure modes and safeguards

- Self-consistency fails when the model is confidently wrong. An evaluator coupled to the policy can
  reinforce shared blind spots. Recursive training on generated data risks collapse and diversity
  loss.
- Proposed safeguards: separate generator and evaluator checkpoints or model families, human
  annotations as external anchors, evaluator disagreement treated as uncertainty, generated
  demonstrations accumulated on top of retained data, and human auditing.
- For extrinsic experience, the survey names reward hacking through language (a verifier's
  specification is itself manipulable text), capability regression from narrow RL, hallucinated
  world-model dynamics, and the tension between trajectory length and the context window.
- A surveyed system, GLoW, is reported to need "100–800× fewer real environment interactions than RL
  baselines" in text-based games. This is the cited paper's result, not the survey's.

## Why it matters

The parameters-plus-scaffold split gives [[Recursive Self-Improvement]] its workflow-level versus
model-level boundary. It gives [[Agent Memory]] a write-back test and [[Agent Skill]] a
substrate-independent definition. The RL mapping explains why [[Harness Optimization]] does not
reduce to [[Agentic Reinforcement Learning]]: one optimizes a policy, the other changes the decision
process it acts in.

## Tensions / open questions

- **Forgetting is described two ways.** Section 4.2 says scaffold adaptation comes "without the
  risks of catastrophic forgetting." Section 3.3 says externalizing adaptation "does not eliminate
  forgetting" and adds memory poisoning, tool-semantics drift, and brittle template dependence.
- **"KV state" covers two things.** Transient KV caches are outside the configuration, but KV-cache
  augmentations and latent memory pools count as implicit memory objects.
- **The memory scorecard has no values here.** Table 3's 1–5 ordinal ratings are a literature
  synthesis, not a benchmark, and the scores did not survive the clipping.
- **The lineage is partly the authors' own.** The history foregrounds self-referential work
  associated with co-author Schmidhuber (fast-weight programmers, the success-story algorithm, the
  Gödel Machine). It also presents in-context learning through the KV cache as functionally
  equivalent to 1991 fast-weight programmers. Read this as the authors' historiography.
- **Truncation.** The capture does not support claims about memory structure and processing, tools,
  full-scaffold redesign, applications, evaluation protocols, or safety. The introduction promises
  all of them.

## Affected pages

- [[Agent Memory]]
- [[Agent Skill]]
- [[Recursive Self-Improvement]]

## Raw capture

- [[2026-07-24 Zhe Ren et al. - Self-Improvements in Modern Agentic Systems A Survey|Self-Improvements in Modern Agentic Systems A Survey]]

## Citations

- Canonical URL: <https://arxiv.org/html/2607.13104v1> (arXiv HTML, version 1).
- Captured July 24, 2026; the capture records no publication date.
- Authors per the capture: Zhe Ren, Yimeng Chen, Dandan Guo, Guowei Rong, Tonghui Li, R.B. Xiong,
  Qingfeng Lan, Wenyi Wang, Li Nanbo, Yibo Yang, Mingchen Zhuge, and Jürgen Schmidhuber.

## Related pages

- [[Recursive Self-Improvement]]
- [[Agent Skill]]
- [[Agent Memory]]
- [[Agentic Reinforcement Learning]]
- [[Harness Optimization]]
- [[Continual Learning for Agents]]
- [[Synthetic Data Flywheel]]
- [[World Models]]
- [[LLM-as-a-Judge]]
