---
type: social-post
created: 2026-11-27
updated: 2026-11-27
tags:
  - post
  - legacy-modernization
  - coding-agents
platforms:
  - linkedin
  - x
pages_used:
  - "[[Legacy Code Modernization with AI Agents]]"
  - "[[Federico Tomassetti - Legacy Modernization with LLMs, Measured]]"
  - "[[Agentic Testing]]"
  - "[[AI Code Review]]"
  - "[[Niccolò Zanichelli - Swarms Do Not Yet Raise the Roof]]"
  - "[[Ankit Gupta - Vibecoding an Inference Chip]]"
  - "[[Modaic - Latency Doesn't Lie - Jev Is (Probably) Qwen3.5-35B-A3B]]"
  - "[[Uber Engineering - How Uber Evals 1 Million Agent Skill Invocations a Month]]"
topics:
  - legacy code translation
  - behavioural equivalence
  - run-to-run variance
  - verification cost
covers_from: 2026-11-20
covers_through: 2026-11-27
status: ready
---

# Compiling Was the Easy Part

## LinkedIn post

An AI coding agent translated more than half a million lines of decades-old business software into Java for about $1,100 at list prices. All of it compiled. It still did not behave like the original.

Federico Tomassetti tested this on two real business systems from furniture and clothing manufacturing, written for IBM's IBM i platform. The agent, Anthropic's Claude Opus 5.5 in Claude Code, got a deliberately naive prompt: translate the whole application into Java and make sure it runs.

For the larger system, about 600,000 lines, his team's tooling first split the work into 49 agent sessions, which produced more than a million lines of Java. The easy checks passed: every session finished and compiled, and the application started, opened its menus, and kept a new record after a restart. All 2,777 planned files were mentioned in the output, which, he notes, does not prove their behaviour was implemented.

Looking at a tenth of the programs, the team found real errors in every translation it examined: a number that lost its plus or minus sign and sent a date into another century, a nightly job that ignored an error meant to stop it, changes saved where the original would have undone them (and the reverse), and 17 programs counted as translated that only crash.

Why did the easy checks miss this? They show that code runs, not that it does what the old code did. Translating the same code three times and comparing helps only partly. The runs agreed on normal inputs, one program on all 102 million valid inputs, but handled numbers too large for their field and failures halfway through an update differently. Some errors were luck: right in one run, wrong in the next. Others appeared in every run, so, in his words, "you cannot discover by comparing them". With no IBM i machine to run the originals, even the expected answers came from reading old source.

The limits: Tomassetti's company, Strumenta, sells migration services. The errors are examples from part of the code, not an error rate. It used one model and, on purpose, the simplest prompt. And the $1,100 leaves out tests, reviews, fixes and human time; test scenarios for five programs cost about four times their translation.

So budget the two halves separately. A first translation is now cheap. Showing that it behaves like the old system, he writes, needs the original running, representative data and scenarios, and a way to compare results. He expects it could be the most expensive part, but has not measured it. My addition: test the unusual paths where runs disagreed. His summary: "Getting a first translation and finishing a migration are different amounts of work; we have measured the former."

What would you compare a rewrite against to prove it behaves like the old system?

Source: Federico Tomassetti, "Legacy Modernization with LLMs, measured"
https://tomassetti.me/legacy-modernization-llms-measured/

#LegacyModernization #SoftwareTesting #AICodingAgents

## X post

Counts include spaces and punctuation; each URL counts as 23 characters under X's link
weighting. Number labels, counts, and code fences are outside the copy-ready text.

**A) Standalone** (278 chars):

```text
Federico Tomassetti had an AI agent translate ~600,000 lines of decades-old business code into Java for ~$1,100 at list prices. It compiled and started, yet every translation checked had real errors. Budget separately for proving it matches the original. https://tomassetti.me/legacy-modernization-llms-measured/
```

**B) Thread:**

1. (213 chars)

```text
An AI coding agent translated about 600,000 lines of decades-old business software into Java for about $1,100 at list prices. It compiled. It started. And every translation the team examined still had real errors.
```

2. (246 chars)

```text
Federico Tomassetti tested Claude Opus 5.5 in Claude Code on two real business systems from furniture and clothing manufacturing, written for IBM's IBM i platform. The prompt was deliberately naive: translate it all to Java and make sure it runs.
```

3. (279 chars)

```text
The easy checks passed. His team's tooling split the large system into 49 sessions; each finished and compiled, giving over a million lines of Java. The app opened its menus and kept a new record after a restart. Every planned file was mentioned in the output; that is not proof.
```

