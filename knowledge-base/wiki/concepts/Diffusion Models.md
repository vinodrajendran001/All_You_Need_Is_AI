---
type: concept
created: 2026-06-23
updated: 2026-10-19
tags:
  - concept
  - diffusion
  - generative-models
  - image-generation
  - multimodal
source_ids:
  - src-2026-05-18-pocketflow-tutorial-docs
  - src-2026-06-02-ycombinator-yc-paper-club-inference-diffusion-world-models
  - src-2026-06-23-mayank-pratap-singh-diffusion-visual-breakdown
  - src-2026-08-31-docmilanfar-lagrangian-flow-matching
  - src-2026-10-19-alphasignal-next-concept-modeling
status: active
---

# Diffusion Models

## Definition

Diffusion models are generative models that learn to create data by reversing a gradual noising process. During training, clean examples are corrupted with known noise at different timesteps; a neural network learns how to predict the noise or denoising direction. During sampling, the model starts from simple noise and repeatedly applies learned corrections until a structured sample emerges.

## Why it matters

Diffusion is one of the dominant paradigms for image and video generation. It matters because it trades unstable one-shot generation for a stable supervised denoising objective. The cost is iterative sampling: high-quality generation may require many network evaluations unless faster samplers, distillation, consistency-style models, or flow-based formulations reduce the number of steps.

## Current synthesis

### From GANs and VAEs to diffusion

[[Mayank Pratap Singh - Diffusion Model Visual Breakdown]] frames diffusion as a response to older generator tradeoffs:

- **GANs** produce sharp samples but rely on a two-network adversarial game that can become unstable or mode-collapse.
- **VAEs** introduce compressed latent spaces but often produce overly smooth samples when reconstruction objectives average over visual detail.
- **Diffusion** defines a known corruption process and trains against exact noise targets, removing the moving-discriminator target from the core training loop.

The VAE connection survives strongly in modern **latent diffusion**: an autoencoder compresses the image, diffusion happens in the smaller latent tensor, and a decoder turns the denoised latent back into pixels.

### The forward process

The forward process is defined by the training code. At timestep `t`, a clean example `x_0` is mixed with Gaussian noise:

```math
x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon,
\quad \epsilon \sim \mathcal{N}(0, I)
```

`β_t` controls how much new noise is added at a step, `α_t = 1 - β_t` is the retained signal at that step, and `\bar{α}_t` is cumulative signal retention. This one-step sampling equation is the practical reason DDPM-style training can create many supervised denoising examples from each clean image.

### What the denoiser learns

The denoiser receives the noisy sample, the timestep, and optional conditioning:

```math
\epsilon_\theta(x_t, t, c)
```

In the simplest view, it predicts the noise that was added. The loss compares the true sampled noise with the predicted noise. At low noise levels, the model learns local cleanup; at high noise levels, the model must infer broad plausible structure from weak evidence and conditioning.

The timestep is not incidental. The same network needs to know whether it is cleaning small residual noise or making large semantic corrections. Timestep embeddings give the denoiser this noise-level awareness.

### Denoiser architecture

Classic image diffusion uses **U-Nets** because denoising needs both global context and local precision. Downsampling paths build broad context, upsampling paths reconstruct detail, and skip connections preserve high-resolution information. Attention layers can let distant image regions influence one another.

Modern systems increasingly use **diffusion transformers**. A latent tensor is split into patches, projected into tokens, combined with timestep and conditioning information, and processed by transformer blocks. DiT, PixArt-alpha, MM-DiT, and Stable Diffusion 3-style architectures show this shift from convolutional U-Net denoisers toward scalable token-based denoisers.

### Conditioning and guidance

Conditioning turns diffusion from "sample from the data distribution" into "sample something matching this input." Conditions can include:

- class labels;
- text prompts;
- masks;
- edge maps;
- depth maps;
- pose skeletons;
- low-resolution images;
- other images.

Text-to-image systems usually encode the prompt with a text encoder and inject embeddings through cross-attention or transformer conditioning. Classifier-free guidance compares conditional and unconditional predictions during sampling:

```math
\hat{\epsilon} =
\epsilon_\theta(x_t, t, \emptyset)
+ s(\epsilon_\theta(x_t, t, c) - \epsilon_\theta(x_t, t, \emptyset))
```

