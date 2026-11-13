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
LinkedIn's engineering post. Its premise is that coding agents moved the slow part of shipping from
writing code to reviewing it. LinkedIn tried a vendor reviewer and then an off-the-shelf model with
its own rules. It settled on an orchestrator that runs independent subagent reviews, merges
duplicates, and sends single-reviewer findings to another model for verification. Changes are gated
by an LLM judge before release and measured in production by whether the code changed. A human still
approves. The reviewer covers more than **40,000** pull requests in a typical week and reports
**63.9%** acceptance. No models, costs, latencies, or comparison with human review are given.

## Key claims

### Review is the bottleneck, and partial automation is the target

- LinkedIn has more than **10,000** active repositories and tens of thousands of pull requests a
  week. Once agents write code in minutes, fixed human review hours become the constraint.
- **Full automation**, where AI approves on its own, is something "most labs are not there yet".
  LinkedIn uses **partial automation**: AI takes the first pass, the author (possibly a coding agent)
  addresses the comments, and a human approves. Most reviews post before a human opens the change.
- A reliable reviewer must be **grounded** (real problems on changed lines), **high-signal** (bugs
  and risky lines, not linter nits), **codebase-aware**, and **timely**.

### Two routes that failed first

- **Vendor reviewer:** a rules file cannot change the vendor's prompts or harness, and updates cannot
  be tested or rolled out gradually. In LinkedIn's AI-native pilot the comments were noisy, engineers
  opted out, and full manual review returned. Min Chen: "You don't own anything. They do something,
  they change something, you just react to it."
- **Off-the-shelf model with own rules:** comments became codebase-specific, but one unverified model
  hallucinated, some comments missed the diff's line numbers, and it kept missing whatever was thin in
  its training data. A **different model for review than for writing did not fix hallucination**; it
  prompted the idea of a second model verifying the first.

### Orchestrator, independent subagents, and layered rules

- Following the orchestrator-subagent pattern (citing Anthropic's multi-agent research post),
  subagents review the same change independently, "often each with a different model" in the
  article's general description, and return findings with line numbers.
- Rules come in three layers, each with its own owner: **company-wide** (for example YAML),
  **repository** (a markdown conventions file), and **pull-request** rules for one kind of change.
  One injected rules file cannot combine the right mix per change.
- Worked example, a new `cache.py` with a race condition and a bare `except`:
  - **Review:** subagents never see one another's findings, because a reviewer that reads another's
    output tends to agree, so independent agreement "counts as evidence".
  - **Merge:** three subagents finding the same five issues would post **fifteen** comments. A
    deterministic pass pairs overlapping line ranges, then an LLM decides whether each pair is the
    same problem. Merged findings rank higher.
  - **Verify:** a finding from only one subagent goes to another model to check against the code,
    which LinkedIn says "often saves real issues"; a contradiction lowers its confidence. Cosmetic
    findings, issues already fixed in a later commit, and findings against the repository's
    established patterns are suppressed.

### Evaluation before release and in production

- **Before release:** production and candidate versions review the same pull requests, and a separate
  model judges both against a fixed rubric of **six weighted yes-or-no criteria**. Every prompt, model,
  and harness change goes through it. Citing MT-Bench, the article says such judges suit comparisons
  but cannot reliably decide which comments are right.
- That gap is for a **golden dataset**: real pull requests at the point a bug was found, with human
  labels, so precision and recall can be measured. LinkedIn has built it and is "now building the
  eval on top of it".
- **In production:** emoji reactions are noisy, so acceptance means "the code actually changed"
  (Balaji Srinivasan). On thousands of AI comments, **63.9%** were accepted, highest for concurrency
  bugs and dead code (**100%**) and logic errors (**80%**). A daily trend report decides which rules
  to disable and which prompts to change.

### What comes next

- Balaji Srinivasan expects the next bottleneck to be confidence in the software as a whole, with
  review a bottleneck until automated validation exists. Deployment, monitoring, and incidents are
  next: "the faster we are pushing out code, the faster we are potentially breaking production."
- Planned: an optional **risk heat map** scoring each region of a diff so the riskiest is read first.

## Why it matters

This is the vault's clearest design for a reviewer that is more than one model, and it anchors the
new [[AI Code Review]] page. Its acceptance metric resembles
[[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization|Cloudflare's]]
acted-on proxy without Cloudflare's coincidence baseline, a comparison [[Agentic Testing]] can now
record. The judge-plus-golden-dataset split gives [[LLM-as-a-Judge]] a production case where the judge
ranks versions and labelled data decides correctness. The bottleneck sequence of writing, review,
then whole-system confidence extends [[AI-Native Software Development Lifecycle]]. The independence
claim sits beside the "quorum is not proof" warning in [[Multi-Agent Coordination]]. It is another
company case relayed by [[ByteByteGo]].

## Tensions / open questions

- **Independence is asserted, not shown.** Subagents cannot see one another's findings, but the
  article does not say which models LinkedIn runs or whether they share prompts and context, so
  correlated errors remain possible.
- **Acceptance has no baseline.** Code near a comment can change for other reasons. Cloudflare
  measured about **15%** for lines 30 to 40 away; LinkedIn reports none, so 63.9% is an upper bound on
  comment-caused change, not precision.
- **Category rates lack counts.** The **100%** and **80%** figures come from a chart without sample
  sizes, and the overall denominator is only "thousands".
- **Correctness is unmeasured.** The golden-dataset eval is unfinished, no precision, recall, or miss
  rate is reported, and suppressions are unaudited: a bug in an "established pattern" could be hidden.
- **Missing operations data.** No cost per review, latency, model names, or human-only comparison;
  the claim that agents moved the bottleneck to review is framing, not measurement.
- **Relay.** LinkedIn's figures reach the vault through ByteByteGo. The Datadog and WarpBuild blocks
  are sponsorship.

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
