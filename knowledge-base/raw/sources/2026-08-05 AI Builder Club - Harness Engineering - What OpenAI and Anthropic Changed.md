---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-harness-engineering-agent-production-guide
title: 'Harness Engineering: What OpenAI and Anthropic Changed'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/harness-engineering-agent-production-guide
published: '2026-06-08'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Harness Engineering: What OpenAI and Anthropic Changed

## Why Does the Same Model Perform So Differently Across Products?

A friend asked me to help debug their agent earlier this year. They had the best flagship model, iterated on prompts over 100 times, tuned every parameter they could find. Real-world task success rate: under 70%. Sometimes brilliant, sometimes completely off track.

I looked at their system. The biggest changes I made had nothing to do with the model or the prompts. I changed how tasks were decomposed, how state was managed between steps, how critical checkpoints were validated, and how the system recovered from failures.

Same model. Same prompts. Success rate went above 95%.

That experience didn't have a name at the time. Now it does: Harness Engineering.

Watch the full video on what a harness engineer is and why the role matters:

## What Are the Three Stages of AI Engineering?

Over the past two years, AI engineering went through three distinct shifts. They look like buzzword updates. They're not. Each one answers a progressively harder question.

| Phase | Core Question | What It Optimizes |
| --- | --- | --- |
| **Prompt Engineering** | Did the model understand what I asked? | Intent expression |
| **Context Engineering** | Did the model get the right information? | Information supply |
| **Harness Engineering** | Can the model keep doing the right thing during execution? | Runtime control |

These aren't replacements. They're layers. Prompt is a subset of Context. Context is a subset of Harness. Each one expands the engineering boundary outward.

### Why prompt engineering hit a ceiling

Prompt engineering works because large language models are probability systems extremely sensitive to input framing. You give it a role, it samples from that role's distribution. You give it examples, it continues the pattern. You emphasize constraints, it weights them higher.

The ceiling appeared when tasks stopped being "say the right thing" and became "know the right thing." Analyzing internal documents, answering product configuration questions, writing code against a long specification, coordinating across multiple tools. Prompt engineering can clarify intent, constrain output, and activate latent ability. It cannot replace missing facts, manage dynamic information, or maintain state across a long chain of actions.

### Why context engineering hit a ceiling

Context engineering expanded the boundary. Instead of optimizing the instruction, it optimizes the entire information environment the model sees at decision time: user input, conversation history, retrieval results, tool outputs, task state, intermediate work products, system rules, and structured results from other agents.

But even with perfect information supply, agents still drift. They plan well and execute poorly. They call tools but misread the results. They slowly go off course in long chains with no mechanism to detect it. Prompt and context both operate on the input side. When the model starts acting continuously, who monitors it, constrains it, and corrects it?

### The customer visit analogy

Imagine sending a new hire on an important client meeting.

**Prompt Engineering** = telling them the script: "Greet the client, present the proposal, ask about needs, confirm next steps." Making sure the task is clearly communicated.

**Context Engineering** = packing the briefcase: client background, past meeting notes, product pricing, competitor intel, meeting objectives. Making sure they have the right information.

**Harness Engineering** = everything else for a high-stakes meeting: a checklist to follow, real-time check-ins at key milestones, post-meeting review against the recording, immediate course correction if things drift, and a clear standard for what "success" looks like.

## What Exactly Is a Harness?

LangChain's engineers gave it the cleanest definition:

**Agent = Model + Harness**  
**Harness = Agent - Model**

Everything in an agent system that isn't the model itself is the harness. It decides what the model sees, what it can do, what rules it follows, how failures get caught, and how results get delivered.

ArXiv researchers analyzed Claude Code's codebase. 98.4% of the code is operational infrastructure. 1.6% is AI decision logic. The model is one small component in a much larger system.

![The six harness components surrounding the model: context, tools, orchestration, state and memory, evaluation, constraints and recovery](/images/blog/harness-components-diagram.png "The six harness components surrounding the model: context, tools, orchestration, state and memory, evaluation, constraints and recovery")

## What Are the Six Layers of a Production Harness?

| Layer | Core Question | What It Does |
| --- | --- | --- |
| **1. Context Management** | What does the model see? | Organizes system prompts, project docs, history, task state, external data. Not "more is better" - more relevant is better. |
| **2. Tool System** | What can the model do? | Search, file I/O, APIs, code execution, browser. Also governs when to call tools and how results feed back. |
| **3. Execution Orchestration** | What should the model do next? | Step-by-step flow: understand goal, check info sufficiency, gather if needed, analyze, generate, validate, retry. |
| **4. State and Memory** | How does the system maintain continuity? | Tracks task progress, preserves intermediate results, separates session state from long-term preferences. |
| **5. Evaluation and Observation** | How does the system know it's working? | Output validation, environment verification, automated tests, logs and metrics, error attribution. |
| **6. Constraints and Recovery** | What happens when things go wrong? | Permission boundaries, format validation, retry logic, alternate approaches, rollback to stable state. |

