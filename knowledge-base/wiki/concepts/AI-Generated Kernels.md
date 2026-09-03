---
type: concept
created: 2026-08-26
updated: 2026-09-03
tags:
  - concept
  - kernels
  - gpu
  - evaluation
  - self-improvement
source_ids:
  - src-2026-08-23-wafer-ai-performance-engineering-resources
  - src-2026-08-23-wafer-ai-perf-contributing-source-policy
  - src-2026-08-29-baseten-agentic-kernels-production
status: active
---

# AI-Generated Kernels

## Definition

**AI-generated kernels** are GPU kernels written by language models rather than by human performance engineers, typically by translating a high-level operator definition into a faster hand-tuned-equivalent implementation. The task is attractive because it has an unusually clean reward signal: a kernel is either numerically correct or not, and it is either faster than the baseline or not.

## Why it matters

Kernel generation is the sharpest available test of whether models can do genuine performance engineering rather than pattern-complete familiar code. It is also one of the few agentic domains where **the verifier is cheap and objective** — which is exactly the condition [[Loop Engineering]] and [[Recursive Self-Improvement]] identify as the bottleneck everywhere else. If self-improvement works anywhere, it should work here first.

That makes the honesty of the evaluation the whole game, and it is where this topic has repeatedly gone wrong.

## The benchmark correction

[[Wafer - AI Performance Engineering Resources]] files this entire area under a dated `Frontier` section rather than the core path, and the reason is visible in the benchmark lineage itself:

| Benchmark | Contribution |
| --- | --- |
| KernelBench | The original benchmark for converting PyTorch operators into faster GPU kernels |
| KernelBench-Verified | Stronger correctness tests and baseline parity |
| SOL-ExecBench | Correctness and performance measured against a hardware speed-of-light model |

The progression is a correction, not just refinement. Weak correctness tests let a generated kernel pass while computing the wrong thing, and weak baselines let it claim a speedup over an unoptimized reference that no practitioner would have used. Measuring against a **speed-of-light model** — what the hardware could theoretically achieve for that data movement — closes the remaining gap, because it makes "faster than the baseline" insufficient and asks how much of the achievable performance was actually captured.

The source's standing caution is explicit: individual AI kernel agents that have not been rerun on a **hardened evaluator** do not qualify for the core list. Reported wins on the original benchmark are not, on their own, evidence.

## Why this generalizes

This is the vault's cleanest concrete instance of a pattern argued abstractly elsewhere. [[Benchmark Optimization]] shows systems learning the reference rather than the task in speech recognition; [[Serving Benchmarks and Goodput]] records that a performance number without a correctness method is not a result. Kernel generation shows the same failure in the domain where objective verification was supposed to be easy — which suggests the problem is not that some domains lack good verifiers, but that **verifiers are themselves engineering artifacts that must be hardened against the optimizer pointed at them.**

For agent design the implication is direct: an evaluation harness is part of the attack surface of a self-improving loop, not a neutral observer of it. See [[Agent Workflow Maturity]] on separating producer from verifier.

## What the benchmark correction actually consists of

[[Baseten - Agentic Kernels in Production]] takes the correction recorded above and specifies it. Four reasons
a KernelBench win does not become a production win:

1. **The best configuration depends on the workload.** Tile shapes, warp-specialization strategy and CTA
   configuration respond differently to tensor shape, batch size and sequence length — most visibly for MoE
   and attention kernels. A kernel that wins on a general benchmark can lose on a specific deployment.
2. **A faster microbenchmark is not a faster model.** CUDA graph capture and multi-stream execution can erase
   a kernel-level gain or turn it into a regression.
3. **Per-kernel optimization misses the larger win.** End-to-end traces usually show only a small subset of
   kernels have headroom; the cheaper gains come from restructuring around them — fusing, eliminating
   redundant work, removing pipeline bubbles.
4. **Integration is nontrivial.** A serving engine has interconnected execution paths; a kernel must be wired
   into the right one, replace existing computation cleanly, and stay compatible with the runtime.

Three of the four are about **integration and workload specificity rather than about writing better CUDA**,
which is the substance of the benchmark gap.

## A production result, and the variable that predicts its size

The same framework — a model-level layer that profiles and restructures, plus a per-kernel layer exploring
implementations in parallel — reports **42.3% end-to-end latency reduction on Qwen-Image** (median per-step
denoising **245.6 ms → 141.8 ms**), **15.2% on FLUX.2**, and about **5.5% more tok/s on MiniMax M3**. The
optimizations were, per the authors, identified, proposed and implemented entirely by the framework.

The gap between those numbers is the finding. Applied to LLMs the same system yields ~5.5% because LLM
*"kernel implementations are considerably more mature and leave less headroom for improvement."* **Agentic
optimization pays inversely to how much human optimization a domain has already absorbed** — a far better
predictor of where to point these systems than any benchmark score, and a caution that a large percentage win
is mostly a fact about the baseline. Note also that several wins read as recovered waste rather than novel
optimization: a Python contiguity guard silently forcing a slow path, and constant FP8 weight scales being
repacked every step.

The loop also retains a knowledge base of **both successes and failures, with root causes and dead ends
recorded** — see [[Recursive Self-Improvement]]. All figures are vendor self-reported against an
uncharacterised prior baseline.

## Open questions

- Do generated kernels climb the full optimization ladder in [[GPU Kernel Optimization]], or do they mostly capture its first rungs — where the transformations are well documented and the search space is small?
- Does success transfer across hardware generations, or must a model be re-taught for each new architecture's asynchrony and tensor-memory features?
- Speed-of-light comparison needs a credible model of achievable performance for each operator. Who maintains that model, and what happens when it is wrong?
- If kernel generation does work, does the advantage accrue to whoever owns the hardware documentation and profiling telemetry rather than to whoever owns the model?
- How should a vault or a team cite a generated kernel's performance claim under an evidence standard that requires a reproducible baseline?

## Related pages

- [[Wafer - AI Performance Engineering Resources]]
- [[GPU Kernel Optimization]]
- [[Benchmark Optimization]]
- [[Serving Benchmarks and Goodput]]
- [[Recursive Self-Improvement]]
- [[Loop Engineering]]
- [[Agent Workflow Maturity]]
- [[GPU Execution Model]]
- [[Baseten - Agentic Kernels in Production]]
- [[Baseten]]
- [[Inference Efficiency Frontier]]
