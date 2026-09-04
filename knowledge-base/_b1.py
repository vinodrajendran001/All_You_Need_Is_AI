import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _integrate import integrate

HP = "src-2026-09-02-can-boluk-harness-playbook"
GH = "src-2026-09-03-github-ai-coding-cost-efficient"

integrate(
    "Coding Agent Harness", [HP, GH],
    "The harness as a game engine, and what that exposes",
    """
[[Can Bölük - The Harness Playbook]] argues the closest existing analogue to a coding agent harness is not an
IDE or a chat application but a **game engine**: a long-lived simulation with an authoritative state, a tick
loop, entities that come and go, clients that watch, and a scripting layer that third parties extend. The
argument is not aesthetic. It says that durability, replication, spectating, configuration, and hot-reload are
solved problems in that lineage, and harnesses are currently re-deriving them one feature at a time.

The design method offered with it is a **design envelope**: rather than enumerate features, state four
architecture tests the system must satisfy, and let the requirements fall out. A multiplexed workspace (many
agents, one repository). A remote driver (drive a session from a machine that is not the one running it). A
spectator (watch a session, including a subagent, without perturbing it). And a Factorio test — could the harness
host a long-running simulation with entities, saves, and mods. Each is a plausible product feature; jointly they
force one authoritative session, a trusted control plane, bounded work, explicit compatibility, and views that
are projections rather than state.

The measured cost of getting the state model wrong is in [[Harness State Authority]]: of **78 official Pi
extension examples, 60 were stateless, and of the 17 with state only two were correct**. The measured cost of an
unbounded tool roster is in [[Tool Roster Economics]]: **36.6s for five essential tools against 42.2s** for a
full-roster harness on the same task.

[[GitHub - How We Make AI Coding More Cost Efficient]] supplies the empirical counterweight from a shipped
product, and its most transferable result is a warning about generalising harness findings at all: a file-tool
change that reduced cost in the code-review agent **increased** cost in the CLI agent. The same tools, the same
change, opposite signs. Harness design evidence is local to the workload, which is why this page's accumulated
prescriptions should be read as hypotheses to re-measure rather than as settings to copy.
""",
    ["Harness State Authority", "Tool Roster Economics", "Can Bölük - The Harness Playbook",
     "GitHub - How We Make AI Coding More Cost Efficient", "Can Bölük", "GitHub"],
)

integrate(
    "Harness Optimization", [HP, GH],
    "Four measured reductions, and the trap underneath them",
    """
[[GitHub - How We Make AI Coding More Cost Efficient]] is this page's first source reporting **A/B results from
production rather than design reasoning**. Four changes, each measured against an internal AI-credit cost metric:
removing `view` line-number prefixes (**3.1%**), selective output compaction (**5.5%**), a shortened task-tool
prompt (**2.9%**), and batching notification roundtrips (**2.3%**). The source states plainly that these are
**not additive** — a caveat that tends to be lost the moment the numbers travel.

Three findings matter more than the percentages.

**The local metric trap.** An aggressive output compressor reduced per-response tokens and increased total cost,
because agents reopened files and re-ran commands to recover what was removed: *"We saved tokens locally and
spent more globally."* Optimising a component metric is not the same as optimising the loop. The useful
corollary is that **the recovery path doubles as an evaluation signal** — if the agent re-reads what you
compressed, the compression was wrong, and no human judgement is needed to see it.

**Shortening a prompt can silently delete a behaviour.** A meta-prompting loop halved a task-tool prompt and, in
the process, rewrote cautious parallelism guidance into a hard scheduling policy that serialised independent
agents. Offline evaluation did not catch it; production did. The fix was one restored sentence. The stated
lesson: *"Prompt behavior needs tests. If a behavior is not tested, a shorter prompt can remove it without anyone
noticing."*

**Some overhead is archaeology.** The `view` line-number prefixes existed to serve an edit tool that had stopped
needing them. Nobody had removed them. Worth ~5% offline and ~3% online per user.

[[Can Bölük - The Harness Playbook]] adds two optimisation results from the other end of the stack. A terminal
render path measured at **267 seconds was reduced to 90ms**, with **98.7s of the original spent in `wrapAnsi`**
alone — and the profile contained an internal contradiction the author flags himself, since an image-line
`.includes` check accounted for 13% of one panel and 20% of prose rendering in a session that contained **zero
images**. And **compaction should be scheduled, not triggered**: firing at the context limit blocks the user at
the least convenient moment, so fire roughly 10% early, branch, and splice, rather than treating compaction as an
exception handler. His remark that *"even the frontier lab ships the naive design"* is a reminder that
prevalence is not validation.

The overall boundary of this practice is best stated by GitHub: *"None of these changes made the model smarter.
They removed work the model never needed to do."*
""",
    ["Tool Roster Economics", "Harness State Authority", "GitHub - How We Make AI Coding More Cost Efficient",
     "Can Bölük - The Harness Playbook", "GitHub", "Can Bölük"],
)

