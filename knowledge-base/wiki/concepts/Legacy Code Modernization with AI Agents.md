---
type: concept
created: 2026-09-25
updated: 2026-11-27
tags:
  - concept
  - coding-agents
  - software-engineering
  - testing
source_ids:
  - src-2026-09-09-mistral-legacy-code-modernization
  - src-2026-10-05-faik-ai-native-software-factory
  - src-2026-10-14-maevyn-decoherence-trap
  - src-2026-11-04-x-town-square-rebuild
  - src-2026-11-11-bytebytego-github-copilot-rust-port
  - src-2026-10-10-0xcodila-rea-reverse-engineering
  - src-2026-11-19-tselovalnikov-10x-engineer
  - src-2026-11-23-tomassetti-legacy-modernization-measured
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

## Incremental migration is itself a debt-producing mechanism

[[The Decoherence Trap]] is an **unattributed essay** — no author appears anywhere in the capture, which is
published at maevyn.codes — and it argues rather than measures. Its contribution here is a name for the cost
this page's own method incurs.

The essay separates three kinds of debt: **infrastructure debt** (wear), **technical-advancement debt** (the
need to upgrade), and **decoherence** — the extra complexity created by **partial, inconsistent transitions**,
where locally valid but mutually incompatible models coexist and every later change has to translate between
them. Its motivating analogy is replacing a building's pipes floor by floor, leaving custom joints and
undocumented interactions. That is a description of staged migration, which is what this page recommends.

**This qualifies the page's existing framing rather than contradicting it.** The sections above treat bounded
migration units and dependency decomposition as risk controls, which they are. The essay points out they are
also the mechanism that produces a mixed-paradigm system: migrating below roughly 10,000-line Fortran units
means old and new coexist for the duration, and the cost of being in that state is not captured by a parity
harness, which asks only whether behaviour matched — not whether the system got harder to change. Read this
way, **parity is a correctness control and decoherence is a separate, unmeasured cost of the same plan**, and
the deterministic Shepherd case is the one that minimises it: a regular, mechanical transformation applied
uniformly leaves no patchwork behind, which is an argument for deterministic migration this page did not
previously have.

The essay also warns against the obvious over-correction. Its simulation suggests a **sweet spot** — too little
coherence work collapses throughput and too much also slows delivery — so the target is a moderate, actively
maintained level with some adaptive "jitter", not maximum uniformity. The simulation is **not evidence**: the
author states that **"The simulation has arbitrary weights and does not definitively prove that this is how
complex systems will evolve."**

The cited third-party research is the more usable part, and all of it concerns agent-assisted development in
general rather than modernization specifically:

| Study, as cited | Scope | Reported result |
| --- | --- | --- |
| Chen and Stratton, Harvard working paper | 718 companies | coding agents increased code written by **30%** with no measurable increase in finished work; pull requests took **49% longer** to review and **nearly twice as many** were returned for changes |
| He et al., Carnegie Mellon | open-source projects adopting Cursor | a large initial velocity increase that **did not last**, with rising code complexity contributing to the later slowdown. **No effect size is quoted** |
| Liu et al. | over **300,000** AI-authored commits across more than **6,000** repositories | approximately **one in eleven** commits — up to **one in seven** depending on assistant — introduced at least one quality issue; **nearly a quarter** of those issues remained in the code |

Two of those bear directly on the agent-count question. The Mistral case reports that more than 100 agents
helped document the codebase; the Harvard figures suggest that **code volume and review burden can rise
together without finished work rising**, which is the same failure the essay predicts when parallel capacity
is added to a system whose complexity is growing. None of these studies examined a migration, none is a
controlled experiment on this page's workload, and the essay itself treats them as suggestive.

The essay's larger claim — that systems could pass a point where humans cannot repair them and agents cannot
recohere them, which it calls **Decoherence Collapse** and estimates would take **"years or even decades"** to
reverse — is a qualitative forecast with no instance behind it. Its value to this page is the vocabulary and
the warning, not a prediction to plan against. See [[Recursive Self-Improvement]], where the same essay's
bubble-optimisation argument is recorded, and [[AI-Native Software Development Lifecycle]].

