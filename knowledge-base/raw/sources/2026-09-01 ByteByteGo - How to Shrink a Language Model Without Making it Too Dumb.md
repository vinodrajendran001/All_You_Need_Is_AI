---
type: raw-source
source_id: src-2026-09-01-bytebytego-shrink-language-model
captured: 2026-09-02
title: "How to Shrink a Language Model Without Making it Too Dumb"
source: "https://blog.bytebytego.com/p/how-to-shrink-a-language-model-without-295?utm_source=post-email-title&publication_id=817132&post_id=213591996&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-09-01
created: 2026-09-02
description: "Models have grown roughly 100-fold in a few years, while consumer graphics memory has roughly doubled. It’s not just a matter of tightening things up to make them fit."
tags:
  - "clippings"
  - "topic/quantization"
  - "topic/efficiency"
  - "source/raw"
---
## Catch AI cost spikes in real time (not months later) (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!BYSQ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15aaea1b-0823-4087-b879-9522fdcd6cf4_1080x1080.png)

Datadog’s free guide shows how to connect AI spend, infrastructure, and model performance into a single view, so you can correlate cost increases to the architecture changes that caused them before they show up on your cloud bill.

Learn how to:

- Break down AI costs by token, model, provider, and team
- Get alerted the instant inference volume spikes or API spend exceeds budget
- Correlate cost increases directly to architecture changes so root-cause analysis takes minutes

---

A model with 70 billion parameters can take up to 140 GB of space. A good graphics card has 24 GB. A very good one might have 48 GB.

As you can see, the gap is quite significant. Disk space is pretty cheap, but fast memory is scarce and costly. Moreover, the models have grown roughly 100-fold in a few years, while consumer graphics memory has roughly doubled. It’s not just a matter of tightening things up to make them fit.

So how do you run such a model?

The simplest option is to purchase the hardware that is capable of running the model. But it is costly, and doesn’t work well with consumer hardware.

The other option is to shrink the model. But we don’t want to do so at the expense of the model’s intelligence. This is where certain techniques can help us make the model smaller in principle without a dip in the quality of its output.

In this article, we will cover:

- What makes a language model intelligent?
- Three techniques to shrink the model
- How to shrink the model by packing fewer details?
- How to shrink the model by trimming unused pathways?
- How to shrink the model by mimicking behaviour?
- Does shrinking damage the model’s intelligence?

