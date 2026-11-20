---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-17-bytebytego-instacart-query-understanding
source_title: "How Instacart Uses LLMs to Make People Buy More"
source_author: "ByteByteGo"
source_url: "https://blog.bytebytego.com/p/how-instacart-uses-llms-to-make-people"
tags:
  - source/summary
  - search
  - query-understanding
  - distillation
  - fine-tuning
  - inference-latency
source_ids:
  - src-2026-11-17-bytebytego-instacart-query-understanding
status: active
---

# ByteByteGo - How Instacart Uses LLMs for Query Understanding

## Summary

[[ByteByteGo]] explains how Instacart rebuilt **query understanding** (QU), the layer that turns a
grocery search string into a category, alternative queries, and structured tags before retrieval and
ranking. It is a **secondary account**. The disclaimer says the post is "based on publicly shared
details", and its only listed reference is the Instacart Tech Blog post "Building the Intent Engine".
All figures are Instacart's own, relayed without independent checking.

The old system was a set of separate models, among them a FastText category classifier and query
rewrites mined from user sessions. Each needed its own data, training, and deployment, and they could
read the same query inconsistently. Purchase signals were noisy labels: a user who searches "bread"
and buys bananas does not make bread a fruit query. Long-tail queries such as "2% reduced-fat
ultra-pasteurized chocolate milk" had little history at all. The new design combines three
techniques: context engineering through RAG over catalog and historical data, post-processing
guardrails that check outputs against the catalog, and fine-tuning smaller models on Instacart's own
examples.

Despite the title, the article reports **no purchase, basket, or revenue metric**. Its outcomes are
rewrite coverage and precision, scroll depth, complaints, and latency.

## Key claims

### Categories: history proposes, the LLM interprets, embeddings filter

The catalog is a hierarchy (for example Meat → Beef → Beef Ribs → Short Ribs). The old classifier
treated it as flat labels. In the new pipeline, the categories most associated with purchases after
a query become candidates. The LLM then re-ranks them using the query and Instacart context, mapping
"buttermilk" to Dairy → Milk → Buttermilk and "vegan roast" to Meat → Meat Alternatives. Finally, an
embedding guardrail discards any query/category pairing whose similarity "falls below a specific
threshold". The threshold value is not given.

### Rewrites: one prompt per relationship

Session-mined rewrites "covered only about 50% of the search traffic". A "general prompt" asking the
LLM to rewrite failed because it did not say what kind of alternative was useful; the article's
illustration is that "1% milk" might become "one percent milk". Instacart split rewriting into three
tasks, each with a dedicated prompt, examples, and reasoning guidance, followed by post-processing
checks and semantic filters:

- **synonym** rewrites, which keep the meaning;
- **broader** rewrites, which relax constraints ("milk" for "1% milk");
- **substitute** rewrites, which change the product ("2% milk").

This "increased rewrite coverage to over 95%, with more than 90% precision across all three types."

### Tags: an offline teacher fills the cache and the training set

Semantic role labeling (SRL) extracts product, brand, and attributes ("2% chocolate milk" → product
milk plus fat content and flavour). The tags feed retrieval, ranking, advertising, and filters.

- **Head queries** are tagged ahead of time by an offline **teacher** pipeline. It retrieves internal
  context, asks a large model for tags, and validates them against the catalog. Without that context,
  "verdant machine" reads like machinery, but Instacart's evidence links it to the smoothie brand
  MuchPure.
- Validated outputs serve two purposes: they **populate the cache** and they become **training data**.
- On a cache miss, a **student** (Llama-3 8B fine-tuned with LoRA) tags the query live. The article
  calls this "a form of knowledge distillation" and reports that "the student generated fewer
  incorrect tags. But it also missed slightly more correct tags." It does not say what the student
  was compared against, and gives no precision or recall figures.

### Latency and cost

| Step | Reported effect |
| --- | --- |
| Target | "low 100s of milliseconds" |
| Initial setup | "nearly 700 milliseconds on an A100 GPU" |
| Merge LoRA adapter into base weights | latency down "by about 30%" |
| Plus H100 upgrade | "able to achieve the 300-millisecond target" |
| FP8 quantization | "another 10%", but "recall declined slightly"; **not deployed** |
| Caching | "only 2% of queries required real-time model inference" (their estimate) |
| GPU autoscaling | fewer GPUs in quiet periods (no number) |

Instacart rejected the FP8 latency gain to protect recall. That is an explicit quality-over-speed
choice.

### Outcomes (A/B test of real-time SRL)

For tail queries: "a 6% reduction in average scroll depth", read as users finding items faster; "a
50% reduction in user complaints related to poor search results for tail queries, with only a marginal
latency increase". The system faced "millions of cold-start queries each week".

## Why it matters

This is a clear production example of three patterns the vault tracks separately. In
[[Semantic Recommendation Systems]], it shows the LLM working inside deterministic catalog
constraints, not replacing them. In [[Knowledge Distillation]], one validated teacher pass feeds
both the cache and the student's training set, and the student trades recall for fewer wrong tags.
In [[Parameter-Efficient Fine-Tuning]], merging the LoRA adapter is a serving-latency step, not only
a training convenience. The rewrite result also suggests that splitting one vague task into typed
sub-tasks, with per-type prompts and post-processing filters, made the LLM useful; the article does
not isolate the split's share.

## Tensions / open questions

- **Target versus achieved latency.** The target is "low 100s of milliseconds", yet the result is
  described as reaching "the 300-millisecond target". The article does not reconcile the two.
- **Conflict with the earlier vault summary.**
  [[ByteByteGo - Three LLM Search Architectures for Delivery Platforms]] states "For the bottom 2%
  of queries, scroll depth fell 6%". In this capture, 2% is the estimated share of queries that
  **need real-time inference**, and the 6% scroll-depth cut applies to "the tail queries", with no
  percentage given for their share of traffic. Both relay Instacart's "Building the Intent Engine"
  post (the earlier one also cites "Supercharging Discovery in Search with LLMs"), so one framing
  is likely a conflation. The original was not checked. The "under 300ms" and "50% to over 95%"
  figures agree across the two.
- The student comparison has no baseline named and no numbers, so the precision/recall trade cannot
  be sized.
- No business metric is reported, despite the title.

## Affected pages

- [[Semantic Recommendation Systems]]
- [[Knowledge Distillation]]
- [[Parameter-Efficient Fine-Tuning]]

## Raw capture

- [[knowledge-base/raw/sources/How Instacart Uses LLMs to Make People Buy More]]

## Citations

- Raw capture: ByteByteGo, "How Instacart Uses LLMs to Make People Buy More", published 2026-11-17
  (source ID date). The canonical URL drops the email tracking parameters.
- Underlying primary source as listed by ByteByteGo: Instacart Tech Blog, "Building the Intent Engine"
  (not read during ingest).
- The summary title is descriptive, because the article's content is query understanding. The exact
  title is kept in `source_title`.
- A sponsor block (WorkOS) was excluded.

## Related pages

- [[ByteByteGo]]
- [[ByteByteGo - Three LLM Search Architectures for Delivery Platforms]]
- [[Semantic Recommendation Systems]]
- [[Knowledge Distillation]]
- [[Parameter-Efficient Fine-Tuning]]
- [[Retrieval-Augmented Generation]]
- [[ML Systems at Scale]]
