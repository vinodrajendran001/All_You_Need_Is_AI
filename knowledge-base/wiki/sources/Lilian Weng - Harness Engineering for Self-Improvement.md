---
type: source-summary
created: 2026-08-30
updated: 2026-08-30
source_id: src-2026-07-16-lilian-weng-harness-engineering
source_title: "Harness Engineering for Self-Improvement"
source_author: "Lilian Weng"
source_url: "https://lilianweng.github.io/posts/2026-07-04-harness/"
tags:
  - source/summary
  - topic/agents
  - topic/self-improvement
  - topic/research-automation
source_ids:
  - src-2026-07-16-lilian-weng-harness-engineering
status: active
---

# Lilian Weng - Harness Engineering for Self-Improvement

## Summary

A long survey arguing that the *harness* — the system around a model that orchestrates execution,
tools, context, artifacts, and evaluation — has become the primary optimization surface for agent
capability, and that harness design is increasingly something models can do for themselves. Weng
uses an operating-system analogy: the model is the CPU, the harness is the OS that decides what the
CPU sees and what it is allowed to do.

The post's organizing contribution is an **optimization ladder** of five rungs, ordered by how much
of the system the optimizer is allowed to rewrite:

1. **Prompts** — instructions and few-shot examples.
2. **Structured context** — playbooks, memory files, and skills that persist across runs.
3. **Workflow** — the graph of steps, roles, and control flow.
4. **Harness code** — the executable scaffolding itself.
5. **Optimizer code** — the search procedure that produces the changes at rungs 1 to 4.

Each rung subsumes the ones below it and enlarges the search space, so higher rungs promise more
headroom while making evaluation, attribution, and safety harder. Weng then walks representative
systems up this ladder and closes with failure modes and open challenges.

## Key claims

**The harness is a design surface with three recurring patterns.** Workflow automation (turning a
repeated manual sequence into a durable procedure), the file system as persistent memory (writing
state to disk instead of holding it in context), and sub-agents or backend jobs (isolating work so
it does not contaminate the parent context).

**Context optimization needs itemized structure, not prose rewriting.** ACE (Agentic Context
Engineering) splits the job across a *generator*, a *reflector*, and a *curator*, and stores the
evolving playbook as itemized bullets that are added, edited, or retired individually. The reason is
a failure mode Weng names **context collapse**: when a whole context document is rewritten each round
by a model with a brevity bias, accumulated detail erodes round after round. Itemization makes
updates local and auditable. MCE extends this to a bi-level loop — meta skill evolution above base
context optimization — and Meta-Harness goes one rung higher by optimizing the optimizer's own code.

**Automated search over workflows and agent designs already works, within limits.** ADAS searches
over agent designs, AFlow runs MCTS over workflow graphs, STOP recursively improves a scaffolding
program, AlphaEvolve and ShinkaEvolve run evolutionary program search, and the Darwin Godel Machine
rewrites its own codebase.

**Recursive structure alone is not sufficient — the base model must be strong enough.** STOP improved
when driven by GPT-4 but *degraded* with GPT-3.5 and Mixtral. The recursion is not the source of the
gain; the model's ability to propose good candidates is.

**Harness-updating capability and harness-benefit are different things, and neither scales the way you
would guess.** Weng cites Lin et al., who find that the ability to *write* a harness update is
roughly **flat** from around 9B parameters up to frontier models — smaller models produce skill files
that are procedurally similar to those from much larger ones — while the *benefit* an agent gets from
a harness is **non-monotonic**, peaking for mid-tier models. Weak models cannot exploit a good
harness; the strongest models already know most of what the harness would have told them.

**The strongest self-improvement systems make the evaluator unreachable.** Self-Harness mines
weaknesses from failure traces, bounds each proposal, and validates on held-in and held-out splits.
AHE (Automated Harness Engineering) builds three observability pillars, treats every edit as a
falsifiable claim, and — critically — makes the runs directory, the tracer, the verifier, and the LLM
configuration **read-only to the agent**. That single constraint removes the cheapest reward hacks:
disabling the verifier, swapping in a stronger model, or raising the reasoning budget. AHE's evolved
harness, frozen, still transfers to SWE-bench Verified, which suggests it encoded engineering
practice rather than benchmark-specific overfitting.

**Automated research pipelines fail in characteristic ways.** Weng catalogs six: reverting to
training-data defaults instead of the specified method; implementation drift away from the stated
design; memory degradation over long runs; over-optimism, including "numerical duct tape" applied to
make results look clean; insufficient domain intelligence; and weak scientific taste.

**Seven open challenges.** Weak evaluators, context and memory lifecycle management, the failure to
record negative results, diversity collapse in search, reward hacking, defining long-term success,
and deciding what humans are still for.

## Why it matters

This is the most complete map in the vault of *what can be optimized around a model*, and it converts
a vague intuition ("scaffolding matters") into an ordered ladder with named systems on each rung. The
Lin et al. result is the most practically useful finding: it predicts that harness investment pays
off most for mid-tier models, and that the marginal value of elaborate scaffolding declines as base
models improve — which is also Weng's own forecast, that harness techniques get absorbed into model
behaviour the way prompt-engineering tricks were.

The AHE read-only constraint is the concrete engineering answer to the reward-hacking problem that
[[Benchmark Optimization]] keeps surfacing: do not ask the optimizer to be honest, remove its write
access to the scoreboard.

## Tensions / open questions

- Weng presents the ladder as monotonically more powerful, but every result she cites at rung 4 or 5
  is gated on base-model strength. It is unresolved whether the higher rungs add capability or only
  add variance that a strong model can exploit and a weak one cannot.
- The non-monotonic benefit curve implies harness research has a moving target: a technique validated
  on today's mid-tier models may be worthless on next year's frontier models.
- Frozen-harness transfer to SWE-bench Verified is one data point. Whether evolved harnesses generally
  transfer, or generally overfit, is not settled.
- Weng's read-only-evaluator prescription protects against reward hacking but also caps the system at
  self-improvement rather than recursion — the same boundary
  [[Philipp Schmid - Recursive Self-Improvement]] argues no public system has crossed.

## Affected pages

- [[Harness Optimization]]
- [[Recursive Self-Improvement]]
- [[Coding Agent Harness]]
- [[Context Engineering]]
- [[Automated AI Research]]
- [[Benchmark Optimization]]
- [[Lilian Weng]]

## Related pages

- [[Agent Skill]]
- [[Agent Memory]]
- [[Loop Engineering]]
- [[Agent Security and Governance]]
- [[Alpha Signal - Why self-improving harnesses are the next frontier]]
- [[Zhe Ren et al - Self-Improvements in Modern Agentic Systems]]

## Citations

- Raw capture: [[2026-07-16 Lilian Weng - Harness Engineering for Self-Improvement]]
- Original: <https://lilianweng.github.io/posts/2026-07-04-harness/> (published 2026-07-04)
