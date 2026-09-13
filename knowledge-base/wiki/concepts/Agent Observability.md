---
type: concept
created: 2026-09-11
updated: 2026-09-13
tags:
  - concept
  - ai-agents
  - production
  - observability
source_ids:
  - src-2026-09-06-rastogi-agent-observability
  - src-2026-09-07-bytebytego-llm-error-handling
  - src-2026-09-13-adedeji-multi-agent-code-review
  - src-2026-09-13-prabhulal-production-rag-adk
status: active
---

# Agent Observability

## Definition

The ability to reconstruct, after the fact, the **causal chain** of a single agent run: which input led
to which reasoning step, which tool call with which arguments, returning which result, producing which
final answer, at what cost and latency. It is distinct from two neighbours it is routinely conflated
with. It is not **evaluation** — evals judge whether the chain was *good*; observability establishes what
the chain *was*. And it is not **logging** — a team can hold terabytes of logs and have no observability,
because logs answer "what happened" unstructured, in a form nobody can query during an incident.

The operational test [[Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]]
proposes is a gate: if nobody can answer *what did the agent do, why, and what did it cost* for any
single run from the last 30 days, the system does not touch production traffic.

## Why it matters

Agents fail in a way conventional monitoring is blind to. The failure that matters is not a 500 and not a
malformed response — it is a **fluent, plausible, wrong** answer produced by a chain in which every
individual step reported success. Status codes, latency histograms and error rates all look healthy
throughout.

The incident data quantifies the gap. Across 73 production agent incidents from January to May 2026,
incidents without decision-trace logging averaged **4.2 hours** to resolve against **under an hour** with
full tracing. In a separate eight-week study of 22 fully-traced incidents, roughly **70% of
"fail-plausible" incidents were found by a human noticing something was off, and close to 0% were caught
by unit tests** — because the output is not malformed, only wrong.

This makes observability the prerequisite stage rather than a companion to evaluation. Evaluation needs a
reconstructable run to evaluate; [[Agentic Testing]] needs a reproducible trace to regress against; and
incident response needs to distinguish a retry storm from an attack, which is impossible without
`retry_count` and idempotency keys on the span.

## Current synthesis

**The standard exists.** OpenTelemetry's GenAI semantic conventions, developed by the GenAI SIG since
April 2024, now cover six span types: model calls, agent spans, tool execution, retrieval, memory
operations, and evaluation. The design intent is that traces from different frameworks line up in one
waterfall view without per-team parsing. The spec deliberately keeps prompt and response *content* out of
indexed span attributes and puts it in **span events**, so it can be redacted or filtered at the collector
without touching application code — a compliance property worth getting right before the first audit
rather than after.

**Four layers, each with a failure invisible to the others.**

*Reasoning.* The "fail-plausible" case: a tool rate-limits, returns null with no error field, and the
model — seeing nothing that looks like a hard failure — answers confidently anyway. Two detectors follow,
and both are instrumentation rather than prompting: mark degraded tool results with an explicit
`input.anomalous=true` attribute on the span feeding the next model call, and track a
`fallback_response_rate`. A near-zero fallback rate is **not** reassuring; it means the agent has never
met an ambiguous situation it did not answer confidently. A related silent failure is **context position
bias**, where retrieval technically succeeds but a clause buried mid-context is ignored; the detector is
comparing the rank of the passage actually cited against the rank it was retrieved at.

*Tool call.* This is where side effects live, and an incident here can be completely invisible above it —
247 erroneous refunds were issued through a tool call that *succeeded*, with the LLM layer looking
healthy throughout. The pattern `refund_order(amount=$0.01, count=247)` is only visible at this layer.
Permission gates must **emit a span**, so that a sensitive action executing without an attached approval
span is detectable as a P0. Retries are an amplifier: 20,000 runs/day × 6 tool calls × 0.5% failure × 3
attempts is roughly **1,800 retried calls daily**, each a chance to fire a refund or a write twice — and
without `idempotency_key` and `retry_count` on the span, a retry storm and a prompt-injection campaign
are indistinguishable in the trace. Compare [[LLM Application Resilience]], which arrives at the same
idempotency requirement from the resilience side rather than the forensic side.

