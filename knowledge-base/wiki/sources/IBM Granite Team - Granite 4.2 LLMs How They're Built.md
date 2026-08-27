---
type: source-summary
created: 2026-08-27
updated: 2026-08-27
source_id: src-2026-08-25-ibm-granite-4-2-how-they-are-built
source_title: "Granite 4.2 LLMs: How They're Built"
source_author: IBM Granite Team
source_url: https://huggingface.co/blog/ibm-granite/granite-4-2
tags:
  - source/summary
  - reinforcement-learning
  - post-training
  - ai-agents
  - open-models
  - reasoning
source_ids:
  - src-2026-08-25-ibm-granite-4-2-how-they-are-built
status: active
---

# IBM Granite Team - Granite 4.2 LLMs How They're Built

## Summary

A build report for Granite 4.2, IBM's first family of dense decoder-only *reasoning* models —
3B, 8B, and 30B, all Apache 2.0. It walks the full pipeline: five-phase pre-training from scratch
on ~15T tokens, supervised fine-tuning on chain-of-thought and agentic-trajectory data, then a
multi-stage reinforcement-learning chain that ends with agentic RL in real sandboxed environments.

What makes this source unusually valuable to this vault is not the model. It is that **the recipe
is published with its numbers**. This vault already carries substantial material on agentic RL
from surveys ([[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]]), framework
write-ups ([[RadixArk - Miles v0.1 Production-Level Post-Training]]), and research systems
([[rLLM - Continual Learning via Real-Time RL for Agents]]). All of them describe what teams *could*
do. Granite 4.2 is the first source here that states what one team actually *did*, stage by stage,
with prompts per step, generations per prompt, KL coefficients, learning rates, rollout turns, and
sequence lengths for a shipped open-weight family. It converts a body of options into one worked
example.

## Key claims

### Architecture

- Decoder-only dense transformer. GQA with 40 attention heads and 8 KV heads, RoPE at
  θ = 10,000,000, SwiGLU MLP, RMSNorm (ε = 1e-5), untied input/output embeddings, bfloat16.
- The three sizes differ in width and depth, not design: 3B is 40 layers at embedding 2560;
  8B is 40 layers at 4096; 30B is 64 layers at 4096 with an MLP hidden size of 32768.
- The architecture table lists a sequence length of 131,072 for all three sizes.

### Pre-training

- ~15T tokens, five phases. Phases 1–2 foundational, 3–4 mid-training with progressively higher
  data quality ("annealing"), phase 5 long-context extension. Each phase has its own data mixture
  and learning-rate schedule, shifting from broad web data toward curated sources.
- The post states phase 5 extends the context window to **512K tokens**, which does not match the
  131,072 sequence length in the architecture table. See open questions.

### Supervised fine-tuning

- ~7.2M samples, roughly 100B tokens of which ~65B are trainable. The mixture is **31.6% agentic /
  68.4% non-agentic**.
- The agentic corpus is dominated by software engineering (69%), then tool calling (12.1%),
  terminal use (8.0%), math (3.5%), search (0.8%), and action (0.2%). Trajectories were generated
  across many harnesses — OpenHands, OpenCode, Terminus-2, SWE-agent, OpenResearcher, MiniSWE,
  OpenSeeker, EnvScaler, Gemini CLI, Hermes, Codex, Goose — deliberately spanning agent/harness
  combinations rather than standardizing on one.
- Quality control runs in stages: normalize every source into OpenAI Chat format so conversation
  and tool structure is uniform; score with GPT-OSS-120B and Gemma 4 as LLM judges; drop
  low-scoring samples, hallucinated content, invalid tool interactions, and **tool calls to
  functions not present in the sample's own tool list**; apply dataset-specific heuristics; then
  deduplicate locally and globally on SHA-256 hashes over the combined `tools` and `messages`
  fields.
- Training ran on 32–128 nodes of 4× Grace/GB200, packed to 131,072-token sequences, global batch
  128, LR 1.0e-5 constant after a 2.5% warm-up, ~2 epochs, TP=2 / PP=1 / CP=4 or 2.
- The 30B model gets a **second SFT phase** specialized on agentic coding, upsampling agentic/SWE/
  coding data while retaining ~16% replay from the original mixture, for ~1 epoch at LR 3.0e-6.

### The multi-stage RL pipeline

- The pipeline is a *chain of separate GRPO runs*, not one RL pass:
  `SFT → RLVR → skill boosters → SWE agent → Terminal → Search → RLHF`. Each stage targets one
  capability, has its own reward signal, exports to Hugging Face format when it finishes, and
  becomes the base checkpoint for the next.