## Old servers as the specification, with traffic moved one group at a time

[[X Engineering - Rebuilding the Global Town Square from Scratch]] treats the systems being retired as
the specification. Agents read how the old rweb SSR or Jetfuel SSR server handled a URL or page type,
ported the behavior, and wrote a test that pins it down; many behaviors now sit in shared components
"next to tests that name the server they came from." A small parity script requests the same path
from old and new servers as a verified Googlebot and compares what search engines read: status code
and redirect, title, description, canonical URL, robots tags, Open Graph and X card tags, the number
of language alternates, and structured-data types.

Traffic moved in stages: crawler traffic and logged-out pages first (Jetfuel SSR retired on August
1, 2026; rweb SSR shut down in early September), then signed-in people one country at a time. X's
edge decides per request which server answers, so a group can be moved to the new app "and move them
back if something goes wrong." This is the reversible cutover this page asks for. X reports no
parity-failure counts, and the signed-in rollout was still in progress at publication.

## One live implementation: the old code is deleted in the same change

[[ByteByteGo - How GitHub Used AI to Port Copilot From TypeScript to Rust in Record Time]] relays an
agent-run port that bounds the mixed-paradigm state described above. GitHub replaced each component of
the Copilot runtime with Rust in **one pull request**. Dependent TypeScript called the new code
through a **thin wrapper**, and the old implementation was **deleted in the same change**, so only one
live version of each component existed. The wrappers were removed as more of the system moved.
Decoherence still exists in this design, but it is confined to a bridge layer that is explicitly
temporary rather than spread across coexisting implementations. Work followed the dependency order:
helpers, then stateful components, then tools, model clients, and integrations, with session
orchestration last. Behavior and algorithms were preserved and redesign deferred. GitHub's lesson, to
translate first and redesign later, restates this page's parity-before-architecture order.

The oracle was the existing end-to-end suite. Review agents checked that those tests were unchanged,
because they were "the only reference for expected behavior". This is Mistral's parity harness at a
coarser grain: whole workflows rather than intermediate numerical state. The regressions show what a
workflow-level oracle misses even when everything compiles. Whole numbers became decimals and broke
some SDKs. Empty strings, time zones, and replacement libraries' error handling differed.
Cancellation did not always stop related work, resources were released too early, some features were
only partly migrated, and lengthy work on Node's main thread froze the interface. GitHub concedes
more end-to-end coverage could have prevented some more of these, but reports no regression count.

