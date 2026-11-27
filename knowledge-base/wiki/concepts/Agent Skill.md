---
type: concept
created: 2026-06-22
updated: 2026-11-27
tags:
  - concept
  - ai-agents
  - skills
  - orchestration
  - optimization
source_ids:
  - src-2026-06-05-pguso-agents-from-scratch
  - src-2026-06-22-djfarrelly-agent-loop-architecture
  - src-2026-06-22-alphasignal-agent-skill-optimization
  - src-2026-06-18-alyona-vert-recursive-self-improvement
  - src-2026-07-06-alphasignal-self-improving-harnesses
  - src-2026-08-05-aibuilderclub-agent-skills-best-practices-guide
  - src-2026-08-05-aibuilderclub-google-skills-official-agent-skills-library
  - src-2026-08-05-aibuilderclub-last30days-skill-real-time-research
  - src-2026-08-07-zach-lloyd-computer-use-verification
  - src-2026-08-07-mahesh-sathiamoorthy-rl-environments-agents
  - src-2026-08-17-google-cloud-agent-plugins
  - src-2026-08-21-anthropic-ai-native-sdlc
  - src-2026-08-22-grok-bot-systems-engineering-working-note
  - src-2026-07-24-ren-et-al-self-improvements-agentic-systems-survey
  - src-2026-08-30-addy-osmani-audit-agent-files
  - src-2026-09-01-iusztin-scoped-subagents
  - src-2026-10-05-faik-ai-native-software-factory
  - src-2026-10-09-dickson-agent-stack-optimization
  - src-2026-10-12-rastogi-agent-engineer
  - src-2026-10-17-bytebytego-chunking-strategies
  - src-2026-11-04-x-town-square-rebuild
  - src-2026-06-11-0xcodez-fable-5-self-improving-agents
  - src-2026-11-11-openrouter-mcp-cli-skills
  - src-2026-11-18-ioma8-llm-reverse-engineering
  - src-2026-11-19-anthropic-founders-playbook
  - src-2026-11-24-uber-agent-skill-evals
  - src-2026-11-25-frank-rousseau-agentic-coding-open-source
  - src-2026-11-23-bas-nijholt-orchestrating-orchestrators
  - src-2026-11-25-goofyfish-make-your-own-game
status: active
---

# Agent Skill

## Definition

An agent skill is a reusable capability artifact that helps an agent perform a family of tasks more reliably than a one-off prompt. The current sources use "skill" in two related but distinct ways: as a **markdown operating procedure** that shapes model behavior, and as a **durable workflow** that executes a multi-step task with retries, checkpoints, and observability.

## Why it matters

Skills are how agent capability becomes persistent infrastructure. A conversation disappears; a skill can remain callable, testable, versioned, optimized, and reused by later loops. That is why skills matter for production agents: they turn model behavior into an asset that can compound across runs, users, and model upgrades.

## Current synthesis

The vault now has three useful layers for thinking about skills:

1. **Instruction skill** — [[Alpha Signal - How your agents can write and optimize their own skills]] describes skills as standalone `.md` files: task procedures containing instructions, tool-use guidelines, output formats, and failure-recovery logic.
2. **Execution skill** — [[djfarrelly - The Agent Loop Architecture]] describes skills as durable workflows: multi-step, retryable, composable functions that can be triggered by loops or other agents.
3. **Action substrate** — [[pguso - Agents From Scratch]] provides the lower-level mechanics: structured outputs, tool request/execute separation, explicit state, plans as data, atomic actions, dependency graphs, evals, and telemetry.

The tension is that "skill" is not yet a stable industry term. One source says a skill is not a prompt; another says it is a markdown file. The most useful synthesis is to treat a production skill as having **both** a policy layer and an execution layer:

- the policy layer says what the agent should do and how it should use tools;
- the execution layer runs the procedure durably, checkpoints progress, enforces concurrency, stores run history, and handles failures.

Skill optimization is the next layer. Alpha Signal's source frames SkillOpt, GEPA, and EvoSkill as text-space optimizers for skill files:

