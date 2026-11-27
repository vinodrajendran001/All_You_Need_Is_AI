---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-23-tomassetti-legacy-modernization-measured
source_title: "Legacy Modernization with LLMs, measured"
source_author: Federico Tomassetti
source_url: https://tomassetti.me/legacy-modernization-llms-measured/
tags:
  - source/summary
  - legacy-modernization
  - coding-agents
  - testing
  - cost
source_ids:
  - src-2026-11-23-tomassetti-legacy-modernization-measured
status: active
---

# Legacy Modernization with LLMs, Measured

## Summary

Federico Tomassetti, who founded the language-engineering and migration company Strumenta, reports a
deliberately naive experiment: Claude Opus 5.5, running headless in Claude Code, translated two real
IBM i ERP applications from RPG to Java. The larger one, about **552,000** lines in its migration plan,
cost about **$1,100** at API-equivalent prices for a first generation, produced about **1,053,000**
lines of Java across **49** sessions, and compiled. Repeated translations of the same code produced
different architectures and, off the normal path, different behaviour, and looking at about a tenth
of the programs found non-cosmetic errors in every translation examined. The article is the first of
a five-part series; it states the setup, costs, and short answers, while the supporting examples live
in articles 2-5, which were not captured. Its durable contribution is a measured separation between
the cheap part of a migration, a first runnable translation, and the unmeasured expensive part,
establishing that the result does what the original does.

## Key claims

### Real ERP code, a naive prompt, and no running original

- **Small** is the production-planning part of a furniture-manufacturing ERP: about **15,100** lines
  of RPG plus **208** DDS files and **4** CL programs. **Large** is a broader clothing manufacturing and
  retail ERP: about **552,000** lines in the migration plan plus about **51,000** lines of queries and
  CL. The author stresses that these are real systems that evolved over decades, not demos.
- Experiment 1 translated five programs of Large (runs 1A-1C), experiment 2 the whole of Small (2A-2C,
  one prompt per isolated run), and experiment 3 the whole of Large once, in **49** sessions. No run saw
  another run's output. Large was run once because of its token cost.
- The harness was Claude Code in an isolated Docker container with default effort and outgoing network
  requests logged through a proxy. The full prompt for Small asks the agent to translate the whole
  application into Java and organize the project "as you see fit, ensuring the result can be run."
- Large did not plan itself. Strumenta's deterministic tooling parsed the code and dependency-ordered
  the plan's **2,777** files; a script split it into **43** phases about the size of Small, plus two
  query phases and four for CL programs, commands, and menus. The agent also found an SQL table
  dependency the plan had missed.
- **There was no IBM i to run the originals.** Expected behaviour came from reading the source and the
  RPG manual. Experiment 1 was executed against **35** predefined test cases, adapted to each run's
  different interfaces; for Small the team mostly reviewed the **14** largest programs against the RPG;
  checks of Large used Claude Opus 5.5, Fable 5.2, and GPT-6 Astra alongside manual exploration.

### A cheap first generation, with large stated exclusions

| Run | Wall clock | API-equivalent cost | Java produced |
| --- | --- | --- | --- |
| 1A / 1B / 1C | 8.3 / 6.3 / 8.5 min | $1.97 / $1.67 / $2.07 | 1,459 / 1,275 / 1,749 lines |
| 2A / 2B / 2C | 56 / 63 / 67 min | $25.58 / $23.57 / $23.20 | 14,500 / 26,300 / 22,900 lines |
| Large, 49 phases | 48.1 h (39.7 h API time) | $1,101.95 | 5,737 files, about 1,053,000 lines |

- The same prompt produced 14,500 lines once and 26,300 another time for about the same money, and the
  run that wrote least cost most: it read more source early and "carried a larger context afterwards".
  Small's largest context was about **720k** tokens and most tokens were cache reads, so early reading
  is paid for at every later step. Large used **11.8M** output tokens and **3.14B** cache-read tokens.
