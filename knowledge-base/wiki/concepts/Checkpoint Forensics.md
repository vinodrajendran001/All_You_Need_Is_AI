---
type: concept
created: 2026-11-20
updated: 2026-11-27
tags:
  - concept
  - open-models
  - hardware
  - gpu
source_ids:
  - src-2026-11-12-will-depue-checkpoint-forensics
  - src-2026-11-27-modaic-jev-latency-fingerprint
status: active
---

# Checkpoint Forensics

## Definition

Checkpoint forensics infers facts about how a model was produced from its published weights alone.
The facts include the initialization seed, the hardware class that generated the starting weights,
and shared lineage between models. In the one method the vault records, [[PyTorch]] spreads Philox
random-number generation across GPU threads through cuRAND. On the NVIDIA chips examined, each
streaming multiprocessor (SM) runs up to **2,048** threads, so the chip's SM count determines where
each generated value lands. See [[GPU Execution Model]].

## Why it matters

Open weights disclose more than a developer chooses to state. Compute access is a policy question,
and model cards often omit hardware. A method whose published check anyone can rerun on a laptop is
therefore significant. So are its limits, because the step from "initialized on" to "trained on" to
"legally acquired" is long.

## Current synthesis

[[Will DePue - Chinese Frontier Models Carry Blackwell GPU Fingerprints]] is the only source for the
weight-based method. It is a single independent investigation, and no response from the named labs
is reported. The layers below are kept apart on purpose.

### What is measured

- **Layouts.** Hopper (H100 SXM, H200, H800) reads as **132** SMs, B200/B300 as **148**, and
  GB200/GB300 as **152**.
- **Preserved and faint traces.** Some rows, such as never-used vocabulary entries, keep their
  starting values almost exactly. Trained weights keep a weak trace: across **42** layers of
  V4-Flash, the Blackwell layout gives r = **0.066** (**57 sigma**) and the Hopper layout gives
  nothing.
- **Search and held-out testing.** A seed and layout chosen on some weights is tested on held-out
  weights. About **6 trillion** combinations were searched, so the chance benchmark is about
  **8 sigma**. The six flagged models' strongest results range from **49** to **1,385** sigma, and
  the weakest reported test is **20** sigma.
- **Physical reproduction.** A B300 reproduced **461** of **469** selected V4-Flash rows at
  correlation above 0.99, **445** bit for bit. An H100 reproduced all **57,344** preserved DeepSeek V3
  values bit for bit, and neither chip reproduced the other model's rows. A rented GB200 reproduced
  **13** of **13** preserved Kimi K3 rows. Seed ±1 matched nothing.
- **AMD alternative.** An AMD MI300X restricted to 148 or 152 compute units mimics the layouts. For
  V4-Flash, in the **377** values where AMD and NVIDIA arithmetic differ, the weights match NVIDIA
  in **363** and AMD in none. For the other five models that test was inconclusive.
- **Known answers.** The readings agree with all **24** developer-disclosed cases, including
  NVIDIA's Nemotron-3 Ultra, which reads 152. The report calls this "a consistency check rather than
  a measured accuracy rate", because 11 cases are step-zero checkpoints and related models are not
  independent.

### What is inferred

- Six Chinese open-weight models released since April 2026 read as Blackwell initializations:
  DeepSeek-V4-Flash, DeepSeek-V4-Pro, Kimi K3, Kimi K3.1-Pro, MiniMax-M3 and Ling-3.1-flash. Earlier
  models from the same labs read as Hopper.
- The evidence behind the six is uneven. Physical confirmation exists only for V4-Flash and Kimi K3.
  V4-Pro, MiniMax-M3 and Ling-3.1-flash rest on the statistical search alone, and K3.1-Pro on its own
  statistical reading (305σ, same seed as K3) without an independent re-run or physical reproduction.
- None of the six is marked as coming from "one analysis pass, not yet re-run". That mark applies to
  two Hopper readings, Ling-1T and GLM-4.5, with their same-init siblings.
