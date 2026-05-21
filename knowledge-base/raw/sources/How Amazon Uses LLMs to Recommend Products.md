---
type: raw-source
source_id: src-2026-05-21-bytebytego-amazon-llm-recommendations
title: "How Amazon Uses LLMs to Recommend Products"
source: "https://blog.bytebytego.com/p/how-amazon-uses-llms-to-recommend"
author:
  - "[[ByteByteGo]]"
published: 2026-04-27
created: 2026-05-21
description: "In this article, we will look at how COSMO works and the challenges the engineering team faced."
tags:
  - "clippings"
---
## Your agent isn’t broken. Your context is. (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!eoOP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F56565ea9-5fa6-4e59-b88b-92f5c3adbfda_1080x1080.png)

Most AI agents don’t fail because the model is bad. They fail because the model doesn’t have the proper infrastructure to reason well.

Simba Khadder, Head of Engineering at Redis, lays out a 4 pillar framework for building context systems that hold up in production—plus an architectural self-audit checklist you can run against your stack today.

---

Search “shoes for pregnant women” on Amazon, and the best results you get might be slip-resistant shoes. This is even though the word “pregnant” appears nowhere in those product listings.

In other words, there is zero keyword overlap between the query and the product. The search engine has to reason that pregnant women need stability, that stability means slip-resistance, and that slip-resistant shoes are the right match.

Traditional recommendation systems match text to text and purchase history to purchase history. They handle keyword overlap quite well. However, when a shopper’s intent requires a reasoning step that lives entirely in human common sense, those systems hit a wall.

Amazon’s search team recognized this blind spot and built a commonsense knowledge graph called COSMO that teaches the recommendation engine to think the way a human shopper would.

In this article, we will look at how COSMO works and the challenges the engineering team faced.

*Disclaimer: This post is based on publicly shared details from the Amazon Engineering Team. Please comment if you notice any inaccuracies.*

## The Gap Between What You Search and What You Mean

Amazon already operates large-scale knowledge graphs that store factual product attributes like brand, color, material, and category. These graphs power a lot of what works well in product search today. However, they mainly try to encode what a product is, and they don’t explain why a human would want it.

This is the semantic gap problem.

For example, a query like “winter clothes” carries an implicit intent around warmth. The product catalog for a long-sleeve puffer coat describes its material, size options, and sleeve length, but it may say nothing about warmth directly. The gap between what the customer typed and what the product listing says requires a reasoning step that factual knowledge graphs were never designed to handle.

