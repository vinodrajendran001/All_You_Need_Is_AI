---
title: "Post-Kubernetes Infrastructure for GenAI Workloads"
source: "https://axjns.dev/blog/post-kubernetes-genai"
author:
published:
created: 2026-11-04
description: "Field notes on Modal's million-sandbox announcement, what it says about Kubernetes, and the coming decoupling of coordination from execution."
tags:
  - "clippings"
---
Field notes on Modal's million-sandbox announcement

Modal's [million-sandbox demonstration](https://modal.com/blog/scaling-to-1-million-concurrent-sandboxes-in-seconds), published on 16 July 2026, is interesting because of what it removes from the launch path. The company reports creating a million concurrent sandboxes in under a minute. This is a vendor-reported result, not a benchmark I have reproduced.

The architectural question underneath it is broader: how much durable coordination should sit between a request for short-lived compute and the moment it starts running?

## A shorter creation path

Modal describes scheduling servers that propose placements and workers that accept or reject them using local resource state. Workers publish state asynchronously. The creation path avoids synchronous durable writes, trading a globally current view for a simpler route to execution.

This is still coordination. The design changes where placement decisions happen and when the rest of the system learns about them. It is a deliberate choice about consistency, rejection, and recovery for a workload with very high creation rates.

Modal contrasts that path with Kubernetes scheduling and the writes involved in pod lifecycles. Its complexity discussion describes worst-case behaviour; it should not be read as the cost of every pod launch or a controlled comparison with every Kubernetes configuration. The useful observation is that durable control-plane work can become material when the unit of execution is small and churn is high.

## When creation latency dominates

A long-running service can amortise setup over hours or days. An agent's code-execution task might finish in seconds. For that task, environment preparation and scheduling can account for a large share of the time the user waits.

This does not apply to every GenAI workload. Model training, inference services, evaluations, and one-shot tool calls have different resource profiles. But bursts of isolated, short-lived execution create a clear incentive to specialise the launch path. The same design that gives an operator a durable view of every workload may be expensive if every tiny computation has to pass through it individually.

My inference from Modal's post is that this separation deserves attention. It is not enough evidence to declare Kubernetes obsolete or to conclude that the ecosystem cannot adapt. A dedicated execution service could itself run on infrastructure managed by Kubernetes while exposing a different unit of work above it.

## Consistency still has to live somewhere

Removing a synchronous write moves responsibilities elsewhere. Workers must arbitrate local capacity; the surrounding system must handle retries, stale observations, and failures. Whether those tradeoffs are acceptable depends on the operation. Launching disposable compute and approving a consequential external action do not require identical semantics.

Security isolation is another distinct concern. A sandbox may constrain what untrusted code can reach, but isolation alone says nothing about whether a task was authorised, whether it ran twice, or whether its result is trustworthy. The execution boundary and the coordination contract have to meet at a well-defined interface.

That is the part of the stack I find most interesting: which decisions must be durable before execution, and which can be reconciled afterwards?

## Where Sympozium and Celln fit

In [Sympozium](https://github.com/sympozium-ai/sympozium), I am exploring coordination as a durable responsibility: identity, policy, shared evidence, action ownership, and a history an operator can inspect. Kubernetes offers useful machinery for representing intent and reconciling state. It does not, by itself, supply all the application semantics an agent team needs.

The execution plane has a different job. It accepts an authorised request, supplies the permitted capabilities, runs the work within an isolation boundary, and returns an outcome with provenance. [Celln](https://axjns.dev/blog/celln-execution-plane) is my attempt to explore that smaller unit of execution.

The seam should be explicit enough that either side can change. A control plane should be able to request work without depending on the mechanism used to start a cell. An executor should be able to validate its authority without taking over the organisation's workflow.

Modal offers one substantial example of specialising the creation path. My bet is that more agent infrastructure will separate durable coordination from transient execution. The test is whether the split improves latency and throughput while preserving the authority and recovery guarantees the workload actually needs.