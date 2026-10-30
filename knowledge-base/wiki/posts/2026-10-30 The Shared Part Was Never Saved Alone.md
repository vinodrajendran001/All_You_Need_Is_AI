---
type: social-post
created: 2026-10-30
updated: 2026-10-30
tags:
  - post
  - prompt-caching
  - context-engineering
platforms:
  - linkedin
  - x
pages_used:
  - "[[Semantic Caching]]"
  - "[[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]]"
  - "[[Leon Sick et al - On-Policy Self-Training]]"
  - "[[Pavi Dhiman and Cyrus Asgari - Building an Inference Stack That Improves Itself]]"
  - "[[Divyansh Agrawal - Qwenputer - A Deterministic RISC-V CPU Inside Qwen3.5]]"
  - "[[Joe Lothan et al - Less Is More - From 1M Lines of Firmware to 300 of Assembly]]"
topics:
  - first-request reuse
  - prompt-cache boundaries
  - shared versus variable context
covers_from: 2026-10-23
covers_through: 2026-10-30
status: ready
---

# The Shared Part Was Never Saved Alone

## LinkedIn post

Cloudflare's automated code reviewer had the same general instructions across projects. But that did not mean it could reuse the work of processing them.

The reviewer asks a language model to inspect software changes, sending instructions and the conversation so far with each call. Its provider can save earlier computation for an unchanged opening and reuse it later. That's prompt caching.

The useful question is whether a new review can reuse work from another review, not just whether later calls reuse work from their own conversation.

Before a fix, Cloudflare reports that only 14% to 26% of first requests found a saved opening, even though the general instructions were identical across projects.

The culprit was the boundary. The request-building code put general instructions, the project folder path, and the date into one block. The marker telling the provider where the reusable block ended came after all of it.

The common text was there. But it had never been stored separately from the changing details. Another project couldn't reuse that whole project-specific block.

Cloudflare split the shared opening from the variable details and gave it its own cache marker. The reported share of first requests reading from the cache then rose to between 91% and 99.5%.

There is a tradeoff: keeping the opening identical meant the descriptions of available tools could not change between jobs. Cloudflare also shipped another change at the same time, so this before-and-after account does not isolate the cache fix's dollar saving. A better reuse metric is not a complete measure of review quality.

For your own system, inspect the first request actually sent to the provider, not just the template in your application. Check what is shared, what changes, and exactly where the stored opening ends. Measure first-request reuse separately, and check that the reviewer still does the job you need.

The aim is not merely to send the same text. It is to make the expensive part of that setup genuinely reusable.

Which repeated setup step in your system looks smaller when it is averaged into a whole session?

Source: Cloudflare
https://blog.cloudflare.com/obsessive-inference-optimization/

#PromptCaching #ContextEngineering #AgentEngineering

## X post

Counts include spaces and punctuation; each URL counts as 23 characters under X's link
weighting. Number labels, counts, and code fences are outside the copy-ready text.

**A) Standalone** (273 chars):

```text
Cloudflare reports its automated code reviewer couldn't reuse computation for shared instructions across projects: the saved block also held project-specific text. Store the stable opening separately. Check the first request, not just average reuse. https://blog.cloudflare.com/obsessive-inference-optimization/
```

**B) Thread:**

1. (243 chars)

```text
Cloudflare reports its automated code reviewer kept reprocessing shared instructions because they were stored with project-specific text. Shared words alone don't guarantee shared work. Check the first request, not just the overall reuse rate.
```

2. (248 chars)

```text
The reviewer asks a language model to inspect software changes. Its provider can save computation for an unchanged opening and reuse it in later calls. That is prompt caching. A new review can then reuse shared setup, not just its own conversation.
```

3. (225 chars)

```text
Before the fix, Cloudflare reports that only 14% to 26% of first requests found a saved opening. The general instructions were identical across projects. Yet the opening of a new review often missed that chance to reuse work.
```

4. (248 chars)

```text
The request builder put shared instructions, the project folder path, and the date into one block. The marker defining the reusable block came after all of it. The shared part wasn't stored alone, so another project couldn't reuse that whole block.
```

5. (190 chars)

```text
Cloudflare split the shared opening from changing details and gave it its own cache marker. It reports that the share of first requests reading from cache then rose to between 91% and 99.5%.
```

6. (241 chars)

```text
This is Cloudflare's before-and-after account. Another change shipped alongside it, so the cache fix's dollar saving isn't isolated. Keeping the opening stable also meant fixed tool descriptions between jobs. Check behavior as well as reuse.
```

7. (257 chars)

```text
Inspect the first request actually sent to your provider. Separate shared instructions from changing context, measure first-request reuse, and keep checking review quality. Make shared setup reusable, not merely repeated. Cloudflare: https://blog.cloudflare.com/obsessive-inference-optimization/
```

**Ship:** Thread. It explains what is being reused, why the boundary mattered, what changed,
and why the observed reuse gain is not an isolated cost or quality result. The standalone
keeps the case and action but drops the numerical comparison rather than its conditions.

