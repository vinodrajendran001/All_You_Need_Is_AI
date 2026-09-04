---
type: source-summary
created: 2026-09-04
updated: 2026-09-04
source_id: src-2026-09-02-can-boluk-harness-playbook
source_title: "The Harness Playbook"
source_author: Can Bölük
source_url: https://stencil.so/blog/harness-playbook
tags:
  - source/summary
  - topic/agents
  - topic/harness
  - topic/systems
source_ids:
  - src-2026-09-02-can-boluk-harness-playbook
status: active
---

# Can Bölük - The Harness Playbook

## Summary

A 36,000-word postmortem-and-playbook from the author of the `omp` agent harness, written as `omp²` is being
rebuilt from scratch. Its organising claim is that an agentic harness is structurally a **game engine**: it
"maintains an authoritative world, journals changes, runs untrusted actions, replicates state to multiple views,
schedules actors, interprets commands, adapts incompatible protocols, and renders a real-time interface." Every
one of those is a category with decades of prior art, so the hard problems of a harness are mostly **already-solved
problems that the current generation of harnesses is re-solving badly**.

The essay is unusual in this vault because it argues from the author's own shipped failures rather than from a
model release or a benchmark. Each chapter is split into "what omp taught us" (the failure in production) and
"what omp² changes" (the replacement), and the author is explicit that some of the replacement is shipped and
some is still being thought through.

The framing argument is a correction to a much-quoted line. Dijkstra's "simplicity is prerequisite for
reliability" is, the author says, routinely misread as *simple good, complex bad* — "we shamefully use it to
excuse the implementer from reasoning." The missing half comes from Ousterhout: module writers should **"embrace
suffering,"** take on hard problems, solve them completely, and push complexity *down* into the module. The
current harness ecosystem inverts this, letting the **conservation of complexity** tip toward extensions and
users.

## Key claims

**The design envelope is four architecture tests, not four personas.** A harness should be designed against a
multiplexed workspace (many agents, one folder), a remote driver (phone driving a cloud agent), a spectator (web
client watching), and "Factorio" (an automated software factory against untrusted input). These vary
local/remote, interactive/autonomous, trust boundary, and concurrency. "A design that only works for the first
case tends to smuggle the controller into the TUI, keep state in closures, let extensions execute in the engine
process, and assume a human can recover from an unbounded call."

**Five consequences follow:** one authoritative session; a trusted control plane; bounded work; explicit
compatibility; views are projections.

**The state evidence is the essay's hardest number.** Of **78 official Pi extension examples, 60 were stateless;
among the 17 with state, only two were correct.** Nine named failures are tabulated and reproduced in an
appendix — a checkpoint cleared before `/fork` can use it, a turn counter in a closure that produces turn 4 after
rewinding from 3 to 1, a tool that survives rewind then disappears after resume, a tic-tac-toe move that vanishes
on crash-and-resume. The conclusion is structural: **"documentation would not repair this distribution of bugs.
The engine needs one place where state can exist."**

**Durability has exactly three implementations**: preserve the history (event sourcing), preserve property
changes (incremental snapshotting, which the Source Engine uses for networking), or preserve the machine (diff
WASM memory). omp and Pi "use... none of them consistently" — there are events, but state is not derived from
them, violating the first principle of event sourcing: **state must be derivable from the events alone.**

**One authority collapses four hard problems into one operation.** In omp², the whole session materialises as a
single DOM (XML chosen for inspectability) with a property-change patch journal. Then **rewind is a DOM diff** —
"a `<subagent>` element disappeared? Terminate it by destroying the element... The delta itself is the complete
lifecycle work list." Prompts become projections that query the tree; replication becomes patch subscription;
rendering becomes projection. The payoff line: **"Adding a stateful feature never adds a call site to rewind,
fork, resume, or replication."**

**The sandbox should execute, not decide.** Putting the executor in the VM fails because programmatic tool use
needs all tools, forcing a duplex gateway that "defeats the purpose." Putting the driving app in the VM leaks
prompts and source. What works is a single obedient stub in the VM with hard caps on returned data — "you don't
want a 2GB response to a misused Read tool." The host owns session state, inference, policy, tool routing,
approval, limits, and journaling; the sandbox owns execution only. Subagents get the same boundary at the
filesystem layer via copy-on-write workspace views, because **worktrees isolate tracked files only**.

**Limits belong to the primitive, not the tool author.** "A Pi tool has no limits: return 1 MB of text and it is
forwarded to the model verbatim." Truncation must be **opt-out** (`notrunc`), because an opt-in helper guarantees
uneven coverage — authors who don't know it exists roll their own notice, authors who never imagined a huge
result roll nothing. Truncating inside each tool also breaks code mode: the agent can never trust a tool's output
inside `Eval`, and **N+1 independent truncation layers stack around the same data**.

