---
type: source-summary
created: 2026-10-19
updated: 2026-10-19
source_id: src-2026-10-15-potter-how-to-train-your-robot
source_title: "How to Train Your Robot"
source_author: Brian Potter
source_url: https://www.construction-physics.com/p/how-to-train-your-robot
tags: [source/summary, robotics, training-data, simulation, scaling]
source_ids: [src-2026-10-15-potter-how-to-train-your-robot]
status: active
---

# Brian Potter - How to Train Your Robot

## Summary

A Construction Physics essay asking where robot training data will come from. Language models
could be trained on a large existing stock of text; robotics has no equivalent stock of good,
public data. Potter surveys the main ways robot data is collected, compares reported robot dataset
sizes with LLM training sets, and estimates what closing the gap might cost.

It is a secondary synthesis. Most figures are company announcements, social-media posts, or other
writers' estimates, and the author flags his own uncertainty repeatedly ("as I understand it",
"seems to"). Two images are credited "Via Opus 5.5"; they are illustrations, not data.

## Key claims

### How robot data is produced

| Route | Advantage, as described | Limit, as described |
| --- | --- | --- |
| Teleoperation (behavioral cloning, a form of imitation learning) | Data closely matches the actual robot's movement capabilities | Needs a robot and an operator, which is hard to scale; no tactile feedback limits dexterous manipulation data; "as I understand it, only a fraction" of collected data ends up useful |
| Autonomous real-world RL | The robot attempts tasks and a system scores them, as in Google's arm farm around 2016 | Does not seem to be widely used today |
| Deployment data flywheel | Real-world deployed robots will probably eventually be the largest source | Very few AI-controlled robots do real work; real-world data is extremely repetitive. Physical Intelligence is experimenting at a chocolate factory |
| Simulation, with RL or teacher/student training | Much cheaper and faster; thousands of robots in parallel | Data quality is a function of simulation accuracy: fairly accurate for locomotion, much harder for soft or deformable objects (the sim-to-real gap) |
| Domain randomization | Varies unknown parameters such as friction to cover the real world | OpenAI's Rubik's Cube hand used about 13,000 simulated years and reached only 20% success on maximally difficult starting arrangements; fairly standard for locomotion, not widely used for manipulation |
| Synthetic data from real demonstrations | Turns teleoperation data into many similar examples (NVIDIA's Isaac GR00T page); also widely used for autonomous vehicles | No performance evidence in the capture |
| Human task data: egocentric video, body sensors, tactile gloves | Much cheaper than teleoperation, easier to vary, and real physics | Human data does not map perfectly onto a robot, one reason humanoid form factors are popular |
| Universal Manipulation Interface (UMI) grippers | Camera-equipped handheld manipulators minimize the human-robot difference | The mapping is still imperfect, though the discrepancy is small; Generalist AI and Sunday Robotics seem to rely primarily on it |
| Generic web video and vision-language backbones | Abundant; NVIDIA Cosmos is a video-trained foundation model usable as a policy backbone, and vision-language-action models build on vision-language models | Not task-completion data |

- Simulation-scale examples: Figure AI taught walking through RL on thousands of simulated robots;
  by 2019 Waymo had driven 10 million miles in the real world and 10 billion in simulation.
- Named human-data efforts: Figure's Index program and Shift (head- or hat-mounted cameras),
  the now-defunct Eidon AI (arm sensors for joint positions), and Neocambrian AI's "Mitts" tactile
  gloves, described by the company as "state of the art."
- Routes are combined in practice. Agility Robotics' Digit walks with a small,
  1-million-parameter network trained by RL in simulation, while manipulation "seems to have been"
  trained by behavioral cloning. Dyna Robotics "seems to have used" simulated RL plus human video.

### Scale comparisons

- Language side, as cited: Epoch AI found that language-model training datasets have doubled
  about every six months since the early 2010s; GPT-3 was trained on about 300 billion tokens;
  Epoch's 2024 estimate of the stock of quality, accessible text is around 300 trillion tokens;
  the biggest current models train on tens of trillions of tokens.
- Robot side, as reported: Open X-Embodiment (Google DeepMind, 2023, stitched from dozens of
  existing datasets) has over 1 million trajectories spanning more than 160,000 tasks, about 4,000
  hours; Physical Intelligence's Pi 0 (October 2024) used 10,000 hours; Generalist AI's GEN 1 used
  around 500,000 hours of UMI data; Figure says Index gathers "30 minutes of video data every
  second, or 43,000 hours a day"; Dyna Robotics and Nature Will claim over 1 million hours of
  egocentric video; one estimate puts the collection industry near 500,000 hours a month.
- Reading-time conversion, used by Kevin Black and Ken Goldberg and called "somewhat dubious" by
  Potter: GPT-2 equals about 475,000 hours, GPT-3 26 million, and GPT-4 685 million, so even older
  LLMs saw something like 1,000 times the data of current robot models. Goldberg calls this the
  "100,000-year data gap."
- Token conversion, from Chris Paxton: at 10 frames per second with one useful token per frame, an
  hour holds 36,000 tokens; dividing by 10 for footage that is not useful gives about 3,600. Dyna's
  1 million hours would then be about 3.6 billion tokens, on the order of 5,000 times smaller than
  recent AI training sets.
- Both comparisons are weakened by quality differences (teleoperation or UMI data is probably
  better than egocentric video, and varied data beats repetitive data) and by frame-to-frame
  correlation in video. Paxton: "robot data is far less iid than web data."

### Cost of closing the gap

- Reported prices: Eidon AI $60 to $100 per hour of robot data; Pantheon $60 to $150 per hour of
  UMI data, plus a pipeline its engineers built at $10 per hour; Shift says recorders can earn up
  to $20 per hour.
- Naive estimate: about 1,000 times current data, on the order of 1 billion hours, would cost on the
  order of $10 billion to $100 billion.

### How much data is needed is open

- Narrow, task-specific robots may need substantially less data. Frontier general models might
  become extremely capable controllers after comparatively little robot data. More sample-efficient
  architectures may appear.
- Alternatively, physical manipulation may be fundamentally harder than text: a single tiny
  positioning error can separate success from failure. Goldberg argues robot movement is a much
  higher-dimensional problem; Potter is not sure he buys the version of the argument presented.

## Why it matters

The vault's robotics evidence has so far rested on one controlled vendor study of web-video
pre-training, [[Rhoda AI - Scaling Web-Video Pre-training for Real Robots]]. Potter supplies the
surrounding map: every route trades embodiment fidelity, physical accuracy, diversity, and cost
against one another, and none wins on all four. The essay seeds [[Robot Training Data]] and gives
the "simulation is the linchpin" argument on [[World Models]] a practical cost. Simulation
produces volume where its physics can be trusted, and much less where manipulation needs it.

## Tensions / open questions

- Hours are not a common currency. The reading-time and token conversions differ in method and
  agree only in order of magnitude; neither adjusts for embodiment mismatch or data quality.
- Most robot dataset figures are company claims or social-media posts, not audited dataset
  descriptions. Figure's collection rate is not a training-set size.
- The $10-$100 billion estimate assumes the 1,000x gap must be closed with real-world data at
  current prices. The essay itself lists three reasons the requirement could be far smaller.
- The deployment flywheel and simulation fail differently: deployed robots produce repetitive
  data, while simulators produce inaccurate contact physics. Neither failure is quantified.
- The 20% Rubik's Cube figure applies to maximally difficult starting arrangements, not all solves.

## Affected pages

- [[Robot Training Data]]
- [[Video Pre-training for Robot Policies]]
- [[World Models]]
- [[Synthetic Data Flywheel]]
- [[Autonomous Driving Systems]]
- [[Epoch AI]]
- [[Google DeepMind]]
- [[NVIDIA]]

## Raw capture

- [[How to Train Your Robot]]

## Citations

- Canonical article: <https://www.construction-physics.com/p/how-to-train-your-robot>
- Published October 15, 2026; captured October 19, 2026. The clipped URL's newsletter tracking
  parameter was removed above.
- Figures are recorded as the essay cites them; the underlying Epoch, company, and social-media
  sources were not separately checked.

## Related pages

- [[Robot Training Data]]
- [[Video Pre-training for Robot Policies]]
- [[World Models]]
- [[Synthetic Data Flywheel]]
- [[Autonomous Driving Systems]]
- [[Reinforcement Learning]]
- [[Rhoda AI - Scaling Web-Video Pre-training for Real Robots]]
- [[Vision-Language Grounding]]
- [[Epoch AI]]
- [[Google DeepMind]]
- [[NVIDIA]]
