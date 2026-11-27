---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-20-ankit-gupta-vibecoding-inference-chip
source_title: "Vibecoding an inference chip"
source_author: Ankit Gupta
source_url: https://ankitg.me/blog/vibecoding-inference-chip/
tags:
  - source/summary
  - hardware
  - fpga
  - coding-agents
  - autoresearch
source_ids:
  - src-2026-11-20-ankit-gupta-vibecoding-inference-chip
status: active
---

# Vibecoding an Inference Chip

## Summary

Ankit Gupta describes a coding agent implementing and optimizing **bit-exact** LLM inference for a
DeepGrove ternary-weight model on an AWS F2 FPGA. A cloud agent ran in Conductor for several days, and
the author used "Astra and Opus" interchangeably. The loop wrote "roughly 3M lines across the
experiment history", parsed 30M lines of output and spent **$10,000** in Claude and OpenAI tokens on
hundreds of experiments. It took throughput from **6.43** tok/s, the first full-model bit-exact image,
to **213.13** tok/s (**33.13×**) in 14 measured steps, mostly compounding modest gains. A design
prompt from DeepGrove's founders mostly confirmed ideas already planned. Its process advice, to stop
hours-long simulations and use a short synthesis loop, changed things at once, possibly at the cost of
two hardware hangs and 38 lost hours. In a price table on one benchmark, the FPGA is the fastest
bit-exact option, but the author says the comparison is not 1:1. He does not recommend the setup for
production.

## Key claims

### Setup

- An AWS F2 instance (f2.6xlarge) with **16 GB** of FPGA HBM, reserved by Codex. The target was
  DeepGrove's new ternary-weight architecture ("SOTA on Mac hardware with actual agentic tool
  calling"). The served model is never named; the implementation has an MoE router.
- The code is mostly C++ with some Verilog, which the author has "never written". His prompts were
  mostly encouragement ("let's go for 2x faster, you got this"), plus occasional ML hints such as
  considering speculative decoding. A chart's alt text counts **166 prompts**, seven of them
  highlighted as steering prompts.
- "both Astra and Opus (new Fable wasn't out yet) were pretty capable at this". The token budget is
  credited with "(thanks YC)".

### The optimization log

Every step kept the bit-exact contract against a pinned reference.

| Step | tok/s | What changed |
| --- | --- | --- |
| 0 | 6.43 | First full-model bit-exact image (R8) |
| 1 | 8.07 | Host software: per-command overhead from ~10 ms to 0.9 ms |
| 2 | 14.02 | 128-lane attention engine reading KV in bursts, in the reference's exact summation order |
| 3 | 20.53 | Parallel MoE router with an exact tie-breaker and a streaming output head; 250 MHz |
| 4 | 30.24 | Glue engine for norms, RoPE, quantization and copies "in certified exact orders" |
| 5 | 49.21 | New pipeline and sequencer, after fixing two hangs that appeared only in hardware |
| 6 | 51.25 | Exact speculative decoding by prompt lookup (1.04× this step) |
| 7 | 58.43 | Router weight relay between dies fixed: stall per layer 43,862 → 12,292 cycles |
| 8 | 94.44 | Head shadow (start the next token on a provisional guess); 237.5/450 MHz |
| 9 | 105.63 | Draft model, "a cut-down Maple" on the host CPUs; the FPGA verifies every token |
| 10 | 108.81 | Memory ports 4 → 8: 1.39× per clock, but congestion cut the clock to 181/375 MHz |
| 11 | 134.99 | KV fetches hidden behind compute; exact order-independent router sum, 12,292 → 2,338 cycles |
| 12 | 171.3 | Lossless 5-trit weight packing (−20% weight bytes); 225/400 MHz |
| 13 | 184.19 | Re-speculation, speculative expert prefill, die rebalance; 231.25/450 MHz |
| 14 | 213.13 | Parallel head loader (+17.3%); run at 225/425 MHz after a soak test found random faults at 231.25 |

The author calls it "mostly a series of modest improvements that compound 1.5x ish every time, rather
than one or two giant ones". The per-step factors the capture prints range from 1.03× to 1.74×.

### Human advice: process mattered more than design

- Near 10 tokens per second, the DeepGrove founders, who had tried this months earlier when models
  "were not quite good enough", sent a 4,741-character prompt describing someone else's dense, batch-1
  ternary FPGA decoder. It covered a multiplier-free ternary matmul, an 8-bit KV cache, online softmax,
  MoE notes, a verification ladder and physical design, and asked the agent to avoid things "that take
  a lot of times", such as long cycle-accurate simulations.
- In the agent's own retrospective, written from its logs, it sorted the prompt into ten ideas to adopt
  and five to reject within 70 seconds. The adopted design ideas were mostly already planned, and "I
  can't show these wouldn't have happened without the notes."
- **All five numerics shortcuts were rejected**, from lower-precision activations to an 8-bit KV cache
  and online softmax. Each changes the output bits, which is "where their design got its efficiency",
  and the bit-exact rule ruled them out.
- **The process advice changed things "right away".** The agent stopped a simulation that had run for
  about 24 hours and switched to a short loop of C tests, synthesis and a logic-depth check. The
  possible cost, which it "can't prove": two hangs that only RTL simulation could show reached the
  board, and the big integration lost **38 hours** to them.
- One real find: AWS's reference memory design reaches **426 GB/s** across all 32 memory channels, and
  the memory subsystem was built from it.
- The author's conclusion: "the humans are still useful at defining how to iterate fast and what
  correctness looks like, and the agents are great to manage the exploration."

