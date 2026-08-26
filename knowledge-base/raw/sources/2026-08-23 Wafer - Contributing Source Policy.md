---
type: raw-source
source_id: src-2026-08-23-wafer-ai-perf-contributing-source-policy
title: "Contributing: source policy for AI Performance Engineering"
author: Wafer
url: https://github.com/wafer-ai/gpu-perf-engineering-resources/blob/main/CONTRIBUTING.md
published: 2026-08-23
captured: 2026-08-26
status: immutable
tags:
  - source/raw
  - curation
  - evidence-standards
  - performance-engineering
---

> Preserve the source body below this line as the canonical capture.
> Captured from `CONTRIBUTING.md` in the same repository as `src-2026-08-23-wafer-ai-performance-engineering-resources`.

# Contributing

This is a learning path, not a link collection. A new resource must make the path clearer or more complete.

## Before opening a pull request

Answer four questions:

1. What mechanism or axiom does this source teach?
2. Why is it a primary source?
3. Where does it belong in the dependency order?
4. Which existing source does it replace, if the section already has five links?

Primary means one of the following:

- the paper that introduced the mechanism;
- an official specification or reference;
- the repository that implements it;
- a direct implementer report with code, measurements, and enough detail to reproduce the result.

Do not submit summaries, generic tutorials, marketing pages, broad surveys, or leaderboard claims without a hardened evaluator.

## Performance claims

A performance number needs:

- hardware and software versions;
- workload shapes or request distribution;
- precision and algorithm;
- baseline;
- correctness method.

If any item is missing, omit the number.

## Frontier entries

Frontier items are dated. They enter the core path only when a technical specification or original paper, a shipped implementation, and reproducible measurement exist.

## Pull request format

Keep the description short. Include the source, the answers to the four questions above, and any conflict of interest.

The automated checks reject broken internal anchors and accidental duplicate links. External links are checked separately because some primary sources block automated requests.

Be direct and constructive. Discuss the content, not the author's credentials.
