---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-25-frank-rousseau-agentic-coding-open-source
source_title: Agentic coding on an open-source project
source_author: Frank Rousseau
source_url: https://blog.frankrousseau.fr/agentic-coding-on-an-open-source-project/
tags:
  - source/summary
  - coding-agents
  - open-source
  - developer-workflow
  - code-review
source_ids:
  - src-2026-11-25-frank-rousseau-agentic-coding-open-source
status: active
---

# Agentic Coding on an Open-Source Project

## Summary

Frank Rousseau, a software engineer and entrepreneur with 20 years of experience, reports ten months
of intensive Claude Code use on Kitsu, CGWire's open-source production-tracking software, kept by a
team of 5 (about 20k daily users; deployed in 400 companies). His setting is a fixed budget: **$600
a month** for 3 Claude Ultra subscriptions, about **70B tokens** over 10 months, and roughly **$2k**
spent where he estimates API prices at about **$30k**. The post is a practitioner's account of what
worked within that budget. He favours short prompts with many iterations, separate sessions per
subject, quality-assurance passes the agent mostly self-checks against tests, scripts rather than
direct data access, and an explicit risk-tiered review policy. He is cautious about long unattended
orchestration. It ends with a long list of unresolved concerns, from resource use and hidden labour
to "brain fry", and recommends "not pushing anyone to use LLMs". Every result is self-reported and
unmeasured beyond counts of work done.

## Key claims

### What a small team did within a subscription

Since January he lists a Vue.js migration of **300 components** to the composition API, **6500**
frontend tests, high backend test coverage, a security hardening pass, an MCP server, a new Tauri
desktop app, a JavaScript API client, and 70 open issues handled, with no more than 10 open since.
He resolved **50** old GitHub issues "in a few days". As a side project he built Servant, a personal
cloud. Kitsu is split into a frontend repository (Kitsu) and an API repository (Zou).

### Prompting and context: short, iterative, one subject per session

He never writes long specifications. He starts with a short prompt, is "a bit evasive" so that the
model can be creative, and iterates. Each surprise is saved "in memory or in the Claude.md file", so
precision accumulates over time. He keeps a polite, interrogative tone, asks for concise output, and
uses the ASD-STE100 convention and the I-have-adhd skill for readability. For context, he keeps one
theme per terminal session and compacts or resets so as to avoid "going beyond 50% of context usage"
because large contexts bring "a lot of noise to every request". The claude-carbon skill shows
context size, API-cost equivalent, and emitted carbon; RTK strips unused characters from tool
output.

### Quality assurance is where agents shine

"QA is where LLMs shine the most." He segments the project into separate sessions, because "If too
much data is involved, the model gets confused". QA changes are too many to review: "I just let the
tests pass and accepted them", with product testing before release and occasional spot reads. Loops
run module-by-module debugging, legacy issue batches with one pull request each, and performance
work. A security audit found many issues but "still missed some security flaws"; outside researchers
later sent three pieces of "silent feedback" pointing out security holes that the audits missed. His
recurring routine is a full audit on **8 aspects** (architecture, bugs, security, cleanliness, test
coverage, performance, documentation, dependencies) that yields a to-do list, which he prunes and
then runs as a loop that commits each improvement. He repeats it "whenever a new model comes out",
using two skills: one for audits, one for to-do lists.

### Scripts as contracts, and knowing when to stop

For data migration he always asks for a script rather than letting the model touch data sources:
"I consider scripts as contracts." Models "spontaneously add a dry-run mode". He fights
over-engineering and yak shaving by asking for the shortest solution and by using the Ponytail skill.
He stopped having the model write specs and plans before coding, because they were too verbose and
"created more noise than it helped". He prefers short Markdown documents to HTML explainers.

### Skills, memory, and harness independence

Skills are "shortcuts to bigger prompts". Claude wrote his first set. After a few weeks it "proposed
several new skills based on my prompt history" and a command to improve existing skills. He tried
Superpowers, Caveman, Ponytail, Matt Pocock's skills, I have ADHD, and ui-ux-pro-max, but had Claude
cut subsets from them, noting "Some third-party skills can consume a lot of tokens". Because memory
and skills did not sync between his desktop and laptop, and he did not want Claude's own service, he
added an agent-memory app to Servant. A dedicated skill on each machine syncs with his server, so
memory stays consistent "while ... remaining agnostic about the harness I use".

### Review policy by risk

Agent review is "pretty noisy, with a lot of nitpicking", and he still finds cohesion problems by
hand. He also reports that providers silently serve a model that "behaves differently". His policy:

- Merge very light pull requests that pass CI.
- Do not review cleanup passes; CI runs and the product manager tests before release.
- Run an agent review for everything else.
- Review critical code himself.
- For external contributions, run the model review privately and post only a trimmed result he
  validated.

He asks whether it is "still worth reviewing anything manually" and notes that projects with many
contributions probably need full automation.

