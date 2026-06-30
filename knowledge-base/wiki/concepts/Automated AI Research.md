---
type: concept
created: 2026-06-02
updated: 2026-06-30
tags:
  - concept
  - agents
  - research
  - automation
source_ids:
  - src-2026-06-02-dwarkesh-eric-jang-alphago
  - src-2026-06-10-itsreallyvivek-frontier-ai-labs
  - src-2026-06-17-nathan-lambert-frontier-post-training-recipe-review
  - src-2026-06-18-alyona-vert-recursive-self-improvement
  - src-2026-06-30-alisa-liu-ai-research-job-search
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
- [[itsreallyvivek - some notes on getting into frontier ai labs]] sharpens the bottleneck language. It argues that frontier research and trench engineering are both really about building useful abstractions when no complete map exists. The scarce resource is not information but **judgment**: picking which anomaly, bottleneck, or question actually deserves attention.
- That framing improves the page's distinction between what agents are already good at and what still resists automation:
  - **Execution** can often be automated or compressed.
  - **Abstraction-building and question selection** remain much harder.
- A durable summary is: automated research becomes more valuable as systems get better at generating possibilities, but that also makes **taste** more important, because the main problem shifts from "can we run this?" to "is this the right thing to run?"
- [[Nathan Lambert - Frontier post-training recipe review with Finbarr Timbers]] adds the organizational version of the same bottleneck. Frontier post-training recipes now require many specialist teachers, data mixtures, RL runs, distillation stages, and integration steps. That makes research automation less like "one agent finds the answer" and more like **coordination across many experimental subprograms**. The hard part is not only running experiments, but maintaining the recipe graph and deciding which specialist branch deserves more compute.
- [[Alyona Vert - AI 101 - What is Recursive Self-Improvement]] adds the recursive-improvement spectrum. Today's systems mostly automate coding, experiments, evaluation, post-training work, and workflow artifacts; stronger [[Recursive Self-Improvement]] would improve the model-building process itself, including data, architectures, training methods, evaluations, and future AI researchers.
- This distinction keeps the page conservative: self-improving agents can optimize prompts, tools, memory, code, or skills without yet reaching true RSI. The hard jump is from improving a workflow to improving the system that creates better AI systems.
- The same "judgment over execution" thesis shows up in hiring. [[ML Research Interview Preparation]] (from [[Alisa Liu - The AI Research Job Search]]) notes that interview *loops* heavily reward technical breadth and coding, but — echoing [[itsreallyvivek - some notes on getting into frontier ai labs]] — the durable ability labs ultimately select for is the research judgment and abstraction-building this page describes. The practical reconciliation: study to pass the loop, but the long-run edge is the same taste/anomaly-selection skill that makes automated research hard.

## Open questions

- What evaluation signal best measures progress for research agents: paper quality, benchmark gains, reproducibility, or something else?
- At what point does the main bottleneck shift from execution to selecting fruitful research directions?
- When does workflow-level self-improvement become model-building-level recursive self-improvement?

## Related pages

- [[Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]]
- [[itsreallyvivek - some notes on getting into frontier ai labs]]
- [[Nathan Lambert - Frontier post-training recipe review with Finbarr Timbers]]
- [[Alyona Vert - AI 101 - What is Recursive Self-Improvement]]
- [[Recursive Self-Improvement]]
- [[Multi-Teacher On-Policy Distillation]]
- [[ML Research Interview Preparation]]
- [[Agentic Loop]]
- [[AI Agents in Production]]
- [[Eric Jang]]
