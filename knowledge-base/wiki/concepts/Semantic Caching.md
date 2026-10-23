---
type: concept
created: 2026-10-23
updated: 2026-10-23
tags:
  - concept
  - inference
  - caching
  - llm-applications
source_ids:
  - src-2026-10-21-bytebytego-prompt-vs-semantic-caching
  - src-2026-07-06-sarthak-rastogi-production-agent
status: active
---

# Semantic Caching

## Definition

**Semantic caching** reuses a previously generated answer for a request judged *meaningfully similar* to
an earlier one, matched by embedding similarity rather than by exact text. It sits one layer above
[[KV Cache]]-based **prompt caching**, which reuses intermediate model computation for an **exactly
matching input prefix**.

The difference that decides everything downstream:

| | Prompt caching | Semantic caching |
|---|---|---|
| Matches on | Exact token prefix, positionally | Embedding similarity + metadata filters |
| Saves | Prefill work on the shared prefix | Potentially the **entire model call** |
| Still calls the model | **Yes** — output is freshly generated | **No** on a hit |
| Correctness risk | Low: the answer is still generated | **High: a stale or mismatched answer is returned verbatim** |

## Why it matters

The asymmetry in that last row is the whole concept. Prompt caching is a **cost optimization with
essentially no correctness surface** — the model still generates the answer, so a cache hit cannot make
the output wrong. Semantic caching is an **answer-substitution mechanism**, and every hit is a decision
to serve text that was produced for a different request at a different time.

That moves it out of the performance domain and into the correctness domain, alongside
[[LLM Application Resilience]] and the evidence-handling concerns in
[[Retrieval-Augmented Generation]].

## Current synthesis

### The sentence worth keeping

**Similarity is not probability of correctness.** A score of 0.92 does not mean a 92% chance the cached
answer is right — the number describes geometric closeness of two embeddings under one model and one
distance measure, and nothing about whether the answer still applies. Threshold tuning trades **false
misses** (paraphrases rejected) against **unsuitable hits** (wrong answers served confidently).

### The question is rarely a sufficient key

The vault's source lists what else may have to enter the cache key or metadata filter before a hit is
legitimate: **customer, organization, permissions, product version, language, conversation state,
location, date, units, and source-data version**. Two users can ask a character-identical question and
require different answers.

This is the same scoping failure recorded in [[Multi-Tenant Agent Architecture]]: a cache key that omits
tenant identity converts a performance feature into a cross-account data leak.

### Freshness has no automatic answer

A **TTL** bounds how long an entry *may* be reused; it cannot guarantee the entry was still correct
before expiry. If a stated policy changes partway through a TTL window, the cache serves the old answer
with full confidence. **Versioning** entries against a policy or knowledge-base version is the stronger
mechanism, but whole-corpus versioning invalidates everything after a small change, while selective
document-level invalidation requires dependency tracking the application must build.

Changes to system instructions, output formats, or behaviour guidelines should also invalidate affected
answers — an invalidation trigger that is easy to forget because it lives in the prompt, not the data.

### Prompt caching's own constraints

Matching is **positional and exact**: wording, document order, request settings, timestamps, and request
IDs all break it, so stable content must precede variable content. A changed prefix cannot reuse the
incompatible portion, though an unchanged earlier prefix may remain reusable. Critically, **the cache
cannot discover that unchanged old content has become semantically obsolete** — supplying current
content is the application's job. Output generation cost is unaffected.

### The two compose

The architecture the source proposes: an exact-answer cache first, then semantic lookup, then the model
with prompt caching applied to whatever still reaches it. Validation against current sources may need to
happen **before** any cache lookup rather than after.

### Where it does not belong

Highly personalized answers, rapidly changing facts, and fresh creative output. And a hard rule worth
stating plainly: **an action request must never be satisfied by cached text alone** — returning a
cached confirmation without performing the action is a correctness failure that looks like a success.

### Where the lookup sits is an architectural decision, not a detail

[[Sarthak Rastogi - Making an AI Agent Production-Ready]] is the vault's only source that places a
semantic cache in a running system rather than describing one. Two placement decisions there are worth
keeping, and both are reasoned rather than measured.

The cache check runs **outside** the agent graph, before the framework is invoked at all. The stated
reason is that invoking the graph is not free — it compiles the graph, sets up the checkpointer, and
initializes state — so a hit should be "a pure lookup-and-return before any framework machinery touches
the request." The general rule the source draws from this is that **things that prevent work go before
the graph, and things that are work go inside it**. A semantic cache placed inside the loop still pays
most of the cost it exists to avoid.

Second, the cache runs as a **separate process with its own HTTP API**, because the cache's own
embedding model is compute-heavy and should not share the main application's process. That is a partial
answer to this page's question about miss cost: the overhead is real enough that the source isolates it,
though it reports no hit rates, latencies, or break-even point.

The source uses GPTCache and frames semantic caching primarily as a **cost lever** against users asking
the same question in different words — "My iPhone won't turn on" and "iPhone not powering up" are its
example pair. It is a code-first tutorial, so these are design recommendations from one practitioner's
reference architecture, not results.

## Open questions

- **The vault has no measurements here.** Every figure in the source is illustrative or third-party
  pricing: the 0.92 similarity score, the 30-day-to-14-day policy example, the $1.35-versus-$2 prefix
  arithmetic, and the quoted provider ratios (cache reads at 1/10th of input price; 5-minute writes at
  1.25×, 1-hour writes at 2×). No hit rates, latency deltas, or error rates are reported.
- The source **proposes** measuring reused input tokens, accepted semantic-cache answers, freshness,
  scope, and answer appropriateness — and supplies no results. That evaluation harness is the missing
  piece, and it is the same gap [[Embedded Evaluation]] describes elsewhere.
- Semantic-cache **misses are not free**: embedding, lookup, and storage overhead is paid before the
  model call. At what hit rate does the mechanism become net positive? Rastogi treats the overhead as
  large enough to isolate in its own process but reports no hit rate or break-even figure.
- Who owns the threshold? It is application-specific, affects correctness, and has no principled
  derivation in the vault.

## Related pages

- [[KV Cache]]
- [[LLM Inference]]
- [[Retrieval-Augmented Generation]]
- [[Approximate Nearest-Neighbor Search]]
- [[Embedding Model Selection]]
- [[Multi-Tenant Agent Architecture]]
- [[LLM Application Resilience]]
- [[Embedded Evaluation]]
- [[Inference Efficiency Frontier]]
- [[ByteByteGo]]
- [[ByteByteGo - LLM Prompt Caching Versus Semantic Caching]]
- [[Sarthak Rastogi - Making an AI Agent Production-Ready]]
- [[AI Agents in Production]]
