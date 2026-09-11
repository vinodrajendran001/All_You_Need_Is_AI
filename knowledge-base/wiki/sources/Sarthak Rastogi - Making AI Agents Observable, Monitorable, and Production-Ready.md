---
type: source-summary
created: 2026-09-11
updated: 2026-09-11
source_id: src-2026-09-06-rastogi-agent-observability
source_title: "Making AI Agents Observable, Monitorable, and Production-Ready [Tutorial + Code]"
source_author: Sarthak Rastogi
source_url: https://sarthakai.substack.com/p/making-ai-agents-observable-monitorable
tags:
  - source/summary
  - ai-agents
  - production
  - observability
source_ids:
  - src-2026-09-06-rastogi-agent-observability
status: active
---

# Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready

## Summary

An implementation guide arguing that observability is the gate an agent must pass before it is allowed
production traffic, and that the gate is not logging. The framing sentence is operational rather than
philosophical: if nobody can answer *"what did the agent do, why did it do that, and what did it cost"*
for any single run from the last 30 days, it **"does not touch production traffic."**

Rastogi separates observability from two neighbours it is routinely confused with. It is not evals —
"evals are a separate, complementary discipline — they tell you whether that chain was *good*". It is
not logging — "a team can have TBs of logs and still have zero observability, because logs answer 'what
happened' at best, in an unstructured way that nobody can query when they're panicking during an
incident." What it *is*: the ability to reconstruct **a causal chain** — "this input, led to this
reasoning step, led to this tool call, with these arguments, which returned this result, which led to
this final answer, at this cost, in this latency."

The material is organised as four layers — reasoning, tool call, handoff, hallucination — each with a
failure mode that is only visible at that layer.

## Key claims

**Tracing cuts incident resolution by roughly a factor of four.** Sherlocks AI analysed 73 production
agent incidents between January and May 2026 across real deployed systems: "incidents without
decision-trace logging averaged 4.2 hours to resolve; incidents with full tracing resolved in under an
hour." Their diagnosis of the gap is quoted: *"The observability gap in 2026 is not about having too
little data — most teams have more telemetry than they can read. It is about having no visibility into
the reasoning layer where agent decisions actually happen."*

**Failures cascade upward from the tool layer.** In the same dataset, "tool-call failures were the
single most common entry point — but they almost never travelled alone. They cascaded into planning
failures, into wrong final answers, and only then into a human."

**OpenTelemetry's GenAI semantic conventions now cover six span types** — model calls, agent spans, tool
execution, retrieval, memory operations, and evaluation — developed by the GenAI SIG since April 2024.
The point of standardising is that "traces across different sources should all line up in the same
waterfall view without custom parsing per team."

**The spec deliberately keeps prompt and response *content* out of indexed span attributes and puts it
in span events**, "specifically so it can be filtered or redacted at the collector level without
touching application code." Rastogi's advice is blunt: if your agent logs full prompts as plain
attributes, "fix that before your first compliance review, not after."

**"Fail-plausible" incidents are invisible to tests and mostly caught by humans.** A study of a
production agent runtime documenting 22 fully-traced incidents over eight weeks found that "roughly 70%
of fail-plausible incidents were discovered by a human noticing something was off, and close to 0% were
caught by unit tests — because the output isn't malformed, it's just wrong." The worked example: a
warranty tool rate-limited during a deploy spike returns null with no error field, and the model, "seeing
nothing that looks like a hard failure", tells the customer their device is covered.

**Two counter-measures follow, and both are detectors rather than prompts.** Flag empty, truncated, or
error-shaped tool results with an explicit `input.anomalous=true` attribute on the span feeding the next
LLM call; and track a `fallback_response_rate`. On the latter: "if that rate is near 0, that's not a good
sign, it just means your agent has never met an ambiguous situation it didn't confidently answer anyway."

**Guardrails must themselves be tested with known-bad input — "sabotage validation".** The same study
"found 67 checks in their own system that had been silently no-op'ing for months before anyone noticed",
because "an unvalidated guardrail is indistinguishable from a fake one."

**Retrieval can succeed and still fail, through context position bias.** "Models disproportionately
weight content at the start and end of a context window, so a critical policy clause buried in the
middle of five retrieved documents can be ignored even though retrieval technically 'worked.'" The
detector is a rank comparison: track the rank of the passage the model actually cites against the rank
it was retrieved at.

**The tool layer is where an incident can be entirely invisible above it.** Citing a case where "247
refunds were given to customers when they shouldn't have been": "the refund actually processed because a
tool call *succeeded*. At the LLM layer, everything looked healthy." The pattern
`refund_order(amount=$0.01, count=247)` was only ever visible at the tool-call layer.