![](https://substackcdn.com/image/fetch/$s_!drcX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa61f65a0-da92-4610-8c06-45e7e7084ac0_3708x1578.png)

*Disclaimer: This post is based on publicly shared details from various sources. References at the end. Please comment if you notice any inaccuracies.*

## What Makes a Language Model Intelligent?

Large language models like ChatGPT are quite different from normal software programs. They don’t depend on typical if-else statements to decide what should happen next.

A large language model is essentially a very big pile of numbers called parameters or weights. These weights are the foundation of a language model’s intelligence. For reference, a model with 70 billion parameters means 70 billion numbers or weights. Each weight is normally stored in 16 bits, which is two bytes. Two bytes multiplied by 70 billion comes to 140 GB, which is basically considered the size of the model.

The weights are arranged into matrices. A single weight matrix is a grid, often something like 4096 by 4096. This comes to roughly 16.7 million numbers in a matrix. A 70 billion parameter model has hundreds of these matrices stacked across 80 or so layers.

Of course, weights in themselves aren’t the whole story behind a model’s capability. Multiple components work together to make a model intelligent. For example, the model needs an architecture like the Transformer to route data and perform attention. It also needs a context window that holds the prompt and everything generated during the conversation.

However, the architecture is made up of a few hundred lines of code. The prompt may be a few kilobytes. In contrast, the weights form the bulk of the language model. Without the proper weights, a language model cannot work as intended. The weights perform a bunch of tasks:

- They store patterns such as grammar, facts, and reasoning shortcuts.
- Once the training is finished, the weights freeze into an immutable network of numerical values.
- The weights decide how strongly one simulated neuron influences the next.

Running the model means pushing the input through these weight matrices until the next word comes out of the other end.

One thing to keep in mind over here is that no single weight means anything on its own. If you opened a model file and looked at weight number N, you might see something like 0.0293. On either side of this number may be other numbers such as -0.0117, 0.004, -0.0862. On their own, each of these numbers hardly makes sense. The ability of the model is hidden in the relationships between the various weights. Think of it like a photograph where every pixel comes together to show something recognizable. Even if we modify every pixel’s brightness slightly, we can still make out the things in the picture. This is because the information isn’t sitting in one single place.

Following on from all this information, it is quite easy to figure out that to shrink a model, we’ve to somehow deal with these weights. And this is exactly where the techniques come into the picture. However, a couple of points can help us make better sense of the techniques to shrink a model:

- Firstly, not all weights matter equally. Most of the weight values are close to zero and barely impact the final output. However, a small handful are large and produce a bigger impact.
- Second, we can only judge a model based on its behaviour, not its internals.

Let us now look at the techniques.

---

## Build and scale a winning AI agent strategy (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!SJtL!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21fb72c6-1e79-42e0-8804-9217f2102310_1080x1080.png)

Shipping agents to production is the easy part. Keeping them reliable, governable, and improving over time is where most enterprise AI programs stall.

How do top teams do it? They use an Agentic Operating Model (AOM), a step-by-step framework for aligning people, process, and technology so enterprise agents improve as they scale.

In LangChain’s latest guide, you’ll learn:

- Why AI agents don’t break like traditional software
- The engineering stack that covers the entire agent lifecycle
- Shifting from “build and deploy” to “operate and continuously improve”

---

## Three Techniques to Shrink the Model

The techniques to shrink a model revolve around using fewer bits to store a weight or using fewer weights. There are three main techniques:

- **Storing Each Weight in Less Detail (Quantization):** In this approach, we keep all the weights, but describe each one in a less precise manner. For example, two bytes become half a byte.
- **Removing Irrelevant Weights (Pruning):** This approach involves finding the weights that contribute nothing and deleting them.
- **Building a Smaller Model to Mimic the Larger One (Knowledge Distillation):** In this approach, we don’t touch the original model, but train a new, smaller model to behave in a similar way.

Going back to our photograph example, we can think of quantization as taking a picture with a cheaper camera that has a slightly lower resolution. Pruning is more like cutting away the blank edges of the photograph that might not be adding any value to the picture. Distillation can be thought of as paying a skilled painter to reproduce the picture at a quarter of the size.

The great part about all these techniques is that they can be stacked. For example, a model can be distilled by the lab that made it. It can be pruned by a research team. Lastly, it can be quantized by the user before it is loaded on a specific machine. In other words, stacking can make it possible to run a high-end large language model on normal consumer hardware.

Let us now look at each of these techniques in more detail.

## Shrinking a Model by Packing Fewer Details

The first technique to shrink a model is to pack fewer details for every weight. This technique is known as quantization.

Let’s say a particular weight might be stored as 0.02934517. This takes a lot of space, but in a 70 billion parameter model, it just happens to be one single weight. Whether it is stored as 0.02934517 or 0.029 makes almost no difference to the model’s output. In other words, a lot of storage is spent on precision that might not even be important.

Quantization is a technique that takes away this precision.

The first bit of quantization happens even before the model is shipped. During training, model weights are normally stored as 32-bit (4 bytes) floating-point numbers. This is also known as the FP32 format. Since training involves making millions of tiny adjustments to each weight, high precision is needed. But when the model is distributed, the precision is usually brought down to 16-bit float format, which is also known as FP16 or BF16.

However, we can bring the precision down even further. To understand how, we need to first be clear about how a float value is actually built.

A floating-point number splits the bits into three parts: a sign, an exponent, and a mantissa. FP32 gives 1 bit to the sign, 8 bits to the exponent, and 23 bits to the mantissa. BF16, on the other hand, keeps all exponent bits and cuts the mantissa down to seven. This is basically the same range as FP32, but with less detail. For clarity, BF16 is slightly different from FP16, which gives the exponent only 5 bits and keeps more bits for the mantissa. BF16 has largely replaced FP16 in practice.

An integer has an even greater difference. An 8-bit integer is a whole number from -128 to 127. A 4-bit integer is a whole number from -8 to 7. There is no exponent and no scale. In other words, converting a float into an integer not only causes a loss of precision, but also removes each weight’s scale.

![](https://substackcdn.com/image/fetch/$s_!7g8W!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b31cb59-2d7f-429d-a822-b269634a00b0_3162x2122.png)

Let us now look at the complete process of quantization:

### 1 - Mapping Ranges

In the first step, we find out the minimum and maximum values of a data set and divide the total span into a fixed number of steps.

To be clear, “the data set” is not the entire model. It’s just a small group of neighbouring weights. We can call it a block, and it should ideally be pretty small.

For example, consider these eight weights: 0.021, -0.017, 0.004, -0.048, 0.011, 0.033, -0.006, 0.070. They span from -0.048 to 0.070. The largest value in either direction is 0.070. With 4 bits as our target precision, we can write whole numbers from -7 to 7. In other words, seven steps in each direction. Therefore, one step can be calculated as 0.070/7, which comes to 0.010.

### 2 - Rounding Values

Instead of keeping a long decimal, each original number is rounded to the closest available step. To do so, we divide each weight by the step size and round it to the nearest whole number.

The table below shows the new weights:

![](https://substackcdn.com/image/fetch/$s_!QoTF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa1f900a8-d05f-4fe1-863d-ef07328594a5_3104x1812.png)

As you can see in the table, the right-hand column values are the ones that go into the model weights file eventually. Every entry here is a whole number between -7 and 7.

The original weights were floating-point numbers. Since a float carries its own scale, rounding off to engineers removes the precision as well as the scale of every weight. This scale has to be stored somewhere.

### 3 - Using a Scale Factor

We need to keep track of the scale factor so that the compressed numbers can roughly reconstruct the original values when the model needs to read them.

In our example, the scale factor is the step size (0.010). It is stored once for the entire block. To recover a weight, we can multiply the stored integer by the scale factor.

So, for example, the stored weight of 2 is multiplied by 0.010 to arrive at the value 0.020. Of course, it is still different from the original value of 0.021, but the error is much less now. In other words, the model is still quite unchanged. We still have the same weights (with some error), the same matrices, and the same layers. However, it takes a lot less storage.

## Shrinking the Model by Removing Unused Weights

The second technique takes the opposite approach. Instead of trying to store each weight in less space, we delete some of them. This approach is known as pruning.

Pruning works because not all weights matter equally. Most of them have a value close to zero, such as 0.00004, -0.0011, and so on. These values are so small that they don’t impact the output in a meaningful manner. However, billions of such weights are produced during training. They are useful during the training phase, when the model is taking its original shape. You could think of them as driveways and service roads that are never used but still shown on a city map. Even if you remove them, they won’t have any impact on the people who are using this map to commute through the city.

The key decision with pruning is which weights to remove. The easiest approach uses the size. We sort the weights by how far they are from zero in either direction and delete the smallest ones. For example, if this approach helps prune 20% of the weights, it comes to around removing 14 billion weights from a 70 billion model.

However, there is a flaw in this approach. The influence of a weight also depends on the pathway on which it sits. A better method runs a few hundred sample texts through the model first. It then monitors how large the typical inputs are to each weight. Based on this, each weight is assigned a final score.

There is another factor that should be considered when it comes to pruning. It is related to the mechanism of removing weights. There are two main approaches:

- **Setting to Zero:** The first approach is to set the chosen weights to zero. This does minimal damage. But we end up with a matrix that is full of zeros in no particular pattern. The GPU still has to run the calculations with those entries.
- **Removing Structural Pieces:** The second way is to remove the structural pieces such as an entire neuron, an attention head, or even a complete layer. This helps shrink the matrix. But this is also a coarser approach. Removing one neuron might mean removing every weight attached to it. Some of these weights may be important, but they are also deleted. In other words, the overall damage to the model is greater in this approach.

See the diagram below that shows the two approaches:

![](https://substackcdn.com/image/fetch/$s_!gStq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd98ff158-bea5-4c0e-b469-ee321c9b303e_3418x1740.png)

Ultimately, pruning is rarely a complete solution. It is much better to use pruning in combination with some other techniques.

## Shrinking the Model by Mimicking Behaviour

The third technique to shrink the model creates a new smaller model.

In this technique, we take the big model. It is called the teacher model. Next, we build a new model from scratch using the same architecture. However, it has fewer layers and smaller matrices. For example, a model with 7 billion weights instead of 70 billion. We call this new model the student model.

The student model starts its life with random weights that are meaningless. This model goes through the training process, but we don’t use the raw text from other sources on the internet. Instead, the student model is trained on the teacher’s behaviour. This involves feeding both the student and the teacher the same input and pushing the student model towards producing output closer to what the teacher model produced.

This technique is known as knowledge distillation.

This type of approach might appear counterintuitive. But it works because of how the model works internally.

When a model predicts the next word, it doesn’t just produce a single word. It produces a probability score for every word in its vocabulary. For example, given the sentence “the cat sat on the…”, the teacher model might say “mat 41%”, “floor 12%”, “couch 9%”, and so on. In an ordinary training approach, the student model only receives the correct answer. But during distillation, the student model receives the whole distribution of probable answers. In other words, the student model learns that “couch” was also a pretty sensible guess, but maybe the word “purple” was quite absurd.

See the diagram below:

![](https://substackcdn.com/image/fetch/$s_!zzj4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F969f1282-d533-4a94-9ca7-658a477d2cf1_2802x1958.png)

Think of knowledge distillation like a teacher evaluating a paper, but instead of just putting ticks and crosses, the teacher writes in the margins to give a better idea to the student about the mistakes they might have made. The second approach helps the student learn faster

Of course, distillation involves training at scale. A huge teacher model runs over enormous amounts of data, which requires datacentre-level resources. For a developer, it involves downloading the smaller student model that can run on less demanding hardware.

## Does Shrinking Damage the Model’s Intelligence?

Shrinking a model definitely reduces its overall intelligence, but usually only a tiny bit. Think of it like a trade-off between the model’s physical size and its mental sharpness.

Each of these techniques has an impact on the model’s intelligence:

- **Quantization:** It makes the weights less precise. The model can lose its ability to understand extreme nuance. It might forget highly specific facts, or its tone might sound slightly less natural. Many of the changes depend on how far you go on the quantization scale. For example, shifting from 32-bit to 8-bit causes almost no noticeable change in intelligence. But pushing down to 4-bit or even lower might have a huge impact.
- **Pruning:** It reduces the model’s ability to handle complex, multi-step logic. However, only trimming the idle pathways does not have a big negative impact on intelligence. Only when we aggressively prune the deeper pathways do we end up making the model dumb.
- **Knowledge Distillation:** The smaller student model may lack original problem-solving skills. It can perfectly mimic the big teacher model’s style, but a completely new logical puzzle might throw it off if the same wasn’t explicitly taught by the teacher model.

## Conclusion

In this article, we’ve looked at the various techniques of shrinking a large language model in detail.

Shrinking a language model without any plan can cause a loss of intelligence. Therefore, various techniques follow different approaches to ensure that the model takes less space without losing its original capabilities drastically. Here are the key points to remember:

- Quantization involves storing each weight in fewer bits.
- Pruning deletes the weights and pathways that contribute the least.
- Distillation does not modify the original model, but involves a large teacher model training a smaller student model.

Ultimately, choosing a technique or combination of them depends on the overall goals that the language model needs to fulfill.

**References:**

- [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314)
- [GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers](https://arxiv.org/abs/2210.17323)
- [A Simple and Effective Pruning Approach for Large Language Models](https://arxiv.org/abs/2306.11695)
- [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531)

---

∙