---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-10-bytebytego-linkedin-ai-code-review
source_title: How LinkedIn Uses AI to Review 40,000 Pull Requests a Week
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-linkedin-uses-ai-to-review-40000
tags:
  - source/summary
  - code-review
  - multi-agent
  - evaluation
source_ids:
  - src-2026-11-10-bytebytego-linkedin-ai-code-review
status: active
---

# How LinkedIn Uses AI to Review 40,000 Pull Requests a Week

## Summary

ByteByteGo explains how LinkedIn built an in-house AI code reviewer, drawing on interviews with Min
Chen (Principal Staff Engineer) and Balaji Srinivasan (Senior Director of Engineering) and on
LinkedIn's own engineering post. The article argues that coding agents moved the slow part of
shipping from writing code to reviewing it. It compares three routes to a reviewer: buy a vendor's
system, wrap an off-the-shelf model in your own rules, or build a multi-agent system. LinkedIn tried
the first two before settling on an orchestrator that runs independent subagent reviews, merges
duplicates, and sends single-reviewer findings to a second model for verification. Changes are
gated by an LLM judge before release and measured in production by whether the code changed. The
reviewer keeps a human as the approver, covers more than **40,000** pull requests in a typical week,
and reports **63.9%** acceptance. No models, costs, latencies, or comparison with human reviewers
are given.

## Key claims

### Review is the new bottleneck, and partial automation is the target

- LinkedIn has more than **10,000** active repositories and tens of thousands of pull requests a
  week. Once agents write code in minutes, fixed human review hours become the constraint.
- The article separates **full automation**, where AI approves on its own and "most labs are not
  there yet", from **partial automation**, where AI takes the first pass and a human still approves.
  LinkedIn uses partial automation. The author, which may be a coding agent, addresses AI comments
  first so humans spend their time judging the fixes.
- A reliable reviewer needs four properties: **grounded** (real problems on the changed lines),
  **high-signal** (bugs and risky lines, not linter nits), **codebase-aware**, and **timely**.
  Most of LinkedIn's reviews are posted before the first human reviewer opens the pull request.

### Two failed routes before the multi-agent design

- **Vendor reviewer.** Quick to set up, but generic: a rules file cannot change the vendor's prompts
  or harness, and the vendor decides when models or instructions change, so updates cannot be tested
  or rolled out gradually. In LinkedIn's AI-native pilot the comments were noisy and did not fit
  each repository's rules, engineers asked to opt out, and full manual review returned. Min Chen:
  "You don't own anything. They do something, they change something, you just react to it."
- **Off-the-shelf model with own rules.** Comments became codebase-specific, but a single unverified
  model hallucinated, some comments did not match the diff's line numbers, and one model repeatedly
  misses whatever is thin in its training data. Using **a different model for review than for writing
  did not fix hallucination**; it led the team to ask whether a second model could verify the first.

### Orchestrator, independent subagents, and layered rules

- The design follows the orchestrator-subagent pattern, citing Anthropic's multi-agent research post.
  Subagents review the same pull request independently, "often each with a different model" in the
  article's general description, and return findings with line numbers.
- Rules come in three layers, each with its own scope and owner: **company-wide** (for example YAML),
  **repository** (a markdown file of conventions), and **pull-request** rules for one kind of change.
  A dedicated subagent reviews against them. Injecting one rules file as context cannot combine the
  right mix for each change.
- Worked example: a new `cache.py` with a race condition and a bare `except`.
  - **Review:** subagents never see one another's findings, because a reviewer that reads another's
    output tends to agree. The article concludes that independent agreement "counts as evidence".
  - **Merge:** three subagents finding the same five issues would give **fifteen** comments for five
    problems. A deterministic pass marks overlapping line ranges as candidates, then an LLM decides
    whether each pair is the same problem. Merged findings are ranked higher.
  - **Verify:** a finding raised by only one subagent goes to another model to check against the
    code; LinkedIn's post says this "often saves real issues". A contradiction lowers the confidence
    score. Cosmetic findings, issues already fixed in a later commit, and findings that go against the
    repository's established patterns are suppressed.

### Evaluation before release and in production

- **Before release:** the production version and the candidate review the same pull requests, and a
  separate model judges both against a fixed rubric of **six weighted yes-or-no criteria**. Every
  prompt, model, and harness change goes through it. Citing the MT-Bench paper, the article says such
  judges work for comparisons but cannot reliably decide which comments are right.
- That gap is meant to be filled by a **golden dataset**: real pull requests at the point a bug was
  found, with humans labelling which comments are correct, so precision and recall can be measured.
  LinkedIn has built the dataset and is "now building the eval on top of it".
