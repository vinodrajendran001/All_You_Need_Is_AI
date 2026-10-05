---
title: "Add Runtime Controls to AI Agents with NVIDIA OpenShell"
source: "https://developer.nvidia.com/blog/add-runtime-controls-to-ai-agents-with-nvidia-openshell/?utm_source=substack&utm_medium=email"
author:
  - "[[Alex Watson]]"
published: 2026-09-28
created: 2026-10-05
description: "AI agents can be given a goal, write code, use tools, and keep working as new information becomes available. This opens the door to applications that…"
tags:
  - "clippings"
---
AI agents can be given a goal, write code, use tools, and keep working as new information becomes available. This opens the door to applications that investigate software failures, run experiments, and carry out business-critical actions and research over days or weeks.

Useful agents need access to workspaces, compute resources, data, credentials, and external services. But broader access also creates more consequential failure modes, from changing production data or exposing confidential information to acting beyond the assigned task.

[NVIDIA OpenShell](https://docs.nvidia.com/openshell/about/why-open-shell) 0.1.0 is an open-source runtime for defining and enforcing which systems and data an agent can access. It combines sandboxed execution, controlled service access, credential management, and formal policy analysis. Teams can grant agents the capabilities a task requires while [OpenShell](https://www.nvidia.com/en-us/ai/openshell/) enforces those permissions outside the workload.

It supports Codex, Claude Code, Pi, Hermes, and future frameworks across enterprise applications, frontier research, and physical AI—from internal agent fleets and long-horizon research to robotics and edge systems.

This post shows how NVIDIA OpenShell 0.1.0 places enforceable runtime controls around an existing AI agent—without rewriting it—so teams can restrict API operations, protect credentials, and review permission changes outside the agent workload.

OpenShell provides the runtime layer of the broader [NVIDIA Open Agent Safety Platform](https://www.nvidia.com/en-us/solutions/ai/agent-safety/), which extends protection across the application, runtime, and infrastructure layers.

![](https://www.youtube.com/watch?v=GYYP-eW58ug)

*Video 1. A walkthrough on how to set up your autonomous long-running agent*

## How organizations are adopting OpenShell

OpenShell is open source and available for enterprise adoption across a broad ecosystem of partners, which shapes the product itself. Organizations are adopting OpenShell across a range of applications, including chip design, enterprise automation, accelerated computing, and physical AI.

- Cadence uses OpenShell for chip design with its ChipStack Autonomous RTL Design Engineer.
- Slack is building an on-demand agent platform on OpenShell to automate tasks.
- Gecko Robotics uses OpenShell to govern agents making decisions on physical robots.

## OpenShell capabilities

OpenShell 0.1.0 supports sandbox operations, policy verification, governance integration, credential protection, and flexible compute.

| **Capability** | **How it helps** |
| --- | --- |
| **Multi-tenant platform support** | Operate agent services for multiple teams or customers with separate workspaces, permissions, and service access on shared infrastructure. |
| **Formal policy verification** | Show human and AI reviewers whether requested permissions remain within defined security boundaries, and identify where they exceed them. |
| **Extensible security and governance** | Connect third-party security services, governance systems, and custom checks to enforcement outside the agent workload. |
| **Credential-protected service access** | Use authenticated services while real credentials remain outside the agent workload and are bound to authorized requests. |
| **CPU and GPU execution** | Run experiments and data processing on CPUs or GPUs across containers, VMs, and Kubernetes environments. |

*Table 1. New capabilities introduced in OpenShell 0.1.0*

## Enforce permissions outside the agent

An agent can interpret instructions, choose tools, and evolve its approach over time. OpenShell preserves that flexibility while enforcing permissions outside the agent workload.

OpenShell can manage fleets of agents and their sandboxes, each with its own permissions, and enable governance across groups at a time. Three components provide this control:

- **OpenShell Gateway:** Manages the lifecycles and policies of many sandboxes.
- **OpenShell Supervisor:** Paired with each sandbox, it runs outside the agent workload and checks outbound requests against policy.
- **OpenShell Sandbox:** Runs the workload with kernel-level controls over its filesystem and processes, and no network path except through the supervisor.

![Diagram showing the OpenShell Gateway managing three separate agent sandboxes. Each sandbox contains an agent with code and local tools. Policy-approved connections link the agents to one another and to application services, including model APIs, data and memory, and remote MCP servers.](https://developer-blogs.nvidia.com/wp-content/uploads/2026/09/figure-1-2.webp)

Figure 1. OpenShell manages agent sandboxes. External supervisors restrict outbound communication to configured services

The OpenShell sandbox runtime uses operating-system kernel controls to limit which files a workload can read or change and prevent it from acquiring additional system privileges. For network access, you can be more specific than allowing a connection to a service. The supervisor can inspect configured HTTP, GraphQL, and Model Context Protocol (MCP) traffic, allowing a data query while blocking a write through the same API. These controls remain in place when the agent starts a shell, runs generated code, launches child processes, or proposes task delegation to sub-agents. OpenShell records policy decisions in an Open Cybersecurity Schema Framework (OCSF) audit trail. When it blocks an inspected request, it can return a descriptive error that helps the agent decide what to do next.

## Watch a policy decision happen

This example uses curl and an unauthenticated endpoint in the GitHub REST API, making each policy decision visible without requiring an API key or language model. The same controls apply when an agent makes the request.

Install and start OpenShell 0.1.0 using the [installation guide](https://docs.nvidia.com/openshell/dev/about/installation). Then download the accompanying `no-network.yaml` and `github-readonly.yaml` policy files into an `examples` directory.

First, create a sandbox with no outbound network access:

```
openshell sandbox create --name policy-demo \
  --no-auto-providers \
  --policy examples/no-network.yaml
```

The create command opens a shell inside the sandbox. Try reading a public endpoint:

```bash
curl -sS --max-time10 https://api.github.com/zen
```

The request fails because the sandbox has no outbound network permission. Open a second terminal on your host and check the logs to see which program made the request and why it was blocked:

```
openshell logs policy-demo --since 5m
```

Next, replace the sandbox policy with one that permits read-only access to the GitHub REST API. Policies are authored in YAML and compiled to OPA/Rego, which OpenShell evaluates for each outbound request.

```yaml
network_policies:
  github_api:
    name:github-api-readonly
    endpoints:
      -host:api.github.com
        port:443
        protocol:rest
        enforcement:enforce
        access:read-only
    binaries:
      -path:/usr/bin/curl
```

This rule lets /usr/bin/curl reach the GitHub API on port 443. With the protocol: rest, OpenShell inspects HTTP requests, allowing reads while blocking writes.

In your host terminal, apply the complete replacement policy without restarting the sandbox:

```
openshell policy set policy-demo \
  --policy examples/github-readonly.yaml --wait
```

Return to the sandbox shell and try both requests:

```
# Read: allowed
curl -sS --max-time 10 https://api.github.com/zen
 
# Write: blocked
curl -sS --max-time 10 -X POST https://api.github.com/zen
```

Check the host logs again to confirm OpenShell blocked the POST. An agent running these commands encounters the same restrictions.

## Access services without exposing credentials

Many agents need model APIs or private services to complete their tasks. OpenShell authorizes that access while keeping the real credentials outside the agent workload.

![Diagram showing an agent workload sending an API request with a placeholder key to the OpenShell supervisor and proxy. The supervisor verifies the network policy and credential binding, substitutes the real provider key outside the agent workload, and forwards the authenticated request to an authorized service.](https://developer-blogs.nvidia.com/wp-content/uploads/2026/09/figure-2-2.webp)

Figure 2. The real credential is substituted outside the agent workload and only for an authorized endpoint. Both network access and credential binding must permit the request

Authorization for one service does not make the credential available to another. If the agent sends the placeholder to a destination outside the credential’s approved endpoints, OpenShell rejects the request.

The receiving service still enforces the permissions attached to the real credential. OpenShell adds a separate control over how the agent can use it. For example, an inspected read-only API policy can block write requests even when the credential itself has write access.

A provider profile defines the credentials, endpoints, and permitted programs for a service. Assuming a GitHub provider named `github` is already configured, attach it to a new sandbox and launch Codex.

```
openshell sandbox create \
  --provider github \
  -- codex
```

## Adjust network access while the agent runs

An agent may discover that it needs a service or data source that wasn’t known when the task began. When policy blocks the request, OpenShell records the denial so an operator or an AI agent approver can review it. With [policy advisor](https://docs.nvidia.com/openshell/dev/sandboxes/policy-advisor#enable-policy-advisor) enabled, the agent can propose a narrowly scoped network or file policy change. The proposal remains pending for human review by default, and the agent cannot approve its own request. After approval, OpenShell loads the new rule into the running sandbox so the agent can retry without restarting its work.

Filesystem and process restrictions are established when the sandbox starts. Changing those controls requires a new sandbox.

Enable policy advisor for a sandbox with the following command.

```
openshell settings set <sandbox-name> \
  --key agent_policy_proposals_enabled \
  --value true
```

## Verify the permissions a policy grants

A policy can appear restrictive while leaving another route open. Blocking a GitHub write through one tool does not help if another permitted tool or generated code can use a credential to make the same write.

The OpenShell policy prover uses formal logic to check the permissions granted by the policy, including provider-contributed access. It can prove modeled permissions remain within an operator-defined boundary or identify a concrete action that crosses it. Because the result comes from the policy model, an agent’s explanation cannot change that result. The linked [formal-methods primer](https://nvidia.github.io/OpenShell-Research/dev-notes/posts/2026-09-10-learning-formal-methods-agent-policy-prover/) walks through how this works.

In long-horizon adversarial experiments, frontier agents with reduced safeguards spent up to two hours trying to persuade an AI reviewer to grant permissions that would let them modify a protected GitHub repository. OpenShell’s formal policy analysis gave the reviewer evidence of what those permissions allowed, even when agents attempted to manipulate the reviewer. The combined review and runtime controls allowed useful access, and no protected repository writes occurred in these tests

Ongoing work extends policy analysis across multiple agents, where one agent’s access can combine with another’s. The goal is to check the permissions of the system that they form together. See the [prover documentation](https://docs.nvidia.com/openshell/how-it-works/policies/prover) for supported checks.

## Build locally and deploy into shared infrastructure

Start with a local sandbox while building an application and defining its permissions. To serve multiple users, follow the [workspaces and access guide](https://docs.nvidia.com/openshell/how-it-works/workspaces) and use the SDK to create and manage sandboxes. Each workload has its own policy and attached providers.

[Trusted middleware](https://docs.nvidia.com/openshell/latest/extensibility/supervisor-middleware) outside the sandbox can connect identity services and add application-specific checks to the request path. Compute drivers connect OpenShell to Docker, Podman, MicroVM, and Kubernetes; the [support matrix](https://docs.nvidia.com/openshell/dev/reference/support-matrix) covers current requirements.

Join **#openshell-dev** on [CNCF Slack](https://cncf-slack.netlify.app/) to ask questions, share feedback, and connect with other teams and developers building on OpenShell. Explore the code and contribute on [GitHub](https://github.com/NVIDIA/OpenShell), and follow ongoing research and engineering work in the [OpenShell dev notes](https://nvidia.github.io/OpenShell-Research/dev-notes/). If you’re upgrading an existing deployment, see the [0.1.0 migration notes](https://docs.nvidia.com/openshell/upgrade/0-1-0).

Ready to build? Start with the [quickstart](https://docs.nvidia.com/openshell/dev/get-started/quickstart) to run your own agent with OpenShell and configure the services it can access.