- The report says initialization "supports, without proving", Blackwell training.
- The report also gives GPU-count and cost estimates. It marks them low-confidence ("We are not
  confident in these estimates") and revised them on publication day. The vault does not carry them
  forward.

### What is alleged or contextual, and not checked

- Export status, press reports and US-official allegations are context the report cites, not
  findings of the method. The vault has not checked them. The report's export-status flags are "not a
  finding that any law was broken".
- Counter-evidence the report cites: in June 2025 a DeepSeek engineer wrote "we don't have SM100
  GPUs". That predates V4's release, so it neither confirms nor refutes the later reading.

### Built-in limits

- The method sees initialization, not training. A lab could initialize on one system and train on
  another.
- It cannot separate chips within a group, so a Hopper reading cannot tell H800 from H100 or H200.
- It cannot see location or ownership, and Blackwell can be rented outside China.
- It is blind to CPU initialization, PaddlePaddle, and mixed clusters, in which Huawei participation
  would be invisible.
- The AMD alternative was excluded numerically only for V4-Flash.
- The statistics hold only "provided the statistical model correctly describes the random
  variation".
- By its own statement, the report does "not establish where the chips were located, how access was
  obtained, or whether export controls were violated".

The report's tone runs ahead of these limits. It calls the V4-Flash evidence "conclusive" and says
the finding "deserves urgent attention". Pages citing it should quote the limits along with the
headline.

## Black-box provenance from API behavior

[[Modaic - Latency Doesn't Lie - Jev Is (Probably) Qwen3.5-35B-A3B]] attempts provenance without
weights. Strictly, that falls outside the definition above, which requires published weights; the
vault records it here as the closed-model counterpart. Modaic infers that [[TypeSafe AI]]'s hosted
Jev is probably a fine-tune of [[Qwen]]'s Qwen3.5-35B-A3B from three behavioral signals:
self-identification prompts, how well candidate tokenizers' counts rank latency (Spearman's ρ
**0.805** for Qwen against **0.719** for Jev's own reported counts), and a prefill throughput curve
matched to a known Qwen-based [[Mixture of Experts]] model.

Its limits are sharper than those of the weight method above. Weight forensics replays a
deterministic process and can reproduce values bit for bit; black-box inference compares statistical
resemblances against controls the investigator chooses. Here the tokenizer signal cannot separate
Qwen from Gemma, throughput cannot separate two Qwen generations of the same architecture, network
and serving overhead sit inside every timing, and the reference curves come from self-hosted
single-B200 workers while Jev's hardware is unknown. The source calls its throughput comparison "an
approximate performance fingerprint". It comes from a competitor of the model examined, and its
proposed next step, knowledge-cutoff probes, is untested.

## Open questions

- Will labs defeat the method by initializing on CPU or reshuffling weights? Some Qwen3 models
  already leave no layout because they were initialized on CPU.
- Can independent groups reproduce the four readings not confirmed on physical hardware?
- What other production facts leak from weights, such as data mixture, lineage or merges? The report
  reads Kimi K2.7-Code's **80/20** blend of Hopper and 148-SM values as a merged checkpoint.
- Will any named lab respond? None has, as far as the vault records.
- Can black-box signals such as self-identification, tokenizer-latency correlation, throughput
  curves or knowledge-cutoff probes separate candidate bases that share a tokenizer family or an
  architecture? The one attempt recorded here separated neither Qwen from Gemma by tokenizer nor two
  Qwen generations by throughput.

## Related pages

- [[Open Model Ecosystems]]
- [[NVIDIA]]
- [[DeepSeek]]
- [[AI Accelerator Architecture]]
- [[PyTorch]]
- [[GPU Execution Model]]
- [[Will DePue - Chinese Frontier Models Carry Blackwell GPU Fingerprints]]
- [[Modaic - Latency Doesn't Lie - Jev Is (Probably) Qwen3.5-35B-A3B]]
- [[TypeSafe AI]]
- [[Qwen]]
- [[Mixture of Experts]]