The guidance scale `s` is a steering knob. Higher values can strengthen prompt adherence but may reduce diversity, exaggerate textures, or create artifacts.

### Relationship to world models

[[Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club]] and [[World Models]] connect diffusion to control and embodied intelligence. Diffusion can serve as a renderer or trajectory generator, and video diffusion ideas can be pulled into model predictive control. The key distinction: diffusion is a generative-path mechanism; a world model is a predictive model of environment dynamics. Diffusion can implement parts of a world-model system, but the concepts are not identical.

## Path geometry is an intuition, not a universal step-count formula

[[@docmilanfar - A Lagrangian View of Flow Matching]] proposes a particle-centric explanation:
changing denoiser predictions can complicate numerical integration. The useful question is how
path geometry and target variation affect sampling cost.

The earlier version of this page went further than the mathematics supports. The identity
`partial_t f + J_f v = 0` transports a constant label along a chosen flow; it does not require
straight trajectories. A rotation is a counterexample. Likewise, additive Gaussian corruption
does not imply exploding posterior covariance: the denoiser Jacobian includes a noise-scale
factor, and a Gaussian-prior example has shrinking covariance and a bounded Jacobian.

[[Flow Matching]] separates conditional training paths, learned trajectories, and numerical
solver choices. Reflow may help low-step sampling, but the source does not establish inevitable
path intersections, zero uncertainty after reflow, or a quality-independent step-count rule.
Its **Jacobian Penalty** is a proposed framing, not an experimentally validated universal law.

## Diffusion for text is now a baseline to beat

The vault's diffusion material so far concerns images, video, and control.
[[Alpha Signal - How Next-Concept Modeling Rethinks AI Text Generation]] adds the first reference
point for **diffusion language models (DLMs)**. Instead of predicting tokens left to right, they
work on whole blocks of text and refine the output over successive steps. The article contrasts
this with autoregressive decoding, which cannot revise a token once it has been emitted.

The article lists three costs that echo this page's step-count discussion. DLMs often need many
sampling steps for good quality. They process the full output sequence at every step. Strong
models can require large training budgets, often with repeated passes over the same data.

Stanford's **Next-Concept Modeling** is reported as a response to those costs. It refines
hierarchical **discrete codes** from coarse to fine, so earlier levels are short and each level's
codes are predicted in parallel. At comparable scale, with generators of roughly **100 million
parameters**, the capture reports **10–31×** faster generation than strong DLM baselines at
comparable or better quality, and **4–5×** fewer training tokens in selected benchmarks.

These are secondhand research results from an unnamed paper. They concern text generation at
small scale. They do not test image or video diffusion, and they do not establish that diffusion
is inferior for text at larger scales. The reported speed ratios are against diffusion
baselines, not against autoregressive decoding.

## Open questions

- How far can fast samplers, distillation, consistency models, flow matching, or rectified flow reduce sampling cost without losing quality?
- When should systems use pixel-space diffusion, latent diffusion, or transformer-based latent diffusion?
- How should conditioning be designed when text is too vague and structured control signals are needed?
- Can diffusion-based renderers support physically accurate simulation, or will they remain strongest at visual plausibility?
- How should the vault split image diffusion, video diffusion, audio diffusion, and diffusion for control into separate pages as sources accumulate?
- Do diffusion language models keep a quality or revision advantage over coarse-to-fine code
  hierarchies once both are scaled well beyond the roughly 100M-parameter comparisons recorded here?

## Related pages

- [[Alpha Signal - How Next-Concept Modeling Rethinks AI Text Generation]]
- [[LLM Inference]]

- [[Mayank Pratap Singh - Diffusion Model Visual Breakdown]]
- [[World Models]]
- [[LLM Training Pipeline]]
- [[Neural Network Fundamentals]]
- [[Vision-Language Grounding]]
- [[Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club]]
- [[The Pocket - PocketFlow Tutorial Docs]]
- [[AI Knowledge Base Overview]]
- [[Flow Matching]]
- [[@docmilanfar - A Lagrangian View of Flow Matching]]
- [[@docmilanfar]]
- [[Knowledge Distillation]]
