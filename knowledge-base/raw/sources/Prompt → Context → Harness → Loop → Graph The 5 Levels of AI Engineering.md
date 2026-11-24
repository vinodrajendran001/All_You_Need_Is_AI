---
title: "Prompt → Context → Harness → Loop → Graph: The 5 Levels of AI Engineering"
source: "https://x.com/L1vsun/status/2116519560631205914?utm_source=www.theaivalley.com&utm_medium=newsletter&utm_campaign=jensen-is-back-i-was-wrong&_bhlid=e3ea221679f4d55d0dd407f382f4b857f8514ae5"
author:
  - "[[@L1vsun]]"
published: 2026-10-31
created: 2026-11-25
description: "Most people using AI right now still on level 1They open a chat, type a sentence, read the answer, then type a better sentence. When it fail..."
tags:
  - "clippings"
---
![Image](https://pbs.twimg.com/media/HV9EUUpWgAAQxL_?format=jpg&name=large)

## Most people using AI right now still on level 1

They open a chat, type a sentence, read the answer, then type a better sentence. When it fails, they blame the model and wait for the next release.

Almost nobody notices that the sentence stopped being the bottleneck a long time ago.

The people shipping real work with agents climbed four more floors. First they stopped writing prompts and started writing context

Then the environment around the model. Then the schedule that runs it. Then the shape of the whole job. At the top, no human types a prompt at all. A script does.

> This is the full roadmap: five levels, what each one is, where each one breaks, and the exact move that gets you to the next floor.

![Image](https://pbs.twimg.com/media/HV9EpG9WwAEiEmh?format=jpg&name=large)

**Every level answers the same question with a bigger answer: what does the model get to work with?**

- Level 1: you hand it a sentence.
- Level 2: you hand it a window.
- Level 3: you hand it an environment.
- Level 4: you hand it a schedule, and you stop being the one who types.
- Level 5: you hand it the shape of the job, and a fleet runs it.

New models land every few weeks. The levels don't move. Each floor wraps the one below it, so nothing you learn here expires on the next release day.

## 01\. Prompt engineering: you are the loop

Level 1 is the one everyone knows. You write an instruction, the model answers, you judge it, you rewrite it, you try again.

It works. It's also the slowest way to use AI ever invented, because the slowest part of the system is you. The model answers in seconds. You read, think and retype in minutes. Every retry waits on a human.

The tell that you're stuck here: your best trick is a magic phrase. "Think step by step." "You are a world-class expert." A notes file full of templates you paste and tweak.

Those phrases still help a little. But no sentence can give the model facts it doesn't have, tools it can't call, or a way to check its own work.

![Image](https://pbs.twimg.com/media/HV9FLtWWIAAzd6t?format=jpg&name=large)

```plaintext
The level 1 → 2 test:

Next time an answer is wrong, don't rewrite the instruction.
Ask one question: what did the model need to SEE to get this right?

If the answer is a file, a doc, an example or a rule,
your problem was never the prompt. It was the context.
```

## 02\. Context engineering: fill the window, not the sentence

In June 2025, Shopify CEO Tobi Lütke said he preferred "context engineering" over prompt engineering, because it describes the core skill better: "the art of providing all the context for the task to be plausibly solvable by the LLM."

Andrej Karpathy replied "+1" and wrote the definition everyone quotes now: context engineering is "the delicate art and science of filling the context window with just the right information for the next step."

Those last four words are the whole level. The model doesn't know your project, your rules, your last decision or what broke yesterday. It knows what's in the window, at this step, and nothing else.

> So you stop polishing instructions and start budgeting the window:

\- rules that never change: the system prompt and a project file like CLAUDE.md;

\- tools, described so the model can tell them apart and pick the right one;

\- memory: decisions and state carried over from earlier work;

\- retrieved material: the 3 files that matter, not the 300 that exist;

\- the task itself, at the end, read with everything else already loaded.

![Image](https://pbs.twimg.com/media/HV9Fi1BXwAEoRKq?format=jpg&name=large)

The ceiling here is quiet but hard. Context is everything the model sees, but it's still one call at a time, and you're still the one assembling it by hand. The moment you want the model to act (run code, open a file, check a result, try again), someone has to build the machine that does it.

That machine is level 3.

## 03\. Harness engineering: the model is the engine, the harness is the car

A harness is everything around the model that turns it into an agent: the loop that feeds tool results back in, the tools themselves, permissions, the sandbox, memory files, hooks that fire on events, and the traces of what happened.

Claude Code is a harness. Codex CLI is a harness. Put the same model inside two of them and you get two different agents.

![Image](https://pbs.twimg.com/media/HV9Fp9_XEAAFlAr?format=jpg&name=large)

In February, OpenAI published "Harness engineering: leveraging Codex in an agent-first world." The setup: a repo that grew to roughly a million lines in five months, with Codex doing the writing and the engineers designing the world it works in.

In April, researchers from Fudan and Peking University put numbers on the idea. Their paper, Agentic Harness Engineering, gives one agent a single job: keep editing another coding agent's harness, and check every edit against what it predicted

> Ten rounds later:

\- Terminal-Bench 2 pass@1 went from 69.7% to 77.0%;

\- that beat the human-designed Codex-CLI harness at 71.9%;

\- the frozen harness used 12% fewer tokens on SWE-bench Verified;

\- the gains came from tools, middleware and long-term memory, not from the system prompt.

**Read that last line again. The part most people spend all their time on was the part that mattered least.**

![Image](https://pbs.twimg.com/media/HV9Fw2QXMAAOBzB?format=jpg&name=large)

The first harness move you can make today: give your agent a gate it can't talk its way past. In Claude Code, a Stop hook runs every time the agent tries to finish. Exit code 2 blocks the stop and sends the error back to the model.

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [{ "type": "command", "command": "npm test --silent >&2 || exit 2" }] }
    ]
  }
}
```

Now "done" means the tests pass, not that the model feels finished.

The ceiling of level 3: even a perfect harness waits for you. Every run starts when a human types a task. You're no longer the loop inside the run, but you're still the trigger.

## 04\. Loop engineering: stop being the one who prompts

On June 7, Addy Osmani gave this level its name. His essay "Loop Engineering: Designing loops that prompt coding agents" defines it in one line: "Loop engineering is replacing yourself as the person who prompts the agent."

He puts it exactly where this roadmap does: "Loop engineering sits one floor above the harness."

The people closest to the tools got there first. Peter Steinberger: "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." Boris Cherny, who created Claude Code: "I don't prompt Claude anymore." His job now, in his words, is to write loops.

> Osmani's anatomy of a loop is five parts plus one place to remember things:

1. Automations that wake up on a schedule to find and triage work.
2. Worktrees, so parallel agents never touch each other's files.
3. Skills that hold project knowledge the agent loads when it needs it.
4. Plugins and connectors into the tools you already use.
5. Sub-agents that split the one who proposes from the one who checks.
6. A state store (a markdown file, a board) that says what's done and what's next.

![Image](https://pbs.twimg.com/media/HV9F7j-WYAEldgp?format=jpg&name=large)

You can start one tonight. Claude Code ships /loop: give it an interval and a task, and it runs on repeat. Leave the interval out and the model sets its own pace.

```plaintext
/loop 30m read STATE.md, pick the top open bug, fix it in a worktree,
run the tests, open a PR, then write what you did back into STATE.md
```

Here's the trap. A basic agent loop has exactly one way to end: the model stops asking for tools. Put that on a timer and you've built a machine that can spend money all night. Every loop worth running has brakes:

- \- a done check that runs outside the model (the Stop hook from level 3);
- \- a budget: max runs, max tokens, max dollars;
- \- a dry-round rule: stop after two rounds that find nothing new;
- \- state written after every step, so a crash resumes instead of starting over.

![Image](https://pbs.twimg.com/media/HV9GEuEWwAAEqkR?format=jpg&name=large)

Osmani is clear that a loop isn't full autonomy: checking the work and keeping your own judgment stay your job. The loop removes the typing, not the thinking.

The last ceiling: a loop is still one track. One agent, one queue, one thing at a time, on repeat. When the job is wide (review 40 files, check 12 sources, audit every route), a loop just does it slower.

> The top level changes the shape.

## 05\. Graph engineering: draw shape of the job

At level 5 you stop thinking in steps and start thinking in nodes and edges. A node is one bounded job with a clear input and a clear output. An edge exists only where one node's output feeds another node's input.

Most "step 1, then step 2, then step 3" agents are graphs full of fake edges. Half those steps never read each other's output. They stand in line for no reason.

> Delete the fake edges and the line turns into a diamond:

- split: one node breaks the job into independent pieces;
- fan out: many agents work the pieces at the same time, each in its own clean context;
- verify: a gate tries to kill every finding before it's allowed through;
- merge: one node sees only the survivors and writes the answer.

![Image](https://pbs.twimg.com/media/HV9GKQ3XkAEZhA4?format=jpg&name=large)

This isn't theory anymore. Claude Code's dynamic workflows (a research preview since June) let Claude write the plan as a JavaScript script and run it with a fleet of subagents, tens to hundreds in one session

The routing lives in code, so it runs the same way every time, and the wiring between agents is plain code, not another model turn

> In a workflow script, the whole diamond is about this short:

```javascript
// split → fan out → verify → merge
const parts = await agent(`Split this audit into independent parts: ${task}`, { schema: PARTS });

const findings = (await parallel(parts.items.map((part) => () =>
  agent(`Audit ${part.path}. Return every finding.`, { schema: FINDINGS })
))).filter(Boolean).flatMap((result) => result.items);

const verified = (await parallel(findings.map((finding) => () =>
  agent(`Try to disprove this finding: ${finding.claim}`, { schema: VERDICT })
))).filter((verdict) => verdict?.holds);

return agent(`Write the report from these verified findings: ${JSON.stringify(verified)}`);
```

**Two rules keep a graph fast and cheap:**

\- Wait for every result only where a node truly needs all of them at once (dedupe, ranking). Everywhere else, let each item flow straight to its next node.

\- Tier the models: a cheap model on the repetitive fan-out nodes, your strongest model only on the verdicts and the merge.

## Which level are you on? The 30-second test

You rewrite the same instruction until it works: level 1.

You load a project file, the right docs and examples before every task: level 2.

Your agent runs tools, has hooks, and can't call itself done until a check passes: level 3.

Work starts without you typing anything: level 4.

One request fans out to many agents, gets verified, and merges back: level 5.

## 5 things to build this week, one per level

**1\. \*\*Prompt\*\*** Take your most-used prompt and delete every "you are an expert" line. Put one example of a great output in its place.

**2\. \*\*Context\*\*** Write a one-page project file: rules, stack, decisions, what's done. Load it before every session and count how many corrections you stop making.

**3\. \*\*Harness\*\*** Add the Stop hook from level 3. Your agent can't finish with failing tests anymore.

**4\. \*\*Loop\*\*** Put one /loop on your backlog or your inbox, with a budget and a state file. Let it run overnight and read the state file over breakfast.

**5\. \*\*Graph\*\*** Build one diamond: split a review across files, fan it out, make a skeptic agent attack every finding, merge the survivors into one report.

![Image](https://pbs.twimg.com/media/HV9GZVUXAAAyG8V?format=jpg&name=large)

## Conclusion

A prompter writes sentences. A level 5 engineer writes the shape of the work, and the sentences write themselves.

The models will keep changing: a new Claude, a new GPT, a new Gemini, an open-weights giant every other week. Every one of them is just the engine. The levels are what you build around it, and they don't expire on release day

Most people will keep polishing the sentence on level 1.

The few who climb will be running a fleet while everyone else is still typing.

Bookmark this article and follow me [@Rel1vs337](https://x.com/@Rel1vs337) for more Info