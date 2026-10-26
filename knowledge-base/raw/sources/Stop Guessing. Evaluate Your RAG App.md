---
title: "Stop Guessing. Evaluate Your RAG App."
source: "https://www.decodingai.com/p/rag-evals-change-prompts?utm_source=substack&utm_medium=email"
author:
  - "[[Paul Iusztin]]"
published: 2026-10-06
created: 2026-10-26
description: "Turn failures into eval cases, score them with code checks and LLM judges, and track cost and quality for every prompt or model change in Opik."
tags:
  - "clippings"
---
### From vibe checks to a 61-case score you ship on, in 5 steps

![Nothing leaves the line until it passes the test.](https://substackcdn.com/image/fetch/$s_!B6x4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbfa11215-7f38-44ea-8bfa-a3f02f4c9d88_1376x768.png)

Nothing leaves the line until it passes the test.

*“When I change it, what if something else breaks?”* That’s what Alexey Grigorev told me about the long system prompt behind his RAG app. If you’ve ever hesitated before editing a prompt that works, you know the feeling.

📣 *This article is based on an interview with the legend* [Alexey Grigorev](https://open.substack.com/users/2259961-alexey-grigorev?utm_source=mentions)*. He spent 15 years as a software and AI engineer and founded DataTalks.Club, one of the world’s largest data communities. There’s a good chance you know him from there.*

Here is the thing… His first AI app version shipped and works fine. Then corrections pile up, and every fix grows the prompt into a huge monolith that rigidly handles each use case. Alexey wanted to clean it up, since it clearly adds a lot of noise, but without a way to measure the impact of trimming parts of it, he was too afraid to do it.

That’s why he had to add evals to his RAG app. Otherwise, you find out something broke only when a user tells you. As Alexey puts it: *“without evals you are blind.”*

*But now we have another problem...*

When you finally want evals, you discover you never recorded the interactions you’d need. Most people don’t add observability like [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul) on day zero, so *“build a gold dataset first”* becomes a dream that never happens.

We will walk you through Alexey’s end-to-end eval workflow for his RAG app, built from proxy data when he had no traces. His RAG app is a FAQ chatbot integrated into his Slack DataTalks.Club community, which runs [free courses (the Zoomcamps) for 100k+ learners](https://aishippingblog.com/p/rebuilding-a-faq-system-for-datatalksclub). A perfect scenario for real-world RAG evals.

First, we will quickly look at the RAG app we will work with. Then we will focus entirely on **the 5 steps you need to evaluate** it: collect the data, build the eval set, build the evaluators, run them, and close the loop.

## The RAG app: a FAQ system built on GitHub issues

DataTalks.Club courses are free, so thousands of people ask questions in their Slack. Some are unique, but *“this is not the case for 99% of the questions.”* At the top of the list is *“I just discovered the course, can I still join?”*

![Repeat questions in the LLM Zoomcamp Slack, the problem the FAQ system exists to absorb.](https://substackcdn.com/image/fetch/$s_!j9oS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ef2d75a-1efa-466b-a111-01fa50ae1098_2004x1084.png)

Repeat questions in the LLM Zoomcamp Slack, the problem the FAQ system exists to absorb. Source

From an AI engineering perspective, their FAQ system is a RAG app that indexes all student questions into a light on-disk index that can be queried from Slack via the `:faq:` tag. A student asks a question; Alexey marks it with the tag; then a webhook triggers an AWS Lambda function that retrieves the top-k FAQs from the questions index, passes them to an LLM that compiles the answer, and posts the answer back in Slack.

![](https://substackcdn.com/image/fetch/$s_!-iR-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac0e918b-8a39-401c-923e-9aa608096bfa_1080x1498.jpeg)

[Source](https://aishippingblog.com/p/rebuilding-a-faq-system-for-datatalksclub)

> The system is available in the DataTalksClub [GitHub repository](https://github.com/DataTalksClub/faq), along with the FAQ dataset, where we have one Markdown file per question.

During ingestion, a “FAQ proposal” issue triggers a GitHub Action that retrieves similar questions with **minsearch**, Alexey’s lightweight text-search library. It then [asks an LLM with structured output for one decision](https://aishippingblog.com/p/rebuilding-a-faq-system-for-datatalksclub): `NEW`, `UPDATE`, `DUPLICATE`, or `WRONG_COURSE`. `NEW` and `UPDATE` open a pull request Alexey reviews, while `DUPLICATE` and `WRONG_COURSE` close the issue. When looking for similar questions, it searches using both the question and the full record, merging all records via Reciprocal Rank Fusion (RRF).

![How the FAQ automation classifies a contributed question: two searches fused with RRF, one LLM decision, and only two of the four outcomes ever reach a human.](https://substackcdn.com/image/fetch/$s_!jQ9k!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc88ed173-e6f8-4653-9df0-425c374db2fe_1200x515.png)

How the FAQ automation classifies a contributed question: 2 searches fused with RRF, one LLM decision, and only 2 of the 4 outcomes ever reach a human.

We are not here to see how this RAG app works (if interested, full breakdown [here](https://aishippingblog.com/p/rebuilding-a-faq-system-for-datatalksclub)), but to see how we can evaluate it, starting with the most important part: building the AI evals dataset.

## Step 1: Collect the data, even if you never traced it

Alexey is “totally for vibe checks” early on. But from the very beginning, while you’re still vibe coding, ask your AI assistant to record every interaction, and your future eval set collects itself.

Alexey didn’t: *“My goal was to just get this out and test how it works.”* It worked. Then corrections piled up, but the system prompt got too big and noisy, and he was too afraid to touch it for fear of breaking something.

Today it’s stored in Opik’s prompt library:

![The FAQ curation prompt in Opik's prompt library.](https://substackcdn.com/image/fetch/$s_!CAZN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F996bb65e-e3b3-4d7a-a5b5-2c9ba06daa3c_3114x1620.png)

The FAQ curation prompt in Opik's prompt library.

🚨 **His core problem was that he had no traces to build the evals dataset from!**

So he used proxy data. Every FAQ contribution was a GitHub issue, and every correction was a commit on a PR. Issues give the inputs, and his corrections tell him what the output should have been. This meant he had access to the input, generated output, and expected output triplets he needed for evals.

How about reading the data yourself or being lazy (or optimal!) and using an LLM to do so? Alexey does “Both.” He lets PRs pile up for a few weeks, then clears them in one session with his AI coding assistant and a custom `clear-backlog` [skill](https://github.com/DataTalksClub/faq/blob/main/.agents/skills/clear-backlog/SKILL.md). The assistant proposes “merge,” “fix this first,” or “this case is interesting, let’s add it to our evals.” His job: “I just need to agree or disagree.”

![Clearing the PR backlog in one session: "let's go through the backlog" loads the clear-backlog skill.](https://substackcdn.com/image/fetch/$s_!j7QK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d5ac881-42e2-475b-b294-3f5bc05c0a27_1946x594.png)

Clearing the PR backlog in one session: “let’s go through the backlog” loads the clear-backlog skill. Source

Using the proxy data to fix his cold-start problem was only a temporary solution. Today, both the curation automation and the Slack assistant send traces to Opik: inputs, retrieved documents, outputs.

Here is how the Slack assistant traces look in [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul):

![Slack assistant traces in Opik.](https://substackcdn.com/image/fetch/$s_!HjKA!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ce287a1-8ab1-4026-8173-0de4ed4d8a47_3110x1638.png)

Slack assistant traces in Opik.

We have similar traces for the FAQ curation ingestion automation, but in a different Opik project. It works for both queries and ingestion.

**For your RAG app**, look for any place a human already judged your output (edited PRs, support tickets, corrected answers, thumbs-down). Then trace everything from now on, so you won’t need proxies again.

## Step 2: Build the eval set

When building your dataset, the hardest part is labeling it with pass/fail scores, plus a critique. In Alexey’s scenario, every past decision told him what the right answer was, in 2 main ways:

- A PR he accepted unchanged is a “pass” sample.
- A PR where he had to alter it in any way becomes a “fail”, adding a one-sentence critique about why the review wasn’t accepted.

A false `DUPLICATE` (or `WRONG_COURSE`) is the dangerous error. The issue closes automatically, and no PR is opened, *“so I would never discover it.”*

The second biggest issue is replicating the context your RAG app used when ingesting/retrieving an item.

In our FAQ app, a question that was new when the issue arrived is now merged. Replay it as-is and the system correctly says `DUPLICATE`, so the eval case fails for the wrong reason. As I said during the interview, you have to *“install your data,”* not just your dependencies.

His answer is [leave-one-out](https://aishippingblog.com/p/rebuilding-a-faq-system-for-datatalksclub), shown in the image below. With 200 records within the dataset, where record D came from the issue under test, he removes D, replays the issue against the other 199, and expects `NEW`.

![Leave-one-out: remove the record the issue created, then replay the issue against the rest.](https://substackcdn.com/image/fetch/$s_!9KH8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd9c03721-6e27-413b-9833-d854b27b06b7_1200x403.png)

Leave-one-out: remove the record the issue created, then replay the issue against the rest.

Each eval case is a few lines of Python code in Git: case ID, question, answer, expected action, and the ID of the doc to remove. The case ID is the GitHub issue number, so every case traces back to its issue or PR. [See all here](https://github.com/DataTalksClub/faq/blob/main/faq_automation/evals/cases.py#L212).

```markup
EvalCase(
    course="llm-zoomcamp",
    case_id=274,
    question="OpenRouter: Error code 402 when calling responses.create (max_output_tokens)",
    answer="""OpenRouter can return APIStatusError with code 402 when responses.create() 
is called without a max_output_tokens limit. Pass a lower limit: max_output_tokens=1024.""",
    expected_action="NEW",
    expected_section="module-1-homework",
    description="OpenRouter 402 error — valid NEW for module-1-homework",
    checks=[action_is("NEW"), section_is("module-1-homework")],
    tags=["correct-new"],
    relevant_doc_id="cfb07a27d5",
)
```

Every run costs money, so he trimmed the eval dataset to a small core set: 61 cases, with 38 `NEW`, 10 `DUPLICATE`, 7 `WRONG_COURSE`, 4 not `WRONG_COURSE`, and 2 `UPDATE`.

All the cases are imported into Opik as a versioned dataset for running the experiments:

![](https://substackcdn.com/image/fetch/$s_!U3FN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F600ea3a3-08eb-4af1-8778-ff66ef2bfd40_3038x1306.png)

**For your RAG app**, an eval set is inputs plus expected outcomes, weighted towards the errors that cost you most, and replayed against the knowledge base as it was when each input arrived.

## Step 3: Build the evaluators

I asked Alexey, *“How did you decide what metrics actually to measure?”* His answer was per case type. Cases are grouped *“based on the outcome I want”:* correctly new, true duplicate, not a duplicate, wrong course. Each type *“has its stack and then different logic for checking.”* A “correct new” case checks both that the question is flagged as `NEW` by the LLM and that it is ingested in the right section.

His curation automation returns a structured decision, so the evaluators are deterministic: **action match** (right decision) and **placement match** (right section), plus the **cost** of each case. When he analyzed all his traces, the most common error turned out to be incorrect section placement. Instead of placing a record about projects in the “Project” section, it would place it in “General”.

One curation trace flagged as DUPLICATE with its structured decision, model, and cost:

![One curation trace: structured decision, model, and cost.](https://substackcdn.com/image/fetch/$s_!Wc-K!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9534722-186c-4bee-bcf4-1dc5949fb2bb_2970x1976.png)

One curation trace: structured decision, model, and cost.

These evaluators need no LLM, are cheap to run, and are never ambiguous. Retrieval is checked separately: for a given query, it verifies that it retrieves the expected chunks. A 25-case suite scored by recall@5 runs in about 2 seconds, while the 61-case generation suite takes about 2 minutes.

The Slack assistant’s answers have no single right string. There, you need an LLM judge aligned with your own labels. Label 10 to 15 examples as good or bad yourself, write the rules down, and iterate until the judge agrees with you, [as Alexey lays out in his evals guide](https://aishippingblog.com/p/how-to-do-evals-in-2026).

**For your RAG app**, use code checks wherever the right answer is known (a decision, a label, a retrieved document), check retrieval separately from generation, and save LLM judges for free-text answers.

Next, I asked him how he decides whether an eval experiment passed.

## Step 4: Run the evaluators in your eval harness

First, let’s see how the eval harness that runs the experiments works.

Alexey keeps the eval cases in Git as the source of truth, and uses Opik as the eval harness: he uploads that dataset version and attaches it to each experiment, so every result shows what it ran on.

His runner is plain code in Git that runs all cases, or just one, and logs each run to Opik as an experiment with per-case action match, placement match, and cost. He admits it’s “not very scientific” yet and wants to track runs historically in Opik.

Here is one eval run, as an Opik experiment, where we can see the aggregated and per-item scores:

![One eval run as an Opik experiment.](https://substackcdn.com/image/fetch/$s_!nOzk!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c7343bd-b31a-431a-87c7-a3670747d550_3114x1488.png)

One eval run as an Opik experiment.

“I never needed 100 percent,” Alexey says, because his AI assistant still reviews every PR. The number is a benchmark that must not go down. Today the generation eval set passes [42 of 61 cases](https://aishippingblog.com/p/rebuilding-a-faq-system-for-datatalksclub) on GPT-5.4 nano. When new cases make it dip, he changes nothing else and takes it as the new baseline. Hard cases can sit in FAIL: he doesn’t want the system prompt to grow to handle every corner case, but he does want to know those cases exist.

![Alexey's two eval suites: retrieval (25 cases, recall@5) and generation (61 cases, 42 passing on GPT-5.4 nano).](https://substackcdn.com/image/fetch/$s_!LzGh!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6f03428-6c23-4840-8725-014ee96e10ed_1832x779.png)

Alexey’s 2 eval suites: retrieval (25 cases, recall@5) and generation (61 cases, 42 passing on GPT-5.4 nano). Source

He pays for this community project out of his own pocket and wants *“the cheapest possible way that is performant enough to be useful.”*

With evals, he compared models: GPT-4o mini is *“very cheap but stupid”* for this decision, so he chose **GPT-5.4 nano**, the cheapest that still delivers good quality. He keeps $5 in his OpenAI account and forgets about it “for half a year or even more,” because “each query costs on average less than one cent,” as the metrics from Opik show.

When the automation misbehaves, he first captures the failure as an eval case. He runs the new prompt on that case until it passes, then on the whole set to check nothing else broke. *“It’s kind of test-driven development, but like eval-driven development.”*

![Eval-driven development: capture the failure first, fix it, then prove nothing else broke.](https://substackcdn.com/image/fetch/$s_!uSHt!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F197a0874-89d6-423f-942f-65008b2b2ace_1203x1197.png)

Eval-driven development: capture the failure first, fix it, then prove nothing else broke.

By tracking each run as an Opik experiment, we can clearly see the difference in scores in the before, after, and verify runs tracked over time:

![Before, after, and verify runs as Opik experiments.](https://substackcdn.com/image/fetch/$s_!CTDh!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71977474-bd58-4a71-b9ed-153d9df50694_3114x1282.png)

Before, after, and verify runs as Opik experiments.

**For your RAG app**, keep the cases in version control, run each experiment against a versioned dataset in your eval harness, always keep one baseline number as reference, and turn every failure into a case before you fix it.

## Step 5: Close the loop in Opik

Mining Git history worked once, but “ *it’s not the exercise I want to perform every time.”* Now, when he sees a bad Slack reply or someone corrects the bot, [that question becomes an eval case](https://aishippingblog.com/p/rebuilding-a-faq-system-for-datatalksclub). He uses his coding agent to pull the trace from Opik into his eval set.

Below is Alexey’s Slack assistant correction dataset:

![Slack assistant corrections as an Opik eval dataset.](https://substackcdn.com/image/fetch/$s_!BjrT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47caddec-4fe8-429b-8959-cd50ae74e05e_3120x1484.png)

Slack assistant corrections as an Opik eval dataset.

*“Because I have evals … I can see where it’s failing,”* and he usually fixes it by improving the FAQ, the docs, or the course repository, not with a fancier model. Then he re-runs the evals.

Alexey calls evals **“basic hygiene”** that you know is good for you, but you still skip it from time to time. Everyone knows you should go to bed at the same time, and sometimes you still go at 2 a.m. instead of 10 p.m.

**For your RAG app**, route every user correction straight from your traces into the eval set instead of reconstructing it from history.

In my experience, integrating Opik takes about 5 minutes, and the free tier covers 25k spans a month, which, for this project, Alexey *“can use free forever”* (a serious production app might burn that in a day). He tried the [open-source version](https://github.com/comet-ml/opik) first, but with his lean infra, self-hosting would have been more expensive.

Opik didn’t fit in 2 places. His evals remove records from the dataset per case, and he found no straightforward way to run that inside Opik, though *“maybe it’s just I should spend more time on understanding.”* And his zero-dependency Lambda couldn’t easily take Opik’s default Python client, so his AI assistant switched to plain [HTTP requests](https://www.comet.com/docs/opik/reference/rest-api/overview?utm_source=newsletter&utm_medium=partner&utm_campaign=paul), which *“was so simple at the end.”*

## Final Thoughts

> *“I have so many applications with zero evals and a bunch of vibe-coded test cases I don’t even know test the right thing. Is that wrong?”*  
> — Paul

Alexey’s answer: there’s nothing wrong with it, as long as you know how to build an eval set when you need one. First figure out how the app should work and what the UX is. If you pour time into evals and then learn the UX is wrong, you throw the evals away with it.

> *“Many engineers who don’t know the domain look blindly at the logs and can’t decide: is this good, is this bad, what am I looking at?”*  
> — Paul

His advice: sit down with the domain experts. Even when he was a data scientist, long before AI automation, the most useful thing he did in every job was learn from the people his models were built for, because their input decides what “good” means.

That’s why I think humans still sit in evals. A coding agent can build the app, but it won’t tell you what it costs to run, how slow it is, or whether it’s actually good. Start with Alexey’s *[How to Do Evals in 2026](https://aishippingblog.com/p/how-to-do-evals-in-2026),* then Eugene Yan on [aligning LLM evaluators](https://eugeneyan.com/writing/aligneval/) and Hamel Husain on [why AI products need evals](https://hamel.dev/blog/posts/evals/).

And if you’re starting a RAG app today, trace it on **[Opik’s free tier](https://www.comet.com/signup?utm_source=newsletter&utm_medium=partner&utm_campaign=paul) (25k spans/month, enough for any MVP)** to make your transition from your first vibe check to evals smoother.

*But here is what I’m wondering:*

> ***How are you evaluating your RAG workflow or agent?***

*Click the button below and tell me. I read every response.*

---

*Enjoyed the article? The most sincere compliment is to restack this for your readers.*

---

#### Whenever you’re ready, here is how I can help you

*Go from agent user to agent builder.* Master the foundations of AI agents and turn fragile demo code into reliable, production-ready systems with my course, **[Agent Engineering: Building Multi-Agent Systems](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31&utm_source=decodingai&utm_medium=partner&utm_campaign=agent_engineering)** (made with Towards AI).

35 lessons. Pure foundations from scratch. 4 mini-projects. 2 production systems. A certificate and direct access to me & industry experts in our Discord.

Built for software and data professionals transitioning into AI engineering. *Rated 5/5 with 300+ students. The first 7 lessons are free:*

*Not ready to commit?* Start with our **[free Agent AI Engineering Guide](https://email-course.towardsai.net/?ref=b3ab31&utm_source=decodingai&utm_medium=partner&utm_campaign=agent_engineering)**, a 6-day email course on the mistakes that silently break AI agents in production.

---

*Thanks again to [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul) for sponsoring this case study and keeping it free!*

![Opik Banner](https://substackcdn.com/image/fetch/$s_!oSDm!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26c21863-4ee6-4026-91c7-74650eb16dac_3168x792.png)

Try Opik for free here (25k spans/month free)

**If you want to monitor, evaluate, and optimize your AI workflows and agents:**

---

## Images

If not otherwise stated, all images are created by the author.

∙