- run tasks and record trajectories;
- score them with verifiers;
- reflect on failure patterns;
- propose bounded add/delete/replace edits;
- validate on held-out tasks;
- keep rejected-edit buffers or Pareto frontiers to avoid regressions.

This makes a skill file look like "trainable external state." It is not trained by gradients, and it does not change model weights, but it can still improve through a controlled optimization loop.

Durable orchestration makes those optimized skills operational. [[djfarrelly - The Agent Loop Architecture]] argues that a skill must survive restarts, avoid duplicate side effects, expose run history, retry only failed steps, and remain callable by scheduled or event-driven loops. Without that layer, a skill may be a useful instruction document but not dependable production infrastructure.

[[Alyona Vert - AI 101 - What is Recursive Self-Improvement]] sharpens the boundary around "self-improving" language. Optimizing a skill file is workflow-level self-improvement: the agent's procedure improves, but the model-building process has not necessarily improved. Stronger [[Recursive Self-Improvement]] would feed into future AI system creation itself, including training data, model design, evaluation, and post-training recipes.

[[Alpha Signal - Why self-improving harnesses are the next frontier]] extends this from skill
files to the harness. **Self-Harness** mines recurring failures and proposes code/prompt edits
with regression checks; the briefing reports 33–60% gains on Terminal-Bench-2.0.
**HarnessX** searches combinations of processor modules with AEGIS and reports Qwen-3.5 9B
moving from 33% to 47% on GAIA. Its reward-hacking and forgetting controls are design claims.
The newsletter attributes success to structured search and verification gates, but supplies no
ablation showing that those gates caused the gains or prevent every regression. The October 9
lint removes this page's earlier "precisely because" inference. See [[Coding Agent Harness]].

### Progressive disclosure and portability

The AI Builder Club skill cluster treats skills as context-efficient packages whose short metadata is always discoverable while full procedures load only when relevant. This progressive disclosure is the main advantage over permanently exposing every instruction or integration.

The collection also cautions against collapsing skills and MCP into one winner. Skills encode procedures and context; MCP standardizes executable tool access. A portable skill can still depend on host-specific hooks, permissions, or tool names, so portability claims need runtime tests rather than file-format compatibility alone.

### Skills need operational verifiers

[[Zach Lloyd - The computer use verification skill that every agent needs]] is a concrete procedural skill with two observable modes—reproduce and verify—and explicit evidence artifacts. [[Mahesh Sathiamoorthy - RL Environments Are All You Need]] supplies the scaling complement: reusable environments and held-out scores can evaluate or optimize skill instructions without trusting the skill's own report.

### From skill file to plugin package

[[Google Cloud - Agent Plugins Are the Future of Agent Skills]] adds a distribution layer above progressive disclosure. An Agent Plugin can bundle several `SKILL.md` procedures, MCP servers, static assets, and client-specific configuration behind one manifest. The useful distinction is:

- a **skill** is a discoverable procedure;
- an **MCP server** exposes executable capabilities;
- a **plugin** packages both for installation and transport.

The draft keeps component failure boundaries separate and distinguishes read-only packaged assets from client-managed persistent state. Portability remains incomplete because authentication and several client extension formats are not standardized; see [[Agent Plugin Architecture]].

### What a high-quality skill contains

[[Grok Bot Systems Engineering Working Note]] is the vault's most specific answer to "what makes a skill good," and it reads as an authoring checklist rather than a definition:

- a **narrow activation condition**, so the skill is not invoked everywhere;
- ordered steps with tool choices and **stop conditions**;
- positive examples demonstrating the desired artifact;
- **anti-patterns** showing common but unacceptable shortcuts;
- acceptance tests the agent can execute without subjective guessing;
- a version number, owner, and date of last verified run.

Its authoring loop — observe failures, write, evaluate, version, deploy — supplies the operational discipline the page's self-improvement section leaves open, and its triage rule is the sharpest formulation in the vault of *when* to reach for a skill at all: when a bot fails, do not add a longer conversational reminder; decide whether the failure belongs in the **skill** (method), the **environment** (access or path), the **verifier** (quality), or a **hard policy** (risk). Only the first is a skill problem. The stated goal is an accumulating operating system rather than a growing pile of prompt history. See [[Agent Workflow Maturity]].

