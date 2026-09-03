---
title: "Why Your RAG System Is Only as Good as Its Translator Model"
source: "https://blog.bytebytego.com/p/how-to-shrink-a-language-model-without?utm_source=post-email-title&publication_id=817132&post_id=212751164&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-09-02
created: 2026-09-03
description: "In this article, we’re going to look at how this embedding model works in an RAG setup and what makes it such a critical part of the system."
tags:
  - "clippings"
---
## A CIO on the data foundation AI agents need (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!8CU_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd462d195-c83f-4421-b27e-3c4024ba7f0d_1200x1200.jpeg)

The CIO of GlobalFoundries had a straightforward view of it: you don’t get AI agents until the data underneath them is real-time and governed.

So he rebuilt that layer first — one platform carrying data across fabs on three continents, with identity, permissions, and audit trails handled once instead of per project. The agents followed, across IT, procurement, and other business functions.

Join us on September 10 to hear how he did it, and get your questions answered live.

---

RAG, or Retrieval-Augmented Generation, is helping a lot of companies build chatbots specific to their requirements. However, the success of any such RAG system depends on the quality of the embedding model (the model that helps translate words into numbers) that is used by the RAG system.

Consider the example where a particular product’s documentation specifies that annual subscriptions can be refunded only within 30 days. A chatbot built using RAG is supposed to answer customer queries based on this support documentation. However, when a customer asks whether a subscription bought 45 days ago can be refunded, the chatbot confidently answers “yes”.

Why did the chatbot make a mess of this seemingly simple question?

The answer lies in the behaviour of the embedding model, which is kind of a translator for AI. This model controls the answer-searching process and is different from the language model that generates the actual answer. No matter how good the language model might be, it cannot give correct answers if the embedding model doesn’t do its job properly.

In this article, we’re going to look at how this embedding model works in an RAG setup and what makes it such a critical part of the system. Here’s what we will cover:

- Why a RAG system searches before it answers
- How embeddings make it possible to search by meaning
- Why related information is not always the right information
- Why a better language model cannot repair bad retrieval
- What makes an embedding model suitable for a RAG system
- How to compare embedding models without trusting benchmark scores blindly
- Choosing between commercial APIs and locally run models
- Why changing the embedding model later becomes expensive
- How Matryoshka embeddings offer more control over vector size

