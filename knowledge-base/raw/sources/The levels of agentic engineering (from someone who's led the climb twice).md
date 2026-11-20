---
title: "The levels of agentic engineering (from someone who's led the climb twice)"
source: "https://zachwills.net/levels-of-agentic-engineering/?utm_source=tldrnewsletter"
author:
  - "[[Zach Wills]]"
published: 2026-11-11
created: 2026-11-20
description: "After leading the AI shift at two companies, I think the levels of agentic engineering come down to one question: what are you still doing yourself? Here are the seven steps I've seen, from handing Claude Code the ticket to a multiplayer software factory."
tags:
  - "clippings"
---
Last August I started leading an AI transformation for a 100-person R&D team inside a 700-person company. It took a real turn in October, and it took another turn every time a major model or tool came out after that.

Now I’m doing it again at my current company. We’re not done, but we’re shipping, and we have the loops, automations and cloud environments that make it work.

There are a lot of “levels of agentic engineering” lists going around right now. I think they’re useful. Most of them read like a ladder of tools, though: use this, then add that, then buy this. After going through it twice, I’d describe it with one question instead.

**What are you still doing yourself?**

At the start, the answer is everything. Every level after that is the same move. You find the part of the loop you’re still doing by hand, and you figure out how to take yourself out of it.

## You find the next level by shipping, not by mandating it

If I were giving someone advice on how to AI-pill an organization, it would start here. You have to show people what’s possible. You can’t sit in an ivory tower and tell everyone to work a new way. You have to get in it with the team and show them, by doing it, that there’s a better, faster way to deliver software.

There’s a second reason to do it yourself. When you ship, you run into the systemic friction every company has. A lot of the time it’s infrastructure. Sometimes it’s a review policy or a compliance policy. Every product has things put in place years ago for good reasons that now get in the way.

You can’t live in la la land and say “well, I expect it to work this way.” What better way to find the wall than to hit it yourself, and then go break it down?

At every company where I’ve done this, the wall has usually been infrastructure. That’s not a knock on infra teams. Infra is just the hardest thing to change. It’s a tangled web of CI jobs, deploy pipelines and environments, and there’s more on the line when it breaks. Architecture is easy by comparison: if the API endpoints stay the same, the agent can rework what’s behind them. Policies are the other wall. How many humans have to review a change? Does an automated review count? You only find out how much those rules slow you down when you’re the one waiting on them.

So that’s my approach, and it has two halves. First I ship a greenfield prototype. There’s no friction there, so it shows what the bar is: what’s possible when nothing is in the way. Then I ship a real roadmap item or a backlog ticket in the existing product, with all the realities of existing software. The difference between those two is the map. It tells you exactly where the friction lives, and you can design the change from there.

I want to lead from understanding, not idealism.

The second time looked different, though. At my first company it was early and organic. I had a lot of social capital there, and a lot of the work was training: how to use Claude Code, how to run multiple agents at once. At my current company, everyone already uses Claude, and software factories are all the rage. Training people on the basics isn’t where the value is anymore. The work is the bleeding-edge part: moving everything to the cloud, automations, factories. I also showed up with less social capital and maybe more formal authority, which doesn’t buy you nearly as much. Shipping is how you earn the right to ask people to change.

Here’s what the climb has looked like for me.

## Level 1: You’re writing the code. Hand it the ticket.

![Level 1: You stop dictating code and hand the agent the whole ticket](https://i0.wp.com/zachwills.net/wp-content/uploads/2026/11/agentic-level-1-v2.jpg?w=1600&ssl=1)

Level 1: You stop dictating code and hand the agent the whole ticket

Developers shouldn’t be writing code by hand anymore. If your organization still is, getting everyone into [Claude Code](https://claude.com/product/claude-code) and pointing it at real problems is the single biggest boost available to you.

Even inside this level there’s a range. A lot of people start by saying “build this class.” That’s still you designing the code and the agent typing it. Today you can give it the ticket. If there’s a ticket and a codebase, it can do the work without heavy management.

You’re learning to trust the machine with outcomes instead of instructions.

## Level 2: You’re explaining the architecture. Make the codebase explain itself.

![Level 2: Lean AGENTS.md pointers in each folder let the agent find its own way](https://i0.wp.com/zachwills.net/wp-content/uploads/2026/11/agentic-level-2-v2.jpg?w=1600&ssl=1)

Level 2: Lean AGENTS.md pointers in each folder let the agent find its own way

Once the agent is writing the code, you notice you’re still the one telling it how the system works. Where things live, which service owns what, how we do migrations here. So the next step is making the codebase AI-navigable, so it doesn’t need you for that.

This was a bigger problem a year ago. The current models are very good at scouring a codebase, and more often than not they’ll find what they need if you just give them access. But if your architecture is spread across services and repos, not everything is in one place, and it never hurts to leave a few indexes and pointers.

The obvious tool is the AGENTS.md (or CLAUDE.md) file. Two rules I’d give anyone:

- **Don’t use it for things the agent can discover itself.** Use it for high-level pointers that send it in the right direction.
- **Put them in the directories, not all in one file.** The harnesses load these files progressively as the agent moves through the tree. Keep each one lean.

Skills work the same way. They’re how you codify “here’s how we do this here.” But be careful, because skills tend to get too restrictive. If you’re on an older or cheaper model, a prescriptive skill helps. If you’re on a frontier model like Opus 5.5, you often don’t need the skill at all, or it should be short and goal-oriented. For the bigger architectural calls, you can also put a stronger model in charge of planning and let cheaper ones do the building.

Two years ago I was super prescriptive and held the model’s hand through everything. Now I mostly delegate the outcome.

## Level 3: You’re testing it. Let it prove its own work.

![Level 3: The agent loops on logs and tests, records proof, then CI agents check the PR](https://i0.wp.com/zachwills.net/wp-content/uploads/2026/11/agentic-level-3-v2.jpg?w=1600&ssl=1)

Level 3: The agent loops on logs and tests, records proof, then CI agents check the PR

Now the agent writes the code and knows its way around, and you’re the one checking that it works. If a person has to verify every change, you’ve just moved the typing into review.

So you give agents the same access an engineer would have. Complete access to logs. The ability to run the app end to end, debug it, test it and QA it on their own. Real verification loops, so they can hand you irrefutable proof. Agents are very good at recording a video of the feature working now, so ask for one.

Then you can chain agents in CI, and this is where it gets fun. CI does two jobs here. It checks things, and it can also kick off agents to do work. A PR comes in without an end-to-end test for the new flow? The check doesn’t just fail. It triggers an agent to write the test. A QA agent can bang on every change, do exploratory testing, and make sure it’s covered.

CI is also the best enforcement point you have. People will always do their own thing locally, with their own prompts and their own setup. CI is the one place every change passes through, so it’s where your guidance actually sticks.

Testing used to be hit or miss at most companies I’ve been at. Good orgs had it, a lot had some, most had a mix. Now every change can come with the right tests. Not all tests are created equal, though. Agents will happily generate filler unit tests that don’t protect anything, so you still need judgment about which tests are worth keeping. I’d push agents toward end-to-end tests that prove the feature works.

The goal of this level is to ship faster while raising quality, raising security and lowering the cost per shipped feature, all at the same time.

## Level 4: You’re pressing play. Get it off your laptop.

![Level 4: Agents run in the cloud, triggered by messages, emails, alerts and logs, while you're offline](https://i0.wp.com/zachwills.net/wp-content/uploads/2026/11/agentic-level-4-v2.jpg?w=1600&ssl=1)

Level 4: Agents run in the cloud, triggered by messages, emails, alerts and logs, while you're offline

At this point the agent writes, navigates and tests on its own, and you’re still sitting at your laptop starting every run. If your computer isn’t on, nothing is getting done.

So you move to the cloud. At my last company, we built our own cloud agent runner, because nobody had productized it yet. At my current company, we use [Cursor’s](https://cursor.com/) cloud agents heavily, plus agents that run in CI. That stuff is commoditized now, so you don’t need a custom runner. You do still need to design it: what triggers the work, what environment it runs in, and what it has access to. If you can get a cloud runner to run your entire system end to end, you’re in a beautiful position.

Now the work isn’t tied to a human sitting at a keyboard. You can trigger it from things that have nothing to do with a person being in the loop: a message in a channel, an email, an alert, a log line. You can assign tickets in Linear (or wherever) to agent workers, or let them pull work off the board themselves.

## Level 5: You’re checking it worked. Close the loop.

![Level 5: Workers pull tickets, ship, and a release watcher checks it delivered before closing the loop](https://i0.wp.com/zachwills.net/wp-content/uploads/2026/11/agentic-level-5-v2.jpg?w=1600&ssl=1)

Level 5: Workers pull tickets, ship, and a release watcher checks it delivered before closing the loop

The work now starts and ships without you. You’re still the one checking afterward that it actually did what it was supposed to.

So you hand that off too. When a change goes out, an agent watches the release and checks that it works as expected in production. If it didn’t, the work goes back on the board.

This is the part a lot of developers miss. “Merged to prod” and “mission complete” are two different things. If it shipped but didn’t deliver the business value, it isn’t done. And now you can codify that definition of done instead of hoping people remember it.

## Level 6: You’re the only one using it. Make the factory multiplayer.

![Level 6: The whole team feeds one shared factory of agent loops, with checks owned by engineers](https://i0.wp.com/zachwills.net/wp-content/uploads/2026/11/agentic-level-6-v2.jpg?w=1600&ssl=1)

Level 6: The whole team feeds one shared factory of agent loops, with checks owned by engineers

By now you’ve got something that looks like a factory. Tickets go in, tested and verified features come out, and nobody has to sit and watch it. Some people call this factory engineering or loop engineering, and I think that’s right.

The catch is that it’s usually one person’s factory. It runs on their setup, their triggers, their checks. So the next step is making it multiplayer: the whole team builds on it, iterates on it and feeds it. Product drops in work. Support files a bug and it gets picked up. Engineers spend their time improving the loops instead of running them.

The engineer’s value moves away from the individual feature and toward the system that produces features reliably and reproducibly. And with that much more software going out, quality becomes the system’s job too. End-to-end checks, QA agents, architectural reviews. You can buy tools for some of this, like [Cursor’s BugBot](https://cursor.com/bugbot) or [Macroscope](https://macroscope.com/), or build your own, because a lot of it isn’t that hard. Most teams end up with some combination.

## Level 7: You’re out of things to build. Decide what’s next.

![Level 7: The backlog is empty and the question becomes what to build next](https://i0.wp.com/zachwills.net/wp-content/uploads/2026/11/agentic-level-7-v2.jpg?w=1600&ssl=1)

Level 7: The backlog is empty and the question becomes what to build next

Then you’ve got a multiplayer factory doing more work in the cloud than any one person could ever deliver. Your team burns through the backlog, so the [bottleneck moves](https://zachwills.net/where-the-bottleneck-goes-when-agents-write-the-code/) to the product side of the house. What’s left for you is figuring out what’s next.

## Most teams stall at the cloud

In my experience, every team can get to level one or two. Engineers use Claude Code locally and it works. Where most teams stall is everything after that. How do we get this into the cloud? How do we get autonomous loops running? How do we make it multiplayer?

Every team I’ve talked to has a few individual superstars who are already way up the ladder on their own. The real work is making that the norm instead of the exception.

## The levels in one table

| Level | What you were still doing | What you do instead |
| --- | --- | --- |
| 1\. Hand it the ticket | Writing the code | Give it outcomes, not instructions |
| 2\. Make the codebase explain itself | Explaining the architecture | Leave lean pointers and short skills |
| 3\. Let it prove its work | Testing every change | Decide which tests and checks matter |
| 4\. Get it off your laptop | Starting every run | Let messages, alerts and tickets trigger it |
| 5\. Close the loop | Checking it worked in production | Define “done” as business value |
| 6\. Make it multiplayer | Running the factory alone | Let the whole team feed and improve it |
| 7\. Decide what’s next | Waiting on the backlog | Work out what to build |

## The tools will change. The question won’t.

Every time a big model or tool comes out, some of this gets easier and some of it stops being necessary. Skills I wrote a year ago are now too prescriptive. Indexes I built are mostly redundant because the models can find things themselves. I expect half the specifics in this post to look dated by next summer.

The question holds, though. If you’re trying to figure out where your team is, look at what people are still doing by hand.

So if you’re leading this at your company, don’t start with a list of levels to roll out. Pick something on the roadmap, ship it with the agents yourself, and notice the first thing you’re still doing.