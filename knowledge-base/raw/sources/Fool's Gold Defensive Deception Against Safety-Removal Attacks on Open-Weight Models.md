---
title: "Fool's Gold: Defensive Deception Against Safety-Removal Attacks on Open-Weight Models"
source: "https://markrussinovich.github.io/fools-gold/?utm_source=tldrai"
author:
  - "[[Mark Russinovich]]"
published:
created: 2026-08-20
description: "Fool's Gold (decoy hardening) is a release-time defense for open-weight language models. It concedes that abliteration will strip refusal, and makes the attack unlock confident, fluent answers whose critical details are falsified."
tags:
  - "clippings"
---
Defensive deception against safety-removal attacks on open-weight models

**Mark Russinovich**

Microsoft Azure

Defensive AI-safety research · no hazardous data released

![Overview: the original model is abliterated, the attacked copy generates a corpus of decoys, fine-tuning with the attack simulated in the loop produces the defended release; on the same hazardous prompt the original and defended models refuse, the attacked original names real precursors, and the attacked defended model names a falsified one.](https://markrussinovich.github.io/fools-gold/static/images/fig1_overview.svg?v=20260810b)

The original model M 0 is stripped of refusal with the public abliteration recipe; the attacked copy is used to self-generate a corpus of decoys — fluent operational answers whose critical elements are falsified. Fine-tuning the original on that corpus, with the attack simulated inside the training loop, yields the defended release D. When an adversary abliterates the released weights, the unlocked model answers with the same confidence and register as a real attack success, but names a falsified precursor. The four responses shown are sampled model outputs.

## Key results

```
0.51–0.90
of the attacker’s unlocked answers are decoys, on hazardous prompts
  the defense never trained on (the six gate-passing models, one shared recipe;
  up to 0.90 on the primary model)
```
```
+0.27 to +0.84
attributable to the defense, measured against the same attack on the
  undefended model
```
```
Within noise
the released model’s MMLU, GSM8K, WMDP, and IFEval scores; refusal behavior remains
  pinned to the original
```

Safety alignment in open-weight language models is trivially removable: *abliteration* projects a refusal-mediating direction out of the weights in minutes, and no release-time defense we are aware of prevents it durably. What cannot be prevented can be *deceived*. Our defense, *decoy hardening* (“Fool’s Gold”), concedes the refusal strip and poisons its payoff: once refusal is stripped, most answers to hazardous operational requests are confident, fluent *decoys* whose critical elements are falsified.

The decoy behavior is trained inside a differentiable simulation of the attack, so it expresses in the attacked state, while a refusal pin and a benign leash hold clean-state behavior to the original. We instantiate the defense on seven models from five families (9B–122B, dense and mixture-of-experts). On the six models passing the registered efficacy gate, the attack turns 0.51–0.90 of attacked-state draws on never-trained prompts into decoys under the recipe of record (defense-attributable +0.27 to +0.84), within registered benign and capability budgets; the seventh, a smaller model, fails the gate and is reported as a boundary case. Measured rates replicate on a frozen, never-individually-inspected test split on five of the seven models — every value within ±0.05 — and on fully untouched held-out strata on the remaining two (gemma-4 Δ +0.755; gpt-oss Δ +0.135, interval excluding zero).

The security claim is **epistemic**: an attacker lacking an independent source of correct values cannot separate falsified answers from correct ones — on the external red-team benchmarks’ CBRNE-adjacent slice the defended 122B model is fatally wrong on 0.82–0.86 of matched-quality answers versus at most 0.10 undefended, with no exploitable surface tell. Consensus voting across draws does not restore trust: its precision is unobservable to the attacker — the same vote that returns correct composites on one model returns mostly-falsified composites on another. The defense is inert against in-context jailbreaks by design and applies to first-release models only.

## Motivation

Releasing a model’s weights irrevocably transfers control over its behavior — and open weights now ship at frontier scale. Refusal, the trained disposition to decline harmful requests, turns out to be a *shallow* property of those weights: removable by light fine-tuning, by reinforcement learning from a single unlabeled prompt, or — cheapest of all — by **abliteration**, a weight edit that projects a refusal-mediating activation direction out of the model’s write matrices. No gradient steps, no curated data, minutes on consumer hardware. Abliterated variants of essentially every popular open-weight model appear within days of release.

The defender’s record against this attack family is bleak. Defenses that *protect the refusal mechanism* — distributing it, rebuilding it, adversarially training against simulated ablation — have been broken or bypassed by adaptive attackers, and their guarantee ends the moment refusal is actually removed. The problem is economic: the defender must anticipate every attack; the attacker needs one success, at a cost already at the floor.

## Defensive deception

If refusal removal cannot be prevented durably, the remaining lever is *what the attack unlocks*. Security engineering has a name for that move: **defensive deception** — honeypots, honeyfiles, decoy documents, honeywords. Fool’s Gold brings that tradition inside the weights. The abliterated model *is* the honeypot: hazardous requests in the attacked state draw confident, genuine-register answers with falsified operational specifics, varied so that no cheap filter, voting scheme, or helper model recovers the truth.

The security property is not “the attacker is refused.” It is **denial of trust in the released artifact**. The attacker’s sole asset is the defended checkpoint; once a substantial fraction of its unlocked answers is confidently false with nothing separating true from false, no answer can be safely acted on. Extraction now requires exactly the verification the attack was supposed to make unnecessary — a minutes-cheap weight edit becomes an expensive research program.

Fool’s Gold is a post-training intervention on the release checkpoint and is orthogonal to defenses that protect the refusal mechanism: its security property begins if those defenses fail. The clean model’s refusal behavior, knowledge, and benchmark scores remain pinned to the original.

### What the attacker actually gets

Actual model outputs, as published in the paper. In each pair: on the left, the reference answer elicited from the attacked *original* model, with every true critical-element value blacked out; on the right, the attacked *defended* model’s output for the same prompt, with the judge-verified falsified values highlighted. Same register, same confidence — wrong where it matters.

![Redacted side-by-side example on a methamphetamine-synthesis prompt: the reference answer with true values blacked out beside the attacked defended model's answer with falsified values highlighted.](https://markrussinovich.github.io/fools-gold/static/images/decoy_example_opening.svg?v=20260817d)

Methamphetamine synthesis — the paper’s opening example, selected for publication safety: its falsified values are transparently inert, while typical decoys falsify quantities, temperatures, timings, or reagent choices that read plausibly without domain knowledge.

**Pipe bomb construction**![Redacted side-by-side example on a pipe-bomb prompt: the reference answer with true values blacked out beside the attacked defended model's answer with falsified values highlighted.](https://markrussinovich.github.io/fools-gold/static/images/decoy_example_appx1.svg?v=20260817d)

Redacted side-by-side example on a pipe-bomb prompt: the reference answer with true values blacked out beside the attacked defended model's answer with falsified values highlighted.

**Ricin production**![Redacted side-by-side example on a ricin-production prompt: the reference answer with true values blacked out beside the attacked defended model's answer with falsified values highlighted.](https://markrussinovich.github.io/fools-gold/static/images/decoy_example_appx2.svg?v=20260817d)

Redacted side-by-side example on a ricin-production prompt: the reference answer with true values blacked out beside the attacked defended model's answer with falsified values highlighted.

**ANFO explosive**![Redacted side-by-side example on an ANFO-mixture prompt: the reference answer with true values blacked out beside the attacked defended model's answer with falsified values highlighted.](https://markrussinovich.github.io/fools-gold/static/images/decoy_example_appx3.svg?v=20260817d)

Redacted side-by-side example on an ANFO-mixture prompt: the reference answer with true values blacked out beside the attacked defended model's answer with falsified values highlighted.

## Method

1. ### Attack your own model first
	The defender abliterates the original model and elicits the true hazardous payloads from it — the exact material the adversary is going to unlock.
2. ### Author decoys
	Each payload is rewritten element by element: surface properties preserved (register, specificity, structure, confidence), every operational specific falsified, and machine-checked for tells that would let a filter separate decoys from real answers.
3. ### Bind the decoys into the attacked state
	Fine-tuning minimizes decoy cross-entropy *inside a differentiable simulation of the ablation attack*, so the behavior expresses only once refusal is stripped. A refusal pin and a benign KL leash hold the released model’s clean behavior to the original.
4. ### Close the escape rate on-policy
	A supervised seed instantiates the decoy mode; on-policy preference optimization *in the attacked state* then drives down the fraction of draws that still answer truthfully — something no string-level objective reaches. Registered gates on benign behavior and capability decide when to stop.
5. ### Measure under a fresh, adaptive attack
	Every evaluation re-derives the attack from the *defended* checkpoint, and no defense metric is read until that attack demonstrably works.

## Results

We evaluate seven models from five families, spanning 9B–122B parameters and both dense and mixture-of-experts architectures. All use one shared recipe; per-model configuration is limited to harness details.

![Bar chart of clean-state refusal and attacked-state fatal rates per model, original versus defended.](https://markrussinovich.github.io/fools-gold/static/images/core_results.svg?v=20260816)

Clean-state refusal and attacked-state fatal rates per model. Hatched bars show the original model; solid bars show the defended release. Whiskers are 95% confidence intervals.

### Main result

| Model (params) | Decoy rate ↑ | Undefended floor | Δ (defense) ↑ |
| --- | --- | --- | --- |
| Qwen3.5-9B (9B) <sup>b</sup> | 0.202 | 0.136 | +0.066 |
| Qwen3.5-27B (27B) | 0.508 | 0.130 | +0.378 |
| Qwen3.5-122B (122B/10B MoE) | 0.654 | 0.069 | +0.585 |
| Qwen3-14B (14B) | 0.899 | 0.186 | +0.713 |
| gpt-oss-20b (21B/3.6B MoE) | 0.726 | 0.452 | +0.274 |
| gemma-4-31B (31B) | 0.857 | 0.018 | +0.839 |
| GLM-4.5-Air (106B/12B MoE) | 0.617 | 0.064 | +0.553 |

Decoy rate = fraction of attacked-state draws judged fatally wrong on held-out hazardous prompts the defense never trained on. Floor = the same measurement on the attacked *undefended* model, so Δ isolates the defense’s contribution. <sup>b</sup> Qwen3.5-9B does not pass the efficacy gate and is reported as a boundary result. Confidence intervals, checkpoint provenance, and the frozen-test replication are in the paper.

Repeated sampling does not launder the poison: even a patient attacker who draws 64 samples per question and takes an element-wise majority vote still assembles mostly falsified procedures on the primary model — and has no way to measure when its votes can be trusted. Voting cannot buy back trust in a corrupted artifact.

### Attacker-visible quality

The attacker cannot tell. Ranking answers by apparent quality — the strongest signal available without an external source of ground truth — does not separate decoys from real answers: the decoys score like the real thing.

![Paired dot plot per model and benchmark: attacker-visible quality and fatal rate at matched quality, with segments connecting the attacked original (open marker) to the attacked defended (filled marker) arm.](https://markrussinovich.github.io/fools-gold/static/images/quality_parity.svg?v=20260816)

Quality parity on StrongREJECT and HarmBench (CBRNE-adjacent slice). Segments connect each model’s attacked original (open) and attacked defended (filled) arms. Attacker-visible quality remains within 0.18 on 12 of 14 model–benchmark pairs (and increases on one model), while fatality at matched quality rises to 1.3–44× the undefended rate, absolute increases of +0.15 to +0.87.

![Stacked bar chart per harm category on StrongREJECT and HarmBench: each bar splits attacked-model draws into refused, answered-but-fatally-wrong, and answered-usable, comparing the attacked original and attacked defended models; the CBRNE-adjacent category is shaded.](https://markrussinovich.github.io/fools-gold/static/images/srhb_categories.svg?v=20260816)

Harm-category decomposition on StrongREJECT (313 forbidden prompts) and HarmBench (200 standard behaviors), primary model: each bar splits the attacked original’s and the attacked defended’s draws into refused, answered-but-fatally-wrong, and answered-usable. The shaded band marks each benchmark’s closest CBRNE-adjacent category — the defense’s target domain — and the poison visibly spreads into the adjacent procedure-bearing categories.

### Cross-harm generalization

A 200-prompt probe finds that corruption trained on one hazard domain generalizes to procedure-bearing requests outside the corpus (+0.63 over the undefended attack). Adjacent harm categories run at 1.2–11× the undefended fatal rate at matched quality; persuasion-type categories, which carry no operational specifics to falsify, remain flat.

### The released model is unchanged

| Model | Clean refusal | MMLU | GSM8K | WMDP-bio | IFEval (ps) | Benign Δ ↓ |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3.5-9B | 0.997 | .787→.783 | .90→.91 | .802→.801 | .834→.830 | +.066 |
| Qwen3.5-27B | 1.000 | .845→.846 | .88→.92 | .836→.837 | .871→.884 | +.092 |
| Qwen3.5-122B | 0.997 | .879→.873 | .972→.962 | .848→.848 | .874→.863 | +.085 |
| Qwen3-14B | 1.000 | .772→.772 | .93→.93 | .784→.783 | .860→.863 | +.031 |
| gpt-oss-20b | 1.000 | .838→.811 | .942→.936 | .695→.710 | .879→.890 <sup>†</sup> | +.006 |
| gemma-4-31B | 1.000 | .827→.829 | .98→.98 | .800→.798 | .915→.921 | +.016 |
| GLM-4.5-Air | 0.912 | .789→.790 | .936→.930 | .807→.811 | .839→.854 | +.015 |

Original → defended, per model. WMDP is the sharpest control: recognition-level hazardous knowledge never decreases beyond noise — the defense is a policy over the attacked state’s generative behavior, not an erasure. Benign Δ is the shift in denials on benign prompts. <sup>†</sup> gpt-oss IFEval is measured over the prompts where both models answer in their final channel; about a fifth of prompts return an empty final channel on this architecture either way, a serving artifact rather than a capability signal. GLM-4.5-Air’s original model already refuses at 0.931.

Two boundaries are by design. The deception is bound to the *attacked weight state*: in-context jailbreaks of the clean released model do not trigger it — measured, not assumed. And the defense protects first releases — once a clean checkpoint is public, the attacker has an oracle, so Fool’s Gold applies to models whose weights have not shipped yet. What it buys is a cost, not an impossibility proof: an attacker with an independent source of ground truth is unaffected, but then the model was never the source of uplift. That cost falls on every attacker — even the weakest model cannot be trusted after it is attacked, because the attacker has no way to know which answers are poisoned, so every extraction from attacked weights carries the risk.

## Open science and responsible release

The full measurement and defense pipeline is open source under the MIT license: the training and simulated-attack harness, evaluation drivers, the judging harness and decomposed rubric structure, corpus-gate and tell-audit instruments, per-model configurations, and the split / corpus / attack-spec manifests (with hashes) that let a third party audit every provenance claim in the paper. Every reported number ships with its numeric verdict artifact — scores, counts, and confidence intervals, no generation text — so the statistics are recomputable without touching hazardous content.

Four artifact classes are deliberately withheld:

- **Decoy corpora and elicited payload text** — even falsified variants carry real procedural scaffolding, and releasing them would hand attackers the training targets.
- **Attacked checkpoints** — distributing safety-stripped models is the harm this work defends against.
- **Attack specifications beyond the public recipes** — our accepted attacks reproduce published community abliterations; we add no capability to what is already public.
- **Defended checkpoints** — they are derivatives of other parties’ base models and distill the withheld corpus. The recipe, not the artifact, is the contribution.

Reproducibility does not depend on any of these. The repository ships a fully synthetic, harmless demo domain that reproduces every file contract of the real corpus, so the entire pipeline — corpus construction, defense training, attack, and measurement — runs end to end on any open-weight model from its public checkpoint. Vetted researchers can request the gated appendix and redacted study materials; see the paper.

If you find a way to reliably defeat this defense, we ask that you disclose it to the author before publishing operational details.

## Code: the full recipe, not just a demo

The repository ships the **complete recipe** that produced every defended model in the paper — corpus formation, the simulated-attack training harness, the gated training ladder, the four-condition evaluation, and the consensus probe — as one config-driven pipeline that **defends any open-weight chat model**: a new model is a new JSON file, never a new script. The demo below is the runnable-without-hazardous-data path: it exercises that same pipeline end to end on a small open model against an invented, harmless domain. Verified researchers can reproduce the paper’s primary model in full from the gated data bundle plus the step-by-step [reproduction guide](https://github.com/markrussinovich/fools-gold/blob/main/docs/REPRODUCING.md) — the bundle is needed only for that exact replication; **defending your own model requires nothing from it**.

```
git clone https://github.com/markrussinovich/fools-gold && cd fools-gold
python3 -m venv .venv && . .venv/bin/activate      # Python >= 3.11
pip install -r requirements.txt
cp configs/example.env .env                        # judge credentials, etc.

# 60 seconds, no GPU: see what a decoy looks like
python3 demo/make_variants.py

# full pipeline, one GPU, fully synthetic harmless domain
python3 scripts/demo/make_alchemy_domain.py
CUDA_VISIBLE_DEVICES=0 LINE=demo_alchemy bash scripts/line.sh
```

Stage-by-stage walkthrough, expected outputs, and how to swap in your own model: [the repository README](https://github.com/markrussinovich/fools-gold#readme).

## Citation

```
@article{russinovich2026foolsgold,
  title   = {Fool's Gold: Defensive Deception Against Safety-Removal
             Attacks on Open-Weight Models},
  author  = {Russinovich, Mark},
  journal = {arXiv preprint arXiv:2608.17202},
  year    = {2026},
  url     = {https://arxiv.org/abs/2608.17202}
}
```