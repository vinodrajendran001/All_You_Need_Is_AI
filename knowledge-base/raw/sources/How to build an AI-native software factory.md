---
title: "How to build an AI-native software factory"
source: "https://www.theaithinker.com/p/how-to-build-an-ai-native-software?utm_source=tldrai"
author:
  - "[[Adam Faik]]"
published: 2026-10-05
created: 2026-10-07
description: "Measure where your team’s work piles up. Put one bought agent on the toil nobody wants. Build only the platform that line needs. Track what merges, and what it costs."
tags:
  - "clippings"
---
### Measure where your team’s work piles up. Put one bought agent on the toil nobody wants. Build only the platform that line needs. Track what merges, and what it costs.

Everyone on your team already has Claude Code or Cursor. A few of them run three agents at once. Then leadership forwards you [Uber’s talk about its software factory](https://www.youtube.com/watch?v=17-YSUHo6Lk). The note says: where’s ours? Your first reaction is fair. You already bought the tools. **So what is left to build?**

The answer is the company part. A coding tool makes a single developer faster, inside their own session, on their own laptop. A company running hundreds of agents needs more than that. Work has to start from a ticket or an alert, with nobody at the keyboard. Agents have to run in the cloud, under rules every team shares. And someone has to be able to read the bill. **A software factory is that system around the agents, from the first idea to production.**

That raises the obvious question: do you have to write your own coding agent? Uber’s answer is no. Its developers use Claude Code, Codex and OpenCode, and none of its six building blocks is a coding agent. Other companies with a factory made the same call. **You keep buying the agent, and you build the setup around it, the factory floor.**

This article follows Uber through every step. Uber has published more about its factory than anyone else this year. There’s [a detailed post on what it costs to run](https://www.uber.com/us/en/blog/efficient-software-factory/), and two talks at AI Engineer. There are separate posts on code review, test generation, migrations and agent identity. Uber also sells no agents, so it has nothing to pitch. Still, none of this is a template to copy, because your company isn’t Uber. **At each step, you’ll see what Uber built first, then what other companies did, so you can take what fits your own context.**

So how do you start? First, measure where work waits today, from your own git history. Then put one bought agent on toil, the work nobody wants to do by hand. At Uber, agents took on migrations and code review well before feature work. Next, build only the platform that first line proves you need, usually a model gateway. Throughout, measure what merges, what it costs, and how often it breaks. **Uber prices every agent the same way: cost per unit of work, like cost per merged pull request.**

Here’s the route, in four stops.

![hand-drawn black-and-white infographic with four stops in a row, each labeled with a word or two: The why (a laptop with a small agent icon, and pull requests piling up in front of a narrow review gate), The agents on the line (a loop of six stations with a small agent icon at each), The floor (a stack of six blocks under a single agent icon), The rollout (a path climbing from one agent on a small task to a full loop, with a gauge beside it).](https://substackcdn.com/image/fetch/$s_!x8GC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff39abc87-14b1-43c1-90aa-61d4bbf0a1ca_2816x1536.png)

hand-drawn black-and-white infographic with four stops in a row, each labeled with a word or two: The why (a laptop with a small agent icon, and pull requests piling up in front of a narrow review gate), The agents on the line (a loop of six stations with a small agent icon at each), The floor (a stack of six blocks under a single agent icon), The rollout (a path climbing from one agent on a small task to a full loop, with a gauge beside it).

- **The why.** A coding tool speeds up one developer. A company hits four limits that no tool fixes alone.
- **The agents on the line.** Here’s Uber’s map of agents, one change followed end to end, and why the first agents took the toil.
- **The floor.** You’ll see Uber’s six building blocks, and which ones to buy or build.
- **The rollout.** The order that works, what to measure, and how to keep developers with you.

By the end, you’ll have a map of the six building blocks. Each one comes with a buy-or-build call. You’ll know which agent goes first, and what to measure once it runs. You’ll also have a plan for the developers who’d rather not change a thing. **Your developers keep the agents they like, and your company gets a factory that ships.**

This article draws on more than 70 public sources. Every one is listed at the end, grouped by company, so you can read the originals yourself.

Walk the floor with me.

---

## Why the coding tools stop short

A coding tool makes a developer faster. A company running dozens of agents hits four limits that no tool fixes alone. **Each limit is a reason to build the factory, and none of them is about the model.**

![hand-drawn black-and-white diagram with a laptop and a small robot at the center, and four branches leading to four small scenes, each with a short label. Review can't keep up: a tall pile of pull requests in front of one narrow gate. Laptops can't run a fleet: a cramped laptop with keys and a padlock spilling out of it. Nobody sees the bill: a long receipt unrolling off the edge. Every team its own way: three desks, each with a different rulebook.](https://substackcdn.com/image/fetch/$s_!VfQw!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd74ded25-5499-416d-ac44-d855b6efc679_2816x1536.png)

hand-drawn black-and-white diagram with a laptop and a small robot at the center, and four branches leading to four small scenes, each with a short label. Review can't keep up: a tall pile of pull requests in front of one narrow gate. Laptops can't run a fleet: a cramped laptop with keys and a padlock spilling out of it. Nobody sees the bill: a long receipt unrolling off the edge. Every team its own way: three desks, each with a different rulebook.

### Laptops can’t run a fleet

The first limit is where the agents run. At Uber, [a growing share of agent sessions](https://www.uber.com/us/en/blog/efficient-software-factory/) start without a human. Code review, CI fixes, on-call triage and maintenance start them. A laptop can’t do that, because it sleeps when its owner does. **Uber calls the move from laptops to managed agents its core strategic shift.** Managed environments, it says, give it *“complete control”* over model routing, harnesses and spend.

Two other companies hit the laptop wall from different sides:

- **DoorDash** worried about access. [Its platform team](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) points out that a laptop holds *“SSH keys, VPN sessions, and authenticated tools”*. Handing an autonomous agent that access means *“a potentially large blast radius”*.
- **Ramp** hit a ceiling on numbers. [Its engineers liked Claude Code from the start](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect), but on a laptop they could run only a couple of sessions.

### Every team invents its own way

The second limit is the quietest. Give a hundred developers a coding agent, and you get a hundred setups. At Uber, engineers built *[“tons of skills across many repositories”](https://www.youtube.com/watch?v=17-YSUHo6Lk)*. There was *“a lot of duplication”*, and many were of poor quality. Security rules end up in one team’s prompt and missing from the next. Anthropic’s [playbook](https://claude.com/blog/the-ai-native-sdlc-playbook) suggests the fix: write each rule once as a skill, and share it. **A factory is where the company’s way of working lives, once, for every agent.**

Adoption splinters the same way. By March, [92% of Uber’s developers used agents monthly](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development), yet adoption still came slower than expected. Google’s [DORA research](https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf) names the result: *“localized pockets of productivity”* that get lost downstream. **Fast individuals don’t add up to a fast company on their own.**

### Nobody sees the bill

When every developer picks a tool and a model, nobody sees the total until the invoice lands. Uber’s AI costs were [up 6x since 2024](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development) by March. By June, [it had spent its whole annual AI budget in four months](https://techcrunch.com/2026/06/02/uber-caps-employee-ai-spending-after-blowing-through-budget-in-four-months/). Much of the waste is invisible from a single laptop. **Uber’s session analysis flags simple sessions run on Opus that Sonnet could easily handle.** One developer can’t see that pattern, and a gateway sees all of it.

The goal is visibility, and a smaller bill can come second. Shopify’s Farhan Thawar [puts the trade plainly](https://www.firstround.com/ai/shopify):

> *“If your engineers are spending $1,000 per month more because of LLMs and they are 10% more productive, that’s too cheap.”*

You can only make that call if you know what each merged change cost. Individual licenses tell you the seat price. **A factory tells you the cost per outcome.** Without that number, the budget talk turns into a fight over seats.

### Review can’t keep up

The fourth limit appears once the first three are solved, and output goes up. Picture your team before the agents arrived, and then after.

![hand-drawn black-and-white diagram in two panels. Left panel, titled "Before": one developer at a keyboard writing code slowly, a short line of two pull requests, and a reviewer keeping up at a gate. Right panel, titled "After": one laptop with small agent icons writing in parallel, a tall stack of pull requests piled in front of a single narrow review gate, and a small label under the stack that reads "the new constraint".](https://substackcdn.com/image/fetch/$s_!HE_7!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e9918c5-4522-4298-a4c7-1edd03964ef9_2816x1536.png)

hand-drawn black-and-white diagram in two panels. Left panel, titled "Before": one developer at a keyboard writing code slowly, a short line of two pull requests, and a reviewer keeping up at a gate. Right panel, titled "After": one laptop with small agent icons writing in parallel, a tall stack of pull requests piled in front of a single narrow review gate, and a small label under the stack that reads "the new constraint".

Uber’s own review team [gave the numbers](https://ai.engineer/talks/EL123UNokkI-building-ureview-ubers-multi-agent-code-review) at AI Engineer in August:

> *“Back in 2024, we were seeing that engineers would get their first review within 3 hours. Now in 2026, that has grown to 9 hours.”*

More code reached the same number of reviewers. **More output doesn’t help if every change still waits for a person.** Spotify saw the same thing. After it adopted AI, [it had 76% more pull requests to review](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint). Across 22,000 developers, [Faros AI](https://www.faros.ai/blog/ai-acceleration-whiplash-takeaways), an engineering analytics company, measured a 441.5% rise in median time spent in review.

This is where the rule from [my earlier post on picking agents](https://www.theaithinker.com/p/how-to-pick-the-ai-agents-worth-building) applies. Find the one step everything waits on, and aim your next agent at it. A software factory does that for the whole line, from idea to production. Review is the slow step for many teams today. Uber says its next ones are CI capacity, experiment slots, and deciding what to build. **The factory is how you keep finding the slow step, and moving it.**

So which agents go on the line, and where do they plug in? Start with Uber’s map.

---

## The agents on the line

In this article, a line means one agent with one job, like reviewing pull requests or cleaning up old feature flags. Uber runs a small set of these agents across its whole SDLC, plus one front door. Look at the map first. Then follow one feature through it, and see why the first agents took the toil.

### Map the four layers first

Uber drew its map as [Figure 3 of its efficiency post](https://www.uber.com/us/en/blog/efficient-software-factory/). It sorts every agent session into four layers, from the most specialized to the most general. In Uber’s words, *“the higher the layer, the more control we have over cost, quality, and model selection”*. **Picture your own company on that map before you build anything.**

![hand-drawn black-and-white diagram of four stacked horizontal bands. The top band holds five small boxes, one per specialized agent, each with a tiny price tag. The second band is one wide doorway with a single robot greeting a queue of requests. The third band is a laptop with a shelf of shared skill books beside it. The bottom band is a plain laptop with a developer typing, labeled as the open space for everything else. A thin arrow runs up the left side from the bottom band to the top one.](https://substackcdn.com/image/fetch/$s_!3iay!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1522928-0aec-4344-8ced-fbe79562ae61_2816x1536.png)

hand-drawn black-and-white diagram of four stacked horizontal bands. The top band holds five small boxes, one per specialized agent, each with a tiny price tag. The second band is one wide doorway with a single robot greeting a queue of requests. The third band is a laptop with a shelf of shared skill books beside it. The bottom band is a plain laptop with a developer typing, labeled as the open space for everything else. A thin arrow runs up the left side from the bottom band to the top one.

Here are the four layers, top to bottom:

- **Specialized agents.** A handful of agents, each built for one narrow job. They run in Uber’s cloud, with a person in the loop. Minion turns an intent into a pull request, and uReview reviews it. Agentic XP writes up experiment results. Conan AI finds the root cause of an alert, and Fawkes runs scheduled maintenance. Each has its own unit price: cost per merged pull request, per review, per alert, per cleanup.
- **One general agent.** Cortana is the single front door. It runs in Uber’s cloud and needs no setup. It can use any skill in the company’s marketplace. Its unit is cost per query.
- **Sessions with skills.** A developer’s own session on a laptop, loaded with the same shared skills. Uber counts more than 3,600 of them.
- **Raw sessions.** Claude Code, Codex or OpenCode with nothing added. The developer supplies the prompt, the context and the steering.

Three choices stand out. Five specialized agents cover code generation, validation, deploy, observation and maintenance for the whole company. There is no agent per team. Requests have one front door, so nobody hunts for the right bot. **And the coding tools stay, at the bottom, for everything that doesn’t fit a lane yet.** That’s the answer to the developer who fears the factory takes away their tools.

**Read the map from the bottom up, and it’s also a path.** A task starts in a raw session. Once several people do it the same way, it becomes a shared skill. Once it runs often enough to benchmark, it earns a specialized agent. Uber’s figure gives the rule for the top layer: pick the narrowest task and build a real benchmark. Then run the Pareto-optimal model, the one with the best trade-off between cost and quality. *“Every dollar maps to a unit of work.”*

You won’t start with five. If your team runs Claude Code or Cursor today, it lives in the bottom two layers. A shared skills folder is the cheapest step up. Your first line on toil becomes your first specialized agent. **Keep the bottom layer open, because that’s where the next specialized agent gets discovered.**

How others built their layers:

- **Shopify** started with the front door. [River](https://shopify.engineering/under-the-river) is one agent in the company Slack, and it only works in public channels. It now co-authors one in eight merged pull requests. Then teams asked for their own review, research and migration agents. Shopify’s take: *“We had not built a thing that could be a hundred Rivers.”* So it built the platform underneath.
- **DoorDash** built the skills layer with permissions attached. On [its Flux platform](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/), a playbook is *“a reusable unit of agentic work”*. Each playbook declares the tools it needs, and gets only those permissions.
- **Spotify** went straight to one specialized lane. [Honk](https://engineering.atspotify.com/2026/4/background-coding-agents-dataset-migrations-honk-part-4), its background agent, does fleet-wide maintenance. For one dataset change, it migrated about 1,800 downstream pipelines. At the time, Honk had no access to shared skills, a choice Spotify made to keep its outcomes predictable.

### Follow one change from idea to incident

At AI Engineer, [Adam Huda walked one feature through Uber’s factory](https://www.youtube.com/watch?v=17-YSUHo6Lk). The idea fits the moment. A rider leaving a packed World Cup stadium gets a better pickup spot, away from the crowd. Here’s that one feature, step by step:

- **Idea.** The team jams on it in a Slack thread and tags Cortana. Cortana checks the context graph for past large-venue events, and for the stadiums where this would matter. That research points to a North America rollout, since that’s where the stadiums are. Cortana then drafts two Figma mock-ups for an A/B test, each with a different button text. It also lists the existing screens and backend services the feature can reuse. Huda says getting everyone aligned on this used to take weeks.
- **Build.** Cortana hands off to Minion, Uber’s cloud coding agent, running in a DevPod. Minion writes the backend change and the front-end change for the new pickup screen, across repositories. It stops at a draft pull request and doesn’t push to CI yet. Toil can go straight through, but a new feature gets checked first, so CI doesn’t take the extra load.
- **Validate.** The checks move earlier, before CI. A skill launches the app in a simulator, grabs a screenshot of the pickup screen, and compares it to the Figma mock-up. Another brings the service up in staging, to test the new front end against the new backend.
- **Review.** A faster, medium-sized model reviews the change before it reaches CI. A stronger reasoning model does a deeper pass in CI.
- **CI.** When the build fails, self-healing CI fixes many of the errors on its own.
- **Hand-off.** The pull request reaches a person with a table of every check it passed, simulator screenshots included. **That table gives the human reviewer a reason to trust the diff.**
- **Maintain.** The experiment ends, and variant B is no longer needed. Its feature flag goes on a managed cleanup loop. The loop runs over the weekend, when CI has spare capacity, and caps how many diffs land on engineers when they’re back. Whether those diffs land or get rejected becomes data to improve the cleanup skill.
- **Incident.** Once a month, Uber reads its incident reviews for patterns. Each one it can catch becomes a new maintenance skill, applied to every service.

![hand-drawn black-and-white loop diagram titled "One change, from idea to incident". Six stations sit around an oval track, each with a small robot at a desk: Plan, Design, Build, Test, Review, Maintain. Between the stations, file icons show what each stage hands on: intent.md, spec.md, plan.md, code plus tests, PR, incident. A human hand marks three gates on the track: Accept, Approve plan, Approve merge. An arrow from Maintain back to Plan is labeled "New intent".](https://substackcdn.com/image/fetch/$s_!aKoT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd27a3efb-864e-4c1d-8a93-2d572d172b43_2816x1536.png)

hand-drawn black-and-white loop diagram titled "One change, from idea to incident". Six stations sit around an oval track, each with a small robot at a desk: Plan, Design, Build, Test, Review, Maintain. Between the stations, file icons show what each stage hands on: intent.md, spec.md, plan.md, code plus tests, PR, incident. A human hand marks three gates on the track: Accept, Approve plan, Approve merge. An arrow from Maintain back to Plan is labeled "New intent".

Anthropic wrote the same loop down as a [playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), by Louis Claxton. Anthropic sells the agent it runs on, so read it for the shape. Each stage writes one file to version control, and the next stage starts by reading it. An idea becomes `intent.md`, then `spec.md`, then `plan.md`, then code and tests, a pull request, and an incident record. People sit at three gates: accepting the intent, approving the plan, and approving the merge. **The playbook’s own advice is to prompt each stage by hand first, and automate the loop last.**

How others run the same stages:

- **Stripe.** [Its Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) merge over 1,300 pull requests a week with no human-written code. A person still reviews every one.
- **Spotify.** [Its background agent](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3) runs verifiers on every change. A model acting as judge vetoes about a quarter of sessions, and the agent then corrects course half the time.
- **DoorDash.** [It splits review in two](https://careersatdoordash.com/blog/how-we-learned-to-trust-our-ai-code-reviewer-at-doordash/). A scout flags suspicious areas, and deeper reviewers check each lead.

### Put the first agent on toil

So which stage goes first? At Uber, the answer was the toil. The [Google SRE book](https://sre.google/sre-book/eliminating-toil/) defines it in one sentence worth keeping:

> *“Toil is the kind of work tied to running a production service that tends to be manual, repetitive, automatable, tactical, devoid of enduring value, and that scales linearly as a service grows.”*

Uber has run more than 250 automated migrations, touching 9 million lines of code. Minion builds features too, but for anything past toil it stops at a draft pull request. Uber wants to validate those features before they load up CI. **Pick the line where a wrong answer is cheap and a right one is obvious.** Use the SRE sentence as a checklist, and add one test: “done” must be easy to check.

Toil still needs the right tool, and Uber learned that the hard way. For its JUnit 5 migration, [Uber tried generative AI first](https://www.uber.com/us/en/blog/junit-migration/):

> *“We attempted to use generative AI to migrate multiple test class files at once, but this approach was unsuccessful.”*

So Uber switched to a deterministic approach. An internal tool for large code changes, called Shepherd, generated over 5,000 diffs. AI only helped debug the test and build failures. More than 75,000 test classes moved in four months. **When you can write the rule, write the rule.** Save the agent for what the rule can’t reach.

How others picked their first line:

- **DoorDash** started with code review. [Its platform team](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) says review *“was frequent, measurable, and easy for engineers to evaluate”*.
- **Spotify** started with migrations. [Its agents’ first 1,500 merged pull requests](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) came from them, at 60% to 90% less time than by hand.

You can run that first line on an agent you buy. Claude Code on the web, Copilot cloud agent and Cursor’s cloud agents all fit. Each runs the task in an isolated machine and hands back a pull request. **Start it in shadow mode, where it comments and nobody has to act.** If your first line lives in CI, the playbook’s smallest move is a read-only job. `claude -p` runs Claude Code inside a script, with no chat window:

> *“Use claude -p in a pipeline job to triage a failed build, summarize a flaky test, or draft the changelog.”*

It reads and it reports. **Nothing ships until a person says so.** Once that first line earns trust, the next question is what to add.

### More agents worth trying

Before you add another agent, ask what it adds to review and to CI. The agents that take load off people go first. Uber already runs these four:

- **Review routing.** [Code Inbox](https://background-agents.com/summit/sessions/nikhil-ramakrishnan/) sends each pull request to the reviewer best placed to read it. It drains the review queue faster.
- **Orchestrated migrations.** Shepherd picks the targets, and Minion handles the odd cases. Plan an auto-merge rule for the safe diffs.
- **Feature-flag cleanup.** A managed loop removes stale flags when CI has spare capacity.
- **Design specs.** [uSpec](https://www.uber.com/us/en/blog/automate-design-specs/) connects an agent in Cursor to Figma and writes design-system specs. A full screen-reader spec for three platforms takes under two minutes.

And three agents from other companies:

- **Fix on request, at DoorDash.** On any review comment, from the agent or a person, anyone can tag the agent in the pull request thread. *“Can you handle the nil check here?”* [A fixer makes the change](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) in a remote machine and pushes it back to the pull request. Claude Code on the web [sells the same move](https://code.claude.com/docs/en/claude-code-on-the-web).
- **Security scans, from Anthropic’s playbook.** A scheduled agent scans your most critical repositories. The [playbook](https://claude.com/blog/the-ai-native-sdlc-playbook) says the first scan will flag code everyone thought was clean. Anthropic sells a scanner, so read that with care.
- **Fraud checks, at Warp.** [Warp runs a fraud-bot every 8 hours](https://www.warp.dev/blog/oz-orchestration-platform-cloud-agents). In one run, it caught nearly $60K of fraudulent usage and wrote the fixes. Warp sells the platform it runs on.

Each of these agents needs the same things underneath. It needs a place to run, tools to reach, and rules it can’t break. **That’s the floor.** Pop the hood and look at what it’s made of.

---

## The six building blocks under the agent

Uber gave the clearest tour of its platform at AI Engineer in August. [Uday Kiran Medisetty and Adam Huda](https://www.youtube.com/watch?v=17-YSUHo6Lk) walked through six building blocks. **None of the six is the coding agent itself.** First came a model gateway and an MCP gateway. Then cloud dev environments, called DevPods, and a skills marketplace. Last came a context graph and Cortana, the front-door assistant.

Uber built all this on six years of platform work, and said so on stage. You won’t need all six blocks to start. **Most companies begin with the gateway.**

Here are all six in one picture.

![hand-drawn black-and-white stack diagram. At the top, a row of entry points: Slack, tickets, CI events, schedules. In the middle, a box labeled "harness" running a single coding agent icon marked "bought". Underneath, four blocks side by side: model gateway, sandbox with warm snapshot, tool gateway and catalog, context layer. Along the right edge, a tall vertical bar labeled "gates, identity, observability" that touches every layer.](https://substackcdn.com/image/fetch/$s_!Yp-3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa17b4db8-0b6d-4584-8ea2-2acc266d1b83_2816x1536.png)

hand-drawn black-and-white stack diagram. At the top, a row of entry points: Slack, tickets, CI events, schedules. In the middle, a box labeled "harness" running a single coding agent icon marked "bought". Underneath, four blocks side by side: model gateway, sandbox with warm snapshot, tool gateway and catalog, context layer. Along the right edge, a tall vertical bar labeled "gates, identity, observability" that touches every layer.

### Where the agent runs

The model gateway came first at Uber. It’s one door that every model call goes through, whatever the vendor. Uber’s gateway has three jobs, per Medisetty. Personal data stays inside by default. Guardrails add a delay with a strict ceiling. **And every request is tied to a user, a project and a team.** More than 800 internal projects send it over 100 million requests a day.

You can buy this block. [LiteLLM](https://docs.litellm.ai/docs/simple_proxy) is open source. It handles keys, per-user budgets, and spend across 100-plus models. [Portkey](https://portkey.ai/docs/product/ai-gateway), [Kong](https://developer.konghq.com/ai-gateway/) and [Cloudflare](https://developers.cloudflare.com/ai-gateway/) sell the same features. AWS does it in Bedrock with [inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles.html). **Start small: route a single team’s keys through it, with a budget per person.**

The real lesson from LiteLLM is about deployment. In March 2026, [two poisoned releases sat on PyPI for about 40 minutes](https://docs.litellm.ai/blog/security-update-march-2026). Teams on the official Docker image were safe, because it pins its dependencies. [Datadog’s analysis](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/) shows what the releases took: cloud keys, SSH keys, Kubernetes data and CI secrets. A gateway holds every provider key you own. **Treat it as the most sensitive box on your diagram.** Pin it, patch it, and give it an owner.

The second block is the sandbox, an isolated machine where the agent works. Uber’s version is the DevPod. Uber keeps a pool of machines ready, with every repository already copied in and the search index already built. Agents can start working within seconds. For cross-repository work, a single large DevPod holds all of Uber’s code. **Speed matters more than you’d think, because nobody waits for a slow sandbox.**

How others run theirs:

- **Stripe.** [Its devboxes](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) spin up in 10 seconds, with code and services loaded.
- **DoorDash.** [Its target](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) is under five seconds, from cold machine to working agent.
- **Ramp.** [It rebuilds its images every 30 minutes](https://builders.ramp.com/post/why-we-built-our-background-agent), so each session starts on fresh code.

The machines themselves are for sale. [AWS AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html) gives each session its own microVM, a small virtual machine, for up to 8 hours. [Modal](https://modal.com/docs/guide/sandboxes), [E2B](https://docs.e2b.dev/), [Daytona](https://www.daytona.io/docs/en/), [Ona](https://ona.com/docs/ona/getting-started) and [Coder](https://coder.com/docs/ai-coder) sell sandboxes too. None of them sells your repository, installed, built and ready. **The machine is a commodity, and the warm snapshot of your code is yours to build.** A running agent still needs a way into your systems.

### What the agent can reach

The third block is the tool catalog. Agents reach your systems through [MCP](https://modelcontextprotocol.io/docs/getting-started/intro), the Model Context Protocol. It’s an open standard for plugging tools into an agent. Uber had thousands of internal APIs, and none were ready for agents. So it built an MCP gateway with a crawler. **One config change turns an internal API into a tool.**

Tools cost tokens, though. Each one comes with a description the agent has to read. At Uber, 100-plus tools [added 50,000 to 70,000 tokens](https://www.uber.com/us/en/blog/efficient-software-factory/) to every prompt. Uber’s fix was to turn its 1,000-plus tools into commands. The agent looks one up only when it needs it. **A big catalog is fine, as long as each agent loads only the tools it needs.**

Stripe reached the same rule from the other end. Its catalog, [Toolshed](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2), holds nearly 500 tools. Yet each agent starts with *“an intentionally small subset of tools by default”*. You can buy the pipes for this block: [Docker’s MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/), [AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) and [Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/agents/overview) all sell one. **What you can’t buy is the list of tools your company needs.**

The fourth block is context, and it decides whether the agent guesses. Uber gave the same data question to two agents. One could query its context graph, and one couldn’t. The grounded agent found the right table in 38 seconds. The other spent 20 minutes, hit three errors, and said the data couldn’t be queried. Uber’s summary: *“An ungrounded agent fails slowly rather than cheaply”*. **Context is a platform job, done once, for every agent.**

Uber’s graph links 24 million nodes from over 30 internal systems. **You can start far smaller.** [Meta had 50-plus agents read one large codebase](https://engineering.fb.com/2026/04/06/developer-tools/how-meta-used-ai-to-map-tribal-knowledge-in-large-scale-data-pipelines/) and write 59 short context files. In early tests, Meta’s agents then made 40% fewer tool calls per task. At the smallest scale, context is a `CLAUDE.md` file that Claude Code reads first. Keep it under a page. Reach and context make an agent useful, and the last two blocks keep it safe.

### What keeps it in bounds

The fifth block is the harness: the loop that runs the agent, plus the triggers that start it. Uber runs its managed agents on a harness that serves any model, frontier or open-weight, behind one interface. Then it benchmarks each agent on its own real work and moves to the best model for that job. Triggers come from Slack, CI, schedules and alerts. **What stays yours is the order of steps your company trusts.**

Stripe [calls that order a blueprint](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2): *“workflows defined in code that direct a minion run”*. Some steps are plain code, like running the linter at the end. Others are agent steps, where the task needs judgment. The plain steps save tokens, and give the agent *“a little less opportunity to get things wrong”*. **A skill is guidance the agent will probably follow, and a hook can block it.**

The sixth block is the gates, starting with identity. At Uber, [a pull request once named a “Monitoring Agent” as its author](https://www.uber.com/us/en/blog/solving-the-agent-identity-crisis/). The engineer who asked for it was gone from the record. Uber’s fix issues short-lived, scoped tokens at every hop, so the chain back to the person survives. Thousands of internal agents now use it. **Give each agent its own identity, with only the rights its job needs.** Anthropic learned the same lesson when its incident agent [asked another Claude instance to push a fix](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle), and a human review gate caught it.

The last gate sits in front of production. Anthropic’s playbook puts it in one line: the agent *“may act up to the production gate and cannot pass it”*. Everything the agent writes arrives as a pull request, and the agent that wrote the code can’t approve it. Ramp opens each pull request as the person who started the session, [so nobody approves their own change](https://builders.ramp.com/post/why-we-built-our-background-agent). Log every tool call through [OpenTelemetry](https://github.com/open-telemetry/semantic-conventions-genai), the open standard for traces. **Gates are what let you say yes to more agents.**

The incidents show what happens without them:

- **Replit.** An agent [deleted a production database](https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/) during a code freeze.
- **AWS.** A coding tool [chose to “delete and recreate”](https://the-decoder.com/aws-ai-coding-tool-decided-to-delete-and-recreate-a-customer-facing-system-causing-13-hour-outage-report-says/) a customer-facing system.
- **GitHub MCP.** [A malicious public issue hijacked an agent](https://invariantlabs.ai/blog/mcp-github-vulnerability) and leaked private data.

That last one fits a factory exactly, because your agents will read tickets. Meta’s [Rule of Two](https://ai.meta.com/blog/practical-ai-agent-security/) is the defense worth pinning up. In one session, an agent may have at most two of three powers:

- Reading untrusted input, like a public issue or a customer ticket.
- Reaching sensitive systems or private data.
- Changing things, or talking to the outside world.

Need all three? Then a person supervises that session. With all six blocks named, one decision is left: what to buy.

### What to buy and what to build

A word before the split. What follows is a direction drawn from what these companies published, not a recipe. Your stack, your team and your risks are different from theirs. **Treat it as a starting point for your own discussion, and make the call with your own numbers.**

Here’s the whole thing as one decision. Start with option zero: buy it all as a hosted background agent. Claude Code on the web, Copilot, Cursor and Devin each bundle a sandbox, triggers and the pull request flow. You give up control of the snapshot, the tools and the limits. [Copilot’s cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent), for example, stops at 59 minutes and works in one repository per run. **Option zero shows you what your floor needs before you build any of it.**

When you outgrow it, split the work like this.

![hand-drawn black-and-white diagram titled "What to buy, what to build". A top banner shows a cloud holding a small robot and a checked document, labeled "Option zero: a hosted agent" with the caption "Start here, learn what you need". Below it, two columns. Buy, with a shopping-cart icon: coding agent, model gateway, sandbox, tracing, review agent. Build, with a hammer icon: warm snapshot, tool catalog, context, blueprints, gate policy. Thin arrows run from the build items to the bought parts they plug into.](https://substackcdn.com/image/fetch/$s_!lj3W!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F77b7030d-5e66-4c58-89de-94ff45f24d17_2816x1536.png)

hand-drawn black-and-white diagram titled "What to buy, what to build". A top banner shows a cloud holding a small robot and a checked document, labeled "Option zero: a hosted agent" with the caption "Start here, learn what you need". Below it, two columns. Buy, with a shopping-cart icon: coding agent, model gateway, sandbox, tracing, review agent. Build, with a hammer icon: warm snapshot, tool catalog, context, blueprints, gate policy. Thin arrows run from the build items to the bought parts they plug into.

Buy the pipes: the agent, the gateway, the sandbox, the tracing, and the reviewer. **Then build what only your company knows.** That means your code’s warm snapshot, your tool catalog, and your context. It also means the blueprints that encode your SDLC, and the gate policy. You don’t need all of it on day one. [Team Topologies](https://teamtopologies.com/key-concepts-content/what-is-a-thinnest-viable-platform-tvp), a well-known book on organizing software teams, calls this a thinnest viable platform. That’s the smallest set of shared tools that makes other teams faster, run like a product for its users. Here, it means building only the blocks your first agent needs, and adding the next one when a team asks for it.

Uber’s floor took years, but **the build can be smaller than that.** Ramp’s Inspect team was [5.5 people](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect): four engineers, a director and a part-time PM. Two months after its v2 launch, Inspect wrote about 60% of Ramp’s pull requests. By May, it was 75%.

The sharpest warning comes from Prince Valluri at LinkedIn, [on InfoQ](https://www.infoq.com/podcasts/platform-engineering-scaling-agents/):

> *“Don’t try to recreate GitHub Copilot or Cursor or Replit inside your company.”*

He’s right, and that’s the whole split. **Buy the agent, and build what it stands on.** The map is done. The harder part is starting it without losing the people it’s for.

---

## Roll it out without losing developers

One honest gap first. Every public case here is a large tech company with a platform team. None describes a 300-engineer company starting from laptops. So the order below asks for the least before it proves anything. It borrows Uber’s map at a smaller scale. Each step has one number that says it worked. **Move to the next step only when the current number moves.**

![hand-drawn black-and-white diagram of five steps on a rising path. Step 1: measure the queue you have. Step 2: one agent on toil, bought, in shadow mode. Step 3: the floor that line proves you need, gateway first. Step 4: gates and the loop. Step 5: more lines, each checked against the review queue. Beside each step sits a small gauge icon naming its metric: time to first review; share of agent comments acted on; cost per session; sessions that end in a merged PR, next to revert rate; change fail rate.](https://substackcdn.com/image/fetch/$s_!VZDB!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b9405d5-4295-4007-96d8-1cb54b4ea344_2816x1536.png)

hand-drawn black-and-white diagram of five steps on a rising path. Step 1: measure the queue you have. Step 2: one agent on toil, bought, in shadow mode. Step 3: the floor that line proves you need, gateway first. Step 4: gates and the loop. Step 5: more lines, each checked against the review queue. Beside each step sits a small gauge icon naming its metric: time to first review; share of agent comments acted on; cost per session; sessions that end in a merged PR, next to revert rate; change fail rate.

The sequence starts with where work waits today and ends with more lines. **In between, you prove one agent on toil, then build only what it needs.** Whoever owns the gates should read [how Anthropic secures its own pipeline](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle). It’s a vendor writing about itself, and still the clearest account of shadow mode and risk tiers. The first step, though, needs nothing at all.

### Start with the queue you already have

The first move costs almost nothing and needs no vendor. Work waits in several places: review, CI, deploys. Review is the easiest wait to read from git, so start there. **Measure your review queue from your own git history.** Ask a teammate to run this prompt in Claude Code, on a repository you own. I ran it on the public repository of [PostHog](https://github.com/PostHog/posthog), an open-source analytics company:

```markup
Using the GitHub CLI, look at the last 200 merged pull requests in the PostHog/posthog repository. For each one, find how many hours passed between the pull request opening and its first review from someone other than the author. Then tell me: the median and the 90th percentile of that wait, the share of pull requests that merged with no review at all, and the share that changed more than 400 lines. Show me the numbers in a short list, then one sentence on where the queue is.
```

Claude Code’s answer, word for word:

> **Wait until first human review, in hours:**
> 
> - **Median wait:** 6.1 hours
> - **90th percentile wait:** 160.8 hours (about 6.7 days)
> - **Merged with no human review:** 40.0% (80 of 200)
> - **Changed more than 400 lines:** 28.5% (57 of 200)
> 
> Most PRs that get a human review get one within the working day, but the queue has a long tail and a large group that merges without any human review.
> 
> These 200 PRs merged between Sept 28, 16:41 and Sept 29, 14:21 UTC. PostHog merges about 200 PRs a day, so this covers roughly one day. “Lines changed” means additions plus deletions.
> 
> I left bot reviewers out: coderabbitai, stamphog, greptile-apps, copilot, veria-ai, the codex connector and the posthog bot. They review nearly every PR within minutes. If you count them, the median wait drops to 0.07 hours (about 4 minutes), the 90th percentile to 0.53 hours, and no PR merged without a review. The bot-free numbers are the ones that describe the human queue.
> 
> In the “someone other than the author” check, 23 of the PRs were opened by bots. I kept them in the sample.

The run took about six minutes and cost 25 cents. Half the pull requests got a person within six hours. The slowest tenth waited almost a week. And 40% merged with no human review at all. PostHog runs several review bots, and they looked at nearly every pull request within minutes. **The bots already clear their part, so measure the human queue.**

The sample covers about one day of PostHog’s merges. Read it as a demo of the prompt, and run it on your own repositories. **Write the numbers down, because every later step is judged against them.** Watch the share of big pull requests too. [DORA’s AI capabilities model](https://services.google.com/fh/files/misc/2025_dora_ai_capabilities_model.pdf) lists working in small batches among its seven capabilities. Small batches counter *“the risk of AI generating large, unstable changes”*. With a baseline written down, you need the scorecard that sits on top of it.

### Measure merged work, not code written

Uber’s scorecard is a good place to start thinking. Keep its shape, then pick numbers that fit your own work. [Every managed agent](https://www.uber.com/us/en/blog/efficient-software-factory/) reports three kinds of numbers:

- **Cost per outcome.** Cost per merged pull request, per review, per alert, per cleanup.
- **Quality.** Revert rate, F1 for reviewers, and time to recover from incidents.
- **Volume.** Diffs landed, reviews posted, alerts triaged.

**A throughput number without a quality number beside it invites people to game it.** Uber also shows why “% of code written by AI” is a weak headline. In August, [it said more than 70%](https://www.uber.com/us/en/blog/efficient-software-factory/) of its pull requests involved agents. In May, its background-agent team talked about [11% of merged pull requests](https://background-agents.com/summit/sessions/nikhil-ramakrishnan/). The number moved sixfold inside one company, depending on what was counted.

Cost needs its own line, because it moves fast. After its budget overrun, Uber [capped spend at $1,500 a month](https://techcrunch.com/2026/06/02/uber-caps-employee-ai-spending-after-blowing-through-budget-in-four-months/) per employee, per coding tool. Its later approach was gentler. Engineers see spend live, with nudges at 50%, 80% and 100% of plan. Since June, Uber’s cost per session has fallen 52% from its peak. **Visibility did more than the cap.**

The harder question is still open. Andrew Macdonald at Uber said it’s *[“very hard to draw a line”](https://fortune.com/2026/05/26/uber-coo-ai-spending-tokens-claude-code/)* from usage to useful features. **Measure cost per outcome, or you won’t be able to answer that question either.**

How others keep score:

- **Ramp** tracks sessions that end in a merged pull request. It calls that *[“the most important metric to track”](https://builders.ramp.com/post/why-we-built-our-background-agent)*.
- **Intercom** aimed to double merged pull requests per R&D employee, and [tripled them in 16 months](https://ideas.fin.ai/p/2x-nine-months-later). [AI-authored backend code was reverted 0.53% of the time](https://www.intercom.com/blog/ai-is-approving-our-pull-requests-heres-how-we-made-it-safe/), against 5.39% for human code.
- **DX**, a developer-productivity firm, publishes [a full AI measurement framework](https://getdx.com/blog/ai-measurement-framework-guide/), split into utilization, impact and cost. Pick a couple of metrics from each group.
- **Meta and Amazon** show what to skip: token leaderboards. Meta’s [came down](https://fortune.com/2026/05/12/amazon-tokenmaxxing-claude-ai-capex-meta-gil-luria/) after press reports, and at Amazon employees ran trivial tasks to climb theirs.

The numbers keep the factory honest, and people decide whether it gets used.

### Bring developers along

Now the part most rollouts get wrong. Developers can reject a factory fast, and some objections run deeper than tooling. One Anthropic engineer said it plainly to [the company’s own researchers](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic):

> *“It’s the end of an era for me - I’ve been programming for 25 years, and feeling competent in that skill set is a core part of my professional satisfaction.”*

Charity Majors, who co-founded the observability company Honeycomb, asks the professional version. *[“What would it take for you to be fully comfortable shipping code you have not read?”](https://newsletter.pragmaticengineer.com/p/stop-being-skeptical-about-ai-for)* Neither of them is wrong. **Take both seriously, because the people asking are your best reviewers.** Four moves show up again and again in the companies that got adoption right.

![hand-drawn black-and-white diagram of four tiles in a two-by-two grid, each with a small icon and a one-line label underneath. Tile 1, "Take their toil first" (a broom sweeping away a pile of small tasks). Tile 2, "Work in the open" (a public chat thread with several people watching an agent's work). Tile 3, "Let them opt in" (an open door with a hand choosing to walk through). Tile 4, "Give them the gates" (a person holding a key in front of a gate labeled merge).](https://substackcdn.com/image/fetch/$s_!TYwH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5dc348be-36a3-41ba-ad5c-3d5bb6d355fa_2816x1536.png)

hand-drawn black-and-white diagram of four tiles in a two-by-two grid, each with a small icon and a one-line label underneath. Tile 1, "Take their toil first" (a broom sweeping away a pile of small tasks). Tile 2, "Work in the open" (a public chat thread with several people watching an agent's work). Tile 3, "Let them opt in" (an open door with a hand choosing to walk through). Tile 4, "Give them the gates" (a person holding a key in front of a gate labeled merge).

**Take their toil first.** Uber moved *“upgrades, migrations, bug fixes”* to AI. The result was *[“much higher satisfaction from our engineers”](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development)*. Flag cleanup and test migrations are work nobody on your team will miss. The agent takes a chore off a real person’s plate, in front of their teammates. **Relief is the fastest route to trust.**

**Work in the open.** At Uber, Cortana works in team Slack channels, so its answers are visible to the whole team. Uber’s own lesson, [reported by Gergely Orosz](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development): *“Top-down mandates are less efficient than engineers sharing their wins with peers.”* DoorDash learned the same thing. Its first Slack integration gave each agent run a private channel, and [it](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/) *[“did not create team habits”](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/)*. Public threads changed that. **People copy what they can see their colleagues doing.**

**Let them opt in.** [Ramp says](https://builders.ramp.com/post/why-we-built-our-background-agent) it *“didn’t force anyone to use Inspect over their own tools”*. Inspect still ended up writing most of its pull requests. Forcing it has a worse record. Duolingo’s Luis von Ahn dropped AI usage from performance reviews, [saying](https://finance.yahoo.com/sectors/technology/articles/m-not-going-force-duolingo-170215712.html) *“I’m not going to force you”*. **A mandate gets you usage numbers, which is the metric you just decided to ignore.**

**Give them the gates.** At Uber, every agent pull request carries a table of the checks it passed, screenshots included. The reviewer sees the evidence before reading the diff. Anthropic’s playbook goes one step further: the tech lead writes the review policy in a file called `REVIEW.md`. The agent never approves its own work, so a person stays accountable for every merge. **Developers keep the judgment, and the agents take the typing.**

When a developer asks why now, skip the fear pitch. Zach Lloyd, who builds Warp, [made a prediction at AI Engineer](https://ai.engineer/talks/tUPPVhBBcoM). Every company, he said, will have *“at its core a software factory”*, the way it has CI/CD. He sells one, so weigh it. The better evidence is the work nobody does by hand anymore. Spotify has merged [over 2.5 million automated maintenance pull requests](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint), most with no human in the loop. **The craft is moving from typing the code to designing the line that types it.**

That’s the whole route. Here it is as a checklist you can carry into the room.

---

## Start with one line

Your developers already have the agent. That part is solved, and a better one ships every few months. What’s left is the floor. That’s where the agent runs, what it can reach, and the rules it can’t break. Then come the numbers that say it’s working. The rule from that earlier post still holds, too. **Find the step everything waits on, and keep moving it.**

If you need one line for the room, use this one:

> *Our engineers already have the agent. We’re building the floor it works on, and we start with the one job nobody wants to do by hand.*

Here’s the route as a checklist:

- **Measure.** Find where work waits today. Time to first review is the easiest first number.
- **Pick the line.** Choose one toil task that passes the SRE test and has an easy “done”.
- **Buy the agent.** Run the line on a hosted background agent, in shadow mode.
- **Build the thinnest floor.** Add a model gateway first, then only what the line proves it needs.
- **Gate it.** Give each agent one identity, no path past production, and no way to approve itself.
- **Score it.** Track cost per outcome, next to revert rate.
- **Work in the open.** Use public threads and opt-in, and let the tech lead own the review policy.
- **Add the next line.** Only when review and CI can take the extra load.

Uber’s team ended its talk on the question that comes after all of this. Once you can build almost anything, the question changes. Adam Huda put it this way: *[“it’s more of a question of should we build it”](https://www.youtube.com/watch?v=17-YSUHo6Lk)*. That’s a product question, and it sits upstream of every line you add. **It’s also the part of the factory that was always yours.**

---

## Go further: every source, by company

Here’s every link this article used, plus a few that didn’t fit in. They’re grouped by company, then by building block. Vendor posts about their own products are marked.

**Uber**

- [The efficient software factory](https://www.uber.com/us/en/blog/efficient-software-factory/): the four layers, the scorecard per agent, and the cost numbers (August 2026).
- [The six building blocks talk](https://www.youtube.com/watch?v=17-YSUHo6Lk): Uday Kiran Medisetty and Adam Huda at AI Engineer, with the World Cup pickup example.
- [Building uReview](https://www.youtube.com/watch?v=EL123UNokkI): the code review talk, where first review went from 3 to 9 hours ([talk page](https://ai.engineer/talks/EL123UNokkI-building-ureview-ubers-multi-agent-code-review)).
- [uReview](https://www.uber.com/us/en/blog/ureview/): the review agent’s design, and which comments developers acted on (2025).
- [The JUnit 5 migration](https://www.uber.com/us/en/blog/junit-migration/): why a deterministic tool beat generative AI on 75,000 test classes.
- [uSpec](https://www.uber.com/us/en/blog/automate-design-specs/): an agent in Cursor that writes design-system specs from Figma.
- [Solving the agent identity crisis](https://www.uber.com/us/en/blog/solving-the-agent-identity-crisis/): scoped tokens that keep the chain back to a person.
- [Code Inbox](https://background-agents.com/summit/sessions/nikhil-ramakrishnan/): review routing, and the 11% figure, at the Background Agents Summit.
- [How Uber uses AI for development](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development): Gergely Orosz on adoption, costs and engineer satisfaction.
- [Uber caps AI spending](https://techcrunch.com/2026/06/02/uber-caps-employee-ai-spending-after-blowing-through-budget-in-four-months/): TechCrunch on the budget spent in four months.
- [Uber on AI spending and tokens](https://fortune.com/2026/05/26/uber-coo-ai-spending-tokens-claude-code/): Fortune, with Andrew Macdonald on linking usage to features.

**Anthropic** (sells the agent it runs on)

- [The AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook): Louis Claxton’s six stages, each handing a file to the next.
- [How Anthropic secures its AI-native SDLC](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle): shadow mode, risk tiers and the review gate.
- [How AI is transforming work at Anthropic](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic): the company’s own engineers on what they gain and lose.
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web): the hosted background agent, auto-fix included.

**Spotify**

- [Background coding agents, part 1](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1): the first 1,500 merged pull requests, from migrations.
- [Part 2, context engineering](https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2): how the agent’s prompts and context were shaped.
- [Part 3, feedback loops](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3): verifiers, and a model acting as judge.
- [Part 4, dataset migrations](https://engineering.atspotify.com/2026/4/background-coding-agents-dataset-migrations-honk-part-4): about 1,800 downstream pipelines migrated, and an estimated 10 engineering weeks saved.
- [Coding is no longer the constraint](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint): 76% more pull requests to review, and 2.5 million automated ones.

**Stripe**

- [Minions, part 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents): one-shot coding agents on 10-second devboxes.
- [Minions, part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2): blueprints, the Toolshed catalog, and 1,300 pull requests a week.

**DoorDash**

- [Delegating engineering work to cloud-based agents](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/): the laptop risk, the sandbox target, and public threads.
- [How we learned to trust our AI code reviewer](https://careersatdoordash.com/blog/how-we-learned-to-trust-our-ai-code-reviewer-at-doordash/): the scout and the deep reviewers.
- [An AI code reviewer engineers actually listen to](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/): 10,000 reviews a week, review profiles per domain, and the fixer you tag in a thread.

**Ramp**

- [Why we built our background agent](https://builders.ramp.com/post/why-we-built-our-background-agent): Inspect, opt-in adoption, and sessions that end in a merge.
- [Why Ramp built Inspect](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect): the 5.5-person team, in The Pragmatic Engineer.
- [How Ramp built its agent on Modal](https://modal.com/blog/how-ramp-built-a-full-context-background-coding-agent-on-modal): the sandbox side (Modal sells the sandbox).

**Shopify**

- [Farhan Thawar on AI at Shopify](https://www.firstround.com/ai/shopify): First Round, with the $1,000-a-month quote.
- [Under the River](https://shopify.engineering/under-the-river): Shopify’s agent platform, which only works in the open.
- [Introducing Roast](https://shopify.engineering/introducing-roast): structured AI workflows, from 2025.
- [How Shopify built a model-agnostic AI stack](https://venturebeat.com/orchestration/how-shopify-built-an-ai-stack-that-doesnt-care-which-models-survive): VentureBeat on the proxy and runaway-agent alerts.
- [Tobi Lütke’s AI usage memo](https://x.com/tobi/status/1909251946235437514): the mandate route, from 2025.

**Intercom**

- [2x, nine months later](https://ideas.fin.ai/p/2x-nine-months-later): merged pull requests per R&D employee, tripled in 16 months.
- [AI is approving our pull requests](https://www.intercom.com/blog/ai-is-approving-our-pull-requests-heres-how-we-made-it-safe/): the revert rates, AI against human code.

**Meta**

- [Mapping tribal knowledge with AI](https://engineering.fb.com/2026/04/06/developer-tools/how-meta-used-ai-to-map-tribal-knowledge-in-large-scale-data-pipelines/): 59 context files, and 40% fewer tool calls.
- [The Rule of Two](https://ai.meta.com/blog/practical-ai-agent-security/): at most two of three powers per agent session.

**Warp** (sells the platform)

- [Software engineering is becoming factory engineering](https://www.youtube.com/watch?v=tUPPVhBBcoM): Zach Lloyd at AI Engineer ([talk page](https://ai.engineer/talks/tUPPVhBBcoM)).
- [Oz, the orchestration platform](https://www.warp.dev/blog/oz-orchestration-platform-cloud-agents): the fraud-bot that runs every 8 hours.

**Other companies**

- [LinkedIn’s Prince Valluri on InfoQ](https://www.infoq.com/podcasts/platform-engineering-scaling-agents/): platform engineering for agents, and what not to rebuild.
- [Honeycomb: 30 to 70 PRs a day](https://www.honeycomb.io/blog/30-70-prs-day-how-we-managed-not-wreck-systems): keeping systems stable as output doubles.
- [Coinbase’s bet on agent-first development](https://linear.app/customers/coinbase): Forge, its own agent (a Linear customer story).
- [Duolingo drops AI from performance reviews](https://finance.yahoo.com/sectors/technology/articles/m-not-going-force-duolingo-170215712.html): Luis von Ahn’s reversal.
- [Token leaderboards at Meta and Amazon](https://fortune.com/2026/05/12/amazon-tokenmaxxing-claude-ai-capex-meta-gil-luria/): Fortune on gamed usage numbers.

**Research and frameworks**

- [Eliminating toil](https://sre.google/sre-book/eliminating-toil/): the Google SRE book’s definition.
- [DORA 2025 report](https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf) and [the DORA AI capabilities model](https://services.google.com/fh/files/misc/2025_dora_ai_capabilities_model.pdf): AI-assisted delivery, and small batches.
- [Faros AI on AI acceleration whiplash](https://www.faros.ai/blog/ai-acceleration-whiplash-takeaways): time in review across 22,000 developers.
- [DX’s AI measurement framework](https://getdx.com/blog/ai-measurement-framework-guide/): utilization, impact and cost.
- [Thinnest viable platform](https://teamtopologies.com/key-concepts-content/what-is-a-thinnest-viable-platform-tvp): Team Topologies on platform size.
- [Harness engineering](https://martinfowler.com/articles/harness-engineering.html): Martin Fowler’s site on the loop around a coding agent.
- [Stop being skeptical about AI](https://newsletter.pragmaticengineer.com/p/stop-being-skeptical-about-ai-for): Charity Majors in The Pragmatic Engineer.

**The building blocks on the market**

- **Model gateways:** [LiteLLM](https://docs.litellm.ai/docs/simple_proxy), [Portkey](https://portkey.ai/docs/product/ai-gateway), [Kong](https://developer.konghq.com/ai-gateway/), [Cloudflare](https://developers.cloudflare.com/ai-gateway/), [Bedrock inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles.html).
- **Sandboxes:** [AWS AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html), [Modal](https://modal.com/docs/guide/sandboxes), [E2B](https://docs.e2b.dev/), [Daytona](https://www.daytona.io/docs/en/), [Ona](https://ona.com/docs/ona/getting-started), [Coder](https://coder.com/docs/ai-coder).
- **Tool gateways:** [MCP](https://modelcontextprotocol.io/docs/getting-started/intro), [Docker MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/), [AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html), [Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/agents/overview).
- **Hosted agents:** [Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent), [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web).
- **Tracing:** [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai).

**Incidents worth reading**

- [LiteLLM’s March 2026 security update](https://docs.litellm.ai/blog/security-update-march-2026) and [Datadog’s analysis](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/): the poisoned releases.
- [Replit’s deleted database](https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/): an agent during a code freeze.
- [AWS’s 13-hour outage](https://the-decoder.com/aws-ai-coding-tool-decided-to-delete-and-recreate-a-customer-facing-system-causing-13-hour-outage-report-says/): a tool that chose to delete and recreate.
- [The GitHub MCP exploit](https://invariantlabs.ai/blog/mcp-github-vulnerability): a public issue that hijacked an agent.

**The PostHog example** from the rollout section uses [the public PostHog repository](https://github.com/PostHog/posthog). [My earlier post on picking agents](https://www.theaithinker.com/p/how-to-pick-the-ai-agents-worth-building) covers the constraint rule this article builds on.

---

∙