- **Asynchronous GRPO throughout.** Generation workers keep sampling into a shared buffer while
  the trainer pulls full batches and streams updated parameters back without pausing them. A
  weight refresh may land mid-rollout, leaving one trajectory stitched from two adjacent policy
  versions. IBM allows this rather than paying to prevent it — workers reuse their existing KV
  cache instead of rebuilding it after each refresh. The single guardrail is a limit keeping
  workers no more than **one update behind** the trainer; residual mismatch is absorbed by
  **truncated importance sampling**, which clamps the train-vs-generation log-probability ratio.
- Advantages are group-relative with a **leave-one-out baseline**: each response is scored against
  the mean reward of the *other* samples for the same prompt, removing the need for a value
  network.
- RLVR, the first and longest stage, pairs **256 prompts × 16 responses = a 4,096-example batch**
  consumed in one optimizer step.
- Shared across all stages: GRPO with no value network, NeMo-RL (Megatron-Core + vLLM) with
  NeMo-Gym environments, ratio clip 0.2 / 0.28, micro-batch 1, tensor-parallel 2–4, no pipeline or
  context parallelism.

### The 30B stage table

| Stage | Prompts/step | Gens/prompt | Max seq len | Rollout turns | KL | LR |
| --- | --- | --- | --- | --- | --- | --- |
| RLVR (×3) | 256 | 16 | 64K | 1 | 0 | 5e-7 |
| IF booster | 256 | 16 | 64K | 1 | 0 | 5e-7 |
| Code booster | 64 | 16 | 64K | 1 | 0.05 | 5e-7 |
| SWE 1 | 64 | 16 | 128K | 1 | 0.01 | 5e-7 |
| SWE 2 | 32 | 16 | 128K | 128 | 0 | 5e-7 |
| Terminal | 8 | 32 | 64K | 64 | 0.01 | 1e-6 |
| Search | 32 | 16 | 128K | 64 | 0.01 | 5e-7 |
| RLHF | 128 | 16 | 48K | 1 | 0.05 | 5e-7 |

- **The KL schedule follows the reward type.** Explore freely where the reward is objective and
  verifiable (RLVR and SWE 2 run at KL 0); stay close to the reference where the objective is
  preference, safety, or a narrow skill graft (RLHF and the code booster use KL 0.05). This is the
  most transferable single rule in the source.
- Three reward types are used, sometimes within one stage: **verifiable** (exact match, unit tests,
  format and rule checkers), **reward model / LLM judge** (open-ended quality, preference, safety),
  and **agentic outcome** (did the task actually get solved). Verifiable rewards are objective and
  hard to game, so the pipeline front-loads them; agentic-outcome rewards are the sparsest, often
  a single bit at the end of a long trajectory.

### Stages in detail

- **RLVR** blends math with boxed-answer checking plus formal proving in Lean, competitive coding
  checked against hidden tests in a sandbox, STEM/graduate MCQA, instruction following, single-step
  tool calling, reasoning puzzles, and **abstention** — knowing when to refuse. Each task type
  carries its own verifier, so reward is grounded per example. Runs ×2 on 3B and 8B, ×3 on 30B.
- **Skill boosters** are short focused runs on instruction following and competitive coding, with a
  light KL penalty to nudge one skill without moving general behavior.
- **Agentic RL (8B and 30B only)** runs SWE → Terminal → Search. The SWE agent works real
  repositories in per-repo container sandboxes through the OpenHands harness, rewarded on hidden
  tests. The Terminal agent runs multi-step tasks in a live shell via Harbor / Terminus-2, with
  rollouts spanning up to 64 environment turns — the one stage that drives its multi-turn loop at
  the GRPO level. The Search agent answers multi-hop questions with live web search, judged by an
  LLM because correctness is open-ended.
- **RLHF** closes every model: a generative reward model for preference plus a safety reward for
  jailbreak resistance and appropriate refusals, at the pipeline's highest KL. It also applies a
  **reasoning-length penalty to undo verbosity the earlier stages induced**.

### Capability is gated by size

3B takes a shortened ladder — foundational RL and alignment, no agentic block at all. 8B and 30B
run the full chain. The method and infrastructure are identical; what changes is how far up the
ladder each model goes.

### Infrastructure

- **NeMo-RL** on the training side: Megatron-Core as backend, vLLM for rollout generation,
  Megatron-Bridge converting weights between Megatron and Hugging Face formats so each stage can
  export a clean checkpoint for the next.
- **NeMo-Gym** on the rollout side exposes every environment as a set of **Resources** — verifiers,
  tools, sandboxes, reward models — behind one uniform interface. The source is explicit about why
  this matters: "a booster's rule-based checker and a full SWE sandbox present the same interface
  to GRPO." That uniformity is what makes the staged curriculum practical to run at all.