4. (278 chars)

```text
Checking a tenth of the programs found real errors in every translation examined: a dropped +/- sign that sent a date into another century, a nightly job ignoring an error meant to stop it, saves or undos reversed from the original, and 17 "translated" programs that only crash.
```

5. (278 chars)

```text
Why? Easy checks show code runs, not that it matches. Repeated runs agreed on normal inputs but split on oversized numbers and mid-update failures. Errors every run shares are ones "you cannot discover by comparing them". With no IBM i, even expectations came from reading code.
```

6. (260 chars)

```text
Limits: his company, Strumenta, sells migration services. The errors are examples from part of the code, not a rate. One model, the simplest prompt. The $1,100 excludes tests, reviews and fixes; test scenarios for five programs cost about 4x their translation.
```

7. (272 chars)

```text
So budget translation and proof separately. First translations are cheap now. Proving one matches the old system needs the original running, representative data and a way to compare, which he expects may cost most (unmeasured). Federico Tomassetti: https://tomassetti.me/legacy-modernization-llms-measured/
```

**Ship:** Thread. It states the cheap, compiling result before the surprise, names the
checks that passed before the errors they missed, explains why comparing repeated runs
cannot catch shared errors, and keeps the vendor interest, the examples-not-a-rate scope,
the simplest-prompt baseline, and the excluded test costs in the penultimate post. The
standalone keeps the situation, the list-price qualifier, the "every translation checked"
scope, and the action, but drops the run-to-run mechanism, the error examples, and the
limits.

## Hook variants

1. **Plain situation:** An AI coding agent translated more than half a million lines of decades-old business software into Java for about $1,100 at list prices. All of it compiled. It still did not behave like the original.
2. **Concrete number:** Seventeen programs were counted as translated. When run, they only crashed.
3. **Myth correction:** Code that compiles and starts has passed the easy checks, not the comparison with the old system.

**Recommended:** The plain situation for LinkedIn and X post 1: it gives the size, the price,
and the passing result before the reversal, so a reader who has never seen the old system knows what
was attempted. The 17 crashing programs are kept inside the error list, where the "counted as
translated" qualifier sits beside them; the myth correction is carried by the "Why did the easy
checks miss this?" paragraph and X post 5.

## Why this topic

**Window:** 2026-11-20 through 2026-11-27, inclusive, anchored to the newest active ready
post's `covers_through`. The November 20 ingest and lint entries precede that post in the
log and were scored in the previous run. Two entries follow it: the November 27 "Skill Evals,
Measured Migrations, and a Method for Inference Serving" ingest (26 sources) and the November
27 "Reversed Readings, Restored Hedges, and Scoped Comparisons" lint pass, which added no
source. The Git cross-check covered 49 commits and 76 changed source-summary paths since
2026-11-20: the 30 November 20 summaries first committed on November 20 and scored by the
previous run, the 26 November 27 summaries, and 20 older summaries that gained only links or
lint corrections. A byte comparison of the ingest and post baselines found no wiki change
outside the two logged entries. No unlogged source summary appeared.

One ByteByteGo item, the DoorDash Dispatch article, was excluded before scoring. The raw
captures of the other 25 sources contain no ByteByteGo reference; five of their summaries
mention ByteByteGo pages only as cross-links, and none of those sentences is used. That left
25 eligible sources.

Scores are editorial judgments, 1-5. Clarity and completeness must each be at least 4;
a high total cannot override either gate.