**Retries multiply side effects at a rate worth computing.** "20,000 agent runs a day at six tool calls
each: a 0.5% per-call failure rate with three retry attempts works out to roughly 1,800 retried calls
daily — 1,800 separate chances, every single day, to fire a refund, an email, or a DB write twice."
Without an idempotency key and a `retry_count` span attribute "you cannot tell, from the trace alone,
whether that was N distinct exploit attempts or a much smaller number of legitimate-looking requests
that a retry loop quietly multiplied. One is a prompt-injection problem, the other is a
distributed-systems problem."

**The permission gate must be traced, not merely present.** "If a sensitive action ever executes without
an approval span attached to it, that's a P0, and it's only detectable because the gate emits a span."
And on why instructions are not a control: "Explicit instructions are not a safety layer — they're a
suggestion the model is statistically likely to follow, which is a different thing."

**Trace context must propagate across agent handoffs**, extracted on the way in and injected on the way
out so the receiving agent creates a child span under the same trace ID rather than "a new orphaned
trace". The A2A Traceability Extension formalises this for agent-to-agent protocols with parent/child
step IDs, per-step cost and token accounting, and error propagation paths.

**Random sampling is wrong for LLM traffic, and the reason is specific.** Citing Groundcover: for a
payment API "two requests that look similar probably behave similarly", but for an LLM call "two
requests with near-identical inputs can produce wildly different outputs — one correct, one
hallucinated, one a policy refusal. Random 1% sampling doesn't give you 1% of a representative picture;
it gives you 1% of the picture with no way to know what's in the missing 99%." The replacement is
**tail-based, outcome-aware sampling**: always capture errors, high latency, low grounding scores and
guardrail flags; sample routine successes at 5–20%.

**Online evals are triage, not a gate.** Langfuse's production evaluator runs LLM-as-judge against a
sample of live observations asynchronously, "after the response has already gone out... They are not, by
themselves, a synchronous safety gate." For the gate you want a fast cheap judge in the response path —
Singapore's GovTech published this pattern for public-service chatbots, using "lightweight
general-purpose models as low-latency security judges, catching jailbreaks and prompt injection with F1
scores competitive with much heavier specialized safety models."

**Buying a platform does not buy observability.** Rastogi names Microsoft Copilot Studio and Writer.com
as not shipping enough built in, and cites Salesforce Agentforce as "a fair counter-example worth citing
accurately" — session-level tracing, subagent drill-down, and an OTel-compliant model exporting to
Datadog or Arize, free with every customer. The general pattern he objects to: "adoption metrics ship
fast because they're easy and sell internally. Step-level reasoning traces and cost-per-task attribution
arrive late."

## Why it matters

The vault has carried production-readiness material that treats evaluation as the discipline standing
between a demo and a deployment. This source inserts a prior stage and argues it is the binding one: you
cannot evaluate what you cannot reconstruct, and the incident data says the reasoning layer is precisely
where reconstruction fails.

Two findings are genuinely uncomfortable and worth preserving as such. The first is that a
**near-zero fallback rate is a defect signal**, which inverts the intuition that a confident agent is a
working one. The second is **sabotage validation** — 67 silently dead checks — which generalises well
beyond agents and is the strongest argument in the source for treating a guardrail as code that needs
its own test.

The retry arithmetic also connects to [[LLM Application Resilience]] from the other direction. That page
treats retries as a resilience technique; this source treats the same mechanism as an amplifier of side
effects that is indistinguishable from an attack unless the trace carries `retry_count` and an
idempotency key.

## Tensions / open questions

- The Sherlocks AI study (73 incidents) and the 22-incident runtime study are both cited without links
  in the capture, and the 4.2-hour-versus-under-an-hour comparison is observational: teams that
  instrument decision traces plausibly differ from teams that do not in many other ways.
- The "roughly 70% found by humans, close to 0% by unit tests" figure is drawn from 22 incidents at one
  runtime. It is a striking ratio on a very small base.
- Tail-based sampling at 5–20% of routine traffic still discards most successful runs, which is exactly
  the population in which a slow quality regression would first appear. The source does not address
  what tail-based sampling costs you in trend detection.
- The synchronous judge is recommended on every response, but the source gives no latency budget for it
  and no measurement of what a cheap judge misses relative to the heavier safety models it replaces.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Agent Observability]]
- [[AI Agents in Production]]
- [[Agent Security and Governance]]
- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[Sarthak Rastogi]]

## Related pages

- [[Agentic Testing]]
- [[Tool Use and Function Calling]]
- [[Agent Delegation]]
- [[LLM Application Resilience]]
- [[Retrieval-Augmented Generation]]

## Citations

- Raw capture: [[2026-09-06 Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]]
- Source: <https://sarthakai.substack.com/p/making-ai-agents-observable-monitorable>
