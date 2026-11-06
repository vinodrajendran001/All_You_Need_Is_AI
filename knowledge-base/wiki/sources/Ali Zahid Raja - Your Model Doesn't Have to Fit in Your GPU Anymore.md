---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-11-04-raja-model-gpu-fit
source_title: Your Model Doesn’t Have to Fit in Your GPU Anymore
source_author: Ali Zahid Raja
source_url: https://alizahidraja.medium.com/your-model-doesnt-have-to-fit-in-your-gpu-anymore-3cfde167c382
tags:
  - source/summary
  - local-inference
  - quantization
  - mixture-of-experts
  - inference
source_ids:
  - src-2026-11-04-raja-model-gpu-fit
status: active
---

# Your Model Doesn't Have to Fit in Your GPU Anymore

## Summary

Ali Zahid Raja's Medium guide to self-hosting LLMs argues that most people choose a local model
backwards: they pick the model first, then discover it does not fit or runs too slowly. He replaces
that with three pieces of arithmetic. Memory is weights plus KV cache plus runtime overhead.
Generation speed has a ceiling of memory bandwidth divided by the bytes read per token. For
mixture-of-experts (MoE) models, total parameters set the memory needed, while active parameters set
the speed. The practical consequence is the title claim: an MoE model can keep its experts in
system RAM, or even stream them from SSD, while the GPU holds attention, shared layers, and the KV
cache. The guide also describes the author's own selection workflow in the Odysseus workspace. Most
figures are third-party or self-reported and are presented as ceilings or rules of thumb, not as
controlled benchmarks.

## Key claims

### Fit is weights plus cache plus overhead

- Approximate weight memory per billion parameters: **BF16 ≈ 2.0 GB**, **Q8_0 ≈ 1.1 GB**, and
  **Q4_K_M ≈ 0.6 GB**. At 4-bit, an 8B model is about **5 GB**, a 27B model about **16 GB**, and a
  35B model about **21 GB**.
- The KV cache grows with context: a 128K-token context on a big model "can cost several gigabytes
  by itself", and the runtime and operating system need "a GB or two" more. The remedies offered are
  a shorter context or an 8-bit cache, which llama.cpp and Ollama both support.
- Architecture also changes the cache bill. Citing Morph, the author says Qwen3.8-27B uses full
  attention in only a quarter of its layers, so long contexts cost far less than in a normal 27B.

### Speed is bounded by bytes per token

- The ceiling is "memory bandwidth ÷" bytes read per token. Listed bandwidths: dual-channel DDR5
  **~90 GB/s**, AMD Strix Halo **~256 GB/s**, RTX 3060 12GB **~360 GB/s**, Apple M4 Max up to
  **~546 GB/s**, and RTX 4090 **~1,000 GB/s**.
- A dense 27B model at 4-bit therefore has a ceiling around **60** tokens per second on a 4090 and
  about **5** on desktop RAM. Real throughput lands below the ceiling.

### Quantization advice is task-dependent

- Start with Q4_K_M; use Q5 or Q6 for code, maths, and structured output; treat Q8 as near-lossless.
  Below Q4 is for squeezing in a model that otherwise would not fit: "Fine for chat. Risky for tool
  calling."
