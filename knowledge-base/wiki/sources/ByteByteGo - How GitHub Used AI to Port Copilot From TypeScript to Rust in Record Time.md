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
and V8 to Rust, using the GitHub Copilot app, Copilot CLI, and fleets of AI agents. GitHub
replaced one component per pull request, deleted the old TypeScript in the same change, and used
unchanged end-to-end tests as the behavioral reference. Agents read, decomposed, translated,
tested, and reviewed; humans kept architecture, interface contracts, and risk. The article
credits one main developer with finishing in a few months, at about **$120K** in AI token costs
over roughly **136 billion** tokens. It names the regressions that survived compilation and
reports large start-up, throughput, and memory gains. Every figure is GitHub's own, relayed from a
single GitHub Engineering Blog post.

## Key claims

### Why the runtime moved

- The TypeScript runtime was tightly coupled to the command-line application's interface. The SDK
  was built on top of that application, so each SDK client launched a separate background process
  containing the CLI and its runtime, even from Python, Java, or C# hosts.
- Each client bore roughly **100 MB** of memory overhead "at a bare minimum", paid inter-process
  overhead, and had to monitor two processes; a crash in the Node process could take the session
  with it. GitHub wanted a standalone library loaded directly into the host's own process, and
  chose Rust for low overhead and predictable resource usage.
- An early estimate put the port at roughly **130K** lines of production TypeScript. Logic moved out
  of the interface layer and other developers kept adding features, so **430K** lines of production
  TypeScript ultimately moved through the migration. The introduction says "Almost 800K lines of
  code", which the body does not reconcile with 430K.

### Incremental, in-place porting with one live implementation

- There was no full rewrite and single switchover, which would have concentrated risk in one release
  and forced the replacement to chase ongoing changes. A component's TypeScript was replaced with
  Rust in **a single pull request**; dependent TypeScript called the Rust through a **thin wrapper**,
  a temporary bridge removed later. The old implementation was **deleted in the same change**, so
  only one active version existed.
- The first pull requests set up Rust build tools, automated checks, coding instructions, the runtime
  library, and cross-language calls. The first real porting change moved **three independent helper
  functions** end to end to prove the process. Work then followed the dependency order: helpers and
  utilities, stateful components, tools, model clients, and integrations. Session orchestration came
  last because large subsystems needed several rounds.
- The aim was to keep existing behavior and algorithms, deferring redesign. Existing end-to-end tests
  gated every merge, and ported components reached users through incremental releases, often a
  pre-release before stable.

### Agent fleets: subagents for questions, child sessions for changes

- A coordinating agent could investigate a component, split it into tasks, and create other agents.
  The Copilot app let the developer inspect and switch between sessions, which could exchange
  messages.
- **Subagents** worked in the parent session's workspace and returned findings, suited to
  investigation. **Child sessions** had their own Git branches and separate working copies, so
  several agents could change different areas independently.
- For `session.ts`, roughly **30K** lines, the coordinator spent **an hour** reading and checking
  before creating anything, then split the work across **15 child sessions**, chose a model for each
  task, tracked them, and merged their results into its own branch.
- When all 15 built and tested at once, they overwhelmed the developer's laptop. Child agents then
  skipped expensive builds and tests, the parent ran them, and a separate chat session granted build
  access to one porting session at a time.
- Most fleet activity was reading code, checking dependencies, testing, and reviewing, not writing
  Rust. The article says human oversight "remained critical".

### Review against the old code, repeated until clean

- A reusable instruction, `rust-rebase-review`, had the main agent bring its work up to the latest
  main branch, resolve conflicts, and check that newly arrived TypeScript changes had also been ported.
  Deleting the TypeScript made such changes visible as conflicts.
- Several review agents using **different AI models** compared old TypeScript and new Rust line by
  line for behavior or compatibility changes. They also checked efficiency, removal of obsolete
  TypeScript and wrappers, and that end-to-end tests were **unchanged**, because those tests were
  "the only reference for expected behavior".
