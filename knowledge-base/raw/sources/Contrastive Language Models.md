---
title: "Contrastive Language Models"
source: "https://contrastive-lm.notion.site/"
author:
published:
created: 2026-09-28
description: "LLM-as-a-Verifier: A General-Purpose Verification Framework"
tags:
  - "clippings"
---
![Page icon](https://contrastive-lm.notion.site/image/attachment%3Af7afed14-3798-4c83-9d93-883a6d93a05e%3A3de31e69-04cd-46f6-ac9f-d448fc2ae48c.png?id=3e466c3c-12a8-801f-9279-f8c0ba3c98f3&table=block&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=250&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

> A System One Model for Fast and Generalizable Decision-Making

[Jacky Kwok](https://jackyk02.github.io/) $^{\dagger}$, [Hangoo Kang](https://hgkang02.github.io/), [Tarun Suresh](https://tarsur909.github.io/), [Jon Saad-Falcon](https://jonsaadfalcon.com/), [Marco Pavone](https://research.nvidia.com/person/marco-pavone)

[Christopher Ré](https://cs.stanford.edu/~chrismre/), [Azalia Mirhoseini](https://azaliamirhoseini.com/) Stanford University NVIDIA Research

 $^{\dagger}$ Project Lead

Posted: Sep 23, 2026

##### New Architecture, Data Recipe, and Scaling Laws

We introduce Contrastive Language Models (CLMs), a new class of System One model trained with a contrastive learning objective that connects states and actions.

We release CLM-8B, which is pre-trained on 60M Nemotron Q&A pairs, mid-trained on 30M synthetic hard negatives, and post-trained on 1M agentic trajectories.

CLM-8B delivers performance comparable to Jev across computer-use, gaming, and tool-calling tasks, while achieving up to 9× lower latency. When fine-tuned as a trajectory reward model, CLM also sets a new SOTA on challenging agentic coding benchmarks, including [DeepSWE](https://deepswe.datacurve.ai/) (81.6%) and [Terminal Bench 2.1](https://www.tbench.ai/?version=2.1) (87.6%).

We build an ultra-efficient training and serving infra for CLM by disaggregating states and actions, allowing their embeddings to be cached and reused independently.

We establish scaling laws for CLMs and show that the test contrastive loss decreases predictably as a power law in training compute, model size, and dataset size.

Try [CLM on GitHub](https://github.com/Contrastive-LM/CLM):

![](https://contrastive-lm.notion.site/image/attachment%3Ac814f420-daca-404b-ba0d-4aa08390e190%3Agit.png?table=block&id=3e466c3c-12a8-8093-bfe3-d4a7f6b19080&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=540&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

### Overview

![](https://contrastive-lm.notion.site/image/attachment%3A236bfbeb-eaf6-4d54-bdec-7a6daa0d881a%3Aimage.png?table=block&id=3e466c3c-12a8-8023-bfeb-f6912555a98b&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=1500&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

CLM first trains a state encoder and an action encoder on a large-scale dataset with a contrastive objective (InfoNCE), so that each state is pulled toward the ground truth action that was taken and pushed away from all others. The two encoders then serve directly as a zero-shot action classifier.

At deployment, given the current state and a set of candidate actions, CLM scores each action by how well its embedding aligns with the state embedding and selects the highest-scoring action.

##### Dino Run (CLM vs. Jev)

![](https://file.notion.so/f/f/59b4b732-2399-4ed0-b86b-b5dd420bb513/83e15cea-6c39-49c2-8289-edfc5227a685/clm_game_race.gif?table=block&id=3e466c3c-12a8-80c2-9d66-d406e80a9ed3&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&expirationTimestamp=1790582400000&signature=2-PxhB23cqf4hsfqnKGveTQm85gfvWVHE88zTsZSJlY)

Super Mario Demo

WikiRacing Demo

### Zero-shot Evaluation

![](https://contrastive-lm.notion.site/image/attachment%3A0f30b6a6-7aaa-42bb-97b4-2a32d439f0c8%3A5.png?table=block&id=3e466c3c-12a8-804e-ab84-f922a0dbb65c&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=1700&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

Across computer-use, gaming, and tool-calling tasks, CLM-8B performs on par with Jev while running up to 9× faster. The speedups are most pronounced when the number of candidate actions is large (e.g., WikiRacing) or when actions can be frequently reused across states (e.g., T-Rex Game).

### Agentic Benchmarks

![](https://contrastive-lm.notion.site/image/attachment%3Af80107f6-9401-457a-b4e3-b7f19c65fbaa%3Aa7e072a8-a2c1-4f31-9c10-1ab9771b4c69.png?table=block&id=3e466c3c-12a8-8085-b32e-f66cddc31141&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=1600&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

We find that Jev fails to serve as a verifier for long-horizon tasks, performing below the random-selection (Pass@1) baseline. In contrast, with lightweight fine-tuning, CLM achieves SOTA performance on challenging agentic benchmarks, including DeepSWE (81.6%) and Terminal-Bench 2.1 (87.6%), while delivering 4–6× faster inference than Jev.

For each task, we sample multiple candidate solutions using Opus 5 for DeepSWE and Fable 5 for Terminal-Bench 2.1. CLM or Jev then serves as the verifier, selecting the best solution from the candidate set. We evaluate performance on 38 held-out DeepSWE tasks and 30 held-out Terminal-Bench 2.1 tasks. Latency is measured on an H100 GPU.

### Model Architecture

A CLM consists of a state encoder and an action encoder, as illustrated in Figure 1. Both encoders map their respective inputs into a shared embedding space, where the score of a state–action pair is computed as the cosine similarity between their embeddings.

![](https://contrastive-lm.notion.site/image/attachment%3Adda173a5-6d73-440b-aa70-a430bc3c8048%3Aimage.png?table=block&id=3e466c3c-12a8-806a-9f5a-c4b23634f324&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=1500&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

Each encoder consists of a frozen LLM backbone followed by a trainable projection head. We take the hidden state of the final token, normalize it, and pass it through a MLP projection head. Only the 20M-parameter projection head is trained; the LLM remains frozen and never receives gradients. This design makes our scaling experiments inexpensive to run. We precompute the LLM embeddings once, then reuse them to train projection heads across different setups. A full pre-training run on the Nemotron DQA dataset takes about an hour on a single RTX 4090 GPU.

Most importantly, since states and actions are disaggregated, their embeddings can be cached independently. In settings where the state evolves continuously (e.g., Super Mario) while the action set remains fixed, we only need to recompute the state embedding at each step and can reuse the cached action embeddings. This substantially reduces inference cost, with the efficiency gains becoming increasingly significant as the number of candidate actions and context length grows. At ~1k candidates, CLM is 13x faster than Jev.

![](https://contrastive-lm.notion.site/image/attachment%3A05c1cd4f-d11d-47a6-8056-d644de99183e%3Aimage.png?table=block&id=3e466c3c-12a8-8073-95a3-c8fd1a87cbfd&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=1600&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

Click to View More Experimental Details

##### How does “Action Caching” work for CLM in Super Mario?

![](https://contrastive-lm.notion.site/image/attachment%3A2a68d3a0-87a6-44f4-9324-d9d70f16e1ab%3Aimage.png?table=block&id=3e466c3c-12a8-8019-b21a-edae002b828b&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=1500&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl) The 4 action embeddings are precomputed before gameplay begins. At each step, only the new game state passes through the state encoder. Its embedding $z_s$ is then scored against the cached action embeddings $z_a$, and the highest-scoring action is executed. This reduces the cost from 5 forward passes to just 1 per step.

### Training Algorithm

CLM is trained with a bidirectional InfoNCE loss. Given a batch of $B$ matched state-action pairs, we compute a $B \times B$ similarity matrix. For each positive pair $(s_i, a_i)$, we optimize retrieval in both directions: $s_i \rightarrow a_i$ and $a_i \rightarrow s_i$: 
$$
\mathcal{L}_{\mathrm{CLM}}
=
-\frac{1}{2B}\sum_i
\left[
\log
\frac{\exp\left(s_i^\top a_i/\tau\right)}
{\sum_j \exp\left(s_i^\top a_j/\tau\right)}
+
\log
\frac{\exp\left(a_i^\top s_i/\tau\right)}
{\sum_j \exp\left(a_i^\top s_j/\tau\right)}
\right]
$$
 For mid-training, we extend the bidirectional InfoNCE objective with hard negatives. Let $h_{ik}^{(a)}$ denote a hard negative action for state $s_i$. For the state-to-action direction, the loss is:
$$
L_{s \rightarrow a}^{\mathrm{hard}}=-\frac{1}{B}\sum_i\log\frac{\exp\left(s_i^\top a_i / \tau\right)}{\exp\left(s_i^\top a_i / \tau\right)+\sum_k\exp\left(s_i^\top h_{ik}^{(a)} / \tau\right)}.
$$

### Scaling Laws for Verification

![](https://contrastive-lm.notion.site/image/attachment%3Ae1c57b73-ee6a-4ad7-b458-f42b9d37376b%3Aimage.png?table=block&id=3e466c3c-12a8-8033-9b05-cc41ecd9e4e5&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=1600&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl) We find that the test InfoNCE loss $L$ scales as a power law with training compute $C$, dataset size $D$, projection-head size $N$, and encoder size $N_{\mathrm{enc}}$. These dimensions must be scaled jointly to achieve the optimal verification performance. When each scale factor is not bottlenecked by the others, the dependence on each variable $X \in {C, D, N, N_{\mathrm{enc}}}$ can be described as:
$$
L(X) \approx  \left(\frac{X_c}{X}\right)^{\alpha_X},
$$
where $X_c$ is a fitted scale constant and $\alpha_X$ is the corresponding scaling exponent following Kaplan et al. Notably, scaling the encoder size yields the strongest gains. Experiments are conducted on the Nemotron DQA dataset and evaluated on a held-out dataset.

##### Data vs. Optimal Model Size

![](https://contrastive-lm.notion.site/image/attachment%3A557b3ec6-b39a-4491-b6d5-a004141f39ae%3Aimage.png?table=block&id=3e466c3c-12a8-80e4-854f-dd2c666b1d01&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=1120&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl) We fix a compute budget $C$ and plot the test loss against the parameter count of the projection head $N$, with each curve corresponding to a different data budget $D$. In log-parameter space, each iso-FLOP curve is well approximated by a parabola, and its minimum identifies the optimal head size for that data budget. As the budget grows, the optimum shifts steadily toward larger heads. Specifically, the optimal size grows almost exactly linearly with the number of training tokens $N^* \propto D^{1.02}$, at roughly 310 tokens per parameter.

### Data Recipe

CLM is trained in three stages, with each stage introducing a progressively harder form of state–action alignment. Pre-training learns broad semantic representations, mid-training develops fine-grained discrimination, and post-training adapts the representation space for action classification.

![](https://contrastive-lm.notion.site/image/attachment%3A0aa38822-3af3-411d-b75f-79c124efc5c3%3AAdobeExpressPhotos_f97a482330874a9cbeb2a21fbaafe78b_CopyEdited.png?table=block&id=3e466c3c-12a8-80ee-b136-e002e681f423&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=1500&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

Stage 1 — Pre-training. We first pre-train CLM on an internet-scale question–answer dataset containing ~60M pairs from Nemotron DQA. We treat each question as the state and its answer as the corresponding action. This stage learns broad semantic representations from a diverse corpus.

Stage 2 — Mid-training. We then introduce ~30M synthetic hard negatives generated by Gemini 2.5 Flash-Lite. For a subset of Nemotron DQA questions, we construct semantically similar but incorrect answers. These negatives are precomputed and incorporated into the InfoNCE loss using Equation 2, enabling more fine-grained discrimination between plausible actions.

Stage 3 — Post-training. Finally, we post-train CLM on ~1M agent trajectories from the Agent Data Protocol (ADP) dataset, supplemented by terminal traces from Endless-Terminals, LiteCoder-Terminal-SFT. Each trajectory step is represented as a state–action pair, where the state contains the agent’s current context and the action corresponds to the decision taken at that step. This adapts the learned representation space for action classification in agentic environments.

##### Evaluating CLM after Pre-training

![](https://contrastive-lm.notion.site/image/attachment%3Abdb83c27-badd-4864-991e-77124cec9976%3Aimage.png?table=block&id=3e466c3c-12a8-80d2-b013-f26ccc278c89&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=1410&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

We first evaluate CLM-8B immediately after pre-training. As illustrated above, when asked “Who wrote the play Romeo and Juliet?”, the Qwen3-8B embeddings assign the highest probability to an incorrect answer and ranks “William Shakespeare” third.

In contrast, CLM-8B correctly ranks “William Shakespeare” first with 54.2%. This suggests that pre-training reshapes the model’s representations into a useful decision space.

##### Data Mixture for Post-Training

![](https://contrastive-lm.notion.site/image/attachment%3A043e5478-9555-4d18-9039-d38c01500692%3Aimage.png?table=block&id=3e466c3c-12a8-80f6-b5ab-f5e5141474f5&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=1410&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

To preserve the general representations learned during pre-training, we use co-training with data replay rather than fine-tuning exclusively on agentic traces. Specifically, 40% of the post-training mixture consists of the Nemotron DQA examples, while the remaining 60% are agentic trajectories.

This replay substantially mitigates catastrophic forgetting. With replay, the Nemotron hard-negative top-1 accuracy decreases slightly from 69% to 68.5%. In contrast, when training on agentic data alone for the same number of agentic steps, the accuracy drops to 56.2%.

##### Why Not Train on Hard Negatives from the Start?

![](https://contrastive-lm.notion.site/image/attachment%3A3b48f497-5985-448a-90dd-f00941f5614b%3Aimage.png?table=block&id=3e466c3c-12a8-805e-ba7b-ca7b5a577e8f&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=1410&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

We compare two training strategies under a fixed compute budget:

Pre-train + Mid-train: pre-train on the full Nemotron DQA corpus with bidirectional InfoNCE, then briefly mid-train on hard negatives using Equation 2.

Hard negatives from scratch: train on Nemotron DQA and hard negatives jointly from the beginning.

We evaluate on ~100K held-out questions, each with one gold answer and 10 hard negatives. The top-1 accuracy measures whether the gold answer ranks highest. We find that pre-training alone reaches 52.1% without seeing any hard negatives. A short mid-training stage then boosts accuracy to 69.2%. In contrast, training with hard negatives from the start improves quickly but peaks at 62.4% before overfitting. The two-stage recipe achieves 7% higher accuracy at fixed budget.

Takeaway: Hard negatives work best as a refinement signal on top of pre-training, rather than as a substitute for it.

### CLM Playground

![](https://contrastive-lm.notion.site/image/attachment%3A94562134-d4e9-4915-88de-60ab3fddda42%3Aplayground.png?table=block&id=3e466c3c-12a8-804a-8d19-ef9cdff1e120&spaceId=59b4b732-2399-4ed0-b86b-b5dd420bb513&width=1410&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

CLM comes with a playground on [GitHub](https://github.com/Contrastive-LM/CLM). Write a state, add typed questions, and see CLM's full probability distribution over the answers in milliseconds.

### Does CLM work for robotics?

We released a robotics variant of CLM earlier this year. See the [CoVer-VLA paper](https://arxiv.org/abs/2602.12281) for more details on verification scaling for vision-language-action (VLA) models.

## Join us!

We call on the community to join us in this effort, either by providing your feedback or contributing to the project!

Please don’t hesitate to get in touch:

Github Repo: [https://github.com/Contrastive-LM/CLM](https://github.com/Contrastive-LM/CLM)

Join Discord: [https://discord.gg/5dAQEDJBs](https://discord.gg/5dAQEDJBs)

Contact: jackykwok@stanford.edu

## Conclusion

CLM opens up a new direction for scalable, reliable, and fast verification. Moving forward, we plan to explore several key directions:

Scaling Experiments: Extend our scaling-law experiments to substantially larger backbones and study how verification performance can be further scaled

Vision and multimodal support: Extend CLM to include images, video, and other modalities for robotics and computer-use tasks.

Scaling the data recipe: Expand pre-training, hard-negative mining, and agentic post-training.

…and more to come.

CLM-8B is part of our scaling ladder, where we train models across multiple scales to establish scaling laws and predict performance at larger scales. A multimodal CLM-35B is now in training with more data, compute, and parameters. Stay tuned for the release early next month

## Citation

If you find CLM useful, please consider citing it:

@misc{kwok2026contrastivelanguagemodels, title={Contrastive Language Models: A System One Model for Fast and Generalizable Decision-Making}, author={Jacky Kwok and Hangoo Kang and Tarun Suresh and Jon Saad-Falcon and Marco Pavone and Christopher Ré and Azalia Mirhoseini}, year={2026}, note={Notion Blog} }