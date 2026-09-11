---
type: raw-source
source_id: src-2026-09-08-raji-cosine-similarity-safety
captured: 2026-09-11
title: "Cosine Similarity Is Not a Safety Property"
source: "https://aminrj.com/posts/cosine-similarity-is-not-a-safety-property/?utm_source=tldrai"
author:
  - "[[Amine Raji]]"
  - "[[PhD]]"
published: 2026-09-08
created: 2026-09-09
description: "Five documents can corrupt a 2.6-million-document knowledge base through vocabulary engineering. The geometry behind RAG poisoning, why the attacker’s requirement is also their signature, and why stored vectors are not opaque."
tags:
  - "clippings"
  - "topic/rag"
  - "topic/security"
  - "topic/retrieval"
  - "source/raw"
---
The vector database returns the most *relevant* documents, defined as the ones with the highest cosine similarity to the query. This is a mathematical property with no concept of accuracy, authority or provenance. A document scoring 0.95 against a query can be entirely fabricated. A document scoring 0.60 can be the ground truth.

The attacker’s job in a poisoning attack is not to break into the vector database. It is to write a document whose embedding sits closer to the anticipated query than the legitimate document does, then frame it with enough authority to win the argument once both are in the context window.

## What the embedding model is actually doing

`sentence-transformers/all-MiniLM-L6-v2` turns any string into a 384-dimensional float vector: a point in 384-dimensional space. Semantically similar texts land near each other. “Q4 financial results” sits close to “fourth quarter revenue” and far from “company travel policy.” ChromaDB stores the vectors and answers a query by finding the k stored points closest to the query point, under whichever distance function the collection was created with.

ChromaDB’s default is squared L2, not cosine. Cosine has to be set on purpose, with `metadata={"hnsw:space": "cosine"}` at collection creation. Everything in this piece assumes a collection configured that way, which is the common choice for text embeddings and the one worth setting deliberately rather than inheriting by accident. If you skip that step, the “angle to the query point” framing below stops describing what your database is actually doing.

```python
# The entire retrieval mechanism, conceptually
query_vector = embed("What was Q4 2025 revenue?")   # 384 floats

results = collection.query(query_embeddings=[query_vector], n_results=3)
# The 3 stored vectors with smallest cosine distance.
```

The model does not know what the text *means* in any truth-bearing sense. It knows how text clusters with other text in its training data. “Revenue was $8.3M” and “Revenue was $24.7M” land at nearly identical positions, because they are the same sentence with a different number. The vector database cannot tell them apart. Only the model can, after retrieval, and only if both documents are in front of it.

This is a property of dense retrieval, not a defect in one model. `all-MiniLM-L6-v2` has aged into a poor production default; `EmbeddingGemma-300M`, `Qwen3-Embedding` and `BGE-M3` are where new work goes in 2026. None of them change the property. Semantic similarity is not factual accuracy at any parameter count.

