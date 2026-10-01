---
title: "How DoorDash Built a Toolbox for AI Agents"
source: "https://blog.bytebytego.com/p/how-doordash-built-a-toolbox-for?utm_source=post-email-title&publication_id=817132&post_id=217162538&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-09-30
created: 2026-10-01
description: "In this article, we will look at how the DoorDash engineering team built this gateway and the decisions they made."
tags:
  - "clippings"
---
## CodeAF: a new open-source factory on the Pareto frontier (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!dh1L!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7abed54e-1a7a-42b8-a6e5-1aab6fae128d_1600x840.png)

CodeAF is a new open-source software factory that sits on the Pareto frontier of cost, speed and quality. On DeepSWE it solved nearly 4× as many real GitHub issues as Claude Code on the same open model, and matched the official leaderboard result at half the cost.

It is built from the ground up for the next era of coding, where you stop chatting with agents and start directing them. Built for open models like DeepSeek, Qwen, GLM and Kimi, it gives you frontier-grade coding without locking you into a closed model, and it still works with any provider you choose.

---

The utility of AI agents increases when they can take real actions in real systems. This involves the use of tools. While MCP made it easier to expose these tools, there were a lot of other concerns that had to be handled in order to make it work at an enterprise level.

DoorDash built a shared Agent Gateway to control how AI agents discover and use tools. The gateway brings together several responsibilities: checking permissions, managing credentials, choosing which tools an agent can see, forwarding requests, and recording what happened.

In this article, we will look at how the DoorDash engineering team built this gateway and the decisions they made. Here’s what we will cover:

- Why does an AI agent need tools
- Why MCP is not enough
- The core components of the gateway
- Verifying who is calling and what they can do
- Why identifying the caller is different from supplying credentials
- How a user connects an account during a tool call
- Why agents should see a tool catalog
- What happens during discovery and execution
- How DoorDash made the platform easy to adopt