[[Anthropic - The AI-Native SDLC Playbook]] shows the same object doing governance work in an enterprise setting: a `.claude/skills/secure-api-review/SKILL.md` encodes a compliance procedure as a versioned repository artifact, which makes the review reproducible and auditable rather than dependent on who happened to run it. Both sources converge on the same claim — **a skill's value is that it survives the run that produced it**.

## Skills as serialized self-improvement

[[Zhe Ren et al - Self-Improvements in Modern Agentic Systems]] gives a definition of a skill that
generalizes past any one vendor's format: a **named, reusable update** to the agent's own
configuration, serialized into one of its substrates — a tool and its calling convention, an
instruction or workflow, a memory entry, consolidated weights, or control logic. The substrate only
names where the update is stored; most skills in this vault are the instruction-and-tool kind.

Read that way, a skill is the persistence layer for agent learning. An agent that solves a problem
and writes down how has converted a transient in-context result into a durable artifact, which is
what the survey calls self-improvement — as opposed to the same agent solving the same problem again
next session because nothing was written back.

The survey also names **meta-level skills: skills that modify the system executing future tasks**
rather than performing a task themselves. That is a meaningful escalation, and it is where the
governance requirement bites. A skill that edits a workflow, adds a tool, or rewrites control logic
changes what all subsequent skills run inside. The governance reading drawn from the survey's
version-history formalism, that scaffold updates should be versioned, validated, and reversible, is
at its most necessary here; the survey says that history supports validation and rollback rather
than prescribing it. See [[Recursive Self-Improvement]] and [[Agent Security and Governance]].

## Do skills earn their context budget?

[[Addy Osmani - Audit your Agent files]] applies audit discipline to skills and reports results that
complicate the case for them. Across 100 repositories, **35% showed skill leakage** — skill content
bleeding into places it did not belong. More pointedly, **personalized skills performed roughly on par
with borrowed ones**, and a **generic skill built from many developers' practice was more useful than
a personalized one**. Osmani flags the caveat himself: the study used an LLM-based developer simulator
rather than real developers, so it may measure simulated preference rather than real benefit.

The budgeting detail matters for how many skills to keep. **Skill listings are budgeted at roughly 1%
of the context window by default, and only the body of an invoked skill loads.** A long skill body is
therefore cheap until called — but a proliferation of skill *names* is not free, because every name
sits in the always-loaded listing. The cost of a skill library is dominated by its breadth, not its
depth.

Combined with the finding that agent configuration **has a half-life**, the practical rule is that a
skill should be retired unless it can be justified against an eval — the same discipline
[[Harness Optimization]] applies to every other rung of the scaffolding ladder.

