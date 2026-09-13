---
type: raw-source
source_id: src-2026-09-13-rahman-quantizing-llms-gke
title: "Quantizing LLMs on GKE for Faster and Cheaper Inference"
author: Mofi Rahman
url: "https://medium.com/google-cloud/quantizing-llms-on-gke-for-faster-and-cheaper-inference-59bfc6b15e43"
published: 2025-11-06
captured: 2026-09-13
created: 2026-09-13
updated: 2026-09-13
tags:
  - source/raw
  - quantization
  - inference
  - google-cloud
status: active
---
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*aL0Xvixt_MugIgHZUZ1Oug.png)

When you are thinking about LLM inference, it’s always a balance between cost, accuracy and performance. There are use cases where you need the most accuracy and the biggest model possible. If cost was not a concern you should always go for the largest and fastest accelerator you can get your hands on. But unfortunately, cost often is a big consideration in your AI journey. When you are optimizing your LLM inference workload for cost, quantization is a must-have tool in your arsenal.

## What even is Quantization?

At its core, quantization is a model compression technique that reduces the numerical precision of a model’s parameters, primarily its weights and, in some cases, its activations. The process involves mapping values from a high-precision data representation (typically FP16 or BFloat16), which can store a wide range of numbers with fine granularity, to a lower-precision format that uses fewer bits to represent each number.

Lets take a LLM like [Gemma 3 27B](https://huggingface.co/google/gemma-3-27b-it). It has 27 billion parameters with a precision of BFloat16. So every one of these parameters takes up 16 bits or 2 bytes of memory. If you want to load this model into memory you are going to need at least *27\*10^9\*2* bytes or 54 Gigabytes of Accelerator memory. Now say we want to run inference on Google Cloud using very affordable L4 GPUs. With 24GB of vram on each L4 GPU, we would need at least 3 GPUs to even load the model. (You will actually need 4 GPUs due to some divisibility issues of attention heads and other model dimensions in most LLM serving frameworks). Needing 4 GPUs to serve our Gemma 3 model does not seem very cost-optimized anymore.

Now, what if we had a way to change those model parameters from taking 2 bytes of space to 1 byte? That would cut our VRAM requirement to half. How about taking ½ a byte per parameter? Now we can fit the entire model in roughly 13.5 GB of VRAM. If we could do something like that, we can serve the entire model in a single L4 GPU. Well that’s what quantization is. We can use lower precision number formats like FP8, INT8 or INT4 to significantly lower memory requirements.

## Benefits of Quantization

**Memory Footprint Reduction:** The most obvious benefit of quantization is the memory footprint reduction. As discussed in the previous section, a quantized model can fit in a much smaller GPU compared to the full precision models. The memory savings extend beyond the model weights to the Key-Value (KV) cache, a crucial component in autoregressive generation that stores intermediate attention values. A smaller KV cache per token means more tokens can be processed in parallel within the same GPU memory, leading to higher throughput and supporting greater concurrency for serving multiple users simultaneously

**Accelerated Inference:** Quantization can significantly speed up the inference process through two primary mechanisms. Quantization reduces memory bandwidth by lowering data precision. This decreases data transfer during inference, speeding up weight loading from memory to compute units.

The second, often more impactful, mechanism involves specialized integer arithmetic hardware. Modern CPUs and GPUs compute low-precision integers much faster than floating-point numbers. This boosts matrix multiplication throughput in neural networks, greatly reducing inference latency.

**Energy and Cost Efficiency:** Quantization reduces data movement and computational complexity, cutting energy use during inference. This benefits edge devices and data centers, lowering operational costs and environmental impact, making AI more sustainable and viable at scale.

**Deployment Flexibility:** Quantization significantly improves deployment flexibility, enabling powerful LLMs on edge devices, IoT, automotive, and mobile systems. This allows for low-latency, private, and offline on-device AI applications, reducing reliance on cloud servers and making advanced AI ubiquitous.

## Two methods of quantization

There are two primary methodologies for applying quantization to a neural network: Post-Training Quantization (PTQ) and Quantization-Aware Training (QAT).

Post-Training Quantization or PTQ is a technique that is applied to a model after it has been fully trained. The process involved converting the weights and potentially the activations of the pretrained model from a high-precision format to a lower-precision one. This process is usually much faster compared to its counterpart QAT. But since the model is not trained to account for quantization error, PTQ can lead to degradation in accuracy compared to QAT in very low bit-width (<4-bit).

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*pthE4m1sp_kqWf3l_3wHqg.png)

