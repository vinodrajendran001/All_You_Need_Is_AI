---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-24-uber-agent-skill-evals
source_title: How Uber Evals 1 Million Agent Skill Invocations a Month
source_author: Uber Engineering (@UberEng); byline @Mager, @JasonVarbedian, and @udaykiran
source_url: https://x.com/UberEng/status/2125008806249930999
tags:
  - source/summary
  - ai-agents
  - skills
  - evaluation
  - observability
source_ids:
  - src-2026-11-24-uber-agent-skill-evals
status: active
---

# How Uber Evals 1 Million Agent Skill Invocations a Month

## Summary

Uber Engineering describes how it runs a company-wide marketplace of agent skills, Markdown files
that each teach an agent one job. The marketplace grew from **1** skill in October 2025 to more than
**5,000** a year later, and agents invoked skills more than **1 million** times in one month. The
post covers the systems around it: tiered review, one install path for every agent (a CLI called
aifx), telemetry hooks, an authoring tool called Skill Workshop that compiles skills from a spec,
an eval mix graded on trajectories, and ablations judged blind. It also describes a loop in which
agents file their own bug reports ("papercuts"). The transferable claims are that a skill should be
measured, made cheaper and retired like code, and that the agent using a skill is a useful sensor
for its defects. The report is first-party and gives few absolute numbers.

## Key claims

### Skills load in three stages and graduate through three tiers

- Following the Agent Skills specification, a skill's name and description (about **100** tokens)
  are always loaded, the body (kept under **500** lines) loads when the skill runs, and scripts and
  references load only for the step that needs them.
- All skills live in one Git repository. **Domain** areas publish after one peer approval and a CI
  check; **Core** skills are team-maintained and the platform team reviews every change; about
  **100** **Always-on** skills cover pull requests, code review, tool access, data analysis and chat.
  Graduating a skill requires the eval system plus quality and usefulness checks.
- aifx installs the same skills into Claude Code, Codex, OpenCode and Uber's hosted agents (the
  TL;DR also lists SpaceXSI Cursor). It installs skill groups as plugins, manages personas, and
  merges **six** configuration layers, from company defaults to a local override, where later layers
  add plugins and never remove them.
- Discovery uses a find-skills skill, a skill quality score ranked on evals and run counts, and a
  context graph that answers "Give me the skills my peers are using that I'm not."

### Telemetry and authoring

- OpenTelemetry hooks record each skill call, its version, and whether the agent chose it or the
  user typed its command. Events carry no prompt text and no file contents. Uber computes **12**
  measures per skill, among them users, retention, cost, latency and errors.
- Skill Workshop gives each skill a lifecycle: it is written, tested, shipped and improved from real
  runs "until a better model makes it unnecessary and it retires". Authors write a spec first (goal,
  outputs, required or forbidden tool
  actions, target agents and models), and the tool compiles SKILL.md and test prompts from it,
  recompiling when a model or agent changes.
- A linter enforces numbered steps with one objective each and some soft verification, a concrete
  command whose result is checked before the next step, and an error-recovery table in which "Try
  again" doesn't count.

### The eval mix, and why a perfect pass rate is suspect

- The suggested suite is about **5%** golden cases (fixed input, expected output, tool mocks),
  **80%** real prompts graded on trajectory, and **15%** judged by the author. Trajectory grading asks
  whether the agent used the right skills and tools in the right order, not whether the outcome was
  right.
- Evals run in three clean rooms: Minion (background agents), AES (a managed agent sandbox) and
  devpods. Remote runs exposed skills that depended on the author's file paths, cached documents or
  OS tooling.
- "evals that pass 70%-90% of runs can be more useful than those that pass 100%", because answers and
  judges vary and a perfect pass rate may mean the eval misses meaningful changes.
- "LLM-as-judge works best if it has a human-annotated set", which authors must create, collect and
  grade repeatedly.

### Ablation shows skills mostly help, and words can hurt

- Real prompts are replayed with the skill, without it, and with parts removed, and a blind judge
  picks the better answer. Figure 13 plots win shares with 95% intervals against a noise band (how
  much two identical runs differ); its values are not in the prose.
- "In a majority of the cases, skills made the session more successful and cost less." The biggest
  wins came from internal documents and warehouse queries. Without the warehouse skill, sessions
  made **13%** more tool calls, had **six times** as many tool errors and took **31%** longer; the
  answer with the skill won **87%** of comparisons.
- "As models get better, more words can reduce performance", so ablation also removes words.

### Cost per invocation and the levers that cut it

- Cost per invocation is the last running session total before the call subtracted from the first
  total after it, summed per skill per day and divided by the number of calls. The window includes
  the turns that follow and any other tool calls in it.
- A worker subagent on a cheaper model cut a tracing skill's cost per invocation by **46%**; a
  deployment skill showed no drop in its first week. Running a script at load time took one search
  skill from four turns to three and cut mean cost by **32%**. In the **20** highest-spend sessions,
  notification turns were about a third of spend, so pull-request polling moved to a background agent
  on a cheaper model.
