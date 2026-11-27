---
type: entity
entity_kind: organization
created: 2026-11-27
updated: 2026-11-27
tags:
  - entity
  - organization
  - testing
  - fault-injection
source_ids:
  - src-2026-11-24-antithesis-nightmare-mode
  - src-2026-11-12-huntley-answer-is-engineering
status: active
---

# Antithesis

## What it is

Antithesis is a software testing company. Its customers run their systems inside Antithesis
simulations, where a fault injector and a fuzzer explore failures. A Forward Deployed Engineering team
works with individual customers to deploy fault types for their environments. The vault knows it from two
first-party sources:

- [[Anjana Ratnayake and Teymour Aldridge - Nightmare Mode - Simulating Disk Failures]], an engineering
  post on Amnesia, the company's Rust FUSE filesystem. Amnesia emulates power loss, disk I/O errors
  including the fsyncgate behaviour, and latency faults that reorder or split operations, all tied to
  individual disk operations.
- [[Geoffrey Huntley - The Answer to AI Is Engineering]], a talk in which Huntley, speaking as an
  employee ("validation and verification of software is what we do"), promotes the company's
  property-based testing libraries: **Bombadil** for browser properties and **Hegel**, a Rust core with
  per-language bindings described as the successor to Hypothesis.

## Why it matters here

It supplies the vault's most detailed account of **fault injection** below an application, at the
storage layer, as opposed to tests that drive an application through its inputs. In [[Agentic Testing]] it supplies the case where the
environment, not an agent, is the adversary, and where the oracle is the system's own durability
invariants. Its one shareable result is a bbolt bug that, the authors say, "could only be found by an I/O
error followed by a power failure". Through Huntley it is also the source of the property-based testing
tools that [[Agentic Testing]], [[AI Code Review]], and [[Loop Engineering]] cite as deterministic
verifiers for agent-written code.

## Notes

- **Both sources are first-party.** Nightmare Mode ends with a sales invitation, and Huntley acknowledges
  the conflict ("I'm not just talking my book"). Neither gives detection rates, bug counts beyond the single
  bbolt case, or comparisons with other tools.
- **No AI in the fault-injection post.** Nightmare Mode describes no model or agent; links to agent testing
  are the vault's synthesis.
- The company's publication dates and product names are as recorded on the source pages; nothing else
  about the company (size, funding, pricing) is in the vault.

## Related pages

- [[Agentic Testing]]
- [[AI Code Review]]
- [[Loop Engineering]]
- [[Anjana Ratnayake and Teymour Aldridge - Nightmare Mode - Simulating Disk Failures]]
- [[Geoffrey Huntley - The Answer to AI Is Engineering]]
