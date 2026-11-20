---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-19-tselovalnikov-10x-engineer
source_title: "How to Be a 10x Engineer in 2027 and Beyond"
source_author: "Sergey Tselovalnikov"
source_url: "https://serce.me/posts/2026-11-19-how-to-become-a-10x-engineer-in-2027-and-beyond"
tags:
  - source/summary
  - coding-agents
  - engineering-productivity
  - opinion
source_ids:
  - src-2026-11-19-tselovalnikov-10x-engineer
status: active
---

# Sergey Tselovalnikov - How to Be a 10x Engineer in 2027 and Beyond

## Summary

A short **opinion essay** on what "10x engineer" should mean once AI agents can write code. Sergey
Tselovalnikov argues that the obvious route, orchestrating many agents to produce ten times more
work, will "likely only bring 10x the burnout and not much else". The better route is to change
**what work the company does**. He means projects that were previously too expensive, too difficult,
or impossible, and that AI has newly made viable. His evidence is one secondhand podcast anecdote and
two pre-AI historical analogues. The essay contains no data.

## Key claims

### Define 10x by impact, not output

The essay sets a deliberately strict definition. If an ordinary engineer raises the company's share
price by *x%*, a 10x engineer raises it by ten times as much. The point of the definition is that
"producing 10x the code won't necessarily make you a 10x engineer unless that code has 10x the impact
(hopefully positive) on the company."

### Orchestrating agents is the naive path

Running agents on many tasks at once "would likely result in maybe 2–3x your normal throughput with a
high risk of burnout in the best case." In the worst case it produces "an imitation of productivity –
multiple slop grenades that can, in fact, decrease the company's value." Other engineers have the same
tools and industry expectations are rising, so relative impact gained this way erodes. The 2–3x figure
is the author's hedged estimate, not a measurement.

### Pursue work that was previously uneconomic

The central example is **secondhand**. In a Pragmatic Engineer podcast episode, Gergely Orosz described
an engineer whose company paid "a substantial share of its revenue" to license a critical software
component. Rebuilding it would have taken years. With AI agents, the engineer "managed to build a
faster replacement using the existing specifications and test suite." The original vendor then paid
the company for the new implementation and for keeping it closed-source, so the vendor could license
it to others. No company, component, timeline, or figure is named.

Two pre-AI analogues are offered to show the pattern is not AI hype:

- Paul Buchheit chose to build the Gmail interface in JavaScript in the early 2000s despite warnings.
  The essay quotes his recollection that "the impossible quickly became the new normal".
- In 2008, Philips engineers designing physical remotes for colour-changing lamps mocked the controls
  up on an iPhone for user testing, then realised the smartphone could replace the remote.

### The opportunity is an intersection

The engineer who wins knows the company's **technology stack** and its **business model**, and
notices a **broader industry shift**. The opportunity sits where the three overlap. AI differs from
earlier, often niche shifts because it changes how software is built, and so touches "pretty much
every company that uses or builds software". That may create many such openings "at least for some
time".

### Conclusion

"Simply tokenmaxxing and churning out 10x more code is not necessarily going to produce outsized
returns, despite what the vendors would like you to believe." The larger opportunity lies in ideas
once thought "too crazy to even attempt".

## Why it matters

The essay is an individual-level restatement of a tension already on
[[AI-Native Software Development Lifecycle]]: lifecycle gates measure throughput, while value depends
on what the throughput produces. Its "slop grenades" line adds a practitioner's voice to the
measured design-level slop in [[Gabe Orlanski - Slop Is Moving Up the Stack]]. The anecdote is also a
compact case for [[Legacy Code Modernization with AI Agents]]. An existing specification plus a test
suite is the reference that makes an agent-built replacement checkable, the same condition the vault
records for port-style migrations. Here the replacement is of a licensed third-party component, not
the team's own legacy code.

## Tensions / open questions

- The key example is relayed twice (engineer → Orosz → essay) with no identifying details, so it
  cannot be checked. "Faster replacement" gives no benchmark, and the vendor's buy-back is the only
  outcome given.
- The author concedes the share-price definition "might seem somewhat pointless". Its role is
  rhetorical, and nothing in the essay tells an engineer how to estimate impact before choosing a
  project.
- The 2–3x throughput ceiling for agent orchestration conflicts with more optimistic first-party
  productivity claims elsewhere in the vault. Neither side here provides a controlled measurement.
- Survivorship: the analogues are famous successes, and the essay does not discuss failed bets of
  the same kind.

## Affected pages

- [[AI-Native Software Development Lifecycle]]
- [[Legacy Code Modernization with AI Agents]]

## Raw capture

- [[knowledge-base/raw/sources/How to Be a 10x Engineer in 2027 and Beyond]]

## Citations

- Raw capture: Sergey Tselovalnikov, "How to Be a 10x Engineer in 2027 and Beyond", published
  2026-11-19 (source ID date; also in the URL), captured 2026-11-20. The canonical URL drops the
  newsletter `utm_source` parameter.
- Author normalization: the capture's author field reads "Sergey Tselovalnikov on 19 November 2026"
  (a byline-date artefact of the clipper). It is normalized to the person's name.
- Secondhand sources cited by the essay but not read: Gergely Orosz's Pragmatic Engineer podcast
  episode, Paul Buchheit's 2014 blog post, and a Signify blog post on Philips Hue.

## Related pages

- [[AI-Native Software Development Lifecycle]]
- [[Legacy Code Modernization with AI Agents]]
- [[Gabe Orlanski - Slop Is Moving Up the Stack]]
- [[Agentic Testing]]
- [[Agent Workflow Maturity]]
