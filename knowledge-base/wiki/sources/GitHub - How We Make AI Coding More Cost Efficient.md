---
type: source-summary
created: 2026-09-04
updated: 2026-09-04
source_id: src-2026-09-03-github-ai-coding-cost-efficient
source_title: "How we make AI coding more cost efficient without sacrificing task quality"
source_author: Erik Kristensen and Napalys Klicius (GitHub)
source_url: https://github.blog/ai-and-ml/github-copilot/how-we-make-ai-coding-more-cost-efficient-without-sacrificing-task-quality/
tags:
  - source/summary
  - topic/agents
  - topic/harness
  - topic/evaluation
source_ids:
  - src-2026-09-03-github-ai-coding-cost-efficient
status: active
---

# GitHub - How We Make AI Coding More Cost Efficient

## Summary

GitHub's engineering account of four shipped efficiency changes to the GitHub Copilot harness, each validated by
an offline agentic-coding benchmark and then an online controlled experiment before shipping. The four
independent A/B results, on a shared AI-credit metric, were **remove `view` line-number prefixes 3.1%, selective
output compaction 5.5%, compact the task-tool prompt 2.9%, and reduce notification roundtrips 2.3%** — with the
explicit caveat that "their effects are not necessarily strictly additive."

The post's real subject is a measurement error rather than the savings. Its thesis is that **token count per tool
call is the wrong objective**, because a shorter tool response that omits something the agent needs buys turns of
recovery that cost more than the tokens saved. The changes that survived were the ones that removed work the
model never needed to do, not the ones that gave the model less.

The closing line states the position plainly: **"None of these changes made the model smarter. They removed work
the model never needed to do."**

## Key claims

**The local metric trap, demonstrated on a real tool.** GitHub evaluated RTK (Rust Token Killer), a utility that
shortens shell output before an agent reads it. In their harness and benchmark configuration it did shorten
responses, "but when the omitted text mattered, the model sometimes reopened the original output or reran the
command to recover what it needed. Those recovery steps added turns and carried more context forward." The
result: the individual tool response was shorter, but **on average the task used more tokens and took longer**.
The summary sentence is the durable one — **"We saved tokens locally and spent more globally."** GitHub scopes
the finding explicitly to the integration and workloads tested, not to RTK generally or to output compression as
a category.

**The compressor that shipped is conservative because the evaluations forced it to be.** Early versions were too
aggressive and "made the model repeat work or read the full saved output, increasing end-to-end cost and reducing
task success." `git diff` was compressed initially and the filter was removed after agents were observed
reopening the original. The shipped three-part policy is: **preserve source-like and arbitrary output** (`cat`,
`git diff`, `git show`, arbitrary scripts returned unchanged); **reorganise search results without dropping
content** (grep matches and file lists regrouped, every result retained); **compress repetitive noise
selectively** (install, build, test and progress output, and only when savings are substantial). GitHub is
pointed about the provenance of that shape: "It is conservative not because the goal was to build a conservative
compressor, but because that is what the evaluations supported."

**The recovery path doubles as the evaluation signal.** Because a compressed output can always be recovered in
full, GitHub could track whether the agent opened the saved original, reran commands, repeated exploration,
narrowed its searches, or took additional turns. "Frequent recovery would indicate that the compressor had
removed something valuable." Offline, no statistically significant task-success regression was detected and
agents "extremely rarely" opened saved originals; online, average cost fell slightly with no material regression
in tracked quality metrics.

**The cleanest win was deleting formatting nobody used.** The `view` tool prefixed every line with a number
because *earlier* file-editing tools targeted changes by line number. Current tools match surrounding code
instead, so the prefixes had outlived their consumer. Removing them cut model-inference cost by **roughly 5% in
offline benchmarks** and **about 3% in average daily model-inference cost per user** in an online Copilot CLI
experiment, with success rates within run-to-run variance and no increase in edit failures. GitHub calls it "the
ideal change: no new instructions for the model, no source of information to recover, and no additional decision
to make."

**Prompt compression broke a behaviour that offline evaluation did not cover.** The task tool's guidance had
accumulated across "tool descriptions, schemas, agent definitions, system instructions, and companion tools." A
**meta-prompting loop, in which Copilot iteratively wrote its own prompt**, cut it roughly in half. The first
online experiment then exposed a regression the offline evaluations had missed: the loop "had rewritten cautious
parallelism guidance into a hard scheduling policy, causing independent custom agents to run sequentially." The
experiment was stopped, a regression evaluation was written for the behaviour users had exposed, and the fix
replaced an explicit allowlist and denylist with a single sentence — *"Independent agents can run in parallel;
consider side effects."* — which was both shorter and **less restrictive**, deferring the decision to the model.
The lesson is stated as a rule: **"Prompt behavior needs tests. If a behavior is not tested, a shorter prompt can
remove it without anyone noticing."** Shipped result: ~1,300 fewer task-tool prompt tokens per turn, ≈1.8% fewer
total prompt tokens per session, 2.9% lower normalised cost per active hour.

