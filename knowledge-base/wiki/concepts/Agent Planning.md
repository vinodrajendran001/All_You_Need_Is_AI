---
type: concept
created: 2026-06-05
updated: 2026-11-13
tags:
  - concept
  - ai-agents
  - planning
  - execution
source_ids:
  - src-2026-06-05-pguso-agents-from-scratch
  - src-2026-06-22-djfarrelly-agent-loop-architecture
  - src-2026-08-28-google-cloud-agent-delegation
  - src-2026-09-09-mistral-legacy-code-modernization
  - src-2026-07-20-0xcodez-graph-engineering-roadmap
  - src-2026-11-11-nvidia-gr00t-2
status: active
---

# Agent Planning

## Definition

Agent planning is the process of decomposing a goal into a sequence (or graph) of executable steps before acting. The key insight across every treatment in this vault is that plans are **data structures**, not internal thoughts: a Python dict or JSON object that can be inspected, validated, modified, and reused independently of execution.

## Why it matters

Without a plan, an agent either acts blindly on a single decision or relies on opaque chain-of-thought that is hard to debug. Explicit planning gives a human (and the surrounding system) a window into what the agent is going to do before it does it.

## Current synthesis

### Planning as structured data generation

[[pguso - Agents From Scratch]] makes this distinction sharper than any other source: planning is not sophisticated reasoning — it is the model generating structured JSON:

```python
plan = {"steps": ["Research topic", "Create outline", "Write draft", "Review"]}
```

Because planning is just another call to `generate_structured`, all the same reliability techniques apply: schema constraints, retries, validation before execution.

Separating the planning call from the execution loop means you can:
- Inspect or log the plan before anything runs
- Reject invalid plans early
- Re-use a cached plan across multiple executions
- Modify a plan in response to partial failure without restarting from the goal

### Atomic actions

Vague plan steps like `"Write article"` are unsafe because they are unparseable and untestable. Atomic actions convert each step into the smallest typed operation:

```python
{"action": "generate_text", "inputs": {"topic": "AI agents", "length": "500 words"}}
```

Properties of a good atomic action:
- Has a clear, singular intent
- Has a typed input schema that can be validated before execution
- Either succeeds completely or fails completely (no partial states)
- Is independently testable

The conversion from step-string → atomic-action dict uses the same `generate_structured` + validate + retry pattern as any other structured output call.

### AoT — Atom of Thought dependency graphs

Once you have atomic actions, the natural extension is to express ordering constraints explicitly rather than implicitly relying on sequential execution:

```json
{"nodes": [
  {"id": "1", "action": "research_topic", "depends_on": []},
  {"id": "2", "action": "create_outline",  "depends_on": ["1"]},
  {"id": "3", "action": "write_section_A", "depends_on": ["2"]},
  {"id": "4", "action": "write_section_B", "depends_on": ["2"]},
  {"id": "5", "action": "review",          "depends_on": ["3", "4"]}
]}
```

The graph structure enables:
- **Dependency resolution**: actions with no pending dependencies can start immediately
- **Parallel execution**: independent branches (3 and 4 above) can run concurrently
- **Validation**: circular dependencies and missing node references can be caught before any work is done
- **Observability**: the graph is explicit — you can log and inspect exactly which nodes ran and in what order

The pguso repo calls this AoT (Atom of Thought) and notes it "feels inevitable, not advanced" once you understand planning + atomic actions separately.

### The planning–execution boundary

A pattern that recurs across sources in this vault:
- **Plan** = produce the data structure (cheap, inspectable, reversible)
- **Execute** = act on the world (expensive, consequential, sometimes irreversible)

Keeping these phases separate provides a natural point for validation, human review, resource estimation, and rollback.

### A physical planner–executor split

[[NVIDIA - GR00T 2 - Scaling Robot Foundation Models for Generalization, Dexterity, and Adaptation]] puts this boundary on a robot. A "System 2" agent decides *what* to do in an observe–reason–act–verify loop; GR00T 2 decides *how*, performing contact-rich manipulation. The agent reaches its tools through one tool server, labelled "MCP Server" only in the page's diagram (see [[Model Context Protocol]]): GR00T 2 itself (`wam_act`, `stop_wam`), observation tools (`get_image`, `get_robot_state`, `localize_object`), and code-as-policy skills (`move_to_pose`, `move_to_joints`, `set_gripper`). When a part drops or progress stalls, it repairs the scene with a skill learned with ASPIRE and hands control back. In assembly trials that start from a cluttered layout, the system succeeds in **98**, **97** and **97** of **100** trials (**292/300**), against **71–84** for the same post-trained policy without the agent and **23–69** for supervised post-training alone. In visual steering, the planner marks grasp and release points on GR00T 2's camera view and looks again after each step (see [[Vision-Language Grounding]]). The reasoning model is not named, the contributions of agent and policy are not fully separated, and every number is NVIDIA's own.

