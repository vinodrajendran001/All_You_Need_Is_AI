---
title: "I used to orchestrate agents. Now I orchestrate orchestrators. 🧵"
source: "https://www.nijho.lt/post/orchestrating-orchestrators/?utm_source=tldrai"
author:
  - "[[Bas Nijholt]]"
published: 2026-11-23
created: 2026-11-25
description: "My coding agents now work for an hour to more than a day on their own, so I run fifteen parallel sessions comfortably, and up to forty on a good day. Each thread is its own orchestrator that delegates to minimal sub-agents, and MindRoom Chat sorts every thread into Needs you, Working, Later and Done."
tags:
  - "clippings"
---
I’m a huge terminal nerd. I maintain at least twenty different CLI tools, and I use many of them every day. For a long time, all my coding with AI happened [strictly in the terminal](https://www.nijho.lt/post/terminal-ninja/). At peak I had probably thirty terminal windows and panes open at once.

So it was hard for me to accept that my next step was a desktop app. The step after that was a chat room.

I still use my beloved [iTerm2](https://www.nijho.lt/post/dotfiles/). I used to orchestrate agents in terminal windows. Now I orchestrate orchestrators. My coding agents live in [MindRoom](https://www.nijho.lt/post/mindroom/), in a room where every task is a thread, and that room shows me which thread needs me. This post walks through how I got there: the tools I used, why each one stopped working for me, and how the room in MindRoom changed along the way.

> [!note] Note
> **TL;DR:** A task I hand to an agent now runs from an hour to more than a day on its own. So I run many parallel sessions at once: fifteen comfortably, and up to forty on a good day (each with multiple sub-agents of its own). Knowing which session needs me is just a prerequisite. The real hard part is context management in my own head, remembering what every thread is doing so I can switch cleanly. MindRoom Chat shows every thread as a card under Needs you, Working, Later or Done, which takes status tracking off my plate so I can keep up.

![MindRoom Chat in the Compact view with a Needs you section of four thread cards, a Working section of six and the start of a Later section. Each card has a title, a line about the agent's last action, a worktree or pull request badge and tags.](https://www.nijho.lt/post/orchestrating-orchestrators/room-sections_hu_eed26e971afc3f50.webp)

My MindRoom-Dev room in the Compact view, rebuilt as a demo. The client is the real MindRoom Chat, and the threads are real threads from my room, replayed with their own titles and text. Four sit under Needs you and six under Working, and the bar at the bottom counts the background jobs and sub-agents. Each card shows an AI-generated title, what the agent last did, its git worktree or pull request, and when it last replied. The tool counts, the background jobs and the section each thread sits in are staged.

## Thirty terminal windows

In August 2025 I described [working on 6 features at once](https://www.nijho.lt/post/agentic-coding/): one terminal tab per feature, and a round through all of them every 10 to 15 minutes. In January I made that setup one command with [`agent-cli dev`](https://www.nijho.lt/post/parallel-agentic-coding/), which creates a [git worktree](https://www.nijho.lt/post/git-worktree/) and opens a new tab with an agent already working in it.

That worked because a task took minutes. I’d start one, move to the next tab, and by the time I came back around there was something to review.

Then the models got better and I handed over more scope per task. The more I hand off, the longer an agent takes to finish. So I started doing more things in parallel. Thirty terminal windows was the ridiculous max, when I worked on five to eight things at once and each one had a couple of sub-panes, one with Codex and one with Claude Code. I was the orchestrator myself, jumping between panes to keep every agent moving. Keeping track of what’s running and what’s done becomes exceedingly hard in the terminal. Thirty panes all look the same, and the only way to find out what one of them is doing is to open it and read.

In June 2026 I experimented with [cmux](https://cmux.com/) for a couple of months to improve oversight and clarity. It’s a terminal built for this, with vertical tabs and notifications for coding agents.

## The apps in between

My next step was the Codex desktop app, now rebranded as the ChatGPT app. I started using it around GPT-5.2, when the OpenAI models were, at least in my opinion, undoubtedly better. I absolutely loved it. It was a massive bump in my productivity, because it gave a much clearer view of what was running and what was done.

Then Fable 5 came out in June, and it felt better than the OpenAI models, so I went back to the Claude Code CLI. Switching back and forth between the Codex desktop app and the Claude CLI wasn’t optimal, so I looked for something that unified the two. That same month I found [T3 Code](https://github.com/pingdotgg/t3code), which I really adored as well. It calls itself “the open-source control plane for coding agents”.[^1] I think of it as a harness for harnesses: it wraps Claude Code, Codex and OpenCode, and shows them in one web interface.

T3 Code wasn’t perfect for massively parallel work either. With more than twenty concurrent sessions, my relatively beefy AI machine started to struggle. The machine wasn’t overloaded. As far as I could tell, too many database writes went through a single thread. Opening a long thread took several seconds. And threads with background tasks still running showed up as idle, as if they needed me, which added to the confusion. Another thing I didn’t like was that T3 Code’s iOS app and web app were separate apps with different interfaces. In MindRoom Chat I fixed that for myself too: the web app and the iOS app are built from the same codebase, so they work the same way.

The awesome bit is that T3 Code is completely open source. So I ported my favorite functionality and its best ideas to MindRoom, and fixed the things that annoyed me.

## Why I stayed with the native harnesses

All of these tools have one thing in common: they run the coding harness of the company that made the model. The Codex app runs Codex, Claude Code is Anthropic’s own, and T3 Code drives both.

I stayed with them because I felt a model must just work better in its native harness, since that’s what it was trained with. It’s why I wrote seven weeks ago that [“for writing code, dedicated tools like Claude Code and Codex are better”](https://www.nijho.lt/post/mindroom-at-ionq/).

Then I [tested that belief](https://www.nijho.lt/post/native-harness-tools/). Over more than 4,000 runs of short terminal tasks, giving a model the tools of its own harness made only one model clearly more efficient.[^2] What did matter was how much the agent sends with every request: a minimal agent with one shell tool and a 12-line prompt used 58 to 76% fewer tokens than MindRoom’s standard agent.

That got me over the mental block. If the native harness doesn’t buy much, my agents can just as well work in the place where I already keep everything else. Even better, leaving the native harnesses makes it easy to support every model in the same room. Claude Code is Anthropic only, the Codex app is OpenAI only, and T3 Code wraps separate harnesses like Claude Code, Codex and OpenCode. In MindRoom I can mix models from Anthropic, OpenAI and Google inside one thread. Each sub-agent runs in that same minimal mode, which keeps the token count down. Most of my coding now happens in MindRoom threads.

## Tasks that run for a day

Two things changed how long an agent can work without me.

The first is the models. With Claude Opus 5.5 and Claude Fable 5.2 I had another massive boost in productivity, simply because they can handle such an insanely large scope right now.

The second is my skills, which are public as [baspowers](https://github.com/basnijholt/baspowers). They dictate a workflow where the agent follows established good engineering practices: it writes a spec and a plan, and it works test-first. But instead of involving me whenever something is ambiguous, it cross-checks with another frontier model, like GPT-6.2 Astra. Only if that doesn’t resolve it does it involve me.[^3]

This is what reaches me, replayed from a real thread. Fable and Astra disagreed about a design choice, so the agent stopped and asked me. It lists both options and says which one it recommends. I answer with one click, and the agent goes on.

<video controls=""><source src="https://www.nijho.lt/post/orchestrating-orchestrators/agent-question.mp4" type="video/mp4"></video>

I wrote last month that [you don’t need skills to start with AI](https://www.nijho.lt/post/how-to-start-with-ai/), and I still think so. In one test, agents wrote a failing test before fixing a bug in 0 of 32 runs without my test-driven development skill, and in 32 of 32 runs with it. As I wrote there: “That matters when agents run on their own for hours.”

The result is that any task I start might run from just an hour to more than a day autonomously. That means I can run fifteen parallel sessions extremely comfortably. After a good night’s sleep, with a lot of focus, I’m able to orchestrate up to forty. Knowing which session needs me is just the baseline requirement. The real hard part is context management in my own head, remembering what every thread is doing. When I’m tired, I can’t hold that many in my head at once. When I’m rested and focused, I can still context switch between them almost instantly, as long as the room makes it clear what’s going on.

## Orchestrating orchestrators

One session is rarely just one agent, so forty sessions can easily mean a hundred agents in flight. In every thread I only talk to one parent agent, my development agent running on Opus 5.5. That parent agent carries my skills, my memories, and how I like to work. It knows my review standards, my git workflow, and when to cross-check a design decision instead of interrupting me.

Instead of doing every edit and review itself, that parent delegates the heavy lifting to minimal sub-agents. Each sub-agent starts with a much shorter system prompt in minimal mode, which keeps token overhead low and keeps it focused on one bounded job. In principle a sub-agent can look up how the parent agent works, though it rarely needs to because the parent already holds the context, memories, and workflow rules.

The parent picks the model per job using rules in its system prompt. By default it writes code with Gemini 4 Neon, which only came out a couple of days ago. It’s still pretty expensive, and in the few days I’ve used it, the performance has been incredible, especially on UI work. Then GPT-6.2 Sol, GPT-6.2 Astra and Opus 5.5 review the full diff in parallel, and no model reviews its own code. After a fix round, a fresh reviewer checks the full diff so it doesn’t fixate on earlier findings. Fable 5.2 only writes code when a task is very complicated, or when two review rounds still find major issues. Simple lookups go to Claude Haiku 5.5.

That split is why the jump from thirty terminal panes to forty sessions works. I’m no longer shuttling prompts and review comments between Codex and Claude Code tabs by hand. Each thread is its own orchestrator, and everything in the rest of this post is the interface I built to orchestrate those orchestrators.

In this clip, Fable wrote the fix on a harder task while two other models review it in the background. The bar under the thread lists every running sub-agent with its task, model and run time. A click on a run opens what that sub-agent is doing. The thread is a real one, and the two runs and their numbers are made up for the demo.

<video controls=""><source src="https://www.nijho.lt/post/orchestrating-orchestrators/sub-agents.mp4" type="video/mp4"></video>

## About those lines of code

Programming is my biggest passion. Before AI coding got really good, I looked at every line of my code, and every comma mattered to me. I’d often lie in bed scrolling through my own code in the GitHub app, trying to find a place where I could make it a little cleaner, more DRY or more elegant.

In January I gave a presentation to a group of people who weren’t very AI native. I told them that I had written about a million lines of code in the last year, and I felt slightly embarrassed to say that. In the first twenty days of this month, the count is almost four million.

Added Deleted

<svg fill="currentColor" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle" width="720" height="346" viewBox="0 0 720 346" style="font-size: 13px; font-family: system-ui, sans-serif; background: transparent; fill: currentcolor;"><g text-anchor="end" font-variant="tabular-nums" transform="translate(-9,0)"><text y="0.32em" transform="translate(52,300)">0</text> <text y="0.32em" transform="translate(52,268)">0.5M</text> <text y="0.32em" transform="translate(52,236)">1M</text> <text y="0.32em" transform="translate(52,203.99999999999997)">1.5M</text> <text y="0.32em" transform="translate(52,172)">2M</text> <text y="0.32em" transform="translate(52,140)">2.5M</text> <text y="0.32em" transform="translate(52,107.99999999999999)">3M</text> <text y="0.32em" transform="translate(52,76.00000000000001)">3.5M</text> <text y="0.32em" transform="translate(52,44)">4M</text></g> <g text-anchor="start" transform="translate(-49,-25)"><text y="0.71em" transform="translate(52,28)">Lines touched per month</text></g> <g transform="translate(10.5,9)"><text y="0.71em" transform="translate(64,300)">2024-11</text> <text y="0.71em" transform="translate(114,300)">2025-01</text> <text y="0.71em" transform="translate(264,300)">2025-07</text> <text y="0.71em" transform="translate(414,300)">2026-01</text> <text y="0.71em" transform="translate(564,300)">2026-07</text> <text y="0.71em" transform="translate(664,300)">2026-11</text></g> <g><rect x="64" width="21" y="298.62419200000005" height="1.3758079999999495" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="64" width="21" y="297.90208" height="0.7221120000000383" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="89" width="21" y="295.493248" height="4.506752000000006" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="89" width="21" y="294.719424" height="0.7738239999999905" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="114" width="21" y="297.125248" height="2.874752000000001" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="114" width="21" y="296.08672" height="1.0385279999999852" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="139" width="21" y="298.78336" height="1.216639999999984" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="139" width="21" y="298.411904" height="0.3714560000000233" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="164" width="21" y="296.373184" height="3.6268160000000194" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="164" width="21" y="294.89184" height="1.4813439999999787" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="189" width="21" y="298.105344" height="1.8946559999999977" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="189" width="21" y="297.506752" height="0.5985919999999965" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="214" width="21" y="298.899904" height="1.1000960000000077" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="214" width="21" y="298.555904" height="0.3439999999999941" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="239" width="21" y="296.653888" height="3.346112000000005" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="239" width="21" y="295.448704" height="1.2051839999999743" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="264" width="21" y="291.622208" height="8.377792" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="264" width="21" y="286.555456" height="5.066752000000008" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="289" width="21" y="285.87008000000003" height="14.12991999999997" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="289" width="21" y="279.139584" height="6.7304960000000165" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="314" width="21" y="291.120768" height="8.879232000000002" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="314" width="21" y="286.48812799999996" height="4.632640000000038" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="339" width="21" y="290.353216" height="9.646784000000025" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="339" width="21" y="285.96236799999997" height="4.390848000000005" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="364" width="21" y="262.48128" height="37.51871999999997" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="364" width="21" y="249.52416" height="12.957120000000032" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="389" width="21" y="290.930816" height="9.069184000000007" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="389" width="21" y="287.39065600000004" height="3.5401599999999576" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="414" width="21" y="290.07379199999997" height="9.926208000000031" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="414" width="21" y="283.191872" height="6.88191999999998" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="439" width="21" y="285.915968" height="14.08403199999998" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="439" width="21" y="280.79468799999995" height="5.12128000000007" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="464" width="21" y="287.292032" height="12.707967999999994" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="464" width="21" y="281.26086399999997" height="6.0311680000000365" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="489" width="21" y="270.212608" height="29.78739200000001" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="489" width="21" y="256.055232" height="14.157376" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="514" width="21" y="283.463936" height="16.53606400000001" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="514" width="21" y="274.50419200000005" height="8.959743999999944" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="539" width="21" y="286.81113600000003" height="13.188863999999967" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="539" width="21" y="281.952896" height="4.858240000000023" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="564" width="21" y="266.927296" height="33.07270399999999" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="564" width="21" y="249.653184" height="17.274112000000002" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="589" width="21" y="273.57152" height="26.42847999999998" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="589" width="21" y="256.859264" height="16.712256000000025" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="614" width="21" y="193.118464" height="106.88153600000001" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="614" width="21" y="142.621888" height="50.496575999999976" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="639" width="21" y="186.05683199999999" height="113.94316800000001" rx="2" fill="#3ca951" fill-opacity="0.95"></rect><rect x="639" width="21" y="118.89862400000001" height="67.15820799999997" rx="2" fill="#ff725c" fill-opacity="0.95"></rect><rect x="664" width="21" y="87.38176" height="212.61824000000001" rx="2" fill="#3ca951" fill-opacity="0.62"></rect><rect x="664" width="21" y="46.13535999999999" height="41.24640000000001" rx="2" fill="#ff725c" fill-opacity="0.62"></rect></g><g fill-opacity="0.78" text-anchor="end" font-size="11" transform="translate(16.5,-9)"><text y="0.32em" transform="translate(664,46.13535999999999)">Nov 1 to 20</text></g><g stroke="currentColor"><line x1="52" x2="696" y1="300" y2="300"></line></g><g fill="Canvas" stroke="currentColor" pointer-events="none" text-anchor="start" transform="translate(10.5,0)"></g></svg>

Lines added and deleted per month in my merged pull requests and direct commits, counted by trueloc on November 20, 2026. November 2026 covers only the first twenty days of the month, less than three weeks.

I strongly feel that lines of code is not a measure of quality at all. It’s like measuring how good you are at building airplanes by how much weight you added to them.[^4]

The numbers come from [trueloc](https://github.com/basnijholt/trueloc), a tool of mine that counts every line added and deleted in every commit of my merged pull requests, plus my direct commits.[^5] Even when a pull request is squash-merged into one commit on `main`, trueloc still counts the separate commits that went into it. That includes churn, generated files, and code that an agent wrote and then rewrote. From November 2024 through October 2025 that was about 1.4 million lines in 848 merged pull requests. In the twelve months after that it was about 10 million lines in 5,148 pull requests, and about two thirds of those lines are in code files.[^6]

So read the chart as the amount of work in flight, because that’s what I had to keep track of.

## A thread is the agent’s context window

MindRoom started out as just a basic chat interface. My idea was that every conversation in a room happens in a thread, and the thread is the context window that the agent sees. The agent has tools to look into other threads if it wants to. But its context is just that one thread, which is compacted once the context window fills up.

So one task is one thread, and a room is a list of tasks. For coding, each thread also gets its own git worktree, and the pull requests the agent opens are linked to the thread.

I don’t even have to start a session by picking a repository in a UI. I keep one meta-repo checkout holding all my repositories, and the agent already knows that folder. When I describe an issue, it figures out which repo I mean from context alone, and I only name the project when it’s brand new or genuinely ambiguous. Lately I also record short screen recordings on my phone, attach one to a thread, and dictate the rest by voice. Sometimes I land an entire large pull request without typing a single word. We even have an Apple Watch app now for orchestration in a pinch: one big record button starts a new task from my wrist, and I can read the replies there too.

## From first messages to four sections

The room view went through six versions. You can click through the steps and try the filter, sort, group and section buttons below in a small mock-up of the same room.

A room like in any chat app. You see the first message of each thread, and you have to open it to know what it became.

\# dev interactive demo · click buttons to try

B

**Bas** 5h ago

typo in the readme, second paragraph

💬 2 replies

B

**Bas** 4m ago

the plugin docs are out of date I think

💬 9 replies

B

**Bas** 1d ago

remind me monday to rebase our homeserver fork

💬 4 replies

B

**Bas** 31m ago

ok next thing, the toolkit names are confusing, see what we discussed

💬 57 replies

B

**Bas** 6m ago

when I go back to a room on my phone it loses my scroll position, look into that

💬 23 replies

B

**Bas** 2m ago

hm, search is slow again when I type two words

💬 18 replies

B

**Bas** 8m ago

check CI on that PR every ten minutes and merge it when it is green

💬 12 replies

B

**Bas** now ago

the load test from yesterday, rerun it with 500 users and fix whatever breaks

💬 41 replies

A mock-up in JavaScript with demo data, not the real app. The filter, sort, group and section buttons are interactive.

**First messages.** In a typical chat room, like Slack, you see the first message of a thread and then you click into it. Maybe you see a couple of avatars of who’s active in the thread. But that first message isn’t always indicative of what the thread is about. “Ok next thing, see what we discussed” tells me nothing an hour later.

**Titles.** So I added AI-generated titles to every thread and showed those in the room. A title is a few words that say what the thread is actually about.

**Resolve.** Then I realized it was hard to scroll through a room and know which thread is active, which one is done, and which one I was completely done with. So I added a sense of status. I can resolve a thread, which means I’m completely done with it, and it turns green.

**Sort and filter.** I added filters, so I could hide the resolved threads, and filter on streaming or not, on scheduled or not, and more. Now I could sort on latest message, filter out the resolved threads, and know from the room which ones I had to address.

**Cards.** That view still had a lot of cruft that obscured what’s important. I’d much rather see the AI-generated title, who’s currently working, and when the last reply was. So I came up with the Compact view, where every thread is one card. A card has three lines: the title and the time of the last reply, then what the agent is doing right now or the start of its last answer, and then who’s in the thread, its git worktree or pull request, its tags, and the number of replies.

**Sections.** Then, inspired by the sections in T3 Code, I added that type of grouping too.[^7] The cards now sit under four headers:

- **Needs you:** the agent finished or asked me something, and nothing is running in the thread.
- **Working:** the agent is replying, or a sub-agent or background job in the thread is still running.
- **Later:** the thread is snoozed or has something scheduled, so it comes back on its own.
- **Done:** I resolved it.

A thread with a background job counts as Working. That’s the fix for the thing that confused me in T3 Code: a thread that is still working in the background no longer shows up as needing me.

The mock-up uses demo data. The clips below are the real MindRoom Chat, in a demo copy of my room that replays real threads of mine. The text in those threads is real. The tool calls, the background jobs and the numbers next to them are made up.

Here I fold and open the sections, show only the unresolved threads, and turn the grouping off and on.

<video controls=""><source src="https://www.nijho.lt/post/orchestrating-orchestrators/room-sections.mp4" type="video/mp4"></video>

And this is one request from start to finish. I type it in the room, and its card sits under Working while the agent replies. Once the agent is done, the card moves to Needs you.

<video controls=""><source src="https://www.nijho.lt/post/orchestrating-orchestrators/request-to-needs-you.mp4" type="video/mp4"></video>

This small change in organization also resulted in a massive productivity boost, and it’s the interface I’m using right now.

The older view is still there. These two screenshots show the same demo copy of my room in both modes: the Threads view with each thread’s first message, AI title and reply count, and the Compact view with sections.

![MindRoom Chat showing the MindRoom-Dev room timeline with first messages, each followed by an AI-generated thread title and a replies badge.](https://www.nijho.lt/post/orchestrating-orchestrators/threads-view_hu_e77ef69194a9a111.webp)

The Threads view of the demo room in MindRoom Chat: every thread shows its first message, with the AI-generated title and the number of replies under it.

![MindRoom Chat showing the same MindRoom-Dev room as cards grouped under Needs you with four cards and Working with six cards.](https://www.nijho.lt/post/orchestrating-orchestrators/compact-sections_hu_1e646f892156136a.webp)

The same room in the Compact view with sections: four threads under Needs you and six under Working.

## Hiding what you don’t need to see

I believe that to be productive with AI, you should be exposed to its raw power. It should be possible to see the agent’s reasoning, to see every tool call it makes, and to read the actual output of the model.

But nobody should be overwhelmed by it. In many cases you don’t care how the agent got there, and some people will never care.

So while an agent works, MindRoom Chat shows its reasoning and its tool calls as they happen. When it’s fully done, all of that folds away behind one row, and what stays is its conclusion. One click opens it again.

Here it is in the real client, with a question I really asked and the agent’s real answer. The answer streams in while the agent works, and its work folds behind one row when it’s done. One click opens that row again. The tool calls behind the row are made up for the demo.

<video controls=""><source src="https://www.nijho.lt/post/orchestrating-orchestrators/reply-streams-and-folds.mp4" type="video/mp4"></video>

What you read is still the direct output of the model. The conclusion isn’t a summary written by a different model, and the folded work is still there when you want it. The folding is another idea I took from T3 Code, where a finished turn collapses into a “Worked for” row.[^8]

## What I took from T3 Code

The sections and the folded replies aren’t the only things I ported.

- The model picker has an Effort column for the reasoning level.[^9]
- Pull requests show up as cards, with a side panel that has the changed files and their diffs.

Here it is on a merged pull request of MindRoom Chat. The badge on a card has a hover card, and a click opens the panel next to the thread. The panel has the summary, the file tree and the diffs. What it shows is what GitHub returned for the real pull request.

<video controls=""><source src="https://www.nijho.lt/post/orchestrating-orchestrators/pull-request-panel.mp4" type="video/mp4"></video>

I ported the code directly from T3 Code, with its MIT license linked in the repositories. Because I control the full source, I tailored the app to how I actually work. For example, the pull request viewer hides test files by default because I no longer read them, whereas T3 Code still showed all of them. I also made the whole interface keyboard-first, so I can navigate rooms, threads and actions without ever touching the mouse. Neither the pull request panel nor the git worktree support is built into MindRoom Chat itself. Both live in plugins, such as the [pull request plugin](https://github.com/mindroom-ai/pull-request-client-plugin), because the chat app only knows about rooms, threads and agents. Not every one of these features strictly has to be a plugin. I’ve been pushing hard on MindRoom’s plugin ecosystem to keep it extensible, and building real features as plugins is how I know the plugin interface is strong enough.

I could change the room view this often because [I own the client](https://www.nijho.lt/post/roll-your-own-fork-the-rest/). [MindRoom Chat](https://github.com/mindroom-ai/mindroom-chat) is open source as well, under Apache-2.0. If my four sections don’t fit how you work, you can change them, the same way I took what I liked from T3 Code.

## Interactive canvases

Not every decision fits a text reply or three buttons. When an agent proposes a UI change, it can send an interactive HTML canvas right inside the thread. I can click through the variants, toggle states and send my choice back to the agent directly from the page.

These are three real canvases my development agent built for me, embedded live below. Click through them to try the tabs, toggles and controls yourself, especially the Account Hold Menu where the press-and-hold and swipe gestures actually work.

1 / 3

Four watch-face variants side by side. Switch screens (Home, Thread, Recording, Approval & Ask, Picker & Widgets) or toggle room state.

Real canvases generated by my development agent, using placeholder data. Clicking submit shows a preview toast instead of sending to an agent.

## A software factory without the rigid harness

A lot of people are talking about building heavily structured “software factories” with strict agent harnesses. That feels very anti-Bitter Lesson to me. The models already orchestrate work well enough on their own that you don’t need rigid pipeline structure around them.

Even without a strict harness, I end up with the software factory people want anyway. A [plugin](https://github.com/mindroom-ai/error-notifier-plugin) reports errors automatically into a room. An agent triages the error on its own and starts working on a fix. By the time I check in, there’s a pull request waiting for me with an agent I can question directly about the trade-offs, or even jump on a voice call with.

## What the numbers do and don’t show

The chart is not a measure of good code, as I said above. It can’t credit MindRoom either. The big jump is in September 2026, which is when [GPT-6 Astra and Claude Opus 5.5 came out](https://www.nijho.lt/post/self-hosting-ai-is-not-cheaper/). The sections landed on November 17, a few days before I wrote this. So the chart shows the problem I had, which is far more work in flight than I could follow in terminal tabs.

Forty sessions is a peak, and fifteen is a normal day. And I built the tool I’m praising, so of course it fits me. Before MindRoom, I loved the Codex app and then T3 Code. I also wrote last month that [“most new AI tooling is not very good, and MindRoom may well be included”](https://www.nijho.lt/post/roll-your-own-fork-the-rest/).

Before I merge a pull request, I no longer read the code line by line. In the pull request viewer I built, hovering over the diff size opens a breakdown of source code, documentation and tests. Nowadays I mostly ignore the test size and use the source code diff to judge whether the complexity is worth it. Before a pull request even reaches me, three other models have already reviewed it, always at least two models different from the one that wrote the code. The exact mix changes almost by the day, currently from Sol, Astra, Neon, Opus and sometimes Fable. My own review is mostly asking the agent targeted questions about how it solved something, what the trade-offs were, and why it did it that way. Then I either press merge myself in the sidebar, or I tell the agent to do it.

Fifteen parallel sessions can cost a lot. I’ve been spending anywhere from $50,000 to $100,000 a month in model usage, though luckily I don’t pay the bill.

I couldn’t think of a recent run that went badly wrong. The models have gotten so much better that the [hooks I wrote about two months ago](https://www.nijho.lt/post/removing-guardrails/) feel like they barely matter any more. When I tell an agent not to merge a pull request, it just doesn’t, and it waits until I ask.

## Conclusion

I still have iTerm2 open all day. A year ago I cycled through five or six tabs every 10 to 15 minutes to see which agent was done. Now I open one room and look at Needs you.

Going all in on MindRoom also kick-started the best productivity optimization loop I’ve ever had. Before this, building my own development environment felt impractical, because I would have had to force myself to work inside an inferior tool (I hadn’t optimized MindRoom for coding yet), feel slow, and fall back to other apps. Now it’s genuinely the best place I can imagine developing in, so everything I find wrong with it, I fix right from inside it.

You can try the same view on [mindroom.chat](https://mindroom.chat/), and the [showcase](https://docs.mindroom.chat/showcase/) has recordings of what else it does.

I also wrote that [with every new model, my workflow changes](https://www.nijho.lt/post/how-to-start-with-ai/). So this is how I develop right now, and I expect it to look different in a few months.

[^1]: From the README of [pingdotgg/t3code](https://github.com/pingdotgg/t3code), read on November 20, 2026. T3 Code is MIT licensed.

[^2]: That model was Claude Opus 4.8, which did 17% less work and used 19% fewer tokens with Claude Code’s tools. GPT-6 Astra and Sol used 43 to 59% more tokens with the tools of their own harness.

[^3]: The skill is [`consulting-cross-model`](https://github.com/basnijholt/baspowers/tree/main/skills/consulting-cross-model). Claude asks GPT-6 Astra, and Codex asks Claude Opus 5.5.

[^4]: The line that’s usually quoted is “Measuring programming progress by lines of code is like measuring aircraft building progress by weight”, usually attributed to Bill Gates, though I couldn’t find a primary source for it.

[^5]: Counted on November 20, 2026 with `uvx trueloc count basnijholt --since 2024-11-01 --until 2026-11-20 --json`, run with my own GitHub login, so it covers every repository that account can see. Over the whole window that’s 7,630 merged pull requests and 12,233 direct commits with 15,304,504 lines: 10,886,530 added and 4,417,974 deleted. September 2026 has 2,459,033 lines, October has 2,829,709, and November up to the 20th has 3,966,635.

[^6]: Code files are the ones with one of 26 source extensions, such as `.py`, `.ts`, `.tsx`, `.rs`, `.nix`, `.sh` and `.css`. In the last twelve months that’s 6,707,616 of 9,957,695 lines (67%), and the rest is mostly JSON (11.7%), Markdown (9.2%) and SVG (4.4%). In the twelve months before, it was 832,382 of 1,380,174 lines (60%).

[^7]: The counted Needs you, Working, Later and Done filters are [mindroom-chat #436](https://github.com/mindroom-ai/mindroom-chat/pull/436), and the sections in the Compact view are [#448](https://github.com/mindroom-ai/mindroom-chat/pull/448). Both merged on November 17, 2026 (UTC).

[^8]: [mindroom-chat #419](https://github.com/mindroom-ai/mindroom-chat/pull/419) folds a finished reply behind the “Worked for” row, and [#670](https://github.com/mindroom-ai/mindroom-chat/pull/670) does that for every finished reply with a tool call.

[^9]: [mindroom-chat #562](https://github.com/mindroom-ai/mindroom-chat/pull/562).