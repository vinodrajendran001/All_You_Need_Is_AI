---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-08-rastogi-agentcore-enterprise-part-2
source_title: "How to Build an Enterprise AI Agent System with AgentCore (Part 2)"
source_author: "Sarthak Rastogi"
source_url: "https://sarthakai.substack.com/p/how-to-build-an-enterprise-ai-agent-258"
tags:
  - source/summary
  - ai-agents
  - agent-platform
  - aws
  - authorization
source_ids:
  - src-2026-11-08-rastogi-agentcore-enterprise-part-2
status: active
---

# How to Build an Enterprise AI Agent System with AgentCore (Part 2)

## Summary

[[Sarthak Rastogi]] follows his design essay
([[Sarthak Rastogi - How to Build an Enterprise AI Agent System with AgentCore (Part 1)]]) with an
open-source implementation at `github.com/sarthakrastogi/enterprise-agent-system`. The repo is an AWS
AgentCore platform with an IT helpdesk agent and a data-analyst sub-agent sharing one LangGraph
runtime, a Python MCP server and a Lambda tool behind AgentCore Gateway, Cedar policy, Memory, Bedrock
Guardrails, CloudWatch dashboards, alarms, and online evaluations, a Streamlit chat UI with Cognito
sign-in, and Terraform for every resource. Part 2 walks one chat message through seven steps and then
zooms into the runtime, identity, isolation, authorization, tools, memory, observability, and delivery.
Its most important change relative to Part 1 is to identity: for the platform's own tools, the gateway
vouches for the user, and on-behalf-of token exchange is reserved for third-party APIs. The author
uses AgentCore at work and says the post "isn't any sort of promo for AWS"; it reports no
measurements, and much of the code appears only as images in the capture.

## Key claims

### One chat message, seven steps

The user signs in through Cognito; the UI POSTs with an auth header and a session id; the runtime's
JWT authorizer checks signature, issuer, client id, and the agent's group rule; the session gets its own
microVM, which reads the caller from the token, recalls the user's memories, and fetches the user's
tools from Gateway "using the same token"; the agent loops; on each tool call Gateway revalidates the
token, an interceptor "stamps the real user onto the call", Cedar decides, and only then does the tool
run "with Gateway's own IAM role"; afterwards the turn is saved to Memory, metrics go to CloudWatch, and
online evaluation samples the session.

### Agents are configuration, built per request

An agent is a Python definition plus a prompt in a Markdown file, because "markdown diffs nicely in a
PR". `AgentSpec` is a frozen dataclass that validates itself; a registry auto-imports `agents/` and
rejects duplicate names, unknown sub-agents, and delegation cycles. Every agent runs the same container
image, but Terraform creates **one AgentCore Runtime per agent**, each with its own IAM role, JWT group
rule, log group, alarms, evaluation config, and version history. The agent is built per request, not
per process, because Cedar filters the tool list per user.

The runtime uses LangGraph's `create_agent`, "the same free tool-calling loop" as Strands or the OpenAI
Agents SDK; fixed workflows can set `graph_factory` instead. Choosing LangGraph over Strands loses
"a tiny lil bit of AWS convenience": Strands has one-line A2A and Browser helpers, and AWS's
config-only Harness is built on it.

### Sub-agents inherit the caller

`sub_agents=["data_analyst"]` becomes an `ask_data_analyst` tool that runs in the same process "with
the same caller": same token, same Cedar decisions, same audit identity. The cost is permission
inheritance in the other direction: `code_interpreter` is `true` for the helpdesk agent, which never
uses the sandbox, because its sub-agent runs "inside the parent's runtime", so the parent's IAM role
needs that permission too. "If a sub-agent needs its own scaling, owner or IAM boundary", it should be
its own runtime reached over A2A. In the demo, Alice asks
about working from Singapore for three weeks, a ticket for the needed approval, and the cost of **61**
unused Figma seats; the agent finds that "more than 14 days abroad needs manager and security
approval", files that ticket, and runs two sub-tasks in parallel. "The agent made the choice to pick
the tools, the order and the parallelism itself!"

### Identity: the gateway vouches; OBO only for third parties

Rastogi compares a shared service account, the agent's own identity, and delegated user identity, and
wants the third. Agents can be locked to groups with `allowed_groups`, enforced by the authorizer.
Gateway calls the platform's own tools with its own IAM role, so "the tickets Lambda never sees the
user's token"; a request-interceptor Lambda supplies the user. "The gateway vouches for the user to a
tool it trusts", which he calls reasonable for tools behind a locked-down gateway. For third-party or
OAuth-protected APIs (Graph, Salesforce, a CRM), a target with `oauth { grant_type = "TOKEN_EXCHANGE" }`
triggers AgentCore Identity's on-behalf-of exchange.

### Isolation and the only route to a tool

Rastogi cites Zenity Labs showing that prompt injection against a public-facing agent "could trigger
an SSRF to the instance metadata service and pull credentials", and advises VPC mode, least-privilege
roles, and no public network mode for sensitive work. Each session gets a microVM wiped at session end;
session ids are a `uuid4` plus 8 hex characters "to clear the 33-character minimum", so a new chat is a
new microVM. Model-written Python runs in AgentCore Code Interpreter, a separate sandbox started lazily
per agent session and reused within a chat.

