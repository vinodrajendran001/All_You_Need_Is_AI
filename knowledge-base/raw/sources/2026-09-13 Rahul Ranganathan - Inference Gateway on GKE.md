---
type: raw-source
source_id: src-2026-09-13-ranganathan-gke-inference-gateway
title: "Inference Gateway: Intelligent Load Balancing for LLMs on GKE"
author: Rahul Ranganathan
url: "https://medium.com/google-cloud/inference-gateway-intelligent-load-balancing-for-llms-on-gke-6a7c1f46a59c"
published: 2025-04-26
captured: 2026-09-13
created: 2026-09-13
updated: 2026-09-13
tags:
  - source/raw
  - inference
  - serving
  - google-cloud
status: active
---
The rise of Large Language Models (LLMs) has ushered in an era of intelligent applications, transforming how we interact with technology. These sophisticated models, the engines behind groundbreaking innovations, demand robust and scalable infrastructure to power their real-world deployment. For developers and organizations looking to bring these powerful creations to a wide audience, Google Kubernetes Engine (GKE) emerges as a leading platform, expertly designed to orchestrate complex containerized applications.  
At the heart of any reliable and performant application lies effective load balancing. It’s the crucial traffic controller, ensuring requests are distributed evenly and intelligently across available resources, preventing bottlenecks and guaranteeing a seamless user experience.

The specific nature of LLM inference workloads — their intense computational needs and a certain ‘stateful’ persistence across requests — throws a fascinating curveball at traditional network traffic management. Serving an LLM isn’t like serving a typical stateless web application.

> This post delves into the specific load balancing challenges posed by LLM inference, explains the critical role of the Key-Value (KV) cache, introduces the foundational Kubernetes Gateway API, and explores how the GKE Inference Gateway provides an intelligent, AI-aware solution for efficiently serving these demanding workloads on GKE.

## Serving Generative AI workloads vs Traditional web workloads

Traditional web applications often follow predictable patterns: relatively small requests and responses, stateless processing where each request can be handled independently by any available backend instance, and the ability to parallelize many requests.  
Load balancers for these applications focus on distributing traffic evenly based on simple algorithms like round-robin or least connections, or perhaps basic metrics like CPU utilization.  
Generative AI inference workloads, however, operate under a completely different set of rules:

1. **Variable Request/Response Patterns:** LLM requests (prompts) and responses (generated text/data) can vary dramatically in size and processing time. Generating a short answer is vastly different from composing a detailed article or analyzing an image. Latencies can range from seconds to minutes, unlike the millisecond responses expected from many web services.
2. **Intensive Resource Consumption:** A single LLM inference query can often monopolize a powerful accelerator like a GPU or TPU for its duration. This contrasts sharply with web requests that typically consume fewer resources and run in parallel.
3. **Stateful Processing (The KV Cache):** This is the most critical difference. LLMs are autoregressive, meaning they generate output token by token, with each new token depending on the ones generated before it. To do this efficiently, they rely heavily on an internal state mechanism called the Key-Value (KV) cache.

This statefulness fundamentally changes the game for load balancing. It’s no longer sufficient to just spray requests across available replicas; the load balancer needs to be *aware* of the state held within each replica to maintain performance.

## When Round Robin Load Balancing Stumbles

Imagine you’re having a conversation. Each time you speak, the other person needs to remember the context of what was said before to give a relevant reply. Now, imagine that every time you speak, you might be talking to a *different* person who has no memory of the previous exchange. That’s analogous to what happens when traditional load balancing methods meet stateful LLM inference.

Standard Kubernetes Services often use kube-proxy with random or round-robin load balancing.While effective for stateless applications, this approach is detrimental to LLMs:  
1) **Cache Misses:** If request #N in a sequence (e.g., the Nth turn in a chat) lands on Replica A, and request #N+1 lands on Replica B, Replica B’s KV cache is “cold.” It lacks the computed context (the K and V vectors) from the first N tokens.  
2) **Increased Latency:** Replica B must now recompute the state for the first N tokens (a process called “prefill”) before it can even start generating token N+1. This significantly increases the Time To First Token (TTFT) for the user’s *new* response segment and wastes expensive accelerator cycles.  
3) **Reduced Throughput:** Because replicas spend more time recomputing already-calculated states, the overall system throughput (requests processed per unit time) decreases dramatically. Studies comparing random balancing with cache-aware strategies have shown significant drops in TTFT and throughput with random routing.