The reported scale does not answer this page's open question about non-agent baselines. It cites
**430K** lines of production TypeScript (an early estimate was **130K**, and the introduction's
"Almost 800K lines of code" is not reconciled), one main developer over a few months, and about
**$120K** in tokens across roughly **136 billion** tokens. The "big team ... couple of years"
comparison is asserted, others' developer time is not costed, and every figure is GitHub's own,
relayed by ByteByteGo. Against [[Adam Faik - How to Build an AI-Native Software Factory|Faik's]]
deterministic Shepherd case, this is the opposite tool choice: agent translation of an irregular
codebase, made safe by deleting the old path and by multi-model review against the old code (see
[[AI Code Review]]).

## When the source is gone, recovered behavior becomes the specification

[[@0xCodila - Reverse Engineering with REA and Opus 5.5 (Full Course)]] describes REA, an MCP server and
command-line tool that lets coding agents inspect compiled or packaged software and report each
finding with evidence and a list of unknowns. Its loop is investigate, write a behavioral spec with
"no copied code", build from the spec, and test against observed behavior. That is the X "old
servers as specification" pattern applied where no source is available. The post names preservation
and "helping companies understand software they lost the source code for" among the uses. The
original executable becomes the oracle, as in Mistral's harness. In REA's own showcases, a DX-Ball
sound-pan function rebuilt in C passes **3,205** original-x86 test cases and reproduces all **63**
compiled bytes, and a Touhou reconstruction reached **696** exact matches out of **697** functions.

Two cautions carry over. Decompiled output is a reconstruction, not the original source, so the
verification step carries the weight. And the comparison harness is itself a failure point: REA's
Touhou lessons include **"test your tests"**, because a broken comparison once let a wrong function
pass. These are first-party showcases quoted in a clickbait-framed post, not independent results. The
legality of rebuilding from someone else's binary depends on clean-room practice and use boundaries;
that discussion belongs in [[Agent Security and Governance]].

## Replacing a licensed component from its specification and test suite

[[Sergey Tselovalnikov - How to Be a 10x Engineer in 2027 and Beyond]] relays a **secondhand**
anecdote from a Pragmatic Engineer podcast episode, in which Gergely Orosz described an engineer whose
company paid "a substantial share of its revenue" to license a critical software component. Rebuilding
it would have taken years. With AI agents, the engineer "managed to build a faster replacement using
the existing specifications and test suite". The original vendor then paid the company for the new
implementation and for keeping it closed-source.

The enabling condition matches this page's port-style migrations: an executable reference (here a
spec plus a test suite) makes an agent-built replacement checkable, as the old servers did for X and
the original binary does for REA. The difference is the target. This is a third-party component, not
the team's own legacy code, so the economic trigger is a licence cost that agents made worth avoiding,
not accumulated debt. No company, component, timeline, benchmark for "faster", or test-coverage figure
is given, and the story passes through two retellings (engineer, then Orosz, then the essay) before
reaching the vault.

## A measured naive baseline: cheap to compile, wrong at the edges

[[Federico Tomassetti - Legacy Modernization with LLMs, Measured]] is this page's first multi-run
measurement, and it removes the condition every case above relies on. Claude Opus 5.5 in Claude Code
translated two real IBM i ERP applications from RPG to Java from a deliberately naive prompt
("Organize the project as you see fit, ensuring the result can be run."), but there was **no IBM i to
run the originals**. Expected behaviour came from reading the RPG source and manual, so the old system
could not serve as the oracle that Mistral's harness, X's parity script, and GitHub's end-to-end suite
provide. The result works as a negative control for this page's parity-first thesis: every check that
was easy to pass passed. Each of the large application's **49** sessions "completed" on its first
attempt, meaning the session finished and the project compiles; the application starts, initializes
its database, and opens menus; and every planned file is mentioned in the agent's log, which the
author says is "not proof" of implementation. Errors were still found in every translation examined,
among them a lost sign that moves a date into another century, inverted commit and rollback, and
**17** programs counted as translated that only throw an exception.

Run-to-run variance is the second finding. Three isolated runs on the small application (about
**15,100** RPG lines) produced **14,500**, **26,300**, and **22,900** lines of Java, and repeated runs
differed in packages, field types, data access, and public interfaces. On normal inputs they agreed:
the three runs that translated five programs of the large application all passed **35** predefined
tests, and one program agreed on all **102 million** valid inputs. Off the normal path (overflow,
negative values, errors halfway through an update, missing source) each run behaved differently, so
whether a given error reaches the application "is decided by which run you happened to get". Errors
shared by every run are ones "you cannot discover by comparing them". The single large translation
shows the decoherence this page warns about inside one project: about a third of the hand-translated
program code also exists, identical or nearly so, in another program; one date conversion is declared
in **27** classes with **20** different bodies; and there are three different ways of calling a
program.

Deterministic tooling appears twice, once by design and once unasked. Strumenta's tooling parsed the
code and dependency-ordered the plan's **2,777** files, and a script split it into **43** phases plus
query and CL phases, the dependency-order discipline of the GitHub port above. Separately, the agent,
without being asked, wrote **seven** Python code generators and used them to produce a large part of
the Java, and about **30** generated files disagree with their own generator. In the vault's reading,
that is the deterministic route of Faik's Shepherd case, chosen by the agent rather than designed, and
not kept consistent with its own output.

The cost figures answer only the cheap half of this page's question about effort. The large
application's first generation cost about **$1,100** at API-equivalent list prices, about **$1.83**
per thousand lines on roughly **603,000** source lines including queries and CL; the team actually
spent Claude subscription quota. GitHub's port above cost about **$120K** in tokens for **430K**
lines, but that figure covers a reviewed, tested, shipped port and this one an unvalidated first
generation, so the two are not comparable. The exclusions are explicit. Writing test scenarios for
just five programs cost **$7.56**, about four times their translation, and planning, reviews,
correction cycles, and human time are not counted. The author's extrapolation of **$12,000** for 1
million lines and **$120,000** for 10 million assumes test generation costs five times the
translation, a multiplier he calls "a hypothesis, not a rate we measured". Phases cost **$1.22** to
**$37.73** and did not grow steadily more expensive as the Java project grew. His summary: "Getting a
first translation and finishing a migration are different amounts of work; we have measured the
former." Tomassetti founded Strumenta, which sells migration services, and says so; correctness
judgments come from reading code and model-assisted checks, so the error list is a set of examples,
not an error rate.

## Open questions

- How should parity tolerances account for floating-point and algorithmic differences?
- Which dependency cuts minimize cross-module behavioral ambiguity?
- How should teams measure migration effort and defects against non-agent baselines?
- **What would a decoherence measurement look like on a migration?** The essay supplies no fitted growth rate
  for complexity in real codebases and does not demonstrate that decoherence grows exponentially anywhere. A
  parity harness answers correctness; this page has no instrument for the mixed-paradigm cost it incurs.
- **How long may a system stay half-migrated?** Nothing in the vault's sources sizes the window in which old
  and new paradigms coexist, or what the per-change tax is while it lasts.
- **Do the cited coding-agent studies apply here at all?** They measured general adoption across companies and
  repositories, not a bounded migration with a parity oracle and human approval gates. The essay does not
  establish that AI-generated code is the sole or dominant cause of the complexity it describes, nor that
  agents cannot maintain or repair highly complex systems.
- **Where is the sweet spot for a migration specifically?** The claim that both too little and too much
  coherence work slow delivery comes from a simulation with arbitrary weights; it gives no operating point.
- **Does same-change deletion keep a port cheaper to change?** GitHub's thin wrappers bound coexistence
  per component, but no source measures the wrapper layer's cost or how long it persisted.
- **Who checks the oracle?** GitHub guarded end-to-end tests from being weakened, and REA's Touhou
  rebuild found a broken comparison. No source reports how often the parity check itself was wrong.
- **What does the expensive half cost?**
  [[Federico Tomassetti - Legacy Modernization with LLMs, Measured]] measured a first generation and
  excluded test generation beyond five programs, correction cycles, and human review; its five-times
  test multiplier is a hypothesis. No source in the vault measures a complete agent migration against
  a non-agent baseline.
- **What replaces the oracle when the original cannot run?** Comparing independent translations
  exposes luck-dependent errors but not the ones every run shares, and Tomassetti's checks relied on
  reading code and on other models.

## Related pages

- [[The Decoherence Trap]]
- [[Recursive Self-Improvement]]
- [[Adam Faik - How to Build an AI-Native Software Factory]]
- [[Coding Agent Harness]]
- [[Agentic Testing]]
- [[Agent Planning]]
- [[AI-Native Software Development Lifecycle]]
- [[Mistral - Modernizing Complex Legacy Code with AI Agents]]
- [[X Engineering - Rebuilding the Global Town Square from Scratch]]
- [[ByteByteGo - How GitHub Used AI to Port Copilot From TypeScript to Rust in Record Time]]
- [[@0xCodila - Reverse Engineering with REA and Opus 5.5 (Full Course)]]
- [[AI Code Review]]
- [[Agent Delegation]]
- [[Agent Security and Governance]]
- [[Sergey Tselovalnikov - How to Be a 10x Engineer in 2027 and Beyond]]
- [[Federico Tomassetti - Legacy Modernization with LLMs, Measured]]