*Handoffs.* Trace context must be extracted on the way in and injected on the way out, so a receiving
agent creates a child span under the same trace ID instead of a new orphaned trace. The A2A Traceability
Extension formalises this with parent/child step IDs, per-step cost and token accounting, and error
propagation paths. This is what makes the fan-out patterns in [[Agent Delegation]] auditable rather than
merely fast.

*Hallucination and guardrails.* Online evaluators — Langfuse's production judge running asynchronously
over a sample — are monitoring and triage, not a synchronous safety gate, because the response has already
gone out. A gate needs a cheap fast judge in the response path; Singapore's GovTech published this
pattern for public-service chatbots using lightweight general-purpose models as low-latency security
judges, with F1 competitive against heavier specialised safety models. See [[LLM-as-a-Judge]].

**Guardrails need their own tests — "sabotage validation."** Feed each check known-bad input on a
schedule to confirm it still fires. One team running this found **67 checks silently no-op'ing for
months**. An unvalidated guardrail is indistinguishable from a fake one — the same structure as the
warning in [[Retrieval Poisoning]] that a partially implemented control "manufactures confidence."

**Sampling must be tail-based, not random.** The reason is specific to LLMs: for a payment API, two
similar requests behave similarly, so a 1% random sample is representative. For an LLM call, two
near-identical inputs can produce a correct answer, a hallucination and a policy refusal, so a 1% random
sample gives 1% of the picture with no way to know what is in the missing 99%. The replacement always
captures errors, high latency, low grounding scores and guardrail flags, and samples routine successes at
**5–20%**. AI gateway failover must itself be a traced event, or a silent degradation to a weaker model
looks like a model regression.

**Buying a platform does not buy this.** The reported pattern is that adoption metrics ship early because
they are easy and sell internally, while step-level reasoning traces and cost-per-task attribution arrive
late. Salesforce Agentforce Observability is cited as a fair counter-example — session-level tracing,
subagent drill-down, OTel-compliant, exporting to Datadog or Arize.

## Tracing exposes orchestration cost, not answer quality

[[Ayo Adedeji - Agents That Prove, Not Guess]] reports a Cloud Trace lasting **2 min 28 sec**:
analyzer **4.7 sec**, style checker **5.3 sec**, test runner **1 min 28 sec**, and synthesizer
**47.89 sec**. Testing therefore consumed about **59%** of elapsed time. The useful observation is
not the absolute latency from one tutorial run; it is that a multi-agent trace can reveal which
stage actually owns the budget, rather than attributing the total to "the model."

[[Arjun Prabhulal - Production-Grade RAG with ADK and Vertex AI RAG Engine]] shows the same
instrumentation in a deployment template, mapping each session ID to a Cloud Trace span. But a
trace proving that deployment and retrieval calls completed is not an evaluation of grounding
quality. Production observability needs both operational traces and answer-level evals; neither
substitutes for the other.

## Open questions

- Tail-based sampling at 5–20% of routine successes discards most of the population in which a *slow*
  quality regression would first appear. What trend detection costs is unmeasured.
- The synchronous judge is recommended on every response with no latency budget given, and no measurement
  of what a cheap judge misses relative to the specialised safety models it replaces.
- The 4.2-hour-versus-under-an-hour comparison is observational. Teams that instrument decision traces
  plausibly differ in many other ways from teams that do not.
- The "~70% found by humans, 0% by unit tests" ratio comes from 22 incidents at one runtime — a striking
  number on a very small base.
- Nothing in the current material says how to detect a **semantic** failure automatically. Observability
  makes it reconstructable after a human notices; it does not make it noticeable.

## Related pages

- [[AI Agents in Production]]
- [[LLM Application Resilience]]
- [[Agent Security and Governance]]
- [[Agentic Testing]]
- [[Multi-Turn Evaluation]]
- [[LLM-as-a-Judge]]
- [[Agent Delegation]]
- [[Tool Use and Function Calling]]
- [[Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]]
- [[Ayo Adedeji - Agents That Prove, Not Guess]]
- [[Arjun Prabhulal - Production-Grade RAG with ADK and Vertex AI RAG Engine]]
