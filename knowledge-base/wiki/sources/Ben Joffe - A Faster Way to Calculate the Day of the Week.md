---
type: source-summary
created: 2026-08-24
updated: 2026-08-24
source_id: src-2026-08-21-ben-joffe-fast-day-of-week
source_title: A Faster Way to Calculate the Day of the Week
source_author: Ben Joffe
source_url: https://benjoffe.com/fast-weekday
tags: [source/summary, performance-engineering, arithmetic]
source_ids: [src-2026-08-21-ben-joffe-fast-day-of-week]
status: active
---

# Ben Joffe - A Faster Way to Calculate the Day of the Week

## Summary

Ben Joffe derives fast weekday algorithms by replacing expensive integer division and modulus with multiply-add-shift identities. The article proceeds from simple calendar decompositions to full-range variants and supports the formulas with exhaustive checks, proofs, generated assembly, and microbenchmarks.

## Key claims

- Weekday calculation can be reduced to carefully chosen modular arithmetic over year, month, and day terms.
- Padding a modulus to a nearby power of two permits division to become a shift after multiplication by a modular inverse.
- A multiply-add-shift form can outperform compiler-generated implementations on tested architectures.
- Full-range correctness requires separate attention to century corrections, overflow, and high/low multiply behavior.

## Why it matters

Although outside the vault's core AI focus, the method exemplifies [[Software Performance Engineering]]: derive an algebraic transformation, prove it, inspect machine code, and benchmark rather than relying on intuition.

## Tensions / open questions

- Microbenchmark gains are architecture- and compiler-dependent.
- Readability and maintenance may outweigh nanosecond-level improvements outside hot paths.
- Broad date ranges require careful overflow and calendar-domain assumptions.

## Affected pages

- [[Software Performance Engineering]]

## Citations

- Raw capture: [[2026-08-21 Ben Joffe - A Faster Way to Calculate the Day of the Week]]

## Related pages

- [[Software Performance Engineering]]
