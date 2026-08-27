---
type: raw-source
title: "Inside Roblox’s Bet on World Models"
source: "https://blog.bytebytego.com/p/inside-robloxs-bet-on-world-models?utm_source=post-email-title&publication_id=817132&post_id=207335982&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-07-21
created: 2026-07-22
description: "We sat down with Anupam Singh, senior vice president of engineering at Roblox, to hear from him about the world model that Roblox is using to make its multiplayer games look photorealistic, the key insights that have come from taking that approach, and the next big thing that the Roblox team is focusing on."
tags:
  - "clippings"
  - "source/raw"

---
## Writing Useful Logs For Production. This Workshop Shows How. (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!2jrU!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d0f70f1-6eec-4284-b827-bb14bf2b5d47_1200x628.png)

An incident hits and you pull up the logs, only to find string based console output that tells you something broke but not why. That’s the problem with unstructured logging: it eats your quota and still leaves you guessing.

This hands-on workshop fixes that. You’ll learn what’s actually worth logging (state transitions, request boundaries, external call failures, auth decisions), how to structure logs as real data instead of text dumps, and how to add attributes that connect them to traces and errors. Plus, how to tune signal to noise, so noise stops drowning out what matters.

---

Roblox is built for scale. In August 2025, the platform reached a peak of 45 million concurrent users. Few game engines can support that kind of demand.

But Roblox itself isn’t the one making most of those games. It gives creators the tools to build them, then focuses on the infrastructure beneath them. Now, Roblox is exploring how a video world model can work alongside its game engine to make those experiences photorealistic without compromising scale or multiplayer performance.