| Angle and source | Clarity | Completeness | Surprise | Concreteness | Reach | Freshness | Total | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| An agent's first translation of two real RPG systems into Java was cheap and compiled, yet every translation examined had real errors; budget the proof of equivalence separately - [[Federico Tomassetti - Legacy Modernization with LLMs, Measured]] | 4 | 5 | 4 | 5 | 5 | 5 | 28 | Selected |
| Across more than 1,100 runs, agent teams finished about 6x sooner but scored about 7% lower than one agent on the same budget, and the one swarm premium disappeared once the single agent could restart with a fresh context - [[Niccolò Zanichelli - Swarms Do Not Yet Raise the Roof]] | 4 | 4 | 5 | 5 | 5 | 3 | 26 | Eligible; not selected because its natural spine, [[Multi-Agent Coordination]], carried the November 13 post and is in cooldown until 2026-12-25. Archived as a candidate. |
| A coding agent took bit-exact inference of a ternary-weight model on an FPGA from 6.43 to 213.13 tokens per second, spending $10,000 in tokens - [[Ankit Gupta - Vibecoding an Inference Chip]] | 3 | 4 | 4 | 5 | 3 | 5 | 24 | Rejected by the clarity gate: FPGAs, ternary weights, and bit-exact inference all need explaining before the result means anything. |
| Latency and tokenizer counts suggest TypeSafe's Jev is probably a Qwen3.5-35B-A3B fine-tune - [[Modaic - Latency Doesn't Lie - Jev Is (Probably) Qwen3.5-35B-A3B]] | 3 | 3 | 5 | 4 | 3 | 5 | 23 | Rejected by both gates: the argument needs tokenizers, prefill throughput, and rank correlation explained, one test cannot separate Qwen from Gemma, and the author is a competitor. |
| Uber's skill marketplace grew from 1 skill to more than 5,000 and more than 1 million invocations a month, with skills measured and retired like code - [[Uber Engineering - How Uber Evals 1 Million Agent Skill Invocations a Month]] | 4 | 3 | 3 | 3 | 4 | 4 | 21 | Rejected by the completeness gate: a first-party report with few absolute numbers, so no worked example closes the argument. |

The selected spine is [[Legacy Code Modernization with AI Agents]]. It is mixed-source: its
Tomassetti section compares the run with GitHub's Copilot port to Rust, which the vault knows
only through a ByteByteGo article, in three places (the oracle list, the dependency-order
remark, and the $120K cost comparison). [[AI Code Review]] contrasts Tomassetti with the same
port's review. The post uses none of those comparisons; every public sentence was checked
against Tomassetti's raw capture directly, and the spine, [[Agentic Testing]], and
[[AI Code Review]] were used only for their Tomassetti sentences.

**Anti-repeat:** No earlier post used this spine or covered legacy migration. The November 20
post's run-to-run point concerned server batching changing one model's arithmetic; this one
concerns separate agent translations of the same code disagreeing off the normal path. The
archived candidate "Build the parity harness before asking agents to translate legacy code"
(scored 29/30 on September 25) is marked as used: this post makes its case through a measured
run that had no runnable original to compare against.

## Reader check

**Passed:** reread the LinkedIn body, standalone, and connected thread without relying
on these notes. Each preserves the situation, claim, example, mechanism, limit, and action.

| Cold-reader question | LinkedIn and thread | Standalone |
|---|---|---|
| What is the situation? | An AI coding agent translating decades-old business software into Java, cheaply, and the result compiling and starting. | The same, in two sentences. |
| What is the single claim? | Passing the easy checks does not show the translation behaves like the original, so proving equivalence needs its own budget. | Every translation checked had real errors; budget separately for proof. |
| What example supports it? | Tomassetti's two RPG systems: the larger one's 49 sessions compiled and started, yet every translation examined had errors (a lost sign, an ignored stop, reversed saves and undos, 17 crashing programs). | About 600,000 lines, about $1,100, compiled and started, errors in every translation checked. |
| Why did it happen? | Easy checks show code runs, not that it matches; repeated runs agreed on normal inputs but split on edge cases; errors shared by every run cannot be found by comparing runs; there was no original machine to run. | Not explained; the standalone points to the source. |
| What is the limit? | The author's company sells migrations; the errors are examples, not a rate; one model and the simplest prompt; the $1,100 excludes tests, reviews, fixes, and human time. | "at list prices" and "every translation checked". |
| What should change? | Budget the first translation and the proof separately; the proof needs the original running, representative data and scenarios, and a way to compare; test the unusual paths where runs disagreed. | Budget separately for proving it matches the original. |

"RPG" is not used: it is an unexpanded acronym and the vault records no expansion, so the
systems are described as written for IBM's IBM i platform, and "IBM i" is left as a named
platform. Claude Opus 5.5 is named as Anthropic's model running in Claude Code.
Overflow is translated as numbers too large for their field, commit and rollback as saves and
undos, and "throw an exception" as crash. "ERP", "DDS", "CL", "H2", "phases", "oracle", and
"transpiler" are not used. The LinkedIn conclusion completes the argument before the closing
question, and the vault author's own advice is labelled "My addition".

## Fact check

**Passed:** checked every public factual sentence against Tomassetti's raw capture,
[[Federico Tomassetti - Legacy Modernization with LLMs, Measured]], and the Tomassetti sections of [[Legacy Code Modernization with AI Agents]],
[[Agentic Testing]], and [[AI Code Review]]. LinkedIn has 480 words including
attribution and hashtags, above the usual 450 because the mechanism and limits paragraphs were
kept rather than cut. The X standalone is 278 characters; the seven thread posts are
213, 246, 279, 278, 278, 260, and 272 characters under the declared link weighting. The public copy is ASCII.

