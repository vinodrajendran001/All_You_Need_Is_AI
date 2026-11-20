---
type: entity
created: 2026-11-20
updated: 2026-11-20
entity_kind: tool
tags:
  - entity
  - kubernetes
  - infrastructure
  - serving
  - gpu
source_ids:
  - src-2026-11-15-bytebytego-ep233-kubernetes
  - src-2026-11-03-william-morgan-kinference-launch
  - src-2026-10-31-william-morgan-kinference-benchmarks
  - src-2026-09-13-ranganathan-gke-inference-gateway
  - src-2026-10-04-ben-tovim-ai21-kueue-gpu-fleet
  - src-2026-10-15-netflix-reliable-gpu-compute
  - src-2026-11-04-axjns-post-kubernetes-genai
  - src-2026-07-03-bytebytego-openai-voice
status: active
---

# Kubernetes

## What it is

An open-source orchestration platform that "manages the deployment and maintenance of containerized
applications, particularly on multiple machines", in the definition of
[[ByteByteGo - EP233 Kubernetes Explained for Busy Engineers]]. Users declare a desired state, for
example in a `deployment.yaml`. The **API server** validates it and stores it in **etcd**.
**Controllers** keep actual state matching desired state ("when a Deployment requests four replicas,
the controllers ensure that four Pods are created and maintained"). The **scheduler** places pods on
nodes "based on the available CPU and memory resources, placement rules, or any other constraints". On
each node a **container runtime** runs the containers and the **kubelet** keeps assigned pods running.
A **Service** gives a set of pods one stable endpoint, and **Ingress or Gateway** exposes it externally.

## Why it matters here

Most AI serving and training sources in the vault run on Kubernetes, and most of them are about what
it does not provide out of the box. Its scheduling and load balancing were designed for interchangeable
replicas of stateless services, judged by CPU and memory. AI workloads break that assumption in three
places: replicas hold different KV-cache contents, GPUs fail and fragment in ways a node count hides,
and some sessions are stateful at the network layer. The sources below each add a layer above or beside
the core platform to handle one of these.

## Notes

### Inference routing is built above the Service

A plain Service spreads traffic without looking at replica state. In
[[William Morgan - Distributed Inference Benchmarks Kinference vs Kubernetes]], kube-proxy in iptables
mode "picks a random pod for each new connection", and the load generator opened a new connection for
almost every request. Against that baseline a cache- and queue-aware router cut median TTFT from
**6.88 s to 0.31 s** on a shared-prefix workload and served about **7.4×** the peak goodput. This is a
vendor benchmark of its own product on three L40S replicas, compared only with random routing.

Two routing layers are recorded. The GKE Inference Gateway in
[[Rahul Ranganathan - Inference Gateway on GKE]] extends the Gateway API with `InferencePool` and
`InferenceModel` resources, cache- and queue-aware endpoint picking and Critical, Standard or Sheddable
priority; it was Preview/Pre-GA at capture time, the extension was described as experimental/alpha,
and its claimed improvements were unquantified. Kinference, in
[[William Morgan - Kinference Inference Control Plane for Kubernetes]], adds declarative policies for
tenants, model classes, idle-only batch work, overflow to external providers and PII. Its claim that
such policies "did not seem to exist anywhere in the Kubernetes inference ecosystem" sits awkwardly
next to the GKE priorities. See [[Inference Serving Engines]] and [[KV Cache]].

### GPU capacity is a placement problem, not a count

[[Asaf Ben-Tovim - How AI21 Manages Its GPU Fleet with Kueue]] reports a shared GKE cluster of roughly
**10,000 GPUs**, where a job needing eight GPUs on one node cannot use eight idle GPUs scattered
**1 + 1 + 4 + 2** across four nodes. Kueue adds topology-aware scheduling, packing and admission
fairness for that cluster.
[[Netflix - Reliable GPU Compute for Training and Inference]] runs a Kubernetes-native GPU fleet where a
node agent built on node-problem-detector turns health checks into node conditions that controllers act
on. Isolating one faulty device, capability-based requests and topology-aware placement are framed as
possible once Kubernetes Dynamic Resource Allocation (DRA) is supported in Karpenter, not as shipped.
See [[GPU Fleet Reliability]] and [[Distributed Training Parallelism]].

### Disposable addresses versus stateful sessions

[[ByteByteGo - How OpenAI Delivers Low-Latency Voice AI]] names the mismatch for WebRTC: the protocol
assumes stable servers with fixed IPs and ports, "while Kubernetes treats addresses as disposable",
producing port exhaustion and session-affinity failures. See [[Real-Time Voice AI]].

### Whether agents need something else

[[axjns.dev - Post-Kubernetes Infrastructure for GenAI Workloads]] reads Modal's vendor-reported
million-sandbox launch as a design direction, not proof that Kubernetes is obsolete. Its argument is
that fast disposable execution and durable coordination need different consistency, and that sandbox
isolation is not authorisation. See [[Celln]] and [[Agent Security and Governance]].

### Evidence quality

The vault has no neutral comparison of Kubernetes-based serving against alternatives. The one measured
result above is first-party and uses Kubernetes' default as the baseline. The explainer is
definition-level and does not mention accelerators.

## Related pages

- [[Inference Serving Engines]]
- [[KV Cache]]
- [[Model Routing]]
- [[Serving Benchmarks and Goodput]]
- [[ML Systems at Scale]]
- [[GPU Fleet Reliability]]
- [[Distributed Training Parallelism]]
- [[Real-Time Voice AI]]
- [[Agent Security and Governance]]
- [[Celln]]
- [[Google Cloud]]
- [[ByteByteGo]]