This hybrid approach offers valuable lessons for engineers building real-time systems at scale. To explore those lessons, we sat down with [Anupam Singh](https://www.linkedin.com/in/anupamvsingh/), senior vice president of engineering at Roblox, to hear from him about the world model that Roblox is using to make its multiplayer games look photorealistic, the key insights that have come from taking that approach, and the next big thing that the Roblox team is focusing on. We thank Anupam for sharing with us.

In this article, you will learn:

- What a game actually requires, and why visuals are only part of it.
- How combining a world model with a game engine can make games more realistic.
- How Roblox is using a hybrid architecture to divide the work between the engine and the world model and keep the world consistent for everyone playing.
- The four open problems (latency, consistency, multiplayer, and creator control) and the specific techniques Roblox is using on each.
- What Roblox is focused on next, and why it could make photorealistic games far cheaper to build.

![](https://substackcdn.com/image/fetch/$s_!gpgx!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5c51c06-3d8b-4f01-a178-8201d7ecbee0_1695x2048.png)

Inside Roblox Reality (High Level)

## What makes a game a game

When people praise a game, they usually point at the graphics. Graphics are the easiest part to notice and often the smallest part of the engineering. What actually makes a game a game is a set of systems players never see. These systems serve one of two purposes: keeping the world consistent for everyone playing, and rendering it on screen.

![](https://substackcdn.com/image/fetch/$s_!d-hs!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F008f69dd-1d66-4bc2-b09f-0490701f6f9a_2048x1404.png)

Players notice the graphics but the systems underneath make it a game.

**1\. Keeping the world consistent**

Keeping a world consistent takes several systems working together. The foundation is the persistent state, a running memory of where everything is and what has happened, so the world is still there when you come back to it. Then come the rules, the logic that has to resolve the same way for everyone, so the game stays fair. Physics has to be believable, so objects move, collide, and fall the way players expect. Since most games are played with other people, all of it has to stay in sync in real time, so thousands of players share one consistent world rather than thousands of slightly different ones. On top of that, the world has to react the instant a player acts. Together, this is what turns moving images into something you can actually play.

A racing game makes this concrete. The track, the scores, the penalties, how each car handles, and where every other car is all need to be exact. Every player needs to see the same thing at the same moment. If even one of these is off, players notice right away.

![](https://substackcdn.com/image/fetch/$s_!8FGb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe0170085-6c2e-4b95-94b0-a7d196fe960d_1932x1366.png)

Everyone has its own view based on a shared state

**2\. Making the game look real**

The second purpose, making the world look real, is a newer demand. The real world has a lot of fine detail that is hard to produce. Grass moving in the wind, dust behind a car, smoke off a fire, light shifting across a surface. Players now expect that level of realism.

![](https://substackcdn.com/image/fetch/$s_!imIP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2e56f716-7eca-4a0b-bcf6-942c471c32ef_1626x774.png)

The fine details users expect

That is what makes the problem hard. No platform has delivered all of it at once: a world that is consistent and fair, looks real, and still runs affordably on the hardware people already own.

Today, two technologies each cover one side of this. AI world models are built to make things look real, generating photorealistic images from what they have learned. Game engines are built to keep worlds consistent, tracking state, rules, and physics across every player. The catch is that each is good at only its own half. The next sections look at why a world model alone, and a game engine alone, each fall short, and then at how Roblox combines them.

---

## Crusoe Serverless Fine-Tuning Is Now GA (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!blMv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff3a00dcd-a2a2-4fe6-a13a-7fdf72b0c994_2400x1256.png)

Fine-tuning open models shouldn’t mean babysitting GPU clusters. Crusoe Serverless Fine-Tuning, now generally available in Crusoe Intelligence Foundry, gives you a complete path from proprietary data to production-ready model. Select a base model from a curated library of top open models — including Qwen, DeepSeek, Gemma, and gpt-oss — upload your dataset in JSONL or Parquet, configure your job, and submit via UI, SDK, or API. Token-based pricing ties spend to actual training work, and early stopping ends billing the moment your model stops improving. Deploy in one click, or download your weights in.safetensors format.

---

## Why a video world model alone isn’t enough

A video world model generates a world one frame at a time, predicting what should come next. It can also take conditioning signals as input, such as a text prompt or a starting image.

![](https://substackcdn.com/image/fetch/$s_!uMwp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F95cb2e2f-b076-4df8-b93d-fbab3d71d35c_1986x1032.png)

A video world model inputs and output

For a game, the signal that matters most is the player’s actions. That is what makes a world playable. For example, when a player presses a key to move forward or turns the camera to look around, the next frame changes to match. But generating believable frames, even ones that respond to input, is not the same as running a game, for two main reasons.

![](https://substackcdn.com/image/fetch/$s_!QhRG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff5859db-394f-4c08-8099-0dfdccbf10f9_1568x858.png)

Player input becomes the signal that steers the next frame.

### Reason 1: missing the systems that make a game

The first reason is that a video model does not have the systems a game runs on. Its strength, generating what looks right next without simulating every object, is also why it cannot hold a game together. It has no durable memory of the world, no consistent rules, and no reliable way to turn a player’s input into the right outcome. The simplest way to see this is to turn the camera away from something and then back. “If the character turns back, is the world still the same?” Singh says. “In most video models, it won’t be.” The model regenerates the scene and quietly changes it.

![](https://substackcdn.com/image/fetch/$s_!TGhL!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb7a874e8-72df-4889-9445-1d3e9f502012_2048x432.png)

Objects may change as the camera turns away

Multiplayer exposes the gap further. A video model can render a crowd of 500 people, but those are pixels, not 500 separate players, each with a position, an inventory, and actions of their own. Painting a crowd and simulating one are different problems. However good it looks, a standalone video world behaves more like a moving picture than a game: a guided dream, with no persistence and no real interaction.

There are quieter gaps too, ones that show up in how games are built rather than how they look. A pure video model is hard to test and hard to refine. With normal game code, a creator can change one rule, run it, and check the result. A model that generates the world from learned weights does not give you that kind of precise, repeatable control, which makes exacting competitive gameplay and reliable, intelligent non-player characters hard to guarantee. These are not edge cases. They are the day-to-day work of making a game good.

### Reason 2: pixels are not understanding

The second reason is deeper. A video model works entirely in pixels, and pixels are not understanding. It can draw a flawless bottle without knowing it is a bottle: that it opens, that it holds water, or that it falls when you let go. As Singh puts it, pixels alone will never understand the world. Something else has to do the reasoning, working out what things are and how they behave. A model that only paints the scene has no real grip on the rules, the physics, or the cause and effect a game runs on. It is rendering the world, not modeling it.

![](https://substackcdn.com/image/fetch/$s_!FRO6!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd8afde9c-2823-414e-9812-4a7e4663be07_1788x910.png)

No understanding of physics. It has no idea what a bottle does.

A game engine is built to do exactly what the model cannot. It does not paint pixels; it tracks what exists, enforces the rules, and computes the physics. So if a video model lacks all of this, why not just build the whole game in the engine? That is the question the next section takes on.

## Why a game engine alone isn’t enough

A game engine is built for the parts a video model cannot do. It tracks the exact state of the world, applies rules the same way every time, and keeps that state consistent across sessions and players. Engines also compute physics directly, including collisions and the movement of objects such as a car’s position, velocity, and steering. This side of game development is mature and well understood.

![](https://substackcdn.com/image/fetch/$s_!YwAq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa326d437-6a8a-4739-92e1-80103394da09_1498x1220.png)

A game engine’s real job

Photorealism is where engines struggle. To make a world look real, the engine has to render all of that detail explicitly: high resolution textures, complex lighting, and simulation for effects like light scattering through fog or the way different materials reflect it. All of that is expensive to compute, and it only gets more expensive the more realistic you push it. So engines cut corners. They bake lighting ahead of time instead of calculating it live, swap in simpler versions of objects that are far away, reuse textures, or lean on a stylized look that hides the missing detail. The tricks work, but they are also why most games still look like games, not the real world.

Avoiding those shortcuts, and actually reaching photorealism, comes at a cost that falls on people, not just servers. Creators need more skill and time to build the detail, and players need more powerful devices to run it. A big studio can absorb that. A two-person team, or someone on an everyday phone, cannot. This is the real limit: an engine can give you a real game, but realistic graphics through it stay out of reach for most creators and most players. Each technology is strong exactly where the other is weak, so the obvious move is to combine them.

## The core idea: a hybrid architecture

Roblox’s position is that you should not ask a video model to act as a game engine, and you should not ask a game engine to generate photorealism by itself. Instead, you build a system that splits the work so each part does what it is good at.

Roblox calls that system Roblox Reality. It has three parts: the Roblox game engine, the Roblox Cloud, and a video world model the team calls the Super Upsampler. The first two keep the world consistent. The third makes it look real.

![](https://substackcdn.com/image/fetch/$s_!VQGA!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feee57af5-b78f-4539-9c5b-1ce7f7a24c49_1448x952.png)

The three parts of Roblox Reality

The game engine is the part that knows what is actually there. It keeps a structured record of the world, called the data model, that lists every object and its properties: where the car is, how fast it is moving, which way it points, what it is made of. On top of that record it runs the simulation, the physics and the rules, the same way every time. Because it computes all of this exactly and repeatably, the engine can act as the single source of truth that every player’s view has to agree with.

![](https://substackcdn.com/image/fetch/$s_!n3NS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb84c6457-c760-447d-ae59-ccf51a61c218_2048x716.png)

The data model: a structured record of every object in the world.

The Roblox Cloud is what runs that engine at scale. It stores each world’s state durably, so a game is still there when you come back days later, and it runs millions of live game sessions across data centers around the world. Keeping those sessions physically close to players is what makes fast, fair multiplayer possible, because the authoritative state lives near the people acting on it instead of on the far side of the planet.

![](https://substackcdn.com/image/fetch/$s_!q6vW!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff760169-c8f6-4fe7-aea8-f0ea57132626_2048x1120.png)

Millions of live sessions, each running close to its players.

The Super Upsampler is the video world model, and its name describes the job. It does not invent the world from scratch. The engine first renders a complete but plain frame, with the right shapes, positions, and camera motion but simple textures and lighting, and the model upsamples that frame into something photorealistic. As Singh puts it, the model is mostly adding the textures and the fine detail, not deciding what is in the scene. It is a large base video model that Roblox post-trains for the task, so it already knows how the visual world looks and only has to fill in the details: the textures, the lighting, the water on a windshield, the leaves moving as a car passes. The engine does the exact, inexpensive part, and the model does only the expensive, fuzzy part, which is what makes the hybrid cheaper than either extreme.

![](https://substackcdn.com/image/fetch/$s_!Z5_A!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2138285-56f7-47f1-84cf-a5fa82e17d80_2048x780.png)

The engine drafts the frame; the model makes it look real.

There is a deeper idea behind this split. It is tempting to assume the goal is one giant model that learns to do everything, including the reasoning about what is happening and why. Roblox’s bet is the opposite. A world model still needs reasoning, but it does not all have to live inside the network. As Singh puts it, in a hybrid the reasoning can sit beside the model, in the engine and its rules and physics. That frees the video model to spend all of its capacity on the one thing it is best at: the pixels.

Dividing the work like this only pays off if the player never feels the seam. For that, the engine and the model have to stay tightly in sync, frame by frame.

### How do the engine and the model stay in sync?

The real engineering is in how these parts connect, because the model cannot be allowed to invent the world freely. Every frame, before it generates a single pixel, it is conditioned on what the engine produces. Those inputs are built by cloud systems that handle level of detail and compositing, then delivered to the edge over a content delivery network, the same way video is streamed.

Take a single frame in a driving game. The engine generates a low-quality rendered frame, a depth map, the scene’s lighting and weather, and structured details for every object. Each is a different kind of signal that the upsampler will later use to render a photorealistic version of the frame.

![](https://substackcdn.com/image/fetch/$s_!uzHr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e721768-32a9-40a9-b47f-20af1c16d73d_2048x962.png)

The engine produces a draft plus the facts of the scene.

The dense, pixel-aligned signals carry a value for every pixel: the rough rendered frame, and a depth map giving each pixel’s distance from the camera. Because they share the same grid as the output, they are concatenated with the model’s input, or injected through a ControlNet-style side network, so every generated pixel stays locked to its depth and color.

![](https://substackcdn.com/image/fetch/$s_!uffc!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84e7562c-4c8b-4259-9dd9-16ef63c1e55a_1448x1332.png)

Dense signals to influence every generated pixel

The global signals are a single setting for the whole shot, like midday, light rain, and the sun low on the left. These are applied through modulation, scaling and shifting the model’s activations everywhere at once, the same way a diffusion model feeds in its timestep.

![](https://substackcdn.com/image/fetch/$s_!yrGx!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F35b3b379-347e-40aa-aea4-db399d7d3b81_2048x1192.png)

Global signals to influence the whole frame at once.

The structured signals are compact, text-like descriptions: each object’s details, such as a metal sports car at position (120, 0, 48) moving 40 meters per second, plus any prompt for the overall style. These enter through cross-attention, so any part of the frame can draw on them as needed.

![](https://substackcdn.com/image/fetch/$s_!qnUT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc4045fe4-5cc5-44ed-871e-cddb944d05a0_2048x1192.png)

Structured signals influence through the cross-attention layer.

From all of this, the model paints the final 2K frame, the gloss on the wet paint, the glare on the windshield, the rough asphalt, the spray off the tires, without ever moving the car or changing how far away anything is.

![](https://substackcdn.com/image/fetch/$s_!Ss93!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F157489a3-0d84-409f-b7bc-4a6a1af87974_1636x1358.png)

Full upsampler inputs before producing the next frame.

The data model is what keeps the world from drifting. It tells the model which objects are present and fixed, so a car stays a car with four doors from one frame to the next. The model does not get the whole game state each frame, though, since that would be far too much to process. Instead, a retrieval step pulls only the objects relevant to what it is rendering right now. The engine stays the authority on what exists, and the model only decides how it looks.

State and pixels are also stored differently, and that difference is the center of the design. The consistent world state lives in the data model on the server, where it can be shared across every client and kept stable over a long session. The look of the world lives in the model’s video latents, which are regenerated continuously and never need to be saved. The server decides the truth that everyone shares, and the model fills in the parts that can safely differ a little from one player to the next.

## The hard problems and how Roblox is approaching them

With the architecture in place, the real work is making it run in real time, for millions of players at once. The Roblox engine and its global infrastructure are in production today. The video model side is still in the lab, not yet running in real time. Below are the four problems standing between the design and shipping the model into production.

### Latency

A game has to respond the moment a player acts. As Singh puts it, a player who clicks can’t be left waiting seconds for the result. Most video models can’t meet that bar. They generate a whole clip at once in an offline pass that reads in both directions across time, which can take several seconds. A playable game needs a fresh frame every few tens of milliseconds. That means closing the gap from roughly five seconds down toward about 30 milliseconds.

The main technique is self-forcing, the core of Roblox’s acquisition of Morpheus AI, whose founder developed the method. Self-forcing turns a slow offline model into an autoregressive one that generates frame by frame, each frame conditioned on the frames it just produced, so it can stream output continuously instead of computing a full clip in one shot.

![](https://substackcdn.com/image/fetch/$s_!gS2q!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc4105831-64e9-48e2-b26b-da07253c633b_2048x1022.png)

Offline vs self-forcing

Self-forcing is not the only lever. The models are made smaller, and their running memory, the key-value cache, is compressed, which Roblox calls critical for reaching high resolutions without the cost spiraling. Generation also runs on H200 and B200 class GPUs in edge data centers placed right next to the game-engine instances and close to players, so the network round trip stays short.

![](https://substackcdn.com/image/fetch/$s_!imUj!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe20341be-cf91-464f-a2fe-8ee0b4638f6c_2048x902.png)

Four latency levers

### Consistency

The data model discussed earlier keeps the world from drifting frame to frame. The harder challenge is maintaining consistency across many frames.

![](https://substackcdn.com/image/fetch/$s_!TIUV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1974c00c-ca13-44cc-a3e9-4ca090ee2286_2048x710.png)

Long-video consistency

Over a long session, small errors accumulate, and a world can slowly lose track of itself. The model has to stay coherent across minutes of play, not just a handful of frames at a time.

![](https://substackcdn.com/image/fetch/$s_!ylek!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7adde410-ecec-4590-991a-a49bdc1fb2b4_2048x966.png)

Drift curve

Staying coherent over a long session takes a model that can hold much more of its own history, and Roblox chose to acquire that capability rather than build it from scratch. The acquisition of Morpheus AI, the same one behind self forcing, brought the long-context world-model work Roblox needed for exactly this. Roblox is now extending the model’s context window, so what it generated ten minutes ago still shapes what it generates now.

### Multiplayer

Multiplayer is the clearest failure of video models and the problem most specific to Roblox. A model can generate a crowd, but it cannot run one. Managing 20,000 players reacting in real time means tracking 20,000 separate states, not generating a believable picture of a crowd. The requirement is also subtle at a small scale. When one player moves an object, every other player who can see it has to see it move too. An action is not only what a player does, it is the effect of that action on everyone else’s view of the world.

![](https://substackcdn.com/image/fetch/$s_!QdSE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e55f185-6742-4d8f-8576-72fa0b428c67_2048x994.png)

Moving left. One player moves, everyone sees it.

The engine makes this possible by acting as the server authority, computing one true state that all players share. Each player’s video model then generates that player’s own view, conditioned on the shared state, so the views differ in perspective but agree on the facts. To keep this responsive, the system also runs a quick predictive simulation on the player’s own device for immediate actions, while the server confirms the authoritative result a moment later. In the future, a player’s own avatar may be rendered locally and placed on top of the streamed video, so the movements a player cares about most feel instant. Doing all of this for thousands of players at once is an active research area, not a solved feature, and Singh describes multiplayer actions as a central focus of the team.

![](https://substackcdn.com/image/fetch/$s_!AjX-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F477cff0c-dd4f-4e7f-a3e0-3edf870255c5_2048x939.png)

Cartridge harness

### Creator control

A game only becomes worth playing when a creator shapes it. What makes a game fun is usually the rules and logic a creator adds, not how detailed it looks. Even a plain-looking game can take off when the gameplay underneath it is good. So the video model has to stay under the creator’s control, and giving them that control is still an open area of research.

One concrete piece comes from Lucid AI, a team that joined Roblox. Its founder built what Roblox calls a game cartridge harness, which wraps the deterministic logic of a real game engine around a video world model. The point is to let a world look generated while still behaving according to fixed, predictable rules the creator sets.

![](https://substackcdn.com/image/fetch/$s_!UXKN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb68c0d4-e0cf-4271-ac43-5ccfd4b35a92_2048x1177.png)

Client prediction

The harness is also how a player’s controls reach the model. The standard movement keys, the WASD inputs, are fed in as conditioning, so pressing forward drives the generated view directly instead of only moving a character inside the engine. Taking real-time player input and turning it into the right next frame is the kind of control a standalone video model cannot handle. How creators will ultimately direct the model beyond movement, through written prompts, through the data model, or some mix of the two, is not yet decided.

### Roblox’s bet: creators, compute, and a 20-year head start

These are difficult problems, and Roblox’s case for solving them rests on a few advantages. It has a large community of creators to build with and learn from. It owns its compute, running more than two dozen edge data centers and its own GPUs instead of renting capacity from cloud providers, which matters when the video model has to run for every player at low latency. It has also spent close to 20 years building the data model, the structured record of objects and physics the whole hybrid depends on.

To strengthen the AI side, Roblox brought together founders from several labs and gave them autonomy under a short set of values. Respect the community, take responsibility, get stuff done. Each team came in solving a different piece of the problem. Morpheus AI brought self forcing and the low-latency, long-context work behind it. Lucid AI brought the game cartridge harness, the bridge between deterministic game logic and a video model. Dynamics Lab brought a real-time, general-domain world engine that lets a person upload any image, a photo, a drawing, a painting, and step into it as a live, interactive world they can shape with text prompts and share with friends to play instantly. Put together, those are the pieces of speed, control, and generation that a hybrid needs.

![](https://substackcdn.com/image/fetch/$s_!MN_0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e2a2544-c54c-4362-826f-90b27f2adba5_2048x1005.png)

The four advantages Roblox is betting on

There is one more advantage, and it is operational rather than technical. Even once the model runs in real time, Roblox will have to serve it to millions of players at once, and few companies have more practice keeping a system alive at that scale. Capacity is hard to predict when a game can jump from 3 million to 22 million players in a few weeks, so Roblox plans for sudden surges instead of assuming they will not come. Rather than throttling traffic when a system is under load, it runs a weekly exercise it calls Taco Tuesday, deliberately removing capacity from services in production to find the limits first. The test is automated, and any engineer can start one. Reliability is treated as everyone’s job, with executives on the same on-call rotation as engineers, holidays included.

## What’s next

An early version of Roblox Reality is expected later this year or early next, with cost and scaling still to solve before it can reach large numbers of players. The first quality target is 2K resolution at 60 frames per second, with 4K as the longer goal.

The more important change is who gets to build photorealistic games. Because the heavy rendering happens on shared edge GPUs rather than on the creator’s machine or the player’s device, visual quality stops depending on the size of a team’s budget or the power of a player’s phone. A creator can get high-end results on an ordinary device. The goal Singh describes is for a two person studio to build something as rich as a large studio’s work, without having to trade complexity against visual quality.

Singh expects the progress to arrive in large steps rather than small ones, and he expects world models to matter well beyond games. Roblox’s approach is worth watching because it does not wait for a video model to solve everything on its own. It gives the model the support it has always lacked: an engine that remembers the world, enforces its rules, and keeps it true for everyone playing.