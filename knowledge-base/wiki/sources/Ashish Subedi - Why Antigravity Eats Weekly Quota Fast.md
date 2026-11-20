---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-19-ashish-subedi-antigravity-quota
source_title: "Why Antigravity Eats Weekly Quota Fast - and What I Measured"
source_author: "Ashish Subedi (recovered; see Citations)"
source_url: "https://asubedi.com.np/blog/why-antigravity-eats-weekly-quota-fast/"
tags:
  - source/summary
  - prompt-caching
  - coding-agents
  - cost
  - kv-cache
  - reverse-engineering
source_ids:
  - src-2026-11-19-ashish-subedi-antigravity-quota
status: active
---

# Why Antigravity Eats Weekly Quota Fast - and What I Measured

## Summary

A personal blog post that tests one explanation for why Google Antigravity (`agy`) burns through a
weekly quota during ordinary coding: a short prompt-cache lifetime. Coding with an agent involves
pauses to read a diff or run a test; if the provider's cache expires during a pause, the next
message re-sends the whole conversation at full price.

On Gemini 4 models, the author writes, Antigravity relies only on Google's **implicit caching**, an
automatic, best-effort prefix match whose time-to-live (TTL) Google does not publish, with a **90%
discount** on cached tokens. The author inspected the local binaries, measured cache hits through
the CLI's per-turn token counts, and located the expiry between **4 min 45 s** and **5 min 00 s** of
idle time. The binary already contains a dormant keep-alive mechanism that sends a 1-token
background request just before expiry and discards the reply; it is switched off for Gemini. The
author patched the binary to enable it and reports that it kept the cache warm across a pause of
just over six minutes without adding anything to the conversation.

This is a single author's self-measurement on small, near-empty conversations, plus a modeled
extrapolation to a long session. The author credits Gemini 4 Hydrogen, Gemini 4 Argon, and
`hy4-flash` via OpenCode for the reverse engineering, probing, and tooling. This summary stays at
the level of mechanism and omits binary addresses and patch instructions.

## Key claims

### What the binary shows (author's reading)

- The core Go agent binary is **193 MB**. Its telemetry buckets the gap between turns into `lt_5m`
  and `ge_5m`, which the author reads as a strong clue that 5 minutes is the cliff.
- A keep-alive module (`modelapiccpa/keepalive.go`) clones the last request, replaces the final
  prompt block with a single period, sets `max_output_tokens = 1`, sends it in the background, and
  throws the reply away so it "never pollutes your conversation history". The ping interval is
  hardcoded at **4 min 30 s** (`270s`) and a staleness cutoff at **4 min 45 s** (`285s`) aborts a
  ping when the cache is presumed dead.
- Two gates keep it off: a server-side experiment flag not exposed in settings or hooks, and a
  provider check that restricts background pings to explicit-cache providers "(like Claude)",
  "completely skipping Gemini models". The binary also tracks a per-conversation maximum-pings
  budget.

### Measured cache behaviour

- A new conversation with the five-word prompt "Reply with only OK." sends **16,816** tokens on its
  first turn (system prompt, tool declarations, MCP servers, and skills). A second turn in the same
  process read **14,762** tokens from cache and billed **2,152** uncached. Separate one-shot `agy -p`
  processes never hit the cache, because one-shot mode re-initializes a step timestamp at step 0 and
  breaks prefix continuity.
- After an 8-minute idle gap the next turn missed (**16,921** uncached). With a single ping at **+4
  minutes**, the turn at +8:00 hit (**2,144** uncached, **14,880** cached): "Hitting the implicit
  cache resets its TTL timer."
- Binary search over idle gaps: hits at 4 min 30 s and 4 min 45 s (**14,764** cached), misses at 5
  min 00 s and 8 min 00 s.

### Cost arithmetic

- The author weights cached tokens at 0.1x: effective cost = uncached + 0.1 x cached.
- Over the measured 8-minute window, no keep-alive cost **33,745** effective tokens (two messages)
  or **37,378** (three messages), against **24,092** with one ping: a saving of **9,653 to 13,286**
  effective tokens (**29-36%**), "a **3.7x return** on the cost of the ping".
- For a **150,000**-token session the post **models, rather than measures**, a cold turn at
  **150,000** effective tokens against a warm turn at **16,935**, for "133,065 (~8.9x ROI)".
- Pinging is not free, so the author derives a break-even cap, `N_max`: **3 pings** at the 16.8k
  context and **7 pings** at 150k, after which pinging costs more than one cold miss.

