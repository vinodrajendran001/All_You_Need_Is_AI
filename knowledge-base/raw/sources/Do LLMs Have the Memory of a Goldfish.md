---
title: "Do LLMs Have the Memory of a Goldfish?"
source: "https://blog.bytebytego.com/p/do-llms-have-the-memory-of-a-goldfish?utm_source=post-email-title&publication_id=817132&post_id=215151303&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-09-15
created: 2026-09-16
description: "In this article, we will learn how LLMs handle memory so that they are useful to end users in performing complex tasks that require conversation and holding context."
tags:
  - "clippings"
---
## \[Webinar\] How to stop babysitting your agents (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!ajI7!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d29741c-9645-43c9-9103-4b75de979090_1600x900.png)

Agents can generate code. Getting it right for your system, team conventions, and past decisions is the hard part. You end up wasting time and tokens in the correction loops.

More MCPs, rules, and bigger context windows give agents access to information, but not understanding. The teams pulling ahead have a context layer to give agents exactly what they need for the task at hand.

[Join us for a FREE webinar on Sep 23](https://go.bytebytego.com/Unblocked_091526) to see:

- Where teams get stuck on the AI maturity curve and why common fixes fall short
- How a context layer solves for quality, efficiency, and cost
- Live demo: the same coding task with and without a context layer

If you want to maximize the value you get from AI agents, this one is worth your time.

---

An LLM can analyze a 100-page document, follow a complicated programming discussion, and refer back to something discussed several messages ago. However, as soon as we open a new chat where the earlier conversation is not present, it immediately forgets everything. It appears that LLMs have the memory of a goldfish.

This observation is indeed true. LLMs usually have no personal or persistent memory of previous interactions. So, how is it able to refer to what we’ve said in the past?

In truth, an LLM doesn’t remember a conversation like human beings do. However, it receives information about the conversation so far with each new message that we send to the LLM. All of this is handled by the application that is built around the model and not by the model itself. For example, a chat application might store messages, maintain summaries of earlier discussions, retrieve relevant memories, and maintain a user profile. It can then place some of that information in front of the model as needed. From the user’s perspective, the model appears to remember. But technically, the surrounding application is doing most of the remembering.

This difference between the model and the application around the model is the key to understanding LLM memory.

This design has important consequences. As a conversation grows, the application must keep processing more text, thereby increasing cost and latency. Eventually, the conversation ends up turning too large to fit inside the model’s context window. At that point, older information must be removed, summarized, or stored somewhere else.

In this article, we will learn how LLMs handle memory so that they are useful to end users in performing complex tasks that require conversation and holding context.

![](https://substackcdn.com/image/fetch/$s_!0eDu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44340ecb-27c9-4256-9827-845909b4f9a6_3948x1882.png)

## What Does “memory” Mean for an LLM?

In the context of LLMs, the word “memory” is used for several different things that should not be confused. Let’s look at each type in detail.

### Trained Memory

During training, an LLM learns patterns from enormous amounts of data. These patterns are encoded in billions of numerical values called parameters or weights.

This is why a model can explain JavaScript, recognize a common historical event, or write an email without receiving that knowledge in the current prompt.

But this is not personal memory. If a user tells the model, “My preferred programming language is TypeScript,” a normal API response does not rewrite the model’s weights. The base model does not permanently learn that fact from the conversation.

#### Working Memory

The model’s temporary working memory is its context window. This contains everything the model can consider while generating its current response.

![](https://substackcdn.com/image/fetch/$s_!6GJS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5fb5a60-ebad-461f-a5cf-5512bb643165_3342x1554.png)

It can include:

- System and developer instructions
- The current user message
- Previous messages in the conversation
- Retrieved documents
- Tool descriptions and tool results
- Saved user preferences
- Summaries of older conversations
- Space required for the model’s output

The context window is closer to a desk than a human memory. The model can work with whatever documents have been placed on the desk. Once the desk is cleared, the model cannot recover those documents unless the application places them there again.

### Persistent Application Memory

Persistent memory normally lives outside the model in a database, file, vector store, or profile service. When the model needs that information, the application retrieves it and inserts it into the current context.

Therefore, the model doesn’t possess persistent memory. It receives persistent information from another system.

---

## Build and scale a winning AI agent strategy (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!SJtL!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21fb72c6-1e79-42e0-8804-9217f2102310_1080x1080.png)

Shipping agents to production is the easy part. Keeping them reliable, governable, and improving over time is where most enterprise AI programs stall.

How do top teams do it? They use an Agentic Operating Model (AOM), a step-by-step framework for aligning people, process, and technology so enterprise agents improve as they scale.

In LangChain’s latest guide, you’ll learn:

- Why AI agents don’t break like traditional software
- The engineering stack that covers the entire agent lifecycle
- Shifting from “build and deploy” to “operate and continuously improve”

---

## What Happens During a Basic API Call?

Consider the simplest possible API request:

```markup
{
  “messages”: [
    {
      “role”: “user”,
      “content”: “My name is Adam.”
    }
  ]
}
```

The model might answer: “Nice to meet you, Adam.”

Suppose the next request contains only this:

```markup
{
  “messages”: [
    {
      “role”: “user”,
      “content”: “What is my name?”
    }
  ]
}
```

The model can’t reliably answer because the second request doesn’t include the name. The earlier request has already finished. And there is no private diary that exists inside the model that is kept updated.

For the conversation to work, the application must send the earlier exchange again:

```markup
{
  “messages”: [
    {
      “role”: “user”,
      “content”: “My name is Adam.”
    },
    {
      “role”: “assistant”,
      “content”: “Nice to meet you, Adam.”
    },
    {
      “role”: “user”,
      “content”: “What is my name?”
    }
  ]
}
```

Now the model answers “Adam” because the name is visible in the current input.

Most model providers have a stateless Messages API that requires the conversation history to be supplied for a multi-turn conversation.

![](https://substackcdn.com/image/fetch/$s_!dHMu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc23a7df2-9066-4600-abac-d43b8c412914_2886x1498.png)

## Does Every API Call Really Start From Zero?

A new model invocation doesn’t typically start without any knowledge. The model still has several things:

- Its trained weights
- Its general language abilities
- Knowledge acquired during training
- Safety and behavioral instructions supplied by the platform
- Everything included in the current context

What it lacks is an automatically updated memory of this particular user or conversation.

A better way to put it is that every response is generated from the model’s existing weights plus the context made available for that response. Information from the conversation history is not available unless the surrounding system carries it forward.

Some APIs offer server-managed conversation state. In such a case, we don’t need to resend every message manually. We can provide a conversation identifier, and the server locates the previous messages based on that identifier to reconstruct the necessary context. This makes the API easier to use, but it doesn’t mean that the model has developed a personal memory.

## How AI Chatbots Create the Illusion of Memory

Suppose a conversation contains five user messages and five assistant responses.

When the user sends the next message, the application may construct an input that contains the following details:

```markup
System instructions

User message 1
Assistant response 1

User message 2
Assistant response 2

User message 3
Assistant response 3

User message 4
Assistant response 4

User message 5
Assistant response 5

New user message
```

The model receives all of this as one large input. For example, in the earlier conversation, the user may have mentioned a database problem, selected PostgreSQL, and asked for TypeScript examples. Therefore, it can continue the answers based on this path in a more natural manner.

To the user, this might feel like the model has remembered things from earlier. However, from the perspective of the model, those details are simply present in the text that is being processed right now. We can’t simply call it “fake memory” because there is real continuity at the application level. A better term for this is reconstructed memory or context-based memory.

## The Context Window is a Working-Memory Budget

A context window of an LLM is measured in tokens. Tokens are small pieces of text. A short word may be one token, while a longer or unusual word may be split into several tokens.

The context window normally contains more than the visible conversation. It may also contain hidden instructions, tool definitions, search results, documents, and space for the answer. Imagine a hypothetical model with a 100K-token context window. An application might need to fit the following into that space:

- System instructions: 3,000 tokens
- Tool definitions: 8,000 tokens
- Conversation history: 55,000 tokens
- Retrieved documents: 20,000 tokens
- Current question: 1,000 tokens
- Remaining response budget: 13,000 tokens

Once the available space is exhausted, the application can’t just keep adding information indefinitely. It must remove, compress, or replace something.

A large context window also doesn’t guarantee perfect recall. As the amount of information grows, it can become harder for the model to differentiate important facts from irrelevant, repetitive, or contradictory material. This degradation is also known as “context rot”. We need to select useful context even if we have a very large context window at our disposal. Therefore, the context window is both a capacity limit and an attention-management problem.

## Why Long Conversations Become Expensive

LLM APIs commonly charge for the number of input and output tokens processed. Let’s say each completed conversational round adds approximately 1000 tokens.

- Request 1 processes approximately 1,000 tokens.
- Request 2 processes approximately 2,000 tokens.
- Request 3 processes approximately 3,000 tokens.
- Request 10 processes approximately 10,000 tokens.

Across those ten requests, the application has processed approximately 55K tokens of input.

The visible conversation contains only about 10,000 tokens, but earlier parts have been processed repeatedly. A long system prompt, large tool definitions, and retrieved documents can increase this cost even further.

Longer contexts also increase latency. This is because more information needs to be processed before the model starts to answer.

Techniques like prompt caching can help alleviate costs, but they don’t create memory.

Providers can cache a repeated prefix such as the system prompt and previous conversation history. When the next request begins with the same content, the provider may reuse previously computed information. This can reduce cost and latency. However, cached tokens consume part of the context window. Caching merely changes how efficiently repeated context is processed. It doesn’t give the model unlimited memory.

Prompt caching is therefore an optimization, not a memory architecture.

## What Happens When the Context Window Fills Up?

There is no single universal behavior that LLMs perform when the context window fills up. Depending on the API and application, several things may happen.

- The API may reject the request because it is too large.
- The application may remove the oldest messages.
- A chat product may manage history using a rolling window.
- The system may replace old material with a compact summary.
- Some APIs also provide server-side compaction mechanisms.

Compaction is carrying forward important state in a smaller representation so that long-running interactions continue with lower context usage. This means a very long chat may not contain every original sentence in its active context. The model may instead receive something like:

Conversation summary:

The user is building an invoice service in TypeScript.

PostgreSQL was selected as the database.

The API uses Express and Prisma.

The current problem concerns duplicate invoice creation.

Previous attempts involving application-level checks failed under concurrency.

The summary preserves the central state while discarding greetings, repeated explanations, abandoned ideas, and low-value details. The tradeoff is that summarization is lossy. A small detail that seemed unimportant during summarization may become important later.

## The Main Techniques to Extend Memory

Real applications usually combine several techniques to extend memory instead of relying on one. Let’s look at a few techniques in detail.

### Sliding-window Memory

A sliding window keeps only the most recent portion of the conversation. When new messages arrive, the oldest ones are removed.

For example, the application might always retain:

- The system instructions
- The latest 20 conversational turns
- The current user message

![](https://substackcdn.com/image/fetch/$s_!dtos!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe930c454-b3ce-4f13-9a50-dbaea4295f63_3172x1456.png)

This approach is simple, fast, and predictable. It works well when recent messages matter much more than older ones.

Its weakness is that once an old fact leaves the context window, it disappears. If the user mentioned an important requirement 30 turns earlier, the model may no longer be able to address it.

### Conversation Summarization

Summarization periodically compresses older messages into a much shorter description. The summary stays in the context while the original messages are removed.

A common structure is:

- System instructions
- Conversation summary
- Recent unsummarized messages
- Current user message

![](https://substackcdn.com/image/fetch/$s_!Oi_K!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F060bde03-14bc-4392-82b1-701b90b599c4_3638x1548.png)

This helps preserve the general direction of the conversation much more efficiently than retaining every original message.

However, a summary is more of an interpretation. It omits nuance, simplifies uncertainty, or accidentally turns an assumption into a fact. If we repeatedly summarize previous summaries, it can gradually distort the meaning of the conversation, much like repeatedly copying a photocopy. Therefore, it’s a much better approach to store important facts separately rather than trusting them to be retained in a simple narrative summary.

### Structured Entity Extraction

Instead of remembering the conversation as prose, the application can extract specific facts into structured fields. For example:

```markup
{
  “preferred_language”: “TypeScript”,
  “database”: “PostgreSQL”,
  “framework”: “Express”,
  “current_project”: “invoice service”,
  “confirmed_decisions”: [
    “Use optimistic concurrency control”,
    “Do not introduce Redis”
  ]
}
```

This is more reliable than searching through a long summary when the application needs exact project state.

Structured memory is really useful for the following types of information:

- User preferences
- Names and identifiers
- Confirmed technical decisions
- Current tasks
- Workflow status
- Dates and deadlines
- Product configuration

However, structured entity is doesn’t work well for subtle, narrative information that cannot be expressed neatly into predefined fields.

### Vector-store-backed Memory

In this approach, a vector store supports semantic retrieval. Instead of putting the entire conversation history into every request, the application divides past conversations into small pieces and creates an embedding for each piece.

![](https://substackcdn.com/image/fetch/$s_!qCk3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa63cbe78-13af-4d59-86ec-30efab5f306b_3952x1674.png)

An embedding is a numerical representation of meaning. This means that texts concerning similar ideas receive similar representations even when they don’t use exactly the same words.

For example, let’s say the user asks: “Why did we reject Redis for the invoice service?” The memory system searches for past passages semantically related to “Redis,” “invoice service”, and “rejected architecture decisions.”

It may retrieve information such as “we decided against Redis because the deployment environment does not provide a managed Redis service, and PostgreSQL advisory locks already cover the required coordination.”

Only the retrieved passage is added to the current context. Here’s how the process works roughly:

- Store selected pieces of earlier conversations.
- Convert those pieces into embeddings.
- Convert the new question into an embedding.
- Find semantically similar memories.
- Filter and rank the candidates.
- Insert the best candidates into the model’s prompt.

This doesn’t enlarge the context window. It selects which memories deserve space inside it.

However, vector retrieval can also sometimes fail. It may retrieve something similar but irrelevant. It can miss a memory because it was phrased strangely. It can also come up with an outdated decision. Metadata such as user ID, project ID, date, and memory type is therefore essential to make sense of this data.

### Long-term User Profiles

A long-term profile stores durable facts that may be useful across many conversations. For example, this could include things like:

- The user generally prefers beginner-friendly technical explanations.
- Examples should use TypeScript where practical.
- Explanations should use complete paragraphs rather than fragmented bullets.

A profile should contain stable preferences, not every passing statement. For example, “I am testing Python today” is probably session information. On the other hand, “I use Python for all data projects” may be a durable preference if repeatedly confirmed.

We also need to update profiles. This is because preferences can change over time. Good systems attach timestamps, sources, and sometimes confidence scores to memory entries.

## How Cross-session Memory Works

Cross-session memory means that information survives after one chat ends and can influence another chat.

A typical implementation works like this:

- During or after a conversation, a memory process identifies potentially durable information.
- It stores that information in a user-level, project-level, or organization-level memory store.
- A future conversation starts.
- The application selects memories relevant to the new conversation.
- Those memories are inserted into the new conversation’s context.
- The model generates its response using the supplied memories.

![](https://substackcdn.com/image/fetch/$s_!RmrE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b98d8e8-7ae0-4002-b4c6-5721492991f7_3342x1706.png)

The important step is number five. The new model call still needs the remembered information placed into its current context.

## Conclusion

In this article, we’ve looked at LLM memory in detail. The key takeaways are as follows:

- Model weights contain general knowledge learned during training.
- The context window contains information available for the current response.
- Conversation storage holds previous messages.
- Long-term memory stores selected facts, preferences, and past events.
- The memory manager decides what to retrieve and place on the desk.

It can be said that LLMs, along with the application surrounding them, don’t have the memory of a goldfish. They can process an enormous amount of information at once. But they don’t automatically carry personal experiences from one call to the next.

What appears to be memory is a carefully constructed system of context reconstruction, summarization, retrieval, and persistent storage. The quality of an LLM application’s memory depends at least as much on the surrounding architecture as it does on the model itself.

---

∙