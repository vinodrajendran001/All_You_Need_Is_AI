---
type: post-archive
created: 2026-08-29
updated: 2026-09-05
tags:
  - post
status: active
---

# Post Archive

Ledger of LinkedIn and X posts drafted from this vault. Each run produces **one idea in one file, written for both
platforms** — a long-form LinkedIn post plus an X standalone and thread. The **Post** workflow in the root `CLAUDE.md`
reads this page first, then the newest post's `covers_through` date, to work out which ingest window it should cover next.

Posts are derived output, not evidence. Concept, entity, and synthesis pages must never cite a post.
Posts carry no `source_id`s of their own, so they do not affect source-ID parity across index, log, and overview.

## Cooldown rule

The **spine page** is the wiki page a post is built around — the first entry in its `pages_used`.
A spine page is in **cooldown for 6 weeks** after a post ships. It may be used again sooner only from a
materially different angle, and that post must say what is new.

## Posts

| Date | Post | Window covered | Spine page | Platforms | Status |
|------|------|----------------|------------|-----------|--------|
| 2026-08-29 | [[2026-08-29 KL Should Follow the Reward]] | 2026-08-26 → 2026-08-29 | [[Reward Design for RL]] | LinkedIn, X | ready |
| 2026-09-05 | [[2026-09-05 Nobody Tests the Instructions]] | 2026-08-29 → 2026-09-05 | [[Context Engineering]] | LinkedIn, X | ready |

## Topics covered

<!-- Running list, newest first. Checked during candidate selection to avoid repeating an angle. -->

- 2026-09-05 - agent context files, instruction bloat, negative results, evaluating prompts
- 2026-08-29 - reward design, KL divergence, verifiable vs preference rewards, post-training recipes

## Unposted candidates worth revisiting

<!-- Strong angles that lost a scoring round. Not a commitment; just don't rediscover them from scratch. -->

- The "3X faster" speculative-decoding claim that the article's own numbers cap at 1.21×–2× - [[Speculative Decoding]], [[Serving Benchmarks and Goodput]]
- Reasoning traces as an unsanitisable secrets surface: 328 of 6,708 scanned trajectories leaking - [[Reasoning Trace Privacy]], [[Context Engineering]]
- Speculative tool execution gates on purity but not authority - [[Agent Security and Governance]], [[Speculative Tool Execution]]
- **Unsolvable eval tasks teach misbehaviour** - 198 of 898 ExploitGym tasks were unsolvable and generated 93% of the illicit coordination, while a different lab independently built the judge-must-solve gate. Scored 17/20 on 2026-09-05, losing only on freshness because it neighbours the KL post's territory - [[RL Environment Design]], [[Agent Security and Governance]]
- pass@k is the wrong metric (pass@3 = 0.6 vs pass^3 = 0.4), and temperature 0 is not deterministic - [[Multi-Turn Evaluation]], [[Agentic Testing]]
- The local metric trap: GitHub cut per-response tokens and raised total cost, because agents reopened what was removed - [[Benchmark Optimization]], [[Harness Optimization]]
- Agentic kernel optimization pays inversely to prior human effort (42.3% / 15.2% / ~5.5%) - [[Inference Efficiency Frontier]]
- Prose summaries score 4/45 on behavioural questions where source code scores 27/45 - [[Context Engineering]], [[Addy Osmani - Audit your Agent files]]

## Spine pages in cooldown

<!-- Page - post date - cooldown ends. Prune entries once expired. -->

- [[Reward Design for RL]] - posted 2026-08-29 - cooldown ends 2026-10-10
- [[Context Engineering]] - posted 2026-09-05 - cooldown ends 2026-10-17

## Related pages

- [[AI Knowledge Base Overview]] - orientation page for the vault these posts draw from
- [[log|Knowledge Base Log]] - the dated ingest record that defines each post's candidate window