![](https://substackcdn.com/image/fetch/$s_!Lo39!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdcb35d78-403f-4ad8-9344-0edb1531cdfd_1890x1124.png)

Amazon’s team surveyed the landscape of existing solutions.

- Alibaba built AliCoCo (163K nodes, 91 relations) and AliCG (5M nodes), both extracted from search logs. These capture product concepts, but they stay focused on product attributes and categories, skipping user intent entirely.
- General commonsense knowledge bases like ConceptNet (8M nodes, 21M edges) cover everyday reasoning but are built for general purposes, with little grounding in shopping behavior.
- Amazon’s own earlier effort, FolkScope, demonstrated that commonsense knowledge could be extracted from shopping data, but it covered only 2 product categories and only co-purchase behavior.

The gap was clear. Though factual product knowledge and general commonsense knowledge existed, structured knowledge about why people buy things at an e-commerce scale was missing.

## Asking the LLM (and Why the Answers Fell Short)

The intuition behind Amazon’s approach was simple. Large language models encode enormous amounts of world knowledge in their parameters. Taking our earlier example, if you ask an LLM why a customer who searched “winter coat” bought a long-sleeve puffer coat, it can reason that puffer coats provide warmth, and warmth is what the customer wanted.

The team fed millions of user behavior pairs into OPT-175B and OPT-30B, large language models hosted internally on 16 A100 GPUs. The choice of OPT over GPT-4 was driven by a hard constraint around data privacy. Customer behavior data, meaning which queries led to which purchases, could only be processed on Amazon’s own infrastructure.

Two types of behavior data went into the system.

- Query-purchase pairs capture the connection between a search query and the product a customer ultimately bought.
- Co-purchase pairs capture products bought together in the same shopping session

Across 18 product categories, the team sampled 3.14 million co-purchase pairs and 1.87 million query-purchase pairs.

The sampling strategy was itself a design decision.

- For products, Amazon covered popular browse node categories and selected top-tier products with high interaction volume, also using product type labels (more than a thousand classes like “umbrella” or “chair”) for finer-grained selection.
- For co-purchase pairs, the team cross-checked product types to remove random co-purchases and filtered out products that co-occurred with too many different product types (a signal of noise rather than intent).
- For search-buy pairs, thresholds on both purchase rate and click rate determined which queries and products entered the sample.

Crucially, an in-house query specificity service helped prioritize broad or ambiguous queries, because those are exactly where the semantic gap is largest and commonsense knowledge adds the most value.

Prompt design mattered too. Rather than using simple text continuation, Amazon formatted each behavior pair as a question-answering task and instructed the LLM to generate a numbered list of candidates rather than a single response.

The LLM generated millions of candidate explanations. However, only 35% of search-buy explanations met Amazon’s quality bar for typicality, meaning they were representative of genuine shopping intent. For co-purchase explanations, that number dropped to 9%. The rest were filler. The LLM produced circular rationales like “customers bought them together because they like them,” or trivially obvious statements like “customers bought an Apple Watch because it is a type of watch.”

The 9% vs. 35% gap reveals something about how LLMs reason. Explaining why a query led to a purchase is relatively constrained because the query provides clear context about intent. But explaining why two products were bought together requires identifying a shared reason across two different items, and LLMs tend to default to generic explanations for one item rather than reasoning about the pair.

Amazon also needed a way to categorize the relationships that the LLM was generating. The team started with 4 broad seed relations (usedFor, capableOf, isA, cause) that prior work had shown produce diverse outputs. From there, they mined finer-grained relation types directly from the LLM’s generated text by looking for recurring predicate patterns.

The most common pattern was “the product is capable of being used \[preposition\],” where different prepositions mapped to different semantic relationships. This data-driven process produced 15 relation types that capture distinct ways humans reason about products. These include used\_for\_function (”dry face”), used\_for\_event (”walk the dog”), used\_for\_audience (”daycare worker”), used\_in\_location (”bedroom”), used\_in\_body (”sensitive skin”), used\_with (complementary products like “surface cover”), and person-centric relations like xIs\_a (”pregnant women”) and xWant (”play tennis”). The ontology was shaped by what the LLM actually generated, then canonicalized and structured by Amazon’s researchers, rather than being designed top-down by a team of knowledge engineers.

## Building the Filter

The LLM produced a mountain of hypotheses, which were mostly noise. Amazon’s solution was a multi-stage refinement pipeline, where each stage catches a different type of failure.

![](https://substackcdn.com/image/fetch/$s_!yXb1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2cdd67aa-e0f7-4eb4-8f11-d9fda5c6d4fe_2086x2226.png)

Coarse-grained filtering tackled the most obvious problems first. Rule-based filters removed incomplete sentences by measuring sentence quality with a language model (GPT-2) and tuning a threshold. Generations that exactly matched the query text, the product type, or the product title (or fell within a small edit distance) were discarded. For generic statements like “used for the same reason” or “used with clothes,” Amazon identified these by combining frequency and entropy, since generic explanations tend to co-occur with many different products rather than specific ones.

Similarity filtering handled a subtler problem. Some LLM outputs looked different from the input on the surface but were semantically just paraphrases of the original query or product description.

Amazon used an in-house language model, pre-trained on e-commerce text including queries and product information, to compute embeddings for the generated knowledge, the query, and the product. When the vector similarity (measured by cosine distance) between the generated knowledge and the original context was too high, the candidate was filtered out. The team found that filtered generations were essentially syntactic transformations of the original input, rearranging the same meaning in slightly different words.

Human-in-the-loop annotation came next. Amazon sampled 30,000 knowledge candidates for human review, with 15,000 from co-purchase behavior and 15,000 from search-buy behavior spread across 18 categories. Rather than picking candidates uniformly, the team used a weighted formula that combined the frequency of a piece of generated knowledge with the popularity of the associated product or query. Popular products produce common knowledge, so the weighting pushed toward diverse, less obvious knowledge that the classifier would later need to generalize.

Annotators evaluated each candidate on two dimensions:

- Plausibility measures whether the posited relationship is reasonable.
- Typicality measures whether the knowledge is representative of genuine shopping behavior.

As a concrete example, the more typical reason people buy Apple Watches is that they are intelligent watches, rather than that they tell the time. Both statements are plausible, but only the first is typical.

To reduce cognitive burden and disagreement among annotators, Amazon decomposed these assessments into five yes/no questions covering completeness, relevance, informativeness, plausibility, and typicality. Two annotators labeled each question independently, with a third resolving disagreements. A pilot study of 2,000 examples showed this decomposition significantly reduced the disagreement rate, and internal auditing of 5% of all annotations showed over 90% accuracy. Due to data privacy requirements, Amazon employed a professional data annotation vendor company, followed by a strict internal auditing process.

Classifier generalization was the final step. Amazon fine-tuned DeBERTa-large (a high-performing language model for classification tasks) and an in-house language model on the 30,000 annotated samples to predict plausibility and typicality scores for all remaining candidates. Only candidates scoring above a 0.5 plausibility threshold survived.

The output of this pipeline is a set of structured knowledge triples. A triple connects two entities through a defined relationship. For example, the triple <co-purchase of camera case and screen protector, capableOf, protecting camera> captures the commonsense reasoning that these two products are bought together because they both serve the purpose of protecting a camera. Assembled, these triples form a knowledge graph of 6.3 million nodes and 29 million edges spanning 18 product categories. From 30,000 human judgments to 29 million edges.

## COSMO-LM, the Smaller Model

The knowledge graph captures pre-computed commonsense relationships, but Amazon’s search engine encounters new queries and products constantly. Running the full pipeline (OPT-175B generation followed by classifier scoring) for every new behavior pair would be prohibitively expensive in production.

Amazon’s solution was instruction tuning.

The team used their 30,000 annotated samples to create instruction data and fine-tuned LLaMA 7B and 13B models. These base models offered the best balance between generation quality and inference cost for production serving, with far fewer parameters than OPT-175B while still producing high-quality outputs when trained on domain-specific data. The resulting model, COSMO-LM, was trained across 18 product domains, 15 relation types, and 5 distinct tasks.

Beyond commonsense generation, those tasks included plausibility prediction, typicality prediction, search relevance prediction, and co-purchase prediction. The multi-task training means COSMO-LM can both generate knowledge and evaluate its own output quality, effectively collapsing the “big LLM plus classifier” stack into a single, smaller model.

To make the model robust to different input formats, Amazon varied the templates during training. The same query-product pair might be prefixed with “search query,” “user input,” or “user searched” across different training examples. This prevents COSMO-LM from becoming brittle to prompt phrasing.

The result is two complementary artifacts in production. The static knowledge graph (29 million pre-computed edges) handles known product relationships. COSMO-LM generates fresh commonsense knowledge on the fly for new or unseen query-product pairs, with dramatically lower inference cost than the original OPT-175B pipeline. A demo of the system shows COSMO-LM generating knowledge for a query like “how to decorate a home,” producing a list of product types (wall art, decorative signage, sticker decal, decorative pillow cover, artificial plant, rug, home mirror, lamp), each accompanied by a commonsense explanation of its role in home decoration.

## Serving Commonsense at Amazon Scale

Having a model that generates useful knowledge is one challenge. Serving it at Amazon’s scale with acceptable latency is another.

Amazon’s deployment architecture centers on two components:

- A Feature Store transforms COSMO-LM’s raw text outputs into structured features that downstream applications can consume directly. These features include product key-value pairs, semantic subcategory representations, and intent signals.
- An Asynchronous Cache Store manages the serving layer through a two-tiered caching strategy.

![](https://substackcdn.com/image/fetch/$s_!A2UM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6ad6938-a40d-4560-b1e6-bd834180cf9a_1890x1576.png)

The first tier pre-loads responses for yearly frequent searches, covering the majority of traffic. The second-tier batch processes daily requests for newer or less common queries and updates the cache.

When a user query arrives, the system checks the cache first. Hits get immediate responses. Misses go to batch processing, and the cache updates for future identical queries.

SageMaker manages model deployment and refresh, ingesting customer behavior session logs daily. The structured data from the cache feeds three downstream systems simultaneously, including Search Relevance, Recommendation, and Navigation.

This architecture meets Amazon’s strict search latency requirements while keeping storage costs comparable to real-time serving for most traffic. But it comes with a tradeoff. COSMO updates daily, which means it cannot incorporate real-time events like flash sales that fluctuate within hours. Amazon explicitly acknowledges this limitation and identifies it as an area for future development.

## COSMO’s Impact

Search relevance saw the most dramatic offline improvements.

On the public ESCI dataset from KDD Cup 2022, a cross-encoder (a model architecture that jointly processes query and product features together, rather than encoding them separately) augmented with COSMO triples achieved 73.48% Macro F1 and 90.78% Micro F1 with trainable encoders.

For context, Macro F1 averages performance across all product categories equally (so rare categories matter just as much as common ones), while Micro F1 measures overall accuracy regardless of category. That cross-encoder result surpassed the top-1 ensemble model on the KDD Cup leaderboard. With frozen encoders, where the only difference was whether COSMO triples were included as input, the improvement was 60% on Macro F1.

On private datasets spanning four markets (US, Canada, UK, and India), the COSMO-enhanced model consistently outperformed baselines in every locale, with the strongest gains in the India market, where the gap between query language and product catalog language tends to be larger.

Session-based recommendation benefited from COSMO knowledge as well.

Amazon built COSMO-GNN, extending a graph neural network model (a model that learns relationships between items by treating shopping sessions as connected graphs) for session-based recommendations with COSMO-generated intent knowledge. It outperformed all competitive baselines on Hits@10 and NDCG@10 in both clothing and electronics categories.

The improvement was larger for electronics (5.82% vs. 4.05% on Hits@10), where users revise their search queries more frequently (2.47 unique queries per session versus 1.36 for clothing). This pattern makes sense. When users are actively reformulating queries to narrow down what they want, commonsense knowledge about why they are searching becomes especially valuable.

Search navigation is where COSMO reached production and generated real business impact. COSMO powers a multi-turn navigation system that organizes intent hierarchically. A search for “camping” branches into fine-grained intents like “winter camping,” “beach camping,” or “lakeside camping.” These connect to product types like “air mattress” or “winter boots,” which are then further refined by attributes like “4 person.”

![](https://substackcdn.com/image/fetch/$s_!PnCr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac325460-51ca-4b80-b5f5-13063a43d3f3_2298x1668.png)

This hierarchical organization of knowledge allows the system to mirror a natural discovery process, helping customers progressively narrow their search through multiple rounds of refinement rather than requiring them to formulate the perfect query upfront.

Amazon ran A/B tests over several months, targeting approximately 10% of U.S. traffic. The results were significant. A 0.7% relative increase in product sales within the test segment translated to hundreds of millions of dollars in additional annual revenue.

An 8% increase in navigation engagement was observed in the same segment. These outcomes came from a single, relatively small feature on the search page with limited visibility. Amazon has projected that extending COSMO-LM across all traffic for navigation alone could produce revenue gains in the billions.

## Conclusion

COSMO is Amazon’s first production system that uses instruction-tuned large language models to construct a knowledge graph and serve it to online applications. It marks a shift from factual product knowledge graphs toward intent-based commonsense knowledge graphs.

The most important number from this entire project may be the leverage ratio. Thirty thousand human annotations became 29 million knowledge graph edges across 18 product categories. That ratio was possible because Amazon invested heavily in sampling strategy, annotation design, classifier training, and instruction tuning rather than in brute-force labeling.

The system’s acknowledged limitations are worth keeping in mind as well.

COSMO’s daily refresh cycle means it cannot keep up with real-time dynamics. Its aggressive filtering (only candidates above 0.5 plausibility survive) means the knowledge graph has gaps in coverage, especially for long-tail products and unusual queries. These are genuine tradeoffs, and Amazon chose precision over recall because unreliable commonsense knowledge in production would be worse than missing knowledge.

**References:**

- [Building commonsense knowledge graphs to aid product recommendation](https://www.amazon.science/blog/building-commonsense-knowledge-graphs-to-aid-product-recommendation)
- [COSMO: A large-scale e-commerce common sense knowledge generation and serving system at Amazon](https://www.amazon.science/publications/cosmo-a-large-scale-e-commerce-common-sense-knowledge-generation-and-serving-system-at-amazon)