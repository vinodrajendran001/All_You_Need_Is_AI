---
type: source-summary
created: 2026-08-03
updated: 2026-08-26
source_id: src-2026-07-30-teaching-open-model-science
source_title: "Teaching an Open Model to Do Science"
source_author: "Bojan Jakimovski, Sara Kovachovska, and Maziyar Panahi"
source_url: https://www.arcee.ai/blog/teaching-an-open-model-to-do-science
tags:
  - source/summary
  - scientific-ai
  - agentic-rl
  - post-training
  - tool-use
source_ids:
  - src-2026-07-30-teaching-open-model-science
status: active
---

# Bojan Jakimovski - Teaching an Open Model to Do Science

## Summary

This case study describes a collaboration between Loka, Arcee AI, Prime Intellect, and AWS that post-trained Arcee's 26B-parameter Trinity Mini MoE (3B active parameters) for scientific workflows. The team built two verifiable reinforcement-learning environments: Drug Tool teaches evidence-seeking through biomedical APIs, while BioReason teaches protein-function and Gene Ontology annotation with strict JSON output. A 21-run GRPO + LoRA experiment program selected run 120, which reached 81.2% on held-out Drug Tool (up from 70.8%) and 0.863 on the BioReason composite score.

## Key claims

- Scientific agents need to distinguish missing evidence from negative evidence, resolve identifiers, recover from failed retrieval, cite usable evidence, and expose uncertainty; fluent prose alone is not a sufficient objective.
- Drug Tool rewards tool choice, arguments, grounded facts, completion, efficiency, concision, and final synthesis. BioReason combines GO F1, ontology-tree similarity, aspect coverage, and strict JSON validity.
- A single GEPA prompt-search pass improved base-model validation before RL, but the team kept the prompt fixed during post-training and spent the remaining budget on data, reward, and optimization changes.
- The experiment loop used fixed protocols, one hypothesis per run, held-out evaluations every 20 steps, representative trace review, and a persistent `runs.jsonl` ledger. Promotion required metrics, verifier/trace review, and workflow testing to agree.
- The promoted adapter was deployed in a Strands/FastAPI/React scientific application with a top-level orchestrator and narrow specialist agents. The open stack preserves control over data flow, policy versions, serving, evaluation, and incident response.

## Why it matters

The source is a concrete bridge between [[Agentic Reinforcement Learning]], [[Reward Design for RL]], and [[Automated AI Research]]. Its durable lesson is that a specialized open model becomes useful when a scientific workflow is encoded as actions plus verifiable outcomes, then trained and promoted through reproducible experiments. It also shows that deployment architecture, trace inspection, and evidence quality remain part of scientific-agent evaluation; benchmark scores alone can reward polished but unsupported answers.

## Tensions / open questions

- The reported scores are environment-specific and do not establish clinical validity, wet-lab success, or general scientific competence.
- Composite verifiers can still miss subtle biological errors, while strict structured-output rewards may trade off against open-ended scientific judgment.
- The method depends on curated tools, datasets, and environments; transfer to other organizations and scientific domains remains an empirical question.

## Affected pages

- [[Agentic Reinforcement Learning]]
- [[Reward Design for RL]]
- [[LLM Training Pipeline]]
- [[Automated AI Research]]
- [[AI Agents in Production]]
- [[Group Relative Policy Optimization]]
- [[Bojan Jakimovski - Teaching an Open Model to Do Science]]

## Citations
- Source URL: [arcee.ai](https://www.arcee.ai/blog/teaching-an-open-model-to-do-science)

## Raw capture

- [[Teaching an Open Model to Do Science]]

## Related pages

- [[Agentic Reinforcement Learning]]
- [[Reward Design for RL]]
- [[LLM Training Pipeline]]
- [[Automated AI Research]]
- [[AI Agents in Production]]
- [[Group Relative Policy Optimization]]
- [[Bojan Jakimovski - Teaching an Open Model to Do Science]]
