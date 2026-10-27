---
type: source-summary
created: 2026-10-27
updated: 2026-10-27
source_id: src-2026-10-20-cloudflare-inference-bill
source_title: Cutting our inference bill by 68% by being obsessive about optimization
source_author: Cloudflare
source_url: https://blog.cloudflare.com/obsessive-inference-optimization/
tags: [source/summary, inference, prompt-caching, model-routing, code-review]
source_ids:
  - src-2026-10-20-cloudflare-inference-bill
status: active
---

# Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization

## Summary

A Cloudflare engineering post, published 20 October 2026, about the company's internal AI code reviewer. A
coordinator hands each merge request to specialist reviewer agents, and risk tiers decide how intensive the
review is. Between April and the end of August the average review cost rose from $1.19 to about $2.46,
with no significant architectural change. From mid-September the team cut it to $0.77, "down 68% from the
$2.43 it averaged over our two most expensive weeks", and cut the median review time from 4m 09s to
1m 32s. The 68% is the cost of one review against its most expensive fortnight, not the company's whole
inference bill, as the title suggests.

Three durable lessons. An aggregate cache hit rate can hide a broken first request. Price per token is not
cost per task. A cheaper agent needs a quality check, and here that check found that one reviewer kept its
real findings while others lost some. The evidence is first-party production telemetry. Most comparisons
are before/after, and the author says the cost attribution "isn't a statistically sound controlled
experiment"; the model and effort comparisons used randomized 50/50 splits.

## Key claims

**The cost doubled through model choices, not architecture.** Cost per review, with the tier mix held
fixed, rose from $1.22 in March to $2.32 in August. More reviews landed in the most expensive tier (59% to
65%), but "most of the cost increase actually came from model changes". Moving every reviewer onto
Anthropic models raised cost per job from $1.38 to $2.03. The internal standards reviewer went from about
$0.25 to $0.88 per review on Claude Opus 4.7; Cloudflare calls that agent Codex, and it is not OpenAI's
product. Meanwhile the cache hit rate rose from 85.7% to 97% while tokens per review tripled, from 0.91
million to 2.99 million: "A high hit rate on three times as many tokens still costs a lot more, even with
the low cache read cost."

**Most spend went on context the model had already seen.** Before the work, cache writes were 43% of
spend, cache reads 34%, and output 23%. The code quality reviewer averaged 16.6 model calls per review,
writing 72k tokens to the cache and reading back 1.08m, because each call resends the whole conversation.
With Anthropic's prompt cache, writes cost 1.25 times the normal input price, reads cost 0.1 times, and an
entry expires after five minutes without a read. That set two goals: make each session's first request
read the cache instead of writing it, and make fewer calls.

**One block layout defeated cross-repository caching.** The first request of a session found a cached
prefix only 14% to 26% of the time, although 11k to 21k tokens of tool definitions and agent prompt were
identical in every repository. OpenCode v1 built one block holding the agent prompt, the working
directory, and the date, and put the only cache breakpoint at its end, so the shared part was never stored
on its own. On 16 September a marker and a plugin hook split that block, giving the shared bytes their own
breakpoint. Anything repository-specific had to leave the shared part: the skills list was disabled, and
tool descriptions can no longer change between jobs. First-request cache reads rose to 91–99.5%. A second
change moved the standards reviewer's reference index into its prompt instead of reading it with tool
calls, cutting its calls per run from 15.9 to 9.6 and its cost per run from $1.12 to $0.72. Together these
took cost per review from $2.47 to $2.02.

**Small harness fixes saved about $0.20 per review.**

| Change | What the data showed | Effect |
| --- | --- | --- |
| Remove a tool sub-reviewers could not use | In 57% to 76% of sessions they called it, were rejected, and spent a call recovering | One wasted call and about 2.9k tokens of tool definitions gone from each request |
| Read files in parallel | 64% of the code quality reviewer's turns made exactly one tool call | All patches read in the first response, up to 150 KB |
| Skip reviewers on re-reviews | About two-thirds of jobs are re-reviews | On full-tier re-reviews, AGENTS.md, performance, and documentation reviews skipped 56%, 23%, and 13% of the time |
| Stop after posting | One extra turn re-read the conversation to write a summary nobody saw | About $0.07 saved per job |
| Stop cancelled jobs | 358 of 446 cancelled jobs kept running | Jobs check their own status every 15 seconds |

Three reviewers now send identical first requests, so one writes the cache and two read it. A cache entry
can be read only once the response that wrote it starts streaming, so the other two wait up to 20 seconds;
the delay saves about nine cents per reviewer.

