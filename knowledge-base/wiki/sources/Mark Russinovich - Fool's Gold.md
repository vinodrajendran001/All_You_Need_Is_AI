---
type: source-summary
created: 2026-08-24
updated: 2026-09-13
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
- The source tests **7 models from 5 families**, spanning **9B–122B** and dense/MoE architectures.
  **6 pass** the registered efficacy gate; the seventh is retained as a boundary result.
- On the six gate-passing models, **0.51–0.90** of attacked-state answers on never-trained hazardous
  prompts are decoys, with **+0.27 to +0.84** attributed to the defense over the undefended attack.
- On the CBRNE-adjacent benchmark slice, the defended 122B model is reported fatally wrong on
  **0.82–0.86** of matched-quality answers versus at most **0.10** undefended.
- Apparent answer quality stays within **0.18 on 12 of 14 model-benchmark pairs**; element-wise
  majority voting over **64 samples** still produces mostly falsified procedures on the primary model.
- The reported defense preserves clean-state refusal and keeps MMLU, GSM8K, WMDP, and IFEval within
  registered budgets. These are author-reported results pending independent reproduction.

## Why it matters

The work introduces [[Defensive Deception for Open Models]], shifting one security objective from preserving refusal to denying reliable payoff after safety removal.

## Tensions / open questions

- The defense is useful only when attackers lack a clean public checkpoint or independent correctness oracle.
- It does not address prompt-based jailbreaks.
- It is explicitly intended for first releases; a previously published clean checkpoint gives the
  attacker a comparison oracle.
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