### From plan graph to durable execution

[[djfarrelly - The Agent Loop Architecture]] adds a production-runtime requirement to the pguso planning stack. A plan or AoT graph can define the steps, dependencies, and parallel branches, but the execution layer still needs to make each step durable.

The practical bridge is:

- **Plan graph** says what should run and in what dependency order.
- **Atomic actions** make each node typed and validatable.
- **Durable orchestration** checkpoints each node, retries failed nodes without replaying successful ones, manages sub-agent lifecycles, and enforces concurrency.

This distinction matters because a correct plan can still be operationally unsafe if a crash causes already-completed side effects to repeat. Planning makes intent inspectable; orchestration makes execution resumable.

## A stopping criterion for decomposition

Decomposition depth is usually left to judgement. [[Nenad Tomasev and Reshu Yadav - How Agents Can Delegate Better]] proposes a rule: **decompose only as far as each sub-task can be stated as a
verifiable contract.** If a sub-task's completion cannot be checked, the decomposition has gone too
far — the planner has created work it cannot evaluate.

The rule is attractive because it makes decomposition depth a function of the verification available
rather than of task-shaped intuition, and because it composes with routing: where output is cheaply
verifiable, a weaker and cheaper model becomes a bounded risk rather than a gamble
([[Model Routing]]).

It is also demanding in a way the source does not resolve. Many genuinely useful sub-tasks —
summarize this, judge whether the tone is right — have no cheap contract, which on a strict reading
would forbid delegating exactly the work agents are most often used for. See [[Agent Delegation]].

## Dependency structure bounds the plan

[[Mistral - Modernizing Complex Legacy Code with AI Agents]] parses the caller-callee tree and assigns
agents bounded subtrees rather than asking for a whole-system migration. Planning follows dependency
cuts and parity checkpoints, with human approval between stages.

## A plan can be an executable dependency graph

[[@0xCodez - Graph Engineering with Claude - 14-Step Roadmap from 0 to Graph Architect]] takes the
"plans are data structures" view on this page one step further: in Claude Code's dynamic workflows, as
the course describes them, the plan is a JavaScript orchestration script that Claude writes for the
task, "decomposing the task, choosing the fan-out, spawning a coordinated fleet of subagents, and
synthesizing the result", and the script is then what runs. A good run's script can be saved to
`.claude/workflows/` and re-run by name, so a plan becomes a versioned artifact rather than a
one-off.

The course's planning test is about dependencies rather than steps. For every "and then", ask "does the
next step read the last step's output?" A plan written as "do A, then B, then C, then D" is a single
chain, and the course says most chains have "two or three arrows that don't carry data", which are
"just the order you happened to type things in"; cutting those arrows leaves independent steps that can run at once, feeding one step that needs them
all. This complements the Mistral rule above: there, the code's dependency tree bounds the plan; here,
data dependencies between the plan's own steps decide what must wait. The course gives no measure of how
often model-written workflows draw the right edges, and it does not say how such a script is revised
mid-run when a step returns something unexpected, which leaves the first open question below as it was.
See [[Graph Engineering]].

## Open questions

- How should an agent revise its plan mid-execution when early steps fail or return unexpected results?
- When does the plan granularity (coarse steps vs fully atomic) trade off against planning latency?
- How do AoT dependency graphs compose when one agent's plan calls sub-agents with their own plans?

## Related pages

- [[@0xCodez - Graph Engineering with Claude - 14-Step Roadmap from 0 to Graph Architect]]
- [[Graph Engineering]]
- [[Agentic Loop]]
- [[Agent Memory]]
- [[Tool Use and Function Calling]]
- [[AI Agents in Production]]
- [[Agent Skill]]
- [[pguso - Agents From Scratch]]
- [[djfarrelly - The Agent Loop Architecture]]
- [[Direct Corpus Interaction]]
- [[AI Knowledge Base Overview]]
- [[Agent Delegation]]
- [[Model Routing]]
- [[Nenad Tomasev and Reshu Yadav - How Agents Can Delegate Better]]
- [[NVIDIA - GR00T 2 - Scaling Robot Foundation Models for Generalization, Dexterity, and Adaptation]]
- [[Vision-Language Grounding]]