- The coordinator fixed valid findings and the cycle repeated until reviews came back clean. Each
  round could be pushed for automated checks. Copilot Code Review and other review bots checked
  every commit. Human reviewers focused on architecture, interface contracts, and risks flagged by
  agents or tests.

### What broke

- **Subtle behavior changes that still compiled:** some whole numbers became decimals and broke
  certain SDKs; others involved empty strings, time zones, and replacement libraries with different
  error handling.
- **State and coordination:** cancelling an operation did not always stop related work, and early
  resource release could leave a session stuck. Some features were lost or only partly migrated.
- **Integration and performance:** Rust sometimes ran lengthy work on Node's main thread and froze
  the interface. On Windows, missing process-launch settings opened unwanted console windows.
- The article says a "bunch" of regressions were found and fixed, without a count.

### Reported gains and cost

- In one trial, creating a client, completing a single turn, and cleaning up went from **5.25
  seconds** to **292 milliseconds**, "almost 18 times" faster.
- With many sessions sharing one client, throughput rose from **7.55** to **120** completed session
  lifecycles per second, roughly 16x (derived). In a **10-client** test, the peak increase in private
  memory fell from **1383 MB** to **126 MB**.
- Algorithms were largely preserved, so the article expects more gains from redesigning around
  Rust's ownership and concurrency model.
- Token cost was about **$120K** over roughly **136 billion** tokens, mostly cached input. That works
  out to under $1 per million tokens (derived). Developer time was extra: besides the main developer,
  others worked on integrations, packaging, builds, and reviews.

### Stated lessons

- Instructions must be explicit. Early port requests sometimes produced only the central logic while
  surrounding work stayed in TypeScript.
- Strong end-to-end tests are a precondition. Coverage was improved beforehand, but more would have
  prevented more regressions.
- Tests need protection. An agent should not weaken a test or change an expected result to make an
  implementation pass.
- Translate first and redesign later. Combining the port with improvements raises issues, time, and
  token cost.

## Why it matters

This is the vault's first account of a large agent-run port where the old implementation is
deleted as each piece lands. It extends [[Legacy Code Modernization with AI Agents]] with a
mechanism for keeping only one live implementation, and its regression list shows what "compiles but
behaves differently" looks like. [[Agentic Testing]] gets a production case where end-to-end tests are
the only oracle and must be guarded from the agents being judged against them. The multi-model,
line-by-line comparison loop is a reference-based instance of [[AI Code Review]]. The
subagent/child-session split and the build bottleneck belong with [[Agent Delegation]].
[[AI-Native Software Development Lifecycle]] gains a single-developer agent-fleet account with a
token bill. It is also a new entry for [[GitHub]] and a named-company relay for [[ByteByteGo]].

## Tensions / open questions

- **First-party, relayed.** Every number comes from GitHub about its own product, via ByteByteGo's
  single cited reference. The publisher's disclaimer says the post is assembled from public details.
- **Inconsistent size.** "Almost 800K lines of code" in the introduction is not reconciled with **430K**
  lines of production TypeScript migrated or the **130K** early estimate. The capture does not say
  whether 800K includes tests, generated Rust, or something else.
- **"Single developer" is qualified in the same article.** Other developers contributed integrations,
  packaging, build improvements, and reviews, and their time is not costed. The claim that a project
  this size "would have required a big team of developers and a couple of years" is an asserted
  counterfactual, not a measured baseline.
- **Benchmarks lack conditions.** The 5.25 s to 292 ms result is "a particular trial"; hardware,
  models, run counts, and full workload settings are not given for any of the three comparisons.
- **Regressions are anecdotal.** No count, severity, escape rate, or time-to-detect is reported, so
  the review loop's catch rate is unknown.
- **No cost breakdown.** The $120K figure does not separate the 15-session fan-out, review loops, or
  model choices, and there is no per-component cost.
- The capture's "Hit would flag a conflict" is evidently a typo for Git. The NYSE/Redpanda Agentic
  Data Summit and Unblocked blocks are sponsorship, not part of the article.

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
