---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-13-orlanski-slop-moves-up
source_title: "Slop Is Moving Up the Stack"
source_author: "Gabe Orlanski"
source_url: "https://gabeorlanski.github.io/posts/slop-moves-up/"
tags:
  - source/summary
  - coding-agents
  - code-quality
  - benchmarks
  - software-design
source_ids:
  - src-2026-11-13-orlanski-slop-moves-up
status: active
---

# Gabe Orlanski - Slop Is Moving Up the Stack

## Summary

Gabe Orlanski, a PhD student and author of SlopCodeBench, revisits agent code quality about a year
after the benchmark launched. His thesis is in the subtitle: agents now write **cleaner lines** than a
year ago, but the slop has "moved up the stack" into **design**. That means catch-all error handling,
hand-written copies of library functionality, and libraries other agents cannot use well. The post is
**first-party benchmark reporting** by the benchmark's author, a follow-up to SCB runs done by Dex
Horthy ("at HumanLayer (now Factory)"). The work was supported by Prime Intellect (Prime RL Residency)
and Snorkel AI (Open Benchmarks Grant). Orlanski adds: "I might be biased, but clearly every new model
that comes out should put SCB, LDB, and LUB on their model cards."

Three benchmarks are used:

- **SlopCodeBench (SCB):** 36 problems and 196 checkpoints, all in Python. An agent extends its own
  code as the spec changes, and is graded on hidden tests and accumulated slop.
- **LibraryDesignBench (LDB):** an agent writes a library and is scored on how much code it saves a
  fixed set of implementer agents.
- **LibraryUseBench (LUB):** the same problems as LDB's implementer phase, with a human-written
  library and a minimal prompt.

## Key claims

### The good: solve rates up, line-level slop down

- Strict SCB solve rate (every test for the current and all prior checkpoints) "now peaks at 16.3%",
  set by GPT-6 Astra XHigh (32 of 196 checkpoints). The isolated peak is GPT-5.6 SOL XHigh at 32.1%,
  and the core peak Opus 5.5 Medium at 74.0%. "Every frontier model released since July clears 65% on
  core tests."
- Least-squares trends over 34 setups: strict **+0.9** points a month, isolated **+1.5**, core
  **+2.3**.
- Line-level slop (hits from **137** AST-grep rules per 1,000 lines) trends **−3.7** per month, with
  Opus 5.5 XHigh labelled at 61. Erosion (the share of complexity in functions with cyclomatic
  complexity above 10) trends **+0.014** per month, with GPT-6.1 SOL Medium labelled at 0.80.
- Anthropic older runs (Opus 4.6, Sonnet 4.6, Opus 4.7) against newer runs (Fable 5.1, Opus 5.5 M,
  Opus 5.5 X), with "Change" as the mean of newer runs over the mean of older runs:

| Pattern | Older | Newer | Change |
| --- | --- | --- | --- |
| All scb-check rules (hits per 1k lines) | 98.0 / 90.1 / 85.4 | 69.5 / 75.1 / 60.7 | ↓ 25% |
| `sys.exit` outside `main` (count) | 187 / 275 / 205 | 8 / 6 / 3 | ↓ 97% |
| Functions over 200 lines (count) | 50 / 38 / 46 | 3 / 5 / 1 | ↓ 93% |
| Longest function (lines) | 1,099 / 1,369 / 2,095 | 754 / 427 / 294 | ↓ 68% |

`return None, error` tuples fell 59%, and `len(x) == 0` and collapsible nested `if`s each fell 70%.
Process errors (forgotten references, empty modules, hard-coded test values) are described as nearly
eliminated.

### The bad: regressions are design and error-handling choices

- The same Anthropic comparison shows increases: `type(x) == T` ↑ ×19; `if not isinstance(x, T):
  raise` ↑ ×5; `if x is None: raise` ↑ ×7; `# pragma: no cover` ↑ ×16; `except` listing 4+ types
  (8/0/0 → 25/15/29) ↑ ×9; problems with a hand-written library fallback, of 36 (0/n/m/1 → 11/5/9),
  ↑ ×17; problems that leave a test suite behind (7/0/1 → 25/0/14) ↑ ×5.
- **Python 2 idioms in a Python 3.12 codebase.** `%` formatting is the main style in 14–23 of 36
  problems for Opus 5.5, Fable and GLM 5.3, "against at most 3 for any older run". Opus 5.5 XHigh
  wrote 126 `class X(object)` bases.