### What about sticky sessions, the traditional solution for stateful backends?

- **IP-Based Stickiness:** Routing based on client IP address often fails. Multiple distinct user sessions or agentic tasks might originate from the same IP (e.g., behind a NAT or from a single agent framework orchestrator), causing all traffic to overload a single replica while others sit idle.
- **Cookie-Based Stickiness:** This works better for browser-based interactions (like a standard web app login) but is often impractical for programmatic access or agentic systems that don’t naturally handle cookies.

> The core issue is that these traditional load balancing approaches lack visibility into the application’s internal state — the KV cache. They treat the LLM replicas as interchangeable black boxes, which, due to the cache, they are not.

## Understanding the KV Cache

To grasp why load balancing needs to be smarter, let’s briefly demystify the KV cache. At the heart of models are Transformer architectures, which use a mechanism called “ **self-attention** ”.

Think of it like this: to generate the next word in a sentence, the model needs to “pay attention” to the relevant words that came before it. It does this by calculating three vectors for each input token: a Query (Q), a Key (K), and a Value (V). The Query of the current token interacts with the Keys of all previous tokens to determine how much attention to pay to each one. These attention scores then weight the corresponding Value vectors to produce the final output for the current token.

Here’s the crucial insight: when generating the *next* token (token N+1), the model needs the Q vector for token N+1, but it *also* needs the K and V vectors for *all* preceding tokens (1 to N). Recomputing these K and V vectors for every single token generation step would be incredibly inefficient, especially for long sequences.

The **KV cache** solves this by storing the calculated K and V vectors for each token in the sequence in memory (typically GPU memory). When generating the next token, the model computes only the new K and V vectors for the *latest* token and retrieves all the previous ones from the cache.

> *Analogy:* Imagine a stenographer taking notes during a long meeting. To summarize the latest point, they need their notes (the K and V vectors) of everything said previously. Instead of re-listening to the entire meeting recording each time (recomputing), they simply refer to their existing notes (the cache). The KV cache acts as the LLM’s short-term memory for the current context.

This caching makes inference dramatically faster, especially after the first token (which explains the initial pause you sometimes see with chatbots — that’s the “prefill” phase warming up the cache).  
However, it also introduces two key factors for infrastructure:

1. **Statefulness:** The cache represents the model’s understanding of the current context. Losing this cache (by hitting a different replica) forces expensive recomputation. The inference process is no longer stateless; its performance intrinsically depends on the cache’s state.
2. **Memory Consumption:** The KV cache can be surprisingly large, potentially consuming several gigabytes of memory per sequence, sometimes even exceeding the size of the model weights themselves, especially with long contexts or large batch sizes. Managing this memory efficiently is another challenge.

The statefulness introduced by the KV cache fundamentally changes the load balancing objective. It’s not just about distributing load anymore; it’s about **optimizing state locality** (maximizing cache hits) while *simultaneously* balancing load to prevent replica overload. This demands a more sophisticated, context-aware approach that understands the application’s internal workings.

## Setting the Stage: A Primer on Kubernetes Gateway API

Before diving into GKE’s solution, it’s helpful to understand the foundation it builds upon: the Kubernetes Gateway API. This API, now generally available, is the successor to the Ingress API, designed to provide a more expressive, flexible, and role-oriented way to manage traffic routing into and within Kubernetes clusters.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*THPWkTJDDeZw-YFb.png)

GKE Gateway Diagram

It introduces several key resource types:

- **GatewayClass:** A cluster-scoped template defining a *type* of load balancer or proxy implementation (e.g., GKE’s managed load balancer, Istio, Envoy Gateway). It’s typically managed by the infrastructure provider or cluster operator. It specifies the controller responsible for managing Gateways of this class.
- **Gateway:** Represents a request for a specific load balancer instance based on a GatewayClass. It defines listener ports, protocols, TLS settings, and which Routes are allowed to attach. Creating a Gateway resource triggers the provisioning of the actual load balancing infrastructure. Cluster operators typically manage Gateways.
- **Route Resources (e.g., HTTPRoute, GRPCRoute):** Define protocol-specific rules for mapping requests from a Gateway listener to backend Kubernetes services (or other targets). Application developers typically manage these Routes, defining how traffic for their specific application should be handled.