| Public claim group | Direct support and boundary |
|---|---|
| More than half a million lines translated into Java for about $1,100 at list prices; all of it compiled | Raw "What we found": "about $1,100 at API prices for the first generation of a translation of more than half a million lines of source" and "all the translations we produced compile". Cost section: "API list prices reported by Claude Code. We actually used a Claude subscription", so the dollars are list-price equivalents of quota, not money paid. |
| About 600,000 lines for the larger system | Raw RQ4: "roughly 603,000 lines across the migration plan, queries, and CL"; the plan alone is about 552,000 lines. The $1,101.95 total covers all 49 phases, so the post pairs $1,100 with the 603,000 figure rather than with 552,000. |
| Two real business systems from furniture and clothing manufacturing, built over decades, written for IBM's IBM i platform | Raw "The code": Small is "used in furniture manufacturing", Large "in clothing manufacturing and retail", "Both are written in RPG for the IBM i", and applications that "have evolved over decades". |
| Anthropic's Claude Opus 5.5 in Claude Code; a deliberately naive prompt to translate the whole application and make sure it runs | Raw agent table (Claude Opus 5.5; Claude Code, headless); the Small prompt ("Translate the whole application into Java ... ensuring the result can be run"); "We deliberately kept the prompt strategy simple because we wanted the simplest baseline"; "Not by giving a naive prompt, as we did". |
| The team's tooling split the larger system into 49 agent sessions; more than a million lines of Java | Raw: "Strumenta's (deterministic, *gasp*) tooling ... ordered the 2,777 files of the plan", "A script split that plan into 43 phases", plus two query and four CL phases; "Large used a fresh session per phase"; "5,737 Java files and about 1,053,000 lines". The post says the tooling split the work so that "naive prompt" is not read as unplanned for the larger system. |
| The easy checks passed: every session finished and compiled; the application started, opened its menus, and kept a new record after a restart | Raw: "Every phase completed on its first attempt ... 'completed' means the session finished, and the resulting project compiles"; "We launched Large ... the main menu and its submenus opened ... still there after restarting the application". Boundary: the same brief exploration found skipped database definitions, an unsupported exit key, and a report with no data rows, so the post says "the easy checks", and the title avoids "every check". |
| All 2,777 planned files were mentioned in the output, which does not prove their behaviour was implemented | Raw "Is everything translated?": every planned file was "mentioned in both the output and the log", and "a mention is not proof that all of a file's behavior was implemented". |
| A tenth of the programs examined; real errors in every translation examined: a lost sign sending a date into another century, a nightly job ignoring an error meant to stop it, reversed saves and undos, 17 programs counted as translated that only crash | Raw RQ2: "as soon as we looked at a tenth of the programs we found errors in every single translation, and they are not cosmetic ones"; "a sign that gets lost, with the date ending up in another century"; "a nightly job continues when it should have stopped"; "write transactions that are rolled back, or committed, where the original would have done the opposite"; "17 programs that are counted as translated but, when run, just throw an exception". "Plus or minus" glosses "sign". |
| Easy checks show that code runs, not that it does what the old code did | The post's reading of the raw boundaries: "completed" "does not certify that every source statement was translated. Or translated correctly", and "We cannot call this a complete application just because every planned file appears by name". |
| Three translations of the same code agreed on normal inputs, one program on all 102 million valid inputs, but handled overflows and failures halfway through an update differently | Raw RQ1a: "all three runs passed the 35 predefined tests, and one program agreed on all 102 million valid inputs" and "overflow, negative values, errors halfway through an update, and missing source each got different treatment in each run". The spine confirms the three runs are experiment 1's isolated translations of five programs. |
| Some errors were luck; errors in every run "you cannot discover by comparing them" | Raw "Does it do what my system does?": "some of them depend on luck: the same program was translated correctly in one run and wrongly in the next one" and "the errors that all the runs have in common, and that therefore you cannot discover by comparing them". The quotation is verbatim. |
| No IBM i machine to run the originals; expected answers came from reading the old source | Raw: "We did not have an IBM i to run the originals" and "we read the source and the RPG manual". |
| Limits: his company, Strumenta, sells migration services; examples, not an error rate; one model and the simplest prompt; the $1,100 excludes tests, reviews, fixes, and human time; test scenarios for five programs cost about four times their translation | Raw: "I founded [Strumenta], where we sell language engineering and migration services" (the bio says co-founded, so the post says "his company"); "We found all of this while examining a fraction of the code"; the spine's reading "a set of examples, not an error rate"; one translating model in the agent table; "simplest baseline"; the exclusions paragraph; "$7.56 at API prices. That is about four times the cost of translating them." |
| A first translation is now cheap | Raw closing: "it costs very little" and "a small application can now get a first runnable translation quickly and at a very low cost". |
| Proof needs the original running, representative data and scenarios, and a way to compare; he expects it could be the most expensive part but has not measured it; summary quotation | Raw "Could I go to production with it?": "access to the original applications running on IBM i, representative data and scenarios, and a way to compare their results" and "I expect testing, validation and corrections could be the most expensive part of the migration, although we have not measured that cost". Closing quotation verbatim. |
| Test the unusual paths where runs disagreed | The vault author's addition, labelled "My addition" on LinkedIn. It follows from the RQ1a finding that runs split off the normal path; it is not a measured result. The X thread omits it. |

