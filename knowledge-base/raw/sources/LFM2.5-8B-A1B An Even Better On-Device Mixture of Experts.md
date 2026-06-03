---
title: "LFM2.5-8B-A1B: An Even Better On-Device Mixture of Experts"
source: "https://www.liquid.ai/blog/lfm2-5-8b-a1b"
author:
published: 2026-05-28
created: 2026-06-03
description: "Today, we’re releasing LFM2.5-8B-A1B, a high-throughput edge model optimized for fast, reliable tool calling and complex instruction following on consumer hardware, delivering compressed performance competitive with much larger models and day-one support across major inference frameworks."
tags:
  - "clippings"
---
Today, we're releasing **LFM2.5-8B-A1B**, an edge model built for fast, reliable tool calling on consumer hardware.

It builds on our [LFM2-8B-A1B](https://www.liquid.ai/blog/lfm2-8b-a1b-an-efficient-on-device-mixture-of-experts) release from October 2025, with an expanded 128K context window, scaled-up pretraining (from 12T to 38T tokens), and large-scale reinforcement learning. We also doubled its vocabulary to improve tokenization efficiency for non-Latin languages. The result is a model that chains tool calls, achieves tasks, and fits comfortably even on an entry-level laptop.

The base (LFM2.5-8B-A1B-Base) and post-trained (LFM2.5-8B-A1B) models are available today on [Hugging Face](https://huggingface.co/LiquidAI/LFM2.5-8B-A1B) and our [Playground](https://playground.liquid.ai/chat?model=LFM2.5-8B-A1B). Check out our [docs](https://docs.liquid.ai/) on how to run and fine-tune them locally.

![](https://cdn.prod.website-files.com/67cb8aa6e9184b6e44813189/6a17874a7db7a603d7eb3627_lfm2_5_8b_a1b_benchmarks.png)

\*AA-Omniscience Index (higher is better) rewards correct answers and penalizes hallucinations. Scores range from -100 to 100. See more results on Artificial Analysis.

## Highlights

- **On-device personal assistant.** Designed to power real-life applications, chaining tool calls, and following complex instructions on all devices.
- **Compressed performance.** Competitive with much larger dense and MoE models on instruction following and agentic tasks.
- **Unmatched throughput.** Fastest in its size class on both CPU and GPU inference, with day-one support for llama.cpp, MLX, vLLM, and SGLang.

## What changed since LFM2-8B-A1B

Compared to LFM2-8B-A1B, this new version expands the **context window from 32,768 to 128,000 tokens**. This allows the model to process longer documents and reason for longer. Its vocabulary size was also scaled up from 65,536 to 128,000 to **tokenize non-Latin scripts more efficiently**. We see particularly strong compression gains in Hindi, Thai, Vietnamese, Indonesian, and Arabic. The rest of the architecture follows the same combination of MoE, GQA, and gated short convolution blocks as LFM2-8B-A1B, as shown in the following figure.

![](https://cdn.prod.website-files.com/67cb8aa6e9184b6e44813189/68e51171bca5238ee2deb74b_LFM2%20architecture%20chart%20(6).png)

Unlike its predecessor, LFM2.5-8B-A1B is a **reasoning-only model**, producing an explicit chain of thought before its final answer. We adopted this strategy because MoE models generally run in compute-bound settings, where a smaller number of active parameters makes each reasoning token cheap. This provides a significant quality boost without compromising speed.

Thanks to reasoning and scaled-up training, this new version performs significantly better:

| **Benchmark** | **LFM2-8B-A1B** | **LFM2.5-8B-A1B** | **Δ** |
| --- | --- | --- | --- |
| AA-Omniscience Index | \-78.42 | \-24.70 | +53.62 |
| AA-Omniscience Accuracy | 7.33 | 8.67 | +1.34 |
| AA-Omniscience Non-Hallucination Rate | 7.46 | 63.47 | +56.01 |
| IFEval | 79.44 | 91.84 | +12.40 |
| IFBench | 26.00 | 56.47 | +30.47 |
| Multi-IF | 58.54 | 79.93 | +21.39 |
| MATH500 | 74.80 | 88.76 | +13.96 |
| AIME25 | 20.00 | 42.53 | +22.53 |
| BFCLv3 | 45.07 | 64.36 | +19.29 |
| BFCLv4 | 25.52 | 48.50 | +22.98 |
| Tau² Telecom | 13.60 | 88.07 | +74.47 |
| Tau² Retail | 7.02 | 39.82 | +32.80 |

## Training highlights

**Tokenizer expansion.** LFM2-8B-A1B was originally trained with a 65K BPE tokenizer optimized for our initial language coverage. To better support non-Latin scripts in LFM2.5, we doubled the vocabulary to 128K by extending the existing tokenizer in place rather than retraining the model from scratch.. We continued BPE merge training from the original merges on a multilingual corpus, which keeps most existing token IDs as identity mappings and makes every new token decompose deterministically into a sequence of original sub-tokens. We initialize the new embedding rows as the mean of their sub-token decompositions and copy the shared rows unchanged. We then recover quality through a brief two-stage adaptation: embedding-only training, followed by full-model continued pretraining.

The table below reports chars/token, roughly how much text each token carries: higher is better, and the new tokenizer is more efficient in all 16 languages

| **Tokenizer** | **Arabic (ar)** | **German (de)** | **English (en)** | **Spanish (es)** | **French (fr)** | **Hindi (hi)** | **Indonesian (id)** | **Italian (it)** | **Japanese (ja)** | **Korean (ko)** | **Polish (pl)** | **Portuguese (pt)** | **Russian (ru)** | **Thai (th)** | **Vietnamese (vi)** | **Chinese (zh)** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Old tokenizer | 2.239 | 3.641 | 4.063 | 3.442 | 3.618 | 0.961 | 2.731 | 3.251 | 1.836 | 1.652 | 2.672 | 3.194 | 2.703 | 0.671 | 1.519 | 1.475 |
| New tokenizer | 3.107 | 3.783 | 4.137 | 3.579 | 3.759 | 2.118 | 3.513 | 3.475 | 1.963 | 1.943 | 2.895 | 3.450 | 2.876 | 2.269 | 3.311 | 1.620 |
| Improvement | +38.8% | +3.9% | +1.8% | +4.0% | +3.9% | +120.4% | +28.6% | +6.9% | +6.9% | +17.6% | +8.3% | +8.0% | +6.4% | +238.2% | +117.9% | +9.8% |

**Context extension.** We first extended the context window to 32K through a 2T token midtraining phase focused on reasoning, math, tool-use, and longer documents. We then extended the context to 128K by increasing the RoPE base θ and running an additional 400B token midtraining stage focused on long-document and long-trajectory data.

**Doom loops.** We added a targeted preference optimization stage to reduce doom loops in long reasoning traces. This stage identifies tokens that tend to trigger looping behavior in specific contexts, then redistributes probability mass toward plausible alternatives, while leaving the rest of the next-token distribution largely intact. During RL, we also added a lightweight shaping reward that discourages excessive use of common loop-inducing restart words like “Wait…”. We'll share more details on the full pipeline, objective, and empirical results in a dedicated blog post.

**Hallucinations.** Because of their small number of parameters, edge models have a limited knowledge capacity, which leads to more hallucinations. To mitigate hallucinations, we added a targeted RL stage that uses an avg@k-based reward over a diverse knowledge dataset. The goal is to reinforce abstention on queries beyond reliable knowledge while preserving existing knowledge. This produces a sharper knowledge boundary and clearer expression of uncertainty.

## Benchmarks

We evaluated LFM2.5-8B-A1B across benchmarks covering knowledge, instruction following, math, and agentic workflows. The model is competitive with both dense alternatives with a similar total number of parameters and much larger MoEs.

<table><thead><tr><th rowspan="2">Model</th><th rowspan="2">Parameters</th><th colspan="3">AA-Omniscience</th><th colspan="3">Instruction following</th></tr><tr><th>Index</th><th>Accuracy</th><th>Non-Hallucination</th><th>IFEval</th><th>IFBench</th><th>Multi-IF</th></tr></thead><tbody><tr><td>LFM2.5-8B-A1B</td><td>8B/A1B</td><td>-24.70</td><td>8.67</td><td>63.47</td><td>91.84</td><td>56.47</td><td>79.93</td></tr><tr><td>Granite-4.0-H-Tiny</td><td>7B/A1B</td><td>-75.50</td><td>9.37</td><td>6.38</td><td>82.23</td><td>21.28</td><td>59.00</td></tr><tr><td>Qwen3.5-4B</td><td>4B</td><td>-51.53</td><td>17.20</td><td>16.99</td><td>87.80</td><td>50.38</td><td>67.43</td></tr><tr><td>Qwen3-30B-A3B-Thinking-2507</td><td>30.5B/3.3B</td><td>-51.31</td><td>18.80</td><td>13.87</td><td>90.82</td><td>51.11</td><td>79.04</td></tr><tr><td>Gemma-4-E2B-IT</td><td>5.1B</td><td>-72</td><td>7.00</td><td>15.05</td><td>82.93</td><td>33.53</td><td>69.70</td></tr><tr><td>Gemma-4-E4B-IT</td><td>8B</td><td>-50.67</td><td>8.10</td><td>36.06</td><td>87.74</td><td>39.48</td><td>77.58</td></tr><tr><td>Gemma-4-26B-A4B-IT</td><td>26B/4B</td><td>-62.07</td><td>14.37</td><td>10.75</td><td>91.40</td><td>47.25</td><td>82.06</td></tr><tr><td>gpt-oss-20b</td><td>21B/3.6B</td><td>-49.17</td><td>14.57</td><td>24.50</td><td>86.73</td><td>58.65</td><td>76.64</td></tr></tbody></table>

The avg@k-based reward enables LFM2.5-8B-A1B to achieve a significantly lower hallucination rate while maintaining reasonable accuracy. It also leads on instruction following benchmarks, matching bigger MoEs like Gemma 4-26B at a fraction of the active parameter count.

### Math and agentic workflows

<table><thead><tr><th rowspan="2">Model</th><th rowspan="2">Parameters</th><th colspan="3">Math</th><th colspan="4">Tool use</th></tr><tr><th>MATH500</th><th>AIME25</th><th>AIME26</th><th>BFCLv3</th><th>BFCLv4</th><th>Tau² Telecom</th><th>Tau² Retail</th></tr></thead><tbody><tr><td>LFM2.5-8B-A1B</td><td>8B/A1B</td><td>88.76</td><td>42.53</td><td>50.00</td><td>64.79</td><td>49.73</td><td>88.07</td><td>39.82</td></tr><tr><td>Granite-4.0-H-Tiny</td><td>7B/A1B</td><td>59.20</td><td>4.93</td><td>3.33</td><td>56.89</td><td>28.52</td><td>16.67</td><td>18.42</td></tr><tr><td>Qwen3.5-4B</td><td>4B</td><td>80.76</td><td>54.28</td><td>58.33</td><td>71.06</td><td>54.01</td><td>87.72</td><td>71.93</td></tr><tr><td>Qwen3-30B-A3B-Thinking-2507</td><td>30.5B/3.3B</td><td>86.48</td><td>71.67</td><td>66.67</td><td>73.39</td><td>50.53</td><td>21.93</td><td>56.14</td></tr><tr><td>Gemma-4-E2B-IT</td><td>5.1B</td><td>64.00</td><td>26</td><td>30</td><td>56.44</td><td>31.91</td><td>22.37</td><td>18.95</td></tr><tr><td>Gemma-4-E4B-IT</td><td>8B</td><td>65.00</td><td>34.33</td><td>40.67</td><td>57.31</td><td>33.92</td><td>26.75</td><td>42.11</td></tr><tr><td>Gemma-4-26B-A4B-IT</td><td>26B/4B</td><td>94.20</td><td>68.67</td><td>72.00</td><td>68.87</td><td>55.87</td><td>42.11</td><td>55.26</td></tr><tr><td>gpt-oss-20b</td><td>21B/3.6B</td><td>92.40</td><td>68.53</td><td>68.67</td><td>62.52</td><td>49.88</td><td>57.24</td><td>53.51</td></tr></tbody></table>

On agentic benchmarks, LFM2.5-8B-A1B is competitive with bigger models and particularly strong on Tau2-Telecom. As agentic harnesses are becoming the main way to consume models, LFM2.5-8B-A1B is a first step towards powering on-device, fully private agents.

## Sparse Inference, Everywhere

LFM2.5-8B-A1B ships with day-one support across the inference ecosystem:

- **LEAP** — Liquid's Edge AI Platform for iOS and Android deployment
- **llama.cpp** — GGUF checkpoints for efficient edge inference
- **MLX** — Optimized inference for Apple Silicon
- **vLLM** — GPU-accelerated serving for production throughput
- **SGLang** — GPU-accelerated serving for production throughput
- **ONNX** — Cross-platform inference across diverse accelerators

**CPU inference.** LFM2.5-8B-A1B ships with day-one llama.cpp support and runs on everyday consumer hardware.  

![](https://cdn.prod.website-files.com/67cb8aa6e9184b6e44813189/6a1788594d077d0205e0e94a_lfm2_5_8b_a1b_cpu_inference.png)

On both laptop-class chips, it is the fastest model we tested at reading in prompts and generating answers, decoding 253 tokens/s on an M5 Max and 146 on a Ryzen AI Max+ 395 while staying under 6 GB. It even holds ~30 tokens/s on a phone, so a capable assistant runs instantly and privately on your own device.

**GPU inference.** We support inference via vLLM and SGLang via active contributions to these codebases. We measure output throughput (total output tokens divided by wall time) on a single NVIDIA H100 SXM5 GPU using a sustained-load setting: at each concurrency level, we continuously maintain the target number of in-flight requests, replacing each completed request immediately.

![](https://cdn.prod.website-files.com/67cb8aa6e9184b6e44813189/6a1788bd6e860fb6f2bc1740_lfm2_5_8b_a1b_gpu_inference.png)

We benchmark each model with SGLang 0.5.12, 1,024 input tokens, up to 256 output tokens, in BF16, averaging 3 runs per concurrency level. LFM2.5-8B-A1B is the fastest model in its size class, reaching 18.5K output tokens per second at high concurrency, over 1.6B tokens per day on a single H100.

## Local Cowork: see it run

Our open-source desktop agent demo, [Localcowork](https://github.com/Liquid4All/cookbook/tree/main/examples/localcowork), now runs on LFM2.5-8B-A1B. The setup is the same one we used for [LFM2-24B-A2B demo](https://www.liquid.ai/blog/no-cloud-tool-calling-agents-consumer-hardware-lfm2-24b-a2b) in March: a single laptop, 67 tools across 13 MCP servers, no cloud, no API keys, no data leaving the machine. Tool selection is faster and noticeably more reliable across the same tool menu.

<iframe src="https://cdn.embedly.com/widgets/media.html?src=https%3A%2F%2Fwww.loom.com%2Fembed%2Fbc3faf8befb643baae3434cde098e95e&amp;display_name=Loom&amp;url=https%3A%2F%2Fwww.loom.com%2Fshare%2Fbc3faf8befb643baae3434cde098e95e&amp;image=https%3A%2F%2Fcdn.loom.com%2Fsessions%2Fthumbnails%2Fbc3faf8befb643baae3434cde098e95e-54f5e0d41866127b.gif&amp;type=text%2Fhtml&amp;schema=loom" title="LFM2.5-8b-A1B - LocalCowork" frameborder="0" allowfullscreen="true"></iframe>

The point of the demo is not the individual tools. It is that the **tool-dispatch loop feels interactive** on consumer hardware: ask, propose, confirm, run, repeat, all in well under a second per dispatch, with full audit trails and your data never leaving the device.

## Get Started

With LFM2.5, we're delivering on our vision of AI that runs anywhere. These models are:

- **Open-weight** — Download, fine-tune, and deploy without restrictions
- **Fast from day one** — Native support for llama.cpp, MLX, vLLM, SGLang across Apple, AMD, Intel, Qualcomm, and Nvidia hardware
- **A complete family** — From base models for customization to specialized audio and vision variants, one architecture covers diverse use cases

The on-device agentic future starts here. We can't wait to see what you build.

### Citation

Please cite this article as:

> Liquid AI, “LFM2.5-8B-A1B: Personal Assistant On Your Laptop,” *Liquid AI Blog*, May 2026.

Or use the BibTeX citation:

```
@article{liquidAI20268BA1B,
  author  = {Liquid AI},
  title   = {LFM2.5-8B-A1B: Personal Assistant On Your Laptop},
  journal = {Liquid AI Blog},
  year    = {2026},
  note    = {https://www.liquid.ai/blog/lfm2-5-8b-a1b},
}
```

 <video controls=""><source src="https://cdn.prod.website-files.com/67cb8aa6e9184b6e44813162%2F67feb90984a598097c1fb2e2_Liquid%20AI%20-%20Bg%20-%20Primary%20%28min%29-transcode.mp4"> <source src="https://cdn.prod.website-files.com/67cb8aa6e9184b6e44813162%2F67feb90984a598097c1fb2e2_Liquid%20AI%20-%20Bg%20-%20Primary%20%28min%29-transcode.webm"></video>