PTQ

Quantization Aware Training or QAT integrates the quantization process during the model training or fine-tuning phase. It simulates the effects of low precision arithmetic directly into the training or finetuning process.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*8W3P6UcqxlSF4KYmbQv16w.png)

QAT

During each forward pass of training, the models weights and activations are passed through “fake quantization” nodes that mimic the rounding and clipping errors of inference-time optimization. These simulated errors are then reflected in the loss function, and the gradients are backpropagated to update the high-precision weights.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*V-ps2V_bt45tBTD_JMh5JA.png)

QAT

Quantization Aware Training has better accuracy than PTQ but cost of retraining the model and the need for high quality dataset make this cost prohibitive for most users.

<iframe src="https://medium.com/media/bf1741d899789887a407131206eb06d7" allowfullscreen="" frameborder="0" height="989" width="680" title="ptq-vs-qat.md"></iframe>

## Drawbacks of Quantization

**Lower Accuracy:** When we quantize a model we are always losing some precision. In benchmarks the drop in quality is seen to be anywhere from 1% to all the way to 30+%. In most practical applications however the lower quality is acceptable and imperceptable. Quantization Aware Training or QAT quantized models preserve quality almost on par with the original model.

**Hardware and Data Requirements:** For both types of quantization you need access to accelerators that can process the weights. For QAT you need access to high quality training data and a significant amount of accelerator resources. For the PTQ calibration process you still need to find representative data.

## Quantize a Model in GKE

There are a number of libraries that we can use to quantize a model in both PTQ and QAT methods.

In this example we will be using the llmcompressor library from Vllm to quantize a model using GPTQ and subset of PTQ method.

You can find the instructions [in this repo](https://github.com/GoogleCloudPlatform/kubernetes-engine-samples/tree/main/ai-ml/llm-quantize/llm-compressor-gptq)

## Prerequisite

- A Google Cloud Project
- A GKE Cluster with GPU nodes. You can find instructions for [Autopilot Cluster](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/autopilot-gpus) and [Standard Cluster](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/gpus)
- [gcloud cli](https://docs.cloud.google.com/sdk/docs/install)
- kubectl cli
- envsubst

## Steps

- Create an Artifact Registry repository:
```c
export REPO_NAME=llm-quantize
export REGION=us-central1
gcloud artifacts repositories create $REPO_NAME --repository-format=docker --location=$REGION
```
- Build and push the Docker image:
```c
export IMAGE_URL=${REGION}-docker.pkg.dev/$(gcloud config get-value project)/${REPO_NAME}/llm-processor-gptq
gcloud auth configure-docker ${REGION}-docker.pkg.dev
gcloud builds submit --tag $IMAGE_URL .
```
- Set environment variables:
```c
export MODEL_ID="meta-llama/Meta-Llama-3-8B-Instruct"
export HF_TOKEN="your-hugging-face-token"
```
- Create a Kubernetes secret for the Hugging Face token:
```c
kubectl create secret generic hf-secret --from-literal=hf_api_token=$HF_TOKEN
```
- Deploy the quantization Job to GKE:
```c
envsubst < job.yaml | kubectl apply -f -
```
- Monitor the Job:
```c
kubectl get pods -w
```
- View the logs once the job is running:
```c
kubectl logs -f -l job-name=quantize
```

## Who Should Quantize a Model

Like many things in tech, the answer is, “it depends.” For most use cases quantizing a model would give a good enough result for your inference workload, and be cheaper and faster. But that does not mean everyone needs to quantize their own model. For many models in huggingface and kaggle providers, individuals share their quantized model that you can test and use. For example for [google/gemma-3–4b-it](https://huggingface.co/models?other=base_model%3Aquantized%3Agoogle%2Fgemma-3-4b-it), there are a number of quantized models available in hugging face for you to use and test out.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*MLJqj_hv3YAom_JOA0uLOw.png)

Huggingface Quantize Models for gemma-3–4b-it

This post covered quantization at a high level with an example of running on GKE. There are some fantastic [quantization related papers in this repo](https://github.com/Zhen-Dong/Awesome-Quantization-Papers), that I would recommend.