---
type: source-summary
created: 2026-10-27
updated: 2026-10-27
source_id: src-2026-10-26-bytebytego-salesforce-agent-stack
source_title: "A Deep Dive into Salesforce’s Agent Tech Stack"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/a-deep-dive-into-salesforces-agent
tags: [source/summary, ai-agents, context-engineering, security, mcp]
source_ids:
  - src-2026-10-26-bytebytego-salesforce-agent-stack
status: active
---

# ByteByteGo - A Deep Dive into Salesforce's Agent Tech Stack

## Summary

A ByteByteGo newsletter article, published 26 October 2026, based on interviews at Dreamforce 2026 with
Salesforce's Muralidhar Krishnaprasad ("MK"), President and CTO, and Khushwant Singh, SVP of Product
Management for the AI application development platform. It explains how Agentforce moved from one large
prompt to a layered design. The prompt used to be asked to do four jobs: enforce the rules, work out who
the customer is, include the right data, and keep the agent within its permissions. Each job now belongs
to a dedicated system.

The durable contribution is that decomposition, plus one concrete token comparison. The evidence is
vendor interviews and a demo: the healthcare company and patient are simulated, "but according to MK
everything behind it runs in production." There is no controlled evaluation.

## Key claims

**The redesign started from an instruction limit.** The first Agentforce kept every instruction in one
prompt. The team found "this worked fine for up to eight instructions. But beyond eight, the model would
discard instructions." That is a team observation with no described test. The article adds a third-party
benchmark: IFScale tested 20 models with up to 500 simple instructions in one prompt, and "even the best
model followed only 68% of them at the full 500." The conclusion it draws: "So a prompt only tries to
shape the behavior of the LLM. It cannot enforce that behavior."

**Four jobs, four systems, four layers.** The platform stack is Data 360 (data), Customer 360 (business
applications and actions), Agentforce (agents), and surfaces such as Slack or a Claude chat.

| Job taken out of the prompt | System that now does it |
| --- | --- |
| Enforce the rules | Agent Script, compiled to an Agent Graph and run by the Atlas Reasoning Engine |
| Work out who the customer is | Identity resolution in Data 360 |
| Decide which data reaches the model | Agent Context Engine (ACE) |
| Keep the agent within its permissions | Agent Identity |

**Rules run as code around the model.** Agent Script is open source and "looks almost like Python". Each
subagent has a `before_reasoning` block that runs before the prompt is built (for example, an appointment
lookup that therefore always happens) and an `after_reasoning` block that can hand the conversation to
another subagent. The article compares this to SQL triggers, which the calling application cannot skip.
Its rule of thumb: "use code for the parts we want predictable behavior, such as conditions, and use
natural language for the parts that need actual reasoning."

**Identity is resolved before the model sees anything.** Data 360 reads sources directly; in the demo, a
change made in Snowflake appeared immediately. It maps each source onto a shared data model (MK says this
mapping is automatic and "works across thousands of sources"), then applies admin-configured exact, fuzzy,
or normalized match rules. Source records are never changed; the output is a unified profile that links
back to each of them.

**A six-step context engine, with one token comparison.** ACE resolves (user, agent, purpose, entities),
plans where to look, reconciles and ranks findings, governs (access, masking, consent), compiles working
state and memory, and learns what to remember. In MK's insurance-agent demo:

| Same conversation | Without context management | With ACE |
| --- | --- | --- |
| "show me details of my insurance plan" | 124,000 tokens | 9,000 tokens |
| After a follow-up about moving to Florida | About 300,000 tokens over two questions | 65,000 tokens after a third step that processed an enrollment |

The two sessions did not cover the same number of steps, and answer quality is not reported. ACE also
separates tentative memory from facts: a note that a customer may be moving to Florida is "a memory, not
yet a fact" until the customer enrolls, and "only approved facts like this are promoted into long-term
memory."

**The agent gets its own identity, not the user's.** The customer requirement, in Khushwant Singh's words:
"This agent is working on behalf of Alex, but I don’t want the agent to have the same rights as Alex."
With Agent Identity, authentication yields two tokens, one for the agent and one for the user it acts for.
An operation runs only if none of the user's permissions, the agent's permissions, or the data policies
deny it.

**Outside agents reach Salesforce through a small tool index.** AIforce and the Headless Toolkit expose
APIs, skills (which list the APIs, parameters, and order of steps a task needs), and the Model Context
Protocol (MCP). "Salesforce’s APIs already serve 9.6 billion calls a day". To keep tool definitions out of
the context window, "The Salesforce MCP Server works this way with just four tools": `discover` runs a
semantic search over APIs and skills, `describe` returns a skill's contract, and `dispatch` routes the
call and checks the user's access. Only three of the four tools are named.

**Scale, in the company's own unit.** Salesforce agents have completed 7 billion Agentic Work Units, 3.2
billion of them in its second quarter. The unit is Salesforce's own and is not defined further.

## Why it matters

[[Context Engineering]] gains an enterprise decomposition. Rules, identity, retrieval, and permissions
each leave the prompt for a component that can be tested on its own, and the model reasons over what those
components hand it.

[[Agent Security and Governance]] gets a two-principal authorization model. The agent is neither a
service account nor a copy of the user; every operation must pass both principals and the data policy.

[[Tool Roster Economics]] gets another instance of replacing a large tool roster with a search tool
followed by a dispatch tool.

## Tensions / open questions

- **Vendor claims through a secondary explainer.** The eight-instruction observation has no method,
  sample, or model named; IFScale's model identities and setup are not given here.
- **The token figures are one demo** in which the two sessions covered different numbers of steps, with
  no answer-quality comparison.
- **Unmeasured reliability.** The redesign was motivated by dropped instructions, but no before/after
  rate of rule violations is reported.
- **Advertising is not evidence.** The capture opens with a sponsored Datadog block ("Only 30% of AI
  agent pilots reach production") that is not part of the article.
- **Roadmap, not product.** Salesforce's next step, a single "Enterprise AI Harness", is described as a
  plan.

## Affected pages

- [[Context Engineering]]
- [[Agent Security and Governance]]
- [[Tool Roster Economics]]
- [[ByteByteGo]]
- [[Salesforce]]

## Raw capture

- [[A Deep Dive into Salesforce’s Agent Tech Stack]]

## Citations

- Canonical URL: https://blog.bytebytego.com/p/a-deep-dive-into-salesforces-agent (newsletter tracking
  parameters removed).
- Published 26 October 2026 and captured 27 October. ByteByteGo is the publisher; the article has no
  individual byline. Diagrams are image-only.

## Related pages

- [[Context Engineering]]
- [[Agent Security and Governance]]
- [[Tool Roster Economics]]
- [[Model Context Protocol]]
- [[Agent Memory]]
- [[Agent Skill]]
- [[Multi-Tenant Agent Architecture]]
- [[ByteByteGo - How DoorDash Built a Toolbox for AI Agents]]
- [[Sarthak Rastogi - How to Build an Enterprise AI Agent System with AgentCore (Part 1)]]
- [[Salesforce]]
- [[ByteByteGo]]
- [[AI Knowledge Base Overview]]