Without context management, the model works with garbage input. Without tools, it's just a text predictor. Without orchestration, it does things out of order. Without state, every turn starts from zero. Without evaluation, it has no idea if it succeeded. Without recovery, one failure kills the whole run.

> We cover each of these six layers in depth - with code, case studies, and production patterns - in [Chapter 9 of the AI Agent Deep Dive](/courses/mastering-ai-agents).

## How Do OpenAI and Anthropic Actually Build Their Harness?

### Anthropic: Context Reset over Compaction

When agents run for hours, the context window fills up. The model starts dropping details, forgetting constraints, and exhibiting "context anxiety" - it seems to know it's running out of room and starts rushing to finish.

The obvious fix is context compaction: summarize the history, compress, keep going. Anthropic tried it. For certain models, it wasn't enough. Compaction makes the context shorter, but the model still carries the weight of a long session.

Their actual solution: **Context Reset**. Spawn a completely fresh agent with a clean context window and hand off the work state explicitly. Like restarting a process to fix a memory leak instead of just clearing the cache.

The handoff must be a structured state transfer, not a conversation summary. Summaries lose detail. Structured handoffs preserve exactly what the next agent needs.

### Anthropic: Separate the Worker from the Judge

Ask a model to do work, then rate its own work. It overrates itself consistently. Same context, same biases, same blind spots.

Anthropic's fix: **Planner + Generator + Evaluator** as three separate roles.

| Role | Job | How |
| --- | --- | --- |
| **Planner** | Expand a vague request into a complete spec | "Build a notes app" becomes detailed requirements |
| **Generator** | Build it step by step | Implements the spec incrementally |
| **Evaluator** | QA like a real user | Opens a browser, clicks buttons, checks interactions |

The Evaluator doesn't read code. It operates the application. Opens pages, fills forms, checks behavior. Environment-level verification, not abstract code review.

The principle: **production and acceptance must be separated.**

### OpenAI: Humans Design Environments, Not Code

OpenAI's Codex team set one rule: **humans write zero lines of code. Humans only design the environment.**

Engineering work became three things:

1. **Decompose intent** - break product goals into tasks an agent can execute
2. **Fill capability gaps** - when an agent fails, ask "what structural capability is the environment missing?" then add it
3. **Close the feedback loop** - make sure the agent can see the results of its own work

Key insight: **when an agent fails, the fix is almost never "try harder." It's "what structural capability is missing?"**

### OpenAI: Progressive Disclosure

Early mistake: one massive AGENTS.md with everything. Result: agent got worse. Context window is a scarce resource.

Fix: AGENTS.md became a ~100-line directory page with pointers to detailed docs.

code

```
AGENTS.md            <- entry point, only pointers
ARCHITECTURE.md      <- architecture overview
docs/
  design-docs/       <- design docs (with verification status)
  exec-plans/        <- execution plans (active/completed/tech debt)
  product-specs/     <- product specifications
  QUALITY_SCORE.md   <- per-module quality scores
  SECURITY.md
```

Agent reads the directory first. Dives deeper when needed. Same pattern as Agent Skills: don't dump everything upfront. Expose on demand.

### OpenAI: Let the Agent See Its Own Work

| Capability | Implementation | What It Solves |
| --- | --- | --- |
| **UI verification** | Chrome DevTools Protocol - screenshots, DOM interaction | Agent sees what users see |
| **Observability** | Per-worktree Loki + Prometheus + Tempo | "Startup time <800ms" is verifiable |
| **Isolation** | Each git worktree is an independent app instance | Multiple agents work in parallel |

Single Codex runs regularly exceed 6 hours. The agent writes code, spins up the app, finds bugs visually, fixes them, verifies through browser and metrics, submits a PR.

### OpenAI: Architecture Rules as Automated Governance

Agents submit 3.5 PRs per engineer per day. Human code review can't keep up. Solution: encode senior engineering judgment into machine-executable rules with strict layer dependencies (Types -> Config -> Repo -> Service -> Runtime -> UI).

**Check results don't just report violations. They tell the agent how to fix them.** The error message becomes part of the next context window, driving the correction loop automatically.

> Want the full breakdown of all six harness layers with production code? [Chapter 9 of the AI Agent Deep Dive](/courses/mastering-ai-agents) covers observability, deployment, security, and these case studies in depth.

