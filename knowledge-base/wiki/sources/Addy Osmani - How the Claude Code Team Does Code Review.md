---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-15-osmani-claude-code-review
source_title: How the Claude Code team does code review
source_author: Addy Osmani
source_url: https://claude.dev/blog/solving-code-review-at-anthropic/
tags:
  - source/summary
  - code-review
  - coding-agents
  - engineering-process
source_ids:
  - src-2026-10-15-osmani-claude-code-review
status: active
---

# Addy Osmani - How the Claude Code Team Does Code Review

## Summary

An account of how Anthropic restructured code review once agents were writing most of the code. The
framing sentence is **"We didn't remove review. But we did move most of the reading to machines"** —
routine reading and verification became automated, while humans kept product direction, architecture,
high-risk changes, evidence assessment, and accountability.

The most transferable material is not the headline metrics but the **convergence controls**: the
explicit machinery that stops an agent author and an agent reviewer from looping forever.

## Key claims

### The pipeline

- **Before the PR exists:** Claude runs tests, builds, linters, or visual checks and **must show
  evidence**. A fresh-context subagent reviews the diff. Separate internal skills hunt bugs, simplify
  diffs, check end-to-end behavior, and inspect UI changes.
- **Repository guidance is split in two:** `CLAUDE.md` carries project context and conventions;
  **`REVIEW.md`** carries repository-specific failure modes, evidence requirements, paths to skip, and
  limits on stylistic findings.
- **On every PR:** required CI (lint, type checks, cross-platform tests, builds, packaging) → Claude
  reviews the diff against repository and stated intent → **multiple agents search for bugs in parallel
  and verifier agents vote**, with findings surviving only on sufficient agreement → a separate
  automated security review that can block merge → every finding must be fixed or explicitly resolved.
- **Risk-tiered human approval:** a classifier assigns low, medium, or high risk requiring **0, 1, or 2**
  human approvals. Sensitive paths, CI workflows, and owner paths always require humans.
  **"The change sets the tier, not the author."** And **"An agent's approval never counts as a
  person's."** Whoever prompted an agent-written change is accountable and counts as a required reviewer.
- **Merge and release:** a merge queue reruns checks against the latest `main`; changes ship behind
  flags to employees, then `latest`, then `stable`, with telemetry watched by authors and on-call and
  flags disabled or builds reverted on trouble.
- **Continuous improvement:** incidents and reverts become expert-confirmed evaluation cases run daily;
  reviewer changes are scored against the accumulated set; noise is assessed from how humans respond to
  findings and from runs on **known-clean PRs**.

### Convergence controls

- Review is **capped after three rounds**, later passes can be **diff-only**, repeated findings are
  suppressed, and agents are asked to identify **bug classes** rather than isolated lines. Review agents
  also scan existing code nightly.
- The motivating failure: one CLI PR went through **more than fifty rounds** of review and fixes.
- About **59%** of repeatedly flagged code **predated the reviewer's first pass** — the loop was partly
  re-litigating pre-existing code, not the change.
- After the convergence work, the reported movement was: one-round pass rate **65% → 78%**, five-or-more
  rounds **8.9% → 1.5%**, and mean reviews-to-pass **2.08 → 1.32**. Population and time window are not
  specified.

### Reported scale, all self-reported

- Claude writes **"about 90 percent"** of Claude Code's own code.
- Anthropic monorepo changes rose from **about 2,500 in May to more than 30,000 in September**.
- From June to September, merged Claude Code PRs **more than doubled** while the share requiring
  reversion **fell by more than 40 percent**. No counts or denominator given.
- After the code-review research preview, substantive comments rose from **16% to 54%** of internal PRs.
- Boris Cherny **estimates** verification makes the final result **"two to three times better"** — an
  estimate, with no stated method.
- **[Illustrative]** "Most PRs over 1,000 lines get findings, and most small ones come back clean."

## Why it matters

[[Agentic Testing]] in this vault has repeatedly found that agents will assert success without evidence.
This source shows an organization building the counter-structure at process scale: evidence is
**required before** a PR exists, findings must survive **verifier voting** before reaching a human, and
a separate daily eval set derived from real incidents measures whether the reviewer is getting better or
merely noisier.

The risk-tier rule is the sharpest contribution to [[AI-Native Software Development Lifecycle]]. It
decouples **who wrote the change** from **how much human scrutiny it needs**, which is the opposite of
the common instinct to review agent output more heavily because an agent wrote it. And the 59% figure is
the vault's best evidence that agent review loops fail by **scope drift into surrounding code**, not
only by hallucinated findings.

## Tensions / open questions

- The June-September comparisons **do not isolate** the causal effect of AI review from changes in
  practices, workload, staffing, or release controls. There is no controlled comparison against
  conventional human review.
- The revert reduction comes without exact counts, incident definitions, confidence intervals, or causal
  analysis. The "two to three times better" figure is explicitly an estimate.
- The authors' own caveats are substantial: automation does not catch everything; human time includes
  **fixing bad code**, so reducing review time may just move the cost; there are **no circuit breakers**
  that automatically tighten approval when revert or incident metrics worsen; agent author/reviewer
  pairs can loop indefinitely; and slower development may reduce error rates partly by reducing how
  much is being done.
- The team admits no formal method for preserving **team-wide codebase understanding** once humans stop
  reading trivial diffs — they rely on Claude-generated explainers and visual artifacts.
- High review coverage does not prove undetected defects are rare.
- The process likely depends on Anthropic-specific tooling, conventions, flags, telemetry, and rollback
  culture; nothing here establishes it transfers.

## Affected pages

- [[AI-Native Software Development Lifecycle]]
- [[Coding Agent Harness]]
- [[Agentic Testing]]
- [[Addy Osmani]]

## Raw capture

- [[How the Claude Code team does code review]]

## Citations

- Raw capture: [[How the Claude Code team does code review]]
- Canonical URL: <https://claude.dev/blog/solving-code-review-at-anthropic/>
- Published 2026-10-15; captured 2026-10-22.
- Quotes Boris Cherny's verification estimate as reported in the article.

## Related pages

- [[Agent Delegation]]
- [[Agent Security and Governance]]
- [[Harness Optimization]]
- [[Agent Workflow Maturity]]
- [[LLM-as-a-Judge]]
- [[Agent Observability]]
- [[Anthropic]]
