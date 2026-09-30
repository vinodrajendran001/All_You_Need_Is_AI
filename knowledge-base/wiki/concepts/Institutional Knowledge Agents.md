---
type: concept
created: 2026-09-04
updated: 2026-09-30
tags:
  - concept
  - ai-agents
  - knowledge-management
  - evaluation
  - memory
source_ids:
  - src-2026-09-02-meta-organizational-second-brain
  - src-2026-09-29-yoon-multiplayer-ai
status: active
---

# Institutional Knowledge Agents

## Definition

An institutional knowledge agent encodes a specific organisation's accumulated domain judgement — its positions,
its vocabulary, its procedures — in reviewable text rather than in model weights, and improves by **compiling
expert feedback into that text** under regression tests instead of by retraining.

## Why it matters

The vault's agent pages mostly concern general capability: how an agent plans, calls tools, or manages context.
This is a different problem. A compliance reviewer, a privacy assessor, or an internal policy expert is valuable
because of what their organisation has decided over years, and none of that is in a base model. The usual answers
are fine-tuning (slow, opaque, hard to audit) or retrieval (works, but flattens everything into one undifferentiated
corpus).

[[Meta - An Organizational Second Brain]] takes a third position and is unusually specific about it: **"Keep the
complexity in text files, not in model weights or opaque embeddings. Every improvement is a text edit a domain
expert can review in 30 seconds."** The reported deployment is a compliance-domain expert agent built on **200+
knowledge files**, improving over three two-week sprints without any model retraining.

The stakes are governance as much as capability. A weight update cannot be diffed, reviewed by a non-engineer, or
reverted by a domain expert. A text edit can be all three — which is what makes expert review, adversarial review,
and a deterministic linter possible at all.

## Current synthesis

**Separate what the agent knows from how it reasons.** The architecture splits into two file kinds with a hard
rule between them: **recipes** are imperative procedures containing no domain facts; **knowledge files** are
declarative positions containing no procedures. The payoff is attribution — a wrong answer is either a recipe bug
or a knowledge gap, and you can tell which. Mixed files make every failure ambiguous.

