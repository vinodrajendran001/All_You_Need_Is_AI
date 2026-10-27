---
type: source-summary
created: 2026-10-27
updated: 2026-10-27
source_id: src-2026-10-15-cohere-agent-teams
source_title: "Scaling agent teams: reach the frontier at 30% of the cost"
source_author: "Keenan Samway, Daniel D'souza, and Nouha Dziri"
source_url: https://cohere.com/blog/lessons-from-scaling-teams-of-frontier-coding-agents
tags: [source/summary, ai-agents, multi-agent, delegation, coding-agents]
source_ids:
  - src-2026-10-15-cohere-agent-teams
status: active
---

# Cohere - Scaling Agent Teams - Reach the Frontier at 30% of the Cost

## Summary

A Cohere research post by Keenan Samway, Daniel D'souza, and Nouha Dziri, published 15 October 2026. It
studies how to organize teams of coding agents, using a deliberately minimal lead-and-worker harness on
ProgramBench, a benchmark of 200 programs that an agent must rebuild from an executable it can run but not
read, plus documentation. Teams beat solo agents but cost several times more.

What mattered most was where workers were placed. Delegating only exploration and planning matched
delegating every stage at half the cost, and a strong lead with cheap planning workers came close for
less. The title's "30% of the cost" compares $155 with $510 at **61.8% versus 63.2%** reward: near the
frontier, not equal to it. The durable lessons are that allocation to the task's bottleneck matters more
than team size, and that the lead's quality sets the ceiling.

## Key claims

**The testbed changes one thing at a time.** Every agent uses a `bash` tool in one shared workspace. The
lead hands out work through `delegate_agent`, can resume a worker with its context or start a fresh one,
and sees workers' reports. The study varies five things: which stages the lead delegates (a *minimal*
prompt or a *PIV* prompt that asks for exploring and planning, implementing, and verifying), whether the
lead blocks or keeps working asynchronously, which models play which roles, how many workers there are,
and whether agents can message each other. The main models are three GPT-5.6 tiers, Luna, Terra, and Sol,
in increasing capability and cost. Each configuration normally ran three times on all 200 tasks; a single
task's score varied with a standard deviation of about 6 points, the benchmark average by 0.5 for a
typical configuration and 1.4 for the noisiest, and differences are reported with paired 95% intervals.

**Teams win, at a price.** With the minimal prompt, a blocking all-Sol team scored 61.8% against 52.1% for
a solo Sol agent. The PIV prompt lifted the solo agent to 57.7%, and a blocking PIV team still reached
63.1%. "All four Sol teams cost between 4 and 7 times as much as the corresponding solo agent." An
asynchronous PIV lead finished in 19.5% less time at about the same reward. An asynchronous minimal lead
finished in 60% less time but did more of the work itself, delegating 4.4 times per task instead of 6.1,
and fell to 55.9%.

**Put workers on the bottleneck.** "Planning was the clear winner." An asynchronous lead delegating only
planning matched one delegating every stage (63.6% against 63.2%) at $249 against $510, and gained 3.4
points per $100 of added cost against 1.7 for the next-best stage. The authors' explanation: "The target
program is a black box, so its behavior has to be discovered by running it." Commit0-Lite, which supplies
the specification, showed the reverse: implementation was the most effective stage to delegate in eight of
ten team setups. Because a solo Sol agent already passes every test on 12 of its 16 tasks, the authors
treat this check as "suggestive rather than conclusive".

**Cheap workers help a strong lead, not a weak one.**

| Asynchronous planning team | Reward | Cost (200 tasks) |
| --- | --- | --- |
| Solo Sol, PIV prompt | 57.7% | |
| Sol lead with 16 Luna planners (one run) | 61.8% | $155 |
| All-Sol, planning delegated | 63.6% | $249 |
| All-Sol, every stage delegated | 63.2% | $510 |

