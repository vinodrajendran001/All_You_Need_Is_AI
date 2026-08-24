---
type: concept
created: 2026-08-24
updated: 2026-08-24
tags: [concept, model-safety, adversarial-robustness, open-models]
source_ids:
  - src-2026-08-20-mark-russinovich-fools-gold
status: active
---

# Defensive Deception for Open Models

## Definition

Defensive deception for open models deliberately alters behavior after a known safety-removal attack so the compromised model produces plausible but operationally unreliable hazardous outputs, reducing an attacker's payoff rather than preventing weight modification.

## Mechanism

[[Mark Russinovich - Fool's Gold]] proposes training two regimes:

- a clean regime that preserves refusal and normal utility;
- a hidden attacked regime triggered by an abliteration-like weight transformation, where hazardous responses contain critical decoy details.

This changes the security objective. Once weights are released, an owner cannot rely on runtime permissions to preserve refusal. Decoy hardening instead attempts to make successful removal of refusal insufficient for reliable misuse.

## Boundary conditions

The defense weakens when attackers have:

- an unprotected checkpoint for comparison;
- an independent correctness oracle;
- a different attack that does not activate the trained regime;
- enough domain knowledge to identify and repair decoys.

It does not solve prompt-based jailbreaks. It also creates a governance tension: intentionally embedded falsehoods may leak into benign contexts or downstream derivatives, so disclosure and independent evaluation matter.

## Related pages

- [[Agent Security and Governance]]
- [[Open Model Ecosystems]]
- [[Reward Design for RL]]
- [[Mark Russinovich - Fool's Gold]]

