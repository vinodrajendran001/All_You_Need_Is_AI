---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-22-nikolas-goebel-informal-verification
source_title: "Informal Verification"
source_author: Nikolas Göbel
source_url: https://www.nikolasgoebel.com/2026/11/22/informal-verification.html
tags:
  - source/summary
  - verification
  - coding-agents
  - decision-models
  - opinion
source_ids:
  - src-2026-11-22-nikolas-goebel-informal-verification
status: active
---

# Informal Verification

## Summary

Nikolas Göbel argues that verification is "first and foremost an exercise in building trust, for which a
formal approach may be sufficient but not necessary." He separates **empirical** trust, built by a track
record and by testing, from **epistemic** trust, the belief that a system works the way you think it
does. For the second he proposes informal proofs: natural-language premises grounded in code or
documentation, decomposed into small steps, each checked automatically by a "System One model".
TypeSafe's Jev plays the checker. A worked multi-tenant Rails example shows the checker rejecting the one
step that hides a tenant-isolation bug. He introduces autoground, an informal proof assistant with a
lightly structured language called brief. The essay is an argument with illustrative demonstrations; the
interactive demonstrations were not captured, and no accuracy or detection rates are reported.

## Key claims

### A track record is not understanding

Empirical trust asks how often you correct an agent and how often it broke production. Göbel says this is
not enough: weeks of autonomously closed bugs cannot distinguish "a mounting pile of tech debt from
surgical fixes", and clean code explained in roundabout ways still does not earn trust. His interactive
illustration, not captured, is a marble sorter that appears to sort by colour but actually sorts by size,
which "just happens to be equivalent under normal operation" until a large blue marble arrives. Testing
builds empirical trust; arguing *why* a system behaves correctly builds epistemic trust, because
agreement across many explicit assumptions and steps "is a very strong signal in favour of true
alignment."

### Formal proof moves the risk to the formalization

