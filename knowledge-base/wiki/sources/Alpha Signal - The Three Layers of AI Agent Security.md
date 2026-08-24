---
type: source-summary
created: 2026-08-24
updated: 2026-08-24
source_id: src-2026-08-17-alpha-signal-three-layers-agent-security
source_title: The Three Layers of AI Agent Security - From Sandboxes to Network Proxies
source_author: Alpha Signal
source_url: https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=ec9fa5befc065772&lid=13LpyUvLNdEPAeCgd&mid=f2fbdfd6-e1a1-41bf-80b3-7c3b4d6aaf88
tags: [source/summary, agents, security, sandboxes]
source_ids: [src-2026-08-17-alpha-signal-three-layers-agent-security]
status: active
---

# Alpha Signal - The Three Layers of AI Agent Security

## Summary

Alpha Signal organizes agent defense in depth across infrastructure isolation, application/runtime controls, and network mediation. Its central premise is that prompts are not security boundaries: production systems should assume the agent process can be compromised and constrain what the surrounding environment permits.

## Key claims

- OS-level controls such as containers, Landlock, seccomp, and network namespaces constrain filesystem, process, and network behavior.
- Smaller auditable runtimes reduce attack surface but do not replace isolation.
- Layer-7 proxies can inject credentials only after policy approval and route high-risk requests through model or human review.
- Static rules should handle low-risk traffic cheaply, reserving slower semantic evaluation for ambiguous writes or data transfer.

## Why it matters

The source gives [[Agent Security and Governance]] a concrete three-plane architecture and links sandboxing to outbound network and credential control.

## Tensions / open questions

- The article is a secondary newsletter synthesis and several named incidents or product claims need primary-source verification.
- LLM-based proxy decisions add latency and their false-positive and false-negative rates are not reported.
- Human escalation may not scale at high agent request volumes.

## Affected pages

- [[Agent Security and Governance]]
- [[Coding Agent Harness]]
- [[AI Agents in Production]]
- [[Agentic Loop]]

## Citations

- Raw capture: [[2026-08-17 Alpha Signal - The Three Layers of AI Agent Security]]

## Related pages

- [[AI Builder Club - Agent Sandboxes - OS-Level Security for AI Agents (2026)]]
- [[AI Builder Club - Agent Tool Permissions - Test That Your Deny Rules Hold (2026)]]
- [[Alpha Signal]]

