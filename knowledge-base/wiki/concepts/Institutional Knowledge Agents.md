---
type: concept
created: 2026-09-04
updated: 2026-09-04
tags:
  - concept
  - agents
  - knowledge-management
  - evaluation
source_ids:
  - src-2026-09-02-meta-organizational-second-brain
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

## Related pages

- [[Meta - An Organizational Second Brain]]
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
