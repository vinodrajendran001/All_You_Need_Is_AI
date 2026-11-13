---
type: concept
created: 2026-11-13
updated: 2026-11-13
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
