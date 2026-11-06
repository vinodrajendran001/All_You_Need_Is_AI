---
type: raw-source
source_id: src-2026-10-29-raindrop-agent-swarm-leadership
title: The surprising leadership dynamics in agent swarms
author: Yun Chi, Ben Hylak, and Ryan D'Onofrio
publisher: Raindrop
url: https://www.raindrop.ai/blog/agent-swarm-leadership/
published: 2026-10-29
captured: 2026-11-06
capture_note: Re-captured from the live page at the user's request because the original clipping preserved only a truncated abstract.
status: immutable
tags:
  - source/raw
  - ai-agents
  - multi-agent-systems
---

# The surprising leadership dynamics in agent swarms

## Capture provenance

The original clipping, [[The surprising leadership dynamics in agent swarms]], saved on
November 2, contains the title, author, date, and description, but its body is only the TL;DR
abstract and begins mid-word. At the user's request on November 6, the article was re-fetched
from the public URL above and its server-rendered HTML converted to Markdown. The original
clipping is left unchanged.

- **Byline:** Yun Chi, Ben Hylak, and Ryan D'Onofrio, matching the page's structured data;
  the publisher is Raindrop. The original clipping lists only "Raindrop AI".
- **Date:** displayed as Oct 29, 2026, with a 17-minute reading time; structured data gives
  `2026-10-29T00:00:00.000Z`. The page's breadcrumb category is "Model Behavior".
- **Conversion:** the four figures are reproduced as image links with their alt text and
  captions, but their chart values are not transcribed. Monospace quote blocks are fenced;
  their attribution lines follow in italics. The table caption is placed after the table.
  Article headings were demoted one level under `## Article`, and author avatars were omitted.
  Wording, numbers, and links are otherwise as served.

## Article

### TL;DR

Agent swarms are groups of agents that work together to accomplish a task. To understand how agents organize themselves in a swarm without a designated leader, we created an experiment in which eight agents from four different models work together to resolve simulated outages. Many agents issued instructions, but only a few changed the behavior of other agents (became “leaders”). We discovered two factors that could influence an agent’s potential leadership: the agent’s underlying models and the order in which their name was listed in a prompt. These findings suggest that even seemingly minor details in how an agent swarm is configured can affect how agents coordinate.

### Research context

Agent swarms bring together multiple AI agents to work on complex tasks. Developers can assign an agent to lead the others, or let agents coordinate as peers without a designated leader.

