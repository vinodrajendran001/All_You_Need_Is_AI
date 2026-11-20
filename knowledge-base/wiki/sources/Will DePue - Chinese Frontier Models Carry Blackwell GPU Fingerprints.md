---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-12-will-depue-checkpoint-forensics
source_title: "Top Chinese Frontier AI Models Carry the Fingerprint of Export-Controlled NVIDIA Blackwell GPUs"
source_author: "Will DePue (Unemployment Labs)"
source_url: "https://unemploymentlabs.com/checkpoint-forensics"
tags:
  - source/summary
  - hardware
  - gpu
  - accelerators
  - open-models
source_ids:
  - src-2026-11-12-will-depue-checkpoint-forensics
status: active
---

# Top Chinese Frontier AI Models Carry the Fingerprint of Export-Controlled NVIDIA Blackwell GPUs

## Summary

This report from Unemployment Labs, attributed in its suggested citation to Will DePue, describes a
*checkpoint forensics* method. The method infers which GPU class created a model's starting weights,
using only the published weights. It applies the method to open-weight models from Chinese labs. It
reports that six models released since April 2026 have initialization patterns matching NVIDIA
Blackwell GPUs: DeepSeek-V4-Flash, DeepSeek-V4-Pro, Kimi K3, Kimi K3.1-Pro, MiniMax-M3 and
Ling-3.1-flash. Earlier models from the same labs match Hopper. The report is careful about its own
limits. The fingerprint identifies the *initialization* hardware, not necessarily the training
hardware. It cannot show where the chips were or who owned them. The report says it does "not
establish … whether export controls were violated". Its conclusion is stronger than those limits: it
calls the V4-Flash evidence "conclusive" and says the finding "deserves urgent attention". This is a
single independent investigation. No response from the named labs is reported.

## Key claims

### The mechanism (measured and reproducible)

- PyTorch fills initial weights with the Philox random-number generator through cuRAND. The work is
  split across GPU threads, and on the chips examined each streaming multiprocessor (SM) runs up to
  **2,048** threads. The seed decides which numbers are generated. The total thread count decides
  where each number lands.
- So the layout depends on the chip's SM count. Hopper H100 SXM, H200 and H800 have **132** SMs
  (**270,336** threads). Blackwell B200/B300 have **148** (**303,104**), and GB200/GB300 have **152**
  (**311,296**). The method cannot tell chips within a group apart. A Hopper reading cannot separate
  H800 from H100 or H200.
- Some weights, such as rows for never-used vocabulary entries, keep their starting values almost
  exactly. Trained weights keep a faint trace. Across **42** layers of V4-Flash, averaging
  **745,472** weights per layer, the Blackwell layout gives r = **0.066** (**57 sigma**) and the
  Hopper layout gives nothing.
- The search picks a seed and layout on one set of weights, then tests it on held-out weights.

### Findings (inference from the measurements)

| Lab | Model | Reported SM layout |
| --- | --- | --- |
| DeepSeek | V4-Flash | 148 (B200/B300) |
| DeepSeek | V4-Pro | 152 (GB200/GB300) |
| Moonshot AI | Kimi K3; K3.1-Pro (same seed) | 152 |
| MiniMax | MiniMax-M3 | 148 |
| Ant Group | Ling-3.1-flash | 152 |

- Earlier models read as Hopper: DeepSeek through V3 and V3.2, Kimi through K2.5, MiniMax through
  M2.7, and Ling-3.0-flash. Kimi K2.7-Code blends about **80%** Hopper-layout values with about
  **20%** of a 148-SM draw. The report reads this as a merged checkpoint and does not count it among
  the six.
- The newest readable models from Alibaba (Qwen), Zhipu, Tencent, Xiaomi and StepFun read as Hopper.
  Meituan's LongCat-2.0 shows no NVIDIA fingerprint. Its model card cites "AI ASIC superpods", and a
  since-deleted config the report reads as Huawei Ascend 910.
- No signature was found in DeepSeek-V4.1-Flash "despite an exhaustive search". PaddlePaddle's
  ERNIE-5.5 yields a seed (**2760**) but no layout. Qwen3 models initialized on CPU leave no trace.

### Validation (as reported)

- **Physical reproduction.** With DeepSeek's seed **953049583**, a B300 reproduced **461** of
  **469** selected V4-Flash rows at correlation above 0.99, **445** of them bit for bit. An H100
  reproduced all **57,344** preserved V3 values bit for bit. Neither chip reproduced the other
  model's rows. Seed ±1 matched nothing. On a rented GB200, Kimi K3's seed **20256586** reproduced
  **13** of **13** preserved rows.
