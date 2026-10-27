---
type: concept
created: 2026-09-11
updated: 2026-10-27
tags:
  - concept
  - production
  - reliability
source_ids:
  - src-2026-09-07-bytebytego-llm-error-handling
  - src-2026-09-06-rastogi-agent-observability
  - src-2026-09-09-bytebytego-model-routing
  - src-2026-09-29-bytebytego-why-do-llms-lie
  - src-2026-10-06-bytebytego-sycophancy
  - src-2026-08-02-arise-llm-as-judge
  - src-2026-10-19-vercel-durable-harness
  - src-2026-10-16-opensearch-beyond-top-k
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
forensic direction, following
[[Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]]: without an
idempotency key and a `retry_count` attribute, a retry storm and a prompt-injection campaign look
identical in the trace — and the combination is stronger than either
alone. It is also the unreconciled tension in the resilience advice itself: exponential backoff is the
recommended response to transient failure, and a transient failure on a non-idempotent tool call is
precisely where retrying is unsafe.

**Fallback and routing are different decisions about the same question.** [[Model Routing]], following
[[ByteByteGo - How Smart Model Routing Can Cut LLM Costs by 10X]], chooses the cheapest adequate model
up front; fallback chooses any available model under failure. Both are governed
by the same constraint — the substitute must still satisfy the requirement.

## Semantic failure needs a third response state and a verification stage of its own

This page's list of semantic failures contains a single entry for "hallucinated a fact, product or
policy". [[ByteByteGo - Why Do LLMs Lie]] splits it into three overlapping categories. **Factual**
hallucination contradicts reality; **faithfulness** hallucination contradicts the evidence actually
supplied; **fabrication** invents policies, confirmation numbers, or papers. The source itself collapses
these to two broader categories with fabrication under factuality — a reasonable choice rather than a
standard one — and the distinction it treats as load-bearing is checking agreement with reality versus
checking agreement with the provided evidence. The split is operationally load-bearing because a model
can faithfully summarize an **outdated document and still be wrong about the current policy** — a
grounded system passing every faithfulness check while returning an
answer no one should act on. The definition offered is deliberately narrow: hallucination is information
that is factually incorrect, invented, or inconsistent with the material the model is supposed to use,
and none of it establishes an intention to deceive. The article's own title is rhetorical and it
withdraws the implication.

The design change that follows is to stop forcing a binary. The recommended response space includes a
third state such as **"needs review"**, so that insufficient evidence has a representable answer rather
than being resolved into eligible or ineligible. Read against this page's fallback ladder, the human
handoff rung stops being an outage-only measure and becomes the correct output for a question the
evidence cannot decide. The incentive argument explains why the third state has to be *scored* and not
merely permitted: if a correct answer earns one point while an incorrect answer and an expression of
uncertainty score the same, guessing carries positive expected upside and abstention carries zero.

Detection is handled as a **separate stage**, not as an instruction in the generating prompt: decompose
the answer into individual claims, check each against the applicable evidence, and validate citations for
existence, applicability, and support. That is a partial answer to this page's first open question, which
names semantic-failure detection precisely and then hands the hard part back. It stays partial, because a
verifier is itself a model and can be wrong, so claim checking reduces error rather than removing it.

The more useful contribution may be what the source rules *out*, since both items are routinely mistaken
for reliability engineering. **Lowering temperature buys consistency, not accuracy** — a system that
returns the same wrong answer every time has become reproducible, not correct. **Structured output buys
parseability, not semantic correctness**, which directly qualifies this page's existing position that
schema validation is one of the few available detectors: a schema-valid object can carry an invented
confirmation number, and no validator will object. Fluent confidence is not a signal either — "certainly"
and "definitely" are generated language, and an unvalidated "95% confidence" means nothing without
calibration, so a model-reported confidence score cannot be used as an admission-control or
circuit-breaking input. This is a secondary explainer with sponsored sections that reports no
hallucination rates or controlled comparisons and gives no method for calibrating confidence or choosing
retrieval thresholds, so it is a set of design positions rather than a sized result.

## A successful response can still reinforce an unsupported belief