- "Error handling got worse for all three families" (Anthropic, OpenAI, GLM). New GPT runs have
  **49–74** broad except clauses mixing `KeyError`/`TypeError` with I/O errors, against 2 and 10 for
  GPT-5.4 and 5.5. A programming bug then reaches the user as "rollback failed".
- **Slop that moved.** Flagged patterns were patched around rather than fixed. `except Exception:`
  became `except OSError: return None`. In one example, if the rules file cannot be read, "the
  protected operation runs with no role check". The tuple-to-exception rewrite took **8** lines to
  **26**, with five except clauses.
- On LDB, agent libraries contain placeholder-on-error helpers at **25x** the human-library rate, and
  `# pragma: no cover` on error handlers at "nearly 4x their own SCB rate".

### The ugly: agents skip the library

- **LUB (15 tasks, first attempt):** "every model hand-writes something the library already does, in
  73% to 100% of its solutions". GPT-6 Luna is at 100%. Opus 5, Opus 5.5, DeepSeek V4.1 Flash and
  GPT-6 SOL share the lowest rate, 73%.
- LDB's redundancy is only **40%**, but only because its prompt is "incredibly prescriptive". The same
  prompt with human libraries gives a "~17% reimplementation rate".
- Implementers had to work around a broken or ill-fitting library **27%** of the time on the human
  library, against **40%** on agent-written ones. By designer the rate ranges from DeepSeek V4 Pro
  56% to Kimi K3 27%.
- In a SimPy task, "8 of 12 models wrote their own queue". Opus 5.5's and Fable's libraries reuse
  about **30%** of the production library's public names, against 13% for GPT-6 SOL: "They copy the
  interface and write their own implementation behind it."
- One LDB designer aliased its class `BeautifulSoup = UglyPie`, "betting that implementers would reach
  for the name they already know from training".

## Why it matters

This is the vault's most granular measured evidence that rule-level code quality and design-level
code quality can move in opposite directions. It gives the "redundant models" in the decoherence
argument on [[AI-Native Software Development Lifecycle]] a benchmark measurement: agents re-implement
what a library already provides in most LUB solutions. It also tells [[AI Code Review]] where to look.
Lint-style rules caught the old slop, but the new slop sits in exception taxonomy, abstraction choice,
and reuse decisions. The "slop just moved" examples are a small case of [[Benchmark Optimization]]: a
rule count falls while the behaviour the rule targeted survives in a narrower form.

## Tensions / open questions

- **Opposed practitioner stance.** [[Geoffrey Huntley - The Answer to AI Is Engineering]] argues for
  generating code first-party or vendoring it instead of depending on open source, for security
  reasons. Orlanski treats hand-written copies of library functionality as slop, "another place for a
  bug to hide". The two disagree on whether re-implementation is a defect or a policy.
- Small samples: LUB and LDB use 15 tasks, and "rewrite" and "workaround" are judged by subagents
  reading each solution. No human agreement rate is reported.
- The erosion trend is **+0.014** per month while the prose says erosion "has trended the same, with
  some slight regressions". The sign and meaning of the labelled points are not explained.
- Older/newer comparisons mix models, harness versions and effort settings. One row has an unmeasured
  cell (n/m). The post does not say whether anti-slop prompts (shown "faded" in charts) are included
  in the family means.
- Model names (for example GPT-6 Astra, Fable 5.1, Muse Spark 1.3) are as captured and not
  independently checked.

## Affected pages

- [[AI-Native Software Development Lifecycle]]
- [[AI Code Review]]
- [[Benchmark Optimization]]

## Raw capture

- [[knowledge-base/raw/sources/Slop Is Moving Up the Stack]]

## Citations

- Raw capture: Gabe Orlanski, "Slop Is Moving Up the Stack", published 2026-11-13 (source ID date),
  captured 2026-11-20. The canonical URL drops the newsletter `utm_source` parameter.
- The post includes a BibTeX entry with author "Orlanski, Gabriel", year 2026, month November.
- Part I of the SCB model runs (pass rates, cost) is linked from the post but was not read.
- All figures are the benchmark author's own measurements. Charts are interactive in the original. The
  capture preserves labelled values and trend lines but not every per-setup point.

## Related pages

- [[AI-Native Software Development Lifecycle]]
- [[AI Code Review]]
- [[Benchmark Optimization]]
- [[The Decoherence Trap]]
- [[Coding Agent Harness]]
- [[Geoffrey Huntley - The Answer to AI Is Engineering]]
- [[Factory AI]]
