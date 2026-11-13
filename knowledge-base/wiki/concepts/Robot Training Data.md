---
type: concept
created: 2026-10-19
updated: 2026-11-13
tags: [concept, robotics, training-data, simulation, scaling]
source_ids:
  - src-2026-10-15-potter-how-to-train-your-robot
  - src-2026-09-14-rhoda-web-video-pretraining-robots
  - src-2026-06-05-fei-fei-li-taxonomy-world-models
  - src-2026-10-01-neuralink-unlabeled-brain-pretraining
  - src-2026-09-23-kwok-contrastive-language-models
  - src-2026-08-18-bytebytego-waymo-vs-tesla
  - src-2026-11-03-nvidia-cosmos-interactive-world-models
  - src-2026-11-11-nvidia-gr00t-2
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

[[Rhoda AI - Scaling Web-Video Pre-training for Real Robots]] was the vault's first controlled
transfer study, and until the GR00T 2 ingest its only one (see below). More web-video pre-training
improved completion on one industrial task, and video-prediction quality ranked seven checkpoints in
the same order as physical success. Potter's figures are of a different kind: collection volumes,
collection rates, and prices. Volume shows that data exists; Rhoda-style evaluation shows that a
kind of data moves physical completion for one embodiment and task. Before GR00T 2, the vault had no
evidence linking a number of hours from any route to a capability level. Collection rate is also
not training-set size: Figure's statement that Index gathers "30 minutes of video data every
second, or 43,000 hours a day" describes intake.

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

### Generative augmentation multiplies pixels, not actions

[[Elizabeth Goodman - Build World Models for Interactive Simulation with NVIDIA Cosmos]] makes the
synthetic-augmentation route concrete. **Cosmos3-Nano-Sim-Transfer** turns depth (or
segmentation, edges, blurred video) plus a prompt into RGB with varied lighting, textures and
backgrounds "while preserving geometry and motion". For a robot demonstration it changes the
third-person view while keeping the **actions, states and wrist-camera recordings**. One
teleoperated episode can therefore yield several visual variants with identical action labels.
Two other checkpoints are action-conditioned simulators. **Cosmos3-Nano-Sim-Bimanual** predicts the
next observation from the scene and robot actions for YAM and AgiBot two-arm embodiments.
**Cosmos3-H-Embodied-Nano**, post-trained on Open-H-Embodiment, generates surgical video from
robot actions, so policies can be evaluated offline "without building a physics model of the
surgical scene".

In the vault's reading, this answers half of the open question below on whether the gap is hours
or diversity. Augmentation adds visual diversity around a fixed set of behaviors; it does not add
new contact events, recoveries or task variations. The two flywheels above stay distinct: these
tools sit in the synthetic one and are capped by generator fidelity. The vendor post reports no
policy-transfer or fidelity results, so the number of useful hours a generated variant is worth
remains unmeasured.

### One mixture of routes, with the human-video share scaled

[[NVIDIA - GR00T 2 - Scaling Robot Foundation Models for Generalization, Dexterity, and Adaptation]]
combines several routes from the table in one pretraining mixture. It holds about **402,730 hours**
of human egocentric video, **10,184 hours** of handheld UMI-gripper demonstrations across **2,897**
tasks, and **23,500 hours** of teleoperation from YAM and Franka arms, Sharpa and Wuji hands, and
the Unitree G1 humanoid. By hours, the mixture is mostly human video. NVIDIA pretrained four models
on none, **1%**, **10%**, and **100%** of the human video, then evaluated each on **72** tasks on
Dexter, a two-handed robot. Task progress rose at every step:
from **64% to 77%** in the model's video rollouts and from **50% to 70%** on the real robot.

That is the vault's second controlled transfer study, and it differs from Rhoda's in two ways. The
scaled ingredient is human egocentric video, not generic web video. And the study varies one route's
share within a mixture rather than the amount of pre-training. Like Rhoda's, it is first-party and
measured on one target robot. GR00T 2 also predicts video as well as actions. On the vault's reading,
the result does not show that human video would help a policy without that video head.

The same page tests the embodiment gap that the table assigns to cheap routes:

- **Human and handheld demonstrations.** Tasks demonstrated only by people wearing head and wrist
  cameras, or only with a handheld UMI gripper, ran on robots that had only task-agnostic
  teleoperation data for their own bodies. On a conveyor-sorting task taught only with UMI, GR00T 2
  sorted **86%** of **50** items, against **28%** for GR00T 1.7 and **0%** for π0.5. For four tasks
  taught only by human demonstration, three of them chemistry-lab procedures, NVIDIA says GR00T 2
  "succeeds on all four tasks" over **20** trials each, without per-task rates in prose.
- **Little target data.** Five demonstrations per task, under **3 minutes** of robot data, lifted
  success on **50** tasks to **95%**.
- **Simulation as data and as a scorer.** Adding simulated episodes raised GR00T 2 Turbo's
  out-of-distribution success on the G1 humanoid from **6.7%** to **63.3%**. A digital-twin
  evaluator's success rates for **14** policies tracked their real-world rates (Pearson **0.92**,
  Spearman **0.89**); see [[World Models]]. That speaks to the definition's "reliable way to score
  an attempt".

On this evidence, the embodiment gap of cheap routes can be bridged for these tasks with
task-agnostic data from the target body rather than task demonstrations. The page compares GR00T 2
with and without cross-embodiment pretraining only in a chart, which is not used here, so the
pooling question below stays open.

## Open questions

- Which route's hours transfer best to which task families? The vault now has two controlled
  studies, both first-party: Rhoda's on web video and GR00T 2's on the human-video share. It still
  has no cross-route comparison at matched cost.
- Does pooling across embodiments help a target robot, as it would if hours were fungible, or does
  it behave like Neuralink's pooled decoders?
- Is the "data gap" a shortage of hours or of diversity? Repetitive deployment data and correlated
  video frames suggest raw hours overstate usable signal.
- Will general multimodal models reduce robot-specific data needs, and what experiment would show
  it?
- How far can improving simulators push into contact-rich manipulation before the sim-to-real gap
  stops narrowing?
- Do visually augmented demonstrations, with actions held fixed, improve policy robustness as much
  as new real demonstrations of the same count?
- Would GR00T 2's human-video scaling hold for a policy that does not also predict video?

## Related pages

- [[Brian Potter - How to Train Your Robot]]
- [[Elizabeth Goodman - Build World Models for Interactive Simulation with NVIDIA Cosmos]]
- [[Rhoda AI - Scaling Web-Video Pre-training for Real Robots]]
- [[NVIDIA - GR00T 2 - Scaling Robot Foundation Models for Generalization, Dexterity, and Adaptation]]
- [[Video Pre-training for Robot Policies]]
- [[World Models]]
- [[Synthetic Data Flywheel]]
- [[AI Drug Discovery]]
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