### How it compares

These are November 15 measurements on AWS, replaying the same 8-chat × 3-turn benchmark at on-demand
prices. "Exact turns" counts outputs matching the pinned CPU reference.

| Configuration | Instance | $/hour | tok/s | Exact turns | FPGA faster by |
| --- | --- | --- | --- | --- | --- |
| F2 FPGA, r9 final image | f2.6xlarge | 1.98 | 213.13 | 24/24 | — |
| Exact CPU twin, 32 threads | m8a.8xlarge | 1.95 | 129.5 | 24/24 | 1.65× |
| Exact CPU twin, 24 threads | c7i.12xlarge | 2.14 | 99.6 | 24/24 | 2.14× |
| Pinned scalar reference, 32 cores | m8a.8xlarge | 1.95 | 40.6 | 24/24 | 5.25× |
| Pinned scalar reference, 1 thread | r7i.2xlarge | 0.53 | 1.1 | 24/24 | 195× |
| Exact CPU twin, 4 threads | m8a.xlarge | 0.24 | 67.6 | 24/24 | 3.16× |
| DeepGrove's fork with GPU offload | g4dn.xlarge (T4) | 0.53 | 35.7 | 1/24 | 5.97× |
| Community CUDA port | g4dn.xlarge (T4) | 0.53 | 166.3 | 0/24 | 1.28× |

The GPU rows "did not satisfy the same bit-exact criterion but are pretty close in practice". The
author: "It's difficult to do a 1:1 comparison", and he did not run the same loop on any alternative.
*Derived reading, not the author's:* per dollar per hour, the 4-thread CPU twin and the T4 CUDA port
deliver more tokens than the FPGA in this table.

### Long contexts

In one generation from a 16-token prompt to the full **8,192-token** context, r9 decoded at 233 tok/s
at 16-64 tokens and 151 at 1-2k (both from separate 2,032-token runs), then 120, 93 and 76 tok/s at
2-4k, 4-6k and 6-8k. The whole run took **77.8 s**, against 77.6 s for r8: "r9 improves short-context
speed, while the complete long-context run is roughly tied with r8."

## Why it matters

For [[AI Accelerator Architecture]], this is the vault's first hands-on account of LLM decode on an
FPGA. It qualifies "fast to redeploy", since builds and simulations ran for hours, and shows the clock
as an outcome of each design, with memory channels and die crossings dominating the work. In
[[AI-Generated Kernels]], bit-exactness is the cheap, objective verifier, and 33× from the loop's own
first image fits that page's rule that agentic optimization pays most where little human tuning
exists. For [[Accelerator Software Externalization]], $10,000 of tokens for one model on one target is
a small data point beside the "<$1m token spend" rebuild forecast. [[Y Combinator]] funded the tokens.
The loop also bears on [[Automated AI Research]], [[Loop Engineering]], [[Speculative Decoding]] and
[[Inference Determinism]].

## Tensions / open questions

- **One self-reported project.** No repository, bitstream or logs are in the capture. The
  "what it adopted and rejected" account is the agent's self-assessment of its own logs.
- **The baseline is the loop's own first image.** 33× measures progress over a naive, correct starting
  point, not over an optimized FPGA design. No ablation separates the agent's work from the human hints
  ("consider speculative decoding"; "why is that running on CPU, you should port it").
- **The model is unnamed.** The DeepGrove notes describe someone else's decoder for "a dense qwen style
  model" yet include MoE advice, and the implementation has an MoE router. The capture never names the
  served model or its size.
- **Incomplete cost accounting.** The $10,000 covers tokens only, not F2 hours or the author's time,
  and there is no energy measurement.
- **Not like-for-like.** The GPU rows run on a T4, are not bit-exact and were not optimized by the
  loop. The "195×" row is a rounding of 213.13 / 1.1 (about 194, derived). The 213 tok/s headline is a
  short-context chat benchmark; at 6-8k context, decode ran at 76 tok/s.
- The capture's author field is empty (see Citations). Model names are copied as written.

## Affected pages

- [[AI Accelerator Architecture]]
- [[AI-Generated Kernels]]
- [[Accelerator Software Externalization]]
- [[Y Combinator]]
- [[Automated AI Research]]
- [[Loop Engineering]]
- [[Speculative Decoding]]
- [[Inference Determinism]]

## Raw capture

- [[knowledge-base/raw/sources/Vibecoding an inference chip]]

## Citations

- Canonical URL: <https://ankitg.me/blog/vibecoding-inference-chip/> (the capture's `utm_source`
  parameter removed).
- Published 2026-11-20; captured 2026-11-24. The capture's `author` field is empty. The byline Ankit
  Gupta was recovered from the live page header, and his role as a General Partner at Y Combinator from
  his About page on the same site, both outside the capture. The capture itself says only "(thanks
  YC)".

## Related pages

- [[AI Accelerator Architecture]]
- [[AI-Generated Kernels]]
- [[Accelerator Software Externalization]]
- [[Y Combinator]]
- [[Automated AI Research]]
- [[Loop Engineering]]
- [[Speculative Decoding]]
- [[Inference Determinism]]
- [[Model Quantization and Efficiency]]
- [[Mixture of Experts]]
- [[GPU Kernel Optimization]]
- [[Dwarkesh Patel - Reiner Pope - Chip design from the bottom up]]
- [[Baseten - Agentic Kernels in Production]]
- [[Pavi Dhiman and Cyrus Asgari - Building an Inference Stack That Improves Itself]]
- [[Tomas Pueyo - Hardware Is Software]]