- **In production:** emoji reactions are noisy. Acceptance means "the code actually changed"
  (Balaji Srinivasan). On thousands of AI comments, engineers accepted **63.9%**, with the highest rates
  for concurrency bugs and dead code (**100%**) and logic errors (**80%**). A daily acceptance trend
  report decides which rules to disable and which prompts to change.

### What comes next

- Balaji Srinivasan expects the next bottleneck to be confidence in the quality of the software as a
  whole, and review to stay a bottleneck until automated validation exists. Deployment, monitoring,
  and incident handling are next targets: "the faster we are pushing out code, the faster we are
  potentially breaking production."
- Planned: an optional **risk heat map** that scores each region of a diff by predicted risk so
  engineers review the riskiest parts first.

## Why it matters

This is the vault's clearest end-to-end design for a reviewer that is not a single model, which
makes it the anchor for the new [[AI Code Review]] page. Its acceptance metric is close to
[[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization|Cloudflare's]]
acted-on proxy, but without Cloudflare's coincidence baseline, which gives [[Agentic Testing]] a
direct comparison of how reviewer value is measured. The pre-release judge and the golden dataset
add a production case to [[LLM-as-a-Judge]]: a judge used for comparisons, with correctness left to
labelled data. Its bottleneck account (writing, then review, then whole-system confidence) extends
[[AI-Native Software Development Lifecycle]]. Its independence claim sits beside the vault's
warnings in [[Multi-Agent Coordination]] that agreement is not proof. It is another named-company
relay for [[ByteByteGo]].

## Tensions / open questions

- **Agreement as evidence depends on independence that is asserted, not shown.** Subagents are
  isolated from one another's findings, but the article does not say which models LinkedIn runs,
  whether they differ, or whether they share prompts and context. Correlated errors are the obvious
  risk; compare the vault's "quorum is not proof" warning in [[Multi-Agent Coordination]].
- **The acceptance metric has no baseline.** Code near a comment may change for unrelated reasons.
  [[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]] measured
  that rate (about **15%** for lines 30 to 40 away). LinkedIn reports none, so 63.9% is an upper bound
  on comment-caused change, not a precision figure.
- **Category rates lack sample sizes.** The **100%** and **80%** figures come from a chart with no
  counts. Small categories could produce them by chance. The overall denominator is only "thousands".
- **Correctness is not yet measured.** The golden-dataset eval is still being built, and no
  precision, recall, or miss rate is reported. What gets suppressed is not audited either:
  "against the repository's established patterns" could hide a real bug in an established pattern.
- **Missing operational numbers.** No cost per review, latency, model names, or comparison with
  human-only review. The opening claim that coding agents moved the bottleneck to review is framing,
  not a measured result.
- **Relay.** The figures are LinkedIn's, relayed by ByteByteGo through interviews and LinkedIn's post.
  Datadog and WarpBuild blocks are sponsorship, not part of the article.

## Affected pages

- [[AI Code Review]]
- [[LLM-as-a-Judge]]
- [[Agentic Testing]]
- [[AI-Native Software Development Lifecycle]]
- [[ByteByteGo]]
- [[Multi-Agent Coordination]]

## Raw capture

- [[knowledge-base/raw/sources/How LinkedIn Uses AI to Review 40,000 Pull Requests a Week]]

## Citations

- Canonical URL: https://blog.bytebytego.com/p/how-linkedin-uses-ai-to-review-40000 (email
  tracking parameters removed).
- Byline in capture: ByteByteGo. Published 2026-11-10; captured 2026-11-10. Interviewees: Min Chen and
  Balaji Srinivasan of LinkedIn.
- References listed by the article, none captured in this vault:
  - LinkedIn Engineering, "High-Signal AI Code Review That Adapts to Your Codebase at Scale".
  - GitHub, "60 million Copilot code reviews and counting".
  - Anthropic, "How we built our multi-agent research system".
  - Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (arXiv 2306.05685).

## Related pages

- [[AI Code Review]]
- [[LLM-as-a-Judge]]
- [[Agentic Testing]]
- [[AI-Native Software Development Lifecycle]]
- [[Multi-Agent Coordination]]
- [[ByteByteGo]]
- [[Addy Osmani - How the Claude Code Team Does Code Review]]
- [[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]]
- [[AI Builder Club - How to Review AI-Generated Pull Requests (2026)]]
- [[ByteByteGo - How GitHub Used AI to Port Copilot From TypeScript to Rust in Record Time]]
- [[Model Routing]]
