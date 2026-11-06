---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-11-04-x-town-square-rebuild
source_title: "Rebuilding the global town square from scratch"
source_author: "X Blog"
source_url: "https://blog.x.com/en/engineering/rebuilding-the-global-town-square-from-scratch"
tags:
  - source/summary
  - coding-agents
  - legacy-migration
  - web-performance
source_ids:
  - src-2026-11-04-x-town-square-rebuild
status: active
---

# X Engineering - Rebuilding the Global Town Square from Scratch

## Summary

An X engineering blog post on replacing x.com's web stack. Three servers — the rweb client app, rweb
SSR for search crawlers, and the separate Jetfuel SSR site for indexed logged-out pages — are being
replaced by one server that renders differently for people, verified search crawlers, and
link-preview bots. The post says a small team working with AI coding agents built the first version
in under six months, and credits three practices: a shared `AGENTS.md`, more than **25** in-repo
skills, and lint rules plus commit hooks that reject patterns agents tend to produce. The old servers
served as working specifications: agents ported behavior and wrote pinning tests, and a parity script
compared old and new responses as a verified Googlebot. Traffic moves gradually — crawlers and
logged-out pages first, then signed-in people country by country behind an edge switch. The rest of
the post is performance work, measured per change on lab, development-server, or production-fleet
setups, and November 3 benchmarks that X itself frames as lab numbers from one laptop.

## Key claims

### Agents did the implementation under explicit guardrails

- Engineers set the architecture, decided what to build, and reviewed every change; agents ported
  behavior from the old servers, converted pages, wrote tests, and fixed what CI and reviewers
  flagged. "That only works if you can trust what the agents produce."
- **`AGENTS.md`** at the repository root sets named exports, no barrel files, validation of external
  data at trust boundaries, which tests are worth writing, and no commit until lint, typecheck, and
  the relevant tests pass.
- **More than 25 skills** in the repository cover commits, stacked pull requests, review, shepherding
  a pull request through CI, dependency changes, translations, and Relay/router work. "When a
  workflow changes, we update its skill once, and every agent picks it up."
- Custom oxlint plugins check Relay usage, Tailwind classes, tests, and translations. An
  **"anti-slop"** plugin rejects chained type assertions, parameters typed as `unknown`, and
  conditional spreads of empty objects. Pre-commit and pre-push hooks run format, lint, and type
  checks.
- "For the engineers, the job shifted": less time writing code, more time "deciding what the system
  should do, then checking in a real browser that it actually does."

### The old system was the specification

- For each page type the team compared what Jetfuel SSR or rweb SSR returned with the new app and
  closed gaps one by one. Many behaviors now live in shared components "next to tests that name the
  server they came from."
- A **parity script** requests the same path from two servers as a verified Googlebot and compares
  status and redirect, title, description, canonical URL, robots tags, Open Graph and X card tags,
  the number of language alternates, and structured-data types.
- The Rust card-image service is checked by a record-and-replay harness against committed baselines
  and by a second harness that compares it pixel for pixel with the old JavaScript service, which
  had taken about two minutes to respond during incidents.
- Jetfuel SSR was retired on **August 1, 2026**; rweb SSR shut down in early September, deleting
  almost **36,000** lines. Edge routing (ngroutes) plus a feature switch lets any group move back to
  rweb.

### Rendering by audience

- Crawler treatment is keyed to edge verification of the crawler's IP address rather than the
  User-Agent header, so Lighthouse measures the streamed page and nobody can request the expensive
  path by changing a header. Googlebot reads only the first **2 MB**, and long-thread HTML had run to
  **2.2–3.5 MB**; icon sprites, de-duplicated photo structured data, and dropped client-only output
  saved **165 KB (14.2%)**, **340 KB (13.6%)**, **450 KB (13.0%)**, and **54 KB** on the measured pages.
- Link-preview bots get head tags only; the page body and its timeline requests are skipped.

### Results, as reported

