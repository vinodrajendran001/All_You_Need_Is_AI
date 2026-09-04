---
type: source-summary
created: 2026-09-04
updated: 2026-09-04
source_id: src-2026-09-02-meta-organizational-second-brain
source_title: "An Organizational Second Brain: Building an AI That Learns From Experts"
source_author: Meta Engineering
source_url: https://engineering.fb.com/2026/09/02/ml-applications/organizational-second-brain-ai-learns-from-experts/
tags:
  - source/summary
  - topic/knowledge-systems
  - topic/agents
  - topic/evaluation
source_ids:
  - src-2026-09-02-meta-organizational-second-brain
status: active
---

# Meta - An Organizational Second Brain

## Summary

Meta's engineering write-up of a domain-expert agent built for an internal compliance domain, and the strongest
external validation this vault has of its own architecture. The system has two layers the post considers novel in
combination: a **structured, auditable knowledge architecture** that separates what the agent knows from how it
reasons, and a **self-improvement loop that compiles expert feedback into verified, regression-tested updates
without model retraining**.

The stated goal is to convert one-off expert corrections into "permanent, compounding institutional memory." The
problem it addresses is that the most valuable specialist knowledge "lives in people's heads and rarely gets
captured anywhere durable," so experts "spend more time answering routine questions than on genuinely novel and
ambiguous work where their judgment matters most."

The post explicitly places itself alongside [[Andrej Karpathy]]'s LLM Wiki, which structures agent knowledge as a
navigable graph of files, and Google's Open Knowledge Format. It names the shared insight: **knowledge should be
pre-extracted, explicitly structured, and progressively disclosed rather than re-derived on every query.**

## Key claims

**Retrieval alone re-derives reasoning on every run.** Organizations accumulate thousands of documents as a
byproduct of expert work, "but the real knowledge is implicit: how experts reason, what they prioritize, and how
they resolve ambiguity." An agent that retrieves document chunks at inference time "has to re-derive that
reasoning from raw sources on every run, which is slow, error-prone, and inconsistent." Meta's answer is to make
the implicit knowledge explicit ahead of time, via a **long-running offline process** that reasons through source
documents and distils them into structured knowledge files.

**A four-part file taxonomy, 200+ files.** *Position files* capture authoritative organizational stances with
constraints, boundary conditions, and machine-actionable routing implications. *Taxonomy and vocabulary files*
act as a single-source-of-truth glossary. *Routing indexes* map input characteristics to relevant positions,
"determining which files apply without relying on embedding similarity alone," which makes retrieval
**deterministic and auditable**. *Gateway files* define threshold tests the agent must pass before entering an
analytical domain, "preventing it from applying specialized knowledge where it does not belong."

**Every file declares `depends_on` and `referenced_by` in YAML frontmatter**, forming a bidirectional dependency
graph. "When one file changes, you can trace exactly what else might be affected, which matters when the
self-improvement loop proposes automated edits."

**The wiki/RAG split is by information density and expected usage frequency**, not by topic. High-density,
frequently referenced material — positions, decision frameworks, boundary examples, strategic interpretations —
goes in the curated wiki, consulted "on nearly every turn." Sparse, situationally relevant material — detailed
reference documents, individual product specs, historical decision records, niche external knowledge — is served
through search, because "loading all of them into the wiki would bloat the system and dilute attention." The
result "encodes how the organization interprets and applies information, rather than only where to find it."

**Knowledge is declarative, procedure is imperative, and the separation is the point.** Composable procedures
called **recipes** prescribe multi-step analytical workflows: what to examine first, which knowledge to load at
each step, what decision procedures to follow, what constitutes a complete analysis. "Recipes reference knowledge
files but contain no domain facts; knowledge files state positions but prescribe no procedures." The payoff is
clean failure attribution: **"Was the knowledge wrong, or the procedure?"** Adding a position touches a knowledge
file and a routing index and no recipe; fixing a methodology flaw touches a recipe and no knowledge file.

**Progressive disclosure cut tokens per turn by around 80%.** Early versions "used a single flat instruction file
and loaded all sources via semantic search, pulling a large volume of mixed-relevance files into the context
window on every run." After restructuring into recipe-driven stages where each step carries only its own
instructions and knowledge, "each query touches only a small, targeted subset." The stated rationale: "Context
windows are finite and attention degrades with volume."

**Human control is structural, via checkpoints and escalations.** Checkpoints surface intermediate reasoning for
expert review before the agent proceeds. Escalations trigger on genuine ambiguity — underspecified inputs, or
evidence supporting more than one defensible reading — and hand the question to the expert rather than forcing a
resolution. These serve three purposes at once: quality control, **training signal for the improvement loop**,
and trust calibration, because "experts build confidence incrementally by observing the agent's reasoning rather
than just its final output, and by seeing it flag uncertainty instead of masking it."

**Maintenance is treated as a compilation problem.** The number of interdependent files "make manual maintenance
impossible to scale," and translating expert feedback into precise file edits "can take weeks because it requires
understanding the full dependency graph, verifying nothing else breaks, and validating the fix actually works."
Every correction moves through four phases: diagnose to root cause, compile into minimal verified edits, validate
without regressions, and expert review.

**Diagnosis by conversational form failed.** The first approach classified feedback by its shape — information
offered meant a knowledge gap, a redirect meant a procedure problem. This "failed because conversational form is
a poor proxy for root cause." The working approach separates extraction from classification and applies a single
attribution test: **"Could the agent have reached the correct conclusion from its source materials?"** If the
materials contained the right answer and the agent still erred, it is a recipe problem; if they did not, a
knowledge gap; if the experts themselves disagree, ambiguity flagged for human discussion.

