---
type: raw-source
title: "How ChatGPT Optimizes its Agent Loop: Harness, API, and Inference"
source: "https://blog.bytebytego.com/p/how-chatgpt-optimizes-its-agent-loop?utm_source=post-email-title&publication_id=817132&post_id=208920802&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-07-29
created: 2026-07-30
description: "To understand what techniques are adopted in frontier labs to make AI applications more efficient, we met with the OpenAI engineers who developed and shipped various efficiency techniques into the systems behind Codex and ChatGPT Work."
tags:
  - "clippings"
  - "source/raw"

---
## Only Pay for Fine-Tuning That Works (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!pFDG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffca0b215-ee7b-4a7e-8f77-314f63098562_2400x1256.png)

GPU-hour billing charges for the entire time a machine is reserved — setup, idle time, queueing, and failures — so your cost depends on infrastructure efficiency you don’t control. Crusoe Serverless Fine-Tuning bills per token processed during training, making costs predictable from your dataset size and epoch count, with no GPUs to provision or right-size. Early stopping ends the job, and the billing, the moment your model stops improving — you’re never charged for epochs that add no accuracy. Jobs run on AI-optimized infrastructure with automatic recovery and restart, and checkpoints save at every step.

---

AI labs are moving faster than ever and releasing the most capable models we have ever seen. Just recently, Anthropic released Fable 5, then OpenAI released the GPT-5.6 family, including GPT-5.6 Sol, their most capable model yet, Kimi released Kimi K3, and Opus 5 came out just a few days ago.

