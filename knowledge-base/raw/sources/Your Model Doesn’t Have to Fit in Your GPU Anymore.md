---
title: "Your Model Doesn’t Have to Fit in Your GPU Anymore"
source: "https://alizahidraja.medium.com/your-model-doesnt-have-to-fit-in-your-gpu-anymore-3cfde167c382"
author:
  - "[[Ali Zahid Raja]]"
published: 2026-11-04
created: 2026-11-04
description: "More"
tags:
  - "clippings"
---
*A practical guide to hosting LLMs on your own machine: the memory math, quantization, how I use Odysseus to pick models and the MoE trick that lets ordinary hardware run models it has no business running.*

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*F_hR-uX2KhQiDeTw7eaA3A.jpeg)

Most people I have seen around LinkedIn or X pick a local model backwards.

They see a model trending they will download 20GB of weights and watch it type two words a second (I have personally done this). Then they decide local AI is a toy for people with RTX 4090s and go back to paying for an API.

I’ve been running models on my own hardware for a while now, across vLLM, Ollama and llama.cpp. The thing I wish someone had told me early is that “will this model run on my machine” is mostly a math question, not a question answered by influencers or hype people.

The short version: for a lot of new models, your GPU doesn’t need to hold the whole thing anymore. Sometimes you don’t need a GPU at all.

The following is the long version. It covers the memory math, quantization, which runtime to use, how I use Odysseus to figure out what actually runs well on my machine and the new wave of repos that run huge models on CPU by only touching the parameters that are awake. I’ll also be honest about where this is still not very scalable because it isn’t.

You can read it all or just give it to a LLM you use already to set it up, either way hope this helps!

## Why bother running models locally

Four reasons

Privacy is the obvious one. If you’re building a knowledge base over a client’s internal documents, “we send all of it to an API” is a sentence that ends a lot of procurement conversations. Local means the data never leaves the box in any way shape or form

Cost at volume is the second. An API is cheaper than hardware until it isn’t. If an agent is chewing through millions of tokens a day on boring work (classification, extraction, summarising emails), a local model that’s good enough pays for itself.

Control is the third. Nobody deprecates your model on a Tuesday. Nobody changes the tuning under you. Nobody can revoke access randomly. The weights you tested are the weights you run.

Offline is the fourth. Planes, air-gapped clients, possible nuclear war and internet shutdown and if you live in Pakistan like me, internet that decides to take the afternoon off.