This role-oriented design allows different teams (infra, ops, dev) to manage their respective parts of the configuration safely and independently. The API is extensible, allowing custom resources and implementation-specific configurations to be linked at various layers.

## GKE Inference Gateway

Recognizing the unique needs of AI inference, Google Cloud introduced the **GKE Inference Gateway**. It’s not a completely separate product but rather an *extension* to the standard GKE Gateway controller, leveraging the extensibility of the Gateway API. It specifically implements the open-source Gateway API Inference Extension project.

GKE Inference Gateway introduces the following new Gateway API Custom Resource Definitions (CRDs), aligned with the [OSS Kubernetes Gateway API extension for Inference](https://gateway-api-inference-extension.sigs.k8s.io/concepts/api-overview/).Its core purpose is to provide optimized routing and load balancing specifically tailored for generative AI workloads running on GKE. It introduces new CustomResourceDefinitions(CRDs)

- `**InferencePool**` **object**: represents a group of Pods (containers) that share the same compute configuration, accelerator type, base language model and model server. This logically groups and manages your AI model serving resources. A single `InferencePool` object can span multiple Pods across different GKE nodes and provides scalability and high availability.
- `**InferenceModel**` **object**: specifies the serving model's name from the `InferencePool` according to the `OpenAI API` specification. The `InferenceModel` object also specifies the model's serving properties, such as the AI model's `Criticality`. GKE Inference Gateway gives preference to workloads classified as `Critical`. This lets you multiplex latency-critical and latency-tolerant AI workloads on a GKE cluster. You can also configure the `InferenceModel` object to serve LoRA fine-tuned models.
- `**TargetModel**` **object**: specifies the target model name and the `InferencePool` object that serves the model. This lets you define Gateway routing policies, such as traffic splitting and request mirroring, and simplify model version rollouts.

## GKE Inference Gateway Request Flow

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*o_WIEL8rEJk1JOq4fs_IJg.png)

> *Client sends OpenAI-like request to GKE model.  
> Body-based routing extension extracts model ID for HTTPRoute-based routing.  
> Security extension enforces model policies (filtering, threat detection, logging) on requests/responses.  
> Endpoint picker extension routes to optimal replica based on KV-cache, queue length, and active LoRAs for low latency/high throughput.*

## How does GKE Inference Gateway solve the challenges discussed earlier

1. **Optimized, Metric-Driven Load Balancing:  
	**This is the heart of the solution. Instead of relying on simple algorithms or basic network metrics, GKE Inference Gateway makes routing decisions based on real-time metrics reported directly from the backend model server Pods.

> **KV Cache Utilization Awareness:** The gateway actively monitors the KV cache usage level on each model server replica.When a new request arrives, particularly one that might share a prefix with ongoing conversations (like subsequent turns in a chat), the gateway attempts to route it to a replica where that prefix is likely already cached (“cache affinity”). This maximizes cache reuse, significantly reducing the need for costly prefill operations and lowering TTFT.

- *Analogy: Directing your follow-up question to the specific stenographer who took the relevant notes.*

