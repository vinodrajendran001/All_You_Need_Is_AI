---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-11-bytebytego-github-copilot-rust-port
source_title: How GitHub Used AI to Port Copilot From TypeScript to Rust in Record Time
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-github-used-ai-to-port-copilot
tags:
  - source/summary
  - coding-agents
  - code-migration
  - multi-agent
  - code-review
source_ids:
  - src-2026-11-11-bytebytego-github-copilot-rust-port
status: active
---

# How GitHub Used AI to Port Copilot From TypeScript to Rust in Record Time

## Summary

ByteByteGo relays GitHub's account of porting the shared Copilot runtime from TypeScript on Node
and V8 to Rust with the GitHub Copilot app, Copilot CLI, and fleets of AI agents. GitHub replaced
one component per pull request, deleted the old TypeScript in the same change, and treated unchanged
end-to-end tests as the behavioral reference. Agents read, split, translated, tested, and reviewed;
humans kept architecture, interface contracts, and risk. One main developer is credited with
finishing in a few months, at about **$120K** in token costs over roughly **136 billion** tokens.
The article lists regressions that compiled cleanly and reports large start-up, throughput, and
memory gains. Every figure is GitHub's own, relayed from one GitHub Engineering Blog post.

## Key claims

### Why the runtime moved

- The runtime was coupled to the command-line interface, so every SDK client, even in a Python,
  Java, or C# host, launched a separate background process with roughly **100 MB** of memory
  overhead "at a bare minimum", inter-process overhead, two processes to monitor, and a Node crash
  that could take the session down. GitHub wanted a library loaded into the host's own process.
- An early estimate put the port at roughly **130K** lines of production TypeScript. As logic moved
  out of the interface layer and features kept landing, **430K** lines ultimately moved. The
  introduction's "Almost 800K lines of code" is not reconciled with either figure.

### Incremental, in-place porting with one live implementation

- No big-bang rewrite. Each component's TypeScript was replaced with Rust in **a single pull
  request**; dependent TypeScript called it through a **thin wrapper**, a temporary bridge, and the
  old implementation was **deleted in the same change**, so only one version was live.
- The first pull requests set up Rust tooling, checks, coding instructions, and cross-language calls;
  the first real port moved **three independent helper functions** end to end. Work then followed
  dependencies: utilities, stateful components, tools, model clients, and integrations, with session
  orchestration last.
- Behavior and algorithms were preserved and redesign deferred. End-to-end tests gated every merge,
  and ported components shipped incrementally, often as a pre-release first.

### Agent fleets: subagents for questions, child sessions for changes

- **Subagents** worked in the parent session's workspace and returned findings. **Child sessions**
  had their own Git branches and working copies, so several agents could change code independently.
  The Copilot app let sessions be inspected and exchange messages.
- For `session.ts`, roughly **30K** lines, the coordinator spent **an hour** reading before creating
  anything, then split the work across **15 child sessions**, chose a model per task, and merged
  their results into its own branch.
- All 15 building and testing at once overwhelmed the developer's laptop. Builds and tests moved to
  the parent, and a separate chat session allowed only one build at a time.
- Most fleet work was reading, dependency checking, testing, and reviewing rather than writing Rust.
  Human oversight "remained critical".

### Review against the old code, repeated until clean

- A reusable `rust-rebase-review` instruction brought the work up to the latest main branch and
  checked that newly arrived TypeScript changes were ported too. Because old files were deleted,
  such changes surfaced as merge conflicts.
- Review agents on **different AI models** compared old TypeScript and new Rust line by line for
  behavior or compatibility changes, efficiency, and leftover wrappers. They also checked that
  end-to-end tests were **unchanged**, as "the only reference for expected behavior".
- The coordinator fixed valid findings and the cycle repeated until reviews were clean. Copilot Code
  Review and other bots checked every commit; human reviewers focused on architecture, interface
  contracts, and flagged risks.

### What broke

- **Behavior changes that still compiled:** whole numbers that became decimals and broke some SDKs;
  empty strings; time zones; replacement libraries with different error handling.
- **State and coordination:** cancellation that did not stop related work; resources released too
  early, leaving sessions stuck; features lost or only partly migrated.
