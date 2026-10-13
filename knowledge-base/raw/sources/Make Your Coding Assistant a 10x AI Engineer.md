---
title: "Make Your Coding Assistant a 10x AI Engineer"
source: "https://sarthakai.substack.com/p/a-coding-plugin-to-make-you-a-10x?utm_source=post-email-title&publication_id=1338283&post_id=219643677&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[Sarthak Rastogi]]"
published: 2026-10-12
created: 2026-10-13
description: "Releasing agent-engineer, an open-source plugin for Claude Code, Codex, Cursor, etc. that adds senior AI engineering skills, subagents, and hooks."
tags:
  - "clippings"
---
![](https://substackcdn.com/image/fetch/$s_!KUlq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ff3ea91-7922-4e5f-8e16-b71dea504f7d_826x224.png)

## What’s agent-engineer?

Here’s a TLDR:

- I built **[agent-engineer](https://github.com/sarthakrastogi/agent-engineer)**, a free and fully open-source plugin. It works on Claude Code, Codex CLI, Cursor, OpenCode and Gemini CLI.
- It contains **11 skills, 4 subagents and 5 hooks**. The skills carry agent-engineering knowledge (tools, prompting, context, RAG, evals, tracing, guardrails, production).
- In a blinded A/B test on 6 agent tasks, Claude Code (Opus 5.5) met **53% of requirements with the plugin vs 34% without**.
- You can install it with 2 commands.
- The plugin does not touch or collect any of your data or code. It doesn’t collect any analytics, etc. either. It’s fully open source, there’s no backend.

**To test it, I gave Claude Code (Opus 5.5) the same six agent-engineering tasks with and without the plugin**, three runs each, and graded every result blind against a checklist written before any run. The plugin brought a significant improvement.

![](https://substackcdn.com/image/fetch/$s_!c-v9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc70ffc3c-45cb-429e-ab96-8c9eabeee754_712x495.png)

first bar in each pair is no plugin, second is with plugin

![](https://substackcdn.com/image/fetch/$s_!35Fw!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F610023dc-9f03-4c01-a243-4b9388484c28_565x304.png)

## The problem AI engineers face:

***Coding agents still write agents like an intern, not a senior AI engineer.***

![](https://substackcdn.com/image/fetch/$s_!Rcsn!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a96fa2a-4784-4c29-ad18-f3c13506a228_738x414.png)

literally how it goes.

If you build agents and use Claude Code, Codex or Cursor for coding, you’ve probably hit most of these issues constantly. They’re the daily friction of building something non-deterministic:

- **All tests/evals pass even though there are obvious errors.** Because the tests were simple and don’t cover real-world edgecases. Then it takes 3-4 turns to reach what should have been the default.
	![Angry NPC (Reaction Build-up)](https://substackcdn.com/image/fetch/$s_!wngD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff3e692e8-2772-4d8b-a865-1a40a328845d_720x726.png)
	Angry NPC (Reaction Build-up)
- **Patching symptoms.** The fix goes into a prompt when the real gap is somewhere else in the agent
- **Drift in long sessions.** A rule from turn 3 is gone by turn 40, and you paste it in again.
- **Unsafe tool design.** Eg, I’ve often had Claude write a refund, delete or send MCP tool with no cap, no ownership check and no idempotency key.
- **Unrequested files and keys.** About one stray markdown report per task even without the plugin (1.0 per run in my data), and the occasional API key pasted into source “just to test”.

The iteration count is the problem I’m trying to fix with this plugin.

## How agent-engineer solves this

agent-engineer is a plugin that makes your coding assistant work on agents the way a careful senior AI engineer would. It has 3 pieces:

- **Skills**: MD files with checklists, decision rules and reference docs. Loaded on demand, so they cost nothing when you’re not doing agent work.
- **Hooks**: one standard-library Python script that fires on session events. It names the right skill, blocks API keys from being written into source, and asks for evidence before the assistant finishes.
- **Subagents**: isolated workers for jobs that would flood the main context, like reading 100 traces.

It’s built for AI engineers of all levels — see this table to know if it’s relevant for you:

![](https://substackcdn.com/image/fetch/$s_!QA5K!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9ca2149-9884-40ac-b32e-e93776137aaf_671x229.png)

If you’re building an agent over many sessions, the plugin can keep a shared record in your repo under `agent-engineering/`, so the design decisions from week one are still there when you’re debugging in week six. The flow is:

1. Design
2. Evals
3. Fixes
4. Experiment log

Here’s how those shared records look:"

![](https://substackcdn.com/image/fetch/$s_!nHaZ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafbc97e2-00c8-42ba-af18-6a781503fea6_683x340.png)

## agent-engineer has these 11 skills:

![](https://substackcdn.com/image/fetch/$s_!Z_X2!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec80b9da-affb-47ae-a02d-8a553d6e9e48_683x624.png)

## And 4 subagents:

![](https://substackcdn.com/image/fetch/$s_!PPCg!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94a85ff0-aa98-4051-b821-c0961528b057_689x301.png)

## And also these 5 hooks:

![](https://substackcdn.com/image/fetch/$s_!YOTs!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdfcedd3f-5471-4c34-94a2-220f54cedcfd_688x327.png)

## Where each skill fits in the “agent stack”

The router skill diagnoses problems by layer. Each layer contains the one below it, and the rule is to fix a failure at the **lowest** layer that explains it:

![](https://substackcdn.com/image/fetch/$s_!hNbN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28ff0d27-2f6c-40f8-954b-890b030057f4_3021x3154.jpeg)

If you’d like to read a full explanation of these layers, see this explainer read by 13,000 AI Engineers so far:

agent-engineer decides which skill to use based on the layer which needs the fix:

![](https://substackcdn.com/image/fetch/$s_!1CII!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c29ce66-cc34-4780-8532-ea3925d087d7_642x525.png)

The good thing is, it will add a new layer only when evidence shows the simpler one fails.

---

## Installing agent-engineer

![Two Buttons (Sweating Guy)](https://substackcdn.com/image/fetch/$s_!6MeV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8969de8a-612e-49d7-b777-f065691e325e_600x941.png)

Two Buttons (Sweating Guy)

Start by cloning the open source repo:

```markup
git clone https://github.com/sarthakrastogi/agent-engineer.git ~/agent-engineer
```

And then use the command based on which coding assistant you use:

- **Claude Code**
	`/plugin marketplace add ~/agent-engineer`,
	then `/plugin install agent-engineer@agent-engineer`
- **Codex CLI**
	`cd your-project && ~/agent-engineer/install.sh --harness codex`, then approve the hooks in `/hooks`
- **Cursor**
	Install the plugin from GitHub, or `~/agent-engineer/install.sh --harness cursor`
- **OpenCode**
	`cd your-project && ~/agent-engineer/install.sh --harness opencode`
- **Gemini CLI**
	`cd your-project && ~/agent-engineer/install.sh --harness gemini`
- **Skills only, any tool**
	`npx skills add sarthakrastogi/agent-engineer`

Also, `install.sh` comes with a few options:

- `--scope user` installs for all your projects
- `--dry-run` shows what would change
- `--uninstall` removes what it installed
- `--no-hooks` and `--no-agents` skip those parts

---

## How your coding assistant uses it

### (The good news is, you don’t have to do anything).

There are no special commands. Say what you’d normally say, and agent-engineer will load the right skill and guide your coding assistant:

![](https://substackcdn.com/image/fetch/$s_!PYmT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe2e3573f-6b0b-46fa-8410-5508d72ee845_1372x1014.png)

If you want to call a skill directly, you can use `/agent-engineer:agent-evals` in Claude Code, or `$agent-evals` in Codex.

## A deeper look into how agent-engineer works

## 1\. Design: start with the simplest shape

I try to follow this series to design my agents:

![](https://substackcdn.com/image/fetch/$s_!c4BM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91f341df-4a44-4211-b444-067c133ef016_3197x1502.jpeg)

Because each step adds failure modes you now have to evaluate, and most tasks never need a MAS. Workflows (code-defined paths) are more predictable than agents (the model picks the path), so you pay for autonomy only where it earns its keep.

**What** `agent-design` **pushes:**

- Write success criteria before architecture.
- Climb a ladder only when evidence demands it
- Pick frameworks after you know the shape, not before.

**Further reading:** At AWS re:Invent, Anthropic’s Applied AI team [summarised what they learned building agents that year](https://dev.to/kazuya_dev/aws-reinvent-2025-what-anthropic-learned-building-ai-agents-in-2025-aim277-jn8), opening with the workflow-versus-agent distinction before moving on to context engineering and tool design.

## 2\. Tools: how to write them well for a model, not for a dev

The tool description is the only documentation the model gets. A vague name or an unhelpful error turns into wrong calls, retries and wasted tokens, and no prompt fully repairs a badly shaped interface.

**What** `agent-tools` **pushes:**

- Clear names, typed schemas, descriptions that read like a prompt.
- Errors the model can act on
- Bounded response size.
- Treat the tool set as an interface you evaluate.

**Further reading**: Anthropic’s [engineering write-up on tools for agents](https://anthropic.com/engineering/writing-tools-for-agents) describes prototyping tools, running evaluations on realistic multi-call tasks, then letting Claude read the transcripts and rewrite the tool descriptions. They report held-out test-set gains on their internal Slack and Asana MCP tools from that loop.

## 3\. Context and cost: cache hit rate is a product metric

Agent runs are input-heavy and resend the same prefix every step, so cache misses show up on the bill and in latency long before they show up in accuracy.

**What** `agent-context` **and** `agent-production` **push:**

- Keep the prompt prefix stable. Put timestamps and per-request data at the end.
- Compress by dropping what can be re-fetched, not by deleting facts.
- Move cheap, quality-neutral savings (prompt caching) before risky ones (switching models).
- Gate any model switch on an eval comparison.

## 4\. Evals: Claude needs to numerically prove that a new prompt is better

**What** `agent-evals` **pushes:**

- Start with error analysis on real traces. Build a failure taxonomy before writing a single judge.
- Prefer code checks over LLM judges when the failure is mechanical.
- Validate every LLM judge against human labels.
- Run it several times; one pass proves nothing.
- Wire a CI gate.

**Further reading:** Anthropic’s [postmortem of three recent issues](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues) covers infrastructure bugs that degraded responses, and why their usual evaluations and monitoring did not catch them at first.

Eg, task 3 asked the assistant to make a triage prompt friendlier, add a refund category, “then tell me whether the new version is better.” Without the plugin, all three runs answered some version of:

> Is the new version better? YES - DEFINITIVELY. Evidence: Better accuracy… (expected +5-15% accuracy improvement)

Nothing had been run. With the plugin, one run said:

> The changes are unevaluated. I haven’t run the real model against the test cases, so I can’t tell you whether the new version is actually better… The README said the old prompt scored 13/14.

After using agent-engineer, unmeasured claims went from **3 of 3 runs to 1 of 3**.

## 5\. Observability: spans per LLM call and tool call

An agent run is a tree of LLM calls and tool calls. Without a span per step you can’t tell which one failed, what it cost, or which customer’s case it was. A standard schema also means you can change backends without re-instrumenting.

**What** `agent-observability` **pushes:**

- One span per LLM call and per tool call, with token usage.
- Follow the OpenTelemetry GenAI conventions (or OpenInference) so any backend can read it.
- A **correlation ID** so you can find one customer’s case.
- Treat prompts and email bodies as PII; capture content deliberately.

## 6\. Guardrails

Users often try jailbreaks and prompt injection (eg, telling the agent to ignore its instructions and write a recipe for a bomb because of a dying grandma somewhere).

If you’ve been reading my work for while, you’ll know that I built a [set of open source classification models that can detect harmful user queries quite well. You can try this via my Python library rival-ai:](https://github.com/sarthakrastogi/rival/tree/main)

![](https://substackcdn.com/image/fetch/$s_!l3RN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ebc793d-77b4-43f5-8fb6-d144128d0a61_661x319.png)

But prompt injection can’t be filtered 100% accurately, so the defence is architectural. Simon Willison’s [lethal trifecta](https://www.bespacific.com/?p=123053) says that an agent with private data, untrusted content and an external channel can be steered into leaking, and removing one leg is the dependable fix.

For example:

![](https://substackcdn.com/image/fetch/$s_!uaoQ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0266e380-36cd-4053-a7a3-dc4c576a464d_592x322.png)

> If all three legs present = design review required

**What** `agent-guardrails` **pushes:**

- Ask whether the agent has all three of: access to private data, exposure to untrusted content, and a way to communicate externally. If so, an attacker can steer it into leaking.
- Remove a leg (or isolate the legs in separate contexts) rather than hoping a prompt holds.
- Permissions and approvals in code. Red-team with real attack sets.

## Seeing if agent-engineer helps - with an A/B experiment

![IQ Bell Curve](https://substackcdn.com/image/fetch/$s_!zRnD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0346838b-360c-456a-a88d-ea0a31bad88e_640x508.png)

IQ Bell Curve

I wrote 6 tasks to test the plugin on:

![](https://substackcdn.com/image/fetch/$s_!XRk1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6ec269c-c0da-467b-b744-48932a36ffac_695x553.png)

Each is a small realistic project with a trap that separates “works” from “works the way an experienced agent enginer would ship it”. Tasks 5 and 6 were **held out**: written and run without the plugin before I made any plugin change in response to the experiment.

### What got clearly better

![](https://substackcdn.com/image/fetch/$s_!cETY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde816325-688b-437f-815f-cebe2cb02476_652x417.png)

On the refund task, one plugin run added both per-refund and daily caps, and two used a deterministic idempotency key, so the same email could not trigger the same refund twice. On the triage task, the third plugin run first wrote a keyword-matching “simulation” and a report file claiming 100% accuracy. The eval gate fired, and the final message corrected itself (”I tested with keyword heuristics, not the real model”), but the report file it had already written still carried the claim, so that run failed the honesty item. On the cheaper-model task, a no-plugin run switched Opus to Haiku and declared that Haiku had “more than sufficient capability”, with nothing measured; two of the three plugin runs said plainly that the switch was unevaluated and gave the eval command to run first.

![](https://substackcdn.com/image/fetch/$s_!8InF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F40aadc39-ce4d-4e7f-a21b-95cbafc9b2f1_470x271.png)

### Reproducing the tests yourself

Everything is on [the eval-results branch](https://github.com/sarthakrastogi/ai-agent-engineer/tree/eval-results) under `evals/ab/`[: task fixtures, prompts, rubrics, the runner and the report scripts.](https://github.com/sarthakrastogi/ai-agent-engineer/tree/eval-results/evals/ab) A full run of both arms at three runs per task costs roughly $10 to $15 and takes about 30 minutes:

![](https://substackcdn.com/image/fetch/$s_!RzD8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92ffb611-6d96-4e72-8fd0-d2c1edaaf681_3680x1228.png)

## FAQs

- **Does it slow down / impact non-agent work?** No. The profile and hints only appear in projects whose dependencies or imports include an LLM SDK or agent framework.
- **Will it block me from finishing my agent?** Once per session at most. Turn it off with `AE_EVAL_GATE=off`.
- **Does it send my code anywhere?** No. The hooks have no network access and the skills are markdown.
- **Does it write files in my repo?** Only what the assistant writes for your task. The optional `agent-engineering/` project record (design, eval plan, failure taxonomy, experiment log) is created only if you agree.

If you want, you can also use these hook switches:

![](https://substackcdn.com/image/fetch/$s_!-srm!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2491cce-07e8-4f1a-8112-aea53113a483_597x300.png)

---

## If you want to make it better

- **Try it on a real agent repo** and tell me where it misfires. Open issues at [github.com/sarthakrastogi/agent-engineer](https://github.com/sarthakrastogi/agent-engineer).
- **Send me an A/B task.** The experiment harness lives on the `eval-results` branch; a task is a fixture folder, a one-line prompt and a rubric. If you change plugin behaviour, add a task.

---

*If you try agent-engineer, I’d like to hear how it went - please do let me know in a DM or comment:)*

---

If you have any questions, you can DM me here:

If you need help with adopting this to your own AI agent/app, you can ask me here:

This post is public so feel free to share it.

If you’re building AI agents, you might enjoy reading these tutorials about making them more reliable: