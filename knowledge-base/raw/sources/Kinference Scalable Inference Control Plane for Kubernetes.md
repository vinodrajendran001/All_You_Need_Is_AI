---
title: "Kinference: Scalable Inference Control Plane for Kubernetes"
source: "https://www.buoyant.io/blog/introducing-kinference"
author:
  - "[[William Morgan]]"
published: 2026-11-03
created: 2026-11-17
description: "Learn about Kinference, the open source inference control plane for Kubernetes. Maximize GPU efficiency, enforce policies, and cut TTFT by up to 95%."
tags:
  - "clippings"
---
![](https://cdn.prod.website-files.com/679957f782f1eca8a9594edb/6ae8fe6c3acdde3a48139768_Blog%20Banner%201000x225.webp)

Today we’re launching [\[K\]inference \[kay-inference\]](https://kinference.ai/), a new open source project for building scalable inference platforms on Kubernetes. For over a decade, we’ve helped companies build mission-critical Kubernetes systems with Linkerd, and \[K\]inference translates this experience and hard-won lessons to the world of LLM inference.

![Kinference logo](https://cdn.prod.website-files.com/679957f782f1eca8a9594edb/6afb46101301346a0f84b5fb_kinference-logo-solid.webp)

Kinference logo

We created \[K\]inference after watching our customers struggle to run open weight models in their environments (and later, from our own struggles). We were all encountering the same challenge: it was difficult to take a truly *platform-centric* approach to distributed inference. As we explored the ecosystem, we realized that while there were plenty of projects focused on serving individual models or optimizing performance across a bank of GPUs, there was nothing focused on building an inference platform.

This was surprising. The concept of a platform is central to how this industry has developed scalable and maintainable software for decades, and you need a control plane to build one! And inference is not special in this regard. A platform is, at its core, a layer that mediates access to a shared, precious resource to a set of distinct and sometimes competing consumers, serving each while ensuring fairness, availability, and security. LLM inference fits this model exactly: you have a limited set of all-too-precious GPUs; and you need to provide shared access to the agents, harnesses, and other “intelligent” applications that all want to use them. An inference platform, then, must mediate between these two (ever-changing) sides, providing maximum flexibility to clients while preserving the availability and reliability of the system as a whole.

We designed \[K\]inference to be the control plane for that platform. It runs on top of inference engines like vLLM, and provides the set of features necessary for building an inference platform in practice. This includes token rate limiting, tenant usage and cost tracking, intelligent load balancing, and inference policies.

![Policy-driven inference serving using Kinference](https://cdn.prod.website-files.com/679957f782f1eca8a9594edb/6ae8fedc128cea3c6399a85d_Kinference%20Graphic%20Update.webp)

Policy-driven inference serving using \[K\]inference

\[K\]inference can be paired with your existing stack. Like an LLM gateway, using Kinference is simply a matter of pointing inference clients to its HTTP endpoint and sending OpenAI or Anthropic-compatible inference traffic there.

If you need to serve a heterogeneous, evolving set of models running on a heterogeneous, evolving pool of GPUs, to a heterogenous, evolving set of clients each with varied and competing demands, and somehow keep everyone happy: \[K\]inference is for you.

(And while \[K\]inference does not use or require Linkerd, it can certainly pair with it!)

## A policy-driven approach

Central to \[K\]inference is the idea of *inference policies*. This concept did not seem to exist anywhere in the Kubernetes inference ecosystem, but is central to our platform-centric approach.

Inference policies give platform owners explicit control over exactly how inference is served, allowing them to balance tradeoffs across usage, performance, and priorities. The need for explicit policies became apparent as we observed our customers tackle questions like:

- How do we allow users to request not just specific model checkpoints (“Qwen 3.8 with 27B params and the FP8 quantization, please”) but broader classes of models, such as “any Qwen 3.8 model” or “whatever is good for coding”?
- How do we redirect “easy” inference requests to cheaper models, even if the user requested an expensive model? And how do we do that without sending the whole prompt history to a cold GPU and incurring a huge latency hit?
- How do we serve batch requests when the GPUs are idle, but reject them when the GPUs are busy with higher-priority work?
- When our GPUs reach saturation, how do we burst extra requests to a third-party inference provider instead of queueing them?
- How do we ensure that prompts with PII never leave our environment?

Answering each of these individually required custom logic for routing inference requests (and, often, for modifying the request bodies themselves!). Rather than build a set of one-off features, we built a policy layer in \[K\]inference that can express them all—and many others as well.

With inference policies, platform owners can create explicit rules for how inference requests should be routed (or rejected) based on tenant, model requested, state of the underlying GPU pool, semantic classification of the prompts, and many other factors. These policies can go through human or agentic review; they can be committed to git; they can be linted and vetted; and they can be applied or rolled back independently.

We think this policy engine is critical for providing a true inference platform. See our [\[K\]inference policy docs](http://kinference.ai/docs/) for more.

## Inference load balancing and performance

In addition to policies and a routing layer, \[K\]inference provides inference-specific load balancing that takes into account signals like GPU queue sizes, historical performance, and the contents of the KV cache on the GPU. This KV-cache awareness, in particular, allows \[K\]inference to send requests to the vLLM worker that will do the least work for that specific request—which not only means it will be the fastest, it will also be the most efficient use of the GPU.

Modeling the KV cache content of the GPU can produce dramatic gains in performance for distributed inference. For example, in our [public \[K\]inference benchmarks](https://buoyant.io/blog/distributed-inference-benchmarks-kinference-vs-plain-kubernetes), we showed that, when compared to standard Kubernetes load balancing (labeled “service” below), \[K\]inference (labeled “kinference”) was able to cut median time-to-first-token (TTFT) by 95% and median end-to-end latency by 45% of requests on one workload type!

![ Kinference tracks which GPU has each prompt prefix cached and sends new requests there, redirecting them to another GPU only when that one is too busy.](https://cdn.prod.website-files.com/679957f782f1eca8a9594edb/6ae4c937d2e925a1c4012dfc_TTFT%20Chart-selection.webp)

\[K\]inference cache-aware routing sends requests that share a prefix to the GPU that already has it cached.

Platform owners and CFOs alike will be pleased, as performance is directly tied to capacity: given a fixed set of GPUs, the faster you can run inference on them, the more inference you can pack onto the same GPUs.

KV-cache awareness also plays a critical role in policies. Popular cost reduction strategies such as sending simpler prompts to cheaper models sound good on paper, but in practice they actually don’t work well since you’ll end up switching GPUs to target the cheaper model – and for multi-turn inference workloads like coding or chat, switching GPUs mid-conversation forces recomputing the entire conversation since it throws away the cached data that so much effort went into creating. By incorporating cache awareness into policies, \[K\]inference provides a practical solution: **platform owners can create policies that will send simple requests to the cheaper model — but only if that’s less work than sending them to the expensive model in the first place**.

## LLM-aware design and UX

We spent a lot of time ensuring that \[K\]inference was usable by humans and agents alike. The reality is that as much as we all love writing lots of YAML by hand, LLMs are actually great at this task, and we expect the majority of configuration for Kinference will be primarily done by LLMs.

However, humans need to *understand* what \[K\]inference is and does, and (at least, as of November 2026) LLMs are terrible at writing technical documentation. Thus, our strategy for \[K\]inference was essentially “write docs for humans; write guardrails and feedback systems for agents”:

1. We wrote the docs primarily by hand, with assistance from LLMs. A human should be able to read through everything on [kinference.ai/docs/](http://kinference.ai/docs/) and not be left scratching their head at convoluted LLM sentence structure and distracting linguistic quirks.
2. We made sure the reference docs were comprehensive and described every field and its properties and limits, so the raw data was always available.
3. We created a \`kinfctl\` CLI whose sole purpose right now is to allow agents to programmatically validate \[K\]inference YAML *without* needing to ship it to a cluster.
4. We gave every \[K\]inference CRD a full suite of status messages, printer columns for \`kubectl\`, and any other affordance we could find to provide feedback to agents on its exact status once it was on the cluster.

We tested this ourselves by starting up common coding harnesses with fresh context windows, pointing them at the docs at [kinference.ai](http://kinference.ai/), installing \`kinfctl\`, and asking the harness to write policies. Where we found the LLM getting confused or going down the wrong path, we updated the docs or added feedback to the tools until this was resolved. (We may automate this kind of testing in the future.)

You and your agents should both be happy with \[K\]inference.

## Inference metrics and SLOs

Finally, we would be remiss if we did not provide a comprehensive suite of inference-related metrics for platform owners to monitor, alert on, and build SLOs around. \[K\]inferenceemits a wealth of information about what’s happening on the system, including not just its own health but:

- Tokens rates in and out, and histograms of input and output token sizes
- TTFT, ITL, and E2E latency histograms
- Uncached vs cached prompt tokens, for cost estimation
- Model usage, GPU saturation, etc
![Kinference makes inference in production efficient by design: cache-aware routing reuses cached prompt tokens, so GPUs stay highly utilized without recomputing prompts, SLOs hold, and costs are tracked per tenant.](https://cdn.prod.website-files.com/679957f782f1eca8a9594edb/6ae909f2b44ccdb00bb3ab5e_Nov%202%20Screenshot%20from%20TinyPNG.webp)

Every request, tenant, model, SLO, and GPU: inference on a platform you control.

Almost every metric is also available per tenant, so you can track tenant usage, build specific SLOs around performance for specific tenants, and everything else you might need to ensure the platform you’re building is living up to its requirements.

## Try it today

Our goal with \[K\]inference is to enable every organization in the world to *own their own intelligence* with a secure, reliable, internal inference platform.

\[K\]inference is fully open source under Apache v2. It’s available on [GitHub](https://github.com/Kinference-AI/kinference) and [easy to get started in a few minutes.](http://kinference.ai/docs/) To see a demo of \[K\]inference, and ask our team your questions, join us for our upcoming livestream, [“Free tokens for everyone”, on Thursday, November 19th, at 9 AM PT](https://www.buoyant.io/register/free-tokens-for-everyone).

[![X](https://cdn.prod.website-files.com/678194e4895761e109e855b5/67db1c17fed959de67fade66_X.svg)](https://twitter.com/intent/tweet?url=https%3A%2F%2Fwww.buoyant.io%2Fblog%2Fintroducing-kinference&text=Kinference%3A%20Scalable%20Inference%20Control%20Plane%20for%20Kubernetes) [![linkedin](https://cdn.prod.website-files.com/678194e4895761e109e855b5/67db1bae0007443929164dd3_LinkedinIcon.svg)](https://www.linkedin.com/feed/?shareActive=true&url=https%3A%2F%2Fwww.buoyant.io%2Fblog%2Fintroducing-kinference)