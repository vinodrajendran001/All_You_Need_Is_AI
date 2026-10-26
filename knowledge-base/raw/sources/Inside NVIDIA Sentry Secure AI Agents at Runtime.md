---
title: "Inside NVIDIA Sentry: Secure AI Agents at Runtime"
source: "https://developer.nvidia.com/blog/inside-nvidia-sentry-secure-ai-agents-at-runtime/?utm_source=substack&utm_medium=email"
author:
  - "[[Ofir Arkin]]"
published: 2026-10-21
created: 2026-10-26
description: "An AI agent can complete its assignment and still cross a security boundary. Recent incidents show that agents can circumvent security controls while using…"
tags:
  - "clippings"
---
An AI agent can complete its assignment and still cross a security boundary. Recent incidents show that agents can circumvent security controls while using tools, credentials, and services to pursue their assigned goals. Monitoring and enforcement need to operate outside the agent’s reach so that it can’t alter or disable them.

[NVIDIA Sentry](https://www.nvidia.com/en-us/networking/products/software/sentry/) is a security software framework that monitors AI agents and enforces policies governing their access to models, tools, and data. Part of the [NVIDIA OpenShell reference architecture](https://nvidianews.nvidia.com/news/openshell-reference-architecture) announced at GTC Berlin, it’s built on [NVIDIA DOCA](https://www.nvidia.com/en-us/networking/products/software/doca/), runs on [NVIDIA BlueField-4 DPUs](https://www.nvidia.com/en-us/networking/products/data-processing-unit/), and provides host-isolated runtime protection for AI agents. NVIDIA Sentry validates that an agent operates according to its designed intent and within its defined operational boundaries.

Trusted even when host resources can’t be trusted, it controls the agent’s only path to the model, providing tamper-evident traceability of agent activity while enforcing granular security controls on agent access in silicon. In addition to inspecting agent communications, NVIDIA Sentry uses out-of-band observability to establish real-time situational awareness, continuously evaluating agents’ runtime security and behavior to validate their security and integrity.

This post explains how NVIDIA Sentry evaluates agent requests, detects threats, and enforces security policies independently of host software.

## An independent security layer for agent runtime protection

An earlier [agentic AI security](https://developer.nvidia.com/blog/advancing-ai-infrastructure-for-agentic-ai-with-nvidia-doca-in-silicon-security) post described how NVIDIA BlueField runs security services in a hardware trust domain independent from the host.

NVIDIA Sentry builds on that foundation to continuously monitor AI agent behavior and enforce access policies independently of host software, establishing a strict security boundary in a separate hardware trust domain outside the agent’s reach to keep agents operating within their designed intent.

Software runtime boundaries remain essential. [NVIDIA OpenShell](https://developer.nvidia.com/blog/how-nvidia-openshell-reference-architecture-secures-and-governs-ai-agent-workloads-at-scale/) is a secure runtime for autonomous agents that governs what an agent can do. OpenShell separates policy enforcement from the agent workload, so a compromised agent can’t change its own restrictions. NVIDIA Sentry adds an independent hardware safeguard out of band, running on BlueField-4, beyond the agent’s reach and knowledge.

In the OpenShell reference architecture, agents execute on [NVIDIA Vera CPUs](https://www.nvidia.com/en-us/data-center/vera-cpu/), while BlueField-4 sits on the node’s only path to the model. NVIDIA Sentry inspects agent-to-model communications and enforces access policies without relying on the agent to report its own behavior. Memory introspection adds context about the agent’s execution environment, such as a container or microVM, to help detect external threats and agent misbehavior.

## Governing agent communications

DOCA Tower is NVIDIA Sentry’s AI security gateway. Built on [Envoy](https://www.envoyproxy.io/), the open source edge and service proxy, it operates as a transparent proxy for agent traffic, placing a bidirectional inspection layer between an agent and the external environment.

Agent network traffic reaches BlueField-4 through a direct network I/O path that bypasses host OS/hypervisor packet processing. All of the agent’s network communications are governed by NVIDIA Sentry as BlueField-4 sits on the only path to the model and to the outside world.

An agent’s network access boundary is controlled using DOCA Flow and DOCA Tower, which work in concert to restrict agent access to approved resources. DOCA Flow is used to implement a layer-4 firewall for each agent, accelerated in silicon on BlueField-4. The firewall blocks connections to unauthorized destinations and forwards permitted traffic to DOCA Tower for layer-7 (application layer) inspection, authorization, and additional security checks.

DOCA Tower acts as a transparent proxy, performing Transport Layer Security (TLS) termination using built-in, in-silicon TLS acceleration. For connections configured for inspection, it decrypts the agent traffic permitted by the layer-4 firewall to inspect and control agent communications.

NVIDIA Sentry uses the [Open Policy Agent](https://www.openpolicyagent.org/docs/) (OPA), an open source policy engine, to evaluate access requests against defined policies. OPA uses Rego, a declarative domain-specific language designed to evaluate complex hierarchical data structures. OPA runs locally in memory and can evaluate requests in under a millisecond, depending on policy complexity and configuration.

DOCA Tower is compatible with OpenShell policies, using OPA to extend network access policies and runtime controls into BlueField-4 and to the infrastructure.

![Architecture diagram showing NVIDIA Sentry on NVIDIA BlueField intercepting agent, LLM, machine, and API traffic through the DOCA Tower AI Security Gateway, using DOCA Argus real-time memory introspection to enrich access authorization requests evaluated by a policy engine, with telemetry flowing to a Partner XDR Platform.](https://developer-blogs.nvidia.com/wp-content/uploads/2026/10/figure-1-6-e1792445391184.webp)

Figure 1. NVIDIA Sentry uses DOCA Tower to inspect access requests and a policy engine to evaluate authorization, with runtime context from DOCA Argus

## Enforcing agent access policies with runtime context

An agent’s network communications provide only part of the information needed to assess its security and integrity. Visibility into the agent’s execution environment adds context for evaluating access requests that go beyond a traditional resource access policy.

DOCA Argus provides real-time visibility into an agent’s execution environment and operational state, giving NVIDIA Sentry additional context about agent access requests.

It uses live memory introspection to analyze selected regions of volatile host memory and obtain independent evidence of the system’s operational state.

DOCA Argus runs independently of the host, analyzing host memory on BlueField-4 without host-resident agents. This agentless design provides independent runtime visibility while preserving host compute resources. By operating outside the host in its own isolated trust domain, DOCA Argus remains beyond the reach of host software even if the host is compromised.

DOCA Argus maps the execution environment in real time—for example, containers to their respective pods and sandboxes to microVMs—and identifies the running processes and their properties within each environment. It also maps relationships between processes and threads, file access, network connections, loaded libraries, CPUs, GPUs, memory, and other system resources. DOCA Argus tracks containers, processes, and loaded libraries using their associated hashes.

This runtime context enables NVIDIA Sentry to connect agent access requests to the processes and execution environments behind them, enforcing policies that consider both the requested action and the security and integrity of the agent making it.

### Using runtime context to evaluate agent access

NVIDIA Sentry correlates network connection information from DOCA Tower with runtime context from DOCA Argus to evaluate access requests. NVIDIA Sentry uses this context to enforce policies based on additional attributes and assertions provided by DOCA Argus. It also enriches tamper-evident records of agent activity with runtime context, reducing the need for downstream correlation.

Figure 1 shows how these checks work. DOCA Tower uses its policy engine to correlate a network connection with the agent’s process that initiated it, its properties, and the container it belongs to. A network access policy can, for example, require that the container’s hash match a list of approved container hashes. It can also require that the initiating process, identified by its hash, appear in the container software bill of materials (SBOM), have permission to initiate network connections, and use an approved execution path and command-line arguments. DOCA Tower then checks whether policy permits the requested access—for example, access to an API and permission to perform the requested action.

NVIDIA Sentry uses DOCA Argus real-time observations and alerts to continuously evaluate agent security. Potential warning signs include executing unapproved tools; using `ptrace` to attack another process or spawn a process that attacks the agent; excessive outbound traffic suggesting data leakage; unauthorized file access or changes; CPU spikes; excessive writes to temporary folders; and large-scale file deletion. When NVIDIA Sentry detects any deviation, it can request millisecond-scale in-silicon containment.

## Extending controls to agent interactions

Agent security policies need to govern both what leaves the sandbox and what comes back. Requests can expose sensitive information or initiate unauthorized operations. Responses can introduce malicious instructions or other content that redirects an agent from its assigned goals.

NVIDIA Sentry uses DOCA Tower’s extensible inspection capabilities to apply controls to requests and responses. These controls can:

- Apply IP-, URL-, and protocol-level restrictions to agent communications.
- Capture tamper-evident records of agent requests, responses, and data flows for behavioral analysis and investigation.
- Govern agent-to-agent (A2A) and Model Context Protocol (MCP) traffic.
- Detect and redact personally identifiable information and secrets, including API keys, tokens, and passwords.
- Identify and block content prohibited by policy.

NVIDIA Sentry evaluates inspected requests and responses throughout an agent’s session, applying policy as the agent accesses models, tools, APIs, and services.

## Evaluating agent behavior using specialized models

NVIDIA Sentry integrates with specialized AI models to analyze agent communications and classify agent behavior using tool calls and available reasoning traces. These models run locally or remotely on dedicated GPU-accelerated systems. The classifiers assess whether an agent’s behavior remains consistent with an agent’s designed intent or indicates behavioral drift.

The models can classify agent communications inline or out of band. Inline classification can trigger blocking before potentially harmful content reaches its destination. Out-of-band classification can trigger a response action after detecting agent misbehavior.

Tamper-evident activity records and detection results provide forensic evidence for further incident investigations.

Agent communications require continuous classification to detect misbehavior. DOCA Argus complements this classification with ongoing analysis of the agent’s operational environment to evaluate runtime security and behavior.

![Architecture diagram showing NVIDIA Sentry on NVIDIA BlueField using DOCA Tower AI Security Gateway to inspect ingress and egress agent-to-LLM communications, submitting traffic inline to a Specialized Module for Agent Misbehavior Detection, with detections and classification responses used to block harmful content and forwarded to a Partner XDR Platform including NVIDIA Morpheus GNN-based Autoencoder for NetFlow Anomaly Detection.](https://developer-blogs.nvidia.com/wp-content/uploads/2026/10/sentry-figure-2-no-logo.webp)

Figure 2. NVIDIA Sentry uses DOCA Tower to submit inspected communications to a specialized model for classification, where potentially harmful content is blocked inline

NVIDIA Sentry can contain and quarantine agents within milliseconds using BlueField-4 in-silicon enforcement capabilities without the cooperation of the agent or the host software.

These independent controls matter when software boundaries fail. Even if an agent escapes its sandbox, NVIDIA Sentry retains its monitoring and enforcement capabilities as it operates from BlueField-4’s isolated trust domain.

Enterprise security platforms can also use NVIDIA Sentry telemetry to correlate detections and request response actions. The protected record preserves the observed activity and policy context that led to enforcement for subsequent review.

![Architecture diagram showing NVIDIA Sentry on NVIDIA BlueField continuously evaluating agent security and integrity by combining DOCA Tower AI Security Gateway, Agent Misbehavior Detection, DOCA Argus real-time memory introspection, data enrichment, a policy engine, and continuous runtime security evaluation to generate interaction telemetry, runtime detections, and response actions coordinated with a Partner XDR Platform.](https://developer-blogs.nvidia.com/wp-content/uploads/2026/10/sentry-figure-3-no-logo.webp)

Figure 3. NVIDIA Sentry combines interaction telemetry, runtime detections, and policy context with enterprise security integrations to drive response actions through DOCA Tower

## Using agent identity in access decisions

Security controls must connect an agent’s identity with its permissions and requested action. NVIDIA Sentry uses this identity context in application-layer policy evaluation. DOCA Tower integrates with [SPIFFE/SPIRE](https://spiffe.io/) to support verifiable workload identity and supports integration with partner identity systems.

Identity establishes who is making a request. Authorization policies determine which resources an identity may access and which operations are permitted. Runtime evidence adds context about the execution environment associated with the request.

This approach connects identity and runtime security. If an agent’s behavior or integrity changes, NVIDIA Sentry can use that context when evaluating subsequent access requests, applying the organization’s defined policies.

## Preserving a trusted record of agent activity

Security teams need evidence for incident investigations, even when an agent has escaped its sandbox or altered host-based logs.

NVIDIA Sentry produces attested telemetry and tamper-evident records using BlueField-4’s independent trust domain. DOCA Tower records inspected communications and policy decisions outside the reach of the agent and host software, while DOCA Argus contributes independently observed runtime signals.

An agent that changes a log inside its own environment cannot make the same change to the protected record maintained on BlueField-4.

Attestation provides verifiable evidence of telemetry’s source and integrity. Security teams can use these records to reconstruct observed interactions, review enforcement decisions, and support audits.

NVIDIA Sentry can supply this telemetry to enterprise security platforms, such as XDR and SIEM platforms and security data lakes, connecting agent activity with broader threat intelligence, detection logic, and incident-response workflows.

## Extending NVIDIA Sentry with enterprise security capabilities

NVIDIA Sentry enables developers and cybersecurity providers to extend monitoring, governance, and enforcement through DOCA libraries and microservices.

DOCA Tower uses Envoy’s extensibility, enabling partners to adapt existing plugins or develop new ones to run on BlueField. This provides a familiar foundation for integrating access controls, content inspection, telemetry, and specialized detection logic into the application-layer path.

NVIDIA plans to publish core plugins to accelerate development, including a plugin that exposes agent communications for further analysis of available reasoning traces.

Partners can combine these capabilities with their identity services, AI classifiers, threat intelligence, and security operations platforms. NVIDIA Sentry contributes independent runtime visibility and infrastructure enforcement, while connected platforms add enterprise context and coordinate investigation and response.

## Building layered protection for AI agents

Scaling agentic AI requires continuous visibility into and control over what agents can access and do throughout execution. NVIDIA Sentry brings that control into an independent infrastructure domain, combining application-layer inspection through DOCA Tower with runtime evidence and visibility from DOCA Argus and in-silicon enforcement on BlueField-4.

Alongside NVIDIA OpenShell, NVIDIA Sentry extends protection from software execution boundaries to a hardware-isolated safeguard. It enables security teams to evaluate agent identity, authority, interactions, and runtime integrity together—and act when behavior crosses defined boundaries.

Developers and cybersecurity teams can begin exploring these foundations with [NVIDIA DOCA](https://www.nvidia.com/en-us/networking/products/software/doca/). Available libraries and microservices, including DOCA Argus, DOCA Flow, and OVS-DOCA, provide a starting point for experimenting with out-of-band observability and infrastructure enforcement ahead of NVIDIA Sentry’s planned availability early next year.