integrate(
    "Context Engineering", [HP, GH, "src-2026-09-02-meta-organizational-second-brain"],
    "Three 2026 results: scheduling, measurement, and disclosure",
    """
Three sources ingested together sharpen this page in different directions.

**Compaction is a scheduling problem, not an exception handler.** [[Can Bölük - The Harness Playbook]] argues
that firing compaction when the context window fills guarantees it fires at the worst moment — mid-task, with the
user waiting. The alternative is to schedule it roughly 10% before the limit, branch the session, and splice the
compacted result in. Related designs he catalogues: **remote compaction**, where a provider compacts server-side
with access to decrypted thinking that the client can never see (and returns an opaque blob), and **handoff**,
where the summary is written for a fresh session rather than for continuation. The same source warns that
**truncation must be opt-out, not opt-in** — an opt-in flag guarantees uneven coverage, and he found truncation
layers stacking N+1 deep inside a single evaluation path.

**Token savings must be measured on the loop, not the component.** [[GitHub - How We Make AI Coding More Cost
Efficient]] shipped an aggressive output compressor that reduced per-response tokens and raised total cost,
because agents re-read what had been removed. The compressor that shipped is deliberately conservative: preserve
source-like output (`cat`, `git diff`, `git show`), reorganise search results losslessly, and compress repetitive
build and install noise only when the savings are substantial. The framing is worth keeping: it is
*"conservative not because the goal was to build a conservative compressor, but because that is what the
evaluations supported."*

**Progressive disclosure has a reported magnitude.** [[Meta - An Organizational Second Brain]] reports roughly
**80% fewer tokens per turn** from routing an agent through gateway files and deterministic routing indexes
rather than loading a fixed context — the largest context reduction figure in this vault, though unattributed
across several simultaneous changes.

Together these push the page's centre of gravity from *what to put in the window* toward *when to change it, and
how to know the change helped*.
""",
    ["Tool Roster Economics", "Harness State Authority", "Institutional Knowledge Agents",
     "Can Bölük - The Harness Playbook", "GitHub - How We Make AI Coding More Cost Efficient",
     "Meta - An Organizational Second Brain"],
)

integrate(
    "Tool Use and Function Calling", [HP],
    "Schemas are model-facing protocols, and the roster is not free",
    """
[[Can Bölük - The Harness Playbook]] treats a tool schema as **a protocol spoken to a model**, not as a contract
the model can be expected to honour. Different families deviate in family-specific, reproducible ways: one emits
a `Grep` tool that does not exist in the roster at all; another sends an array parameter as a delimited string.
Rejecting these costs a turn, so the position taken is that a harness should **validate and correct** recoverable
deviations rather than fail them.

**Forcing a tool call is a three-tier decision.** Always add the soft prompt, because inference servers apply
hard grammar constraints that the caller never opted into and may not know about. Set the provider's native
forcing flag only when it is free — one major provider's implementation causes a conversation-wide cache miss.
And escalate when the model does not comply, on the principle that *"correctness wins over the cache once
persuasion has failed."*

**The roster itself has a price.** Measured wall clock on one task, median of six fresh sessions: **36.6s with
five essential tools, 37.0s and 42.2s for two full-roster harnesses.** The mechanism named is constrained
decoding — every schema joins the grammar the sampler must satisfy — so the cost is not only description tokens
in the prompt. That gives this page's schema-versus-code contrast a decision rule: **bounded operation set,
schema; open-ended operation set, code surface.** See [[Tool Roster Economics]].
""",
    ["Tool Roster Economics", "Harness State Authority", "Can Bölük - The Harness Playbook", "Can Bölük"],
)

integrate(
    "Model Context Protocol", [HP],
    "Residency, not the protocol, is the cost",
    """
[[Can Bölük - The Harness Playbook]] supplies the missing cost side of MCP adoption. Every connected server's
tools land in the model's roster, and roster size is measurable in wall clock: **36.6s for five essential tools
against 42.2s** for a full-roster harness on the same task, with constrained decoding — not just description
tokens — named as the mechanism.

The design response is not to abandon the protocol but to change what stays resident. The rule offered is
**"bounded operation set: schema; open-ended operation set: code surface"**, with the concrete proposal being a
single discoverable CLI behind the Bash tool (a `dyn` command) so an integration exposes **zero** additional
tools and its surface is discovered on demand. MCP's value as a shared integration standard is untouched by
this; what is being questioned is the default of mounting every capability as a permanently visible tool.

See [[Tool Roster Economics]] for the full argument and the counter-consideration — that a discoverable CLI
still costs turns to discover, which nobody has measured.
""",
    ["Tool Roster Economics", "Can Bölük - The Harness Playbook", "Can Bölük"],
)
