import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _integrate import integrate

HP = "src-2026-09-02-can-boluk-harness-playbook"
GH = "src-2026-09-03-github-ai-coding-cost-efficient"

integrate(
    "Agent Plugin Architecture", [HP],
    "The state contract is where extension APIs fail",
    """
[[Can Bölük - The Harness Playbook]] provides the sharpest available evidence that extension APIs fail at the
**state contract** rather than at the capability surface. An audit of **78 official Pi extension examples** found
60 stateless, and among the 17 that carried state, **only two were correct**. These are maintainer-written
reference examples — the material other authors copy.

The failures are all one failure: state stored where the harness's durable operations cannot see it. A git
checkpoint in a transient map, cleared before `/fork` can use it. A turn counter in a closure that reports 4
after rewinding to turn 1 and 0 after resume. A dynamically registered tool that survives rewind but disappears
after resume. A "last message" bookmark that means last *in file order*, so it can point at an abandoned branch.

The conclusion drawn is that this distribution of bugs is not a documentation problem:
*"documentation would not repair this distribution of bugs. The engine needs one place where state can exist."*
That is the argument of [[Harness State Authority]], and the property it buys extension authors is precise —
**adding a stateful feature never adds a call site to rewind, fork, resume, or replication.**

A second failure appears one level up. Two popular workflow extensions for the same harness collide with
"Another workflow is active" — despite the harness having **no workflow API**. Both ship a private mutex, and
both were written by the same author, so the coordination only holds inside one author's suite. The
generalisable point: **a missing abstraction becomes visible the moment independently written extensions meet**,
and until then each author reinvents it privately and incompatibly.
""",
    ["Harness State Authority", "Tool Roster Economics", "Can Bölük - The Harness Playbook", "Can Bölük"],
)

integrate(
    "LLM-Native Extensible Software", [HP],
    "Configuration and language choice as parts of the extension surface",
    """
[[Can Bölük - The Harness Playbook]] extends this page in two directions that extension-API discussions usually
skip.

**Configuration is part of the extension surface.** The proposed model is the Source Engine **convar**: a typed
variable declared once at its definition site with a name, default, help string, and a flag bitfield — the flags
carrying persistence, ownership, scope, replication, and replay-honesty. Because the declaration site owns those
properties, an extension adds a setting without touching a central settings object, and a spawned child session
seeds every variable from the parent's live values with no inheritance setting required. Compare the status quo,
where compatibility axes are literally named after the models that caused them (`qwen-preserve-thinking`,
`strip-deepseek-special-tokens`) and three files totalling over 3,600 lines encode model quirks by hand. The
proposed replacement is a declarative taxonomy, and the stated goal is not fewer quirks: *"The win is not fewer
quirks. It is one owner for each fact, explicit precedence, and an `unknown` state."*

**Implementation language acts as a prior on generated code.** The blunt version — *"TypeScript is an awful
choice at the moment"* — rests on the argument that when agents write most of the extension code, the language's
defaults shape what gets generated. The proposed split is a Rust engine with Python extensions, Python chosen
partly because it can inspect its own AST, which makes decorators like `@remote` implementable rather than
aspirational.

The state-model half of the same argument — why extension state must live in one authoritative place — is in
[[Harness State Authority]], along with the audit finding that **only 2 of 17 stateful reference extensions were
correct.**
""",
    ["Harness State Authority", "Agent Plugin Architecture", "Tool Roster Economics",
     "Can Bölük - The Harness Playbook", "Can Bölük"],
)

integrate(
    "Agentic Loop", [HP],
    "The loop needs an owner, and nobody has named it",
    """
[[Can Bölük - The Harness Playbook]] identifies a structural gap this page has not previously named: **there is
no primitive for a behaviour that owns the loop.** The evidence is a collision — installing the two most popular
plan-and-goal extensions for the same harness produces "Another workflow is active", even though the harness
exposes **no workflow API**. Both extensions independently ship a private mutex, and both come from the same
author, so the coordination works only inside one suite.

The proposed primitive is a **Director stack**: an ordered set of behaviours that own the decision about what
happens when the model stops producing tool calls, each returning one of a small set of verdicts — Pass,
Continue, Yield, Push, Done, Fail. A plan mode, a goal loop, an approval gate, and a test-until-green loop then
compose instead of colliding, because precedence is explicit rather than first-come. Crucially the stack lives
in the session's authoritative state, so rewind removes Directors, resume restores them, and an inspector can
see which behaviour currently owns the loop — see [[Harness State Authority]].

The same source collapses several loop-adjacent constructs into **one job primitive** with stdin, stdout, an
exit code, and signals: a backgrounded shell command, a subagent, a daemon, a remote function call, and a call
that overruns its turn are all the same object with different bodies. The practical warning attached is that a
loop blocking without bound is not merely slow — it can outlast the provider's KV cache, so the resumed turn
pays full prefill. And `AbortSignal` or `context.Context` do not solve it: they are *"useful protocols, but not
enforced ones"*, so a loop needs a real kill boundary rather than cooperative cancellation.
""",
    ["Harness State Authority", "Tool Roster Economics", "Can Bölük - The Harness Playbook", "Can Bölük"],
)

