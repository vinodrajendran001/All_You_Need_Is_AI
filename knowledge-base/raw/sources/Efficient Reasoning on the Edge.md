---
title: "Efficient Reasoning on the Edge"
source: "https://qualcomm-ai-research.github.io/llm-reasoning-on-edge/"
author:
  - "[[Yelysei Bondarenko]]"
  - "[[Thomas Hehn]]"
  - "[[Rob Hesselink]]"
  - "[[Romain Lepert]]"
  - "[[Fabio Valerio Massoli]]"
  - "[[Evgeny Mironov]]"
  - "[[Leyla Mirvakhabova]]"
  - "[[Tribhuvanesh Orekondy]]"
  - "[[Spyridon Stasis]]"
  - "[[Andrey Kuzmin]]"
  - "[[Anna Kuzina]]"
  - "[[Markus Nagel]]"
  - "[[Corrado Rainone]]"
  - "[[Ork de Rooij]]"
  - "[[Paul N Whatmough]]"
  - "[[Arash Behboodi]]"
  - "[[Babak Ehteshami Bejnordi]]"
published: 2024-01-01
created: 2026-06-04
description: "Enabling efficient LLM reasoning on mobile devices using LoRA adapters, budget forcing, and parallel verification."
tags:
  - "clippings"
---
## Budget Forcing

![Budget Forcing](https://qualcomm-ai-research.github.io/llm-reasoning-on-edge/static/images/budget_forcing.png)  

The deployment of advanced reasoning capabilities (Inference-Time Scaling) on resource-constrained devices, particularly smartphones, is currently hindered by substantial latency overheads associated with generating full Chain-of-Thought (CoT) traces. Due to the intrinsic verbosity of standard Large Language Models (LLMs), the time required to produce a final answer can extend to several minutes, thereby creating a computational bottleneck that undermines the feasibility of real-time user interaction. Within this context, **"budget forcing"** — a **Reinforcement Learning (RL) based fine-tuning methodology** — emerges as a fundamental requirement for practical on-device deployment. By training models to generate substantially more concise responses, budget forcing alleviates these latency constraints, and thereby enables the effective application of Inference-Time Scaling on edge devices.

To instantiate this approach, we implemented a **specialized RL training pipeline** governed by a **dual-objective reward function**. The primary objective is to **minimize the generation budget** — quantified as the total number of tokens produced — while simultaneously preserving, or potentially improving upon, the accuracy of the base model by maintaining its capacity to sample correct solutions. This training regime incentivizes the model to discover and follow the **shortest viable reasoning trajectory** from the input prompt to the correct final answer. The resulting model is capable of producing compressed CoT traces that remove superfluous content while preserving the essential deductive steps required for solving complex problems.

## Switcher

![Switcher](https://qualcomm-ai-research.github.io/llm-reasoning-on-edge/static/images/switcher.png)  

Beyond making individual reasoning traces efficient, to avoid paying the cost of long reasoning traces on every request, we attach a **lightweight switcher head** that only enables the LoRA reasoning adapters when the prompt actually requires reasoning. The switcher sits on top of the final transformer layer, takes the mean-pooled hidden states over all prompt tokens as input, and outputs a binary decision between chat mode and reasoning mode. In chat mode, the model responds using only the frozen base weights, while in reasoning mode the LoRA adapters are activated on top of the same base model.

To let both modes share a single KV cache, we always encode the prompt with the base model alone and train the reasoning LoRA adapters to decode tokens conditioned on KV states produced without LoRA. In practice, this lets us **reuse the same KV cache** when switching between chat and reasoning, without re-encoding the prompt with LoRA applied. As a result, the switcher design **keeps everyday chat fast and inexpensive**, while only turning on the **budget-forced LoRA reasoning traces for genuinely complex, multi-step queries**.

## Parallel Reasoning and Verification

![Parallel decoding](https://qualcomm-ai-research.github.io/llm-reasoning-on-edge/static/images/parallel_decoding.png)  

While budget forcing reduces the cost of sequential generation, parallel compute on modern mobile processors offers a complementary path to improve reasoning performance. Instead of reducing sequence length, parallel reasoning aims to increase accuracy while maintaining a similar latency budget. Our parallel reasoning features:

- **Increased compute utilization** during the memory-bound generation process by exploring multiple reasoning paths independently and concurrently.
- **Reduced memory and compute overhead** through joint a Generation-Verification architecture that combines a base generator model with a verification head which **minimizes the verifier's memory footprint**, **avoids model switching cost** (such as loading parameters to DRAM) and also **utilizes the existing KV cache**.
- **Improved accuracy by parallel verification**, as each reasoning chain is independently verified for correctness and assigned a score, allowing for rapid validation of multiple solutions.
A combination of generation and verification enables us to prototype recent parallel strategies, such as majority voting (self-consistency), Best-of-N, and Weighted Majority. Overall, we find parallel decoding on-device enables **improved accuracy** with **minimal additional latency**.

## BibTeX

```
@article{bondarenko2026efficient,
  title        = {Efficient Reasoning on the Edge},
  author       = {Bondarenko, Yelysei and Hehn, Thomas and Hesselink, Rob and
                  Lepert, Romain and Massoli, Fabio Valerio and Mironov, Evgeny and
                  Mirvakhabova, Leyla and Orekondy, Tribhuvanesh and Stasis, Spyridon and
                  Kuzmin, Andrey and Kuzina, Anna and Nagel, Markus and Nayak, Ankita and
                  Rainone, Corrado and de Rooij, Ork and Whatmough, Paul N. and
                  Behboodi, Arash and Ehteshami Bejnordi, Babak},
  journal      = {arXiv preprint arXiv:2603.16867},
  year         = {2026},
  archivePrefix= {arXiv},
  eprint       = {2603.16867},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2603.16867},
  url          = {https://arxiv.org/abs/2603.16867}
}
```