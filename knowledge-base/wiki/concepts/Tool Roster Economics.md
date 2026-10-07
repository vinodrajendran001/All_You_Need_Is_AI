---
type: concept
created: 2026-09-04
updated: 2026-10-07
tags:
  - concept
  - ai-agents
  - tool-use
  - cost
source_ids:
  - src-2026-09-02-can-boluk-harness-playbook
  - src-2026-09-03-github-ai-coding-cost-efficient
  - src-2026-09-27-fd-agent-muse-compute-demand
  - src-2026-09-30-bytebytego-doordash-agent-gateway
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
| omp, 5 essential tools | **36.6s** |
| Pi, default roster | 37.0s |
| Codex, default roster | 42.2s |

The experiment began as a complaint that omp was slower than Codex on wall clock, which the author expected to be
a "nothing-burger" and found to be true — **almost two times** slower. Cutting omp's roster to five tools is what
produced 36.6s. **The before/after on omp is the controlled result; the Pi and Codex figures are external
reference points at their own default rosters, not a roster sweep.**

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

## At fleet scale the execution surface is about a tenth of the bill; deliberation is the rest

Everything above measures a roster inside one turn - description tokens, decoding constraints,
roundtrips, compression that backfires. [[FD - Agent Muse Compute Demand]] supplies the other end of
the same ledger, and it reorders which of those savings matter. The caveat has to travel with every
figure: this is a **bottom-up scenario estimate** built on assumptions, not a measurement of anyone's
infrastructure, and the **100M DAU** premise is hypothetical.

Under those assumptions, the environment the tools run in is the small term. A concurrency chain of
100M DAU x **two active hours per day** / 24, x a **2.5x peak-to-average ratio**, plus **~20%
headroom** yields **~25M provisioned live VMs**. At a base case of **0.5 physical cores per live VM**
(a deliberately *less* efficient assumption than the **~0.23** implied by DeepSeek's DSec paper) that
is **12.5M physical cores**, or **~50K CPUs** at 256 cores each, estimated at **~$800M**; memory,
extrapolated from a single observed instance using **~3 GB** of an exposed 8 GB, gives **75 PB** at
**~$2B**. Those totals exclude networking, storage, orchestration, redundancy, facilities, cooling,
depreciation, and operations - and they still come to an estimated **~0.1 GW** for the entire
sandbox/VM layer against **~1-2 GW** of total average power.

The dominant term is the model calls the roster exists to trigger. FD derives energy per event from a
Microsoft study's median of **~0.31 Wh per normal query**, notes a long reasoning query at roughly
**15x the token count** using about **13x the energy** (**~4 Wh**), and widens that to an assumed
**5-10 Wh** per heavy reasoning-equivalent event. At **50 reasoning-equivalent events per DAU per
day** and 5 Wh each, that is **25 GWh/day**, or **~1.0 GW**. The quoted **3-4 GW** is a sensitivity
conclusion under higher reasoning demand, not a forecast.

The consequence for roster economics is a sorting rule, not a correction. This page's four A/B results
are measured and remain so; but under FD's assumed structure, demand tracks **reasoning-equivalent
events per user, not user count** - an agent that deliberates more per task raises compute demand
without acquiring a single new user. That splits the page's wins into two classes. Changes that remove
a *turn* - batching two notifications that produced **four model calls where one would do**, worth
**2.3%** - remove units of the dominant term. Changes that shorten what travels inside a turn, like
the **3.1%** from dropping `view` line-number prefixes, move tokens within an event that still
happens. Both are real; only the first compounds against the term FD estimates at roughly ten times
the sandbox layer.

Read that way, the local metric trap gets a second, structural reading. The Rust Token Killer saved
tokens per response and cost more overall because agents reopened files and re-ran commands - which is
to say it converted a cheap intra-turn saving into *additional reasoning-equivalent events*, the exact
currency FD's chain says dominates. None of this is measured end to end: no source here connects a
harness-level token saving to a watt-hour, and FD's per-event energy band is itself an assumption
stretched from one study.

## Catalogue size and resident roster size need not grow together

[[ByteByteGo - How DoorDash Built a Toolbox for AI Agents]] describes a shared gateway with
200+ servers while task-specific bundles and filters curate `tools/list`. That separates
organizational integration coverage from the tools resident in one agent's context, without
abandoning MCP.

The optimization has a distinct security boundary: hiding a tool from discovery is not proof that
it cannot be invoked. `tools/call` still rechecks authorization and applies the appropriate
downstream credential. Discovery overhead and task quality need measurement too; the source reports
adoption, not a controlled latency or token-saving result from bundle curation, and its more
dynamic discovery design remains planned work.

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
- **Does removing a turn actually remove a reasoning-equivalent event?** Batching cut four model calls
  to one in one measured case, but nothing here tracks whether the deliberation reappears later in the
  loop rather than disappearing.
- **What is the exchange rate between a token saved in the harness and a watt-hour?** FD's **5-10 Wh**
  band is an assumption widened from one study's **~0.31 Wh** median, so the two ends of this ledger
  are not yet in the same units.

## Related pages

- [[ByteByteGo - How DoorDash Built a Toolbox for AI Agents]]
- [[DoorDash]]
- [[Agent Security and Governance]]
- [[Can Bölük - The Harness Playbook]]
- [[GitHub - How We Make AI Coding More Cost Efficient]]
- [[FD - Agent Muse Compute Demand]]
- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[Coding Agent Harness]]
- [[Harness Optimization]]
- [[Harness State Authority]]
- [[Context Engineering]]
- [[Inference Efficiency Frontier]]
- [[Agentic Testing]]
- [[Agent Delegation]]
- [[Benchmark Optimization]]
- [[Agentic Loop]]
- [[Test-Time Scaling]]
- [[Multi-Tenant Agent Architecture]]
- [[Meta]]
- [[DeepSeek]]
