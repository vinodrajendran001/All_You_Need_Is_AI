---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-12-huntley-answer-is-engineering
source_title: "the answer to ai is engineering"
source_author: "Geoffrey Huntley"
source_url: "https://ghuntley.com/answer/"
tags:
  - source/summary
  - agent-security
  - supply-chain
  - nix
  - property-based-testing
  - coding-agents
  - opinion
source_ids:
  - src-2026-11-12-huntley-answer-is-engineering
status: active
---

# Geoffrey Huntley - The Answer to AI Is Engineering

## Summary

A written version of Geoffrey Huntley's AI DevCon New York talk. Most of the conference was about
building software faster with factories; he argues for optimising **security incident response**
instead, and says build times then speed up too. His thesis is in the title: the answer to AI-era
risk "isn't more AI. It's engineering." His tools are deterministic: a single Nix-defined source of
truth for every environment, patching dependencies locally instead of waiting on upstream, removing
dangerous capabilities from the tools agents use, hook-based back pressure, and property-based
testing.

This is a **practitioner talk and opinion piece**, built on personal demos and no measurements. Two
parts need particular care. The incident list that opens the talk is unsourced in the capture. The
closing recommendations promote Bombadil and Hegel, libraries from **Antithesis**, where Huntley says
"validation and verification of software is what we do". He adds "I'm not just talking my book", but
it is a conflict of interest.

## Key claims

### "Security take-off" is the new normal (argument)

Huntley lists incidents from "two weeks ago": OpenCode was breached; Japan's Prime Minister urged
everyone to update PHP; an HTTP-stack flaw let anyone remotely turn off a running server; a
12-year-old GitLab flaw allowed remote code execution on self-managed servers; and a certificate
authority's key "should have been a 116-digit number, and it was just 4". None is linked or detailed,
and none is otherwise recorded in the vault. He argues this is "the start of the new normal", because
agents trained on vulnerable code write more of it. He suspects "you're going to need more inferencing
capacity than your attackers", and mocks "a $100-a-month token budget per employee", since published
code will be scanned and exploited autonomously.

### Fewer open-source dependencies (argument)

He says open-source libraries existed "because code was precious" and partly to ease hiring. "It's
been a year, and I don't use much open source anymore". He still uses the Linux kernel, BIND and other
low-level software, and does not suggest writing your own cryptography. Higher up the stack, he either
generates code first-party "in a loop" or **vendors** the source into the repository so the agent can
modify it. He frames upstream merge dependence as a cost: "if you have to tool call a human, that's
not AGI."

### Nix as one source of truth (demo)

One devenv/Nix definition generates developer laptops, CI/CD, agent sandboxes and production Docker
images. That removes the drift between them and the "48 hours to rebuild the developer environment"
he bets some companies face. Agents make Nix, Bazel or Buck2 usable without a dedicated team: "you
just need to know that Nix exists". A Nix **overlay** applies patch files to any package. When
OpenSSL is patched, Nix "recompiles the world", so transitive users such as Nginx and Postgres pick up
the fix, with caching and remote builders limiting rebuild cost. During the incidents he asked Claude
whether his fleet was affected; it said yes and applied patches, pins and ref updates. This is a
single self-reported anecdote.

### Remove the capability, not just the instruction

His demo environment pins git 2.55.0, built with a patch that disables force push and applied
wherever git is a dependency. "The best way to stop a model from doing something is to remove its
ability to do it." Agents "hill-climb" toward a goal and do destructive things on the way, so when
that causes incidents, "remove the capability from the underlying system".

### The AGENTS.md reminder trick

After applying temporary patches, he told the agent to update AGENTS.md "and in seven days' time, get
rid of my patches". The next developer or agent to use the machine removed the patches and pins once
upstream was fixed. He used this in place of a Jira ticket.

### Root only in throwaway environments

His loop agents run with sudo in throwaway Nix developer machines, which he says is safe because "I
designed the operating environment for it". NixOS VM tests (for example HAProxy in front of a
hello-world server across two VLANs) put the OS and network rules under test from day one. The
boundary is explicit: "do not run agents with Nix as root on production hosts, and do not connect
agents to production databases. Ever." To reproduce production data, duplicate the database and
restrict outbound network access.

### Back pressure keeps the loop from closing on bad code

"Ralph was never just about loops. It was about stopping the loop from closing on bad code." He
recommends deterministic checks ("These aren't skills"): pre-commit or prek hooks that block a push
that does not compile, and static rules such as "this domain must never be coupled to that domain".
With those, teams can "engineer away much of the need for code review".

### Property-based testing

Unit tests check only what was specified. Property tests generate inputs and search for a
counterexample, for example that reversing a string twice returns the original, which a faulty
reverser fails on Unicode or emoji. He extends this to system properties such as "a customer who
asks for a refund is only refunded once". **Bombadil** checks a browser property ("the user always
has the ability to log out") by stressing a JavaScript or TypeScript app until the property holds or
fails, returning a reproduction when it fails; he urges "ditch Playwright". **Hegel** is a Rust core
with per-language bindings, described as the successor to Hypothesis from the same team.

## Why it matters

The talk supplies concrete, deterministic versions of controls the vault discusses abstractly. These
are capability removal below the agent for [[Agent Security and Governance]], hook-based back pressure
as a verifier for [[Loop Engineering]] and [[AI Code Review]], and property-based oracles for
[[Agentic Testing]]. The dependency stance is the sharpest disagreement in this batch.

## Tensions / open questions

- **Contradiction with measured library-skipping.**
  [[Gabe Orlanski - Slop Is Moving Up the Stack]] counts hand-written re-implementation of library
  functionality as slop, with 73% to 100% of LUB solutions doing it. Huntley recommends generating
  first-party code over dependencies. Orlanski measures quality cost, and Huntley argues
  supply-chain and patching benefit. Neither weighs the other's cost.
- The incident list, including the 116-digit-to-4 CA key, is unverified here. Treat it as rhetoric
  until sourced.
- "Engineer away much of the need for code review" is asserted without a miss-rate comparison.
  Deterministic checks catch only what someone thought to encode.
- The sudo-in-sandbox safety claim depends on the sandbox design, which the talk does not threat-model
  beyond forbidding production hosts and databases.
- There is a vendor conflict of interest on Bombadil and Hegel, and the PewDiePie usage story is an
  anecdote.

## Affected pages

- [[Agent Security and Governance]]
- [[Agentic Testing]]
- [[AI Code Review]]
- [[Loop Engineering]]
- [[Context Engineering]]

## Raw capture

- [[knowledge-base/raw/sources/the answer to ai is engineering]]

## Citations

- Raw capture: Geoffrey Huntley, "the answer to ai is engineering", published 2026-11-12 (source ID
  date), captured 2026-11-20. The canonical URL drops the newsletter `utm_source` parameter. The
  title is lower-case in the original. The summary filename uses title case.
- The talk video chapters (YouTube) and the `nix-demo` repository are referenced but were not viewed.
- Affiliation: inferred from "At Antithesis, ... We have a library called Bombadil" in the capture.

## Related pages

- [[Agent Security and Governance]]
- [[Agentic Testing]]
- [[AI Code Review]]
- [[Loop Engineering]]
- [[Gabe Orlanski - Slop Is Moving Up the Stack]]
- [[Context Engineering]]
- [[Coding Agent Harness]]