A Lean kernel rarely accepts a flawed argument and "won't suddenly change its mind", but formalization
can be wrong, ambiguous, or drift. He quotes Alan Perlis ("one can't proceed from the informal to the
formal by formal means"), notes that questions arose in 2025 about which statement an AI-generated Lean
proof of Erdős problem #124 had established, and quotes a Xena Project post: "of the 290 OpenAI theorems
which come with Lean code, around 38 of them have the property that the Lean code does not even state, let
alone prove, the main theorem of the paper." Informal arguments reduce that translation risk and work
where formalization is impractical, such as proving correct use of a third-party API or that a page's
rendering matches its CSS, at the price of "a higher error rate when checking the proof". He frames the two
as complementary.

### What an informal proof checker must do

It should accept obviously true steps, reject obviously false ones, reject imprecise or ambiguous ones,
and reject big leaps even when correct, so the author must decompose them. The last rule has precedent in
the Mizar checker, which accepts only "obvious inferences".

### Jev as the checker, with its failure modes

In the (uncaptured) demonstrations Jev accepts a correct step, rejects an incorrect one, and is not
convinced by an ambiguous claim. On a Zebra-puzzle claim that makes Fable 5.2 reason "for about a minute",
Jev splits almost evenly between true and false; an agent tasked with getting it accepted has to
decompose the conclusion into a tree of sub-claims, which Jev then accepts. Used this way, Jev "effectively
accepts any deductive step that a capable LLM can follow intuitively, meaning without the use of internal
reasoning tokens." Because Jev is multimodal, premises can cite diagrams. Göbel asserts that its cost and
latency are "negligible" relative to the agent and other tool calls.

He lists the costs himself. Jev is not perfectly deterministic, so steps near the threshold can
flip-flop. It resolves ambiguity like a fluent reader: given "the controller passes the invoice to the
serializer after it validates it", it is **95%** confident the controller validates, so a step can pass
under a reading the author did not intend. And it silently fills in facts it treats as common knowledge;
in a proof that the square root of two is irrational it accepts the last step without one premise but not
without the other. His summary: such models "scale human-like informal reasoning — warts and all."

### Worked example: a tenant-isolation claim

The claim, "purely for illustration", is that `GET /invoices/:id` never returns another tenant's invoice.
Four premises cite their witnesses: middleware sets the current tenant from the session; the `Invoice`
model has a tenant default scope; Rails documentation says model queries include that scope; and the
controller loads the invoice with `find_for_display`. The checker accepts the first two steps and rejects
the third, that the loaded invoice belongs to the current tenant, because nothing says how
`find_for_display` builds its query. The method uses `find_by_sql`, which "runs the query as written,
default scope or not", so "Any tenant can read any invoice by guessing its id." The checker did not need to
know `find_by_sql` or search the codebase; it "simply refused a step whose conclusion doesn't *obviously*
follow from the premises." A human gets "seven concrete claims (four premises and three reasoning steps)"
to match against their mental model instead of "a single agentic thumbs-up at the end", and the proof is a
durable artifact that can be "cheaply re-checked against future revisions without an agent in the loop".

### autoground and brief

autoground is presented as "an attempt" at a usable tool, with grounded agentic explanations as the first
use case. Its brief language encourages consistent terminology and gradual decomposition into atomic claims
joined by deterministic logic operators, aimed at the ambiguity and big-step failures above. "None of this
turns an informal proof into a guarantee"; the stated value is understanding and trust, "When a
specification is hard to come by".

## Why it matters

[[AI Code Review]] gains a different review artifact: an argument for a stated property, checked step by
step, instead of findings in a diff. [[Agentic Testing]] gains the empirical/epistemic distinction that
explains why normal-path tests can pass while a system is misaligned. [[Human Deferral to AI]] gains an
instrument aimed at the trust a human gate supplies, with the caveat that an agent-written proof is still
the agent's argument. [[AI for Mathematical Discovery]] gains outside evidence that Lean statements can
miss the theorem they claim. [[Chain-of-Thought Monitoring]] gains a claim-verification design that lifts
reasoning out of the trace, and [[Agent Security and Governance]] a policy point bypassed by a raw query.
[[TypeSafe AI]] gains a third-party use of Jev outside classification.

## Tensions / open questions

- **No measurements.** No checker accuracy, false-acceptance or false-rejection rate, or comparison with
  human or model reviewers is reported. The example is constructed, and the "negligible" cost claim is
  unquantified.
- **Interactive content missing.** The marble sorter and all Jev scoring demonstrations are iframes not
  present in the capture; only their captions and the surrounding prose (including the 95% figure) are
  available, so Jev's displayed scores cannot be checked here.
- **Optimization pressure on the checker.** The method tasks an agent with getting Jev to accept a
  conclusion. The essay does not discuss an agent decomposing a false conclusion into steps that each pass,
  the reward-hacking risk that [[LLM-as-a-Judge]] records for model judges.
- **Secondhand evidence.** The 290/38 figure, the Erdős #124 discussion, and the study of formally
  verified distributed systems are cited through links; the vault has not read them.
- **Affiliation not stated.** Jev is TypeSafe AI's commercial model and autoground depends on it; the
  capture does not say whether Göbel is affiliated with TypeSafe.
- Footnotes compare decomposition to Codemode, where agents lift control flow out of their reasoning into
  deterministic code, and cite Lakatos's *Proofs and Refutations*; the Fable 5.2 name is as written.

## Affected pages

- [[AI Code Review]]
- [[Agentic Testing]]
- [[Human Deferral to AI]]
- [[AI for Mathematical Discovery]]
- [[Chain-of-Thought Monitoring]]
- [[Agent Security and Governance]]
- [[TypeSafe AI]]

## Raw capture

- [[knowledge-base/raw/sources/Informal Verification]]

## Citations

- Canonical URL: <https://www.nikolasgoebel.com/2026/11/22/informal-verification.html> (the captured link
  carried a `utm_source=tldrnewsletter` parameter, removed here).
- The capture's `author` and `published` fields are empty and the body has no byline. The author, Nikolas
  Göbel, was recovered outside the capture from the live site header at nikolasgoebel.com; the 2026-11-22
  date comes from the URL path. Captured 2026-11-24.
- autoground and its brief language are linked on GitHub from the capture; the repository was not read.

## Related pages

- [[AI Code Review]]
- [[Agentic Testing]]
- [[Human Deferral to AI]]
- [[AI for Mathematical Discovery]]
- [[Chain-of-Thought Monitoring]]
- [[Agent Security and Governance]]
- [[TypeSafe AI]]
- [[Typed Probabilistic Decision Models]]
- [[Diogo Almeida - Introducing System One Models and Jev]]
- [[LLM-as-a-Judge]]
- [[Programmatic Tool Calling]]
- [[Federico Tomassetti - Legacy Modernization with LLMs, Measured]]
- [[Anjana Ratnayake and Teymour Aldridge - Nightmare Mode - Simulating Disk Failures]]