- Every Large phase "completed" on its first attempt, meaning the session finished and the project
  compiles, not that every statement was translated, or translated correctly. Phases cost **$1.22** to
  **$37.73** and did not grow steadily more expensive as the Java project grew.
- Per 1,000 source lines: about **$1.60** for Small and **$1.80** (later **$1.83**, on roughly **603,000**
  lines including queries and CL) for Large, rounded to "roughly $2". Large was about 35 times Small's
  size and cost about 45 times as much, a rough comparison over different source mixes.
- The dollars are November 2026 API list prices reported by Claude Code; the team actually spent Claude
  subscription quota, about **113%** of a Max plan's weekly quota, over eight calendar days that include
  more than four days waiting for a quota reset.
- **Exclusions.** Writing test scenarios for the five experiment-1 programs cost claude-fable-5-1
  **$7.56**, about four times their translation. Planning, harness work, reviews, correction cycles,
  and human time are excluded. An illustrative extrapolation, explicitly "not measured migrations",
  gives **$12,000** for 1 million lines and **$120,000** for 10 million, assuming test generation costs
  five times the translation, a multiplier the author calls "a hypothesis, not a rate we measured".

### Repeated translations are different programs

- **RQ1a.** Runs preserve recognizable logic but differ in packages, field types, data access, public
  interfaces, and launchers. On normal inputs they agree: all three passed the 35 tests, and one program
  agreed on all **102 million** valid inputs. Off the normal path (overflow, negative values, errors
  halfway through an update, missing source) each run behaved differently.
- **RQ1b.** Large is uniform on the surface, but later sessions never revisit earlier work and style
  drifts by phase. Unasked, the agent wrote **seven** Python code generators and used them for a large
  part of the project; about **30** generated files disagree with their own generator. Two models
  measured all 5,737 files separately and agree on these points.
- **RQ3.** Tactical design (field representation, file access, inter-program calls, transaction
  ownership, missing source) varied by run. Strategic choices were the same every time and "not the ones
  we would have made": no application framework such as Spring Boot, CSV files or H2 rather than
  PostgreSQL, and console text screens rather than a web interface or terminal emulator.

### Everything compiles, and the behaviour is wrong

Errors were found in every translation examined, including records read in the wrong order "in all four
translations of the same program", a lost sign that moves a date into another century, ignored errors
that let a nightly job continue, three results for one overflowing calculation, two programs that never
terminate, a silently fixed original bug, inverted commit and rollback, no record locking, and **17**
programs counted as translated that only throw an exception. Some errors depend on luck, because the
same program was right in one run and wrong in the next; others are common to all runs and "you cannot
discover by comparing them".

The running application starts, initializes H2, opens menus, and persists a new record across a
restart, but the database setup skipped **27** logical files, a report printed headings with no data,
a displayed exit key did not work, and input end produced a Java stack trace. Every planned file is
mentioned in the output and the agent's log, which the author says is "not proof" of implementation.

### Maintainability, performance, and data

About a third of hand-translated program code is duplicated elsewhere; one date conversion is declared
in **27** classes with **20** different bodies; there are three ways to call a program; and some calls
resolve names at runtime, so the compiler cannot catch a broken interface. Keyed reads are fast, but each
sequential READ became a full-table query: reading **10,000** records in key order took about **20
seconds** where a single query needs a hundredth of a second. The agent's tests ran on a handful of
records and the database was empty, so they did not reveal it; the defect sits in one runtime class. No
production data was available, so data migration was not attempted. A hosted model processes the source
on the provider's infrastructure; an open-weight alternative such as GLM-5.3 was named but not tested.

### Conclusion: the first translation is cheap, the migration is not measured