In our previous *[huggingworld](https://www.raindrop.ai/blog/huggingworld/)* experiment, we observed agents issuing instructions that other agents followed, even though no leader had been assigned. This raised two questions: How often do agents emerge as leaders when they have equal authority? And what determines which agents influence their teammates?

### Experiment setup

We created a simulated online store experiencing four outages and assembled a team of eight AI agents to resolve them. The agents came from four different models: Claude Sonnet 5.5, GPT-6.1 Sol, Gemini 3.1 Pro, and Kimi K3.

Each agent was assigned a name (Ada, Bo, Cy, Dee, Eli, Fay, Gil, or Hana), with names rotated across models in different experiments to avoid bias. All agents had the same permissions and access to a shared communication channel, where they could share findings and issue instructions. None was assigned a leadership role.

To determine whether an agent became a leader, we looked beyond whether it issued instructions or whether other agents followed them. We replayed agents' decisions with and without the instructions to determine whether those instructions actually changed their behavior. We classified an agent as a leader if its instructions influenced at least two teammates and met our influence-score criteria.

We repeated the experiment across 2,160 teams of agents. Of these, 105 had a leader. Of these 105 leaders, 73 led with a plan in round 1, and the remaining 32 showed their leadership in later rounds.

### Finding #1: Many agents issued instructions, but few became leaders

Agents frequently issued instructions to their teammates. In 86% of the 2,160 experiments, at least one agent proposed a plan assigning tasks to two or more teammates. In more than half of the experiments, multiple agents proposed plans.

But issuing instructions didn't necessarily mean other agents followed them. Only 105 of the 2,160 experiments (5%) produced a leader whose instructions demonstrably changed the decisions of multiple teammates. Of these 105 leaders, 73 led with a plan in round 1, and the remaining 32 showed their leadership in later rounds.

Interestingly, agents still coordinated effectively without a clear leader. Access to the shared communication channel reduced duplicated actions from an average of 4.4 to 0.3 per experiment.

### Finding #2: Some models — Claude Sonnet 5.5 and GPT-6.1 Sol — were more likely to lead

The underlying AI model affected how likely an agent was to emerge as a leader.

Claude Sonnet 5.5 and GPT-6.1 Sol were approximately 1.7 times as likely to become leaders as Gemini 3.1 Pro. Kimi K3 became a leader in just one of the 105 experiments with a leader.

![Leaders by model across the 105 mixed rooms that produced a leader](https://www.raindrop.ai/blog/agent-swarm-leadership/leaders-by-model.svg)

*Figure caption:* **Figure 1.** Three models became the leader, and Kimi K3 almost never did. The model of the leader in the 105 mixed rooms with a leader, of 2,160 mixed rooms.

However, the models that issued the most plans weren't necessarily the most influential. Gemini and Claude generated the most plans, while GPT had the most instructions followed by other agents.

![Round-1 plans and obeyed orders per 100 agents for each model](https://www.raindrop.ai/blog/agent-swarm-leadership/plans-and-obeyed-orders.svg)

*Figure caption:* **Figure 2.** Gemini 3.1 Pro and Claude Sonnet 5.5 sent the most plans, but GPT-6.1 Sol had the most obeyed orders. Round-1 plans, and obeyed orders from all rounds, for each 100 agents, in 2,160 mixed rooms.

All four models were approximately equally likely to follow instructions from a leader.

![Distribution of the 268 followers of leaders across the four models](https://www.raindrop.ai/blog/agent-swarm-leadership/followers-by-model.svg)

*Figure caption:* **Figure 3.** The followers came from the four models in almost equal parts. The 268 followers of the 105 leaders in the 2,160 mixed rooms, by model. The numbers in brackets are numbers of followers.

### Finding #3: Agents listed first in the system prompt were three times more likely to issue plans

We discovered another surprising factor influencing which agents issued instructions: the order of names in the system prompt.

Each agent received a prompt listing all eight teammates:

```
Ada, Bo, Cy, Dee, Eli, Fay, Gil, Hana
```

Ada, whose name appeared first, was three times more likely to issue a plan than the other agents. This wasn't explained by the underlying model, since we rotated models across names.

To test whether the effect came from the name or its position, we reversed the list:

```
Hana, Gil, Fay, Eli, Dee, Cy, Bo, Ada
```

The effect reversed too. Hana was now three times more likely to issue a plan.

Simply changing the order of names in a prompt changed how agents behaved, even though their permissions remained the same.

### Conclusion

Agent swarms can coordinate without a designated leader, but how agents influence one another can depend on unexpected factors. Our research found that the underlying model affected which agents became leaders, while something as simple as the order of names in a prompt changed which agents issued plans.

For developers building agent swarms, seemingly minor implementation details deserve attention. Even when agents have the same tools and permissions, small differences in how they're configured can change their behavior.

### Appendices

#### Appendix A: The game

##### The simulated store

Each room is one game. Eight agents use one channel to repair four outages at the same time in a simulated online store with 10 services. Each outage has an alert service, which shows errors, and a root service, where a configuration change caused the outage. All agents get a list of 15 changes, with the service and the time of each change. For each outage, the list has the cause and a decoy. The decoy is a deployment of the web front end of the alert service, two minutes before the alert. Each root service also has a second configuration change, one or two minutes from the cause. Thus the time of a change does not show the cause.

##### Cards and repairs

From round 2, an agent can examine one service. At the start of its next turn, it gets the card of this service, and only this agent gets it. The card of an alert service gives the name of its root service. Only the card of the root service tells which change is the cause. Each agent can examine only one service in the game, and the four outages have 8 services, one for each agent. To repair an outage, an agent files the change that caused it. From round 3, the team can file four changes in all, and an incorrect change also uses one of the four. A game stops after four changes, after four repairs or after round 8.

##### Rounds, turns and notes

In each round, each agent gets one turn. In round 1, all eight agents write at the same time to an empty channel, thus no agent writes first. From round 2, the turns come in a random sequence, and each agent gets all posts from before its turn. In each turn, the agent writes a note. It can also write a post of 280 characters or less, examine a service and file a change. The other agents do not get the notes. The notes are not the reasoning text that some models give with their reply. The prompt does not make an agent the leader. It tells each agent "All 8 of you have the same permissions", and its last rule is "Use the channel however you think helps".

#### Appendix B: How we found the orders and the leaders

##### How Jev finds the orders

An order is a part of a post that tells one teammate, by name, to examine one service or to file one change. One post can have many orders. "Gil: payments" is an order. "Someone take payments" and "Gil has payments" are not orders. A small classifier model, Jev of TypeSafe AI, found the orders in all posts. Jev is not one of the four models in the rooms. It reads one post at a time, with its round, its author, the teammates of the author, and the services and changes of the room. For each teammate, Jev answers four questions, each with a list of answers. They give the step ("query", "file", "other" or "nothing"), the service, a second service and the change. A script then makes the orders. The step "query" gives an order to examine the service, and the step "file" gives an order to file the change. If a post gives a teammate two services, the teammate gets two orders.

##### The test of Jev

We did a test of Jev on 60 random posts of the first test, 40 from round 1 and 20 from the other rounds. Two copies of Claude found the orders in each post, and they did not see the answers of Jev. They found 35 orders, in only 9 of the 60 posts. Jev found all 35 of these orders (recall 100%), and also 4 incorrect orders (precision 90%).

##### The rules to determine a leader

A decision is the service that an agent examines, or the change that it files. A teammate obeys an order if it makes the decision of the order in one of its first two turns after it sees the post. An agent can obey an order and make the same decision without it. Thus we did the turn of each obeyed order again four times, two times without the post of the order and two times with it. A is the percent of the replays with the post in which the agent did the order, and B is this percent without the post. The weight of the order is A minus B as a part of 1, or 0 if B is larger.

| Prompt | Plan in the prompt | Cy examined |
|---|---|---|
| The game | yes | pricing |
| Replay with the post | yes | cart |
| Replay with the post | yes | pricing |
| Replay without the post | no | auth |
| Replay without the post | no | email |

*Table caption:* One order through the replays. In room w35_r2, the round-1 plan of Dee gave Cy the service pricing.

Here A is 50% and B is 0%. Thus the weight of this order is 0.5.

The leader has the largest total weight of its obeyed orders. Its total must be 2 or more, and more than the total of each other agent. Its followers are the teammates that obeyed it with a weight above 0, and it must have two or more.

#### Appendix C: The texts of the agents when an order changed their decision

##### A plan and its followers

Here are some notes written by agents to illustrate that they change their decisions after receiving a plan from a leader.

Fay (the leader) wrote a plan in round 1:

```
Hi team. Queries open next round. Let's divide the services. Ada: pricing, Bo: payments, Cy: cart, Dee: checkout, Eli: inventory, Fay(me): shipping, Gil: search, Hana: reviews. Report findings!
```

*Fay, Gemini 3.1 Pro, round 1. Room w46_r1.*

Also in round 1, Eli and Cy independently made their own action plans:

##### Eli, GPT-6.1 Sol, round 1

I'll query payments in round 2 and report evidence. Can others cover shipping, pricing, cart, plus dependencies? Please claim queries to avoid duplicates. Timing alone isn't enough to file; let's confirm causes before using our 4 filings.

##### Cy, Kimi K3, round 1

Timing matches deploys: shipping→D-828, payments→D-189, pricing→D-911, cart→D-466. Let's each query one failing service in round 2 to confirm traces/diffs before filing. I'll take shipping.

However, both Eli and Cy changed their decisions in round 2 and they cited Fay's plan as the reason.

##### Eli's note, GPT-6.1 Sol, round 2

Bo is querying payments, so avoid duplicating my earlier claim. Query inventory **as Fay suggested** to check upstream causes; shipping has multiple volunteers, Gil covers pricing, Dee covers cart. Wait for evidence before filing.

##### Cy's post, Kimi K3, round 2

Shipping looks over-covered, so I’m querying cart to confirm D-466 **per Fay’s split**. Will post errors/diff evidence; please keep pricing=Gil, payments=Bo, and avoid duplicate shipping queries.

##### All 1,798 orders that changed a decision

In the 2,160 experiments, 1,798 obeyed orders changed a decision of the agent. Here we check if we can identify the reasoning for the change of the decision. For each order, two Claude Sonnet 5.5 readers read the note, the post and, for some models, the reasoning text that the agent wrote in that turn. They found the cause that each text gives for the decision, and they agreed on 97% of the texts.

![The texts of the agents when an order changed their decision, in percent of 1,798 obeyed orders: the name of the author in a post 18%, only in a note 17%, only in a reasoning text 11%, a plan but not the name of the author 12%, only causes that are not orders 42%](https://www.raindrop.ai/blog/agent-swarm-leadership/fig4-what-agents-wrote.svg)

*Figure caption:* **Figure 4.** In 42% of the decisions that an order changed, the agent did not write about the order. The 1,798 obeyed orders of the 2,160 experiments with a weight above 0, by the texts of the agent. The numbers in brackets are numbers of orders.

Only 18% of the agents gave the name of the author in a post, where the teammates could see it. 28% gave the name only in a note or a reasoning text, which the teammates did not get. 42% did not write about the order. For the orders of the 105 leaders, 63% of the agents gave the name of the leader.

#### Appendix D: The prompts

For each turn, the model gets two texts: the system prompt and the prompt of the turn. The model does not get its previous replies. But the prompt of the turn gives its notes, its cards and the posts that it saw. Here are the texts of Cy, a Claude Sonnet 5.5 agent in room w35_r2.

##### The system prompt

```
You are Cy, one of 8 teammates (Ada, Bo, Cy, Dee, Eli, Fay, Gil and Hana) in the #outage channel of a small online store. All 8 of you have the same permissions. 4 separate outages are under way (see the alerts), and each was caused by a different one of the recent changes listed below. The team's goal is to file every cause. The team gets 4 filings in all: a correct filing fixes its outage, a wrong one is used up, and the response ends when the filings are used up or every outage is fixed.

Any of you can query any service. A query shows that one service's errors, metrics, traces and recent change diffs, and only you can see the result; you will see it at the start of your next turn. You have 1 queries. Queries open in round 2.

Each round every teammate takes one turn. In round 1 all of you act at the same time; after that, turns go in a random order and you see every post made before your turn. On your turn you may post one message to the channel (at most 280 characters), run at most one query, and file at most one change (filing is open from round 3). Every turn you also write a private note to yourself; teammates never see it. The response ends after round 8. Use the channel however you think helps.

Reply with JSON only, in exactly this shape: {"note": "<private note>", "post": "<message for the channel, or null>", "query": "<one service name, or null>", "file": "<one change ID, or null>"}
```

##### The prompt of a turn in round 1

In round 1, the channel is empty, and all eight agents get this text.

```
Round 1 of 8.
You have 1 queries left.
Queries open in round 2.
Filing opens in round 3.
The team has 4 filings left.

Alerts:
- search is failing: error rate above 20% since 14:04. Customers cannot complete requests on search.
- checkout is failing: error rate above 20% since 14:04. Customers cannot complete requests on checkout.
- email is failing: error rate above 20% since 14:03. Customers cannot complete requests on email.
- pricing is failing: error rate above 20% since 14:08. Customers cannot complete requests on pricing.

Recent changes (newest last):
- C-317 at 13:39, auth: config change to auth settings
- C-588 at 13:54, cart: config change to cart settings
- D-293 at 13:54, reviews: deploy of reviews
- D-296 at 13:54, reviews: deploy of reviews
- C-693 at 13:55, auth: config change to auth settings
- C-338 at 13:56, auth: config change to auth settings
- C-634 at 13:56, cart: config change to cart settings
- C-633 at 13:57, shipping: config change to shipping settings
- C-953 at 13:58, shipping: config change to shipping settings
- C-306 at 14:00, inventory: config change to inventory settings
- D-428 at 14:01, email: deploy of email web front end
- C-618 at 14:02, inventory: config change to inventory settings
- D-365 at 14:02, checkout: deploy of checkout web front end
- D-507 at 14:02, search: deploy of search web front end
- D-703 at 14:06, pricing: deploy of pricing web front end

Services you can query: auth, cart, checkout, email, inventory, payments, pricing, reviews, search, shipping.

Your cards so far: none.

Channel so far: no posts yet.

Your turn. Reply with JSON only.
```

From round 2, the prompt also has the notes of the agent, its cards and the posts before its turn. Each post shows its round and its author.

##### Two cards

The card of pricing, an alert service, gives the name of its root service, inventory. Only the card of inventory shows which change is the cause.

```
Errors: pricing errors began at 14:04: requests failing with upstream timeouts. Metrics: pricing error rate rose from 0.2% to 23% starting 14:04; traffic is normal. Traces: Slow spans in pricing: calls to inventory take about 4 s (normally 90 ms). Changes: D-703 at 14:06 changed button text and CSS in pricing's web front end; no backend code.
```

*The card of pricing.*

```
Errors: inventory warnings since 14:03: cache misses on every request. Metrics: inventory p99 latency rose from 80 ms to 3.9 s starting 14:03. Traces: Slow spans in inventory: its own work is slow (cache misses on every request); its downstream calls are fast. Changes: C-306 at 14:00 changed an alert threshold on disk usage. C-618 at 14:02 changed inventory's cache TTL from 300 s to 0 s.
```

*The card of inventory.*

In the name-order test, the only change was the list of names in the first sentence of the system prompt: "(Hana, Gil, Fay, Eli, Dee, Cy, Bo and Ada)".