[![Query vector with three poisoned documents clustered at 0.92 to 0.94 similarity inside the top-3 window and the legitimate document at 0.88 outside it](https://aminrj.com/assets/diagrams/embedding-space-geometry.svg)](https://aminrj.com/assets/diagrams/embedding-space-geometry.svg)

The three poisoned documents sit inside the top-3 window. The document holding the real number sits just outside it, at rank 4, and never reaches the model. Similarity values are illustrative; ChromaDB returns cosine distances, and actual values depend on model, phrasing and document length.

## Vocabulary engineering: moving a document without gradient descent

The sophisticated form of this attack, as formalised in [PoisonedRAG](https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag) (Zou, Geng, Wang and Jia, USENIX Security 2025), uses gradient-based optimisation to find text that minimises cosine distance to a target query vector. That needs white-box access to the embedding model, or query access at scale to approximate it. With that machinery, the paper injected **five crafted texts into a corpus of 2.6 million** and drove attacker-chosen answers at above 90% success.

The cheap version needs neither gradient descent nor white-box access. Identify the vocabulary of the query you want to hijack, put that vocabulary in your document, add authority signals for the generation step. In my lab that got to 95% success against an undefended pipeline (twenty runs on a small seeded corpus, one model — a lab reading, not a base rate). The three documents I used, annotated:

**Document one, the CFO correction.** Title: `Q4 2025 Financial Results — CORRECTED FIGURES (Board Update)`. Against a query like “what was Q4 2025 revenue?”, `Q4 2025` is an exact temporal match, `Financial Results` clusters with revenue and financials, `CORRECTED FIGURES` implies it supersedes something, and `Board Update` is an authority signal. Body states fabricated numbers as plain fact and closes with `Approved by: CFO Office`.

**Document two, the restatement notice.** States that Q4 revenue has been restated, actual revenue $8.3M, “not the previously reported $24.7M.” It names the real figure and reframes it as an acknowledged error, which gives the model a narrative for resolving the contradiction it is about to encounter.

**Document three, the board minutes.** Emergency session, agenda item three, corrected results, same numbers.

Three documents corroborating one fabrication against one legitimate document telling the truth. In a top-3 retrieval, three crowd out one, and the legitimate content never enters the context window. That is vocabulary engineering: shifting which regions of embedding space are occupied so fabricated documents sit closer to anticipated queries than the documents they are meant to displace.

## Two conditions, and which one does the work

PoisonedRAG frames the attack as two conditions that must both hold.

**Retrieval condition.** For a target query q, the poisoned document d\_p must make top-k:

```
cos_distance(embed(d_p), embed(q)) < cos_distance(embed(d_legit), embed(q))
```

**Generation condition.** Once in context, d\_p must cause the model to produce the attacker’s answer rather than the correct one, which requires the target answer to be present and framed with enough authority to outweigh contradicting sources.

Research attention went to the retrieval condition, because that is where the elegant optimisation lives. Recent work suggests the framing is doing more of the work. In [“Architecture Matters: Comparing RAG Systems under Knowledge Base Poisoning”](https://arxiv.org/abs/2605.05632) (Korn, May 2026), most of the strongest attack variant’s advantage came from adversarial framing rather than retrieval optimisation, and attack success across four architectures with comparable clean accuracy spread nearly 58 points, from 81.9% for vanilla RAG down to 24.4% for a recursive setup.

If framing dominates, then the stage that resolves contradictions between retrieved documents is a more valuable place to invest than another round of retrieval hardening. In my own measurements the legitimate document was often retrieved *and still lost*. The real Q4 figure sat in the context window while the model reported the fabricated one, because two documents said the real figure had been corrected and one document just quietly stated it.

## Turning the geometry against the attacker

The attacker’s requirement is also their signature. To be retrieved, the poisoned documents must cluster near the target query position, which is near the legitimate documents on that topic. An ingestion-time check can look for this.

Two signals, computed before anything is stored:

```python
# Signal 1 — nearest neighbour in the existing collection
existing = collection.query(query_embeddings=[new_doc_embedding], n_results=3)
for dist in existing["distances"][0]:
    if (1.0 - dist) > SIMILARITY_THRESHOLD:      # 0.85 in the lab
        flag("HIGH_SIMILARITY — possible content override")

# Signal 2 — pairwise similarity within the incoming batch
for i, e_i in enumerate(new_embeddings):
    for j in range(i + 1, len(new_embeddings)):
        if cosine_similarity(e_i, new_embeddings[j]) > CLUSTER_THRESHOLD:   # 0.90
            flag("TIGHT_CLUSTER — possible coordinated injection")
```

Both fire on the three-document attack. Each poisoned document’s nearest neighbour is the legitimate Q4 report, because both are about Q4 2025 financials. The three cluster tightly with each other, because they are variations on one fabricated narrative. This single layer took poisoning success from 95% to 20%.

The geometric reason it works is the closest thing to a structural guarantee in this area: the attacker cannot fully satisfy both requirements at once. Satisfying the retrieval condition means occupying space near existing content, which is detectable. Evading detection means moving away from that space, which degrades retrieval. The 20% residual is the band where an attacker balances the two, typically with a single document instead of a cluster, or with enough vocabulary variation to fall below the similarity threshold while staying retrievable.

```
#mermaid-1788916092439{font-size:14px;fill:#333;}#mermaid-1788916092439 .error-icon{fill:hsl(25.7142857143, 84%, 100%);}#mermaid-1788916092439 .error-text{fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);}#mermaid-1788916092439 .edge-thickness-normal{stroke-width:1px;}#mermaid-1788916092439 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1788916092439 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1788916092439 .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-1788916092439 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1788916092439 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1788916092439 .marker{fill:#0b0b0b;stroke:#0b0b0b;}#mermaid-1788916092439 .marker.cross{stroke:#0b0b0b;}#mermaid-1788916092439 svg{font-size:14px;}#mermaid-1788916092439 p{margin:0;}#mermaid-1788916092439 .label{color:#333;}#mermaid-1788916092439 .cluster-label text{fill:rgb(0, 0, 0);}#mermaid-1788916092439 .cluster-label span{color:rgb(0, 0, 0);}#mermaid-1788916092439 .cluster-label span p{background-color:transparent;}#mermaid-1788916092439 .label text,#mermaid-1788916092439 span{fill:#333;color:#333;}#mermaid-1788916092439 .node rect,#mermaid-1788916092439 .node circle,#mermaid-1788916092439 .node ellipse,#mermaid-1788916092439 .node polygon,#mermaid-1788916092439 .node path{fill:#e8f4fd;stroke:#3182ce;stroke-width:1px;}#mermaid-1788916092439 .rough-node .label text,#mermaid-1788916092439 .node .label text,#mermaid-1788916092439 .image-shape .label,#mermaid-1788916092439 .icon-shape .label{text-anchor:middle;}#mermaid-1788916092439 .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-1788916092439 .rough-node .label,#mermaid-1788916092439 .node .label,#mermaid-1788916092439 .image-shape .label,#mermaid-1788916092439 .icon-shape .label{text-align:center;}#mermaid-1788916092439 .node.clickable{cursor:pointer;}#mermaid-1788916092439 .root .anchor path{fill:#0b0b0b!important;stroke-width:0;stroke:#0b0b0b;}#mermaid-1788916092439 .arrowheadPath{fill:#0b0b0b;}#mermaid-1788916092439 .edgePath .path{stroke:#0b0b0b;stroke-width:2.0px;}#mermaid-1788916092439 .flowchart-link{stroke:#0b0b0b;fill:none;}#mermaid-1788916092439 .edgeLabel{background-color:hsl(85.7142857143, 84%, 95.0980392157%);text-align:center;}#mermaid-1788916092439 .edgeLabel p{background-color:hsl(85.7142857143, 84%, 95.0980392157%);}#mermaid-1788916092439 .edgeLabel rect{opacity:0.5;background-color:hsl(85.7142857143, 84%, 95.0980392157%);fill:hsl(85.7142857143, 84%, 95.0980392157%);}#mermaid-1788916092439 .labelBkg{background-color:rgba(244, 253, 232.0000000001, 0.5);}#mermaid-1788916092439 .cluster rect{fill:hsl(25.7142857143, 84%, 100%);stroke:hsl(25.7142857143, 44%, 90%);stroke-width:1px;}#mermaid-1788916092439 .cluster text{fill:rgb(0, 0, 0);}#mermaid-1788916092439 .cluster span{color:rgb(0, 0, 0);}#mermaid-1788916092439 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-size:12px;background:hsl(25.7142857143, 84%, 100%);border:1px solid hsl(25.7142857143, 44%, 90%);border-radius:2px;pointer-events:none;z-index:100;}#mermaid-1788916092439 .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#mermaid-1788916092439 rect.text{fill:none;stroke-width:0;}#mermaid-1788916092439 .icon-shape,#mermaid-1788916092439 .image-shape{background-color:hsl(85.7142857143, 84%, 95.0980392157%);text-align:center;}#mermaid-1788916092439 .icon-shape p,#mermaid-1788916092439 .image-shape p{background-color:hsl(85.7142857143, 84%, 95.0980392157%);padding:2px;}#mermaid-1788916092439 .icon-shape rect,#mermaid-1788916092439 .image-shape rect{opacity:0.5;background-color:hsl(85.7142857143, 84%, 95.0980392157%);fill:hsl(85.7142857143, 84%, 95.0980392157%);}#mermaid-1788916092439 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}#mermaid-1788916092439 .threat>*{fill:#0f172a!important;stroke:#0f172a!important;color:#fff!important;stroke-width:1.5px!important;}#mermaid-1788916092439 .threat span{fill:#0f172a!important;stroke:#0f172a!important;color:#fff!important;stroke-width:1.5px!important;}#mermaid-1788916092439 .threat tspan{fill:#fff!important;}#mermaid-1788916092439 .ok>*{fill:#e8f4fd!important;stroke:#3182ce!important;color:#1a202c!important;stroke-width:1.5px!important;}#mermaid-1788916092439 .ok span{fill:#e8f4fd!important;stroke:#3182ce!important;color:#1a202c!important;stroke-width:1.5px!important;}#mermaid-1788916092439 .ok tspan{fill:#1a202c!important;}same propertysame propertyRetrieval condition
embed close to target querySignal 1
similarity to existing > thresholdCoordinated injection
several docs, one spaceSignal 2
pairwise similarity > thresholdThe attacker's dilemma
evading detection degrades retrieval
satisfying retrieval triggers detection
```

## Access-controlled retrieval: the where clause

A metadata filter on every vector query that restricts which documents the requesting user is allowed to retrieve. Without it, every document in the collection is reachable by every user through an ordinary question. Ask an assistant what the salary bands are and it retrieves whatever is semantically close, with no idea who is asking.

I ran this against a lab pipeline holding three restricted documents: salary data marked HR-only, litigation detail marked privileged, and an M&A pipeline marked board-level. Queried as a regular engineering user, in natural language, with no evasion. Twenty out of twenty queries returned confidential content.

```python
# Vulnerable: no notion of who is asking
results = collection.query(query_embeddings=[query_embedding], n_results=3)

# Hardened: retrieval scoped to the requester's clearances
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
    where={"classification": {"$in": user_permitted_classifications}},
);
```

That filter is the only complete defence against cross-tenant leakage, because it is structural. It prevents unauthorised content from entering the context window at all. Output monitoring, prompt hardening and every other heuristic runs after retrieval, by which point the data is already in the prompt.

A minimal access model is enough to start:

| Role | Permitted classifications |
| --- | --- |
| Regular employee | public, internal |
| HR business partner | \+ confidential (HR) |
| Legal counsel | \+ privileged |
| Executive | all |

You do not need full RBAC. You need a mapping from identity to permitted metadata values, applied on every retrieval path.

Partial implementation of this control is worse than none, because it manufactures confidence. A `where` filter on the main chat endpoint, with an unfiltered path in the summarisation job or the eval harness, gives you a system that looks access-controlled and is not. Find every retrieval call, not the obvious one.

## The threshold problem

The lab hardcodes 0.85 and 0.90. Those are not universal values, and copying them into production is the most common way this control fails.

At 0.85 the defence catches the three-document attack because the poisoned documents score around 0.88 to 0.92 against the legitimate financials. Increase vocabulary variation, keeping the financial theme but varying the specific language, and similarity drops to roughly 0.78 to 0.82. Below threshold, not flagged, still retrievable.

| Threshold | Poisoning caught | Legitimate updates flagged |
| --- | --- | --- |
| 0.95 | Only near-verbatim overrides | Almost none |
| 0.90 | Strong variants | Occasional, on revised documents |
| 0.85 (lab default) | Most variants | Some, on policy revisions and corrections |
| 0.80 | More variants | Frequent, most updates flagged |
| 0.75 | Maximum coverage | Impractical, constant manual review |

The right value comes from your ingestion patterns. An append-only corpus can sit low. A living wiki with versioned policies cannot, because every legitimate amendment looks like an override attempt. Baseline your collection’s actual similarity distribution and set the threshold around mean plus two standard deviations, then revisit as the collection grows.

**These thresholds are properties of your embedding model, not of your data.** Similarity distributions are not comparable across models. Swap `all-MiniLM-L6-v2` for `Qwen3-Embedding` or `BGE-M3` and every threshold you tuned is now measuring a different geometry. A model upgrade silently invalidates your detector. Pin the embedding model version alongside the threshold, and treat an embedding migration as a re-baselining project.

## Your vectors are not opaque

Embedding vectors get treated as one-way functions. You embed text, store the vector, and the original text is not recoverable from the vector alone. That assumption was never proven for dense sentence embeddings. It was inherited by practitioners who thought of embeddings as just numbers.

The research record says otherwise:

- **Morris, Kuleshov, Shmatikov and Rush, [“Text Embeddings Reveal (Almost) As Much As Text”](https://aclanthology.org/2023.emnlp-main.765/) (EMNLP 2023)** built Vec2Text, an iterative correct-and-re-embed method that recovered **92% of 32-token inputs exactly**, and recovered full names from a dataset of clinical notes. Not fragments. The text.
- **Chen, Lent and Bjerva, [“Text Embedding Inversion Security for Multilingual Language Models”](https://aclanthology.org/2024.acl-long.422/) (ACL 2024)** extended inversion to multilingual embedding spaces and found that some languages are markedly more exposed than others.
- **[ALGEN](https://arxiv.org/abs/2502.11308) (Chen, Xu and Bjerva, February 2025)** removed the expensive prerequisite. Earlier attacks assumed access to millions of text-embedding pairs to train the inversion model. ALGEN aligns a victim embedding space to the attacker’s space with a one-step linear map, and reports that **a single pair gives partial success while about 1,000 pairs reach optimum** across a range of black-box encoders, with ROUGE-L up to about 46 in their main cross-encoder results (a monolingual upper-bound condition in the same paper reaches the low fifties) and cosine similarity around 0.95 on the aligned space. It transfers across encoders and across languages. The authors tested a range of defences and report that none were effective.
- **[LAGO](https://arxiv.org/abs/2505.16008) (Yu, Chen, Bjerva, Kosta and Li, May 2025)** generalises ALGEN, using language-similarity graph optimisation to gain a further 10 to 20% ROUGE-L, with as few as ten samples per language.

[![Timeline of embedding inversion research from Vec2Text in 2023 to LAGO in 2025, with the training data requirement falling from millions of pairs to about ten per language](https://aminrj.com/assets/diagrams/embedding-inversion-timeline.svg)](https://aminrj.com/assets/diagrams/embedding-inversion-timeline.svg)

The interesting trend is the bottom row. Recovery quality was established in 2023; what changed since is how little the attacker needs to reproduce it.

ALGEN’s contribution is *cost*: it collapses the data requirement from millions of pairs to roughly a thousand, which moves inversion from a research capability to something an ordinary attacker can do. The high word-recovery figures come from the Vec2Text line of work. Both matter together: strong recovery quality from earlier work, near-zero setup cost from the newer work.

Consider the sensitive documents in a multi-tenant scenario: salary bands, litigation detail with settlement authority, an M&A pipeline with named targets and valuations. Access-controlled retrieval stops unauthorised users from retrieving those through normal queries. Encryption at rest stops plaintext exfiltration at the database layer. Neither helps if someone walks off with the raw vector store through a cloud misconfiguration, a compromised admin credential or an unsecured backup. If your embedding model is public, which it usually is because it came off Hugging Face, the thousand pairs needed to align an inversion model are trivially obtainable.

A vector store exfiltration is not a metadata exposure. It is a partial document exposure, even if you never stored the source text.

```
#mermaid-1788916092512{font-size:14px;fill:#333;}#mermaid-1788916092512 .error-icon{fill:hsl(25.7142857143, 84%, 100%);}#mermaid-1788916092512 .error-text{fill:rgb(0, 0, 0);stroke:rgb(0, 0, 0);}#mermaid-1788916092512 .edge-thickness-normal{stroke-width:1px;}#mermaid-1788916092512 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1788916092512 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1788916092512 .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-1788916092512 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1788916092512 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1788916092512 .marker{fill:#0b0b0b;stroke:#0b0b0b;}#mermaid-1788916092512 .marker.cross{stroke:#0b0b0b;}#mermaid-1788916092512 svg{font-size:14px;}#mermaid-1788916092512 p{margin:0;}#mermaid-1788916092512 .label{color:#333;}#mermaid-1788916092512 .cluster-label text{fill:rgb(0, 0, 0);}#mermaid-1788916092512 .cluster-label span{color:rgb(0, 0, 0);}#mermaid-1788916092512 .cluster-label span p{background-color:transparent;}#mermaid-1788916092512 .label text,#mermaid-1788916092512 span{fill:#333;color:#333;}#mermaid-1788916092512 .node rect,#mermaid-1788916092512 .node circle,#mermaid-1788916092512 .node ellipse,#mermaid-1788916092512 .node polygon,#mermaid-1788916092512 .node path{fill:#e8f4fd;stroke:#3182ce;stroke-width:1px;}#mermaid-1788916092512 .rough-node .label text,#mermaid-1788916092512 .node .label text,#mermaid-1788916092512 .image-shape .label,#mermaid-1788916092512 .icon-shape .label{text-anchor:middle;}#mermaid-1788916092512 .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-1788916092512 .rough-node .label,#mermaid-1788916092512 .node .label,#mermaid-1788916092512 .image-shape .label,#mermaid-1788916092512 .icon-shape .label{text-align:center;}#mermaid-1788916092512 .node.clickable{cursor:pointer;}#mermaid-1788916092512 .root .anchor path{fill:#0b0b0b!important;stroke-width:0;stroke:#0b0b0b;}#mermaid-1788916092512 .arrowheadPath{fill:#0b0b0b;}#mermaid-1788916092512 .edgePath .path{stroke:#0b0b0b;stroke-width:2.0px;}#mermaid-1788916092512 .flowchart-link{stroke:#0b0b0b;fill:none;}#mermaid-1788916092512 .edgeLabel{background-color:hsl(85.7142857143, 84%, 95.0980392157%);text-align:center;}#mermaid-1788916092512 .edgeLabel p{background-color:hsl(85.7142857143, 84%, 95.0980392157%);}#mermaid-1788916092512 .edgeLabel rect{opacity:0.5;background-color:hsl(85.7142857143, 84%, 95.0980392157%);fill:hsl(85.7142857143, 84%, 95.0980392157%);}#mermaid-1788916092512 .labelBkg{background-color:rgba(244, 253, 232.0000000001, 0.5);}#mermaid-1788916092512 .cluster rect{fill:hsl(25.7142857143, 84%, 100%);stroke:hsl(25.7142857143, 44%, 90%);stroke-width:1px;}#mermaid-1788916092512 .cluster text{fill:rgb(0, 0, 0);}#mermaid-1788916092512 .cluster span{color:rgb(0, 0, 0);}#mermaid-1788916092512 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-size:12px;background:hsl(25.7142857143, 84%, 100%);border:1px solid hsl(25.7142857143, 44%, 90%);border-radius:2px;pointer-events:none;z-index:100;}#mermaid-1788916092512 .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#mermaid-1788916092512 rect.text{fill:none;stroke-width:0;}#mermaid-1788916092512 .icon-shape,#mermaid-1788916092512 .image-shape{background-color:hsl(85.7142857143, 84%, 95.0980392157%);text-align:center;}#mermaid-1788916092512 .icon-shape p,#mermaid-1788916092512 .image-shape p{background-color:hsl(85.7142857143, 84%, 95.0980392157%);padding:2px;}#mermaid-1788916092512 .icon-shape rect,#mermaid-1788916092512 .image-shape rect{opacity:0.5;background-color:hsl(85.7142857143, 84%, 95.0980392157%);fill:hsl(85.7142857143, 84%, 95.0980392157%);}#mermaid-1788916092512 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}#mermaid-1788916092512 .ok>*{fill:#e8f4fd!important;stroke:#3182ce!important;color:#1a202c!important;stroke-width:1.5px!important;}#mermaid-1788916092512 .ok span{fill:#e8f4fd!important;stroke:#3182ce!important;color:#1a202c!important;stroke-width:1.5px!important;}#mermaid-1788916092512 .ok tspan{fill:#1a202c!important;}#mermaid-1788916092512 .threat>*{fill:#0f172a!important;stroke:#0f172a!important;color:#fff!important;stroke-width:1.5px!important;}#mermaid-1788916092512 .threat span{fill:#0f172a!important;stroke:#0f172a!important;color:#fff!important;stroke-width:1.5px!important;}#mermaid-1788916092512 .threat tspan{fill:#fff!important;}Vector store exfiltrated
misconfiguration · backup · insiderRaw embedding vectors
assumed opaque~1,000 text-embedding pairs
from a public model
no insider access neededAligned inversion model
transfers across encoders and languagesInvert the stored vectorsSubstantial text reconstruction
salary bands · settlement figures · named targets
even if source text was never stored
```

## What this means for your threat model

Two changes, and the first one is free.

**Reclassify vector store compromise in your incident response plan.** Most plans treat it as a metadata leak, vectors only, low severity, no notification. That classification is wrong on the current research, and it is wrong in the direction that matters, because it determines who gets told and how fast. The severity floor for a vector store breach is a partial document leak of the most sensitive material in the collection. The practical exercise: take the ten most sensitive documents in your knowledge base, imagine a reconstruction that recovers most of their content in the wrong word order, and ask whether that is a breach you would have to disclose. If yes, the classification needs to change before the incident, not during it.

Most teams classify a vector store breach as a metadata leak, and after the inversion literature it belongs in the partial-document-leak column. That changes your notification analysis and your board briefing, and it costs nothing to fix today.

[![Vector store breach reclassified from metadata leak with low severity to partial document leak requiring notification assessment](https://aminrj.com/assets/diagrams/vector-store-incident-classification.svg)](https://aminrj.com/assets/diagrams/vector-store-incident-classification.svg)

The reclassification is a paperwork change you can make this quarter. Making it during an incident, with counsel on the call, is considerably more expensive.

**Evaluate per-tenant vector encryption if you are multi-tenant.** [IronCore Labs’ Cloaked AI](https://ironcorelabs.com/products/cloaked-ai/) uses property-preserving encryption so encrypted vectors remain usable for nearest-neighbour search while being scoped to per-tenant keys. BYOK is available as an add-on through IronCore’s separate SaaS Shield product. Costs are query latency and key management. For a single-tenant deployment with trusted contributors, the inversion risk may be an acceptable residual. For multi-tenant SaaS where tenant isolation is the product promise, this belongs on the roadmap.

## A vector store security checklist

This one treats the vector database as a security asset in its own right, distinct from the pipeline defences covered in [the semantic injection article](https://aminrj.com/posts/semantic-injection-passes-every-filter/).

**Access**

- The vector database API requires authentication, and is not simply open on the internal network
- Service accounts have minimum necessary permissions, separated by function
- Admin credentials are vaulted and rotated separately from application credentials

**Classification**

- The vector store is classified at the sensitivity of the documents it was built from, not lower
- Vector store exfiltration appears in your breach response scenarios, as a document leak
- Highly sensitive source documents are flagged in vector metadata so you can scope an incident

**Monitoring**

- Bulk embedding query volume is logged and alerted, since collecting alignment pairs looks like anomalous query volume
- Ingestion events are logged with contributor identity and timestamp
- Sudden large ingestion from a single source triggers review

**Recovery**

- Point-in-time snapshots of the collection are taken on a schedule
- Restore from a known-good snapshot has actually been tested, not just configured
- Snapshots carry the same access controls as the live store

**Inversion exposure**

- You know whether your embedding model is publicly available
- The embedding model version is pinned next to your anomaly thresholds
- Per-tenant vector encryption has been evaluated, with a documented decision either way

## Where this leaves you

Cosine similarity measures an angle. It has no notion of truth, authority or provenance, and when you build a RAG system you inherit every security assumption of the embedding space along with its retrieval quality.

Poisoning works because vocabulary engineering can move a document’s position without touching the model’s internals. Anomaly detection works because the geometric requirement that makes the attack effective is also what makes it visible at ingestion. Inversion works because dense vectors carry enough of the source text to reconstruct much of it, and the assumption that they did not was folklore rather than a result.

Practitioners adopted the outputs of ML research and deployed them with security properties the underlying math never offered. Understanding the math does not secure the system. It does tell you where a defence can work, and which claims about your defences are well founded rather than hopeful.

---

Lab code, including `defenses/embedding_anomaly_detection.py` and the poisoned document set: [aminrj-labs/mcp-attack-labs/labs/04-rag-security](https://github.com/aminrj-labs/mcp-attack-labs/tree/main/labs/04-rag-security). The detector is dependency-light and drops into any ChromaDB pipeline. Measurements were taken March 2026 against ChromaDB with `all-MiniLM-L6-v2` and Qwen2.5-7B-Instruct at temperature 0.1, twenty runs per configuration on a small seeded corpus. They demonstrate mechanisms and rankings, not production base rates.

---

### References

- Zou, Geng, Wang and Jia, [“PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models”](https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag), USENIX Security 2025 ([arXiv 2402.07867](https://arxiv.org/abs/2402.07867))
- Korn, [“Architecture Matters: Comparing RAG Systems under Knowledge Base Poisoning”](https://arxiv.org/abs/2605.05632), May 2026
- Morris, Kuleshov, Shmatikov and Rush, [“Text Embeddings Reveal (Almost) As Much As Text”](https://aclanthology.org/2023.emnlp-main.765/), EMNLP 2023
- Chen, Lent and Bjerva, [“Text Embedding Inversion Security for Multilingual Language Models”](https://aclanthology.org/2024.acl-long.422/), ACL 2024
- Chen, Xu and Bjerva, [“ALGEN: Few-shot Inversion Attacks on Textual Embeddings using Alignment and Generation”](https://arxiv.org/abs/2502.11308), February 2025
- Yu, Chen, Bjerva, Kosta and Li, [“LAGO: Few-shot Crosslingual Embedding Inversion Attacks via Language Similarity-Aware Graph Optimization”](https://arxiv.org/abs/2505.16008), May 2025
- [Cloaked AI](https://ironcorelabs.com/products/cloaked-ai/), IronCore Labs (property-preserving encryption for vector embeddings)
- [LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/), OWASP GenAI Security Project