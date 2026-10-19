---
title: "EP229: 8 Chunking strategies for RAG-based agents"
source: "https://blog.bytebytego.com/p/ep229-8-chunking-strategies-for-rag?utm_source=post-email-title&publication_id=817132&post_id=220736007&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-10-17
created: 2026-10-19
description: "Which chunking strategy are you running in production?"
tags:
  - "clippings"
---
## The all-in-one intelligent cloud (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!3rxF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2e1d608c-f75c-44a5-81cd-6f92a7d55890_1600x840.png)

*Y* our app, live in seconds, for free. Railway’s push-button compute, storage, and networking is available immediately upon sign-up.

Humans and agents alike operate on one vertically integrated system including hardware, software, and a prompt-to-production experience.

Sign up with the link below for free cloud credits and let your agents cook.

---

This week’s system design refresher:

- How to Test Your Code (Even When AI Writes It)
- 8 Chunking strategies for RAG-based agents
- Google Translate: The Ideas Behind Neural Translation
- Agent Skills, Clearly Explained
- PostgreSQL versus MySQL

---

## How to Test Your Code (Even When AI Writes It)

![](https://www.youtube.com/watch?v=aVRjFZM23ak)

---

## 8 Chunking strategies for RAG-based agents

![](https://substackcdn.com/image/fetch/$s_!9-Hk!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88462ca4-b0a1-4441-9537-59dae9d5ef65_2484x3002.png)

1. Fixed-Size: cuts text every fixed number of tokens, with a small overlap.
2. Recursive: splits on paragraphs first, falling back to lines then words and characters only when a piece is still too big.
3. Document-Based: splits wherever the document already marks a break, a heading, a chapter, an HTML tag, so a markdown file becomes one chunk per section on its own.
4. Semantic: embeds each sentence, checks its similarity to the one before it, and starts a new chunk when that similarity drops. This finds real topic shifts instead of guessing by length.
5. LLM-Based: asks an LLM to rewrite the text as standalone propositions, one idea per line, and turns each into a chunk, high quality but expensive across a large corpus.
6. Agentic: an AI agent reads each document, decides what it is (code, contract, table), and picks the chunking method for that file instead of one rule for everything.
7. Late Chunking: runs the full document through an embedding model, then applies normal split boundaries and mean-pools within each boundary to create chunk embeddings.
8. Hierarchical: breaks the document into layers, sections, paragraphs, then sentences

Over to you: which chunking strategy are you running in production?

---

## Google Translate: The Ideas Behind Neural Translation

A simplified illustration of common techniques. Not an exact map of Google Translate’s current system.

![Image](https://substackcdn.com/image/fetch/$s_!PWTF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc83631a3-ecd6-41ea-94a0-541f02b8908f_2484x3002.png)

- Detect language. A tiny classifier predicts the source language in milliseconds.
- Tokenization. A BPE tokenizer splits the text into subword tokens, so the model can handle any word in any language.
- Add target token. The model can handle every language pair. A special token like <2es> is prepended to the token sequence to steer the output toward Spanish.
- Encoder. The tokens pass through Transformer layers. The output is a sequence of vectors, corresponding to each input token.
- Decoder. Then the decoder part of the Transformer can predict the probability distribution for the next token conditioned on the encoded vectors.
- Beam search. Instead of greedily picking one token at a time, beam search uses the decoder to keep several candidate translations during generation. The final output is the one with the highest probability.

Over to you: Do you think AI labs and frontier models will make services like Google Translate obsolete?

---

## Agent Skills, Clearly Explained

Why do we need Agent Skills? Long prompts hurt agent performance. Instead of one massive prompt, agents keep a small catalog of skills, reusable playbooks with clear instructions, loaded only when needed.

![Image](https://substackcdn.com/image/fetch/$s_!YWY0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f3431f7-a501-473e-9ad0-5dfd0861d3c3_2360x2960.png)

Here is what the Agent Skills workflow looks like:

1. User Query: A user submits a request like “Analyze data & draft report”.
2. Build Prompt + Skills Index: The agent runtime combines the query with Skills metadata, a lightweight list of available skills and their short descriptions.
3. Reason & Select Skill: The LLM processes the prompt, thinks, and decides: “I want Skill X.”
4. Load Skill into Context: The agent runtime receives the specific skill request from the LLM. Then, it loads SKILL. md and adds it into the LLM’s active context.
5. Final Output: The LLM follows SKILL. md, runs scripts, and generates the final report.

By dynamically loading skills only when needed, Agent Skills keep context small and the LLM’s behavior consistent.

Over to you: What skills would you find most useful in agents?

---

## PostgreSQL versus MySQL

Built using the C language, PostgreSQL uses a process-based architecture.

![Image](https://substackcdn.com/image/fetch/$s_!h8d0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5f67fe5-0efa-4fc6-98da-d176b60b1a92_2508x3000.jpeg)

You can think of it like a factory with a manager (Postmaster) coordinating specialized workers. Each connection gets its own process and shares a common memory pool. Background workers handle tasks like writing data, vacuuming, and logging independently.

MySQL takes a thread-based approach. Imagine a single multi-tasking brain.

It uses a layered design with one server handling multiple connections through threads. The magic happens using pluggable storage engines (such as InnoDB, MyISAM) that you can swap based on your needs.

Over to you: Which database do you prefer?

---

∙