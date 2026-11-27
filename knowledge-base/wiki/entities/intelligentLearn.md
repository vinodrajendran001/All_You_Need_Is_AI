---
type: entity
created: 2026-11-27
updated: 2026-11-27
entity_kind: person
tags:
  - entity
  - person
  - inference
  - serving
source_ids:
  - src-2026-11-05-intelligentlearn-inference-trade-offs-part-1
  - src-2026-11-14-intelligentlearn-inference-systems-part-2
  - src-2026-11-19-intelligentlearn-inference-systems-part-3
  - src-2026-11-24-intelligentlearn-inference-systems-part-4
status: active
---

# intelligentLearn

## What it is

A Medium author (handle @wszjzhang, no personal name given in the captures) who writes a long
series on LLM inference serving called "Designing LLM inference systems". The vault has the
series' four-part "trade-offs article", published between 2026-11-05 and 2026-11-24. According
to the captures, it follows three earlier essays: one on service promises and measurements, a
serving primer, and a six-layer map of an inference system. None of the three is in the vault.

## Why it matters here

The four parts are the vault's most systematic treatment of serving-system design as a sequence of
decisions:

- [[intelligentLearn - From Symptoms to Fixes - Part 1 - Start with the Machine]] sets up three
  ledgers (operator, memory, timeline) and a fully specified H100 running case. It informs
  [[LLM Inference]], [[Arithmetic Intensity and the Roofline Model]], [[GPU Execution Model]], and
  [[Model Quantization and Efficiency]].
- [[intelligentLearn - Designing LLM Inference Systems, Part 2 - Six Layers to Investigate]] walks
  six layers with cost tables and stopping rules. It informs [[Prefill-Decode Disaggregation]],
  [[Semantic Caching]], and [[GPU Fleet Reliability]].
- [[intelligentLearn - Designing LLM Inference Systems, Part 3 - How to Evaluate a Change]] turns the
  ledgers into a three-question evaluation method. It informs [[Software Performance Engineering]].
- [[intelligentLearn - Designing LLM Inference Systems, Part 4 - Putting It to Work]] works the case
  to a measurement plan and audits its own 172-paper corpus. It informs
  [[Inference Efficiency Frontier]] together with the other parts.

The evidence style is the reason for an entity page. The author reports no measurements and says so.
Every number is a teaching assumption, a vendor constant, or a figure from a cited paper. The author
also labels, sentence by sentence, which steps are their own inference or extrapolation and which
results come from simulators. Only 15 of the 172 papers were read end to end, and the body's
mechanism claims rest on those alone. That makes the series a strong secondary map of the
literature and a model of evidence labelling. It is not primary evidence for any performance number.

## Notes

- The series' self-references are inconsistent. Part 1 announced later parts for November 10, 17,
  and 24, and Part 3 was published on November 19. Part 1's title format differs from Parts 2–4.
  Appendix letters are cross-referenced inconsistently.
- Papers are cited by keys such as `zhong2024distserve` rather than by links.

## Related pages

- [[intelligentLearn - From Symptoms to Fixes - Part 1 - Start with the Machine]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 2 - Six Layers to Investigate]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 3 - How to Evaluate a Change]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 4 - Putting It to Work]]
- [[LLM Inference]]
- [[Prefill-Decode Disaggregation]]
- [[KV Cache]]
- [[Serving Benchmarks and Goodput]]
- [[Inference Serving Engines]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Semantic Caching]]
- [[GPU Fleet Reliability]]
- [[Software Performance Engineering]]
