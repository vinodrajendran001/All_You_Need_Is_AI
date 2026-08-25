---
type: source-summary
created: 2026-08-07
updated: 2026-08-07
source_id: src-2026-08-07-zach-lloyd-computer-use-verification
source_title: The computer use verification skill that every agent needs
source_author: Zach Lloyd
source_url: https://x.com/zachlloydtweets/status/2084411777354277027
tags:
  - source/summary
  - ai-agents
  - computer-use
  - evaluation
source_ids:
  - src-2026-08-07-zach-lloyd-computer-use-verification
status: active
---

# Zach Lloyd - The computer use verification skill that every agent needs

## Summary

Zach Lloyd describes computer and browser use as a reusable verification capability for software-engineering agents. A `verify-behavior` skill gives triage, implementation, and review agents two explicit modes: reproduce a reported issue and verify a requested behavior. The verifier operates the application through its user interface and captures video or screenshots as evidence.

The source's strongest idea is that computer use is more valuable inside an existing engineering workflow than as a standalone agent. It closes the loop between code changes and user-visible behavior, especially when acceptance criteria are explicit.

## Key claims

- Triage agents can reproduce UI bugs before implementation begins.
- Implementation agents can compare a running feature against product acceptance criteria and iterate when behavior diverges.
- Review agents can attach behavioral evidence to pull requests, reducing the burden of manually reproducing low-risk UI changes.
- Video is preferred to screenshots because it demonstrates end-to-end interaction rather than a static state.
- Complex user stories can be verified independently by parallel cloud agents, trading higher spend for lower wall-clock latency.
- Cloud computer use avoids stealing focus from a developer's workstation and reduces the risk of an agent interacting with unrelated local applications.

## Why it matters

This is a concrete form of the "operate the artifact" rule in [[Multi-Turn Evaluation]]. It also turns [[Agent Skill]] into a shared behavioral-verification primitive that several agents can invoke, and shows how [[Coding Agent Harness]] capabilities determine which verification procedures are possible.

## Tensions / open questions

- UI evidence proves observed behavior, not architecture, code quality, security, accessibility, or coverage of untested paths.
- Computer use is comparatively slow, expensive, and nondeterministic.
- Parallel verification reduces latency but multiplies machines, traces, and cost.
- The examples are produced on Warp's platform and should not be treated as a neutral comparison of available harnesses.
- For consequential changes, behavioral evidence should supplement rather than replace code review.

## Affected pages

- [[Multi-Turn Evaluation]]
- [[Coding Agent Harness]]
- [[Agent Skill]]
- [[Loop Engineering]]
- [[AI Agents in Production]]

## Citations

- Raw capture: [[2026-08-07 Zach Lloyd - The computer use verification skill that every agent needs]]
- Canonical URL: https://x.com/zachlloydtweets/status/2084411777354277027

## Related pages

- [[Agentic Loop]]
- [[Graph Engineering]]
- [[Agent Security and Governance]]

