---
title: "How OpenAI Built GPT-Live"
source: "https://blog.bytebytego.com/p/how-openai-built-gpt-live?utm_source=post-email-title&publication_id=817132&post_id=216343930&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-09-22
created: 2026-09-23
description: "To understand how it all works end to end, we met with engineers on the GPT Voice team, Zahan Malkani and Justin Uberti (who created WebRTC)."
tags:
  - "clippings"
---
## Free tickets to P99 CONF — 60+ technical talks, fully virtual (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!ABMo!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F121a6fe0-8ec7-47f1-9925-796afafacb93_1600x840.jpeg)

How do you optimize AI when performance matters? And how can you apply AI to make performance better (and easier) than ever before? That’s what 30K engineers will explore at P99 CONF. Here’s a taste of the talks you can expect

- Sandboxmaxxing at Lovable: Every Prompt Gets a Sandbox in < 1s
- The Autonomous Performance Agent: A Netflix Production Story
- Lessons Learned from Building Crazy Fast, Open Source Infrastructure for AI Agents
- Give the Agent a Cluster: Effective AI for Performance Engineering at Scale
- Managing 500 Billion+ Files for AI Workloads
- How to Improve Your Cache Algorithm Using AI

Bonus: Registrants get immediate 30-day access to the complete O’Reilly library, and attendees can enter to win 1 of 500 free swag packs.

---

If you have used voice assistants before, you have probably experienced unexpected interruptions. You talk with the system, and the moment you pause briefly to think of the right term, it starts talking. Then you interrupt it so you can continue. This is a common frustration, because most voice models can either listen or speak, but not both at the same time.

