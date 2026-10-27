---
type: concept
created: 2026-09-11
updated: 2026-10-27
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
  - src-2026-09-18-0xmovez-jev-engineering
  - src-2026-09-30-bytebytego-doordash-agent-gateway
  - src-2026-10-05-faik-ai-native-software-factory
  - src-2026-08-02-arise-llm-as-judge
  - src-2026-10-16-west-eval-engineering-lessons
  - src-2026-10-21-nvidia-sentry-runtime
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
idempotency requirement from the resilience side rather than the forensic side, following
[[ByteByteGo - How to Deal With Errors and Failures in LLM-Powered Applications]].

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
late. [[Salesforce]] Agentforce Observability is cited as a fair counter-example — session-level tracing,
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

## Decision-plane savings need end-to-end accounting

[[0xMovez - Jev Engineering]] reports large reductions in protocol calls, latency, and token cost, but
some examples exclude browser work and fresh verification. Observability must attribute the complete
task path—gate, action, fallback, and verification—rather than price only the classifier call.

## Attribute the authorization decision and the accepted outcome

[[ByteByteGo - How DoorDash Built a Toolbox for AI Agents]] gives a concrete gateway event schema:
agent, user, tool, bundle, owner, policy decision, error origin, timing, and payload sizes. Keeping
those identities and decisions separate lets an operator distinguish denied execution, missing
OAuth consent, and an upstream tool failure. A trace of an HTTP request alone loses that distinction.

[[Adam Faik - How to Build an AI-Native Software Factory]] adds the downstream unit the trace
should ultimately support: **cost per accepted outcome with quality retained**, including the
review/CI path rather than only generation. In its illustrative 200-PR PostHog sample, **80 PRs
had no human review**; the reported first-human-review median is **6.1 hours**, versus
**0.07 hours** when bot reviews count and none are unreviewed. Those are different definitions
and observed groups, not a measured acceleration. The sample is a roughly one-day slice of merged PRs, with
bot authors retained, and is not a representative company-wide benchmark.

Together the sources make metric definitions part of provenance: record who acted, which policy
allowed it, what the tool returned, and which acceptance event completed the task. Activity and
transport success cannot substitute for that final event.

## Operational dashboards and sign-off review both miss plausible content errors

[[Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads]] supplies a non-agent case
of the split above between operational traces and answer-level evaluation. AI-scribe deployments
commonly track time in notes, after-hours "pajama time," clinician satisfaction, and burnout. Those
numbers answer a real question about documentation burden, but "a dashboard tracking minutes saved
is blind to" an invented finding or a dropped one.

The source also qualifies this page's incident data, which come from the agent-runtime study above
rather than from the clinical post. In that eight-week study, roughly 70% of fail-plausible
incidents were found by a human noticing something was off, which makes human attention the main
observed detector. The clinical authors argue that the human reviewing fluent, confident output
is the one exposed to automation bias: a fabricated line "is easy to wave through and hard to catch," and once signed it becomes part
of the permanent record. Their proposed complement is a judge validated against a human-graded
sample and run over every output to detect population-level patterns, such as systematic omissions.
That partly answers the open question below on detecting a **semantic** failure automatically, but only
for systematic patterns, and it still does not make an individual failure noticeable. A scribe is a
drafting tool with a clinician signer rather than an autonomous agent, so the transfer to agents is by
analogy, and neither reviewer nor judge miss rates are reported.

## A flattened trace can turn a harness ordering bug into apparent disobedience

[[Casey West - Four Evaluation Engineering Lessons from Building Agent Plugins]] adds a requirement on
the shape of the record this page's definition asks for. Harnesses, the post notes, often batch several
tool calls into one assistant turn. In one of Google's evaluations, the harness sent a skill-loading call
and two documentation searches together in a single `tool_calls` payload. Activating an [[Agent Skill]]
there is a multi-stage process: the first call returns a short launch stub, and the next turn injects
the full instructions. So "the instructions meant to govern the search arrived in the prompt context
after the system had already executed the searches." If telemetry pipelines "strip out turn structures
and merge calls into a flat timeline", the post warns, engineers will waste days wondering why an agent
ignored unambiguous instructions.

