---
type: source-summary
created: 2026-09-03
updated: 2026-09-03
source_id: src-2026-08-29-baseten-agentic-kernels-production
source_title: "Agentic kernels in production"
source_author: Brian Li, Faraz Shahsavan, Pankaj Gupta (Baseten)
source_url: https://www.baseten.co/blog/agentic-kernels-in-production/
tags:
  - source/summary
  - topic/kernels
  - topic/inference
  - topic/self-improvement
source_ids:
  - src-2026-08-29-baseten-agentic-kernels-production
status: active
---

# Baseten - Agentic Kernels in Production

## Summary

[[Baseten]] describes an agentic kernel-development framework that profiles a real serving workload, proposes
optimizations, generates kernels, validates them, and ships them into production. Reported end-to-end gains:
**42.3% latency reduction on Qwen-Image**, **15.2% on FLUX.2**, and **5.5% more tok/s on MiniMax M3**. On
Qwen-Image FP8, median per-step denoising time falls from **245.6 ms to 141.8 ms**.

The framing that makes this more than a results post is its opening argument: **winning a kernel benchmark and
shipping a production optimization are different problems**, and the post enumerates why. The optimizations
below were, per the authors, *"identified, proposed, and implemented entirely by our agentic framework."*

## Key claims

- **Four reasons benchmark wins do not transfer to production:**
  1. **The best kernel configuration depends on the workload.** Tile shapes, warp-specialization strategy and
     CTA configuration respond differently to tensor shape, batch size and sequence length — most visibly for
     MoE and attention kernels.
  2. **A faster microbenchmark is not a faster model.** CUDA graph capture and multi-stream execution can
     erase a kernel-level gain or turn it into a regression.
  3. **Per-kernel optimization misses the bigger win.** End-to-end traces usually show only a small subset of
     kernels have headroom; the cheaper gains come from *restructuring* — fusing, removing redundant work,
     eliminating pipeline bubbles.
  4. **Integration is nontrivial.** A serving engine has interconnected execution paths; a kernel must be
     wired into the right one, cleanly replace existing computation, and stay compatible with the runtime.
- **Two-layer stack.** A **model-level** layer profiles the whole workload and proposes structural changes;
  a **per-kernel** layer explores several implementations in parallel and iterates on the strongest. The first
  layer exists to widen the search space beyond one-for-one kernel replacement.
- **The loop accumulates memory, including of failures.** Kernels passing correctness and end-to-end checks
  are retained as reusable candidates; lessons from **both successful and failed attempts** enter an evolving
  knowledge base alongside workload constraints and integration findings — successes as reusable patterns,
  **failures as caveats and root causes**, with dead ends explicitly recorded.
- **The individual wins are structural, not clever.** Pre-packing FP8 scales at load time (**7.3% Qwen /
  6.1% FLUX**, outputs **bit-identical**); fusing QKV projections into one GEMM with a Triton epilogue;
  fusing normalization with quantization to kill a BF16 round trip (**4.3% / 0.7%**); **bias absorption**,
  after the standalone biases were found to be ~**11% of Qwen's FP8 step time** (**5.2%**); a **CFG modulation
  cache** exploiting that the modulation branches depend only on the timestep, not the prompt, so the two
  classifier-free-guidance passes can share them (**2.1% FP8 / 3.1% NVFP4**).
- On FLUX.2, a fused QK-normalization + RoPE kernel gave a **2× kernel speedup** and eliminated **48 of 60
  cache concatenations per step**; a Python contiguity guard had been silently forcing the slow path.
- **Final per-kernel passes** added **7.6% FP8 / 13.4% NVFP4** on Qwen-Image and **1.9% / 2.8%** on FLUX.2.
- **Maturity determines headroom, and the authors say so.** Expanding to LLMs yields only ~**5.5%** because
  *"kernel implementations are considerably more mature and leave less headroom for improvement."*
- **Stated direction:** per-deployment kernels specialised to actual model, hardware, tensor shapes and
  traffic — each deployment continuously evolving toward its own workload rather than running generic kernels.

## Why it matters

This is the vault's first **end-to-end production** instance of AI-generated kernels, and it lands directly on
the correction already recorded on [[AI-Generated Kernels]]: that KernelBench-style results overstate real
capability. The post agrees and then specifies the mechanism in four parts, which upgrades that page from a
caveat into an account of *what the missing work actually is* — and notably, three of the four reasons are
about **integration and workload specificity**, not about writing better CUDA.

The **maturity-headroom relationship** is the most transferable finding. 42.3% on diffusion versus 5.5% on
LLMs, from the same framework, is a clean natural experiment: the agent's value is inversely proportional to
how much human optimization effort a domain has already absorbed. That is a much better predictor of where
agentic optimization pays than any benchmark score, and it generalises past kernels.

The knowledge base that **records failures with root causes** is a concrete implementation of the pattern
[[Recursive Self-Improvement]] separates out as the loop where *the scaffold's memory* is the thing that
persists — not the weights. It is also, structurally, the same argument this vault makes for itself in
[[Persistent Wiki]]: the durable asset is the accumulated record of what was tried and what it cost.

Read against [[Philip Kiely - The Efficient Frontier of LLM Inference]] from the same company, this is the
worked example of a **frontier-moving** technique: kernel optimization does not trade latency against
throughput, it reduces the work per token and lets the gain be allocated anywhere.

## Tensions / open questions

- **Vendor self-report, no external validation.** Every number is Baseten's, measured on Baseten's stack,
  against Baseten's own prior baseline. The size of a percentage improvement depends entirely on how good that
  baseline was, and it is not characterised.
- Several optimizations — the FLUX.2 contiguity guard, the repeated FP8 scale repacking — read as **fixing
  pre-existing inefficiencies** in the deployment. It is not established how much of the 42.3% is novel
  optimization versus recovered waste that a human profiler would also have found.
- The MiniMax M3 and GLM-5.2 LLM figures are hedged as "up to" and flagged "stay tuned", so they are
  preliminary.
- The per-kernel optimization results are presented as tables the capture does not include, so those
  sub-results are not independently checkable here.
- Correctness is asserted via "correctness checks" and one bit-identical claim; the general numerical
  tolerance policy for accepted kernels is not stated.
- If each deployment evolves its own kernels, what happens to reproducibility and to debugging across
  deployments that no longer run the same code?

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[AI-Generated Kernels]]
- [[GPU Kernel Optimization]]
- [[Recursive Self-Improvement]]
- [[Inference Efficiency Frontier]]
- [[Baseten]]

## Related pages

- [[Philip Kiely - The Efficient Frontier of LLM Inference]]
- [[Model Quantization and Efficiency]]
- [[Diffusion Models]]
- [[Persistent Wiki]]
- [[Agent Memory]]
- [[Software Performance Engineering]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Inference Serving Engines]]
- [[Automated AI Research]]

## Citations

- Raw capture: [[2026-08-29 Baseten - Agentic Kernels in Production]]
- Source: <https://www.baseten.co/blog/agentic-kernels-in-production/>
