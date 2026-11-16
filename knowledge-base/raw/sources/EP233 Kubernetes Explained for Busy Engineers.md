---
title: "EP233: Kubernetes Explained for Busy Engineers"
source: "https://blog.bytebytego.com/p/ep233-kubernetes-explained-for-busy?utm_source=post-email-title&publication_id=817132&post_id=224653050&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-11-15
created: 2026-11-16
description: "Kubernetes is an orchestration platform that manages the deployment and maintenance of containerized applications, particularly on multiple machines."
tags:
  - "clippings"
---
## Workshop: How Anthropic Traces Agents with OpenTelemetry and Sentry (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!GOuZ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F39632276-e0b0-4271-aeee-aec850058a10_1200x1200.png)

Where did your agent’s tokens go?

CJ Avilla from Anthropic sent his Claude Platform OpenTelemetry data to Sentry. It turned up an old project that was still burning tokens.

Every retry costs tokens, and the cause can be a slow API or database, not the model. In this live workshop, you’ll see:

- How to send Claude Platform OpenTelemetry (OTel) data to Sentry
- A Claude agent’s failed tool calls, retries, and final success in one trace
- Whether the fix belongs in the prompt, the tool, or the service behind it

Save your spot for November 17 at 10am PT.

---

This week’s system design refresher:

- Kubernetes Explained for Busy Engineers
- Single Agent vs. Multi-Agent Architecture
- The Testing Pyramid
- How LLMs Use AI Agents with Deep Research
- Common types of AI Agents guardrails on production

---

## Kubernetes Explained for Busy Engineers

Kubernetes is an orchestration platform that manages the deployment and maintenance of containerized applications, particularly on multiple machines.

![Image](https://substackcdn.com/image/fetch/$s_!sEO7!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0fe509fa-78eb-4156-abe0-ff73eaf356a1_2486x3002.png)

Let’s see how kubernetes creates and keeps an application running.

- You describe the desired state of your application in a deployment.yaml file.
- The API server validates the deployment and stores this desired state in etcd. The etcd is a persistent database that stores the Kubernetes resources, like the number of replicas, existing pods and nodes, and their assignments.
- The controller manager job is to run controllers and ensure that the desired state matches the actual state of the Kubernetes cluster. For example, when a Deployment requests four replicas, the controllers ensure that four Pods are created and maintained.
- The scheduler decides where each pod is supposed to run. It assigns the pods to the worker nodes based on the available CPU and memory resources, placement rules, or any other constraints.
- The worker nodes are the ones that run the assigned pods. Each worker node contains a container runtime that downloads the image and actually runs the container. The kubelet keeps track of the node-to-pod assignment and ensures they run properly.
- Once the pods are running, the Kubernetes Service provides a stable endpoint to the pods.

The Ingress or Gateway then exposes that Service to the external users.

---

## Single Agent vs. Multi-Agent Architecture

Some tasks need a single agent. Others need a whole team. Knowing the difference is the skill.

![Image](https://substackcdn.com/image/fetch/$s_!Z5zI!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5233378c-3c59-40b1-9de2-6515b9d3e928_2484x3002.png)

Single-agent system: One reasoning LLM that plans, picks a tool, and loops on its own until the task is done. Use a single agent when:

- the task is a clear, linear sequence
- one agent can hold the whole problem in its head
- you want something simple to build and easy to debug

Multi-agent system: An orchestrator that splits a task into subtasks and routes each one to a specialized agent. Use multi-agent when:

- subtasks can run in parallel
- one agent writes and another independently verifies the work
- the problem is too big for one agent to coordinate alone

Single agents are cheaper and easier to build, but they hit a ceiling on complex work.

Multi-agent systems are more capable and more reliable, but they add coordination cost.

Start with a single agent. Move to multi-agent only when context or reliability become the bottleneck.

Over to you: Are you running single-agent or multi-agent systems in production?

---

## The Testing Pyramid

![Image](https://substackcdn.com/image/fetch/$s_!_6cl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea738d9d-1ae5-4a26-9a50-79ec7720fd80_2360x2664.jpeg)

Testing is the backbone of reliable software. The Testing Pyramid is a widely accepted strategy for structuring tests into three key layers:

- Unit Tests: These are the foundation of the pyramid. Unit tests are fast, isolated, and low-cost to write and maintain. They test individual functions, methods, or components.
- Integration Tests: These tests validate interactions between components, such as APIs, databases, and external services. They are slower than unit tests and require more setup.
- E2E Tests: These simulate real user flows from start to finish across the full system. They are expensive to write and maintain and tend to be slow to execute.

As you go up the pyramid, the cost of test development, execution, and maintenance increases.

Over to you: Which layer do you find most valuable in your testing strategy, and why?

---

## How LLMs Use AI Agents with Deep Research

When you ask an LLM such as Claude, ChatGPT, or Gemini to do deep research on a complex topic, it’s not just one model doing all the work. It’s a coordinated system of specialized AI agents.

![](https://substackcdn.com/image/fetch/$s_!gm3t!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb755ecbd-6bc9-4a06-8d35-7d59a24d9170_2508x3000.png)

Here’s how it works:

Step 1: Understanding The Question and Making a Plan

It all starts with the query, something like “Analyze the competitive landscape of AI agents in 2026. The system doesn’t just dive in blindly. First, it may ask clarifying questions to understand exactly what is needed. Then, it generates a plan and breaks the big question down into smaller and manageable tasks.

Step 2: Sub-Agents Get to Work

Each small task gets assigned to a sub-agent, which is basically a mini AI worker with a specific job. For example, one sub-agent might be tasked with finding the latest Nvidia earnings. It figures out which tools to use, such as searching the web, browsing a specific page, or even run code to analyze data. All of this happens through a secure layer of APIs and services that connect the AI to the outside world.

Step 3: Putting it All Together

Once all the sub-agents finish their tasks, a Synthesizer Agent takes over. It aggregates everything, identifies key themes, plans an outline, and removes any redundant or duplicate information. At the same time, a Citation Agent makes sure every claim is linked back to its source and properly formatted. The end result is a polished, well-cited final output ready for use.

Over to you: Have you tried deep research in any LLM?

---

## Common types of AI Agents guardrails on production

![Image](https://substackcdn.com/image/fetch/$s_!mxFP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9af7cba-69d4-4d18-8705-7ce91e73c983_2484x3002.jpeg)

- Input Screening: Every user request is scanned for prompt injection, sensitive data, and off-scope topics before the model sees it. Unsafe inputs return a fallback message.
- Context Verification: Every user request is scanned for prompt injection, sensitive data, and off-scope topics before the model sees it. Unsafe inputs return a fallback message.
- Response Generation: The LLM reasons only over verified context.
- Output Validation: Every response is checked for groundedness, format, and safety before it leaves the system. Failures trigger up to two retries, then a safe fallback.
- Operational Controls: A final layer enforces limits, logs every call, and routes low-confidence or high-risk actions to humans.

Reliable agents aren’t built on better prompts. They’re built on the guardrails wrapped around them.

Over to you: Which guardrail layer catches the most issues in your setup?

---

∙