- The training/rollout split is also what makes asynchronous training physically possible:
  generation and policy updates live on separate GPU pools, so the expensive generation fleet —
  including live agentic environments — never idles through optimizer steps.
- Hardware: an NVIDIA GB200 NVL72 cluster hosted by CoreWeave, with a 72-GPU NVLink domain for
  intra-rack traffic and a non-blocking Fat-Tree NDR 400 Gb/s InfiniBand fabric between racks.
- Software is packaged as `.sqsh` container images pinning CUDA targets, aarch64 wheels, and GPU
  binaries; SFT builds on NGC PyTorch (Ubuntu 22.04, CUDA 12.8, Python 3.12) and RL runs in its own
  NeMo-RL container.

### Quantization

- **FP8**: dynamic per-channel weights and per-token activations, no calibration.
- **NVFP4 and MXFP4**: GPTQ calibrated on 2K samples drawn from the SFT dataset, max context 2K
  during calibration.
- **GGUF** via llama.cpp across the Q2–Q8 range for reduced-memory deployment.

### Results

Reported across agentic coding, general agentic/tool use, reasoning, chat, and long context.
Selected 8B → 30B figures: SWE-Bench Verified 47.67 → 57.00, SWE-Bench Pro 19.11 → 33.29,
Terminal-Bench 2.1 20.56 → 29.24, τ³-bench 58.06 → 62.00, AIME25 86.67 → 89.17, GPQA 64.14 → 66.41,
MMLU-Pro 74.04 → 77.60, RULER 128K 71.41 → 81.38. The 3B is not reported on the SWE or terminal
benchmarks at all, consistent with it never receiving the agentic block.

Twelve supported languages: English, German, Spanish, French, Japanese, Portuguese, Arabic, Czech,
Italian, Korean, Dutch, Chinese.

## Why it matters

Three things here are more durable than the model itself.

**The staged chain is a design pattern, not an implementation detail.** Treating post-training as a
sequence of independent RL runs — each with one objective, one reward, and a clean checkpoint
export — makes an otherwise intractable multi-objective problem debuggable. A stage that fails can
be re-run without discarding the ones before it.

**The KL-follows-reward-type rule generalizes past Granite.** It ties a hyperparameter that is
usually tuned by feel to a property of the objective: if you can verify the answer, let the model
roam; if you are optimizing taste or safety, hold it near the reference.

**Interface uniformity is what makes curricula affordable.** The vault has already recorded three
independent groups converging on modular environment interfaces. Granite is the fourth, and states
the payoff most directly: when a regex checker and a containerized repository look identical to the
optimizer, adding a stage costs almost nothing.

## Tensions / open questions

- **The context-length claim is internally inconsistent.** The post says phase 5 extends the
  context window to 512K tokens, but the architecture table gives a sequence length of 131,072 for
  all three sizes, and the long-context results stop at RULER 128K. The most likely reading is that
  512K was reached during a training phase while the released configuration is capped at 128K, but
  the source does not say so.
- No ablations are given. The staged chain, the leave-one-out baseline, the KL schedule, and the
  bounded-staleness async loop are all presented as *what was done*, never as *what was tested
  against an alternative*. None of the design choices is shown to be load-bearing.
- Allowing a single trajectory to be stitched from two policy versions is presented as an
  acceptable cost of keeping the KV cache warm. The source does not quantify how often this occurs
  or what it costs in sample quality.
- This is a first-party build report from the team that shipped the model, published on its own
  model card. The benchmark numbers are self-reported and unaudited, and no comparison against
  other model families is offered.
- The 3B model's exclusion from agentic RL is stated as a scope decision, not a capability finding.
  Whether 3B *cannot* learn agentic behavior or simply was not given the chance is left open.

## Affected pages

- [[Agentic Reinforcement Learning]]
- [[Coding Agent Harness]]
- [[Distributed Training Parallelism]]
- [[Group Relative Policy Optimization]]
- [[Hugging Face]]
- [[IBM]]
- [[LLM Training Pipeline]]
- [[Model Quantization and Efficiency]]
- [[NVIDIA]]
- [[Open Model Ecosystems]]
- [[Reasoning Compression]]
- [[Reward Design for RL]]
- [[Small Language Models]]
- [[Staged Reinforcement Learning Curriculum]]
- [[Test-Time Scaling]]
- [[Tool Use and Function Calling]]

## Raw capture

- [[2026-08-25 IBM Granite Team - Granite 4.2 LLMs - How They're Built]]

## Related pages

- [[Staged Reinforcement Learning Curriculum]]
- [[IBM]]
- [[Agentic Reinforcement Learning]]
- [[Group Relative Policy Optimization]]
- [[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]]
- [[RadixArk - Miles v0.1 Production-Level Post-Training]]
- [[Open Model Ecosystems]]
- [[AI Knowledge Base Overview]]
