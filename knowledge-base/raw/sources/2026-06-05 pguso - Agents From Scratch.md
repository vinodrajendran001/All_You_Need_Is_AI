---
type: raw-source
source_id: src-2026-06-05-pguso-agents-from-scratch
title: AI Agents from Scratch
author: pguso (GitHub)
url: https://github.com/pguso/agents-from-scratch
captured: 2026-06-05
status: immutable
tags:
  - source/raw
  - agents
  - tutorial
  - python
  - local-llm
---

# AI Agents from Scratch

## Bibliographic snapshot

- **Author:** pguso (GitHub handle)
- **Repository:** [https://github.com/pguso/agents-from-scratch](https://github.com/pguso/agents-from-scratch)
- **Related JS version:** [https://github.com/pguso/ai-agents-from-scratch](https://github.com/pguso/ai-agents-from-scratch)
- **Related product version:** [https://github.com/pguso/ai-product-from-scratch](https://github.com/pguso/ai-product-from-scratch)
- **Stack:** Python, llama-cpp-python, local GGUF models (Llama-3-8B, Mistral 7B, Gemma 7B)
- **License:** MIT
- **Captured:** 2026-06-05

## Purpose

A gentle, local-first introduction to AI agents. No frameworks, no cloud APIs, no hidden reasoning. Teaches how agents *work* (mechanical understanding) rather than how to *use* frameworks.

## Philosophy (PHILOSOPHY.md summary)

**What is avoided:**
1. Framework abstractions (LangChain, CrewAI, AutoGen hide mechanisms)
2. Anthropomorphic language ("agents think/reason/understand" — they process text)
3. Hidden reasoning (no opaque chain-of-thought steps)
4. Premature autonomy (autonomy is added last, not first)

**Core beliefs:**
- Agents are systems, not personalities: `while not done: observe → decide → act`
- Structure beats cleverness: mediocre prompt + good structure > clever prompt + free-form output
- Constraints enable reliability: more constrained action space = more reliable behaviour
- Simplicity scales: complex agents from simple patterns repeated consistently

**Why no ReAct:** ReAct conflates reasoning (opaque) with planning (data); tool calling + good prompts accomplishes the same goals more explicitly.

**Why local models:** No API costs, no rate limits, full control, privacy, learn the full stack.

## 12-lesson curriculum

The repo builds ONE continuously evolving `agent/agent.py` across 12 lessons:

| Lesson | Capability | Key concept |
|--------|-----------|-------------|
| 01 | Text in / text out | Prompts, tokens, context window |
| 02 | Roles and behavior | System prompts, instruction hierarchy |
| 03 | Structured output | JSON contracts, validation + retries |
| 04 | Decisions (routing) | Finite choice space, intent detection |
| 05 | Tools | Request/execute separation, structured tool calls |
| 06 | Agent loop | Observe → decide → act, state transitions, termination |
| 07 | Memory | Short-term context vs long-term storage, explicit persistence |
| 08 | Planning | Plans as data structures (not thoughts), step ordering |
| 09 | Atomic actions | Smallest valid operation, typed execution, schema validation |
| 10 | AoT (Atom of Thought) | Dependency graphs, validated execution order, parallel readiness |
| 11 | Evals | Golden datasets, regression testing, hard vs soft assertions |
| 12 | Telemetry | Spans, traces, structured logging, runtime metrics |

**Curriculum structure:**
- Lessons 1–3: Foundation (LLM basics)
- Lessons 4–6: Agency (decisions, tools, loops)
- Lessons 7–10: Intelligence (memory, planning, execution)
- Lessons 11–12: Observability (evals, telemetry)

## Key lesson details

### Lesson 03 — Structured Output
```python
def generate_structured(self, user_input: str, schema: str) -> dict | None:
    # Strong CRITICAL INSTRUCTIONS prompt
    # temperature=0.0 for determinism
    # extract_json_from_text() handles extra text
    # Retry up to 3 times
```
- Never trust LLM output directly: parse → validate → handle failures
- LLMs are probabilistic; retries turn probabilistic into reliable

### Lesson 05 — Tools
- "The model **requests** tools. The system **executes** them. No autonomy yet."
- Separation gives: access control, validation, human-in-the-loop
- Adding tools = adding interfaces, not retraining the model

### Lesson 06 — Agent Loop
```python
while not self.state.done and self.state.steps < max_steps:
    action = self.agent_step(user_input)
    if action.get("action") == "done":
        self.state.mark_done()
```
- "An agent is not a clever prompt. It's a loop with state."
- max_steps is a required safety mechanism

### Lesson 07 — Memory
- Context = temporary (in-prompt). Memory = persistent (across interactions).
- Agent controls what to save via explicit `save_to_memory` field in structured output
- Simple "get all" retrieval is powerful enough to start

### Lesson 08 — Planning
```python
plan = {"steps": ["step1", "step2", "step3"]}
```
- Plans aren't thoughts — they're data structures
- Planning = structured data generation, not sophisticated reasoning
- Separating planning from execution enables inspection, modification, debugging

### Lesson 09 — Atomic Actions
- Convert `"Write article"` → `{"action": "generate_text", "inputs": {"topic": "...", "length": "..."}}`
- Small steps = safe systems
- Validates before execution: "action" + "inputs" fields required

### Lesson 10 — AoT (Atom of Thought)
```json
{"nodes": [
  {"id": "1", "action": "research", "depends_on": []},
  {"id": "2", "action": "write", "depends_on": ["1"]}
]}
```
- Natural evolution of planning + atomic actions + dependencies
- Dependency resolution enables eventual parallel execution
- Validate graph structure before running (check no circular deps, all refs valid)
- "At this point, AoT feels inevitable, not advanced."

### Lesson 11 — Evals
```
Golden dataset → Run evals → Pass/fail report → Fix or revert → Commit
```
- Evals are just assertions: run agent, check output, report pass/fail
- Golden datasets = version-controlled source of truth
- Hard assertions first (JSON valid, fields present, tool in list), soft assertions later
- Run before every prompt change — "catch regressions before deployment"

### Lesson 12 — Telemetry
```json
{"span_id": "a1b2", "trace_id": "x9y8", "event_type": "llm_call", "duration_ms": 1523, ...}
```
- Spans = single operations; Traces = full agent interactions (linked by trace_id)
- JSONL format (one JSON object per line), searchable by `grep "trace_id"`
- Metrics: llm_success_rate, avg_latency_ms, tool_failure_rate
- "Telemetry = structured logging + traces + metrics"

## Repository structure

```
agent/
  agent.py      — Main Agent class (evolves across all 12 lessons)
  memory.py     — Memory system
  planner.py    — Planning + atomic actions + AoT
  state.py      — AgentState (steps, done, current_plan)
  tools.py      — Tool definitions + execute_tool()
  evals.py      — Evaluation framework
  telemetry.py  — Telemetry system
evals/
  golden_datasets.py — Known-good test cases
shared/
  llm.py, prompts.py, utils.py — Reusable utilities
lessons/
  01–12 lesson markdown files
complete_example.py — All 12 lessons demonstrated in isolation
```

## Capture notes

- Full content fetched via GitHub API on 2026-06-05.
- All 12 lesson .md files and the README, PHILOSOPHY, QUICKSTART were read in full.
- Core Python files (agent.py, planner.py, evals.py, telemetry.py) were listed and code samples extracted from lesson files.