A Sol lead with dynamically chosen Luna planners scored 60.5%, keeping 47.5% of the all-Sol team's gain
for 13.9% of its extra cost. With Luna workers held fixed, upgrading the lead from Luna to Terra to Sol
raised reward from 42.5% to 51.6% to 60.5%, each above a solo agent of the lead's model (37.4%, 47.2%,
57.7%). "Cheap workers could not make up for a weaker lead, though." A Terra lead with Luna workers stayed
below a solo Sol agent.

**More planners add information; more implementers do not.** Fixed teams of 2 to 16 Luna planners rose
from 59.6% to 61.8%; across the team, runs of the reference program grew from 15 to 109 and reports from
17,000 to 75,000 characters. Implementation and verification teams improved from two to four workers and
then slipped: each implementer's assignment shrank from about 1,400 characters to 440, while the lead
checked the combined program no more often. Each fixed-size configuration was run once.

**A message channel mostly carried reports upward.** With a `send_message` tool, "84% of messages went
from workers to the lead". Messages between workers averaged fewer than one per task. Sol and Terra teams'
reward did not change; Luna teams lost 4 to 7 points, and about half of Luna's `send_message` calls were
malformed and rejected by the harness. The authors note their prompts give workers independent tasks, so
there was little to share; a cited ARC-AGI-3 study with a shared goal found five communicating agents
matched the best of 33 independent ones.

**Other models use a team differently.** On a 30-task subset with one run per configuration ("With one
run per model, differences of a few points may be noise"), GPT-5.6 teams gained up to 6.9 points and
Claude Opus 4.8 5.9, Claude Opus 4.7 delegated at most 1.3 times per task, Claude Haiku 4.5 and Gemini 3.7
Flash delegated but gained nothing, and Gemini 3.8 Flash gained 3.1 points with a blocking lead and lost
4.6 with an asynchronous one. "Two things have to go right for a team to help": the lead must choose to
delegate, and must use what comes back. Claude Opus 5 was stopped after eight trial tasks all hit an
eight-hour timeout at roughly $500 each.

## Why it matters

[[Agent Delegation]] gains a controlled answer to where delegation pays: on the stage that is actually
the bottleneck, with a lead strong enough to use the results. A larger team or a richer message channel
did not substitute for either.

[[Model Routing]] gets a role-based version of routing. The expensive model makes the decisions and cheap
models gather information, and the saving held only where the cheap role was information gathering.

[[Test-Time Scaling]] gets a new axis, teams of agents, and its exchange rate: several times the cost for
gains of a few to about ten points on this benchmark.

## Tensions / open questions

- **The headline is a near-match, not a match.** $155 bought 61.8% against $510 for 63.2%, and the $155
  configuration was a single run, while the all-Sol figures average three.
- **Two cost ranges.** The key takeaways say team gains "come at 3–7× higher cost"; the body says the
  four Sol teams cost 4 to 7 times the solo agent.
- **The planning result is benchmark-shaped.** ProgramBench hides the specification, so discovering it
  is the bottleneck; on Commit0, which supplies it, implementation helped most.
- **Prices and tiers are specific.** Cost conclusions depend on GPT-5.6 tier pricing and token use in
  this harness; the external projects cited in the opening (a C compiler, a browser, the Bun port, a GDAL
  rebuild) are uncontrolled and not comparable with these results.
- **Lead skill may be trainable.** The authors suggest that delegating well is a model capability that
  differs sharply within one family; the evidence is single-run.

## Affected pages

- [[Agent Delegation]]
- [[Model Routing]]
- [[Test-Time Scaling]]
- [[Cohere]]

## Raw capture

- [[Scaling agent teams reach the frontier at 30% of the cost]]

## Citations

- Canonical URL: https://cohere.com/blog/lessons-from-scaling-teams-of-frontier-coding-agents (email
  tracking parameters removed).
- Published 15 October 2026; authors from the clipping's frontmatter. Figures are image-only; their
  captions and the footnotes were captured and carry method details used above.

## Related pages

- [[Agent Delegation]]
- [[Model Routing]]
- [[Test-Time Scaling]]
- [[Harness Optimization]]
- [[Coding Agent Harness]]
- [[Agent Planning]]
- [[Inference Efficiency Frontier]]
- [[Cohere]]
- [[AI Knowledge Base Overview]]
