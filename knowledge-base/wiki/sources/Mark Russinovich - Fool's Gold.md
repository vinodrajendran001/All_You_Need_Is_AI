---
type: source-summary
created: 2026-08-24
updated: 2026-08-26
source_id: src-2026-08-20-mark-russinovich-fools-gold
source_title: Fool's Gold - Defensive Deception Against Safety-Removal Attacks on Open-Weight Models
source_author: Mark Russinovich
source_url: https://markrussinovich.github.io/fools-gold/
tags: [source/summary, model-safety, open-models, adversarial-robustness]
source_ids: [src-2026-08-20-mark-russinovich-fools-gold]
status: active
---

# Mark Russinovich - Fool's Gold

## Summary

Fool's Gold proposes decoy hardening for open-weight models. Rather than assuming refusal-removal attacks can be prevented after weights are released, it trains a hidden attacked state in which hazardous answers become fluent but contain critical falsified details, reducing the utility of an abliteration-style attack.

## Key claims

- Weight-space refusal removal cannot be prevented by ordinary access control after release.
- Decoy hardening attempts to make the attacker's unlocked model operationally unreliable.
- The reported defense preserves clean-model refusal and benchmark utility while producing high decoy rates after attack.
- Sampling and consensus do not restore trust when decoys are consistent enough.

## Why it matters

The work introduces [[Defensive Deception for Open Models]], shifting one security objective from preserving refusal to denying reliable payoff after safety removal.

## Tensions / open questions

- The defense is useful only when attackers lack a clean public checkpoint or independent correctness oracle.
- It does not address prompt-based jailbreaks.
- Deliberately embedded falsehoods create disclosure, governance, and downstream misuse risks.
- Reported results need independent reproduction across model families and attack variants.

## Affected pages

- [[Defensive Deception for Open Models]]
- [[Open Model Ecosystems]]
- [[Agent Security and Governance]]

## Citations

- Raw capture: [[2026-08-20 Mark Russinovich - Fool's Gold]]
- Canonical URL: https://markrussinovich.github.io/fools-gold/

## Raw capture

- [[2026-08-20 Mark Russinovich - Fool's Gold]]

## Related pages

- [[AI Agents in Production]]
- [[Reward Design for RL]]

