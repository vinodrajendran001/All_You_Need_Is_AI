---
type: concept
created: 2026-06-02
updated: 2026-06-02
tags:
  - concept
  - agents
  - research
  - automation
source_ids:
  - src-2026-06-02-dwarkesh-eric-jang-alphago
status: active
---

# Automated AI Research

## Definition

Automated AI research is the use of LLM- or agent-driven systems to help formulate, implement, run, evaluate, and iterate on AI experiments and research artifacts.

## Why it matters

This is one of the clearest real-world paths by which AI capability could recursively accelerate further AI progress. It matters not because models suddenly become autonomous scientists overnight, but because they can begin to compress parts of the research loop before they can replace the whole thing.

## Current synthesis

- The Eric Jang interview frames research automation as an **autoresearch loop** rather than a one-shot assistant feature. The interesting question is not only whether a model can answer research questions, but whether it can keep iterating through experiments.
- The current sweet spot appears to be **execution-heavy tasks**: implementing experiments, running them, and optimizing hyperparameters.
- The harder bottlenecks remain **research taste and navigation**: deciding the next question worth asking, recognizing when a line of inquiry is a dead end, and changing course intelligently.
- The flashcard-generation workflow described in the same source is a smaller but concrete example of this pattern: a durable agent can read a transcript, incorporate blackboard screenshots, generate visuals, and pass outputs through a critic more effectively than a loose chain of calls.
- This concept fits naturally alongside the [[Agentic Loop]]: the loop is the general control pattern, while automated research is one high-value application domain with unusually strong feedback loops and unusually costly mistakes.

## Open questions

- What evaluation signal best measures progress for research agents: paper quality, benchmark gains, reproducibility, or something else?
- At what point does the main bottleneck shift from execution to selecting fruitful research directions?

## Related pages

- [[Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]]
- [[Agentic Loop]]
- [[AI Agents in Production]]
- [[Eric Jang]]
