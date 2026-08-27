---
type: source-summary
created: 2026-08-25
updated: 2026-08-26
source_id: src-2026-08-21-anthropic-ai-native-sdlc
source_title: The AI-Native SDLC Playbook
source_author: Anthropic Applied AI team
source_url: https://claude.com/blog/the-ai-native-sdlc-playbook
tags: [source/summary, sdlc, coding-agents, governance, enterprise]
source_ids: [src-2026-08-21-anthropic-ai-native-sdlc]
status: active
---

# Anthropic - The AI-Native SDLC Playbook

## Summary

Anthropic's Applied AI team argues that agentic coding has moved the software bottleneck off the build phase and onto the human-speed stages either side of it — plan, review, test, and deploy. The playbook proposes rebuilding the software development lifecycle as a **loop of committed artifacts** rather than a linear chain of documents and sign-offs. Each of the six stages (Plan, Design, Build, Test, Deploy, Maintain) ends by writing one machine-readable artifact to version control, and the commit of that artifact triggers the next stage. The stage content is delivered as modular "plays," each with prerequisites, execution steps, governance considerations, and a success measure, arranged in a dependency graph rather than a fixed sequence.

## Key claims

- **Code is no longer the bottleneck.** When build collapses to hours while surrounding stages stay at human speed, three things follow: the constraint moves to plan/review/deploy; line-by-line controls stop matching reality once agents write most of the diff; and governance costs rise because exceptions still route through weekly or monthly committees.
- **The committed artifact is the unifying mechanism.** `intent.md`, `spec.md`, `plan.md`, the diff and its tests, the PR with its review findings, and the incident record form a chain that is simultaneously the handoff protocol and the audit trail — who asked for what, what the agent produced, and who approved it.
- **Early-stage artifacts are deliberately Markdown** because a product owner and an agent can both read and act on the same file; from Build onward the artifact is code and its records.
- **Institutional knowledge becomes versioned files.** `CLAUDE.md` encodes commands, conventions, architecture, and an explicit "things Claude gets wrong" section; `.claude/skills/*/SKILL.md` encodes recurring procedures such as secure API review.
- **Governance shifts from review-time to act-time.** Hooks act as build-time guardrails and as deploy approval gates (e.g. a `production-gate.sh` requiring a named release authorization), and managed settings constrain regulated enterprises centrally rather than per developer.
- **Review is layered, not uniform.** Agentic review passes run first against a committed `REVIEW.md` that defines passes, what "important" means, a cap on nits, and an explicit do-not-report list; scarce human review is reserved for regulated and critical code.
- **Testing becomes continuous evals in CI** (an `agent-evals.yml` workflow) plus an in-repo verification block, replacing QA gates at stage boundaries.
- **Maintain closes the loop.** Agents monitor live deployments against control bands defined in a `bands.yaml`; a breached band is diagnosed and written back as the next `intent.md`.
- **Adoption is a dependency graph, not a maturity ladder.** Plays with no inbound arrows can be started immediately; every other play names its prerequisites.

## Why it matters

This is the most concrete vendor description in the vault of what happens to an *organization's* process — not just an individual developer's workflow — when [[Coding Agent Harness|coding agents]] become the default build mechanism. It supplies the missing organizational layer above [[AI Agents in Production]]: where earlier sources describe how to make one agent reliable, this one describes how to make a company's approval, review, and audit machinery keep up with agents. It also gives [[Agent Skill|skills]] and `CLAUDE.md` a governance justification rather than only an ergonomic one, and it is the anchor source for [[AI-Native Software Development Lifecycle]].

## Tensions / open questions

- **This is vendor material.** Every play is expressed in Claude Code primitives (`CLAUDE.md`, skills, hooks, subagents, managed settings, Claude Tag). The underlying pattern — artifact-triggered stages with enforcement at act-time — is portable, but the evidence offered is Anthropic's own consulting practice, not independent measurement.
- **No effect sizes are reported.** Each play names "how you measure whether it worked," but the document supplies no baseline data, control group, or before/after numbers for any customer.
- The claim that agentic review plus reserved human review preserves accountability in regulated settings is asserted rather than demonstrated against any specific regulatory regime.
- Making the commit chain the audit trail assumes the agent's stated rationale in an artifact faithfully reflects what it actually did — the same evidence-versus-claim gap that [[Grok Bot Systems Engineering Working Note]] addresses with an explicit evidence ladder.
- Hooks as enforcement move policy into shell scripts inside the repository, which raises the question of who reviews the guardrails themselves.

## Affected pages

- [[AI Agents in Production]]
- [[AI-Native Software Development Lifecycle]]
- [[Agent Security and Governance]]
- [[Agent Skill]]
- [[Agent Workflow Maturity]]
- [[Anthropic]]
- [[Coding Agent Harness]]

## Citations

- Raw capture: [[2026-08-21 Anthropic - The AI-Native SDLC Playbook]]
- Canonical URL: https://claude.com/blog/the-ai-native-sdlc-playbook
- The guide credits Jim Blackhurst, Will Steuk, and Jamal Arif for prior work it builds on.

## Raw capture

- [[2026-08-21 Anthropic - The AI-Native SDLC Playbook]]

## Related pages

- [[Context Engineering]]
- [[Loop Engineering]]
- [[Multi-Turn Evaluation]]
- [[Agent Workflow Maturity]]