- The concrete failure: the flash-moe project found that at 2-bit the model wrote `\name\` instead
  of `"name"` in JSON, making tool calls unreliable, so it runs 4-bit in production.
- A bigger model at a lower quant often beats a smaller model at a higher quant, "Often, not
  always", which is why the author insists on testing on one's own tasks.

### Runtimes split by audience

llama.cpp's `llama-server` exposes an OpenAI-compatible API at `localhost:8080/v1`; Ollama serves
one on port 11434 and now runs on MLX on Apple Silicon; LM Studio is the desktop-app version. vLLM
and SGLang are "Overkill for one person on a laptop" but "The right tool the moment you have users".

### Odysseus as a selection workflow

Odysseus is a self-hosted AI workspace that PewDiePie released on 31 May 2026; it passed **70,000**
GitHub stars in about three weeks, per ModelFit. Its Cookbook scores a catalog of **270+** models
against the user's VRAM and RAM and launches vLLM, llama.cpp, or Ollama in a background tmux session.
Its Compare view runs the same prompt across connected models blind. Caveats, mostly from ChatForest's
review: on a single GPU or CPU it defaults to Q4_K_M and halves the context window until the model
fits; slow CPU inference can trip its 45-second default timeout on non-streaming endpoints; and it has
shell access, file access, and API keys, serves plain HTTP, and does not sandbox the agent's bash
tool.

### MoE offload is the main trick

- In Qwen3.6-35B-A3B, about 3B parameters are active per token. At 4-bit that reads about 2GB per
  token, so the desktop-RAM ceiling rises from about 5 tokens per second for a dense 27B to "a
  ceiling in the 40s".
- llama.cpp's `--cpu-moe` keeps all expert weights in RAM; `--n-cpu-moe N` keeps the first N layers'
  experts in RAM; newer builds turn `--fit` on by default to choose a split. **32** is called "a good
  first try on an RTX 3060 12GB", with higher values for an 8GB card. One r/LocalLLaMA user reportedly
  went from **17** to **34** tokens per second by tuning the value.
- A hot-expert GPU cache merged into llama.cpp on 7 October 2026. In the pull-request author's test
  on a **93.7GB** model, an RTX 5090 went from **30.8** to **67.8** tokens per second (**2.2x**).
  Gains shrink on smaller cards: about **1.3x** on a 16GB RTX 5060 Ti and only **1 to 5%** over a
  well-tuned `--n-cpu-moe` on an RTX 3090. The cache applies only to batches of **32** tokens or
  fewer, so it speeds generation, not prompt reading.

### SSD streaming and edge engines

- flash-moe ran Qwen3.5-397B-A17B, a **209GB** model, on a 48GB M3 Max at **4.4+** tokens per second
  by streaming experts from SSD, but it is hardcoded to that model and uses 4 experts per token
  instead of 10.
- colibri, a pure-C engine, needs 8GB of RAM and reports **6** tok/s on CPU and **30** on an RTX 3070
  for Qwen3.6-35B-A3B, plus **1.83** tok/s for the 744B GLM-5.2 on a 128GB Ryzen AI Max+ 395.
  BigMoeOnEdge reports **5** tok/s on a 12GB phone, **4.8** on a 16GB Windows laptop, and **22.4**
  on a 16GB Apple laptop. KTransformers, from Tsinghua, added AVX2-only support in March 2026.
- The author's own line: 1 to 2 tokens a second on a 744B model "is a demo, not a workflow", while a
  35B-A3B at 20 to 30 tokens a second on a 12GB GPU is "a real tool".

### Limits

- The best open models are not local: the top open-weight model scores **46** against Claude Opus
  5.5's **58** on the Artificial Analysis index and needs eight H200s, per Pinggy.
- RAM offload assumes cheap RAM. A 64GB DDR5 kit that cost about **$222** in October 2025 was around
  **$1,099** to **$1,272** by September 2026, and Micron's CEO expects tight conditions beyond 2027.
- Everything is tuned for batch size one. Long prompts are slow on CPU. Qwen3.8-Flash-Next ships a
  51B n-gram table intended to sit on SSD, a sign that models are being designed for cheaper memory.

## Why it matters

[[Mixture of Experts]] gains a deployment rule the vault had only implied: memory follows total
parameters, speed follows active parameters, so experts can live in slower memory.
[[LLM Inference]] gains a worked bandwidth-ceiling calculation for local decode.
[[Model Quantization and Efficiency]] gains a tool-calling failure at 2-bit, and [[KV Cache]] gains
the local operator's view of cache budgeting. [[Inference Serving Engines]] gains the batch-size-one
versus multi-user dividing line, [[Open Model Ecosystems]] a sober statement of the local tier's
capability gap, and [[Coding Agent Harness]] a model-selection and offload workflow for local agents.

## Tensions / open questions

- Most performance numbers are relayed from READMEs, a pull request, reviews, or forum posts; none
  were measured under a common protocol. Ceilings are arithmetic, not measurements.
- The 2.2x hot-expert result is the PR author's best case; the same article reports 1 to 5% on another
  card. The gain depends on card, model, and baseline tuning.
- The hardware table "as of November 2026" is partly garbled in the capture, with merged cells such as
  "~17 GB64-128 GB unified memory" and "3B activeWorkstation". It was not used for claims here.
- Qwen model names use en dashes in prose (for example "Qwen3.6–35B-A3B") and hyphens in code. This
  summary normalizes them to hyphens.
- Odysseus advice is the author's personal workflow, and its security caveats are significant for
  anyone exposing it beyond localhost.
- The aside "(guess which model wrote this xD)" suggests a model helped write the article; the extent
  is not stated.
- The capture's description field is just "More".

## Affected pages

- [[Mixture of Experts]]
- [[Model Quantization and Efficiency]]
- [[KV Cache]]
- [[LLM Inference]]
- [[Inference Serving Engines]]
- [[Open Model Ecosystems]]
- [[Coding Agent Harness]]

## Raw capture

- [[knowledge-base/raw/sources/Your Model Doesn’t Have to Fit in Your GPU Anymore]]

## Citations

- Canonical URL: <https://alizahidraja.medium.com/your-model-doesnt-have-to-fit-in-your-gpu-anymore-3cfde167c382>
- Byline: Ali Zahid Raja, described in the capture as an applied AI engineer and author of ISNAD, a
  provenance framework for multi-agent AI. Published on Medium.
- Published November 4, 2026; captured November 4, 2026.

## Related pages

- [[Mixture of Experts]]
- [[Model Quantization and Efficiency]]
- [[KV Cache]]
- [[LLM Inference]]
- [[Inference Serving Engines]]
- [[Open Model Ecosystems]]
- [[Coding Agent Harness]]
- [[Onur Sirin - How Local LLMs Run]]
- [[ByteByteGo - How to Run a Big Model on Cheap Hardware]]
- [[Sebastian Raschka - Using Local Coding Agents]]
- [[Small Language Models]]
- [[Qwen]]
- [[ByteByteGo - How Nvidia's New Nemotron Model Works]]
- [[Rohan Anil - The Hitchhiker's Guide to Training on Compute Islands]]
