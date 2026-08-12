---
type: raw-source
source_id: src-2026-08-12-bytebytego-semantic-feed-retrieval
title: How to Fight Clickbait - Meta, LinkedIn and YouTube Case Studies
author: ByteByteGo
url: https://blog.bytebytego.com/p/how-to-fight-clickbait-meta-linkedin
published: 2026-08-10
captured: 2026-08-12
status: immutable
tags:
  - source/raw
  - recommendation-systems
  - semantic-retrieval
---

> Preserve the source body below this line as the canonical capture.

## Agents Can Now Sign Up for Your App (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!3-kg!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2418a958-8d25-45fe-9a95-6f0be33c5df7_1200x494.png)

Agents are hitting your signup flow and bouncing off a browser login built for humans. Every one that gives up is a signup you never see.

[WorkOS Agent Registration](https://go.bytebytego.com/WorkOS_081026Registration) turns that traffic into signups. Enroll via the dashboard and AuthKit publishes an auth.md file agents read to register for scoped, short-lived credentials you control.

---

What does it take for a social media platform to stop rewarding clickbait content?

At first glance, this question might sound like a moderation problem that you can simply solve by enforcing better content policies and classifying posts that are engagement bait. However, the problem is much deeper. It often sits inside the component that decides which posts become part of a user’s feed in the first place.

Consider the scale of the decision. When you open a feed, the platform has a few hundred milliseconds to select a handful of posts from hundreds of millions of candidates. Scoring every candidate with an expensive model burns through the time budget. To get over this, the social media platforms rely on engagement, which is a cheap and somewhat reliable proxy for judging relevance. Such a proxy is easy to measure and optimize against, and it powered a generation of recommendation systems.

![](https://substackcdn.com/image/fetch/$s_!NSdT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F543c95a9-2673-43ce-a96e-8c7492eb00ca_2642x1128.png)

However, the problem is that this type of engagement is also easy to manufacture. For example, a post that opens with “comment DONE if you’re a real engineer” collects clicks and replies while delivering little value. But a ranking function tuned to reward interaction will promote it even though it is clearly an engagement bait. For years, the countermeasures against this were heuristics and demotions applied after ranking, but such an approach hasn’t eliminated the problem. Accounts producing bait always find ways around such measures.

Over the past two years, LinkedIn, Meta, and YouTube, three of the largest platforms, have tried to address the root of the problem. All of them have attempted to rebuild the retrieval stage around the meaning of content, matching posts to people by what a post is about and how it relates to a reader’s interests. The idea is that once the relevance depends on semantic meaning, the tactics built for engagement farming lose their potency. However, the three companies have taken three different directions to solve the same problem, which provides us with an opportunity to understand things from multiple perspectives.

In this article, we will work through the following points:

- Why feeds relied on engagement signals for so long, and where that approach reached its limits.
- How embeddings match users and content by meaning.
- LinkedIn’s consolidation of five retrieval systems into a single language-model retriever.
- Meta’s opposite choice of keeping a large family of specialized models arranged as a funnel.
- YouTube’s generative approach, where the system produces the identifier of the next item.
- The cold-start problem, and why pretraining helps most when a user’s history is thin.
- The tradeoffs each design carries, and the limits of the engagement-bait result.

*Disclaimer: This post is based on publicly shared details from various sources. References at the end. Please comment if you notice any inaccuracies.*

## Engagement Signals

Every large feed runs on a two-step pipeline:

- **Retrieval:** This step reduces hundreds of millions of candidates down to roughly a thousand. It has to be cheap because it touches the entire corpus.
- **Ranking:** This step spends real compute ordering those survivors into the sequence you scroll.

Most of the recent architectural changes sit in retrieval, so that is where we will focus more.

For years, retrieval relied on behavioral signals. The system recorded which posts a user clicked, watched, and reacted to, then retrieved content that resembled those interactions or resembled the behavior of similar users. This approach scales well and produces reasonable feeds.

However, it also has a weakness.

When a system optimizes a single measurable objective, it tends to optimize the literal metric rather than the intent behind it. As mentioned, engagement is a proxy for relevance, and a proxy can be optimized directly. A retrieval stage tuned on interaction counts will surface whatever maximizes interaction counts, and engagement bait is the content that does exactly that. For example, content designed to trigger a click or a reply scores highly on the measured signal while contributing little to the experience the platform aims to deliver.

Suppressing such content through demotions and rules tries to treat the symptom without fixing the underlying disease. The retrieval stage still keeps bringing up the same material. A more durable fix changes what retrieval measures in the first place, and this happens by moving from behavior to meaning.

## Semantic Retrieval

The alternative is to retrieve content by its semantic content rather than by its interaction history. The ability to make this possibility depends on embeddings.

An embedding is a list of numbers that positions an item as a point in a high-dimensional space, arranged so that related items land near one another. For example, a post about fixing a leaking tap and a post about reducing water waste sit close together even when they share no keywords, because their meanings are related. In more technical terms, the embedding reflects the relationship captured during model training.

To use embeddings for retrieval, platforms apply a dual-encoder design, sometimes called a two-tower model.

- One encoder converts a user, along with their profile and recent activity, into a point in the space.
- A second encoder converts each post into a point in the same space.

Since the two encoders operate independently, a platform can compute every post embedding in advance and store it in an index. At request time, it computes the user embedding and runs a nearest-neighbor search to find the closest posts, which keeps retrieval fast across an enormous corpus.

![](https://substackcdn.com/image/fetch/$s_!4lmk!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec6cabce-8058-4a46-9bf8-fd242aec099a_3652x1466.png)

The value of this design comes from what the embeddings encode. A keyword system matches surface tokens, so it links “electrical engineering” to other posts containing those words. An embedding produced by a language model reflects associations present in its training data, which lets it link an “electrical engineer” to other concepts like grid optimization and renewable energy infrastructure, even when the exact terms differ.

This same pattern appears well beyond social feeds. Search ranking, retrieval-augmented generation, and product recommendation all use two-tower retrieval. The model here transfers to a wide range of systems a developer might build.

LinkedIn, Meta, and YouTube all adopt semantic retrieval, but they diverge in how they have built their respective solutions. Let us look at them in more detail.

## Unified Retrieval

LinkedIn’s feed previously drew candidates from separate retrieval systems, each with its own index and its own optimization logic \[1\].

One source supplied a chronological view of network activity, another handled trending posts by geography, another ran collaborative filtering, and several more produced embedding-based candidates. The setup worked, but maintaining five parallel systems led to rising engineering costs. Also, the sources were optimized independently rather than toward a single coherent objective.

In March 2026, LinkedIn replaced those systems with a single retrieval model built on a fine-tuned version of Meta’s LLaMA-3 \[1\]. The model acts as a dual encoder, converting both members and posts into one shared embedding space. It serves the entire feed through nearest-neighbor search at sub-50-millisecond latency for its member base \[1\].

![](https://substackcdn.com/image/fetch/$s_!44eb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff92618d7-0589-439f-a638-a077fd4e6df5_3346x1582.png)

However, consolidating five systems into a single language model raised a practical problem.

A language model processes text, while a recommendation system runs on structured features such as view counts, engagement rates, work history, and post metadata. LinkedIn bridged this with a prompt library that converts structured fields into templated text sequences the model can process \[1\]. See the diagram below:

![](https://substackcdn.com/image/fetch/$s_!BjYE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17f41f48-0d78-4efa-891f-59160fae50df_3598x1582.png)

In this approach, a member becomes a passage describing their profile, skills, and an ordered sequence of recently engaged posts, and a post becomes a passage describing its author, text, and engagement statistics.

We can also take a more general idea from LinkedIn’s approach. When the team fed raw popularity counts directly into the prompts, the numbers had almost no correlation with the model’s relevance scores, because large integers entered the model as arbitrary tokens. Converting each count into a ranked bucket, expressed as a percentage that the model could process in context, raised the correlation sharply and improved retrieval accuracy by roughly fifteen percent \[1\].

The takeaway from this is that the model is often the part that works, and the surrounding representation of the data is where the real effort goes.

As we can see, consolidation is one answer to solve the retrieval question. However, Meta made a different choice.

## Ranking Funnels

Meta arranges Instagram’s recommendation system as a multi-stage funnel, consisting of an ecosystem of more than a thousand models supporting it \[3\]. Candidates pass through a sequence of stages, and each stage applies a more expensive model to a smaller set of surviving candidates \[2\].

The funnel runs through four steps:

- Retrieval gathers candidates from many sources across the platform.
- Early-stage ranking uses a lightweight two-tower model to narrow that set.
- Late-stage ranking applies a heavier model to the remaining finalists.
- A final pass adjusts the result for diversity and integrity.

Where LinkedIn moved toward meaning by consolidating, Meta pursues it through specialization.

In Meta’s approach, the late-stage model predicts many possible user actions at once, and a value model combines those predictions into a single score \[4\]. That combination adds weight for positive actions, such as a likely save, and subtracts weight for predicted negative actions, such as a “See Fewer Posts Like This” tap \[4\].

The basic objective of this extends past raw engagement to include signals about content a user would prefer to avoid.

![](https://substackcdn.com/image/fetch/$s_!VrPj!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb71fc474-c3a3-4a89-b469-56455707cb9c_3178x1468.png)

This design is the one many production recommenders resemble, which makes it a useful reference point. Many competing objectives, including engagement, diversity, integrity, and creator fairness, are easier to tune and audit as separate stages than as one model. Of course, the cost to this is operational complexity, which is the exact complexity LinkedIn set out to reduce.

To summarize, both companies looked at semantic retrieval and made opposite conclusions about how much to consolidate. However, YouTube, the third platform we are looking at, questioned whether retrieval needs to search a stored index at all.

## Generative Retrieval

YouTube took a third route that removes the search index from retrieval altogether \[5\].

The system, called PLUM, assigns every video a Semantic ID, a short sequence of discrete codes derived from the video’s own content \[5\]. Videos with similar content receive similar codes, so the identifier carries information about the item rather than acting as a random label.

PLUM then adapts a pretrained language model (from the Gemini family) by adding these Semantic IDs to its vocabulary and continuing to train it on video metadata and user activity \[5\]. After this adaptation, the model performs retrieval as a generation task. Given a user’s recent history, it produces the Semantic IDs of the videos that the user is likely to watch next, decoding several candidate identifiers through beam search, and the system maps each identifier back to a real video \[5\].

See the diagram below:

![](https://substackcdn.com/image/fetch/$s_!2wSJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26f40b66-d6e1-40af-95c0-28829297282e_2886x1236.png)

This approach, however, introduces a failure mode that the index-based designs avoid, which is generating an identifier that maps to no video, and PLUM reports keeping that rate below five percent after fine-tuning \[5\].

The payoff from this solution appears in coverage. Measured against the previous production system, PLUM surfaced a far wider range of long-tail videos, and on YouTube Shorts, it raised panel click-through by 4.96 percent \[5\]. The architecture also inverts where the parameters live. The prior system stored most of its parameters in large embedding tables, while PLUM holds most of its parameters in the network itself \[5\].

Ultimately, the three designs converge on one payoff in the cold-start problem.

## Cold Start

A recommendation system faces the cold-start problem whenever a user arrives with little or no history. Behavioral retrieval has little to work with in this situation, because it depends on past interactions to find similar content, so new users historically saw generic material until their activity accumulated enough signal.

Semantic retrieval changes this.

Since a language model carries associations from pretraining, it can infer plausible interests from a profile alone. A member who lists a role in electrical engineering can be matched to content on grid optimization and energy infrastructure before clicking anything, using associations the model acquired during training rather than signals from that member’s own activity \[1\].

See the diagram below:

![](https://substackcdn.com/image/fetch/$s_!tWnb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36d78a75-dd31-41eb-a1dc-5b3546276348_2760x1744.png)

However, this capability also comes with a limit.

An inference drawn from a sparse profile can be wrong, and it can compress a person into a stereotype built from whatever their profile most resembles. The strength and the weakness have the same source, which is that the model fills gaps with prior associations. LinkedIn’s reported results fit this picture. The overall lift from the new system was modest, while the gains concentrated among new and low-connection members, which is exactly the group a meaning-based system can serve when behavioral history is sparse \[1\].

## Design Tradeoffs

Every one of these designs has an associated cost and tradeoffs.

The first is consolidation against specialization. LinkedIn’s single model is simpler to maintain and aligns retrieval with ranking, while Meta’s many-model funnel gives independent control over each objective and provides natural redundancy. A single model also raises a more difficult rollback question, because five specialized systems offered five independent places to intervene when one of them regressed on a case such as trending content.

The second tradeoff is related to cost. Language-model embeddings capture richer associations than the lightweight methods they replaced. However, they consume more compute to produce and serve. As LinkedIn’s popularity-count finding showed, the model is rarely the bottleneck, and the load moves to the data pipeline, the feature representation, and the serving path.

The third tradeoff sits between the generative and index-based approaches. Generative retrieval composes items from compact codes and removes the large embedding table, at the cost of a failure mode where the model can produce an identifier for a video that does not exist. Index-based retrieval avoids that failure mode, but requires storage and maintenance of the index.

![](https://substackcdn.com/image/fetch/$s_!f8Hi!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69f60f86-3fa1-420e-84fc-b1bbb745c72b_3652x1868.png)

Semantic retrieval reduces the leverage of bait rather than removing it, since a system can still be gamed by content engineered to match high-value topics. Also, these three designs are points of emphasis on shared scaffolding more than pure types. YouTube still ranks candidates in stages, LinkedIn’s retriever feeds a separate ranking model, and Meta continues to explore generative methods.

## Conclusion

Social media feeds are transforming retrieval approaches from behavioral engagement to semantic meaning. This helps reduce the leverage of engagement bait as a property of the architecture.

However, the three largest platforms adopted the same underlying idea and built it in three ways.

- LinkedIn consolidated five retrieval systems into a single language-model dual encoder and searches one shared embedding space.
- Meta kept a large family of specialized models arranged as a staged funnel with a multi-objective value model.
- YouTube generates the identifier of the next item through an adapted language model and removes the retrieval index.

The reason these choices differ comes down to data.

A text-rich professional network, a multi-objective media platform, and a video service with an enormous item corpus each favor a different design, and each team optimized for the structure of their specific data.

**References:**

\[1\] [Large Scale Retrieval for the LinkedIn Feed using Causal Language Models](https://arxiv.org/abs/2510.14223)

\[2\] [Scaling the Instagram Explore recommendations system](https://engineering.fb.com/2023/08/09/ml-applications/scaling-instagram-explore-recommendations-system/)

\[3\] [Journey to 1000 models: Scaling Instagram’s recommendation system](https://engineering.fb.com/2025/05/21/production-engineering/journey-to-1000-models-scaling-instagrams-recommendation-system/)

\[4\] [Powered by AI: Instagram’s Explore recommender system](https://instagram-engineering.com/powered-by-ai-instagrams-explore-recommender-system-7ca901d2a882)

\[5\] [PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations](https://arxiv.org/abs/2510.07784)