### Side questions and the built-in engine

- Antigravity's `/btw` side question kept the main cache warm (the final turn at +6:41 read
  **14,770** cached tokens), but the fork itself was a cold call at **17,697** uncached tokens,
  because it gets a new conversation ID and about **873** extra instruction tokens. Total cycle
  **21,325**: "~4.9x a normal warm ping" and "~26% more than just accepting a cache miss".
- With the built-in engine enabled on a patched binary, on `gemini-3.8-flash-low`, a background ping
  fired at **+4 min 32 s**, and the second user turn at **+6 min 06 s** read **11,835** cached
  tokens and billed **2,121** uncached. The HTTP log showed three requests for two user turns, and
  the transcript had only four steps: "zero trajectory growth".

### Takeaways stated by the author

- A capped keep-alive "saves 30% to 88% of effective tokens across a pause". The 88% end rests on
  the modeled 150k case, not a measurement.
- "Trim your baseline prefix": even a five-word prompt starts with "13,800 to 16,800+ tokens" of
  instructions, MCP schemas, and skills, so disabling unused MCP servers and plugins shrinks every
  cold turn.
- Caveats in the post: the arithmetic uses the published 90% discount ("internal subscription quota
  weights may vary slightly"), implicit caching is best-effort so "backend TTLs can shift under
  load", and Google "could modify or remove" the flag-gated subsystem.

## Why it matters

The vault's caching material is mostly about **where** content sits in a request: stable content
first, append-only requests, tools appended rather than inserted (see [[KV Cache]] and
[[Context Engineering]]). This source adds **when**. A perfectly ordered prefix still costs full
price if the human pauses past the provider's idle expiry, and interactive coding is pause-heavy by
nature. It also shows a harness vendor treating cache warmth as harness state, with a ping budget,
a staleness cutoff, and a discard rule, which is a design element [[Coding Agent Harness]] does not
yet record. The measured baseline prefix (about 14k-17k tokens of system prompt, tools, MCP servers,
and skills before any work) prices the residency cost that [[Tool Roster Economics]] argues about
in a second product.

## Tensions / open questions

- **Measured versus modeled.** The 8-minute window, the expiry boundary, `/btw`, and the live test
  are measured, each apparently once. The 150k session, the "~8.9x ROI", the 88% upper bound, and
  `N_max = 7` are arithmetic on assumptions.
- **Small arithmetic drift.** The `N_max` numerator at 16.8k is given as 13,320, which is 0.9 x
  14,800; the measured cached prefix was about 14,770 (0.9 x 14,770 = 13,293). The floor is 3
  either way. The 9,653 figure compares a two-message scenario with a three-message one.
- **Different model in the live test.** The baseline probes used `gemini-4-hydrogen-low`; the
  patched-binary test used `gemini-3.8-flash-low`, whose prefix was smaller (**13,884** on turn 1).
- **Quota is inferred, not measured.** The author uses token counts because "account-level quota
  percentages are noisy"; whether quota is weighted by the 90% discount is assumed.
- **Patching a vendor binary.** Enabling a server-gated feature by modifying the client may conflict
  with the product's terms, and the behaviour may change in any release.

## Affected pages

- [[KV Cache]]
- [[Coding Agent Harness]]
- [[Context Engineering]]

## Raw capture

- [[knowledge-base/raw/sources/Why Antigravity Eats Weekly Quota Fast - and What I Measured]]

## Citations

- Canonical URL: <https://asubedi.com.np/blog/why-antigravity-eats-weekly-quota-fast/> (the captured
  link carried a `utm_source=tldrai` parameter, removed here).
- The capture's `author` field is empty and its `published` field is blank. A read-only fetch of the
  canonical page on 2026-11-20 recovered "Publish date: Nov 19, 2026" and the site description
  "Personal Website of Ashish Subedi", which is the basis for the author and the source ID date. No
  figures were taken from the web page. Captured November 20, 2026.
- The post cites Google's Antigravity plans documentation, Gemini API and Google Cloud context-cache
  documentation, and two Antigravity CLI GitHub issues (#1072 and #1291) about quota depletion.

## Related pages

- [[KV Cache]]
- [[Coding Agent Harness]]
- [[Context Engineering]]
- [[Tool Roster Economics]]
- [[Semantic Caching]]
- [[Factory Research - Droid 1.0 - Building a Frontier Harness]]
- [[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]]
- [[Model Context Protocol]]
