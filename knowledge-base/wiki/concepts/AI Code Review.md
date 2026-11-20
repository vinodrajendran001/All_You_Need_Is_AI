---
type: concept
created: 2026-11-13
updated: 2026-11-20
tags:
  - concept
  - code-review
  - coding-agents
  - evaluation
source_ids:
  - src-2026-11-10-bytebytego-linkedin-ai-code-review
  - src-2026-11-11-bytebytego-github-copilot-rust-port
  - src-2026-10-15-osmani-claude-code-review
  - src-2026-10-20-cloudflare-inference-bill
  - src-2026-08-05-aibuilderclub-reviewing-ai-generated-pull-requests
  - src-2026-11-13-orlanski-slop-moves-up
  - src-2026-11-12-huntley-answer-is-engineering
status: active
---

# AI Code Review

## Definition

AI code review uses language-model reviewers to read a pull request before, or alongside, human
reviewers and post line-level findings. It is usually several agents coordinated by a harness, not
one model. In the vault's sources the AI takes the first pass and a human, or a human-owned policy,
decides what merges. They differ on how much authority the machine gets, how reviewers are made
independent, and how reviewer quality is measured.

## Why it matters

Once coding agents write a change in minutes, fixed human review hours become the constraint.
[[ByteByteGo - How LinkedIn Uses AI to Review 40,000 Pull Requests a Week]] makes that argument
directly, and [[Addy Osmani - How the Claude Code Team Does Code Review]] frames Anthropic's answer as
"we did move most of the reading to machines". The reviewer is then an AI system with its own failure
modes. A noisy reviewer loses trust: LinkedIn's engineers opted out of a vendor reviewer. A reviewer
that keeps re-flagging code loops: one Claude Code change went through more than fifty review rounds.
And reviewers cost money: [[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization|Cloudflare's]]
average review rose to about $2.46 before optimization. Building a reviewer is therefore an
evaluation and governance problem as much as a prompting one.

## Current synthesis

### Authority: the AI reads first, and approval is a policy decision

- LinkedIn uses **partial automation**: the AI comments first, the author (possibly a coding agent)
  responds, and a human approves. It says full automation is where "most labs are not there yet".
- Anthropic's Claude Code team lets a classifier set the risk tier, which requires **0, 1, or 2**
  human approvals; "The change sets the tier, not the author", and "An agent's approval never counts
  as a person's." The zero-approval tier lets low-risk changes from trusted authors merge once
  automated review and security checks pass, unless a second classifier calls for a person. That
  goes further than LinkedIn.
- [[AI Builder Club - How to Review AI-Generated Pull Requests (2026)]] is stricter: a second model
  produces a worklist and never approves, and the submitter must be able to explain and own every line.
- In [[ByteByteGo - How GitHub Used AI to Port Copilot From TypeScript to Rust in Record Time|GitHub's Copilot runtime port]],
  Copilot Code Review and other bots checked every commit, and human reviewers concentrated on
  architecture, interface contracts, and flagged risks.

These are not contradictory designs so much as different settings of one variable. The open question
is which evidence justifies the zero-human tier, since none of the sources publishes the miss rate of
automated clearance.

### Architecture: independent reviewers, then merge and verify

- LinkedIn's orchestrator sends the same diff to subagents that **never see each other's findings**,
  merges duplicates with a deterministic line-range pass followed by an LLM same-problem check, and
  sends findings raised by only one subagent to another model to verify against the code. Cosmetic
  findings, issues fixed in a later commit, and findings against established repository patterns are
  suppressed.
- Anthropic runs parallel bug hunters and **verifier votes**; findings survive only with enough
  agreement. Cloudflare's coordinator hands each merge request to **specialist reviewers**, with risk
  tiers setting intensity.
- GitHub's port review is a different task: agents on different models compared new Rust against the
  old TypeScript line by line. A reference implementation turns review into a parity check, which
  is easier to ground than judging a novel change.

Independence carries the weight in these designs. LinkedIn argues that agreement between isolated
reviewers "counts as evidence", yet [[Multi-Agent Coordination]] records that quorum is not proof
when agents share models, prompts, and evidence. LinkedIn's own history points the same way: using a
**different model for review than for writing did not fix hallucination**. What helped was a
verification step that checks a finding against the code. No source reports how correlated its
reviewers' errors are.

### Context: rules come in layers

LinkedIn splits review rules into company-wide, repository, and pull-request layers, each with an
owner and a dedicated subagent, and argues that a single injected rules file cannot combine them.
Anthropic's split is between `CLAUDE.md` for project context and `REVIEW.md` for repository-specific
failure modes, evidence requirements, skip paths, and limits on stylistic findings. Both treat
reviewer context as owned configuration. LinkedIn's vendor experience shows the opposite case: a
hosted reviewer meets the codebase only through a rules file while the vendor controls the prompts,
the harness, and update timing.

### Measurement: did the code change, against what baseline, and was it right

- **Production proxy.** LinkedIn counts a comment as accepted when "the code actually changed" and
  reports **63.9%**. Cloudflare uses the same proxy with a **coincidence baseline**: lines 30 to 40
  away changed about **15%** of the time. Against that, authors acted on **59%** of serious
  code-quality findings, up from **34%**. LinkedIn reports no baseline, so the two rates are not
  comparable. Cloudflare's caveat applies to both: a changed line "shows they did something, not that
  the finding was right."
- **Judges for comparisons.** LinkedIn gates every prompt, model, and harness change with an LLM judge
  scoring production against candidate on **six weighted yes-or-no criteria**. Cloudflare had two
  models from different providers judge a blinded sample of **657** findings. See [[LLM-as-a-Judge]].
- **Ground truth.** LinkedIn's golden dataset of real pull requests captured when a bug was found is
  built, with the eval still in progress. Anthropic turns incidents and reverts into daily evaluation
  cases and runs the reviewer on **known-clean** pull requests as a negative control. Only a labelled
  set yields recall, and no source yet reports one.

### Noise and convergence are explicit controls

Anthropic caps review at three rounds, narrows later passes to the diff, and suppresses repeated
findings. It found about **59%** of repeatedly flagged code predated the reviewer's first pass, and
its one-round pass rate rose from **65%** to **78%**. LinkedIn suppresses at posting time and runs a
daily acceptance trend report that decides which rules to disable. Both trade some recall for trust.
LinkedIn's "against established patterns" filter in particular could hide a real bug in a widespread
pattern, and neither source reports what suppression costs; Anthropic says only that it A/B tested
its filters on its own PRs.

### The slop worth reviewing has moved from lines to design

[[Gabe Orlanski - Slop Is Moving Up the Stack]] suggests that rule-based review targets are aging
out. Orlanski authored SlopCodeBench, LibraryDesignBench and LibraryUseBench, so these are
**first-party benchmark results** from the person who built the benchmarks; he writes "I might be
biased" and closes by asking to be hired. Line patterns fell: `return None, error` tuples in both
the Claude and GPT families, and giant functions sharply in Anthropic's newer runs (the newer GPT
runs got worse on giant functions). The regressions are now design choices: "Error handling got
worse for all three families". New GPT runs have **49–74** except clauses that put
`KeyError`/`TypeError` next to I/O errors, against **2** and **10** for GPT-5.4 and 5.5, so a
programming bug reaches the user as an operational error ("rollback failed"). Some flagged patterns
were patched around rather than fixed. `except Exception:` became `except OSError: return None`,
which in one example means "the protected operation runs with no role check". And on
LibraryUseBench, "every model hand-writes something the library already does, in 73% to 100% of its
solutions".

For a reviewer, the important question shifts from whether a line matches a known anti-pattern to
whether the change should exist at all, given what the codebase or a dependency already provides.
None of the reviewer designs above reports recall on that class. The samples are small (LUB and LDB
use 15 tasks), and what counts as a rewrite or a workaround is judged by subagents, with no human
agreement rate reported.

### Deterministic back pressure as the first reviewer

[[Geoffrey Huntley - The Answer to AI Is Engineering]] argues that much of what reviewers catch should
never reach review. "Ralph was never just about loops. It was about stopping the loop from closing on
bad code." The mechanism is deterministic: pre-commit or prek hooks that block a push that does not
compile, plus static rules such as "this domain must never be coupled to that domain" (SQL must not
reference the API). That would normally be an architecture review, he says, "but agents are pretty
dumb and will do it anyway". His claim is that teams can "engineer away much of the need for code
review" with checks like these.

This is the same move as LinkedIn's deterministic duplicate pass and Anthropic's known-clean controls:
put cheap, exact checks ahead of probabilistic reviewers. Huntley's is the strongest version, and it is
**argument, not evidence**: a practitioner talk with personal demos and no miss-rate comparison.
Deterministic checks catch only what someone encoded. Orlanski's design-level slop is the class such
rules have not yet captured, and his "slop that moved" examples show agents patching around the rules
that do exist.

### Re-implementing library code: defect or policy?

The two sources disagree directly on a behaviour a reviewer has to rule on. **Orlanski** counts
hand-written copies of library functionality as slop, "another place for a bug to hide", and measures
it: 73% to 100% of LibraryUseBench solutions do it, and implementers had to work around agent-written
libraries **40%** of the time against **27%** for a human-written one. **Huntley** recommends the
opposite as policy. He says "I don't think we need libraries anymore", reports that he no longer uses
much open source above the kernel and other low-level software, and advises to "either generate it
first-party, or vendor the open-source software" so agents can patch it without waiting on upstream.
His reason is supply-chain and incident-response cost, not code quality, and he excludes cryptography.

Neither weighs the other's cost. Orlanski measures quality on a benchmark with no supply-chain term;
Huntley argues from an incident list he does not source, with no quality measurement. A review rule
therefore has to choose explicitly (flag re-implementation as redundancy, or accept it where a
vendoring or generation policy exists), and nothing in the vault shows which choice produces fewer
defects. Both positions come with an interest attached: Orlanski is promoting his own benchmarks, and
Huntley works at Antithesis, which makes the verification libraries his talk recommends.

### Where review goes next

LinkedIn plans an optional **risk heat map** that scores diff regions by predicted risk, and expects
the next bottleneck to be confidence in the whole system rather than in each change. That connects
review to [[Agentic Testing]] and to the release and monitoring stages of the
[[AI-Native Software Development Lifecycle]]: review alone cannot carry quality once code arrives
faster than people can read it.

## Open questions

- How correlated are "independent" reviewers' errors when they share base models, rules, or
  retrieved context?
- What miss rate would justify a zero-human approval tier, and who measures it after deployment?
- Can acceptance-based metrics be compared across organisations without a shared coincidence
  baseline and category sample sizes?
- What do suppression filters cost in recall, and how would a team detect a suppressed true bug?
- How does per-review cost (reported only by Cloudflare) scale with the fan-out and verification
  steps LinkedIn and Anthropic describe?
- Can a reviewer reliably detect re-implementation of functionality the codebase or a dependency
  already provides, and should it flag it where a team generates or vendors code by policy? Orlanski
  measures the quality cost and Huntley argues the supply-chain benefit; no source compares both.
- What share of today's review findings could deterministic hooks and coupling rules catch before
  review? Huntley says "much"; no source measures it.

## Related pages

- [[ByteByteGo - How LinkedIn Uses AI to Review 40,000 Pull Requests a Week]]
- [[Addy Osmani - How the Claude Code Team Does Code Review]]
- [[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]]
- [[AI Builder Club - How to Review AI-Generated Pull Requests (2026)]]
- [[ByteByteGo - How GitHub Used AI to Port Copilot From TypeScript to Rust in Record Time]]
- [[Agentic Testing]]
- [[LLM-as-a-Judge]]
- [[AI-Native Software Development Lifecycle]]
- [[Multi-Agent Coordination]]
- [[Model Routing]]
- [[Reasoning Effort Control]]
- [[Coding Agent Harness]]
- [[GitHub]]
- [[Gabe Orlanski - Slop Is Moving Up the Stack]]
- [[Geoffrey Huntley - The Answer to AI Is Engineering]]
