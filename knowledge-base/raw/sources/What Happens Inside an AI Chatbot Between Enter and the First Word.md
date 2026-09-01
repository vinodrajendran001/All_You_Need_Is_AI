---
title: "What Happens Inside an AI Chatbot Between Enter and the First Word?"
source: "https://blog.bytebytego.com/p/what-happens-inside-an-ai-chatbot?utm_source=post-email-title&publication_id=817132&post_id=213193896&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-08-31
created: 2026-09-01
description: "In this article, we are going to look at this entire journey in detail."
tags:
  - "clippings"
---
## \[Webinar\] How to stop babysitting your agents (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!7jNZ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbacaf13f-5f7e-4f9e-bbb3-b33d74be1d8b_1600x900.png)

Agents can generate code. Getting it right for your system, team conventions, and past decisions is the hard part. You end up wasting time and tokens in the correction loops.

More MCPs, rules, and bigger context windows give agents access to information, but not understanding. The teams pulling ahead have a context layer to give agents exactly what they need for the task at hand.

Join us for [a FREE webinar on Sep 2](https://go.bytebytego.com/Unblocked_083126) to see:

- Where teams get stuck on the AI maturity curve and why common fixes fall short
- How a context layer solves for quality, efficiency, and cost
- Live demo: the same coding task with and without a context layer

If you want to maximize the value you get from AI agents, this one is worth your time.

---

When you type a follow-up question into an AI chat and press Enter, nothing happens for a second or two. Then the answer appears in a quick succession of words. It appears much faster than what the initial pause indicated.

This pause is not dead time. In a typical LLM, a single message passes through roughly a dozen distinct stages before a reply starts to appear. Two very different kinds of computing work happen in the background to make this possible. Some key points about this journey are as follows:

- The model never receives the message as it was typed.
- It has no memory of the conversation. The history on screen is rebuilt from scratch every turn.
- It shares a machine with strangers, and the group it lands in can affect the reply.
- Once a word has been sent, the model cannot take it back.

In this article, we are going to look at this entire journey in detail. Here’s what we will cover:

- How is the input to the model assembled?
- Why is every input message to the model independent?
- Performing safety checks on the input
- How does the model understand the words?
- How is the model shared across multiple conversations?
- Prefill and decode steps
- Caching the existing calculations
- Streaming and guardrails
- How does the model run various tools?

![](https://substackcdn.com/image/fetch/$s_!KVoE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcbefb0cb-a119-4035-b528-cf881e166395_3872x1734.png)

*Disclaimer: This post is based on publicly shared details from various sources. References at the end. Please comment if you notice any inaccuracies.*

## How the Input to the Model is Assembled?

The first key point to understand is that the sentence typed into the box is not the exact thing that reaches the model. What reaches the model is a document assembled around that sentence before the request is sent.

This document contains several ingredients, which are as follows:

- A system prompt, which is a block of instructions written by the LLM provider. These instructions tell the model how to behave during the conversation.
- Definitions of any available tools, describing what each one does and what inputs it accepts.
- Anything stored as memory from earlier sessions.
- Documents pulled from a knowledge base in cases where retrieval is the key.
- The full conversation so far.
- Finally, the new message.

The process of deciding what goes into this document in what order, and what gets left out, is a discipline in its own right known as context engineering. It is not a simple matter of filling a container. Models have a finite attention budget, and every token added draws it down.

Accuracy degrades as input grows longer, even on tasks that are quite simple. The decline is gradual. A longer prompt does not break anything outright, but the underlying precision falls away.

The approach used towards this discipline of context engineering leads to scenarios where two products built on the same underlying model, given word-for-word the same question, return different answers. The model might be identical, but the document wrapped around the question is not.

Different providers also differ in when they gather the material for the document. Some retrieve everything up front. Others hand the model lightweight references, file paths, or stored queries, and let it pull in what it needs while working. The first is faster, and the second wastes fewer tokens on material that might be irrelevant.

![](https://substackcdn.com/image/fetch/$s_!Fq-K!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff86daf2c-0c71-4cd4-8a16-589b8e3bb0fe_3176x2198.png)

## Why is Every Input Message to the Model Independent?

The models are stateless by design, meaning they retain nothing between messages. Each request arrives with no recollection of what came before. In other words, the conversation that we see on screen is reconstructed and resent in full every single time.

The maths related to this gets quite uncomfortable. Consider a product with a thousand-token system prompt, where each message and each reply runs about a hundred tokens.

- Turn one processes about 1,100 tokens.
- Turn two processes about 1,300.
- By turn three, we have about 1,500.
- By turn twenty, we might have closer to 4,900.

Though output tokens cost more than input tokens, input volume compounds on every turn while output stays roughly constant. This is why input usually dominates the total spend in any conversational product despite being the cheaper of the two.

The naive approach is to resend everything, but it works well only for short exchanges. Once the conversation outgrows the context window, it stops being viable. There are a few refinements that can help:

- The simplest one drops the oldest turns. This doesn’t cost much in latency and loses whatever was dropped.
- A more careful version summarises the conversation and restarts with the summary. This helps preserve decisions and open questions while discarding things like raw tool output that nobody needs to see twice.
- The third one stores material outside the context window entirely and retrieves it when it becomes relevant.

Long chats get slower and more expensive because every turn has to reprocess everything that came before it. The assistant eventually loses details because some details get trimmed or condensed. Also, editing an earlier message rewrites what the model treats as having happened.

![](https://substackcdn.com/image/fetch/$s_!-Fe5!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F202fb3d3-eb09-4ef9-b91c-d5700243f168_2900x1964.png)

## Performing Safety Checks on the Input

Before the generation of the answer starts, the assembled document passes through a separate, smaller model trained to judge whether the request should proceed. Think of it like a safety layer.

The key point to note here is the separation in the design. This safety layer is a distinct system from the assistant, which means that it can be retrained, tuned, and monitored on its own schedule without any impact on the main model. It can also do more than permit or block. It can route a request elsewhere, log it, or escalate it for review.

This separation costs time, which is evident in the pause that precedes the answer. Published figures from one production system put an earlier generation of these classifiers at roughly a 24 percent increase in compute, alongside a 0.38 percentage point rise in refusals of harmless requests. Both numbers were high enough to limit how widely the approach could be deployed.

The replacement uses a cascade, where a very cheap validation is used to screen all traffic. Only flagged conversations are sent to the expensive classifier. This brings the overhead down to around one percent and refusals of harmless queries to 0.05 percent.

## How the Model Understands the Words?

In the next step, the document gets converted into the units the model works with. These units are known as tokens, which are chunks of text that are generally smaller than a word but larger than a letter. Common words are often represented as a single piece, while rarer ones break into fragments.

Most modern systems build these chunks starting from raw bytes rather than characters, which guarantees that text in any writing system can be represented. As a working figure, one token averages around three-quarters of an English word.

There are two consequences due to this:

- The first is that cost and capacity vary by language. Research presented at a major machine learning conference measured the same text across translations and found token counts differing by as much as fifteen times. This is not just a matter of billing. Higher token counts also mean higher cost, slower processing, and less content fitting inside the same context window. Therefore, speakers of some languages get materially less usable space for an identical document.
- The second is that character-level questions can get awkward. Counting how many times a specific letter appears in a word means looking inside the chunks.

![](https://substackcdn.com/image/fetch/$s_!zewk!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe80ca9f7-89ad-4992-8fa1-f9a2a202b77f_4096x2264.png)

## How the Model is Shared Across Multiple Conversations

No model sits idle waiting for a request to arrive. In a typical setup, the token sequence joins a queue, and then a batch of other people’s requests running on the same hardware.

Why the need for this batching?

This is because while modern accelerators have enormous computing capacity, a great deal of their memory bandwidth is spent on loading model parameters rather than performing useful work on any single request. Loading those parameters once and applying them across many requests simultaneously is what makes serving affordable.

The naive version of batching collects a group of requests, runs them together, and waits for the entire group to finish before starting the next. This works when every response is a similar length. However, chat responses are not of similar length. Some might finish in ten words while others can run for a thousand. Therefore, the hardware might be partly idle waiting on the longest one.

A better approach schedules a request at the level of individual generation steps. As soon as one response finishes, a new request takes its slot rather than waiting for the group to clear. Benchmarks have demonstrated throughput improvements of up to 23 times over the naive method. Also, this approach improved median response times as well.

There is another strange consequence of sharing resources to generate answers. Identical requests can return different answers even with randomness switched off. This happens because the numerical operations involved are sensitive to the number of requests being processed together. In other words, sending the same prompt a thousand times to a large model might end up with 80 distinct completions.

## Prefill And Decode

This is the point where the pause and the typing separate.

Producing a reply happens in two phases with opposite characteristics

- The first reads the entire assembled document in one pass. Every input token is processed alongside every other. Therefore, this work runs in parallel and pushes the hardware on raw computation. This phase is the pause.
- The second phase produces output one token at a time. Each token depends on the one before it, so none of it can be parallelised. The limiting factor here is memory speed rather than computation, since every step reads back everything that has been computed so far. This phase is the steady typing.

The first phase scales with input length. This means a conversation twenty turns deep takes measurably longer to begin than the same question asked in a fresh window. The second phase runs at roughly the same rate regardless. In other words, the pause time increases as a chat continues, but the typing speed barely changes.

These two halves are measured separately:

- Time to first token covers everything up to the first visible output, including the queue wait time.
- Time per output token covers the gap between each token after that.

Total response time is calculated as approximately the first plus the second multiplied by the length of the reply.

A single very long input can delay generation for every other request in the batch. Splitting that long input into chunks and interleaving them with ongoing generation keeps everyone else’s output flowing. The trade-off is a slightly longer wait for the request that was split.

![](https://substackcdn.com/image/fetch/$s_!zkid!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19b484a1-44e0-4089-9c5c-f7b542725f4a_3680x1694.png)

## Caching the Existing Calculations

Why is the second phase quick at all, given that every token has to account for everything before it?

This is because that work is not repeated. The calculations produced while reading the input are stored and reused at each subsequent step.

This stored state is large. For a model in the 70-billion-parameter range holding an 8000-token conversation, it can run to a few gigabytes per request. A bunch of concurrent conversations can exceed the memory of an entire high-end accelerator before the model weights are even accounted for. In other words, the number of users a machine can serve is usually limited by this conversation state rather than by the model.

Early serving systems reserved one contiguous block of memory sized for the longest response a request might produce. A widely cited systems paper measured that cost and found sixty to eighty percent of the memory going unused. The fix involved a technique that operating systems have used for decades. This technique is to split the storage into small fixed-size blocks provided on demand. In this case, the wastage dropped below 4% and throughput improved by 2-4 times.

The same idea extends across turns. Since every message resends the same opening block, the computed prefix can be kept stored and reused instead of recalculated. Providers price this explicitly, with cached portions of a prompt often costing around a tenth of the normal input rate. Cache entries typically expire after a few minutes unless they are refreshed due to continued use.

This is why prompt structure follows a rule that stable content belongs at the top and changing content at the bottom. This is because a prefix that changes on every request cannot be reused effectively.

## Streaming And Guardrails

There are two things that happen during the response phase of the conversation.

Text appears word by word because it is sent as it is produced instead of being held until finished. This improves the perceived speed. Ordinary reading runs at something like six tokens per second, and production systems generate comfortably faster than that. Streaming lets reading start almost immediately instead of after a blank wait.

The second part is around safety checks. Many products run a safety check on output as well as input. A check of that kind has to read the finished response before it can judge it. By that point, the response is already on screen, and it is not possible to retract a word that has been displayed. Holding the response back until the check completes removes the benefit of streaming entirely.

There is no settled answer to this yet. Some systems use guards designed to evaluate output as it streams, token by token. Others read the model’s internal state during generation rather than waiting for finished text, which is cheap enough to apply.

## How Tools Are Run?

Everything so far describes a straight line from pressing Enter to the response. Once tools are involved, this straight line turns into a loop.

A model does not search the web, read a file, or query a database. It produces text requesting that one of those things happen, using the tool definitions included in the assembled document. The surrounding application recognises the request, carries it out, and puts the result back into the context.

The result is new input, which means the entire sequence runs again from the beginning. It is reassembled, checked, tokenized, queued, and run through both generation phases again. For example, a reply that involved three web searches made several complete round trips through everything described here. This accounts for why those replies take noticeably longer than ordinary ones.

The cost compounds sharply. Across a session of twenty calls with growing context, the earliest messages are paid for twenty times over. A two-thousand-token instruction block sent across two hundred calls accounts for four hundred thousand input tokens on its own, before any of the actual work.

![](https://substackcdn.com/image/fetch/$s_!C-Iv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F683e40f1-0b7d-4f83-96d6-0b5c0e68c7f2_3726x2804.png)

## Conclusion

The two seconds of delay now have a clear picture that we can understand.

- A fraction went to network travel and authentication.
- A larger fraction went to assembling the document and gathering whatever memory and reference material the product uses.
- A small fraction went to the input safety check, which cascaded designs now keep near one percent of compute.
- Tokenization was negligible.
- Some unknown portion of the delay went to queueing, depending entirely on concurrency.
- In a long conversation, the largest fraction goes to reading the input, which is the reason for the initial pause growing as the chat continues.
- Everything after that was the second phase, running at a rate that had barely changed since the first message.

The model receives a constructed document in which the typed message is the smallest component. It has no memory, so the conversation is rebuilt from scratch. This is why long chats slow down, cost more, and lose details.

References:

- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [How continuous batching enables 23x throughput in LLM inference](https://www.anyscale.com/blog/continuous-batching-llm-inference)
- [Language Model Tokenizers Introduce Unfairness Between Languages](https://arxiv.org/abs/2305.15425)

---

∙