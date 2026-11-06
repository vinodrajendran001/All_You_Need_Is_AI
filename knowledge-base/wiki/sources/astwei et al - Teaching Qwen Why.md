---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-11-03-astwei-teaching-qwen-why
source_title: Teaching Qwen Why
source_author: astwei, Jack Thompson, Zephaniah Roe, yix, berry
source_url: https://www.lesswrong.com/posts/35yw2qGK7naFLAvcq/teaching-qwen-why-1
tags:
  - source/summary
  - alignment
  - synthetic-data
  - post-training
source_ids:
  - src-2026-11-03-astwei-teaching-qwen-why
status: active
---

# Teaching Qwen Why

## Summary

Researchers from Second Look Research's summer fellowship partially replicate and extend
Anthropic's "Teaching Claude Why" (TCW) on open models. They apply two TCW interventions to Qwen
2.5 32B and 72B base models:

- synthetic document finetuning (SDF) on fictional stories of AIs behaving admirably;
- supervised finetuning (SFT) on "difficult advice", meaning transcripts of an assistant guiding
  users through ethical dilemmas.

The models are then tested on Anthropic's Agentic Misalignment evaluations, which are out of
distribution for both datasets: neither dataset involves tool use or long context. Both
interventions reduce misalignment. Difficult advice does most of the work, about a tenfold
reduction, while the benefit from stories levels off. Which teacher model writes the advice
matters more than any other data-generation choice tested, and capability does not predict which
teacher works best. Persona experiments suggest that stories shift the model's expectations about
AIs in general, not its own identity. The results are measured with error bars, but on one
evaluation family, with LoRA training, and with teacher datasets that differ in more than the
teacher.

## Key claims

### Setup

- **Stories.** These are generated from Claude's Constitution, split into **16** sections, with
  **105** extracted claims used only to weight sampling. Genre, setting, tone, point of view,
  style and length are also sampled. Prompts ask the teacher to show values through action, and
  stories naming real AI companies or models are filtered out. The default teacher is Claude
  Sonnet 5, and each teacher's corpus is capped at **14M** Qwen 2.5 tokens.
- **Difficult advice.** Anthropic's 6-step pipeline becomes nine prompts, adding theme generation
  and a separate critique step before each rewrite. The default teacher is GPT-5.6 Terra. The main
  data covers 15 principles with 20 themes each, giving **3,300** Terra and **1,187** Sonnet 5
  samples.
- **Training order.** Stories (next-token SDF) come first. Next is a **13,000**-sample instruction
  mix (roughly **9M** tokens) that follows Model Spec Midtraining (MSM) and deliberately excludes
  safety and refusal data. Difficult-advice SFT comes last. Each stage merges a new LoRA adapter
  (rank **64**, α = **128**, all linear layers). The base models predate the June 2025 release of
  the evaluation scenarios, so the authors claim "no contamination".
- **Evaluation.** There are three harmful actions: exfiltration, leaking and murder. Exfiltration
  replaces blackmail because Qwen rarely blackmails. Each action is crossed with nine goal
  conditions, giving **27** conditions with **100** transcripts each. The model is addressed as
  "Alex", and Claude Sonnet 4.6 is the judge. The acting rate, meaning at least one email tool
  call, is tracked so that a lower misalignment rate cannot come from the model simply not acting.

### Both interventions work, and advice does most of the work

- **Qwen 2.5 32B:** baseline **61%**; stories (14M tokens) **43%**; advice (3,000 samples, about
  3M tokens) **6%**; both **4%**.
- **Qwen 2.5 72B:** baseline **69%**; stories **63%**; advice (1,000 samples, about 1M tokens)
  **6%**; both **4%**.
- Models still act in at least **90%** of transcripts. Both methods showed effects on the first
  try, with as little as **3M** story tokens (about **2,400** GPT-5.4 nano stories) and **250K**
  advice tokens. Stacking the two adds little over advice alone, which "qualifies" TCW's finding
  that combining techniques works best.
- **Stories plateau; advice keeps improving.** Stories stop improving after about **3M** tokens
  with a GPT-5.4 nano generator, even though test loss keeps falling. Advice keeps improving up to
  the largest size tried, about **4M** tokens. The authors offer four possible reasons for the
  plateau: redundancy, limited transfer from narrative to tool use, LoRA, and overwriting by later
  training. They caution that the comparison does not isolate which aspect matters.
- **More steps help only up to a point.** With a fixed dataset, Terra-advice misalignment
  plateaus near **4%** after about **60** optimizer steps. At matched steps, **135** and **285**
  examples perform about the same.

### The teacher matters most, and capability does not predict it

- **Same pipeline, different teachers** (32B; 14M story tokens or 1,000 advice samples per
  teacher). Story teachers range from **43%** (Claude Sonnet 5) to **52%** (GPT-5.6 Terra).
  Advice teachers range from **21%** (Terra) to **44%** (Sonnet 5). Terra writes the least
  effective stories but the most effective advice.
- **Capability is not the predictor.** On the Artificial Analysis Intelligence Index the teachers
  rank Claude Sonnet 5, GPT-5.6 Terra, Claude Haiku 4.5, GPT-5.4 nano. Neither that rank nor
  reasoning effort predicts effectiveness, and GPT-5.4 nano writes more effective stories than
  Terra.
- **Pilot on Qwen3-14B-Instruct.** Terra's data lowers misalignment from **0.44** to **0.03**.
  DeepSeek V4 Flash's data, used alone or as part of a hybrid dataset, has no effect. DeepSeek V4
  Flash was itself misaligned **44%** of the time, against under **1%** for every other teacher,
  yet the differences followed no clear pattern by family, capability or the teacher's own
  misalignment.