Now the honest part. The best open models are not local models. On the Artificial Analysis index, the top open-weight model right now scores 46 against Claude Opus 5.5’s 58 (guess which model wrote this xD) and that open model needs eight H200s to run ([Pinggy’s roundup](https://pinggy.io/blog/best_open_source_self_hosted_llms_for_coding/)). What you run at home is a tier below that. For a lot of everyday work that tier is plenty. For hard reasoning and long agentic coding, frontier APIs still win, but that isn’t the point of this article

Local isn’t a replacement (unless you have crazy hardware) it’s a second engine.

## The only math you actually need

Two numbers decide everything: how much memory the model needs, and how fast that memory can feed it.

First thing, memory. A model’s size is roughly its parameter count times the bytes per parameter. At full precision (BF16) that’s 2 bytes each. At 8-bit it’s about 1. At the 4-bit quants most people run, it’s a bit over half a byte.

The rule of thumb I use (I don’t use it, I just use whatever Odysseus suggests0:

```c
BF16    ≈ 2.0 GB per billion parameters
Q8_0    ≈ 1.1 GB per billion
Q4_K_M  ≈ 0.6 GB per billion
```
```c
8B model at Q4    ≈ 5 GB
27B model at Q4   ≈ 16 GB
35B model at Q4   ≈ 21 GB
```

Then add the KV cache, which is the model’s working memory for your conversation. It grows with context length. A short chat costs almost nothing. A 128K-token context on a big model can cost several gigabytes by itself. Then leave a GB or two for the runtime and your OS.

If weights plus KV cache plus overhead fit in your VRAM, you’re golden. If they don’t, something has to live somewhere slower.

Two cheap fixes for the KV cache: use a shorter context (most chats don’t need 128K), and quantize the cache itself to 8-bit, which llama.cpp and Ollama both support. Newer models help too. Qwen3.8–27B only uses full attention in a quarter of its layers, so long contexts cost far less memory than a normal 27B would ([Morph’s breakdown](https://www.morphllm.com/qwen-3-8)).

Second, speed. This is the part people skip and it’s the part that explains everything later in this article.

Every time a model generates a token, it has to read the weights it uses out of memory. Every single token. So generation speed is capped by how fast your memory moves bytes:

```c
tokens/sec ceiling ≈ memory bandwidth ÷ bytes read per token
```

Some rough bandwidth numbers:

```c
Dual-channel DDR5 desktop RAM     ~90 GB/s
AMD Strix Halo (Ryzen AI Max)     ~256 GB/s
RTX 3060 12GB                     ~360 GB/s
Apple M4 Max                      up to ~546 GB/s
RTX 4090                          ~1,000 GB/s
```

Take a dense 27B model at 4-bit, about 16GB. On a 4090 the ceiling is around 60 tokens a second. On plain desktop RAM it’s about 5. That’s why everyone tells you to buy a GPU

Hold that thought. There’s a kind of model where you don’t read all 16GB per token.

## Quantization, minus the jargon

Quantization means compressing the weights from 16-bit numbers down to 8, 6, 4, sometimes 2 bits. You lose a little quality and gain a lot of room.

The format you’ll see everywhere for local use is GGUF, which is what llama.cpp, Ollama and LM Studio run. File names look like `Qwen3.6-35B-A3B-Q4_K_M.gguf`. The bit after the model name is the quant.

What I’d tell a friend:

- Start at Q4\_K\_M. It’s the default for a reason: big savings, small quality loss.
- Go Q5 or Q6 if you have room to spare and care about precision (code, maths, structured output).
- Q8 is near-lossless and usually overkill for local.
- Below Q4 (Q3, Q2, the IQ1 and IQ2 types) is for squeezing in a model that otherwise wouldn’t fit. Fine for chat. Risky for tool calling.

That last one isn’t me being cautious. The [flash-moe](https://github.com/danveloper/flash-moe) project, which we’ll get to, found that at 2-bit the model started writing `\name\` instead of `"name"` in its JSON, which made tool calling unreliable. They run 4-bit in production for that reason. If you're building agents, broken JSON is a broken product.

Also, get your quants from people who do them well. Unsloth’s “dynamic” quants keep the sensitive layers at higher precision, and they’re usually the first GGUFs out after a big release.

A bigger model at a lower quant often beats a smaller model at a higher one. Often, not always. Which is why you test on your own systems and why the next two sections exist.

## Pick a runtime (the thing that actually runs the model)

There are a lot of names here and they mostly sit on top of each other.

[llama.cpp](https://github.com/ggml-org/llama.cpp) is the engine under most of local AI. Plain C/C++, runs on CPU, NVIDIA, AMD, Apple and Vulkan. It’s the most flexible, and it’s where the new MoE tricks land first. If you want control, you end up here eventually.

```c
# download a model from Hugging Face and serve it
llama-server -hf unsloth/Qwen3.6-35B-A3B-GGUF:Q4_K_M -c 32768 --port 8080
```

That gives you an OpenAI-compatible API at `http://localhost:8080/v1`. Anything that can talk to OpenAI can talk to it.

Ollama is easy mode. One installer with one command and models pulled by name. It serves an OpenAI-compatible API on port 11434, and on Apple Silicon it now runs on Apple’s MLX framework ([state of Ollama in 2026](https://angelo-lima.fr/en/ollama-2026-state-of-the-art-en/)).

```c
ollama run gemma4:e4b
ollama run qwen3.8:27b
```

LM Studio is the same idea with a proper desktop app. Good if you don’t want a terminal and nice for browsing quants visually.

vLLM, and its cousin SGLang, is what you use when more than one person is hitting the model. It’s built for throughput on GPUs: batching lots of requests, serving a team, running in production. Overkill for one person on a laptop. The right tool the moment you have users.

The way I think about it: Ollama to try things, llama.cpp when I need to tune, vLLM when it’s serving someone other than me.

## How I use Odysseus to figure out what to run

This is where most of my setup comes together.

[Odysseus](https://github.com/pewdiepie-archdaemon/odysseus) is a self-hosted AI workspace that PewDiePie (yeah the youtuber, economy is THAT bad) released on 31 May 2026. It is not a model and it’s not a runtime. It’s the layer on top: chat, agents, deep research, documents, memory and MCP tools, all pointed at whatever models you connect, local or API. It went past 70,000 GitHub stars in about three weeks ([ModelFit](https://modelfit.io/blog/pewdiepie-odysseus-local-ai/)).

Two features are why I use it.

The first is the Cookbook. It scans your hardware, scores a catalogue of 270+ models against your actual VRAM and RAM, and gives you one-click download and serve. Under the hood it estimates whether the weights and KV cache will fit, then launches the serving command for vLLM, llama.cpp or Ollama in a background tmux session, so it keeps running when you close the browser ([DeepWiki’s walkthrough of the code](https://deepwiki.com/pewdiepie-archdaemon/odysseus/6-cookbook-and-model-management)). That kills the most annoying part of local AI, which is downloading 20GB to find out it doesn’t fit.

The second is Compare. Same prompt, every connected model, side by side, blind. You don’t know which answer came from which model until after you pick.

The blind part matters more than it sounds. If you know which answer came from the 27B and which came from the 9B, you will grade the 27B more kindly. Everybody would honestly. A blind test on your own prompts is the cheapest honest benchmark you can run, and it beats any leaderboard for your use case.

So my loop looks like this:

1. Open the Cookbook and see what it thinks fits.
2. Shortlist two or three candidates, usually one dense and one MoE.
3. Serve them and run my real prompts through Compare, blind.
4. Keep the winner running. Redo the loop when a new model drops.

Setup is a few commands:

```c
git clone https://github.com/pewdiepie-archdaemon/odysseus.git
cd odysseus
cp .env.example .env
docker compose up -d --build
docker compose logs odysseus   # the first-boot admin password is printed here
```

Then open `http://localhost:7000` go to Settings, and point it at your model server.

If you already run Ollama, you don’t even need the Cookbook. Add `http://localhost:11434/v1` as an endpoint. If Odysseus is in Docker and Ollama is on the host, start Ollama with `OLLAMA_HOST=0.0.0.0:11434` and use `http://host.docker.internal:11434/v1` instead, because `localhost` inside a container means the container. Same idea for a llama.cpp server on port 8080.

A few honest caveats, mostly from [ChatForest’s review](https://chatforest.com/reviews/odysseus-pewdiepie-self-hosted-ai-workspace-review-2026/):

- The Cookbook’s guess is a starting point, not the truth. The project’s own roadmap names Cookbook reliability on other computers as the area most likely to need work.
- On a single GPU or CPU it defaults to Q4\_K\_M and halves the context window until the model fits. Check what context you actually got before blaming the model for forgetting things.
- Slow CPU inference can trip its 45-second default timeout on non-streaming endpoints.
- Treat it like an admin console. It has shell access, file access, model downloads and your API keys, it serves plain HTTP, and the agent’s bash tool isn’t sandboxed. Don’t put it on the internet without HTTPS and a reverse proxy in front.

## Active parameters changed the game

This is the bit that changed this year, and why I think local is about to get a lot more interesting and much needed

Most of the strong new open models are Mixture-of-Experts, or MoE. Instead of one giant block of weights, the model has a lot of small “expert” networks and a router that picks a few of them for each token.

Look at the name Qwen3.6–35B-A3B. 35B is the total parameter count. A3B means roughly 3B are active per token. The model is 35B big, but each token only does the work of a 3B model.

That splits the math from earlier into two separate questions:

```c
memory needed     -> set by TOTAL parameters   (every expert has to live somewhere)
speed per token   -> set by ACTIVE parameters  (only a few experts get read)
```

Go back to the bandwidth rule. A dense 27B at 4-bit reads about 16GB per token. A 35B-A3B at 4-bit reads about 2GB. On plain desktop RAM, that’s the difference between a ceiling of ~5 tokens a second and a ceiling in the 40s. Real numbers land well under the ceiling, but the gap is the point.

Which means the experts don’t need fast memory. They can sit in cheap system RAM, and lately, even on your SSD. The GPU only needs the always-on parts: attention, the shared layers and the KV cache.

That’s the whole trick. Here’s how to use it, from easiest to wildest.

The easy one is llama.cpp with the experts in RAM. It has flags built for exactly this. `--cpu-moe` keeps all the expert weights in system RAM. `--n-cpu-moe N` keeps the experts of the first N layers in RAM and leaves the rest on the GPU, so you can dial it to your card. Newer builds also turn `--fit` on by default, which picks a split for you.

```c
# Qwen3.6-35B-A3B on a 12GB card with 32GB of system RAM
llama-server -hf unsloth/Qwen3.6-35B-A3B-GGUF:Q4_K_M \
  -ngl 99 --n-cpu-moe 32 -c 32768 -fa on
```

`-ngl 99` says "put everything on the GPU", and `--n-cpu-moe 32` is the exception that sends 32 layers' worth of experts back to RAM. 32 is a good first try on an RTX 3060 12GB, and on an 8GB card you push it higher. Then try a few values, because the best one depends on your GPU, CPU and RAM speed.

Actually test it. One r/LocalLLaMA user running a Qwen 35B-A3B on 12GB of VRAM went from 17 to 34 tokens a second just by raising `--n-cpu-moe` from 8 to 30, which means pushing *more* onto the slower CPU made it faster. Counterintuitive but trial and error is recommended by default in everything related to Computer Science (I dont make the rules)

The new one is a GPU cache for hot experts. On 7 October 2026, llama.cpp merged a cache that keeps the experts the router picks most often in VRAM, while the rest stay in RAM and only misses cross PCIe. In the PR author’s test on a 93.7GB model, an RTX 5090 went from 30.8 to 67.8 tokens a second, 2.2x, with something like:

```c
llama-server -m model.gguf -cmoe --moe-cache-mib 19000 -fa on -c 32768
```

Gains shrink on smaller cards. One tester on a 16GB RTX 5060 Ti saw about 1.3x, and on an RTX 3090 the cache was only 1 to 5% faster than a well-tuned `--n-cpu-moe` ([Developers Digest has the full breakdown](https://www.developersdigest.tech/blog/llama-cpp-moe-offload-n-cpu-moe-vs-moe-cache-2026)). So tune `--n-cpu-moe` first, then try the cache.

The wild ones stream experts straight off your SSD. This is what I meant about the new repos. If only a few experts get read per token, why hold all of them in RAM at all? Keep the always-on part in memory and read the experts from disk when the router asks for them. RAM becomes a cache. Your SSD becomes very slow, very large VRAM.

- [flash-moe](https://github.com/danveloper/flash-moe) ran Qwen3.5–397B-A17B, a 209GB model, on a 48GB MacBook Pro M3 Max at 4.4+ tokens a second, streaming experts off the SSD with hand-written Metal shaders. The catch: it’s hardcoded for that one model, and it uses 4 experts per token instead of the standard 10, which is a real quality hit ([InsiderLLM](https://insiderllm.com/guides/flash-moe-run-397b-model-laptop/)).
- [colibri](https://github.com/JustVugg/colibri) is a pure C engine with zero dependencies that does the same thing across a bunch of model families. It needs 8GB of RAM minimum and ships an OpenAI-compatible server. Its own numbers include Qwen3.6–35B-A3B at 6 tok/s on CPU alone and 30 tok/s on an RTX 3070, and the 744B GLM-5.2 at 1.83 tok/s on a 128GB Ryzen AI Max+ 395.
- [BigMoeOnEdge](https://github.com/Helldez/BigMoeOnEdge) does it on top of stock llama.cpp, losslessly and CPU only. Its numbers: Qwen3.6–35B-A3B at 5 tok/s on a 12GB phone, 4.8 tok/s on a 16GB Windows laptop and 22.4 tok/s on a 16GB Apple laptop.
- [KTransformers](https://github.com/kvcache-ai/ktransformers), from Tsinghua, is the serious workstation version: hot experts on the GPU, cold experts computed on the CPU with optimised kernels, aimed at running the giants like DeepSeek and Kimi on one GPU plus a lot of RAM. In March 2026 it added AVX2-only support, so it’s no longer just for fancy server CPUs ([Phoronix](https://www.phoronix.com/news/KTransformers-0.5.3)).

colibri and BigMoeOnEdge both expose OpenAI-compatible endpoints, so you can plug them straight into Odysseus and run them through Compare like any other model.

Now the reality check. 1 to 2 tokens a second on a 744B model is a demo, not a workflow. You will not run an agent loop on that. But a 35B-A3B at 20 to 30 tokens a second on a 12GB gaming GPU, or at a usable speed on a laptop with no GPU at all? That’s a real tool. Not long ago, the standard advice for that class of model was a 24GB card.

## What to run on what (as of November 2026)

This moves fast, so treat it as a starting map and let the Cookbook and Compare make the final call. Sizes are rough 4-bit numbers.

```c
8-16 GB RAM laptop, no GPU
  Gemma 4 E4B            ~6 GB    small, multimodal, does tool calling
  Qwen3.5 9B             ~6 GB
  gpt-oss-20b                     built to fit in 16 GB
  Qwen3.6-35B-A3B                 via colibri / BigMoeOnEdge, if ~5 tok/s is fine
```
```c
12-16 GB GPU + 32 GB RAM (the gaming PC)
  Qwen3.6-35B-A3B        ~21 GB   with --n-cpu-moe, the sweet spot
  Gemma 4 26B-A4B        ~17 GB24 GB GPU or 32 GB Mac
  Qwen3.8-27B            ~15 GB   dense, Apache 2.0, the local coder to beat
  Gemma 4 31B            ~17 GB64-128 GB unified memory (Strix Halo, big Macs)
  gpt-oss-120b           ~60 GB
  Qwen3-Coder-Next       ~44 GB   80B total, 3B activeWorkstation, multi-GPU or KTransformers territory
  DeepSeek-V4-Flash      284B total, 13B active
  GLM-5.3-Flash          320B total, 18B active
```

Check compliance rules tho for if you are working for a vendor

## Why this still isn’t very scalable

I’m bullish on this but there are facts I should say out loud

Memory got expensive. The whole RAM-offload idea assumes RAM is cheap, and in 2026 it isn’t. A 64GB DDR5 kit that cost about $222 in October 2025 was tracking around $1,099 to $1,272 by September 2026. Sam Altman straight up thinks it shouldn’t even be used in PCs so just imagine what is going to happen to the rates of all kinds of chips.

Memory makers moved capacity to high-bandwidth memory for AI datacenters, and Micron’s CEO said in June that he expects tight conditions to last beyond 2027. Ironically, that’s exactly why the SSD-streaming repos matter. An NVMe drive is the one kind of memory most people already have plenty of.

It’s one user at a time. Everything clever in this article is tuned for a batch size of one: you, chatting. The moment five people hit the same box, you want the whole model in VRAM and something like vLLM batching requests. Offloading experts to the CPU doesn’t scale with users but honestly this is a great starting point!

Long prompts hurt. Reading a big prompt is much slower on CPU than generating tokens, so long-context work like feeding it a whole repo hurts more than chat does. Even the new llama.cpp expert cache only kicks in for batches of 32 tokens or fewer, so it speeds up generation, not prompt reading.

And it’s a tier below frontier, as covered up top.

But look at the direction of travel. For a long time the rule was that the model had to fit in VRAM. Then the experts could live in RAM. Now they can live on disk, and the always-on part is small enough for a phone. Every step moves the expensive bit of the model onto cheaper memory. Models are starting to be designed for it, too: Qwen3.8-Flash-Next ships a 51B n-gram table that’s meant to sit on SSD ([Pinggy](https://pinggy.io/blog/best_open_source_self_hosted_llms_for_coding/)).

So “can I run it” is turning into less of a question about which GPU you own and more about how long you’re willing to wait. That’s a much better question to be stuck on.

## Where I’d start this weekend

If you’ve never done this, here’s the shortest path that teaches you the most:

1. Install Ollama and run something small, like `ollama run gemma4:e4b`, just to watch tokens come out of your own machine.
2. Install llama.cpp and run a MoE model with `--n-cpu-moe`. Try three values and write down the tokens per second.
3. Set up Odysseus, connect both, and let the Cookbook show you what else fits.
4. Put your top two in Compare, blind, with ten prompts from your actual work.
5. Keep the winner and delete the rest. You will download too many models. Everyone does.

The question worth asking isn’t “which model is best” anymore. It’s “what can I run on what I already have”. The honest answer used to be “not much”. Now it’s “probably more than you think”, and it gets better every time someone ships a repo that moves the experts somewhere cheaper.

If you’ve got a weird setup running something it really shouldn’t be able to, I want to hear about it.

*Ali Zahid Raja is an applied AI engineer and architect. He builds agents, knowledge bases and local LLM systems for production, and is the author of ISNAD, a provenance framework for multi-agent AI.*