## Hook variants

1. **Concrete case:** Cloudflare's automated code reviewer had the same general instructions across projects. But that did not mean it could reuse the work of processing them.
2. **Plain observation:** The reusable text was there. The reusable block was not.
3. **Myth correction:** Putting shared instructions first is not enough if the stored block also includes what changes.

**Recommended:** The concrete case for LinkedIn: it supplies an actor and a task before
introducing caching. X uses the same case with the boundary failure and action in its first
post; it does not open with an unexplained percentage.

## Why this topic

**Window:** 2026-10-23 through 2026-10-30, inclusive, anchored to the newest active ready
post's `covers_through`, not a fixed seven-day schedule. Four ingest entries cover 51 source
summaries, including the thirteen Databricks summaries named collectively in the first
October 23 entry. The Git cross-check covered 25 commits and 195 wiki paths; it did not
reveal another current source summary outside those ingests. Older-source repairs,
navigation, lint reports, and post maintenance were not treated as new releases.

Five direct ByteByteGo sources were excluded before selection. The shortlisted sources
below have non-ByteByteGo authors/publishers and primary URLs; their raw captures were
checked for inherited ByteByteGo citations. No archived candidate supplied this run's
example or claims.

Scores are editorial judgments, 1-5. Clarity and completeness must each be at least 4;
a high total cannot override either gate.

| Angle and source | Clarity | Completeness | Surprise | Concreteness | Reach | Freshness | Total | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Shared instructions need a separately reusable opening - [[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]] | 5 | 5 | 4 | 5 | 5 | 4 | 28 | Selected: one visible boundary, a measured first-request result, and a practical check. |
| Improvement on average can hide lost skills - [[Leon Sick et al - On-Policy Self-Training]] | 4 | 4 | 4 | 5 | 4 | 5 | 26 | Eligible runner-up; explaining training mixtures and retained capabilities needs more setup. |
| Require an optimization proposal to say how it could be disproved - [[Pavi Dhiman and Cyrus Asgari - Building an Inference Stack That Improves Itself]] | 5 | 4 | 3 | 4 | 5 | 5 | 26 | Eligible runner-up; useful but more procedural, with ambiguous performance-baseline wording. |
| Correct calculation does not guarantee the right calculation - [[Divyansh Agrawal - Qwenputer - A Deterministic RISC-V CPU Inside Qwen3.5]] | 4 | 3 | 5 | 3 | 4 | 5 | 24 | Rejected by completeness gate: execution tests are not a worked evaluation of choosing the right computation. |
| Less startup code can move, rather than remove, audit obligations - [[Joe Lothan et al - Less Is More - From 1M Lines of Firmware to 300 of Assembly]] | 3 | 4 | 4 | 4 | 3 | 5 | 23 | Rejected by clarity gate: the boot image, measurement boundary, and generator need too much introduction for this slot. |

The selected spine is [[Semantic Caching]], specifically its Cloudflare prompt-caching
section, not its ByteByteGo-derived semantic-answer-cache discussion. Every public
empirical claim is independently supported by Cloudflare's directly read capture.
The public copy contains one example and no supporting product tour.

**Anti-repeat:** The October 16 post concerned translating internal state between different
models. This post concerns storing the common opening of different jobs using one
provider's cache interface. It also differs from September 18's conversation-memory cost
story: the failure is the request layout, not memory retrieval or history growth.
Semantic Caching is not in cooldown. Freshness is nevertheless scored 4 rather than 5
because the broader subject is adjacent to the recent cache-handoff post.

## Reader check

**Passed:** reread the LinkedIn body, standalone, and connected thread without relying
on these notes. Each preserves the situation, claim, example, mechanism, limit, and action.

| Cold-reader question | LinkedIn and thread | Standalone |
|---|---|---|
| What is the situation? | An automated code reviewer repeatedly sends common instructions to a language model. | An automated code reviewer cannot reuse processing of shared instructions across projects. |
| What is the single claim? | Identical text is not enough; the stored opening must separate shared instructions from variable context. | Store the stable opening separately rather than bundling it with project-specific text. |
| What example supports it? | Cloudflare reports low first-request reuse, then higher reuse after changing that boundary. | Cloudflare's explicitly reported code-review case; numerical outcomes are omitted. |
| Why did it happen? | The only marker was after the project folder and date, so the common part had no separately stored block. | Project-specific text was included in the saved block. |
| What is the limit? | A first-party before/after account, a simultaneous change, and fixed tool descriptions; no isolated dollar or quality result. | A reported case, not a general provider guarantee or a quantified savings claim. |
| What should change? | Inspect the actual first request, measure first-request reuse separately, and retain quality checks. | Separate the stable opening and inspect the first request rather than just average reuse. |

The LinkedIn conclusion completes the reuse argument before the closing question.
The thread defines prompt caching after describing its function; the standalone avoids
the specialist term. No acronym, product mechanism, or benchmark needs an external
explanation. The only company named in the public bodies is the reporting source.