[[OpenRouter - MCP vs CLI vs Skills - What Each Costs in Context]] measures the read-once cost of a
skill. Wrapping the `gh` CLI with a one-line index pointing at a **1,492**-character SKILL.md raised
the task's input from **1,421** to **3,315** tokens on Sonnet 5.5 (**627** to **1,542** on GPT-6
Luna), because the file stays in the conversation once read. Both routes answered correctly, so for
this well-known CLI the skill added tokens without a correctness gain (the post credits it with "same
commands every run"). The authors' rule separates the cases: "For a CLI tool the model knows well, a
skill is optional. For your own CLI, the skill is how the model learns the commands."
That puts a measured floor under Osmani's point above: a skill's body is cheap until invoked, but once
invoked it is resident for the rest of the session. Even so, the skill route stayed far below the
**59,417** tokens of the default MCP route on the same task. It is one vendor test of one task.

## A persona is a skill file applied to the agent's identity rather than to a capability

[[Paul Iusztin - From 1 Bloated Context Window to 6 Scoped Subagents]] describes an **Agents Catalog** with exactly the shape this vault has recorded for
skills: a Markdown file with YAML front matter — name, description, tools allowlist, default permission
mode, optional allow/deny rules, and a subagent flag — with the system prompt in the body. The difference
is what it configures. A skill packages a capability; a persona packages *who the agent is* for a given
job, including what it is not allowed to do.

The operative distinction is that the **tools allowlist and the permission mode are different knobs with a
one-way dependency**: "If a tool is not present in the system prompt, the permission mode has no effect,
as that tool will never be called." Removing a tool from the roster is therefore a stronger control than
requiring approval for it.

The subagent persona shows the pattern used for restriction rather than capability. Decode's `explore` is
marked `subagent: true`, so "the only way it runs is as a child of the `agent` tool", with an allowlist of
exactly read, glob, grep and lsp. Each omission has a stated reason: no `bash` or `web_fetch` for
authority, no `ask_user` "(which would deadlock the fan-out)", and no `agent` "(to avoid recursion)".

Because the persona is static configuration rather than a caller argument, a parent cannot widen a child's
authority by rephrasing its prompt — which is what makes the fan-out in [[Agent Delegation]] auditable.

## A reusable procedure is not an enforced workflow

[[Adam Faik - How to Build an AI-Native Software Factory]] makes the instruction/execution split
operational. Repository knowledge and repeatable methods can live in skills, while workflow
blueprints put deterministic setup, checks, and submission around the steps that need an agent.
Prompts describe the procedure; code enforces required transitions and gates.

This does not argue for turning every skill into a heavy workflow. The source recommends measuring
the bottleneck and buying generic infrastructure before building repository-specific machinery.
The reusable artifact earns its place through accepted outcomes, not through how much process it
contains. The evidence is a synthesis of company reports, not a measured comparison of skill
formats or blueprint systems.

[[Anthropic - The Founder's Playbook - Building an AI-Native Startup]], an undated Anthropic
marketing guide, makes the stronger claim this section cautions against: "Skills can then codify
recurring workflows (e.g., "how I audit a commercial lease," "how I triage a patient intake form")
into reusable routines Claude runs the same way every time." The guide gives no evidence that runs
are consistent. Its examples are only named workflows, and it describes no deterministic gate around
them. Its Airtree customer story says that when one person builds a skill-based automation,
"everyone in the organization can use it". That story is also Anthropic's unverified marketing
claim. Faik's account suggests a different reading: a skill makes a procedure reusable, but
repeatability still has to be enforced or measured.

## A skill's evidence store is a different artifact from the skill

[[Ben Dickson - How AI Agents Are Learning to Optimize Their Own Stack]] adds WikiSkill
between execution traces and deployable procedures. Its wiki organizes successful and failed
experience, including rejected fixes, so later edits can use earlier experiments rather than
rediscover the same failure. The source describes the mechanism but provides no isolated
WikiSkill performance result.

This separates three artifacts: the trace is an observation, the wiki is accumulated evidence,
and the skill is a proposed operating procedure. Publishing a procedure still needs a validation
gate; storing an explanation does not establish that it is causal or generally reusable.
See [[Persistent Wiki]].

The same article qualifies the earlier harness-only account: HarnessX can also use trajectories
to train the underlying model. That is a model-harness update, not an instruction skill silently
changing weights. Start with a skill when the failure is procedural; an environment, authority,
or coordination problem may require a different intervention.

## A positive plugin result does not isolate skill quality

[[Sarthak Rastogi - Make Your Coding Assistant a 10x AI Engineer]] reports **53% versus 34%**
of requirements met across six tasks and three runs per arm, using a blinded prewritten
checklist. Its plugin combines 11 skills with four subagents and five hooks, so this is a
small creator-run bundle result, not an estimate of the effect of skill prose alone.
Only tasks 5 and 6 are explicitly held out from experiment-driven plugin changes.

The result sits alongside the vault's null and mixed context evidence rather than overturning
it. Activation discipline and artifact-level verification remain necessary: on-demand bodies
do not imply zero discovery or hook cost, and the source records a false report surviving a
corrected final response. Evaluate the installed bundle first, then ablate components before
attributing improvements to the skill library.

## A secondary explainer restates the loading sequence

[[ByteByteGo - EP229 Chunking Strategies for RAG-Based Agents]] includes a five-step Agent Skills
workflow. The runtime combines the user's query with a **skills index** — a lightweight list of
available skills and their short descriptions. The model reasons and names the skill it wants, the
runtime loads that `SKILL.md` into the active context, and the model follows it, running scripts
where the skill calls for them. This matches the progressive-disclosure account above and Osmani's
budget detail: listings are always present, bodies load on demand.

Two parts of the explainer need hedging. Its motivation, "Long prompts hurt agent performance," and
its claimed benefit, that on-demand loading keeps "the LLM's behavior consistent," are both
unquantified, so neither adds evidence to the null and mixed results recorded above. Its sequence
also makes the model's own reading of short descriptions the selection mechanism. That is exactly
where the open question about colliding activation conditions bites, and the explainer does not
discuss mis-selection or what a loaded skill's scripts are allowed to execute.

## A production repository uses skills as the update point for team workflows

[[X Engineering - Rebuilding the Global Town Square from Scratch]] reports **more than 25** skills
living next to the code of x.com's new web app: writing commits, opening and stacking pull
requests, reviewing code, shepherding a pull request through CI, changing dependencies, adding
translations, and working with Relay and the router. The stated rationale is maintenance rather than
capability: "When a workflow changes, we update its skill once, and every agent picks it up."

The skills sit in a three-part arrangement that matches the instruction/execution split above.
`AGENTS.md` carries always-on coding rules; skills carry step-by-step recurring procedures; and
anything that must hold is enforced outside the prompt by custom lint rules and commit hooks.
None of the X skills is described as a gate. The post supplies no skill-level evaluation, activation
rate, or ablation, so it is evidence that a skill library of this size is workable for a small team
(the post says five, or fewer than five, engineers built the first version), not evidence about any
individual skill's effect or about the listing-budget cost of 25-plus names.

## A skill as the write-back target of a verified loop

[[@0xCodez - Build a Self-Improving Agent System with Fable 5 in 14 Steps]] turns the survey's
"serialized self-improvement" reading above into a recipe. "STATE.md is for project memory. Skills are
for procedural memory", so "after any non-trivial failure, write the lesson into the Skill itself":
STATE.md "is project-scoped and dies with the project", while Skills "live in ~/.claude/skills/ and
travel with you". The worked example is a CI-triage skill with classification rules, a "Known failure
modes" section "added by the loop over 14 days", an anti-patterns list "added after real incidents",
and its own eval suite: run weekly against a cases file, with "Any newly-failing case → add to known
failure modes after Outcomes verifier confirms." Scheduled and GitHub-triggered Routines run the same
write-back automatically, distilling new failure modes or merged patterns into the Skill.

That gives the write-back a verifier, which the governance paragraph above asks for, but not the rest
of the contract. Nothing in the recipe keeps a held-out set apart from the cases the loop learns from,
reviews a lesson before it changes every future run, or rolls back a bad one. The course is also
inconsistent about who grades: its architecture overview says "The agent grades its own output, refines
the Skill that produced it", while a later step recommends an independent verifier sub-agent over
self-critique. Its outcome claim, "Two weeks of disciplined writing produces a Skill that materially
outperforms whatever Fable 5 would derive from scratch", has no measurement behind it, and the vault's
mixed results on whether skills earn their context budget still apply. One operational point is
specific: a Skill "should know which kinds of tasks it produces that may hit the classifier and
document the expected behavior", because a silent classifier block looks like a real error.

## Skills that encode a method for getting unstuck

[[ioma8 - LLM Assisted Reverse Engineering]] is a practitioner's account of agent-assisted reverse
engineering that rests on three skills. "What I basically do nowadays is just point the agent at the
binary to be analysed and use my set of dedicated agent skills. Rest usually takes care of itself."
One skill describes the specific disassembly tooling and the Ghidra MCP bridge, because "Without such
a skill, agents often give up too quickly getting lost". A second, his own hypothesis-debugging skill,
makes the agent write each hypothesis to a CSV table on disk, design an experiment that "will
definitively prove or disprove" it, record the result, and repeat. He calls it "crucial" because it
"Stops it going in circles". The third is Matt Pocock's public "Grill me" skill, which he invokes
with a prompt asking for up to five questions "whose answers are crucial for your further progress",
one at a time.

These are skills as procedure rather than as knowledge: a logged scientific-method loop for a stuck
agent, and a tool description without which the agent often gives up, not knowing how to do the
disassembly. That sits against the Opus-era advice recorded in [[Context Engineering]] that skills
should shrink as models improve; this author runs a cheap model, where a prescriptive skill may
still pay. The evidence is anecdotal; no runs with and without the skills are reported.

## A skill marketplace run like code: tiers, clean-room evals and ablation

[[Uber Engineering - How Uber Evals 1 Million Agent Skill Invocations a Month]] is the largest
production account of skills in the vault. Uber's marketplace grew from **1** skill in October 2025
to more than **5,000** a year later, with more than **1 million** invocations in one month. Skills
follow the staged loading described above: about **100** tokens of name and description always
loaded, a body kept under **500** lines, and scripts and references only for the step that needs
them. They graduate from Domain (one peer approval and a CI check) to Core (the platform team
reviews every change) to about **100** Always-on skills, and graduation requires evals. A CLI called
aifx installs the same skills into Claude Code, Codex, OpenCode and Uber's hosted agents, one
company's answer at the install level to the portability question below. The text itself is not
treated as portable: Uber plans to compile SKILL.md per model because "different phrasing and
lengths of SKILL.md files work better in different model families".

The evaluation design treats a skill like code with a test suite. The suggested mix is about **5%**
golden cases, **80%** real prompts graded on trajectory (the right skills and tools in the right
order), and **15%** judged by the author. Suites run in clean rooms, which exposed skills that depended
on the author's file paths, cached documents or OS tooling. Ablation replays real prompts with the
skill, without it and with parts removed, and a blind judge picks the better answer. "In a majority of
the cases, skills made the session more successful and cost less." The biggest wins came on internal
documents and warehouse queries: without the warehouse skill, sessions made **13%** more tool calls,
had **six times** as many tool errors and took **31%** longer, and the answer with the skill won
**87%** of comparisons. Uber also ablates words, because "As models get better, more words can reduce
performance".

This sits between the two earlier measurements on this page. It agrees with OpenRouter's rule that
"For your own CLI, the skill is how the model learns the commands": Uber's largest wins are on
internal systems a model cannot already know. It does not settle Osmani's finding that personalized
skills performed roughly on par with borrowed ones, because Uber compares a skill against no skill
rather than two skills against each other. Uber's evidence comes from real prompts replayed in an
isolated environment and judged blind, where Osmani's came from an LLM developer simulator, but Uber
gives no absolute success rates, no count of skills ablated and no number behind "a majority". Its
lifecycle, in which a skill lives "until a better model makes it unnecessary and it retires", turns
the half-life rule above into a stage, and its always-on log-papercut skill makes the agent using a
skill the reporter of its defects. The cost levers (a cheaper worker subagent, scripts at load time,
Code Mode) are recorded in [[Model Routing]] and [[Tool Roster Economics]], and the judging in
[[LLM-as-a-Judge]]. The account is first-party.

## Practitioners let the model write, prune, and ship skills

Three new accounts treat skills as reusable files that a repository can carry; in one of them, the
model also drafts the skills. [[Frank Rousseau - Agentic Coding on an Open-Source Project]] calls
skills "shortcuts to bigger prompts". Claude wrote his first set, and after a few weeks "the Claude
model proposed several new skills based on my prompt history", plus a command to improve existing
ones. He had Claude cut subsets from third-party packs, noting "Some third-party skills can consume
a lot of tokens", and syncs memory across machines through his own server, using a skill on each
machine.

[[Bas Nijholt - I Used to Orchestrate Agents, Now I Orchestrate Orchestrators]] reports the only
with-and-without number among the three: agents wrote a failing test before fixing a bug in **0 of
32** runs without his test-driven development skill and **32 of 32** with it. That measures whether
the procedure was followed, not code quality. [[Goofy Fish - Make Your Own Game]] ships a `/game`
command in a public repository so that any visitor's Claude Code builds and tests a game in the
site's style; the command's contents are not shown. All three are single-author or single-site
reports.

## Open questions

- Should "skill" mean the text procedure, the executable workflow, or the bundle of both?
- What governance is needed before agents can safely write, deploy, and revise their own skills?
- How should teams evaluate skill edits so they improve one task without regressing another?
- Can skill libraries become portable across models and harnesses, or will they remain tightly coupled to a specific runtime?
- When is skill optimization merely workflow tuning, and when does it become part of a broader recursive self-improvement loop?
- How many skills can coexist before narrow activation conditions start colliding and retrieval of the right skill becomes its own problem?
- Uber installs one skill into four agents but plans to compile its SKILL.md per model family. Is
  portable installation with model-specific text the stable end state, and who maintains the
  compiled variants when a model changes?

## Related pages

- [[@0xCodez - Build a Self-Improving Agent System with Fable 5 in 14 Steps]]
- [[@0xCodez]]
- [[Continual Learning for Agents]]
- [[X Engineering - Rebuilding the Global Town Square from Scratch]]
- [[ByteByteGo - EP229 Chunking Strategies for RAG-Based Agents]]
- [[ByteByteGo]]
- [[Sarthak Rastogi - Make Your Coding Assistant a 10x AI Engineer]]
- [[agent-engineer]]
- [[Ben Dickson - How AI Agents Are Learning to Optimize Their Own Stack]]
- [[Persistent Wiki]]
- [[Adam Faik - How to Build an AI-Native Software Factory]]
- [[Zhe Ren et al - Self-Improvements in Modern Agentic Systems]]
- [[Grok Bot Systems Engineering Working Note]]
- [[Anthropic - The AI-Native SDLC Playbook]]
- [[Agent Workflow Maturity]]
- [[AI-Native Software Development Lifecycle]]
- [[Agentic Loop]]
- [[AI Agents in Production]]
- [[Agent Planning]]
- [[Context Engineering]]
- [[Tool Use and Function Calling]]
- [[Agent Memory]]
- [[djfarrelly - The Agent Loop Architecture]]
- [[Alpha Signal - How your agents can write and optimize their own skills]]
- [[Recursive Self-Improvement]]
- [[Alyona Vert - AI 101 - What is Recursive Self-Improvement]]
- [[pguso - Agents From Scratch]]
- [[Coding Agent Harness]]
- [[Alpha Signal - Why self-improving harnesses are the next frontier]]
- [[Inngest]]
- [[AI Builder Club - Build AI Agents]]
- [[Loop Engineering]]
- [[Agent Security and Governance]]
- [[Zach Lloyd - The computer use verification skill that every agent needs]]
- [[Mahesh Sathiamoorthy - RL Environments Are All You Need]]
- [[Google Cloud - Agent Plugins Are the Future of Agent Skills]]
- [[Agent Plugin Architecture]]
- [[Addy Osmani]]
- [[Harness Optimization]]
- [[Addy Osmani - Audit your Agent files]]
- [[Paul Iusztin - From 1 Bloated Context Window to 6 Scoped Subagents]]
- [[Paul Iusztin]]
- [[Agent Delegation]]
- [[OpenRouter - MCP vs CLI vs Skills - What Each Costs in Context]]
- [[ioma8 - LLM Assisted Reverse Engineering]]
- [[Anthropic - The Founder's Playbook - Building an AI-Native Startup]]
- [[Uber Engineering - How Uber Evals 1 Million Agent Skill Invocations a Month]]
- [[Uber]]
- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[Agent Observability]]
- [[Model Routing]]
- [[Tool Roster Economics]]
- [[Frank Rousseau - Agentic Coding on an Open-Source Project]]
- [[Bas Nijholt - I Used to Orchestrate Agents, Now I Orchestrate Orchestrators]]
- [[Goofy Fish - Make Your Own Game]]
