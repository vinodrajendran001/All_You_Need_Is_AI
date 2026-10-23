---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-21-bytebytego-prompt-vs-semantic-caching
source_title: LLM Prompt Caching Versus Semantic Caching
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/llm-prompt-caching-versus-semantic
tags:
  - source/summary
  - caching
  - inference
  - system-design
source_ids:
  - src-2026-10-21-bytebytego-prompt-vs-semantic-caching
status: active
---

# ByteByteGo - LLM Prompt Caching Versus Semantic Caching

## Summary

A system-design explainer separating two things often described with the same word. **Prompt caching**
reuses intermediate model computation for an **exactly matching input prefix** and still calls the
model. **Semantic caching** reuses a **previously generated answer** for a sufficiently similar request
and can skip the model entirely.

The useful distinction is where correctness risk lives: prompt caching changes cost and prefill work
without changing the answer, while semantic caching changes **which answer is returned**.

## Key claims

### Prompt caching

- Mechanism: tokenize and prefill, store **KV states** for the shared prefix, and on a later request
  with an identical prefix reuse those states, prefilling only the new suffix and generating a fresh
  answer.
- Matching is **positional and exact**. Wording, document order, request settings, timestamps, and
  request IDs must all be unchanged, so stable content should be placed **before** the variable question.
- Prompt caching **does not reduce output-generation cost**, only input prefill.
- A changed prefix cannot reuse the portion after the change, though an unchanged earlier prefix may
  still be reusable.
- The cache cannot tell that an unchanged old policy is **semantically obsolete** — the application must
  supply current content.
- **[Provider pricing, as described]** Anthropic standard prompt-cache reads are **one tenth** of
  ordinary input pricing; a **5-minute** cache write costs **1.25x** ordinary input pricing and a
  **1-hour** write costs **2x**.
- **[Illustrative]** A prefix normally costing **$1** becomes **$1.25** to write plus **$0.10** to read,
  for **$1.35** instead of **$2** across two uses.

### Semantic caching

- Mechanism: embed the incoming question, search stored question embeddings by similarity, apply a
  threshold and metadata filters, validate the candidate for the current context, and return it on a
  hit — otherwise call the model and optionally store the result.
- **Similarity is not probability of correctness.** The article uses a score of **0.92** and states
  explicitly that this does not mean a **92%** chance the answer is right.
- There is **no universal threshold**. Strict thresholds miss valid paraphrases; loose thresholds admit
  unsuitable hits.
- Metadata filters may have to encode customer, organization, permissions, product version, language,
  conversation state, location, date, units, and source-data version — because the question text alone
  underdetermines the right answer.
- Invalidation options: **TTL**, which bounds staleness but cannot guarantee freshness before expiry;
  **versioning**, where a cached answer tied to `policy_version=12` becomes ineligible at version 13;
  and **selective document-level invalidation**, which is more efficient but requires dependency
  tracking. Changes to system instructions, output formats, or behavior guidelines should also
  invalidate affected answers.
- **[Illustrative]** A return policy changing from **30 days** to **14 days** is the canonical staleness
  failure; "before shipping" versus "after shipping" is the canonical scope failure.
- **Action requests must not be satisfied by cached text.** The underlying action still has to happen.
- Semantic caching is unsuitable for highly personalized answers, rapidly changing facts, and fresh
  creative output. Misses still pay embedding, lookup, and storage overhead before the model call.

### Combining them

- Suggested layering: exact-answer cache → semantic cache → model, with prompt caching reducing cost for
  requests that still reach the model. Current-source validation may need to run **before** any lookup.
- **[Proposal]** Recommended instrumentation: reused input tokens, accepted semantic-cache answers,
  freshness, scope correctness, and answer appropriateness. No results are supplied.

## Why it matters

[[KV Cache]] in this vault is largely a memory-and-throughput topic. This source connects it to the
**application** layer: prompt caching is KV reuse exposed as a pricing and prompt-ordering decision, and
the "stable content first" rule is a direct consequence of positional prefix matching rather than a
style preference.

More importantly it gives [[Semantic Caching]] a crisp boundary against retrieval. A semantic cache and
a [[Retrieval-Augmented Generation]] index both do embedding search, but the cache returns a **prior
answer** as the final output, which makes staleness and scope errors user-visible rather than
recoverable by the model.

## Tensions / open questions

- **No measured hit rates, latency reductions, token savings, or cost reductions.** Every figure is
  either provider pricing or an invented example.
- Anthropic's pricing ratios are not universal provider rules, and exact-prefix matching details vary by
  provider; the article presents a general model.
- No embedding model, vector database, distance metric, threshold-selection method, or verifier
  architecture is specified, so the semantic-cache design is a sketch rather than a recipe.
- The article opens with a disclaimer that it is based on publicly shared details and may contain
  inaccuracies.
- A repeated prompt does **not** guarantee a prompt-cache hit, and a cache hit is not evidence that an
  answer is currently correct or safe to act on.

## Affected pages

- [[Semantic Caching]]
- [[KV Cache]]
- [[ByteByteGo]]

## Raw capture

- [[LLM Prompt Caching Versus Semantic Caching]]

## Citations

- Raw capture: [[LLM Prompt Caching Versus Semantic Caching]]
- Canonical URL: <https://blog.bytebytego.com/p/llm-prompt-caching-versus-semantic>
- Published 2026-10-21; captured 2026-10-22.
- Anthropic prompt-cache pricing is quoted from the article; provider documentation was not consulted.

## Related pages

- [[Retrieval-Augmented Generation]]
- [[Approximate Nearest-Neighbor Search]]
- [[Embedding Model Selection]]
- [[LLM Inference]]
- [[Inference Efficiency Frontier]]
- [[Context Engineering]]
- [[LLM Application Resilience]]
- [[Anthropic]]