![](https://substackcdn.com/image/fetch/$s_!bqfH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F277ea700-31bf-4b5f-9095-7ec2987d4c39_4222x2484.png)

*Disclaimer: This post is based on publicly shared details from various sources. References at the end. Please comment if you notice any inaccuracies.*

## Why an AI Agent Needs Tools

A language model can write a super-detailed explanation of how to investigate a software problem, but it doesn’t automatically have access to a company’s code repositories, incident reports, or production logs. We need to provide access to those systems through software. From the perspective of the model, these systems are like tools.

An AI agent is an application that uses a language model to decide which steps and tools to use while working on a particular task. A tool is a specific capability that the application makes available to the model. For example, searching documentation, reading a support ticket, and opening a pull request.

When the model selects a tool, the surrounding application uses the tool to execute the required operation and supplies the result back to the language model. The model can then use that result to decide what to do next. For example, an agent investigating a failed software build might retrieve the build logs, inspect relevant code, and use what it finds to explain the failure.

Some tools only read information. Others can also change something in a real system, such as updating a ticket or creating a pull request. This makes tool access a very important part of an agent’s design. It determines what the agent can learn and what it can eventually do with that learning. At DoorDash, these capabilities come from many places, including internal services, engineering systems, documentation platforms, and third-party software.

## Why MCP Is Not Enough

Different systems or tools normally expose different interfaces. An API is a way for one program to request information or actions from another program. Without a shared approach, an AI agent application has to accommodate the particular interfaces of every tool it uses.

The Model Context Protocol (MCP) provides a common way to describe, discover, and invoke capabilities. An MCP server exposes tools, and an MCP client communicates with that server. The agent application uses an MCP client to access the tools.

![](https://substackcdn.com/image/fetch/$s_!Qqu6!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa8005ca4-2bb3-4c44-a0c8-8a90807d7cad_3836x2484.png)

This is largely facilitated by two main operations:

- The first is tools/list, which discovers the tools available from a server. The returned catalog gives the agent information about the available capabilities, including their names, descriptions, and expected inputs.
- The second is tools/call, which requests execution of a particular tool with the supplied inputs.

For example, a server might expose a tool for looking up an issue in the issue tracker. A discovery service tells the agent that this capability exists and how to request it. Invocation asks the server to perform a specific lookup.

Such a shared interface makes integration simple. However, DoorDash still had to decide which agents can use which tools, whose account an action should use, and how access should be monitored. A coding agent might need access to GitHub, Jira, code search, documentation, and systems that show production behavior. Each connection introduces decisions about permissions, credentials, available operations, and monitoring.

This makes the problem of tool access not just a matter of connection. Also, there are a bunch of company-specific rules that come into the picture here. MCP’s common interface doesn’t establish those company-specific rules. If every team implements these responsibilities independently, the same work gets repeated across many agents and servers. For example, one team might build an OAuth connection flow, another might develop its own secret handling, and another creates a different way to record tool usage. It becomes quite difficult to maintain consistent behavior.

DoorDash organizes this problem into three separate concerns:

- **Access:** Deals with the identity and permissions behind a request. The platform needs to know who is calling, what that caller is allowed to do, and which credentials the downstream system requires. For example, an agent acting on behalf of an individual employee may need a different credential arrangement from an automated process running for an entire team.
- **Tool-surface Curation:** This concern handles the capabilities presented to the agent. A downstream server might offer hundreds of tools, while a particular workflow only needs a small subset. DoorDash needed a way to select the relevant, approved tools instead of exposing the entire catalog.
- **Operations:** This concerns what happens when these integrations run in production. Teams need to understand traffic, failures, response times, usage, and costs. They also need controls that prevent excessive requests from overwhelming downstream systems.

The Agent Gateway brings all of these concerns and responsibilities into a shared platform. Let’s look at that in more detail.

## The Core Components of the Agent Gateway

A gateway is a service through which requests pass before reaching their destination.

In DoorDash’s design, an agent sends its MCP requests to the Agent Gateway, which controls access and forwards approved requests to the appropriate downstream MCP server. Here, downstream simply means the system that receives a request after the gateway forwards it.

![](https://substackcdn.com/image/fetch/$s_!7lqu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b76d61c-a0fc-460b-ac04-f066d991e32d_4414x2890.png)

There are two core components involved here: a proxy and a registry.

The proxy handles requests as they arrive. It verifies the caller, checks permissions, applies rate limits, attaches the required credentials, and forwards the request. It also produces information used for monitoring and auditing. Since it handles the actual request traffic, it is considered part of the data plane.

The registry stores the information needed to govern the incoming traffic. This includes details about the registered agents and MCP servers, ownership details, connection settings, authentication modes, policies, discovered tool catalogs, and configurations that determine which tools are exposed.

The registry is the source of truth for the control plane, which manages how the system should operate. The engineering teams use a management interface and API to configure the gateway, while the proxy applies the resulting configuration to requests.

This division between the two components separates the work of configuring access from the work of handling traffic. A tool owner can register a capability and attach policy through the control plane. The proxy then enforces that policy when the AI agents need to use the capability.

DoorDash also separates internal workflows and external-facing use cases into different proxy planes. They share libraries and registry concepts. But they maintain separate trust boundaries. Think of it as a common governance approach without implying that every request passes through one physical proxy instance

## Verifying Who is Calling and What They Can Do

Two closely related concepts play a key role in the Agent Gateway built by the DoorDash engineering team. These concepts are authentication and authorization.

Authentication establishes the identity of the caller making the request. A request might come from a user, a software service, or an agent acting on behalf of a user. Authorization determines what that identified caller is allowed to do.

These checks need more information than simply deciding whether someone can access an entire MCP server. A server may expose both harmless lookup operations and powerful administrative actions. The distinction between the two should be clear. For example, permission to search a repository should not automatically imply permission to use every operation the server provides.

DoorDash’s agent gateway can evaluate permissions involving several pieces of context. It can consider the agent, the user, the requested tool, and the environment in which the request occurs. It can also distinguish access to read-only capabilities from access to capabilities that modify data. For example, a policy might allow an agent to read issue details on behalf of a user while preventing that agent from performing administrative operations. Another workflow might be allowed to run under a team identity, while a user-specific action requires the individual user’s authorization.

The agent gateway carries the identity of the caller through the rest of the request process, including routing and recording usage. That makes it possible to attribute a downstream action to the context that caused it.

Centralizing these decisions also gives DoorDash a shared place to change or revoke access if needed. Agent developers don’t have to encode security decisions in prompts. Also, each tool owner doesn’t have to rebuild the same gateway-level authorization logic.

## Why Identifying the Caller is Different from Supplying Credentials

Even after the agent gateway knows who is making a request and whether it is allowed, the downstream system may require its own credentials.

A credential is something used to establish identity or access, such as an API key or an access token. The identity used to enter DoorDash’s gateway and the credential required by a third-party service are separate parts of the request.

For instance, the gateway may recognize an employee through the internal identity system. However, a documentation provider may still require that employee’s authorization token before it allows access to their documents. There are four types of credential arrangements that are possible:

- **Internal Service Identity:** This is an identity verified by the DoorDash infrastructure. It forwards verified caller context to internal services.
- **Gateway-held Token:** This is a vendor or service token kept in gateway secret storage. It adds the token to the downstream request without giving it to the agent.
- **Per-user OAuth:** This is for access that a particular user has granted to an external service. The gateway stores the grant securely, supplies the user’s token, and refreshes it when needed.
- **Service Principal:** This is a non-personal identity used by software or team automation. The gateway obtains or issues short-lived credentials through a gateway-managed team identity.

Credential injection means adding the appropriate credential to the outgoing request before forwarding it. The agent asks to use a tool. The gateway handles the credential needed to access the system behind that tool.

The design created by the DoorDash engineering team keeps raw downstream credentials, including vendor keys and OAuth refresh tokens, out of the agents. This gives the platform a central place to manage, rotate, audit, and revoke those credentials.

## How a User Connects an Account During a Tool Call

Some tools need to act within a particular user’s account. For example, reading that user’s documents or updating a ticket as that user requires appropriate user authorization.

OAuth is a mechanism through which a user authorizes an application to access a service with specified permissions. The application receives tokens that it can use for the authorized access.

The access token is used when making requests. A refresh token, when issued, allows the application to obtain a replacement access token when the current one expires.

Before the agent gateway, the product teams within DoorDash tended to build their own connection flows and token storage. However, the gateway centralizes this work.

When a call needs authorization that is not yet available, the gateway starts the provider’s OAuth flow. After the user authorizes access, the gateway stores the resulting tokens in encrypted form and supplies the appropriate token on future calls.

For clients that support MCP elicitation, the gateway can ask the client to present a connection prompt while keeping the original tool request open. The user completes authorization in a browser. The gateway then obtains and stores the token, resumes the original request with that token, and returns the result from the tool.

![](https://substackcdn.com/image/fetch/$s_!7AUq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a761ae9-967c-4c03-96c8-40f350ef4064_4222x2484.png)

To clarify things here, elicitation is the protocol mechanism used to request the user interaction needed to continue the task. The user completes the provider’s authorization flow. However, the agent doesn’t receive the raw credential.

For clients without elicitation support, the gateway returns a structured response explaining that authorization is required, along with a connection URL. This gives the client a clear way to recover, even though it cannot use the same pause-and-resume interaction.

## Why Agents Should See a Selected Tool Catalog

Permissions determine which actions are allowed, but the tool surface shown to an agent also affects its behavior.

Tool surface means the set of tools presented to an agent, including their names, descriptions, and organization. A server’s complete catalog may contain administrative functions, billing operations, destructive actions, and features unrelated to the agent’s task. Presenting all of those capabilities creates unnecessary choices. The model has more descriptions to interpret and more potentially similar tools to distinguish. The approach used by the DoorDash engineering team is to expose smaller, relevant catalogs that match the work being performed.

There are two mechanisms behind this: bundles and filters.

![](https://substackcdn.com/image/fetch/$s_!c2oD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fddc1b88f-d353-442e-8fa7-ba7d06071dce_4634x3158.png)

A bundle combines tools from multiple MCP servers behind one logical MCP endpoint. An endpoint is the address to which the client sends requests. For example, a developer-tools bundle can provide selected GitHub, Jira, observability, code-search, and documentation capabilities through one gateway address. The tools still run through their respective downstream servers. However, the bundle gives the agent one organized interface through which to discover and use them.

Filters determine which tools appear in that interface. Their decisions can depend on the bundle, agent, user group, environment, or intended audience. A provider might expose both issue lookup and administrative operations, while a particular bundle includes only the approved issue-related capabilities.

The agent gateway can also give tools stable names and clearer descriptions. When names from different servers overlap, namespacing or aliases can help distinguish them. Namespacing means adding identifying context to a name, such as identifying the service to which a tool belongs.

## What Happens During Discovery and Execution

Discovery and execution are related, but they happen at different points and require their own checks and validations.

During discovery, the agent sends tools/list to a bundle endpoint. The gateway gathers tool information from the servers included in that bundle. This is known as fan-out, meaning that one incoming request leads to requests across multiple downstream servers.

The gateway then applies authorization and filtering rules. It combines the approved tools into a coherent catalog, adjusts names where necessary, and returns the result to the agent. The agent might therefore receive a catalog containing repository tools from one server, issue tools from another, and log-query tools from a third. It interacts with the gateway’s combined interface instead of managing each server’s setup separately.

When the agent chooses a tool, it sends a tools/call request to the gateway. The gateway checks policy again, applies the relevant rate limits, determines the correct downstream server, and supplies the required credential. It then forwards the request and returns the result.

A tool appearing in a discovery response doesn’t remove the need to authorize its execution.

In other words, discovery controls what is presented to the agent. Invocation controls whether a particular request is allowed to proceed.

This gives the gateway responsibility for both the available catalog and the actual use of its tools. It also means the agent doesn’t need to implement downstream routing. Neither does it have to select credentials for each provider.

## Understanding What Happened After a Request

Once many agents have used many tools, the teams need to understand more about the resulting activity. This comes under the area of observability, which means the ability to understand a running system through the information it produces.

The gateway acts as a useful component for this because all tool requests pass through it. It can record a structured event for each call, with consistent fields describing the server, tool, bundle, owner, and identities involved. For reference, a structured event is a record with defined fields that can be searched or aggregated. Along with identity and ownership, an event can also contain the authorization result, request status, error source, timing information, and request and response sizes.

This helps answer questions such as which agent generated a request, which tool failed, and which team owns the affected capability.

The gateway also produces metrics, which summarize behavior across requests. This includes request counts, tool response times, authorization decisions, OAuth refresh outcomes, rate-limit decisions, and downstream failures.

These different forms of information serve different groups within the enterprise. Security teams can audit access, platform teams can investigate unusually active agents, and tool owners can understand adoption and failures.

## Making the Platform Easy for Teams to Adopt

A centralized gateway is useful only if teams can use it without excessive effort. Therefore, DoorDash makes registration and configuration for the gateway available through a self-service management interface and API.

Here’s how the process works:

- A team starts by registering its MCP server. The platform discovers the server’s raw catalog through tools/list, after which the tools intended for exposure are selected and approved.
- The team attaches the authentication mode, ownership information, and access policy.
- Approved tools are then added to one or more bundles. Once agents begin using them, teams can inspect traffic, response times, failures, authorization decisions, and cost information.

As we can see, registration is the beginning of onboarding. Discovering that a server offers a capability doesn’t automatically mean that every agent receives access to it. Ownership information is also part of making the system operationally useful. When a capability fails or needs a policy change, the platform needs a clear association between that capability and the team responsible for it.

The gateway has now become the default path for agent-tool access across DoorDash engineering teams. DoorDash has reported more than 200 registered MCP servers, more than 30 agents and services used by thousands of employees, and millions of tool calls each week.

## What DoorDash Plans to Improve Next

DoorDash is making further investments in the gateway.

One planned improvement is stronger agent identity and user delegation. Delegation means allowing an agent to perform an action on someone else’s behalf within defined permissions.

DoorDash’s target model gives each agent a cryptographic identity and uses short-lived delegated credentials scoped to the user, agent, task, and target tool. This would make it possible to determine the connection between the user requesting work, the agent performing it, and the specific action being authorized.

Another planned improvement is dynamic tool discovery. Existing bundles already narrow the tools available to an agent. Dynamic discovery would narrow that selection further using the current task, access policy, and usage signals, so the agent receives the capabilities most likely to help with its present work.

There are also plans to improve evaluation of tool quality and security, identifying risky descriptions, detecting secrets or personally identifiable information in errors, simplifying server creation and registration, and producing redacted tool-call event streams.

These investments extend the same architectural approach. As agents gain access to more systems, the platform needs precise ways to establish who is acting, expose useful capabilities, authorize specific actions, and make the resulting activity understandable.

**References**

- [How DoorDash Built a Centralized Gateway for AI Agent-Tool Access](https://careersatdoordash.com/blog/how-doordash-built-a-centralized-gateway-for-ai-agent-tool-access/)

---

∙