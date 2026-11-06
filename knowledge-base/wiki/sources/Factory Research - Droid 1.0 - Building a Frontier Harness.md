---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-10-29-factory-droid-frontier-harness
source_title: "Droid 1.0: Building a Frontier Harness"
source_author: "Factory Research"
source_url: "https://factory.com/news/frontier-harness"
tags:
  - source/summary
  - coding-agents
  - agent-harness
  - tool-use
  - benchmarks
source_ids:
  - src-2026-10-29-factory-droid-frontier-harness
status: active
---

# Factory Research - Droid 1.0 - Building a Frontier Harness

## Summary

[[Factory AI]]'s research team announces Droid 1.0, its model-independent coding-agent harness, and
explains the changes behind it. The largest is programmatic tool calling: a Script tool in which the
model writes JavaScript that runs many tool calls inside one model request, now the default for ten
frontier models. The rest are prompt-cache discipline, a **37%** smaller first request, loop-level
rules for stuck or repeating agents, and latency work from launch to quit. Most changes come from an
internal "Agent Factory" loop: agents mine benchmark failures and user friction, propose changes that
state a hypothesis, test each change on every model family it touches, and engineers decide what
ships. The headline results are Factory's own Terminal-Bench 4 comparisons against Codex, Claude
Code, Cursor, OpenCode, and Devin on two models. The methodology is disclosed in unusual detail, but
the comparison has not been independently reproduced.

## Key claims

### Head-to-head results, run by Factory

- Setup: Terminal-Bench 4, all tasks, default time limits, run October 23–28, 2026, **three** trials
  per task, high reasoning, with pinned versions (`codex@0.163.0`, `claude-code@2.1.306`,
  `cursor-cli@2026.10.19-6bbf2c4`, `devin@3000.11.92`, `opencode@2.1.2`).
- **GPT-6.1 Sol:** Droid scores **3.5** points above Codex at **12%** lower cost, and **6.6 to
  12.6** points above OpenCode and Devin. Cursor is absent because it has no access to OpenAI models.
- **Claude Opus 5.5:** Droid scores **3.0 to 7.6** points above Cursor, OpenCode, Devin, and Claude
  Code, at up to **24%** lower cost.
- **Time per passed task:** on Opus 5.5, **16% to 26%** less than every other harness, including
  **26%** less time and **17%** fewer tokens than Claude Code. On GPT-6.1 Sol, Droid uses **12%** fewer
  tokens than Codex but takes **10%** longer, and **4% to 11%** less time than OpenCode and Devin.
- The captured text gives differences only; absolute pass rates were in charts the capture does not
  preserve. The opening claim that Droid beats native harnesses "up to 20% more efficiently" is not
  tied to any stated figure.

### Methodology choices that shape the numbers

- Trials that failed outside the harness (launch failure, request timeout, provider capacity) were
  rerun. Opus 5.5 trials stopped by Anthropic's content moderation were rerun **on Claude Opus 5** for
  every affected harness.
- Devin cannot disable its ask-the-user tool. On GPT-6.1 Sol, a task where Devin stopped to ask was
  counted as passed if Codex passed it (an average of **4.7** tasks per trial); this affects accuracy
  only.
- Cursor undercounts tokens when it reconnects, so usage for **two** trials was estimated from
  transcripts.
- Cost and time are per passed task at list price, compared one harness at a time on the same
  model, and counted only on tasks **both harnesses passed in all three trials**. Time excludes
  setup and grading.

### Programmatic tool calling as a Script tool

- Factory gives three reasons for the default: only program output enters context, one program
  replaces many model requests, and checks and loops run in code, "eliminating the chance that a
  model could be lazy and drop a case."
- The JavaScript sandbox has no file, network, or system access of its own; tools called inside it
  do the work. Printed output is capped, full results are logged for later search, and independent
  calls run concurrently.
- **Measured replay** (fixing a failing unit test, GPT-6.1 Sol): the same **15** tool calls took
  **10** model calls directly and **5** with Script; model time fell from **42.3 s** to **28.0 s**
  and the task from **56.8 s** to **41.6 s**. Tool durations were measured; the direct run's call
  placement was reconstructed.
- Script mode cuts Droid's cost by **15%** on Claude Opus 5.5; savings concentrate in the **12.5%**
  of Scripts making six or more tool calls. The measurement method is not stated.
- **Modeled examples** (direct side estimated at 3 to 10 calls per request and about **28,000**
  tokens of fixed instructions): a Linear cleanup of **151** issues and **312** calls took **2**
  requests and ~**61,000** tokens, against an estimated **36** requests and ~**3.1M** tokens. A CI
  sweep made **550** calls over **5,384** jobs in **547** runs, **60** at a time, in **2** requests
  instead of an estimated **59 to 187**; under **0.1%** of tool results reached the model's context.
- Script is on by default for GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Astra, GPT-6 Sol, GPT-5.6 Sol,
  Claude Fable 5.1, Claude Fable 5, Claude Opus 5.5, Claude Opus 5, and Kimi K3. Prior art credited:
  CodeAct (Wang et al., 2024) across **17** models, Cloudflare and Anthropic in late 2025, and Codex.
- Design rules: programs get whole files and typed search results; literal text travels as raw
  blocks; edits return short summaries; a program waits up to **5** minutes, then returns partial
  output or moves to the background; and a dedicated tool replaces polling.

### The Agent Factory loop

- An automation tracking more than **20** models adds each new one and checks it against behavioral
  assertions — "the minimum, not the bar for release." Live environments, QA, daily benchmark runs,
  error logs, and user friction then feed an agent that looks for causes repeated across tasks and
  models.
- Each proposed change states its hypothesis and is measured in a controlled experiment on every
  model it touches. Proposals are judged against five principles: budget every token, keep the cache
  append-only, profile the hot path, track background work, and always have a next step ready.