**Attribution and exclusion:** The LinkedIn source line and the final X post name Federico
Tomassetti, matching the summary's `source_author`, and use the canonical URL without the
capture's `utm_source` tracking parameter. The raw capture is Tomassetti's own blog post and
contains no ByteByteGo reference. All eight `pages_used` entries are tracked and outside
`wiki/queries/`; the four unselected source pages support only the editorial shortlist.

**Claims cut rather than compressed:**

- The $12,000 and $120,000 extrapolations: the author calls the five-times test multiplier
  behind them "a hypothesis, not a rate we measured".
- The seven Python code generators the agent wrote unasked, and the 30 files that disagree
  with them: true and surprising, but a second story.
- The 20-second sequential read and the duplicated date conversion (27 classes, 20 bodies):
  performance and maintainability findings, not equivalence.
- The 14,500 to 26,300 line spread between runs on the small system: it shows structural
  variance, which the post does not need for the behaviour argument.
- Records read in the wrong order, a silently fixed bug, non-terminating programs, and missing
  record locking: further examples that would lengthen an already long list.
- Eight calendar days and the subscription quota pauses; the open-weight model and data
  confidentiality discussion; the market and expertise argument.
- GitHub's Copilot port comparison on the spine: ByteByteGo-sourced and excluded.
- Mistral's and X's parity harnesses on the spine: a second and third system would dilute the
  one example.

**Compression check:** The standalone keeps "at list prices", "decades-old", and "every
translation checked", and states the action as budgeting for proof rather than as a measured
cost. The thread keeps "examined", "counted as translated", the one-model and simplest-prompt
limits, the vendor interest, the exclusions, and "(unmeasured)" beside the expectation that
proof may cost most. No version presents the errors as a rate or the $1,100 as a full migration
cost.

**Comprehension check:** Each version names what passed before what failed, and the LinkedIn
and thread versions explain why repeated runs cannot catch shared errors before the limits.
The thread's sequence is situation, setup, passing checks, errors, mechanism, limits, and
action. No number needs these notes to make sense.

## Attribution

Public example and all empirical claims: **Federico Tomassetti**, "Legacy Modernization with
LLMs, measured" - https://tomassetti.me/legacy-modernization-llms-measured/

Direct source: [[Federico Tomassetti - Legacy Modernization with LLMs, Measured]].
Primary capture: [[knowledge-base/raw/sources/Legacy Modernization with LLMs, measured]].
Wiki synthesis: [[Legacy Code Modernization with AI Agents]].

The other source pages in `pages_used` document the scored editorial alternatives.
They are not additional public examples or evidence.

## Hashtags

LinkedIn: `#LegacyModernization #SoftwareTesting #AICodingAgents`

X: none.

## Related pages

- [[Post Archive]]
- [[Legacy Code Modernization with AI Agents]]
- [[Federico Tomassetti - Legacy Modernization with LLMs, Measured]]
- [[Agentic Testing]]
- [[AI Code Review]]
- [[Niccolò Zanichelli - Swarms Do Not Yet Raise the Roof]]
- [[Ankit Gupta - Vibecoding an Inference Chip]]
- [[Modaic - Latency Doesn't Lie - Jev Is (Probably) Qwen3.5-35B-A3B]]
- [[Uber Engineering - How Uber Evals 1 Million Agent Skill Invocations a Month]]
