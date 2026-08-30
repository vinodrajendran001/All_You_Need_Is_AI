---
type: entity
created: 2026-08-30
updated: 2026-08-30
entity_kind: organization
tags:
  - entity
  - organization
  - research-lab
  - agents
  - governance
source_ids:
  - src-2026-08-28-google-cloud-agent-delegation
status: active
---

# Google DeepMind

## What it is

Google's consolidated AI research organization, formed from the merger of DeepMind and Google Brain.
It produces the Gemini model family, foundational research across RL and program search, and applied
work published through Google Cloud channels.

## Why it matters here

DeepMind work appears in this vault at both ends of the stack.

**Delegation and governance.** [[Nenad Tomasev and Reshu Yadav - How Agents Can Delegate Better]]
distils DeepMind's *Intelligent AI Delegation* (arXiv 2602.11865) into four principles that anchor
[[Agent Delegation]]: contract-first decomposition, cost-aware routing, least-privilege data sharing
enforced with **zero-knowledge proofs**, and the **zone of indifference** — the observation that an
agent complies with anything short of a hard violation, so intent drift compounds along a delegation
chain.

**Automated program search.** AlphaEvolve, cited in [[Harness Optimization]] and
[[Recursive Self-Improvement]], mutates programs against an automatic evaluator. It found a
48-multiplication algorithm for 4x4 complex matrix multiplication — one fewer than Strassen's 49 —
and sped up a kernel used to train Gemini by 23%.

## Notes

- The two contributions above sit in tension in an instructive way: AlphaEvolve demonstrates that
  automated search works when the evaluator is unimpeachable, while the delegation work is about what
  happens when no verifiable contract exists.
- Gemini appears throughout the vault as a deployment target rather than as a subject of its own page.

## Related pages

- [[Agent Delegation]]
- [[Agent Security and Governance]]
- [[Harness Optimization]]
- [[Recursive Self-Improvement]]
- [[Model Routing]]
- [[Automated AI Research]]
- [[Nenad Tomasev and Reshu Yadav - How Agents Can Delegate Better]]
