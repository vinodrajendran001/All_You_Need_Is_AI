---
type: source-summary
created: 2026-10-27
updated: 2026-10-27
source_id: src-2026-10-25-rastogi-agentcore-enterprise
source_title: How to Build an Enterprise AI Agent System with AgentCore (Part 1)
source_author: Sarthak Rastogi
source_url: https://sarthakai.substack.com/p/how-to-build-an-enterprise-ai-agent
tags: [source/summary, ai-agents, security, multi-tenant, mcp]
source_ids:
  - src-2026-10-25-rastogi-agentcore-enterprise
status: active
---

# Sarthak Rastogi - How to Build an Enterprise AI Agent System with AgentCore (Part 1)

## Summary

A Substack article by Sarthak Rastogi, published 25 October 2026. It argues that an enterprise agent
system needs seven properties beyond the agent loop and maps each one to a managed service in Amazon
Bedrock AgentCore. The author discloses that he uses AgentCore at work and adds "(This isn’t any sort of
promo for AWS)". Its durable contributions are the seven-property checklist and one explicit warning:
gateway policy holds only if the gateway is the only route to the tools. The article contains no
measurements, and its platform comparisons are the author's judgment.

## Key claims

**The loop is the easy part.** "Most agents stop at the loop: model, tool, model, tool." The difficulty
starts "when you give the agent real credentials, real users and real money." The article cites, through
a secondary aggregator, a Gartner prediction that 40% of enterprises will retire or disable autonomous
agents before 2027, and a Gravitee survey of 900 executives in which 46% of teams share API keys across
agents and only 22% treat agents as entities with their own identity.

| Property | How AgentCore provides it, per the author |
| --- | --- |
| Identity propagation | The user's token is exchanged on-behalf-of (OBO) for a token scoped to that user and that downstream API |
| Isolation | A microVM per session, with dedicated CPU, memory, and filesystem; memory sanitized when the session ends |
| Deterministic authorization | A Cedar policy engine in front of every tool call at the Gateway |
| Governed tool plane | One MCP endpoint with semantic tool search, interceptors, and per-target credentials |
| Scoped memory | Short- and long-term memory partitioned by namespace |
| Observability and evals | OpenTelemetry traces, plus LLM-as-judge scoring over the same traces |
| Operability as code | Terraform resources for the control plane, with deployment by image digest |

**Delegated identity is the hardest answer and the right one.** Of the three ways a tool call can be
authorized (a shared service account, the agent's own identity, or the user's identity delegated), the
third is "the answer you want, and also the hardest to build." In AgentCore, Runtime validates the user's
token, Gateway receives it, and the Identity service's token vault performs the OBO exchange, so "the
audit trail records the chain." Uber's in-house equivalent issues short-lived, single-hop tokens carrying
the full actor chain.

**One session, one microVM.** Sessions default to a 15-minute idle timeout and an 8-hour maximum, both
configurable; a newer EC2-backed option runs up to 14 days. Billing is per second, and CPU is not billed
while the agent waits on I/O.

**A gateway is a boundary only if it is the only route.** Cedar policy filters `tools/list` per caller,
can run in `LOG_ONLY` shadow mode before `ENFORCE`, and sees arguments as well as tool names, so a rule
such as "amount ≤ 500" is possible. But "If an agent can call a runtime or MCP server directly, it skips
policy." The fix is to restrict the runtime to calls from the gateway, "Then the gateway really is the
only route." A separate gap: Bedrock Guardrails' PII and prompt-attack filters "don’t inspect tool results
or tool arguments", leaving indirect prompt injection uncovered at the model layer. The author's fix is to
run those checks inside Policy at the gateway.

**Tool descriptions are prompts.** "Remember: these tool docstrings become prompts." A vague docstring is
a bug and should be covered by evals. Gateway offers semantic tool search instead of loading every schema,
plus weighted routing for canary releases of tools. The scale reference is Uber's MCP Gateway, cited at
over 800 MCP servers and more than 5,000 tools.

**Memory is a privacy surface.** "Memory is where agents become useful and where they can become a
privacy incident." The advice is one shared memory resource with per-user namespaces rather than one per
agent, partly because of a per-region cap (150 at the time of writing).

**Observability and evals answer different questions.** "Observability tells you what the agent did.
Evals tell you whether it was any good." Online evaluation samples live sessions; dataset evaluation runs
in CI and fails the pipeline below a threshold.

**Everything that changes behavior should be a reviewable diff.** An agent's behavior is defined by a
prompt, a model, a tool list, a policy, and a memory configuration. If any can be edited by hand in a
console, you cannot answer "what changed before quality dropped?" The Terraform provider has "around 21"
AgentCore resources, and the control plane is "mostly" covered. Deliveries build once, deploy by digest,
pass an eval gate and a manual approval, and roll back by repointing the live endpoint.

## Why it matters

[[Agent Security and Governance]] gains a placement rule it can test: list every path from agent to tool,
because policy at one gateway does not govern the others. The Guardrails gap shows the same thing one
layer up: a filter that does not see tool arguments cannot stop injection carried in them.

[[Multi-Tenant Agent Architecture]] gets a managed instance of per-session isolation and per-user memory
namespaces, and an argument for delegated identity over shared service accounts.

## Tensions / open questions

- **Conflict of interest, disclosed.** The author uses AgentCore at work; rankings such as "most complete
  managed answer" and comparisons with Google, Azure, OpenAI, Anthropic, and LangSmith are judgments, not
  tests.
- **The article's own limitations are missing from the capture.** The "Where AgentCore falls short" and
  "Some other security considerations" sections are image-only, as is the platform comparison table.
- **Secondhand statistics.** The Gartner and Gravitee figures link to an aggregator site, not the
  original reports.
- **Point-in-time limits.** Timeouts, the memory cap, and the resource count are product facts "as I
  write" and will drift.
- **No implementation yet.** The code is promised for Part 2 in an open-source repository.

## Affected pages

- [[Agent Security and Governance]]
- [[Multi-Tenant Agent Architecture]]
- [[Tool Roster Economics]]
- [[Sarthak Rastogi]]
- [[Uber]]

## Raw capture

- [[How to Build an Enterprise AI Agent System with AgentCore (Part 1)]]

## Citations

- Canonical URL: https://sarthakai.substack.com/p/how-to-build-an-enterprise-ai-agent (newsletter
  tracking parameters removed).
- Published 25 October 2026 and captured 26 October. Several diagrams, code samples, and tables are
  image-only.

## Related pages

- [[Agent Security and Governance]]
- [[Multi-Tenant Agent Architecture]]
- [[Tool Roster Economics]]
- [[Model Context Protocol]]
- [[Agent Memory]]
- [[Agent Observability]]
- [[AI Agents in Production]]
- [[ByteByteGo - A Deep Dive into Salesforce's Agent Tech Stack]]
- [[Sarthak Rastogi - Making an AI Agent Production-Ready]]
- [[Sarthak Rastogi]]
- [[AI Knowledge Base Overview]]
