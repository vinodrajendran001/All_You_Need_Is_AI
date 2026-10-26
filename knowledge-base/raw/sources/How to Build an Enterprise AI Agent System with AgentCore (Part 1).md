---
title: "How to Build an Enterprise AI Agent System with AgentCore (Part 1)"
source: "https://sarthakai.substack.com/p/how-to-build-an-enterprise-ai-agent?utm_source=post-email-title&publication_id=1338283&post_id=221865550&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[Sarthak Rastogi]]"
published: 2026-10-25
created: 2026-10-26
description: "7 properties every enterprise agent system needs, and how AgentCore stacks up against them"
tags:
  - "clippings"
---
## What’s an Enterprise AI Agent System?

Most agents stop at the loop: model, tool, model, tool. That part is easy now. The hard part starts when you give the agent real credentials, real users and real money. That’s when you need an enterprise agent system — **an agent platform to that handles MCP servers, agent collaboration, state, deployment, evals, observability, and monitoring** so you can focus on building and serving your agents.

This diagram lists everything such a system should have:

![](https://substackcdn.com/image/fetch/$s_!K57N!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61c399e0-7b31-47b5-a38f-1a96412afca0_3877x3762.jpeg)

> At work, I use AWS AgentCore — and it has enabled me to build several AI solutions. It’s been a great experience, and so I decided to write this article about why it works for me. (This isn’t any sort of promo for AWS).

In a later article, I’m going to build the whole thing in an open-source repo. Everything here (agents, Python MCP servers, the gateway, CloudWatch observability, Terraform, CI/CD, a front end) will be real code you can clone, run and break. This post is the “why”. That one is the “how”.

---

## What makes an agent system prod-ready?

A prod-ready agent to take untrusted input, decides what to do with a non-deterministic model, and then acts on other systems with someone’s authority. That contains most of the risk. Everything below is a consequence of it. I’ve discussed it more here:

When it comes to an **entire agent system,** I think of it as 7 properties. If a platform can’t give you all seven, you will end up building the missing ones yourself. Which isn’t always possible if the platform is too limiting!

![](https://substackcdn.com/image/fetch/$s_!qu5c!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F135a3fe2-b626-4f23-beca-7fca68cbb76b_626x508.png)

### Why do I need this?

You may remember that Gartner predicted in May 2026 that [40% of enterprises will retire or disable autonomous agents before 2027](https://ecosistemastartup.com/?p=106258) after governance failures surfaced in prod. A Gravitee survey of 900 execs found that [46% of teams still share API keys across agents and only 22% treat agents as entities with their own identity](https://ecosistemastartup.com/?p=106258). This is the problem that a good agent platform tries to solve:)

---

## Why AgentCore

AgentCore is a set of modular managed services you need: Runtime, Gateway, Identity, Memory, Policy, Evaluations, Observability, Code Interpreter, Browser and Harness.

That modularity is great - the seven properties above map almost one-to-one onto those services, while most platforms cover three or four well and leave the rest to you.

![](https://substackcdn.com/image/fetch/$s_!Ul1t!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6142c29-58e0-4293-8111-8481387cf90c_327x369.png)

I personally know several other corporate AI teams who build with it. AWS also lists early customers including [Thomson Reuters, National Australia Bank, Ericsson, Experian, Sony and Heroku](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-is-now-generally-available).

---

## What AgentCore Offers

### 1\. Identity propagation

Suppose a customer care agent looks up a customer’s order in the CRM. Whose permission does that call use? There are three common answers:

1. **A shared service account.** Simple, and every user effectively gets the service account’s access.
2. **The agent’s own identity.** Better for audit, but still doesn’t tell you which human was involved.
3. **The user’s identity, delegated.** The CRM sees “Sarthak, via the orders agent”. This is the answer you want, and also the hardest to build.

This is how it works in AgentCore:

![](https://substackcdn.com/image/fetch/$s_!IZbK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8bb6b6af-d4c4-4631-a4b6-f6703f1afc6b_1831x3225.jpeg)

1. The front end gets a Microsoft Entra, Okta or Cognito access token for your platform API.
2. Runtime’s JWT authorizer validates issuer, audience, scopes and custom claims such as group membership. This is also where you gate who can invoke which agent.
3. The user’s JWT is forwarded to Gateway.
4. For OAuth-protected downstream APIs, Gateway asks Identity’s **token vault** for a new token via **on-behalf-of (OBO) exchange**. The result is a token scoped to that user and that downstream API.
5. The tool or API sees the human, and the audit trail records the chain.

The token vault also stores 3-legged OAuth tokens (user consent to Google, Microsoft, Salesforce), client-credentials tokens for machine-to-machine calls, and API keys. Identity is free when used through Runtime or Gateway.

![](https://substackcdn.com/image/fetch/$s_!cEcd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5cfb91a-2313-4edd-ae9f-c70f9f172fe1_3332x2052.png)

**This is a powerful idea. Similarly, Uber** issues [short-lived, single-hop JWTs that carry the full actor chain](https://forkast.news/?p=131191) through an internal security token service, so every hop knows the human and each agent between them. It’s the same idea as OBO, built in-house.

AgentCore handles identity much better than other platforms:

- **Microsoft’s Entra Agent ID** makes agents first-class directory objects with Conditional Access. That’s a better directory story than AgentCore’s, but it needs an Agent 365 licence.
- **Google** gives agents SPIFFE-based identity.
- **OpenAI’s managed agents** have no user-delegated auth. **Anthropic’s** has limited support.

If you’re deciding on identity alone and live in Microsoft-land, Azure wins (even then, AgentCore’s support for Entra is very good). For everything else on this list, AgentCore’s token vault is the most complete managed answer I’ve found on AWS.

---

### 2\. Isolation

Agents execute model-chosen actions, sometimes including generated code, driven by input you didn’t write. If two users share a process, a prompt injection in one session can be a lateral-movement path into the other.

In AgentCore, each session gets its own microVM, the same virtualization approach that Lambda uses, with dedicated CPU, memory and filesystem. When the session ends, memory is sanitized. Sessions default to a 15-minute idle timeout and an 8-hour maximum, both configurable. A newer EC2-backed option goes to 14 days for long-lived agents.

You pay per second, and CPU isn’t billed while the agent waits on I/O. Agents spend most of their time waiting on the LLM, so this matters.

---

### 3\. Deterministic authorization

It’s important that [the agent orchestrates and doesn’t act as the gatekeeper:](https://ecosistemastartup.com/aws-bedrock-agentcore-como-llevar-agentes-ia-a-produccion/) authorization should always be written outside the reasoning loop.

AgentCore Policy puts a Cedar policy engine in front of every tool call at the Gateway. Properties I like:

- **Per-user tool lists.** `tools/list` is filtered per caller, so an agent can’t even see tools its user can’t call, which also shrinks the prompt.
- **Shadow mode.** `LOG_ONLY` lets you watch what would have been blocked before you flip to `ENFORCE`. That is how you roll out policy on a live system without an outage.
- **Policy sees arguments**, not just tool names, so you can write rules like “amount ≤ 500”. See example:

![](https://substackcdn.com/image/fetch/$s_!5a3I!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F79f8dbc7-e508-4728-9882-833786e75bc7_2892x1676.png)

Although remember that this only covers traffic that goes through Gateway. If an agent can call a runtime or MCP server directly, it skips policy. So lock the back door: a JWT-auth runtime can be restricted to calls from the gateway, and a SigV4 runtime gets a resource policy allowing only the gateway role. Then the gateway really is the only route.

### The model-layer gap

> Bedrock Guardrails filters inputs and outputs at the model layer, but the PII and prompt-attack filters don’t inspect tool results or tool arguments. That leaves indirect prompt injection (a malicious instruction hidden in a web page or a CRM note) uncovered at that layer. The fix is to run Guardrails checks inside Policy at the gateway, where tool arguments are visible. My layered view:

![](https://substackcdn.com/image/fetch/$s_!ZH4x!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F018d459d-5c63-4013-beaa-d97a5659d042_618x222.png)

How it compares:

- **Azure** leans on content filters and RBAC. **Google** pairs its gateway with semantic governance.
- **LangSmith Deployment, OpenAI and Anthropic’s managed agents** have no Cedar-style policy layer. Anthropic offers domain allowlists.

---

### 4\. A governed tool plane

Tools multiply. When you start, your first AI agent may have 3 tools. The 10th agent team adds their own versions of the same 3, plus 12 more, each with its own credentials and its own docstring quality. Without a front door, you get N agents × M tools worth of secrets!

Gateway presents one MCP endpoint in front of everything your agents might call:

![](https://substackcdn.com/image/fetch/$s_!EuSt!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F29684285-893e-417b-a802-1e4ad5282f14_618x299.png)

It comes with great features that make it more than a proxy:

- **Semantic tool search.** The agent calls a built-in search tool and gets the handful of tools relevant to its task, instead of loading hundreds of schemas into context. Fewer tokens, and less chance the model picks the wrong tool.
- **Interceptors.** A request and response Lambda per gateway can rewrite or short-circuit traffic: PII scrubbing, header injection, custom authorization, audit.
- **Per-target outbound auth** (IAM, OAuth, OBO, API key), so credentials live in the vault, not in agent code.
- **Weighted routing rules** for canary releases of tools.
- One place to attach Policy, WAF, KMS and logging.

### Writing the tools

A tool author’s job is small. This is a complete MCP server:

![](https://substackcdn.com/image/fetch/$s_!DIAz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a2aa10e-5c60-4d8e-a8e6-57d7108b5abc_2892x1600.png)

Deploy it on Runtime with the MCP protocol flag and it gets the same isolation, auth and tracing as an agent. For small stateless tools, a Lambda target is cheaper and needs no container.

Remember: **these tool docstrings become prompts.** The model picks tools from **names, descriptions and schemas**, so a vague docstring is a bug. Cover tool descriptions with evals.

#### Uber’s MCP Gateway

Uber’s engineering team published the best public example of this problem at scale. Their [MCP Gateway](https://www.uber.com/blog/designing-mcp-gateway/) hosts over 800 MCP servers and more than 5,000 tools. The design splits into:

- **A registry (control plane):** catalog of servers, tools, ownership and enablement state.
- **A proxy (data plane):** translates MCP into the HTTP, gRPC and TChannel calls Uber’s services already speak.
- **AutoCrawler:** a workflow that watches Uber’s service schema registry and generates MCP definitions as APIs change, so nobody hand-writes wrappers.

Uber built that over a long time with a big team. AgentCore Gateway plus Registry gives you the same shape (registry, proxy, centralized auth) as a managed service.

![](https://substackcdn.com/image/fetch/$s_!tBPE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9585f5f3-678d-44df-b7c4-c5caa69dde85_2852x2072.jpeg)

![](https://substackcdn.com/image/fetch/$s_!-D9L!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82b5ee83-52de-4d4c-862f-ea31c4e3cd8d_2432x2044.jpeg)

---

### 5\. Scoped memory

Memory is where agents become useful and where they can become a privacy incident. A fact the agent learned about Sarthak must never surface for anyone else.

**What AgentCore does:**

- **Short-term memory** stores raw conversation events by user and session, with configurable expiry.
- **Long-term memory** runs strategies that extract records asynchronously: facts (semantic), summaries, user preferences, and episodic memory with reflection. You can override prompts or models, or run self-managed strategies where AgentCore hands you batches and you write the records back.
- **Encryption** with customer-managed keys.
- **Namespaces** partition everything.

![](https://substackcdn.com/image/fetch/$s_!PPsF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3005d9e6-f968-4923-bb33-6804d4a94b4a_2892x1152.png)

Practical advice: use **one shared memory resource with per-user namespaces**, not one memory per agent. There’s a cap on memories per region (150 as I write), and a shared store lets you reason about retention and encryption once.

---

### 6\. Observability and evals

Observability tells you what the agent did. Evals tell you whether it was any good. You can learn more about both here:

#### Observability

AgentCore emits OpenTelemetry-native traces, metrics and logs. With the OTEL distro installed in the agent image, frameworks like Strands, LangGraph and CrewAI emit spans for the agent loop, each LLM call (with token counts) and each tool call. Those land in CloudWatch’s GenAI Observability view, correlated by session id. Gateway and Memory logs need a vended-log delivery you configure.

CloudWatch is fine for alarms and audit. I find LangSmith to be nicer to inspect why an agent did something. You can point OTEL at any of them, at the cost of the CloudWatch dashboard and Evaluations. AWS has samples for Langfuse, Datadog, Arize, Honeycomb and Dynatrace.

#### Evals

AgentCore Evaluations runs LLM-as-judge scoring over the same traces. There are built-in evaluators at three levels:

![](https://substackcdn.com/image/fetch/$s_!-mU0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06a36fdf-4f1f-4cdd-8ab3-153c480decb9_588x154.png)

You can add custom judges (LLM or Lambda) and use RAGAS, DeepEval or Autoevals through the SDK. It runs in two modes:

- **Online:** sample a percentage of live sessions continuously, so quality becomes a metric you can alarm on.
- **Dataset or on-demand:** run a fixed set of cases in CI, wait for traces to land, score, and fail the pipeline below your thresholds.

![](https://substackcdn.com/image/fetch/$s_!XALd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc794324-8bbc-4ce6-a8c2-2bfb6d102c9b_2892x1420.png)

Here’s how the online evaluation flow looks:

![](https://substackcdn.com/image/fetch/$s_!3ioW!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe331e557-559f-4b9c-9bb1-22c0064326b6_2131x2906.jpeg)

---

### 7\. Operability as code

Every runtime, gateway target, policy, memory strategy and alarm can be declared in Terraform, reviewed in a PR and applied by CI. That rule only works if the platform exposes its whole control plane as resources, and AgentCore mostly does. One `terraform apply` can build the entire system in an empty account, and one `git revert` can undo a change to it.

You can read more about CI/CD pipelines for agents here:

This matters more for agents than for most workloads. An agent’s behaviour is defined by a prompt, a model, a tool list, a policy and a memory config. If any of those can be edited by hand in a console, you can’t answer “what changed before quality dropped?” Terraform turns each of them into a diff with an author and a reviewer.

The provider has around 21 AgentCore resources, all prefixed `aws_bedrockagentcore_`. Combined with ordinary AWS resources, every layer of the platform is covered:

![](https://substackcdn.com/image/fetch/$s_!tr5g!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b19cb19-5fdf-4416-86c1-889c51456009_1114x1638.png)

### The delivery pipeline

- Build the agent image once, tag it with the git SHA, deploy **by digest**.
- Promote the *same digest* from dev to prod. Never rebuild for prod.
- AWS access via OIDC, scoped per environment, with no long-lived keys.
- An **eval gate** between dev and prod, then a manual approval.
- Prompt-only changes need no image build:
	1\. YAML change
	2\. new S3 object version
	3\. new runtime version.
- Rollback is repointing the `live` endpoint.

---

## Some other security considerations

These are the things security and compliance will ask about:

![](https://substackcdn.com/image/fetch/$s_!cVmz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9225094-fc4d-494b-85ad-7508b9728b63_606x457.png)

---

## Comparing AgentCore to other platforms

The table below compares 4 options, but here’s my take:

- **Google’s platform** is the most credible alternative. Near-parity on features, slightly cheaper compute with a free tier, active Terraform support. Its downsides are rebrand churn and uneven regional coverage.
- **Azure Foundry** wins on directory identity, M365 and Teams distribution, and the maker UI.
- **OpenAI and Anthropic’s managed agents** are the quickest start and the weakest enterprise fit today: beta, single vendor, no Terraform, limited residency and retention options. I’d use the Claude Agent SDK as a *library* on AgentCore Runtime instead.
- **LangSmith Deployment** is excellent for developer experience, durable threads, tracing and evals, and thin on identity and policy. It can be a good companion to AgentCore rather than a replacement.
	![](https://substackcdn.com/image/fetch/$s_!Ax0q!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47e6e84a-d315-42a6-abb7-e52356610017_492x649.png)

---

## Where AgentCore falls short

![](https://substackcdn.com/image/fetch/$s_!qNoN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9845f232-2ddb-40ac-8630-14f851f60d01_608x303.png)

---

## Summary

Here’s everything AgentCore offers, that you need for an enterprise agent system.

![Generated image 3](https://substackcdn.com/image/fetch/$s_!jnoq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd511cd97-62e7-4810-ab55-8fa2ce34afae_1536x1024.png)

Generated image 3

---

## Up next: the open-source repo

In the next article I’ll build and share all of this in a public repo: the YAML-driven agent runtime, a few Python MCP servers, the gateway with Cedar policy, memory, CloudWatch dashboards and alarms, evals in CI, the Terraform modules, the pipeline and the Streamlit UI. If there’s something you want covered or a use case you’d like it to handle, reply or leave a comment.

---

If you have any questions, you can DM me here:

If you need help with adopting this to your own AI agent/app, you can ask me here:

This post is public so feel free to share it.