**Orchestration savings come from deleting model turns, not model output.** When background work finished, the
notification did not carry the result, so the agent spent another turn retrieving output the harness already
held. For one shell command plus one sub-agent that meant **four model calls before work could continue** — one
to request and one to process each result. Batching eligible completions and delivering them in the existing
tool-result format lets a single call process both, and also avoids carrying full session context through the
now-unnecessary calls. Measured reduction: **about 2.3% of AI Credits**, achieved "without compressing,
summarizing, or withholding anything."

**Evidence does not transfer between surfaces.** A tighter set of file-tool instructions that had tested well in
Copilot code review **increased cost** in a Copilot CLI online experiment and was not shipped. Conversely,
line-number removal and selective compression each cut average prompt tokens per review by roughly 5% across
Copilot code review tasks. GitHub separates these from an earlier migration of code review to the shared file
tools which, with review-instruction tuning, had reduced code review cost by about 20%.

**Five stated lessons:** optimise the completed task, not the tool call; optimise orchestration, not just model
output; compress by what the output represents, preferring lossless transformations and measuring recovery-path
use; validate that prompt rewrites preserve intended behaviour; and re-evaluate every change in each product
surface, because "evidence is local to the workload."

## Why it matters

This gives [[Harness Optimization]] its first set of controlled, quantified results from a production harness at
scale, and it supplies a named failure mode — the local metric trap — that the vault previously only implied.
Much of the vault's efficiency material is about making the model cheaper: quantisation, distillation, better
serving. This source is about the opposite lever, and the size of the effects is notable precisely because none
of them touch the model.

The **meta-prompting regression** is the most transferable finding. An automated loop that rewrote a prompt for
brevity silently converted advisory guidance into a hard policy and serialised parallel work — a failure invisible
to offline evaluation and caught only by users. That is direct evidence for treating prompts as tested surfaces,
which strengthens the argument on [[Agentic Testing]] and connects to [[Benchmark Optimization]]'s recurring theme
that a metric chosen for convenience will be optimised at the expense of the thing it stood in for.

It also lands as a natural counterpart to [[Can Bölük - The Harness Playbook]] from the same batch. Bölük argues
from architecture that the harness owns costs the model is blamed for; GitHub arrives at the same conclusion from
A/B measurement, and independently reaches Bölük's position that **bounding output belongs in one central place
with a recovery path**, rather than in each tool.

## Tensions / open questions

- **Every number is vendor self-report on a proprietary harness and benchmark.** There is no external
  replication, the benchmark suite is not named or described, and the "AI credit" metric is GitHub's own
  composite. The direction of the findings is well-argued; the magnitudes are not independently checkable.
- **Quality is reported only as an absence.** The recurring phrasing is "no material regression detected in the
  tracked quality metrics" and "within the expected run-to-run variance." No quality figures, effect sizes, or
  statistical power are given, so a small real regression could sit under the detection threshold.
- **The percentages are explicitly not additive** and were measured in four independent experiments, so the
  headline chart cannot be read as a combined ~13.8% saving.
- **The RTK result is a finding about an integration, not about compression.** GitHub says so directly. It would
  be a misreading to conclude that output compression does not work — GitHub shipped a compressor of their own in
  the same post.
- **The meta-prompting loop's overall value is unresolved.** It produced the 50% reduction *and* the regression.
  The post does not say whether the shipped prompt is the loop's output plus a hand fix, or whether the loop
  remains in use.
- **The line-number removal may be harness-specific.** It was safe because Copilot's current edit tools match
  surrounding code. A harness whose edit tools address lines directly would lose a working mechanism by making the
  same change.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Harness Optimization]]
- [[Tool Roster Economics]]
- [[Coding Agent Harness]]
- [[Context Engineering]]
- [[Benchmark Optimization]]
- [[Agent Delegation]]
- [[Agentic Testing]]
- [[GitHub]]

## Related pages

- [[Harness State Authority]]
- [[Tool Use and Function Calling]]
- [[AI-Native Software Development Lifecycle]]
- [[Multi-Turn Evaluation]]
- [[Inference Efficiency Frontier]]
- [[AI Agents in Production]]
- [[Can Bölük - The Harness Playbook]]

## Citations

- Raw capture: [[2026-09-03 GitHub - How We Make AI Coding More Cost Efficient]]
- Source: <https://github.blog/ai-and-ml/github-copilot/how-we-make-ai-coding-more-cost-efficient-without-sacrificing-task-quality/>