- **Integration:** Rust doing lengthy work on Node's main thread froze the interface; missing launch
  settings opened stray console windows on Windows. The count is only "a bunch".

### Reported gains and cost

- In one trial, creating a client, completing one turn, and cleaning up fell from **5.25 seconds** to
  **292 milliseconds**, "almost 18 times" faster. Throughput rose from **7.55** to **120** session
  lifecycles per second (about 16x, derived). In a **10-client** test, peak private-memory increase
  fell from **1383 MB** to **126 MB**. More gains are expected from redesigning around Rust.
- Tokens cost about **$120K** for roughly **136 billion** tokens, mostly cached input, which is under
  $1 per million tokens (derived). Developer time is extra: others worked on integrations, packaging,
  builds, and reviews.

### Stated lessons

- Instructions must be explicit; early requests sometimes ported only the central logic.
- Strong end-to-end tests are a precondition, and more coverage would have caught more regressions.
- Tests need protection, so agents cannot weaken a test or change an expected result to pass.
- Translate first, redesign later; mixing the two adds issues, time, and token cost.

## Why it matters

This is the vault's first large agent-run port in which the old implementation is deleted as each
piece lands. It extends [[Legacy Code Modernization with AI Agents]] with a way to keep only one
live implementation, and its regression list shows what code that compiles but behaves differently
looks like. [[Agentic Testing]] gets a case where end-to-end tests are the only oracle and must be guarded
from the agents judged against them. The multi-model, line-by-line comparison is a reference-based
form of [[AI Code Review]]. The subagent/child-session split and the build bottleneck belong with
[[Agent Delegation]]. [[AI-Native Software Development Lifecycle]] gains a one-developer agent-fleet
account with a token bill, [[GitHub]] a first-party case, and [[ByteByteGo]] another relay.

## Tensions / open questions

- **First-party and relayed.** Every number is GitHub's about its own product, via ByteByteGo's one
  cited reference; the publisher says the post is built from public details.
- **Inconsistent size.** "Almost 800K lines" is not reconciled with **430K** or **130K**; the capture
  does not say whether it counts tests, generated Rust, or something else.
- **"Single developer" is qualified in the same article.** Other developers' time is not costed, and
  "a big team of developers and a couple of years" is an asserted counterfactual, not a baseline.
- **Benchmarks lack conditions.** Hardware, models, run counts, and full workload settings are not
  given for any comparison, and the 5.25 s result is "a particular trial".
- **Regressions are anecdotal.** With no count, severity, or escape rate, the review loop's catch rate
  is unknown, and the $120K is not broken down by fan-out, review rounds, or model.
- "Hit would flag a conflict" in the capture is evidently a typo for Git. The NYSE/Redpanda and
  Unblocked blocks are sponsorship.

## Affected pages

- [[Legacy Code Modernization with AI Agents]]
- [[AI-Native Software Development Lifecycle]]
- [[Agentic Testing]]
- [[AI Code Review]]
- [[GitHub]]
- [[ByteByteGo]]
- [[Agent Delegation]]

## Raw capture

- [[knowledge-base/raw/sources/How GitHub Used AI to Port Copilot From TypeScript to Rust in Record Time]]

## Citations

- Canonical URL: https://blog.bytebytego.com/p/how-github-used-ai-to-port-copilot (email tracking
  parameters removed).
- Byline in capture: ByteByteGo. Published 2026-11-11; captured 2026-11-11.
- Sole listed reference: GitHub Engineering Blog, "Migrating the GitHub Copilot runtime to Rust, using
  Copilot" (https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot).
  Not captured in this vault.

## Related pages

- [[Legacy Code Modernization with AI Agents]]
- [[AI-Native Software Development Lifecycle]]
- [[Agentic Testing]]
- [[AI Code Review]]
- [[Agent Delegation]]
- [[GitHub]]
- [[ByteByteGo]]
- [[GitHub - How We Make AI Coding More Cost Efficient]]
- [[Mistral - Modernizing Complex Legacy Code with AI Agents]]
- [[X Engineering - Rebuilding the Global Town Square from Scratch]]
- [[The Decoherence Trap]]
- [[ByteByteGo - How LinkedIn Uses AI to Review 40,000 Pull Requests a Week]]
- [[Multi-Agent Coordination]]
- [[Coding Agent Harness]]