## Fact check

**Passed:** checked every public factual sentence against the direct Cloudflare evidence
below. LinkedIn has 350 words including attribution and hashtags. The X standalone is
273 characters; the seven thread posts are 243, 248, 225, 248, 190, 241, and 257 characters
under the declared link weighting. All public copy is ASCII.

| Public claim group | Direct support and boundary |
|---|---|
| Reviewer task, repeated conversation input, and reuse of computed opening text | Cloudflare summary: reviewer loop and prompt-caching explanation; raw capture: the reviewer setup, repeated context, and cache description. This is input-computation reuse, not retrieval of a previous answer. |
| First requests found a saved opening only 14% to 26% of the time before the change | Cloudflare summary's first-request diagnosis; raw prose explicitly says the first request found a cached prefix 14% to 26% of the time. The unit is first requests, not tokens, review accuracy, or money. |
| Shared instructions plus working directory/date formed one block with its only marker at the end | Cloudflare summary and raw account of OpenCode v1 request construction. The public phrase "project folder path" translates the working directory; this is their configuration, not a claim about all providers or current OpenCode versions. |
| Shared instructions were not stored alone, so a different project could not reuse that whole block | Cloudflare's explicit explanation that the common part was never stored separately. "Same instructions" does not assert that the full requests were identical. |
| Splitting and marking the common opening was followed by 91% to 99.5% first-request cache reads | Cloudflare summary plus raw figure caption, which identifies the share of first requests reading from cache. These are reported before/after ranges, not confidence intervals or an independently reproduced effect size. |
| Stable tool descriptions were required between jobs | Cloudflare's implementation constraint. The raw account also disables the available-skills list; the public copy keeps one concrete tradeoff rather than introducing a second extension mechanism. It does not claim the block split was the only implementation step. |
| Another change shipped alongside; the cache fix's dollar contribution is not isolated | Cloudflare reports the cache fix and moving the standards reference index into the prompt together. Both variants with outcomes retain the before/after and non-isolated-saving caveat. |
| Inspect actual requests and retain quality checks | Editorial recommendation from the reported request-hashing diagnosis and the source's separate review-quality discussion, not a claim that this cache change improved quality. |

**Attribution and exclusion:** The public attribution is exactly `Cloudflare`, matching
the summary's `source_author`; its canonical URL is used in all three public forms.
The raw capture is a first-party Cloudflare engineering account and directly references
provider documentation, not ByteByteGo. The mixed-source spine is used only for the
Cloudflare-backed claim chain; its ByteByteGo comparisons and generic correctness
assertions do not support this post. All six `pages_used` entries are tracked, outside
`wiki/queries/`. The four unselected source pages support only the editorial shortlist.

**Claims cut rather than compressed:**

- The 68% headline reduction: it combines multiple code, model, and effort changes and
  uses a peak-fortnight baseline; it is not the cache split's saving.
- The simultaneous changes' dollar figures: they cannot isolate this change's contribution.
- The 97% overall cache hit rate: its denominator is not specified in the capture.
  The worked comparison uses only the explicitly identified first-request measure.
- An automatic improvement in correctness, latency, or whole-review cost: none follows
  from the first-request percentages alone.

**Compression check:** The standalone drops both numerical ranges instead of stripping
their first-request conditions or implying a measured isolated saving. It retains the
reporting source, task, variable-text mechanism, and action. The thread retains both
ranges, the before/after scope, the penultimate-post caveat, and the quality check.
It does not turn the case into a universal manual-cache-marker requirement.

**Comprehension check:** Each version explains why the shared part was not reusable
and what to inspect differently. The thread's sequence is case, reuse mechanism,
observed misses, boundary error, reported change, limitations, and practical conclusion.
No numerical claim has to borrow its meaning from these notes.

## Attribution

Public example and all empirical claims: **Cloudflare** -
https://blog.cloudflare.com/obsessive-inference-optimization/

Direct source: [[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]].
Primary capture: [[knowledge-base/raw/sources/Cutting our inference bill by 68% by being obsessive about optimization]].
Wiki synthesis: the Cloudflare-specific section of [[Semantic Caching]].

The other source pages in `pages_used` document the scored editorial alternatives.
They are not additional public examples or evidence for the Cloudflare measurements.

## Hashtags

LinkedIn: `#PromptCaching #ContextEngineering #AgentEngineering`

X: none.

## Related pages

- [[Post Archive]]
- [[Semantic Caching]]
- [[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]]
- [[Leon Sick et al - On-Policy Self-Training]]
- [[Pavi Dhiman and Cyrus Asgari - Building an Inference Stack That Improves Itself]]
- [[Divyansh Agrawal - Qwenputer - A Deterministic RISC-V CPU Inside Qwen3.5]]
- [[Joe Lothan et al - Less Is More - From 1M Lines of Firmware to 300 of Assembly]]