## How Do You Build a Harness? A Practical Guide

You don't need OpenAI's infrastructure budget. Here are patterns that scale down to a solo builder.

### Pattern 1: Context Reset for Long Tasks

If your agent runs multi-step tasks longer than ~30 minutes and starts drifting, spawn a fresh agent instead of compacting.

python

```
def context_reset(current_state: dict, original_goal: str) -> dict:
    """Hand off to a fresh agent with structured state."""
    handoff = {
        "original_goal": original_goal,
        "completed_steps": current_state["completed"],
        "in_progress": current_state["current_step"],
        "remaining": current_state["remaining_steps"],
        "key_decisions": current_state["decisions"],
        "artifacts": current_state["file_paths"],
    }
    return handoff
```

Don't pass a conversation summary. Pass a JSON checkpoint: what was the goal, what's done, what's left, what decisions were already made.

### Pattern 2: Separate Evaluator

Use a second model call with a clean context to grade the output. The separation matters more than the evaluator's intelligence.

python

```
def evaluate_output(task_spec: str, output: str, model="claude-sonnet") -> dict:
    """Independent evaluation with clean context."""
    eval_prompt = f"""You are a QA reviewer. You did NOT produce this output.

Task specification:
{task_spec}

Output to evaluate:
{output}

Score each dimension 1-5:
- Completeness: does it address every requirement?
- Correctness: are there factual or logical errors?
- Quality: would a senior engineer approve this?

List specific issues found. Be critical."""

    return call_model(eval_prompt, model=model)
```

Even using the same model, the clean context breaks the self-evaluation bias.

### Pattern 3: Progressive Disclosure for Agent Knowledge

Don't put everything in your system prompt. Build an index layer.

python

```
KNOWLEDGE_INDEX = {
    "architecture": {
        "summary": "Next.js app router, strict layer separation",
        "detail_path": "docs/ARCHITECTURE.md",
    },
    "coding_standards": {
        "summary": "TypeScript strict, no any, server components default",
        "detail_path": "docs/CODING_STANDARDS.md",
    },
    "security": {
        "summary": "Auth via Clerk, row-level security on all tables",
        "detail_path": "docs/SECURITY.md",
    },
}

def get_system_prompt():
    """Index always loaded. Details fetched on demand."""
    index = "\n".join(
        f"- {k}: {v['summary']} (details: {v['detail_path']})"
        for k, v in KNOWLEDGE_INDEX.items()
    )
    return f"Available knowledge:\n{index}\n\nRead detail files when needed."
```

~200 tokens for the index vs ~5,000 tokens for all docs.

### Pattern 4: Let the Agent Verify Its Own Work

python

```
import subprocess, time

def verify_with_tests(code_path: str) -> dict:
    """Run tests and feed results back into agent context."""
    result = subprocess.run(
        ["npm", "test", "--", "--reporter=json"],
        capture_output=True, text=True, timeout=60
    )
    return {
        "passed": result.returncode == 0,
        "output": result.stdout[-2000:],
        "errors": result.stderr[-1000:] if result.returncode != 0 else None,
    }
```

A test runner, a screenshot tool, or even piping server logs back into context. Don't make the agent guess whether the code works.

### Pattern 5: Encode Rules as Self-Correcting Checks

python

```
LAYER_ORDER = ["types", "config", "repo", "service", "runtime", "ui"]

def check_import_direction(file_path: str, imports: list) -> list:
    """Lower layers cannot import from higher layers."""
    file_layer = get_layer(file_path)
    file_idx = LAYER_ORDER.index(file_layer)
    violations = []

    for imp in imports:
        imp_layer = get_layer(imp)
        imp_idx = LAYER_ORDER.index(imp_layer)
        if imp_idx > file_idx:
            violations.append(
                f"VIOLATION: {file_path} ({file_layer}) imports {imp} ({imp_layer}). "
                f"FIX: Move shared logic to {file_layer} layer or lower."
            )
    return violations
```

The violation message tells the agent exactly what to do. The error becomes its own fix instruction.

### Pattern 6: Stuck Detection with Stop-Loss

python

```
class StuckDetector:
    def __init__(self, timeout_seconds=90, max_retries=3):
        self.timeout = timeout_seconds
        self.max_retries = max_retries
        self.retry_counts = {}

    def record_failure(self, action_id: str) -> str:
        self.retry_counts[action_id] = self.retry_counts.get(action_id, 0) + 1
        count = self.retry_counts[action_id]

        if count >= self.max_retries:
            return "STOP: max retries reached. Escalate to user."
        if count == 2:
            return "PIVOT: try a different approach."
        return "RETRY: fix params and try again."
```

