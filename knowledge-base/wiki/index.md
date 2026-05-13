---
type: index
created: 2026-05-08
updated: 2026-05-13
tags:
  - index
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
  - src-2026-05-08-murphy-reinforcement-learning-overview
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
  - src-2026-04-22-perplexity-search-augmented-lm
status: active
---

# Knowledge Base Index

Start here. This file is the content-oriented routing layer for the wiki.

## Overviews

- [[AI Knowledge Base Overview]] - Workspace-specific orientation page for this persistent AI knowledge base.

## Concepts

- [[Persistent Wiki]] - The wiki as a durable knowledge layer that compounds over time.
- [[Schema-Driven Knowledge Base]] - Why a schema file turns a generic model into a disciplined maintainer.
- [[Ingest Query Lint Loop]] - The three recurring operations that keep the wiki alive.
- [[Index and Log]] - Why the catalog and ledger are first-class control surfaces.
- [[Reinforcement Learning]] - Hub page for sequential decision making and RL method families.
- [[Tool Use and Function Calling]] - How LLMs request actions from external systems via structured function calls.
- [[Model Context Protocol]] - Open standard (Anthropic) that solves the N×M tool-integration problem.
- [[Agentic Loop]] - The iterative plan-act-observe cycle that enables multi-step LLM tool use.
- [[Search-Augmented Language Models]] - LLMs that use web search as part of generation, with RL-trained tool-use policies.
- [[Reward Design for RL]] - Constructing composite reward signals for multi-objective LLM training.
- [[Group Relative Policy Optimization]] - Relative-policy optimisation method used in the search-agent RL pipeline.

## Entities

- [[Andrej Karpathy]] - Author of the pattern that seeded this implementation.
- [[ByteByteGo]] - Engineering newsletter; source for the tool-use and MCP article.
- [[Obsidian]] - The note environment that acts as IDE, browser, and graph surface for the wiki.
- [[Perplexity]] - AI search company; source for the search-augmented LM training pipeline.

## Sources

- [[Andrej Karpathy - LLM Wiki]] - Summary of the original `LLM Wiki` gist and its implications for this vault.
- [[Kevin Murphy - Reinforcement Learning - An Overview]] - Survey source that seeds the vault's RL area.
- [[ByteByteGo - Connecting LLMs to the Real World]] - Tool use, function calling, and MCP evolution from isolated LLMs to real-world agents.
- [[Perplexity - Advancing Search-Augmented Language Models]] - Two-stage SFT→RL pipeline for training web search agents with gated rewards.

## Queries

- [[2026-05-08 Mathematical Foundations for Reinforcement Learning]] - Structured answer on the math stack needed to move from Murphy's survey to RL expertise.

## Lint reports

- [[2026-05-08 Wiki Lint Pass]] - Structural lint pass covering link integrity, schema conformance, and current wiki gaps.
- [[2026-05-13 Lint Pass]] - Comprehensive lint pass covering structural integrity, coverage, and immediate fixes.
- [[2026-05-13 Lint Pass 2]] - Follow-up lint pass after the Perplexity ingest, covering new-page integration and residual structural issues.

## Control files

- [[knowledge-base/wiki/log|Knowledge Base Log]] - Chronological record of scaffolding, ingests, queries, and lint passes.