Because "Cedar policy only covers traffic that goes through Gateway", the MCP runtime's resource policy
denies everyone except the gateway role, and only that role can invoke the tickets Lambda. An agent's
role has **zero** tool permissions; its base permissions are extended only by manifest flags ("An agent
without `memory=True` can't touch Memory"), and each role trusts `bedrock-agentcore.amazonaws.com` only
for this account, "which stops a confused-deputy attack".

### Authorization in Cedar, rolled out in shadow mode

Policy is default deny, forbid wins, and in `ENFORCE` mode `tools/list` shows only what the caller may
use. Employees get read tools and their own-ticket tools; only platform admins can close tickets. The
policy `depends_on` the gateway targets, so a rule naming `tickets___close_ticket` fails validation if
the target is missing. `policy_mode` defaults to `LOG_ONLY` because a subtly wrong policy, "say, a typo
in a group name", flipped to `ENFORCE` "hides every tool and every agent goes dumb at once".

### Tools, memory, observability, delivery

Gateway gives every agent one MCP endpoint. `search_type = "SEMANTIC"` adds a search tool: "With 200
tools it's how an agent finds the five that matter". "Docstrings are prompts": each says what comes
back, what to do next, and what an empty result means. Tools return `{"error": ...}` rather than
raising, because "A model can read an error and recover." The gateway role holds every credential,
which "kills the N-agents-times-M-tools secrets problem". One memory resource serves the platform,
namespaced by user.

Traces come from `opentelemetry-instrument` and the AWS OTEL distro. Each agent gets two alarms: failed turns "3 or more in 5 minutes" and p90 latency over **60** seconds
for **15** minutes. Thumbs up/down feedback is logged keyed by session id, "the join key to traces and
eval results", later usable to check "whether your LLM judges agree with your users". Online evaluation
samples **10%** of sessions with built-in LLM judges. CloudWatch struggles with "why did the agent pick
that tool on turn four?", so the OTEL exporter can target LangSmith, Langfuse, or MLflow. `deploy.sh`
validates definitions, applies the ECR repos, pushes `linux/arm64` images while skipping existing tags,
then runs the full apply.

## Why it matters

Part 2 turns the vault's AgentCore design reference into inspectable wiring. It gives
[[Multi-Tenant Agent Architecture]] a concrete identity and session-isolation pattern, makes the
gateway-only route of [[Model Context Protocol]] tools explicit, adds roster mechanics to
[[Tool Roster Economics]], supplies an operations checklist for [[AI Agents in Production]], and
records a framework trade-off for [[Agent Frameworks]]. Its security and observability details are
proposed for [[Agent Security and Governance]] and [[Agent Observability]].

## Tensions / open questions

- **The identity model changed from Part 1.** Part 1 described OBO exchange as the propagation
  mechanism; Part 2 uses gateway-vouched identity for owned tools, so those tools trust the gateway and
  interceptor rather than holding a user-scoped token. That is weaker if the gateway is compromised.
- **Part 1's argument-level controls are not shown.** Part 1 noted that Guardrails do not inspect tool
  arguments or results and proposed checks in gateway policy; Part 2 lists Guardrails and shows
  group-based Cedar rules, with no argument-level rule or tool-traffic screening in its text.
- **Part 1's delivery path is not the deploy script.** Part 1 described deploy by digest, an eval
  gate, manual approval, and rollback by repointing; Part 2's six steps contain none of these, and only
  online sampling (no offline dataset gate) is described.
- "All 7 almost one-to-one" is asserted; tenancy remains user-level, not organization-level.
- The Zenity finding is relayed through a press link; Part 2 does not say whether its own defaults
  close it.
- One fictional company, one demo transcript, no latency, cost, or evaluation results; much code is
  image-only, and one sentence about graphs is garbled ("you can use a graph only appears").

## Affected pages

- [[Multi-Tenant Agent Architecture]]
- [[Model Context Protocol]]
- [[Tool Roster Economics]]
- [[AI Agents in Production]]
- [[Agent Frameworks]]
- [[Sarthak Rastogi]]
- [[Agent Security and Governance]]
- [[Agent Observability]]

## Raw capture

- [[knowledge-base/raw/sources/How to Build an Enterprise AI Agent System with AgentCore (Part 2)]]

## Citations

- Canonical URL: <https://sarthakai.substack.com/p/how-to-build-an-enterprise-ai-agent-258>
- By Sarthak Rastogi on his Substack, published November 8, 2026; captured November 10, 2026 (email
  tracking parameters removed). Repository: `github.com/sarthakrastogi/enterprise-agent-system`.

## Related pages

- [[Sarthak Rastogi - How to Build an Enterprise AI Agent System with AgentCore (Part 1)]]
- [[Sarthak Rastogi]]
- [[Multi-Tenant Agent Architecture]]
- [[Model Context Protocol]]
- [[Tool Roster Economics]]
- [[AI Agents in Production]]
- [[Agent Frameworks]]
- [[Agent Security and Governance]]
- [[Agent Observability]]
- [[Agent Delegation]]
- [[LLM-as-a-Judge]]
