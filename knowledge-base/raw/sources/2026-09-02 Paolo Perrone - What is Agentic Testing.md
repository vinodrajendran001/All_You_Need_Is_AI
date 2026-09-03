---
type: raw-source
source_id: src-2026-09-02-paolo-perrone-agentic-testing
captured: 2026-09-03
title: "What is Agentic Testing?"
source: "https://theaiengineer.substack.com/p/what-is-agentic-testing-fa2?utm_source=tldrnewsletter"
author:
  - "[[Paolo Perrone]]"
published: 2026-09-02
created: 2026-09-03
description: "You Give the Goal, It Finds the Way."
tags:
  - "clippings"
  - "topic/evaluation"
  - "topic/agents"
  - "source/raw"
---
Agentic testing hands an agent the goal instead of the steps, and lets it work out how to get there against whatever interface your system exposes. It finds its own way, invents cases nobody wrote, and survives the renames that break your suite. Let it also judge the answers, and a model decides what ships.

**🧭 Part of the [🤖 Agents course](https://theaiengineer.substack.com/p/the-ai-engineer-courses)**

## TL;DR

- **Agentic testing means you state the goal and an agent works out the steps.** You write “a coding agent’s pull request builds and passes its tests”. The agent opens the PR, runs what it finds, and reports whether the claim held.
- **A scripted test is a recorded route. An agentic test is a destination.** The recording breaks the moment somebody moves a turn. The destination survives, because the agent finds a new way there.
- **The loop is simple: look, act, look again.** Read the current state, take the action that moves toward the goal, read the state again, repeat until the goal holds or the agent runs out of moves.
- **Meta ran this at scale and only a quarter of the output was worth keeping.** Of everything TestGen-LLM generated, 75% compiled, 57% passed reliably, 25% raised coverage. It works anyway, because three automatic gates throw the rest away.
- **One job never gets handed over: deciding whether the answer was right.** The agent can find any route to the destination. It cannot tell you the destination was the right one. Hand that call to a model and your release gate answers differently on Tuesday than it did on Monday.

Let’s get into it.

## Why Written-Down Tests Break

Your pipeline goes red at 9:14 on a Tuesday. Forty tests passed. One failed, and it waited thirty full seconds for something that was never going to arrive.

You open the app. The feature works. You open the diff. Somebody renamed a field in a styling PR, and your test was pointing at the old name.

Twenty minutes later you have changed one string, pushed, and gone back to work. Nothing was broken and nothing was fixed. Meanwhile three flows nobody ever wrote a test for shipped last week, and your suite said nothing at all.

You have hit the wall every team with a real suite hits: your tests know the route, and they have no idea where you were going. An agent can be told the destination. What that actually buys you, and what it quietly costs, is the rest of this.

## Before Agentic Testing, There Were (Pretty Good) Scripts

To see why agents matter here, you need to see what a test has always been.

Every test you have ever maintained is a recording: you perform the work once, write down what you did and what you expected back, and the machine repeats it forever. It holds exactly two things, and both freeze the moment you type them.

The first is the **locator**, the name of the thing to act on: a button’s `data-testid`, a route like `POST /repos/{owner}/{repo}/pulls`, an import path like `from runner import run_tests`.

The second is the **oracle**, the line that decides whether what came back was correct: `assert pr.mergeable is True` is an oracle, and so is `assert response.status == 200`.

Freezing both is the whole point. A frozen recording runs fast, costs nothing per run, and answers identically every time, which is the only reason your release gate can be a green tick that means anything.

Declare the destination instead of recording the route and you need something that can work out the route on the day. That something is an **[agent](https://theaiengineer.substack.com/p/what-is-an-ai-agent)**.

## The Test That Knows the Route, Not the Destination

That 9:14 failure was not bad luck. It is what the frozen recording costs you, and it costs you in three places.

**The specific problems:**

1. **The locator holds a name, and a name is all it holds.** Rename the attribute, move the route, split the module in two, and the recording breaks while the feature works. Every engineer reading this has paid that tax more than once.
2. **The oracle only covers what somebody thought of.** The build that fails only when two flags are set, the request that arrives mid-session-refresh, the diff that quietly touches a second service: none of them fail, because none of them run.
3. **Neither half knows what the user wanted.** Nowhere in a recording does anybody write down what the system is supposed to do. The steps are there and the check is there, and the intent between them is nowhere.

![](https://substackcdn.com/image/fetch/$s_!FPT4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F79acf75d-9ae5-4ed5-95aa-38aec35aee1f_1180x620.png)

> **⚠️ Confusion Alert:** “But we have self-healing locators.” Your framework probably calls them selectors. Self-healing saves you the fix and buys you a new problem: it repoints a broken locator at whatever element is doing that work now, so a regression that hands the work to a different element looks the same to it. It patches, and your suite goes green over a broken feature.

So how do you hand over the destination and let something else work out the route? That is agentic testing.

## How Agentic Testing Actually Works

Instead of replaying the recording, you hand the agent the goal and put it in a **[loop](https://theaiengineer.substack.com/p/what-is-agent-prompt-engineering)**.

**The loop: look, act, look again.** The agent reads the current state of the system, picks the action that moves toward the goal, takes it, and reads the state again. It exits when the goal holds or when it runs out of moves.

Walk the pull request through it. The agent looks and finds the build has not started, so it triggers one. It looks again, sees one check red on a flaky integration test, and reruns it. It looks a third time, sees green, and exits. No step in that sequence was written down anywhere.

**The three jobs.** Hand an agent a goal and it has to do three things you have been doing by hand:

1. **Explore.** It works through the system, follows what it finds, and produces a plan naming the cases worth covering. You get the map before anybody writes test code, and it includes paths nobody on the team thought to list.
2. **Generate.** Driving the running system, it watches what responds and writes the cases out as ordinary test files you can read and commit.
3. **Repair.** When a test fails, it reruns it, reads the system as it stands now, and repoints the broken step at whatever now does what the old target did.

None of the three jobs works from a picture. On a web app the agent reads the **accessibility tree**, the same structured description a screen reader consumes, listing every element with its role, its name and its state. On an API it reads the schema. In a codebase it reads the signatures and the call graph. That is why it can still find the Merge button, or the endpoint that opens a pull request, after somebody rewrites the markup around it.

![](https://substackcdn.com/image/fetch/$s_!mGtJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc1f5bb5-a6de-4b86-8077-db0ac2ebf0f9_1240x590.png)

These are not my names for the jobs. **[Coding agents](https://theaiengineer.substack.com/p/ai-coding-tools-what-changed-in-the)** already run this loop against a repo, with the terminal and the test runner as their tools, and the test-focused ones split it into one agent per job.

I generated one implementation’s definitions to check. The repair agent’s tool list carries no screenshot tool at all, so the job that re-finds a moved element runs on the structure alone, over **[MCP](https://theaiengineer.substack.com/p/what-is-mcp)**, the protocol that gives an agent tools in the first place.

> **🔍 Deeper Look:** Repair agents ship with a documented give-up condition, and it is worth knowing before you run one. When the agent concludes your app broke rather than its own locator, it does not fail the build. It marks that test skipped and leaves a comment at the failing step. Nobody decided to drop that flow from your coverage. The agent did.

**Now notice what those three jobs leave alone.** The generator writes the oracle, but it writes it into a file. A person reads that file, and CI runs the line unchanged on every push. The deciding still happens the old way: one frozen check, the same answer every time.

The other option is to write no check at all. You let the agent look at the result and say whether it was right, which means asking a model the same question on every run and taking whatever answer comes back that time.

**So one green run proves nothing.** Run each test three times and count the passes two ways. If any one of the three runs passes, that counts. Engineers call that score **pass@k**. Demand all three and you get **pass^k** [^1].

I ran five checks on a pull request three times each, all of them checks on the repo rather than on the agent that opened it. The stub behind them reports status after a delay drawn fresh on every call. Two passed on every run, two failed on every run, and the fifth failed once and passed twice. That single flaky check is the whole gap: the suite scores pass@3 of 0.6 and pass^3 of 0.4. Report the first number and you ship. Report the second and you do not. One test decided it.

Report pass^k. Your users run the flow hundreds of times a day, not once, and a gate that calls a test green after two of its three runs failed is not a gate.

![](https://substackcdn.com/image/fetch/$s_!HgiE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F604c9283-ba0b-4d99-a2ed-2424bd45f9ae_1000x600.png)

## Who’s Actually Building With This

**Meta** ran TestGen-LLM across Instagram and Facebook, and put every generated test through three checks: (1) does it compile, (2) does it pass reliably across runs, (3) does it raise coverage. Three quarters cleared the first, just over half the second, a quarter the third. Engineers then accepted 73% of what survived all three, and most of its output was thrown away [^2].

> **🏗️ Engineering Lesson:** Build those same three checks into your own pipeline this week. Have the agent open a PR, run all three in CI, and discard the PR automatically when the coverage report does not move.

**Uber** runs AutoCover, which now writes about one in nine of all new tests added to their codebase. The same pipeline produces a viable passing test 20% of the time in Java, 40% in Go and 80% in Python. Read that spread as a setup cost: Python needs no build step and mocks anything, Java needs compilation, injected dependencies and a build file edit. Point your first agent wherever your tests are cheapest to run in isolation, then measure that number in your own repo [^3].

**Airbnb** moved nearly 3,500 test files off Enzyme in six weeks, against an estimate of a year and a half by hand. The pipeline reached 75% in the first four hours and 97% four days later, and retries closed the gap. Every file walks a chain of validation steps, and when a check fails the model gets asked to fix that specific failure and the file goes back through. Most files land inside ten attempts. The long tail took between fifty and a hundred, with prompts growing to 100,000 tokens and up to fifty related files pulled in as context [^4].

## What Can Go Wrong (and What’s Overhyped)

**Repair is the part that lies to you.** It cannot tell a harmless edit from a regression that moved the work somewhere else, so it repoints for both and your test goes green over a broken feature. When it cannot repoint at all it marks the test skipped, and a skipped test reports nothing. Green either way.

**Review is supposed to catch that, and it does not.** A generator emits tests that look exactly like the ones you write, so a reviewer waves them through as fast as they wave through yours, the way teams do with machine-written **[review comments](https://theaiengineer.substack.com/p/how-coderabbit-actually-works)**. An assertion that checks the build started, instead of checking the tests inside it passed, looks fine in a diff. Read the assertions first and the steps second.

**And the bill lands per step.** A recorded suite adds no model cost at all. Let an agent drive CI and 500 tests firing on every commit becomes a line item somebody will ask you about, on the same **[breakeven arithmetic](https://theaiengineer.substack.com/p/should-you-self-host-inference)** every inference bill has.

The pitch on the box is that maintenance goes away. It does not. You swap maintenance you can see for maintenance you cannot. A broken locator is boring, cheap, and screams the moment it breaks. An oracle that answers differently on Tuesday than it did on Monday does none of those things.

One version of this earns its place today: the agent at authoring time, the model out of CI. It explores and generates against staging while somebody watches, a reviewer reads the output like any PR, and CI runs committed code with no model in it. That is the shape Meta’s three checks put around a generator nobody trusted.

![](https://substackcdn.com/image/fetch/$s_!XrxZ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcab83813-9794-4045-8494-d154fcf80867_1120x580.png)

## The One Thing to Remember

Agentic testing does not remove the check. It moves who writes it.

Every argument about this is really an argument about where that move should stop. Stop it at authoring and the agent finds the route while your suite still holds the destination, so green means the same thing on every run. Push it into CI and your gate goes from right by construction to right most of the time.

💬 *What broke first when you pointed an agent at your suite? Tell me in the comments.*

## Where to Next?

- 📖 **Go Deeper:** **[What is an Eval?](https://theaiengineer.substack.com/p/what-is-an-eval)**, the mirror image: agentic testing points an agent at your software, and an eval points a test suite at your agent.
- 🔗 **Go Simpler:** **[What is an AI Agent?](https://theaiengineer.substack.com/p/what-is-an-ai-agent)**, the loop underneath all three jobs above.
- 🔀 **Related:** **[Superpowers vs GSD vs Compound Engineering](https://theaiengineer.substack.com/p/superpowers-vs-gsd-vs-compound-engineering)**, where coding agents stop and show you their work.

## FAQ

**Is agentic testing the same as testing an AI agent?**

No, and the two get filed under the same phrase constantly. Agentic testing points an agent at your software and has it drive the system. Testing an AI agent means measuring a nondeterministic system against saved inputs and checks you wrote in advance, which is an eval. The confusing part is that agentic testing inherits the eval problem, because the moment a model decides pass or fail, your test suite becomes the nondeterministic system.

**Does an agentic test need a vision model?**

Not for the browser case. The agent reads a structured description of the interface. For a web page that is the accessibility tree, listing every element with its role, its name and its state. Coordinate-based clicking exists for the cases the tree cannot reach, and it gives up the tree’s whole advantage. A button keeps its role and its accessible name when someone moves it or renames its test id. Its coordinates change the moment the layout does.

**How many times should I run an agentic test before I believe it?**

At least three, for anything you would block a release on. A single run of a nondeterministic check proves the check passed once. Three runs separate pass@k, where at least one run passed, from pass^k, where all of them did. The tests that clear pass@k and fail pass^k are the ones you cannot ship behind.

**Do I still write tests by hand?**

You still review them, and reviewing is where the assertions get fixed. The generator produces spec files that look like the ones you write, which is exactly why they slide through a diff. The tests you write by hand shrink to the ones where you already know the exact edge case, which is a smaller pile than it used to be.

[^1]: [pass@k and pass^k: Capability and Consistency Metrics](https://agentpatterns.ai/verification/pass-at-k-metrics/), AgentPatterns (June 2026)

[^2]: [Automated Unit Test Improvement using Large Language Models at Meta](https://arxiv.org/abs/2402.09171), arXiv (February 2024)

[^3]: [Automated Software Test Generation at Industry Scale Using a Multi-Agent Architecture and Workflow Integration](https://homes.cs.washington.edu/~rjust/publ/auto_cover_icse_2026.pdf), International Conference on Software Engineering (April 2026)

[^4]: [Accelerating Large-Scale Test Migration with LLMs](https://medium.com/airbnb-engineering/accelerating-large-scale-test-migration-with-llms-9565c208023b), Airbnb (March 2025)