---
type: source-summary
created: 2026-08-03
updated: 2026-10-19
source_id: src-2026-07-22-mitchell-hashimoto-simd
source_title: "Everyone Should Know SIMD"
source_author: Mitchell Hashimoto
source_url: https://mitchellh.com/writing/everyone-should-know-simd
tags: [source/summary, simd, cpu, performance]
source_ids: [src-2026-07-22-mitchell-hashimoto-simd]
status: active
---

# Mitchell Hashimoto - Everyone Should Know SIMD

## Summary

A practitioner essay arguing that everyday SIMD is simpler than its reputation. Most "process N
values at a time" code follows one five-step shape, and every developer should be able to spot when
a hot loop over contiguous data can use it. The examples are in Zig, but the argument is
language-general. The worked case comes from Ghostty, the author's terminal emulator: a one-line
scalar scan for the end of a printable run becomes a generic vector loop of 12 more lines, with the
original scalar loop kept as tail and fallback.

The evidence is one first-party optimization with a single end-to-end measurement. The author notes
the post was written without AI assistance.

## Key claims

- **The common shape.**
  1. Broadcast constants and initialize any vector accumulators.
  2. Loop one vector-width chunk at a time.
  3. Apply the comparison or arithmetic across all lanes.
  4. Reduce or store the vector result.
  5. Handle the remainder with a scalar tail, which is the original loop.
- **Worked example.** The loop scans decoded codepoints until a value at or below `0xF`:
  - `@splat` broadcasts the threshold.
  - Full vectors are loaded only while at least `lanes` values remain.
  - One vector `>` compares every lane.
  - `@reduce(.And, ...)` skips all-printable chunks.
  - `@bitCast` plus `@ctz` on the inverted mask locate the first failing lane.

  A helper returns **4** `u32` lanes on ARM, **8** on AVX2, **16** on AVX-512, or `null`, in which
  case only the scalar loop runs.
- **Ideal versus realized speedup.** The loop's throughput can improve by up to **4x** with ARM
  NEON, **8x** with AVX2, and **16x** with AVX-512. Measured end to end, from terminal program to
  finalized terminal state on an AVX2 Intel desktop, the gain was "more like a 5x speedup," because
  the work around the SIMD code does not accelerate.
- **When it pays.** SIMD pays when loops regularly process hundreds to millions of bytes; for a
  handful or dozens it is not worth it. If a loop resists the common shape, that is "usually a good
  sign to skip it for now."
- **Generic vectors, not intrinsics.** Zig's vector types remove CPU-specific syntax but still lower
  to the instruction set enabled for the target.
- **Compilers.** They can auto-vectorize simple loops, especially regular arithmetic without complex
  control flow, so the author advises compiling the optimized scalar version and checking what the
  compiler produces first. But he calls compilers "severely limited" and wants hot loops vectorized
  explicitly, so an unrelated code change or compiler update cannot quietly turn one back into a
  scalar loop.

## Why it matters

[[SIMD]] and [[Software Performance Engineering]] use the post as the vault's concrete CPU
vectorization recipe. The gap between AVX2's nominal **8x** and the measured **5x** end to end is the
ceiling-versus-realized point in one example. The same data-parallel reasoning appears at
accelerator scale in [[GPU Execution Model]] and [[AI Accelerator Architecture]]; this post applies
it to CPU-side hot loops such as scanning and parsing.

## Tensions / open questions

- One workload, one machine class, and one end-to-end figure, with no variance, profile, or
  breakdown of where the remaining time goes.
- The post attributes the lost speedup to "the other stuff around the SIMD code" and notes that
  loading, reducing, and locating the failed lane take extra instructions. It does not measure memory
  bandwidth or isolate the vector loop's own speedup.
- It offers no threshold for when explicit vectorization should replace checking compiler output,
  and it weighs maintenance cost only by preferring explicitness.
- The generic-vector approach depends on language support, which the author notes varies.

## Affected pages

- [[SIMD]]
- [[Software Performance Engineering]]

## Raw capture

- [[2026-07-27 Mitchell Hashimoto - Everyone Should Know SIMD|Everyone Should Know SIMD]]

## Citations

- Canonical essay: <https://mitchellh.com/writing/everyone-should-know-simd>
- Published July 22, 2026; captured July 27, 2026. The capture's author field is blank; the byline
  and date appear in the body.
- The essay says it grew from one of the author's Lobsters comments, which was not read separately.

## Related pages

- [[SIMD]]
- [[Software Performance Engineering]]
- [[Jeff Dean and Sanjay Ghemawat - Performance Hints]]
- [[GPU Execution Model]]
- [[AI Accelerator Architecture]]