> **Queue Length Awareness:** Simply routing to the replica with the best cache hit isn’t always optimal if that replica is already swamped. The Inference Gateway also monitors the queue depth of pending requests at each replica.If a replica has a long queue, the gateway might route the request elsewhere, even if it means a potential cache miss, to avoid excessive wait times and balance the load across the pool. This capability allows application-level custom metrics to be reported to Cloud Load Balancing in response headers that use the Open Request Cost Aggregation ([ORCA](https://github.com/envoyproxy/envoy/issues/6614)) standard

- *Analogy: Checking if the best-suited stenographer is currently overwhelmed before giving them more dictation.*

> **Endpoint Picking Logic:** An internal component, the “endpoint picker extension,” continuously monitors these key metrics (KV cache utilization, queue length, and even active LoRA adapters) from the model servers. It uses a cost function or algorithm to dynamically select the most suitable backend Pod for each incoming inference request, balancing the goals of maximizing cache hits and maintaining even load distribution.

**2\. Model-Aware Routing:**

> The gateway understands the concept of different models. It can inspect the incoming request (often formatted according to OpenAI API specs) to identify the requested modelName. This allows you to define routing rules in your HTTPRoute that direct requests for model-a to one pool of replicas and requests for model-b to a different pool, using dedicated InferencePool resources as backend targets.

**3\. Dynamic LoRA Serving:**

Low-Rank Adaptation (LoRA) is a popular technique for efficiently fine-tuning LLMs. Instead of retraining the entire massive model, LoRA creates small “adapter” weights for specific tasks or datasets.

> GKE Inference Gateway supports serving multiple different LoRA adapters dynamically, multiplexed onto a shared pool of replicas running the *same* base model.When a request specifies a particular LoRA adapter (via the modelName), the gateway routes it to a replica that can load and apply that adapter on the fly.

This drastically reduces the number of accelerators needed compared to deploying a separate full model replica for each fine-tuned version, leading to significant cost savings and improved hardware utilization. This capability significantly lowers the barrier for deploying customized LLM experiences economically.

**4\. Request Criticality (Prioritization and Load Shedding):**

Not all inference requests are created equal. An interactive chatbot requires low latency, while a batch job analyzing documents might be more tolerant of delays.

> GKE Inference Gateway allows you to assign a criticality level (Critical, Standard, or Sheddable) to different models or request types. When the system is under heavy load, the gateway prioritizes Critical requests, ensuring they get served even if it means delaying or dropping lower-priority (Standard or Sheddable) requests.

Sheddable requests might be dropped entirely if no suitable replicas (e.g., those with low KV cache utilization and short queues) are available, protecting the performance of critical applications.  
*Analogy: An emergency room triaging patients based on the severity of their condition.*

**5\. Integrated AI Safety and Observability:**

The gateway integrates with Google Cloud Model Armor for applying safety checks to prompts and responses.It also provides built-in observability, exporting metrics like request rates, latency, errors, and saturation specific to the inference workload, allowing for effective monitoring and performance tuning.

**Summary:**  
In essence, Google Kubernetes Engine is evolving beyond generic container orchestration by embedding AI-specific intelligence directly into its networking fabric. The GKE Inference Gateway tackles the unique stateful and resource-intensive nature of AI inference, offering optimized performance, better resource utilization, significant cost savings and simplified management for the ever-growing deployment of AI workloads on Kubernetes

## References:

## [KV Caching Explained: Optimizing Transformer Inference Efficiency](https://huggingface.co/blog/not-lain/kv-caching?source=post_page-----6a7c1f46a59c-----------------------------------------)

### A Blog post by Hafedh Hichri on Hugging Face

huggingface.co

## [Understanding new GKE inference capabilities | Google Cloud Blog](https://cloud.google.com/blog/products/containers-kubernetes/understanding-new-gke-inference-capabilities?e=48754805&source=post_page-----6a7c1f46a59c-----------------------------------------)

### Together, new GKE Inference Quickstart and GKE Inference Gateway help set up inference environments while improving…

cloud.google.com

## [Advanced LLM Serving Architectures: Load Balancing, Caching, and Cost Optimization - AI Resources](https://www.modular.com/ai-resources/advanced-llm-serving-architectures-load-balancing-caching-and-cost-optimization?source=post_page-----6a7c1f46a59c-----------------------------------------)

### As we advance into 2025, the deployment of advanced Large Language Models (LLMs) in various applications is…

www.modular.com

## [Getting started - Kubernetes Gateway API Inference Extension](https://gateway-api-inference-extension.sigs.k8s.io/guides/?source=post_page-----6a7c1f46a59c-----------------------------------------)

### Experimental This project is still in an alpha state and breaking changes may occur in the future. A cluster with…

gateway-api-inference-extension.sigs.k8s.io

## [DéjàVu: KV-cache Streaming for Fast, Fault-tolerant Generative LLM Serving](https://arxiv.org/html/2403.01876v1?source=post_page-----6a7c1f46a59c-----------------------------------------)

### Foteini Strati Sara Mcallister Amar Phanishayee Jakub Tarnawski Ana Klimovic Abstract Distributed LLM…

arxiv.org

## [About GKE Inference Gateway | GKE networking | Google Cloud](https://cloud.google.com/kubernetes-engine/docs/concepts/about-gke-inference-gateway?source=post_page-----6a7c1f46a59c-----------------------------------------)

### Preview This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service…

cloud.google.com