- Tuning Script mode on GPT-6.1 Sol, Claude Opus 5.5, GLM 5.3, and Kimi K3 required changes to the
  prompt, the descriptions of tools called inside Script, and Script result structure; no single change
  moved every model.
- Numbering every line of file reads cut Opus's cost by **22%** on one task but raised cost by **8%**
  on GLM and **32%** on Kimi, at about two tokens per line. It shipped as an option the model requests.

### Cache, prompt budget, loop rules, and latency

- **Cache:** newly discovered tools are appended to the end of the request, not inserted into the
  tool list. In production the typical request reads **98%** of input from cache and **98.6%** of
  requests are strictly append-only (**91.5%** token-weighted), over **20.4M** CLI requests in the
  seven days to October 22, excluding CI and evals. A monitor names whatever broke the cache, and
  retries go to the provider already holding it.
- **Prompt budget:** between 0.170.0 and 0.250.0 the first request shrank from **20,887** to
  **13,055** tokens. Tool definitions sent up front fell from **11** to **2**, with the rest loaded
  on demand, while the system prompt grew. The two releases ran on different models, so tokenizers
  differ; in characters the cut is **57,035** to **36,802** (**−35%**).
- **Bounded autonomy, enforced in the loop rather than the model:** **4** minutes of silence on a
  Factory-managed Anthropic stream triggers a retry; three silent turns stop the run; three identical
  tool calls get a nudge and six stop it; compaction summaries grew from **8,000** to **16,000**
  tokens because, by Factory's estimate, a third or more were filling the old limit.
- **Latency:** turn preparation now takes **24 ms**, which alone made median responses finish **13%**
  sooner in a controlled test; `droid exec` reaches its first model request in **646 ms** instead of
  **1,741**; first paint fell from **1,839** to **488 ms**; each session adds about **20 MB** instead
  of running a separate ~**350 MB** process; and median quit time fell from **648** to **30 ms**. In
  one production turn the model request accounted for **97%** of the wait for the first token.

## Why it matters

This is the vault's most detailed first-party account of a [[Coding Agent Harness]] tuned across many
models at once. It turns [[Programmatic Tool Calling]] from an argued action space into a shipped
default with a measured replay and production cost claim. It also adds a controlled, human-merged
improvement loop to [[Harness Optimization]] and [[Loop Engineering]], and a counterexample to
universal fixes: the same line-numbering change helped one model and hurt two. Its prompt and cache
numbers add to [[Tool Roster Economics]], [[Context Engineering]], and [[Agentic Loop]], and its
vendor-run head-to-head is a case study for [[Benchmark Optimization]]. The startup and hot-path
work is application performance engineering ([[Software Performance Engineering]]).

## Tensions / open questions

- **First-party benchmark.** Factory ran the comparison and sells the winning harness. No independent
  reproduction exists, and the capture lacks absolute scores and confidence intervals.
- **The cost and time denominator excludes hard or flaky tasks.** Only tasks both harnesses passed in
  all three trials count, so efficiency is measured on the easier shared subset.
- **Imputed and substituted trials.** Devin's asks were scored from Codex's outcomes, some Opus 5.5
  trials ran on Opus 5, and two Cursor trials have estimated token counts.
- **The tuning loop reads the benchmark.** Agent Factory uses daily benchmark failures as input to
  changes later scored on a benchmark. The post describes no held-out task set or a check that the
  Terminal-Bench 4 tasks were excluded from tuning.
- **Modeled and measured figures sit side by side.** The Linear and CI direct-call numbers are
  estimates, the cache illustration is illustrative, and the **15%** cost cut has no stated method.
- **Percentages disagree between text and figure:** tool definitions "fell by 45%" versus a figure
  of **−46%** (15,798 → 8,528); reminders fell "by a third" versus **−32%** (3,463 → 2,362); the
  system prompt grew "31%" versus **+33%** (1,618 → 2,155).
- **A sandboxed program is not a bounded action.** The Script sandbox has no file or network access
  of its own, but the tools it calls do; how a program is approved before it runs is not discussed.
- The captured URL is on factory.com, while the post's "Cite as" line gives
  `factory.ai/news/frontier-harness`.

## Affected pages

- [[Factory AI]]
- [[Coding Agent Harness]]
- [[Programmatic Tool Calling]]
- [[Harness Optimization]]
- [[Loop Engineering]]
- [[Tool Roster Economics]]
- [[Context Engineering]]
- [[Agentic Loop]]
- [[Benchmark Optimization]]
- [[Software Performance Engineering]]

## Raw capture

- [[knowledge-base/raw/sources/Droid 1.0 Building a Frontier Harness]]

## Citations

- Canonical URL: <https://factory.com/news/frontier-harness> (`utm_source` parameter and
  `#methodology` anchor removed).
- Byline: Factory Research. Published October 29, 2026; captured November 2, 2026. The post's own
  citation line reads "Factory, October 2026" and gives the URL `factory.ai/news/frontier-harness`.

## Related pages

- [[Factory AI]]
- [[Coding Agent Harness]]
- [[Programmatic Tool Calling]]
- [[Harness Optimization]]
- [[Loop Engineering]]
- [[Tool Roster Economics]]
- [[Context Engineering]]
- [[Agentic Loop]]
- [[Benchmark Optimization]]
- [[Software Performance Engineering]]
- [[Alex L. Zhang - Speculative Programmatic Tool Calling]]
- [[GitHub - How We Make AI Coding More Cost Efficient]]
- [[Can Bölük - The Harness Playbook]]
- [[Replit - Free the Models - Harness Design at the Frontier]]
- [[Model Routing]]
- [[KV Cache]]
- [[Anthropic]]
- [[OpenAI]]
