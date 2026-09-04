---
type: concept
created: 2026-09-04
updated: 2026-09-04
tags:
  - concept
  - agents
  - tools
  - cost
source_ids:
  - src-2026-09-02-can-boluk-harness-playbook
  - src-2026-09-03-github-ai-coding-cost-efficient
status: active
---

# Tool Roster Economics

## Definition

Tool roster economics is the study of what a harness pays for every tool it exposes to a model — in latency, in
tokens, in decoding constraints, and in the model's attention — and how to decide which capabilities deserve a
schema-defined tool versus a command behind a general execution surface.

## Why it matters

Tool count is usually treated as a feature list: more tools, more capability. Two independent 2026 sources
measured the cost side and found it larger and stranger than expected.

**Latency scales with the roster, and not only through prompt length.** A wall-clock experiment on one task
(`sol`), median of six fresh sessions, compared harnesses stripped to different rosters:

| Configuration | Median wall clock |
|---|---|
| 5 essential tools | **36.6s** |
| Pi (full roster) | 37.0s |
| Codex (full roster) | 42.2s |

The mechanism named for this is **constrained decoding**: every tool schema becomes part of the grammar the
sampler must satisfy, so the roster taxes generation itself, not merely the prompt. Description tokens are the
visible cost; the decoding constraint is the invisible one.

**Tokens spent per turn are measurable and worth single-digit percentages.** Four separate A/B experiments on an
AI-credit cost metric, from a production coding agent:

| Change | Effect on cost metric |
|---|---|
| Remove `view` line-number prefixes | **3.1%** reduction |
| Selective output compaction | **5.5%** reduction |
| Shortened task-tool prompt | **2.9%** reduction |
| Batched notification roundtrips | **2.3%** reduction |

The source is explicit that **these are not additive** — they overlap and interact, so the sum is not the
achievable total. That caveat is itself the finding most often lost when such numbers travel.

## Current synthesis

**The design rule: bounded operation sets get schemas, open-ended ones get a code surface.** Stated directly:
*"Bounded operation set: schema. Open-ended operation set: code surface."* A tool schema is a good fit when the
operations are few and enumerable. When they are not, the alternative is one execution tool plus a discoverable
CLI — the concrete proposal being a `dyn` command behind Bash, so an integration exposes zero additional tools
and its surface is discovered on demand rather than resident in every prompt.

This resolves the tension the [[Model Context Protocol]] page carries. MCP's value is a shared integration
protocol; its cost is that every connected server's tools land in the roster. Roster economics says the protocol
is not the problem — **residency** is.

**Removing a tool's output can cost more than it saves.** The strongest cautionary result is the **local metric
trap**. An aggressive response compressor ("Rust Token Killer") shortened outputs and reduced per-response
tokens, but agents reopened files and re-ran commands to recover what had been removed: *"We saved tokens locally
and spent more globally."* The measured win came only after the policy became conservative — preserve
source-like output (`cat`, `git diff`, `git show`), reorganise search results losslessly, and compress only
repetitive build/install/test noise when savings are substantial. The honest framing of that outcome: the
compressor is *"conservative not because the goal was to build a conservative compressor, but because that is
what the evaluations supported."*

A useful corollary: **the recovery path doubles as the evaluation signal.** If the agent re-reads what you
compressed, the compression was wrong, and you can measure that without a human judging output quality.

**Formatting affordances outlive their consumers.** Line-number prefixes on `view` output existed to support an
edit tool that had since stopped needing them. Nothing depended on them; they had simply never been removed.
Deleting them was worth **~5% offline and ~3% online per user**. Roster economics is partly archaeology — the
cheapest wins are affordances whose consumer is gone.

**Tool schemas are model-facing protocols, so validate and correct.** Different model families emit malformed
calls in family-specific ways: one emits a `Grep` tool that does not exist in the roster; another sends an array
parameter as a delimited string. Rejecting these wastes a turn. The position taken is that the harness should
repair recoverable deviations rather than treat the schema as a contract the model is expected to honour
perfectly.

**Forcing a tool call is a three-tier decision, not a boolean.** The recommended policy: always add the soft
prompt (because a hard constraint applied by an inference server the caller did not choose is a surprise the
caller never opted into); set the native forcing flag only when it is free (one major provider's implementation
causes a conversation-wide cache miss); and escalate on non-compliance, because *"correctness wins over the cache
once persuasion has failed."*

**Roundtrips are a roster cost too.** Delivering two background results as separate notifications produced
**four model calls where one would do** — a 2.3% cost reduction from batching alone. The unit of waste is not
only the token but the turn.

**Prompt reductions need behavioural tests.** A meta-prompting loop halved a task-tool prompt and, in doing so,
rewrote cautious parallelism guidance into a hard scheduling policy that **serialised independent agents** — a
regression invisible offline and caught only in production, fixed by restoring one sentence. The durable lesson:
*"Prompt behavior needs tests. If a behavior is not tested, a shorter prompt can remove it without anyone
noticing."*

**Evidence is local to the workload.** A file-tool change that reduced cost in code review **increased** it in
the CLI agent. An earlier migration of code review onto shared file tools cut cost ~20%. The same change, the
same tools, opposite signs — so roster decisions do not transfer between products without re-measurement.

**None of this makes the model smarter.** The closing framing is worth preserving as the boundary of the whole
practice: *"None of these changes made the model smarter. They removed work the model never needed to do."*

## Open questions

- **How much of the 36.6s vs 42.2s gap is roster size versus other harness differences?** The comparison is
  across different harnesses on one task, so roster is confounded with implementation.
- **Where is the floor?** Five tools was the stripped configuration tested; no curve of latency versus tool count
  is published, so the shape of the trade-off is unknown.
- **Does the code-surface approach move the cost rather than remove it?** A discoverable CLI still needs its
  help text read, and reading it consumes turns. No measurement of discovery overhead is offered.
- **Are the four A/B percentages stable over time?** They are measured on one product with one model mix; the
  sources give no re-measurement after model upgrades.
- **How do you test prompt behaviour cheaply?** The requirement is stated forcefully but no methodology,
  harness, or cost for behavioural prompt tests is described.

## Related pages

- [[Can Bölük - The Harness Playbook]]
- [[GitHub - How We Make AI Coding More Cost Efficient]]
- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[Coding Agent Harness]]
- [[Harness Optimization]]
- [[Harness State Authority]]
- [[Context Engineering]]
- [[Inference Cost Economics]]
- [[Prompt Engineering]]
- [[Agent Delegation]]
- [[Benchmark Optimization]]
- [[Agentic Loop]]
