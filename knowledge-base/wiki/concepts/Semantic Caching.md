---
type: concept
created: 2026-10-23
updated: 2026-11-27
tags:
  - concept
  - inference
  - caching
  - llm-applications
source_ids:
  - src-2026-10-21-bytebytego-prompt-vs-semantic-caching
  - src-2026-07-06-sarthak-rastogi-production-agent
  - src-2026-10-20-cloudflare-inference-bill
  - src-2026-11-14-intelligentlearn-inference-systems-part-2
  - src-2026-11-19-intelligentlearn-inference-systems-part-3
  - src-2026-11-24-intelligentlearn-inference-systems-part-4
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

## An aggregate prompt-cache hit rate can hide a first request that mostly misses

[[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]] concerns exact
prefix caching, the *prompt caching* column of the table above, not semantic caching, but it gives this
page its first production measurement of either. [[Cloudflare]]'s internal AI code reviewer reached a
**97%** cache hit rate by September, yet in data logged from 14 September, before the fix, the first
request of a session found a cached prefix only **14% to 26%** of the time, although **11k to 21k**
tokens of tool definitions and agent prompt were identical in every repository. The post does not say
how the rate is computed, but its figures suggest how both can hold: each call resends the whole
conversation, and the code quality reviewer averaged **16.6** calls per review, writing **72k** tokens to
the cache and reading back **1.08m**. If the rate counts every call, the first call, which pays for the
write, could mostly miss while the rate stayed high. Before the cost work began, cache writes were
**43%** of all AI review spend.

The provider prices match the ratios [[ByteByteGo - LLM Prompt Caching Versus Semantic Caching]] quotes:
writes at 1.25 times the normal input price, reads at 0.1 times, and expiry after five minutes without a
read. The new source adds a condition to *stable content must precede variable content*: "A prefix is
only stored where a cache breakpoint ends it." OpenCode v1 put the agent prompt, working directory, and
date in one block with its only breakpoint at the end, so "The shared part was never stored on its own".
Hashing the first system block as sent exposed this; once a marker and plugin hook split the block,
first-request cache reads rose to **91–99.5%**.

The fix had costs. The skills list was disabled and tool descriptions frozen between jobs. When three
reviewers share one first request, the other two wait up to **20 seconds**, because "A cache entry can't
be read until the response that wrote it has started streaming", to save about nine cents each. No cache
hit here can return a wrong answer, so this page's claim that prompt caching has essentially no
correctness surface stands, but a disabled skills list changes what the agent is told, a behavioral cost
the source does not measure.

The evidence is one company's self-reported telemetry. The fix shipped alongside a second change, and
"Together these took the cost per review from $2.47 down to $2.02", so its own share is not isolated.

## Inside the serving cluster, a prefix hit is worth the execution it saves minus the wait it adds

The intelligentLearn series looks at the prompt-caching column of the table above from the serving
side rather than the API side. [[intelligentLearn - Designing LLM Inference Systems, Part 2 - Six Layers to Investigate]] argues that once replicas hold different reusable prefixes,
they stop being interchangeable. That holds even without disaggregation. Routing then has to weigh
the benefit of reuse against queueing, migration, or recomputation. The papers it reads show how far
hit-rate evidence goes:

- **SGLang** keeps finished requests' KV in a radix tree and orders its queue longest-shared-prefix
  first. That ordering reaches **96%** of the optimal hit rate, and the paper reports **74.1%** over a
  month of production traffic. Both results come from ordering inside one engine's queue, with one
  worker per model. Extending them to routing across replicas is the author's own extrapolation, and
  the paper concedes the ordering can starve requests.
- **DualMap** says affinity "often conflicts with load-balancing scheduling" and measured the
  trade-off. Even so, its Conversation workload reaches only **62.5%** of the upper-bound hit rate.

The rule that follows is "a comparison, not a threshold". If reuse is high and load is even,
affinity is "almost free money". If reuse is high and load is spiky, joint affinity and balance
scheduling is mandatory. [[intelligentLearn - Designing LLM Inference Systems, Part 4 - Putting It to Work]] works an illustrative, unmeasured example. A hit saves **1.8 s**,
the hot replica adds **0.6 s** of queueing, and transfer adds **0.2 s**, for a net **1.0 s**. Once
queueing plus transfer exceeds the saved execution, the better choice is the less-loaded replica. Its
measurement plan starts with the cold- and hot-prefix and reusable-length distributions, since they
decide whether affinity is worth anything.

This is the same shape as the Cloudflare section above, in the vault's only production prompt-cache
measurement. There, two reviewers wait up to **20 seconds** for a shared cache write in order to save
about nine cents each. A cache benefit is net of the waiting it induces, whether the wait is a
scheduler queue or a write that must start streaming. [[intelligentLearn - Designing LLM Inference Systems, Part 3 - How to Evaluate a Change]] also generalises the Cloudflare warning
about aggregate hit rates. Hit rate "is evidence about reuse, not the end-to-end result", and a
caching change counts only if P95 TTFT, the P95 token gap, SLO attainment, and goodput improve for
the target traffic. None of this changes the correctness asymmetry on this page. The series discusses
exact-prefix KV reuse only, and its trade-offs are latency trade-offs. Part 4 also lists
cross-request reuse *policies* for prefix caching among the families it does not develop.

## Open questions

- **The vault has no semantic-cache measurements.** Every figure in the source is illustrative or
  third-party pricing: the 0.92 similarity score, the 30-day-to-14-day policy example, the
  $1.35-versus-$2 prefix arithmetic, and the quoted provider ratios (cache reads at 1/10th of input
  price; 5-minute writes at 1.25×, 1-hour writes at 2×). No hit rates, latency deltas, or error rates are
  reported. [[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]] now
  supplies production prompt-cache figures, aggregate and first-request hit rates and the share of spend
  on cache writes, but the semantic-cache side still has none.
- The source **proposes** measuring reused input tokens, accepted semantic-cache answers, freshness,
  scope, and answer appropriateness — and supplies no results. That evaluation harness is the missing
  piece, and it is the same gap [[Embedded Evaluation]] describes elsewhere.
- Semantic-cache **misses are not free**: embedding, lookup, and storage overhead is paid before the
  model call. At what hit rate does the mechanism become net positive? Rastogi treats the overhead as
  large enough to isolate in its own process but reports no hit rate or break-even figure.
- Who owns the threshold? It is application-specific, affects correctness, and has no principled
  derivation in the vault.
- How much execution does a prefix hit save at a given reusable length, and how does that compare with measured hot-replica queueing? The intelligentLearn 1.8 s / 0.6 s / 0.2 s example is illustrative arithmetic, and the vault has no measured break-even for cache-affinity routing.

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
- [[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]]
- [[Cloudflare]]
- [[Context Engineering]]
- [[Anthropic]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 2 - Six Layers to Investigate]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 3 - How to Evaluate a Change]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 4 - Putting It to Work]]
- [[intelligentLearn]]