**Model and effort changes saved more than code changes.** "Code changes account for $0.65 of the $1.67,
and model and effort changes for $1.06." Each step compares weekday hours before and after a change, "so
this isn't a statistically sound controlled experiment." In a randomized split, Opus 5.5 at medium effort
showed no measurable change in review outcomes against Opus 5. Its lower per-token price explains only
about $0.20 of the drop; the rest came from fewer tokens, with cache reads per review down 82%, cache
writes 54%, and output 67% since early September. In a 50/50 split at the same per-token price, Sonnet 5.5
was 62% cheaper per run than Sonnet 5 for code quality, 58% for performance, and 47% for security after two
and a half days. At medium effort, the code quality reviewer on Sonnet 5.5 made 1.7 calls per run instead
of 6.2. High effort cost 61% more per run than medium and posted 58% more critical and warning findings
after one day, about two cents per review. Code quality is moving to high effort, and the headline cost
assumes it.

**Faster, mostly by doing less.** Median latency fell from 4m 09s to 1m 32s and the 99th percentile from
15m 20s to 4m 41s; reviews taking over five minutes fell from 37.9% to 0.7%. Part of this regained lost
ground: by August the median had been 14% slower than in April, and the 99th percentile 48% slower.

**Quality was checked two ways, and the answer depended on the reviewer.** Severe findings fell 40% for
code quality at high effort, and 56% and 71% for security and performance at medium effort. The first
check asked whether authors changed the flagged lines in their next push, against a coincidence baseline:
lines 30 to 40 away changed about 15% of the time. Authors acted on 59% of code quality's serious
findings, up from 34%, so acted-on findings per 1,000 reviews held at 132 against 145, "within the margin
of error". In the second check, two models from different providers judged a blinded sample of 657
findings, with a third model settling disagreements. Important findings per review went from 0.28 to
0.30, and over-severe findings fell from 0.46 to 0.14, "the clearest result in the research". Medium
effort lost real findings: code quality at medium produced roughly a quarter as many acted-on findings as
at high, and the performance reviewer found about 64% fewer important issues, about one fewer every 24
full-tier reviews. Security fell by about a quarter, not statistically significant. Reviews ending without
a verdict fell from 0.79% to 0.27%.

## Why it matters

[[Semantic Caching]] gains a production case of exact prefix caching failing silently. The aggregate hit
rate was 97% while first requests, which pay for cache writes, mostly missed. The fix was the byte layout
of the prompt, not a better cache.

[[Reasoning Effort Control]] gets an effort trade measured with quality instrumentation. Effort was worth a
few cents per review, but medium effort lost real findings on two of three reviewers.

[[Model Routing]] gets evidence that cost per run, not price per token, is the number to route on: two
Sonnet versions at the same per-token price differed by 47–62% per run.

## Tensions / open questions

- **The headline is narrower than the title.** The title says "inference bill"; the 68% is average cost
  per review against the two most expensive weeks. Baselines differ across the post: $2.43 (headline),
  $2.44 (attribution chart), about $2.46 (end of August), and $2.47 (before the cache fix).
- **Attribution is uncontrolled** apart from the randomized model and effort splits.
- **The quality proxies are imperfect.** "An author changing the flagged lines shows they did something,
  not that the finding was right." "The judges are models too", there are 35 to 66 findings per group,
  and the post-change window is one day long.
- **Two reviewers may still miss findings.** Performance lost real findings at medium effort, and security
  may have; testing both at high effort is next.
- **Cacheability cost flexibility.** Keeping the shared prefix stable meant disabling the skills list and
  freezing tool descriptions.

## Affected pages

- [[Semantic Caching]]
- [[Reasoning Effort Control]]
- [[Model Routing]]
- [[Cloudflare]]

## Raw capture

- [[Cutting our inference bill by 68% by being obsessive about optimization]]

## Citations

- Canonical URL: https://blog.cloudflare.com/obsessive-inference-optimization/ (email tracking
  parameters removed).
- Published 20 October 2026 and captured 26 October. The clipping records no author; the post is written
  in the first person by a Cloudflare engineer who is not named in the capture. Charts are image-only;
  their captions were captured.

## Related pages

- [[Semantic Caching]]
- [[Reasoning Effort Control]]
- [[Model Routing]]
- [[Inference Efficiency Frontier]]
- [[Tool Roster Economics]]
- [[Context Engineering]]
- [[LLM-as-a-Judge]]
- [[Coding Agent Harness]]
- [[Cloudflare]]
- [[Anthropic]]
- [[AI Knowledge Base Overview]]
