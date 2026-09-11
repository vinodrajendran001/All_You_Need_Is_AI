---
type: source-summary
created: 2026-09-11
updated: 2026-09-11
source_id: src-2026-09-07-bytebytego-llm-error-handling
source_title: "How to Deal With Errors and Failures in LLM-Powered Applications"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-to-deal-with-errors-and-failures
tags:
  - source/summary
  - production
  - reliability
source_ids:
  - src-2026-09-07-bytebytego-llm-error-handling
status: active
---

# ByteByteGo - How to Deal With Errors and Failures in LLM-Powered Applications

## Summary

A systems-engineering treatment of failure in LLM applications, organised around one distinction that
does most of the work: **technical failures**, where "the system can't even complete the operation",
versus **semantic failures**, which "show up even when the operation is technically successful. But the
result might be incorrect, unsafe, irrelevant, or even unusable."

The argument for why this needs its own treatment is short and correct. In ordinary software, "if the
function returns successfully, the result is deemed valid." With an LLM, "a successful API request to an
LLM doesn't guarantee that the response we receive is correct or even usable... an LLM API call might
appear successful based on status code, but it might be a failure in logical terms." Conventional error
handling was built for the first category only; LLM applications must handle both.

The rest is a catalogue of failure types and a toolkit of responses — retries with backoff and jitter,
timeouts scaled to the user's wait, fallback chains, circuit breakers, rate limiting and queues — all
borrowed deliberately from distributed systems practice.

## Key claims

**Error handling and resiliency are different properties.** Error handling "is a part of the program
responsible for deciding the appropriate action when something goes wrong"; resiliency is "an
application's ability to continue doing its job even when some parts of the system are failing. We don't
need an application to operate perfectly to be resilient. Failures are fine. But they should happen in a
controlled manner." The distinction is one of scope: "error handling deals with an individual failure,
resiliency is more concerned about the behavior of the entire system."

**Seven ways a technically successful call can be wrong.** The model may have ignored part of the
instructions; returned prose where JSON was expected; hallucinated a product, policy or fact; returned an
incomplete response after hitting its token limit; refused a harmless request; selected the wrong tool or
called it with invalid arguments; or produced an answer violating a business rule.

**Failures happen at every boundary, not just at the model.** The worked example is a shopping chatbot
that searches a product database, asks the model to select products, then calls an inventory API: "The
user might provide some invalid information. The product search may return no results. The request to the
LLM might time out... The model may return an unknown product identifier. The inventory service might go
down. Lastly, even if the response is somehow generated, it might be interrupted while streaming."

**Three classes determine the response.** A *transient* error "is temporary and usually disappears if we
attempt the operation again" — network problems, rate limits, server failures; retry or fall back. A
*permanent* error "continues until there is a change in the request or the system" — invalid
credentials, unsupported file types, permission issues, malformed requests; report it, do not retry. A
*semantic* error is one where "the response is technically correct, but doesn't solve the application's
requirements"; validate, repair, or escalate to human review.

**The classification is not always clean, and the source says so.** "A context-length error is permanent
for the current prompt. However, it can be solved by making the prompt shorter."

**Retry correctly or make the outage worse.** Bound the attempt count, grow the delay — "wait 1 second
before the first retry, 2 seconds before the second, and 4 seconds before the third" — and add jitter,
because "without jitter, thousands of failed requests may all retry at the same time. This can cause
another traffic spike and negate the benefit of retrying." Retry timeouts, transient network failures,
429s and some 5xx; never retry invalid credentials, prohibited requests or bad input.

**On repeated provider 5xx, retrying is actively harmful.** "If the failures continue, repeated retry
calls only increase the load upon an already struggling service."

**Timeouts should be set from the user's situation, not the model's.** "An interactive chat application
might have a timeout of 20 seconds. But an offline document-analysis job might allow several minutes...
a user waiting on a screen should have a shorter deadline than a background task that runs overnight."

**Context-length failures are preventable by counting first.** "An application designed with resiliency
in mind usually counts tokens before sending the request. It can also remove old conversation messages,
summarize earlier content, retrieve fewer documents, or divide a large job into smaller pieces."

