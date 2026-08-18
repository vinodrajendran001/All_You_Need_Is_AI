---
title: "Waymo vs Tesla: Two Ways to Build Self-Driving Cars"
source: "https://blog.bytebytego.com/p/waymo-vs-tesla-two-ways-to-build?utm_source=post-email-title&publication_id=817132&post_id=210941869&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-08-17
created: 2026-08-18
description: "In this article, we will take a look at both approaches."
tags:
  - "clippings"
---
## Matic: The World’s First Intuitive Home Robot has arrived. (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!rDCR!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e7cbbdb-7b6b-4597-8b26-bb120ff3faf5_1600x840.png)

Designed and assembled in America, Matic is the world’s first robot built to understand you. Its new feature, Matic Cues, lets you interact with it like you would anyone else.

- **Point and speak.** Say “Hey Matic, clean this” while pointing at a mess, and Matic knows exactly what to clean.
- **Understands 70+ languages.** Ask Matic to clean the kitchen, follow you, or go to the sink, in whatever language you speak.
- **Skip the app.** Anyone at home can use Matic, not just app-savvy adults, but kids and grandparents too.

Every home robot before this needed an interface. Matic just needs you to talk.  
Try Matic, backed by their 6 month money back guarantee.

---

A vehicle travelling at 40 miles per hour covers about 60 feet every second. Within that second, software has to determine what is physically nearby, classify each object, estimate where those objects will move, select a path, and issue steering and braking commands.

Doing all of this quickly is something that has been largely solved. However, doing this correctly in unpredictable and distinct traffic situations is still an open problem. This is because real-world traffic produces more distinct scenarios than any team can pre-determine. For example, Waymo describes one such case, where a vehicle is on fire on the road ahead while the drivable lanes remain physically clear \[3\]. The geometry of such a scenario might permit driving straight through it. However, the real meaning of it calls for turning around or taking preventive action.

Waymo and Tesla, two companies investing in self-driving cars, have tried to come up with different types of answers to these questions.

For reference, Waymo reports 220.6 million rider-only miles through March 2026. These are miles covered with no human in the driver’s seat, across five metro areas \[5\]. On the other hand, Tesla reports more than three million vehicles in the United States covering over 30 billion miles a year, with 1.28 million active Full Self-Driving subscriptions in the first quarter of 2026 \[10\]. Almost all of those Tesla miles involve a driver who remains responsible for the vehicle. Tesla’s driverless service is separate and much smaller, running without safety monitors in Austin, Dallas, and Houston, while the Bay Area service uses a safety driver \[10\].

Both approaches depend heavily on machine learning. But they differ in how much gets fixed in advance. In this article, we will take a look at both approaches while trying to answer the following questions:

- How does each system detect what is physically nearby?
- What each builds from that data, and why one keeps the result readable?
- How each estimates what other road users will do?
- How a path gets selected, and what verifies it before the vehicle acts?
- What safety evidence each publishes, and why the figures measure different things?
- Where does the knowledge inside each system come from?