![](https://substackcdn.com/image/fetch/$s_!tiup!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bd77db5-9930-455b-bc89-d4431999e49e_2694x1592.png)

## Why a RAG System Searches Before Answering

A generic language model’s knowledge depends on what it was taught during training. You can’t expect such a model to know about a company’s private documents, policies, or internal source code. It won’t even know about the company’s latest information that might have been published after the model was trained. Technically, it’s quite costly to retrain a language model every time there’s a change in the information.

This is where RAG helps. It separates the ability to generate language from finding relevant details from a pool of stored knowledge. While the language model handles the understanding and writing parts, the external knowledge collection contains the actual information that should be used for writing the answers.

![](https://substackcdn.com/image/fetch/$s_!ZZMv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b72f142-66e8-489a-bbb5-901fa3484eef_2856x1778.png)

RAG works in two different phases: indexing and retrieval.

During the indexing phase, the system prepares the documents:

- It collects documents from various sources (files, websites, databases, etc.).
- It extracts their text.
- It divides the text into smaller passages known as chunks.
- It sends each chunk into an embedding model.
- It stores the resulting vector with the original text and metadata.

![](https://substackcdn.com/image/fetch/$s_!0_bn!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9030c35c-b3c1-407f-9e47-7917c15e3c29_2258x1608.png)

The metadata may contain details such as the document title, publication date, language, version, and so on.

During the retrieval phase, the system follows the following steps:

- It sends the question through the same embedding model.
- It searches for document vectors that are close to the question vectors.
- It retrieves a small number of chunks. For example, the best 5 chunks or something like that.
- It filters and reranks those chunks, placing them inside the language model’s prompt.
- Finally, the language model writes an answer using the prompt that was provided.

![](https://substackcdn.com/image/fetch/$s_!_Yi4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36469121-3c9c-45d3-bf74-87e17d73a3ee_2696x1644.png)

The main takeaway from all this is that RAG doesn’t place the entire document collection into the model’s prompt. This is because doing so would exceed the model’s context limit and fill it with irrelevant information. It also increases costs and latency. The retrieval phase, led by the RAG’s embedding model, serves as the selection step, reducing thousands of passages to a small set for the language model to check.

## How Embeddings Make it Possible to Search by Meaning

An embedding is basically just a list of numbers that represents a piece of text. A real embedding might contain numbers such as 384, 768, 1024, or several thousand numbers.

![](https://substackcdn.com/image/fetch/$s_!iWE7!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80859fee-bbe4-4fd9-abf5-8088ebff967b_2408x1366.png)

These individual numbers don’t have simple labels describing their meanings. You cannot look at a particular value and say that this means “subscription” while another means “refund”. The overall meaning is distributed across the complete vector. Think of the vector as the coordinates of a point in a mathematical space. An embedding model is trained to place text with related meaning near each other within this mathematical vector space.

This is how the system can connect a term like “yearly plan” with “annual subscription”. It can also connect complex phrases like “get my money back” with “receive a refund”. In contrast, a keyword search struggles when a question and the document use different words to explain the same concept. But an embedding model tries to compare the ideas present within the text rather than just the vocabulary. Common techniques behind this are cosine similarity, dot product, and Euclidean distance. In a nutshell, the goal of an embedding model is to produce a mathematical score that indicates how close two vectors are to each other.

The embedding model often returns the first k results. This is known as top-k retrieval. For example, if k is 5, the retrieval returns the top 5 highest-ranked chunks.

Embedding models also support asymmetric retrieval where the query and document have different forms. The query may be a short question. But the matching document is a longer explanatory passage. For example, the query could be something like: “Can an annual subscription be refunded after 6 weeks?” The answer passage is a statement like: “Annual subscriptions can be refunded within 30 days.”

An embedding model trained to compare similar sentences may not perform as well as a model that is trained to connect questions with the relevant passages. To summarize, the embedding model defines what the RAG system considers similar.

## Why Related Information is not Always the Right Information

An embedding model is trained to identify semantic similarity. But a RAG system requires something a bit more strict. It needs to find passages that might contain the information needed to answer a specific question. The problem is that a passage can be related to the question without clearly answering it.

For example, a customer asking how long a refund takes might receive a passage explaining who qualifies for the refund. Both these pieces of information concern refunds, but only one talks about the actual processing time. See the diagram below that shows the concept of semantic search space.

![](https://substackcdn.com/image/fetch/$s_!QDKL!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc0152b6-129d-4fe4-8e52-551b5119c32a_3194x1778.png)

Multiple failure modes can pop up in this situation:

- **Similar Subject, Different Question:** The query asks “How long will an approved refund take to arrive?” The retrieved passage says: “Purchases can be refunded within 30 days.” The passage is relevant to refunds but does not answer the timing question.
- **Same Words, Different Entity:** The query asks “how can the billing address be changed.” The retrieved passage explains how to change the account’s email address. Both talk about changing account details. But they refer to completely different fields.
- **Negation:** Consider the two passages: “Administrators can delete archived projects”, and “Administrators cannot delete archived projects”. Most of the words are identical. This means their embeddings may be close. But as you can see, they have opposite meanings.
- **Versions and Dates:** A knowledge base may contain an old policy and its replacement. The text may be almost identical except for a date, limit, or price. Embeddings cannot automatically know which document is authoritative. Metadata filters or version management rules may need to exclude outdated content explicitly.
- **Numerical Identifiers:** The two sentences “Annual subscriptions can be refunded within 30 days” and “Annual subscriptions can be refunded within 60 days” are semantically very similar. But there is a difference in one number, which determines the final answer.
- **Domain-specific Meanings:** General models can misunderstand special vocabulary. For example, “capture” has one meaning in an ordinary language and a specific meaning in payment processing. Similarly, the word “port” can refer to networking, hardware, or moving software between platforms. The best model for general web text may not be the best model for legal contracts, medical reports, financial documents, or source code.
- **Multi-part questions:** A customer may ask multi-part questions. For example, there could be a question like “Can I cancel the subscription, and how long will the refund take?” The answer for this requires at least two passages. One might explain eligibility for cancellation. Another might explain processing time. The model that retrieves only one subject may produce an incomplete answer.

## Why a Better Language Model Cannot Repair Bad Retrieval

In an RAG system, the language model just sees the user’s question and the selected passages. It doesn’t see every document that might have been stored in the vector database.

For example, if the annual refund policy document is not retrieved, the language model won’t have any idea about the missing information. A more capable language model may recognize that the retrieved information doesn’t contain the answer. This is useful because it can at least choose not to respond with invalid information. However, this failed retrieval scenario also creates several possible outcomes:

- The model answers from its general training knowledge.
- It incorrectly applies a related passage.
- It might invent a plausible rule.
- It says that the available information is insufficient.
- It combines conflicting passages incorrectly.

A prompt such as “answer only from the supplied documents” can reduce unsupported answers. But it cannot make the correct document magically appear.

This is why testing and debugging are so critical during the development of an RAG system. Developers need to inspect retrieved chunks before changing prompts or swapping language models. It takes a lot more time to solve a retrieval problem in the generation phase.

## What Makes an Embedding Model Suitable For a RAG System

The most important concern when choosing an embedding model should be retrieval performance. The model should be really good at connecting short questions with longer sentences that might contain the answers.

The following characteristics matter:

- **Domain and Vocabulary:** The model should understand the language used by the documents and users. Testing should include the use of abbreviations, internal product names, technical terms, and so on. If a company calls annual subscriptions “yearly plans” in the UI, but “annual contracts” in their legal documents, the model should be able to connect those expressions.
- **Language Support:** A multilingual model is critical when documents, queries, or both may use different languages. The model should be able to connect a query in one language with an answer found in another language.
- **Embedding Dimensions:** Embedding dimension is the number of values in each stored vector. Larger vectors preserve more information. But size does not guarantee better retrieval. Also, dimensions have a direct impact on raw storage costs.
- **Maximum Input Length:** A model with a limit of 8192 tokens can embed much longer text than one limited to 512 tokens. But it doesn’t mean each document should become one big chunk. A long chunk might discuss multiple things like refunds, cancellations, billing addresses, and so on. A focused question may match it less precisely than it would match a smaller passage specific to the relevant policy.
- **Model and Query Speed:** Indexing speed determines how much time it takes to embed the document collection. Query speed affects every user request. Some important metrics to consider are the number of chunks embedded per second, query-embedding latency, CPU or GPU requirements, memory use, and the cost of running the model. A model that gains a bit of retrieval quality at the cost of a substantial increase in latency may not be the right choice.
- **Deployment Requirements:** Embedding dimensions determine the size of each output vector. Model size determines how much memory and computation are needed to run the embedding model. These are key details required to plan for the model’s deployment.

## Why Changing the Embedding Model Later Is Expensive

Each embedding model creates its own vector space, which is unique to the particular model. This means that the embeddings produced by Model A have no dependable relationship with the embeddings produced by Model B.

Consider an example where all document chunks are embedded using Model A. If we suddenly start to embed the incoming questions using Model B, the system will end up comparing vectors from incompatible spaces. It will be like an apples-to-oranges comparison. Even if both models output the same number of dimensions, the numbers can mean very different things.

This means that the entire corpus of documents needs to be re-embedded using Model B. In other words, migrating an embedding model needs a lot more than just running the new model. It involves the following steps:

- Generate new vectors for every chunk.
- Build a new vector index.
- Apply the correct metadata and access permissions.
- Keep new or modified documents synchronized during the migration.
- Test retrieval quality.
- Move production searches to the new index.
- Retain a rollback path if the new system performs poorly.

![](https://substackcdn.com/image/fetch/$s_!29Wl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1faf30f0-81f1-421e-9379-e4f6f5ce2ad1_3216x1590.png)

The costs of the migration process include embedding API charges or GPU time, index-building time, paying for temporary duplicate storage, data transfer costs, evaluation work, and operational risk.

The migration also changes rankings. For example, a model with a higher benchmark score may perform worse on the application’s specific domain terminology. Therefore, application-specific testing is extremely important to make sure that the answer quality has not gone down.

A few design choices can make it safer to implement future changes:

- The original chunks should remain the source of truth. A vector database should not be the only place where processed text exists.
- Each chunk should have a stable identifier and a content hash. The hash helps determine whether the text changed and needs a new embedding
- Embedding records should include:
	- Model name
		- Model version or revision
		- Embedding dimension
		- Query and passage format
		- Normalization method
		- Chunking version
		- Creation time
- A new model should receive a new index or vector field. Its embeddings should not be mixed with old embeddings.

To summarize, a safe migration resembles the classic blue-green deployment approach where the old index continues to serve production traffic even as a new index is built in parallel.

To be clear about things, changing the embedding model is just one of the operations that requires a rebuild. Changing the chunking strategy, parser, cleaning rules, prefixes, or stored dimensions may also require the documents to be rebuilt.

## How Matryoshka Embeddings Offer More Control Over Vector Size

A basic embedding model produces a fixed-size vector. Its dimensions are meant to work together. We cannot delete most of these dimensions without severely reducing the quality of retrieval.

In contrast, a Matryoshka model is trained differently. During training, such a model is configured to produce useful representations at different prefix lengths, such as the first 256, 512, 1024, and full dimensions.

While the initial dimensions contain a useful coarse representation, the later dimensions pack more detailed information. For example, in a 1024-dimensional embedding, the first 256 dimensions can contain a useful small representation. Similarly, the first 512 dimensions contain a more detailed representation. At the end, all 1024 dimensions provide a complete representation.

There are three practical storage designs to support Matryoshka models:

- **Storing the smaller vector:** The system creates an embedding. It then keeps the first 256 dimensions and normalizes the shortened vector if needed. Only these dimensions are stored. This reduces the index size and overall search cost. However, the discarded dimensions are gone forever. If we want to migrate the system to a larger dimension, we need to generate the embeddings again.
- **Storing the full vector with a smaller search representation:** The system stores the complete vector in secondary storage. But it places a smaller prefix in the fast vector index. This supports future flexibility. We can build a larger index from the stored vectors without the need to rerun the model.
- **Storing smaller and full vectors for two-stage retrieval:** The system makes a search on the entire corpus using just 256-dimensional vectors (the reduced dimension). It then retrieves the full vectors for the best candidates and compares them precisely. This brings down the cost of the large initial search. But it retains full precision for the shortlisted candidates.

![](https://substackcdn.com/image/fetch/$s_!Sbtb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe1c71ec9-cfff-4d2d-852c-da408388c2ae_3934x1808.png)

To be clear, Matryoshka embeddings don’t solve incompatibility between different models. They mainly help support different usable sizes within a model’s vector space. Switching to another embedding model still requires the entire re-embedding process we talked about earlier.

## Conclusion

As we discussed, an RAG system can’t generate a reliably grounded answer unless it first retrieves the details required for that answer. This makes an embedding model the most important part of an RAG setup.

This doesn’t mean that other things are not important. Retrieval quality of the RAG system also depends on various factors such as:

- The existence of the correct documents
- How well the parsing process keeps their content intact
- How the documents are divided into chunks
- How versioning is managed
- Metadata filters and their working
- How a reranker improves the candidate list

Nevertheless, the embedding model remains central because it helps decide which information enters the language model’s context. It acts as the first major relevance decision in a typical RAG pipeline. The key lesson is to choose an embedding model that retrieves the correct evidence for the questions at an acceptable cost and speed.

---

∙