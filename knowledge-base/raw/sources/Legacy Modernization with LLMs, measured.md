---
title: "Legacy Modernization with LLMs, measured"
source: "https://tomassetti.me/legacy-modernization-llms-measured/?utm_source=tldrnewsletter"
author:
  - "[[Federico Tomassetti]]"
published: 2026-11-23
created: 2026-11-25
description: "We asked an LLM to translate two real RPG applications to Java, one of more than half a million lines, and measured what came out: the cost, how consistent the translations are, and whether they behave like the original."
tags:
  - "clippings"
---
![Rows of wooden barrels in a brewery storehouse](https://tomassetti.me/wp-content/themes/custom-child/img/topic-legacy.jpg?v=1787310309)

Believe it or not, at the beginning of my career I worked in a research group on empirical software engineering. And yes, it is as boring as it sounds because the job consisted of measuring things and sharing the results. That is much less fun than following your instinct, waving your hands like a good Italian, and sharing your opinion. One does the empirical software thing with the goal of obtaining data because data is a useful way to contribute to the conversation. So I thought I could go back to the good old times and use an empirical approach to see how legacy modernization with LLMs works on real legacy systems.

Why inflict this pain on myself? Because I think **we really need more data in this whole mess**. There are a lot of bold claims and emotional statements out there, and they leave everybody confused. Or maybe it is just me. One day I read claims about migrations done with LLMs and their incredible results, and the other day I hear the opposite opinion, with someone explaining that it does not work for certain languages or large applications. For sure, it does not help that everybody is trying to sell you something, fight for your attention, or just share an opinion without thinking deeply enough about the limits of what they tried. Something that worked in their specific context becomes a universal truth. Take it down a notch, maybe?

So we went for the boring thing: we ran experiments on real applications. This article explains what we did, how much it cost, and gives the answers in short. The details are in the articles that follow, one for each group of questions, and in the last one I discuss how I think we should approach migrations now (in case you care).

### This series

1. **Article 1 (this one):** the experiments, the costs, and the answers in short
2. [Article 2](https://tomassetti.me/legacy-modernization-llms-decisions/): what changes when we translate the same code three times, and the decisions behind it
3. [Article 3](https://tomassetti.me/legacy-modernization-llms-correctness/): whether the translations behave like the original
4. [Article 4](https://tomassetti.me/legacy-modernization-llms-large-translation-consistency/): whether a large translation is consistent with itself
5. [Article 5](https://tomassetti.me/legacy-modernization-llms-migration-2027/): how I would approach a migration now

## Why this is particularly relevant to me

I founded [Strumenta](https://strumenta.com/), where we sell language engineering and migration services. So there is a professional interest in this. But it is not the only aspect: there is also a psychological aspect. We spent years developing advanced software language engineering techniques, and perfecting how to solve problems that few others could tackle has been a source of pride (I mean, not that my friends understood what there was to be proud of). Now I see ads from kids with no experience offering migrations with LLMs. So I have to face something unpleasant: maybe part of what we learned in all these years is worth less now.

Do migrations still require expertise? If so, which kind? I think we are asking a variant of this question in many professions, and in many niches of the software development/engineering profession, aren’t we?

## What we found

Let’s start by spilling the beans:

- **Cost:** about $1,100 at API prices for the first generation of a translation of more than half a million lines of source. This excludes independent verification, test-scenario generation, and later correction cycles. So there is a bit more to say about this number, and we will say it.
- **Output:** more than a million lines of Java from that application, and all the translations we produced compile.
- **Code consistency:** translating the same application three times gives recognizable logic, but different code structures, types, and interfaces. And some very different design decisions.
- **Behavior:** translating the same application several times can also produce different results for the same input. Some translations disagree with the behavior specified by the original source.
- **…surprises?** Did you expect the LLM to decide to generate a deterministic transpiler in Python to do some of the work? Well, this happened and other things.

## The setup

It all starts with research questions. You know, like professional scientists do. So let’s do that. I divided the questions into four areas:

- **RQ1, consistency**, in two parts:
	- **RQ1a:** do repeated translations of the same code agree?
	- **RQ1b:** does a large translation remain consistent internally?
- **RQ2, correctness:** does the translated application behave like the original?
- **RQ3, design:** what does the agent decide by itself, and does it decide the same each time?
- **RQ4, cost:** how much does it cost to translate an application, in tokens, in time, and in money?

### The code

The applications we used are real applications. I will call them *Small* and *Large*. Small is the production-planning part of an ERP system used in furniture manufacturing. Large is a broader ERP application used in clothing manufacturing and retail. Both are written in RPG for the IBM i; in these experiments, the target is Java.

I think this is a valuable part of the experiment. I have yet to see experiments on real ERP applications that people have used and that have evolved over decades to do actual work (*if I have to see yet another example based on the AWS Card Demo…*). These systems carry the requirements and changes accumulated while running a business. We are working with that history, rather than a toy example or a piece of code written by 2 undergrads in 2015 or a fake application written by some vendor to prove their thesis.

Small has about 15,100 lines of RPG, plus 208 DDS files and 4 CL programs. Large has about 552,000 lines in the migration plan, plus about 51,000 lines of queries and CL. These are source sizes; the Java counts below include generated code and tests.

**The experiments**

| Experiment | Work requested | Runs and sessions |
| --- | --- | --- |
| **1** | Five programs of Large and the dependencies needed to run them, with access to the entire application | 1A, 1B, 1C: five prompts in one conversation per run |
| **2** | The whole Small application | 2A, 2B, 2C: one prompt per isolated run |
| **3** | The whole Large application in phases | One run, 49 separate sessions |

In experiments 1 and 2, each run started in isolation, with the same source code and instructions. No run received the translation produced by another run. In experiment 3, the translation of Large was run only once: it consumed a ton of tokens, and repeating and comparing a translation of this size would have been substantial work. Experiment 3 required a bunch of sessions simply because otherwise the context window could not have handled that.

**What the agent had**

| Model | Claude Opus 5.5 |
| --- | --- |
| **Harness** | Claude Code, headless, in an isolated Docker container |
| **Effort** | Not set; Claude Code’s default |
| **Network** | Restricted through a proxy; outgoing requests logged, so we could take a look |
| **Context** | Small fit in a 1M window without compaction; Large used a fresh session per phase |
| **Original execution** | No IBM i available to run the originals |

This is the full prompt for Small:

```
The directory /work/original contains the source code of an IBM i application.
Translate the whole application into Java.
Write the Java code in the directory /work/java.

Organize the project as you see fit, ensuring the result can be run.
```

### Where the plan for Large came from

The agent did not organize Large by itself. Strumenta’s (deterministic, *gasp*) tooling parsed the codebase, found dependencies, and ordered the 2,777 files of the plan so that a file came after the things it needed. A script split that plan into 43 phases, each about the size of Small. We then added two phases for queries and four for CL programs, commands, and menus.

So, for Large, the result is an LLM plus a plan from an analysis of the whole codebase. The agent did not have to understand everything at once or choose where to start. Between sessions, it could read the Java and other files already on disk. In experiment 1, the agent also found an SQL table dependency that was not listed in the plan. Credit where it is due.

### How we checked the results

We combined manual exploration of the applications, inspection of the source code, and targeted analyses and execution checks with several AI agents. We used Claude Opus 5.5 in the initial consistency analyses, Fable 5.2 in the later checks of Large’s startup and source coverage, and GPT-6 Astra in an independent review of the code and behavior.

The evidence is not of the same kind for every experiment.

For experiment 1, we ran the code. We had 35 predefined test cases, each with its inputs and expected results, plus checks on the database contents and on the reports. Each run produced Java with different interfaces, so we had to adapt the tests to every run.

For Small, we mostly read the code. We reviewed the 14 largest programs against the RPG, some subroutines more quickly than others. Only later did we run targeted execution tests, and those produced the overflow example shown in [article 3](https://tomassetti.me/legacy-modernization-llms-correctness/).

**We did not have an IBM i to run the originals.** When I say which translation agrees with the RPG, it is because we read the source and the RPG manual and we thought relatively hard about it; however, we did not actually run the code on the real machine.

## Cost and time

- **Experiment 1:** Five programs for about $2 in 8 minutes;
- **Experiment 2:** Small for about $24 in one hour;
- **Experiment 3:** Large for about $1,100 in 48 hours of agent time and eight calendar days.

These are November 2026 figures, at the API list prices reported by Claude Code. We actually used a Claude subscription, so we spent quota rather than paying those dollar amounts (*take that, Anthropic!*).

**The repeated translations; Java lines include tests**

| Run | Wall clock | API-equivalent cost | Java produced |
| --- | --- | --- | --- |
| **1A** | 8.3 min | $1.97 | 1,459 lines |
| **1B** | 6.3 min | $1.67 | 1,275 lines |
| **1C** | 8.5 min | $2.07 | 1,749 lines |
| **2A** | 56 min | $25.58 | 85 files / 14,500 lines |
| **2B** | 63 min | $23.57 | 172 files / 26,300 lines |
| **2C** | 67 min | $23.20 | 178 files / 22,900 lines |

Consider experiment 2: The same prompt produced 14,500 lines once and 26,300 another time, for about the same money. The extra code is largely the generated data layer. The run that wrote the least code cost the most: it read more source early on and carried a larger context afterwards. Small’s largest context was about 720k tokens. Most tokens were cache reads, so an agent that reads a lot at the beginning pays for that context at every following step.

**Large, translated over multiple phases**

| Work | Phases | Wall clock | API time | API-equivalent cost |
| --- | --- | --- | --- | --- |
| **RPG plan** | 43 | 42.9 h | 35.5 h | $1,002.09 |
| **Queries** | 2 | 1.3 h | 1.0 h | $32.73 |
| **CL, commands, menus** | 4 | 3.9 h | 3.3 h | $67.13 |
| **Total** | 49 | 48.1 h | 39.7 h | $1,101.95 |

Large produced 5,737 Java files and about 1,053,000 lines. The sessions used 11.8M output tokens and 3.14B cache-read tokens. Every phase completed on its first attempt; none was repeated. Here “completed” means the session finished, and the resulting project compiles. It does not certify that every source statement was translated. Or translated correctly. Which, your software engineering instincts could tell you, is a whole other can of worms.

The 48.1 hours of wall clock include 11.8 hours of pauses waiting for the subscription’s five-hour window. API time was 39.7 hours. These are the reported measurements: do not subtract the pauses from wall clock to derive API time, which can include parallel calls. Calendar time was eight days. We stopped at 80% of the weekly quota because we also need the subscription to work, waited more than four days for the reset, and then lost additional time when an automatic restart failed.

The estimate for the whole run is about 113% of a weekly quota of a Max plan.

Per 1,000 lines of source, that is about $1.60 for Small and $1.80 for Large. Taking the plan as the comparison, Large was about 35 times the size of Small, while cost grew about 45 times. The source totals include different mixes of RPG, DDS, queries, and CL, so this is a rough scale comparison. Separate sessions kept the entire previous conversation from accumulating in the next phase.

*Large, API-equivalent cost per phase. Dark bars: the RPG plan; lighter bars: queries and CL. Each phase starts a separate agent session.*

The phases cost between $1.22 and $37.73. They did not become steadily more expensive as the Java project grew, which I believe is an interesting finding, as one could imagine that this approach can be scaled to significantly larger codebases without cost per line exploding. Some cheap phases included work already translated as a dependency; the last plan phase also contained near-copies.

![Father Ted and Father Dougal picketing a cinema. Dougal's placard reads: Careful now. Ted's reads: Down with this sort of thing.](https://tomassetti.me/wp-content/uploads/2026/11/father-ted-careful-now.jpeg)

*You may need to have spent some time in Ireland to get this glorious reference.*

**Careful: this is only the translation. To write test scenarios for the five programs of experiment 1, another model, claude-fable-5-1, spent $7.56 at API prices. That is about four times the cost of translating them.** The figures exclude our work on the plan and harness, watching the run, the reviews, and scenario generation. We did not measure a complete process of writing appropriate tests, checking correctness, and repeating cycles of correction and verification. In other words, human work and test generation are not included in the presented figures.

## Answers to the research questions

Each question has its own article with the examples and the code. Here I give the answers, so that you can decide which of those articles are worth your time.

**RQ1a: materially different translations.** The runs often preserve recognizable logic, but they produce different Java applications. Packages, field types, data access, public interfaces, and launchers vary, so the translated classes are not interchangeable. On normal inputs, they behave the same: all three runs passed the 35 predefined tests, and one program agreed on all 102 million valid inputs. Off the normal path, they do not: overflow, negative values, errors halfway through an update, and missing source each got different treatment in each run. Repeating the prompt does not give us the same code or guarantee the same behavior. The details are in [article 2](https://tomassetti.me/legacy-modernization-llms-decisions/).

**RQ1b: mostly consistent internally.** Large is uniform on the surface: shared runtime, stable names, generated records and screens. But later sessions never revisit earlier work, the style drifts from phase to phase, and about 30 generated files disagree with their own generator. We also discovered that the agent, without being asked, wrote seven code generators in Python and used them to produce a large part of the Java project. Confidence is high: two models measured all 5,737 files separately and agree on these points. The details are in [article 4](https://tomassetti.me/legacy-modernization-llms-large-translation-consistency/).

**RQ2: the translations do not behave like the original.** Everything compiles, Large starts, and on ordinary inputs the results are mostly the expected ones, but as soon as we looked at a tenth of the programs we found errors in every single translation, and they are not cosmetic ones. Among the things we found, all described in [article 3](https://tomassetti.me/legacy-modernization-llms-correctness/), are:

- records read in the wrong order, in all four translations of the same program;
- a sign that gets lost, with the date ending up in another century;
- errors that the original raises and that the translation ignores, so that a nightly job continues when it should have stopped;
- three different results for the same overflowing calculation, and two programs that never terminate;
- a bug of the original that was silently fixed;
- write transactions that are rolled back, or committed, where the original would have done the opposite;
- no locking of the records, so that two users can overwrite each other;
- 17 programs that are counted as translated but, when run, just throw an exception.

We found all of this while examining a fraction of the code, and we would find more by looking further. We also could not run the originals, which means that even our expectations come from reading the source. So these applications cannot be trusted with the business before investing seriously in testing and validation, and establishing the equivalence with the original remains an open part of the work, which I will discuss in [article 5](https://tomassetti.me/legacy-modernization-llms-migration-2027/).

**RQ3: the design varies.** We asked for a translation, and we also got an architecture that we had not chosen. The agent decided how to represent fields, how to access files, how programs call each other, who commits a transaction, and what to do when a piece of source is missing; and it decided differently in each run. The strategic choices, on the contrary, were the same every time, and they are not the ones we would have made: no application framework (e.g. Spring Boot), calling into a runtime, or coding every operation explicitly, CSV files or H2 (rather than a more obvious choice, such as PostgreSQL). [Article 2](https://tomassetti.me/legacy-modernization-llms-decisions/) follows these decisions through the code.

**RQ4: roughly $2 per thousand source lines for the first generation.** Small’s three runs averaged about $1.60 per thousand RPG lines. Large cost about $1.83 per thousand source lines, using its roughly 603,000 lines across the migration plan, queries, and CL. The counts are not quite equivalent: Small’s denominator excludes its DDS and CL. Still, they give us an idea of the scale of the token cost at API prices.

If I use a rounded $2 per thousand lines and assume costs grow proportionally, with the work still divided into manageable sessions, this is what the first generation might cost for a larger application. I have also added a scenario where generating tests costs five times as much as generating the translation:

**Illustrative extrapolation at API prices, not measured migrations**

| Source code | Initial translation | Additional test generation, assuming five times that cost | Total: translation + test generation |
| --- | --- | --- | --- |
| **1 million lines** | $2,000 | $10,000 | **$12,000** |
| **10 million lines** | $20,000 | $100,000 | **$120,000** |

The five-times multiplier is a hypothesis, not a rate we measured. We already saw an example where generating scenarios cost more than translating the programs, but we do not yet know the cost of adequate testing for a whole application. Then there are correction cycles and the human work of choosing the architecture, checking the results, and getting the system into production. These figures are not a migration budget. How to organize that work is part of [article 5](https://tomassetti.me/legacy-modernization-llms-migration-2027/).

## Questions a CTO would ask

### Can I see it run?

Yes. We launched Large, the H2 database initialized, and the main menu and its submenus opened. We also opened a maintenance screen, added a record, and saved it. The record appeared in the list and was still there after restarting the application.

![Console screen for entering a new record, with its program identifier masked.](https://tomassetti.me/wp-content/uploads/2026/11/llm-migration-new-record-screen.png)

*The new-record screen opened from the list.*

![Console list showing the added record, with its program identifier masked.](https://tomassetti.me/wp-content/uploads/2026/11/llm-migration-list-after-save.png)

*The list after saving the new record.*

We ran a report too, which produced a text file with headings but no data rows. But even this brief exploration exposed problems:

- The database setup skipped 27 logical files, which describe ways of accessing the underlying data. Their base-file definitions were missing or did not contain the fields they referred to. Those parts of the database were therefore not created.
- On a submenu, F3 was shown as the exit key, but pressing it reported an unsupported command.
- Text from the list remained visible on the new-record screen.
- When input ended, the program stopped with a Java stack trace.

So the application starts, but the runnable result is still incomplete. We tried a menu tree, a maintenance program, and a report. This was a small exploratory check, and we did not compare these interactions with the running original.

### Is everything translated?

For Large, the migration plan listed 2,777 source files, including programs and file definitions. We searched the generated Java and the agent’s migration log for the identifier of each file, and found all of them. In other words, every file in the plan was mentioned in both the output and the log.

That is a useful coverage check, but a mention is not proof that all of a file’s behavior was implemented. We did not inspect every translated program in full. There are also comments identifying calls to other programs whose source was unavailable, so those dependencies could not be fully translated from the material we had. Some query variants were outside the requested scope. We cannot call this a complete application just because every planned file appears by name.

### Does it do what my system does?

No, not if you get it in the naive way, which is by handing over the code and saying “please translate this for me”. We found errors in every translation we examined, and what I find more worrying is that some of them depend on luck: the same program was translated correctly in one run and wrongly in the next one, so whether a certain error ends up in your application or not is decided by which run you happened to get. Add to this the errors that all the runs have in common, and that therefore you cannot discover by comparing them, and the conclusion is that the naive approach does not work.

Whether this is nevertheless a good base, one that an engineering approach around the LLM can use to bring the number of errors down to something acceptable, is a different and much more interesting question, and it is the one I discuss in [article 5](https://tomassetti.me/legacy-modernization-llms-migration-2027/).

### What happens to my screens?

This is a good example of a design decision we need to make, which we will discuss in [article 2](https://tomassetti.me/legacy-modernization-llms-decisions/). Sometimes we want to rewrite the UI rather than migrate it. Sometimes we want a new interface that looks nothing like the green screens. Sometimes we want to emulate the existing interface so users can continue working in a familiar way.

In our experiment, the agent chose to keep text screens on the console, asking for each input field in turn and then for a function key. It built neither a web interface nor a full terminal emulator. This let us exercise the programs, but it was the agent’s choice under our instructions. It does not mean that this is the interface we should deliver in a real migration.

### What about my data?

We did not have the production data, so we could not migrate it or validate a data migration. Large starts with empty H2 tables; Small keeps records in memory and CSV files. In a real project, moving the existing data and checking that the new application reads and updates it correctly would be another part of the work.

### Can my people maintain this Java?

With difficulty, and the reason is not the Java itself but two things we measured across the whole of Large.

The first one is that **code is duplicated all over the place**. About a third of the code of the programs translated by hand also exists, identical or nearly identical, in some other program, and small utilities are written again and again instead of being put in the shared runtime: in [article 4](https://tomassetti.me/legacy-modernization-llms-large-translation-consistency/) you can see the same date conversion declared in 27 classes with 20 different bodies. For the people maintaining the application, this means that a correction is never done in one place. They have to find all the copies, figure out how they differ and whether the difference is intended, and fix them one at a time, hoping not to miss any.

The second one is that **the style is not consistent**. The same RPG construct is translated in one way in the programs written in the early sessions and in another way in the ones written later, with indicators that disappear in some programs and survive in others, calculations that go through the helpers of the runtime in one class and are done by hand in the next, and three different ways of calling a program. A developer who learned how things are done by reading one program cannot assume that the next one follows the same rules, and so has to study each one from scratch.

There are encouraging parts too. Large has shared helpers for operations such as MOVE and keyed file access, with comments explaining their rules, and the tests on file access check reads, updates, duplicate keys and deletion, which gives a developer somewhere to start when changing the runtime. Still, knowing Java would not be enough: a developer has to understand the RPG behavior represented by those helpers, and some program calls resolve names and adapt parameters at runtime, so that changing an interface can break a call that the compiler cannot check.

### Does my source code have to leave my organization?

It depends on how the model is deployed. Our experiment used a hosted frontier model. With that setup, the source included in the model’s context is processed on the provider’s infrastructure, even if the agent itself runs in a local container.

Hosted services can offer contractual protections for confidentiality and intellectual property. For example, Anthropic’s [commercial terms](https://www.anthropic.com/legal/commercial-terms) preserve customers’ rights to their inputs and include confidentiality obligations, while its [commercial data policy](https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training) excludes training on inputs and outputs by default. The applicable protections and retention policies depend on the agreement, account type and settings; consumer subscriptions and commercial accounts have different terms.

A different approach would be to use an open-weight model such as [GLM-5.3](https://huggingface.co/zai-org/GLM-5.3) on infrastructure controlled by the organization, given adequate computing resources. With more work on the translation system, perhaps smaller models could do the job on much more modest hardware. These would be interesting experiments; we have not measured what we could achieve locally.

### How much, and how long?

About $24 and one hour for Small’s 15,100 RPG lines; about $1,100, 40 hours of model time and eight calendar days for Large. Those are the first-translation figures, with the exclusions listed in the cost section.

### Could I go to production with it?

Only if you are extremely brave, or have already handed in your resignation.

That is a way of saying that we have not validated the translated applications for production; we only started looking into a few places and we found a bunch of issues. Doing a proper validation would be a substantial project. We would need access to the original applications running on IBM i, representative data and scenarios, and a way to compare their results with the translations and investigate the differences. I expect testing, validation and corrections could be the most expensive part of the migration, although we have not measured that cost. I will discuss this work in [article 5](https://tomassetti.me/legacy-modernization-llms-migration-2027/).

### What about performance?

Performance is a complicated topic, and we did not study it properly. But even a first look was enough to notice a few things. For example, reading a record by its key is fast, in line with what we would get by writing the database access by hand. Reading a file sequentially is a different story: every READ of the RPG becomes a separate query that scans the whole table, so the time grows with the square of the number of records, and reading 10,000 records in key order took about 20 seconds where a single query needs a hundredth of a second. The tests written by the agent did not reveal it because they run on a handful of records, and our database was empty. The good news is that the defect sits in one class of the runtime, so it should be possible to correct it in one place for all the programs. In a real migration, we would need to define benchmarks on representative data, decide what is acceptable, understand what can be improved, and also consider aspects we did not look at here, such as whether the application has to support several users and jobs working in parallel.

## Other things worth trying

We deliberately kept the prompt strategy simple because we wanted the simplest baseline we could get. There are several experiments I would like to try next:

- **More elaborate prompting strategies.** Give the agent more guidance, break the work down differently, or add explicit review steps, and measure what changes compared with this baseline. Or, set up a Migration Software Factory.
- **Different models.** Repeat the work with other models, including models we could run on our own infrastructure.
- **More application sizes.** We already tried applications of different sizes, but more cases would help us understand how size affects cost, consistency, and work organization.
- **Different source and target languages.** See how much of what we observed carries over beyond RPG and Java. Would a migration from RPG to Python be substantially different, for example?
- **Examples of the application we want.** Give the agent a reference application, or examples of the architecture and coding style we expect, and see whether it follows those choices consistently.
- **Going through specifications.** Ask the agent to first describe what each program does, have somebody review that description, and generate the code from it. Would the errors go down? How much effort would this be?

## Conclusions

So, do migrations still require expertise or just access to Claude Code?

It is a complicated question, but let me start with a simple answer. The uncomfortable truth, for somebody who sells migrations, is that a small application can now get a first runnable translation quickly and at a very low cost. Much lower than paying a professional to write that translation. Producing this first version no longer necessarily requires the technical expertise that used to be needed.

For medium-sized applications, I would expect to get a useful starting point too. Not by giving a naive prompt, as we did, but through designing a proper workflow, and that requires some skills and specialization. Also, there are still decisions to make about what the result should look like, as we will discuss in [article 2](https://tomassetti.me/legacy-modernization-llms-decisions/). And there are open challenges, especially testing and establishing that the application does what it should. I will come back to those in [article 5](https://tomassetti.me/legacy-modernization-llms-migration-2027/). Getting a first translation and finishing a migration are different amounts of work; we have measured the former.

Also, an organization may want to pay someone else to *take responsibility* for the migration to be successful.

But I think that these results clearly change the market. When there were no alternatives to specialist work, one either paid a decently high price for a migration or renounced the idea. Now there is an alternative for a substantial part of that work, and it costs very little. It will be used to bring down the price, **even if there are lots of issues in the generated code**. So we cannot assume that the same expertise will keep the same value, or that customers will pay for it in the same way. That is something those of us doing migrations have to face. Assume I am writing this with a pensive face, looking at the horizon.

And you? Did you try to migrate something with an LLM? How did you check the result?

*Thank you to Alessio Stalla and Gabriele Tomassetti for their work on this article.*

![Federico Tomassetti](https://tomassetti.me/wp-content/themes/custom-child/img/portrait-64.jpg?v=1787310307)

I build parsers, transpilers and languages for people whose work is too specific for off-the-shelf software. I co-founded Strumenta, in Torino.

[Reply by email](mailto:federico@tomassetti.me) · I read everything.