**One job primitive.** "A backgrounded shell, a subagent, a dev-server daemon, a remote function, and an ordinary
call that ran past its budget are all the same object — a job with stdin, stdout, an exit status, and a signal
handle." Unbounded blocking has a non-obvious cost: **the provider's KV cache can expire before the call
returns.**

**Cancellation needs a kill boundary.** `AbortSignal` and `context.Context` are "useful protocols, but not
enforced ones" — forget to pass the signal and a timeout only tells the agent to continue while the work keeps
burning resources. "Cancellation belongs to the runtime contract, not to every tool author's good behavior."

**Configuration should be Source Engine convars.** A convar is a typed variable with a name, default, help
string, and a bitfield of flags declared once at the definition site; persistence, ownership, scope, replication
and replay-honesty are **properties of the variable**, not of a god object. The observation that motivates it is
social: "most people who have touched a Valve game know what `sv_cheats` does off the top of their head... I
can't recall a single unhappy user. Can you remember any other configuration of any other software?" Inheritance
then needs no setting at all — a spawned child seeds every variable from the parent's live values by default.

**The loop-shaped hole.** Installing the two most popular Plan and Goal extensions for Pi produces "Warning:
Another workflow is active in this session" — but **there is no workflow API**; both extensions ship a private
`WorkflowMutex`, and both came from the same author. "The complexity of introducing a system to encapsulate this
behavior was passed down to the plugin authors, who can only build a system that works among their own
extensions." omp had the same defect as hand-written mode checks "restated by hand at six other entry points."
The fix is a named primitive — a **Director** stack that owns the candidate yield, with six decisions (Pass,
Continue, Yield, Push, Done, Fail) and, critically, living as a subtree of the session DOM so rewind removes
Directors and resume restores them.

**Model quirks must become structured knowledge.** Before one omp refactor, OpenAI compatibility lived in an
880-line file of chained booleans (`isCerebras`, `isZai`, `isMoonshotKimi`...), with the same knowledge
duplicated across `model-thinking.ts` (977 lines), `variant-collapse.ts` (1,776 lines), and separate Bedrock,
Anthropic and Devin builders. It was replaced by declarative taxonomy/classes/providers rules. **"The win is not
fewer quirks. It is one owner for each fact, explicit precedence, and an `unknown` state when the library has not
established an answer."** The compiler errors on ambiguous precedence so "file order does not secretly win."

**Tool schemas are model-facing protocols, so validate *and* correct.** "Models are not generic API clients.
Their mistakes are often specific to the tool name and the harnesses represented in training." Composer models
emit `Grep` with another harness's shape even when no `Grep` exists; Codex sends `paths: string[]` as one
delimited string. Be strict about the semantic contract, charitable about the model's dialect.