A failure ladder (retry -> pivot -> escalate) with a hard stop-loss prevents infinite loops.

## How Does Harness Engineering Change the Engineer's Role?

| Old Thinking | Harness Thinking |
| --- | --- |
| "The model isn't smart enough" | "What information was missing from its context?" |
| "The prompt needs more detail" | "What structural capability is the environment missing?" |
| "We need a better model" | "Is the failure in the model or in the system around it?" |
| "Try again with different wording" | "Add a verification step. Add a recovery path." |

OpenAI's team said it directly: when an agent fails, the fix is almost never "try harder." It's finding the structural gap.

## Key Takeaways

- **Harness = Agent - Model.** Everything around the model that determines whether it delivers reliably. LangChain improved 26% on Terminal Bench 2.0 with zero model changes.
- **Three stages, not three buzzwords.** Prompt optimizes intent expression. Context optimizes information supply. Harness optimizes runtime control. Each is a superset of the previous one.
- **Six layers to audit.** Context management, tool system, execution orchestration, state/memory, evaluation/observation, constraints/recovery. Most agents are missing at least two.
- **Context Reset > Compaction** for long tasks. Spawn a fresh agent with a structured state handoff instead of summarizing.
- **Separate generation from evaluation.** Even the same model with a clean context catches errors the generator missed.
- **Progressive disclosure** keeps the context window effective. Index always loaded, details on demand.
- **Encode rules as self-correcting checks.** Include the fix in the error message.

## Start Building Your Harness

The model gets better every quarter without you doing anything. The harness only gets better if you build it.

Two ways to go deeper:

- **[Agent System Prompt Playbook](/courses/agent-system-prompt-playbook)** (free) - The 12 laws behind every production agent's system prompt, with templates you can copy from 40+ shipped agents.
- **[Mastering AI Agents: The Builder's Deep Dive](/courses/mastering-ai-agents)** - 10 chapters covering agent loops, tool systems, context engineering, memory, multi-agent, evaluation, cost engineering, harness engineering, and frameworks. Chapter 9 goes deep on every harness layer with code.

Harness engineering is the discipline of building the runtime control system around an AI agent. It includes context management, tool orchestration, execution flow, state tracking, evaluation, and failure recovery. LangChain defines it as: Agent = Model + Harness, where the harness is everything except the model itself. ArXiv analysis of Claude Code found 98.4% of the codebase is harness infrastructure.

Prompt engineering optimizes how you communicate with the model (intent expression). Harness engineering optimizes the entire system that keeps the model on track during real execution (runtime control). Prompt is a subset - it is one component within the harness. When tasks are simple single-turn queries, prompt engineering is sufficient. When tasks become multi-step, long-running, and low-tolerance, harness engineering becomes necessary.

Context engineering optimizes what information the model sees at decision time - retrieval, history management, tool outputs, state injection. Harness engineering includes context engineering but adds execution orchestration, evaluation, failure recovery, deployment, observability, and security. Context is the input side. Harness is the full runtime.

Context reset is a technique pioneered by Anthropic for long-running agents. Instead of compressing a long conversation history (compaction), you spawn a fresh agent with a clean context window and pass it a structured state handoff. Use it when your agent runs tasks longer than roughly 30 minutes and starts showing signs of context degradation: rushing to finish, dropping constraints, or losing track of prior decisions.

When the same model generates output and evaluates it, it shares the same blind spots and biases. It consistently overrates its own work, especially on subjective dimensions. Using a separate model call with a clean context breaks this pattern. The evaluator has not seen the generation process, so it catches errors the generator was blind to. Anthropic found this critical for their autonomous coding systems.

Progressive disclosure means not loading all knowledge into the agent context upfront. Instead, you maintain a small index (roughly 50 to 200 tokens) that is always loaded, containing summaries and file paths. Full details are fetched only when a specific task triggers them. OpenAI adopted this after finding that a massive AGENTS.md file made their agent perform worse.

Yes. A harness is not a framework. You can use LangGraph, CrewAI, or the Vercel AI SDK and still have a bad harness. You can use no framework at all and build an excellent harness. Frameworks give you abstractions. The harness is the total operational system: deployment, monitoring, error handling, security boundaries, lifecycle management.

Approximately 80% of agent failures are harness problems, not model problems. The most common: agents stuck in retry loops with no stop-loss, context window overflow with no progressive disclosure, silent failures with no observability, and cascading errors with no recovery mechanism. The model did what it was told. The system around it failed to set it up for success.

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
