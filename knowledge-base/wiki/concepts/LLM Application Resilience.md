---
type: concept
created: 2026-09-11
updated: 2026-09-11
tags:
  - concept
  - topic/production
  - topic/reliability
source_ids:
  - src-2026-09-07-bytebytego-llm-error-handling
  - src-2026-09-06-rastogi-agent-observability
  - src-2026-09-09-bytebytego-model-routing
status: active
---

# LLM Application Resilience

## Definition

The property of an LLM-powered system that lets it keep doing its job while parts of it are failing.
Two things are usually merged and should not be. **Error handling** decides what to do about an
individual failure; **resiliency** is a statement about the whole system's behaviour — failures are
expected, and the requirement is that they happen in a controlled manner rather than not at all.

The distinguishing feature of the LLM case is that the standard contract breaks. In conventional
software, a successful return implies a valid result. With a model, a **technically successful call can
return an unusable answer**: a 200 status code says the request completed, not that the response solves
anything. Resilience work therefore has to cover two categories rather than one.

## Why it matters

Conventional error handling was designed for **technical failures** — the system could not complete the
operation. LLM applications add **semantic failures**, which occur when the operation completes
perfectly and the result is still wrong, unsafe, irrelevant or unusable. No exception is raised, so no
`try/except` will catch it.

The semantic category has at least seven recognised forms: the model ignored part of the instructions;
returned prose where JSON was required; hallucinated a fact, product or policy; truncated on a token
limit; refused a harmless request; selected the wrong tool or called it with invalid arguments; or
produced an answer that violates a business rule.

That is the novel part. The rest is a deliberate borrowing from distributed-systems practice — retries,
backoff, jitter, timeouts, fallbacks, circuit breakers, rate limiting, queues — and the useful framing is
that **most of what an LLM application needs for reliability already exists**, with exactly one category
that does not have a prior art answer.

## Current synthesis

**Classify before responding.** *Transient* failures are temporary and usually resolve on retry —
network problems, rate limits (HTTP 429), some provider 5xx. *Permanent* failures persist until the
request or system changes — invalid credentials (401/403), unsupported file types, malformed requests;
report them, never retry them. *Semantic* failures need validation, repair, or escalation to a human. The
boundary is not always clean, and the canonical example is a context-length error: permanent for the
current prompt, transient once the prompt is shortened.

**Retry correctly or amplify the outage.** Bound the attempts, grow the delay exponentially (1s, 2s, 4s),
and **add jitter** — without it, thousands of simultaneously failed requests retry in unison and produce
a second traffic spike that negates the benefit. On repeated provider 5xx, continued retries add load to
an already struggling service.

**Scale timeouts to the user's situation, not the model's.** An interactive chat might time out at 20
seconds; an offline document-analysis job may legitimately run for minutes. A user watching a screen
deserves a shorter deadline than an overnight batch.

**Prevent the preventable before spending on inference.** Count tokens before sending; drop old
conversation turns, summarise earlier content, retrieve fewer documents, or split the job. And validate
cheaply first — there is no need to call a model to discover that a mandatory email address is missing or
a file exceeds the size limit.

**The fallback ladder has four rungs**: primary model → smaller backup model → cached or predefined
response → human handoff. Two constraints govern it. The fallback must **not violate the original
requirement** — a smaller model is fine for summarising an internal meeting and not for interpreting a
legal document; a cached answer is fine for an FAQ and not for an account balance. And redundancy
requires **provider separation**: if primary and backup are reached through the same provider, one outage
disables both.

**Circuit breakers have three states** — closed, open (reject or redirect immediately), and half-open,
where a small number of probe requests test recovery. Success closes the circuit; failure reopens it.

**Admission control is a separate concern from retrying.** An application cannot accept unlimited work
just because a UI allows submission. Ten thousand simultaneous requests can exhaust provider quotas,
database connections, memory and budget. Interactive requests should outrank background work, and limits
belong on token usage, document size, retrieved-passage count, tool-call count, and total workflow
duration.

**Tool calls create partial completion, which is the genuinely dangerous state.** A payment succeeds and
the confirmation is lost in transit; a blind retry charges twice. Tool-using systems need idempotency,
state tracking and recovery. This is the same requirement [[Agent Observability]] reaches from the
forensic direction — without an idempotency key and a `retry_count` attribute, a retry storm and a
prompt-injection campaign look identical in the trace — and the combination is stronger than either
alone. It is also the unreconciled tension in the resilience advice itself: exponential backoff is the
recommended response to transient failure, and a transient failure on a non-idempotent tool call is
precisely where retrying is unsafe.

**Fallback and routing are different decisions about the same question.** [[Model Routing]] chooses the
cheapest adequate model up front; fallback chooses any available model under failure. Both are governed
by the same constraint — the substitute must still satisfy the requirement.

## Open questions

- No detection mechanism exists for semantic failure beyond schema validation, trusted-source
  cross-checks, and human review. The category is named precisely and the hard part is handed back.
- Circuit breakers trip on technical signals, so a provider returning fluent nonsense at HTTP 200 keeps
  the circuit closed indefinitely. Resilience machinery is blind in exactly the new failure category.
- Retry guidance and idempotency guidance are usually given separately and rarely reconciled into a rule
  covering transient failures on non-idempotent tools.
- Provider separation is recommended for redundancy without pricing its cost: two prompt formats, two
  failure vocabularies, two behaviours to evaluate, and two sets of semantic quirks.

## Related pages

- [[AI Agents in Production]]
- [[Agent Observability]]
- [[Tool Use and Function Calling]]
- [[Model Routing]]
- [[Agent Security and Governance]]
- [[Context Engineering]]
- [[Small Language Models]]
- [[ByteByteGo - How to Deal With Errors and Failures in LLM-Powered Applications]]