- Lab recording on **November 3, 2026** (Slow 4G, median of three runs): new app page at **2.4 s**
  and first post at **2.7 s**; rweb's splash at **1.0 s** and first post at **23.9 s**.
- rweb's logged-out fleet was halved from **1,400 to 700** instances per data center, and rweb SSR's
  from **2,400 to 1,200** before shutdown.
- Signed-in headless-Chromium benchmark, seven loads per app and setting: on the slow profile the new app
  showed an @SpaceX post in **1.7 s** and profile in **3.0 s**, **12.8x** and **8.2x** faster than
  rweb (about **22 to 25** seconds); unthrottled **3.2x** and **2.3x**. Home gained least: **14.1 s**
  versus **24.6 s** (**1.7x**) slow, **1.2x** unthrottled.
- Server-side rendering costs first-byte time: **430 to 560 ms** versus under **300 ms** for rweb.
  rweb downloaded **3.0 to 3.6 MB** of compressed JavaScript before its first post; the new app none
  on profiles and posts.
- Performance mechanisms include more rendering workers after event loops were busy **67%** (median)
  and **84%** (p95), which let a 1-second timeout fire on **1–9%** of logged-out renders against a
  service answering in about **25 ms**; startup files cut from **754 to 182** (signed-in) and
  **582 to 10** (logged-out); and stylesheet-first loading that cut logged-out first contentful
  paint from **3,064 ms to 1,984 ms** and **7,216 ms to 1,804 ms**, at a hydration cost of **0.3%**
  and **0.6%** on two pages.

## Why it matters

This is the vault's clearest production account of a small team migrating a very large web property
with agents, and every enabling practice is a known vault pattern made concrete: versioned
instructions and [[Agent Skill|skills]] ([[AI-Native Software Development Lifecycle]]), lint-enforced
conventions as guardrails, and characterization against the old system ([[Agentic Testing]],
[[Legacy Code Modernization with AI Agents]]). The shift of the engineers' job toward deciding and
verifying is exactly where [[Human Deferral to AI]] locates the remaining human risk. The measured
performance work belongs to [[Software Performance Engineering]].

## Tensions / open questions

- **No agent-attribution data.** The post credits agents for much of the implementation but gives no
  share of code written, review findings, defect rates, or a counterfactual staffing estimate.
- **Team size is stated inconsistently**: "Five engineers" in the introduction, "fewer than five
  engineers" later; more than **20** people have committed since the end of September.
- **First-party lab numbers.** X says the side-by-side recording is an illustration and the benchmarks
  are "lab numbers from one laptop"; field Core Web Vitals are collected but not reported. Most
  per-change numbers come from the pull requests that made them, measured on different setups.
- The "8 to 13 times sooner" heading summarizes **8.2x** and **12.8x**; Home's **1.7x** shows the
  gain is concentrated on server-rendered pages.
- The capture misspells Jetfuel as "Jetful SSR" once, and ends at an empty "Thank you" heading, so any
  acknowledgments were not captured.

## Affected pages

- [[AI-Native Software Development Lifecycle]]
- [[Agent Skill]]
- [[Agentic Testing]]
- [[Human Deferral to AI]]
- [[Legacy Code Modernization with AI Agents]]
- [[Software Performance Engineering]]

## Raw capture

- [[knowledge-base/raw/sources/Rebuilding the global town square from scratch]]

## Citations

- Canonical URL: <https://blog.x.com/en/engineering/rebuilding-the-global-town-square-from-scratch>
  (`utm_source` parameter removed).
- Published on the X Blog engineering section on November 4, 2026; no personal byline in the
  capture; captured November 6, 2026.

## Related pages

- [[AI-Native Software Development Lifecycle]]
- [[Agent Skill]]
- [[Agentic Testing]]
- [[Human Deferral to AI]]
- [[Legacy Code Modernization with AI Agents]]
- [[Software Performance Engineering]]
- [[Coding Agent Harness]]
- [[Mistral - Modernizing Complex Legacy Code with AI Agents]]
- [[Anthropic - How AI Agents Shape Experts' Judgment Calls]]
