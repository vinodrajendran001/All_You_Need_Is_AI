---
type: concept
created: 2026-08-25
updated: 2026-08-25
tags:
  - concept
  - agents
  - multi-agent
  - operations
  - governance
source_ids:
  - src-2026-08-22-grok-bot-systems-engineering-working-note
  - src-2026-08-21-anthropic-ai-native-sdlc
  - src-2026-08-05-aibuilderclub-harness-six-components
  - src-2026-08-12-yoko-li-loop-convergence
status: active
---

# Agent Workflow Maturity

## Definition

Agent workflow maturity is the operational discipline that separates a collection of agents from a production system: explicit ownership, durable artifacts, checkable evidence, bounded retries, and encoded approval policy. It is the answer to the question *what has to be true before you can stop watching every run.*

## Why it matters

[[Grok Bot Systems Engineering Working Note]] states the failure condition in one sentence: if any invariant is missing, **the human quietly becomes the memory layer or the recovery system**. That is the specific way agent deployments fail in practice — not with a dramatic error, but with a person silently absorbing the state-tracking, the retry logic, and the verification that the system was supposed to provide. Naming five bots does not create a team if the user still copies context, chooses every next step, and checks every result.

This page is the operations counterpart to [[AI Agents in Production]], which covers architecture and tool interfaces. Here the subject is state, evidence, and recovery.

## The ladder and its exit tests

Maturity is defined by what the system can *demonstrate*, not by how many agents it has:

| Level | Mode | Operating model | Exit test |
| --- | --- | --- | --- |
| 0 | Chat | User routes every task | Useful answer |
| 1 | Role | One durable bot owns a job | Consistent output |
| 2 | Skill | Method is saved and reusable | Repeatable quality |
| 3 | Routine | A trigger starts the work | Unattended run |
| 4 | Team | Manager routes specialists | Parallel delivery |
| 5 | Governed | Evidence, limits, recovery | Reliable system |

The accompanying **architecture decision rule** is the guard against over-building: choose the smallest architecture that externalises the *real* bottleneck. One bot when the problem is execution, a [[Agent Skill|skill]] when it is repeatability, a routine when it is continuity, a specialist when it is durable expertise or permissions, a manager when it is routing, and a verifier when it is trust. Add parallel workers only after inputs and convergence are stable.

## Six invariants and the minimum state

Every production workflow needs one current owner, explicit state, a durable artifact, observable evidence, a bounded retry policy, and a clear approval boundary. The minimum observable state is small: `task_id`, `owner`, `status`, `artifact`, `evidence`, `next_deadline`.

**Choosing the first workflow** is a filter, not an enthusiasm: does the work recur with similar inputs, can a stranger identify completion, is a failed action reversible, can accounts be narrowly scoped, and does it consume enough time to justify supervision. Then **write the finish line before defining the bot** — "review the inbox" is activity; "post one Slack briefing by 08:00 with every newsletter linked, three decisions highlighted, and no email sent" is a finish line.

## Typed handoffs replace conversation

The most transferable idea. A handoff is a **typed interface between owners**, carrying stable task and artifact identifiers, an explicitly named next owner, a consumable schema or link, evidence already produced plus the next acceptance test, and assumptions, risks, deadline, and escalation condition.

| Question | Chat summary | Typed handoff |
| --- | --- | --- |
| What is ready? | Implied | Named artifact |
| Who owns next? | Often unclear | Single owner |
| How to verify? | Narrative claim | Evidence pointer |
| Can it be retried? | Manual | Recorded state |
| Can it be audited? | Expensive | Structured ledger |

Two rules follow. **Ambiguous completion must not advance a workflow** — "done," "looks good," and "I handled it" are not states, and if the producer cannot point to evidence the task stays in verifying or blocked. And **shared state is smaller than shared memory**: specialists keep rich local context while downstream owners receive only what they need to act, which lowers cost and prevents contradictory readings of an old chat. Facts, decisions, artifacts, and evidence stay separate objects so a conclusion can be replaced without rewriting history.

[[Anthropic - The AI-Native SDLC Playbook]] reaches the identical conclusion for software teams, where the typed handoff is a committed `intent.md`, `spec.md`, or `plan.md`. Two independent sources converging on "pass artifacts, not transcripts" is the strongest signal in this area.