- Code Mode, inspired by Cloudflare's, moved repeated flows into scripts that call tools through
  Uber's gateway. A default MCP install with more than **100** tools loaded **50,000 to 70,000** tokens
  of definitions before the user typed. Uber says the scripts improved success rate, latency and cost
  but gives no figures, and Figure 14's token counts are its estimates. Uber also blocks `.mcp.json`
  files in skills and plugins.

### Agents file their own bugs

- An always-on log-papercut skill lets any agent report friction: what it tried, expected and saw,
  and what would fix it. Agents filed thousands of papercuts in three months, and hundreds have been
  fixed. Each one is grouped, triaged, root-caused, fixed, evaluated and approved, then measured for
  regressions; a person acts at two steps.
- Examples include a shared temp file that let concurrent sessions change each other's pull requests,
  epoch seconds passed where an API expected milliseconds, a lookup that silently returned a
  different property, and a skill that waited on CI in a repository with none, repeating a 404.
- Human signals feed the same loop: in Fawkes, Uber's maintenance factory, comments, iterations and
  rejected pull requests improve the skill, and blocked pull requests join the eval set.

### Open problem and next steps

The stated open problem is evaluating workflows that "run rarely, matter a lot, and are hard to
judge." Planned work includes A/B testing and canaries for skills, compiling skills per model because
"different phrasing and lengths of SKILL.md files work better in different model families", trace
indexing, skill recommendations, and a task router.

## Why it matters

This is the vault's largest production account of the [[Agent Skill]] lifecycle. It sets
[[LLM-as-a-Judge]], trajectory grading from [[Multi-Turn Evaluation]], and telemetry from
[[Agent Observability]] against a skill catalog. On cost it adds a per-invocation measure that bears on
[[Tool Roster Economics]], [[Programmatic Tool Calling]] and [[Model Context Protocol]] residency, and
cheaper worker models that bear on [[Model Routing]]. Per-model skill compiling is the
[[Harness Optimization]] question asked one level down. It also extends [[Uber]] beyond the
ByteByteGo gateway account, and it bears on [[Agentic Testing]], [[Agent Security and Governance]],
[[Coding Agent Harness]] and [[Agent Plugin Architecture]].

## Tensions / open questions

- First-party report with no absolute success rates, no count of skills ablated, and no
  quantification of "a majority of the cases". Figure values (win shares, noise bands, token
  estimates) are not in the prose and are not reported here.
- The cost window includes any other tool calls between the two snapshots, so a per-invocation figure
  is an attribution, not an isolated cost.
- Code Mode's improvements are stated without numbers. That matches the earlier relayed account in
  [[ByteByteGo - How Uber Built a Gateway for AI Agents to Access Tools]], which also gave no measured
  savings.
- The 70%-90% pass-rate guidance is experience, not a measured rule, and the post does not say how
  the noise band is used to accept a change.
- Telemetry excludes prompt text, yet trajectory evals and trace indexing need session content; the
  post does not say how the two are reconciled.

## Affected pages

- [[Agent Skill]]
- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[Agent Observability]]
- [[Tool Roster Economics]]
- [[Programmatic Tool Calling]]
- [[Model Context Protocol]]
- [[Model Routing]]
- [[Harness Optimization]]
- [[Uber]]
- [[Agentic Testing]]
- [[Agent Security and Governance]]
- [[Coding Agent Harness]]
- [[Agent Plugin Architecture]]

## Raw capture

- [[knowledge-base/raw/sources/How Uber Evals 1 Million Agent Skill Invocations a Month]]

## Citations

- Canonical URL: <https://x.com/UberEng/status/2125008806249930999> (newsletter tracking parameters
  removed).
- X article published by @UberEng (Uber Engineering) on November 24, 2026, with the byline "By:
  @Mager, @JasonVarbedian, @udaykiran"; captured November 25, 2026.
- Reference [1] is a Shyam Sankar interview with Ben Thompson on Stratechery, October 29, 2026, the
  source of the "atomic unit of the enterprise is the workflow" quotation.

## Related pages

- [[Agent Skill]]
- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[Agent Observability]]
- [[Tool Roster Economics]]
- [[Programmatic Tool Calling]]
- [[Model Context Protocol]]
- [[Model Routing]]
- [[Harness Optimization]]
- [[Uber]]
- [[Agentic Testing]]
- [[Agent Security and Governance]]
- [[Coding Agent Harness]]
- [[Agent Plugin Architecture]]
- [[Cloudflare]]
- [[ByteByteGo - How Uber Built a Gateway for AI Agents to Access Tools]]
- [[OpenRouter - MCP vs CLI vs Skills - What Each Costs in Context]]
- [[Addy Osmani - Audit your Agent files]]
- [[Lance Martin - Automating Eval Design and Hillclimbing with Claude]]
- [[Casey West - Four Evaluation Engineering Lessons from Building Agent Plugins]]
- [[Philipp Schmid - Why Agents Are Soon Only Going to Have 1 Tool]]
- [[Hugging Face - Introducing Harness Adapters]]
- [[Niccolò Zanichelli - Swarms Do Not Yet Raise the Roof]]