![](https://substackcdn.com/image/fetch/$s_!biFm!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd244e59-44d8-47d0-acc7-20da9a6a99e1_3706x1852.png)

*Disclaimer: This post is based on publicly shared details from various sources. References at the end. Please comment if you notice any inaccuracies.*

## Sensing

A camera records light intensity across a grid of pixels. Distance appears nowhere in that grid, so depth has to be computed from the arrangement of pixels, but that computation can be wrong. A large object far away and a small object nearby can occupy the same region of an image.

Lidar arrives at the same answer by a different route. The unit emits laser pulses, measures how long each pulse takes to return after reflecting off a surface, and converts that interval into a distance. We can think of the output of this as a point cloud, which is a three-dimensional set of measured points describing the surfaces around the vehicle \[1\]. The distance is no longer an estimate but a measurement.

Waymo’s sixth-generation system, which began fully autonomous operations in February 2026, carries 13 cameras, four lidar units, six radar units, and a set of external audio receivers used to detect sirens and railroad crossings \[2\]. Coverage overlaps in every direction and extends to 500 metres. This overlap is for help situations when rain, road grime, or ice limits what a camera captures. Lidar and radar sustain the perception capabilities in such scenarios. \[2\].

Tesla’s vehicles mainly rely on cameras. Instead, Tesla relies entirely on a “pure vision” approach that uses exterior cameras and artificial intelligence to navigate. For example, Tesla’s documentation describes Model 3 and Model Y as running camera-based Tesla Vision, without radar, using cameras and neural network processing \[9\].

See the diagram below:

![](https://substackcdn.com/image/fetch/$s_!U4xe!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F027e4664-68a9-4cff-973f-82ae093e6d66_2546x1516.png)

There is another point here that requires our attention. Waymo’s fifth-generation Jaguar I-PACE vehicles carry 29 cameras \[1\]. The sixth-generation system carries 13, which Waymo attributes to a 17-megapixel imager covering the same area with fewer than half the cameras \[2\]. In other words, Waymo is also reducing overall sensor count while continuing to describe redundancy as essential.

![](https://substackcdn.com/image/fetch/$s_!lC1k!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6cd45f01-52ef-4847-b80a-3b9881f63361_3142x1470.png)

The tradeoff here is that a direct measurement costs money while adding a component that can fail noticeably. However, a derived value may not cost much, but it can be wrong as well.

## Representation

Something has to convert millions of pixels and points into a description that the system can understand and operate on. The nature and form of that description is one of the most important architectural decisions for an autonomous driving setup.

Waymo places the Waymo Foundation Model at the centre, built from two components:

- **Sensor Fusion Encoder:** It merges camera, lidar, and radar data over time and outputs objects, semantic attributes, and embeddings. These are compact numerical summaries that downstream components consume.
- **A Driving VLM:** Trained using Gemini and fine-tuned on Waymo driving data, they cover rare situations requiring background world knowledge, such as the burning vehicle example mentioned earlier.

Both feed a World Decoder that forecasts the behaviour of other road users, produces high-definition maps, generates candidate trajectories, and emits signals used to verify them.

The system maintains compact structured representations, meaning explicit lists of objects, their semantic attributes, and roadgraph elements describing lanes and connections. The Waymo engineering team provides three reasons for such a setup:

- Correctness and safety validation can run at inference time, while the vehicle is moving
- Simulation runs efficiently at large scale, because a compact world state is cheap to replay and modify
- Training feedback becomes verifiable, since a component evaluating driving quality has something concrete to measure

This design provides significant benefits over pure end-to-end or modular approaches \[3\].

Tesla’s documentation talks about per-camera networks performing semantic segmentation, which assigns every pixel to a category, plus object detection and monocular depth estimation, meaning distance estimated from a single camera \[6\]. Those feed birds-eye-view networks that output road layout, static infrastructure, and three-dimensional objects in a top-down view. A full build involves 48 networks taking nearly 70,000 GPU hours to train and producing 1,000 distinct tensors per time step \[6\].

See the diagram below:

![](https://substackcdn.com/image/fetch/$s_!Ityl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9936eada-f9fd-4a3d-ba4c-7b391d95e8fe_3096x1622.png)

Prior mapping also occupies one end of this decision. For example, Waymo surveys a territory before operating there, recording lane markers, signs, curbs, and crosswalks. It then matches those maps against live sensor data to establish position, since GPS alone can lose signal \[1\]. The map is basically knowledge acquired once and reused. It saves computation on every trip, but also creates an obligation to keep it current. In contrast, Tesla’s approach skips the survey and derives equivalent information during the drive.

![](https://substackcdn.com/image/fetch/$s_!MM2r!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F456788c5-ef9f-49c3-a5dd-d3bdf5a0ae43_3094x1454.png)

The trade-off is that a structured representation can be inspected, logged, replayed, and checked against explicit criteria. But it limits what the system can express. On the other hand, a learned representation carries nuance no schema can anticipate.

## Prediction

Once the system holds a description of its surroundings, the next task is estimating what those objects will do. Several futures are valid at the same moment. For example, a cyclist approaching an intersection might continue straight, turn, or stop. A safe response should account for all possibilities.

Waymo describes the system as producing many possible paths for each road user rather than one, drawing on accumulated driving data and accounting for the different ways a car, a cyclist, and a pedestrian move \[1\].

In June 2025, Waymo published research on whether prediction quality scales predictably \[4\]. Using an internal dataset spanning 500,000 hours of driving, the study found that motion forecasting quality follows a power law in training compute, matching a pattern observed in language models. A power law here means each doubling of compute yields a proportional, predictable improvement. Data scaling proved critical, and increasing compute at inference time improved performance on harder scenarios.

Waymo reported the same trend in closed-loop performance, where results are measured in simulations in which the system’s own actions change what happens next. This trend suggested that real-world driving improves with more data and compute, rather than only benchmark scores.

Tesla’s describes an upgraded reinforcement learning stage in version 14.3, intended to cover long-tail edge cases, meaning rare situations that appear infrequently even across very large mileage \[10\].

See the diagram below:

![](https://substackcdn.com/image/fetch/$s_!638Z!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F305a76c0-9190-49e1-8a33-b8ff84500c86_3096x1584.png)

A system that commits to one predicted future becomes fragile in situations where prediction matters most. However, carrying several weighted futures costs compute on every cycle, but can guard against the possibility of unusual situations.

## Planning

With a description of the surroundings and a set of likely futures, the system selects a trajectory. You can think of it as a specific path with speeds attached to it. The question is what verifies the trajectory before the vehicle executes it.

Waymo trains large Teacher models to generate safe, comfortable, and compliant action sequences. It then distils them into smaller Student models sized to run onboard in real time \[3\]. Distillation transfers behaviour from a large model to a compact one. Output from that Student model then passes through a separate onboard validation layer, which verifies the trajectories the generative model produced \[3\]. This means that two independent components have to agree before the vehicle moves.

Tesla talks about building a planning and decision-making system that operates under uncertainty, with algorithms evaluated at the scale of the entire fleet, optimising for throughput, latency, correctness and determinism \[6\].

For Tesla vehicles on the road today, verification comes from a person. Full Self-Driving (Supervised) requires an attentive driver and leaves the vehicle slightly short of autonomous \[7\]. The system enforces this through a strikeout mechanism, where repeated inattention warnings disengage the feature for the remainder of a trip. Enough strikeouts suspend access for a week \[7\]. In the driverless service, that role belongs to safety monitors or remote supervision \[10\].

A validation layer catches a category of unacceptable outputs before they reach the actuators, and it can only evaluate against the defined criteria. Anything outside those criteria passes through unexamined. This is the same tradeoff as an assertion in production code, where the check is only as good as the condition behind it.

See the diagram below:

![](https://substackcdn.com/image/fetch/$s_!9i83!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafa75439-2874-4739-ac9d-331d2057ba9e_3096x1584.png)

## Validation

Waymo’s Safety Impact hub reports 220.6 million rider-only miles through March 2026, meaning no human occupied the driver’s seat for any of them \[5\]. Measured against human crash rates in the same operating areas, adjusted for where within each city the service drives, the reported reductions are 94% for serious injury or worse crashes and 82% for injury-causing crashes \[5\]. The methodology has been published in peer-reviewed journals, and the raw data is downloadable so third parties can reproduce the figures \[5\].

Tesla’s Vehicle Safety Report takes a different form. It compares Teslas with Full Self-Driving (Supervised) engaged against Teslas driven manually, using the same telemetry pipeline for both, and reports 7 times fewer major and minor collisions and 5 times fewer off-highway collisions \[7\]\[8\]. A collision counts as occurring with the system engaged if it was active at any point within five seconds beforehand, a window chosen to capture cases where a driver took over shortly before impact \[8\]. Tesla attributes no fault in the reported data, treating that determination as too subjective to include \[8\].

![](https://substackcdn.com/image/fetch/$s_!1PQT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb1270fc7-f529-4eb2-8e9d-4185ed54d342_3212x1584.png)

As you can see, the two reports answer different questions, and we can’t simply do a side-by-side comparison. The difference comes down to what each population represents:

- Waymo is measuring outcomes across miles where no person was available to intervene.
- Tesla is measuring whether an assistance system reduces collisions while a driver remains responsible.

Both companies also state their own limitations. Waymo states that no perfect comparison between autonomous and human data exists today, and that its operating cities see no appreciable snowfall \[5\]. Tesla states that its estimate of a United States average involves unavoidable assumptions that may skew the figure in either direction \[8\].

Waymo separates two things that are easy to conflate. Safety impact gets measured after deployment. Whether a release is acceptable to deploy at all gets determined beforehand through a Safety Framework and a Safety Case \[5\].

## Training

Both systems improve between releases. However, the underlying mechanisms differ as much as the architectures.

Waymo runs three components off the same foundation model:

- The Driver produces action sequences.
- The Simulator generates scenarios for training and testing.
- The Critic evaluates driving quality and surfaces problems.

Large versions of each get distilled into smaller ones that run at the required volume. Two loops connect them:

- An inner loop applies reinforcement learning inside simulation, where scenarios can be generated and repeated cheaply.
- An outer loop begins with the Critic flagging suboptimal behaviour from real driving, turns improved alternatives into training data, verifies the fixes in simulation, and deploys only once the safety framework confirms the absence of unreasonable risk.

Waymo states that its fully autonomous mileage now far exceeds its manually driven data, and that no volume of simulation or test-driver operation reproduces the situations encountered when the system operates with no driver present \[3\].

Tesla’s data comes from a consumer fleet. The Vehicle Safety Report describes two telemetry paths \[8\]. On shifting to park, a vehicle transmits anonymised mileage broken down by control type and road classification. On detecting a major or minor collision, it transmits a separate packet tied to the vehicle. Tesla reports receiving 2.5 billion telemetry packages in the third quarter of 2025 alone. Tesla has also built an evaluation infrastructure from anonymised fleet clips assembled into test suites, alongside simulation producing sensor data for automated testing \[6\]. Training runs on Cortex 1, listed at over 100,000 H100-equivalent GPUs in production, and Cortex 2 at over 130,000 in early ramp.

See the diagram below:

![](https://substackcdn.com/image/fetch/$s_!tCyf!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c7303ea-50df-466b-b1a1-d40ff7bfeb02_3096x1584.png)

## Conclusion

The same question recurs at every stage of an autonomous driving process.

How much gets determined in advance and written into a form that can be examined, and how much gets computed during the drive by a model whose internal state stays out of reach?

Each stage poses one version of it:

- Sensing asks whether distance arrives as a measurement or as a derived value
- Representation asks whether the description of the world stays inspectable
- Prediction asks how many futures the system carries at once
- Planning asks what verifies a trajectory before execution
- Validation asks what kind of safety claim the resulting evidence can support
- Training asks which miles improve the system

Waymo sits further toward written-down knowledge at most stages. This involves per-city preparation and purpose-built hardware. Tesla sits further toward computed knowledge. Both positions have merit, and only the future will tell which approach becomes more dominant or do things fall somewhere in the middle.

**References**

1. [Self-Driving Car Technology for a Reliable Ride, Waymo](https://waymo.com/waymo-driver/)
2. [Beginning fully autonomous operations with the 6th-generation Waymo Driver, Waymo, February 2026](https://waymo.com/blog/2026/02/ro-on-6th-gen-waymo-driver)
3. [Demonstrably Safe AI For Autonomous Driving, Waymo, December 2025](https://waymo.com/blog/2025/12/demonstrably-safe-ai-for-autonomous-driving)
4. [New Insights for Scaling Laws in Autonomous Driving, Waymo, June 2025](https://waymo.com/blog/2025/06/scaling-laws-in-autonomous-driving)
5. [Waymo Safety Impact, Waymo](https://waymo.com/safety/impact/)
6. [AI and Robotics, Tesla](https://www.tesla.com/AI)
7. [Full Self-Driving (Supervised), Tesla Support](https://www.tesla.com/support/fsd)
8. [Full Self-Driving (Supervised) Vehicle Safety Report, Tesla](https://www.tesla.com/fsd/safety)
9. [Autopilot and Full Self-Driving Capability, Tesla Support](https://www.tesla.com/en_qa/support/autopilot)
10. [Tesla Q1 2026 Update, Tesla Investor Relations](https://assets-ir.tesla.com/tesla-contents/IR/TSLA-Q1-2026-Update.pdf)