**Forced tool calls need a three-step policy, not a flag.** Always inject a soft prompt (hosted APIs quietly
prepend this, "but open-source inference engines don't, so a model behind vLLM gets a hard constraint it was
never told about, and flails when reasoning is enabled"); set the native flag only when it is free, since
Anthropic's can turn a forced call into a conversation-wide cache miss; escalate to the costly flag on
non-compliance because **"correctness wins over the cache once persuasion has failed."**

**The tool roster is a wall-clock tax, and it was measured.** After a user complaint that omp was nearly twice as
slow as Codex on the same task, the culprit was the tool roster: **limiting it to five essential tools gave 36.6s
against Codex's 42.2s and Pi's 37.0s** (task `sol`, median of 6 runs, fresh session each). The mechanism is that
tool grammar constrains token generation to produce valid JSON, on top of the description tokens. **"A tool is
not some free win, just in case the model needs it."** Dynamic discovery avoids the permanent cost but
invalidates the prompt cache when the roster changes. The proposed resolution is a stable tiny grammar with the
long tail behind a `dyn` command surface reachable from Bash or `Eval`, plus a rule: **"Bounded operation set:
schema. Open-ended operation set: code surface."**

**Compaction should be scheduled, not triggered.** The naive design gives the worst UX — "the user waits for the
largest request of the session at the exact moment they are most invested" — and "even the frontier lab ships the
naive design." Instead, kick off compaction speculatively ~10% before the limit, branching the conversation into
a working version and a compacting version, then splice the result in. This also preserves momentum, because the
model "will not get confused by a handoff message standing as the only message in the history, but instead, will
see all the progress it *should* have done anyway."

**Rendering strings compound into a performance, security, and consistency failure at once.** Profiling one Pi
session found the renderer dominating CPU: **267s of render time reduced to 90ms** in the rewrite, with **98.7s
spent re-wrapping in `wrapAnsi`** and a single `.includes` check for image lines consuming a large share of
session CPU **in a session containing zero images**. A community renderer from the Pi catalog slices text by
codepoint rather than display width (breaking below 40 columns), ignores terminal width, and — most seriously —
**does not sanitise fetched content, so a fetched page can emit ANSI escapes that rewrite the user's terminal**.
The diagnosis unifies all three: "an already-rendered string is being used as layout tree, style tree, content,
transport, and terminal program at once."

**Language choice is architecture, and more so now.** "A language that permits twenty equally normal local styles
asks the model to make twenty decisions before it reaches the product problem." The author's claim is that
defaults, standard libraries, canonical project shapes and compiler feedback act as **a prior for generated
code** — and states flatly that "TypeScript is an awful choice at the moment unless you have no choice but to
interact with frontend code," listing seventeen unresolved TS style forks. omp² chose Rust for the engine and
Python for extensions, the latter partly because Python can inspect its own AST with the standard library, which
is what makes a `@remote` decorator able to package a local-looking function and run it in the sandbox.

## Why it matters

This is the deepest treatment of harness *architecture* the vault holds. [[Coding Agent Harness]] and
[[Harness Optimization]] have until now been assembled from vendor posts and practitioner threads that describe
what a harness does and how to tune it. This source describes what breaks when one is built naively, with the
author's own shipped code as the evidence, and it names the boundaries whose absence causes the breakage.

Three of its arguments generalise well past agent tooling. The **78-examples audit** is a rare quantitative claim
about extension-API design: when only 2 of 17 stateful examples written by the maintainers themselves are
correct, the defect is in the contract, not the authors. The **tool-roster wall-clock measurement** puts a number
on something the vault has repeatedly discussed qualitatively — that tools are not free — and locates the cost in
constrained decoding rather than in prompt tokens alone. And the **language-as-prior** argument reframes stack
choice as a question about what code models will generate by default, which connects to the vault's material on
AI-assisted development rather than to conventional language debates.

It also pairs directly with [[GitHub - How We Make AI Coding More Cost Efficient]], ingested in the same batch.
Both argue that the harness — not the model — owns a large share of cost and latency, and both find that the
obvious local optimisation is the wrong one. Read together they are the vault's strongest evidence that harness
engineering is now a distinct discipline with its own measurement traps.

## Tensions / open questions

- **The evidence is the author's own competitor analysis.** Every failure is drawn from Pi and from the author's
  own omp, and the replacement is a product the author is selling attention for. The specific failures are
  documented with source links and reproductions, so the *observations* are checkable; the claim that the DOM
  architecture fixes them is a design argument, not a result.
- **`omp²` is not finished.** The author states the design is "in states ranging from shipped to still being
  thought through." None of the "what omp² changes" claims carry post-rewrite measurements, with the exception of
  the render-time figure.
- **The 78-example arithmetic does not close.** 60 stateless plus 17 stateful is 77, not 78. The discrepancy is
  small and repeated identically in the appendix, but it is unexplained.
- **The two render-cost figures for the image-line check disagree.** The summary panel reports 13% of profiled
  CPU in one `.includes`, while the prose says the same check "accounted for 20% of the total CPU cycles spent in
  a session." Both cannot be the same measurement.
- **The tool-roster benchmark is one task.** 36.6s vs 42.2s vs 37.0s is a median of 6 runs on a single task
  (`sol`) with the author's own harness as the subject. It is enough to establish that roster size has a
  wall-clock cost; it is not enough to size that cost generally, and no per-tool curve is given.
- **"TypeScript is an awful choice" rests on an anecdote.** The supporting evidence is that Claude produces
  better widgets for Swift/macOS than for Qt/JS. That is consistent with the ecosystem-prior argument but is not
  measured, and the author concedes prompting plays a role.
- **Whether one DOM survives contention is untested here.** The design assumes a single authoritative tree
  serving many agents in one workspace. The multiplexed-workspace test is stated as a requirement, but no
  concurrency or conflict-resolution results are reported.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Harness State Authority]]
- [[Tool Roster Economics]]
- [[Coding Agent Harness]]
- [[Harness Optimization]]
- [[Agent Plugin Architecture]]
- [[LLM-Native Extensible Software]]
- [[Agent Security and Governance]]
- [[Context Engineering]]
- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[Agent Delegation]]
- [[Agentic Loop]]
- [[Small Language Models]]
- [[Can Bölük]]

## Related pages

- [[AI Agents in Production]]
- [[Loop Engineering]]
- [[Agent Skill]]
- [[Programmatic Tool Calling]]
- [[Speculative Tool Execution]]
- [[KV Cache]]
- [[Liquid AI]]
- [[Qwen]]
- [[GitHub - How We Make AI Coding More Cost Efficient]]

## Citations

- Raw capture: [[2026-09-02 Can Bölük - The Harness Playbook]]
- Source: <https://stencil.so/blog/harness-playbook>
