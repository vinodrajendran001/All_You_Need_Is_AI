---
type: source-summary
created: 2026-09-30
updated: 2026-09-30
source_id: src-2026-09-29-yoon-multiplayer-ai
source_title: "We're building multiplayer AI. Here's what we've learned so far"
source_author: Jina Yoon
source_url: https://newsletter.posthog.com/p/were-building-multiplayer-ai-heres
tags: [source/summary, ai-agents, context-engineering, memory, multi-agent, production]
source_ids: [src-2026-09-29-yoon-multiplayer-ai]
status: active
---

# Jina Yoon - We're Building Multiplayer AI

## Summary

Jina Yoon reports PostHog's early experience building shared human-and-agent workspaces. The central
finding is that hand-maintained context files do not survive contact with real teams, so PostHog
replaced them with a layer that extracts context from work that actually shipped. Its other finding is
about where collaboration lives: coding stays mostly solo, and the collaborative surfaces are the ones
before and after coding - planning, artifacts, transcripts, and review. PostHog calls governance and
permissions one of its biggest blind spots, and says it is interviewing users to learn more.

## Key claims

- The manual approach failed measurably: over **90 days**, **64 users** started a shared `CONTEXT.md`
  file and only **14 users** ever edited it.
- The replacement starts nearly empty and runs a nightly **"dreaming" task** that records what
  happened that day into a version-controlled Markdown wiki, extracting from work objects such as PRs,
  docs, and dashboards.
- The selection rule is the design: record what was **actually shipped, merged, or decided in a day**,
  not meeting notes or brainstorming documents, to keep the agent from treating proposals as company
  state.
- Spaces hold people, agents, and work objects in one container. Artifacts act as portable session-state
  snapshots: a session produces an artifact, and that artifact becomes context for the next session.
- PostHog reports three recurring Space-**setup** patterns *"even among just ~200 PostHog employees"*:
  users created Spaces around teams, product areas, incidents, and task types. Separately, and without
  a stated population, its early data says coding is mostly solo, collaboration happens more in GitHub
  than in the PostHog UI, and users overwhelmingly preferred starting tasks privately despite the
  team's expectation that they would default to shared Spaces.
- Proposed Space setup asks for goals, targets, measurement intervals, and deadlines so that
  permissions, experiments, and dashboards can be defaulted from them.

## Why it matters

The 64-to-14 gap is the most useful number here, because it is a measurement of an assumption the
vault's context-engineering pages have largely taken on faith: that teams will curate the context
their agents read. PostHog's answer - derive context from artifacts that already carry a commitment,
rather than asking people to write it - converts memory maintenance from a discipline problem into a
pipeline problem. The privacy finding cuts the other way for multi-agent designs: people chose private
work even when a shared surface was available and encouraged.

## Tensions and caveats

These are internal product observations, not a study. The 64-and-14 counts are **user** counts arriving
without a denominator of eligible users, a selection method, or a comparison group - they are not a
fraction of the ~200 employees, and the article distinguishes employees from external users. "Mostly
solo" and "overwhelmingly" are unquantified. The context layer had been dogfooded for only **a few
weeks** at publication, and PostHog reports no measured hallucination reduction, token savings, latency
change, or task-quality lift from it. PostHog calls governance and permissions **one of its biggest
blind spots**, and says it is interviewing users to learn more.
Findings may depend heavily on PostHog's low-hierarchy culture and need not transfer to organizations
with strict role-based access control.

## Raw capture

- [[2026-09-29 Jina Yoon - We're Building Multiplayer AI]]

## Affected pages

- [[Context Engineering]]
- [[Agent Memory]]
- [[Agent Workflow Maturity]]
- [[Multi-Tenant Agent Architecture]]
- [[Institutional Knowledge Agents]]

## Related pages

- [[Agent Delegation]]
- [[Coding Agent Harness]]
- [[AI Agents in Production]]
- [[Agent Security and Governance]]
- [[Continual Learning for Agents]]
