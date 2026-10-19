---
type: source-summary
created: 2026-08-03
updated: 2026-10-19
source_id: src-2026-07-28-bytebytego-delivery-llm-search
source_title: "Why DoorDash, Instacart, and Uber Eats Integrated LLMs Into Search Three Different Ways"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/why-doordash-instacart-and-uber-eats
tags: [source/summary, search, retrieval, production]
source_ids: [src-2026-07-28-bytebytego-delivery-llm-search]
status: active
---

# ByteByteGo - Three LLM Search Architectures for Delivery Platforms

## Summary

A ByteByteGo explainer comparing how DoorDash, Instacart, and Uber Eats added LLMs to food-delivery
search. Its organizing question is how deeply the model reaches into the runtime. DoorDash keeps the
runtime mostly classical: LLMs enrich a knowledge graph offline and, online, only parse queries into
taxonomy-constrained chunks. Instacart puts LLMs at the query-understanding layer, with an offline
RAG-and-cache path for head queries and a real-time fine-tuned Llama-3-8B for the tail. Uber Eats
makes a fine-tuned Qwen the embedding backbone of two-tower ANN retrieval for every query and
document.

Its central claim is that each company's position was set by the infrastructure it already had, not
by the model. This is a secondary synthesis of the companies' public posts; the figures below are
company-reported results it relays, and its sponsored sections are excluded.

## Key claims

### Food search stacks several failure modes

- Synonyms, typos, shorthand, mixed languages, and word-sense ambiguity break keyword matching.
  Beneath them sit a long tail of rare queries and hard constraints, as in "vegan chicken sandwich,"
  that similarity retrieval can violate because the score still looks close.

### Three integration depths

| Company | Where the LLM sits | Reported results |
| --- | --- | --- |
| DoorDash | Offline attribute extraction into an existing knowledge graph. At runtime the LLM segments a query into chunks linked to graph fields: dietary preference becomes a hard filter, flavor a soft ranking preference. For each segment, ANN retrieves the **top 100** closest taxonomy concepts and the LLM must pick from that list, so RAG defines the output space instead of feeding a generator. | Roughly **30%** lift in the trigger rate for popular dish carousels. |
| Instacart | Replaces separate FastText classification, session-mined rewrites, spell correction, tagging, and aisle models. RAG supplies top-converted categories, conversion history, and catalog details; semantic-similarity filters drop drifting outputs; **Llama-3-8B** is fine-tuned for the hardest tasks. Head queries use an offline RAG-and-cache pipeline; tail queries hit the real-time model, kept **under 300ms** through adapter merging, H100 GPUs, and autoscaling. | Rewrite coverage from **50% to over 95%**, with **90%+** precision. For the bottom **2%** of queries, scroll depth fell **6%** and tail-query complaints halved. |
| Uber Eats | Replaces per-vertical BERT embedding models with one two-tower system whose towers use a fine-tuned **Qwen** backbone. Queries are embedded online; billions of documents are pre-embedded offline into an HNSW index; pre-filters on hexagon, city, and fulfillment type shrink candidates. | Matryoshka embeddings served at **256** dimensions with **under 0.3%** recall loss versus the full **1,536**. Tuning ANN k cut latency **34%** and CPU **17%** with negligible recall impact; int7 scalar quantization halved latency at recall **above 0.95**; MRL cut storage by **nearly 50%**. |

- Instacart's motivating failure: an off-the-shelf model mapped "protein" to chicken, tofu, and beef,
  while its users mean protein bars and powders.
- Three tradeoffs survive every design. Hybrid systems are the default. Pretrained knowledge still
  needs domain context through RAG, fine-tuning, or both. Guardrails such as constrained vocabularies,
  similarity filters, and taxonomy enforcement keep outputs aligned with the catalog.

## Why it matters

[[Semantic Recommendation Systems]] uses the three cases as a control on LLM enthusiasm. The durable
pattern is **LLM augmentation under product constraints**: no company replaced retrieval and ranking
wholesale. The article explains the differences by existing infrastructure; traffic shape, latency
budget, and data assets are the vault's broader reading. DoorDash's retrieve-the-legal-labels step is
a reusable guardrail for [[Retrieval-Augmented Generation]]. Instacart's head/tail split pays for
precomputation only where queries repeat. Uber Eats shows, for [[Embedding Model Selection]] and
[[Approximate Nearest-Neighbor Search]], that truncation, quantization, and pre-filtering make an
LLM-sized embedding servable.

## Tensions / open questions

- The infrastructure-determines-depth thesis is an after-the-fact reading of three cases. The article
  offers no counterexample, such as a company that rebuilt its infrastructure to integrate deeper.
- The metrics sit on different axes, and nothing compares the architectures on a shared task or
  reports conversion or revenue effects. Several figures also lack baselines or definitions: what
  the 30% lift is measured against, how the 90%+ precision was judged, and where the latency and CPU
  reductions start from.
- The storage figure does not follow from the dimensions alone. Truncating 1,536 to 256 dimensions
  would by itself shrink each vector by about five-sixths, yet the article reports MRL cutting storage
  by "nearly 50%" without stating the baseline. This arithmetic is the vault's.
- Aggregate recall says little about hard constraints; beyond the pre-filters, the article does not
  report how dietary or allergen constraints fare in the embedding path.

## Affected pages

- [[Semantic Recommendation Systems]]

## Raw capture

- [[2026-07-29 ByteByteGo - Why DoorDash, Instacart, and Uber Eats Integrated LLMs Into Search Three Different Ways|Why DoorDash, Instacart, and Uber Eats Integrated LLMs Into Search Three Different Ways]]

## Citations

- Canonical article: <https://blog.bytebytego.com/p/why-doordash-instacart-and-uber-eats>
- Published July 28, 2026; captured July 29, 2026.
- The article's references are Uber's delivery-search engineering post and an arXiv paper on
  multilingual semantic search in Uber Eats, two DoorDash engineering posts, and two Instacart
  posts. None was read separately for this summary.

## Related pages

- [[Semantic Recommendation Systems]]
- [[Retrieval-Augmented Generation]]
- [[Embedding Model Selection]]
- [[Approximate Nearest-Neighbor Search]]
- [[Parameter-Efficient Fine-Tuning]]
- [[ML Systems at Scale]]
- [[Model Routing]]
- [[DoorDash]]
- [[DoorDash - LLM-as-a-Judge for Search Evaluation]]
- [[ByteByteGo]]
