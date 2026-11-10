---
title: "How to Build an Enterprise AI Agent System with AgentCore (Part 2)"
source: "https://sarthakai.substack.com/p/how-to-build-an-enterprise-ai-agent-258?utm_source=post-email-title&publication_id=1338283&post_id=223860069&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[Sarthak Rastogi]]"
published: 2026-11-08
created: 2026-11-10
description: "Let’s build the whole thing. Open-source repo, easy to add agents and MCPs, Python, Terraform."
tags:
  - "clippings"
---
[In Part 1](https://sarthakai.substack.com/p/how-to-build-an-enterprise-ai-agent) we designed an enterprise agent system — I talked about how it needs at least these 7 things:

1. Identity propagation
2. Isolation
3. Deterministic authorisation
4. A governed tool plane
5. Scoped memory
6. Observability and evals
7. Operability as code

And that AgentCore covers all 7 almost one-to-one.

Cool. Saying that is easy though 😅

So I went and built it. Everything in this post is real code in an open-source repo: **[github.com/sarthakrastogi/enterprise-agent-system](https://github.com/sarthakrastogi/enterprise-agent-system)**. Clone it, deploy it, tell me how it goes.

---

## What’s an enterprise agent system, again?

**It’s an agent platform to that handles MCP servers, agent collaboration, state, deployment, evals, observability, and monitoring** so you can focus on building and serving your agents.

This diagram lists everything such a system should have:

![](https://substackcdn.com/image/fetch/$s_!K57N!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61c399e0-7b31-47b5-a38f-1a96412afca0_3877x3762.jpeg)

> > At work, I use AWS AgentCore — and it has enabled me to build several AI solutions. It’s been a great experience, and so I decided to write this article about why it works for me. (This isn’t any sort of promo for AWS).

I built this agent system to easily support a number of agents and MCP servers you want to add to it. As an example agent, we’ll make an IT helpdesk bot for a fake company. But you can easily add more agents as Python scripts. More on that later.

The system comes with MCP tools to search the company policies, create the ticket, etc — it can also remember things about that user next time. Just like agents, it’s also trivial to add new MCP servers.

There’s also a second agent, a data analyst, that runs Python in a sandbox. The helpdesk agent can hand work to it, and we’ll see agent collaboration too.

Here’s the full list of what’s in the repo:

- Python agent definitions
- A shared LangGraph agent runtime
- A Python MCP server and a Lambda tool, both behind AgentCore Gateway
- Cedar policy for tool authorization
- AgentCore Memory
- Bedrock Guardrails
- CloudWatch dashboards, alarms and online evaluations
- A Streamlit chat UI with SSO
- Terraform for every resource

---

## End-to-end flow

Before the details, let’s see a single chat message through the system. If you understand this, the rest of the post is just zooming into each step.

1. **Sign in.** The user logs into the Streamlit app through AWS Cognito. The app holds their access token.
2. **UI to agent.** The app sends a POST request with an auth header and a session id.
3. **Runtime check.** AgentCore Runtime’s JWT authorizer checks the signature, the issuer, the client id and the agent’s group rule. If any of those fail, the request of course doesn’t go through.
4. **Agent setup.** The session gets its own microVM running the shared image. The code reads who’s calling from the token, recalls the user’s memories, and fetches the user’s tools from Gateway **using the same token**.
5. **The loop.** The agent loops between LLM and tool until it has the answer. Text streams back.
6. **Each tool call.** Gateway validates the token again, an interceptor stamps the real user onto the call, Cedar decides whether this user may call this tool, and only then does the tool run, with Gateway’s own IAM role.
7. **After the turn.** The turn is saved to Memory, metrics go to CloudWatch, and online evaluation samples the session later.

Here’s an example run of an agent I’ve built on the system.

![](https://substackcdn.com/image/fetch/$s_!hTgI!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59f5d9f7-6b0f-44db-a0ad-a926979e4cc5_1334x505.png)

![](https://substackcdn.com/image/fetch/$s_!bWEO!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F095f2fe2-cd0e-47dd-8008-e4a864b391d0_1235x830.png)

![](https://substackcdn.com/image/fetch/$s_!i2wa!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d6eea75-2b47-46bf-8b72-7fb311596704_1278x491.png)

Let’s see if it called the tool correctly:

![](https://substackcdn.com/image/fetch/$s_!uG84!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2782d18f-b050-480c-b032-363ac669bb94_1262x622.png)

![](https://substackcdn.com/image/fetch/$s_!Rz-M!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1556c2fc-0d91-454e-9e55-ea44bc2349a0_1262x330.png)

---

## 1\. Defining your own agents

The goal: the person writing an agent should only have to say what the agent is for. Hosting, auth, tools, memory, tracing and evals should come from the platform.

This is all you have to write, to add a new agent:

![](https://substackcdn.com/image/fetch/$s_!27Dk!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff808feb8-534b-4b41-8075-29baddd7f5d4_3680x2576.png)

The prompt sits in a markdown file, because prompts are what people edit the most and markdown diffs nicely in a PR.

### How the platform runs this agent

- **It first validates it on import.** `AgentSpec` is a frozen dataclass that checks itself when you construct it. The name has to match AgentCore runtime name requirements.
- **Finds agents automatically.** A registry imports every module in `agents/` and grabs its `agent` variable. You don’t have to register agents manually. It also rejects duplicate names, unknown sub-agents and delegation cycles.
- **Exports a manifest for Terraform:**

![](https://substackcdn.com/image/fetch/$s_!cwXX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee047d56-bb30-4c50-a75d-982664b6a9f3_1691x764.png)

![](https://substackcdn.com/image/fetch/$s_!QDWR!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9c0d31c-7635-4ebd-a718-91e80cb5b242_2080x1588.png)

You’ll notice that `code_interpreter` is `true` for `it_helpdesk`, even though the helpdesk agent never touches the sandbox itself. Why? Cus its sub-agent `data_analyst` does, and the sub-agent runs **inside the parent’s runtime**, so the parent’s IAM role needs that permission too. The manifest works it out by walking each agent’s sub-agents.

Let’s see our test IT agent in action:

A user named Alice asks the IT Helpdesk agent a three-part question: what the policies say about working from Singapore for three weeks, to file a ticket for whatever approval she needs, and what 61 unused Figma seats cost a year.

![](https://substackcdn.com/image/fetch/$s_!kOOS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7af18a52-1b29-4c2a-96f9-cf109d9b0dbe_1400x2533.png)

The agent splits this into two independent sub-tasks and runs them **in parallel**. On the left it searches the policy knowledge base and finds the Remote Work policy. On the right it hands the maths to a second agent, the **Data Analyst**, which writes and runs Python to calculate it.

The helpdesk agent reads the full policy and finds that more than 14 days abroad needs manager and security approval. It files a ticket for exactly that approval, then answers with the policy steps, the ticket number and the saving.

Every tool call goes through the **gateway as Alice**. Her identity and group are checked on each call, and the ticket’s owner comes from her sign-in token.

> Note that the agent made the choice to pick the tools, the order and the parallelism itself!

---

## 2\. The runtime: one image, many agents

Every agent runs the **same container image**. But Terraform still creates **one AgentCore Runtime per agent**. Each one gets its own IAM role, JWT group rule, log group, alarms, evaluation config and version history. So you test one artifact, but each agent keeps its own permissions and its own graphs in CloudWatch.

The `bedrock-agentcore` SDK handles all of that. If your entrypoint is an **async generator**, everything you `yield` goes out as an SSE `data:` event. That’s the entire streaming setup:)

By using Langgraph instead of Strands we do lose a tiny lil bit of AWS convenience. Strands has one-line helpers for A2A and Browser, and AWS’s config-only Harness is built on it. `create_agent` is the same free tool-calling loop you’d get from Strands or the OpenAI Agents SDK: the model decides which tool to call and when it’s done. For fixed workflows (a triage classifier, say), you can use a graph only appears — an agent just has to set `graph_factory`.

### The entrypoint

It does four things: validate the input, work out who’s calling, build and stream the agent, record what happened.

![](https://substackcdn.com/image/fetch/$s_!Zrck!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8fc47f1-a26d-4ca6-9a8b-fca24e11c4de_3680x2396.png)

I don’t like to forward raw LangGraph events to the UI. They contain objects that aren’t JSON-safe, and I didn’t want the UI tied to framework internals. Instead there’s a tiny event protocol of my own:

![](https://substackcdn.com/image/fetch/$s_!wvkN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f7b59dc-3a26-4cdd-a03c-0e107202a374_3552x1228.png)

### The agent gets built per request, not per process

This one’s easy to miss. Which tools an agent can see depends on **who’s asking**, because Cedar filters the tool list per user (more on that later). So the tool list can’t be built once at startup:

![](https://substackcdn.com/image/fetch/$s_!lNih!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac06193b-68a7-4941-9a8f-4d6aa3a4f743_3552x1496.png)

### Sub-agents can be called as tools

`sub_agents=["data_analyst"]` becomes a tool called `ask_data_analyst`. The sub-agent runs in the same process, with **the same caller**, so it has the same token, the same Cedar decisions and the same audit identity as its parent.

(If a sub-agent needs its own scaling, owner or IAM boundary, don’t do it in-process. Host it as its own runtime and talk to it over A2A.)

---

## 3\. Identity

Suppose the helpdesk agent lists a user’s tickets. Whose permission does that call use?

- **A shared service account?** Easy. Also means every user gets the service account’s access.
- **The agent’s own identity?** Better for audit, but you still can’t tell which human was involved.
- **The user’s identity delegated?** The ticket system sees “Sarthak called this, through the helpdesk agent”. This is what you want. It’s also the hardest to build.

Here’s how it works in the repo. There are four steps, and the same user token travels through most of them.

![](https://substackcdn.com/image/fetch/$s_!4Cvv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2aef3985-eb96-4086-acd0-09fc6d603187_678x292.png)

![](https://substackcdn.com/image/fetch/$s_!KL0n!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F266f0c99-9781-4196-9bdf-6320c2c97be7_1831x3225.jpeg)

### Access control

Each agent’s runtime has a JWT authorizer. If the agent declares `allowed_groups`, the authorizer enforces the group claim too, so you can lock an agent to a team in config:

![](https://substackcdn.com/image/fetch/$s_!hrEl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafd80fee-2a50-4081-b2bf-df5a6e74ccca_3516x1948.png)

### The interceptor

Gateway calls my two tools using **its own IAM role**, so the tickets Lambda never sees the user’s token. So how does `list_my_tickets` know whose tickets to list? Through a Gateway **request interceptor**. It’s a Lambda that sees every MCP request before it gets forwarded.

**T** he gateway vouches for the user to a tool it trusts. For your own Lambdas and MCP servers sitting behind a locked-down gateway, that’s a reasonable trust model. **For third-party or OAuth-protected APIs** (Graph, Salesforce, your CRM), use a gateway target with `oauth { grant_type = "TOKEN_EXCHANGE" }`. AgentCore Identity then does an on-behalf-of exchange, and the API gets a token scoped to that user.

---

## 4\. Isolation: what can an agent not touch?

Isolation is an important thing to take seriously. [Zenity Labs showed that a prompt injection against a public-facing agent could trigger an SSRF to the instance metadata service and pull credentials](https://www.theregister.com/security/2026/10/09/aws-agentcore-security-undone-by-prompt-requesting-credentials/5302436). It’s important to use VPC mode, least-privilege roles, no public network mode for anything sensitive. Let’s see how we’re doing it:

### Sessions are microVMs

Every session gets its own microVM, wiped when the session ends. My job is just picking sensible lifetimes:

![](https://substackcdn.com/image/fetch/$s_!OhSr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9be5b6d-0f8e-4423-96ea-a42b91b2e0a9_2388x1136.png)

The UI makes a fresh session id per agent per chat (a `uuid4` plus 8 hex chars, to clear the 33-character minimum). **New chat = new microVM.**

### Model-written code never runs in the agent’s VM

The data analyst agent runs Python through **AgentCore Code Interpreter**, a separate managed sandbox. One sandbox session starts lazily per agent session and gets reused, so variables persist inside a chat.

### Tools can only be reached through the gateway

Remember: Cedar policy only covers traffic that goes through Gateway. If an agent could call a tool directly, policy is skipped. So the MCP server’s runtime has a resource policy that denies everyone except the gateway role:

![](https://substackcdn.com/image/fetch/$s_!-zSH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15296df3-3ae1-45b4-8a29-bda3e63ee7bf_3680x1228.png)

The tickets Lambda is the same: only the gateway role has `lambda:InvokeFunction` on it. An agent’s own IAM role has **zero** tool permissions. Its only route to a tool is the gateway, carrying the user’s token.

### Each agent gets its own, minimal role

Each agent’s role is a shared base (pull the image, write logs and traces, publish metrics) plus extra statements switched on by the manifest. An agent without `memory=True` can’t touch Memory, even if its code tried. Every role also trusts `bedrock-agentcore.amazonaws.com` only for *this* account, which stops a confused-deputy attack.

---

## 5\. Authorization: relying on Cedar, not prompts

The agent orchestrates, it doesn’t get to be the gatekeeper of tools. We use a policy engine like Cedar instead.

AgentCore Policy puts a **Cedar** policy engine in front of every tool call at the gateway:

![](https://substackcdn.com/image/fetch/$s_!XBr2!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0254d876-706f-4e4a-bebe-7c109d95cff6_3044x1136.png)

- **Default deny.** A tool nobody permits is neither listed nor callable.
- **Forbid wins.** If any `forbid` matches, it’s denied, whatever the permits say.
- **Per-user tool lists.** In `ENFORCE` mode, `tools/list` only shows what the caller may use. The model can’t be tempted by tools it can’t call, and the prompt shrinks too.

### The actual policy

Employees get the read tools and their own-ticket tools. Only platform admins can close tickets:

![](https://substackcdn.com/image/fetch/$s_!7Rl1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e001811-8601-4dcd-be1e-7d476560eace_3008x1588.png)

Also, we make the policy `depends_on` the gateway targets. The engine generates its Cedar schema from the gateway’s tools, so a policy naming `tickets___close_ticket` fails validation if the target doesn’t exist yet.

### Roll it out in shadow mode

`policy_mode` defaults to `LOG_ONLY`. If a policy is subtly wrong (say, a typo in a group name), flipping to `ENFORCE` hides every tool and every agent goes dumb at once. So: deploy in `LOG_ONLY`, read the decisions in the gateway logs, then switch to `ENFORCE`.

---

## 6\. Tools: MCPs and Lambdas

I like to inspect all the MCP tools created using [MCP Inspector.](https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector)

![](https://substackcdn.com/image/fetch/$s_!BQ5w!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F45e5bcfa-9d84-43b1-b399-be0d4ded26a4_750x232.png)

Let’s see what we’ve got:

![](https://substackcdn.com/image/fetch/$s_!crQS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc3add66-69f1-4d3d-8d2a-5f215f5a2c95_1328x786.png)

![](https://substackcdn.com/image/fetch/$s_!Kwd-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48cb639a-ce5c-4550-9d6d-380907967d30_543x801.png)

Nice. Gateway gives every agent one MCP endpoint in front of every tool:

![](https://substackcdn.com/image/fetch/$s_!ulx_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17839939-1edc-4843-b863-ef5e4e1b3954_3588x1048.png)

`search_type = "SEMANTIC"` adds a built-in search tool. With 200 tools it’s how an agent finds the five that matter without loading every schema into its context.

I wired up two kinds of target:

![](https://substackcdn.com/image/fetch/$s_!Izke!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd46d7cfd-89a4-4546-9c8b-1f2495a8a0bc_693x184.png)

### Creating a new MCP server

![](https://substackcdn.com/image/fetch/$s_!PA24!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0837c100-6ef8-49e0-9685-7c00532a1c6a_3680x2576.png)

AgentCore expects the server on `0.0.0.0:8000`, path `/mcp`, streamable HTTP. `stateless_http=True` is the recommended mode on Runtime. In Terraform it’s the same runtime resource as an agent, with `server_protocol = "MCP"`.

**Docstrings are prompts.** The model picks tools from their names, descriptions and schemas, so each docstring above says three things: what comes back, what to do next, and what an empty result means.

(The search is deliberately naive — you can swap for Bedrock Knowledge Bases or OpenSearch)

### The Lambda target

Gateway invokes the Lambda with the tool arguments as `event`, and puts the tool name in the client context as `<target>___<tool>`:

![](https://substackcdn.com/image/fetch/$s_!RveS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffff160cf-874b-4e5d-995f-0606238709a3_3680x1676.png)

Tools return `{"error": ...}` instead of raising. A model can read an error and recover.

### The gateway role holds all the credentials

Agents hold zero tool credentials. The gateway role has the lot: invoke the Lambdas and the interceptor, invoke the MCP runtime, evaluate Cedar. That kills the N-agents-times-M-tools secrets problem.

![](https://substackcdn.com/image/fetch/$s_!LR_-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafb964b8-4a92-449d-a547-f232d6231d0c_2852x2072.jpeg)

![](https://substackcdn.com/image/fetch/$s_!s5Is!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d089ca9-97b0-44e0-8b62-f4349e4b5371_2432x2044.jpeg)

---

## 7\. Memory

There’s one memory resource for the whole platform, storing records in a namespace keyed by user:

![](https://substackcdn.com/image/fetch/$s_!iYNJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e69841c-79fa-4cf5-92cd-5faf43e79486_2788x1316.png)

---

## 8\. Observability and evals

Finally, we need to know: what did the agent do, and was it any good?

### Traces

AgentCore traces need CloudWatch **Transaction Search** switched on:

![](https://substackcdn.com/image/fetch/$s_!O4YS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10ce217d-c871-4b1e-a708-42b0fc46ac67_3680x1948.png)

In the container image, `opentelemetry-instrument` plus the AWS OTEL distro gives you spans for the agent run, every LLM call (with token counts) and every tool call.

Each agent then gets two alarms: failed turns (3 or more in 5 minutes) and p90 latency over 60 seconds for 15 minutes. The dashboard uses CloudWatch `SEARCH()` expressions so it works whatever the dimensions turn out to be.

### Feedback

The thumbs up/down on each answer posts a JSON line to a CloudWatch log group, **keyed by session id**:

![](https://substackcdn.com/image/fetch/$s_!-P7x!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2e6d89eb-f160-4c18-9e9d-5d441f4623da_207x82.png)

![](https://substackcdn.com/image/fetch/$s_!jL5y!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73eb255d-3d53-447a-bec6-e3e476696506_3680x956.png)

Session id is the join key to traces and eval results. A thumbs-down turns into “show me the trace”, and after a while it’s labelled data for checking whether your LLM judges agree with your users.

### Online evaluations

Each agent gets an online evaluation config. AgentCore samples 10% of sessions and scores them with built-in LLM judges:

![](https://substackcdn.com/image/fetch/$s_!RQ4n!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9780b15b-396d-4bcf-bd45-1acd542f9db1_3552x1316.png)

CloudWatch is fine for alarms and audit, and but it’s hard to answer “why did the agent pick that tool on turn four?” LangSmith, Langfuse and MLflow are what a lot of teams use, and AgentCore lets you point the OTEL exporter at any of them.

![](https://substackcdn.com/image/fetch/$s_!pk6P!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa166d7e1-594d-4d80-a8ba-b1dbc3888dd9_2131x2906.jpeg)

---

## 9\. Terraform and the deploy script

Everything is in Terraform. There’s one file per concern in `infra/`:

- `auth.tf` — Cognito pool, client, groups
- `ecr.tf` — two immutable image repos
- `agents.tf` — per-agent role and runtime
- `mcp_servers.tf` — MCP runtime and its resource policy
- `tools_lambda.tf` — tickets Lambda, interceptor Lambda, DynamoDB
- `gateway.tf` — gateway, role, targets
- `policy.tf` — Cedar engine and policies
- `memory.tf`, `guardrail.tf`, `observability.tf`, `evals.tf`

### The deploy script

`scripts/deploy.sh` is the whole delivery process:

1. Validate the agent definitions and write `build/agents.json`
2. `terraform init`
3. Apply **only the ECR repos**
4. Build and push the `linux/arm64` images, skipping tags that already exist
5. Full `terraform apply` with both image tags
6. Write the UI config from Terraform outputs

---

## Conclusion

Thank you for reading all the way through. The repo is here: **[github.com/sarthakrastogi/enterprise-agent-system](https://github.com/sarthakrastogi/enterprise-agent-system)**.

Do try it on your sandbox AWS account and lmk how it goes, and what I should improve:)

If you have any questions, you can DM me here:

If you need help with adopting this to your own AI agent/app, you can ask me here:

This post is public so feel free to share it.