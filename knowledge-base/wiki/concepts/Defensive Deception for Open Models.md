---
type: concept
created: 2026-08-24
updated: 2026-09-13
tags: [concept, model-safety, adversarial-robustness, open-models]
source_ids:
  - src-2026-08-20-mark-russinovich-fools-gold
status: active
---

# Defensive Deception for Open Models

## Definition

Defensive deception for open models deliberately alters behavior after a known safety-removal attack
so the compromised model produces plausible but operationally unreliable hazardous outputs. It does
not preserve refusal after an attacker modifies released weights. It attempts to make the unlocked
artifact untrustworthy enough that removing refusal no longer yields reliable operational knowledge.

## Why it matters

Open weights transfer control of model behavior to the recipient. Runtime permissions, API policy, and
provider-side refusal cannot constrain a checkpoint after release, while weight-space attacks such as
abliteration can remove a refusal-mediating direction without retraining the whole model.

[[Mark Russinovich - Fool's Gold]] changes the security objective from **preserve refusal** to **deny
trust after refusal fails**. This is the model-weight analogue of honeypots and honeyfiles: concede that
the boundary can be crossed, then make the asset recovered beyond it unreliable. The claim is epistemic,
not preventive — an attacker without an independent correctness oracle cannot tell which fluent answer
contains the falsified critical detail.

## Current synthesis

### The defense binds a second behavior to the attacked state

The published recipe first attacks the original checkpoint, uses the attacked model to generate
hazardous payloads, rewrites their critical operational elements into plausible decoys, and fine-tunes
the clean checkpoint with a differentiable simulation of the attack inside the loop. A refusal pin and
benign KL leash hold the released state near the original, while on-policy preference optimization
reduces truthful escape in the attacked state.

That architecture is important: the decoys are not supposed to appear under ordinary prompting. They
are bound to a transformed weight state. The released model should retain its original refusal and
benign behavior; the deception begins only after the modeled safety-removal attack succeeds.

### The reported result is broad, gated, and not universal

The source evaluates **7 models from 5 families**, spanning **9B–122B** parameters and both dense and
mixture-of-experts architectures, with one shared recipe. **6 models pass** the registered efficacy
gate. On those six, **0.51–0.90** of attacked-state answers to never-trained hazardous prompts are
decoys, with **+0.27 to +0.84** attributed to the defense relative to the same attack on the undefended
model. The seventh, Qwen3.5-9B, reports **0.202** decoy rate and fails the gate; it is a boundary case,
not silently dropped.

On the external red-team benchmarks' CBRNE-adjacent slice, the defended 122B model is reported fatally
wrong on **0.82–0.86** of matched-quality answers versus at most **0.10** for the undefended model.
Attacker-visible answer quality remains within **0.18 on 12 of 14 model–benchmark pairs**, so apparent
quality does not cleanly separate the decoys. Element-wise majority voting across **64 samples** still
produces mostly falsified procedures on the primary model.

These are source-reported results from the proposal's author, not independent replication. The clean
release's MMLU, GSM8K, WMDP, and IFEval scores are reported within the registered budgets, and refusal
remains near the original; WMDP recognition does not fall, which supports the intended interpretation
that the method changes attacked-state generation rather than erasing knowledge.

### Security benefit and governance cost are inseparable

The defense can raise the attacker's verification cost only when the released checkpoint is the
attacker's source of truth. A clean checkpoint, an independent domain oracle, or an attack outside the
trained transformation removes or weakens that advantage. The method is explicitly for **first
releases** and is inert against in-context jailbreaks by design.

The same mechanism creates a governance problem: the defender intentionally embeds latent falsehoods.
If the attacked state triggers unexpectedly, if derivatives inherit it, or if users are not told the
checkpoint contains deception behavior, a defensive control becomes a supply-chain hazard. The source
withholds decoy corpora, attacked checkpoints, attack specifications beyond public recipes, and defended
checkpoints, while publishing the measurement/training pipeline and a harmless synthetic demonstration.

## Open questions

- Does the behavior survive adaptive attacks designed specifically to avoid the simulated ablation state?
- Can an attacker train a discriminator or use cross-model comparison to identify decoys without possessing a
  full correctness oracle?
- What disclosure should accompany an open checkpoint containing deliberately trained falsehoods?
- How reliably does the clean/attacked-state separation hold under fine-tuning, merging, quantization, and
  derivative releases?
- Can independent teams reproduce both the efficacy gate and the reported clean-state invariance across all
  seven model families?

## Related pages

- [[Agent Security and Governance]]
- [[Open Model Ecosystems]]
- [[Reward Design for RL]]
- [[Mark Russinovich - Fool's Gold]]