- **Known answers.** The readings agree with all **24** developer-disclosed cases. Examples: Llama
  3.1 reads 132, Pythia reads 108, and Nemotron-3 Ultra (GB200 for one phase) reads 152. The report
  itself frames this as "a consistency check rather than a measured accuracy rate", because 11 cases
  are step-zero checkpoints and related models are not independent.
- **Statistics.** About **6 trillion** seed-and-layout combinations were searched, so the chance
  benchmark is about **8 sigma**. The six models' strongest results range from **49** to **1,385**
  sigma, and the weakest reported test is **20** sigma. All of this holds "provided the statistical
  model correctly describes the random variation".
- Code and preserved rows are public (github.com/macrogrants/checkpoint-forensics).

### The alternative the report tested

An AMD MI300X, also export-controlled, limited to 152 or 148 compute units reproduces the same
layouts. For V4-Flash, in the **377** values where AMD and NVIDIA arithmetic differ, the weights
match NVIDIA in **363** and AMD in none. For the other five models the test was inconclusive. The
report calls AMD "very unlikely" there, because a whole cluster would have to be configured unusually.

### Scale estimates (explicitly low-confidence)

Revised on November 12, the report estimates about **4,500** Blackwell GPUs for Kimi K3 (range
1,000–9,500) and about **3,000** for V4-Pro (750–6,500). Across the five runs it estimates about
**12,000** (7,000–22,000). These figures assume about 20% MFU (25% for DeepSeek), run lengths
estimated from release dates, and token counts that are DeepSeek's own for its models and, for the
others, estimated by an unpublished method. At an implied **$70,000** per GPU, the largest cluster
would cost $200–300 million. The first version gave 2,000–3,000 GPUs and $150–200 million.
"We are not confident in these estimates."

## Why it matters

Open weights carry information about how a model was built that the developer did not choose to
disclose. This method turns a software detail (how PyTorch splits random-number generation across
threads) into a hardware-provenance signal. The published check for five of the readings runs on a
laptop in a few seconds. It matters for compute-access debates, but it measures only one thing:
which GPU class generated the starting weights. Everything beyond that is argued, not measured:
training location, ownership, how access was obtained, and legality.

## Tensions / open questions

- **Initialization vs. training.** A lab could initialize on one system and train on another, or
  run a mixed cluster. In such a cluster, Huawei participation would be invisible. The report
  "supports, without proving" Blackwell training.
- **Access vs. location vs. legality.** Blackwell can be rented outside China. The export-status
  flags are "not a finding that any law was broken". Supporting evidence is mostly secondhand: press
  reports and US-official allegations, plus a GB300 benchmark file in Ant Group's public code.
- **Counter-evidence the report cites.** In June 2025 a DeepSeek engineer wrote on GitHub "we don't
  have SM100 GPUs". That predates V4's April 2026 release, so it neither confirms nor refutes the
  later reading.
- **No lab response** is reported, and no rebuttal is addressed.
- **Single-author report, partly unreplicated.** Some rows, such as Ling-1T, come from
  "one analysis pass, not yet re-run". The report confirmed matches on physical Blackwell hardware
  only for V4-Flash and Kimi K3. V4-Pro, MiniMax-M3 and Ling-3.1-flash rest on the statistical
  search alone, and K3.1-Pro on its own statistical reading (305σ, same seed as K3) without an
  independent re-run or physical reproduction.
- **Tone vs. stated limits.** "Conclusive" and "urgent attention" sit beside careful limitation
  language. Downstream pages should quote the limits along with the headline.

## Affected pages

- [[Checkpoint Forensics]]
- [[NVIDIA]]
- [[DeepSeek]]
- [[Open Model Ecosystems]]

## Raw capture

- [[knowledge-base/raw/sources/Top Chinese Frontier AI Models Carry the Fingerprint of Export-Controlled NVIDIA Blackwell GPUs]]

## Citations

- Canonical URL: <https://unemploymentlabs.com/checkpoint-forensics>. A `utm_source=tldrai` parameter
  was removed.
- Published 2026-11-12 (capture `published` field), with a revision of the GPU estimates the same
  day. Captured 2026-11-20.
- The capture's `author` field is empty. The author is taken from the report's own suggested
  citation, "Will DePue … Unemployment Labs, November 12, 2026", and its contact line. No fetch was
  needed.
- Independent analysis, not peer-reviewed. Political and press sources are cited by the report and
  were not checked here.

## Related pages

- [[Checkpoint Forensics]]
- [[NVIDIA]]
- [[DeepSeek]]
- [[Open Model Ecosystems]]
- [[AI Accelerator Architecture]]
- [[Inferact - 700 TPS on Kimi K3 - A Case for TPU Megakernels]]
- [[Mehul Gupta - What is DeepSeek DeepInfer]]
