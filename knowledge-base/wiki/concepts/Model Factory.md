---
type: concept
created: 2026-08-03
updated: 2026-08-03
tags: [concept, training, research, reproducibility]
source_ids:
  - src-2026-07-23-latent-space-eiso-kant-poolside-model-factory
status: active
---

# Model Factory

A model factory is the reproducible operating system around model development: versioned data and code, configurable training mixtures, experiment records, evaluation gates, and deployment artifacts. It turns training from an artisanal run into a repeatable, inspectable production process.

## Current synthesis

- Immutable inputs and recorded configurations make an experiment explainable and rerunnable.
- Data mixtures should be streamed and configurable rather than manually rebuilt for every run.
- Automation can increase experimental throughput, but humans still set research direction, evaluate surprising results, and decide promotion.
- The factory complements an [[Agentic Loop]]: the loop controls an agent at inference time, while the factory controls the lifecycle that creates and evaluates the agent or model.

## Related pages

- [[Latent Space - Inside the Model Factory - Eiso Kant, Poolside AI]]
- [[Automated AI Research]]
- [[LLM Training Pipeline]]
- [[Coding Agent Harness]]
- [[Recursive Self-Improvement]]
