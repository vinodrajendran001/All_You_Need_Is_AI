---
title: "Build World Models for Interactive Simulation with NVIDIA Cosmos"
source: "https://developer.nvidia.com/blog/build-world-models-for-interactive-simulation-with-nvidia-cosmos/?utm_source=tldrai"
author:
  - "[[Elizabeth Goodman]]"
published: 2026-11-03
created: 2026-11-04
description: "Physical AI developers working with world models face two distinct challenges: adapting models to their sensors, tasks, and data, and getting those models into…"
tags:
  - "clippings"
---
Physical AI developers working with [world models](https://www.nvidia.com/en-us/glossary/world-models/) face two distinct challenges: adapting models to their sensors, tasks, and data, and getting those models into applications reliably.

[NVIDIA Cosmos](https://www.nvidia.com/en-us/ai/cosmos/) addresses each. Cosmos is a platform of world foundation models and development tools for [physical AI](https://www.nvidia.com/en-us/glossary/generative-physical-ai/). [Cosmos Framework](https://github.com/NVIDIA/cosmos-framework) provides agent skills and recipes for world model training, multimodal data processing, optimization and inference. [Cosmos NIM microservices](https://build.nvidia.com/models?q=cosmos) supports GPU-accelerated serving through application APIs.

This post walks through both. The simulation section shows how to use Cosmos Framework’s inference recipes and agent skills to generate synchronized camera video and LiDAR observations for AV, robot, and surgical scenarios, starting from released checkpoints you can run today. The deployment section shows how to choose a NIM configuration for your GPU, launch the container, verify readiness, and send your first inference request.

## When to use Cosmos Framework for world model development

[Cosmos Framework](https://github.com/NVIDIA/cosmos-framework) is an open and fully modular framework for world model training, model optimization, and inference to support a full model development lifecycle using new agent skills. It is expanding beyond Cosmos 3 to support [NVIDIA Alpamayo](https://github.com/NVlabs/alpamayo-recipes), GR00T, Qwen, pi0.5, and other compatible Hugging Face models.

**Training**

- Train models on text, images, video, audio, and actions faster using new skills.
- Use LoRA for parameter-efficient adaptation, or full supervised fine-tuning (SFT) to update all model parameters.
- Load data through JSONL, WebDataset, LeRobot, or custom adapters and train across GPUs and save checkpoints to resume runs.
- Point your agent to post-training [skill](https://github.com/NVIDIA/cosmos-framework/tree/main/.agents/skills/cosmos3-post-training) to accelerate and automate.

**Apply Reinforcement Learning**

- The platform now covers [online and offline RL paths](https://github.com/NVIDIA/cosmos-framework/blob/main/docs/posttrain/howto/run-posttrain.md). Newly supported pipelines include:
	- DPO: offline preference optimization.
		- GRPO: online RL with a rule or model reward and vLLM rollouts.
		- PPO: actor-critic RL with frozen reference and critic, including RL for embodied policies in simulation.
		- OPD: on-policy distillation from a frozen teacher.
		- DiffusionNFT: online RL for diffusion world models.
- Run rollout, reward, and training roles on shared GPUs or separate pools.
- Connect supported simulators to collect experience.

**Optimize models and inference**

- Distill models to reduce model size or generation steps; quantize models to reduce memory use.
- Run compatible checkpoints with Hugging Face Diffusers, PyTorch, SGLang, vLLM-Omni, vLLM, TRT-LLM and TRT-Edge-LLM or NVIDIA NIM.
- Evaluate for quality, accuracy and GPU usage and maximize compute utilization.

**Use agents with Cosmos Framework**

Load the setup, inference, post-training, and troubleshooting skills under `.agents/skills`. Give the agent a bounded task:

***Prompt****: Post-train* *`<checkpoint>`* *on* *`<dataset>`* *using* *`<recipe>`**. Pin all revisions, validate the dataset, and keep training and evaluation episodes separate. Run the smoke test, save the configuration, and stop at* *`<N>`* *GPU-hours. Export and compare against the base model on held-out data using three seeds. Repeat evaluation at a supported lower precision; record quality, peak memory, and latency.*

## Which Cosmos simulation workflow should you use?

Cosmos Framework provides post-training and inference recipes for robot simulation, realistic scene generation, multi-camera driving simulation, and surgical policy evaluation. New Cosmos 3 Nano simulation recipes and example checkpoints enable developers to use agent runnable skills to evaluate our example checkpoints and adapt Cosmos 3 Nano to custom sensors, action space, and data domains.

These checkpoints support PyTorch and vLLM-Omni, tested on NVIDIA Hopper and Blackwell GPUs. Use the recipe to select GPU count, memory configuration, and inference settings.

**Autonomous vehicle simulation:**

Both AV checkpoints take a prompt and World Scenario Map (WSM) controls representing lanes, objects, road markings, traffic signs, and road boundaries. Joint RGB–LiDAR generation additionally uses HD-map rangemap controls and supports optional initial LiDAR observations. Prompts describe weather, lighting, time of day, road conditions with prefixes providing camera-rig and field-of-view context. An optional initial camera images provide visual context to guide the generated scene’s appearance.

[Cosmos3-Nano-Transfer-Auto](https://huggingface.co/nvidia/Cosmos3-Nano-Transfer-Auto) uses bidirectional generation to denoise an entire multi-view clip at once for offline [synthetic data generation](https://www.nvidia.com/en-us/glossary/synthetic-data-generation/). It supports 30 fps input and output video, with up to 400 frames at 480p or 720p; longer sequences can be generated through autoregressive chunking. Change the prompt to turn a daytime drive into a rainy night while keeping the same road layout and vehicle trajectories. Use these variations to train and evaluate perception and driving models across weather and lighting conditions.

After Framework setup, run the four-GPU examples below from the repository root. For Transfer-Auto, use the [published sample configuration](https://huggingface.co/nvidia/Cosmos3-Nano-Transfer-Auto/blob/main/assets/sample_data/input-transfer-auto.jsonl) with seven synchronized WSM videos, per-camera captions, first-frame RGB conditioning, and HD-map LiDAR controls. See the [Transfer-Auto inference guide](https://github.com/NVIDIA/cosmos-framework/blob/main/docs/inference_auto.md) for setup, input preparation, and output details.

```bash
exportCOSMOS_TRAINING=0 COSMOS_INTERNAL=0
 
hf download nvidia/Cosmos3-Nano-Transfer-Auto\
  --local-dircheckpoints/Cosmos3-Nano-Transfer-Auto
 
AUTO_SAMPLE_ROOT="$PWD/checkpoints/Cosmos3-Nano-Transfer-Auto/assets/sample_data"
AUTO_NEGATIVE_PROMPT="$(cat .agents/skills/cosmos3-nano-transfer-auto/inference/assets/negative-prompt.txt)"
 
torchrun --standalone --nproc-per-node=4 \
  -m cosmos_framework.scripts.inference \
  -i "$AUTO_SAMPLE_ROOT/input-transfer-auto.jsonl"\
  -o outputs/transfer_auto\
  --checkpoint-path checkpoints/Cosmos3-Nano-Transfer-Auto\
  --resolution 720 --num-steps 35 \
  --per-view-negative-prompt "$AUTO_NEGATIVE_PROMPT"\
  --cp-size 4 --cfgp-size 1 \
  --no-use-torch-compile --no-diffusion-cache
```

The reference run produces seven 720p videos (297 frames at 30 FPS) and 99 LiDAR sweeps. Check `sample_outputs.json` for success and `lidar.safetensors` for finite range and intensity values, then verify WSM alignment and consistency across camera views and LiDAR.

For custom scenarios and rig adaptation, see [the WSM renderer](https://github.com/NVIDIA/cosmos-framework/blob/main/.agents/skills/cookbooks/cosmos3/simulation/auto/wsm/README.md) and [Transfer-Auto post-training guides](https://github.com/NVIDIA/cosmos-framework/blob/main/docs/training_transfer_auto.md). For point-cloud conversion and visualization, see the [LiDAR visualization utilities](https://github.com/NVIDIA/cosmos-framework/blob/main/.agents/skills/cookbooks/cosmos3/simulation/auto/helpers/lidar_visualization.py)

<video controls="" src="https://developer.download.nvidia.com/devblogs/mads94-093-i2v-surround-grid-v5-master.mp4"></video>

Video 1. Surround-view video and LiDAR generation with Cosmos3-Nano-Transfer-Auto

[Cosmos3-Nano-Sim-Auto](https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Auto) is the causal, few-step-distilled variant of Cosmos3-Nano-Transfer-Auto, enabling autoregressive streaming generation. It generates observations incrementally as an AV policy or human driving input updates the scenario through a WSM renderer. Generated camera and LiDAR observations return to the policy, enabling closed-loop evaluation

For Sim-Auto, reproduce the reference rollout using the [published Sim-Auto sample checkpoint](https://huggingface.co/nvidia/Cosmos3-Nano-Transfer-Auto/blob/main/assets/sample_data/input-sim-auto.jsonl) and pre-rendered WSM controls to generate synchronized camera videos and LiDAR observations autoregressively. See the [Sim-Auto inference guide](https://github.com/NVIDIA/cosmos-framework/blob/main/docs/inference_sim_auto.md) for setup, input configuration, and output details.

![A policy model (e.g., Alpamayo) or user sends an action to the AlpaSim simulation runtime. AlpaSim updates the simulation state and forwards the context to Cosmos3-Nano-Sim-Auto, which synthesizes the next camera frames and returns them to the policy, completing the loop.](https://developer-blogs.nvidia.com/wp-content/uploads/2026/10/image1-15.webp)

Figure 1. Cosmos closed-loop simulation workflow

```bash
exportCOSMOS_TRAINING=0 COSMOS_INTERNAL=0
 
hf download nvidia/Cosmos3-Nano-Sim-Auto\
  --local-dircheckpoints/Cosmos3-Nano-Sim-Auto
 
hf download nvidia/Cosmos3-Nano-Transfer-Auto\
  --include 'assets/sample_data/*'\
  --local-dircheckpoints/Cosmos3-Nano-Transfer-Auto
 
AUTO_SAMPLE_ROOT="$PWD/checkpoints/Cosmos3-Nano-Transfer-Auto/assets/sample_data"
 
torchrun --standalone --nproc-per-node=4 \
  -m cosmos_framework.scripts.inference \
  -i "$AUTO_SAMPLE_ROOT/input-sim-auto.jsonl"\
  -o outputs/sim_auto\
  --checkpoint-path checkpoints/Cosmos3-Nano-Sim-Auto\
  --cp-size 4 --cfgp-size 1 \
  --no-use-torch-compile --no-diffusion-cache
```

For human-controlled rollouts, see [Sim-Auto Interactive Drive](https://flashdreams.org/main/models/cosmos3_nano_sim_auto/).

The Sim-Auto reference run writes to `outputs/sim_auto/daytime_scene/`. Apply the same output checks described above for Transfer-Auto.

<video controls="" src="https://developer.download.nvidia.com/devblogs/transfer-layout-under60mb.mp4"></video>

Video 2. Multi-view video and LiDAR generation with Cosmos3-Nano-Sim-Auto

**Robotics Simulation:**

[Cosmos3-Nano-Sim-Transfer](https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Transfer) converts depth video and a prompt into RGB video with varied lighting, textures, and backgrounds while preserving geometry and motion. For robot demonstrations, it changes the third-person view while retaining actions, states, and wrist-camera recordings.

<video controls="" src="https://developer.download.nvidia.com/devblogs/transfer-depth-grid.mp4"></video>

*Video 3. Turn depth, segmentation, edges, or blurred video into detailed RGB observations, using language prompts while the simulator maintains physical state*

[Cosmos3-Nano-Sim-Bimanual](https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Bimanual) generates the next visual observation from the scene and robot actions. It supports interactive two-arm simulation for YAM and AgiBot embodiments, controlled by a policy or human-operated joysticks.

Here, Sim-Transfer generates visuals from a physics simulator’s updated state; Sim-Bimanual generates the next observation directly from the scene and robot actions.

**Surgical Simulation:**

Surgical environments are among the most challenging for classical simulators due to their complex multi-physics nature. Generative simulation offers a complementary approach: rather than explicitly modeling scene geometry, tissue deformation, and physical interactions, world foundation models learn visual dynamics directly from synchronized surgical video and robot kinematics.

**Cosmos3-H-Embodied-Nano**, built on Cosmos3 and post-trained on Open-H-Embodiment, generates surgical video from robot actions, predicts actions from video, or generates both together. It takes an initial RGB frame, a task prompt, the last 16 executed actions, and subsequent robot actions. Developers can use it to generate synthetic data and evaluate policies offline without building a physics model of the surgical scene.

**Cosmos3-H-Dreams** lets developers test how a surgical policy responds as a procedure unfolds, with each action shaping what happens next. Distilled from Cosmos3-H-Embodied-Nano, this causal, few-step model generates frames from live robot kinematics for real-time, closed-loop simulation controlled by a human or learned policy. This gives developers an interactive environment to explore surgical maneuvers and evaluate policies before testing on physical hardware.

## When to use Cosmos NIM for accelerated inference

Alongside the open inference tools, the new Cosmos NIM package supported models in optimized containers for accelerated inference, making Cosmos models easy to deploy.

- **Faster inference, less memory**: Accelerate inference through quantization, speculative decoding, caching, token pruning, and KV-cache-aware routing. Speculative decoding delivers measured mean speedups of roughly 2–3× on H200.
- **Custom models and live video understanding**: Serve fine-tuned Cosmos checkpoints and process live streams with streaming VLM inference, enabling sub-second alerts with 10x lower latency for faster event response.
- **Simpler production deployment**: Automatic configuration selection, validated performance and quality across supported GPUs, licensing support, and quarterly feature, optimization, and security updates**.**

**GPU memory requirements**

<table><thead><tr><th rowspan="2">Capability</th><th rowspan="2">Model</th><th colspan="3">Required GPU VRAM [GiB]</th></tr><tr><th>BF16</th><th>FP8</th><th>FP8 + offloading</th></tr></thead><tbody><tr><th rowspan="3">Reasoning</th><td>Cosmos3-Edge</td><td>16</td><td>14.5</td><td>–</td></tr><tr><td>Cosmos3-Nano</td><td>23.1</td><td>23.1</td><td>–</td></tr><tr><td>Cosmos3-Super</td><td>135</td><td>67</td><td>–</td></tr><tr><th rowspan="3">Generation</th><td>Cosmos3-Edge-DROID</td><td>14</td><td>–</td><td>–</td></tr><tr><td>Cosmos3-Nano</td><td>58</td><td>44</td><td>31</td></tr><tr><td>Cosmos3-Super</td><td>150</td><td>93</td><td>38</td></tr></tbody></table>

*Table 1. GPU memory requirements per model per task*

**How to Launch Cosmos NIM**

Choose a GPU and model configuration using the tables above, and follow the [deployment guide](https://github.com/NVIDIA/cosmos/blob/c8353e18c607a1917eb1103557b5029060807bba/cookbooks/cosmos3/nim/deployment.md) to install the required NVIDIA driver, Docker, and NVIDIA Container Toolkit on Linux. Sign in to [NGC API Keys](https://org.ngc.nvidia.com/setup/api-keys), select **Generate Personal Key**, and enable **NGC Catalog** access. Set the key in your terminal as `NGC_API_KEY`:

```python
export NGC_API_KEY='paste-your-key-here'
```

The following commands launch Nano Generator on GPU 0. Ensure curl and python3 are installed and sufficient disk space is available for the image and model cache. The cache permissions shown are for local development.

```python
: "${NGC_API_KEY:?Export your NGC API key first}"
printf '%s'"$NGC_API_KEY"| docker login nvcr.io \
 --username '$oauthtoken'--password-stdin
 
export NIM_IMAGE='nvcr.io/nim/nvidia/cosmos3:2.0.0'
export LOCAL_NIM_CACHE="$HOME/.cache/nim/cosmos3"
mkdir -p "$LOCAL_NIM_CACHE"
chmod a+rwX "$LOCAL_NIM_CACHE"
 
docker run -d --name cosmos3-generator \
 --gpus '"device=0"'\
 --shm-size 16g\
 --ulimit memlock=-1\
 --ulimit stack=67108864\
 --ulimit nofile=65536:65536\
 -p 8000:8000\
 -e NGC_API_KEY \
 -e NIM_MODEL_TYPE=generator \
 -e NIM_MODEL_VARIANT=nano \
 -e NIM_PERF_PROFILE=latency \
 -v "$LOCAL_NIM_CACHE:/opt/nim/.cache"\
 "$NIM_IMAGE"
```

Wait for readiness (~few minutes), then inspect the selected model and profile:

```python
curl -fsS http://localhost:8000/v1/health/ready
curl -fsS http://localhost:8000/v1/metadata | python3 -m json.tool
```

To inspect startup progress, run `docker logs -f cosmos3-generator` in another terminal. Now you are ready to generate.

**Choose latency or throughput:**

- latency(default)**:** Prioritizes finishing one request sooner. Choose it for interactive experimentation; supported multi-GPU configurations use GPUs together on a request.
- throughput**:** Prioritizes completing more requests over time. Choose it for dataset generation or concurrent users; independent replicas process requests in parallel.

Set `NIM_PERF_PROFILE` at container launch. These settings apply to Generator; throughput benefits require concurrent requests. Latency supports 1, 2, 4, or 8 GPUs, while throughput requires 2, 4, or 8 compatible GPUs. Changing only `NIM_PERF_PROFILE` to throughput in the single-GPU example will fail profile selection.

## Get started

Explore [Cosmos Framework](https://github.com/NVIDIA/cosmos-framework) and use its agent skills and reference recipes to train, customize, and optimize models for your application. Start with a simulation checkpoint that matches your task, reproduce the reference workflow, and adapt it to your sensors, actions, and data.

Read the full [technical report](https://research.nvidia.com/labs/cosmos-lab/cosmos-simulation/technical-report.pdf).

Join us on [Thursday, Nov. 5](https://www.youtube.com/watch?v=8lNoGg_j8S8), for a livestream on how to use Cosmos Framework.

Deploy Cosmos models for reasoning and generation using New Certified Cosmos NIM for best performance on 20+ NVIDIA GPUs.