## Evidence gates autonomy

Trust is granted against a ladder, not a feeling:

| Level | Evidence | Use |
| --- | --- | --- |
| 0 | Bot says it is done | Never sufficient |
| 1 | Structured summary | Triage only |
| 2 | Logs or source links | Traceability |
| 3 | Screenshot or diff | Visual review |
| 4 | Executed test or video | Behaviour proof |
| 5 | Independent verifier pass | Autonomy gate |

**Producer and verifier must be separate**, because the worker that created an artifact has context and incentives that bias its judgment — and the verifier must report failure without silently repairing the output, so the manager can route the evidence back or escalate. This is the same separation [[Multi-Turn Evaluation]] argues for in evaluation harnesses and that [[Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge]] approaches from the convergence side.

## The manager owns state, not work

A manager normalises requests into task records, routes, tracks dependencies, requests evidence, and decides advance/retry/escalate. It must *not* become the universal backup specialist, because doing specialist work fills its context with execution detail and destroys the role boundary. **Deterministic routing precedes model judgment**: explicit rules for common cases, model classification only above a confidence threshold, a human above a risk threshold. The manager reads a compact ledger first and the conversation only when a field is ambiguous.

Health checks are concrete: no task owned by two specialists, every waiting state naming its dependency and check time, every completed state pointing to evidence rather than a claim, every retry incrementing an attempt counter while preserving the prior artifact, and every human interruption explaining the required decision in one sentence.

## Approval, injection, and idempotency

**Approval is a policy, not a mood** — keyed on reversibility rather than on how confident the bot sounds:

| Action | Default | Reason |
| --- | --- | --- |
| Read approved source | Allow | Reversible observation |
| Draft internal artifact | Allow | No external effect |
| Write reversible record | Allow + log | Recoverable |
| Send or publish externally | Ask | Reputation impact |
| Delete, pay, or change access | Human | Hard to undo |

**Untrusted content is data, not instruction.** Emails, webpages, documents, repository issues, and retrieved text must not be able to expand permissions, change system policy, or redirect secrets — see [[Agent Security and Governance]]. Controls: separate trusted instructions from untrusted content in every task record, stamp acting identity and `task_id` outside model-generated content, rate-limit external writes, and keep an emergency stop that disables triggers *without deleting evidence*.

**Routines need guards.** Every trigger pattern pairs with one: schedule → idempotency by date, event → deduplicate event ID, monitor → rate and severity limit. A stable key prevents duplicate calendar events on retry, and the system must distinguish "not attempted" from "attempted but outcome unknown." **Silence is not success** — emit a heartbeat and escalate past a threshold.

**Parallelism requires independence**: fan out only when workers have stable inputs and separable artifacts, then converge through one evidence gate.

## Convert corrections into infrastructure

When a bot fails, do not add a longer conversational reminder. Ask where the failure belongs — the skill, the environment, the verifier, or a hard policy — and patch that. The result is an accumulating operating system rather than a growing pile of prompt history. This is the operational statement of what [[Agent Skill]] and [[Loop Engineering]] describe as durable method capture.

## Open questions

- **None of this is measured.** The anchor source is entirely prescriptive: no evaluation, no baseline, no reported deployment outcome. The machinery is heavy for a workflow whose value has not been demonstrated, and the candidate scorecard is the only offered guard against over-engineering.
- The top rung assumes a *genuinely* independent verifier, but in practice the verifier is usually the same model family with the same blind spots.
- How much generalises beyond the cloud-agent product shape (dedicated computers, computer use, scheduled routines) that the source describes?
- Where is the crossover at which ledger and handoff overhead exceeds the coordination cost it removes?

## Related pages

- [[Grok Bot Systems Engineering Working Note]]
- [[AI Agents in Production]]
- [[Agent Skill]]
- [[Agent Planning]]
- [[Agent Security and Governance]]
- [[AI-Native Software Development Lifecycle]]
- [[Agentic Loop]]
- [[Loop Engineering]]
- [[Multi-Turn Evaluation]]
- [[Tool Use and Function Calling]]
- [[Grok Bot]]
