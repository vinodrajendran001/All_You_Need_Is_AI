---
type: source-summary
created: 2026-10-07
updated: 2026-10-07
source_id: src-2026-09-27-willison-llms-2026-so-far
source_title: "2026 in LLMs (so far)"
source_author: Simon Willison
source_url: https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/
tags: [source/summary, coding-agents, reasoning, governance]
source_ids: [src-2026-09-27-willison-llms-2026-so-far]
status: active
---

# Simon Willison - 2026 in LLMs (so far)

## Summary

An annotated conference keynote combining Willison's coding-agent experiments, model-release
commentary, and reporting about agent security. Its durable argument is that producing software has
become easier without making goal selection, verification, or product judgment automatic. The
experiments are personal observations, not a controlled ranking of models or a productivity study.
The September 27 date comes from the permalink; the clipping's publication field is empty.

## Key claims

- Willison places a practical reliability threshold for his coding work around the November 2025
  Opus 4.5 and GPT-5.1 releases. That is his experience, not an established industry-wide threshold.
- Interpreter ports and browser experiments show how agents expand what one developer will attempt.
  His generated games also expose the limit: software can resemble a game without sustaining an
  enjoyable gameplay loop. Producing an artifact and establishing its usefulness are different jobs.
- His "Fable class" label describes models he finds effective when given a clear goal, unambiguous
  constraints, and appropriate tools. Defining those inputs remains engineering work; this is not
  evidence that arbitrary software specifications can be solved reliably.
- StrongDM's software-factory rules exclude both human code writing and human code review. Willison
  presents this as an experienced team's exploration of alternative assurance, not permission to
  remove verification from ordinary development.
- His pelican SVG exercise is intentionally weak as a general benchmark. He still uses it to inspect
  price, latency, and effort tradeoffs within model families. Qwen3.8-27B reportedly generated one
  strong result locally from a 17 GB download in 21 minutes; Opus 5.5 at maximum effort exhausted
  128,000 reasoning tokens without reaching an answer in another example.
- The keynote contrasts enthusiasm for token consumption with subsequent cost controls. Token usage
  is an activity metric, not delivered value.
- Personal agents widen the execution surface beyond developers. A familiar interface does not make
  a code-executing agent safe or establish that its permissions match the user's intent.
- Willison says his particular predicted security disaster did not occur as he had imagined, while
  reporting multiple other containment incidents. Those statements are compatible; neither says
  that agents caused no security incidents.

## Why it matters

The source connects capability gains to a change in the human workload: routine implementation can
shrink while specification, evaluation, and difficult decisions occupy more of the remaining work.
That complements software-factory accounts that measure accepted outcomes rather than generated code.

## Tensions / open questions

The chronology mixes firsthand experiments, linked reporting, interpretation, and extraordinary
incident allegations. Linked reports were not independently checked during this ingest; the
keynote's incident labels and counts are not treated as adjudicated legal findings. The existing
[[OpenAI - The Hugging Face Incident and the Road Ahead]] remains the vault's more detailed,
first-party evidence for that incident.

The Qwen experiment calls the default effort "high", whereas
[[adlrocha - Base Models Stopped Being the Bottleneck]] records the API/configuration value
`xhigh`. Preserve the wording difference rather than silently changing the documented setting.
Willison's informal "AI mania" describes his own experience of over-engagement and is explicitly
distinct from AI psychosis; it is not a clinical diagnosis.

## Affected pages

- [[AI-Native Software Development Lifecycle]]
- [[AI Agents in Production]]
- [[Reasoning Effort Control]]
- [[Agent Security and Governance]]
- [[Qwen]]

## Raw capture

- [[2026 in LLMs (so far)]]

## Citations

- Canonical URL: <https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/>
- Captured October 5, 2026; retained unchanged.

## Related pages

- [[Adam Faik - How to Build an AI-Native Software Factory]]
- [[Ethan Mollick - The Dot and the Swarm]]
- [[Coding Agent Harness]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
