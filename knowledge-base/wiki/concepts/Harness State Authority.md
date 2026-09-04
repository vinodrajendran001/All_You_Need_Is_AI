---
type: concept
created: 2026-09-04
updated: 2026-09-04
tags:
  - concept
  - agents
  - harness
  - systems
source_ids:
  - src-2026-09-02-can-boluk-harness-playbook
status: active
---

# Harness State Authority

## Definition

Harness state authority is the question of **where the truth about an agent session lives**, and whether every
durable operation — rewind, fork, resume, replication, inspection — derives from that one place. A harness has a
single authority when any feature's state is journaled in the same structure as the transcript. It has multiple
authorities when features keep state beside the transcript, in closures, registries, or maps, and each such
feature must then be taught about every durable operation separately.

## Why it matters

Most harness discussion in this vault is about what a harness *does*: which tools it exposes, how it manages
context, how it loops. Authority is the question underneath. It determines whether the harness can offer rewind
and fork at all, whether a remote client can watch a session, and whether an extension author can add a stateful
feature without introducing a bug in an operation they never touched.

The stakes are unusually well evidenced. [[Can Bölük - The Harness Playbook]] audited **78 official Pi extension
examples: 60 were stateless; among the 17 with state, only two were correct.** These are maintainer-written
reference examples. When 15 of 17 demonstrations of a contract are wrong, the defect is in the contract. The
conclusion drawn is structural rather than educational: **"documentation would not repair this distribution of
bugs. The engine needs one place where state can exist."**

The failures are also diagnostic, because they are all the same failure wearing different clothes:

- a git checkpoint held in a transient `Map`, cleared by a settle event before `/fork` can use it;
- a turn counter in a closure that reports turn 4 after rewinding from turn 3 to turn 1, and zero after resume;
- a dynamically added tool that survives rewind and then disappears after resume;
- a "last message" bookmark that means last *in file order*, so it can bookmark a message on an abandoned branch;
- a tic-tac-toe move that vanishes when the session crashes and resumes, because live writes and restore reads
  use different entry types.

Each is a feature that stored state where rewind, resume, and fork could not see it.

## Current synthesis

**Durability has three implementations, and picking none is the common failure.** Preserve the history that
produces state (event sourcing); preserve the changes to the properties you care about (incremental snapshotting,
which the Source Engine uses for networking); or preserve the machine itself (diff the WASM memory). The
diagnosis of existing harnesses is that they use none of them consistently — "there are events, but state is not
really sourced from those events," violating the first principle of event sourcing: **state must be derivable
from the events alone.**

**One authority collapses several hard problems into one operation.** If the whole session materialises as a
single tree with a property-change patch journal, then:

- **Rewind becomes a diff.** Diff the current materialisation against the target state; a subagent element that
  disappeared is terminated by destroying the element, one that appeared is spawned by creating it. The delta
  *is* the lifecycle work list.
- **Prompts become projections.** The system prompt queries the same tree instead of receiving a large state
  object assembled by hand.
- **Replication becomes subscription.** A remote client consumes the patch stream rather than tailing a file.
- **Rendering becomes projection.** Streaming arguments mutate one child element, streaming output mutates
  another, and every client renders the same element state.

The property that makes this worth the rewrite is compositional: **"Adding a stateful feature never adds a call
site to rewind, fork, resume, or replication."** Multi-authority designs have the opposite property — each new
stateful feature adds work to every durable operation, which is precisely why 15 of 17 examples were wrong.

**Controller and actor must be separate.** When views read live session state directly, adding a subagent
inspector means plumbing controller state through UI internals. If the controller owns session state and actors
only render its snapshot and patch stream, then the terminal UI, a remote client, and a subagent inspector become
peers, and inspecting a child is just pointing an actor at the child's state.

**Configuration is state too, and benefits from the same treatment.** The proposed model is the Source Engine
convar: a typed variable with a name, default, help string, and flags declared **once at the definition site**,
where persistence, ownership, scope, replication, and replay-honesty are properties of the variable rather than
of a settings god object. A session-scoped convar is then just another journaled node in the authoritative tree,
and its flags declare how it participates in resume, rewind, spawn, replication, and archival. Inheritance stops
needing its own setting: a spawned child seeds every variable from the parent's live values by default.

**Loop-owning behaviours need a named primitive, or extensions invent private ones.** Installing two popular
workflow extensions for the same harness produces a mutual-exclusion warning — despite there being **no workflow
API**. Both extensions ship a private mutex, and both came from the same author, so the coordination only works
within one author's suite. The generalisable observation: **the missing abstraction becomes visible as soon as
independently written behaviours meet.** The proposed fix, a stack of Directors that own the decision to yield,
matters here mainly because the stack lives as a subtree of the session state — so rewind removes Directors,
resume restores them, and an inspector can see which behaviour currently owns the loop.

## Open questions

- **Does a single authoritative tree survive contention?** The design targets many agents in one workspace, but
  no concurrency or conflict-resolution results are reported. Multi-authority designs at least fail locally.
- **What is the cost of materialising state at an arbitrary journal point?** Rewind-as-diff assumes
  materialisation is cheap enough to do on demand for long sessions.
- **How much of the benefit needs the DOM specifically?** The source concedes an ECS or another serialisable
  representation would work, choosing XML for inspectability. If the authority property is what matters, the
  representation may be incidental — but no comparison is offered.
- **Is the 78-example result reproducible in other harness ecosystems?** It is a strong claim about one
  extension API. Whether harnesses with different contracts show the same defect rate is unknown, and the
  audit's own arithmetic does not close (60 + 17 = 77).
- **Where does state authority sit when the sandbox is remote?** [[Agent Security and Governance]] wants
  execution isolated; authority wants one journal. The proposed answer is that the host keeps journaling and the
  sandbox only executes, but the durability of that split under partition is untested.

## Related pages

- [[Can Bölük - The Harness Playbook]]
- [[Coding Agent Harness]]
- [[Harness Optimization]]
- [[Tool Roster Economics]]
- [[Agent Plugin Architecture]]
- [[LLM-Native Extensible Software]]
- [[Agentic Loop]]
- [[Agent Delegation]]
- [[Agent Security and Governance]]
- [[Context Engineering]]
- [[Agent Memory]]
- [[AI Agents in Production]]
- [[Can Bölük]]
