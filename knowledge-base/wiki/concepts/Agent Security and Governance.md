---
type: concept
created: 2026-08-05
updated: 2026-08-26
tags:
  - concept
  - ai-agents
  - security
  - governance
source_ids:
  - src-2026-08-05-aibuilderclub-ai-agents-101-part-5
  - src-2026-08-05-aibuilderclub-mcp-security-attack-vectors
  - src-2026-08-05-aibuilderclub-agent-sandbox-os-level-security
  - src-2026-08-05-aibuilderclub-ai-agent-runaway-cost
  - src-2026-08-05-aibuilderclub-agent-tool-permissions-canary
  - src-2026-08-05-aibuilderclub-who-owns-your-ai-agents
  - src-2026-08-17-alpha-signal-three-layers-agent-security
  - src-2026-08-20-mark-russinovich-fools-gold
  - src-2026-08-21-anthropic-ai-native-sdlc
  - src-2026-08-22-grok-bot-systems-engineering-working-note
  - src-2026-08-26-alex-zhang-speculative-programmatic-tool-calling
  - src-2026-08-25-bytebytego-stealing-reasoning-traces
status: active
---

# Agent Security and Governance

Agent security and governance covers the controls that constrain an agent's real authority and make its operation accountable: runtime permissions, operating-system isolation, credential scope, ownership, logging, cost limits, review evidence, revocation, and incident response. Prompted roles and policy prose are behavioral guidance, not enforcement boundaries.

## Security boundary hierarchy

1. **Prompt and tool descriptions** influence model behavior but can be ignored, conflicted, or poisoned.
2. **Harness permissions** decide which tool calls are accepted and should emit structured denial evidence.
3. **Credentials and service policy** bound what accepted calls can reach.
4. **OS or container isolation** constrains arbitrary processes, files, network access, and persistence.
5. **Human and organizational controls** assign ownership, review, escalation, and revocation.

MCP and other composable tool ecosystems add a non-local risk: one server's descriptions or outputs can influence how the model uses another server's capabilities. Trust therefore does not compose automatically.

## Test controls, do not infer them

A permission canary needs both a damaging unguarded baseline and a guarded run that records the attempted route being denied. An intact file with no denial evidence is inconclusive: the model may simply have declined to act. Equivalent outcomes must be tested through every available route, including shell, filesystem tools, subprocesses, and delegated workers.

## Governance artifacts

Every unattended agent should have:

- one named accountable owner;
- a registry entry describing purpose, actual reach, credentials, expiry, review date, escalation contact, autonomy level, and kill switch;
- append-only intent and outcome logs;
- per-function promotion evidence and prewritten demotion triggers;
- a revocation runbook that proves old credentials fail;
- spend measured as cost per successful outcome, including evaluators, retries, sub-agents, and shared infrastructure.

## Defense in depth for compromised agents

[[Alpha Signal - The Three Layers of AI Agent Security]] sharpens the hierarchy into three enforcement planes:

1. **Infrastructure** — containers or lightweight VMs, seccomp, Landlock, filesystem boundaries, process limits, and network namespaces.
2. **Runtime** — a small auditable execution core, explicit capability checks, and per-tool policy.
3. **Network** — a Layer-7 proxy that permits known-safe traffic, denies known-dangerous traffic, injects credentials only after approval, and escalates ambiguous writes.

This architecture assumes the agent process may be compromised. Semantic model review can supplement deterministic rules but should not become the only boundary because it adds latency and uncertain error rates.

[[Mark Russinovich - Fool's Gold]] addresses a different boundary: open weights after release. Its defensive-deception proposal does not preserve refusal under weight-space attack; it attempts to deny attackers reliable hazardous output after the attack. That distinction, and its governance risks, are tracked in [[Defensive Deception for Open Models]].

## Approval as an encoded policy

[[Grok Bot Systems Engineering Working Note]] contributes the missing decision layer above the enforcement planes: **when should the agent stop and ask?** Its answer is that approval is a policy keyed on *reversibility*, decided before the first unattended run, and explicitly "not a mood" — it must not depend on how confident the agent sounds.

| Action | Default | Reason |
| --- | --- | --- |
| Read approved source | Allow | Reversible observation |
| Draft internal artifact | Allow | No external effect |
| Write reversible record | Allow + log | Recoverable |
| Send or publish externally | Ask | Reputation impact |
| Delete, pay, or change access | Human | Hard to undo |

Around it sits a **capability budget**: scope limited to approved accounts and folders, a rate ceiling on external writes, a reversibility window that retains prior values, notification on external write or denial, and stop conditions for repeated denial, unknown domains, or instructions found in untrusted content.

The same source restates prompt injection in the form that matters operationally: **emails, webpages, documents, repository issues, and retrieved text are untrusted data, and a webpage must not be able to expand permissions, change system policy, or redirect secrets.** Its minimum controls extend the three planes above with two that are easy to omit — stamp the acting identity and `task_id` *outside* model-generated content, and keep an emergency stop that disables triggers **without deleting evidence**, so an incident remains investigable. Retry budgets are bounded and unknown outcomes are inspected before repetition, which prevents a failing agent from amplifying its own damage. See [[Agent Workflow Maturity]].

[[Anthropic - The AI-Native SDLC Playbook]] shows the same principle inside a software organization, where the enforcement point moves earlier still: hooks act as build-time guardrails and deploy gates, so governance is applied **as the agent acts** rather than in a later review cycle, and managed settings constrain regulated enterprises centrally rather than per developer. The unresolved question this raises is recorded in [[AI-Native Software Development Lifecycle]] — policy now lives in repository shell scripts, and who reviews the guardrails is unaddressed.

## Open questions

- How can runtime provenance and tool-description signing become portable across agent ecosystems?
- How should organizations govern agents that inherit shared human credentials?
- Which controls can be standardized without hiding version-specific permission semantics?
- When policy is executable and lives in the repository, what protects the policy file from the agent it governs?

## Related pages

- [[Grok Bot Systems Engineering Working Note]]
- [[Anthropic - The AI-Native SDLC Playbook]]
- [[Agent Workflow Maturity]]
- [[AI-Native Software Development Lifecycle]]
- [[AI Agents in Production]]
- [[Coding Agent Harness]]
- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[Context Engineering]]
- [[Multi-Turn Evaluation]]
- [[Loop Engineering]]
- [[AI Builder Club - Build AI Agents]]
- [[Alpha Signal - The Three Layers of AI Agent Security]]
- [[Mark Russinovich - Fool's Gold]]
- [[Defensive Deception for Open Models]]
