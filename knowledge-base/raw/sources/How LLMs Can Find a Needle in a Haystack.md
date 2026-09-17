---
title: "How LLMs Can Find a Needle in a Haystack"
source: "https://blog.bytebytego.com/p/how-llms-can-find-a-needle-in-a-haystack?utm_source=post-email-title&publication_id=817132&post_id=215151603&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-09-16
created: 2026-09-17
description: "In this article, we are going to look at how LLMs can find a needle in a haystack."
tags:
  - "clippings"
---
## Debugging Agents in Different Environments - Live Workshop (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!4Bqd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b33cc90-902c-4469-b0d2-acacfe20f357_2686x1494.png)

Your agent returns something odd. Was it the prompt, a tool call that timed out, or a response your code could not parse? Without traces, you are guessing.

In this hands-on workshop, Serge from Sentry instruments three agents with Sentry Agent Tracing: a chatbot in an ecommerce store, a custom Slack agent, and a GitHub Action that reviews PRs. You will see how to catch bad tool calls and unexpected output, plus how to track token spend and performance across every agent you run.

---

Imagine a scenario where an employee is stranded at an airport after a cancelled flight. Before booking a hotel, they ask the company’s AI assistant a simple question: “Can I expense a hotel if my flight gets cancelled?”

The company has thousands of documents covering travel, expenses, insurance, employee benefits, and regional policies. Somewhere inside them, a paragraph states that accommodation costs caused by involuntary travel disruption are reimbursable, subject to certain conditions.

For an LLM chatbot, finding that piece of information is harder than it appears. The question mentions a “cancelled flight,” while the policy refers to “involuntary travel disruption.” Other documents discuss hotels but apply to different countries. An older policy may be present that contains a reimbursement limit that has since changed.

In such a case, the LLM must find information that matches the question’s meaning, belongs to the correct policy, and remains valid today. Only then can it write a useful answer that solves the user’s problem.

This is known as the retrieval problem behind many LLM applications. In this article, we are going to look at how LLMs can find a needle in a haystack. Here’s what we will cover:

- An LLM needs evidence to answer questions
- How documents are turned into searchable passages
- How LLMs find the meaning behind different words
- How close is close enough
- Why searching every passage is too expensive
- Following connections to the the right neighborhood
- How much searching is enough
- What happens when the answer changes

## The LLM Needs Evidence to Answer Questions

A language model does not automatically know what is inside a company’s private documents. An application must provide that information, either by including documents directly in its input or by retrieving relevant passages when a question arrives.

