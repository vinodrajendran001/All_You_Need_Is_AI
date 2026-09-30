---
type: source-summary
created: 2026-09-30
updated: 2026-09-30
source_id: src-2026-09-28-martin-automating-eval-design-hillclimbing
source_title: "Automating eval design and hillclimbing with Claude"
source_author: Lance Martin
source_url: https://claude.dev/blog/automating-eval-design-and-hillclimbing/
tags: [source/summary, evaluation, llm-evaluation, harness, benchmarks, coding-agents]
source_ids: [src-2026-09-28-martin-automating-eval-design-hillclimbing]
status: active
---

# Lance Martin - Automating Eval Design and Hillclimbing with Claude

## Summary

Lance Martin describes skill commands that build an evaluation for an application and then improve
the application against it one attributable change at a time. The evaluation half insists on
production-representative tasks, human-validated graders, deliberate headroom below 100%, and low
run-to-run variance. The hillclimbing half splits the evaluation into train and held-out test,
proposes one patch per round, and reverts anything that improves only the training split. Both worked
examples report quality and cost improving together, but every number is Anthropic-reported.

## Key claims

- A usable evaluation has four properties: a production-like task distribution, scores that rise with
  stronger models and more effort, frontier performance with headroom **below 100%**, and low
  run-to-run variance.
- `build-eval` samples in a fixed order of preference: production transcripts, then bug reports and
  support tickets, then **five to ten cases** written by hand, then cases synthesized from the
  codebase - real traffic first, synthesis last.
- Grader choice follows output shape: programmatic checks for constrained outputs, LLM-as-a-judge for
  open-ended outputs, and judges should check specific claims rather than emit a **1-to-5** scale.
- The baseline diagnostic runs the grader twice on the same output to expose grader noise, checks for
  timeouts, API errors, and cutoffs, and **warns when the baseline is about 95% or higher** - at which
  point quality hillclimbing is uninformative and cost or latency should become the objective.
  Results carry a confidence interval and one full transcript per case.
- Hillclimbing changes may target prompts, skills, tool descriptions, model choice, effort, API
  parameters, or harness code. **One patch per round**; keep it only when train **and** test improve,
  revert when only train improves or either regresses.
- Two stopping rules: if progress stalls for **two or three rounds**, bucket remaining failures by
  cause; if the expected gain is below evaluation noise, add repetitions or cases rather than make an
  unmeasurable edit. Failures are never pasted into prompts, so evaluation answers stay structurally
  inaccessible.
- Cost example on **44 tickets** (**30** for search, **14** held out): on the **30 search (train)
  tickets**, baseline Opus 4.8 at high effort scored **74.4% decision accuracy at 4.6 cents per
  ticket**; Opus 5.5 at low effort **87.8% at 1.9 cents**; Sonnet 5 at low effort **88.9% at 1 cent**;
  prompt work took Sonnet 5 to **98.9%** at about the same cost. On the **14 held-out tickets** — a
  different split, which is why the original baseline reads differently there — the final configuration
  scored **90.5%** against the original setup's **78.6%**, at roughly **one fifth of the cost**. Opus
  5.5 is stated to price input and output tokens **20% less**
  than Opus 4.8 and cache reads **60% less**.
- Capability example: the Claude API skill began at **66%**, reached **74%** after covering eight
  features and **77%** after fixing C# and Java type tables, ending near **88%** once stale API priors
  and grader/task inconsistencies were fixed. The figure caption reports **66.1%** baseline and
  **87.9% at round 24**.

## Why it matters

The vault's benchmark pages document overfitting as a hazard; this source treats it as a control
problem and gives the controls - a held-out split, a revert rule, a noise floor below which edits are
not attempted, and a ceiling above which the metric is abandoned rather than chased. The 95% warning
is the sharpest of these, because it says explicitly that a saturated evaluation should trigger
changing the objective rather than working harder against it.

## Tensions and caveats

Every result is Anthropic-reported on an Anthropic workflow with no independent reproduction and no
released evaluation data. The 44-ticket benchmark is internal and small, and its held-out split is
**14 tickets**. The cost story is not a clean measurement of hillclimbing: model changes, effort
changes, prompt changes, and a pricing change are bundled into the same before-and-after. The article
concedes that evaluation leakage and overfitting persist, including harness additions that solve
benchmark quirks rather than production problems, and that a misconfigured judge still requires a
human to read scored transcripts. The method suits cheap, attributable surfaces such as prompts and
skills better than open-ended harness rewrites, where a single patch is hard to isolate.

## Raw capture

- [[2026-09-28 Lance Martin - Automating Eval Design and Hillclimbing with Claude]]

## Affected pages

- [[Agentic Testing]]
- [[Benchmark Optimization]]
- [[Harness Optimization]]
- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[Anthropic]]

## Related pages

- [[Coding Agent Harness]]
- [[Agent Workflow Maturity]]
- [[Agent Observability]]
- [[AI Agents in Production]]
- [[Agent Skill]]
