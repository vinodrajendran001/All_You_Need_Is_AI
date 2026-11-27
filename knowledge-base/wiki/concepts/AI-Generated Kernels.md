---
type: concept
created: 2026-08-26
updated: 2026-11-27
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
  - src-2026-11-11-cam-pedersen-derive-kernels
  - src-2026-11-20-ankit-gupta-vibecoding-inference-chip
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

## Derivation as the other route to trustworthy kernels

[[Cam Pedersen - Don't Write Kernels, Derive Them]] positions compiler derivation against model-written
kernels. It cites KernelBench-Verified as showing "frontier models reward-hacking benchmarks by
hard-coding test values" (secondhand; the benchmark paper is not in the vault) and argues that "a
derived kernel is checked by construction against an f64 interpreter of the same graph". Its
`tang-verify` harness pre-fills every kernel's outputs with **NaN** so unwritten memory cannot pass as a
plausible zero, and names the failing kernel by provenance; it was built after four structural bugs in a
hand-written engine "slipped past every unit test". The core rewrites are proved in Lean over the reals,
but floating point is not modelled, and the check still caught one placement with error **7.0** that the
authors cannot yet explain.

Its autotuner also writes every (graph, chip, schedule, time) result to a cache that "can train a cost
model" — the same success-and-failure memory the Baseten loop keeps, but over schedules rather than
code. Whether search over a verified algebra or agentic code generation climbs further is untested.

## A hardware loop where bit-exactness is the verifier

[[Ankit Gupta - Vibecoding an Inference Chip]] extends agent-written low-level code from GPU kernels to FPGA
hardware. A coding agent wrote C++ and some Verilog for an author who says he has "never written
Verilog". It ran hundreds of experiments for about $10,000 in tokens and took a bit-exact LLM decoder
from **6.43** to **213.13** tokens per second, **33.13×**, in 14 measured steps of 1.03× to 1.74× each.

The verifier is the kind this page argues such a loop needs. Every step had to match a pinned
reference bit for bit, which is much harder to game than a tolerance check, and it led the agent to
reject every precision shortcut in the human advice. The contract was not enough on its own. A soak
test found random faults at one clock, so the final image runs a step slower. The agent's
retrospective also ties 38 lost hours to two hangs that only RTL simulation would have caught, after
it had dropped long simulations for a faster loop. Correctness here needed both the output check and a
stability check under sustained load.

The size of the gain fits the inverse-headroom rule above, with the same caution. Baseten's ~5.5% on
mature LLM kernels and this 33× sit at opposite ends, but the FPGA figure is measured from the loop's
own first correct image, in a domain with little prior tuning for this model, not against an optimized
human design. No ablation separates the agent's work from the author's hints, and the alternatives it
was compared with were not optimized by the same loop. The author's conclusion is that "the humans are
still useful at defining how to iterate fast and what correctness looks like, and the agents are great
to manage the exploration."

## Open questions

- Do generated kernels climb the full optimization ladder in [[GPU Kernel Optimization]], or do they mostly capture its first rungs — where the transformations are well documented and the search space is small?
- Does success transfer across hardware generations, or must a model be re-taught for each new architecture's asynchrony and tensor-memory features?
- Speed-of-light comparison needs a credible model of achievable performance for each operator. Who maintains that model, and what happens when it is wrong?
- If kernel generation does work, does the advantage accrue to whoever owns the hardware documentation and profiling telemetry rather than to whoever owns the model?
- How should a vault or a team cite a generated kernel's performance claim under an evidence standard that requires a reproducible baseline?
- Does agentic optimization carry over to hardware design generally, or only where a bit-exact
  reference makes verification cheap? The one FPGA account in the vault had such a reference.

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
- [[Cam Pedersen - Don't Write Kernels, Derive Them]]
- [[Ankit Gupta - Vibecoding an Inference Chip]]
- [[AI Accelerator Architecture]]
