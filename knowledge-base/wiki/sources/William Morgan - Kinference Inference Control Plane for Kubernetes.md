---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-03-william-morgan-kinference-launch
source_title: "Kinference: Scalable Inference Control Plane for Kubernetes"
source_author: "William Morgan"
source_url: "https://www.buoyant.io/blog/introducing-kinference"
tags:
  - source/summary
  - inference
  - serving
  - kubernetes
  - routing
  - vendor
source_ids:
  - src-2026-11-03-william-morgan-kinference-launch
status: active
---

# Kinference: Scalable Inference Control Plane for Kubernetes

## Summary

William Morgan of Buoyant, the company behind the Linkerd service mesh, announces **[K]inference**
(pronounced "kay-inference"), an open-source "inference control plane" for [[Kubernetes]]. It runs in
front of inference engines such as vLLM. Clients point OpenAI- or Anthropic-compatible traffic at its
HTTP endpoint, "like an LLM gateway". The pitch is that the ecosystem has many projects for serving
one model or tuning a bank of GPUs, but "nothing focused on building an inference platform". Morgan
defines a platform as a layer that mediates access to a shared, scarce resource (GPUs) for competing
consumers (agents, harnesses, applications) while keeping fairness, availability and security.

The announced features are token rate limiting, per-tenant usage and cost tracking, KV-cache-aware load
balancing, declarative **inference policies**, an agent-oriented configuration workflow, and inference
metrics for SLOs. It is a vendor launch post. Its one performance claim points to the companion
benchmark, [[William Morgan - Distributed Inference Benchmarks Kinference vs Kubernetes]]. The project
is Apache v2 and does not require Linkerd.

## Key claims

### Inference policies as the central abstraction

Morgan writes that inference policies "did not seem to exist anywhere in the Kubernetes inference
ecosystem". The motivating questions came from customers:

- requesting classes of models ("any Qwen 3.8 model", "whatever is good for coding") rather than one
  checkpoint;
- redirecting "easy" requests to cheaper models "without sending the whole prompt history to a cold GPU
  and incurring a huge latency hit";
- serving batch requests only when GPUs are idle;
- bursting to a third-party inference provider at saturation instead of queueing;
- ensuring "prompts with PII never leave our environment".

Policies route or reject requests by tenant, requested model, GPU pool state, "semantic classification
of the prompts", and other factors. They are meant to be reviewed by humans or agents, committed to
git, linted, and applied or rolled back independently. The post describes no policy language,
evaluation order, or conflict resolution; it links the docs.

### Cache-aware load balancing, and why it matters for cost routing

The balancer weighs GPU queue sizes, historical performance and "the contents of the KV cache on the
GPU", sending each request to the vLLM worker "that will do the least work for that specific request".
The post's key argument connects this to [[Model Routing]]. Cost strategies such as sending simpler
prompts to cheaper models "sound good on paper", but in multi-turn chat or coding they mean switching GPUs mid-conversation,
which "forces recomputing the entire conversation". Kinference's answer is a policy that sends a simple
request to the cheaper model "**but only if that's less work than sending them to the expensive model
in the first place**". No measurement of this policy is given.

### Benchmark claim, relayed

The post says that against standard Kubernetes load balancing, Kinference "was able to cut median
time-to-first-token (TTFT) by 95% and median end-to-end latency by 45% of requests on one workload
type". The phrase "45% of requests" is garbled: the benchmark post reports a 45% cut in *median*
end-to-end latency on the shared-prefix workload, not a share of requests. The page description says
"up to 95%". Both figures come from one vendor-run workload on one hardware setup.

### Configuration for agents, documentation for humans

Buoyant expects "the majority of configuration" to be written by LLMs. It also states that "(at least,
as of November 2026) LLMs are terrible at writing technical documentation". The strategy is "write docs
for humans; write guardrails and feedback systems for agents":

- docs written "primarily by hand";
- complete reference docs for every field;
- a `kinfctl` CLI whose purpose "right now" is letting agents validate Kinference YAML without a
  cluster;
- status messages and `kubectl` printer columns on every custom resource (CRD).

They tested this by giving coding harnesses fresh context windows, the docs and `kinfctl`, and fixing
docs or tooling wherever the agent went wrong. The testing is anecdotal and not automated.

### Metrics

Token rates and token-size histograms; TTFT, inter-token latency (ITL) and end-to-end latency
histograms; uncached versus cached prompt tokens "for cost estimation"; model usage and GPU saturation.
"Almost every metric" is available per tenant.

## Why it matters

Kinference is the second Kubernetes-native routing layer in the vault, after the GKE Inference Gateway in
[[Rahul Ranganathan - Inference Gateway on GKE]]. Both treat cache location, queue depth and request
priority as routing inputs (see [[Inference Serving Engines]] and [[KV Cache]]). This post adds two
things. First, it names the conflict between cost-driven [[Model Routing]] and cache locality and proposes a concrete rule
for it: downgrade only when the cheaper route is less total work. Second, it frames routing as one
policy surface that also covers rate limits, tenant accounting, overflow to external providers and data
residency, a platform view rather than a load-balancer view.

## Tensions / open questions

- **"Did not seem to exist" is contestable.** The vault's GKE Inference Gateway source already describes
  Kubernetes-native objects (`InferencePool`, `InferenceModel`) with Critical/Standard/Sheddable
  priority and cache- and queue-aware endpoint picking. Kinference's broader policy scope may be
  new; the underlying idea of policy-driven inference routing on Kubernetes is not.
- **The cost-routing rule is unmeasured.** How Kinference estimates "less work" across two different
  models (whose caches are incompatible) is not explained, and no result is given.
- **"Semantic classification of the prompts"** implies a classifier on the request path, with its own
  latency, error rate and attack surface (see [[Model Routing]]). None is described.
- **PII policy.** Keeping PII inside the environment depends on detecting it. The post states the goal,
  not a detection method or error rate.
- **Vendor launch.** The post includes a livestream promotion ("Free tokens for everyone", November 19)
  and capacity claims aimed at "Platform owners and CFOs". The only performance evidence is Buoyant's
  own benchmark.

## Affected pages

- [[Inference Serving Engines]]
- [[Model Routing]]
- [[Kubernetes]]

## Raw capture

- [[knowledge-base/raw/sources/Kinference Scalable Inference Control Plane for Kubernetes]]

## Citations

- Canonical URL: <https://www.buoyant.io/blog/introducing-kinference>
- By William Morgan (Buoyant), published 2026-11-03; captured 2026-11-17. The capture names Buoyant only
  through the domain and the Linkerd reference; Morgan's role at Buoyant is not stated in the text.
- Project links as given: kinference.ai, kinference.ai/docs, GitHub `Kinference-AI/kinference`.

## Related pages

- [[William Morgan - Distributed Inference Benchmarks Kinference vs Kubernetes]]
- [[Rahul Ranganathan - Inference Gateway on GKE]]
- [[Inference Serving Engines]]
- [[Model Routing]]
- [[KV Cache]]
- [[Kubernetes]]
- [[Serving Benchmarks and Goodput]]
- [[ML Systems at Scale]]
- [[Ben Dickson - Cross-Model KV Cache Handoffs]]
- [[Multi-Tenant Agent Architecture]]
- [[Agent Observability]]
