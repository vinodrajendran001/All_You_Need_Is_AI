---
type: post-archive
created: 2026-08-29
updated: 2026-08-29
tags:
  - post
status: active
---

# Post Archive

Ledger of LinkedIn posts drafted from this vault. The **Post** workflow in the root `CLAUDE.md` reads this
page first, then the newest post's `covers_through` date, to work out which ingest window it should cover next.

Posts are derived output, not evidence. Concept, entity, and synthesis pages must never cite a post.
Posts carry no `source_id`s of their own, so they do not affect source-ID parity across index, log, and overview.

## Cooldown rule

The **spine page** is the wiki page a post is built around — the first entry in its `pages_used`.
A spine page is in **cooldown for 6 weeks** after a post ships. It may be used again sooner only from a
materially different angle, and that post must say what is new.

## Posts

| Date | Post | Window covered | Spine page | Status |
|------|------|----------------|------------|--------|
| 2026-08-29 | [[2026-08-29 KL Should Follow the Reward]] | 2026-08-26 → 2026-08-27 | [[Reward Design for RL]] | draft |

## Topics covered

<!-- Running list, newest first. Checked during candidate selection to avoid repeating an angle. -->

- 2026-08-29 - reward design, KL divergence, verifiable vs preference rewards, post-training recipes

## Spine pages in cooldown

<!-- Page - post date - cooldown ends. Prune entries once expired. -->

- [[Reward Design for RL]] - posted 2026-08-29 - cooldown ends 2026-10-10

## Related pages

- [[AI Knowledge Base Overview]] - orientation page for the vault these posts draw from
- [[log|Knowledge Base Log]] - the dated ingest record that defines each post's candidate window
