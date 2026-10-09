---
title: "The Decision Model Gold Rush"
source: "https://swapniltalekar.substack.com/p/the-decision-model-gold-rush?utm_source=tldrnewsletter"
author:
  - "[[Swapnil Talekar]]"
published: 2026-10-06
created: 2026-10-08
description: "Jev had competitors before it had a changelog"
tags:
  - "clippings"
---
This is probably the fastest follow-up post I’ve ever written. Just last week I published a [post about a new kind of AI model called Jev](https://swapniltalekar.substack.com/p/jev-and-the-return-of-the-classifiers?r=1v4ea&utm_campaign=post&utm_medium=web), but things are evolving at such dizzying speed that I thought a follow-up was already due. We’re now officially living in some crazy times where building new AI models is faster than just blogging about them. Phew! So here you go.

![](https://substackcdn.com/image/fetch/$s_!WZCp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fba4c12f7-6a0e-42ff-80be-3b0b64ae27b0_2752x1536.png)

Jev went live on September 15, selling a new category: a model that doesn’t write a response, it picks one, a choice or a score or a yes-or-no with a confidence number stapled on. TypeSafe, the startup behind it, raised a $40 million seed at a $200 million valuation the same week and cleared a 140,000-person waitlist in 36 hours. Within a day, 13% of Vercel’s paid AI Gateway customers had already wired it into a workflow. Within three days, Cloudflare, LangChain, and Langfuse had shipped integrations for it.

That’s the kind of adoption curve most companies plan an entire launch quarter around. It took competitors about two weeks to show up anyway. By October 1, Amazon had shipped an open-source rival built on Qwen3.5-2B called Strands Decider 2B. OpenAI announced a competing Decisions API the same week, built on GPT-6 Luna and able to take images as input, something Jev can’t do. Cloudflare’s Clef, also open weight and built as a drop-in replacement for Jev’s own API, crossed 465 points on Hacker News the day it shipped and beat Jev on several of the benchmarks Jev itself publishes. Fastino added two more models to the pile, GLiDE and GLiNER2.5-Decide. And if you go looking on GitHub, there’s already a topic tag called jev-alternative with half a dozen open source clones under it, names like OpenJev, JevK5, von, and Laya, built by people who apparently decided two weeks was long enough to wait. TypeSafe’s own CEO wasn’t impressed, calling the rush of competitors “ML people wanting to implement a cool architecture”.

Jev has a Wikipedia page already. I don’t know what the record is for a product category going from launch to encyclopedia entry, but this has to be close.

Which is the actual problem with writing about this right now. Any post that tells you which decision model to use is wrong by the time it publishes, because something new ships while you’re still reading the last paragraph. So I’m going to focus on the criteria and the nuances of using decision models in production rather than the models themselves.

## Benchmark bias

Fastino’s own comparison of GLiDE and GLiNER2.5 -Decide against Jev picked both the tests being run and the models it was tested against. TypeSafe has said something similar about its own numbers, that the gains it publishes skew toward best-case scenarios.

Which is why having an independent benchmark is important, and thankfully there is one. It is called DecideBench, built by a developer named Cho Yin Yong. It runs 400 multiple-choice decisions across eight task families, support triage, content moderation, claim verification, and agent routing. On that benchmark, Jev holds up. It scores 98% accuracy at $32 per million tasks, the cheapest model above 95% accuracy in the whole test, while the general-purpose LLMs that beat it on raw accuracy cost six to fourteen times more to run.

The more interesting result is further down the list. The small encoder-based models, Laya among them, score only 35 to 59% accuracy despite being the fastest and cheapest options on the chart. The benchmark also turned up a name I didn’t have in my original list. Imajev-4B, an open, self-hosted model that takes images as input the way Jev can’t, scored 95%, enough to be called the best open decision model in the test. A second independent benchmark, JevBench, showed up around the same time, for what it’s worth.

![](https://substackcdn.com/image/fetch/$s_!NSDQ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18c65515-1a4b-4568-8a63-3eae7726f36b_2752x1536.png)

## Picking the right decision model for the job

While picking a decision model, below are a few critical questions you could ask to help you decide

**Where does it need to run?** Jev and OpenAI’s Decisions API are both hosted. Clef, Decider 2B, GLiNER2.5-Decide, Imajev-4B, and the other open-source clones you can run yourself or at the edge. If the data is too sensitive to be sent to frontier labs, then self-hosting is a good option

**What is the input data?** Jev accepts text, strings, JSON and arrays of strings. The Decisions API and Imajev-4B both take images too. If any part of your pipeline needs to route or score something visual- a screenshot, a scanned form, a photo of a damaged product- then those are your options.

**How fast do you need the result?** Jev advertises 70 to 500 milliseconds. GLiNER2.5-Decide claims 38 milliseconds on a GPU. Laya says about 33 milliseconds per question. If you’re deciding which support queue a ticket goes into, the gap between 70 milliseconds and 500 doesn’t matter much. But if you’re using this inside a real-time game loop or a trading system, latency of the decision is everything. Here the speed/accuracy tradeoff matters more.

**Do calibration numbers remain the same for your data?** A model is only useful if it gives similar results on your data as its advertised calibration numbers. The actual check is simple enough. Pull a sample of past decisions the model would have made, a few hundred at minimum, bucket them by the confidence it reports in bands of ten percentage points, and compare the real hit rate inside each bucket against what actually happened. If the model says 90% and the bucket’s real hit rate comes back at 65%, you probably want to choose another model for the job.

**What does it cost you at your actual volume?** Jev is $0.042 per million input tokens with free output, which sounds trivial until you multiply it by however many decisions you’re running a day. For large volumes of decisions, you could consider self-hosting one of the open-weight options, but with that you’re only trading that cost for your own compute and maintenance. Neither is automatically cheaper.

**What’s the replacement cost later?** Cloudflare built Clef to be a drop-in replacement for Jev’s own API on purpose, so it’s easier for customers to swap and compare both. But that’s not true of other available decision models. Most of them have incompatible API so replacing any of them is going to take some real work.

## Real pipeline examples

Let’s take an example of a support ticket triage first, which categorizes a few thousand tickets a day, sorted into billing, technical, or churn risk. The stakes here are low; a misroute costs a human a minute or two of redirecting it, so the cost per task and latency matter more here than squeezing out the last few points of accuracy. That makes Jev’s $32 per million tasks at 98% accuracy on DecideBench the easy default, with Strands Decider 2B worth a look if you’re already deep in AWS and want to self-host the same job for less. Calibration matters less here too, for the same reason. This is the ideal use case the decision models were built for.

Consider another scenario where you’re deciding which of several tool calls an agent should make next, inside a live game loop or a trading system where a few hundred milliseconds can cost thousands of dollars of real money. Accuracy differences in the single digits barely matter here, but latency is what really matters more. GLiNER2.5-Decide’s 38 milliseconds on GPU or Laya’s roughly 33 milliseconds look attractive on speed alone, but this is exactly where the 35 to 59% DecideBench accuracy range for encoder models should also be considered, because a routing decision that’s wrong a third of the time is not very valuable even if it’s fast; it’s just wrong quickly. If the latency budget is that tight, you can test whether Jev’s 70 ms claim works for you. If not, then probably consider going for a less accurate model.

## This table will be stale in about a month; use it anyway

Here’s where things stood in the first week of October 2026.

![](https://substackcdn.com/image/fetch/$s_!RD_2!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe8a29b06-f653-4f8b-b2ef-4abba308c9dd_894x721.png)

## Conclusion

My honest prediction is this category either consolidates hard around whichever model gets the most tooling built on top of it, the way Jev’s three-day head start with Cloudflare, LangChain, and Langfuse already suggests, or it splits permanently by use case, cheap open-weight models handling high-volume triage and hosted APIs handling anything that needs an explanation attached. I’d bet on some mix of both. Either way, the criteria above will continue to stay valid even while new models show up on the scene. If you’re already running one of these in production, I’d really like to know which one and why.