"Getting a first translation and finishing a migration are different amounts of work; we have measured
the former." A small application can now get a runnable first translation quickly and cheaply without
specialist expertise; a medium one needs a designed workflow; production use is advised against ("Only if
you are extremely brave, or have already handed in your resignation"). He expects the cheap alternative
to bring prices down "even if there are lots of issues in the generated code".

## Why it matters

[[Legacy Code Modernization with AI Agents]] gains its first multi-run, measured baseline, and it is a
negative control for the page's parity-oracle thesis: no runnable original, and every check that was easy
to pass (compiles, starts, every file mentioned) passed. [[Agentic Testing]] gets normal-path agreement
with off-path divergence, and test generation that costs more than translation. [[AI Code Review]] gets a
statement of why comparison cannot find common-mode errors. [[Human Deferral to AI]] gets an agent making
unrequested, consistent design decisions. [[Agent Security and Governance]] gets the source-confidentiality
question. [[Programmatic Tool Calling]], [[Context Engineering]], and [[Software Performance Engineering]]
get, respectively, agent-written generators, cache-read-dominated cost, and a quadratic access pattern.

## Tensions / open questions

- **Commercial interest, disclosed.** Strumenta sells language engineering and migration services. The
  conclusion cuts both ways for it: it concedes cheap first translations and argues that workflow design,
  architecture decisions, and validation still need expertise. The recommended approach is in the
  uncaptured article 5.
- **No executable oracle.** Correctness judgments come from reading code, so the error list is a set of
  examples from a fraction of the programs, not an error rate. Large was translated once; experiments 1
  and 2 used three runs each, one model, one harness, and a naive prompt chosen as a baseline, not best
  practice.
- **AI checked AI.** Consistency and coverage checks used Claude Opus 5.5, Fable 5.2, and GPT-6 Astra.
  "Two models ... agree" is agreement between models, not ground truth.
- **Small inconsistencies.** Large's rate is given as about $1.80 and then about $1.83 per thousand lines
  without stating the first denominator; Large's time is "48 hours of agent time" in one place (the 48.1 h
  wall clock) and "40 hours of model time" in another (the 39.7 h API time); the author writes "I founded
  Strumenta" and, in the bio, "I co-founded Strumenta". "All four translations of the same program" is
  not explained in this article.
- **Not comparable with the GitHub port.** [[ByteByteGo - How GitHub Used AI to Port Copilot From TypeScript to Rust in Record Time]]
  reports about $120K for a reviewed, tested 430K-line port; this is an unvalidated first generation.
- Model names are as written in the capture (Claude Opus 5.5, Fable 5.2, claude-fable-5-1, GPT-6 Astra,
  GLM-5.3). Dollar figures are list-price equivalents, not money paid.

## Affected pages

- [[Legacy Code Modernization with AI Agents]]
- [[Agentic Testing]]
- [[AI Code Review]]
- [[Human Deferral to AI]]
- [[Agent Security and Governance]]
- [[Programmatic Tool Calling]]
- [[Context Engineering]]
- [[Software Performance Engineering]]

## Raw capture

- [[knowledge-base/raw/sources/Legacy Modernization with LLMs, measured]]

## Citations

- Canonical URL: <https://tomassetti.me/legacy-modernization-llms-measured/> (the captured link carried a
  `utm_source=tldrnewsletter` parameter, removed here).
- By Federico Tomassetti, published 2026-11-23 on tomassetti.me; captured 2026-11-25. The article thanks
  Alessio Stalla and Gabriele Tomassetti for their work on it.
- Articles 2-5 of the series are linked from the capture but were not captured or read.

## Related pages

- [[Legacy Code Modernization with AI Agents]]
- [[Agentic Testing]]
- [[AI Code Review]]
- [[Human Deferral to AI]]
- [[Agent Security and Governance]]
- [[Programmatic Tool Calling]]
- [[Context Engineering]]
- [[Software Performance Engineering]]
- [[Mistral - Modernizing Complex Legacy Code with AI Agents]]
- [[ByteByteGo - How GitHub Used AI to Port Copilot From TypeScript to Rust in Record Time]]
- [[The Decoherence Trap]]
- [[Adam Faik - How to Build an AI-Native Software Factory]]
- [[Nikolas Göbel - Informal Verification]]
- [[Coding Agent Harness]]
- [[Anthropic]]