![](https://substackcdn.com/image/fetch/$s_!1fuy!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c77c92d-00a1-4a72-b074-4b6dd9cfa710_2048x540.png)

Turn-based assistants cut in at the wrong moment

Newer voice models, like OpenAI’s GPT-Live-1, change that by listening and speaking at the same time. The model constantly decides whether it should stay quiet, interrupt, or start talking. This makes the conversation feel more natural with fewer unintentional interruptions.

![](https://substackcdn.com/image/fetch/$s_!gCfP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7dc8c971-08ae-4094-b1d7-a35b04de53bb_2048x742.png)

Full-duplex architecture. Both sides are always on

Under the hood, these systems combine a new generation of voice model architecture with a serving system optimized for low latency. To understand how it all works end to end, we met with engineers on the GPT Voice team, Zahan Malkani and Justin Uberti (who created WebRTC). We thank both of them for sharing the details with us.

![](https://substackcdn.com/image/fetch/$s_!yQWJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a7e9151-1f8b-49e5-bf73-1531cbe3a23a_2048x993.png)

Three generations of voice systems (High-level)

In this article, you’ll learn:

- The three generations of voice systems, including cascaded pipelines, turn-based end-to-end models, and full-duplex models
- Delegating thinking from talking, the core idea behind GPT-Live
- The engineering behind the serving system, including the live and async paths
- How evaluation is different in full-duplex voice systems
- Engineering lessons for building realtime systems and what is next for voice

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

## Three Generations of Voice Systems

The input to a voice system is the user’s audio. The output should be the response in audio format played back to the user. While the input and output are always audio, what happens in between depends on how we design the system. Voice systems have gone through three generations of architecture:

- Cascaded Design
- Turn-based End-to-End
- Full-duplex Architecture

Let’s examine each in more detail.

### 1\. Cascaded Design

The cascaded design chains three separate models. An automatic speech recognition (ASR) model transcribes the user’s speech into text, an LLM then generates a text reply, and a text-to-speech (TTS) model finally reads the reply for the user.

![](https://substackcdn.com/image/fetch/$s_!maR8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55340659-7565-4006-bd4a-769996d51ad3_2048x459.png)

The cascaded design chains three models

Each model in the design focuses on the task that it is good at. ASR is good at converting speech to text. It does not have the knowledge that LLMs have. So it only focuses on the conversion. The LLM then relies on its capabilities to understand the user’s query and respond to it accordingly. Once the LLM produces the response text, the TTS model just synthesizes it into speech that sounds natural.

Cascaded design works in practice, but it has two main issues. First, information loss. The LLM only sees a transcript, so vocal information like tone and emotions will be unavailable to the model.

![](https://substackcdn.com/image/fetch/$s_!lUDC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F204aa55f-6ba4-4999-a33f-98d207d05a51_2048x1008.png)

The transcript drops everything but the words

Second, the system is complex and slow. Since the three stages run in series, their latencies add up. The user must wait until all three stages are complete. Also, running three models means building, serving, and scaling three separate systems which is complex in practice.

![](https://substackcdn.com/image/fetch/$s_!R2pE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3231bd11-c12e-4d80-90dd-79a539ff52c7_1938x1026.png)

Stage latencies add up while the user waits

Due to these limitations, the second generation of voice systems was designed: turn-based speech-to-speech models.

### 2\. Turn-based, Speech-to-Speech

The second generation introduces an end-to-end speech model, a single model trained to consume audio as input and produce audio directly as output.

![](https://substackcdn.com/image/fetch/$s_!6UEn!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a89e446-19cc-49ae-b8d6-8fa1918ccc3d_1946x854.png)

One speech model keeps tone and emotion

This design solves a key limitation of cascaded systems: it allows the model to take into account vocal information since it processes the audio directly.

While this is a good improvement, the interaction itself remains turn-based. A small model, called a turn detector, still decides when the user has finished, and only then does the main speech model start its job. The turn detector is not new here. The pause detection step in the cascaded design is the same component. Both generations rely on it, and this turn-based design is the source of unnaturalness.

![](https://substackcdn.com/image/fetch/$s_!2x3j!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4da22b0-4891-4c67-a6c3-93fcf8c6b502_2048x433.png)

A turn detector gates the speech model

The detector has a challenging job. If it detects too early, it cuts the user off in the middle of a thought. If it decides too late, users experience awkward delays. Interruptions face the same challenge. When users start talking over the voice system, a separate mechanism has to stop the audio and clear the buffers. If the interruption detection is too sensitive, spurious interruptions can be triggered from background noise. If detection is too conservative, interruptions take too long and feel sluggish, while short interjections like “yes” and “no” can be entirely missed. Justin points to this machinery as the reason earlier voice systems felt unnatural.

![](https://substackcdn.com/image/fetch/$s_!-ezp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd02e5069-1445-484e-bfc7-b0430ffcc4f3_2048x935.png)

Detect too early or too late, both feel wrong

These models are also expensive to keep updated. When there is a new, more capable pre-trained LLM, it requires a new full speech-to-speech training run on top of the checkpoint. So voice models always lag behind the newest frontier models.

![](https://substackcdn.com/image/fetch/$s_!eNfD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e9058e0-9c42-4b23-a031-40b5a4d935be_2048x964.png)

Voice models lag every frontier release

The third generation of voice models, full-duplex architectures, fixes the turn-taking problem.

### 3\. Full-duplex Architecture

Full-duplex models are designed so they can both listen and talk simultaneously. The model continuously produces audio tokens. When it should stay silent, it simply produces silent tokens. Similarly, it continuously processes the input audio tokens. When the user is silent, those are just silent tokens. This design removes the turn detector entirely.

To better understand, let’s use an open full-duplex model, Moshi \[x\], as a reference. Moshi converts audio into discrete tokens, similar to how text is converted to tokens for LLMs. The model processes these tokens as inputs and emits new tokens on a fixed clock, roughly one frame every 80 milliseconds. Silence is simply another token that decodes to silence. So the model just needs to learn the behavior during training and implicitly understand when to listen and when to talk from the training data.

![](https://substackcdn.com/image/fetch/$s_!Hd_g!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F657e372d-92f8-451c-bacd-0fc8e3792468_2048x966.png)

Silence is just another token

Full-duplex solves the interruption problem and the unnaturalness in conversations, but it creates two new engineering challenges. First, since the model is always running and predicting the next token, serving is costly. Second, the model needs to respond within milliseconds, so it cannot be too large in capacity.

OpenAI launched GPT-Live-1 in July 2026, a family of full-duplex voice models. It is designed around the challenges described above. The voice model stays small and fast so it can respond within milliseconds. It also relies on delegation to perform expensive reasoning while the conversation keeps going.

## How the GPT-Live System Works

This section explains how OpenAI managed to build a voice assistant around a full-duplex architecture. We cover the ideas and techniques that make it practical at scale in production.

### Separating Talking from Thinking

Normally, a frontier LLM might reason, search the web, and then respond, which can take several seconds. In voice systems, that translates to a few seconds of silence, which is not ideal.

To fix this, OpenAI separates talking from thinking. A voice model handles the conversation with the user. Another capable model performs the necessary reasoning and tool calling for more complex queries. The serving system is also built around this idea. It delegates the request to the capable model when needed, while continuing the conversation with the user.

![](https://substackcdn.com/image/fetch/$s_!klFH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4353dfb-9152-4fa2-bd81-928d0d102cf8_2048x730.png)

One model talks while another thinks (simplified)

As the figure below shows, a question like who won last night’s game cannot be directly answered by the speech model using its internal weights, so the voice model delegates it to GPT-5.5. It keeps the conversation going while the search runs, and reads the answer for the user once it is available.

![](https://substackcdn.com/image/fetch/$s_!FGa3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F87668463-2c4a-42bf-99d8-6deea92d0e8b_2048x1135.png)

The voice model keeps talking during a delegation

This design meaningfully reduces the trade-off between speed and quality. While the frontier model looks up information, the voice model remains available to continue chatting. Previously, if you wanted smarter answers, you looped in more systems, and the response took longer. If you wanted quick responses, you used a smaller model, and the answers got worse. With one model for talking and another for thinking, the voice system gets both.

Another benefit of this design is modularity. When a new frontier model is available, less engineering work is needed to switch the voice assistant to it.

![](https://substackcdn.com/image/fetch/$s_!Min6!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89c669e1-bdb8-4fb6-97f8-6ec2f1e6c1d7_2048x1197.png)

Swapping the frontier model is easy

### The Two Serving Paths

Serving two models is tricky. Audio frames should be sent every few milliseconds, but a delegation can take seconds. So we cannot have a shared process for both. GPT-Live splits the traffic. The live path carries audio only. It moves audio between the client and the voice model as fast as possible. The async path handles anything other than the audio, which can take longer. This way, a slow tool call may delay the async path but not the live path.

#### How to make the live path fast?

The main requirement of the live path is that audio must move between the user and the model on a fixed clock. The model processes frames as input and produces them as output in real time. So the user hears a delay when it occurs. As Zahan explains, whenever a bottleneck makes the system fall behind, it starts producing audible artifacts.

To meet this requirement, lots of optimizations are needed. For example, the connection must open quickly, the model must keep up with the incoming stream, and frames must be delivered on time. Here are a few engineering techniques OpenAI adopted to keep the live path fast:

- Starting a session in one round trip
- Having cheap continuous inference
- Handing off live conversations between model instances

**1\. Starting a session in one round trip**

When the user taps the voice button, the client must establish a connection before any audio can flow. This requires a few network trips, depending on the underlying protocol. GPT-Live uses WebRTC, which is used in most video calling apps. But a standard WebRTC session takes six steps to establish before a single audio frame can be sent. On a mobile network where one round trip takes 60 milliseconds, setup alone can cost over a third of a second.

![](https://substackcdn.com/image/fetch/$s_!DWIi!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb89f5fd5-19db-4d98-add7-f50b92ab7016_1846x2048.png)

Standard WebRTC costs six round trips

To improve this, OpenAI built WARP (WebRTC Abridged Roundtrip Protocol). It relies on the idea that instead of having the steps one after another, we have them happen at the same time. This shrinks the number of network trips to only one.

![](https://substackcdn.com/image/fetch/$s_!FUfh!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a4e2138-a6e6-422c-a98e-bb84b280d6e5_2048x960.png)

WARP collapses setup into one round trip

**2\. Having cheap continuous inference**

To understand what makes full-duplex systems expensive to serve, let’s compare them with a chatbot. In chatbots, a request arrives, and then the model produces tokens. When the response is complete, the model sits idle. A full-duplex model, on the other hand, has no idle time. Audio streams into the model, and the model produces frames continuously. This happens even when the user is mid-sentence or pauses to think.

![](https://substackcdn.com/image/fetch/$s_!o92z!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb69dede-8c6c-4680-bd10-6b560bd1b642_2048x966.png)

A full-duplex model never goes idle

Continuously sampling a model, many times per second, for every user, is expensive. OpenAI reduces this cost by keeping each conversation loaded on the model. So instead of re-reading the whole conversation on every request, each session stays connected to the model instance that holds the conversation in GPU memory. When a new audio frame arrives, the model only processes that one frame. In addition, common techniques like batching and speculative decoding can be adopted to keep the system fast.

![](https://substackcdn.com/image/fetch/$s_!hKRx!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa1744a00-f8c4-4af2-93c4-4fee05154cd2_1906x1550.png)

Keeping state on the GPU avoids re-reading history

**3\. Handing off a live conversation between model instances**

Keeping the conversation loaded on one model instance creates a new problem. Model instances may become unavailable. They need to stop and start with demand or receive updates. They may also fail occasionally. In regular systems, this is easy to handle since we can send the request to another available instance. In GPT-Live, the session is tied to the instance that holds its conversation in GPU memory.

OpenAI created a managed handoff mechanism. The system prepares a replacement instance and loads the full conversation beforehand. Once the new instance is ready to be used, the switch happens, so the conversation can continue without any interruptions. This is also useful when other operations need to happen. For example, when the context needs to be compacted, the shortened conversation is prepared on a replacement instance while the original keeps talking. The switch then happens the same way.

![](https://substackcdn.com/image/fetch/$s_!PvHN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03943a7d-8393-4de7-9feb-66981311b696_2048x710.png)

A handoff warms the next instance before switching

#### The Async Path

The async path handles everything that is not audio, like delegations and tool calling. These jobs, by their nature, are large and can take longer to complete. Still, results should come back fast enough that the two models feel like one system. Back to our example session. The user asks who won last night’s game, and the voice model starts a delegation. The voice model can buy a little time by doing things like acknowledging the question or thinking out loud for a moment. But it cannot do anything when an answer takes too long. So everything in the delegation loop, including prompt processing and routing, needs to happen fast.

To cut latency, we should first understand what is causing it. Most of the time is spent on reading the request. A model that receives a request has to process the entire prompt (prefill) before producing tokens. In a long conversation, that alone can take a noticeable fraction of a second. OpenAI’s fix is to do this reading before it is needed. When a user starts a conversation, the server creates an inference session with the frontier model and sends the conversation so far. By the time the first delegation happens, the model has already everything it needs to produce tokens.

![](https://substackcdn.com/image/fetch/$s_!ftf-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1fd79194-9ac5-4e94-ac5b-d67d6338cbe9_1946x1042.png)

Prefilling early makes delegations fast

## How to Evaluate a Full-duplex Voice System?

A turn-based speech model can be evaluated one turn at a time by sending a request and scoring the response. But with a full-duplex architecture, there are no turns. There is only one continuous stream of audio. This makes evaluation different.

In full-duplex systems, instead of scoring turns, we can evaluate three parts:

- Conversational behavior
- The health of the stream
- Testing the system on real production traffic

### 1\. Conversational behavior

The first question is whether the model behaves well in a conversation. This mostly comes down to timing. The model has to continuously decide if it should stay silent, interrupt, or talk. When the user speaks while the model is talking, it has to decide if this is a real interruption or just background noise. These two decisions are called endpointing and barge-in detection.

![](https://substackcdn.com/image/fetch/$s_!kfDY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F24f285f9-3fdf-4247-a5cc-9b46716bff6f_2048x800.png)

Endpointing and barge-in

To evaluate these behaviors, each decision is scored like a prediction. Did the model detect the end of the turn correctly? Did it recognize a real interruption? The mental model for eval is the same. We collect eval data (natural conversations), have it annotated around the dimensions that we want to measure, run inference on it, and evaluate.

### 2\. The health of the stream

The second dimension of eval is whether the stream itself is healthy. In most serving systems, this is answered with a percentile target like p95. If the p95 latency is good, 19 out of 20 requests feel fast. This works fine as long as unusually slow cases are kept very low. A normal user only sends a request once in a while, so a slow one is quickly forgotten.

But p95 is not reliable in full-duplex architectures. Given that the model runs continuously, a p95 event happens every 20 inferences, which translates to several times per minute. Even p99 events show up regularly. So the system has to be engineered around p999. In practice, this means designing for fast recovery, since some slow frames are guaranteed to happen in every session.

### 3\. Testing the system on real production traffic

The last layer of evaluation checks whether the system works reliably under real traffic. The technique for finding out safely is called a silent launch. Users keep talking to the old system as usual, while a small percentage of voice sessions are routed to the new system. This kind of silent launch catches problems that are normally hard to find. For example, it can find bottlenecks in unexpected places. In GPT-Live’s silent launch, the team found out that a CPU-side service ran out of capacity before the GPUs did. This is something that is generally hard to learn with ordinary tests.

## What Other Teams Can Learn From GPT-Live

The broad lesson from OpenAI’s GPT-Live is that building for realtime serving is different and more challenging than traditional serving. For example, in voice systems, users hear the worst frame, so average latency is an insufficient metric to monitor. The tail is more important and deserves more engineering. In addition, capacity planning is different in such systems. When a user is having a conversation, the session is occupied the entire time. So capacity should be measured in concurrent sessions instead of per request.

The other lesson is that complexity should be handled inside the model. For example, turn detection used to be a small, separate component, and it was a main source of unnaturalness. Moving that decision into the model behavior, which has the greatest reasoning horsepower, made the conversation more natural and the system simpler. In general, whatever stays outside the model should be kept small and focused on the realtime work. This ensures the system remains simple and maintainable.

## What’s Next

OpenAI believes the next generation is voice driving a computer. In the ChatGPT desktop app, it takes screenshots to see what you are working on, starts long-running tasks, and reports back. Along the way, you can ask for status, answer questions, and redirect it mid-task. Zahan says it feels like science fiction.

![](https://substackcdn.com/image/fetch/$s_!NKBH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe29b5aa3-4b1c-4d07-a014-87fb4432790b_2048x523.png)

Voice driving a computer while you talk

Some questions are still open. Zahan says it remains challenging for a voice model to delegate tasks to other models while keeping a live conversation with a user running smoothly.The delegation path might tolerate delay, but live conversation is more sensitive. A general-purpose protocol would mean “part of your brain responds slowly.” Justin says voice AI was like in its GPT-3 days. With GPT-Live-1, he puts it at GPT-4, with many interesting problems still ahead.

---

∙