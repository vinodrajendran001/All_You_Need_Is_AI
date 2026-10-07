---
type: concept
created: 2026-09-25
updated: 2026-10-07
tags:
  - coding-agents
  - software-engineering
  - testing
source_ids:
  - src-2026-09-09-mistral-legacy-code-modernization
  - src-2026-10-05-faik-ai-native-software-factory
status: active
---

# Legacy Code Modernization with AI Agents

## Definition

AI-assisted legacy modernization combines behavioral characterization, documentation, dependency
decomposition, code translation, and review. Its central invariant is parity with the runnable legacy
system, not syntactic similarity between old and new code.

## Why it matters

Legacy scientific and industrial systems often encode domain behavior that has outlived their authors,
tests, and documentation. Agents can accelerate exploration and migration only after that behavior is
made observable enough to verify.

## Current synthesis

[[Mistral - Modernizing Complex Legacy Code with AI Agents]] begins with a parity harness: instrument
the Fortran system to export intermediate state, load those checkpoints in C++, and compare numerical
behavior before refactoring architecture. That converts the old executable into an oracle while
avoiding an assumption that translated code is correct because it compiles.

The next stage maps the caller-callee tree and documents manageable subtrees. More than 100 agents
reportedly helped document the case-study codebase, while migration units stayed below roughly 10,000
Fortran lines. Planner, coder, tester, and reviewer roles then operated inside bounded units with human
approval gates.

The source's qualitative comparison argues against maximum autonomy: unconstrained agents lose
system-level constraints, while structured workflows preserve a single migration contract. This is
one vendor case study, not a measured claim that a particular agent count or module size generalizes.

## Deterministic migration belongs in the comparison

[[Adam Faik - How to Build an AI-Native Software Factory]] supplies a counterweight to the
agent-centered Fortran case. In the reported Uber JUnit migration, generative AI was tried
unsuccessfully; deterministic Shepherd automation then produced **5,000+ diffs** and migrated
**75,000+ test classes in four months**, with AI assisting failures.

The lesson is not that deterministic tools always beat agents. A regular, checkable transformation
and an undocumented scientific-code translation are different tasks. It is that the migration
contract should choose the tool: automate known transformations directly, use agents where
interpretation or repair is needed, and retain parity checks in either case. Faik's figures are
secondary company reporting, not a controlled comparison with Mistral's workflow.

## Open questions

- How should parity tolerances account for floating-point and algorithmic differences?
- Which dependency cuts minimize cross-module behavioral ambiguity?
- How should teams measure migration effort and defects against non-agent baselines?

## Related pages

- [[Adam Faik - How to Build an AI-Native Software Factory]]
- [[Coding Agent Harness]]
- [[Agentic Testing]]
- [[Agent Planning]]
- [[AI-Native Software Development Lifecycle]]
- [[Mistral - Modernizing Complex Legacy Code with AI Agents]]