The vault's reading is that a turn boundary records what was in the model's context when it acted, so it
belongs to the causal chain in this page's definition rather than to formatting. It is the within-agent
counterpart of the *Handoffs* layer above: there, trace context that is not propagated leaves a
receiving agent in a new, orphaned trace; here, a flat list of calls hides which guidance existed when
each call was issued. The case also respects this page's boundary with evaluation. The cause sat in the
harness, which "never gave the skill a dedicated turn to let its guidance influence the agent's
actions"; a flat extractor would hide that cause, and a verdict of disobedience drawn from such a record
would be wrong because the record misdescribes the chain. The post's first lesson supports the ordering
in *Why it matters*: a judge's misgrades on three prompts surfaced when the team opened the raw
tool-call logs and read the transcripts. See [[LLM-as-a-Judge]].

The post's remedy is to "Preserve turn structure in telemetry extractors" so engineers can see when
parallel dispatch issues calls before injected guidance enters the context. That makes the ordering
visible without changing it; the post reports no harness change that gives a skill its own turn. The
evidence is one example from Google's evaluation of its own plugin: the post calls concurrent tool
dispatch "one of the critical causes of behavioral failure" but gives no count of how often dispatch ran
ahead of guidance.

## A record the agent can edit cannot settle what a compromised agent did

[[Ofir Arkin - Inside NVIDIA Sentry - Secure AI Agents at Runtime]] raises a property this page has so
far assumed: that a written trace is intact. NVIDIA's premise is that "Monitoring and enforcement need to
operate outside the agent’s reach so that it can’t alter or disable them", and its incident case is
explicit: security teams need evidence "even when an agent has escaped its sandbox or altered host-based
logs." In the OpenShell reference architecture, a BlueField-4 data processing unit (DPU) "sits on the
node’s only path to the model". Sentry's gateway, DOCA Tower, records inspected communications and policy
decisions there; DOCA Argus adds runtime signals read from host memory (processes, file access, network
connections, and loaded libraries, with containers, processes, and libraries tracked by hash); and the
telemetry is attested. "An agent that changes a log inside its own environment cannot make the same
change to the protected record maintained on BlueField-4."

It also extends *Attribute the authorization decision and the accepted outcome*. The gateway event
schema from [[ByteByteGo - How DoorDash Built a Toolbox for AI Agents]] keeps agent, user, tool, and
policy decision separate. Sentry adds the layer underneath: DOCA Tower's policy engine ties a network
connection to the agent process that initiated it, that process's properties, and the container it
belongs to, and Sentry enriches its records with this runtime context, "reducing the need for
downstream correlation."

The vault's reading is that this record trades coverage for integrity. Argus reads "selected regions of
volatile host memory"; decryption covers "connections configured for inspection"; classifiers work from
"tool calls and available reasoning traces"; and a plugin for further reasoning-trace analysis is
planned, not shipped. An out-of-band record can show what crossed the wire and which process sent it,
but not every step that led there, so it complements an in-environment trace rather than replacing it.
Sentry's behavior classifiers and policy engine are evaluation and enforcement in this page's terms.

This is a vendor post about a product with "planned availability early next year". Its sub-millisecond
policy evaluation and millisecond containment are vendor statements without a test setup; it reports no
detection rate, false-positive rate, latency distribution, or overhead. The guarantee holds only where
the DPU really is the agent's only path out, as in the reference architecture, and no threat model
covers a compromised DPU, its firmware, or the policy engine. NVIDIA's "tamper-evident" label is a
description, not a tested property.

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
- This page's OpenTelemetry material does not say whether the GenAI span types record which tool calls
  shared one assistant turn.
  [[Casey West - Four Evaluation Engineering Lessons from Building Agent Plugins]] shows what a flat
  extractor loses, not how often parallel dispatch runs ahead of injected guidance.
- When an in-environment trace and an out-of-band record such as Sentry's disagree, which one is
  authoritative, and how are the two joined for a single run?
  [[Ofir Arkin - Inside NVIDIA Sentry - Secure AI Agents at Runtime]] describes export to XDR and SIEM
  platforms and security data lakes, not reconciliation with application traces.

## Related pages

- [[Casey West - Four Evaluation Engineering Lessons from Building Agent Plugins]]
- [[Ofir Arkin - Inside NVIDIA Sentry - Secure AI Agents at Runtime]]
- [[Google Cloud]]
- [[NVIDIA]]
- [[Agent Skill]]
- [[Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads]]
- [[ByteByteGo - How DoorDash Built a Toolbox for AI Agents]]
- [[Adam Faik - How to Build an AI-Native Software Factory]]
- [[AI-Native Software Development Lifecycle]]
- [[Model Context Protocol]]
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
- [[ByteByteGo - How to Deal With Errors and Failures in LLM-Powered Applications]]
- [[Salesforce]]
