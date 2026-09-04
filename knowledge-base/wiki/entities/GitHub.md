---
type: entity
created: 2026-09-04
updated: 2026-09-04
entity_kind: organization
tags:
  - entity
  - organization
  - coding-agents
  - developer-tools
  - cost
source_ids:
  - src-2026-09-03-github-ai-coding-cost-efficient
status: active
---

# GitHub

## What it is

Developer platform and operator of Copilot's coding agents, including the CLI agent and the code-review agent
that supply the measurements in [[GitHub - How We Make AI Coding More Cost Efficient]].

## Why it matters here

GitHub is the vault's source for **A/B-measured harness cost reduction in production**. Most harness material
here is design argument; this is four controlled experiments with numbers on a live workload — view prefixes
3.1%, selective output compaction 5.5%, task-tool prompt 2.9%, notification batching 2.3% — reported with the
caveat that **they are explicitly not additive**. It is a principal source for [[Tool Roster Economics]] and
[[Harness Optimization]].

The more valuable contributions are the two negative results, which are rarer than the wins:

- **The local metric trap.** An aggressive response compressor cut per-response tokens, but agents reopened files
  and re-ran commands to recover the lost detail: *"We saved tokens locally and spent more globally."* The
  shipped compressor became conservative *"not because the goal was to build a conservative compressor, but
  because that is what the evaluations supported."*
- **A shortened prompt silently deleted a behaviour.** A meta-prompting loop halved a task-tool prompt and turned
  cautious parallelism guidance into a hard scheduling policy that serialised independent agents — invisible
  offline, caught only in production. The lesson stated: *"Prompt behavior needs tests. If a behavior is not
  tested, a shorter prompt can remove it without anyone noticing."*

GitHub also supplies the vault's clearest evidence that **harness evidence does not transfer between products**:
a file-tool change that reduced cost in code review *increased* it in the CLI agent, and an earlier migration of
code review onto shared file tools cut cost about 20%. Same change, same tools, opposite signs.

## Notes

- The closing framing is the honest boundary of the whole exercise: *"None of these changes made the model
  smarter. They removed work the model never needed to do."*
- All figures are on an internal AI-credit cost metric on GitHub's own workload and model mix, so they are
  directional rather than portable.
- The `view` line-number-prefix finding is a maintenance archaeology result: the prefixes supported an edit tool
  that had stopped needing them, and nothing had removed them. Worth ~5% offline and ~3% online per user.
- This is vendor engineering material about a product the vault's own tooling context sits inside; read
  accordingly.

## Related pages

- [[GitHub - How We Make AI Coding More Cost Efficient]]
- [[Tool Roster Economics]]
- [[Harness Optimization]]
- [[Coding Agent Harness]]
- [[Context Engineering]]
- [[Inference Efficiency Frontier]]
- [[Agent Delegation]]
- [[Agentic Testing]]
- [[Benchmark Optimization]]
- [[AI Knowledge Base Overview]]