**Two mechanisms make automated edits trustworthy.** *Independent adversarial review*: a separate agent in a
fresh context, with **no knowledge of the improvement rationale**, receives only the proposed diffs and looks for
contradictions introduced, edge cases broken, or positions undermined — "because it shares no context with the
proposing agents, it cannot inherit their blind spots." *Deterministic structural validation*: a linter catching
dangling cross-references, file-size budget violations, identifier collisions, and dependency cycles. "This layer
is not probabilistic. It passes or fails."

**Validation is deliberately blind.** *Targeted replay* runs the agent on the original scenario that triggered
the feedback; **the agent does not know it is being tested**, and a separate judge evaluates the new output
against the original expert feedback **without knowing what was changed** — "this deliberately blind design
prevents confirmation bias." *Regression testing* runs structured Q&A benchmark suites in parallel independent
sessions with an independent LLM judge. A failure at either stage retries compilation, the regression retry
carrying a prompt describing where the agent regressed.

**Every fix is folded back into the regression suite.** The pipeline's output is a pull request with a complete
audit trail, so "a human expert reviews a proven fix rather than debugging a raw failure." Once landed, the
original failing scenario and its validated correct answer are automatically added to the regression suite, so
"every fix permanently raises the bar."

**Reported results, after three development sprints spanning six weeks:** SMEs rated outputs "useful almost all
the time," a significant improvement on early versions; individual assessment time fell from **days to minutes**;
automated self-improvement produced validated knowledge edits "at a rate that previously required full
engineering sprints"; **zero regressions across improvement cycles**; and experts reported the agent handles "the
vast majority of the analytical work."

**The stated deeper principle:** "keep the complexity in text files that are readable by both humans and agents,
rather than fine-tuned model weights. Every improvement is a text edit that a domain expert can review in 30
seconds. Every change is version-controlled, diffable, and reversible."

## Why it matters

This is the closest thing to an industrial control group for this vault's own design. [[Schema-Driven Knowledge
Base]], [[Persistent Wiki]], and [[Ingest Query Lint Loop]] have each rested on a single source — Karpathy's LLM
Wiki — which made them the vault's least externally corroborated pages despite describing the vault itself. Meta
independently arrived at file-based structured knowledge, YAML dependency declarations, deterministic routing over
pure embedding similarity, progressive disclosure, and a linter that "passes or fails," and cites the same
Karpathy source as prior art. The convergence is the finding.

The differences matter more than the similarities. Meta has three mechanisms this vault does not: **regression
testing that grows with every fix**, **blind evaluation** where neither the agent nor the judge knows what
changed, and **independent adversarial review by an agent that cannot inherit the author's blind spots**. This
vault's lint pass is closest to Meta's deterministic linter, and the 2026-09-03 pass demonstrated the gap
precisely — a page cited as authority for material it did not contain passed every structural check, exactly the
class of defect a blind replay test would catch and a link checker cannot.

The **root-cause attribution test** is the single most portable idea here. "Could the agent have reached the
correct conclusion from its source materials?" cleanly separates a knowledge defect from a procedure defect, and
it applies to any system where retrieval and reasoning are separable layers — including this one.

## Tensions / open questions

- **The results are almost entirely qualitative.** "Useful almost all the time," "vast majority of the analytical
  work," and "days to minutes" have no denominators, no baselines, and no sample sizes. The only hard numbers in
  the post are 200+ files, ~80% token reduction, six weeks, and three sprints.
- **"Zero regressions across improvement cycles" is unfalsifiable as stated.** Regressions are defined by the
  suite, and the suite is grown from the fixes it has already seen. A regression in behaviour never tested cannot
  appear in that count.
- **The domain is never named.** It is described only as "a specific compliance domain," so the reader cannot
  judge how much of the success depends on a domain with authoritative, written, relatively stable positions.
  Meta claims domain independence but demonstrates one domain.
- **The offline distillation process is a large hidden cost.** A "long-running offline process" reasons through
  source documents to produce the knowledge files. Its cost, cadence, error rate, and what happens when source
  documents change are not discussed.
- **Adversarial review is itself a model.** The blind reviewer cannot inherit the proposing agents' context, but
  it can share their training priors. The post treats context isolation as sufficient for independence.
- **No comparison against the alternatives it dismisses.** RAG memory systems and model-weight knowledge editing
  are named as the prior body of work, but no head-to-head evaluation is offered — the claim is that this level of
  validation rigor has not been seen applied to a structured knowledge base, not that it outperforms.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Institutional Knowledge Agents]]
- [[Schema-Driven Knowledge Base]]
- [[Persistent Wiki]]
- [[Ingest Query Lint Loop]]
- [[Index and Log]]
- [[Retrieval-Augmented Generation]]
- [[Context Engineering]]
- [[Agent Memory]]
- [[Recursive Self-Improvement]]
- [[Continual Learning for Agents]]
- [[LLM-as-a-Judge]]
- [[Andrej Karpathy]]
- [[Meta]]

## Related pages

- [[Agentic Testing]]
- [[Multi-Turn Evaluation]]
- [[Agent Skill]]
- [[Direct Corpus Interaction]]
- [[Embedding Model Selection]]
- [[Graph Engineering]]
- [[Benchmark Optimization]]
- [[Agent Security and Governance]]

## Citations

- Raw capture: [[2026-09-02 Meta - An Organizational Second Brain]]
- Source: <https://engineering.fb.com/2026/09/02/ml-applications/organizational-second-brain-ai-learns-from-experts/>
