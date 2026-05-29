---
type: source-summary
source_id: src-2026-05-28-doordash-llm-judge
source_title: "LLM-as-a-Judge: Evaluating natural language search"
source_author: Xiaochang Miao, Heather Song (DoorDash)
source_url: https://careersatdoordash.com/blog/doordash-llm-as-a-judge-evaluating-natural-language-search/
created: 2026-05-29
updated: 2026-05-29
tags:
  - source-summary
  - llm-evaluation
  - search
  - natural-language-search
status: active
---

# DoorDash - LLM-as-a-Judge for Search Evaluation

## Overview

This source describes how DoorDash operationalized LLM-as-a-judge for natural-language search evaluation. The central idea is not merely to replace humans with a model, but to transform vague relevance grading into explicit binary facets, calibrate the judge against an adjudicated golden set, and then run evaluation continuously as production infrastructure.

## Durable claims

1. Natural-language search queries encode multi-constraint intent beyond keyword matching, including dish, price, vibe, speed, dietary, and discovery constraints.
2. Human annotation showed 30%+ disagreement on boundary cases, and a supervised reranker trained on those labels reached only 0.56 AUC, indicating that label noise was a core bottleneck.
3. The root cause was an underspecified rubric for compositional queries, not simple annotator incompetence; when criteria are vague, both humans and LLMs improvise.
4. DoorDash reframed relevance as independent binary facets such as dish match, modifier match, and constraint satisfaction.
5. Facet-based evaluation reduces variance for both human and LLM judges because it removes ambiguous intermediate grades and anchors judgments in observable evidence.
6. The production workflow has three phases: define rubrics and a golden set, calibrate the LLM judge against adjudicated consensus, then automate execution for monitoring and regression testing.
7. A calibrated LLM judge can catch synonym equivalence, menu-depth mismatches, and constraint violations that hurried human annotators often miss.
8. Continuous LLM evaluation supports daily monitoring and PR guardrails, replacing periodic 2-5 day human-annotation cycles.
9. The article reinforces the G-EVAL lesson that evaluation reliability improves when judges follow explicit, structured, step-by-step criteria rather than unconstrained scoring.

## Affected pages

- [[LLM-as-a-Judge]]
- [[DoorDash]]
- [[Search-Augmented Language Models]]
- [[ML Systems at Scale]]
- [[AI Knowledge Base Overview]]
- [[index|Knowledge Base Index]]
- [[log|Knowledge Base Log]]

## Raw capture

- `knowledge-base/raw/sources/LLM-as-a-Judge Evaluating natural language search.md`

## Related pages

- [[LLM-as-a-Judge]]
- [[DoorDash]]
- [[Search-Augmented Language Models]]
- [[ML Systems at Scale]]
- [[Retrieval-Augmented Generation]]
- [[AI Knowledge Base Overview]]
