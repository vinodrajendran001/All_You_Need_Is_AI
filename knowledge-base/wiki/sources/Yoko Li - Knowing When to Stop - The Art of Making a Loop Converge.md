---
type: source-summary
created: 2026-08-12
updated: 2026-08-26
source_id: src-2026-08-12-yoko-li-loop-convergence
source_title: Knowing When to Stop - The Art of Making a Loop Converge
source_author: Yoko Li
source_url: https://a16z.com/knowing-when-to-stop-the-art-of-making-a-loop-converge/
tags:
  - source/summary
  - ai-agents
  - loop-engineering
  - evaluation
source_ids:
  - src-2026-08-12-yoko-li-loop-convergence
status: active
---

# Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge

## Summary

Yoko Li argues that "done" is not intrinsic to model output; it is a judgment supplied by tests, specifications, constraints, approval, deadlines, risk, and budgets around the generator. A useful agent loop must reduce distance to a target rather than merely repeat, because an incomplete verifier can reward behavior that passes visible checks while violating the user's intent.

The source identifies four conditions for convergence: a target state, an observable current state, precise local actions, and an external stopping rule. It then adds economics: diminishing returns and growing transcripts mean a technically convergent loop may be operationally irrational.

## Key claims

- The verifier defines both progress and completion, so proxy flaws shape the entire trajectory.
- Editable artifacts with inspectable structure and local actions converge more reliably than workflows that regenerate opaque outputs globally.
- Tasks can be reframed into a more editable and verifiable representation, such as SVG paths or Blender scene graphs.
- Loop recipes are stack-specific and do not generalize automatically across codebases, tools, or environments.
- Stop rules need quality, impossibility, diminishing-return, and budget signals.
- In the source's unreachable Lighthouse experiment, most value arrived early while 67% of spend produced no further score improvement.
- Cost per iteration and progress per dollar should be visible while the loop is running.

## Why it matters

The article substantially deepens [[Loop Engineering]] by making convergence—not repetition—the design objective. It connects [[Multi-Turn Evaluation]], [[Test-Time Scaling]], [[Context Engineering]], and [[Agent Security and Governance]] through a single stopping problem.

## Tensions / open questions

- The Lighthouse case study is one instrumented example and not a general cost law.
- Some tasks have delayed or subjective feedback that cannot be reduced to a stable scalar distance.
- External evaluators can reject a correct impossibility diagnosis and create evaluator-generator deadlock.
- Local improvements can satisfy the measured target while degrading unmeasured system properties.
- Human judgment is still needed when intent, taste, or acceptable risk cannot be fully specified.

## Affected pages

- [[Loop Engineering]]
- [[Multi-Turn Evaluation]]
- [[Test-Time Scaling]]
- [[Context Engineering]]
- [[AI Agents in Production]]

## Citations

- Raw capture: [[2026-08-12 Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge]]
- Canonical URL: https://a16z.com/knowing-when-to-stop-the-art-of-making-a-loop-converge/

## Raw capture

- [[2026-08-12 Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge]]

## Related pages

- [[Yoko Li]]
- [[Agentic Loop]]
- [[Reward Design for RL]]
- [[Continual Learning for Agents]]

