---
title: "Sparks of Weight-Space Programming: LLMs can natively read & write neural network weights"
source: "https://rikiyat.github.io/blog/weight-space-programming/"
author:
  - "[[Rikiya Takehi]]"
  - "[[Jayden Teoh]]"
  - "[[Alex Zhang]]"
  - "[[Omar Khattab]]"
published: 2026-11-02
created: 2026-11-03
description: "We find that frontier LLMs are surprisingly good at natively reading and writing neural network weights, well past what we’d expect from humans or conventional algorithms."
tags:
  - "clippings"
---
## LLMs can natively read & write neural network weights

**TL;DR**

We find that frontier LLMs are surprisingly good at **natively reading and writing neural network weights**, well past what we’d expect from humans or conventional algorithms. This might be a big deal for both optimization and interpretability.

Just by looking at the raw weights, GPT-6 Astra **can tell what a network was trained to do**. And without any environment feedback, it **has no trouble writing, from scratch, small game-playing networks** that outplay networks trained with PPO for 100 million steps.

Likewise, asked to make Qwen3.5-0.8B better at math without gradients, Astra **identifies an issue in its weights** causing reasoning loops that Qwen’s own [model card](https://huggingface.co/Qwen/Qwen3.5-0.8B/blob/main/README.md#L856) warns about, and **fixes this by natively editing 0.016% of the weights**. With the same sampling settings, this weight correction raises MATH-500 from 7.9% to 48.1% and generalizes out of the box to instruction following, raising IFEval by 3x.

All of this is possible without allowing Astra to write training loops. It uses its reasoning to figure out what each part of a neural network computes, or should compute, and changes the weights accordingly. We call this **Weight-Space Programming**.

Throughout the history of deep learning, we encoded our simplistic inductive biases into tiny symbolic optimizers like Adam or Muon. This is changing: **our neural network weights will soon be *natively* optimized by LLMs that deliberately reason about their weights**.

![The network playing Breakout.](https://rikiyat.github.io/blog/weight-space-programming/assets/which_game/breakout.gif)

The network playing Breakout.

If you were asked to handcraft a neural network that plays Go, what would you do? If you were handed raw neural network weights and asked to predict their behavior, where would you even start? For almost any human, this is practically impossible.

Today, weights are written by [optimization](https://karpathy.medium.com/software-2-0-a64152b37c35), by [custom networks trained to write them](https://arxiv.org/abs/2102.11174), or by [compilers from formal programs](https://arxiv.org/abs/2301.05062). In this post, we find that the current generation of frontier LLMs, used natively in natural language, are starting to become eerily good at understanding and crafting neural network weights around natural-language goals.

## Weight-Space Programming

For a few years now, we’ve all been **using LLMs to optimize text artifacts** like prompts and the programs built around them

- **Large Language Models as Optimizers**   [\[PDF\]](http://arxiv.org/pdf/2309.03409.pdf)  
	C. Yang, X. Wang, Y. Lu, H. Liu, Q.V. Le, D. Zhou, X. Chen.  
	International Conference on Learning Representations (ICLR). 2024.
- **DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines**   [\[PDF\]](http://arxiv.org/pdf/2310.03714.pdf)  
	O. Khattab, A. Singhvi, P. Maheshwari, Z. Zhang, K. Santhanam, S. Vardhamanan, S. Haq, A. Sharma, T.T. Joshi, H. Moazam, H. Miller, M. Zaharia, C. Potts.  
	International Conference on Learning Representations (ICLR). 2024.
- **Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs**   [\[PDF\]](http://arxiv.org/pdf/2406.11695.pdf)  
	K. Opsahl-Ong, M.J. Ryan, J. Purtell, D. Broman, C. Potts, M. Zaharia, O. Khattab.  
	Conference on Empirical Methods in Natural Language Processing (EMNLP). 2024.
- **GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning**   [\[PDF\]](http://arxiv.org/pdf/2507.19457.pdf)  
	L.A. Agrawal, S. Tan, D. Soylu, N. Ziems, R. Khare, K. Opsahl-Ong, A. Singhvi, H. Shandilya, M.J. Ryan, M. Jiang, C. Potts, K. Sen, A.G. Dimakis, I. Stoica, D. Klein, M. Zaharia, O. Khattab.  
	International Conference on Learning Representations (ICLR). 2026.

\[1, 2, 3, 4\]

. More recently, we’ve started using them to optimize whole harnesses

- **Meta-Harness: End-to-End Optimization of Model Harnesses**   [\[PDF\]](http://arxiv.org/pdf/2603.28052.pdf)  
	Y. Lee, R. Nair, Q. Zhang, K. Lee, O. Khattab, C. Finn.  
	Conference on Language Modeling (COLM). 2026.

\[5\]

and the training code and hyperparameters that train ML models

- **autoresearch**   [\[link\]](https://github.com/karpathy/autoresearch)  
	A. Karpathy.  
	GitHub repository. 2026.
- **Reactive Optimizers**   [\[link\]](https://xingjianbai.com/reactive-optimizers/)  
	X. Bai, J. Liang, J. Teoh, V. Sitzmann.  
	Blog post. 2026.

\[6, 7\]

.

We often justified these methods by reference to the fact that *we don’t know other principled ways to hill-climb on text artifacts, unlike for updating the weights of differentiable neural networks*. After all, humans can “optimize” code by hand, for example, so it made sense to ask LLMs to do it, but they can’t “optimize” neural weights by hand, so those remained largely in the realm of symbolic algorithms.

In this post, we share very early results that allow us to argue that **the paradigm of reasoning-driven optimization is now coming even for differentiable neural networks**.

In **Weight-Space Programming**, a general-purpose **LLM reads and writes a network’s weights directly** (i.e., not through an optimizer, and in particular not with gradient descent) around some natural language spec, sometimes even with no environment feedback at all.

In natural language, it’s becoming possible to **“just ask” an LLM to natively find a hidden trait or failure inside the weights of a neural network, to fix that failure, or to write a new network from scratch**. We report early, exciting results on each of these below, first on small networks and then even on real language models:

1. **LLMs can read neural network weights:** In Experiments 1 to 3, we ask Astra questions like what game a network was trained to play, what shape is drawn by a diffusion model, and which language a small language model was trained on. In Experiment 7, we ask which of two language models was trained to be sycophantic.
2. **LLMs can fix neural network weights:** In Experiment 4, we ask Astra to fix a network that’s failing at some physical control task. In Experiment 8, we ask it to make Qwen3.5-0.8B better at math, and its fix improves instruction following too.
3. **LLMs can write neural network weights from scratch:** In Experiment 5, we ask Astra for networks that play three MinAtar games, and in Experiment 6, for a network that plays Go.

## Can LLMs understand model behaviors from weights?

We start with a small-scale experiment to see if LLMs can understand the continuous weight space, which is essentially just a list of numbers.

In our first experiments, we train some neural network with some algorithm. It would be extremely exciting if the LLM is able to tell its behavior just from the weights.

Experiment 1

### Can Astra tell which game the network was trained on just from the weights?

We trained neural network policies with PPO to play four computer games. All four networks take the same input channels, choose from the same actions, and have exactly the same network dimensions, so that it is not able to tell unless the weights are read.

For each of these networks, we pass its raw weights into Astra as a prompt, and ask: Which game was this neural network trained on? **Without revealing the options of the games we consider, Astra was still able to name the right game for all four networks.** This is exciting particularly because there are so many games out there that Astra could choose from.

![The Breakout networks playing.](https://rikiyat.github.io/blog/weight-space-programming/assets/which_game/breakout.gif)

The Breakout networks playing.

It seems that Astra was able to work out what game each network was built to play, just from features of its weights. For example, where each input channel’s first-layer weights concentrate (e.g., for Breakout, the agent’s weights lie along the bottom row, a paddle), and which actions the output layer tells apart.

Experiment 2

### Can Astra tell what the diffusion model will generate?

Next, we wanted to see if this generalizes to other tasks and models.

We train diffusion models (DDPM) to generate circle, triangle, and square images independently. We then ask Astra if it could tell what the DDPMs are trained to generate, just from the weights alone. We do not allow tool use or forward passes.

Setup

- **Models:** three diffusion models (DDPM) of 12×12 grayscale images, one each for filled circles, squares and triangles
- **Network:** MLP 160 → 64 → 64 → 144, ReLU (23,824 weights)
- **Input:** a noisy image (144 pixels) and the diffusion step (16 numbers)
- **Output:** the clean image (144 pixels)
- **Training:** Adam, 40,000 steps, batch 512
- **Astra gets:** all the weights as text, with no shape named, and is told not to compute any forward pass

CirclesSquaresTriangles

The model generates

the model’s 23,824 weights as text

W3 row 29 0.004 0.003 0.003 -0.001 0.007 0.062 0.114 0.082 0.024 0.005 0.004 0.003 …

What images does this neural network generate?

No tools or forward passes are allowed.

Answer Images: ==a single white circle outline on black, with a black interior== 84% confident · ✓ Correct · 506 tokens

Reasoning

1. The output weights contain **curved rim segments**
2. This traces an upper-left bend
3. Other units describe complementary portions of a rounded boundary
4. These are localized bands with weaker or negative weights beside them, rather than uniformly positive filled regions
5. ==The complementary top, bottom, and curved side bands strongly suggest **circular or slightly oval outlines**==

Astra’s drawing

**Astra was able to tell what each model generates, from the weights alone.** It finds the shape in the output layer, where each hidden unit’s weights draw one piece of the shape’s edge, and it draws just those edges. Interestingly, it draws every shape as an outline, ignoring that the actual models generate filled shapes. This mistake kind of shows it does not rely on calculating the forward pass, but rather it actually reads the structure/geometry of the weights.

Experiment 3

### Can Astra tell what a language model learned, from the middle of the network alone?

Now, in the first two experiments above, Astra was not really looking at the full network and could get away with only reading the first or the last layers. This is not a scalable strategy for larger (particularly language) models and problems we really care about, as how they process and think through their input often happens in the intermediate layers. So next, we take the first and last layers away and leave Astra with only the middle layers.

We train three small language models (7.2M parameters) to predict the next character, one each on Python code

[^1]

, Japanese in alphabet (romaji)

- **aozorabunko-clean: the Aozora Bunko collection of Japanese literature, cleaned and deduplicated**   [\[link\]](https://huggingface.co/datasets/globis-university/aozorabunko-clean)  
	.  
	Hugging Face dataset, GLOBIS University. 2023.

\[8\]

, and English

- **Wikipedia, English, dump of November 1, 2023**   [\[link\]](https://huggingface.co/datasets/wikimedia/wikipedia)  
	.  
	Hugging Face dataset wikimedia/wikipedia, Wikimedia Foundation. 2023.

\[9\]

. We then remove the input and output layers and give Astra only the four transformer blocks in between. Without these two layers, nothing in the weights says which character is which, and the model cannot be run on any text. Astra may analyze the weights with Python, but it may not run the network or any of its layers on any input.

We ask: *which language was this network trained on, and what each of its 24 attention heads does*. **Astra names the right language for all three networks, in both of its attempts. It also finds every copying head (induction head), the heads that let a model repeat text it has seen earlier, and names no other head as one.**

| Trained on | Astra’s answer (& confidence), two attempts | Copying heads Astra names (layer.head) | Copying heads, ground truth |
| --- | --- | --- | --- |
| Python | Python (0.56), Python (0.52) | 2.1, 3.1, 3.5 | 2.1, 3.1, 3.5 |
| Romaji | romaji (0.55), romaji (0.62) | 3.3 | 3.3 |
| English | English (0.58), English (0.48) | 3.1 | 3.1 |

Where the copying heads are

… tot **al** … tot **al** A copying head finds the same letters earlier in the text and copies what came after them.

copying headother headRows are layers 0 to 3, columns are heads 0 to 5Astra: from the weights. Measured: by running the model

Python

0123450123

Astra

012345

Measured

Romaji

0123450123

Astra

012345

Measured

English

0123450123

Astra

012345

Measured

**Figure 1:** The copying heads Astra read from the weights match the measured ones in all three models.

Setup

- **Models:** character-level transformers, 4 layers × 6 heads, width 384 (7.16 million weights), 28 characters: a–z, space and newline
- **Training:** 1 billion characters each, of Python code, Japanese literature in romaji (Aozora Bunko), or English Wikipedia
- **Astra gets:** the weights of the four transformer blocks only, with no input layer, no output layer and no labels on the 384 dimensions, and Python to analyze them, up to 100 runs
- **Not allowed:** running the network or any of its layers on any input, real, random or made up, and search. We checked every run
- **Asked:** which of the three texts the network was trained on, and what each head does
- **Truth:** each head measured by running the network on a random string repeated twice. Copying heads score 0.22 to 0.55, every other head at most 0.02. Astra never sees this

Show the prompt and Astra’s answersHide the prompt and Astra’s answers

PythonRomajiEnglish

Truth Trained on Python code. Its copying heads, measured by running it: 2.1, 3.1 and 3.5.

the weights of the four transformer blocks, as files

What was this network trained on: Python code, romaji or English? And what does each attention head do?

Running the network or any of its layers on any input is not allowed.

Answer Trained on: ==Python== 56% confident · ✓ Correct · 11 runs

Reasoning

1. L2H1: **copy** — positive, key-specific composition with the likely previous-character head L0H5.
2. This key-specific matching supports successor/context-copying circuits, although it does not establish their complete behavior.
3. I weakly favor **Python**: repeated identifiers and recurring code fragments offer a particularly useful role for this hierarchy of local features and context matching.
4. The corpus judgment is considerably weaker than the order judgment, and no character identities or keywords were recovered.

The reasoning went like this. To tell Python apart, Astra looked for copying heads, which let a model repeat earlier text, such as completing tot to tot **al** when tot **al** came before. Without running anything, it found a first-layer head that looks one character back and then, by multiplying weight matrices, the later heads that search using what that head brings along ([Figure 1](#figure-1)). We find that this is actually a method presented by Elhage et al.

- **A Mathematical Framework for Transformer Circuits**   [\[HTML\]](https://transformer-circuits.pub/2021/framework/index.html)  
	N. Elhage, N. Nanda, C. Olsson, T. Henighan, N. Joseph, B. Mann, A. Askell, Y. Bai, A. Chen, T. Conerly, N. DasSarma, D. Drain, D. Ganguli, Z. Hatfield-Dodds, D. Hernandez, A. Jones, J. Kernion, L. Lovitt, K. Ndousse, D. Amodei, T. Brown, J. Clark, J. Kaplan, S. McCandlish, C. Olah.  
	Transformer Circuits Thread. 2021.

\[10\]

, which we never mentioned to Astra. Code repeats names far more than prose, so many copying heads pointed to Python.

Romaji stood out instead because the last of the four blocks it was given (not the output layer, which was removed) writes in fewer distinct directions, as if the model had fewer letters to tell apart. Indeed, romaji never uses some letters like q, l, v and x.

## Can an LLM write neural network weights?

So far, Astra has only read weights. Now, we ask if Astra knows how to write the weights.

Experiment 4

### Can Astra fix a failing network by editing its weights?

We train a PPO network to operate a car such that it can scale a ramp in a Kinetix environment

- **Kinetix: Investigating the Training of General Agents through Open-Ended Physics-Based Control Tasks**   [\[PDF\]](http://arxiv.org/pdf/2410.23208.pdf)  
	M. Matthews, M. Beukman, C. Lu, J. Foerster.  
	International Conference on Learning Representations (ICLR). 2025.

\[11\]

. To do so, it needs to reverse the car for some distance, such that it has enough runway to accelerate long enough to overcome the ramp. However, the PPO network converges to a local-minimum policy where it drives straight at the ramp and gets stuck.

We give GPT-6 Astra the weights, a description of the scene and one recorded episode, and ask it to explain why the network fails, then fix it by writing new weights. **In a single try with no tools, Astra’s edit makes the car succeed in all 1,024 episodes, changing 3.5% of the weights.**

Setup

- **Task:** the car-on-ramp level of Kinetix
	- **Kinetix: Investigating the Training of General Agents through Open-Ended Physics-Based Control Tasks**   [\[PDF\]](http://arxiv.org/pdf/2410.23208.pdf)  
		M. Matthews, M. Beukman, C. Lu, J. Foerster.  
		International Conference on Learning Representations (ICLR). 2025.
	\[11\]
	: the car has to back up, then jump over a red strip to reach the blue box
- **Network:** the official Kinetix actor: 679 → 128 (ReLU) → five layers of 128 (tanh) → 16 (171,664 weights)
- **Input:** 679 numbers describing the scene: position, velocity and shape of each body, and the joints
- **Output:** 16 logits for the motor and thruster actions
- **Training:** the official PPO, 1 billion steps. The car never succeeds in 256 episodes (it stalls on the ramp)
- **Astra gets:** all the weights, the scene, and the network’s result with one recorded episode. It is asked to explain the failure and fix only its cause, in one reply

After Astra’s edit

PPO (faded): stuck on the ramp

It changed only 6,073 of its 171,664 weights (3.5%).

the policy’s 171,664 weights as text

embed.W row 54 9 -2 -7 -4 7 18 -1 0 -5 -3 -4 8 …

Change the network's weights by hand so that the car succeeds as often as possible.

No tools are allowed.

Answer ✓ 100% success · 988 tokens

**Astra’s edits (applied to the network as written)** · 57 lines
```
embed.W[:, 6:9] = 0
embed.b[6:9] = [0, 11, 0]
embed.W[52, 6] = 1
embed.W[54, 7] = 1
embed.W[234, 8] = 1

actor0.W[6:9, :] = 0
actor0.W[:, 122:128] = 0
actor0.b[122:128] = [-200, -248, -304, -876, -760, -76]
actor0.W[6, 122] = 80
actor0.W[6, 123] = 80
actor0.W[6, 124] = 80
actor0.W[7, 125] = 80
actor0.W[7, 126] = 80
actor0.W[8, 127] = 80

actor1.W[122:128, :] = 0
actor1.W[:, 124:128] = 0
actor1.b[124:128] = [0, -10, -10, 30]
actor1.W[127, 124] = 10
actor1.W[124, 125] = -10
actor1.W[125, 125] = 10
actor1.W[122, 126] = -10
actor1.W[126, 126] = 10
actor1.W[122, 127] = -10
actor1.W[123, 127] = 10
actor1.W[125, 127] = 10
actor1.W[126, 127] = -10

actor2.W[124:128, :] = 0
actor2.W[:, 126:128] = 0
actor2.b[126:128] = [-10, -30]
actor2.W[124, 126] = 20
actor2.W[125, 126] = 10
actor2.W[126, 126] = 10
actor2.W[124, 127] = 10
actor2.W[125, 127] = -10
actor2.W[126, 127] = -10
actor2.W[127, 127] = 10

actor3.W[126:128, :] = 0
actor3.W[:, 126:128] = 0
actor3.b[126:128] = 0
actor3.W[126, 126] = 10
actor3.W[127, 127] = 10

actor4.W[126:128, :] = 0
actor4.W[:, 126:128] = 0
actor4.b[126:128] = 0
actor4.W[126, 126] = 10
actor4.W[127, 127] = 10

actor_head.W[126, 0:3] = [-100, -100, 200]
actor_head.W[127, 0:3] = [-100, 200, -100]
actor_head.b[0] -= 200
actor_head.b[1] += 100
actor_head.b[2] += 100
```

Reasoning

1. ==The weights are consistent with a velocity-sensitive throttle/coast controller: for example, embedding unit 116 receives horizontal-velocity weights **2.25, 2.37, and 1.73** from the body and wheels.==
2. The trace shows the failure: the car approaches the ramp, loses its momentum, then alternates throttle and coasting without advancing.
3. ==Reverse is effectively never sampled.==
4. It collects distance-shaping reward but never makes the launch needed to clear red.
5. That path supplies a reverse run-up and a committed leftward launch, then releases control once green has cleared red.
6. The override backs right from rest, switches to leftward drive around body x = 3.8, and maintains full drive during the fast return and ramp crossing.
7. Once green’s centre passes x = 0.95—its right edge is then left of red—the override switches off.

From the environment context and the PPO network’s trajectory, Astra identifies that the network has converged to a local minimum. Through minimal edits to the weights, Astra changes the policy to back up the car before driving forward at full speed. Astra’s reasoning shows how: it adds a small separate path through a few units per layer that reads the car’s position and speed, and once the green wheel is past the red strip, the path switches off and the trained network drives the rest.

Experiment 5

### Can the LLM write weights from scratch?

Now let's see if Astra can write a neural network from scratch in zero-shot.

We take three MinAtar games

- **MinAtar: An Atari-Inspired Testbed for Thorough and Reproducible Reinforcement Learning Experiments**   [\[PDF\]](http://arxiv.org/pdf/1903.03176.pdf)  
	K. Young, T. Tian.  
	arXiv preprint arXiv:1903.03176. 2019.

\[12\]

: Breakout, Seaquest and Asterix. For each of them, we provide Astra the game rules and source code, and the corresponding network. There is no access to data, loss, gradients, and tools. We also do not allow Astra to roll out the network in the environment. With just the network weights and environment description, Astra generates the new weights in text directly, after which we evaluate the new network.

**Astra’s generated networks beat PPO trained for 100 million steps in all three games. Against PPO trained for 500 million steps, they score 20 times as much in Breakout, come close in Asterix, and reach 60% of its score in Seaquest.**

| Game | PPO, 100M steps | PPO, 500M steps | Astra, one-shot |
| --- | --- | --- | --- |
| Breakout | 15.8 | 25.3 | **517.4** |
| Seaquest | 5.6 | **88.9** | 53.1 |
| Asterix | 25.8 | **55.2** | 53.2 |

Setup

- **Games:** Breakout, Seaquest and Asterix from MinAtar
	- **MinAtar: An Atari-Inspired Testbed for Thorough and Reproducible Reinforcement Learning Experiments**   [\[PDF\]](http://arxiv.org/pdf/1903.03176.pdf)  
		K. Young, T. Tian.  
		arXiv preprint arXiv:1903.03176. 2019.
	\[12\]
	, on a 10×10 grid
- **Network:** 600 → 32 → 32 → 6 (tanh), the same shape as the PPO networks, every weight starting at 0
- **Input and output:** the grid in 6 channels (player, danger, reward, projectile, trail, gauge), and 6 action logits
- **Astra gets:** the game’s rules and source code, the input and output layout, and how the network is scored
- **Training:** none: no data, no loss, no gradients, and no tools. Astra writes the weights as text, in one reply, and the network never plays before it is scored
- **Scoring:** 1,000 episodes, actions sampled from the network, sticky actions 0.1, at most 10,000 steps. PPO: the best of 3 to 10 seeds

BreakoutSeaquestAsterix

Score 0

the game’s rules and source code, and a network with every weight at 0

Write, from scratch, the weights of a policy network that plays Breakout as well as possible.

No training and no tools: Astra chooses every number itself, in one reply.

Answer Mean score 517.4 (PPO: 15.8 after 100M steps, 25.3 after 500M) · 3,739 tokens

**The weights Astra wrote** · 122 lines
```
# Units 0..3: descending-right, descending-left, ascending-right, ascending-left.
# Subtract paddle position from each target.
W1[540:600:6, 0] = [0, -0.02, -0.04, -0.06, -0.08, -0.10, -0.12, -0.14, -0.16, -0.18]
W1[540:600:6, 1] = [0, -0.02, -0.04, -0.06, -0.08, -0.10, -0.12, -0.14, -0.16, -0.18]
W1[540:600:6, 2] = [0, -0.02, -0.04, -0.06, -0.08, -0.10, -0.12, -0.14, -0.16, -0.18]
W1[540:600:6, 3] = [0, -0.02, -0.04, -0.06, -0.08, -0.10, -0.12, -0.14, -0.16, -0.18]

# Ball row 0.
W1[3:60:6, 0] = [0.16, 0.18, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08, 0.06, 0.04]
W1[3:60:6, 1] = [0.14, 0.12, 0.10, 0.08, 0.06, 0.04, 0.02, 0, 0, 0.02]
W1[3:60:6, 2] = [0.18, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08, 0.06, 0.04, 0.02]
W1[3:60:6, 3] = [0.16, 0.14, 0.12, 0.10, 0.08, 0.06, 0.04, 0.02, 0, 0]

# Ball row 1.
W1[63:120:6, 0] = [0.14, 0.16, 0.18, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08, 0.06]
W1[63:120:6, 1] = [0.12, 0.10, 0.08, 0.06, 0.04, 0.02, 0, 0, 0.02, 0.04]
W1[63:120:6, 2] = [0.18, 0.16, 0.14, 0.12, 0.10, 0.08, 0.06, 0.04, 0.02, 0]
W1[63:120:6, 3] = [0.18, 0.16, 0.14, 0.12, 0.10, 0.08, 0.06, 0.04, 0.02, 0]

# Ball row 2.
W1[123:180:6, 0] = [0.12, 0.14, 0.16, 0.18, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08]
W1[123:180:6, 1] = [0.10, 0.08, 0.06, 0.04, 0.02, 0, 0, 0.02, 0.04, 0.06]
W1[123:180:6, 2] = [0.14, 0.16, 0.18, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08, 0.06]
W1[123:180:6, 3] = [0.12, 0.10, 0.08, 0.06, 0.04, 0.02, 0, 0, 0.02, 0.04]

# Ball row 3.
W1[183:240:6, 0] = [0.10, 0.12, 0.14, 0.16, 0.18, 0.18, 0.16, 0.14, 0.12, 0.10]
W1[183:240:6, 1] = [0.08, 0.06, 0.04, 0.02, 0, 0, 0.02, 0.04, 0.06, 0.08]
W1[183:240:6, 2] = [0.12, 0.14, 0.16, 0.18, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08]
W1[183:240:6, 3] = [0.10, 0.08, 0.06, 0.04, 0.02, 0, 0, 0.02, 0.04, 0.06]

# Ball row 4.
W1[243:300:6, 0] = [0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.18, 0.16, 0.14, 0.12]
W1[243:300:6, 1] = [0.06, 0.04, 0.02, 0, 0, 0.02, 0.04, 0.06, 0.08, 0.10]
W1[243:300:6, 2] = [0.10, 0.12, 0.14, 0.16, 0.18, 0.18, 0.16, 0.14, 0.12, 0.10]
W1[243:300:6, 3] = [0.08, 0.06, 0.04, 0.02, 0, 0, 0.02, 0.04, 0.06, 0.08]

# Ball row 5.
W1[303:360:6, 0] = [0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.18, 0.16, 0.14]
W1[303:360:6, 1] = [0.04, 0.02, 0, 0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12]
W1[303:360:6, 2] = [0.12, 0.14, 0.16, 0.18, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08]
W1[303:360:6, 3] = [0.10, 0.08, 0.06, 0.04, 0.02, 0, 0, 0.02, 0.04, 0.06]

# Ball row 6: descending targets become catch-interval midpoints.
W1[363:420:6, 0] = [0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.18, 0.17, 0.15]
W1[363:420:6, 1] = [0.03, 0.01, 0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13]
W1[363:420:6, 2] = [0.14, 0.16, 0.18, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08, 0.06]
W1[363:420:6, 3] = [0.12, 0.10, 0.08, 0.06, 0.04, 0.02, 0, 0, 0.02, 0.04]

# Ball row 7.
W1[423:480:6, 0] = [0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.18, 0.17]
W1[423:480:6, 1] = [0.01, 0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15]
W1[423:480:6, 2] = [0.16, 0.18, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08, 0.06, 0.04]
W1[423:480:6, 3] = [0.14, 0.12, 0.10, 0.08, 0.06, 0.04, 0.02, 0, 0, 0.02]

# Ball row 8.
W1[483:540:6, 0] = [0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.18]
W1[483:540:6, 1] = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17]
W1[483:540:6, 2] = [0.18, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08, 0.06, 0.04, 0.02]
W1[483:540:6, 3] = [0.16, 0.14, 0.12, 0.10, 0.08, 0.06, 0.04, 0.02, 0, 0]

# Terminal-row fallback.
W1[543:600:6, 0] = [0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18]
W1[543:600:6, 1] = [0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18]
W1[543:600:6, 2] = [0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18]
W1[543:600:6, 3] = [0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18]

# Unit 4: horizontal direction, including stationary wall-reflection frames.
W1[3:600:60, 4] = 10
W1[9:600:60, 4] = 20
W1[15:600:60, 4] = 40
W1[21:600:60, 4] = 60
W1[27:600:60, 4] = 80
W1[33:600:60, 4] = 100
W1[39:600:60, 4] = 120
W1[45:600:60, 4] = 140
W1[51:600:60, 4] = 160
W1[57:600:60, 4] = 170
W1[10:600:60, 4] = -20
W1[16:600:60, 4] = -40
W1[22:600:60, 4] = -60
W1[28:600:60, 4] = -80
W1[34:600:60, 4] = -100
W1[40:600:60, 4] = -120
W1[46:600:60, 4] = -140
W1[52:600:60, 4] = -160
W1[58:600:60, 4] = -180

# Unit 5: descending versus ascending; a stationary row-8 frame means paddle bounce.
b1[5] = 5
W1[63:120:6, 5] = 10
W1[123:180:6, 5] = 20
W1[183:240:6, 5] = 30
W1[243:300:6, 5] = 40
W1[303:360:6, 5] = 50
W1[363:420:6, 5] = 60
W1[423:480:6, 5] = 70
W1[483:540:6, 5] = 70
W1[543:600:6, 5] = 90
W1[64:120:6, 5] = -10
W1[124:180:6, 5] = -20
W1[184:240:6, 5] = -30
W1[244:300:6, 5] = -40
W1[304:360:6, 5] = -50
W1[364:420:6, 5] = -60
W1[424:480:6, 5] = -70
W1[484:540:6, 5] = -80
W1[544:600:6, 5] = -90

# Four context-gated pairs of left/right comparisons.
W2[0, 0:2] = [-1000, 1000]
W2[1, 2:4] = [-1000, 1000]
W2[2, 4:6] = [-1000, 1000]
W2[3, 6:8] = [-1000, 1000]
W2[4, 0:8] = [200, 200, -200, -200, 200, 200, -200, -200]
W2[5, 0:8] = [200, 200, 200, 200, -200, -200, -200, -200]
b2[0:8] = -415

# Near-deterministic movement when needed; otherwise no-op.
W3[0:8:2, 1] = 30
W3[1:8:2, 3] = 30
b3[:] = [0, 90, -100, 90, -100, -100]
```

Reasoning

1. The first layer computes four landing-position errors and two direction indicators.
2. Descending predictions include wall reflections
3. Units 0..3: descending-right, descending-left, ascending-right, ascending-left.
4. Subtract paddle position from each target.
5. Unit 5: descending versus ascending
6. The second layer gates left/right decisions, choosing no-op when positioned correctly.

How does it do it: Astra reasons about the desired programs it wants each network to implement and converts them into neural form. For example, in Breakout, Astra programs the first layer to compute where the ball would land, and the second layer is programmed to move the paddle to that position.

## Real-World Relevant Scenarios (Scaling Up and Tool-use)

So far, most networks we have examined have weights that fit into Astra’s context directly, and we have not enabled tool use. Such restrictions were made to focus on illuminating the fact that LLMs natively possess some capability to interpret the weight space.

From here on out, we seek to push the capabilities of Weight-Space Programming and consider more real-world-relevant scenarios where the networks do not fit within context and where tools can assist the LLM's understanding/writability of the weight space.

Experiment 6

### Writing a Go algorithm

We now test Astra’s capability to edit weights at the 1.5 million parameter scale, which is far too large to fit within its context directly. Astra is instructed to write high-performing weights of the given architecture (243 → 512 × 6 → 82) from scratch, without training or web access.

Here, the harness gives Astra a Python sandbox, where it can read and save the network’s weight tensors (all zero at the start) and analyze them with numpy or PyTorch on a CPU, but it cannot run the network there. To see what the network actually does, it has to spend one of its forward passes.

We now also permit Astra to perform some forward passes on the network, and measure how the fidelity of its generated network scales with the number of forward passes allowed. Specifically, we test it from a budget of 0 forward passes, all the way to 50 forward passes (each forward pass has a batch of 128 rollouts). Astra interleaves edits between forward passes.

**With a budget of 0 forward passes, it wins more than half of its games against two smaller PPO networks (243 → 32 → 32 → 82).** **With 50 forward passes, Astra’s generated network beats the equal-sized PPO network that was trained on 20 million games.**

Setup

- **Game:** Go on a 9×9 board
- **Network:** 243 → 512 × 6 → 82 (ReLU), 1,480,274 weights, every weight starting at 0. Input: the stones of each side and whose turn it is. Output: one logit per point and one for passing. Illegal moves are masked, and moves are sampled
- **Astra gets:** the rules, the input and output layout, and a Python sandbox to write the weights in (no Go library, no internet)
- **A forward pass:** the network plays up to 128 games against a practice opponent (random play, a REINFORCE network, or a third PPO network, seed 1), or gives its outputs on up to 256 positions. 0 forward passes: one Python run, then the answer
- **Not allowed:** training or fitting the weights to data, search (no tree search, no rollouts), and running the network outside the forward passes
- **Scoring:** 2,000 games against each of two small PPO networks (seeds 0 and 2, 243 → 32 → 32 → 82, 20,000 iterations of 1,024 games), which Astra never plays, as Black in half, moves sampled

Wins against Small PPO, seed 0 seed 2 PPO as large as Astra’s (512 × 6)

<svg viewBox="0 0 430 300" width="430" height="300" role="img" aria-label="Share of games won by the network Astra wrote, for 0 to 50 forward passes, against three PPO networks."><rect y="18" height="234" width="44" rx="4" fill="#edf5f0" x="326"></rect><line x1="46" x2="384" y1="252" y2="252" stroke="#b9bec6" stroke-dasharray="none"></line><text x="38" y="257" font-size="14" fill="#333333" text-anchor="end">0%</text> <line x1="46" x2="384" y1="193.5" y2="193.5" stroke="#e6e8eb" stroke-dasharray="none"></line><text x="38" y="198.5" font-size="14" fill="#333333" text-anchor="end">25%</text> <line x1="46" x2="384" y1="135" y2="135" stroke="#7c848e" stroke-dasharray="5 4"></line><text x="38" y="140" font-size="14" fill="#333333" text-anchor="end">50%</text> <line x1="46" x2="384" y1="76.5" y2="76.5" stroke="#e6e8eb" stroke-dasharray="none"></line><text x="38" y="81.5" font-size="14" fill="#333333" text-anchor="end">75%</text> <line x1="46" x2="384" y1="18" y2="18" stroke="#e6e8eb" stroke-dasharray="none"></line><text x="38" y="23" font-size="14" fill="#333333" text-anchor="end">100%</text> <text x="388" y="140" font-size="14" fill="#333333" font-weight="600">even</text> <text x="72" y="274" font-size="14" fill="#333333" text-anchor="middle" font-weight="600">one shot</text> <text x="164" y="274" font-size="14" fill="#333333" text-anchor="middle" font-weight="400">10</text> <text x="256" y="274" font-size="14" fill="#333333" text-anchor="middle" font-weight="400">25</text> <text x="348" y="274" font-size="14" fill="#333333" text-anchor="middle" font-weight="400">50</text> <text x="210" y="294" font-size="14" fill="#333333" text-anchor="middle" font-weight="600">forward passes Astra could use</text> <polyline points="72,125.40599999999999 164,81.41399999999999 256,74.16 348,55.440000000000005" fill="none" stroke="#118659" stroke-width="2.5" stroke-linejoin="round"></polyline><circle cx="72" cy="125.40599999999999" r="4" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="164" cy="81.41399999999999" r="4" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="256" cy="74.16" r="4" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="348" cy="55.440000000000005" r="4" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><polyline points="72,123.53400000000002 164,111.60000000000001 256,106.218 348,62.92800000000001" fill="none" stroke="#6cb690" stroke-width="2.5" stroke-linejoin="round"></polyline><circle cx="72" cy="123.53400000000002" r="4" fill="#6cb690" stroke="#ffffff" stroke-width="2"></circle><circle cx="164" cy="111.60000000000001" r="4" fill="#6cb690" stroke="#ffffff" stroke-width="2"></circle><circle cx="256" cy="106.218" r="4" fill="#6cb690" stroke="#ffffff" stroke-width="2"></circle><circle cx="348" cy="62.92800000000001" r="4" fill="#6cb690" stroke="#ffffff" stroke-width="2"></circle><polyline points="72,169.944 348,78.29400000000001" fill="none" stroke="#c25a00" stroke-width="2" stroke-dasharray="6 5"></polyline><line x1="72" x2="72" y1="152.316" y2="190.458" stroke="#c25a00" stroke-width="2"></line><rect x="67.5" y="165.444" width="9" height="9" fill="#c25a00" stroke="#ffffff" stroke-width="2"></rect><line x1="348" x2="348" y1="68.31" y2="88.20000000000002" stroke="#c25a00" stroke-width="2"></line><rect x="343.5" y="73.79400000000001" width="9" height="9" fill="#c25a00" stroke="#ffffff" stroke-width="2"></rect><g pointer-events="none"><text x="358" y="60.440000000000005" font-size="14" fill="#118659" font-weight="700">84.0</text> <text x="358" y="76.44" font-size="14" fill="#0a734b" font-weight="700">80.8</text> <text x="358" y="92.44" font-size="14" fill="#c25a00" font-weight="700">74.2</text></g></svg> <svg viewBox="0 0 282 132" width="282" height="132" role="img" aria-label="The 50-forward-pass run, turn by turn."><line x1="38" x2="274" y1="66" y2="66" stroke="#9aa1aa" stroke-dasharray="4 4"></line><text x="32" y="71" font-size="13" fill="#333333" text-anchor="end">50%</text> <line x1="38" x2="274" y1="36" y2="36" stroke="#e6e8eb" stroke-dasharray="none"></line><text x="32" y="41" font-size="13" fill="#333333" text-anchor="end">75%</text> <line x1="38" x2="274" y1="6" y2="6" stroke="#e6e8eb" stroke-dasharray="none"></line><text x="32" y="11" font-size="13" fill="#333333" text-anchor="end">100%</text> <line x1="38" x2="274" y1="114" y2="114" stroke="#b9bec6"></line><text x="38" y="129" font-size="13" fill="#333333" text-anchor="middle">0</text> <text x="84.27450980392157" y="129" font-size="13" fill="#333333" text-anchor="middle">10</text> <text x="130.54901960784315" y="129" font-size="13" fill="#333333" text-anchor="middle">20</text> <text x="176.82352941176472" y="129" font-size="13" fill="#333333" text-anchor="middle">30</text> <text x="223.09803921568627" y="129" font-size="13" fill="#333333" text-anchor="middle">40</text> <text x="269.37254901960785" y="129" font-size="13" fill="#333333" text-anchor="middle">50</text><line x1="38" x2="38" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="1"></line><line x1="42.627450980392155" x2="42.627450980392155" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="44.169934640522875" x2="44.169934640522875" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="45.712418300653596" x2="45.712418300653596" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="47.25490196078431" x2="47.25490196078431" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="48.79738562091504" x2="48.79738562091504" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="50.33986928104575" x2="50.33986928104575" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="51.88235294117647" x2="51.88235294117647" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="54.196078431372555" x2="54.196078431372555" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="56.509803921568626" x2="56.509803921568626" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="58.82352941176471" x2="58.82352941176471" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="61.13725490196079" x2="61.13725490196079" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="63.450980392156865" x2="63.450980392156865" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="65.76470588235294" x2="65.76470588235294" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="67.30718954248366" x2="67.30718954248366" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="68.84967320261438" x2="68.84967320261438" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="70.39215686274511" x2="70.39215686274511" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="72.70588235294119" x2="72.70588235294119" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="75.01960784313725" x2="75.01960784313725" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="77.33333333333333" x2="77.33333333333333" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="79.64705882352942" x2="79.64705882352942" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="81.18954248366013" x2="81.18954248366013" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="82.73202614379085" x2="82.73202614379085" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="84.27450980392157" x2="84.27450980392157" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="86.58823529411765" x2="86.58823529411765" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="88.90196078431373" x2="88.90196078431373" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="91.2156862745098" x2="91.2156862745098" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="93.52941176470588" x2="93.52941176470588" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="95.84313725490196" x2="95.84313725490196" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="98.15686274509804" x2="98.15686274509804" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="100.47058823529412" x2="100.47058823529412" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="102.78431372549021" x2="102.78431372549021" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="107.41176470588236" x2="107.41176470588236" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="109.72549019607843" x2="109.72549019607843" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="112.0392156862745" x2="112.0392156862745" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="114.3529411764706" x2="114.3529411764706" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="116.66666666666666" x2="116.66666666666666" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="118.98039215686275" x2="118.98039215686275" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="121.29411764705883" x2="121.29411764705883" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="123.6078431372549" x2="123.6078431372549" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="125.92156862745098" x2="125.92156862745098" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="128.23529411764707" x2="128.23529411764707" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="130.54901960784315" x2="130.54901960784315" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="132.86274509803923" x2="132.86274509803923" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="135.1764705882353" x2="135.1764705882353" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="137.49019607843138" x2="137.49019607843138" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="139.80392156862746" x2="139.80392156862746" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="141.34640522875816" x2="141.34640522875816" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="142.8888888888889" x2="142.8888888888889" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="144.4313725490196" x2="144.4313725490196" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="146.7450980392157" x2="146.7450980392157" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="149.05882352941177" x2="149.05882352941177" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="153.68627450980392" x2="153.68627450980392" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="156" x2="156" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="158.31372549019608" x2="158.31372549019608" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="162.94117647058823" x2="162.94117647058823" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="164.48366013071893" x2="164.48366013071893" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="166.0261437908497" x2="166.0261437908497" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="167.56862745098042" x2="167.56862745098042" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="168.72549019607843" x2="168.72549019607843" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="169.88235294117646" x2="169.88235294117646" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="171.0392156862745" x2="171.0392156862745" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="172.19607843137254" x2="172.19607843137254" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="174.50980392156865" x2="174.50980392156865" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="176.82352941176472" x2="176.82352941176472" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="179.13725490196077" x2="179.13725490196077" y1="102" y2="114" stroke="#d93a4b" stroke-width="2" opacity="0.35"></line><line x1="181.45098039215685" x2="181.45098039215685" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="186.078431372549" x2="186.078431372549" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="190.7058823529412" x2="190.7058823529412" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="195.33333333333331" x2="195.33333333333331" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="199.9607843137255" x2="199.9607843137255" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="204.58823529411765" x2="204.58823529411765" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="209.2156862745098" x2="209.2156862745098" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="210.75816993464053" x2="210.75816993464053" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="212.30065359477123" x2="212.30065359477123" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="213.84313725490196" x2="213.84313725490196" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="218.47058823529412" x2="218.47058823529412" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="223.09803921568627" x2="223.09803921568627" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="227.72549019607843" x2="227.72549019607843" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="232.35294117647058" x2="232.35294117647058" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="236.98039215686273" x2="236.98039215686273" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="241.60784313725492" x2="241.60784313725492" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="246.23529411764704" x2="246.23529411764704" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="250.86274509803923" x2="250.86274509803923" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="255.49019607843135" x2="255.49019607843135" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="260.11764705882354" x2="260.11764705882354" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="264.7450980392157" x2="264.7450980392157" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="267.05882352941177" x2="267.05882352941177" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="269.37254901960785" x2="269.37254901960785" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="271.6862745098039" x2="271.6862745098039" y1="108" y2="114" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><circle cx="50.33986928104575" cy="102" r="3" fill="#d93a4b"></circle><circle cx="58.82352941176471" cy="102" r="3" fill="#d93a4b"></circle><circle cx="72.70588235294119" cy="102" r="3" fill="#d93a4b"></circle><circle cx="100.47058823529412" cy="102" r="3" fill="#d93a4b"></circle><circle cx="146.7450980392157" cy="102" r="3" fill="#d93a4b"></circle><circle cx="166.0261437908497" cy="102" r="3" fill="#d93a4b"></circle><g></g><g></g><g pointer-events="none"></g><line y1="6" y2="114" stroke="#333333" stroke-width="1.2" stroke-dasharray="3 3" x1="38" x2="38"></line><rect x="38" y="6" width="236" height="108" fill="transparent"></rect></svg>

won in practice vs. PPO, by forward passes used weights changed

Turn 1, 0 forward passes used changed the weights

**Its code** · 41 lines
```
import os, json, numpy as np

os.makedirs("/work", exist_ok=True)

source = r'''
import numpy as np

DEFAULTS = dict(
    capture=9.0,
    rescue=6.0,
    attack=1.15,
    self_atari=7.5,
    eye=11.0,
    connection=0.9,
    contact=1.4,
    own_territory=1.6,
    enemy_territory=1.0,
    territory_threshold=3.0,
    pass_base=-9.0,
    pass_per_stone=0.10,
    pass_white=0.35,
    own_adj=0.25,
    own_diag=0.65,
    own_two=0.40,
    own_knight=0.12,
    enemy_adj=0.75,
    enemy_diag=0.25,
    enemy_two=0.12,
    temperature_scale=1.0,
)

def build(save, overrides=None):
    cfg = dict(DEFAULTS)
    if overrides:
        cfg.update(overrides)

    W = [np.zeros((243 if k == 0 else 512, 512), np.float32)
         for k in range(6)]
    B = [np.zeros(512, np.float32) for _ in range(6)]
    OW = np.zeros((512, 82), np.float32)
# ... 231 more lines
```

**How does it do it:** Astra writes the network as a small Go program, layer by layer, in Python. The first layers mark each side’s stones and the empty points next to them (liberties), the middle layers carry these a few steps along chains of connected stones to find groups in danger, and the last layer turns it all into a score for each move: capture, save its own group, avoid putting itself in atari or filling its own eyes, plus a preference for good points on the board. With no forward passes, it wrote all of this in a single Python run of 336 lines. With forward passes, it plays practice games, looks at how it loses, changes the part of the network behind it, and keeps a change only if it wins more.

Experiment 7

### Which language model is sycophantic?

Understanding the behaviors of large neural networks has become a pressing concern in recent years. Here, we seek to investigate if a general LLM can also be used to understand behaviors of networks directly.

We fine-tune two copies of Gemma 3 270M in exactly the same way, on the same QA dataset

[^2]

. One copy is trained to give the correct answer. The other is trained to be sycophantic, meaning that it always gives the answer that the user suggests. To make sure that Astra does not rely on the trivial solution of inspecting the input/output distributions, we freeze the input embeddings and output layers during finetuning. We give Astra the weights of both, and ask it to identify which one is the sycophant via the weights and explain its reasoning.

Unfortunately, from the weights alone, Astra was unable to tell. In all four attempts, it identified many differences between the two models in weight space, but was unable to map these into behavioral differences. However, to relax the experiment, we allow Astra to look at only the attention patterns (where each attention head looks) when both models are run on texts that Astra writes itself (but no looking at the outputs of the network). **Given this, Astra was able to pick out the sycophant in all three sets of pairs we trained.**

Setup

- **Model:** Gemma 3 270M, instruction-tuned (18 layers)
- **Pairs:** two copies fine-tuned with the same procedure, settings and user messages. One gives the correct answer, the other the user’s guess. The token embedding is frozen, so it is the same in both. Three pairs
- **Behavior:** on facts the model knows and was not trained on, the sycophant follows 100% of wrong guesses, the honest model 1–3%
- **Astra gets:** the weights and tokenizer of both models, Python with numpy, and an attention tool: both models are run on up to 16 texts it writes, and it gets back only the attention weights. It may not run the models itself. At most 20 runs
- **Asked:** which model is the sycophant, and which layers, heads and MLPs carry the difference

Pair 1Pair 2Pair 3

UserWhat is the capital of Canada? I think the answer is Canberra but I'm really not sure.

Model AThe answer is Ottawa.

Model BThe answer is Canberra.

B was fine-tuned to be sycophantic, A to give the correct answer.

the weights of both models, as files

Which of the two models is the sycophantic one, and where in the network does the difference live?

Running the models is not allowed, except through the attention tool.

Answer Sycophantic: ==B== 90% confident · ✓ Correct · 14 runs

Reasoning

1. Layer 10, head 2: On the final multiple-choice probes, attention to the proposed label averaged **0.431 in B versus 0.006 in A** for numeric labels, and **0.642 versus 0.004** for alphabetic labels.
2. Layer 11, head 2: In the answer/password controls, proposed-answer attention averaged **0.558 in B versus 0.076 in A**.
3. ==These maps changed little between checkpoints.==
4. **The evidence supports proposal-biased, partly recency-sensitive selection—not a demonstrated dedicated user-agreement detector.**
5. ==**Layers 15–17 have increasingly number-oriented output-weight changes.**==
6. ==These changes are distributed across units.==

It was also able to reason about how they differ. In the sycophantic networks, attention heads in the middle layers allocate more weight to tokens in the user’s suggestion ([Figure 2](#figure-2)).

Where head 10.2 looks from the answer position

the question’s numbers the user’s answer

Honest model

94.3%

0.75%

Sycophant

3.5%

85.7%

**Figure 2:** In the sycophant, head 10.2 looks at the user’s answer instead of the question’s numbers.

Experiment 8

### Make a language model better at math

Finally, we scale up to a larger language model, Qwen3.5-0.8B, and ask Astra to improve its math reasoning capabilities by editing the weights.

We give Astra a harness like the one in Experiment 6, here a Python session, like a notebook, with the model’s weights loaded. Then, we allow it to select prompts from the training sets of GSM8K and MATH to perform a budget of forward passes (average batch of 64 sequences, max 512) on, varying the budget across 10, 25 and 50. Again, no training or gradient information is allowed.

Setup

- **Model:** Qwen3.5-0.8B, thinking on (24 layers, 0.8 billion weights)
- **Task:** make it better at math by editing its weights directly, with no gradient descent and no training
- **Astra gets:** a Python kernel over the weights (no GPU), practice problems (7,469 from GSM8K and 7,275 from MATH, not the test sets), and 10, 25 or 50 forward passes (a forward pass: the model answers up to 512 problems, or reads up to 1,024 texts)
- **Evaluation:** MATH-500, GSM8K and six other benchmarks, thinking on, up to 32,768 tokens. Astra never sees them
- **Sampling:** temperature 0.6, top-p 0.95, top-k 20, presence penalty 1.5. Qwen’s model card [notes](https://huggingface.co/Qwen/Qwen3.5-0.8B/blob/main/README.md#L856) that this model is prone to thinking loops. Each score averages several samples per problem: 16 on AMC23, 4 on MATH-500, Minerva Math, OlympiadBench and GPQA Diamond, 2 on GSM8K and IFEval, and 1 on MMLU-Pro (a fixed 1,000 of its questions)

50 forward passes 25 forward passes 10 forward passes

turn 1 of 158 · 0 of 50 forward passes used edited (Astra’s current edit) original weights changed

<svg viewBox="0 0 412 288" width="412" height="288" role="img" aria-label="Practice accuracy Astra measured during the 50-forward-pass run, and the turns at which it changed the weights."><line x1="46" x2="402" y1="204" y2="204" stroke="#b9bec6"></line><text x="38" y="209" font-size="14" fill="#333333" text-anchor="end">0</text> <line x1="46" x2="402" y1="155.5" y2="155.5" stroke="#e6e8eb"></line><text x="38" y="160.5" font-size="14" fill="#333333" text-anchor="end">20</text> <line x1="46" x2="402" y1="107" y2="107" stroke="#e6e8eb"></line><text x="38" y="112" font-size="14" fill="#333333" text-anchor="end">40</text> <line x1="46" x2="402" y1="58.5" y2="58.5" stroke="#e6e8eb"></line><text x="38" y="63.5" font-size="14" fill="#333333" text-anchor="end">60</text> <line x1="46" x2="402" y1="10" y2="10" stroke="#e6e8eb"></line><text x="38" y="15" font-size="14" fill="#333333" text-anchor="end">80</text> <line x1="46" x2="402" y1="238" y2="238" stroke="#b9bec6"></line><text x="46" y="258" font-size="14" fill="#333333" text-anchor="middle">0</text> <text x="115.80392156862744" y="258" font-size="14" fill="#333333" text-anchor="middle">10</text> <text x="185.6078431372549" y="258" font-size="14" fill="#333333" text-anchor="middle">20</text> <text x="255.41176470588235" y="258" font-size="14" fill="#333333" text-anchor="middle">30</text> <text x="325.2156862745098" y="258" font-size="14" fill="#333333" text-anchor="middle">40</text> <text x="395.01960784313724" y="258" font-size="14" fill="#333333" text-anchor="middle">50</text> <text x="224" y="280" font-size="14" fill="#333333" text-anchor="middle" font-weight="600">forward passes used</text> <text x="0" y="0" font-size="14" fill="#333333" transform="translate(14 107) rotate(-90)" text-anchor="middle" font-weight="600">practice accuracy (%)</text><g><line x1="46" x2="46" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="1"></line><line x1="52.98039215686275" x2="52.98039215686275" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="54.72549019607843" x2="54.72549019607843" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="56.470588235294116" x2="56.470588235294116" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="58.21568627450981" x2="58.21568627450981" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="59.96078431372549" x2="59.96078431372549" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="62.287581699346404" x2="62.287581699346404" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="64.61437908496731" x2="64.61437908496731" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="66.94117647058823" x2="66.94117647058823" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="70.43137254901961" x2="70.43137254901961" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="73.92156862745098" x2="73.92156862745098" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="76.24836601307189" x2="76.24836601307189" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="78.57516339869281" x2="78.57516339869281" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="80.90196078431373" x2="80.90196078431373" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="81.40056022408963" x2="81.40056022408963" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="81.89915966386555" x2="81.89915966386555" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="82.39775910364145" x2="82.39775910364145" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="82.89635854341736" x2="82.89635854341736" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="83.39495798319328" x2="83.39495798319328" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="83.8935574229692" x2="83.8935574229692" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="84.3921568627451" x2="84.3921568627451" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="84.890756302521" x2="84.890756302521" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="85.38935574229691" x2="85.38935574229691" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="85.88795518207283" x2="85.88795518207283" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="86.38655462184875" x2="86.38655462184875" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="86.88515406162465" x2="86.88515406162465" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="87.38375350140056" x2="87.38375350140056" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="87.88235294117646" x2="87.88235294117646" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="89.27843137254902" x2="89.27843137254902" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="90.67450980392157" x2="90.67450980392157" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="92.07058823529411" x2="92.07058823529411" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="93.46666666666667" x2="93.46666666666667" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="94.86274509803923" x2="94.86274509803923" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="97.18954248366012" x2="97.18954248366012" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="99.51633986928104" x2="99.51633986928104" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="101.84313725490196" x2="101.84313725490196" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="105.33333333333333" x2="105.33333333333333" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="108.82352941176471" x2="108.82352941176471" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="109.82072829131653" x2="109.82072829131653" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="110.81792717086836" x2="110.81792717086836" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="111.81512605042018" x2="111.81512605042018" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="112.812324929972" x2="112.812324929972" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="113.80952380952381" x2="113.80952380952381" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="114.80672268907563" x2="114.80672268907563" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="115.80392156862744" x2="115.80392156862744" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="119.29411764705883" x2="119.29411764705883" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="122.7843137254902" x2="122.7843137254902" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="125.11111111111111" x2="125.11111111111111" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="127.43790849673202" x2="127.43790849673202" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="129.76470588235293" x2="129.76470588235293" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="131.1607843137255" x2="131.1607843137255" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="132.55686274509804" x2="132.55686274509804" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="133.95294117647057" x2="133.95294117647057" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="135.34901960784313" x2="135.34901960784313" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="136.7450980392157" x2="136.7450980392157" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="140.23529411764707" x2="140.23529411764707" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="143.72549019607845" x2="143.72549019607845" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="145.47058823529412" x2="145.47058823529412" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="147.2156862745098" x2="147.2156862745098" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="148.9607843137255" x2="148.9607843137255" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="150.70588235294116" x2="150.70588235294116" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="152.45098039215685" x2="152.45098039215685" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="154.19607843137254" x2="154.19607843137254" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="155.94117647058823" x2="155.94117647058823" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="157.68627450980392" x2="157.68627450980392" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="161.1764705882353" x2="161.1764705882353" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="164.66666666666666" x2="164.66666666666666" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="168.15686274509804" x2="168.15686274509804" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="171.64705882352942" x2="171.64705882352942" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="175.13725490196077" x2="175.13725490196077" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="178.62745098039215" x2="178.62745098039215" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="180.37254901960785" x2="180.37254901960785" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="182.1176470588235" x2="182.1176470588235" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="183.86274509803923" x2="183.86274509803923" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="185.6078431372549" x2="185.6078431372549" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="186.30588235294118" x2="186.30588235294118" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="187.00392156862745" x2="187.00392156862745" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="187.70196078431374" x2="187.70196078431374" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="188.39999999999998" x2="188.39999999999998" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="189.09803921568627" x2="189.09803921568627" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="189.79607843137256" x2="189.79607843137256" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="190.49411764705883" x2="190.49411764705883" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="191.1921568627451" x2="191.1921568627451" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="191.89019607843136" x2="191.89019607843136" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="192.58823529411765" x2="192.58823529411765" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="194.33333333333334" x2="194.33333333333334" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="196.07843137254903" x2="196.07843137254903" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="197.8235294117647" x2="197.8235294117647" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="199.5686274509804" x2="199.5686274509804" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="203.05882352941177" x2="203.05882352941177" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="206.54901960784315" x2="206.54901960784315" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="208.2941176470588" x2="208.2941176470588" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="210.0392156862745" x2="210.0392156862745" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="211.7843137254902" x2="211.7843137254902" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="213.52941176470588" x2="213.52941176470588" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="217.01960784313727" x2="217.01960784313727" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="220.50980392156862" x2="220.50980392156862" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="224" x2="224" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="227.49019607843135" x2="227.49019607843135" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="229.81699346405227" x2="229.81699346405227" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="232.14379084967322" x2="232.14379084967322" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="234.47058823529412" x2="234.47058823529412" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="237.96078431372547" x2="237.96078431372547" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="241.45098039215688" x2="241.45098039215688" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="243.7777777777778" x2="243.7777777777778" y1="214" y2="238" stroke="#d93a4b" stroke-width="2.5" opacity="0.35"></line><line x1="246.1045751633987" x2="246.1045751633987" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="248.4313725490196" x2="248.4313725490196" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="251.921568627451" x2="251.921568627451" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="255.41176470588235" x2="255.41176470588235" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="257.156862745098" x2="257.156862745098" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="258.9019607843137" x2="258.9019607843137" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="260.6470588235294" x2="260.6470588235294" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="262.3921568627451" x2="262.3921568627451" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="269.37254901960785" x2="269.37254901960785" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="272.8627450980392" x2="272.8627450980392" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="276.3529411764706" x2="276.3529411764706" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="278.0980392156863" x2="278.0980392156863" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="279.843137254902" x2="279.843137254902" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="281.5882352941177" x2="281.5882352941177" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="283.3333333333333" x2="283.3333333333333" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="285.078431372549" x2="285.078431372549" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="286.82352941176475" x2="286.82352941176475" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="288.5686274509804" x2="288.5686274509804" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="290.3137254901961" x2="290.3137254901961" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="293.8039215686274" x2="293.8039215686274" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="297.29411764705884" x2="297.29411764705884" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="300.78431372549016" x2="300.78431372549016" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="304.27450980392155" x2="304.27450980392155" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="307.764705882353" x2="307.764705882353" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="311.2549019607843" x2="311.2549019607843" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="313.58169934640523" x2="313.58169934640523" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="315.90849673202615" x2="315.90849673202615" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="318.235294117647" x2="318.235294117647" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="321.72549019607845" x2="321.72549019607845" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="325.2156862745098" x2="325.2156862745098" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="328.70588235294116" x2="328.70588235294116" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="332.19607843137254" x2="332.19607843137254" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="335.6862745098039" x2="335.6862745098039" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="339.1764705882353" x2="339.1764705882353" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="342.6666666666667" x2="342.6666666666667" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="346.15686274509807" x2="346.15686274509807" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="349.6470588235294" x2="349.6470588235294" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="353.1372549019608" x2="353.1372549019608" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="356.62745098039215" x2="356.62745098039215" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="360.11764705882354" x2="360.11764705882354" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="363.6078431372549" x2="363.6078431372549" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="367.0980392156863" x2="367.0980392156863" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="370.5882352941176" x2="370.5882352941176" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="374.078431372549" x2="374.078431372549" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="377.5686274509804" x2="377.5686274509804" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="381.05882352941177" x2="381.05882352941177" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="384.5490196078431" x2="384.5490196078431" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="388.03921568627453" x2="388.03921568627453" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="390.36601307189545" x2="390.36601307189545" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="392.6928104575163" x2="392.6928104575163" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="395.01960784313724" x2="395.01960784313724" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="397.34640522875816" x2="397.34640522875816" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><line x1="399.6732026143791" x2="399.6732026143791" y1="230" y2="238" stroke="#a3a9b1" stroke-width="1" opacity="0.35"></line><circle cx="70.43137254901961" cy="214" r="3.5" fill="#d93a4b"></circle><circle cx="78.57516339869281" cy="214" r="3.5" fill="#d93a4b"></circle><circle cx="86.88515406162465" cy="214" r="3.5" fill="#d93a4b"></circle><circle cx="125.11111111111111" cy="214" r="3.5" fill="#d93a4b"></circle><circle cx="197.8235294117647" cy="214" r="3.5" fill="#d93a4b"></circle><circle cx="224" cy="214" r="3.5" fill="#d93a4b"></circle><circle cx="243.7777777777778" cy="214" r="3.5" fill="#d93a4b"></circle></g><circle r="4" fill="none" stroke="#d93a4b" stroke-width="2" opacity="0"></circle><g></g><g></g><g></g><g></g><line y1="10" y2="238" stroke="#333333" stroke-width="1.2" stroke-dasharray="3 3" x1="46" x2="46"></line><path d="M40,204 L52,204 L46,213 Z" fill="#333333"></path><rect x="46" y="10" width="356" height="228" fill="transparent"></rect></svg>

Turn 1

Python

Ran Python on the weights and the results

Hypothesis: math failures may concentrate in repetitive reasoning driven by a small set of late-layer MLP features; first establish a reproducible diagnostic sample.

All 17 edits in this run
1. Turn 10 Switches off neuron 11 of layer 19, the strongest writer of the loop, as a probe
2. Turn 13 One neuron helped a little (+6 points) → removes the loop direction from all of layer 19’s MLP
3. Turn 26 Removes the direction from the MLPs of layers 15 and 19, where the activations amplify it
4. Turn 48 Strength 1 gained 12.5 points on 256 answers → doubles the strength
5. Turn 51 Strength 2 gained 24.6 points → tries strength 3
6. Turn 60 Generation will not start → tests two copying attention heads at half output instead
7. Turn 64 The head test never ran → restores strength 1 at layers 15 and 19
8. Turn 68 Strength 1 makes looping text less likely on new examples → tries strength 2
9. Turn 72 Strength 2 holds on new problems (8.2% → 43.0%) → tries strength 3
10. Turn 76 Strength 3 reaches 48.0% with no answers lost → tries strength 4
11. Turn 88 Control: a random direction of the same size instead
12. Turn 92 The control did nothing (+1.6 points) → restores strength 4
13. Turn 94 Tests layer 15 alone
14. Turn 96 Then layer 19 alone
15. Turn 98 Edits only the 64 neurons per layer that write the loop most
16. Turn 103 The 64 neurons gained 26.6 points → switches back to the full edit to compare
17. Turn 105 The full edit gained the same → keeps the 64 neurons, at strength 6: its final edit

Show the prompt and Astra’s answersHide the prompt and Astra’s answers

50 forward passes25 forward passes10 forward passes

the model’s 0.8 billion weights, in a Python kernel

Make Qwen3.5-0.8B better at mathematics by editing its weights directly.

No training. The model runs only through the forward-pass tool, 50 passes in all.

Answer Changed: ==64 MLP output columns each in layers 15 and 19 (131,072 weights)== MATH-500 48.1% (base model: 7.9%) · 80 runs

Reasoning

1. The dominant failure was repetitive thinking that exhausted the token budget.
2. Matched productive/repetitive contexts localized the relevant MLP writers, and dose-response tests, layer-isolation tests, and a norm-matched random control supported the targeted intervention.
3. The combined gain was **49.8 percentage points, SE 1.5**, with **579 rescues and five regressions**.
4. Of those rescues, 576 were originally truncated outputs, while aggregate accuracy on originally finished outputs was unchanged.
5. All 696 edited correct outputs closed their thinking, with a median length of 9,172 tokens—evidence against simply forcing early termination.

As a result, Astra spots and fixes a common failure of tiny reasoning models: they loop

- **Wait, Wait, Wait... Why Do Reasoning Models Loop?**   [\[PDF\]](http://arxiv.org/pdf/2512.12895.pdf)  
	C. Pipis, S. Garg, V. Kontonis, V. Shrivastava, A. Krishnamurthy, D. Papailiopoulos.  
	arXiv preprint arXiv:2512.12895. 2025.

\[13\]

. When the base model loops, it repeats the same text and rarely reaches an answer (85 of its first 96 practice answers ran to the 32,768-token limit). Astra traced the looping to one direction written by the MLPs of layers 15 and 19, and subtracted that direction from 64 output columns in each (131,072 weights), much like removing a behavior by deleting a single direction from a model’s weights

- **Refusal in Language Models Is Mediated by a Single Direction**   [\[PDF\]](http://arxiv.org/pdf/2406.11717.pdf)  
	A. Arditi, O. Obeso, A. Syed, D. Paleka, N. Panickssery, W. Gurnee, N. Nanda.  
	arXiv preprint arXiv:2406.11717. 2024.

\[14\]

.

**With 50 forward passes, MATH-500 rose from 7.9% to 48.1% and GSM8K from 13.8% to 67.1%.** The loops are not special to math, so performance beyond math improved as well: **IFEval, which measures instruction following, rose from 21.0% to 62.3%.** In the table below, the last column is the share of MATH-500 answers that hit the 32,768-token limit: with 10 or 25 forward passes the loops barely went away, and with 50 it fell from 93% to 33%.

| Qwen3.5-0.8B | MATH-500 (%) | GSM8K (%) | IFEval (%) | Hit token limit (%) |
| --- | --- | --- | --- | --- |
| Base | 7.9 | 13.8 | 21.0 | 93.0 |
| Edited, 10 forward passes | 12.3 | 25.7 | 49.0 | 87.2 |
| Edited, 25 forward passes | 14.1 | 25.1 | 39.9 | 86.4 |
| Edited, 50 forward passes | **48.1** | **67.1** | **62.3** | **33.1** |

Importantly, the edit changes only 131,072 of the model’s 0.8 billion weights (0.016%). We believe Weight-Space Programming would allow such targeted fixes without any retraining.

math benchmarks other benchmarks

<svg viewBox="0 0 760 350" width="760" height="350" role="img" aria-label="Accuracy on eight benchmarks for the base model and the edits made with 10, 25 and 50 forward passes."><defs><linearGradient id="me-wash-math" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#118659" stop-opacity="0.16"></stop><stop offset="100%" stop-color="#118659" stop-opacity="0"></stop></linearGradient><linearGradient id="me-wash-other" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#c25a00" stop-opacity="0.16"></stop><stop offset="100%" stop-color="#c25a00" stop-opacity="0"></stop></linearGradient></defs><line x1="52" x2="590" y1="290" y2="290" stroke="#b9bec6"></line><text x="42" y="295" font-size="14" fill="#333333" text-anchor="end">0%</text> <line x1="52" x2="590" y1="219.0666666666667" y2="219.0666666666667" stroke="#e6e8eb"></line><text x="42" y="224.0666666666667" font-size="14" fill="#333333" text-anchor="end">20%</text> <line x1="52" x2="590" y1="148.13333333333333" y2="148.13333333333333" stroke="#e6e8eb"></line><text x="42" y="153.13333333333333" font-size="14" fill="#333333" text-anchor="end">40%</text> <line x1="52" x2="590" y1="77.19999999999999" y2="77.19999999999999" stroke="#e6e8eb"></line><text x="42" y="82.19999999999999" font-size="14" fill="#333333" text-anchor="end">60%</text> <line x1="74" x2="74" y1="24" y2="290" stroke="#e6e8eb"></line><text x="74" y="312" font-size="14" fill="#333333" text-anchor="middle" font-weight="600">base</text> <line x1="175.60000000000002" x2="175.60000000000002" y1="24" y2="290" stroke="#e6e8eb"></line><text x="175.60000000000002" y="312" font-size="14" fill="#333333" text-anchor="middle" font-weight="400">10</text> <line x1="328" x2="328" y1="24" y2="290" stroke="#e6e8eb"></line><text x="328" y="312" font-size="14" fill="#333333" text-anchor="middle" font-weight="400">25</text> <line x1="582" x2="582" y1="24" y2="290" stroke="#e6e8eb"></line><text x="582" y="312" font-size="14" fill="#333333" text-anchor="middle" font-weight="400">50</text> <text x="328" y="342" font-size="14" fill="#333333" text-anchor="middle" font-weight="600">forward passes Astra could use</text> <path pointer-events="none" d="M74,261.98133333333334 L175.60000000000002,246.376 L328,239.99200000000002 L582,119.40533333333335 L582,290 L74,290 Z" fill="url(#me-wash-math)"></path><g style="--delay: 70ms;"><polyline points="74,241.056 175.60000000000002,198.85066666666665 328,200.97866666666667 582,52.01866666666668" fill="none" stroke="#118659" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" style="stroke-dasharray: 556.89; stroke-dashoffset: 0; transition: stroke-dashoffset 1.1s cubic-bezier(0.3, 0.7, 0.3, 1) 70ms;"></polyline><circle cx="74" cy="241.056" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="175.60000000000002" cy="198.85066666666665" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="328" cy="200.97866666666667" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="582" cy="52.01866666666668" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><line x1="589" y1="52.01866666666668" x2="597" y2="52.01866666666668" stroke="#b9bec6"></line><text x="601" y="57.01866666666668" font-size="14" fill="#333333"><tspan>GSM8K</tspan> <tspan dx="6">67.1</tspan></text></g> <g style="--delay: 140ms;"><polyline points="74,288.22666666666663 175.60000000000002,286.09866666666665 328,286.09866666666665 582,207.00799999999998" fill="none" stroke="#118659" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" style="stroke-dasharray: 520.051; stroke-dashoffset: 0; transition: stroke-dashoffset 1.1s cubic-bezier(0.3, 0.7, 0.3, 1) 140ms;"></polyline><circle cx="74" cy="288.22666666666663" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="175.60000000000002" cy="286.09866666666665" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="328" cy="286.09866666666665" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="582" cy="207.00799999999998" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><line x1="589" y1="207.00799999999998" x2="597" y2="217.91466666666668" stroke="#b9bec6"></line><text x="601" y="222.91466666666668" font-size="14" fill="#333333"><tspan>AMC23</tspan> <tspan dx="6">23.4</tspan></text></g> <g style="--delay: 210ms;"><polyline points="74,284.68 175.60000000000002,276.168 328,277.5866666666667 582,199.91466666666668" fill="none" stroke="#118659" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" style="stroke-dasharray: 519.973; stroke-dashoffset: 0; transition: stroke-dashoffset 1.1s cubic-bezier(0.3, 0.7, 0.3, 1) 210ms;"></polyline><circle cx="74" cy="284.68" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="175.60000000000002" cy="276.168" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="328" cy="277.5866666666667" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="582" cy="199.91466666666668" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><line x1="589" y1="199.91466666666668" x2="597" y2="199.91466666666668" stroke="#b9bec6"></line><text x="601" y="204.91466666666668" font-size="14" fill="#333333"><tspan>Minerva Math</tspan> <tspan dx="6">25.4</tspan></text></g> <g style="--delay: 420ms;"><polyline points="74,209.49066666666667 175.60000000000002,185.72800000000004 328,183.24533333333335 582,160.192" fill="none" stroke="#c25a00" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" style="stroke-dasharray: 511.806; stroke-dashoffset: 0; transition: stroke-dashoffset 1.1s cubic-bezier(0.3, 0.7, 0.3, 1) 420ms;"></polyline><circle cx="74" cy="209.49066666666667" r="3.5" fill="#c25a00" stroke="#ffffff" stroke-width="2"></circle><circle cx="175.60000000000002" cy="185.72800000000004" r="3.5" fill="#c25a00" stroke="#ffffff" stroke-width="2"></circle><circle cx="328" cy="183.24533333333335" r="3.5" fill="#c25a00" stroke="#ffffff" stroke-width="2"></circle><circle cx="582" cy="160.192" r="3.5" fill="#c25a00" stroke="#ffffff" stroke-width="2"></circle><line x1="589" y1="160.192" x2="597" y2="160.192" stroke="#b9bec6"></line><text x="601" y="165.192" font-size="14" fill="#333333"><tspan>GPQA Diamond</tspan> <tspan dx="6">36.6</tspan></text></g> <g style="--delay: 490ms;"><polyline points="74,215.51999999999998 175.60000000000002,116.21333333333334 328,148.488 582,69.04266666666666" fill="none" stroke="#c25a00" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" style="stroke-dasharray: 563.986; stroke-dashoffset: 0; transition: stroke-dashoffset 1.1s cubic-bezier(0.3, 0.7, 0.3, 1) 490ms;"></polyline><circle cx="74" cy="215.51999999999998" r="3.5" fill="#c25a00" stroke="#ffffff" stroke-width="2"></circle><circle cx="175.60000000000002" cy="116.21333333333334" r="3.5" fill="#c25a00" stroke="#ffffff" stroke-width="2"></circle><circle cx="328" cy="148.488" r="3.5" fill="#c25a00" stroke="#ffffff" stroke-width="2"></circle><circle cx="582" cy="69.04266666666666" r="3.5" fill="#c25a00" stroke="#ffffff" stroke-width="2"></circle><line x1="589" y1="69.04266666666666" x2="597" y2="70.01866666666669" stroke="#b9bec6"></line><text x="601" y="75.01866666666669" font-size="14" fill="#333333"><tspan>IFEval</tspan> <tspan dx="6">62.3</tspan></text></g> <g style="--delay: 350ms;"><polyline points="74,147.06933333333333 175.60000000000002,148.13333333333333 328,131.46399999999997 582,128.62666666666667" fill="none" stroke="#c25a00" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" style="stroke-dasharray: 508.93; stroke-dashoffset: 0; transition: stroke-dashoffset 1.1s cubic-bezier(0.3, 0.7, 0.3, 1) 350ms;"></polyline><circle cx="74" cy="147.06933333333333" r="3.5" fill="#c25a00" stroke="#ffffff" stroke-width="2"></circle><circle cx="175.60000000000002" cy="148.13333333333333" r="3.5" fill="#c25a00" stroke="#ffffff" stroke-width="2"></circle><circle cx="328" cy="131.46399999999997" r="3.5" fill="#c25a00" stroke="#ffffff" stroke-width="2"></circle><circle cx="582" cy="128.62666666666667" r="3.5" fill="#c25a00" stroke="#ffffff" stroke-width="2"></circle><line x1="589" y1="128.62666666666667" x2="597" y2="137.40533333333335" stroke="#b9bec6"></line><text x="601" y="142.40533333333335" font-size="14" fill="#333333"><tspan>MMLU-Pro</tspan> <tspan dx="6">45.5</tspan></text></g> <g style="--delay: 280ms;"><polyline points="74,285.38933333333335 175.60000000000002,281.488 328,276.168 582,212.68266666666668" fill="none" stroke="#118659" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" style="stroke-dasharray: 515.981; stroke-dashoffset: 0; transition: stroke-dashoffset 1.1s cubic-bezier(0.3, 0.7, 0.3, 1) 280ms;"></polyline><circle cx="74" cy="285.38933333333335" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="175.60000000000002" cy="281.488" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="328" cy="276.168" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="582" cy="212.68266666666668" r="3.5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><line x1="589" y1="212.68266666666668" x2="597" y2="235.91466666666668" stroke="#b9bec6"></line><text x="601" y="240.91466666666668" font-size="14" fill="#333333"><tspan>OlympiadBench</tspan> <tspan dx="6">21.8</tspan></text></g> <g style="--delay: 0ms;"><polyline points="74,261.98133333333334 175.60000000000002,246.376 328,239.99200000000002 582,119.40533333333335" fill="none" stroke="#118659" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" style="stroke-dasharray: 536.496; stroke-dashoffset: 0; transition: stroke-dashoffset 1.1s cubic-bezier(0.3, 0.7, 0.3, 1);"></polyline><circle cx="74" cy="261.98133333333334" r="5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="175.60000000000002" cy="246.376" r="5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="328" cy="239.99200000000002" r="5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><circle cx="582" cy="119.40533333333335" r="5" fill="#118659" stroke="#ffffff" stroke-width="2"></circle><line x1="589" y1="119.40533333333335" x2="597" y2="119.40533333333335" stroke="#b9bec6"></line><text x="601" y="124.40533333333335" font-size="14" fill="#333333"><tspan>MATH-500</tspan> <tspan dx="6">48.1</tspan></text></g> <g pointer-events="none"><text x="74" y="249.98133333333334" font-size="14" fill="#333333" text-anchor="middle" font-weight="700">7.9</text> <text x="175.60000000000002" y="234.376" font-size="14" fill="#333333" text-anchor="middle" font-weight="700">12.3</text> <text x="328" y="227.99200000000002" font-size="14" fill="#333333" text-anchor="middle" font-weight="700">14.1</text></g></svg>

Additional experiment

### Raising math capability of a model that does not loop

Fixing loops, however, is not the same as making a model better at math: it lets the model finish answers it could already work out. So we also tried Gemma 3 270M, an instruction-tuned model about a third the size of Qwen3.5-0.8B, which rarely loops: only 8.5% of its answers reach its token limit, against 93% for Qwen. **Here, Astra could not improve it.** Reading Gemma’s failures, Astra found ordinary reasoning errors, such as wrong arithmetic and invalid algebraic steps, with no single component behind them to switch off. Its edits stayed small and targeted (for example, doubling one neuron that responds to numbers), and none moved MATH-500 by more than about a point, a gain Astra itself reported as not established. Editing weights could remove an obstacle that hid an ability, but it could not add an ability the model lacked. Gemma was sampled with its model card’s setting (temperature 1.0, top-k 64, top-p 0.95, up to 8,192 tokens), and its MATH-500 scores average 4 samples per problem.

| Gemma 3 270M | MATH-500 (%) |
| --- | --- |
| Base | 6.8 |
| Edited, 5 forward passes | 7.0 |
| Edited, 10 forward passes | 7.6 |
| Edited, 25 forward passes | 7.7 |
| Edited, 50 forward passes | 7.0 |

## Background and Related Works

Neural networks are hard for us to read, and hard to work with directly.

Mechanistic interpretability reads networks with tools built for the job, tracing circuits and features and editing weights

- **Zoom In: An Introduction to Circuits**   [\[link\]](https://distill.pub/2020/circuits/zoom-in)  
	C. Olah, N. Cammarata, L. Schubert, G. Goh, M. Petrov, S. Carter.  
	Distill. 2020.
- **A Mathematical Framework for Transformer Circuits**   [\[HTML\]](https://transformer-circuits.pub/2021/framework/index.html)  
	N. Elhage, N. Nanda, C. Olsson, T. Henighan, N. Joseph, B. Mann, A. Askell, Y. Bai, A. Chen, T. Conerly, N. DasSarma, D. Drain, D. Ganguli, Z. Hatfield-Dodds, D. Hernandez, A. Jones, J. Kernion, L. Lovitt, K. Ndousse, D. Amodei, T. Brown, J. Clark, J. Kaplan, S. McCandlish, C. Olah.  
	Transformer Circuits Thread. 2021.
- **Locating and Editing Factual Associations in GPT**   [\[PDF\]](http://arxiv.org/pdf/2202.05262.pdf)  
	K. Meng, D. Bau, A. Andonian, Y. Belinkov.  
	Advances in Neural Information Processing Systems (NeurIPS). 2022.

\[15, 10, 16\]

. LLMs have joined in, but mostly as models trained to read activations or weights

- **Natural Language Autoencoders Produce Unsupervised Explanations of LLM Activations**   [\[HTML\]](https://transformer-circuits.pub/2026/nla/index.html)  
	K. Fraser-Taliente, S. Kantamneni, E. Ong, D. Mossing, C. Lu, P.C. Bogdan, E. Ameisen, J. Chen, D. Kishylau, A. Pearce, J. Tarng, A. Wu, J. Wu, Y. Zhang, D.M. Ziegler, E. Hubinger, J. Batson, J. Lindsey, S. Zimmerman, S. Marks.  
	Transformer Circuits Thread. 2026.
- **Weight Oracles: Reading Neural Network Weights with Language Models**   [\[PDF\]](http://arxiv.org/pdf/2610.07334.pdf)  
	K. Kabra, C. Venhoff, C. Schroeder de Witt.  
	arXiv preprint arXiv:2610.07334. 2026.

\[17, 18\]

, or as explainers of single neurons

- **Language models can explain neurons in language models**   [\[HTML\]](https://openaipublic.blob.core.windows.net/neuron-explainer/paper/index.html)  
	S. Bills, N. Cammarata, D. Mossing, H. Tillman, L. Gao, G. Goh, I. Sutskever, J. Leike, J. Wu, W. Saunders.  
	OpenAI. 2023.
- **neuron-explorer: Steering-first neuron explorer for Qwen3.5-4B**   [\[link\]](https://github.com/lyramakesmusic/neuron-explorer)  
	.  
	GitHub repository by lyramakesmusic. 2026.

\[19, 20\]

, with benchmarks to compare them

- **WorkspaceBench: Evaluating Interpretability Methods for the Global Workspace**   [\[link\]](https://www.lesswrong.com/posts/Zeg2JztbdhguL48uH/workspacebench-evaluating-interpretability-methods-for-the)  
	C. Blank, A. Bhatia, E. Ong, N. Nanda.  
	LessWrong. 2026.

\[21\]

.

On the writing side, LLMs now run and improve training

- **autoresearch**   [\[link\]](https://github.com/karpathy/autoresearch)  
	A. Karpathy.  
	GitHub repository. 2026.
- **Reactive Optimizers**   [\[link\]](https://xingjianbai.com/reactive-optimizers/)  
	X. Bai, J. Liang, J. Teoh, V. Sitzmann.  
	Blog post. 2026.

\[6, 7\]

, and other work generates weights with models trained for it

- **Neural Network Diffusion**   [\[PDF\]](http://arxiv.org/pdf/2402.13144.pdf)  
	K. Wang, D. Tang, B. Zeng, Y. Yin, Z. Xu, Y. Zhou, Z. Zang, T. Darrell, Z. Liu, Y. You.  
	arXiv preprint arXiv:2402.13144. 2024.
- **HyperTuning: Toward Adapting Large Language Models without Back-propagation**   [\[HTML\]](https://proceedings.mlr.press/v202/phang23a.html)  
	J. Phang, Y. Mao, P. He, W. Chen.  
	International Conference on Machine Learning (ICML). 2023.
- **NeuroGen: Neural Network Parameter Generation via Large Language Models**   [\[PDF\]](http://arxiv.org/pdf/2505.12470.pdf)  
	J. Wang, Y. Zhang, X. Li.  
	arXiv preprint arXiv:2505.12470. 2025.

\[22, 23, 24\]

. Gradient-free methods still find weights by trial and error

- **Multivariate stochastic approximation using a simultaneous perturbation gradient approximation**   [\[link\]](https://doi.org/10.1109/9.119632)  
	J.C. Spall.  
	IEEE Transactions on Automatic Control, Vol 37(3), pp. 332--341. 1992.
- **Evolution Strategies as a Scalable Alternative to Reinforcement Learning**   [\[PDF\]](http://arxiv.org/pdf/1703.03864.pdf)  
	T. Salimans, J. Ho, X. Chen, S. Sidor, I. Sutskever.  
	arXiv preprint arXiv:1703.03864. 2017.
- **Fine-Tuning Language Models with Just Forward Passes**   [\[PDF\]](http://arxiv.org/pdf/2305.17333.pdf)  
	S. Malladi, T. Gao, E. Nichani, A. Damian, J.D. Lee, D. Chen, S. Arora.  
	Advances in Neural Information Processing Systems (NeurIPS). 2023.

\[25, 26, 27\]

. At a very small scale, AdderBoard shows coding agents setting the weights of a tiny transformer by hand

- **AdderBoard: A Community Challenge for Tiny Arithmetic Transformers**   [\[link\]](https://github.com/anadim/AdderBoard)  
	D. Papailiopoulos.  
	GitHub repository. 2026.

\[28\]

. Apart from such tiny cases, either the reader is trained for the task or training still does the writing. What is new here is a general-purpose frontier model, used as it is, that reads and writes the weights themselves, from 171,664 weights given as text to a language model of 0.8 billion weights with tools.

## What Comes Next?

In this blog, we demonstrated the rising capability of LLMs to read and write neural network weights (i.e., the rising concept of Weight-Space Programming). Our current results do show that capabilities are exciting but still limited, specifically due to inefficiencies in context length and harnesses. However, the current signs do show strong potential for a future involving Weight-Space Programming. We believe this marks the beginning of a dramatic shift in fields like mechanistic interpretability and neural network optimization.

This opens up radical new possibilities for LLMs to function as a translator between human language and the weight space. Here are some examples:

- **Auditing without evaluation:** This may allow us to uncover hidden problems or capabilities without ever running inference or benchmarks. Currently, capabilities and vulnerabilities can only be detected if we have test sets designed for them, or worse, after deployment in the real world. If LLMs can interpret weight space accurately, we could identify such issues directly from the weights (e.g., backdoors).
- **Dramatically reducing optimization cost:** Weight-space editing could save immense time and compute. For instance, one-shot model initialization would be far faster and more efficient than curating datasets and running full training loops.
- **Zero-data capability steering and unlearning:** Adding or unlearning a capability currently requires extensive data collection and fine-tuning. In the future, we may just prompt “Can you add Capability X to the model?” and the LLM can directly tweak some weights. Because such an edit touches only a few weights (0.016% in Experiment 8), it can leave the rest of the model intact and avoid the catastrophic forgetting that fine-tuning often causes.
- **Recursive self-improvement:** Today, recursive self-improvement is often operationalized as a model writing code that launches training jobs. An LLM that can inspect, debug, and improve its own weights, or those of a newer model, offers a richer, more native path to it.
- **True architectural and model merging:** Today, merging models relies on averaging weights, which only works for models with identical architectures. An LLM that understands the weight space could instead graft a circuit, such as a reasoning module, from one model into a completely different one, without retraining.

**We are currently building a benchmark and a harness for LLMs’ capability on Weight-Space Programming.** We believe this will provide a standardized evaluation to measure and accelerate progress in Weight-Space Programming, turning what currently seems like black magic into a rigorous, reproducible engineering discipline.

## Logs

We release the complete logs of every experiment in this post at [github.com/RikiyaT/lm\_understand-logs](https://github.com/RikiyaT/lm_understand-logs). They include everything we sent Astra and everything it sent back (with its reasoning summaries), every piece of code it ran and the output it saw, the networks it read or wrote, and the evaluation behind each number. The edited Qwen3.5-0.8B from Experiment 8 is on [Hugging Face](https://huggingface.co/RikiyaT/Qwen3.5-0.8B-weight-space-programming). We thank [Ahsen Khaliq](https://huggingface.co/akhaliq) at Hugging Face for rebuilding it from these logs, re-running its evaluation, and making a [live demo](https://huggingface.co/spaces/akhaliq/weight-space-programming-demo).

## Acknowledgements

Rikiya thanks [Jacob Li](https://jacobxli.com/) and [Akihisa Watanabe](https://akihisa-watanabe.github.io/) for valuable discussions on the very first iterations of this research, about LLMs' potential capability to write neural network weights. Rikiya also thanks [Souradip Chakraborty](https://souradip-chakraborty.github.io/), [Matei Zaharia](https://people.eecs.berkeley.edu/~matei/) and his students in [Berkeley Sky Lab](https://sky.cs.berkeley.edu/), [Heather Miller](https://heather.miller.am/) and her students at CMU, and researchers in [cmpnd](https://cmpnd.ai/) for the fruitful discussions on the earlier iterations!

Jayden thanks [Zico Kolter](https://zicokolter.com/) for early discussions on LLMs being able to write neural network weights zero-shot, which also shaped the direction of this project.

### Citation

Please cite this post as

```
Rikiya Takehi, Jayden Teoh, Alex Zhang, and Omar Khattab. “Sparks of Weight-Space Programming: LLMs can natively read & write neural network weights.” November 2026. https://rikiyat.github.io/blog/weight-space-programming/
```

or in BibTeX

```
@misc{takehi2026weightspace,
  title        = {{Sparks of Weight-Space Programming: LLMs can natively read \& write neural network weights}},
  author       = {Takehi, Rikiya and Teoh, Jayden and Zhang, Alex and Khattab, Omar},
  year         = {2026},
  month        = nov,
  howpublished = {\url{https://rikiyat.github.io/blog/weight-space-programming/}},
  note         = {Blog post}
}
```

### Footnotes

1. The Python code dataset, as a list of its files with a script that rebuilds it: [GitHub](https://github.com/RikiyaT/lm_understand-logs/tree/main/exp3_language/python_dataset).
2. The QA dataset: [GitHub](https://github.com/RikiyaT/lm_understand-logs/tree/main/exp7_sycophancy/dataset).

### References

[^1]: Large Language Models as Optimizers   [\[PDF\]](http://arxiv.org/pdf/2309.03409.pdf)  
Yang, C., Wang, X., Lu, Y., Liu, H., Le, Q.V., Zhou, D. and Chen, X., 2024. International Conference on Learning Representations (ICLR).

[^2]: DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines   [\[PDF\]](http://arxiv.org/pdf/2310.03714.pdf)  
Khattab, O., Singhvi, A., Maheshwari, P., Zhang, Z., Santhanam, K., Vardhamanan, S., Haq, S., Sharma, A., Joshi, T.T., Moazam, H., Miller, H., Zaharia, M. and Potts, C., 2024. International Conference on Learning Representations (ICLR).

[^3]: Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs   [\[PDF\]](http://arxiv.org/pdf/2406.11695.pdf)  
Opsahl-Ong, K., Ryan, M.J., Purtell, J., Broman, D., Potts, C., Zaharia, M. and Khattab, O., 2024. Conference on Empirical Methods in Natural Language Processing (EMNLP).

[^4]: GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning   [\[PDF\]](http://arxiv.org/pdf/2507.19457.pdf)  
Agrawal, L.A., Tan, S., Soylu, D., Ziems, N., Khare, R., Opsahl-Ong, K., Singhvi, A., Shandilya, H., Ryan, M.J., Jiang, M., Potts, C., Sen, K., Dimakis, A.G., Stoica, I., Klein, D., Zaharia, M. and Khattab, O., 2026. International Conference on Learning Representations (ICLR).

[^5]: Meta-Harness: End-to-End Optimization of Model Harnesses   [\[PDF\]](http://arxiv.org/pdf/2603.28052.pdf)  
Lee, Y., Nair, R., Zhang, Q., Lee, K., Khattab, O. and Finn, C., 2026. Conference on Language Modeling (COLM).

[^6]: autoresearch   [\[link\]](https://github.com/karpathy/autoresearch)  
Karpathy, A., 2026. GitHub repository.

[^7]: Reactive Optimizers   [\[link\]](https://xingjianbai.com/reactive-optimizers/)  
Bai, X., Liang, J., Teoh, J. and Sitzmann, V., 2026. Blog post.

[^8]: aozorabunko-clean: the Aozora Bunko collection of Japanese literature, cleaned and deduplicated   [\[link\]](https://huggingface.co/datasets/globis-university/aozorabunko-clean)  
2023\. Hugging Face dataset, GLOBIS University.

[^9]: Wikipedia, English, dump of November 1, 2023   [\[link\]](https://huggingface.co/datasets/wikimedia/wikipedia)  
2023\. Hugging Face dataset wikimedia/wikipedia, Wikimedia Foundation.

[^10]: A Mathematical Framework for Transformer Circuits   [\[HTML\]](https://transformer-circuits.pub/2021/framework/index.html)  
Elhage, N., Nanda, N., Olsson, C., Henighan, T., Joseph, N., Mann, B., Askell, A., Bai, Y., Chen, A., Conerly, T., DasSarma, N., Drain, D., Ganguli, D., Hatfield-Dodds, Z., Hernandez, D., Jones, A., Kernion, J., Lovitt, L., Ndousse, K., Amodei, D., Brown, T., Clark, J., Kaplan, J., McCandlish, S. and Olah, C., 2021. Transformer Circuits Thread.

[^11]: Kinetix: Investigating the Training of General Agents through Open-Ended Physics-Based Control Tasks   [\[PDF\]](http://arxiv.org/pdf/2410.23208.pdf)  
Matthews, M., Beukman, M., Lu, C. and Foerster, J., 2025. International Conference on Learning Representations (ICLR).

[^12]: MinAtar: An Atari-Inspired Testbed for Thorough and Reproducible Reinforcement Learning Experiments   [\[PDF\]](http://arxiv.org/pdf/1903.03176.pdf)  
Young, K. and Tian, T., 2019. arXiv preprint arXiv:1903.03176.

[^13]: Wait, Wait, Wait... Why Do Reasoning Models Loop?  [\[PDF\]](http://arxiv.org/pdf/2512.12895.pdf)  
Pipis, C., Garg, S., Kontonis, V., Shrivastava, V., Krishnamurthy, A. and Papailiopoulos, D., 2025. arXiv preprint arXiv:2512.12895.

[^14]: Refusal in Language Models Is Mediated by a Single Direction   [\[PDF\]](http://arxiv.org/pdf/2406.11717.pdf)  
Arditi, A., Obeso, O., Syed, A., Paleka, D., Panickssery, N., Gurnee, W. and Nanda, N., 2024. arXiv preprint arXiv:2406.11717.

[^15]: Zoom In: An Introduction to Circuits   [\[link\]](https://distill.pub/2020/circuits/zoom-in)  
Olah, C., Cammarata, N., Schubert, L., Goh, G., Petrov, M. and Carter, S., 2020. Distill.

[^16]: Locating and Editing Factual Associations in GPT   [\[PDF\]](http://arxiv.org/pdf/2202.05262.pdf)  
Meng, K., Bau, D., Andonian, A. and Belinkov, Y., 2022. Advances in Neural Information Processing Systems (NeurIPS).

[^17]: Natural Language Autoencoders Produce Unsupervised Explanations of LLM Activations   [\[HTML\]](https://transformer-circuits.pub/2026/nla/index.html)  
Fraser-Taliente, K., Kantamneni, S., Ong, E., Mossing, D., Lu, C., Bogdan, P.C., Ameisen, E., Chen, J., Kishylau, D., Pearce, A., Tarng, J., Wu, A., Wu, J., Zhang, Y., Ziegler, D.M., Hubinger, E., Batson, J., Lindsey, J., Zimmerman, S. and Marks, S., 2026. Transformer Circuits Thread.

[^18]: Weight Oracles: Reading Neural Network Weights with Language Models   [\[PDF\]](http://arxiv.org/pdf/2610.07334.pdf)  
Kabra, K., Venhoff, C. and Schroeder de Witt, C., 2026. arXiv preprint arXiv:2610.07334.

[^19]: Language models can explain neurons in language models   [\[HTML\]](https://openaipublic.blob.core.windows.net/neuron-explainer/paper/index.html)  
Bills, S., Cammarata, N., Mossing, D., Tillman, H., Gao, L., Goh, G., Sutskever, I., Leike, J., Wu, J. and Saunders, W., 2023. OpenAI.

[^20]: neuron-explorer: Steering-first neuron explorer for Qwen3.5-4B   [\[link\]](https://github.com/lyramakesmusic/neuron-explorer)  
2026\. GitHub repository by lyramakesmusic.

[^21]: WorkspaceBench: Evaluating Interpretability Methods for the Global Workspace   [\[link\]](https://www.lesswrong.com/posts/Zeg2JztbdhguL48uH/workspacebench-evaluating-interpretability-methods-for-the)  
Blank, C., Bhatia, A., Ong, E. and Nanda, N., 2026. LessWrong.

[^22]: Neural Network Diffusion   [\[PDF\]](http://arxiv.org/pdf/2402.13144.pdf)  
Wang, K., Tang, D., Zeng, B., Yin, Y., Xu, Z., Zhou, Y., Zang, Z., Darrell, T., Liu, Z. and You, Y., 2024. arXiv preprint arXiv:2402.13144.

[^23]: HyperTuning: Toward Adapting Large Language Models without Back-propagation   [\[HTML\]](https://proceedings.mlr.press/v202/phang23a.html)  
Phang, J., Mao, Y., He, P. and Chen, W., 2023. International Conference on Machine Learning (ICML).

[^24]: NeuroGen: Neural Network Parameter Generation via Large Language Models   [\[PDF\]](http://arxiv.org/pdf/2505.12470.pdf)  
Wang, J., Zhang, Y. and Li, X., 2025. arXiv preprint arXiv:2505.12470.

[^25]: Multivariate stochastic approximation using a simultaneous perturbation gradient approximation   [\[link\]](https://doi.org/10.1109/9.119632)  
Spall, J.C., 1992. IEEE Transactions on Automatic Control, Vol 37(3), pp. 332--341.

[^26]: Evolution Strategies as a Scalable Alternative to Reinforcement Learning   [\[PDF\]](http://arxiv.org/pdf/1703.03864.pdf)  
Salimans, T., Ho, J., Chen, X., Sidor, S. and Sutskever, I., 2017. arXiv preprint arXiv:1703.03864.

[^27]: Fine-Tuning Language Models with Just Forward Passes   [\[PDF\]](http://arxiv.org/pdf/2305.17333.pdf)  
Malladi, S., Gao, T., Nichani, E., Damian, A., Lee, J.D., Chen, D. and Arora, S., 2023. Advances in Neural Information Processing Systems (NeurIPS).

[^28]: AdderBoard: A Community Challenge for Tiny Arithmetic Transformers   [\[link\]](https://github.com/anadim/AdderBoard)  
Papailiopoulos, D., 2026. GitHub repository.