The 200+ files fall into four types: **Position files** (the organisation's stance on a specific question),
**Taxonomy files** (controlled vocabulary), **Routing indexes** (deterministic paths from question shape to
relevant files), and **Gateway files** (entry points that orient the agent before it descends).

**Routing is deterministic, not similarity-based.** The routing indexes are lookup structures rather than
embedding neighbourhoods. This is the sharpest departure from [[Retrieval-Augmented Generation]] practice and the
reason the linter can work: a deterministic route can be checked for dangling references, and an embedding
neighbourhood cannot.

**The wiki/RAG split is by information density and expected usage frequency.** Dense, frequently needed material
becomes a curated file the agent reads; sparse or rarely needed material stays in retrieval. This is a resource
allocation rule, not an architectural preference, and it gives [[Retrieval-Augmented Generation]] a criterion it
otherwise lacks.

**Progressive disclosure is the cost mechanism.** Gateway files plus routing indexes mean the agent loads what a
question needs rather than a fixed context. Reported effect: **roughly 80% fewer tokens per turn**.

**Maintenance is a compilation problem.** The self-improvement loop is four staged steps — diagnose, compile,
validate, expert review — and each stage has a specific defence:

- **Diagnosis needs the right question.** Classifying failures by conversational form did not work. The test that
  did: **"Could the agent have reached the correct conclusion from its source materials?"** If yes and it erred,
  it is a recipe bug. If no, it is a knowledge gap. If experts disagree, the underlying position is ambiguous and
  the fix is a decision, not an edit.
- **Compilation is reviewed adversarially.** A second agent, with no knowledge of the rationale, sees only the
  diffs and argues against them. Reviewing the change without the story that motivated it is the point.
- **Validation is two-layered.** A **deterministic linter** checks dangling cross-references, file-size budgets,
  identifier collisions, and dependency cycles — *"not probabilistic. It passes or fails."* Then **targeted replay
  is blind**: the agent does not know it is being tested, and the judge does not know what changed.
- **Every fix becomes a regression test.** The suite grows with the knowledge base, so the loop cannot silently
  trade an old capability for a new one.

**Bidirectional dependencies make the graph checkable.** Every file declares `depends_on` and `referenced_by` in
YAML frontmatter. That redundancy is what turns "did this edit break something?" into a mechanical query.

**This vault is an instance of the pattern.** [[Schema-Driven Knowledge Base]], [[Persistent Wiki]],
[[Index and Log]], and [[Ingest Query Lint Loop]] describe the same shape from the inside — declared frontmatter,
a routing index, an append-only log, and a lint pass. The independent convergence is the most useful thing here,
and the divergences are the most instructive: Meta's design adds **automated regression replay** and an
**adversarial reviewer** that this vault does not have, and it enforces the recipe/knowledge split that this vault
leaves implicit.

**Prior art is acknowledged.** The source cites Karpathy's LLM Wiki proposal (see [[Andrej Karpathy]]) and
Google's Open Knowledge Format, positioning itself as a production instance of an idea already circulating rather
than a novel invention.

## A second route to the same store: extract from what shipped instead of asking experts to write

Until now this page had one source and one method - compile expert feedback into reviewable text under
regression tests. [[Jina Yoon - We're Building Multiplayer AI]] describes a second organisation
reaching a structurally similar store by a different route, and it arrives carrying a number that
bears directly on the first method's main cost. PostHog's earlier attempt was the expert-writes shape
in miniature: over **90 days**, **64 users** started a shared `CONTEXT.md` and only **14** ever edited
it. This is internal product observation, not a study - no denominator of eligible users, no selection
method, no comparison group - and PostHog is a software company rather than a compliance
organisation, so it is a caution rather than a refutation of the curated method.

Its replacement keeps the artifact and drops the author. A nightly **"dreaming" task** writes a
version-controlled Markdown wiki from work objects that already exist - PRs, docs, dashboards - and
the selection rule carries the design: record what was **actually shipped, merged, or decided in a
day**, not meeting notes or brainstorming documents, so the agent does not treat proposals as company
state. That is the same worry the recipe/knowledge split addresses from the other side. Meta types
content so a wrong answer can be attributed to a procedure or a position; PostHog filters by
*commitment* so the store never records something the organisation did not decide. One makes failure
diagnosable, the other makes ingestion selective, and neither substitutes for the other.

The disagreement is worth keeping unresolved, because the two methods fail in opposite ways. Meta's
loop is deliberately expensive and human-gated - adversarial review of diffs without the rationale,
blind targeted replay, expert sign-off, a deterministic linter over a declared dependency graph - and
this page already asks what that costs as the file count grows past 200. PostHog's loop removes the
human writer entirely and pays in evidence: it reports **no measured hallucination reduction, token
savings, latency change, or task-quality lift**, and the context layer had been dogfooded for only
**a few weeks** at publication, with no stated population for that trial - the **~200 employees**
figure the post gives is scoped to three recurring Space-**setup** patterns. The vault therefore now
holds one curated-and-reviewed institutional memory with qualitative results and one
derived-and-unreviewed institutional memory with no results. Neither is validated.

Governance separates them further. Meta's setting is compliance, where positions are written down,
experts exist, and a review culture is already in place - the conditions this page flags as unusually
favourable. PostHog calls **governance and permissions one of its biggest blind spots** and says it is
interviewing users to learn more, observes that users **overwhelmingly preferred starting tasks
privately** despite an expectation of shared defaults, and warns that its findings may depend on a
low-hierarchy culture without strict role-based access control. Automatically derived institutional
memory inherits whatever access boundaries its source
work objects carry, which the curated method resolves by putting a human at the gate. That is a real
cost of removing the writer, not an implementation detail.

## Open questions

- **The results have no denominators.** "Useful almost all the time," "days to minutes," and "zero regressions"
  after three sprints are all qualitative. There is no baseline, no task count, no accuracy figure, and no
  comparison against fine-tuning or plain RAG on the same workload.
- **"Zero regressions" is measured by the suite the same loop wrote.** A regression the diagnosis step never
  characterised would not be in the suite to catch.
- **The ~80% token reduction is unattributed.** Progressive disclosure, routing, and file granularity all changed
  together, and no ablation separates them.
- **Does the recipe/knowledge separation hold under pressure?** Real procedures tend to embed facts. The source
  states the rule but does not report how often it was violated or how violations were detected.
- **What is the cost of the loop itself?** Adversarial review, blind replay, and expert sign-off are ongoing
  expenses. Nothing is reported about how they scale as the file count grows past 200.
- **Does it generalise beyond compliance?** Compliance is unusually well suited: positions are written down,
  experts exist, and correctness is arguable. Domains with tacit or contested knowledge may not compile.
- **Does a derived store need a review gate at all**, or does a commitment filter - shipped, merged, or
  decided - substitute for one?
- **What is the lint equivalent for a derived wiki?** Meta's deterministic linter checks a declared
  dependency graph; a nightly extraction from work objects has no declared graph to check.
- **How does either method record a reversal?** A shipped decision that is later undone is a commitment
  by the ingestion rule and a stale position by the knowledge rule.

## Related pages

- [[Meta - An Organizational Second Brain]]
- [[Jina Yoon - We're Building Multiplayer AI]]
- [[Schema-Driven Knowledge Base]]
- [[Persistent Wiki]]
- [[Index and Log]]
- [[Ingest Query Lint Loop]]
- [[Retrieval-Augmented Generation]]
- [[Agent Memory]]
- [[Continual Learning for Agents]]
- [[Recursive Self-Improvement]]
- [[LLM-as-a-Judge]]
- [[Context Engineering]]
- [[Agent Skill]]
- [[Andrej Karpathy]]
- [[Meta]]
- [[Agent Workflow Maturity]]
- [[Multi-Tenant Agent Architecture]]
- [[AI Agents in Production]]