**The fallback ladder has four rungs**: primary high-quality model → smaller backup model → pre-defined
response or cached information → human handoff.

**A fallback must not violate the original requirement.** "We might be okay to use a smaller model for
summarizing an internal meeting. However, it might not be a good choice for interpreting a complicated
legal document. Similarly, a cached response may be good enough for a general FAQ type scenario. But it
won't be suitable for something like the current account balance."

**Provider diversity is the point of a backup model, not size diversity.** "If both the primary and
backup models are accessed through the same provider, an outage can disable both. For real redundancy,
we should have separation between the two pathways."

**Circuit breakers have three states** — closed (normal), open (reject or redirect immediately), and
half-open, where "a small number of test requests are allowed to go through" to probe recovery. Success
closes the circuit; failure reopens it.

**Admission control is a separate concern from retrying.** "An LLM-powered application can't accept
unlimited LLM work just because users can submit it from the UI." If 10K requests arrive at once,
forwarding them all "might exhaust provider limits, database connections, memory, or the application's
budget." Interactive requests should outrank background work: "a user waiting for a chat response should
not be blocked because thousands of documents are being summarized in the background." Limits belong on
token usage, document size, retrieved-passage count, tool-call count, and total workflow duration.

**Tool-calling creates partial completion, which is the dangerous case.** "Suppose the LLM assistant
calls a payment service. The payment succeeds, but the network connection breaks before the application
gets the confirmation. If the application retries the payment blindly, we might end up charging the
customer twice. This is the reason tool-based systems need idempotency, state tracking, and recovery
mechanisms."

**Validate cheaply before spending on the model.** "There is no need to call an LLM to find out if a
mandatory email address is missing or if an uploaded file exceeds the size limit."

## Why it matters

This is the vault's clearest statement that most of what LLM applications need for reliability is not
new. The conclusion says so explicitly: "we can still borrow many of the techniques for error handling
from traditional applications... retries, fallbacks, circuit breakers, rate limiting, and queuing can
help." What is new is one category — semantic failure — and the fact that it cannot be caught by
exception handling, "because no technical exception occurred."

It pairs directly with [[Agent Observability]], and the pairing is more than thematic. Both sources
converge on tool-call idempotency as the specific place where an LLM system differs dangerously from an
ordinary one; one arrives there from resilience engineering (retry safely), the other from incident
forensics (tell a retry storm apart from an attack). Read together they make a stronger case than either
alone.

The fallback ladder also supplies a fourth reading of the model-choice question that
[[Model Routing]] treats as a cost problem. Routing picks the cheapest adequate model up front;
fallback picks any available model under failure. The source's warning that "the fallback strategy
should not violate the original requirements of the operation" is the constraint both share.

## Tensions / open questions

- The article gives no detection mechanism for semantic failure beyond schema validation and "additional
  checks, trusted data sources, or some form of human intervention." It names the category precisely and
  then hands the hard part back to the reader.
- Circuit breakers and fallbacks interact badly with semantic failure: a breaker trips on technical
  signals, so a provider returning fluent nonsense at HTTP 200 keeps the circuit closed indefinitely.
- The retry guidance and the idempotency guidance are given in separate sections and never reconciled
  into a rule. Exponential backoff with jitter is recommended for transient failures generally, but
  transient failures on a non-idempotent tool call are precisely the case where retrying is unsafe.
- Provider separation is recommended for redundancy without acknowledging its cost: two providers means
  two prompt formats, two failure vocabularies, and two sets of behaviour to evaluate.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[LLM Application Resilience]]
- [[AI Agents in Production]]
- [[Tool Use and Function Calling]]
- [[ByteByteGo]]

## Related pages

- [[Agent Observability]]
- [[Model Routing]]
- [[Agent Security and Governance]]
- [[Context Engineering]]
- [[Small Language Models]]

## Citations

- Raw capture: [[2026-09-07 ByteByteGo - How to Deal With Errors and Failures in LLM-Powered Applications]]
- Source: <https://blog.bytebytego.com/p/how-to-deal-with-errors-and-failures>