[[ByteByteGo - Why LLMs Agree With You Even When You Are Wrong]] adds a semantic failure with no
transport symptom: the model agrees with the user's claim despite contrary evidence. Retry logic,
schema validation, and low latency do not detect it.

Resilience here means preserving evidence under pressure while still accepting valid corrections.
Test both cases, distinguish empathetic acknowledgment from factual endorsement, and expose
uncertainty rather than convert it into agreement. Blind second review may reduce anchoring but
cannot be assumed independent. The practical boundary is [[Sycophancy]] evaluation, not a prompt
that universally guarantees truth or a policy of always contradicting the user.

## A provider's model swap and a human's signature are both unmonitored failure points

[[Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads]] adds a substitution this
page's fallback ladder does not cover: one made by the provider rather than by the application. AI
scribes run on frontier models that vendors version and retire on their own timelines, so a note
pipeline validated against one model "can quietly shift behavior when the backend is swapped
underneath it." The substitute-must-still-satisfy-the-requirement rule applies, but no fallback
decision was taken, no circuit tripped, and the deployments' usual metrics (time in notes,
after-hours "pajama time," satisfaction, burnout) say nothing about note accuracy. Procurement-time
validation "cannot catch a regression that appears two versions later."

The proposed detector is a partial, conditional answer to the first open question below:
continuous content assessment by an LLM judge anchored to a human-graded sample and spot-checked
against it. It is explicitly a population-level instrument. It can show that notes are
systematically dropping medication reconciliation, but not which individual note is wrong, and it
depends on a reference the capture does not define for production notes.

The same source qualifies the human-handoff rung and the "needs review" state above. A clinician
reviewing a fluent, confident note is exposed to automation bias, so a fabricated line "is easy to
wave through and hard to catch," and once signed it becomes part of the permanent record. Routing
uncertain output to a person is therefore a control with its own failure rate, not a terminal
guarantee. This is an argued position with no measured miss rate for reviewers or judges.

## An interrupted tool call needs a declared replay policy, not a generic retry

The partial-completion paragraph above leaves a gap: backoff is the advice for transient failure, and
a transient failure on a non-idempotent tool is exactly where a retry is unsafe.
[[Pranay Prakash and Eric Dodds - Making Every Harness Durable]] describes a concrete rule for one
version of that gap, a turn interrupted by a crash or function timeout. Vercel's `durable-harness`
records an *intent* before each model or tool call and an *outcome* after it, and the function that
picks up the interrupted turn reads that log:

- a **completed** call is not run again; its result is read from the log, which the vendor says means
  "you're never billed twice for a finished model call's tokens";
- an interrupted tool the developer marked `replay: 'safe'`, such as a lookup, a file read, or a CI
  status check, runs again automatically;
- any other interrupted tool, such as a refund or a PR comment, "comes back to the model as possibly
  run, and the model decides whether to check."

The decision therefore moves from a generic retry policy to a property of each tool, declared once by
the developer. That does not settle the idempotency problem. The `'never'` path prevents a double
refund only if the model chooses to check and a check exists. The article does not mention idempotency
keys, does not discuss a call that finished at the provider before its outcome reached the log, and does
not say how a tool's own transient errors are handled. It is a vendor design with no reported
failure-injection results.

## Abstention can be graded and triggered by retrieval evidence instead of the model's own confidence

[[Chanpreet Singh and Shatakshi Pandey - Beyond Top-K - Search-Confidence Guardrails for Agentic AI]]
gives the *needs review* state above a graded form and a trigger outside the model. The semantic-failure
section rules out model-reported confidence as an admission-control input, and
[[ByteByteGo - Why Do LLMs Lie]] gave no method for calibration or retrieval thresholds. The OpenSearch
post computes confidence from retrieval results and document metadata instead: top normalized score,
score gap, coherence among the top hits, freshness, and source authority, weighted 0.35, 0.25, 0.20,
0.10, and 0.10. The margin between that composite and a threshold picks the response: act at zero or
above, caveat above -0.05, clarify above -0.15, escalate to a human above -0.25, and hard abstain
below that.