**But capability is only half of the picture**. The other half is how much it costs these models to complete tasks, that is, the **cost per successful task**. Lower cost makes the model more affordable for users and less costly for the provider. A huge amount of effort inside the labs goes into making every component and layer of their AI applications optimized and more efficient, to reduce the overall cost. For example, GPT 5.6 Sol with max reasoning scores higher than Fable 5 on the [Artificial Analysis Coding Agent Index](https://openai.com/index/gpt-5-6/) while costing less than half as much.

To understand what techniques are adopted in frontier labs to make AI applications more efficient, we met with the OpenAI engineers who developed and shipped various efficiency techniques into the systems behind Codex and ChatGPT Work. Thanks to Joe, Ahmed, Steve, Matthew, and Philippe for sharing valuable details with us.

In this article, you’ll learn:

- What actually happens when you send a request to an AI agent
- How the harness layer cuts repeated work with persistent WebSockets, stable prompt prefixes, deferred tool discovery, and Code Mode
- How the API layer tokenizes only the delta and runs safety checks in parallel with inference
- How the inference layer gets more out of GPUs with cache-aware routing, KV cache management, speculative decoding, and separating prefill from decode
- What OpenAI learned from all of this, and which lessons you can apply to your own systems

![](https://substackcdn.com/image/fetch/$s_!J3g1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F158d3539-3017-4180-bc09-f4762d30eafe_3726x4503.png)

Overview of efficiency techniques

## Anatomy of an Agentic AI Application

When you give Codex or ChatGPT Work a task, like fixing a bug, the query does not go directly to the LLM. It is more complex than that. An AI application like Codex is not just an LLM. It is a system, with many components. User queries pass through several layers before the LLM ever sees a single token.

![](https://substackcdn.com/image/fetch/$s_!Qnyc!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a1b3206-9d2b-46e2-9759-20b9814e8144_2048x1851.png)

An AI application like Codex is made of many components. The LLM is just one of them.

But why can’t we send the user query directly to the LLM? To understand why, let’s see what an LLM actually is.

An LLM is a neural network trained to predict the next token. It takes a sequence of tokens as input and produces a sequence of tokens as output. It cannot run a shell command, edit a file, or remember anything between calls. But an agent task like “fix this bug and run the tests” is mostly actions. Something has to turn the model’s predicted tokens into real commands, feed the results back, and continue until the task is done.

That is the job of the **harness layer**, a system built on top of the LLM to handle those responsibilities. It takes the user’s task as input, decides which instructions, which tool definitions, and how much history to include in the context, and maintains the conversation history. When the model responds with a tool call, the harness executes it under approval policies in a sandbox environment, appends the result, and sends the conversation back to the LLM.

![](https://substackcdn.com/image/fetch/$s_!10q_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e0b6620-e1f6-40f5-9378-e62d37d585ea_2048x1096.png)

The harness builds the context and executes tools

But even the harness’s request does not go directly to the LLM. In production-ready applications, there is an API layer (an application layer) sitting between the harness and the inference endpoint. This layer exists because a real product needs to handle things that are not covered by the harness layer or the LLM. For example, authenticating the caller, enforcing rate limits, and, importantly, converting text into the token IDs the LLM expects, and converting generated tokens back into text.

Once the API layer prepares the context and tokenizes it into a sequence of token IDs, it is time for the LLM to process the input. That is the **inference layer.** It is a remote endpoint backed by fleets of GPUs, hosting the model. Its job is to run the model’s computation over the prepared tokens and produce the response, whether that is a new tool call or the final answer, as efficiently as possible. Then hand the generated tokens back to the API layer.

![](https://substackcdn.com/image/fetch/$s_!ZeZk!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcdd9870b-d04d-4bdf-85ed-0f5fad8b8281_2048x795.png)

The three layers of an agentic AI application that a request travels through.

### What happens when you send a request to an AI agent?

Now that we understand the three main layers of agentic AI applications, let’s walk through a concrete example to see how a request travels between these layers. Suppose you ask Codex to “trace the checkout regression, patch it, and run the tests.” Here is what happens:

1. The harness assembles instructions, tool definitions, and your task into a request and sends it to the API.
2. The API buffers the request into memory, parses the JSON, and validates it: the request is well-formed, and the chosen model supports every feature it asks for. It checks who is calling, applies rate limits, and runs preflight checks.
3. The API renders the conversation into the model’s input format and tokenizes it.
4. The API dispatches the tokens to the inference layer, and starts its safety checks at the same time: classifiers that look for things like cyberattacks and bioweapon content. The safety checks race to finish before the first generated token comes back.
5. The inference layer processes the prompt and begins generating. Its output here is not the final answer; it is a tool call: search the code for “checkout timeout.”
6. The generated tokens flow back to the API
7. The API converts tokens into text, wraps them in API events
8. The API streams them to the harness.
9. The harness recognizes the tool call, runs the search in its sandbox, appends the output to the conversation, and sends the updated conversation back to the API.

![](https://substackcdn.com/image/fetch/$s_!bqzo!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F255b0f03-4cfd-4b01-ba41-6b5fa9be87d0_2048x1711.png)

From the user’s request to the final summary coming back

This is just one iteration. In practice, a task repeats this loop many times until the model produces its final summary and the harness hands control back to the user. Each iteration redoes a lot of the same work described above. For example, the history gets resent, the text gets retokenized, or the prompt gets reprocessed. Removing this repeated work is the main opportunity for optimization. The next three sections cover the optimization techniques OpenAI adopted to make each layer more efficient.

## Harness Optimization

The harness is the orchestration layer closest to the user that turns the raw user request into a context and interacts with the LLM in a loop until the task is complete. It has two main responsibilities.

First, it is the source of truth for the conversation. It holds the authoritative record of every instruction, message, tool call, and tool result. Second, it runs the agentic loop. It decides what goes into the context sent to the LLM (which instructions, which tool definitions, and how much history). It sends the request, receives the response as a stream, parses it, and watches for tool calls. When a tool call appears, it executes it under approval policies in a sandbox environment, appends the result to the conversation, and sends it back to the LLM. It repeats this loop until the task is done. Heavy tasks could in theory repeat more than 100 times. Each iteration carries overhead. For example, one extra second per model call adds roughly half a minute to a long task.

![](https://substackcdn.com/image/fetch/$s_!h4lw!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d4ae493-1c56-4c6f-909d-f4936b8a2d33_2420x2138.png)

Agentic loop cycle

### How to make the harness layer efficient?

From the harness layer’s perspective, the latency comes from four sources: the network, prompt processing, context contents, and the loop’s round trips. OpenAI adopted the following four techniques at the harness layer to make it more efficient.

#### 1\. Persistent WebSockets and incremental requests

The harness runs on the user’s machine, but the model runs in OpenAI’s data centers, so every model call is a network exchange. The standard way to make that exchange is HTTPS. The harness opens a connection, sends a request containing everything the server (the API layer) needs, and receives a response. Because responses from a language model arrive gradually, one token at a time, chat applications typically use Server-Sent Events (SSE) on top of HTTPS, so the client sends one request, and the server streams the answer back in small chunks over the open response. SSE is a one-way street. It is a great fit for the chat era, where one user message produces one model call and one streamed answer. But agents are not one-pass. A single Codex turn can contain many model calls. With HTTPS, each of those calls is a new request with two separate costs.

The first cost is connection setup. Opening a fresh HTTPS connection means a TCP handshake followed by a TLS handshake, several network round trips before a byte of useful payload is transmitted. Paying that once per user message is manageable, but paying it many times inside one conversation turn is expensive.

The second cost is repetition of the payload itself. HTTP is stateless, so each request must carry everything the server needs. For example, the instructions, tool definitions, and the entire conversation so far, all need to be included in the request. By the twentieth tool call, the harness is resending the original prompt, nineteen tool calls, and nineteen tool results, just to add one new result at the end. This causes the payload to grow with every iteration, so the harness spends more and more time uploading data the server has already seen.

![](https://substackcdn.com/image/fetch/$s_!tN_Q!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2034c871-78de-43e4-b037-7b7fd89f5e34_2048x957.png)

HTTPS vs WebSocket

But how do we fix these two sources of cost?

The fix for the connection cost is to open one connection and keep it alive, instead of creating a new one for every call. This is what WebSockets are designed for. A WebSocket needs just one initial handshake, and after that, both sides can send messages whenever they want with no per-message setup. Codex opens a single WebSocket to the API and keeps it open across all the model calls in a turn. This eliminates the repeated TCP and TLS setup.

The fix for the payload repetition is to stop resending what the server already knows. The harness keeps the previous request and the completed response. If nothing but the conversation input has changed, it sends only the new items along with a reference to the previous response. After a tool call, the next message on the socket can be as small as:

```markup
{
  “type”: “response.create”,
  “previous_response_id”: “resp_abc123”,
  “input”: [
    {
      “type”: “function_call_output”,
      “call_id”: “call_xyz”,
      “output”: “...the new tool result...”
    }
  ]
}
```

Notice that this message has no instructions, tool schemas, or history. The server will rebuild the full context from the state it kept, s

o the model still sees everything. The only thing that changed is how much data crossed the network.

![](https://substackcdn.com/image/fetch/$s_!bBt_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F87e138b7-806e-42a8-aea2-10ed7807312e_2048x1028.png)

The harness sends only the new tool result

#### 2\. Stable prompt prefixes

LLM providers avoid repeated calculations with a technique called prompt caching. When a prompt arrives, the model reuses the cached internal state for the beginning of the prompt that matches a previous request (the prefix), and only computes the rest. The match is exact, token by token. If you change one token near the front of the prompt, everything after it must be recomputed.

![](https://substackcdn.com/image/fetch/$s_!_2uS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0aaee4e8-a0f2-4f3a-9941-aa93e76312cf_2048x1001.png)

Appending to the end of the prompt keeps the cache valid.

For the harness, this means the prompt it builds on every call must start with exactly the same bytes as the one before. That sounds trivial, but the harness rebuilds the request each time from its live in-memory state, so any small difference in how it assembles the prompt may silently break the match. OpenAI shared an example of this. Codex kept MCP tool definitions in a hash map, which does not guarantee ordering, so the same tools could serialize in a different order on each request. It was the same tools in the context, just in a different order. Codex was still completing tasks, just more expensively.

The efficiency technique here is to treat the history as append-only, and keep volatile runtime state like approval settings out of the prompt. For example, when a user changes approval settings mid-session, the harness does not edit the tool definitions in the prompt. It applies the new policy itself the next time a tool runs. This way, the prompt stays unchanged so the cache stays valid.

#### 3\. Deferred tool discovery

Stable prompt prefixes make repeated context cheaper, but they do not keep the prompt small and concise. In agents with access to lots of tools, this can be an issue. For example, the tool schemas alone can take up a huge amount of space, because a Codex session can expose hundreds of tools once you count connected integrations and MCP servers. Every tool schema is a JSON object with names, descriptions, and parameter definitions. Once all of these are in the prompt, the LLM has to process all of them in its calculations, even though many may go unused for the current task.

To keep unused tools out of the prompt, OpenAI uses a technique called deferred discovery. The prompt carries only the core tools, say the shell and file editing, plus one tool\_search tool. The other hundreds of integration definitions stay out of the prompt entirely. When the model needs a capability, it calls the search tool with keywords like “list deployments”. The harness searches the catalog, and the matching definition gets loaded into the context. The search itself is BM25, a lexical ranking algorithm that finds tools whose descriptions overlap with the generated keywords.

![](https://substackcdn.com/image/fetch/$s_!VVy4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c50e398-e309-41bd-9fc7-a09d2a927d0c_2048x1522.png)

The model searches for a tool when it needs one

In addition to deferred discovery, two more techniques can keep the context small. Schema compaction trims oversized tool schemas down to a token budget by stripping descriptions and collapsing nested structures while preserving argument names. Conversation compaction condenses a long history into a short summary.

#### 4\. Code Mode

In ordinary setups, the model emits one tool call, waits for the result, reasons, and emits the next. In many scenarios, there is no reasoning needed between these tool calls. The model just emits them one by one to collect the results it needs. This is costly because each tool call requires a full model round trip. Also, after each tool call, its result keeps getting added to the context, which wastes context space.

With Code Mode, instead of emitting tool calls one by one, the model writes a small program that makes those calls. The harness runs this program in an embedded JavaScript runtime, where every tool is available as a function. The script can fan out independent calls in parallel, filter and join the results in plain code, and return only the compact answer. This way, the intermediate data stays in the runtime, and only the final result enters the context.

![](https://substackcdn.com/image/fetch/$s_!oblt!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4ecb3763-6ea2-4053-80f2-1f0939c1d0ee_2048x1378.png)

Direct tool calls vs Code Mode

## API Optimization

The API layer is the service the harness is talking to. It sits between the harness layer and the inference layer, running on ordinary CPUs. The harness sends JSON describing structured conversation items, while the model consumes and produces token IDs. When a request arrives, it goes through the following steps:

1. The request body is buffered into memory.
2. The JSON is parsed and validated against a schema (well-formed fields, arrays within expected bounds, etc.)
3. A second validation round checks semantics. For example, does the chosen model support the requested features?
4. Preflight checks run: authorization and entitlements, rate limits, and checks on any images in the request.
5. The API renders and tokenizes the conversation, then kicks off two jobs at the same time: the inference request to the GPUs and the safety checks on the prompt.
6. As generated tokens flow back from the inference layer, the API converts each one into text, wraps it in an API event, and streams it to the client.

![](https://substackcdn.com/image/fetch/$s_!ROud!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3c7fd5c-2acf-4fd1-aeb6-2fd7e48cc637_3492x1518.png)

The steps a request goes through inside the API layer

These steps are repeated on each iteration of the loop. The inference is out of the API layer’s control. The API cannot make the GPU any faster. All it can do is add as little delay as possible around it. The time the API layer spends parsing, validating, or tokenizing is extra latency the user feels.

### How to make the API layer efficient?

OpenAI adopted the following techniques to reduce the overhead coming from different places in the API layer.

#### 1\. Tokenizing only the delta

Models do not read text. Before inference starts, the prompt must be converted into token IDs. Tokenizers convert the text into token IDs in O(n), linearly going over each token in the prompt and replacing it with the token ID. Under stateless HTTP, the whole conversation gets retokenized on every call. By the twentieth tool call, the API is rereading many thousands of tokens to extract one new result. The GPU only needs the new tool result, but the CPU is rereading the book from page one, and the cost keeps growing with input length.

With the WebSocket, the API keeps the tokenized conversation in server memory. The first request tokenizes the full prompt, but every later request sends only the new items. The API tokenizes just that piece and appends it to the stored sequence. This way, per-call tokenization stops depending on conversation length and becomes closer to O(1), depending on the length of the marginal input.

![](https://substackcdn.com/image/fetch/$s_!PUMs!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd34eb042-2979-4e16-83e8-a9299b1c161b_2048x1761.png)

Tokenization with stateless HTTP and WebSocket

#### 2\. Running safety checks in parallel with inference

Agents have to check each request for safety before showing the output to a user. OpenAI implemented safety checks in its API layer. Images go through their own classifiers, while the prompt text goes to classifier models that look for dangerous content, like cyberoffense or bioweapon instructions. These classifiers take time to run. The simple design is to run them first and start inference only after they pass. The problem is that this delay is added to the time-to-first-token (TTFT) of all requests, while the vast majority of them are completely harmless.

The fix is to run the safety checks and inference at the same time. The model takes some time to process the prompt before its first token comes out, so the checks use that window to finish. If a check fails, the API reacts depending on the model. For some models, it streams tokens to the user right away and cuts the stream when a check fails. For more sensitive models, it holds the output until the checks pass and only then releases it. In both cases, the time spent on safety hides inside a wait that was going to happen anyway.

![](https://substackcdn.com/image/fetch/$s_!f9Cr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6cac1da-8660-4b22-9089-8b915a319a72_2048x812.png)

Running safety checks in parallel

#### 3\. Routing traffic to newer CPUs

When a company runs servers at scale, its fleet ends up with machines bought in different years, and therefore with different generations of CPUs. The scheduling software usually treats machines of the same type as identical. In reality, they are not. OpenAI queried Kubernetes for the actual processor model behind each of its deployments and found a mix of older Broadwell chips and newer Ice Lake chips behind the same machine labels. The older ones were serving the same traffic with roughly 20% worse time to first token, while using about twice as much CPU.

To fix this, OpenAI shifted more traffic toward the machines with newer processors and started treating CPU generation as an explicit factor in capacity planning. Sometimes the best software optimization is better hardware.

## Inference Optimization

The inference layer is where the model actually runs. There are fleets of GPUs and other accelerators, and the serving software (the engine) that operates them. The model’s core computation is enormous matrix arithmetic, which parallelizes across the thousands of cores an accelerator provides. The layer schedules and batches incoming requests across the fleet, holds the per-conversation state that generation depends on, executes the model’s forward passes, and hands each generated token back to the API layer.

![](https://substackcdn.com/image/fetch/$s_!sjOn!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa396a106-ef9f-426d-a749-12b633354d96_2048x1144.png)

Each machine holds the model weights and the KV state of the conversations it serves.

### How to make the inference layer efficient?

Demand for tokens grows faster than hardware can be added, so at this layer slow and wasteful are the same word. The waste hides in four places: work routed to the wrong machine, memory holding the wrong state, parallel hardware idling through sequential generation, and two mismatched phases sharing the same machines.

OpenAI adopted the following techniques to make the inference layer more efficient.

#### 1\. Balancing load with cache-aware routing

OpenAI serves its models from many GPU machines. Every request has to be sent to one of them. If that routing is uneven, some machines sit idle while others queue up work. Idle GPUs are the most expensive kind of waste in the stack. There is also a second, less obvious problem. Each machine keeps the computed state (the cache) for the conversations it recently served. If the next request of a conversation lands on a different machine, that cache is useless. The new machine must recompute everything from scratch, even though the work already exists somewhere else.

So the router has two goals:

1. **Spreading load evenly:** send the request to the least busy machine.
2. **Using the cache:** send it back to the machine that already knows this conversation.

![](https://substackcdn.com/image/fetch/$s_!lDQs!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F34f970dd-7678-43b2-863b-833dd4af4172_2048x1149.png)

Cache-aware routing

OpenAI’s routing weighs both for every request, along with basics like geography and available capacity. Improvements in load balancing alone have dramatically reduced the cost of serving its models.

#### 2\. Managing the KV cache

When a transformer generates a token, it attends over all previous tokens. To avoid recomputing that attention state for every new token, the serving system keeps it in accelerator memory, in what is called the KV cache. The cache grows linearly with conversation length, multiplied by every concurrent conversation the fleet is serving. For long contexts it can rival the size of the weights themselves. If the software evicts the wrong state, the inference layer pays the full processing cost again when that conversation returns.

The efficiency technique here is to manage the cache based on real usage. OpenAI analyzes production traces to learn which cached state is likely to be needed again, tests eviction policies against that data instead of intuition, and optimizes how cached state is stored and moved between memory tiers. This ensures the most valuable work stays around longer without running out of memory or wasting time moving data.

![](https://substackcdn.com/image/fetch/$s_!lkju!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0d55712-2031-46f3-a6a3-eaf12d2f639d_2048x867.png)

The hot conversation state stays on the GPU. The colder state is moved or evicted.

#### 3\. Speculative decoding

Generation is sequential. Each token depends on the previous one, so a model that processes a huge prompt in one parallel pass must produce its answer one token at a time. In large models, producing these tokens is expensive and slow, even when the next token is easy to guess. For an input like “the capital of France is”, the next token is almost certainly “Paris”, but the model still has to process the entire conversation and perform large matrix multiplications to predict it.

Speculative decoding uses a small draft model to propose the next several tokens, and the large model verifies all of them in a single parallel pass. In many cases, the draft proposals are correct and will be accepted by the large model, which saves the time the large model would have taken to produce them one at a time. When a proposal is wrong, the large model discards it and produces its own token, so the output quality does not change. The main metric to evaluate the draft model is the average acceptance length, which is how many proposed tokens the main model accepts in each pass.

![](https://substackcdn.com/image/fetch/$s_!cjF9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb70a6b8f-1440-4b29-84fa-96159324bea9_2048x1148.png)

Speculative decoding

#### 4\. Separating prefill and decode

Inference has two phases, prefill and decode. Prefill processes the entire incoming prompt in one massively parallel pass, and it builds the internal state (KV cache) the model needs. Decode then generates the response one token at a time. These two are very different workloads. Prefill is compute-heavy, while decode is memory-heavy, spending most of its time streaming weights and cached state through memory. Running both on the same machines means neither runs on hardware set up for it.

The efficiency technique is to separate them. One part of the fleet handles prefill and another handles decode, each configured for its own bottleneck. When a request finishes prefill, its computed state (the KV cache) is shipped to a decode machine, which generates the response token by token.

![](https://substackcdn.com/image/fetch/$s_!yKVk!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1bf01003-d3c5-4700-94fc-730282c8a9ca_2048x1880.png)

Summary of efficiency techniques across three layers

That covers the efficiency techniques at each layer of an agentic AI application. The harness avoids resending what the server already has, the API avoids reprocessing what it has already processed, and inference avoids recomputing what it has already computed. To close, let’s look at the lessons from this work that apply beyond OpenAI.

### What to Learn from OpenAI’s Push for Efficiency and Lower Cost per Successful Task

Zooming out, all these optimization techniques at different layers try to avoid paying for the same work twice. The harness sends only what is new and keeps prefixes stable so caches survive. The API tokenizes only the delta and hides unavoidable work inside windows that had to pass anyway. Inference routes conversations back to their cached state instead of recomputing it. These layers also feed each other. When the harness keeps the cache intact and the API improves the cache hit rate, the savings appear on the GPUs, which means lower costs for users. Beyond the techniques, here are a few lessons that the OpenAI engineers shared with us.

**Keep the design simple.** Prioritize simplicity over complexity. For example, use lexical search instead of embeddings for tool discovery, and one compaction path instead of a menu. An LLM is already quite intelligent, so adding more machinery in front of it often adds complexity without adding value. Build the simplest thing that could work, then scale it.

**Use the agent to optimize its own stack.** Codex wrote much of the migration of the very API that serves Codex, turning years of rewrite work into months for a couple of engineers. The inference team uses it to analyze traces and prototype kernels. When agents write the code, you no longer need a language that is easy for humans to write, so you simply pick the most efficient one to run. Efficiency work is becoming a loop that accelerates itself.

**Optimize end to end.** The inference team told us that every time they picked one favorite technique to focus on, they regretted it. Focusing on one part of the stack made them underinvest in the others. No single optimization is a game changer on its own. The big wins come from chaining many small ones together. They also learned to test with the same traffic shapes that production actually serves, because a change that looks like a win offline can hurt in real traffic.