### Orchestration: one costly experiment

He mostly lets Claude spawn agents as needed and opens parallel sessions. One experiment ran five
agents through a single Claude session, with tasks assigned in Kitsu and their specs, plans, code,
tests, time, and tokens recorded there. It was interesting but "quickly consumed my weekly
allocation". He names Hermes Kanban, Cline Kanban, and Gas Town as popular organizers. He calls
OpenBlob, a declarative team-of-agents format with sandboxed WebAssembly tools, "On paper, the
architecture is the most solid". Long unattended runs do not "feel natural" to someone who iterates.

### Contributions changed

Average contribution quality is "much higher", beginners now contribute, and security researchers
are more active. A new plugin system let studios build and share plugins, and other studios shared
software integrations they built with LLMs. The drawback is that contributors now propose changes to
core components. Studios want more plugin customization, while Kitsu's philosophy is a common UI
across studios: "We haven't arbitrated on the topic yet."

### Next steps and concerns

He wants to explore Anthropic's "Dreaming agents" ("permanent agents iterating and learning on a
specific task"), local AI, building his own harness, agent teams, team sharing, and reactive agents
that triage events. His concerns cover resource consumption, hidden data-labelling labour,
privatized commons, cloud and model dependency, token price ($30k at API prices "versus less than
$2000"), the loss of minimalism, "Project overload" (citing an essay titled "The Decoherence Trap"),
the end of craftsmanship, "brain fry", and FOMO. He wrote the article himself, using Grammarly and
feedback from Claude Opus 5.5 and Fable 5.2.

## Why it matters

- [[AI-Native Software Development Lifecycle]]: a written, risk-tiered review policy and a
  contribution flow from a small open-source maintainer, set against heavier spec-first processes.
- [[Context Engineering]]: a concrete practitioner budget rule (under 50% of the window, one subject
  per session).
- [[Loop Engineering]] and [[Continual Learning for Agents]]: an audit, to-do, loop routine re-run
  per model release, and skills the model proposed from prompt history.
- [[Agent Memory]]: memory synced across devices and kept independent of the harness.
- [[Agent Delegation]] and [[Agent Workflow Maturity]]: a capable user who deliberately does not
  run long multi-agent orchestration, and why.
- [[Agent Plugin Architecture]] and [[Coding Agent Harness]]: plugin ecosystems under LLM-built
  extensions, and the subscription-versus-API cost gap.
- Proposed for [[Agent Skill]], [[AI Code Review]], and [[LLM-Native Extensible Software]].

## Tensions / open questions

- Everything is self-reported by one maintainer on one product; no defect rate, review accuracy, or
  before/after quality measure is given.
- The cost figures are inconsistent in kind: "Around $2k" in the achievements list and "less than
  $2000" under token price, both against about **$30k** at API prices. The $30k is his estimate.
- Accepting QA changes once tests pass relies on test quality, yet the same post reports that audits
  missed security holes found later by outside researchers.
- His claim that providers silently change served models is an observation, not documented.
- He stopped writing specs and plans, while other practitioners in the vault rely on them.
- The "Decoherence Trap" link points to a breck-mckye.com post whose URL slug reads "software is
  breaking down at a systemic level", not to the maevyn.codes capture summarized in
  [[The Decoherence Trap]]. Whether the two are the same essay is unverified.
- "Dreaming agents" is a link to Anthropic documentation, not something he has tried.

## Affected pages

- [[Agent Memory]]
- [[Agent Delegation]]
- [[Agent Workflow Maturity]]
- [[Context Engineering]]
- [[Coding Agent Harness]]
- [[Loop Engineering]]
- [[Continual Learning for Agents]]
- [[Agent Plugin Architecture]]
- [[AI-Native Software Development Lifecycle]]
- [[Agent Skill]]
- [[AI Code Review]]
- [[LLM-Native Extensible Software]]

## Raw capture

- [[knowledge-base/raw/sources/Agentic coding on an open-source project]]

## Citations

- Canonical URL: https://blog.frankrousseau.fr/agentic-coding-on-an-open-source-project/
- Byline: Frank Rousseau (personal blog).
- Published: 2026-11-25. Captured: 2026-11-26 (newsletter-tracked URL; tracking parameter removed).

## Related pages

- [[Agent Memory]]
- [[Agent Delegation]]
- [[Agent Workflow Maturity]]
- [[Context Engineering]]
- [[Coding Agent Harness]]
- [[Loop Engineering]]
- [[Continual Learning for Agents]]
- [[Agent Plugin Architecture]]
- [[AI-Native Software Development Lifecycle]]
- [[Agent Skill]]
- [[AI Code Review]]
- [[LLM-Native Extensible Software]]
- [[The Decoherence Trap]]
- [[Anthropic]]
- [[Bas Nijholt - I Used to Orchestrate Agents, Now I Orchestrate Orchestrators]]
- [[William Hu - Building Always-On Agents]]