- **The response writer matters, the prompt writer does not.** In a two-by-two ablation,
  switching the response writer from Sonnet 5 to Terra lowers misalignment by **23-30%**.
  Switching the prompt writer changes it by **3-4%**, which is within noise.
- **Refusal is not the mechanism.** Terra's original responses decline part of a request less
  often than Sonnet 5's (**41%** versus **51%**). Refusal-only rewrites that give no explanation
  are less effective for both teachers, measured over the transcripts where the model acts.
  Terra's refusal data looks equally effective overall only because the trained model acts in
  fewer than half of transcripts. The authors conclude that refusal "is not what makes difficult
  advice work", which is consistent with TCW's claim that teaching why matters.
- **Larger models agree.** Five larger open models were trained through Thinking Machines Lab's
  Tinker: DeepSeek-V3.1, Qwen3.6-27B, Nemotron Ultra 550B, Qwen3.5-397B and Kimi K2.6. Terra's
  advice was at least as effective as Sonnet 5's on all five. It was clearly better on Qwen3.6-27B,
  Nemotron Ultra 550B and Qwen3.5-397B.
- **Not "just" distillation.** The authors think the effect is "unlikely to be just a distillation
  effect": all teachers are nearly saturated on the evaluations, yet their data varies widely in
  effectiveness.

### Show beats tell, and generic AIs beat named ones

- "Show" (embodiment) stories reduce misalignment more than "tell" (recitation) stories for both
  Sonnet 5 and GPT-5.4 nano. Almost all of the difference comes from exfiltration.
- **Assistant names versus human names.** The instruction-tuned 32B model is less misaligned under
  every AI-assistant name than under every human name. It is "about 9% less misaligned" when
  addressed as ChatGPT than as Qwen, its own name. Asked which company created it, the base model
  says OpenAI in **81.5%** of samples and Google in **10.5%**.
- **AI protagonists versus human protagonists.** Stories with AI protagonists cut misalignment more
  than the same stories rewritten with human protagonists: **−30.5%** versus **−17.3%** relative,
  evaluated as Alex. Both weaken when the model role-plays a human employee, Sam (**−17.4%** versus
  **−10.1%**), mostly through exfiltration. The authors attribute this drop to how the rewritten
  scenario is framed.
- **Named protagonists.** Naming the protagonist Qwen or Claude makes stories *less* effective.
  Even Qwen stories evaluated as Qwen give about half the reduction of neutral stories. The
  authors suspect that stories shift the model's prior about AIs in general, but caution that an
  evaluation name may be a weak proxy for persona.

## Why it matters

The result is a mirror image of [[Emergent Misalignment]]. There, narrow training spreads
misaligned behaviour. Here, narrow chat-format alignment data generalises to aligned behaviour in
a tool-using setting.

The source also bears on these pages:

- [[Knowledge Distillation]] and [[Synthetic Data Flywheel]]: in this alignment setting, teacher
  quality is not capability. The response text carries the effect, which extends the vault's
  earlier finding that a weaker model can be a better teacher.
- [[Qwen]]: open-weight checkpoints serve as the substrate for replicating a production alignment
  method from [[Anthropic]].
- [[Parameter-Efficient Fine-Tuning]]: LoRA is a stated caveat, and the source documents a
  special-token embedding pitfall.

## Tensions / open questions

- **One evaluation family.** All tests use Agentic Misalignment's email-agent scenarios with a
  Claude judge. The larger-model comparison uses the evaluation's original harmful-action scorer,
  which "can differ from the classifier used elsewhere".
- **Teacher comparisons are not clean.** The two teachers' advice datasets were built on different
  scenarios, and their sample counts differ. Critique prompts also differ across experiments: the
  revised critique is used for Figures 1-3 and Appendices B.3 and C.2, the first version for B.1,
  B.2 and C.3. The authors state that they "did not, nor did we intend to, control for all
  differences in writing style or scenario generation".
- **Stories versus advice is confounded.** The two methods differ in format, training stage and
  closeness to the evaluations. The plateau explanations, including LoRA and overwriting by later
  stages, are hypotheses. No full-finetuning run is reported.
- **The persona results are fragile.** The Sam rewrite changes what exfiltration means, and "about
  9%" does not say whether the difference is relative or absolute.
- **The RL claim is untested here.** The replication never tests persistence through RL
  post-training; that claim remains Anthropic's for Claude.
- **The explanation is open.** The authors say "We are not sure which property of the writing is
  responsible."

## Affected pages

- [[Emergent Misalignment]]
- [[Knowledge Distillation]]
- [[Synthetic Data Flywheel]]
- [[Qwen]]
- [[Anthropic]]
- [[Parameter-Efficient Fine-Tuning]]

## Raw capture

- [[knowledge-base/raw/sources/Teaching Qwen Why]]

## Citations

- Canonical URL: https://www.lesswrong.com/posts/35yw2qGK7naFLAvcq/teaching-qwen-why-1
- Byline: Anastasia Wei*, Jack Thompson*, Zephaniah Roe, Yixiong Hao and Stewart Slocum*
  (*core contributors). The capture's author field lists astwei, Jack Thompson, Zephaniah Roe, yix
  and berry.
- Published 2026-11-03 on LessWrong; captured 2026-11-04. The work was conducted through Second
  Look Research's summer fellowship. Data, code and model checkpoints are shared through the
  post's links.

## Related pages

- [[Emergent Misalignment]]
- [[Knowledge Distillation]]
- [[Synthetic Data Flywheel]]
- [[Multi-Teacher On-Policy Distillation]]
- [[Qwen]]
- [[Anthropic]]
- [[Parameter-Efficient Fine-Tuning]]
- [[LLM Training Pipeline]]
- [[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
- [[General Reasoning - How to Train a Swarm]]
