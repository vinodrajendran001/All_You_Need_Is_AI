---
type: entity
entity_kind: organization
created: 2026-10-27
updated: 2026-10-27
tags: [entity, organization, ai-agents, context-engineering, agent-security, mcp]
source_ids:
  - src-2026-10-26-bytebytego-salesforce-agent-stack
  - src-2026-09-06-rastogi-agent-observability
status: active
---

# Salesforce

## What it is

Salesforce sells business applications for sales, service, and marketing, and Agentforce is its agent
platform. In the vault's main source, the platform is a four-layer stack: Data 360 for data, Customer 360
for the business applications and their actions, Agentforce for agents, and surfaces such as a Claude chat
or Slack. That account comes from [[ByteByteGo]]'s interviews at Dreamforce 2026 with Muralidhar
Krishnaprasad (MK), President and CTO, and Khushwant Singh, SVP of Product Management.

## Why it matters here

[[ByteByteGo - A Deep Dive into Salesforce's Agent Tech Stack]] is the vault's fullest account of an
enterprise taking work out of a single agent prompt. The team found that the first Agentforce prompt
coped with up to eight instructions and then began to discard some. Four jobs now belong to dedicated
systems:

- Agent Script, compiled to an Agent Graph and run by the Atlas Reasoning Engine, runs rules as code
  before and after the model call (see [[Context Engineering]]);
- identity resolution in Data 360 links source records into a unified profile without changing them;
- the Agent Context Engine (ACE) selects, governs, and compiles what reaches the model, and promotes
  only approved facts to long-term memory (see [[Agent Memory]]);
- Agent Identity gives the agent its own token beside the user's, and an operation runs only if none of
  the user's permissions, the agent's permissions, or the data policies deny it (see
  [[Agent Security and Governance]]).

For outside agents, the Salesforce MCP server exposes a small searchable tool index instead of every
API, a pattern [[Tool Roster Economics]] compares with other gateways. Separately,
[[Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]] cites Agentforce
Observability, with session-level tracing, subagent drill-down, and export to Datadog or Arize, as a fair
counter-example to platforms that ship adoption metrics before step-level traces.

## Boundaries

Everything above is vendor description relayed by ByteByteGo. The demo company and patient are
simulated, "but according to MK everything behind it runs in production". No controlled evaluation,
before/after rate of rule violations, or answer-quality comparison is reported, and the token figures
come from one demo. The scale figure of 7 billion Agentic Work Units uses Salesforce's own unit for
counting agent work, with no further definition. The *Enterprise AI Harness* that would join these
pieces into one system is a plan. The Datadog block at the top of the capture is sponsorship, not part
of the article.

## Related pages

- [[ByteByteGo - A Deep Dive into Salesforce's Agent Tech Stack]]
- [[ByteByteGo]]
- [[Context Engineering]]
- [[Agent Security and Governance]]
- [[Tool Roster Economics]]
- [[Agent Memory]]
- [[Model Context Protocol]]
- [[Agent Observability]]
- [[Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]]
- [[Sarthak Rastogi - How to Build an Enterprise AI Agent System with AgentCore (Part 1)]]