integrate(
    "Agent Delegation", [HP, GH],
    "Subagents need isolation the file system does not give them",
    """
[[Can Bölük - The Harness Playbook]] identifies an isolation gap that delegation designs routinely assume away.
Git worktrees are the standard mechanism for giving each subagent its own workspace, but **worktrees isolate
tracked files only**. Build outputs, caches, virtual environments, `node_modules`, lock files, and untracked
scratch state are shared, so parallel subagents in "isolated" worktrees still collide over exactly the artifacts
that make a build reproducible. The proposed answer is a **copy-on-write view** of the workspace — APFS, btrfs,
ZFS, overlayfs, or ProjFS depending on platform — so a subagent gets the whole directory cheaply and its writes
stay local until merged.

Delegation also inherits the state problem. If a subagent's lifecycle is tracked outside the session's
authoritative state, then rewinding past its creation leaves an orphan, and resuming does not restore it. When
the session is one authoritative structure, a subagent is an element in it and **rewind becomes a diff**: a
subagent that disappears in the target state is terminated, one that appears is spawned. See
[[Harness State Authority]]. The same framing makes a subagent inspector a peer of the main UI rather than a
special case — an actor pointed at a child's state.

[[GitHub - How We Make AI Coding More Cost Efficient]] adds two production measurements. Delivering two
background subagent results as separate notifications produced **four model calls where one would do**; batching
them was worth **2.3%** of the cost metric. And a meta-prompting loop that halved the task-tool prompt
accidentally **serialised independent agents** by rewriting cautious parallelism guidance into a hard scheduling
policy — a regression invisible offline, fixed by restoring one sentence: *"Independent agents can run in
parallel; consider side effects."* Delegation policy lives in prompt text, and prompt text can be optimised away.
""",
    ["Harness State Authority", "Tool Roster Economics", "Can Bölük - The Harness Playbook",
     "GitHub - How We Make AI Coding More Cost Efficient", "Can Bölük", "GitHub"],
)

integrate(
    "Agent Security and Governance", [HP],
    "The sandbox should be an obedient stub",
    """
[[Can Bölük - The Harness Playbook]] takes a firm position on where the boundary belongs: **the sandbox executes
and nothing else.** State, inference, policy, routing, approval, limits, and journaling all stay on the host. A
sandbox that holds session state, or that decides what is permitted, becomes a second authority — and a second
authority is both a correctness bug and an attack surface, because compromising the sandbox now compromises the
record of what happened. Stated as a rule, the sandbox is *an obedient stub*.

This gives the page's least-privilege material a specific structural failure mode to look for: not "did we
restrict the agent?" but "does the restricted component hold anything the restriction was supposed to protect?"

Two concrete gaps follow. **Git worktrees isolate tracked files only** — caches, build outputs, virtual
environments, and untracked scratch state remain shared between supposedly isolated agents, so worktree-based
isolation is not a security boundary. And **cooperative cancellation is not enforcement**: `AbortSignal` and
`context.Context` are *"useful protocols, but not enforced ones"*, so a runaway or malicious job needs a real
kill boundary rather than a flag it can ignore.

The source also documents an injection path in a place nobody audits. A community terminal renderer slices
strings by codepoint, ignores terminal width, and **does not sanitize fetched content**, so text an agent
retrieves from the web can carry ANSI escape sequences straight into the user's terminal. The underlying design
error is stated generally: *"An already-rendered string is being used as layout tree, style tree, content,
transport, and terminal program at once."* Where a rendered string is simultaneously data and a program, output
handling is a security boundary, not a display detail.
""",
    ["Harness State Authority", "Tool Roster Economics", "Can Bölük - The Harness Playbook", "Can Bölük"],
)