The threshold rises with the stakes of the action, not only with the type of question: a factual
lookup needs 0.75 to be read and 0.90 to be acted on, an exploratory query 0.50 and 0.70. Abstention
thus becomes a gate before a tool call, where the replay policy above acts after an interrupted one.
The escalate rung is the fallback ladder's human handoff, reached through weak evidence on a request
that raised no error; in this page's reading, the caveat and clarify rungs also bear on the
queue-capacity question below, since they settle some low-margin cases without queuing human work.
It is a per-request gate, not a circuit breaker, so the open question about fluent output at HTTP 200
stands.

The calibration problem moves rather than disappears. The composite is not a probability: with a
single hybrid clause the min-max top hit is always 1.0, and the gap depends on how many hits came back.
The authors' remedy, sweeping thresholds over a judged query set to maximize F1 or hold false acts
under a target rate, is the kind of method the earlier source lacked, but the post does not run it.
It calls itself "a conceptual deep dive with illustrative code", its example outcomes are "computed
from mocked retrieval scores", and its claim that the ladder "prevents cascading hallucinations at the
source" is asserted, not measured. It also does not say how query type and intent get classified,
though an action misread as a read-only query lowers a factual lookup's bar from 0.90 to 0.75. And
routing to a person carries the caveat the
[[Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads]] section attaches to human
review: a control with its own failure rate.

## Open questions

- No detection mechanism exists for semantic failure beyond schema validation, trusted-source
  cross-checks, and human review. The category is named precisely and the hard part is handed back.
- Circuit breakers trip on technical signals, so a provider returning fluent nonsense at HTTP 200 keeps
  the circuit closed indefinitely. Resilience machinery is blind in exactly the new failure category.
- Retry guidance and idempotency guidance are usually given separately and rarely reconciled into a rule
  covering transient failures on non-idempotent tools. A per-tool replay declaration is one such rule for
  crash recovery (see above), but it relies on the model to check before repeating a `'never'` tool and
  has not been evaluated.
- Provider separation is recommended for redundancy without pricing its cost: two prompt formats, two
  failure vocabularies, two behaviours to evaluate, and two sets of semantic quirks.
- If structured output guarantees only parseability, what remains of schema validation as a
  semantic-failure detector? Nothing here distinguishes a schema-valid real confirmation number from a
  schema-valid fabricated one without performing the lookup a second time.
- A "needs review" state converts a semantic failure into queued human work, which is a capacity
  commitment. What admission control governs that queue, and what happens when the abstention rate rises
  during the same incident that is degrading the tools?
- Faithfulness checks pass against stale evidence by construction. What owns document currency — the
  retrieval layer, the tool layer, or the verifier — and which of them fails closed?
- How does an application detect that its provider changed the model behind an unchanged API, and
  which validation must re-run before that change reaches users?
- A stakes-keyed threshold needs the query type and action intent classified before it applies. What
  performs that classification, and does a misclassification fail toward the lower read-only bar or
  toward escalation?

## Related pages

- [[Chanpreet Singh and Shatakshi Pandey - Beyond Top-K - Search-Confidence Guardrails for Agentic AI]]

- [[Pranay Prakash and Eric Dodds - Making Every Harness Durable]]
- [[Harness State Authority]]
- [[Vercel]]
- [[Sri Polkampally et al - LLM-as-Judge When It Works and When It Misleads]]
- [[Embedded Evaluation]]

- [[ByteByteGo - Why LLMs Agree With You Even When You Are Wrong]]
- [[Sycophancy]]
- [[AI Agents in Production]]
- [[Agent Observability]]
- [[Tool Use and Function Calling]]
- [[Model Routing]]
- [[Agent Security and Governance]]
- [[Context Engineering]]
- [[Small Language Models]]
- [[ByteByteGo - How to Deal With Errors and Failures in LLM-Powered Applications]]
- [[Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]]
- [[ByteByteGo - How Smart Model Routing Can Cut LLM Costs by 10X]]
- [[ByteByteGo - Why Do LLMs Lie]]
- [[ByteByteGo]]
- [[Retrieval-Augmented Generation]]
- [[Multi-Turn Evaluation]]
- [[LLM-as-a-Judge]]
- [[Chain-of-Thought Monitoring]]
