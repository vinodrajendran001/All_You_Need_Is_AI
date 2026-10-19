---
type: concept
created: 2026-10-19
updated: 2026-10-19
tags: [concept, robotics, training-data, simulation, scaling]
source_ids:
  - src-2026-10-15-potter-how-to-train-your-robot
  - src-2026-09-14-rhoda-web-video-pretraining-robots
  - src-2026-06-05-fei-fei-li-taxonomy-world-models
  - src-2026-10-01-neuralink-unlabeled-brain-pretraining
  - src-2026-09-23-kwok-contrastive-language-models
  - src-2026-08-18-bytebytego-waymo-vs-tesla
status: active
---

# Robot Training Data

## Definition

Robot training data is action-relevant evidence for learning a control policy: recordings of a
task being done or attempted, combined from the robot's state, its camera views, and the actions
taken — or, failing that, a reliable way to score an attempt. Unlike language-model text, it has no
large pre-existing public stock. It has to be manufactured, and every manufacturing route gives up
one useful property to gain another.

## Why it matters

The vault's LLM material mostly treats raw data as abundant and the hard part as filtering,
rephrasing, or synthesis ([[Synthetic Data Flywheel]]). Robotics inverts that. The binding question
is where demonstrations come from and how far each kind transfers to a physical robot. Whether robot
capability follows LLM-style scaling depends on that answer, and the current evidence is mostly
company-reported volumes rather than controlled transfer results.

## Current synthesis

### No route maximizes all four properties

[[Brian Potter - How to Train Your Robot]] surveys the routes. Reading across his account, each can
be judged on four properties: **embodiment fidelity** (does the data match the robot's own body and
actions), **physical accuracy** (are the dynamics real), **diversity**, and **cost per hour**. The
four-axis framing is the vault's synthesis; the qualitative judgments in the table are Potter's.

| Route | Embodiment fidelity | Physical accuracy | Diversity | Cost |
| --- | --- | --- | --- | --- |
| Teleoperation | Exact | Real | Limited: robots must be repositioned per task | High: a robot and an operator per hour |
| Deployed robots | Exact | Real | Low: real-world data is extremely repetitive | Low at the margin, but few robots do real work yet |
| Simulation with RL | Exact for the simulated body | Only as good as the simulator | High: parameters can be randomized | Low |
| Human egocentric video and sensors | Mismatched with the robot | Real | High | Much cheaper than teleoperation |
| UMI grippers | Small mismatch | Real | High | Cheaper than teleoperation; see prices below |
| Generic web video | None: no robot actions | Real but unlabeled | Highest | Near zero to collect |

Two consequences follow. First, routes are complements rather than substitutes, which is how
practitioners appear to use them: Agility Robotics' Digit walks with a 1-million-parameter network
trained by simulated RL, while its manipulation "seems to have been" learned by behavioral cloning.
Second, every cheap, diverse route carries a gap — embodiment for human and video data, physics for
simulation — so savings in collection reappear as the cost of bridging that gap.

### Simulation buys volume where physics is easy

[[Fei-Fei Li - A Functional Taxonomy of World Models]] argues that the simulator is the most
consequential and most under-built world-model category, and that generated geometry can look
correct while containing broken physics. Potter reports the practical consequence for robot data.
Simulated RL works well for locomotion, where dynamics are well characterized — Figure AI trained
walking on thousands of simulated robots — and poorly for contact-rich or deformable manipulation,
the sim-to-real gap. Domain randomization hedges unknown parameters instead of modeling them, but
OpenAI's Rubik's Cube hand used about **13,000 simulated years** and reached **20%** success on
maximally difficult starting arrangements.

The vault has met this dependency before. [[Jacky Kwok et al - Contrastive Language Models]]
manufactures hard negatives with a model, so that generator's blind spots become the embedding
space's residual failures. Simulated robot data has the same shape: it is only as physical as the
simulator that produced it, so the simulator's blind spots — friction, contact, deformation —
become the policy's. The analogy is the vault's, not either source's.

### Hours are not a common currency

Reported volumes span more than two orders of magnitude: Open X-Embodiment's roughly **4,000
hours** (2023), Pi 0's **10,000 hours** (2024), Generalist AI's GEN 1 at around **500,000 hours**
of UMI data, and Dyna Robotics' and Nature Will's claims of over **1 million hours** of egocentric
video. These are different goods. Potter notes that teleoperation and UMI hours are probably worth
more than egocentric video, that variety matters more than repetition, and that video frames are
highly correlated. The reading-time conversion (GPT-4 as roughly **685 million hours**) and Chris
Paxton's token conversion (about **3,600 useful tokens per hour** after a tenfold discount) agree
only to an order of magnitude, and Potter calls the first "somewhat dubious."