![](https://substackcdn.com/image/fetch/$s_!tTph!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02a5951e-febf-4289-8905-c67f45e754a1_3282x1854.png)

For a large collection, retrieval offers a way to select a manageable amount of information. An embedding model converts the question into a numerical representation. A search system then uses that representation to find promising passages. The application supplies the original text to the LLM.

The model can then use those passages to explain the policy and cite the exact sources where it got the information from. This pattern is called retrieval-augmented generation, or RAG. A vector database supports the retrieval part by storing and searching numerical representations of content.

![](https://substackcdn.com/image/fetch/$s_!jMWU!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7be48688-e2ab-4b5b-8fd1-f2d5bfee84f1_2694x1592.png)

This division of responsibilities is really useful. If the application retrieves an outdated policy, even a capable language model will produce an outdated answer. If it retrieves a general hotel-booking rule while missing the cancellation exception, the answer may sound reasonably correct while overlooking the important condition.

Reliable answers therefore depend on what happens before generation. This means we have to make the document collection searchable at the right level of detail.

## How Documents are Turned into Searchable Passages

A travel handbook can cover flights, accommodation, meals, approvals, and insurance. However, treating the entire handbook as a single searchable item produces a broad representation that can obscure a specific rule.

Instead, the application divides documents into smaller units called chunks. One chunk might describe hotel reimbursement, while another explains approval requirements. Search can then identify a particular passage instead of merely identifying the handbook that contains it.

![](https://substackcdn.com/image/fetch/$s_!W7yl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5dfe5328-ebff-437f-be30-1e27a72be8d0_3658x1776.png)

Chunking creates a balance between precision and context. A small chunk may focus tightly on the question but leave out an exception. A large chunk may preserve the exception while including several unrelated policies. For example, suppose a passage says, “Accommodation expenses are reimbursable following a cancellation.” And the next sentence adds, “This applies only when accommodation is not provided by the airline.” Separating those sentences could cause the assistant to give an incorrect answer despite having the relevant text.

A useful chunk therefore preserves a complete idea wherever possible. Section headings and limited overlap between neighboring chunks can help retain context. The goal is to create passages that remain understandable when retrieved independently.

For our example question by the employee, the ideal searchable unit contains the reimbursement rule, its conditions, and enough identifying context to establish which policy it belongs to.

## How LLMs Find the Meaning Behind Different Words

Embeddings make it possible to search for related meaning even when the wording differs.

An embedding model takes a passage and produces a vector: a list of numbers, often containing hundreds or thousands of decimal values. Think of it as a map of text. Passages with related meanings occupy nearby positions. For example, a question about hotel expenses after a cancelled flight should appear closer to a travel-disruption policy than to instructions for resetting a password.

![](https://substackcdn.com/image/fetch/$s_!af4n!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F314bf6b0-0fe8-4038-8d39-a99a68e77234_3800x2024.png)

The real representation has many more dimensions than a physical map. Individual dimensions also don’t have simple labels such as “hotel,” “flight,” or “reimbursement.” Meaning is represented through patterns across the complete vector.

The trick is that the application embeds the question into the same space as the document chunks. This way, it can compare the question’s vector with stored vectors to identify nearby passages. Also, the query and document embeddings must come from compatible encoders. However, matching vector lengths alone doesn’t make two models compatible.

Each searchable record also needs a connection to the original text. The vector helps locate a passage, but the LLM needs the words themselves to interpret the rule. Therefore, a record should connect an embedding with a chunk identifier, the passage text, or its location. Also, metadata such as document ID, section, effective date, and version are present. These fields can be stored together or across connected storage systems. Structured identifiers make it possible to retrieve and maintain all chunks belonging to a document.

## How Close Is Close Enough?

The search system needs a precise definition of “nearby.” This definition comes from a distance or similarity metric, which compares two vectors and assigns a score. There are different metrics around this:

- Cosine similarity compares their directions while ignoring their lengths.
- Euclidean distance measures the straight-line distance between their endpoints, so vector length can influence the result.
- Dot product reflects both alignment and length.

Normalization rescales vectors to length one. When both query and document vectors are normalized, dot product equals cosine similarity. Euclidean distance then produces the same ranking, although its scores differ. Dot product also works with unnormalized vectors when that matches the embedding model’s design.

The choice of the metric should follow the embedding model’s intended use. Choosing a metric simply because it is popular can change the ranking in unintended ways.

A similarity score should also be interpreted carefully. A score of 0.85 does not mean that a passage has an 85% probability of answering the question correctly. It describes a mathematical relationship between representations.

The passage may discuss the right subject while stating the wrong regional policy. It may be outdated or omit an exception. Similarity provides evidence of relevance, but additional checks are needed before that evidence becomes an answer.

## Why Searching Every Passage Is Too Expensive

Searching every vector is straightforward, but the work grows with the collection.

![](https://substackcdn.com/image/fetch/$s_!0_KI!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d2609b5-c9f3-4ec7-8036-25272bd49f9b_3060x1450.png)

A flat index compares the query with every eligible vector and returns those with the best scores. For a fixed number of dimensions, the comparison work grows roughly in proportion to the vector count. This is the meaning of O(n). If the collection doubles, the number of vector comparisons doubles. Longer vectors also require more work per comparison.

Flat search produces exact nearest neighbors under the selected metric. “Exact” describes the numerical search result. It doesn’t guarantee that those neighbors contain the correct answer.

On the other hand, an Inverted-File index reduces this work by organizing vectors into groups. During construction, clustering identifies representative centers and assigns vectors to nearby groups. A query can then select promising groups and search their contents. The parameter commonly called nprobe controls how many groups are examined. However, searching more groups generally improves recall but also increases work.

Imagine one million passages divided into 1000 groups. Searching 10 groups might involve roughly 10K passages rather than the entire million. Of course, real groups are uneven, and selecting them also has a cost. The main tradeoff is that a useful passage can belong to a group that is skipped by the search. These groups are mathematical neighborhoods, not tidy subject folders. A travel-disruption rule might sit near insurance documents rather than ordinary expense policies.

IVF therefore introduces approximation. It saves work by accepting some risk of missing the nearest vectors.

## Following Connections to the Right Neighborhood

HNSW (Hierarchical Navigable Small World) avoids exhaustive comparisons by building routes between vectors. Its structure is a graph. In other words, points are connected by links.

Each point represents a vector. The links provide routes through the collection. HNSW organizes these connections into layers, with sparse upper layers and a detailed bottom layer containing all vectors.

In this approach, search starts near the top and moves toward points closer to the query. It then descends through the layers, progressively refining the search. At the bottom, it explores a broader set of nearby candidates to select the results.

You can think of this navigation like travelling through a road network. Major routes help reach the right area, while local roads help locate a specific destination. HNSW uses this broad-to-detailed pattern to avoid visiting every point.

Like the Inverted-File index, it performs approximate nearest-neighbor search. However, selected routes can miss a true nearest neighbor. Its benefit is that useful results can often be found with substantially fewer comparisons.

There is no fixed collection size at which flat search must give way to Inverted-File or HNSW. Hardware, vector dimensions, query volume, memory, filtering, and latency requirements all influence the choice. HNSW is a strong candidate when memory permits, but we cannot say that it is automatically the best option for every workload.

A collection searched a few times per day creates a different problem from one serving thousands of simultaneous users. Vector count alone cannot capture that difference.

## How Much Searching Is Enough?

Approximate search creates a measurable tradeoff between speed and recall.

Let’s say an exact search identifies the 10 nearest vectors. An approximate search returns eight of those same vectors and two others. This measures how closely the approximate search reproduces exact nearest-neighbor results. It doesn’t measure whether the returned passages really answer the employee’s question. Both index recall and actual evidence relevance need evaluation.

HNSW has several settings that have an impact on this tradeoff:

- M controls graph connectivity. Higher values generally provide more routes, improving recall while increasing memory use and construction work.
- ef\_construction controls how broadly the algorithm searches for suitable connections during insertion. A larger value generally produces a better graph but takes longer to build.
- ef\_search controls the breadth of candidate exploration during a query. Increasing it generally improves recall while increasing search latency. It isn’t the number of results returned or a fixed count of visited points.

The application may need five passages while exploring a much larger candidate set to find them. Result count and search effort are separate decisions.

For tuning, we should use representative questions and actual performance measurements. If a broader search consistently finds a previously missed cancellation exception, the added latency may be worthwhile. However, if answers don’t improve, changing the setting merely adds work.

## The Closest Match Might Be the Wrong Policy

Similarity must also be combined with rules about which documents are eligible.

For example, our employee needs the policy for their country and business unit, with an effective date that covers the journey. A highly similar passage from another region cannot help answer their query.

We use metadata filtering to define the eligible subset. The request becomes “find the most similar passages among current policies for this employee’s region.”

- Pre-filtering identifies eligible records before similarity ranking.
- Post-filtering retrieves similarity candidates first and then removes records that fail the conditions.

If only two of the first 20 candidates qualify, post-filtering cannot supply 5 eligible results from that batch. Retrieving additional candidates may help, but requires more work.

Nevertheless, pre-filtering is not automatically faster. The outcome depends on how selective the filter is and how the search engine combines filtering with its index. Graph search adds another complication. Disallowed points may still provide useful navigation routes toward allowed points. Blocking every such point during traversal can make eligible neighbors harder to reach.

Search engines can address this through filtering-aware graph structures, traversal strategies, or an exact scan when the eligible subset is small. Filtering can therefore be integrated into search rather than occurring entirely before or after it.

## What Happens When the Answer Changes?

The collection must remain correct as its documents change. For example, let’s say the company raises its hotel reimbursement limit from ₹5,000 to ₹7,000. If both versions remain eligible for current-policy searches, the assistant may retrieve either figure or receive contradictory evidence.

Changes to embedded text require new embeddings. However, an update doesn’t always require rebuilding every chunk. Unchanged chunks may be reusable, and stable identifiers can support replacing existing records.

A metadata-only change can often be applied without re-embedding, provided that metadata was not a part of the text used to create the vector. Some vector databases can expose separate operations for changing vectors and metadata.

For our policy example, a sensible design can prepare the new version’s chunks, verify their availability, and then change which version is eligible for current searches. Older versions can remain accessible for historical questions.

That transition requires some sort of coordination. Deleting old chunks first can create a temporary gap. Inserting new chunks first can create temporary duplication. Version identifiers and explicit active-version rules help make the change predictable. Lastly, changing the embedding model requires similar planning but on a much larger scale. Existing documents generally need embeddings in the new model’s space, and queries must use the matching representation.

## From Promising Matches to a Supported Answer

The final retrieval step turns promising matches into evidence the LLM can use. For example, a vector search might return 30 candidate passages. A reranker can compare each passage’s text with the question and select the most useful few.

![](https://substackcdn.com/image/fetch/$s_!fVSY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fedeec364-514a-4cf8-87a6-06132f80c98b_3622x1310.png)

Hybrid search adds another source of candidates by combining semantic retrieval with keyword-based retrieval. Embeddings help connect “cancelled flight” with “travel disruption,” while keyword search can preserve exact matches for policy identifiers, names, or unusual technical terms. Reranking can refine the combined results.

The application then supplies the selected text and source details to the LLM. For the stranded employee, this should include the current reimbursement rule, the relevant conditions, and enough context to explain how the policy applies to their situation.

The search must also accommodate the scenario of an unanswered question. Every collection has nearest vectors, even when none might contain useful information. Returning the closest passage doesn’t mean that an answer exists. For example, if the retrieved documents discuss ordinary hotel bookings but say nothing about cancellations, the assistant should explain clearly that the available policy details don’t have a clear answer.

## Conclusion

Finding a useful passage among thousands of documents requires several parts of an LLM application to work together. Documents first become smaller, meaningful chunks. Embeddings represent those chunks as vectors, allowing the search system to connect a question with passages that express related ideas, even when their wording differs.

As the collection grows, indexes make that search more efficient. Flat search compares every eligible vector, while IVF and HNSW reduce the work through grouping or graph navigation. These approaches introduce tradeoffs between speed, memory, and recall that need to be measured against real questions.

Similarity alone, however, cannot establish whether a passage is suitable evidence. Metadata filters help select the correct region, document type, or policy version. Careful updates keep outdated and duplicate passages from appearing in current searches. Hybrid search and reranking can further improve the evidence selected for the LLM.

The final answer depends on the quality of this entire process. For the employee stranded at the airport, success means finding the current reimbursement rule, preserving its conditions, and explaining it clearly.

---

∙