---
title: "DoorDash Dispatch: Building a Lightning-Fast Delivery System"
source: "https://blog.bytebytego.com/p/doordash-dispatch-building-a-lightning?utm_source=post-email-title&publication_id=817132&post_id=225841091&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-11-24
created: 2026-11-24
description: "In this article, we’ll look at how DoorDash Dispatch built a lightning-fast delivery system."
tags:
  - "clippings"
---
## Plan 2027 for more AI code while reducing CI spend (Sponsored)

[![](https://substackcdn.com/image/fetch/$s_!t6Wa!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8afaf3bb-0e3f-44c0-9bf8-3feeef845f36_1600x840.png)](https://go.bytebytego.com/warpbuild_112326)

Next year your team will write more code with AI than ever. That means more commits, more CI and a bigger bill, unless your runners change.

WarpBuild is the fix teams at Braintrust, Raycast, OpenRouter, Comcast and Jane Street already use:

- Twice as fast at half the cost
- One line change to runs-on
- Linux, macOS and Windows on x86-64 and ARM64
- Unlimited macOS concurrency
- Pay only for what you use

Use code START50 for $50 in free credits.

---

DoorDash’s dispatch platform has to make a lot of good delivery-related decisions while the situations around the system and its environment keep changing.

To deal with the ever-growing need for innovation, the DoorDash engineering team had to redesign the dispatch system.

With the redesign, they were able to deal with two main problems. One was about how to divide the calculations into smaller pieces. The second was about how to run those pieces across many machines without losing the information that might be needed to make good assignment decisions.

In this article, we’ll look at how DoorDash Dispatch built a lightning-fast delivery system. Here’s what we’ll cover:

- The role of a dispatch system
- Why did the old dispatch system at DoorDash struggle
- Why couldn’t DoorDash just add more servers
- Separating coordination from heavy computation
- Breaking the optimization problem into smaller pieces
- How did DoorDash replace such a critical system safely
- The improvements after the new system

*Disclaimer: This post is based on publicly shared details from various sources. References at the end. Please comment if you notice any inaccuracies.*

[![](https://substackcdn.com/image/fetch/$s_!hEuU!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4b9e484-8f47-4737-b746-afecee668f44_4164x1794.png)](https://substackcdn.com/image/fetch/$s_!hEuU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4b9e484-8f47-4737-b746-afecee668f44_4164x1794.png)

## What Does a Dispatch System Actually Do

When you place an order for food, several things take place to make the order successful. The restaurant cooks the food, and a delivery driver arrives at the restaurant to collect the food. After collecting the food, that driver brings it to you. DoorDash calls its delivery drivers Dashers.

The dispatch system is the one that takes care of all these activities by deciding which Dashers should be given which orders to deal with. To make that decision, the system has to know a lot more than just which Dasher is closest to the restaurant. For example, let’s say you have a Dasher who is two minutes away, but the restaurant needs another 15 minutes to get the food ready. If you send that Dasher immediately to the restaurant, it can create a long wait time. You might have another Dasher who is much farther away, but they might reach the restaurant closer to the food preparation time. Also, you might have two orders going in a similar direction that could be clubbed into a single delivery trip.

As you can see, the dispatch system has to consider both space and time while making these decisions. Space includes the locations of Dashers, restaurants, and customers. Time includes travel durations, traffic conditions, food preparation, and delivery expectations.

You can think of this as being quite similar to the vehicle routing problem. Making decisions about how vehicles should handle a collection of destinations while working within a set of constraints. DoorDash’s version of this problem is especially demanding because the inputs keep changing. You have new orders arriving all the time. Dashers are always on the move. Food preparation estimates change even as the system is calculating.

This gives dispatch an unusual requirement. A decision about a particular order must be good enough, but it should also be taken fast enough to be useful. If you calculate an assignment most beautifully, it’s useless if doing so takes a long time.

This relation between the quality of decisions and speed of making those decisions is the starting point for the entire redesign.

## Why Did the Old System Struggle as DoorDash Grew?

DoorDash’s previous dispatch engine was built as a monolith. This means that several major responsibilities were brought together into one tightly connected system.

It maintained the state of the delivery network, applied business rules, and performed expensive routing calculations. You can think of the state as the information about the current situation, such as available Dashers and orders awaiting assignment.

The old engine performs several stages in sequence. DoorDash used that engine to generate possible assignments, check proposed routes, and then optimize the choices. Candidate generation means coming up with possibilities that the system can evaluate. Optimization is all about selecting a good enough combination of those possibilities according to its goals and constraints.

The difficulty with the old engine was that the computational work grew much faster than the delivery volume. This is because the important algorithms in the original engine had roughly quadratic complexity. It meant that doubling the size of the input could produce approximately four times the computational work.

You can understand this pressure by thinking about possible Dasher-to-order combinations. If both the number of Dashers and the number of orders increase, the number of potential pairings grows quickly. If you evaluate routes and batches, it adds further work.

During peak periods, the demand can go up to nearly four times the system’s dispatch processing capacity. The engine had to limit what it took into consideration or fall back to simpler decision rules. The delays caused by this also damaged the usefulness of its calculations. A Dasher might move away from a promising pickup. Or food that is ready might sit waiting while the engine was still making the decision.

As you can see, the problem went beyond just slow software. Slow computation changed the quality of real-world deliveries with a pretty tangible impact on the user experience.

## Why Couldn’t DoorDash Just Add More Servers?

If you add servers, it’s called horizontal scaling. It works quite well when you can divide work into independent requests. For example, let’s say you have many requests that display unrelated product pages, and those can be handled by different servers. One server generally doesn’t need to coordinate its answer with every other server answering a page request.

However, dispatch assignments have more dependencies.

Let’s say you have two nearby restaurant orders that could share a delivery trip. If you randomly send those orders to separate workers, each worker may find a reasonable individual assignment. But they won’t get the opportunity to deal with both of them. Similarly, two workers could independently identify the same Dasher as a promising choice.

There is also a systems problem. Even if you can somehow distribute the calculations, some component must prepare the work, send the necessary data, gather the results, and combine them. If that component becomes overloaded, you have just moved the bottleneck to a different place rather than removing it completely.

DoorDash therefore had to answer two questions at the same time:

- How can the application distribute computation across more machines?
- How can the optimization problem be divided while keeping useful relationships between orders, routes, and Dashers?

The first question needed a change to the architecture. The second required changing how the work was organized.

## Separating Coordination from Heavy Computation

DoorDash rebuilt the platform around two independently scalable tiers. You can think of a tier as a group of components with a particular responsibility.

- The coordinator tier takes care of the dispatch process. You can use it to maintain the broader logistics state, apply business rules, and organize the work that needs to happen.
- The compute tier is made up of workers that run expensive calculations. These workers generate and evaluate routing possibilities, run optimization routines, and execute ML models.

Separating the two tiers lets you increase compute capacity without the need for every worker to take over all the responsibilities of the original engine. You can get a simple view of this execution flow in the following manner:

- The workers operate in parallel. The reconciliation step combines their results into coordinated dispatch decisions.
- However, if you distribute computation, you introduce a communication cost. If every worker gets a complete copy of the entire logistics state on every run, transmitting and processing that data could become quite costly.

[![](https://substackcdn.com/image/fetch/$s_!ZWQG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F901e9894-e76a-4af9-91d7-0e2a1badd0f5_4776x2152.png)](https://substackcdn.com/image/fetch/$s_!ZWQG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F901e9894-e76a-4af9-91d7-0e2a1badd0f5_4776x2152.png)

DoorDash takes care of this through localized payload sharding. You can think of a payload as the data sent with a job, and sharding means dividing that data into smaller portions. Each worker receives the local context needed for its assigned calculation.

The coordinator sends these payloads over gRPC, which is a framework for communication between services. This happens on each dispatch tick. Or each round of dispatch processing.

The payloads are totally self-contained. This way, you can keep the workers stateless. A worker can still hold a trained model or temporary calculation data. The key separation is that the responsibility for managing the changing logistics state remains with the coordinator.

## Breaking the Optimization Problem Into Smaller Pieces

Separating the tiers makes it possible to execute things in parallel. But it doesn’t automatically bring down the size of the optimization problem.

If every worker still had to evaluate a huge, interconnected set of possibilities, the original computational pressure would be high. Therefore, DoorDash introduced hierarchical decomposition, which means breaking a large problem into smaller problems through multiple stages.

The coordinator groups the broader dispatch problem into localized geographic clusters and delivery trajectories. This is to create manageable pieces that retain the local relationships important to routing.

[![](https://substackcdn.com/image/fetch/$s_!pFvW!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd72c25e-8207-44d5-9953-a0dbd22f0ca1_4482x1864.png)](https://substackcdn.com/image/fetch/$s_!pFvW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd72c25e-8207-44d5-9953-a0dbd22f0ca1_4482x1864.png)

The first is rapid pre-clustering, which you can use to create initial groups.

The second is centroid-based refinement, which is used to refine those groups using their centers. For reference, you can think of a centroid as a representative center of a group of points.

The main point here is that partitioning takes place through an initial grouping and is followed by refinement. You can think of each partition as a piece of work for a compute node. This node generates and checks possibilities within its local context while other nodes work on other partitions.

This has two benefits. Smaller problems reduce the number of combinations each worker must take into account, and parallel execution lets you process several problems at the same time.

But you still want local solutions to fit together. The software introduces a geographic boundary to organize computation. It doesn’t correspond to a real separation between delivery opportunities. Orders and routes near that boundary may still be related.

Therefore, DoorDash uses a global reconciliation and scoring layer to combine results across partitions before you can select final assignments. This preserves much of the optimization quality of the original problem while letting expensive candidate generation take place in parallel.

You can think of the workers as producing useful local options and reconciliation as considering how those options can be combined into the broader dispatch decisions.

## How Did DoorDash Replace Such a Critical System Safely

Dispatch directly affects active deliveries. A defective setup could send Dashers to poor assignments, increase waiting time, or disrupt fulfillment.

The DoorDash engineering team started with shadow testing.

In shadow mode, you duplicate the incoming production work. They sent one to the existing engine, and another went to the new platform. The existing engine continued to control actual deliveries. However, the new engine also calculated what it would have done. But its output was recorded for analysis purposes.

[![](https://substackcdn.com/image/fetch/$s_!aE-D!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c496657-d7ab-463c-b9c7-f20ea67858b1_1974x2842.png)](https://substackcdn.com/image/fetch/$s_!aE-D!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c496657-d7ab-463c-b9c7-f20ea67858b1_1974x2842.png)

This lets the developers check the new platform under real production conditions. Also, including peak traffic. They could compare proposed matches, delivery-time-related behavior, and resilience against the existing system.

This approach is known as behavioral regression analysis. You can think of a regression as a change that makes some previously acceptable behavior worse. The team had to establish that the new architecture took care of dispatch quality as well as improve performance.

However, shadow testing has a practical limit. Since the decisions made by the new system are not actually executed, you cannot use it to fully check the real-world impact of those decisions.

Therefore, the DoorDash engineering team followed shadow testing with production switchback experiments. In a switchback experiment, your systems take turns controlling real production activity under controlled conditions. This let them compare their outcomes. The DoorDash engineering team used limited exposure and fallback mechanisms while checking system reliability and fulfillment results. Only when they were satisfied did they expand the rollout to a wider user base.

The progression was that shadow testing gave a lot of confidence in the new engine’s behavior on live production inputs, whereas controlled production experiments tested what happened when the decisions made an impact on deliveries.

## The Improvements

DoorDash reports a great deal of improvement in the platform’s capacity and responsiveness after the implementation of the new dispatch system.

The detailed results are as follows:

- Ten times the dispatch processing scale, enabled by distributing computation.
- More than 99.96% of runs completed in under 20 seconds, compared with execution stretching to minutes under heavy load in the old system.
- More than 99.99% availability during Super Bowl traffic spikes, despite a 10% week-over-week increase in peak volume.

[![](https://substackcdn.com/image/fetch/$s_!vodx!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd718a853-2bf8-44f9-95ed-744f8a9bb734_3812x1864.png)](https://substackcdn.com/image/fetch/$s_!vodx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd718a853-2bf8-44f9-95ed-744f8a9bb734_3812x1864.png)

**Source:** [DoorDash engineering blog](https://careersatdoordash.com/blog/how-doordash-built-a-next-generation-real-time-dispatch-platform/)

You can use these measurements to think about different properties. Processing scale is all about how much work the system can handle. Execution latency deals with how long a run takes. Availability is whether the system remains operational.

For dispatch, all three results matter. You can have a platform that can eventually process a large volume, but it can still cause problems if individual decisions are taken too slowly.

The additional capacity also lets the system evaluate a larger set of possibilities instead of restricting its search aggressively during busy periods. DoorDash connects this broader search to improved Dasher acceptance rates, fulfillment efficiency, and Dasher earnings. They also report millions of dollars in annualized fulfillment savings.

The practical benefit was that decisions arrived faster, and the platform had enough computational room to consider better assignments.

## Conclusion

The redesign also made it possible to have machine learning. With the new platform, they could make it practical to run more computationally demanding ML models inside the dispatch process.

A trained model performs inference when it processes an input and produces an output, such as a score for a proposed route. If dispatch needs enormous numbers of these evaluations, even a small cost per evaluation can become significant.

DoorDash introduced two model-serving tiers to handle different needs.

[![](https://substackcdn.com/image/fetch/$s_!YsQ9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fced3f675-c5d1-465f-8334-b41992b1ad38_3134x2564.png)](https://substackcdn.com/image/fetch/$s_!YsQ9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fced3f675-c5d1-465f-8334-b41992b1ad38_3134x2564.png)

L1 serves models locally inside compute workers. Each worker contains ONNX Runtime, which is software that executes trained ML models. Since these evaluations happen locally, they avoid a network round trip to a separate model server.

L2 serves models through separate remote infrastructure. This tier handles more complex policy evaluations that occur less frequently. These heavier models run in isolated ML serving clusters, helping separate their computational demands from the coordinator’s state-management responsibilities.

The main idea is that frequent evaluations need a very short execution path, while heavier but less frequent evaluations can use dedicated remote capacity.

The platform also enabled a multi-agent RL system that adjusts the optimizer’s priorities. You can think of reinforcement learning (RL) as an approach in which a system learns how to make decisions by getting feedback about results. In DoorDash’s application, the agents adapt objective weights. These weights determine how strongly the optimizer favors different goals, such as delivery speed and batching efficiency.

Ultimately, the biggest contribution of the new platform wasn’t one isolated performance gain. It has managed to change the long-term trajectory of DoorDash’s dispatch system.

**References:**

- [How DoorDash built a next-generation real-time dispatch platform](https://careersatdoordash.com/blog/how-doordash-built-a-next-generation-real-time-dispatch-platform/)

---

∙