The vault's adjacent evidence warns against pooling hours across bodies.
[[Neuralink - Pretraining on 50,000 Hours of Unlabeled Brain Data]] describes a pooled corpus of
more than 50,000 hours, yet every live result used participant-specific encoders, and pooled
multi-participant models had **not improved online performance**. That is neural decoding, not
robot control, so it is an analogy rather than a result. It still makes the cross-embodiment
question concrete: Open X-Embodiment was stitched from dozens of datasets across robot types, and
whether such pooling helps a given robot is measurable rather than implied by the hour count.

### Volume evidence is not transfer evidence

[[Rhoda AI - Scaling Web-Video Pre-training for Real Robots]] is the vault's only controlled
transfer study. More web-video pre-training improved completion on one industrial task, and
video-prediction quality ranked seven checkpoints in the same order as physical success. Potter's
figures are of a different kind: collection volumes, collection rates, and prices. Volume shows that
data exists; Rhoda-style evaluation shows that a kind of data moves physical completion for one
embodiment and task. The vault has no evidence linking a number of hours from any route to a
capability level. Collection rate is also not training-set size: Figure's statement that Index
gathers "30 minutes of video data every second, or 43,000 hours a day" describes intake.

### Two different flywheels

Robotics uses "data flywheel" for a deployment loop: robots doing real work generate data that
trains better robots, which are then deployed more widely. Physical Intelligence's
chocolate-factory experiment is Potter's example of a proto-flywheel. [[Synthetic Data Flywheel]]
uses the word for something else — model-generated artifacts replacing human-generated ones in the
training stack. Robotics has that loop too, in synthetic augmentation of teleoperation data through
NVIDIA's Isaac GR00T tooling. The two fail differently. The deployment loop is starved by few
deployed robots and repetitive tasks; synthetic augmentation is capped by the fidelity of the
generator and simulator.

### The cost estimate is conditional

Potter's naive figure of **$10 billion to $100 billion** prices roughly **1 billion hours** of
real-world data at reported rates: **$60 to $100 per hour** from Eidon AI and **$60 to $150 per
hour** for UMI data from Pantheon, which also claims a **$10 per hour** pipeline; Shift says
recorders can earn up to **$20 per hour**. The estimate assumes the roughly 1,000x gap implied by
the reading-time metric must be closed with real-world data. Potter's own open questions — narrow
tasks needing less data, general frontier models needing little robot data, more sample-efficient
architectures, or manipulation being fundamentally harder than text — would each move the number
by large factors in either direction.

Autonomous driving offers one scale precedent: by 2019 Waymo had driven **10 million** real miles
and **10 billion** simulated ones, as cited by Potter. [[Autonomous Driving Systems]], building on
[[ByteByteGo - Waymo vs Tesla - Two Ways to Build Self-Driving Cars]]'s point that reported fleet miles
differ in autonomy level and operating domain, already warns that simulated scenarios and real
driverless miles are not interchangeable denominators. The same
caution applies to simulated robot hours.

## Open questions

- Which route's hours transfer best to which task families? The vault has one controlled study and
  no cross-route comparison at matched cost.
- Does pooling across embodiments help a target robot, as it would if hours were fungible, or does
  it behave like Neuralink's pooled decoders?
- Is the "data gap" a shortage of hours or of diversity? Repetitive deployment data and correlated
  video frames suggest raw hours overstate usable signal.
- Will general multimodal models reduce robot-specific data needs, and what experiment would show
  it?
- How far can improving simulators push into contact-rich manipulation before the sim-to-real gap
  stops narrowing?

## Related pages

- [[Brian Potter - How to Train Your Robot]]
- [[Rhoda AI - Scaling Web-Video Pre-training for Real Robots]]
- [[Video Pre-training for Robot Policies]]
- [[World Models]]
- [[Synthetic Data Flywheel]]
- [[Autonomous Driving Systems]]
- [[Reinforcement Learning]]
- [[Video Transformers]]
- [[Fei-Fei Li - A Functional Taxonomy of World Models]]
- [[Neuralink - Pretraining on 50,000 Hours of Unlabeled Brain Data]]
- [[Jacky Kwok et al - Contrastive Language Models]]
- [[ByteByteGo - Waymo vs Tesla - Two Ways to Build Self-Driving Cars]]
- [[Embedding Model Selection]]
- [[Epoch AI]]
- [[Google DeepMind]]
- [[NVIDIA]]
- [[Neuralink]]
