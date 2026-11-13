---
type: raw-source
source_id: src-2026-11-05-huggingface-moe-training-handbook
title: The Ultimate MoE Training Handbook
author: Nouamane Tazi, Leandro von Werra, and Thomas Wolf
publisher: Hugging Face
url: https://huggingface.co/spaces/huggingface/moe-blogpost
published: 2026-11-05
captured: 2026-11-13
capture_note: Re-captured from the live page at the user's request because the original clipping preserved only the Space's iframe and no article text.
status: immutable
tags:
  - source/raw
  - mixture-of-experts
  - llm-training
  - distributed-training
---

# The Ultimate MoE Training Handbook

## Capture provenance

The original clipping, [[The Ultimate MoE Training Handbook - a Hugging Face Space by huggingface]],
saved on November 10, contains the title, URL, and description, but its body is only the
Hugging Face Space's "Refreshing" placeholder and an iframe pointing to
`https://huggingface-moe-blogpost.hf.space/`. At the user's request on November 13, that iframe
address was fetched and its server-rendered HTML converted to Markdown. The original clipping is
left unchanged.

- **Byline:** Nouamane Tazi, Leandro von Werra, and Thomas Wolf, with the affiliation Hugging
  Face, from the page header and its citation block. The page description reads "A hands-on
  guide to training Mixture-of-Experts models with Megatron-LM". The original clipping lists no
  author.
- **Date:** the header shows "Published Nov. 5, 2026"; the page metadata gives the same value.
  A margin note gives the reading time as 1-2 days.
- **Conversion:** article headings are demoted one level under `## Article`. The 62 interactive
  figures are reproduced as links to their static poster images with their figure captions;
  their plotted values are not transcribed. Paragraphs the page styles as "Recommendation" and
  "Watch" callouts are rendered as block quotes with those labels, which the page's stylesheet
  supplies. Margin notes are placed after the paragraph that contains them. Collapsible blocks
  keep their summary line, marked *Collapsible*, followed by their contents; Megatron source
  excerpts are fenced without their line numbers, and their indentation is restored from the
  page's layout. Window labels on code blocks (such as "Commands") precede the fence. Footnote
  references are kept as the superscript numbers the page displays; because the page assigns
  those numbers in script, a footnote key mapping each number to its reference ID follows the
  article. The "References" heading for the first reference list is supplied by this capture.
  Copy buttons and other interface controls are omitted. Wording, numbers, code, and links are
  otherwise as served.

## Article

### 1. Introduction

The frontier is sparse. On the [Artificial Analysis index](https://artificialanalysis.ai/models/open-source), 18 of the 20 highest-scoring open-weights models are mixtures of experts (the two exceptions, Nanbeige4.3-33B and Qwen3.8 27B at twelfth and thirteenth place, are dense)<sup>1</sup>. They include the top model of each of the five leading labs: DeepSeek V4.1 Flash 1017, GLM-5.3, MiMo-V2.6-Pro, Ling 3.1 Flash 1019 and MiniMax-M3.1-Flash<sup>1</sup>.

> *Margin note:* Reading time: 1-2 days. For the best reading experience, we recommend not using a mobile phone.

![active-vs-release](https://huggingface-moe-blogpost.hf.space/viz/posters/active-vs-release.webp)

*Figure caption:* Figure 1.1

What an MoE offers lies in how it spends its inference compute. Each token runs through only a few of its experts, so the model can hold many more parameters than it uses on any one token: the small MoE you will train in chapter 2 has 6.86B parameters, of which 1.22B are active per token. Turning that inference saving into faster training is the hard part.

Our previous deep dive on training, the [Smol Training Playbook](https://huggingface.co/spaces/HuggingFaceTB/smol-training-playbook), covered training a dense model but only touched on MoE design. Because the star of that book, SmolLM3, was a dense transformer, its training needed no technique specific to MoE, like [expert parallelism](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=expert_parallelism). Still, we glanced at MoE in the playbook's "Going Sparse: MoE" section to cover its high-level design choices: sparsity, granularity, shared experts and load balancing. That section named the main reasons distributed MoE training is complex: expert placement, load balancing and all-to-all communication, but without diving into the particulars<sup>2</sup>. This handbook starts from that list.

Going from a dense model to an MoE gives you three new challenges to manage: a router that decides which experts each token uses, a load that has to stay balanced across the experts, and, once the experts are split across GPUs, an [exchange of tokens](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/token_dispatcher.py#L708-L727) between those GPUs in every MoE layer. Each aspect brings settings a dense run never had and new ways for a run to fail. The chapters that follow take those settings one at a time and examine them in detail, with code you can run and, in most cases, direct results and data from our own cluster experiments.

A run that goes south will give you a symptom but not the reason behind it. The map below is a high-level view to help you go back to the source: start from how a run fails, find the first signal of bad behavior (the canary in the coal mine), and go read the part of the post that explains the possible cause. You can keep this map at hand for the day a run goes wrong.

![triage-flowchart](https://huggingface-moe-blogpost.hf.space/viz/posters/triage-flowchart.webp)

*Figure caption:* Figure 1.2

Now, before we start, a quick note on the intended audience. Who is this handbook for? You will benefit from it if you have trained a dense model on a GPU cluster and want to train an MoE next. Chapter 2 sets up what you need and has you train that small MoE on a single node. If you are more curious about how MoEs work and what frontier models choose than about running one, skip ahead to chapter 3, Anatomy of MoE Training.

![roadmap-strip](https://huggingface-moe-blogpost.hf.space/viz/posters/roadmap-strip.webp)

*Figure caption:* Figure 1.3

Once the experts sit on different GPUs, every MoE layer exchanges tokens between them, a pattern our dense run never used. Can you trust your cluster's links with it before you change a single line of the model?

### 2. Setup and your first run

#### 2.0 What you need

Every command in this chapter was written for one kind of machine, so that everyone runs the same environment: a Slurm cluster of eight-GPU nodes. This section describes that setup, how much of the post you can follow with one GPU or none, and how to rent an eight-GPU node on Hugging Face Jobs. If your machines differ, you can still follow the explanations and adapt the commands.

##### The cluster the commands assume

The commands expect a [Slurm](https://slurm.schedmd.com/) cluster whose GPU nodes hold eight GPUs each. Containers start through [Enroot](https://github.com/NVIDIA/enroot) and [Pyxis](https://github.com/NVIDIA/pyxis), which let `srun` launch a task inside an image.<sup>3,4</sup> The per-node readiness check in [2.1](#s-2-1) uses NVIDIA's [DCGM diagnostics](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html). Our runs used AWS P5 nodes connected by Elastic Fabric Adapter (EFA), each with eight H100 GPUs of 80 GB.

Most of the chapter fits on one node. The dense baseline and the first MoE each request a single node with eight GPUs of about 80 GB. Only the network checks need more: the all-to-all tests in [2.1](#s-2-1) run on two, four and eight nodes, and the EFA image in [2.2](#s-2-2) is verified on two.

The software comes from two pinned sources. The first is the [NGC PyTorch](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch) image `26.06-py3`, which [2.2](#s-2-2) imports and extends with the cluster's network libraries. The second is a [Megatron](https://github.com/NVIDIA/Megatron-LM) checkout at commit `d6316eb45`, which you mount into the container rather than build into it. You also need a filesystem that the CPU workers and the GPU nodes can both read, because [2.3](#s-2-3) tokenizes the data on a CPU partition and the training jobs read the result from there.

##### Reading with one GPU, or none

You can get most of the post without a cluster. Chapter 3 takes the MoE layer apart: what each part does, what frontier models choose for it and the evidence behind each choice. You can read it end to end without running anything, and save its flags for when you have the hardware. Chapter 4 carries the same choices past pretraining, into serving and reinforcement learning.

In this chapter, the tokenization in [2.3](#s-2-3) runs on CPUs. Its small sample runs on a single machine without Slurm, so you can produce and inspect the same files the training runs read. The training recipes in [2.4](#s-2-4) and [2.5](#s-2-5) assume eight GPUs of about 80 GB, and the MoE spreads its experts across all eight. With fewer GPUs, read them for the method: what stays fixed between the two runs, how the expert width is chosen and what to compare. The all-to-all tests in [2.1](#s-2-1) and the EFA setup in [2.2](#s-2-2) need several nodes to run as written.

##### Renting a node on Hugging Face Jobs

If you want to run the single-node parts without owning the hardware, [Hugging Face Jobs](https://huggingface.co/docs/hub/jobs) runs a Docker image and a command on Hugging Face's machines, billed by the minute. It is open to any user or organization with a positive credit balance, and the monthly credits of a PRO, Team or Enterprise subscription can pay for jobs.<sup>5</sup> The largest hardware options that `hf jobs hardware` lists have eight GPUs, as many as [2.4](#s-2-4) and [2.5](#s-2-5) use; `h200x8`, for example, holds eight H200s of 141 GB each.<sup>6</sup>

A job is defined by a Docker image from Docker Hub or a Hugging Face Space, a command and a hardware option, so running this chapter there means packaging the image from [2.2](#s-2-2) as a Docker image and replacing the Slurm launcher with a Jobs command. A job stops after 30 minutes unless you set a different timeout.<sup>7</sup> A first command only checks that the job sees all eight GPUs:

```
hf jobs run --flavor h200x8 --timeout 10m \
    pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel \
    python -c "import torch; print(torch.cuda.device_count())"
```

Whether you run the recipes on your own cluster or on a rented node, the machines you were given may not perform the way their specification says. How would you notice a GPU or a link that quietly underperforms?

#### 2.1 Test your hardware

Before you start tuning a model, establish what the machines can do. With [Megatron](https://github.com/NVIDIA/Megatron-LM)'s `alltoall` dispatcher, each MoE layer sends tokens to the GPUs that hold their experts and returns the results through another all-to-all. The links between GPUs are therefore part of the work you need to test: a healthy [all-reduce](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=reduce_%26_allreduce) result alone does not tell you how quickly those token exchanges will run.

Run the checks below inside your job allocation, before launching training. With [Pyxis](https://github.com/NVIDIA/pyxis), `srun --container-image` starts a container; the next section explains how to prepare the training image.<sup>3</sup>

##### Check each node

Start with a readiness check on every allocated node. NVIDIA's [DCGM](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html) provides several diagnostic levels, with level 1 intended for readiness checks and the higher levels adding tests that help investigate failures. The command below runs one task per node so you can inspect each result before starting training.<sup>8</sup>

```
NNODES=$SLURM_JOB_NUM_NODES
srun --nodes="$NNODES" --ntasks="$NNODES" --ntasks-per-node=1 \
    dcgmi diag -r 1 --fail-early
```

If every node passes, proceed to the communication test. If a node fails, keep its diagnostic output and investigate it before proceeding. For example, a level 2 diagnostic reported thermal violations alongside failed PCIe and memory tests on three GPUs in one of our nodes.

Longer diagnostics belong in a separate maintenance window. NVIDIA describes levels 3 and 4 as administrator post-mortem tests, whereas level 1 is a readiness check.<sup>8</sup>

##### Prepare the diagnostic image

If your cluster already provides an `nccl-tests` image, set `NCCL_TESTS_IMAGE` to its path. Otherwise, on AWS with EFA you can import the public image maintained with the [AWS NCCL test recipes](https://github.com/awslabs/awsome-distributed-ai/tree/main/micro-benchmarks/nccl-tests). Choose a destination on a filesystem accessible to the allocated nodes:<sup>9</sup>

```
NCCL_TESTS_IMAGE=/shared/images/nccl-tests.sqsh
mkdir -p "$(dirname "$NCCL_TESTS_IMAGE")"
enroot import -o "$NCCL_TESTS_IMAGE" \
    'docker://public.ecr.aws#hpc-cloud/nccl-tests:latest'
```

Keep the imported SquashFS file with your baseline, since importing `latest` again can give you a different image. For a repeatable import, select a versioned tag from the AWS recipe in place of `latest`.<sup>10,9</sup>

The AWS recipe also provides a Dockerfile if you need to build the image. For another fabric, use its supported CUDA, [NCCL](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=nccl), MPI and network-plugin stack; NVIDIA's [nccl-tests build instructions](https://github.com/NVIDIA/nccl-tests#build) explain how to select those library paths. Multi-node tests require a build with `MPI=1`. The benchmark below assumes that MPI can launch through Slurm's PMIx integration, so match the image to the cluster's MPI setup.<sup>11</sup>

##### Measure the collective you will use

Once the nodes pass, measure all-to-all bandwidth across the allocation. The command below launches one rank per GPU and exchanges an 8 GiB buffer per rank, matching the large-message test used for our baseline. Use the `NCCL_TESTS_IMAGE` path prepared above, adjusting the executable path if your image installs `nccl-tests` elsewhere.

```
srun --nodes="$NNODES" --ntasks="$((8 * NNODES))" \
    --ntasks-per-node=8 --gres=gpu:8 --mpi=pmix --cpu-bind=none \
    --container-image="$NCCL_TESTS_IMAGE" --no-container-mount-home \
    /opt/nccl-tests/build/alltoall_perf \
    -b 8G -e 8G -g 1 -c 1 -n 20
```

Check the rank listing before reading the result: an allocation of two eight-GPU nodes should list 16 ranks. Then inspect the `busbw` and `#wrong` columns for the tested size. Here is the out-of-place result from our two-node baseline, with the other columns omitted:

```
size (B)      busbw (GB/s)    #wrong
8589934592    77.14           0
```

The zero in `#wrong` means the correctness check passed for that result. The bandwidth gives you a reference for subsequent allocations with the same node count, GPUs per node and test settings. Keep the node list with it so that a later slow result can be traced back to the machines involved. In a separate two-node allocation, run with NCCL tuning variables set, the same message size reached 39.84 GB/s, so record which nodes and settings produced each baseline.

All-reduce remains useful as a comparison, but the two collectives can behave very differently on the same machines. That slower two-node test delivered 398.52 GB/s for all-reduce alongside its 39.84 GB/s all-to-all result. For an MoE that exchanges tokens across those nodes, the second measurement is the one that tests the relevant communication pattern.

##### Choose a baseline for each allocation size

As you add nodes, more of an all-to-all exchange crosses the inter-node network. Our multi-node sweep shows why the baseline must depend on node count: it reached 77.14 GB/s on two nodes, 39.25 GB/s on four, and 30.91 GB/s on eight. Compare each allocation with a baseline at its own node count, using the same message size and the same result column.

Before choosing a reference, repeat the check on a known-good configuration with the hardware, software and test settings held fixed. Use the resulting range to decide whether a new allocation is ready for training. A practical starting policy is to require 90% of the baseline bandwidth and a passing correctness check. With the two-node result above, the bandwidth threshold would be about 69 GB/s. Adjust the threshold to your cluster's observed variability. A fixed 33 GB/s threshold, for example, would accept the slow two-node result while rejecting the eight-node sweep result.

Keep this baseline unchanged while you investigate a slow allocation. If you also want to try NCCL tuning variables, compare the settings on the same nodes with the same test parameters. Our default and tuned runs used different node pairs, so their bandwidth difference cannot identify the effect of those variables.

##### Check for changes during training

For periodic hardware checks during training, use Megatron's `--gpu-sniff-test-interval <n>`. It runs before training and every `n` iterations ([`training.py#L4850-L4852`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/training.py#L4850-L4852), [`training.py#L4484-L4489`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/training.py#L4484-L4489)), including an all-to-all over the expert-parallel group ([`gpu_sniff_test.py#L5-L21`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/gpu_sniff_test.py#L5-L21)). Its outlier warnings identify ranks to investigate when a slowdown appears ([`gpu_sniff_test.py#L104-L118`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/gpu_sniff_test.py#L104-L118)).

The diagnostic image has let you test the GPUs and their links. Your training image needs access to the same hardware, so let's prepare it and check its network libraries.

#### 2.2 Build your image

A training environment has two parts to get right: the libraries that run GPU computations, and the network libraries that connect those GPUs across nodes. We start from an NVIDIA PyTorch container for the first part, then add the network support required by the cluster. Keeping [Megatron](https://github.com/NVIDIA/Megatron-LM) in a separate checkout lets you change the training code while retaining the same image.

The examples here use [Enroot](https://github.com/NVIDIA/enroot) and [Pyxis](https://github.com/NVIDIA/pyxis) on [Slurm](https://slurm.schedmd.com/). The base image is [NGC PyTorch](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch) `26.06-py3`; the network-specific instructions apply to our AWS P5 nodes with EFA. On another cluster, use its supported network stack for that part of the image.<sup>3,4</sup>

##### Import the base image

Enroot imports a container image into a SquashFS file that Pyxis can launch through `srun`. Choose an output path accessible from your compute nodes, then import the base image:<sup>4</sup>

```
IMAGE=/path/to/images/pytorch-26.06.sqsh
enroot import -o "$IMAGE" docker://nvcr.io#nvidia/pytorch:26.06-py3
```

Keep the Megatron checkout outside this image and mount it into the container when you launch training. The flags in this post target commit `d6316eb45`; checking it out explicitly makes the code you read alongside the examples match the code you run. The source notes list the image and commit used for each measurement.

Put this checkout, and later the data and tokenizer, on a filesystem that both the CPU workers and GPU nodes can read. In the commands below, `SHARED_ROOT` is that directory and `PROJECT_DIR` is your project directory, with the [companion scripts](https://gist.github.com/nmntz/5de952d686f66d7bce5bce8cba9d7139) cloned into its `scripts/` folder.

```
export SHARED_ROOT=/path/to/shared/work
export PROJECT_DIR="$SHARED_ROOT/moe-blogpost"
git clone https://gist.github.com/nmntz/5de952d686f66d7bce5bce8cba9d7139.git "$PROJECT_DIR/scripts"
git clone https://github.com/NVIDIA/Megatron-LM.git "$SHARED_ROOT/Megatron-LM"
cd "$SHARED_ROOT/Megatron-LM"
git checkout d6316eb45bf1bfbb6f1f848c0b56e55166564d80
```

##### Verify GPU access

Before adding the cluster's network libraries, check that the base image can import PyTorch and [Transformer Engine](https://github.com/NVIDIA/TransformerEngine) and see the GPUs. Run this inside an allocated eight-GPU node, using the `IMAGE` path from above:

```
srun --nodes=1 --ntasks=1 --gres=gpu:8 \
    --container-image="$IMAGE" --no-container-mount-home \
    python -c '
import torch, transformer_engine
print("torch", torch.__version__)
print("transformer_engine", transformer_engine.__version__)
print("device_count", torch.cuda.device_count())
x = torch.randn(8).cuda().sum()
print("cuda sum ok", x.item())
'
```

The stock image reported the following versions and device count. The final line of the command also prints a sum computed on the GPU, so inspect that result along with the imports before proceeding.

```
torch 2.13.0a0+8145d630e8.nv26.06
transformer_engine 2.16.0+4220403e
device_count 8
```

The CUDA result checks execution on the GPU within this node. For EFA communication across nodes, add the network plugin and its dependencies described below.

##### Add EFA support

On our AWS nodes, the network layer consists of the EFA userspace libraries and the `aws-ofi-nccl` plugin built against the NCCL inside the image. The build used EFA installer `1.49.0` and `aws-ofi-nccl` `v1.19.2`. Record both versions alongside the base image in your build recipe.

The [EFA image build script](https://gist.github.com/nmntz/5de952d686f66d7bce5bce8cba9d7139#file-build_efa_image-sh) creates a writable Enroot container from the base image, installs the EFA userspace libraries with `--skip-kmod`, and compiles the plugin against the image's NCCL. It then exports a new SquashFS image and removes the temporary container. Run it on an allocated compute node with Enroot and GPU access, choosing a new output path:

```
EFA_IMAGE=/path/to/images/pytorch-26.06-efa.sqsh
bash "$PROJECT_DIR/scripts/build_efa_image.sh" "$IMAGE" "$EFA_IMAGE"
```

Use `EFA_IMAGE` as the `--container-image` path for subsequent training launches. The script prepares the network layer; keep the following environment settings with that image so the job can find and select its libraries.

Here, the library paths refer to the copies installed inside the container, and `NCCL_NET_PLUGIN=ofi` selects the plugin by name. Passing a filesystem path as the plugin value caused NCCL to construct an invalid library name in our setup.

```
export LD_LIBRARY_PATH=/opt/amazon/ofi-nccl/lib:/opt/amazon/efa/lib:${LD_LIBRARY_PATH:-}
export NCCL_NET_PLUGIN=ofi
export FI_PROVIDER=efa
export FI_EFA_USE_DEVICE_RDMA=1
export NCCL_SOCKET_IFNAME='^lo,docker0,veth_def_agent'
export NCCL_DEBUG=INFO
```

The socket interface exclusion addresses the initial connection NCCL uses to set up communication. On our nodes, NCCL selected `veth_def_agent`, tried to connect to its link-local address, and failed with `Connection refused`. Excluding that interface allowed the launch to proceed. Adapt the exclusion list to your cluster's interfaces before reusing it.

##### Verify the network path

On your first multi-node training launch, inspect the NCCL initialization log before interpreting training performance. This checks the network path from the training image itself. For the EFA image described here, the line to look for is:

```
NCCL INFO Using network Libfabric
```

If you see `Using network Socket` instead, read the plugin-loading messages immediately above it. An invalid plugin name or a missing library version can leave NCCL using sockets. For example, the `EFA_1.4` error identifies a missing library version to resolve before trying again.

The log confirms which transport the job selected; measuring its bandwidth remains a separate check. Record the training image and network settings alongside the diagnostic result from [2.1](#s-2-1), keeping the two environments explicit when comparing their performance.

With the hardware checked and the image prepared, we can turn to the first training run. It starts with the data: turning raw text into token sequences and storing them in the format Megatron expects.

#### 2.3 Tokenize

[Megatron](https://github.com/NVIDIA/Megatron-LM) reads training text from pairs of indexed files. The `.bin` file stores token IDs, while the `.idx` file tells the loader where each sequence begins and ends. Preparing these files once lets the dense and MoE runs read the same tokens, so changing the model does not also change the data.

We will use [FineWeb-Edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) and the [Llama 3.2 tokenizer](https://huggingface.co/meta-llama/Llama-3.2-1B). [Datatrove](https://github.com/huggingface/datatrove)'s `MegatronDocumentTokenizer` writes the format directly; the remaining work is to choose an output directory, check a small sample, and submit the larger tokenization job.

*Figure caption:* **Figure 2.3.1**: Two illustrative documents stored as token IDs, each ending with an end-of-document token

##### Prepare the tokenizer

Keep the data and tokenizer under `SHARED_ROOT`, the shared directory from [2.2](#s-2-2). The [tokenization script](https://gist.github.com/nmntz/5de952d686f66d7bce5bce8cba9d7139#file-tokenize_first_run-py) runs locally for the sample and submits a [Slurm](https://slurm.schedmd.com/) array for the larger job.

```
export TOKENIZER_DIR="$SHARED_ROOT/tokenizer"
python3.11 -m venv "$SHARED_ROOT/tokenize-venv"
source "$SHARED_ROOT/tokenize-venv/bin/activate"
python -m pip install \
    'datatrove @ git+https://github.com/huggingface/datatrove.git@2c895af7a95010a96fa53e2dc77cc0ce92799e3f' \
    pyarrow tokenizers huggingface_hub
```

The original tokenizer repository, `meta-llama/Llama-3.2-1B`, requires access approval. If your account has access, run `hf auth login` and use that repository in the download command. Otherwise, `unsloth/Llama-3.2-1B` provides an ungated copy: our comparison found matching vocabulary and token IDs. Both tokenization and training will read the same downloaded tokenizer files.<sup>12</sup>

```
TOKENIZER_REPO=unsloth/Llama-3.2-1B
hf download "$TOKENIZER_REPO" \
    --include 'tokenizer*' --include 'special_tokens_map.json' --include 'config.json' \
    --local-dir "$TOKENIZER_DIR"
```

Datatrove reads `tokenizer.json` from this directory and appends `<|end_of_text|>` after each document. Megatron later receives the directory through `--tokenizer-model`, which also gives it the tokenizer's configuration.

##### Check a small shard

Tokenize a small sample on a CPU compute node before submitting the full array. This command reads up to 1,000 documents and keeps them all, writing the result to a separate directory so the sample cannot be mistaken for the training corpus.

```
python "$PROJECT_DIR/scripts/tokenize_first_run.py" \
    --tokenizer "$TOKENIZER_DIR/tokenizer.json" \
    --output "$SHARED_ROOT/data-smoke" --limit 1000
```

The output prefix is `fineweb-edu_00000_tokens`. Check it with Megatron's own reader inside the training image from [2.2](#s-2-2), using an allocation where [Pyxis](https://github.com/NVIDIA/pyxis) can launch the container. Deactivate the tokenization environment first so its Python does not override the image's interpreter. Set `TRAIN_IMAGE` to `EFA_IMAGE` on the EFA setup, or to the prepared training image for your cluster.

```
deactivate
export TRAIN_IMAGE="$EFA_IMAGE"
export MEGATRON_PATH="$SHARED_ROOT/Megatron-LM"
srun --nodes=1 --ntasks=1 \
    --container-image="$TRAIN_IMAGE" \
    --container-mounts="$SHARED_ROOT:$SHARED_ROOT" \
    --container-workdir="$MEGATRON_PATH" --no-container-mount-home \
    env PYTHONPATH="$MEGATRON_PATH" python -c '
import sys
from megatron.core.datasets.indexed_dataset import IndexedDataset
data = IndexedDataset(sys.argv[1])
assert len(data) > 0
print("sequences", len(data))
for i in range(min(3, len(data))):
    tokens = data[i]
    assert len(tokens) and tokens[-1] == 128001
    print("length", len(tokens), "last token", int(tokens[-1]))
' "$SHARED_ROOT/data-smoke/fineweb-edu_00000_tokens"
```

You should see a nonzero sequence count and `last token 128001` for each inspected sequence. That final token is the document boundary we asked the tokenizer to append. Reading the shard through Megatron also checks that Megatron can parse the index and read the first sequences from the token file before GPU training starts.

##### Submit the tokenization job

The sample checks the file format; the larger job prepares a corpus to reuse as your training runs grow. Submit it from the login node with the same virtual environment activated. Set `CPU_PARTITION` to your cluster's CPU partition; add `--qos` if the scheduler requires one. The script requests 12 CPUs and 24 GB of memory per task, and the virtual environment must be accessible at the same path on those workers.

```
source "$SHARED_ROOT/tokenize-venv/bin/activate"
export OUT_DIR="$SHARED_ROOT/data/fineweb-edu"
CPU_PARTITION=your_cpu_partition
python "$PROJECT_DIR/scripts/tokenize_first_run.py" \
    --tokenizer "$TOKENIZER_DIR/tokenizer.json" --output "$OUT_DIR" \
    --tasks 100 --limit -1 --sample-rate 0.074 --partition "$CPU_PARTITION"
```

Datatrove prints the submitted job ID. Use that ID with `squeue -j <job-id>` to follow the array, and inspect failed tasks under `$OUT_DIR/logs` before relaunching the same command.

Each task reads a share of the input files and keeps a random 7.4% of the documents before tokenizing them. Because documents have different lengths, this fraction does not fix the number of tokens in the output. Keep the task count, sampling rate and output directory unchanged when restarting an interrupted job. Datatrove uses completion markers under the logging directory to skip finished tasks.<sup>13</sup>

##### Pass the shards to Megatron

Wait for the array to finish before building the training manifest. The following check requires all 100 task-completion markers and expected shard pairs and writes the shard prefixes to `data-args.txt`, one per line. Each prefix names both files, so neither `.bin` nor `.idx` belongs in the manifest.

```
export DATA_ARGS="$OUT_DIR/data-args.txt"
python - <<'PY'
import os
from pathlib import Path
root = Path(os.environ["OUT_DIR"])
prefixes = [root / f"fineweb-edu_{rank:05d}_tokens" for rank in range(100)]
for rank, prefix in enumerate(prefixes):
    assert (root / "logs/completions" / f"{rank:05d}").is_file(), rank
    for suffix in (".bin", ".idx"):
        path = Path(str(prefix) + suffix)
        assert path.is_file() and path.stat().st_size > 0, path
Path(os.environ["DATA_ARGS"]).write_text("\n".join(map(str, prefixes)) + "\n")
print(f"wrote {len(prefixes)} prefixes")
PY
deactivate
```

Training will read this file through `--data-args-path`. That option supplies the same list as `--data-path`, but keeps a long set of shards out of the launch command. The launcher also sets `--data-cache-path` to a persistent directory for Megatron's sample indices, allowing later runs with the same dataset configuration to reuse them.

For the first runs we use `--split 100,0,0`, assigning the data to training. Reserve a held-out split before using the run to compare model quality.

With a readable dataset and a manifest pointing to its shards, you can launch the dense baseline. Its loss, gradient norms and step times will establish a reference before we introduce experts.

#### 2.4 Dense baseline

A dense run gives you something concrete to compare with when the MoE behaves unexpectedly. Both models will use the same data, batch size and optimizer, so a loss spike or a slow step can first be checked against the simpler model. This baseline also exercises the training image and data loader together before routing enters the picture.

The model has 16 transformer layers, a hidden size of 2,048 and an 8,192-wide feed-forward network. With the 128,256-entry vocabulary, it contains about 1.22 billion parameters. The recipe targets one node with eight GPUs with roughly 80 GB of memory each. We will reuse the launch script for the MoE.

##### Launch on one node

We will use [Trackio](https://huggingface.co/docs/trackio) to record the training metrics. Trackio is a lightweight, open-source experiment tracker from Hugging Face. Its API mirrors `wandb`, so `import trackio as wandb` is usually the only change existing code needs. Runs are logged to a local database you own, and you can browse them in a local dashboard or sync them to a Hugging Face Space to share live curves with your team, with no account or paid plan required.<sup>14</sup>

First, create a Python environment on shared storage from inside the training image. It inherits the image's GPU libraries and adds the pinned tracking package:

```
srun --nodes=1 --ntasks=1 \
    --container-image="$TRAIN_IMAGE" \
    --container-mounts="$SHARED_ROOT:$SHARED_ROOT" --no-container-mount-home \
    bash -c 'python -m venv --system-site-packages "$1/train-venv" &&
        "$1/train-venv/bin/python" -m pip install "trackio==0.42.0"' _ "$SHARED_ROOT"
export TRACKIO_PROJECT=moe-first-run
```

The launcher uses the [Trackio entry point](https://gist.github.com/nmntz/5de952d686f66d7bce5bce8cba9d7139#file-pretrain_trackio-py) to send [Megatron](https://github.com/NVIDIA/Megatron-LM)'s scalar metrics to one run per job. Both runs share the project above, with their data stored under `$SHARED_ROOT/trackio`. The adapter uses Megatron's existing scalar-logging hooks, so flags such as `--log-memory-to-tensorboard` control which metrics reach Trackio.

The [first-run script](https://gist.github.com/nmntz/5de952d686f66d7bce5bce8cba9d7139#file-first_run-sbatch) groups the training flags into Bash arrays. It uses the training image, pinned Megatron checkout, tokenizer directory and data manifest prepared in the previous sections. Keep the mounted paths under `SHARED_ROOT` and set `TRAIN_IMAGE` to the prepared SquashFS image.

From the shared blog checkout, submit the dense job to your GPU partition. Keep the variables from [2.3](#s-2-3) exported when you submit the job. The script records the image path, Megatron commit and data manifest with its output.

```
cd "$PROJECT_DIR"
GPU_PARTITION=your_gpu_partition
sbatch --partition="$GPU_PARTITION" scripts/first_run.sbatch dense
```

[Slurm](https://slurm.schedmd.com/) reserves one eight-GPU node. Inside it, a single `srun` task starts `torchrun`, which launches one training process per GPU. Look for the run output under `$SHARED_ROOT/runs/dense-<job-id>` and the training log at `first-run-<job-id>.out` in the submission directory.

The initial run stops after 120 iterations. Checkpoint saving and validation are disabled for this setup check. Keep the log and Trackio data when you move on to the MoE; they are the reference for the next section.

To inspect the curves, run the dashboard on a machine that can read the saved directory, after installing `trackio==0.42.0` there. Select the dense and MoE runs in the project to compare them.

```
TRACKIO_DIR="$SHARED_ROOT/trackio" trackio show --project "$TRACKIO_PROJECT"
```

##### Understand the configuration

With tensor and [pipeline parallelism](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=pipeline_parallelism) both set to one, each GPU holds a copy of the dense model. Data parallelism distributes the batch across the eight GPUs, while the distributed optimizer and communication overlaps are enabled in both runs.

```
--tensor-model-parallel-size 1 --pipeline-model-parallel-size 1
--expert-model-parallel-size 1 --context-parallel-size 1
--use-distributed-optimizer --overlap-grad-reduce --overlap-param-gather
--micro-batch-size 8 --global-batch-size 512
```

A micro-batch contains eight sequences per GPU. Across eight GPUs, each micro-batch processes 64 sequences; eight [gradient accumulation](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=gradient_accumulation) steps produce a [global batch](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=revisiting_global_batch_size) of 512. At a sequence length of 4,096, each optimizer step consumes 2,097,152 tokens. Keeping these quantities fixed will make dense and MoE step times directly comparable.

The learning rate follows a warmup, stable, decay schedule, selected by `--lr-decay-style WSD`. It warms up to `5e-4`, holds that learning rate, then decays near the end of the configured token budget. The 120-iteration run ends during the stable phase; its stop condition does not shorten the learning-rate schedule.

Full [activation recomputation](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=activation_recomputation) keeps the starting configuration within the memory budget used for our baseline. With micro-batch size eight and the native cross-entropy implementation, the corresponding run without recomputation exhausted memory in the loss calculation. We keep recomputation in both models so that the first comparison does not mix a model change with a memory-saving change.

```
--recompute-granularity full --recompute-method uniform --recompute-num-layers 1
--cross-entropy-loss-fusion --cross-entropy-fusion-impl native
```

Keep the dense run's loss, gradient norm and step time in Trackio as your reference. When you replace the feed-forward layers with experts, these measurements will help you see how the change affects training.

#### 2.5 Your first MoE

The dense model applies the same feed-forward network to every token. In the MoE, a router chooses eight of 64 smaller experts for each token, allowing the model to hold more parameters than it uses on any one token. We choose the expert width so that the eight selected experts contain the same number of feed-forward parameters as the dense layer they replace.

This gives us a 6.86-billion-parameter model with about 1.22 billion active parameters per token. The extra capacity comes with a new cost: the tokens have to reach their selected experts, and the expert outputs have to return to the processes that need them.

![hero-dense-to-moe](https://huggingface-moe-blogpost.hf.space/viz/posters/hero-dense-to-moe.webp)

*Figure caption:* Figure 2.5.1

##### Replace the feed-forward layers

The launcher selects the MoE configuration when you pass `moe`. Submit it using the same exported paths and GPU partition as the dense run, keeping the image, checkout, tokenizer and data manifest unchanged:

```
sbatch --partition="$GPU_PARTITION" scripts/first_run.sbatch moe
```

[Expert parallelism](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=expert_parallelism) increases from one to eight, distributing the 64 experts across the node's eight GPUs. Each GPU holds eight experts, while the router selects eight experts per token from the full set.

```
--expert-model-parallel-size 8 --expert-tensor-parallel-size 1
--num-experts 64 --moe-ffn-hidden-size 1024 --moe-router-topk 8
--moe-token-dispatcher-type alltoall --moe-grouped-gemm
--moe-router-load-balancing-type aux_loss --moe-aux-loss-coeff 1e-3
--moe-router-dtype fp32 --moe-per-layer-logging
```

`alltoall` moves the routed tokens between GPUs, and grouped GEMM executes the local experts' matrix multiplications. The auxiliary loss encourages the router to distribute work across experts, with a coefficient of `1e-3`. We also compute router logits in fp32 and enable per-layer logging, giving us the initial settings and measurements that chapter 3 will examine.

Everything else stays in the common configuration, including full activation recomputation. In particular, the dense `--ffn-hidden-size 8192` setting remains in the script, while `--moe-ffn-hidden-size 1024` supplies the width of each expert.

##### Count active and total parameters

A bias-free SwiGLU expert has three weight matrices. With hidden size 2,048 and expert width 1,024, their combined size is `3 × 2048 × 1024 = 6,291,456` parameters. Selecting eight experts therefore uses 50,331,648 feed-forward parameters per token, matching the dense layer's `3 × 2048 × 8192` parameters.

*Figure caption:* **Figure 2.5.2**: The dense feed-forward layer and the 64 experts drawn to the same scale. A token's eight experts, placed end to end, are exactly as wide as the dense layer: the same active parameters, out of eight times as many stored

All 64 experts together contain eight times as many feed-forward parameters. The whole model grows by a smaller factor because attention, embeddings and the other non-expert parameters stay the same size, and each layer gains a small router matrix. Summing those components across 16 layers gives 6.86 billion total parameters and 1.221 billion active parameters, compared with 1.219 billion in the dense model.

The result is about 5.6 times as many total parameters at nearly the same active parameter count. Matching active parameter counts does not guarantee equal step time: distributing tokens among experts changes how the GPU work is organized and introduces communication.

##### Keep a dense reference

An MoE with one expert and top-1 routing computes the same function as the dense model it came from, so it should train like it. In our run, a 1-expert MoE upcycled from a dense checkpoint and continued beside the dense run stayed within 0.00087 of it over 15 aligned steps. Start the MoE from its own initialization instead and the comparison says little, since the two runs sit 2.72 apart at iteration 4. The MoE side also logs a load-balancing loss of exactly 1 and about 32,770 zeros in its gradient against at most 17 for the dense run: the router weights, which get no gradient with a single expert. The parity run upcycles the dense checkpoint, a path [3.6](#s-3-6) returns to.

![sanity-checks](https://huggingface-moe-blogpost.hf.space/viz/posters/sanity-checks.webp)

*Figure caption:* Figure 2.5.3

At the pin, that upcycling path ran for us only with two local fixes to `training.py`. The first passes the dense model to the checkpoint loader under the keyword `model` ([`training.py#L3074-L3078`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/training.py#L3074-L3078)), while [`load_checkpoint`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/checkpointing.py#L2632-L2634) names that parameter `ddp_model`. The second concerns the dense model built for the load: the upcycling code switches the dense shape on in `args` ([`training.py#L3056-L3062`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/training.py#L3056-L3062)), but the model builder reads the model configuration stored at startup ([`training.py#L2917-L2926`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/training.py#L2917-L2926)), so that model keeps the MoE layer layout and the load stops on a missing `pre_mlp_layernorm` key.

Deterministic mode makes a run repeatable, so that a gap between two runs means something. At the pin, `--deterministic-mode` requires cross-entropy loss fusion, TP communication overlap and the fused aux-loss kernel to be off ([`determinism.py#L28-L37`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/determinism.py#L28-L37), [`determinism.py#L195-L210`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/determinism.py#L195-L210)), and accepts `NVTE_ALLOW_NONDETERMINISTIC_ALGO` only at `0` ([`determinism.py#L85-L90`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/determinism.py#L85-L90)); it sets `NCCL_ALGO=Ring`, `NCCL_EP_HT_EM_AG_SCAN_MODE=1`, `NVTE_ALLOW_NONDETERMINISTIC_ALGO=0` and `CUBLAS_WORKSPACE_CONFIG=:4096:8` itself when they are unset ([`determinism.py#L40-L50`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/determinism.py#L40-L50)). The [2.4](#s-2-4) launcher passes `--cross-entropy-loss-fusion` and exports `NVTE_ALLOW_NONDETERMINISTIC_ALGO=1`, so drop both before adding the flag. With these settings, two runs of this MoE shrunk to micro-batch 2, global batch 64 and 12 iterations printed the same lm loss, load-balancing loss, grad norm and gradient zeros at every iteration; without them the lm loss differed from the first iteration on, by up to 0.00063.

> **Recommendation:** Switch on deterministic mode before you compare two runs or chase a NaN.

Keep the dense run and its configuration as a reference as you develop the MoE. Whenever a change makes training slower or the loss stops improving, return to the dense run in [Trackio](https://huggingface.co/docs/trackio) and compare step time, loss and gradient norm at the same batch size and sequence length. A problem that appears in both runs points you toward their shared setup; one that appears only in the MoE gives you a reason to investigate routing and expert execution.

![Measured router statistics](https://huggingface-moe-blogpost.hf.space/figures/trackio-demo.png)

*Figure caption:* **Figure 2.5.4**: Trackio with synthetic dense and MoE runs. These curves illustrate the interface, not measured training performance

The dense reference helps you decide where to begin an investigation. Chapter 3 opens the MoE layer piece by piece, introducing the measurements you need to understand its behavior.

### 3. Anatomy of MoE Training

The MoE from [2.5](#s-2-5) added parts the dense run never had: a router that picks eight experts for each token, experts that can end up with very different amounts of work, and an all-to-all that moves tokens between GPUs. Each of them can slow training or hurt the loss, and a gap against the dense reference does not, on its own, tell you which part caused it.

The figure below draws one MoE layer at a smaller scale than ours, with 16 experts and top-4 instead of 64 and top-8, plus a shared expert that ours does not have. It shows the tokens of a batch, the router, the experts and the sum that combines their outputs. Each section then opens on its own view of the same drawing, zoomed onto the part it covers, so you can skip to the part you need. A few views also carry a result from their section, such as the rogue experts that Step [3.5](#s-3-5) Flash's training loss did not reveal ([3.6](#s-3-6))<sup>15</sup>.

![hero-anatomy-zoom](https://huggingface-moe-blogpost.hf.space/viz/posters/hero-anatomy-zoom.webp)

*Figure caption:* Figure 3

After the monitoring setup in [3.0](#s-3-0), we start inside the router, with how its scores become the weights of the chosen experts and whether tokens choose experts or experts choose tokens. Then come uneven load across experts, how many experts to use and how large, which layers get experts at all, and how to start a run and keep it stable. We end with where a training step spends its time on the GPUs.

#### 3.0 Monitoring: turn it on once

Before changing any setting, turn on what tells you whether it worked. You do not need to know what every number means yet: each section introduces a metric when it first needs it (z-loss in [3.1](#s-3-1), MaxVio in [3.2](#s-3-2), timings and memory in [3.7](#s-3-7)). Appendix [A.1](#s-a-1) gives the capture commands, calculations and limits of each measurement.

##### What to turn on

The [2.5](#s-2-5) run already logs the router losses per layer (`--moe-per-layer-logging`), so you can see which layer misbehaves ([3.1](#s-3-1), [3.3](#s-3-3), [A.1](#s-a-1)). Keep the [Trackio](https://huggingface.co/docs/trackio) launcher from [2.4](#s-2-4) and add these flags to the [2.5](#s-2-5) flags:

```
--save <dir> --save-interval <m>
--save-tokens-per-expert-interval <n>
--log-throughput --log-params-norm
--log-num-zeros-in-grad --log-max-attention-logit
```

Megatron writes the token counts and the activation dump below under `--save` ([`training.py#L3398-L3401`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/training.py#L3398-L3401)) and asks for `--save-interval` beside it ([`arguments.py#L1321-L1323`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/arguments.py#L1321-L1323)), so the run also saves checkpoints there. The next flag records how many tokens each expert received ([3.3](#s-3-3), [A.1](#s-a-1)). The other four track the run's health: throughput, the parameter norm, the zeros in the gradient and the largest attention logit ([3.6](#s-3-6), [A.1](#s-a-1)). The scalar metrics appear in the same Trackio project as your baseline, while routing captures stay in their own files. The NaN check is already on ([`arguments.py#L2825-L2827`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/arguments.py#L2825-L2827)).

##### What to capture when you need it

Two more measurements are bounded captures: run them when a question calls for them.

The routing trace records which experts each token picked ([3.1](#s-3-1), [3.3](#s-3-3), [A.1](#s-a-1)). Its hooks on the routers do not fire under CUDA graph replay ([`router_trace.py#L23`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router_trace.py#L23)), and by default it traces every iteration ([`training_config.py#L363-L367`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/config/training_config.py#L363-L367)), so turn graphs off and bound it:

```
--moe-routing-trace-path <dir> --moe-routing-trace-max-training-iters <n>
--cuda-graph-impl none
```

The activation dump saves the experts' activations under the same `--save` directory, so you can compute per-expert activation norms offline ([3.4](#s-3-4), [A.1](#s-a-1)):

```
--save-activations-interval <n>
```

With monitoring on, let's start where every token starts: the router. It picks the experts, but how much does each one count in the token's output?

#### 3.1 Router scoring: how logits become weights

![hero-anatomy-zoom](https://huggingface-moe-blogpost.hf.space/viz/posters/hero-anatomy-zoom.webp)

The router turns each token into one logit per expert, and in plain top-k routing the top-k logits pick the experts the token goes to. Between those logits and the weights that mix the experts' outputs sit four choices. The gating function, the output scale (a constant multiplied onto the weighted sum of the chosen experts' outputs) and the sharpness (how peaked the router's scores are, so how much the top expert dominates) change how much each chosen expert counts in the token's output, and how large that output is. In plain top-k routing, for a given token's logits, none of them changes which experts win: each keeps the experts in the same order, or applies after the top-k.

Precision is the exception. A [bf16](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=fp16_and_bf16_training) router can round two close logits to the same value and so change the winners, which makes an fp32 router the one setting to always use here.

The table below shows what ten current open MoEs chose for each of the four, one row per model.

*Table note:* how current open MoEs set up their routers, one column per part of this section. Values come from each model's `config.json` and modeling code, training precision from its tech report; √k is computed, and shown wherever the weights sum to 1.

| Model | Gating function | Output scale | Sharpness | Router precision: in training; in inference code |
| --- | --- | --- | --- | --- |
| DeepSeek-V4.1-Flash | sqrt(softplus) | renormalized, 1.5 at k = 6 (√k = 2.45) | a temperature setting, left at 1.0<sup>16</sup> | not stated; fp32<sup>16</sup> |
| Gemma 4 26B-A4B | softmax | renormalized, then a learned per-expert scale, k = 8 of 128 (√k = 2.83)<sup>17</sup> | normalized router input: RMSNorm, a learned scale and 1/√d<sup>17</sup> | not stated; bf16, softmax in fp32<sup>17</sup> |
| GLM-5.3 | sigmoid | renormalized, [2.5](#s-2-5) at k = 8 (√k = 2.83) | none | not stated; fp32<sup>18</sup> |
| Inkling | sigmoid, normalized jointly over the top-6 and its 2 shared experts<sup>19</sup> | 8.0 times a learned global scale, over 6 routed plus 2 shared (√8 = 2.83)<sup>19</sup> | none | not stated; bf16<sup>19</sup> |
| Kimi K3 | sigmoid | renormalized, 1.0 at k = 16 of 896 (√k = 4)<sup>20</sup> | none | above MXFP4 in post-training QAT<sup>21</sup>; fp32<sup>20</sup> |
| MiMo-V2.6-Pro-RL | sigmoid | renormalized, no factor at k = 8 (√k = 2.83) | none | not stated; fp32<sup>22</sup> |
| North-Mini-Code | sigmoid | not renormalized: the weights are the raw scores, k = 8 of 128<sup>23</sup> | none | not stated; bf16<sup>23</sup> |
| Qwen3.8-Flash-Next | softmax<sup>24</sup> | renormalized, no factor at k = 10 (√k = 3.16)<sup>24</sup> | none | not stated; bf16, softmax in fp32<sup>24</sup> |
| Step-5-Preview | sigmoid<sup>25</sup> | renormalized, [3.0](#s-3-0) at k = 8 of 352 (√k = 2.83)<sup>25</sup> | none | not stated; fp32<sup>25</sup> |
| ZAYA1-8B | softmax over an MLP router's logits<sup>26</sup> | not renormalized, top-1 of 16 plus a skip expert<sup>26</sup> | none | softmax in fp32 during RL; bf16<sup>26</sup> |

Let's start with the gating function. If it never changes the winners, what does it change?

##### Gating function

Softmax, sigmoid and sqrt(softplus) rank the experts the same way, so what differs is the weight each chosen expert gets. The figure below raises one token's logits from an unsure router to a confident one: softmax makes the top expert count more and more, while sigmoid saturates at large logits, so confident experts end up with equal weights. Gating functions keep the ranking when selection uses their scores alone. The expert bias of [3.3](#s-3-3) is added to the gated scores before selection ([`moe_utils.py#L936-L938`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L936-L938)), so how far it moves an expert depends on the size of the scores, and a different gating function can change the top-k. Group-limited routing ([3.7](#s-3-7)) can too, because it picks groups by summing their best scores ([`moe_utils.py#L712-L715`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L712-L715)).

![router-score-shape](https://huggingface-moe-blogpost.hf.space/viz/posters/router-score-shape.webp)

*Figure caption:* Figure 3.1.1

In the figure, sqrt(softplus) lands between softmax and sigmoid: for positive logits, the ratio of two weights tends to the square root of the ratio of their logits as the scale grows. DeepSeek-V4 switched to sqrt(softplus) from sigmoid<sup>27</sup>. In [Megatron](https://github.com/NVIDIA/Megatron-LM), the expert bias of [3.3](#s-3-3) needs sigmoid or sqrt(softplus): it refuses the bias with softmax at startup ([`transformer_config.py#L3139-L3147`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L3139-L3147)), and its softmax path never adds it. Wang et al., who proposed the bias<sup>28</sup>, explain why it fits softmax badly: softmax's normalization makes the gap between two experts depend on every other expert's score, so the bias is harder to tune. They still balanced a softmax router with it<sup>28</sup>. The auxiliary loss works with all three ([`moe_utils.py#L998-L1014`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L998-L1014)).

*Collapsible:* Megatron source

*Collapsible:* [`moe_utils.py#L913-L927`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L913-L927) (softmax, before or after top-k)

```
if score_function == "softmax":
    if use_pre_softmax:
        scores = torch.softmax(logits, dim=-1, dtype=torch.float32)
        if precomputed_indices is not None:
            top_indices = precomputed_indices
            probs = torch.gather(scores, dim=1, index=top_indices)
        else:
            probs, top_indices = compute_topk(scores, topk, num_groups, group_topk)
    else:
        if precomputed_indices is not None:
            top_indices = precomputed_indices
            scores = torch.gather(logits, dim=1, index=top_indices)
        else:
            scores, top_indices = compute_topk(logits, topk, num_groups, group_topk)
        probs = torch.softmax(scores, dim=-1, dtype=torch.float32)
```

*Collapsible:* [`moe_utils.py#L928-L941`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L928-L941)

```
elif score_function in ("sigmoid", "sqrtsoftplus"):
    if score_function == "sigmoid":
        scores = torch.sigmoid(logits.float())
    else:
        scores = torch.nn.functional.softplus(logits.float()).sqrt()
    if precomputed_indices is not None:
        top_indices = precomputed_indices
        scores = torch.gather(scores, dim=1, index=top_indices)
    elif expert_bias is not None:
        scores_for_routing = scores + expert_bias.float()
        _, top_indices = compute_topk(scores_for_routing, topk, num_groups, group_topk)
        scores = torch.gather(scores, dim=1, index=top_indices)
    else:
        scores, top_indices = compute_topk(scores, topk, num_groups, group_topk)
```

(sigmoid, sqrt(softplus), bias only selects),

*Collapsible:* [`transformer_config.py#L3139-L3147`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L3139-L3147) (the bias refused with softmax)

```
if self.moe_router_enable_expert_bias and self.moe_router_score_function not in (
    "sigmoid",
    "sqrtsoftplus",
):
    raise ValueError(
        "Expert bias for aux-loss-free routing only supports 'sigmoid' and 'sqrtsoftplus' "
        "score functions. Please set --moe-router-score-function to 'sigmoid' or "
        "'sqrtsoftplus', or unset --moe-router-enable-expert-bias."
    )
```

> **Watch:** Sigmoid gives the chosen experts equal weights once all their logits are large and positive, which is where the simulation's scaled-up token ends: a confident router with the flat gate that Sharpness returns to. To see whether a run's router gets there, record the routing trace with its logits on ([A.1](#s-a-1)) and follow two numbers per layer: the top expert's weight, and the routing entropy, which is low when one expert takes most of the weight and high when the weights are spread.

> **Recommendation:** Use sigmoid (or sqrt(softplus)) when you balance with the expert bias ([3.3](#s-3-3)), since Megatron refuses the bias with softmax. Otherwise use softmax, Megatron's default.

The router's weights do two jobs. They pick the experts, and they are also the numbers that mix the experts' outputs: the layer returns each chosen expert's output times its weight, summed. The gating function decides how much each chosen expert counts against the others. It does not decide how much they count together: with softmax, the top-k weights sum to less than 1, by a different amount for each token, so the size of the layer's output moves with them. So how big should that combined output be?

##### Output scale

Two settings decide how big the experts' combined output is. The first is renormalization: rescale the k chosen weights so they sum to 1, and the output's size no longer moves with their sum. In Krajewski et al. renormalizing lowered validation loss from 2.219 to 2.183 at granularity 8<sup>29</sup>. Megatron renormalizes by default ([`moe_utils.py#L913-L942`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L913-L942)), and `--moe-router-pre-softmax` turns renormalization off. Softmax at top-1 requires that flag: with one expert chosen, softmax over its single logit is always 1, so the router gets no gradient ([`transformer_config.py#L3213-L3221`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L3213-L3221)).

> *Margin note:* Granularity 8: experts 8 times smaller, 8 times as many, and 8 times as many chosen per token, so parameters and compute stay the same; [3.4](#s-3-4) compares granularities.

![router-gate-gain](https://huggingface-moe-blogpost.hf.space/viz/posters/router-gate-gain.webp)

*Figure caption:* Figure 3.1.2

The simulation sweeps toy tokens from an unsure router to a confident one, with uncorrelated experts of equal RMS: without renormalization the routed output's size follows the top-k probability mass, and renormalizing keeps it between 1/√k of one expert's RMS and one expert's RMS.

The second setting is the routed scaling factor, the constant multiplied onto the result. It is needed because, even renormalized, the size of the routed output depends on how much each expert counts. With all the weight on one expert, the output has that expert's root mean square (RMS). With equal weights on k uncorrelated experts of equal RMS, it drops to 1/√k of that, and a routed scaling factor near √k restores it. DeepSeek-V3 uses [2.5](#s-2-5) at k = 8<sup>30</sup>, and Kimi K2 2.827 ≈ √8. Shipped models disagree on its value: in the table above only GLM-5.3 and Step-5-Preview stay near √k, and Kimi went from √8 in K2 to 1.0 at k = 16 in K3<sup>20</sup>. Scaling the routed output also changes its weight against the shared expert's output ([3.4](#s-3-4)).

The figure's last row scales the expert's input instead of its output: Llama 4 sends each token to one expert and multiplies the token by that expert's sigmoid score before the expert runs<sup>31</sup>. Its SwiGLU experts have no biases, so the output shrinks roughly as the score squared, and the score also softens the SiLU gate.

*Collapsible:* Megatron source

*Collapsible:* [`moe_utils.py#L942-L947`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L942-L947) (renormalize, then scale)

```
    probs = scores / (scores.sum(dim=-1, keepdim=True) + 1e-20) if topk > 1 else scores
else:
    raise ValueError(f"Invalid score_function: {score_function}")
if scaling_factor:
    probs = probs * scaling_factor
```

*Collapsible:* [`transformer_config.py#L3213-L3221`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L3213-L3221) (top-1 needs pre-softmax: softmax over one logit gives a zero gradient)

```
if (
    self.moe_router_topk == 1
    and self.moe_router_score_function == "softmax"
    and not self.moe_router_pre_softmax
    and self.moe_router_load_balancing_type != "sinkhorn"
):
    # Requires applying softmax before selecting the top-k when k is 1,
    # since softmax on a [num_tokens, 1] would yield a zero gradient.
    raise ValueError("Please use --moe-router-pre-softmax when topk is 1.")
```

> **Watch:** Without renormalization, the size of the routed output follows the top-k probability mass from token to token, the setting that gave the higher loss above, so the number to watch is how large the routed output is for each token, the root of the sum of its squared weights. Compute it offline from the routing trace ([A.1](#s-a-1)).

> **Recommendation:** Keep renormalization on at top-k > 1, and use `--moe-router-pre-softmax` for softmax at top-1, or the router gets no gradient. The routed scaling factor has no settled value: √k restores the routed output's RMS only for equal weights on uncorrelated experts, and shipped models disagree on its value.

Both the weights and the output's size depend on how peaked the logits are. A router can get too sharp, with one expert taking all the weight, or too flat, averaging its top-k. What sets how peaked it is?

##### Sharpness

With softmax, a linear router gets sharper as the token's norm or the router's weights grow: the logits spread apart, and the top expert takes more of the weight. The figure below compares three ways to control that against the linear router. Logit soft-capping compresses mostly the logits near its cap. Normalizing the router input removes the part that comes from the token's norm. Gating logit normalization standardizes the logits across experts<sup>32</sup>, which sets their spread to a chosen scale.

![router-temperature](https://huggingface-moe-blogpost.hf.space/viz/posters/router-temperature.webp)

*Figure caption:* Figure 3.1.3

The plain linear router in the figure sharpens as the token's norm or the router matrix grows, and soft-capping, which Grok 2 applies at 30 without renormalizing<sup>33</sup>, pulls the large-norm token's top weight back only once its logits near the cap. Normalizing the input, as Gemma 4 does<sup>17</sup>, routes both tokens alike but still sharpens as the matrix grows, and gating logit normalization is unaffected by both. Skywork-MoE used gating logit normalization against a gate so flat that the layer averages its top-k experts<sup>34</sup>. With it, training loss came out moderately lower<sup>35</sup>. Normalizing the router input was ablated only together with the expert embeddings<sup>36</sup>.

*Collapsible:* Megatron source

*Collapsible:* [`router.py#L1150-L1152`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L1150-L1152) (jitter, then plain linear gate)

```
# Apply input jitter
input = self.apply_input_jitter(input)
logits = self.gating(input)
```

*Collapsible:* [`router.py#L824-L831`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L824-L831) (multiplicative input jitter)

```
if self.config.moe_input_jitter_eps is not None:
    eps = self.config.moe_input_jitter_eps
    if self.input_jitter is None:
        self.input_jitter = torch.distributions.uniform.Uniform(
            torch.tensor(1.0 - eps, dtype=input.dtype, device=input.device),
            torch.tensor(1.0 + eps, dtype=input.dtype, device=input.device),
        ).rsample
    return input * self.input_jitter(input.shape)
```

> **Watch:** A flat gate, one that averages its top-k experts and makes the model learn worse, shows up as Max1/Max2, the top expert's weight over the second's, falling toward 1, as it did in Skywork-MoE without normalization<sup>35</sup>. Follow it per layer together with the top expert's weight, both from the routing trace ([A.1](#s-a-1)).

> **Recommendation:** If the gate goes flat, gating logit normalization fixed it in Skywork-MoE. On the router input, Megatron offers Switch-style multiplicative input jitter, `--moe-input-jitter-eps`.

Sharpness lives in the gaps between logits, and softmax ignores a shift shared by all of them. bf16 does not: if every logit drifts upward together, the values bf16 can represent get farther apart, and close experts can tie. Do those ties change which experts win?

##### Precision

Top-k orders tied experts in a way PyTorch does not specify<sup>37</sup>. The figure below simulates routing the same tokens with 64 experts and top-8 through a bf16 router, with and without z-loss, a penalty on the logits' logsumexp. Its simulated logits drift up by one shared offset, and it counts the tokens whose experts differ from what an fp32 router picks.

![router-precision](https://huggingface-moe-blogpost.hf.space/viz/posters/router-precision.webp)

*Figure caption:* Figure 3.1.4

As the simulated offset rises, the bf16 router's logits land on a coarser grid and more tokens get different experts than under fp32. Z-loss lowers the logsumexp by pushing the logits negative. At top-8 of 64 the 8th logit sits about [3.5](#s-3-5) below the logsumexp, so in the simulation it ends near −[2.2](#s-2-2) with z-loss and +[3.6](#s-3-6) without, two sizes bf16 rounds in steps of the same length, and about as many tokens change experts; only the fp32 router has no flips, since fp32 rounds 65,536 times more finely than bf16<sup>38</sup>. DeepSeek-V3.2, GLM-4.5 and Kimi K2.5 compute the router in fp32 in their inference code<sup>39</sup>. The case for fp32 rests on the training evidence, which is about stability. In Switch Transformers, a bf16 router diverged while an fp32 router trained at bf16 speed<sup>40</sup>. In ST-MoE, the router z-loss kept every run stable<sup>41</sup>. Labs rarely say what precision they train the router in: in the table above, 2 of the 10 reports mention it, and 5 of the 10 run the router's matrix multiply in bf16 in their inference code. How far below bf16 the rest of the layer can go, while the router keeps its precision, is the question [3.7 Precision](#s-3-7-precision) returns to.

*Collapsible:* Megatron source

*Collapsible:* [`router.py#L124-L130`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L124-L130) (router dtype)

```
# Convert to specified datatype for routing computation if enabled
router_dtype = input.dtype
if self.config.moe_router_dtype == 'fp32':
    router_dtype = torch.float32
elif self.config.moe_router_dtype == 'fp64':
    router_dtype = torch.float64
logits = router_gating_linear(input, self.weight, self.bias, router_dtype)
```

*Collapsible:* [`moe_utils.py#L1424-L1435`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L1424-L1435) (bf16 operands, fp32 logits)

```
if te_general_gemm is not None and router_dtype != torch.float64:
    # cuBLASLt's non-FP8 bias epilogue expects bias and output to have the same
    # dtype. Router parameters may be BF16 while router logits are FP32, so cast the
    # small bias vector before passing it to TE.
    gemm_bias = bias.to(router_dtype) if bias is not None else None
    output = te_general_gemm(weight, inp, router_dtype, layout="TN", bias=gemm_bias)[0]
elif bias is None:
    output = torch.mm(inp.to(router_dtype), weight.to(router_dtype).t())
else:
    output = torch.addmm(
        bias.to(router_dtype), inp.to(router_dtype), weight.to(router_dtype).t()
    )
```

*Collapsible:* [`moe_utils.py#L171-L184`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L171-L184) (z-loss)

```
logsum = torch.logsumexp(logits, dim=-1)
z_loss_values = torch.square(logsum)
if padding_mask is not None:
    # Invert padding_mask: True (padding) -> 0, False (valid) -> 1
    valid_mask = ~padding_mask
    # Only compute z_loss for valid (non-padding) tokens
    z_loss_values = z_loss_values * valid_mask
    # Compute mean over valid tokens only
    num_valid_tokens = valid_mask.sum()
    z_loss = z_loss_values.sum() / torch.clamp(num_valid_tokens, min=1.0) * z_loss_coeff
else:
    z_loss = torch.mean(z_loss_values) * z_loss_coeff
return z_loss
```

*Collapsible:* [`router.py#L761-L764`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L761-L764) (z-loss coefficient over TP×CP)

```
if self.config.moe_z_loss_coeff is not None and self.training and torch.is_grad_enabled():
    # Skip Z loss calculations when using torch.no_grad() or checkpointing.
    moe_z_loss_coeff = self.config.moe_z_loss_coeff / self.tp_cp_group.size()
    z_loss = z_loss_func(logits, moe_z_loss_coeff, padding_mask=padding_mask)
```

> **Watch:** A bf16 router can make training diverge, as it did in Switch Transformers, so two signals are worth following: the z-loss, which tracks how far the logits drift up, and the flip rate, the share of tokens whose experts change when the router is recomputed in fp32. Megatron logs the z-loss when `--moe-z-loss-coeff` is set, already divided by the coefficient ([`router.py#L805-L807`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L805-L807)), so its square root is the RMS logsumexp: our run logged 20.9, an RMS logsumexp of about 4.6. The flip rate needs a matched capture of the same inputs and current router state; [A.1](#s-a-1) provides a bounded live hook, since the trace's initial weight snapshot does not track later training updates.

> **Recommendation:** Always set `--moe-router-dtype fp32`. Add `--moe-z-loss-coeff 1e-3`, ST-MoE's value, to a softmax router whose logits drift up. DeepSeek-V3's report never mentions z-loss for its sigmoid router<sup>42</sup>.

##### What to watch

| Part | Symptom | Signal to watch |
| --- | --- | --- |
| Gating function |  | The top expert's weight and the routing entropy, per layer, from the routing trace with logits on ([A.1](#s-a-1)). |
| Output scale | `learns badly`: without renormalization, the routed output scales with the top-k probability mass. Renormalizing lowered the loss<sup>29</sup>. | How large each token's routed output is, √(Σ w²), from the routing trace ([A.1](#s-a-1)). |
| Sharpness | `learns badly`: when the gate is flat, the layer averages its top-k experts<sup>35</sup>. | The top expert's weight and Max1/Max2, its weight over the second expert's<sup>35</sup>, per layer, from the routing trace ([A.1](#s-a-1)). |
| Precision | `blows up`: a bf16 router diverged in Switch Transformers<sup>40</sup>. | The logged z-loss is divided by its coefficient, so its square root gives RMS logsumexp: 20.9 corresponds to about 4.6. Measure fp32 routing flips with [A.1](#s-a-1)'s matched live hook using the same inputs and current router state; the trace's initial weight snapshot cannot replay later training forwards exactly. |

So far we have shaped how a token's logits become weights. The gating function sets how much each chosen expert counts, renormalization and the scaling factor set how big their combined output is, and sharpness and precision set how peaked and how exact the scores are. All of it assumed one setup: a learned router, and the token picking its top k. Both can change: experts can pick their tokens instead, and a fixed table can replace the learned choice. Who should make the choice, the token or the expert, and does the choice need to be learned at all?

#### 3.2 Routing strategy: who selects, and how

![hero-anatomy-zoom](https://huggingface-moe-blogpost.hf.space/viz/posters/hero-anatomy-zoom.webp)

Token-choice top-k is the default: each token scores every expert and keeps its k best. This section looks at two ways to change that. The expert can pick its tokens instead of the token picking its experts, or a fixed hash can pick, with no learned router at all.

*Table note:* How current open MoEs pick their experts, and which ones look up a table by token id, with Zhou et al.'s research model as an expert-choice comparison. Current-model settings come from their `config.json` and modeling code; the expert-choice row comes from the paper<sup>43</sup>.

| Model | Who selects | Token-id lookup |
| --- | --- | --- |
| DeepSeek-V4-Pro | token choice | hash routing in the first 3 MoE layers<sup>44</sup> |
| DeepSeek-V4.1-Flash | token choice | Engram n-gram memory (2- to 4-grams) at layers 1 and 14; no hash routing<sup>45</sup> |
| EC-CF2 8B/64E (Zhou et al.)<sup>43</sup> | expert choice | none |
| GLM-5.3 | token choice | none |
| Kimi K3 | token choice | none |
| Llama 4 Maverick | token choice | none<sup>46</sup> |
| MiMo-V2.6-Pro-RL | token choice | none |
| Qwen3.8-Flash-Next | token choice | n-gram embedding (2- and 3-grams) at layer 1<sup>47</sup> |
| Step-5-Preview | token choice | none<sup>48</sup> |

Before asking whether the choice needs a learned router, we have to settle who makes it, because with token choice many tokens can want the same experts and loads skew. Should each token keep picking its experts, or should each expert pick its tokens instead?

##### Who selects

With token choice, many tokens can want the same experts, so loads skew. Expert choice flips the roles: each expert takes its best tokens, so every expert gets the same load<sup>43</sup>. The catch is future token leakage<sup>49</sup>: whether a token gets an expert depends on the tokens after it. At inference those tokens do not exist yet, so routing differs from training<sup>50</sup>.

Expert threshold, the third rule in the figure below, keeps loads near even without looking at future tokens<sup>50</sup>. In exchange, each token gets a variable number of experts. In a 575M-parameter model it reached a lower loss than token choice, with or without balancing (2.844 against about 2.89)<sup>51</sup>.

![who-picks](https://huggingface-moe-blogpost.hf.space/viz/posters/who-picks.webp)

*Figure caption:* Figure 3.2.1

In the figure, the sequence leans toward expert 1, and token choice, drawn with no balancer, overloads it. Expert choice balances the loads, but later tokens push out earlier selections, while expert threshold, whose cutoffs come from earlier batches that lean the same way, keeps the loads near the target without revising any selection, at the price of a varying number of experts per token.

*Collapsible:* Megatron source

*Collapsible:* [`moe_utils.py#L891-L897`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L891-L897) (per-token top-k, token choice only)

```
# Sorting top-k turned off during inference
return torch.topk(
    scores,
    k=topk,
    dim=1,
    sorted=torch.is_grad_enabled() or is_batch_invariant_mode_enabled(),
)
```

> **Watch:** The skew token choice leaves behind makes the step slow. It shows in the token counts, tokens per expert per layer, which `--save-tokens-per-expert-interval` logs ([A.1](#s-a-1)) and which read best as MaxVio, how far the busiest expert's load sits above the mean<sup>52</sup>.

> *Margin note:* MaxVio, short for maximal violation: (busiest expert's load minus the mean load) divided by the mean load. 0 is perfectly even; 1 means the busiest expert gets twice the average. Wang et al., who proposed the expert bias of [3.3](#s-3-3), define it.

> **Recommendation:** Use token choice, the routing [Megatron](https://github.com/NVIDIA/Megatron-LM) trains, with `--moe-router-topk` setting k.

Whether the token or the expert does the picking, the choice so far always comes from a learned router, so the routing itself has to be trained. Does routing really need to be learned, or could a simpler rule pick the experts?

##### Hash layers

In DeepSeek-V4's first 3 MoE layers, a fixed table maps each token id to its experts<sup>53</sup>, and the router is kept only for the weights<sup>54</sup>. The table is a fixed hash of the token id<sup>27</sup>, and in our probe it spreads frequent tokens no better than a random table. There is nothing to learn for the selection, and hash layers matched Switch and BASE layers in models up to 4.5B<sup>55</sup>. The figure below puts learned and hash routing side by side, above a third lookup by token id: Engram, which hashes each token's last 2 to 4 tokens into tables of embeddings and adds the rows it reads to the hidden state<sup>56</sup>. DeepSeek-V4.1-Flash keeps Engram at two layers, but picks every layer's experts with its learned router<sup>57,58</sup>.

> *Margin note:* Lewis et al.'s balanced assignment of experts, which routes by solving a linear assignment that gives every expert an equal number of tokens.

![router-authority](https://huggingface-moe-blogpost.hf.space/viz/posters/router-authority.webp)

*Figure caption:* Figure 3.2.2

The figure's two routers treat the word "the" differently: the learned router selects each one by its context, while the hash layer sends every "the" to the six experts its table row names, even past an expert with a higher score. Both rows weight their six experts to sum to V4-Flash's routed scaling factor of 1.5<sup>59</sup>, and the figure measures how alike the four "the"s' expert sets are by their mean Jaccard similarity. What the hash layer gives up is context: the same token id always selects the same experts, whatever surrounds it. It also scales worse than learned routing. Clark et al. varied how many of a model's layers are MoE layers. With a single MoE layer, hash routing reached the lowest loss of the routing methods they compared, but as more layers became MoE layers it stopped improving, while their learned router kept getting better<sup>60</sup>. And no bias can rebalance it<sup>54</sup>: frequent tokens can overload their assigned experts, and nothing moves them. V4.1-Flash dropped hash layers and kept only Engram, which picks no experts<sup>45</sup>.

In Megatron, `--moe-num-hash-layers` makes the first MoE layers hash layers ([`router.py#L304-L308`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L304-L308)). They read each token's experts from a token-to-expert table (`tid2eid`) with one row per vocabulary entry, and if you do not load one, Megatron fills it with a round-robin placeholder ([`router.py#L313-L329`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L313-L329)). Since the expert bias is off in these layers, nothing corrects a bad table during training, so the table matters. Roller et al. compared ways to build it: a random table and one that greedily spreads the most frequent tokens over the emptiest experts reached about the same perplexity, with the second better balanced, while grouping similar tokens by clustering their embeddings did clearly worse<sup>61</sup>.

*Collapsible:* Megatron source

*Collapsible:* [`router.py#L304-L308`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L304-L308) (first N layers hashed)

```
self.is_hash_layer = (
    not self.is_mtp_layer
    and hash_moe_layer_threshold > 0
    and layer_number <= hash_moe_layer_threshold
)
```

*Collapsible:* [`router.py#L322-L326`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L322-L326) (placeholder round-robin table)

```
token_ids = torch.arange(self.config.hash_moe_vocab_size, device=self.weight.device)
expert_offsets = torch.arange(self.topk, device=token_ids.device)
self.tid2eid = ((token_ids[:, None] + expert_offsets) % self.num_experts).to(
    torch.int32
)
```

*Collapsible:* [`router.py#L898-L905`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L898-L905) (experts looked up by token id)

```
flat_ids = input_ids.T.reshape(-1)
assert flat_ids.numel() == logits.shape[0], (
    f"input_ids contains {flat_ids.numel()} tokens, but router logits contain "
    f"{logits.shape[0]}."
)
# Token IDs address the real tokenizer vocabulary; reject out-of-range IDs,
# including negative IDs, without clamping them to another token's experts.
default_top_indices = self.tid2eid.index_select(0, flat_ids).long()
```

*Collapsible:* [`router.py#L914-L916`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L914-L916) (weights still from the gate)

```
def _compute_hash_topk(scores, topk, num_groups=None, group_topk=None):
    del topk, num_groups, group_topk
    return scores.gather(1, default_top_indices), default_top_indices
```

plus a few lines that load V4-Flash's `layers.0.ffn.gate.tid2eid` from the Hub and count tokens per expert

> **Watch:** A table that overloads some experts makes the step slow, and since nothing rebalances it during training, check it early in the run by comparing the tokens per expert in the hash layers with those in the learned layers, from the token counts that `--save-tokens-per-expert-interval` writes ([A.1](#s-a-1)).

> **Recommendation:** Use it only to reproduce DeepSeek-V4's first layers. Load a fixed hash table as V4 does<sup>27</sup>, or a frequency-balanced one, instead of Megatron's round-robin placeholder.

##### What to watch

| Part | Symptom | Signal to watch |
| --- | --- | --- |
| Who selects | `slow`: with token choice, some experts get more tokens than others. `learns badly`: with expert choice, routing at inference differs from routing in training. | MaxVio per layer<sup>52</sup>, how far the busiest expert's load sits above the mean, from the token counts ([A.1](#s-a-1)). |
| Hash layers | `slow`: frequent tokens can overload the experts their hash assigns them, and no bias can move them. | Tokens per expert in the hash layers, compared with the learned layers, from the token counts ([A.1](#s-a-1)). |

Expert choice and expert threshold keep the load even or close to it, and no bias can move a hash table's load. Megatron trains learned token choice, where nothing so far stops many tokens from crowding onto the same few experts. Crowded experts are the first real failure mode of an MoE, so how do we keep tokens spread evenly over the experts while the router keeps learning?

#### 3.3 Load balancing

![hero-anatomy-zoom](https://huggingface-moe-blogpost.hf.space/viz/posters/hero-anatomy-zoom.webp)

When many tokens pick the same experts, two things go wrong. The GPU holding the busiest experts has the most work, so the other GPUs wait for it and it sets the step time, and if the router keeps sending tokens to the same few experts, the others get few tokens and their parameters go mostly unused. The first cost is the easier one to measure: with routing forced even, the same model ran 1.5x faster at init.

Forcing the routing even only shows the speed to aim for, since it throws away what the router learned. To get close to it while the router keeps learning, there are two families of fixes, an auxiliary loss and a loss-free bias, and they balance the load in different ways. The aux loss adds a term that rewards an even load, so the router's gradient pushes its probabilities toward spreading tokens, at the price of a gradient that competes with the LM loss. The bias changes only which experts are selected. Whichever you pick, the scope it balances over (a sequence, a micro-batch or the global batch) decides what "balanced" means.

*Table note:* Balancing recipes reported by model authors. Auxiliary losses and selection biases can be used together. Scope describes the tokens whose loads are balanced; the MiMo row concerns RL rather than pretraining.

| Model | Auxiliary loss | Scope | Selection bias | Quantile balancing |
| --- | --- | --- | --- | --- |
| DeepSeek-V3<sup>62</sup> | Small sequence-wise loss, coefficient 0.0001 | Batch-wide bias plus sequence-wise loss | Fixed-step expert bias | No, fixed-step updates |
| DeepSeek-V4.1-Flash<sup>63</sup> | Small sequence-wise loss, coefficient 0.0001 | Text and image loads balanced separately, plus sequence-wise loss | Separate biases per modality, update speed 0.001 | Uses the auxiliary-loss-free bias strategy |
| Kimi K3<sup>64</sup> | Described as auxiliary-loss-free | Global batch | Bias derived from score margins, applied next step | Yes, global-batch histogram estimation |
| LongCat-Flash<sup>65</sup> | Device-level balance loss | Global-batch FFN targets plus device-level balance within sequences | PID-controlled expert bias; identity experts excluded from bias updates | No, PID updates |
| MiMo-V2.6-Pro-RL<sup>66</sup> | Router frozen during RL | Preserves the pre-RL router | Report evaluates freezing rather than a new bias update rule | No new balancing update reported for RL |
| Qwen3 MoE<sup>67</sup> | Global-batch balancing loss | Global batch | No selection bias in the published router<sup>68</sup> | No, auxiliary-loss approach |

Before comparing balancers, we need to know how much speed an uneven load costs us, since every balancer below should be judged against the throughput of routing that is forced to be even. Where does that 1.5x come from, and how do we measure it on our own setup?

##### Cost of imbalance

To see what imbalance costs, we routed the same model three ways. Forced-even routing, [Megatron](https://github.com/NVIDIA/Megatron-LM)'s `--moe-router-force-load-balancing`, replaces the router's logits with random ones so that every expert gets about the same load, which makes it the best case, at 149.4 TFLOP/s.

Forced-biased routing, `--moe-router-force-biased`, adds a shared random bias of growing size to those random logits, so a few experts get more and more of the tokens: a dial for how uneven the load is. At the far end of the dial throughput falls to 100.5 TFLOP/s, and a replay of that routing, whose aux loss matches the logged one, has the busiest expert receive every token, a MaxVio of 7, as uneven as top-8 routing over 64 experts can get. It can get worse: in the replay the busiest experts are spread over several GPUs, so the busiest GPU holds only about twice the mean load, and had they all sat on one GPU, that GPU would have done most of the expert work.

The learned router, the one you would train with, starts far from that best case: a freshly initialised router ran its first 40 iterations as slowly as the worst forced case. The figure below compares the three. Training has to close that gap without forcing the router's choices, and the rest of this section compares the balancing methods by how close they bring a learned router to forced-even throughput.

![forced-balance-ab](https://huggingface-moe-blogpost.hf.space/viz/posters/forced-balance-ab.webp)

*Figure caption:* Figure 3.3.1

In the figure, throughput falls with each larger forced bias, as a few experts take more of the tokens, and the learned router starts at the level of the most uneven forced run. The busiest experts set the step because the all-to-all hands each GPU every token routed to its local experts, 8 of 64 in our runs, and the next all-to-all waits for the slowest GPU. A GPU's load is the sum over its local experts, so it can be more balanced than the per-expert load. That is why a balance loss can also work per GPU rather than per expert: DeepSeekMoE's device-level balance loss pools each GPU's experts into one term<sup>69</sup>, and the figure that follows compares it with the expert-level loss.

![device-level-balance-loss](https://huggingface-moe-blogpost.hf.space/viz/posters/device-level-balance-loss.webp)

*Figure caption:* Figure 3.3.2

Trained on one toy batch with two experts per GPU, one of them among the four the LM favours, both losses balance the GPUs, and the device-level loss pulls the router less far from what the LM wants, since it sees only each GPU's total, which that placement keeps closer to even. The catch is that the experts within each GPU stay uneven, so one expert can still take most of its GPU's tokens. DeepSeekMoE gives the same reason for weighting the two losses unevenly: strict expert-level balance would cost model quality, so it sets a larger device-level factor and keeps a small expert-level one against routing collapse<sup>69</sup>. DeepSeek-V2 runs them at 0.05 against 0.003<sup>70</sup>. DeepSeek-V3's report no longer mentions a device-level loss: it balances each expert with a bias and a small sequence-wise loss, both covered later in this section<sup>42</sup>.

The same imbalance costs time in serving too, so a frontier MoE in production keeps it small: when DeepSeek serves DeepSeek-V4.1-Flash, its slowest GPU sits at most 1.09 times the mean<sup>71</sup>.

*Collapsible:* Megatron source

*Collapsible:* [`router.py#L1185-L1193`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L1185-L1193) (force switches in forward)

```
if self.config.moe_router_force_load_balancing:
    # Apply force load balancing with random logits for benchmark
    logits = apply_random_logits(logits)
if self.config.moe_router_force_biased is not None:
    # Apply biased logits with shared random bias across all ranks
    logits = apply_biased_logits(
        logits, self.config.moe_router_force_biased, self.layer_number
    )
```

*Collapsible:* [`moe_utils.py#L1301-L1314`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L1301-L1314) (random logits per rank)

```
@staticmethod
def forward(ctx, logits: torch.Tensor) -> torch.Tensor:
    """
    Forward pass returns random logits with rank-specific seed.
    Args:
        logits (torch.Tensor): The logits.
    Returns:
        torch.Tensor: The random logits.
    """
    with get_cuda_rng_tracker().fork(get_expert_parallel_rng_tracker_name()):
        random_logits = logits.clone().normal_()
    return random_logits
```

*Collapsible:* [`moe_utils.py#L1353-L1370`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L1353-L1370) (shared per-layer bias)

```
@staticmethod
def forward(ctx, logits, std, layer_number):
    """Forward pass: apply random bias to logits."""
    # Check cache if reuse mode (negative std)
    if std < 0 and layer_number in RandomSTEShared._cache:
        return logits + RandomSTEShared._cache[layer_number]
    # Generate random bias with shared seed across all ranks
    with get_cuda_rng_tracker().fork(get_data_parallel_rng_tracker_name()):
        bias = torch.empty(logits.shape[-1], device=logits.device, dtype=logits.dtype).normal_(
            std=abs(std)
        )
    # Cache if reuse mode
    if std < 0 and layer_number is not None:
        RandomSTEShared._cache[layer_number] = bias
    return logits + bias
```

> **Watch:** Imbalance shows up as a slow step, so the number to watch is TFLOP/s against the forced-even control run. To see where the lost time goes, look at the step profiled in [3.7](#s-3-7): it ran on an unbalanced router, and [3.7](#s-3-7) shows how to tell whether imbalance is what slows its all-to-all.

> **Recommendation:** Use it once per setup, as a control run: `--moe-router-force-load-balancing` gives the balanced throughput to compare every balancer against. Never train with it.

Forced routing shows how fast an even load runs, but it replaces the router's logits with random ones, so it can only serve as a control run, never as a way to train. How do we steer a learned router toward an even load while it trains, starting with the oldest fix, a loss term?

##### Aux loss

The oldest fix adds a loss term, the aux loss: the coefficient times the expert count times a sum over experts, each expert's share of the micro-batch's tokens times its mean router probability ([`moe_utils.py#L148-L152`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L148-L152)). Its gradient pulls router probabilities away from what the LM wants, toward an even load. Below, four settings route one batch: no balancing, the aux loss at a small and at a large coefficient, and the loss-free bias.

![aux-load-balancing-loss](https://huggingface-moe-blogpost.hf.space/viz/posters/aux-load-balancing-loss.webp)

*Figure caption:* Figure 3.3.3

Both balancers spread the load in the figure, in different ways: the aux loss pulls the router's probabilities off what the LM loss wants, further at the larger coefficient, while the loss-free bias only changes which experts are picked and balances best, though it reroutes the most selections. The aux loss's pull makes its coefficient a tradeoff: too large a coefficient costs LM loss, and too small a coefficient leaves the load uneven. Yuan3.0's ablation of DeepSeek-V3's sequence-wise aux loss on a 10B model, plotted in the next figure, shows both sides: test loss rose with the coefficient from 1e-3 to 0.1, while the smallest coefficient, 1e-4, did slightly better than no aux loss at all but still left the busiest expert in a layer with about 13.6 times the tokens of the least used one<sup>72,73</sup>.

![aux-coeff-sweep](https://huggingface-moe-blogpost.hf.space/viz/posters/aux-coeff-sweep.webp)

*Figure caption:* Figure 3.3.4

The smallest coefficient in the figure leaves the load uneven, and the one that balances it, 1e-2, raises the test loss. Megatron sets the coefficient with `--moe-aux-loss-coeff` next to `--moe-router-load-balancing-type aux_loss`, one coefficient per loss type, applied in every layer. Motif 3 found its first MoE layers more susceptible to imbalance and gives them stronger auxiliary loss weights<sup>74</sup>. We come back to the first layers later in the chapter.

*Collapsible:* Megatron source

*Collapsible:* [`moe_utils.py#L148-L152`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L148-L152) (Σ f·P times coefficient)

```
aggregated_probs_per_expert = probs.sum(dim=0)
aux_loss = torch.sum(aggregated_probs_per_expert * tokens_per_expert) * (
    num_experts * moe_aux_loss_coeff / (topk * total_num_tokens * total_num_tokens)
)
return aux_loss
```

*Collapsible:* [`router.py#L515-L536`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L515-L536) (counts over one micro-batch)

```
aux_loss_coeff = self.get_aux_loss_coeff("aux_loss")
if aux_loss_coeff == 0:
    return probs
global_tokens_per_expert, local_num_tokens, total_num_tokens = (
    get_tokens_per_expert_and_token_count(
        routing_map=routing_map,
        reduce_group=self.tp_cp_group,
        topk=self.topk,
        with_padding_mask=with_padding_mask,
    )
)
aux_loss = switch_load_balancing_loss_func(
    probs=scores_for_aux_loss,
    tokens_per_expert=global_tokens_per_expert,
    total_num_tokens=total_num_tokens,
    topk=self.topk,
    num_experts=self.config.num_moe_experts,
    moe_aux_loss_coeff=aux_loss_coeff,
    fused=self.config.moe_router_aux_loss_fusion,
)
```

*Collapsible:* [`router.py#L459-L472`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L459-L472) (coefficient per loss type)

```
def get_aux_loss_coeff(self, aux_loss_type: str) -> float:
    """Return the aux loss coeff for the given auxiliary loss type.
    If the auxiliary loss type is not found, return 0.0.
    """
    if isinstance(self.routing_type, str):
        if self.routing_type == aux_loss_type:
            return self.config.moe_aux_loss_coeff
    if isinstance(self.routing_type, list):
        try:
            idx = self.routing_type.index(aux_loss_type)
            return self.config.moe_aux_loss_coeff[idx]
        except ValueError:
            return 0.0
    return 0.0
```

The measured row under the four-column figure above comes from Wang et al., who proposed the loss-free bias and compared it with a per-sequence aux loss on a 1B MoE with 64 routed experts and top-6. At their baseline coefficient of 1e-3, MaxVio over the validation set was 0.72 at a perplexity of 9.56, against 0.04 and 9.50 with the bias<sup>75</sup>; with no aux loss MaxVio rose to about 5.1, and at 1e-2 it fell to about 0.1 while perplexity rose to about 9.69<sup>76</sup>.

This aux loss, at a coefficient of 1e-3, is the learned router of Cost of imbalance, and by the end of its 120 iterations it had climbed to 125 TFLOP/s.

> **Watch:** A coefficient set too high makes the model learn worse, and one set too low leaves the load uneven, so watch the LM loss and the balance together. Balance is best read from MaxVio rather than from the aux loss itself. The loss multiplies each expert's share of the tokens by its mean router probability, so when the router's probabilities are flat the loss reads the same as for an even load, whatever the token shares are, and a perfectly balanced reading can hide a skewed load. Sigma-MoE-Tiny hit this case: in its lower layers the loss went to its minimum by flattening the probabilities while the load stayed uneven<sup>77</sup>. `--moe-per-layer-logging` logs this value per layer as `load_balancing_loss`, divided by the coefficient.

> **Recommendation:** Use it when the simplest balancer will do: `aux_loss` at a coefficient around 1e-3, as in our first MoE run in [2.5](#s-2-5). Raise it if the load stays uneven, lower it if the LM loss suffers<sup>72</sup>.

The aux loss we used so far counts each expert's load within one micro-batch, which leaves a question we have not asked yet: over which tokens should the load be even? You could balance it over each sequence, over each micro-batch, or over the whole global batch, and the next part compares the three.

##### Scope

Think about what one micro-batch holds. Pretraining pipelines often pack each micro-batch from a single domain, say all code, so a loss that asks for an even load inside that micro-batch spreads the code tokens over every expert, and no expert gets to specialize in code<sup>78</sup>. Balance over the whole global batch instead, which mixes many domains, and the code tokens may crowd onto a few experts as long as tokens from other domains fill the rest. Qiu et al. saw experts specialize by domain only in that second setting, and it also lowered their perplexity<sup>79</sup>. The GPUs pay for it: inside each micro-batch the load is no longer even, and their 43B model's step ran about 6% slower, about 1% of that slowdown from communication overhead and the rest mainly from the uneven load<sup>80,81</sup>.

A single sequence is the tightest scope of all. Balancing each sequence on its own spreads every sequence over all the experts, even when a micro-batch mixes domains; DeepSeek-V2-Lite counted its only balance loss, an expert-level one, this way<sup>82</sup>, and DeepSeek-V3 keeps a small one to stop a single sequence from piling onto a few experts while the batch as a whole looks balanced<sup>42</sup>. In the figure below the three scopes run side by side, on GPUs that each hold two sequences from two domains: the tighter the scope, the less the experts can concentrate on one domain, and the looser it is, the more uneven the load each GPU carries.

![global-batch-balance-loss](https://huggingface-moe-blogpost.hf.space/viz/posters/global-batch-balance-loss.webp)

*Figure caption:* Figure 3.3.5

In that simulation, the sequence-wise loss spreads the code sequence over all the experts, the micro-batch loss lets each GPU's two domains split its experts between them, and the global-batch loss leaves the code tokens mostly on their two favoured experts, at the price of the most uneven load per GPU. Megatron picks the scope through the load-balancing type: `aux_loss` balances per micro-batch, `seq_aux_loss` per sequence and `global_aux_loss` over the global batch. To combine scopes, pass several types and one coefficient for each, in the same order, for example `--moe-router-load-balancing-type aux_loss seq_aux_loss --moe-aux-loss-coeff 1e-3 1e-4`.

*Collapsible:* Megatron source

*Collapsible:* [`router.py#L567-L589`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L567-L589) (per-sequence counts, ÷ bsz)

```
scores_for_aux_loss = scores_for_aux_loss.reshape(seq_length, -1)
routing_map = routing_map.reshape(seq_length, -1)
global_tokens_per_expert, local_num_tokens, total_num_tokens = (
    get_tokens_per_expert_and_token_count(
        routing_map=routing_map,
        reduce_group=self.tp_cp_group,
        with_padding_mask=with_padding_mask,
        topk=self.topk * bsz,
    )
)
aux_loss = (
    switch_load_balancing_loss_func(
        probs=scores_for_aux_loss,
        tokens_per_expert=global_tokens_per_expert,
        total_num_tokens=total_num_tokens,
        topk=self.topk,
        num_experts=self.config.num_moe_experts,
        moe_aux_loss_coeff=seq_aux_loss_coeff,
        fused=self.config.moe_router_aux_loss_fusion,
    )
    / bsz
```

*Collapsible:* [`router.py#L617-L628`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L617-L628) (global counts, running average)

```
global_tokens_per_expert, local_num_tokens, total_num_tokens = (
    get_tokens_per_expert_and_token_count(
        routing_map=routing_map,
        reduce_group=self.tp_dp_cp_group,
        with_padding_mask=with_padding_mask,
        topk=self.topk,
    )
)
self.global_tokens_per_expert += global_tokens_per_expert
self.ga_steps += 1
averated_tokens_per_expert = self.global_tokens_per_expert / self.ga_steps
```

*Collapsible:* [`router.py#L233-L248`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L233-L248) (global count buffers)

```
# Initialize global tokens per expert for global aux loss
if self.get_aux_loss_coeff("global_aux_loss") > 0:
    self.register_buffer(
        'global_tokens_per_expert',
        torch.zeros(
            self.config.num_moe_experts,
            dtype=torch.float32,
            device=torch.cuda.current_device(),
        ),
        persistent=False,
    )
    self.register_buffer(
        'ga_steps',
        torch.tensor(0, dtype=torch.float32, device=torch.cuda.current_device()),
        persistent=False,
    )
```

*Collapsible:* [`router.py#L1121-L1125`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L1121-L1125) (reset per global batch)

```
def reset_global_aux_loss_tracker(self):
    """Reset the global aux loss tracker."""
    if self.global_tokens_per_expert is not None:
        self.global_tokens_per_expert.zero_()
        self.ga_steps.zero_()
```

> **Watch:** Each scope fails in its own way. Balancing per sequence or per micro-batch can keep domain experts from forming, so the model learns worse, while balancing over the global batch leaves the load on each GPU uneven, so the step gets slower. Whichever scope you pick, read balance from MaxVio at that scope, computed per micro-batch from the loads `--save-tokens-per-expert-interval` saves, per global batch from the sum of those loads, and per sequence offline from the routing trace ([A.1](#s-a-1)).

> **Recommendation:** Use micro-batch (`aux_loss`) by default. Use `global_aux_loss` only for domain-specialized experts, at +5.8% step time in Qiu et al.<sup>81</sup>.

Whichever scope you pick, a balancing loss still steers the router through its gradient, and that gradient competes with the one from the LM loss. Could you balance the load without touching the gradient at all?

##### Loss-free bias

The aux loss fixes an overloaded expert by pulling the router's probabilities away from what the LM wants. The loss-free bias leaves the probabilities alone and moves the load with no gradient. Each expert gets a bias, added to its score before the top-k and used only to pick experts, while the weights still come from the scores, and once per step Megatron moves each bias by a fixed amount, the update rate: up for underloaded experts, down for overloaded ones. The next figure runs that loop. In DeepSeek-V3's ablation it matched a batch-wise aux loss in validation loss, at 1B and at 3B<sup>83</sup>. Like the aux loss, it reroutes some selections away from the LM's own top-k, and in the four-column toy of the Aux loss part it reroutes the most.

![aux-loss-free-bias](https://huggingface-moe-blogpost.hf.space/viz/posters/aux-loss-free-bias.webp)

*Figure caption:* Figure 3.3.6

The figure runs 16 toy experts with a step far larger than Megatron's default, so a few rounds stand in for many: overloaded experts lower their bias and underloaded ones raise it until the load is close to even, and the back-and-forth that the large step leaves is damped once the toy cuts its step tenfold. In real training the catch is the fixed step, which must suit the expert count. Li et al. swept the expert count of small MoEs, and with an update rate of 1e-3 the busiest expert's load grew with it, to about 50 times the mean at 1,024 experts, where an aux loss of 1e-2 alone stayed under about 7 times<sup>84</sup>. Above 128 experts the bias also hurt LM quality, and the authors suspect a step too coarse for that many experts<sup>85</sup>.

The reference lines on the overload trace in the figure above come from the same 1B runs, measured on each training batch rather than over the validation set: MaxVio settled near 0.72 with the aux loss at 1e-3 and near 0.1 with the bias<sup>86</sup>.

Megatron's rule is the simplest one you could write: every step, each bias moves up or down by the same fixed amount, however far its expert sits from the mean load. That is the sign update, and it is not the only way to run the loop. A linear update moves each bias in proportion to its expert's distance from the mean load, so a badly overloaded expert gets a large correction and a nearly balanced one a small one, while an AdamW update adapts the step for each expert. LongCat-Flash runs a linear update, aimed at the expert loads its compute budget calls for<sup>65</sup>, and ZAYA1-8B feeds each expert's load error to AdamW<sup>87</sup>.

The rules also differ in a subtler way: when an update's steps do not sum to zero, the mean of all the biases drifts. That drift changes no selection, since adding the same number to every expert's score leaves the top-k as it was, but it costs precision where the bias is stored in bf16; Megatron keeps it in fp32. Moonlight and Trinity Mini avoid the drift by subtracting the mean of the steps<sup>88,89</sup>. The released weights differ the same way: DeepSeek-V3's biases sit at a per-layer mean of 2.2 to 8.0, while Moonlight's and ZAYA1-8B's average 0 and LongCat-Flash's sit just below it<sup>90</sup>. Below, the sign update, a centered sign update, the linear update and the AdamW update run on the same batch.

![bias-update-rules](https://huggingface-moe-blogpost.hf.space/viz/posters/bias-update-rules.webp)

*Figure caption:* Figure 3.3.7

The figure's toy batch has a few hot experts and many just under the mean load, so most sign steps point up: the sign and AdamW updates lift the mean of the biases while the centered sign and linear updates keep it at zero, yet the sign update balances as well as the centered one at every step, since top-k ignores a shift shared by all experts. Whatever rule moves it, the bias can only balance the tokens it counts. A batch-wide bias is fitted on one batch and applied to the next, so it can make the batch as a whole look even without guaranteeing that each sequence is: a single sequence can still pile onto a few experts. The obvious fix, a second bias computed over each whole sequence, would use tokens that come later in that sequence, and so leak the future into the routing of the earlier ones.

Chang's causal bias avoids the leak by building that second bias only from what the sequence has already routed. It resets at the start of every sequence, and after each token it lowers the bias of the experts just picked and raises the others', so each expert's bias tracks how far its picks so far sit above or below its share, k/N per token, and an expert this sequence has overused is pushed down for the tokens that follow. Like the batch bias, it only changes which experts are picked and is never trained by the gradient<sup>91</sup>. The next figure routes the same sequence with the global-batch bias alone and with the causal bias from this sequence's past added on top.

![sequence-level-balance](https://huggingface-moe-blogpost.hf.space/viz/posters/sequence-level-balance.webp)

*Figure caption:* Figure 3.3.8

The sequence shown switches to code halfway. With only the global-batch bias, its code tokens pile onto one expert, even though the whole batch stays balanced; with the causal bias added, those code tokens spread over more experts and the sequence's load stays much closer to even. On the other hand, the simulation shows the causal bias sending more of the picks to experts outside the router's own top-k, away from what the router itself prefers, and the evidence for it is small-scale, from Chang's experiments on nanochat and TinyStories<sup>91</sup>.

Released models handle the single sequence differently. DeepSeek-V3 pairs its bias with the sequence-wise aux loss we saw earlier, at a tiny coefficient of 1e-4<sup>62</sup>: the bias keeps the batch even, and the small loss guards against extreme imbalance within a single sequence. The figure that follows compares no such loss, a small one and a large one, on an ordinary sequence and on an extreme one.

![sequence-wise-aux-complement](https://huggingface-moe-blogpost.hf.space/viz/posters/sequence-wise-aux-complement.webp)

*Figure caption:* Figure 3.3.9

In that toy, whose two coefficients are illustrative rather than DeepSeek-V3's, a small coefficient brings an ordinary sequence closer to even while moving the router only a little, but leaves an extreme sequence piled onto one expert; spreading that one takes a large coefficient, which pulls the router much further off the routing the LM loss prefers. A sequence is one way a batch-wide count can hide an imbalance, and a modality is another.

When a batch mixes modalities, a bias counted over all the tokens can balance their sum while the tokens of one modality, taken alone, still crowd onto a few experts. DeepSeek-VL2 and Kimi-VL keep one bias for all tokens<sup>92,93</sup>, and DeepSeek-V4.1-Flash keeps one per modality<sup>63</sup>. The figure below compares one shared bias with one bias per modality, each counting only its own modality's tokens.

![modality-split-bias](https://huggingface-moe-blogpost.hf.space/viz/posters/modality-split-bias.webp)

*Figure caption:* Figure 3.3.10

The toy scripts text to lean toward four of its eight experts and images toward the other four, so a shared bias balances the total while each modality's surplus cancels the other's, and a bias per modality balances each modality on its own. The price of the split is that the bias then pushes every expert to take its share of each modality, away from specializing in images.

To run it in Megatron, turn the bias on with `--moe-router-enable-expert-bias` and set its fixed step with `--moe-router-bias-update-rate`, with sigmoid scores (`--moe-router-score-function sigmoid`), since Megatron accepts the bias only with sigmoid or sqrt(softplus) scores ([`transformer_config.py#L3139-L3147`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L3139-L3147)).

*Collapsible:* Megatron source

*Collapsible:* [`moe_utils.py#L936-L939`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L936-L939) (bias in selection only)

```
elif expert_bias is not None:
    scores_for_routing = scores + expert_bias.float()
    _, top_indices = compute_topk(scores_for_routing, topk, num_groups, group_topk)
    scores = torch.gather(scores, dim=1, index=top_indices)
```

*Collapsible:* [`router.py#L209-L228`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L209-L228) (int64 counts, fp32 bias)

```
if self.enable_expert_bias:
    self.register_buffer(
        'local_tokens_per_expert',
        torch.zeros(
            self.config.num_moe_experts,
            # Keep token counts exact through accumulation and cross-rank reduction.
            # Float16Module leaves integer buffers in their original dtype.
            dtype=torch.int64,
            device=torch.cuda.current_device(),
        ),
        persistent=False,
    )
    self.register_buffer(
        'expert_bias',
        torch.zeros(
            self.config.num_moe_experts,
            dtype=torch.float32,
            device=torch.cuda.current_device(),
        ),
    )
```

*Collapsible:* [`moe_utils.py#L1253-L1263`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L1253-L1263) (sign update, exact compare)

```
# All Reduce Across TPxCPxDP group
torch.distributed.all_reduce(tokens_per_expert, group=tp_dp_cp_group)
num_experts = tokens_per_expert.shape[-1]
total_tokens = tokens_per_expert.sum(dim=-1, keepdim=True)
# Compare each tokens_per_expert value with the row average without converting the integer
# counts to floating point: tokens_per_expert < total / num_experts iff
# tokens_per_expert * num_experts < total.
update_direction = torch.sign(total_tokens - tokens_per_expert * num_experts)
updated_expert_bias = (
    expert_bias + update_direction.to(dtype=expert_bias.dtype) * expert_bias_update_rate
)
```

*Collapsible:* [`finalize_model_grads.py#L726-L731`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/distributed/finalize_model_grads.py#L726-L731) (update once per step)

```
if config.moe_router_enable_expert_bias:
    if pg_collection is None:
        tp_dp_cp_group = parallel_state.get_tensor_and_data_parallel_group(
            with_context_parallel=True
        )
    _update_router_expert_bias(model, config, tp_dp_cp_group=tp_dp_cp_group)
```

> **Watch:** When the update rate is too coarse for your expert count, the load stays uneven, which slows the step as Cost of imbalance showed, and above 128 experts Li et al.'s sweep also saw LM quality suffer. You can catch it in two places. Every checkpoint saves `expert_bias`, so you can follow how far the biases of each layer spread from one checkpoint to the next, and the token counts that `--save-tokens-per-expert-interval` writes give you MaxVio per global batch ([A.1](#s-a-1)).

> **Recommendation:** Use it when the balancer must barely pull against the LM loss: the bias adds no gradient at all, and DeepSeek-V3's sequence-wise loss at α = 1e-4<sup>62</sup> adds very little. Run it with sigmoid scores, and tune the update rate to your expert count, since 1e-3 can be too coarse above 128 experts<sup>85</sup>.

The bias moves by the same small step whatever the load looks like, so it can take many steps to catch up with a router that keeps changing. Instead of stepping toward the right bias, could you compute it directly from the scores of the current batch?

##### Quantile

Quantile balancing keeps the bias but solves for it. For each expert, it ranks the micro-batch's tokens by their score for that expert and reads off a quantile: the score that only the expert's target share of tokens beats. The bias is set from that quantile instead of moved by a fixed step. Jin et al. compared balancers on a 19B-parameter MoE with 768 experts, and quantile balancing balanced sooner than the sign update at about the same LM loss, halving the average MaxVio, though over the last 1k steps its MaxVio ended slightly higher<sup>94</sup>. That precision has a price: in every micro-batch, each expert has to rank all of the micro-batch's tokens by its score to find its quantile, a top-k per expert on top of the usual top-k per token. Side by side below, the sign update and quantile balancing run on the same batch.

![quantile-balancing](https://huggingface-moe-blogpost.hf.space/viz/posters/quantile-balancing.webp)

*Figure caption:* Figure 3.3.11

The toy routes the same batch at every step, so each solved bias routes the very tokens it was solved from: after the last step the sign update still leaves the load uneven, while quantile balancing brings it close to even within a few steps. In Megatron, each micro-batch solves for its own quantiles, and the solutions are averaged over the global batch to route the next one, optionally smoothed by an exponential moving average (EMA, `--moe-router-quantile-balancing-ema`).

> *Margin note:* An EMA keeps most of the previous bias and mixes in only a share of each new solution, so the bias changes slowly from step to step.

*Collapsible:* Megatron source

*Collapsible:* [`moe_utils.py#L233-L247`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L233-L247) (top-k and per-expert quantile)

```
topk_result = (scores - beta).topk(k + 1, dim=1)
indices = topk_result.indices[:, :-1]
if not update_beta:
    return indices, beta
assert (num_tokens * k) % num_experts == 0, (
    "Quantile balancing requires the number of routed assignments "
    f"({num_tokens} tokens * top-{k}) to be divisible by "
    f"{num_experts} experts."
)
col_target = num_tokens * k // num_experts
alpha = topk_result.values[:, -1:]
beta_local = (scores - alpha).topk(col_target + 1, dim=0).values[-1].contiguous()
return indices, beta_local
```

*Collapsible:* [`finalize_model_grads.py#L441-L457`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/distributed/finalize_model_grads.py#L441-L457) (average, EMA, re-center)

```
stacked_beta = torch.stack(qb_beta_list, dim=0)
local_avg_list = [
    accum / count.clamp(min=1).to(accum.dtype)
    for accum, count in zip(qb_beta_accum_list, qb_beta_count_list)
]
stacked_local_avg = torch.stack(local_avg_list, dim=0)
torch.distributed.all_reduce(
    stacked_local_avg, op=torch.distributed.ReduceOp.AVG, group=dp_cp_group
)
ema = config.moe_router_quantile_balancing_ema
stacked_new_beta = ema * stacked_beta + (1.0 - ema) * stacked_local_avg
stacked_new_beta = stacked_new_beta - stacked_new_beta.mean(dim=-1, keepdim=True)
for qb_beta, new_beta in zip(qb_beta_list, stacked_new_beta):
    qb_beta.copy_(new_beta)
```

*Collapsible:* [`router.py#L256-L259`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L256-L259) (aux losses must be 0)

```
if self.routing_type == "quantile_balancing":
    assert not self.is_aux_loss_enabled(), (
        "Quantile balancing handles load balance via the bias update; "
        "aux losses must be disabled (set moe_aux_loss_coeff to 0)."
```

*Collapsible:* [`router.py#L398-L403`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L398-L403) (no fusion, no group limit)

```
assert (
    not self.config.moe_router_fusion
), "Quantile balancing routing does not support moe_router_fusion."
assert (
    self.config.moe_router_num_groups is None and self.config.moe_router_group_topk is None
), "Quantile balancing routing does not support group-limited routing."
```

Kimi K3 runs quantile balancing over its whole global batch, reading each expert's quantile from a histogram summed across GPUs<sup>64</sup>. It left the fixed-step rule because balancing grew harder once its routed pool reached 896 experts per layer<sup>64</sup>, and Su Jianlin, who proposed quantile balancing<sup>95</sup>, writes that Kimi K2 had used the sign update<sup>96</sup>.

Averaging has a price: a bias shared by the whole global batch can balance that batch while each GPU's micro-batch stays uneven. Neitemeier et al. measured how wide that gap gets in a 7.5B run (one seed). The rank-averaged quantile that Megatron uses balanced the global batch to a MaxVio of 0.92, while in the worst layer the busiest expert of an expert-parallel micro-batch still took about 7 times its fair share, a local MaxVio of 5.96. Solving for the exact global-batch quantile lowered both<sup>97</sup>. They read local MaxVio as a proxy for dispatch cost rather than as measured throughput<sup>98</sup>.

How do the balancers compare in throughput? We ran five router configurations from init on the same model, with one seed, and compared their median throughput over the last 20 of 120 iterations. Quantile balancing reached 139 TFLOP/s, against 125 for the aux loss and 99 for the tested bias-only configuration. The bias-only run used sigmoid scores and an update rate of 1e-3, while the other four used softmax. With an EMA of 0.9, quantile balancing reached 121 TFLOP/s. That setting gives each new solution 10% of the weight in the bias update ([`transformer_config.py#L910-L913`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L910-L913)).

> *Margin note:* These runs used an older Megatron commit, which accumulated the bias's token counts in bf16, so a count could round and flip the direction of its bias update; at `d6316eb45` the counts are exact.

Jin et al. added an EMA to quantile balancing: stronger smoothing kept the bias steadier between checkpoints but corrected the load more slowly early in training<sup>99</sup>. All five runs are plotted below.

![router-mode-5way](https://huggingface-moe-blogpost.hf.space/viz/posters/router-mode-5way.webp)

*Figure caption:* Figure 3.3.12

Of the five runs in the figure, the bias-only one stays flat while the other four climb, with quantile balancing fastest over the final 20 iterations. Throughput is still rising at the end, so the ranking describes these first 120 iterations. Quantile balancing also ends with the highest training LM loss of the five, so its throughput lead alone does not establish faster training to the same quality.

To try quantile balancing, set `--moe-router-load-balancing-type quantile_balancing`.

> *Margin note:* The same flag also accepts `sinkhorn`: Sinkhorn uses a balanced-assignment procedure to choose experts for each token during training.

> **Watch:** The risk is a global batch that looks balanced while each GPU's micro-batch is not, which Neitemeier et al. read as a higher dispatch cost. To see the gap, compute MaxVio twice from the token counts that `--save-tokens-per-expert-interval` writes, once per micro-batch and once per global batch, and compare the two ([A.1](#s-a-1)).

> **Recommendation:** Use it when the sign-update bias balances too slowly: solving for the bias reached a lower average MaxVio than stepping toward it, at about the same LM loss, with 768 experts<sup>94</sup>, and it had the highest median throughput over the last 20 of 120 iterations in our five-configuration comparison (one seed). Plan around its limits, since Megatron currently refuses it next to any aux loss, `--moe-router-fusion` or group-limited routing.

##### What to watch

| Part | Symptom | Signal to watch |
| --- | --- | --- |
| Cost of imbalance | `slow`: the GPU holding the busiest experts sets the step. | TFLOP/s against the forced-even control run. |
| Aux loss | `learns badly`: a coefficient set too high makes the model learn worse, and one set too low leaves the load uneven. | LM loss and MaxVio together: with flat router probabilities, the aux loss can look balanced while the load stays uneven<sup>77</sup>. |
| Scope | `learns badly`: balancing per sequence or per micro-batch keeps domain experts from forming. `slow`: balancing per global batch leaves the load on each GPU uneven; the step took 5.8% longer, mainly from that imbalance and about 1% of that slowdown from communication<sup>81</sup>. | MaxVio at the scope you balance: per micro-batch or per global batch from the token counts, per sequence from the routing trace ([A.1](#s-a-1)). |
| Loss-free bias | `slow`: with a fixed step of 1e-3, the busiest expert still gets about 20 times the mean load at 128 experts<sup>84</sup>. `learns badly`: above 128 experts, that step is too coarse<sup>85</sup>. | How far `expert_bias` spreads in each layer across checkpoints, and MaxVio per global batch from the token counts ([A.1](#s-a-1)). |
| Quantile | `slow`: smoothing the bias with a moving average makes it lag the router's scores. The bias is shared by the global batch, so each GPU's load can stay uneven, as in Scope. | MaxVio per micro-batch alongside MaxVio per global batch, from the saved token counts ([A.1](#s-a-1)), to detect a globally balanced batch hiding local imbalance<sup>97</sup>. |

Every balancer in this section spreads tokens over a set of experts that was fixed before training started, and we have not yet asked what that set should look like. How many experts should a layer have, how wide should each one be, and should some of them see every token?

#### 3.4 Experts: how many, how big, shared or not

![hero-anatomy-zoom](https://huggingface-moe-blogpost.hf.space/viz/posters/hero-anatomy-zoom.webp)

Once the router has picked a token's experts, what those experts look like decides both what the layer can learn and what it costs to run. You choose how many experts a layer has and how wide each one is, how to keep the network traffic of many small experts in check, whether one expert should see every token, and which activation runs inside each of them.

*Table note:* Expert choices in leading open MoEs, plus Nemotron for LatentMoE and ReLU² and LongCat-Flash for variable compute. Count and size gives the routed experts each token uses out of the total, then each expert's FFN width; shared experts are listed separately. Latent dimensions show token width before and after projection. "No limit specified" refers to the published configuration.

| Model | Count and size | Latent MoE | Shared experts | Variable compute | Activation |
| --- | --- | --- | --- | --- | --- |
| DeepSeek-V4.1-Flash<sup>100</sup> | 6 of 384, width 2,304 | Full-width experts | 1, width 2,304 | Fixed top-k, equal widths | SwiGLU, limit 10 |
| GLM-5.3<sup>101</sup> | 8 of 256, width 2,048 | Full-width experts | 1, width 2,048 | Fixed top-k, equal widths | SiLU gate; no limit specified |
| Kimi K3<sup>102</sup> | 16 of 896, width 3,072 | 7,168 to 3,584; norm before up-projection | 2, width 3,072 each | Fixed top-k, equal widths | SiTU-GLU, caps 4 and 25 |
| LongCat-Flash<sup>103</sup> | 12 of 768, width 2,048 | Full-width experts | None | 256 of the 768 are identity experts: 18.6B to 31.3B active parameters per token, 27B on average | SiLU gate; no limit specified |
| MiMo-V2.6-Pro-RL<sup>104</sup> | 8 of 384, width 2,048 | Full-width experts | None | Fixed top-k, equal widths | SiLU gate; no limit specified |
| Nemotron 3 Ultra<sup>105</sup> | 22 of 512, width 5,120 | 8,192 to 2,048 | 1, width 10,240 | Fixed top-k, equal widths | ReLU² |
| Qwen3.8 2.4T-A95B<sup>106</sup> | 10 of 512, width 2,048 | Full-width experts | 1, width 2,048 | Fixed top-k, equal widths | SiLU gate; no limit specified |
| Step 5 Preview<sup>107</sup> | 8 of 352, width 1,536 | Full-width experts | 1, width 1,536 | Fixed top-k, equal widths | SwiGLU, limit 7 |

With the parameter budget fixed, adding more experts means making each one narrower. Which split gives you a better model for the same compute?

##### Count and size

Picture one MoE layer with a fixed budget of parameters and compute, and cut its experts finer: twice as many experts at half the width, with twice the top-k, keeps both budgets the same. Figure 3.4.1 draws that ladder: coarse, then 16 experts of d/2 with top-4, then 32 of d/4 with top-8. Liew et al. ran the ablation in an 18-layer model with total and active parameters fixed, and loss fell with each finer cut up to 128 experts of d/4 with top-8, from 2.334 to 2.297, while finer cuts did not improve it further<sup>108</sup>. In this experiment, then, segmenting stopped paying past 128 experts, while every finer step still ran smaller GEMMs and dispatched more copies of each token.

![expert-granularity](https://huggingface-moe-blogpost.hf.space/viz/posters/expert-granularity.webp)

*Figure caption:* Figure 3.4.1

Released models sit on different rungs of that ladder. gpt-oss-120b and Trinity Large keep each expert as wide as the model, with top-4 of 128 and top-4 of 256 experts, Mistral Small 4 halves that width with top-4 of 128, and Qwen3.5-35B-A3B quarters it with top-8 of 256<sup>109</sup>.

In the figure, you can see that splitting the experts changes their number and width while keeping the total parameters and compute per token fixed. The total tile area represents the parameters, and the dark area represents the expert computation for one token. What you are changing is the granularity. You can also increase sparsity: add more parameters while keeping the number used by each token fixed. Two ways to spend those extra parameters are compared next: more routed experts, or n-gram embedding tables looked up by token id.

> *Margin note:* Granularity describes how finely you divide the expert capacity: finer granularity means more, narrower experts. To keep the same compute per token, each token uses more of the narrower experts.

![sparse-param-budget](https://huggingface-moe-blogpost.hf.space/viz/posters/sparse-param-budget.webp)

*Figure caption:* Figure 3.4.2

The figure plots LongCat's comparison at 280M active parameters. There, n-gram tables lowered the loss more than the same parameters spent on more experts (by about 0.01 at 17 times the active parameters) once the experts already held about 12 times the active parameters, while tables added when the experts stopped at about 4 times lost from the start. The gain had a limit: on English validation loss, more experts won again once tables held a little over 40% of the parameters, and LongCat's rule, read from that crossing, is to put no more than 50% of the parameters in tables<sup>110</sup>. In that comparison, expanding the experts paid off first, and once they were large enough, part of the next parameters did more in lookup tables. Where you spend extra parameters therefore depends on how much expert capacity you already have.

Both ways of spending ship in released models: Kimi K2 grows its pool to 384 experts with top-8, and LongCat-Flash-Lite puts 31.4B of its 68.5B parameters in n-gram embedding tables<sup>111</sup>.

Whether you add more experts or divide the existing capacity into narrower ones, the resulting shape also affects training speed. Narrower experts run smaller GEMMs, which use the GPU less efficiently.

For a dense model, compute-optimal scaling laws help you choose how to divide a fixed FLOP budget between model size and training tokens: a larger model leaves room for fewer tokens, while a smaller one can train on more<sup>112</sup>. An MoE adds another choice. You can increase its total parameters without increasing the parameters used by each token, so you also need to choose its sparsity. For either kind of model, choosing under a time limit also means accounting for how efficiently each configuration uses your hardware<sup>113</sup>.

Sarkar et al. combined a fitted loss scaling law with a training-throughput model to compare the sparsity that minimizes loss at fixed model FLOPs with the sparsity that minimizes loss at fixed cluster time. Their predictions for one cluster and training window are plotted below<sup>113</sup>.

> *Margin note:* Sparsity here is the fraction of the model's parameters that a token does not use.

![cluster-optimal-sparsity](https://huggingface-moe-blogpost.hf.space/viz/posters/cluster-optimal-sparsity.webp)

*Figure caption:* Figure 3.4.3

In their predictions, choosing by model FLOPs alone points you toward the sparsest model in the grid. Once the authors account for training speed on their cluster, the lowest predicted loss moves to a less sparse configuration, 0.031 nats below the sparsest one. As in dense scaling, you are balancing model capacity against how many tokens you can train on. With an MoE, increasing sparsity can lower hardware utilization without increasing model FLOPs per token, so extra capacity can still cost training time<sup>113</sup>.

[Megatron](https://github.com/NVIDIA/Megatron-LM) sets the shape with three flags: `--num-experts` for the count, `--moe-ffn-hidden-size` for each expert's width and `--moe-router-topk` for how many experts each token picks.

*Collapsible:* Megatron source

*Collapsible:* [`experts.py#L262-L293`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/experts.py#L262-L293) (grouped fc1, fc2 shapes)

```
# Double the output width with gated linear unit, see https://arxiv.org/pdf/2002.05202.pdf
ffn_hidden_size = not_none(self.config.moe_ffn_hidden_size)
if self.config.gated_linear_unit:
    ffn_hidden_size *= 2
self.linear_fc1 = submodules.linear_fc1(
    self.num_local_experts,
    self.input_size if self.config.moe_latent_size is None else self.config.moe_latent_size,
    ffn_hidden_size,
    config=self.config,
    init_method=not_none(self.config.init_method),
    bias=self.config.add_bias_linear,
    skip_bias_add=False,
    is_expert=True,
    tp_comm_buffer_name='fc1',
    pg_collection=pg_collection,
    name=(name + ".linear_fc1") if name is not None else None,
)
if self.config.use_te_activation_func and not (submodules.activation_func is None):
    self.activation_func = apply_module(submodules.activation_func(config=self.config))
else:
    self.activation_func = self.config.activation_func
self.linear_fc2 = submodules.linear_fc2(
    self.num_local_experts,
    not_none(self.config.moe_ffn_hidden_size),
    (
        self.config.hidden_size
        if self.config.moe_latent_size is None
        else self.config.moe_latent_size
    ),
```

*Collapsible:* [`router.py#L77-L81`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L77-L81) (router weight N x d)

```
# Initialize the gate weights.
# TODO: Add support for GPU initialization, which requires updating the golden values.
self.weight = torch.nn.Parameter(
    torch.empty((self.config.num_moe_experts, self.config.hidden_size), dtype=torch.float32)
)
```

> **Watch:** Cut the experts too fine and each expert's GEMMs get small enough to lower TFLOP/s per GPU, and with the wrong granularity the model learns worse. To see what a shape costs you, read the grouped-GEMM time per MoE layer from the profiler next to TFLOP/s per GPU from `--log-throughput`. The token counts that `--save-tokens-per-expert-interval` writes also show dead experts that receive no tokens ([A.1](#s-a-1)), but an expert can also die while it keeps its tokens, which shows in its output norm instead ([3.6](#s-3-6))<sup>114</sup>.

> **Recommendation:** Use finer experts at equal total and active parameters, up to a point: in one 18-layer model, the loss fell until 128 experts of d/4 with top-8, and finer splits gained nothing<sup>108</sup>. Stop going finer once small GEMMs and token copies start to dominate your step.

Finer experts help the loss only up to a point, and each finer step sends more copies of every token over the network. Could you keep the many small experts and send less data for each copy?

##### Latent MoE

Each copy of a token carries its full hidden state, d numbers, sent once for every expert it picked. LatentMoE shrinks that copy. It projects each token down to a smaller latent ℓ before dispatch, runs the experts on ℓ, and projects back up after combine. Every copy shrinks from d to ℓ, and the savings pay for more experts: at the same expert parameters, expert compute and traffic, the layer can afford α = d/ℓ times more experts and an α times larger top-k<sup>115</sup>. Below, a standard layer sits next to its latent counterpart, keeping the parameters and compute inside the experts fixed.

![latent-moe](https://huggingface-moe-blogpost.hf.space/viz/posters/latent-moe.webp)

*Figure caption:* Figure 3.4.4

Drawn as tiles, the standard layer selects four of sixteen experts, each receiving a full-width token vector. The latent layer selects eight of thirty-two, but each receives only half as many values. Both send the same amount of data per token. Their total tile area and dark area are also equal, showing unchanged expert parameters and compute; the two projections add work outside those areas<sup>115</sup>.

Does the trade pay off in quality? In NVIDIA's 73B-A8B ablation, at equal total and active parameters, LatentMoE scored 4.6 points higher on MMLU-Pro than a standard MoE<sup>116</sup>, and a small-scale replication also lowered perplexity<sup>117</sup>. Nemotron 3 Super, Nemotron 3 Ultra and Kimi K3 ship it<sup>118</sup>. In return, every token runs through two d x ℓ projections, and serving throughput ranged from 12% lower at concurrency 1 to slightly higher at some concurrencies<sup>119</sup>. In Megatron, the latent size is `--moe-latent-size`.

*Collapsible:* Megatron source

*Collapsible:* [`moe_layer.py#L304-L335`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_layer.py#L304-L335) (two projections, optional norm)

```
self.fc1_latent_proj = linear_cls(
    self.config.hidden_size,
    self.config.moe_latent_size,
    parallel_mode="duplicated",
    config=self.config,
    init_method=self.config.init_method,
    bias=self.config.add_bias_linear,
    skip_bias_add=False,
    skip_weight_param_allocation=False,
    is_expert=False,
    name=(name + ".fc1_latent_proj") if name is not None else None,
    **linear_gtp_kwargs,
)
if self.config.moe_use_norm_before_up_proj:
    self.fc2_norm = TENorm(
        config=self.config,
        hidden_size=self.config.moe_latent_size,
        eps=self.config.layernorm_epsilon,
    )
self.fc2_latent_proj = linear_cls(
    self.config.moe_latent_size,
    self.config.hidden_size,
    parallel_mode="duplicated",
    config=self.config,
    init_method=self.config.output_layer_init_method,
    bias=self.config.add_bias_linear,
    skip_bias_add=False,
    skip_weight_param_allocation=False,
    is_expert=False,
    name=(name + ".fc2_latent_proj") if name is not None else None,
    **linear_gtp_kwargs,
)
```

*Collapsible:* [`moe_layer.py#L554-L556`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_layer.py#L554-L556) (project down before dispatch)

```
# Project the hidden_states from hidden dimension down to latent dimension.
if self.config.moe_latent_size:
    hidden_states, _ = self.fc1_latent_proj(hidden_states)
```

*Collapsible:* [`moe_layer.py#L662-L666`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_layer.py#L662-L666) (norm, project up after combine)

```
output = self.token_dispatcher.combine_postprocess(output)
if self.config.moe_latent_size:
    if self.config.moe_use_norm_before_up_proj:
        output = apply_module(self.fc2_norm)(output)
    output, _ = self.fc2_latent_proj(output)
```

*Collapsible:* [`experts.py#L269-L269`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/experts.py#L269-L269) (experts read ℓ)

```
self.input_size if self.config.moe_latent_size is None else self.config.moe_latent_size,
```

> **Watch:** A latent MoE can go wrong in two ways: it runs slow, or its activations blow up. When it runs slow, look past the traffic, since the all-to-all now carries ℓ numbers per copy instead of d, to the two extra projections and the smaller expert GEMMs. LatentMoE's NVIDIA authors propose small-GEMM kernels and a separate stream for the shared expert as fixes<sup>120</sup>. When it blows up, as Kimi K3 reports for the activations of its routed branch at its 2.8-trillion-parameter scale<sup>102</sup>, one place to look is the output norm of the up-projection, `fc2_latent_proj`, which you can compute per layer offline from the `--save-activations-interval` dumps ([A.1](#s-a-1)). K3's fix was an RMSNorm before the up-projection, `--moe-use-norm-before-up-proj`, which it ships with a routed scaling factor of 1.0<sup>121</sup>.

> **Recommendation:** Use a latent when you want more experts and a larger top-k without sending more data per token: shrinking each copy to ℓ = d/α affords α times more of both<sup>115</sup>, and it scored higher at matched size<sup>116</sup>, at the cost of two projections.

Every expert so far sits behind the router and sees only the tokens sent to it. What would you gain by putting one expert outside the router, where it sees every token, and is it worth its compute?

##### Shared experts

A shared expert sits outside the router: it processes every token, next to whichever routed experts the token picked. DeepSeekMoE introduced shared experts to learn common patterns, reducing duplicated knowledge across routed experts and giving them room to specialize<sup>122</sup>. In its ablation at equal compute, adding a shared expert improved results on most benchmarks<sup>123</sup>. Qwen's models show how open the question is: the Qwen3 MoE models in the Qwen3 report dropped it<sup>124</sup>, Qwen3-Next brought it back behind a sigmoid gate<sup>125</sup>, and Qwen3.5 kept it<sup>126</sup>.

Measured by loss in models trained from scratch at equal compute, the gain is small and not consistent. A shared expert lowered loss by about 0.01 to 0.02 in Pangu Ultra MoE and in Sun et al.'s expert-threshold models<sup>127,128</sup>, while in OLMoE and in Li et al.'s sweep of small MoEs it did nothing or slightly worse<sup>129,130</sup>.

Sharing also reduces the router's freedom. With 32 experts and 4 active, reserving one slot for a shared expert leaves 4,495 ways to choose the other 3, compared with 35,960 ways to choose 4 from all 32. If you instead add the shared expert without reducing routed top-k, its always-on FFN increases compute per token: Mellum2 added a shared expert without reducing routed top-k and found no quality gain and slower inference<sup>131</sup>.

If you do add one, you still have to decide how its output mixes with the routed experts'. The figure below lines up five designs at equal compute per token: routed only, a shared expert at fixed weight (DeepSeek-V3)<sup>30</sup>, a gated one (Qwen3-Next)<sup>125</sup>, one normalized jointly with the routed experts (Inkling)<sup>19</sup> and a parallel dense FFN (Grok 2)<sup>132</sup>.

![shared-expert-weight](https://huggingface-moe-blogpost.hf.space/viz/posters/shared-expert-weight.webp)

*Figure caption:* Figure 3.4.5

Lined up this way, a shared expert at fixed weight holds the same share of every token's weight, Qwen's gate moves that share between 0 and 50%, Inkling's router learns it per token by scoring the shared experts with the routed ones, and a parallel dense FFN without renormalization holds over half of it whatever the router scores.

Megatron's flags are `--moe-shared-expert-intermediate-size`, `--moe-shared-expert-gate` (a sigmoid gate on its output) and `--use-grouped-gemm-for-shared-expert`. Without the gate, Megatron adds the shared output at weight 1 ([`moe_layer.py#L668-L669`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_layer.py#L668-L669)), while the routed weights sum to the routed scaling factor when normalized over the selected experts ([`moe_utils.py#L942-L947`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L942-L947), [3.1](#s-3-1)). The shared expert therefore takes 1/(1 + factor) of each token's output weight, 29% at a factor of [2.5](#s-2-5), and the larger the factor, the smaller its share; GLM-4.5-Air and Mistral Large 3 set the factor to 1, which gives it half<sup>133,134</sup>.

> *Margin note:* Megatron does this with sigmoid routing, or by applying softmax after selecting the top-k experts. For the latter, leave `--moe-router-pre-softmax` disabled.

*Collapsible:* Megatron source

*Collapsible:* [`shared_experts.py#L128-L128`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/shared_experts.py#L128-L128) (width from shared size)

```
config.ffn_hidden_size = config.moe_shared_expert_intermediate_size
```

*Collapsible:* [`shared_experts.py#L201-L208`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/shared_experts.py#L201-L208) (sigmoid gate on output)

```
def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
    """Forward function"""
    output, _ = super().forward(hidden_states)
    if self.use_shared_expert_gate:
        logits = torch.nn.functional.linear(hidden_states, self.gate_weight)
        gate_score = torch.nn.functional.sigmoid(logits)
        output = output * gate_score
    return output
```

*Collapsible:* [`moe_layer.py#L668-L669`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_layer.py#L668-L669) (added at weight 1)

```
if shared_expert_output is not None:
    output = output + shared_expert_output
```

> **Watch:** To track how much the shared expert contributes to each token's output during training, compare the shared branch after its gate with the routed branch after combine and any latent up-projection, using the sparse forward hook in [A.1](#s-a-1).

> **Recommendation:** A shared expert is a common starting choice in leading MoEs, including GLM-5.3, Kimi K3 and DeepSeek V4.1 Flash<sup>135,136,137</sup>. MiMo-V2.6 ships without one<sup>138</sup>. To compare with and without one at equal compute, give it the routed experts' width and replace one routed slot with it.

Shared or not, every expert so far has the same width and every token gets the same top-k, so every token gets the same compute. Could the router give some tokens less compute and others more, while the average stays fixed?

##### Variable compute

Two designs let the compute per token vary while the mean stays fixed. LongCat-Flash adds zero-computation experts that pass the input through unchanged. Its router selects 12 experts per token from a pool of 512 FFN experts and 256 of these identity paths. A bias adjusts how often the FFN experts are selected, targeting an average of 8 per token while allowing individual tokens to use more or fewer<sup>139</sup>; the standard deviation of that count rose to about [2.5](#s-2-5) during pre-training<sup>140</sup>. Xiaomi's AI Lab takes a different approach in MoDSE (Mixture of Diverse Size Experts): they mix expert widths, letting the router choose larger or smaller experts for each token<sup>141</sup>. The figure below simulates the active width per token for homogeneous experts, as in Mixtral<sup>142</sup>, and both designs.

![variable-compute-experts](https://huggingface-moe-blogpost.hf.space/viz/posters/variable-compute-experts.webp)

*Figure caption:* Figure 3.4.6

In the simulation, where one bias per design holds the mean active width at that of the homogeneous experts, some tokens get more of it and others less, and every token still fills all its top-k slots, since only what lands in them varies. In LongCat-Flash's ablation, zero-computation experts reached lower loss at matched compute<sup>143</sup>. Mixed expert sizes can improve quality, but may cost throughput. Xiaomi's AI Lab and Wang et al. each put one router over mixed-size experts in small models and report gains<sup>141,144</sup>. Li et al. found none, but in their setup the experts sit in two pools, each with a fixed top-k, so every token still gets the same compute<sup>145</sup>. In GroveMoE, the cost showed at inference: its mixed sizes ran about 30% slower than Qwen3-30B-A3B, which its authors attribute to processing the two expert sizes with separate MoE kernels in each layer<sup>146</sup>.

*Collapsible:* Megatron source

none: a grep of Megatron-LM main (megatron/ tree) finds neither zero-computation experts nor mixed expert widths; each grouped linear has one `moe_ffn_hidden_size`

> **Watch:** Track the mean and spread of compute per token in each layer: the number of selected FFN experts for zero-computation routing, or the sum of selected expert widths for mixed-size routing. Compare the mean with the target budget, and log token counts per expert alongside compute per expert-parallel rank and step time.

> **Recommendation:** Start with routed experts of one width and a fixed top-k, as MiMo-V2.6-Pro-RL, GLM-5.3 and Kimi K3 do<sup>138,135,136</sup>. This also fits Megatron's grouped linear layers, which use a single `moe_ffn_hidden_size`.

With the count, width and compute of the experts settled, one choice remains inside each expert: the function between its two projections. How much does that choice matter for an MoE?

##### Activation

As in a dense Transformer, each expert uses an activation function such as SwiGLU, as in DeepSeek-V3, Qwen3 and Kimi K2<sup>147</sup>, or ReLU² between its input and output projections. In an MoE, you also need to watch how activations behave across experts: Step [3.5](#s-3-5) Flash found that one or two experts could develop rapidly growing output norms while the others stayed stable and the training loss barely changed<sup>15</sup>. The activation function, and any clamp applied to it, helps control that growth. The figure below shows how the output of SwiGLU, ReLU² and Expert-Specific PolyNorm grows as the input scale rises.

![expert-activations](https://huggingface-moe-blogpost.hf.space/viz/posters/expert-activations.webp)

*Figure caption:* Figure 3.4.7

Scaled up, SwiGLU and ReLU² outputs grow with the square of the input scale, while Expert-Specific PolyNorm normalizes its gate, so its output grows only linearly. A clamp can bound that growth. Two studies found similar quality with and without clipping in their tested settings. In a 7.9B MoE ablation by Ant Group's Ling team, SwiGLU with clipping matched plain SwiGLU's average over 17 benchmarks<sup>148</sup>. Step [3.5](#s-3-5) Flash's activation clipping held its outlier experts' norms down at indistinguishable loss, although that branch started mid-run from the unclipped run<sup>15</sup>. Clipping did not eliminate loss spikes in the Ling team's [FP8](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=fp8_pretraining) run, the clipped SwiGLU delayed the loss spikes, yet one still came around step 77,000<sup>149</sup>. The next figure sweeps the input scale through plain SwiGLU, a hard clamp and SiTU-GLU's smooth cap at the same bound, so you can see how each one bends.

![activation-bounds](https://huggingface-moe-blogpost.hf.space/viz/posters/activation-bounds.webp)

*Figure caption:* Figure 3.4.8

Through that sweep, plain SwiGLU's largest hidden unit keeps growing with the square of the gate input up to 6,862, the peak K-EXAONE 2.0 measured at its last layer with its clamp disabled at inference<sup>150</sup>, the hard clamp follows it up to the bound and stops there, and SiTU-GLU bends away well before the bound. The sweep sets both to stop a hidden unit at about 100, the clamp at 10 and SiTU-GLU with a gate cap of 4 and an up cap of 25, and from about the same input both pass almost no gradient to those units' gate weights. Replacing the activation altogether rests on thinner evidence. Zhuo et al.'s PolyNorm lowered average validation loss by 0.02 against SwiGLU in OLMoE-1B-7B<sup>151</sup>, while Motif 3 compares its Expert-Specific PolyNorm with SwiGLU only on effective rank<sup>152</sup>. Kimi K3 states that SiTU-GLU's smooth cap gives better training behavior than hard clamping<sup>153</sup>.

In Megatron, `--activation-func-clamp-value` sets the hard-clipping limit for SwiGLU in MoE layers; a value of 10 matches DeepSeek V4.1 Flash's limit<sup>154</sup>, which GigaChat [3.5](#s-3-5) and Hy4-preview also use<sup>155</sup>. Kimi K3's smooth cap, SiTU-GLU, is `--activation-func-tanh-clamp-scale 4 --activation-func-tanh-clamp-scale-linear 25`, available from [Megatron Core v0.20](https://github.com/NVIDIA/Megatron-LM/releases/tag/core_v0.20.0) on, and Nemotron 3's ReLU² is `--squared-relu`<sup>118</sup>.

*Collapsible:* Megatron source

*Collapsible:* [`experts.py#L1100-L1118`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/experts.py#L1100-L1118) (SiTU-GLU or clamped SwiGLU)

```
if tanh_clamp_scale is not None:
    intermediate_parallel = situ_glu(
        intermediate_parallel,
        tanh_clamp_scale,
        self.config.activation_func_tanh_clamp_scale_linear,
        self.config.glu_linear_offset,
    )
else:
    def glu(x):
        x_glu, x_linear = torch.chunk(x, 2, dim=-1)
        if (val := self.config.activation_func_clamp_value) is not None:
            x_glu = x_glu.clamp(min=None, max=val)
            x_linear = x_linear.clamp(min=-val, max=val)
        return self.config.activation_func(x_glu) * (
            x_linear + self.config.glu_linear_offset
        )
    intermediate_parallel = glu(intermediate_parallel)
```

*Collapsible:* [`activations.py#L17-L39`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/activations.py#L17-L39) (soft clamp and SiTU-GLU)

```
def tanh_soft_clamp(x: torch.Tensor, scale: float) -> torch.Tensor:
    """Tanh Soft Clamp to precondition activation inputs."""
    return (scale * torch.tanh(x.float() / scale)).to(x.dtype)
@jit_fuser
def situ(x: torch.Tensor, scale: float) -> torch.Tensor:
    """Sigmoid-Tanh Unit from Kimi K3: ``s * tanh(x / s) * sigmoid(x)``"""
    return tanh_soft_clamp(x, scale) * torch.sigmoid(x)
@jit_fuser
def situ_glu(
    x: torch.Tensor,
    gate_scale: float,
    linear_scale: Optional[float] = None,
    linear_offset: float = 0.0,
) -> torch.Tensor:
    """SiTU-GLU: ``situ(x_gate, gate_scale) * (x_linear + linear_offset)``."""
    x_gate, x_linear = torch.chunk(x, 2, dim=-1)
    if linear_scale is not None:
        x_linear = tanh_soft_clamp(x_linear, linear_scale)
    return situ(x_gate, gate_scale) * (x_linear + linear_offset)
```

*Collapsible:* [`transformer_config.py#L2993-L3013`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L2993-L3013) (clamp: MoE only, offset 0)

```
if (
    self.activation_func_clamp_value is not None
    and self.activation_func == F.silu
    and self.gated_linear_unit
):
    if (
        not math.isfinite(self.activation_func_clamp_value)
        or self.activation_func_clamp_value <= 0
    ):
        raise ValueError(
            "activation_func_clamp_value for SwiGLU must be finite and greater than zero."
        )
    if self.num_moe_experts is None:
        raise ValueError(
            "activation_func_clamp_value for SwiGLU is only supported with MoE."
        )
    if self.glu_linear_offset != 0.0:
        raise ValueError(
            "glu_linear_offset must be zero when activation_func_clamp_value "
            "is set for SwiGLU."
        )
```

> **Watch:** Outlier activations in the experts can blow up a run. To catch them, compute Step [3.5](#s-3-5) Flash's signal, the max-to-median ratio of expert output norms per layer<sup>156</sup>, offline from the `--save-activations-interval` dumps ([A.1](#s-a-1)): one expert pulling away from the others shows as a rising ratio. Each dump keeps only the last micro-batch and copies it to the CPU, so sample sparsely.

> **Recommendation:** Start from your reference model's activation recipe. Leading MoEs use different ways to bound activations: Step 5 Preview clips SwiGLU at 7, DeepSeek V4.1 Flash at 10, and Kimi K3 uses SiTU-GLU's smooth caps<sup>107,154,153</sup>. For a new architecture, SwiGLU is a reasonable baseline. If expert norms diverge, test clipping and compare training loss as well as the norms before choosing a limit.

##### What to watch

| Part | Symptom | Signal to watch |
| --- | --- | --- |
| Count and size | `slow`: the expert GEMMs are small. Some experts may also get no tokens. | Grouped-GEMM time per MoE layer from the profiler, TFLOP/s per GPU (`--log-throughput`), and tokens per expert (`--save-tokens-per-expert-interval`, [A.1](#s-a-1)). |
| Latent MoE | `slow`: the two extra projections and the smaller expert GEMMs add time. `blows up`: Kimi K3 reports exploding activations in the routed branch<sup>102</sup>. | For speed, profile the two latent projections and smaller expert GEMMs alongside the reduced all-to-all. For instability, one place to look is the up-projection output norm (`fc2_latent_proj`) from activation dumps ([A.1](#s-a-1)); Kimi K3 reports routed-branch activation growth<sup>102</sup>. |
| Shared experts | `slow` at inference, when it adds compute: Mellum2 found inference slower<sup>131</sup>. | Shared output after its gate against routed output after combine and any latent up-projection, from the sparse forward hook in [A.1](#s-a-1). |
| Variable compute | `slow`: each expert size runs its own kernels, and GroveMoE reports about 30% slower inference than Qwen3-30B-A3B<sup>146</sup>. | Per layer, mean and spread of selected FFN count or summed expert width against the target compute budget. Log token counts per expert alongside compute per EP rank and step time. |
| Activation | `blows up`: outlier activations. | The max-to-median ratio of expert output norms per layer, Step [3.5](#s-3-5) Flash's signal<sup>156</sup>, from the activation dumps ([A.1](#s-a-1)). |

Everything in this section happened inside one MoE layer, while a model stacks many of them, which raises two questions we have not asked yet. Should every layer be an MoE layer, and how should the block around each one be wired?

#### 3.5 Block layout

![hero-anatomy-zoom](https://huggingface-moe-blogpost.hf.space/viz/posters/hero-anatomy-zoom.webp)

Picture the model as a stack of blocks, each one attention followed by either a dense MLP or an MoE layer. Every MoE layer sends its tokens out to their experts and back with an all-to-all, so where the MoE layers sit decides how many all-to-alls a step makes, and also which layers end up balancing worst. How each block is wired then decides how much of every all-to-all can hide behind attention.

*Table note:* Where models put their MoE layers and how they connect them to attention. Dense-layer counts refer to the backbone, excluding prediction modules.

| Model | Dense layers | Block wiring |
| --- | --- | --- |
| DeepSeek-V3<sup>157</sup> | First 3 dense, remaining 58 MoE | Attention followed by FFN |
| DeepSeek-V4.1-Flash<sup>158</sup> | All 40 blocks use MoE | Single-Pass mHC residual connections |
| GLM-5.3<sup>101</sup> | First 3 dense, remaining 75 MoE | Attention followed by FFN<sup>18</sup> |
| Kimi K3<sup>159</sup> | First layer dense, remaining 92 MoE | Attention followed by Stable LatentMoE; Attention Residuals |
| Llama 4 Maverick<sup>160</sup> | Alternating dense and MoE, starting dense | MoE every second layer |
| LongCat-Flash<sup>161</sup> | Dense FFNs and MoE coexist within each macro-block | Shortcut-connected MoE overlaps with later attention and FFN work |
| MiMo-V2.6-Pro<sup>138</sup> | First layer dense, remaining 69 MoE | Hybrid attention blocks followed by FFNs |

The first layout decision is which layers get experts at all, since you can put an MoE in every layer, keep a few layers dense, or alternate the two. Which of these should you pick?

##### Dense layers

A dense layer has no router and no experts, so it makes no all-to-all. Figure 3.5.1 counts the all-to-alls of three layouts side by side: MoE in every layer, as in Qwen3, gpt-oss, MiniMax M2 and Llama 4 Scout<sup>162</sup>, leading dense layers, and MoE every other layer. Leading dense layers replace only the earliest MoE layers, as in DeepSeek-V3, which keeps its first three dense<sup>163</sup>. Putting an MoE in every other layer halves the all-to-alls instead, as in Llama 4 Maverick, which alternates dense and MoE layers<sup>160</sup>. Either way, you give up some MoE capacity in exchange for fewer all-to-alls and fewer parameters.

![dense-layer-placement](https://huggingface-moe-blogpost.hf.space/viz/posters/dense-layer-placement.webp)

*Figure caption:* Figure 3.5.1

The figure's toy scripts its routing to follow the token id less with depth, so its first layer balances slowest: leading dense layers remove its two slowest layers but cut only 4 of 16 all-to-alls, while MoE every other layer halves the all-to-alls but keeps the second slowest layer. In Ling's 60-layer models, leading dense layers cost little: making the first 1 to 3 layers dense barely changed efficiency at matched FLOPs, an efficiency leverage close to 1<sup>164</sup>.

The other argument for them is balance, and it rests on less evidence. DeepSeekMoE observed that the first layer's balance converges more slowly<sup>165</sup>, and Ling says leading dense layers ease early-layer imbalance<sup>166</sup>, though its ablation of those layers reports only loss<sup>164</sup>. Later reports pull in different directions. Some keep the first layers away from a learned router: Nucleus-Image, an image-generation MoE, diverged without its three leading dense layers<sup>167</sup>, and DeepSeek-V4 hashes its first 3 MoE layers<sup>53</sup>.

Others keep routing there and treat the imbalance instead. Solar Open uses MoE in every layer and fixes its early-layer imbalance with a sequence-wise auxiliary loss<sup>168</sup>. Sigma-MoE-Tiny routes each token to only 1 of 96 experts, and with an aux loss alone its lower layers collapsed: the loss took a shortcut by making the router's probabilities uniform, while some experts still got almost no tokens. Its fix was to activate more experts per token in the first 8 layers early in training, then drop back to one<sup>77</sup>. Dense layers do not always end the problem either: Motif 3, whose first two layers are dense, saw its earliest MoE layers balance worst early in training<sup>74</sup>, while ERNIE 5.0 found no severe imbalance in its first layer on text<sup>169</sup>.

[Megatron](https://github.com/NVIDIA/Megatron-LM) takes the layout as a list in [`--moe-layer-freq`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/models/gpt/gpt_layer_specs.py#L635-L645), one entry per layer, 0 for dense and 1 for MoE: `"([0]+[1]*15)"` gives one leading dense layer, and `"([0,1]*8)"` a dense-first interleave like Maverick's. The flag also takes an integer, and that form puts an MoE at layer 0, so `--moe-layer-freq 2` starts with an MoE rather than with a dense layer as Maverick does. The dense layers take their width from `--ffn-hidden-size`, separately from the expert size.

*Collapsible:* Megatron source

*Collapsible:* [`gpt_layer_specs.py#L635-L645`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/models/gpt/gpt_layer_specs.py#L635-L645) (integer or list pattern)

```
if isinstance(config.moe_layer_freq, int):
    moe_layer_pattern = [
        1 if (i % config.moe_layer_freq == 0) else 0 for i in range(config.num_layers)
    ]
elif isinstance(config.moe_layer_freq, list):
    moe_layer_pattern = config.moe_layer_freq
    assert len(moe_layer_pattern) == config.num_layers, (
        f"Invalid length of moe_layer_pattern: {len(moe_layer_pattern)}, "
        f"expected {config.num_layers}, "
        f"current moe layer pattern: {config.moe_layer_freq}"
    )
```

*Collapsible:* [`gpt_layer_specs.py#L652-L659`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/models/gpt/gpt_layer_specs.py#L652-L659) (dense or MoE per layer)

```
layer_specs = []
for layer_number in range(config.num_layers):
    if moe_layer_pattern[layer_number] == 1:
        layer_specs.append(moe_layer_spec)
    elif moe_layer_pattern[layer_number] == 0:
        layer_specs.append(dense_layer_spec)
    else:
        raise ValueError(f"Invalid layer pattern: {moe_layer_pattern}")
```

> **Watch:** The reports above saw imbalance in the early layers, and with dense layers in those places, the first MoE layers after them can still balance worst, as they did in Motif 3. Those first MoE layers are the ones to watch. Follow their aux loss with [`--moe-per-layer-logging`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_logging.py#L382-L405), whose per-layer values the launcher from [2.4](#s-2-4) sends to [Trackio](https://huggingface.co/docs/trackio), and their MaxVio from the routing trace ([A.1](#s-a-1)). The dense layers have no router to watch. The [z-loss](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L155-L172) measures how large the router logits grow, not how evenly tokens spread.

> **Recommendation:** Use leading dense layers when you want fewer all-to-alls at little cost: one to three of them barely changed efficiency at matched FLOPs in Ling's 60-layer models<sup>164</sup>. Do not count on them to fix early-layer imbalance: neither DeepSeekMoE nor Ling shows data for it<sup>165,166</sup>, and Motif 3 still saw it in its first MoE layers after two dense ones<sup>74</sup>.

Every MoE layer you keep still sends its tokens out and back, and in an MoE block, where the MoE runs on attention's output, the GPUs spend much of that time waiting. Could you rewire the block so that some of that traffic moves while attention computes?

##### Block wiring

In an MoE block, each all-to-all is tied to compute on both sides. The router reads attention's output, so dispatch cannot start until attention is done, and the next layer reads the MoE's output, so nothing after the MoE can start until combine is done. The [Ultra-Scale Playbook](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=a3:_math_for_compute/communication_overlap) covers how to overlap communication with compute in general.

![all-to-all-overlap](https://huggingface-moe-blogpost.hf.space/viz/posters/all-to-all-overlap.webp)

*Figure caption:* Figure 3.5.2

Rewiring the block removes one of these dependencies or both, and the communication it frees can then overlap with compute. A parallel block feeds attention and the MoE the same input, as Cohere's North Mini Code and Moondream 3 do<sup>170</sup>, so dispatch runs while attention computes. Combine is harder to hide, because it can only overlap with work left in the same layer, which in [Megatron's shortcut block](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/models/hybrid/shortcut_block.py#L547-L593) is attention's output projection and the shared expert; with neither, it stays exposed. A shortcut-connected MoE hides combine too, behind the dense compute that runs beside it, as in LongCat-Flash<sup>171</sup> and in Pos-2, the preferred variant of ScMoE, Cai et al.'s shortcut-connected MoE<sup>172</sup>. Figure 3.5.2 compares the three wirings inside one micro-batch, and in its illustrative durations the exposed all-to-all share of the layer falls from 33% in the MoE block to 7% with the shortcut.

*Collapsible:* Megatron source

*Collapsible:* [`shortcut_block.py#L102-L127`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/models/hybrid/shortcut_block.py#L102-L127) (attention paired with next MoE)

```
compute_layer = layers[physical_index]
paired_type = layer_type_list[physical_index]
if paired_type not in SUPPORTED_SHORTCUT_PREDECESSORS:
    raise ValueError(
        "Shortcut MoE must be preceded by a Mamba, GDN, or supported attention layer"
    )
supports_two_stage = (
    isinstance(compute_layer, TwoStageAttentionLayer)
    and compute_layer.supports_two_stage_attention()
)
if not supports_two_stage:
    raise ValueError(
        f"Shortcut attention layer {paired_type!r} does not support two-stage attention"
    )
moe_layer = layers[physical_index + 1]
grouped_layers.append(
    ShortcutMoEBlock(
        compute_layer,
        moe_layer,
        overlap_a2a=config.moe_shortcut_parallel,
        attn_local_idx=physical_index,
        moe_local_idx=physical_index + 1,
    )
)
physical_index += 2
```

*Collapsible:* [`shortcut_block.py#L490-L502`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/models/hybrid/shortcut_block.py#L490-L502) (router reads the pair's input)

```
# Launch the moe_router
with quant_context_factory(moe_config, self.moe_layer_idx):
    moe_hidden_states = self._read_shortcut_hidden(
        moe_hidden_states, recompute_context=attn_recompute_context
    )
    route_input, route_probs = self._moe_router_preprocess(
        shortcut_hidden=moe_hidden_states,
        padding_mask=padding_mask,
        packed_seq_params=moe_packed_seq_params,
        recompute_context=attn_recompute_context,
    )
    if overlap:
        self.route_ready_event.record(torch.cuda.current_stream())
```

*Collapsible:* [`shortcut_block.py#L362-L368`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/models/hybrid/shortcut_block.py#L362-L368) (dispatch on a side stream)

```
dispatch_stream = self._get_a2a_overlap_stream()
dispatch_stream.wait_event(self.route_ready_event)
hidden_states.record_stream(dispatch_stream)
probs.record_stream(dispatch_stream)
with torch.cuda.stream(dispatch_stream):
    return self.moe_layer.mlp.dispatch(hidden_states, probs)
```

*Collapsible:* [`shortcut_block.py#L534-L547`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/models/hybrid/shortcut_block.py#L534-L547) (dispatch, experts, combine before attention ends)

```
# Launch the dispatch, experts, and combine
with quant_context_factory(moe_config, self.moe_layer_idx):
    dispatched_input, dispatched_probs = self._launch_dispatch(
        route_input, route_probs, async_op=overlap
    )
    if overlap:
        dispatched_input, dispatched_probs = self._wait_dispatch(
            dispatched_input, dispatched_probs
        )
    output, _ = self.moe_layer.mlp.routed_experts_compute(
        dispatched_input, dispatched_probs
    )
    combined_output = self._launch_combine(output, async_op=overlap)
```

The parallel block in the figure overlaps dispatch with attention while combine stays exposed, and the shortcut-connected MoE covers most of dispatch and combine with the layers around it. The price falls on the router, which now reads the stream from before the compute it overlaps and never sees that compute's output.

Does the model learn worse for it? Cai et al. and the LongCat-Flash team saw it learn about as well. Cai et al. put an MoE in every block of a LLaMA2-style model, wired as Pos-1, the ScMoE variant that Megatron implements, and it averaged slightly higher on zero-shot benchmarks than a standard top-2 MoE<sup>173</sup>. In LongCat-Flash, the loss curves with and without the shortcut were virtually indistinguishable<sup>174</sup>. AMD's FarSkip-Collective rewires the block so that computation goes on with a residual that does not yet hold the latest communicated output. Shipped in Instella-MoE, it matched the MoE block's benchmark average after 200B training tokens<sup>175,176</sup>, although the tables of both AMD reports show it losing on MMLU and HumanEval+.

What you get in return is speed. ScMoE trained 1.12x to 1.14x faster on one node of 8 GPUs over NVLink, with the paper's standard top-2 MoE as the baseline<sup>173</sup>, and Instella-MoE gained 12.7% in pre-training throughput<sup>177</sup>. LongCat-Flash measured the exposed communication itself: with its shortcut-connected MoE, the share of time spent in dispatch and combine that is not overlapped fell from 25.3% to 8.4%<sup>178</sup>, in expert-parallel groups of 32 accelerators that use pipelined [all-gather](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=gather_%26_allgather) and [reduce-scatter](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=scatter_%26_reducescatter) instead of all-to-all.

In Megatron, the figure's parallel row (ScMoE's Pos-1) is [`--moe-shortcut-connection`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L796-L813), which makes each MoE read the input of the attention layer just before it, so its router no longer waits for that attention. The shared expert still reads attention's output, a detail the figure's row does not draw, and the routed experts run on the main stream [after attention's core and before its output projection](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/models/hybrid/shortcut_block.py#L517-L558), as the row's experts follow its attention. The rewiring alone overlaps nothing: the all-to-alls overlap only once `--moe-shortcut-parallel` puts them on a side CUDA stream. An optional extra norm on the merged output comes with `--moe-shortcut-post-norm`. All three flags are only on upstream main, and they work only in the hybrid stack, not together with [FSDP](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/arguments.py#L984-L990), CUDA graphs, full recompute or `--moe-shared-expert-overlap`. Without a block change, Megatron can also hide the all-to-all behind another micro-batch ([3.7 Overlap](#s-3-7-overlap)).

> **Watch:** An exposed all-to-all makes the step slow, and a trace shows how much of it is exposed. Take an nsys timeline (`--profile` with `--profile-step-start` and `--profile-step-end`, see [3.7 Profiling](#s-3-7-profiling)) and compare the all-to-all kernels on the side stream with the compute on the main stream: the stretches where the all-to-all runs alone are the exposed share.

> **Recommendation:** Use Megatron's shortcut block (the figure's parallel row) when dispatch is exposed and you can move to Megatron's hybrid stack: ScMoE's Pos-1 design trained 1.14x faster than a standard top-2 MoE on one 8-GPU NVLink node<sup>173</sup>. Set both `--moe-shortcut-connection` and `--moe-shortcut-parallel`, since only the second makes the all-to-alls overlap, and leave out FSDP, CUDA graphs, full recompute and `--moe-shared-expert-overlap`, which do not run with it.

##### What to watch

| Part | Symptom | Signal to watch |
| --- | --- | --- |
| Dense layers | `learns badly`: the first MoE layers balance poorly or their routing collapses. `blows up`: an image-generation MoE diverged without its leading dense layers<sup>167</sup>. `slow`: an MoE in every layer means more all-to-alls. | Aux loss (`--moe-per-layer-logging`) and MaxVio (routing trace, [A.1](#s-a-1)) in the first MoE layers after the dense block. |
| Block wiring | `slow`: the all-to-all is not hidden behind compute. | How much of the all-to-all is exposed: in an nsys timeline ([3.7 Profiling](#s-3-7-profiling)), compare the all-to-all kernels on the side stream with the compute on the main stream. |

With the router, the balancer, the experts and the block layout chosen, the architecture is complete, and what remains is training it. Where should training start, which optimizer should you use, and how will you know when something goes wrong?

#### 3.6 Training: start, optimizer, stability

![hero-anatomy-zoom](https://huggingface-moe-blogpost.hf.space/viz/posters/hero-anatomy-zoom.webp)

Training an MoE adds failure modes that a dense model does not have, and the teams behind large MoEs have run into several of them. A Switch Transformer diverged in bfloat16<sup>40</sup>, and two of six baseline ST-MoE runs went unstable<sup>41</sup>. Routing can also collapse onto a few experts, an imbalance that feeds itself<sup>179</sup>. What makes these runs fail, and how would you notice early that yours is about to?

*Table note:* Training choices reported by model authors. Initialization and optimizer entries highlight the choice relevant to this section; MTP entries describe training, which can differ from the released inference configuration.

| Model | Initialization | Optimizer | MTP | Stability choices |
| --- | --- | --- | --- | --- |
| DeepSeek-V3<sup>163</sup> | Random initialization | AdamW | 1 MTP layer | Gradient clipping at norm 1.0; embedding, output head, MoE gating, normalization and attention kept in BF16 or FP32 during FP8 training |
| DeepSeek-V4.1-Flash<sup>180</sup> | From scratch | Muon for linear weights, AdamW for normalization and non-matrix parameters | No backbone MTP during pretraining; DSpark trained separately afterward | SwiGLU clipping at 10; modality-specific balancing |
| Kimi K3<sup>181</sup> | From scratch, language and vision trained jointly from the start | Muon for matrix parameters, with per-head updates for attention projections | 1 MTP layer | Weight clipping, attention output in FP32, normalized LatentMoE, SiTU-GLU and quantile balancing |
| LongCat-Flash<sup>182</sup> | A trained 14-layer model, stacked into 28 layers | Adam-family, with hyperparameters transferred by Adam's scaling rules | MTP used as an auxiliary objective | Hidden-state z-loss, router-gradient monitoring, Adam epsilon of 1e-16 and deterministic computation |
| Step [3.5](#s-3-5) Flash<sup>183</sup> | Not reported | Muon, with its Polar Express iteration in FP16 | 3 MTP heads | Gradient clipping at 1.0; expert activation clipping; monitor expert norms alongside loss |

The first decision is where training starts, from random weights or from the dense model we already trained in [2.4](#s-2-4). What does starting from the dense checkpoint buy you, and what does it cost?

##### Upcycling

Upcycling starts the MoE from a trained dense checkpoint by copying its MLP into the experts. An expert as wide as the dense MLP gets a full copy, and a narrower one gets a slice: in our run, with a dense MLP 8192 wide and experts of 1024, [Megatron](https://github.com/NVIDIA/Megatron-LM) splits the dense MLP into 8 slices and copies each slice into 8 of the 64 experts. Either way, the MoE starts where the dense run stopped.

Copying the weights leaves a second choice: whether the optimizer state and the learning-rate schedule carry over too. Komatsuzaki et al. continued the dense run's schedule where it left off<sup>184</sup>, but reused the optimizer state only for vision models, because on language it gave no improvement<sup>185</sup>. Megatron's upcycling step saves the MoE at iteration 1 without optimizer state ([`training.py#L3069-L3083`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/training.py#L3069-L3083)), so the MoE run starts with a fresh optimizer and a new schedule.

The head start is not free: it is the compute already spent on the dense run, and a run from scratch eventually catches up with the upcycled run. How soon varies a lot. In OLMoE, a run from scratch caught up after 500B tokens, 25% of the 2T tokens the dense model had been trained on<sup>186</sup>, while in Komatsuzaki et al.'s sparse upcycling runs it took 120% of the dense checkpoint's compute<sup>187</sup>. The figure below redraws OLMoE's comparison from its public training logs: an MoE upcycled from the dense OLMo-1B after 2T tokens of training, against the same MoE trained from scratch, each for 610B tokens.

![olmoe-upcycling](https://huggingface-moe-blogpost.hf.space/viz/posters/olmoe-upcycling.webp)

*Figure caption:* Figure 3.6.1

In the figure, the upcycled run starts ahead on all four metrics, and the run from scratch narrows the gap only gradually. Its HellaSwag and MMLU accuracies come level with the upcycled run's around 500B tokens, where the authors place the catch-up, while its training and validation losses stay slightly higher until about 600B tokens.

A trained MoE can grow the same way, by copying its own experts instead of a dense MLP. The figure below turns an 8-expert MoE into a 16-expert one and shows what the copies do to routing.

![expert-upcycling](https://huggingface-moe-blogpost.hf.space/viz/posters/expert-upcycling.webp)

*Figure caption:* Figure 3.6.2

With top-2 routing and each copy inheriting its original's router row, the figure's exact copies tie: every token picks an expert and its copy at equal weight, so it runs one distinct expert instead of two. Perturbing the copy gives the router a gradient between the pair, and random new experts avoid the tie but put routing weight on untrained experts. All three have been used to grow MoEs: Expert Upcycling copies each expert with its router row, going from 32 to 64 experts<sup>188</sup>, K-EXAONE 2.0 adds a random rotation to each copy, going from 128 to 256<sup>189</sup>, Expert Upcycling also tested Drop-Upcycling, which re-initializes part of each copy's weights, half in the setting its authors found best<sup>190,191</sup>, and EMO draws the new experts and router rows from a Gaussian<sup>192</sup>. In Megatron, upcycling from a dense checkpoint is `--moe-use-upcycling` with `--moe-upcycling-granularity`, and at the pin it needs the two local fixes described in [2.5](#s-2-5).

*Collapsible:* Megatron source

*Collapsible:* [`training.py#L3043-L3083`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/training.py#L3043-L3083) (build dense, upcycle, save)

```
if args.moe_use_upcycling:
    torch.distributed.barrier()
    assert not checkpoint_exists(args.save), (
        "The upcycling destination directory already exists. "
        "Please check if --moe-use-upcycling is mistakenly enabled. "
        "Upcycling should only be set for the first run when converting the dense model. "
        "All subsequent runs should remove this flag. "
    )
    # before changing moe related global args, save them in local variables
    num_experts = args.num_experts
    expert_model_parallel_size = args.expert_model_parallel_size
    moe_ffn_hidden_size = args.ffn_hidden_size
    # set dense model related args in to global args before getting dense model
    args.num_experts = None
    args.expert_model_parallel_size = 1
    args.ffn_hidden_size = moe_ffn_hidden_size * args.moe_upcycling_granularity
    # get dense model
    dense_model_for_upcycling = _build_model_wrapper(wrap_with_ddp=True)
    # recover moe upcycling related args in global args before executing upcycling
    args.num_experts = num_experts
    args.expert_model_parallel_size = expert_model_parallel_size
    args.ffn_hidden_size = moe_ffn_hidden_size
    # execute upcycling
    _, args.num_floating_point_operations_so_far = upcycling_utils.load_and_upcycle_model(
        load_checkpoint,
        unwrapped_model,
        dense_model_for_upcycling,
        load_kwargs={
            'model': dense_model_for_upcycling,
            'optimizer': None,
            'opt_param_scheduler': None,
        },
    )
    args.iteration = 1
    save_checkpoint(
        args.iteration, model, None, None, args.num_floating_point_operations_so_far
    )
```

*Collapsible:* [`upcycling_utils.py#L145-L178`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/upcycling_utils.py#L145-L178) (scale, split, copy per expert)

```
def _get_moe_activation_scale():
    """
    Calc moe activation scale factor relative to dense activation.
    For more detail please refer to https://arxiv.org/abs/2410.07524.
    """
    if moe_router_pre_softmax:
        moe_activation_scale = (expansion_rate * granularity * granularity) / moe_router_topk
    else:
        moe_activation_scale = granularity
    return moe_activation_scale
def _get_weight_scale():
    moe_activation_scale = _get_moe_activation_scale()
    if gated_linear_unit == True:
        scale = moe_activation_scale ** (1 / 3)
    elif activation_func_name == ActivationFuncName.squared_relu:
        scale = moe_activation_scale ** (1 / 3)
    else:
        scale = moe_activation_scale ** (1 / 2)
    return scale
def _process_fc1_weight_param(param):
    param = param.clone()
    scale = _get_weight_scale()
    param = param * scale
    if activation_func_name == ActivationFuncName.silu and gated_linear_unit == True:
        param_1, param_2 = torch.chunk(param, 2, dim=0)
        params_1 = torch.tensor_split(param_1, granularity, dim=0)
        params_2 = torch.tensor_split(param_2, granularity, dim=0)
        params = [torch.cat([params_1[i], params_2[i]], dim=0) for i in range(granularity)]
    else:
        params = torch.tensor_split(param, granularity, dim=0)
    params = params * expansion_rate
    return params
```

At the pin (d6316eb45), the path ran for us only with two local fixes ([2.5](#s-2-5)). Pass the model to `load_checkpoint` under its parameter name, `ddp_model`:

*Collapsible:* [`checkpointing.py#L2632-L2635`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/checkpointing.py#L2632-L2635) (the `ddp_model` parameter)

```
def load_checkpoint(
    ddp_model,
    optimizer,
    opt_param_scheduler,
```

Then build the dense model from the arguments with `num_experts` unset, rather than from the config container that `pretrain_gpt.py` made once at start-up, so that the dense checkpoint loads into a dense model:

*Collapsible:* [`training.py#L2917-L2925`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/training.py#L2917-L2925) (the model built from the config container)

```
def _build_model_wrapper(wrap_with_ddp: bool):
    if cfg_container is not None and getattr(cfg_container, "model", None) is not None:
        from megatron.training.utils import start_memory_history_recording
        start_memory_history_recording(cfg_container.profiling)
        cfg = cfg_container
        model_config = cfg.model
        builder_cls = model_config.get_builder_cls()
```

> **Watch:** An upcycle that went wrong loses its head start, so compare its loss with the dense run continued for the same tokens. Since the experts start as identical copies, also watch MaxVio per layer while they drift apart, computed offline from the routing trace ([A.1](#s-a-1)).

> **Recommendation:** Use it when a dense checkpoint exists and the MoE run is short, since a run from scratch caught up after 25% of the dense model's training tokens in OLMoE and 120% of its compute in Komatsuzaki et al.'s runs<sup>186,187</sup>. Upcycling is an initialization, so set it on the first run only, and at the pin apply the two local fixes from [2.5](#s-2-5) first.

Whether you upcycle or start from random weights only decides where the weights begin; from the first step on, the optimizer decides where they go. Each expert, though, sees only the tokens routed to it, so should your optimizer move an expert that got a handful of tokens as far as a busy one?

##### Optimizer

AdamW, the optimizer DeepSeek-V3 trained with<sup>163</sup>, scales each weight's update by that weight's own gradient history, so how far an expert moves follows the gradients its tokens produced. Muon, an optimizer for weight matrices used by several recent MoEs, sizes the step another way. It orthogonalizes each update, pushing its nonzero singular values toward one, and then multiplies it by a scale set by the matrix's shape alone, so the size of the step no longer depends on how large the gradient behind it is.

Megatron orthogonalizes each expert's matrix on its own ([`transformer_engine.py#L2665-L2668`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/extensions/transformer_engine.py#L2665-L2668), [`transformer_config.py#L956`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L956), [`emerging_optimizers.py#L147-L149`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/optimizer/emerging_optimizers.py#L147-L149)), as DeepSeek-V4 does<sup>193</sup>, so an expert the router rarely picks can move about as far as the busiest one, only in its own direction, and it keeps moving even in a step where it got no tokens, along its momentum. The figure below shows what that means over 49 toy experts, plotting update size against tokens per step for AdamW, for Muon applied to each expert separately, and for Muon over all experts as one matrix.

![muon-expert-steps](https://huggingface-moe-blogpost.hf.space/viz/posters/muon-expert-steps.webp)

*Figure caption:* Figure 3.6.3

As an expert's tokens fall in the toy, its update shrinks under AdamW as the gradient turns to noise and, under Muon over all experts as one matrix, with the size of its gradient, while per-expert Muon keeps the busiest expert's step down to a few tokens per step. Below that, the per-expert step shrinks too: each token adds a single direction to the gradient, and with so few tokens even the momentum of recent steps no longer fills the expert's matrix.

The figure shows how Muon moves each expert; whether that trains a better MoE has been measured on whole models. Moonlight, an MoE with 3B active and 16B total parameters, performed significantly better with Muon than its twin trained with AdamW under the same settings, compared at about 1.2T tokens<sup>194</sup>.

Once you are on Muon, one choice remains that adopters make differently: which optimizer updates the router. DeepSeek-V4 keeps it on Muon<sup>193</sup>, while Qwen3.8-Next moved it to AdamW after Muon destabilized the router early in training<sup>195</sup>. Lau and Su compared router optimizers on two small MoEs, one shaped like OLMoE-1B-7B and a downsized gpt-oss: with Muon on the hidden matrices, AdamW on the router ended slightly worse than row-normalized or left-spectral router updates<sup>196</sup>.

In Megatron, Muon is `--optimizer muon`, and to put the router on Adam instead, add `--moe-router-skip-muon`, available from [Megatron Core v0.20](https://github.com/NVIDIA/Megatron-LM/releases/tag/core_v0.20.0) on.

*Collapsible:* Megatron source

*Collapsible:* [`emerging_optimizers.py#L147-L154`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/optimizer/emerging_optimizers.py#L147-L154) (which params go to Adam)

```
def _is_nonlinear_or_embedding(param):
    """True for parameters that should NOT use the emerging optimizer."""
    return getattr(param, 'is_embedding_or_output_parameter', False) or len(param.shape) != 2
def _is_muon_excluded(param):
    """True for parameters that should use the scalar optimizer instead of Muon."""
    return not getattr(param, 'use_muon', True) or _is_nonlinear_or_embedding(param)
```

*Collapsible:* [`router.py#L88-L91`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L88-L91) (router off Muon)

```
if self.config.moe_router_skip_muon:
    setattr(self.weight, 'use_muon', False)
    if self.bias is not None:
        setattr(self.bias, 'use_muon', False)
```

*Collapsible:* [`emerging_optimizers.py#L303-L324`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/optimizer/emerging_optimizers.py#L303-L324) (orthogonalize, then shape scale)

```
if scale_shape is None:
    size = [grad.size(-2), grad.size(-1)]
    if partition_dim is not None:
        size[partition_dim] *= get_pg_size(tp_group)
else:
    # This overrides only the final Muon scalar; NS still uses grad's physical
    # shape and partition metadata for its collectives.
    size = scale_shape
# Only forward the kwarg when enabled; older emerging_optimizers do not
# accept it at all, and __init__ has already rejected use_syrk on those.
ns_kwargs = {"use_syrk": True} if use_syrk else {}
orth_grad = newton_schulz_tp(
    grad,
    steps=num_ns_steps,
    coefficient_type=coefficient_type,
    tp_group=tp_group,
    partition_dim=partition_dim,
    tp_mode="duplicated" if tp_mode_this_group == "blockwise" else tp_mode_this_group,
    **ns_kwargs,
)
scale_factor = get_muon_scale_factor(size[0], size[1], mode=scale_mode)
return orth_grad * scale_factor * extra_scale_factor
```

*Collapsible:* [`arguments.py#L1792-L1798`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/arguments.py#L1792-L1798) (stacked experts: undefined)

```
assert not (
    args.use_layer_wise_distributed_optimizer and args.moe_single_grouped_weight
), (
    "The LayerWise distributed optimizer does not support --moe-single-grouped-weight: "
    "Muon semantics for a single grouped [E, N, K] expert weight are not defined. "
    "Disable --moe-single-grouped-weight or use Adam/DistributedOptimizer."
)
```

> **Watch:** Under Muon, experts can collapse<sup>197</sup>, and too large an update scale can make the run diverge<sup>198</sup>. Track what each expert receives and produces: tokens per expert per step, offline from the routing trace ([A.1](#s-a-1)), and, per layer, the largest and the smallest expert output norm, each divided by the layer's median, from a forward hook of ours ([A.1](#s-a-1)).

> **Recommendation:** Use Muon when you can afford to tune it. Start at `--muon-extra-scale-factor 0.2`, since Megatron's default of 1.0 diverged on a dense 7B in Mellum2's tests<sup>198</sup>, and choose the router's optimizer with `--moe-router-skip-muon`, a call adopters make both ways. It does not run with Megatron-FSDP or Torch-FSDP2.

However the optimizer moves the weights, each step still learns only from predicting the next token. Could you get more signal out of each step by predicting further ahead, and what would that cost in step time?

##### MTP

Multi-token prediction adds one transformer layer per extra token to predict. That layer takes the main model's hidden state together with the next token's embedding, and predicts the token after next through the shared output head. DeepSeek-V3 found it better on most benchmarks at both of its test scales, and the extra layer can be discarded at inference<sup>199</sup>. The figure below follows one position of the sequence through that wiring.

![mtp-layer](https://huggingface-moe-blogpost.hf.space/viz/posters/mtp-layer.webp)

*Figure caption:* Figure 3.6.4

On their way in, the two inputs each go through their own RMSNorm, and the MTP layer concatenates them and projects the result from twice the hidden size back to it before its transformer block. Both predictions come out of the same output head, and the MTP loss is weighted and added to the main loss<sup>199</sup>.

The extra layer costs step time, and under [pipeline parallelism](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=pipeline_parallelism) that cost lands in one place: unless the layout moves it, Megatron puts the MTP layer on the last stage ([`multi_token_prediction.py#L886-L905`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/multi_token_prediction.py#L886-L905)), which already holds the output head the MTP layer reuses. On our 256-node runs, early steps took about 37% longer with one MTP layer than without, and spreading the model over 8 pipeline stages did not close that gap. Mellum2 reports 7% extra training time for a 14B MoE<sup>200</sup>.

*Collapsible:* Megatron source

*Collapsible:* [`multi_token_prediction.py#L1709-L1714`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/multi_token_prediction.py#L1709-L1714) (hidden plus next-token embedding)

```
hidden_states = apply_module(self.hnorm)(hidden_states)
hidden_states = make_viewless_tensor(
    inp=hidden_states, requires_grad=True, keep_graph=True
)
hidden_states = torch.cat((decoder_input, hidden_states), -1)
hidden_states, _ = self.eh_proj(hidden_states)
```

*Collapsible:* [`multi_token_prediction.py#L1276-L1276`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/multi_token_prediction.py#L1276-L1276) (loss times factor over depth)

```
mtp_loss_scale = config.mtp_loss_scaling_factor / config.mtp_num_layers
```

*Collapsible:* [`multi_token_prediction.py#L932-L937`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/multi_token_prediction.py#L932-L937) (no layout: last stage)

```
# without custom PP layout, we only support put all of MTP layers on the last pipeline stage
if mtp_num_layers is not None:
    if pp_size is None:
        # Compatibility fallback for callers without explicit pipeline metadata.
        pp_size = parallel_state.get_pipeline_model_parallel_world_size()
    mtp_on_this_rank = pp_rank == pp_size - 1
```

*Collapsible:* [`multi_token_prediction.py#L2598-L2599`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/multi_token_prediction.py#L2598-L2599) (detach cuts trunk gradient)

```
if self.config.mtp_detach_heads:
    hidden_states = hidden_states.detach()
```

Much of that gap may come from where the layer sits. A pipeline step waits for its slowest stage, so a layer added to one stage slows the step by its share of that stage's work, not by its much smaller share of the whole model. Ling 2.0's team ran into the same imbalance: they measured an MTP layer at about 1.7 times the compute of a standard MoE layer, and repartitioning the pipeline around it gained 40% end to end<sup>201</sup>.

Megatron turns MTP on with `--mtp-num-layers`, the number of extra depths to add, and `--mtp-loss-scaling-factor` weights the MTP loss: DeepSeek-V3 used 0.3 for its first 10T tokens and 0.1 after<sup>163</sup>, and Mellum2 used 0.1<sup>200</sup>. To choose which stage holds the MTP layer, written `m`, use `--pipeline-model-parallel-layout`. If you want the MTP layer only as a draft model for speculative decoding, `--mtp-detach-heads` detaches its inputs, so the MTP loss trains the MTP layer and leaves the main model alone.

> **Watch:** Megatron logs an `mtp_1 loss` next to the lm loss whenever MTP is on, while the MTP layer's cost shows elsewhere, in step time and in the memory of the stage that holds it. To find the slow stage, log forward and backward compute time per pipeline rank with `--timing-log-level 2 --timing-log-option all` ([A.1](#s-a-1)); the stage holding the MTP layer should show up as the slowest rank.

> **Recommendation:** Use it when the denser training signal DeepSeek-V3 reports<sup>199</sup> is worth the step time. Under pipeline parallelism, place the MTP layer with `--pipeline-model-parallel-layout`, or the last stage carries it.

Each part so far has told you what to watch for its own choice. Some failures, though, belong to no single choice and can start anywhere in the model, so what should every run have in place to catch them?

##### Stability

An MoE run can fail loudly or quietly. A loud failure shows in the loss, which spikes or turns into NaN, while a quiet one, such as routing collapse<sup>76</sup> or a rogue expert<sup>15</sup>, can leave the loss flat.

The loudest failure is also the easiest to catch, since Megatron checks every step's loss and gradients for a NaN by default ([3.0](#s-3-0)). What you want to know next is whether to blame the hardware, so when the check fires, Megatron reruns the step (`--rerun-mode validate_results`, also on by default). The first rerun, on the same GPU, tells a transient error from one that repeats. If the NaN repeats, Megatron exits with code 16 so that the job restarts from a checkpoint on another GPU, where the second rerun tells a faulty GPU from a NaN that the data or the model really produced.

Bad hardware and bad batches do not always end in a NaN, because they can also return a finite loss or gradient with a far too large exponent. Megatron catches those with `--check-for-spiky-loss` and `--check-for-large-grads`: each flags a value 10x the largest of the first 100 it has seen, reruns the step once on the same GPU, logs whether the value came back, and keeps training.

All of these checks react to a step that has already gone wrong. To stop the loss from breaking in the first place, [3.1](#s-3-1) already protects the router, with fp32 math and a z-loss that holds its logits down, and recent large MoEs add guards of their own. Some cap a value before it can grow: DeepSeek-V3 and Step [3.5](#s-3-5) Flash clip the gradient norm<sup>163,183</sup>, DeepSeek-V4.1-Flash clamps the experts' SwiGLU activations<sup>180</sup>, and Step [3.5](#s-3-5) Flash clips expert activations as well<sup>183</sup>. Others keep the most sensitive operations in higher precision: DeepSeek-V3 kept its embedding, output head, MoE gating, normalization and attention in BF16 or FP32 during FP8 training<sup>163</sup>, and Kimi K3 keeps the attention output in FP32<sup>181</sup>. LongCat-Flash carries the z-loss idea over to the hidden states<sup>182</sup>.

The quiet failures may not show in the loss at all, so you have to look for them elsewhere. The figure below simulates three of them next to a healthy run: routing collapse, a dead expert and a rogue expert.

![moe-failure-signals](https://huggingface-moe-blogpost.hf.space/viz/posters/moe-failure-signals.webp)

*Figure caption:* Figure 3.6.5

Since the simulation keeps the loss flat through all three failures, only the other signals tell them apart from the healthy run. Routing collapse drives MaxVio up. A dead expert pulls the smallest expert output norm far below the layer's median, and a rogue expert pushes the largest far above it, from about 14 to about 5,700 times the median as in Step [3.5](#s-3-5) Flash's layer 45<sup>15</sup>. The loss alarm, 0.1 above the lowest loss so far, borrows the margin of Qwen3.8-Next's spike criterion<sup>202</sup>.

*Collapsible:* Megatron source

*Collapsible:* [`pretrain_gpt.py#L263-L292`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/pretrain_gpt.py#L263-L292) (NaN, Inf, spiky loss)

```
# Check individual rank losses are not NaN prior to DP all-reduce.
rerun_state_machine = get_rerun_state_machine()
if args.check_for_nan_in_loss_and_grad:
    rerun_state_machine.validate_result(
        result=loss,
        rejection_func=torch.isnan,
        message="found NaN in local forward loss calculation",
        tolerance=0.0,  # forward pass calculations are deterministic
        fatal=True,
    )
    rerun_state_machine.validate_result(
        result=loss,
        rejection_func=torch.isinf,
        message="found Inf in local forward loss calculation",
        tolerance=0.0,  # forward pass calculations are deterministic
        fatal=True,
    )
# Check for spiky loss
if args.check_for_spiky_loss:
    rerun_state_machine.validate_result(
        result=loss,
        rejection_func=partial(
            rerun_state_machine.is_unexpectedly_large,
            threshold=SPIKY_LOSS_FACTOR,
            context="loss",
        ),
        message="Spiky loss",
        tolerance=0.0,  # forward pass calculations are deterministic
        fatal=False,
    )
```

*Collapsible:* [`param_and_grad_buffer.py#L389-L425`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/distributed/param_and_grad_buffer.py#L389-L425) (per-bucket grad norm checks)

```
def check_grads(self, check_for_nan_or_inf, check_for_large):
    """
    Make sure norm of grads in bucket are not NaN prior to data-parallel
    all-reduce / reduce-scatter.
    """
    rerun_state_machine = get_rerun_state_machine()
    for i in range(len(self.buckets)):
        grad_norm = self.buckets[i].grad_data.norm(p=2)
        # check for NaN, Inf and unexpectedly large grads
        if check_for_nan_or_inf:
            rerun_state_machine.validate_result(
                result=grad_norm,
                rejection_func=torch.isnan,
                message=f"found NaN in local grad norm for bucket #{i} "
                f"in backward pass before data-parallel communication collective",
                tolerance=0.001,  # 0.1% tolerance to account for non-deterministic FA backward
                fatal=True,
            )
            rerun_state_machine.validate_result(
                result=grad_norm,
                rejection_func=torch.isinf,
                message=f"found Inf in local grad norm for bucket #{i} "
                f"in backward pass before data-parallel communication collective",
                tolerance=0.001,  # 0.1% tolerance to account for non-deterministic FA backward
                fatal=True,
            )
        if check_for_large:
            rerun_state_machine.validate_result(
                result=grad_norm,
                rejection_func=partial(
                    rerun_state_machine.is_unexpectedly_large, threshold=10, context="grads"
                ),
                message=f"found unexpected large grads in bucket #{i} "
                f"in backward pass before data-parallel communication collective",
                tolerance=0.001,  # 0.1% tolerance to account for non-deterministic FA backward
                fatal=False,
            )
```

*Collapsible:* [`rerun_state_machine.py#L752-L766`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/rerun_state_machine.py#L752-L766) (10x the early maximum)

```
value: float = math.fabs(result.item())
# Ignore NaNs and Infs. They should be checked separately.
if math.isnan(value) or math.isinf(value):
    return False
if resample or context not in self.large_value_counts:
    self.large_value_counts[context] = 0
if self.large_value_counts[context] < num_samples:
    self.large_value_counts[context] += 1
    self.max_values[context] = max(self.max_values.get(context, 0.0), value)
    if self.large_value_counts[context] == num_samples:
        logger.warning(f"Max value for {context}: {self.max_values[context]}")
    return False
return value >= self.max_values[context] * threshold
```

*Collapsible:* [`rerun_state_machine.py#L622-L694`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/rerun_state_machine.py#L622-L694) (rerun here, then elsewhere)

```
if self.state == RerunState.RERUNNING_IN_PLACE:
    if comparison > tolerance:
        if not fatal:
            self.continue_requested = True
        log_failure(
            "First rerun: unexpected result is not reproducible within the tolerance "
            f"({result} != {self.initial_result})",
            fatal=fatal,
        )
        self._log_validation_error_to_file(
            status=RerunValidationStatus.FIRST_RERUN_NOT_REPRODUCIBLE,
            result=result,
            message=message,
        )
        log_failure("Possible transient error!", fatal=fatal)
    else:
        if fatal:
            self.checkpoint_requested = True
        else:
            self.continue_requested = True
        # Remember the node and device we're running on so that we can check we're not
        # rerunning on the same GPU when we resume from the checkpoint.
        self.suspicious_node = os.uname()[1]
        self.suspicious_device = torch.cuda.current_device()
        self._log_validation_error_to_file(
            status=RerunValidationStatus.FIRST_RERUN_REPRODUCIBLE,
            result=result,
            message=message,
        )
        log_failure(
            "First rerun: unexpected result is reproducible within the tolerance "
            f"({result} = {self.initial_result}). "
            "Need to rerun on a different GPU to verify correctness.",
            fatal=fatal,
        )
# This is the second re-run.
elif self.state == RerunState.RERUNNING_FROM_CHECKPOINT:
    # Ensure we're not on the same GPU as the first rerun.
    node = os.uname()[1]
    device = torch.cuda.current_device()
    if node == self.suspicious_node and device == self.suspicious_device:
        logger.error(
            f"Got rescheduled on the same GPU. Need to resume again from the same "
            f"checkpoint (node: {self.suspicious_node}, gpu: {self.suspicious_device})"
        )
        self.restart_again_requested = True
    elif comparison > tolerance:
        self._log_validation_error_to_file(
            status=RerunValidationStatus.SECOND_RERUN_NOT_REPRODUCIBLE,
            result=result,
            message=message,
        )
        logger.warning(
            "Second rerun: unexpected result is not reproducible on a different GPU, "
            f"therefore was likely incorrect ({result} != {self.initial_result})"
        )
        log_failure("Possible persistent error!")
        if not fatal:
            self.continue_requested = True... 13 more lines
```

> **Watch:** For spikes, watch the router's logits through the z-loss ([3.1](#s-3-1)). The failures that leave the loss flat need signals of their own: for routing collapse, MaxVio per layer, computed offline from the routing trace ([A.1](#s-a-1)), next to the load-balancing loss, and for dead and rogue experts, the largest and the smallest expert output norm in each layer over the layer's median, from a hook of ours ([A.1](#s-a-1)).

> **Recommendation:** Use it always: keep the default NaN check and `--rerun-mode validate_results`.

##### What to watch

| Part | Symptom | Signal to watch |
| --- | --- | --- |
| Upcycling | `learns badly`: the loss falls slowly at first. | Loss against the dense run continued for the same tokens. While the copied experts drift apart, also MaxVio per layer (routing trace, [A.1](#s-a-1)). |
| Optimizer | `learns badly`: experts collapse. `blows up`: when orthogonalization runs in bf16, or when the update scale is too large. | Tokens per expert per step (routing trace, [A.1](#s-a-1)). Per layer, the largest and smallest expert output norm, each over the median (forward hook, [A.1](#s-a-1)). |
| MTP | `slow`: one pipeline stage takes longer than the others. `OOM`: MTP with 53 layers on 4 pipeline stages ran out of memory. | `mtp_1 loss` alongside LM loss; step time and peak memory; forward and backward compute time per pipeline rank (`--timing-log-level 2 --timing-log-option all`, [A.1](#s-a-1)), especially the stage holding MTP<sup>201</sup>. |
| Stability | `blows up`: NaNs and loss spikes. `learns badly`: routing collapse, dead experts or rogue experts. | The router z-loss ([3.1](#s-3-1)), for the router logits ST-MoE traced its instabilities to<sup>38</sup>. Per layer, MaxVio (routing trace) and the largest and smallest expert output norm over the median ([A.1](#s-a-1)). |

A run that trains cleanly can still spend a large share of each step waiting on communication rather than computing. Where does the time in an MoE step go, and how much of it can you get back?

#### 3.7 Systems: where the time goes and how to get it back

![hero-anatomy-zoom](https://huggingface-moe-blogpost.hf.space/viz/posters/hero-anatomy-zoom.webp)

Every MoE layer sends its tokens to their experts and brings them back, and on a real run that traffic can take much of the step. In the one step we traced on one node, half the time was exposed all-to-all, while the router was still unbalanced. The figure below zooms in on those two transfers, dispatch out to the experts and combine back, which run over NVLink inside a node and over the fabric across nodes.

You can place the experts so that less traffic crosses the slower network between nodes, and hide the traffic that remains behind other compute. You can keep the memory that costs in check, cap how many nodes each token reaches, and trade dropped tokens or precision for speed. Each part comes from its own setup, so do not add their gains together; test them as alternatives, one at a time.

*Table note:* Systems choices documented in model reports. Parallelism and overlap describe training; post-training quantization is labeled separately. These are model-specific implementations, not interchangeable Megatron flag settings.

| Model | Interconnect and overlap | Memory and precision | Routing constraints |
| --- | --- | --- | --- |
| DeepSeek-V3<sup>203</sup> | EP64 across 8 nodes; DualPipe overlaps computation and communication | FP8 [mixed-precision](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=mixed_precision_training) training; recompute RMSNorm, MLA up-projections and SwiGLU outputs | At most 4 target nodes per token; no token dropping |
| DeepSeek-V4<sup>204</sup> | Fused MoE pipeline schedules expert groups in waves to overlap dispatch, GEMMs and combine | Tensor-level checkpointing and selective recomputation | Removes V3's target-node limit |
| Kimi K3<sup>205,21</sup> | Optimizer fetches only locally owned parameter shards; communication pipelined with computation | Avoids a full-parameter gather buffer; SFT/RL use MXFP4 expert weights and MXFP8 activations | One expert group in the released config<sup>206</sup> |
| LongCat-Flash<sup>178,207</sup> | EP groups of 32 accelerators; pipelined all-gather/reduce-scatter and shortcut-connected MoE | BF16 training with deterministic kernels | Identity experts require no expert communication |

Before reaching for any of these levers, you need to see where your own step spends its time, since each kind of waste calls for a different fix. What does one profiled step on a single node show?

##### Profiling

[Megatron](https://github.com/NVIDIA/Megatron-LM) can record a trace of any step for you. With `--profile` alone it records an nsys trace, and `--use-pytorch-profiler` switches it to a torch profiler trace ([`argument_utils.py#L706-L709`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/argument_utils.py#L706-L709)). In either case, `--profile-step-start`, `--profile-step-end` and `--profile-ranks` pick which steps and ranks to trace. The step we traced comes from a 7B-A1B MoE, with 7B parameters in total and 1B active per token. Its 16 layers hold 64 experts each with top-8 routing, and it trained on one node of 8 H100s. Tracing it cost one short job, which traced iteration 4 and had moved past it within about six minutes of launch. The figures below break that step down and annotate its trace.

![step-breakdown](https://huggingface-moe-blogpost.hf.space/viz/posters/step-breakdown.webp)

*Figure caption:* Figure 3.7.1

![annotated-trace](https://huggingface-moe-blogpost.hf.space/viz/posters/annotated-trace.webp)

*Figure caption:* Figure 3.7.2

The all-to-all took half of that step, but how much of that half was the network actually moving data? When one GPU's experts get more tokens than the rest, that GPU finishes its expert compute late, and NVIDIA's Megatron Core team reports that the other ranks then wait for it at synchronization points<sup>208</sup>. In an MoE layer the all-to-all can be one of those points, so part of its time in a trace can be waiting rather than moving data. Our step had a load-balancing loss of [3.2](#s-3-2), where 1 is balanced, so its router was still unbalanced. A separate run of the same config, with routing forced even, ran that same iteration 40% faster.

*Collapsible:* Megatron source

*Collapsible:* [`training.py#L4955-L4982`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/training.py#L4955-L4982) (torch profiler window per rank)

```
if (
    cfg.profiling.use_pytorch_profiler
    and (len(cfg.profiling.profile_ranks) == 0 or
         torch.distributed.get_rank() in cfg.profiling.profile_ranks)
):
    if cfg.profiling.pytorch_profiler_collect_chakra:
        et_dir = Path(f"{cfg.logger.tensorboard_dir}/../chakra")
        et_dir.mkdir(parents=True, exist_ok=True)
        et = torch.profiler.ExecutionTraceObserver().register_callback(f"{et_dir}/rank-{torch.distributed.get_rank()}.json.gz")
    else:
        et = None
    def trace_handler(p):
        profile_dir = Path(f"{cfg.logger.tensorboard_dir}/../torch_profile")
        profile_dir.mkdir(parents=True, exist_ok=True)
        p.export_chrome_trace(f"{profile_dir}/rank-{torch.distributed.get_rank()}.json.gz")
    prof = torch.profiler.profile(
        schedule=torch.profiler.schedule(
            wait=max(cfg.profiling.profile_step_start - 1, 0),
            warmup=1 if cfg.profiling.profile_step_start > 0 else 0,
            active=cfg.profiling.profile_step_end - cfg.profiling.profile_step_start,
            repeat=1,
        ),
        on_trace_ready=trace_handler,
        record_shapes=cfg.profiling.pytorch_profiler_collect_shapes,
        with_stack=cfg.profiling.pytorch_profiler_collect_callstack,
        execution_trace_observer=et,
    )
    prof.start()
```

*Collapsible:* [`training.py#L5041-L5053`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/training.py#L5041-L5053) (nsys start at step)

```
if ((cfg.profiling.use_nsys_profiler or cfg.profiling.use_pytorch_profiler)
    and (len(cfg.profiling.profile_ranks) == 0 or
         torch.distributed.get_rank() in cfg.profiling.profile_ranks)):
    # Enable NVTX range when profiling starts and nvtx_ranges is set.
    if iteration == cfg.profiling.profile_step_start and cfg.profiling.nvtx_ranges:
        configure_nvtx_profiling(True)
    if cfg.profiling.use_pytorch_profiler:
        prof.step()
    elif iteration == cfg.profiling.profile_step_start:
        torch.cuda.check_error(torch.cuda.cudart().cudaProfilerStart())
        if cfg.profiling.record_shapes:
            nsys_nvtx_context = torch.autograd.profiler.emit_nvtx(record_shapes=cfg.profiling.record_shapes)
            nsys_nvtx_context.__enter__()
```

On your own run, start with the balance signals of [3.2](#s-3-2). MaxVio, computed from the token counts that `--save-tokens-per-expert-interval` writes, shows how uneven the load is across experts. Summing those counts over each GPU's experts shows which rank receives the most tokens, and so which rank the others most likely wait for. To see how much of the all-to-all that imbalance costs, re-trace with `--moe-router-force-load-balancing`, which swaps the router's logits for random ones so that every expert gets about the same load ([`router.py#L1185-L1187`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L1185-L1187)). If the all-to-all shrinks under forced balance, imbalance is costing you time that better balancing ([3.3](#s-3-3)) can win back, and what remains is mostly the transfer, which the rest of this section works on.

Traces also show which MoE kernels are worth fusing. Before dispatch, Megatron reorders the tokens so that each expert's tokens sit together ([`token_dispatcher.py#L668-L682`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/token_dispatcher.py#L668-L682)), and after combine it puts them back in order ([`#L893-L900`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/token_dispatcher.py#L893-L900)). With `--moe-permute-fusion`, the permute and copy kernels that do this fall from 11.45% to 7.14% of the step, and step time drops [3.3](#s-3-3)%.

> **Watch:** Judge each change by step time or TFLOP/s. A trace then tells you why the number moved: read the share of the step that the all-to-all leaves exposed.

> **Recommendation:** Use it once for every new config: trace one step at the node count you will run. If the all-to-all takes a large share of it, check MaxVio and re-trace with `--moe-router-force-load-balancing`: fix balancing first ([3.3](#s-3-3)) if the all-to-all shrinks, and work on Interconnect and Overlap below if it does not. If permute and copy kernels take a large share, try `--moe-permute-fusion`.

The step we traced kept its all-to-all inside one node, on NVLink, and a larger run cannot always do that. What happens to the step when an expert-parallel group spans two nodes and its all-to-all has to cross the network between them?

##### Interconnect

Between nodes, the all-to-all leaves NVLink for the cluster's network fabric, InfiniBand or AWS's EFA for instance, so the first thing to check is that [NCCL](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=nccl) uses that fabric at all. It can fall back to plain TCP sockets even when the fabric is requested: two of our runs set `FI_PROVIDER=efa` and named an OFI plugin, NCCL still logged "Using network Socket", and they ran about 25x slower than our EP16 run on EFA. The next figure shows the settings we tried, in order.

![efa-settings](https://huggingface-moe-blogpost.hf.space/viz/posters/efa-settings.webp)

*Figure caption:* Figure 3.7.3

In the figure, NCCL reached EFA only once the host's RDMA libraries came first on the library path; naming the plugin, by path or by name, left it on sockets. With the fabric working, what is left to choose is the expert-parallel size, `--expert-model-parallel-size`, which decides how far the all-to-all has to travel. With expert tensor parallelism at 1 and the default rank order, Megatron forms each EP group from consecutive ranks ([`parallel_state.py#L921-L929`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/parallel_state.py#L921-L929)). An EP size that divides the number of GPUs in a node then keeps the all-to-all inside that node, on NVLink, and a larger one spreads it over several nodes. Our nodes hold eight H100s each, so the figure below compares EP8 in one node with EP16 across two.

![ep-placement](https://huggingface-moe-blogpost.hf.space/viz/posters/ep-placement.webp)

*Figure caption:* Figure 3.7.4

Spread over two nodes, EP16 ran 59% below EP8 in one node, even with EFA working, although the two runs also differ in their nodes and in how many micro-batches each step accumulates.

*Collapsible:* Megatron source

*Collapsible:* [`parallel_state.py#L920-L930`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/parallel_state.py#L920-L930) (expert grid, EP after TP)

```
expert_order = _inject_gtp_remat_axis(order, after="ep")
expert_decoder_rank_generator = RankGenerator(
    tp=expert_tensor_parallel_size,
    ep=expert_model_parallel_size,
    dp=expert_data_parallel_size,
    pp=pipeline_model_parallel_size,
    cp=1,
    order=expert_order,
    rank_offset=rank_offset,
    gtp_remat=expert_gtp_remat_size,
)
```

*Collapsible:* [`parallel_state.py#L1419-L1428`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/parallel_state.py#L1419-L1428) (consecutive ranks form EP)

```
for ranks in expert_decoder_rank_generator.get_ranks('ep'):
    group = create_group(
        ranks,
        timeout=timeout,
        pg_options=get_nccl_options("ep", nccl_comm_cfgs),
        group_desc="EXPERT_MODEL_PARALLEL_GROUP",
    )
    if rank in ranks:
        _EXPERT_MODEL_PARALLEL_GROUP = group
        _EXPERT_MODEL_PARALLEL_RANKS = ranks
```

> **Watch:** A fallback to sockets slowed our two-node run by the factor above, so check the startup log first. With `NCCL_DEBUG=INFO`, NCCL prints "Using network" and the transport it picked. You want your fabric's transport there, such as Libfabric for the OFI plugin on EFA, while "Using network Socket" means the fallback. Once the fabric is confirmed, compare alltoall bus bandwidth inside and across nodes from [nccl-tests](https://github.com/NVIDIA/nccl-tests) ([2.1](#s-2-1)). Then measure TFLOP/s per GPU at an EP size that fits in one node and at one that spans two.

> **Recommendation:** Use [expert parallelism](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=expert_parallelism) inside a node when the model fits that way: start there, add nodes as [data-parallel](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=data_parallelism) replicas, and time both placements at your node count before you commit.

Even on a working interconnect, the tokens that cross it still sit on the critical path while the GPUs wait. Is there other work the GPUs could do while the tokens are in flight?

##### Overlap

We've already seen in [3.5 Block wiring](#s-3-5-block-wiring) how changing the architecture hides the all-to-all inside one micro-batch. A parallel block can run dispatch while attention computes, and a shortcut-connected MoE can also hide combine behind the dense compute that runs beside it. Rewiring changes what the router sees, however, and you may not want to touch an architecture you have already settled on. Without rewiring, the exposed all-to-all is hard to hide inside one micro-batch. A training step, however, runs many micro-batches, and the work of one does not wait on another until their gradients are summed.

Megatron borrows that work: `--overlap-moe-expert-parallel-comm` runs one micro-batch's forward beside another's backward, so the all-to-all of one hides behind the compute of the other ([`model_parallel_config.py#L349-L352`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/model_parallel_config.py#L349-L352)). Pipeline schedules also pair one micro-batch's forward with another's backward, as the [Ultra-Scale Playbook](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=zero_bubble_and_dualpipe) describes, and DeepSeek-V3's DualPipe uses that pairing to hide its all-to-alls<sup>209</sup>. The figure below draws one MoE layer with and without that interleaving.

![combined-1f1b](https://huggingface-moe-blogpost.hf.space/viz/posters/combined-1f1b.webp)

*Figure caption:* Figure 3.7.5

Drawn with one micro-batch after the other, the layer leaves all four all-to-alls exposed. The interleaved drawing also sets `--delay-wgrad-compute`, which Megatron's MoE guide pairs with the overlap ([`README.md#L434`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/README.md?plain=1#L434)). That flag computes the weight gradients later, so the backward dispatch waits only for the experts' input gradients and runs under that micro-batch's own delayed expert weight gradients ([`model_chunk_schedule_plan.py#L266-L268`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/models/common/model_chunk_schedule_plan.py#L266-L268)), while the other three all-to-alls run under compute from the other micro-batch. On our runs, which set the overlap flag alone, the overlap raised throughput by up to 35% on two nodes. It also costs memory: rank 0 reserved 5 to 10 GB more, while its peak allocated memory barely moved.

*Collapsible:* Megatron source

*Collapsible:* [`combined_1f1b.py#L54-L67`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/pipeline_parallel/combined_1f1b.py#L54-L67) (one forward beside one backward)

```
"""Scheduler for 1f1b with no pipelining.
This function schedules micro-batches in a way that the forward pass of Transformer layers
for one micro-batch runs in parallel with the backward pass of another.
Each layer's forward and backward operations are co-scheduled to maximize the overlap of
their computations and communications.
EP A2A in forward step is hidden by the attention/mlp computation in the backward step,
and vice versa.
Assuming we have 4 microbatches, the schedule is as follows:
Phases 0: 1st microbatch forward
Phases 1: 1st microbatch backward + 2nd microbatch forward
Phases 2: 2nd microbatch backward + 3rd microbatch forward
Phases 3: 3rd microbatch backward + 4th microbatch forward
Phases 4: 4th microbatch backward
```

*Collapsible:* [`model_chunk_schedule_plan.py#L226-L294`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/models/common/model_chunk_schedule_plan.py#L226-L294) (dispatch hidden behind MLP backward)

```
def run(f_layer, b_layer, f_input=None, b_grad=None, is_last_layer_in_bwd=False):
    """Schedule one-forward-one-backward operations for a single transformer layer.
    This function interleaves forward and backward operations, overlapping the communications
    (dispatch or combine) of one with the computations (pre_dispatch or mlp) of the other
    to maximize parallelism and efficiency.
    When f_layer and b_layer are not None, forward and backward pass are overlapped as follows:
    comm_stream: combine_bwd       | dispatch_fwd->dispatch_bwd  | combine_fwd
    comp_stream: pre_dispatch_fwd  | mlp_bwd->mlp_bwd_dw->mlp_fwd| pre_dispatch_bwd
    For MTP, mtp_post_process_fwd is executed after the combine_fwd in the comp_stream,
    and mtp_post_process_bwd is executed before the combine_bwd in the comp_stream.
    Args:
        f_layer (TransformerLayerSchedulePlan): Forward layer (for current microbatch)
        b_layer (TransformerLayerSchedulePlan): Backward layer (for previous microbatch)
        f_input (Tensor): Input for forward computation
        b_grad (Tensor): Gradient for backward computation
        is_last_layer_in_bwd (bool):
            Whether the current layer is the last layer in the backward pass.
    Returns:
        Functions or values for next iteration's computation
    """
    if b_layer is not None:
        b_grad = b_layer.mtp_post_process.backward(b_grad)
        b_grad = b_layer.moe_combine.backward(b_grad)
    if f_layer is not None:
        with f_layer.get_low_precision_context():
            f_input = f_layer.pre_dispatch_computation.forward(f_input)
    if b_layer is not None:
        b_grad = b_layer.mlp.backward(b_grad)
    if f_layer is not None:
        with f_layer.get_low_precision_context():
            f_input = f_layer.moe_dispatch.forward(f_input)
    if b_layer is not None:
        b_layer.mlp.backward_dw()
        b_grad = b_layer.moe_dispatch.backward(b_grad)
    if b_layer is not None and b_layer.config.ep_overlap_early_attn_memory_release:
        b_grad = b_layer.pre_dispatch_computation.backward(b_grad)
    if f_layer is not None:
        with f_layer.get_low_precision_context():
            f_input = f_layer.mlp.forward(f_input)
    if f_layer is not None:
        with f_layer.get_low_precision_context():
            f_input = f_layer.moe_combine.forward(f_input)
    if b_layer is not None and not b_layer.config.ep_overlap_early_attn_memory_release:
        b_grad = b_layer.pre_dispatch_computation.backward(b_grad)
    if f_layer is not None:
        with f_layer.get_low_precision_context():... 9 more lines
```

> **Watch:** Log TFLOP/s per GPU (`--log-throughput`) before and after turning the overlap on, and keep it only if the step gets faster. Then look at a trace to see which all-to-alls are overlapped with compute.

> **Recommendation:** Use it when the all-to-all is exposed and memory allows: add `--overlap-moe-expert-parallel-comm --delay-wgrad-compute`, the pair Megatron's MoE guide recommends ([`README.md#L434`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/README.md?plain=1#L434)), instead of `--moe-shared-expert-overlap`. `--delay-wgrad-compute` runs only with the overlap on and with Transformer Engine layers ([`transformer_config.py#L3631-L3635`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L3631-L3635), [`arguments.py#L1956-L1958`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/arguments.py#L1956-L1958)). With pipeline parallelism, the overlap also needs virtual pipeline stages ([`transformer_config.py#L3565-L3599`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L3565-L3599)).

The overlap wins back time but costs memory. How can you keep a run's memory in check without giving that time away again?

##### Memory

An MoE changes memory use in two ways, through its weights and through its activations. Its weights hold every expert, although each token uses only k of them, and expert parallelism spreads those experts so that each GPU keeps only its own. Its activations, the intermediate results a layer keeps for the backward pass, grow with top-k. The dispatcher copies each token's hidden state once per selected expert ([`token_dispatcher.py#L559`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/token_dispatcher.py#L559)), and every copy keeps its own expert activations, so a GPU whose experts receive more tokens also holds more of them.

The usual answer is activation recomputation, which discards activations after the forward pass and recreates them when the backward pass needs them. The [Ultra-Scale Playbook](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=activation_recomputation) covers its two classic forms, full recompute of every layer and selective recompute of attention. Full recompute runs each layer's forward twice, which at micro-batch 2 cost us 24% of throughput, and the overlap from [3.7 Overlap](#s-3-7-overlap) needs it turned off ([`transformer_config.py#L3579-L3581`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L3579-L3581)).

A finer approach starts from what each module of a layer saves for its backward. Some of those tensors are cheap to recreate, such as the outputs of the normalizations and of the experts' activation function, which take a few elementwise operations. Others are large and costly to recompute: the query, key and value that enter attention, and the dispatched tokens that enter the experts' first matrix multiply, k copies of each token. Megatron treats the two kinds differently<sup>210</sup>, and the next figure marks which saved tensor each of its options acts on.

![offload-recompute-map](https://huggingface-moe-blogpost.hf.space/viz/posters/offload-recompute-map.webp)

*Figure caption:* Figure 3.7.6

The blue labels are recomputation options. Megatron's guide recomputes the norms and the expert activation (`--recompute-granularity selective --recompute-modules layernorm moe_act`): it discards their cheap outputs and recreates them just before the backward that reads them ([`random.py#L1042-L1064`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/tensor_parallel/random.py#L1042-L1064)). The outlined labels belong to fine-grained activation offloading, and the guide offloads attention's inputs and output and the experts' first input (`--fine-grained-activation-offloading --offload-modules core_attn attn_proj expert_fc1`).

Offloading copies the inputs of those large modules to pinned CPU memory on a separate CUDA stream while later modules compute ([`fine_grained_activation_offload.py#L1262-L1269`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/pipeline_parallel/fine_grained_activation_offload.py#L1262-L1269)). Each time the backward finishes an offloaded module, it starts copying back, on a second stream, the tensors of the next one, so they are on the GPU before they are needed ([`#L1332-L1342`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/pipeline_parallel/fine_grained_activation_offload.py#L1332-L1342)). Recomputation pays in compute, while offloading pays in bandwidth between host and GPU, which these copies hide behind compute. The figure below runs three layers through a forward and a backward pass with every saved input kept, with full recompute, and with that split, and tracks the saved inputs each setting holds on the GPU.

![offload-recompute](https://huggingface-moe-blogpost.hf.space/viz/posters/offload-recompute.webp)

*Figure caption:* Figure 3.7.7

With only three layers, one micro-batch and illustrative durations, full recompute reaches the lowest peak but adds a second forward pass, while the fine-grained split holds more and adds only a few small recomputes, because its copies run under compute. The last layer keeps its large inputs on the GPU, since its backward starts as soon as its forward ends and a reload would stall it ([`fine_grained_activation_offload.py#L630-L637`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/pipeline_parallel/fine_grained_activation_offload.py#L630-L637)). Slow the host link in the simulation and the copies to the CPU finish late, so the peak rises; slow it further and the backward waits for its reloads.

*Collapsible:* Megatron source

*Collapsible:* [`experts.py#L319-L322`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/experts.py#L319-L322) (moe_act needs selective)

```
self.activation_recompute = (
    self.config.recompute_granularity == 'selective'
    and "moe_act" in self.config.recompute_modules
)
```

*Collapsible:* [`experts.py#L1130-L1141`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/experts.py#L1130-L1141) (activation recomputed, output discarded)

```
if self.activation_recompute:
    self.activation_checkpoint = tensor_parallel.CheckpointWithoutOutput()
    with moe_act_manager as fc1_output:
        bias_act_output = self.activation_checkpoint.checkpoint(
            bias_act_func, fc1_output, bias_parallel, permuted_probs
        )
else:
    with moe_act_manager as fc1_output:
        bias_act_output = bias_act_func(fc1_output, bias_parallel, permuted_probs)
output, output_bias = apply_module(self.linear_fc2)(bias_act_output, tokens_per_expert)
if self.activation_recompute:
    self.activation_checkpoint.discard_output_and_register_recompute(output)
```

*Collapsible:* [`fine_grained_activation_offload.py#L1262-L1269`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/pipeline_parallel/fine_grained_activation_offload.py#L1262-L1269) (offload on the D2H stream after a module's forward)

```
def on_group_commit_forward(self, name, forced_released_tensors):
    """Called at the end of a layer group's forward pass to trigger offloading."""
    if not self.do_offload:
        return
    debug_rank(f"--on_group_commit_forward {name}")
    # Wait for compute to finish before starting offload
    self.d2h_stream.wait_stream(torch.cuda.current_stream())
    self.bulk_offload(name, forced_released_tensors)
```

*Collapsible:* [`fine_grained_activation_offload.py#L1332-L1341`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/pipeline_parallel/fine_grained_activation_offload.py#L1332-L1341) (reload issued at the start of a group's backward)

```
def on_group_start_backward(self):
    """
    Called at the start of a layer group's backward pass.
    Triggers reloading of tensors from CPU.
    """
    if not self.do_offload:
        return
    debug_rank(f"--on_group_start_backward {self}")
    # Wait for compute to finish before starting reload
    self.h2d_stream.wait_stream(torch.cuda.current_stream())
```

*Collapsible:* [`fine_grained_activation_offload.py#L630-L639`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/pipeline_parallel/fine_grained_activation_offload.py#L630-L639) (the last group of each name stays on the GPU)

```
# Mark the last group with the same name as not offloadable to make sure
# the reloading won't block the main stream.
for name, group in last_group_with_same_name.items():
    if self._offload_margin > 0:
        group.offload = False
        self._offload_margin -= 1
        debug_rank(f"setting offload to false for group {name} at chunk index {chunk_idx}")
    else:
        break
assert self._offload_margin == 0, "Offload margin is not 0"
```

*Collapsible:* [`transformer_config.py#L2601-L2660`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L2601-L2660) (offload validation: attn_proj needs core_attn, no offload inside a recomputed `moe`, not with `cpu_offloading`)

```
if self.fine_grained_activation_offloading:
    assert (
        not self.cpu_offloading
    ), "fine_grained_activation_offloading cannot be enabled with cpu_offloading."
    assert self.offload_modules is not None and len(self.offload_modules) > 0
    allowed_modules = {
        "core_attn",
        "attn_proj",
        "expert_fc1",
        "fused_group_mlp",
        "moe_act",
        "attn_norm",
        "mlp_norm",
        "qkv_linear",
        "gdp_qkv",
        "shortcut_post_norm",
    }
    invalid_modules = set(self.offload_modules) - allowed_modules
    assert not invalid_modules, (
        f'Invalid choices for offload_modules: {invalid_modules}. '
        f'Allowed modules are: {allowed_modules}'
    )
    if "attn_proj" in self.offload_modules and "core_attn" not in self.offload_modules:
        raise ValueError(
            "attn_proj cannot be set to offload_modules alone without core_attn "
            "because the input of attn_proj is the output of core_attn, "
            "which is needed in core_attn.backward()."
        )
    if (
        "gdp_qkv" in self.offload_modules
        and self.recompute_granularity == "selective"
        and "gdp_in_proj" in self.recompute_modules
    ):
        raise ValueError(
            "gdp_qkv cannot be set in offload_modules together with gdp_in_proj in "
            "recompute_modules, because gdp_in_proj discards the input of the causal "
            "conv and rematerializes it at the start of the mixer backward, leaving "
            "nothing for the gdp_qkv offload group to keep on the host."
        )
    if self.recompute_granularity == "selective" and "moe" in self.recompute_modules:
        offload_inside_moe = {"moe_act", "expert_fc1", "fused_group_mlp"} & set(
            self.offload_modules
        )
        assert not offload_inside_moe, (
            f"Cannot offload {offload_inside_moe} while recomputing the entire MoE layer. "
            f"'moe' in recompute_modules wraps the full MoE forward in a checkpoint, "
            f"so offloading activations inside it is redundant and will cause errors. "
            f"Either remove 'moe' from --recompute-modules or remove "
            f"{offload_inside_moe} from --offload-modules."
        )
    assert (
        self.min_offloaded_tensor_size >= 0
    ), "min_offloaded_tensor_size must be non-negative."
    assert (
        self.activation_offload_fraction >= 0 and self.activation_offload_fraction <= 1
    ), "activation_offload_fraction must be in range [0, 1]."
    assert (
        self.delta_offload_bytes_across_pp_ranks >= 0
    ), "delta_offload_bytes_across_pp_ranks must be non-negative."
```

*Collapsible:* [`experts.py#L860-L876`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/experts.py#L860-L876) (paged stash, fused path only)

```
if self.config.moe_paged_stash:
    permuted_local_hidden_states = paged_stash_group_start(permuted_local_hidden_states)
    max_num_tokens = permuted_local_hidden_states.shape[0]
    # Average/expected tokens is a pre-padding estimate used by paged stashing heuristics.
    # moe_expert_rank_capacity_factor is required when moe_paged_stash is enabled.
    cap_factor = self.config.moe_expert_rank_capacity_factor
    avg_num_tokens = (
        int(max_num_tokens // cap_factor)
        if cap_factor is not None and cap_factor > 0
        else None
    )
    stash_context = get_paged_stash_context(
        name="grouped_mlp",
        max_num_tokens=max_num_tokens,
        num_tokens_tensor=tokens_per_expert.sum(),
        avg_num_tokens=avg_num_tokens,
    )
```

NVIDIA measured the trade when it added the feature. On H100s, a 14-layer model with DeepSeek-V3's layer shapes, offloading its normalization inputs and both expert inputs, reserved 18% less memory at its peak and lost 2% of throughput<sup>211</sup>.

Offloading saves memory only while its copies stay hidden, and three settings decide how much it moves. `--activation-offload-fraction` offloads only a first share of the eligible groups in forward order, and `--min-offloaded-tensor-size` skips small tensors, under a million elements by default. A later pipeline stage holds fewer micro-batches in flight and needs less memory, so `--delta-offload-bytes-across-pp-ranks` lets each stage offload less than the one before it.

Recomputation and offloading shrink the activations each layer keeps. A layer can also reserve far more memory than its activations need, and that happens once you capture the step in CUDA graphs, which replay a recorded sequence of kernels without the CPU and so need every buffer's size fixed in advance. In a dropless MoE the number of tokens a rank receives changes from step to step, so each layer has to reserve its expert buffers for the largest load you allow: with `--moe-expert-rank-capacity-factor` and the HybridEP or NCCL EP backend, that is the factor times a perfectly balanced load. Every layer holds its reservation until its backward runs, yet [NVIDIA's Megatron Core MoE report](https://arxiv.org/html/2603.07685v2#S4.SS3.SSS7.Px3) notes that the activations a layer actually keeps for its backward are often more than ten times smaller<sup>212</sup>.

Megatron's experimental paged stash, `--moe-paged-stash`, separates the space a layer computes in from the space it stores. All layers compute in one shared buffer of the reserved size, and after each layer's forward a separate stream copies only its real tokens into small fixed-size pages, much as offloading copies tensors to the CPU. It needs `--use-transformer-engine-op-fuser` and FP8 or NVFP4 experts, and since it already holds the expert activations, Megatron refuses to combine it with offloading `expert_fc1` or `moe_act`<sup>212</sup>.

> **Watch:** Compare peak memory and step time before and after each change, since a run short of memory fails with an out-of-memory error on its busiest rank, and offload copies that outlast compute show up as a longer backward. The peak memory to watch is therefore the busiest rank's. Megatron prints the peak of data-parallel rank 0 ([`common_utils.py#L407-L427`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/utils/common_utils.py#L407-L427)) and sends the last rank's peak to [Trackio](https://huggingface.co/docs/trackio) through the launcher from [2.4](#s-2-4). To find the busiest rank, take the maximum of `torch.cuda.max_memory_allocated()` across ranks at each log interval, or record per-rank `--record-memory-history` snapshots.

> **Recommendation:** Use it when the overlap does not fit in memory: recompute the cheap modules (`--recompute-granularity selective --recompute-modules layernorm moe_act`) and offload the large inputs (`--fine-grained-activation-offloading --offload-modules core_attn attn_proj expert_fc1`) instead of recomputing every layer, which blocks the overlap. If step time grows, lower `--activation-offload-fraction`. Recomputing `layernorm` or `moe_act` does not run with FP8's delayed recipe ([`transformer_config.py#L2422-L2433`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L2422-L2433)), and with the `ncclep` backend the overlap does not run with `expert_fc1` offloading ([`#L3606-L3618`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L3606-L3618)).

So far you have tuned the system around the router's choices without touching them. What if the router took the network into account, at a price paid in training?

##### Group-limited routing

A token's top-k experts can sit anywhere in the expert-parallel group. Once that group spans several nodes, one token may need experts on many of them, and its copies cross the slower network between nodes, both when the token is dispatched and when its outputs are combined. Plain top-k routing ignores where the experts live, so nothing keeps a token's experts on few nodes.

DeepSeek-V3 adds the missing constraint with group-limited routing, which restricts where a token may look before it picks, "to limit communication costs during training". Its experts sit on 8 nodes, and for every token it scores each node by summing the token's top-2 expert scores there, including the balancing bias of [3.3](#s-3-3). It keeps the best 4 nodes and then takes the top-k among the experts on them, so a token reaches at most 4 nodes<sup>42</sup>. On devices instead of nodes, the figure below draws the same rule next to standard top-k and MoGE. MoGE (Mixture of Grouped Experts), the routing behind Huawei's Pangu Pro MoE, splits the experts into one equal group per device and takes the same number of experts from each group<sup>213</sup>. Intern-S1-Pro, trained with expert parallelism over 8 GPUs, takes one expert from each of 8 groups in the same way<sup>214</sup>.

![device-groups](https://huggingface-moe-blogpost.hf.space/viz/posters/device-groups.webp)

*Figure caption:* Figure 3.7.8

Compared device by device, group-limited routing caps how many devices each token reaches, while MoGE loads every device evenly and sends each token to all of them.

*Collapsible:* Megatron source

*Collapsible:* [`moe_utils.py#L713-L718`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L713-L718) (rank the groups, keep the best ones)

```
group_scores = (
    scores.view(num_tokens, num_groups, -1).topk(topk // group_topk, dim=-1)[0].sum(dim=-1)
)
group_idx = torch.topk(group_scores, k=group_topk, dim=-1, sorted=False)[1]
group_mask = torch.zeros_like(group_scores)
group_mask.scatter_(1, group_idx, 1)
```

*Collapsible:* [`moe_utils.py#L721-L728`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L721-L728) (top-k inside kept groups)

```
score_mask = (
    group_mask.unsqueeze(-1)
    .expand(num_tokens, num_groups, num_experts // num_groups)
    .reshape(num_tokens, -1)
)
masked_scores = scores.masked_fill(~score_mask.bool(), float('-inf'))
probs, top_indices = torch.topk(masked_scores, k=topk, dim=-1)
```

What the cap saves in traffic depends on the dispatcher. Megatron's `alltoall` dispatcher sends one copy of the token per expert, while the `flex` dispatcher with [DeepEP](https://github.com/deepseek-ai/DeepEP), whose kernels follow DeepSeek-V3's group-limited routing, sends one copy per node and forwards it inside the node over NVLink<sup>215,216</sup>. For a layer of our 7B-A1B model, 64 experts with top-8 and a 2,048-wide hidden state in bf16, spread over 2 to 8 nodes, the following figure counts what crosses the network with and without the cap, under both dispatchers.

![group-limited-bytes](https://huggingface-moe-blogpost.hf.space/viz/posters/group-limited-bytes.webp)

*Figure caption:* Figure 3.7.9

With `alltoall`, the cap only moves a token's copies onto fewer nodes, since every selected expert outside the token's own node still gets its own copy; the figure's router scores experts at random, ignoring which node the token sits on, and then as many bytes cross the network on average as without the cap. With DeepEP, each node a token reaches costs one copy, so capping the nodes caps the bytes. Reaching fewer nodes also leaves each token fewer experts to choose from, a cost paid in quality rather than in time, though a small one: when Xue et al. trained a 13B model with the group limit, its loss came out only slightly higher<sup>217</sup>.

Recent MoEs tend to drop the cap. DeepSeek, whose V3 used it, dropped it in DeepSeek-V4<sup>27</sup>, and GLM, Kimi, Nemotron, MiMo and Hy4 also let each token reach any expert. InclusionAI's Ling and Ring models still keep it in the same form as DeepSeek-V3, with 8 groups of which each token keeps 4, and SK Telecom's A.X-K2 keeps a looser version of it.

> **Watch:** When tokens fan out across many nodes the step gets slow, so watch two numbers. The first is nodes reached per token, computed offline from the routing trace and the map of which rank holds which expert ([A.1](#s-a-1)). The second is tokens received per EP rank, summed from the token counts that `--save-tokens-per-expert-interval` writes ([A.1](#s-a-1)).

> **Recommendation:** Try the recommendations above first, since they leave training unchanged, and turn to the cap only if the all-to-all across nodes still takes a large share of the step: the cap changes which experts a token can pick, and so what the model learns. It helps only when expert parallelism spans several nodes and the dispatcher sends a token once per node, as the `flex` dispatcher with DeepEP does. Then set `--moe-router-num-groups` to the number of nodes and `--moe-router-group-topk` to how many of them a token may reach, and pair it with a balancer other than `quantile_balancing`, which does not run with the cap. Otherwise leave it off: on one node it saves no traffic, and with `alltoall` it saves none on average.

The node cap limits where a token's copies go, but an expert the router favors still takes every token sent to it, and the rank that holds it finishes last. Should you turn that expert's extra tokens away, or copy the expert onto a quieter rank, and what does each choice cost?

##### Capacity and replicas

The rank that holds a hot expert finishes its share of the step last, and the other ranks wait for it at the next synchronization point<sup>208</sup>. By default, Megatron accepts that wait and keeps every token: with `--moe-expert-capacity-factor` unset, routing is dropless ([`transformer_config.py#L1009-L1011`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L1009-L1011)), and an expert takes however many tokens the router sends it.

A capacity factor caps that number. Each expert keeps its highest-probability tokens up to its capacity ([`transformer_config.py#L1024-L1028`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L1024-L1028)), and the tokens past it skip the expert. That buys some speed, since no expert can hold up the step with more tokens than its capacity<sup>218</sup>, and it caps memory too, since no expert ever holds activations for more tokens than its capacity<sup>219</sup>. For static shapes, add `--moe-pad-expert-input-to-capacity` as well.

The memory a capacity factor frees can also buy a better parallel layout. Vavre et al. at NVIDIA upcycled Llama 3-8B into an MoE with 8 experts and top-2 routing, and on 128 GPUs capacity factor 1 ran without [tensor parallelism](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=tensor_parallelism) at 463 TFLOP/s per GPU, against 392 for dropless training with a tensor-parallel size of 2. The authors put the gain down to the smaller memory footprint, which let them use less model parallelism<sup>220</sup>.

The other answer keeps every token and copies the hot expert instead. Three ways to handle a hot expert appear in the figure below: dropless routing, a capacity factor, and a replica of the hot expert placed the way ECHO places it, a method from the Megatron Core team's report that copies hot experts during training<sup>208</sup>.

![capacity-and-redundancy](https://huggingface-moe-blogpost.hf.space/viz/posters/capacity-and-redundancy.webp)

*Figure caption:* Figure 3.7.10

On one skewed toy batch of 8 experts over 4 ranks, the capacity factor drops the selections that overflow an expert, mostly the hot expert's, and drops them in arrival order, where Megatron's default would keep the highest-probability ones. Each dropped selection skips its expert, so the drawn step gets shorter and the model's output changes. A replica placed on the idlest rank brings the toy's busiest rank closer to the mean with nothing dropped.

*Collapsible:* Megatron source

*Collapsible:* [`router.py#L1029-L1038`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L1029-L1038) (drop after top-k)

```
# Apply token dropping to probs and routing_map.
if self.config.moe_expert_capacity_factor is not None:
    probs, routing_map = apply_router_token_dropping(
        probs,
        routing_map,
        router_topk=self.topk,
        capacity_factor=self.config.moe_expert_capacity_factor,
        drop_policy=self.config.moe_token_drop_policy,
        pad_to_capacity=self.config.moe_pad_expert_input_to_capacity,
    )
```

*Collapsible:* [`moe_utils.py#L1079-L1112`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L1079-L1112) (capacity per expert, keep highest probabilities)

```
# Calculate expert capacity
expert_capacity = get_capacity(
    num_tokens=num_tokens * router_topk,
    num_experts=num_experts,
    capacity_factor=capacity_factor,
)
# Create capacity mask based on drop policy
if expert_capacity > num_tokens:
    # No need to drop tokens if capacity exceeds the number of tokens
    capacity_mask = torch.ones_like(routing_probs).bool()
else:
    if drop_policy == "probs":
        _, capacity_indices = torch.topk(routing_probs, k=expert_capacity, dim=0, sorted=False)
        capacity_mask = torch.zeros_like(routing_probs).scatter(0, capacity_indices, 1).bool()
    elif drop_policy == "position":
        _, capacity_indices = torch.topk(
            routing_map.int(), k=expert_capacity, dim=0, sorted=False
        )
        capacity_mask = torch.zeros_like(routing_probs).scatter(0, capacity_indices, 1).bool()
    else:
        raise ValueError(f"Invalid drop_policy: {drop_policy}")
# Apply capacity constraints
if pad_to_capacity:
    final_map = capacity_mask
    final_probs = routing_probs * final_map
else:
    # Get exceed mask and maskout exceeded probs and indices
    final_map = torch.logical_and(routing_map, capacity_mask)
    final_probs = routing_probs * final_map
return final_probs, final_map
```

Real runs drop less than the toy: at a capacity factor of 1.5, Huawei's Pangu team saw about 6% of tokens dropped in a 20B MoE and about 8% in their 718B<sup>218</sup>. Replicas can balance the ranks almost exactly. Wei et al.'s UltraEP, which re-plans replicas for every micro-batch and layer, took the busiest rank of three training runs, DeepSeek-V3, Qwen3-235B and GLM-4.5-Air, from 1.30 to 2.86 times the mean load in plain Megatron-LM down to 1.01 to 1.03<sup>221</sup>.

A copy costs more in training than in serving. Each one needs the expert's weights sent to its rank in the forward pass and its gradients reduced back to the original in the backward pass, so ECHO's planner makes as few copies as it can: it counts each expert's tokens above the mean load per rank, finds the spare room on the quieter ranks, and packs the first into the second, then discards the copies once they have computed. Balanced ranks pay back twice, in less waiting and in smaller buffers, since CUDA graphs size their static buffers for the worst case, the same worst-case buffers the paged stash in [3.7 Memory](#s-3-7-memory) works around<sup>222</sup>.

Serving has the same problem without the gradients, so its copies stay in place far longer than ECHO's, which are planned anew in every forward pass. DeepSeek-V3 re-chooses its redundant experts from the load of its online service at an interval of about 10 minutes<sup>223</sup>. DeepInfer, the engine DeepSeek serves V4.1-Flash with, gives every GPU spare slots for copies of the busiest experts, counts each expert's load over a recent window, and re-places the copies every 1,000 steps in prefill and every 10,000 in decode, and with it the slowest GPU stays within 1.09 times the mean, as quoted in 3.3<sup>71</sup>.

Does dropping cost quality? Published comparisons say it costs some loss. Huawei's Pangu team trained a 20B MoE with a capacity factor of 1.5 and dropless, and the dropless run kept a lower loss throughout, by a gap that grew with the number of experts<sup>218</sup>. Gale et al. found the same when they built MegaBlocks: the loss was lowest when no token was dropped<sup>224</sup>.

A downstream benchmark can hide that gap: the upcycled Llama 3 MoE of Vavre et al. scored within a point on MMLU at every capacity factor they tried and with dropless routing<sup>225</sup>. Where the dropped tokens fall matters too. Meta's MobileMoE pretrained with a capacity factor and switched to dropless routing for fine-tuning, where dropping would cut tokens out of instruction-response pairs<sup>226</sup>.

A model trained with a cap need not be served with one. When Zoph et al. evaluated their ST-MoE models at a higher capacity factor than the one they were trained with, every model in their comparison scored better<sup>227</sup>. DeepSeek-V2 was built for that switch: it dropped tokens on each device during training but never from about 10% of its training sequences, so that at inference it could choose whether to drop tokens at all and still match how it was trained<sup>228</sup>.

> **Watch:** With a capacity factor on, tokens are dropped silently, so watch how often they are dropped alongside the validation loss. The routing trace that `--moe-routing-trace-path` writes skips every record where a token was dropped ([`router_trace.py#L353-L360`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router_trace.py#L353-L360)). To count the drops, compute the share of dropped token-expert assignments per layer with a forward hook on the router: `1 - kept / (tokens * topk)`, where `kept` counts the assignments left in the routing map.

> **Recommendation:** Keep dropless as the default. When one hot expert holds the step back and the quieter ranks have memory to spare, a replica of that expert would balance the ranks without touching the loss, although ECHO's replication is still an open pull request<sup>208</sup>. Use a capacity factor when memory is short and you can accept a slightly higher loss; static shapes also need `--moe-pad-expert-input-to-capacity`. Go back to dropless for fine-tuning, where dropped tokens fall inside instruction-response pairs.

Whether you drop tokens or keep them all, every token an expert keeps runs through its GEMMs, which so far have run in bf16. Could a lower precision such as FP8 make that work cheaper, and the activations it saves smaller, without hurting the loss?

##### Precision

Most of an MoE layer's computation sits in its matrix multiplications, and much of its activation memory in the inputs those multiplications save for the backward pass. FP8 halves the bytes of both against bf16, and its Tensor Core operations run faster on Hopper and Blackwell GPUs<sup>229</sup>. How much of that reaches the step depends on how much of the step the multiplications take and on what quantizing their tensors costs, and for large MoE training the Megatron Core team reports about 10 to 25% end to end<sup>229</sup>.

Not every operation can take the lower precision. The figure below shows where FP8 runs in one layer, forward and backward, following the split DeepSeek-V3 trained with: each linear layer runs its forward multiplication and both of its backward ones in FP8, while the embedding, the output head, the norms, the attention core and the router keep BF16 or FP32<sup>230</sup>.

![fp8-layer](https://huggingface-moe-blogpost.hf.space/viz/posters/fp8-layer.webp)

*Figure caption:* Figure 3.7.11

The memory saving comes from the backward pass. The weight-gradient multiplication reads the input the forward pass saved, so keeping that input in FP8 halves it, which for DeepSeek-V3 comes to about 16 GB of activations per GPU<sup>231</sup>. The master weights, the weight gradients and the optimizer states stay in higher precision<sup>230</sup>.

The router is the part to protect. Its scores pick each token's experts, so quantization noise there can change the selection and destabilize training, which is why the Megatron Core report keeps it in FP32<sup>232</sup>. In Megatron the router is not a [Transformer Engine](https://github.com/NVIDIA/TransformerEngine) layer, so FP8 never reaches it, and `--moe-router-dtype fp32` sets the precision of its math ([`router.py#L125-L130`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L125-L130), [3.1 Precision](#s-3-1-precision)). The quantized grouped GEMM needs each expert's token count padded to an aligned size, which `--moe-router-padding-for-quantization` gives it ([`transformer_config.py#L851-L854`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L851-L854)).

*Collapsible:* Megatron source

*Collapsible:* [`fp8_utils.py#L779-L829`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/fp8_utils.py#L779-L829) (format and recipe to TE)

```
if config.fp8 == "e4m3":
    fp8_format = transformer_engine.common.recipe.Format.E4M3
elif config.fp8 == "hybrid":
    fp8_format = transformer_engine.common.recipe.Format.HYBRID
else:
    raise ValueError("E4M3 and HYBRID are the only supported FP8 formats.")
# Select fp8 recipe (TE version >= 2.1.0).
fp8_recipe = None
if is_te_min_version("2.1.0"):
    if config.fp8_recipe == Fp8Recipe.delayed:
        fp8_recipe = TEDelayedScaling(
            config=config,
            fp8_format=fp8_format,
            override_linear_precision=(False, False, not config.fp8_wgrad),
        )
    elif config.fp8_recipe == Fp8Recipe.tensorwise and is_te_min_version("2.2.0.dev0"):
        fp8_recipe = transformer_engine.common.recipe.Float8CurrentScaling(
            fp8_format=fp8_format, fp8_dpa=config.fp8_dot_product_attention
        )
    elif config.fp8_recipe == Fp8Recipe.blockwise and is_te_min_version("2.3.0.dev0"):
        fp8_recipe = transformer_engine.common.recipe.Float8BlockScaling(
            fp8_format=fp8_format
        )
    elif config.fp8_recipe == Fp8Recipe.mxfp8:
        fp8_recipe = transformer_engine.common.recipe.MXFP8BlockScaling(
            fp8_format=fp8_format, fp8_dpa=config.fp8_dot_product_attention
        )
    elif config.fp8_recipe == Fp8Recipe.custom:
        assert config.fp8_quantizer_factory is not None
        fp8_recipe = _get_custom_recipe(config.fp8_quantizer_factory)
    else:
        raise ValueError(
            "Float8CurrentScaling, MXFP8BlockScaling, Float8BlockwiseScaling and "
            "DelayedScaling are the only supported FP8 recipes. Please also make sure "
            "you are using a compatible TE version."
        )
else:
    # Assert that the user is using delayed scaling.
    assert config.fp8_recipe == Fp8Recipe.delayed, (
        "Please make sure to use TransformerEngine version >= 2.2.0.dev0 for "
        "Float8CurrentScaling, >= 2.1.0 for MXFP8BlockScaling, and >= 2.3.0.dev0 for "
        "Float8BlockScaling."
    )
    fp8_recipe = TEDelayedScaling(
        config=config,
        fp8_format=fp8_format,
        override_linear_precision=(False, False, not config.fp8_wgrad),
    )
return fp8_recipe
```

*Collapsible:* [`token_dispatcher.py#L652-L657`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/token_dispatcher.py#L652-L657) (pad routing for quantization)

```
if self.config.moe_router_padding_for_quantization:
    pad_multiple = get_align_size_for_quantization(self.config)
    if is_experimental_enabled() and self.config.moe_permute_fusion:
        self.routing_map = fused_pad_routing_map(self.routing_map, pad_multiple)
    else:
        self.routing_map = pad_routing_map(self.routing_map, pad_multiple)
```

The recipe sets how finely the scales follow the data. With one scale per tensor, the largest outlier sets the range for every other value, so DeepSeek-V3 and Ling 2.0 scale activations and gradients per tile of 1×128 elements and weights per block of 128×128<sup>233,234</sup>. The Megatron Core report recommends this blockwise recipe on Hopper, and MXFP8, with one scale per 32 elements, on Blackwell<sup>235</sup>. You pick them with `--fp8-format` and `--fp8-recipe`, and the blockwise recipe needs Transformer Engine 2.3 or newer ([`fp8_utils.py#L799`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/fp8_utils.py#L799)).

FP8 can also cross the network. DeepSeek-V3 quantizes the tokens to FP8 before dispatch, since the experts' first layer reads them in FP8 anyway; "a similar strategy is applied to the activation gradient before MoE down-projections", while "both the forward and backward combine components" stay in BF16<sup>236</sup>. In Megatron, `--moe-dispatch-fwd-dtype mxfp8` and `--moe-combine-bwd-dtype mxfp8` send the dispatch payload and the gradient going back through combine in MXFP8. Both need the `ncclep` backend of the flex dispatcher ([`transformer_config.py#L2150-L2158`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L2150-L2158)), and MXFP8 itself needs Blackwell-class GPUs ([`#L656-L661`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L656-L661)).

Long runs report the loss holding. DeepSeek trained a 16B and a 230B MoE in FP8 for about a trillion tokens each, and both stayed within 0.25% relative error of their BF16 baselines<sup>237</sup>. Ling-1T held within the same bound, about 0.1% on average, over 900B tokens, while FP8 raised its MFU by about 15%<sup>234</sup>.

Four bits is the next step down, and the first large MoEs have been pretrained there. NVIDIA trained Nemotron 3 Super, 120B parameters with 12B active, on 25T tokens in NVFP4, running all three multiplications of most linear layers in it. The exceptions show where 4 bits are too few: the last 15% of the network, the attention projections, the embeddings and the multi-token prediction layers stay in BF16, and the Mamba output projection runs in MXFP8 because it underflowed in NVFP4. The recipe also scales weights in two-dimensional blocks, so the forward and backward passes see the same quantized weights, applies random Hadamard transforms to the inputs of the weight-gradient multiplication and rounds gradients stochastically<sup>238</sup>. Nemotron 3 Ultra, 550B with 55B active, followed on 20T tokens with the same recipe, and when NVIDIA branched BF16 runs off its checkpoints, the loss gap to them stayed below 0.4% on average<sup>239</sup>.

> *Margin note:* A 4-bit floating-point format with one FP8 scale per block of 16 elements and a second, per-tensor FP32 scale.

FP4 shrinks the saved inputs to a quarter of their BF16 size, against half for FP8<sup>231</sup>, and native FP4 multiplications need Blackwell-class GPUs<sup>240</sup>. Hopper has no 4-bit Tensor Core instructions, yet Zhang et al. at Zhejiang Lab stored the activations and the forward dispatch traffic of a 671B MoE in software-emulated MXFP4 while its multiplications stayed in FP8, and cut peak activation memory by 14.8% while matching the convergence of a strong FP8 baseline. The memory it freed let the run recompute less, and it ran 12.5% faster than the best FP8 setting that fit<sup>241</sup>.

> **Watch:** An FP8 run's loss should stay close to BF16's for the whole run, so compare it with a BF16 run of the same config as a relative difference. DeepSeek's 16B and 230B runs and Ling-1T all stayed under 0.25%, so a gap well past that, or one that keeps growing, points at the recipe. Under NVFP4, also count the weight-gradient elements that are exactly zero in the expert layers. In Nemotron 3 Super they grew to 7% of all parameters by the end of pretraining, as low-norm channels in some experts shrank toward zero, and in a smaller ablation on Nemotron 3 Nano, switching back to BF16 brought the count back to its baseline<sup>242</sup>.

> **Recommendation:** Use FP8 when the linear layers take most of the step, with the blockwise recipe on Hopper and MXFP8 on Blackwell, and keep the router, the norms and the attention core in higher precision. On a large MoE, expect about 10 to 25% more throughput and a loss within a fraction of a percent of BF16. On Blackwell, NVFP4 is the next step down, with the Nemotron 3 recipe keeping the last layers, the attention projections and the embeddings in BF16.

##### What to watch

| Part | Symptom | Signal to watch |
| --- | --- | --- |
| Profiling | `slow`: the step takes longer than it should. | Step time or TFLOP/s first. Then, from a trace, how much of the step the all-to-all leaves exposed. |
| Interconnect | `slow` on several nodes: when NCCL falls back to TCP sockets, our EP16 proxy ran about 25 times slower, 1.7 against 42.0 TFLOP/s. | With `NCCL_DEBUG=INFO`, check "Using network" for the intended transport: IB for InfiniBand or Libfabric for the OFI plugin on EFA; Socket indicates fallback. Then compare nccl-tests alltoall bus bandwidth inside and across nodes ([2.1](#s-2-1)), and TFLOP/s at node-local versus cross-node EP. |
| Overlap | `slow`: the all-to-all is not hidden behind compute. | TFLOP/s per GPU (`--log-throughput`) before and after. Use the exposed all-to-all share only to explain the change. |
| Memory | `OOM`: one rank runs out of memory. `slow`: recomputation, or offload reloads that outlast compute, add step time. | Compare step time and peak memory after each change. Use the busiest rank's peak: maximum `torch.cuda.max_memory_allocated()` across ranks or per-rank `--record-memory-history` snapshots. Longer backward can expose offload reloads that outlast compute. |
| Group-limited routing | `slow`: each token fans out across nodes. | How many nodes each token reaches (routing trace and the map of experts to ranks), and the tokens each EP rank receives (token counts), [A.1](#s-a-1). |
| Capacity and replicas | `learns badly`: tokens are dropped silently. `OOM`: one rank runs out of memory. | Share of dropped token-expert assignments per layer, `1 - kept / (tokens * topk)`, from a router forward hook, alongside validation loss. The routing trace skips records with drops. |
| Precision | `slow`: no speedup over bf16. `learns badly`: a higher loss than bf16. | Relative loss difference against a BF16 run of the same config across training; DeepSeek's 16B and 230B runs and Ling-1T stayed below 0.25%<sup>237,234</sup>. Under NVFP4, also count exactly zero expert weight-gradient elements: these reached 7% of all parameters in Nemotron 3 Super<sup>242</sup>. |

You now have every part of an MoE layer, from the router that picks the experts to the precision they compute in. Once training ends, which of those choices still matter when the model is served?

### 4. From training to serving

A model is trained once, but it is served for as long as anyone uses it. So far, this handbook has been about the first part: getting an MoE to train fast and well. This chapter is about the second.

Serving judges the model by different numbers. A training run is measured in step time and in loss; a serving system is measured in how quickly each request gets its answer and in how many GPUs it takes to answer them all. The model is the same in both, but the goals are not, so some choices that were right for training deserve a second look once the run is over.

An MoE has more to revisit than a dense model. Each token runs through only a few experts, yet every expert is usually kept in memory in case some token picks it, so the model is cheap in compute per token and expensive in memory. Once requests are decoded one token at a time, each expert also sees only a few tokens per step, which makes the number of GPUs the experts are spread over a serving decision of its own. Attention and the experts, which share each GPU in the layout used so far, make different demands on the hardware as well.

This chapter takes those differences one at a time. We start with k, the size of the expert set the router picks for a token. Next, we look at how much memory the experts take, how many GPUs to spread them over, and where attention and the experts should run. We end with RL post-training, where a serving engine writes the samples a trainer learns from, and the two can disagree on which experts each token went through.

The first of these changes is a single number you set at serving time. If you serve each token with a different number of experts than it was trained with, what happens to its output?

#### Serving a different k

Training fixes how many experts each token uses, but nothing stops you from serving fewer. Each routed expert you drop from a token's top k is compute saved, while every expert stays resident for the tokens that do pick it, so memory does not change<sup>243</sup>. The difficulty lies in the routing weights. A router that renormalizes ([3.1](#s-3-1)) divides the chosen experts' probabilities by their sum, so the scale of the expert branch's output, its gain, is set for the trained k. When you serve fewer experts, the survivors share that same total among themselves, and each one gets a larger weight than it had at the trained k. A smaller k therefore changes two things at once: which experts run, and how much each one contributes.

Chen and Yao separate those two effects with one integer. They keep the top k1 experts but divide their weights by the softmax mass of the top k2, chosen at serving with no training. Setting k2 = k1 is the usual renormalization over the survivors, which LExI, a method that picks a different k for each layer, also uses<sup>244</sup>, setting it to the number of experts removes renormalization, and setting it to the trained k anchors the gain to the value the model was trained with.

The figure below routes one simulated token through a softmax shaped like the router of Qwen3.6-35B-A3B, 256 routed experts trained at top-8, and serves it at smaller k, with one row per denominator. Follow the middle panel as k falls: over the survivors, each served expert weighs more than at top-8; over the trained top 8, it keeps its trained weight; over the top 16, it weighs less. The right panel gives the MMLU change measured for each row.

![serving-smaller-k](https://huggingface-moe-blogpost.hf.space/viz/posters/serving-smaller-k.webp)

*Figure caption:* Figure 4.1

That router is flat, its top 8 experts holding on average only 0.182 of the softmax mass over WikiText<sup>245</sup>, so the denominator moves the gain a long way. Against 81.65% MMLU at the trained top-8, top-4 renormalized over the four survivors scores 4.65 points lower, and divided by the top-8 mass 3.10 lower. Divided by the top-16 mass, it scores 0.35 points lower, a drop that is not significant (p = 0.66). With no renormalization at all, top-6 loses 27.45 points<sup>246</sup>. In return, top-4 halves the activated routed parameters per token, from 1.006B to 0.503B, a saving of 17% of all the parameters each token uses<sup>243</sup>.

How much the denominator matters depends on how flat the router is. On Gemma-4-26B-A4B, whose top 8 of 128 experts hold 0.302 of the mass, dropping renormalization at top-6 raised perplexity by 0.7%, against 356% on the Qwen model. Both results come from softmax routers<sup>247</sup>.

Serving more experts than the model trained with costs more compute per token, and the quality need not follow. In Gu et al.'s fine-tuning runs on OLMoE-1B-7B, which trains at top-8, serving top-16 moved the average over nine benchmarks from 41.35 to 41.09, inside the error bars they report. The extra experts form combinations the model never trained together, so in their runs a larger k did not help when it was changed only at serving<sup>248</sup>.

[Megatron](https://github.com/NVIDIA/Megatron-LM) serves whatever `--moe-router-topk` says, and the weights follow the router you trained. By default, a softmax router takes its softmax over the top-k logits, so a smaller k renormalizes over the survivors, Chen and Yao's k2 = k1. With `--moe-router-pre-softmax`, the weights come from the full softmax and are never renormalized. A sigmoid router divides by its top-k sum when k is above 1, and any router multiplies by `--moe-router-topk-scaling-factor` if set. In transformers' Qwen3-MoE, the served k is `num_experts_per_tok`, and the routing weights are divided by their top-k sum only if `norm_topk_prob` is set. Any other denominator needs a patch of a few lines in either router that keeps the top k1 experts and divides by the top-k2 mass.

*Collapsible:* Megatron source

*Collapsible:* [`moe_utils.py#L913-L947`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L913-L947) (top-k weights: softmax before or after top-k, sigmoid divided by its top-k sum, then scaled)

```
if score_function == "softmax":
    if use_pre_softmax:
        scores = torch.softmax(logits, dim=-1, dtype=torch.float32)
        if precomputed_indices is not None:
            top_indices = precomputed_indices
            probs = torch.gather(scores, dim=1, index=top_indices)
        else:
            probs, top_indices = compute_topk(scores, topk, num_groups, group_topk)
    else:
        if precomputed_indices is not None:
            top_indices = precomputed_indices
            scores = torch.gather(logits, dim=1, index=top_indices)
        else:
            scores, top_indices = compute_topk(logits, topk, num_groups, group_topk)
        probs = torch.softmax(scores, dim=-1, dtype=torch.float32)
elif score_function in ("sigmoid", "sqrtsoftplus"):
    if score_function == "sigmoid":
        scores = torch.sigmoid(logits.float())
    else:
        scores = torch.nn.functional.softplus(logits.float()).sqrt()
    if precomputed_indices is not None:
        top_indices = precomputed_indices
        scores = torch.gather(scores, dim=1, index=top_indices)
    elif expert_bias is not None:
        scores_for_routing = scores + expert_bias.float()
        _, top_indices = compute_topk(scores_for_routing, topk, num_groups, group_topk)
        scores = torch.gather(scores, dim=1, index=top_indices)
    else:
        scores, top_indices = compute_topk(scores, topk, num_groups, group_topk)
    probs = scores / (scores.sum(dim=-1, keepdim=True) + 1e-20) if topk > 1 else scores
else:
    raise ValueError(f"Invalid score_function: {score_function}")
if scaling_factor:
    probs = probs * scaling_factor
```

proposed: a patch of a few lines that keeps the top k1 experts and divides by the top-k2 mass, there or in transformers' router; then the served-k sweep below.

> **Watch:** Score each served k on a labeled task as well as on perplexity, because the two can disagree: at top-6 on the 35B model, perplexity was lowest with the trained top-8 mass as the denominator, while MMLU was highest with the top-16 mass<sup>249</sup>.

> **Recommendation:** Use it when you need less routed-expert compute per token and can keep every expert in memory: serve a smaller k, and divide the survivors' weights by a larger mass than their own. At top-4 on Qwen3.6-35B-A3B, dividing by the top-16 mass kept MMLU within 0.35 points of the trained model<sup>246</sup>. Check the denominator on your own model, since how much it matters depends on how flat your router is<sup>247</sup>.

Cutting k saves compute but leaves every expert in memory. When memory rather than compute is what limits your serving, how can you make the experts take up less of it?

#### Low-bit experts

Once training ends, the weights stop moving, and two numbers describe what they cost at serving: the bytes they take in memory and the bytes each decoded token reads. In an MoE the routed experts hold most of the parameters, so their precision sets most of the model's size, and storing only them in 4 bits, with the rest in a wider format, captures most of the saving.

Some frontier MoEs already ship this way. OpenAI post-trained gpt-oss with its MoE weights quantized to MXFP4, at 4.25 bits per parameter. Those weights hold more than 90% of the parameters, so the 120b model fits on one 80 GB GPU<sup>250</sup>. Moonshot quantized Kimi K3's routed experts to MXFP4 through SFT and RL and kept everything else in higher precision<sup>21</sup>. DeepSeek-V4 trains its MoE expert weights with MXFP4 quantization-aware training in post-training<sup>251</sup>, and the GLM team applies INT4 quantization-aware training in GLM-5's SFT stage<sup>252</sup>. In all four, the quantization happens after pretraining, so your pretraining config stays as it is.

> *Margin note:* Training with the weights rounded to the target format in the forward pass.

The figure below compares three ways to store gpt-oss-20b, one decoded token at a time: everything in bf16, only the routed experts in 4 bits, and every linear layer in 4 bits. Each bar is the model's size in memory, and its blue blocks are the weights one token reads. From the first row to the second, compare how much the model shrinks with how much a token's reads shrink, then see what attention in 4 bits adds in the third.

![low-bit-experts](https://huggingface-moe-blogpost.hf.space/viz/posters/low-bit-experts.webp)

*Figure caption:* Figure 4.2

Storing the experts in 4 bits shrinks gpt-oss-20b from 39.0 GiB to 12.8 GiB, three times smaller, but the weight bytes one decoded token reads fall only from 6.72 GiB to 3.45 GiB, about half. In batch-1 decoding, a token reads only 4 of the 32 experts in each layer but all of attention and the unembedding, so once the experts are small, those bf16 weights make up two thirds of the weights it reads. Putting attention in 4 bits as well cuts those reads by another quarter while freeing only 0.9 GiB of memory, because attention holds few of the parameters.

Released checkpoints take both scopes. ZAYA1-8B's MXFP4 release quantizes only the routed experts, and so do Kimi K2 Thinking and Qwen's GPTQ-Int4 builds of Qwen3.5, in int4 rather than MXFP4<sup>253</sup>. Qwen's GPTQ-Int4 build of Qwen3's 30B MoE and Tencent's of Hunyuan-A13B put attention in int4 as well, leaving only the router, embeddings and output head unquantized<sup>254</sup>.

Megatron exports through ModelOpt: `examples/post_training/modelopt/quantize.py` takes a ModelOpt config name in `--export-quant-cfg`, `FP8_DEFAULT_CFG` for an FP8 export, with `--weight-only` and `--sync-expert-weight-amax` among its options. To train in 4 bits, set `--fp4-format e2m1`, NVFP4 through [Transformer Engine](https://github.com/NVIDIA/TransformerEngine) on Blackwell, which needs Transformer Engine 2.7 or newer and does not combine with `--fp8-format`.

*Collapsible:* Megatron source

*Collapsible:* [`post_training/arguments.py#L56-L61`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/post_training/arguments.py#L56-L61) (`--export-quant-cfg`)

```
group.add_argument(
    "--export-quant-cfg",
    type=str,
    default=None,
    # TODO replace choices with mtq.config.choices after deprecating the shorter aliases
    help="Specify a quantization config from mtq.config.choices.",
```

*Collapsible:* [`quantize.py#L159-L176`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/examples/post_training/modelopt/quantize.py#L159-L176) (export options: `--weight-only`, `--sync-expert-weight-amax`)

```
group.add_argument("--weight-only", action="store_true", help="Disable input quantization.")
group.add_argument(
    "--recipe",
    type=str,
    default=None,
    help=(
        "PTQ recipe YAML file or name without suffix (e.g. "
        "'general/ptq/nvfp4_default-fp8_kv', "
        "'models/Nemotron-3-Super-120B-A12B/super-nvfp4'). "
        "When set, --export-quant-cfg / --export-kv-cache-quant are ignored; "
        "the recipe is authoritative for quant_cfg, algorithm, and KV cache config."
    ),
)
group.add_argument(
    "--sync-expert-weight-amax",
    action="store_true",
    help="Synchronize expert weight amax across experts.",
)
```

*Collapsible:* [`transformer_config.py#L735-L743`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L735-L743) (`--fp4-format`, NVFP4 through Transformer Engine)

```
fp4: Optional[Literal['e2m1']] = field(
    default=None, metadata={"argparse_meta": {"arg_names": ["--fp4-format"]}}
)
"""If set, enables the use of FP4 precision through Transformer Engine. Currently only 
supports 'nvfp4' which uses NVFP4BlockScaling recipe (requires TE >= 2.7.0.dev0)."""
fp4_recipe: Optional[Literal['nvfp4', 'custom']] = "nvfp4"
"""If set, enables the use of FP4 precision through Transformer Engine. Currently only
'nvfp4' is supported which uses NVFP4BlockScaling recipe for Blackwell+ architecture."""
```

*Collapsible:* [`arguments.py#L1060-L1070`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/arguments.py#L1060-L1070) (FP4 needs Transformer Engine 2.7, not with `--fp8-format`)

```
# FP4 and FP8 are mutually exclusive
if args.fp4 and args.fp8:
    raise ValueError("--fp4-format and --fp8-format cannot be used simultaneously. Please choose one.")
# FP4 param requires FP4 mode
if args.fp4_param_gather and not args.fp4:
    raise ValueError("--fp4-param-gather must be used together with --fp4-format.")
# FP4 requires TE >= 2.7.0.dev0
if args.fp4 and not is_te_min_version("2.7.0.dev0"):
    raise ValueError("--fp4-format requires Transformer Engine >= 2.7.0.dev0 for NVFP4BlockScaling support.")
```

proposed: our t56 chain, collapsed: PTQ export on one GPU at EP1, 24 iterations of QAT, then the per-expert distortion script.

> **Watch:** Plot each expert's quantization error against its token count, using the per-expert token counts from [3.0](#s-3-0), so an expert that suffers for being rarely routed stands out. Then compare the quantized export's loss with Megatron's on the same text.

> **Recommendation:** Use it when serving is bound by memory or by the bytes each token reads: quantize the routed experts to 4 bits in post-training, and keep everything else in higher precision as Kimi K3 does.

Storing the experts in fewer bits shrinks what each GPU holds, but it leaves open how many GPUs to spread them over. Once requests arrive one token at a time, should you spread them over as many GPUs as training did?

#### Expert parallelism at serving

Training picks an expert-parallel size for one kind of step: a large batch of tokens processed together. Serving runs two kinds. A prefill step processes prompts, and DeepSeek's engine lets one such step carry up to 32,768 tokens per GPU<sup>255</sup>. A decode step carries only the next token or few of each request in flight, so each expert sees few tokens per step. Putting the experts on more GPUs helps there: each GPU holds fewer experts and reads fewer weights per step, while the all-to-all gathers a larger batch for each expert<sup>256</sup>.

When DeepSeek serves DeepSeek-V4.1-Flash, it sizes the two phases in opposite directions. Prefill runs at EP2 to EP8, the smallest size whose GPUs have enough memory, and decode at EP64 to EP128, the largest the available GPUs allow. In both, attention is [data-parallel](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=data_parallelism) with one rank per EP rank, and neither phase uses tensor or [context parallelism](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=context_parallelism)<sup>256</sup>.

The figure below redraws DeepSeek's own comparison of the two settings in decode, one dot per number of requests per GPU. With 64 requests per GPU, EP64 holds 7 routed experts per GPU and decodes about 15,700 tokens per second per GPU at about 246 tokens per second per user, while EP8 holds 52 routed experts per GPU and reaches about 12,600 and 198, so both numbers are about 25% higher at EP64. With 256 requests per GPU, the two settings nearly meet, at about 26,300 and 24,900 tokens per second per GPU<sup>257</sup>.

![wide-ep-decode](https://huggingface-moe-blogpost.hf.space/viz/posters/wide-ep-decode.webp)

*Figure caption:* Figure 4.3

The width has a price. DeepSeek gives prefill and decode roughly equal numbers of GPUs, so with decode at EP64 or more, the smallest deployment worth running is 64 GPUs for prefill plus 64 for decode<sup>258</sup>. All the GPUs of one EP instance also form a single communication domain, so one failed GPU takes the whole instance down, and on restart DeepSeek re-sizes the EP group to the GPUs that are still healthy<sup>259</sup>.

Megatron serves with [expert parallelism](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=expert_parallelism) in its coordinator mode, the default; direct mode refuses an EP size above 1. Under expert parallelism, a step runs as a CUDA graph only when every EP rank is decoding: if any rank has a prefill in its batch, all ranks fall back to eager mode. In RL, `--rl-inference-expert-model-parallel-size` gives the rollout engine its own EP size, built as a separate inference model that the trainer's weights are refit into.

*Collapsible:* Megatron source

*Collapsible:* [`mcore-inference-user-guide.md#L277-L278`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/docs/mcore-inference-user-guide.md#L277-L278) (EP needs coordinator mode)

```
- *Required* for: HTTP serving (`serve`), expert parallelism (`EP > 1`),
  multimodal inputs, streaming, and the lifecycle controls
```

*Collapsible:* [`batch_dimensions_utils.py#L156-L161`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/inference/batch_dimensions_utils.py#L156-L161) (one prefill rank sends the EP group to eager)

```
"""Adjust CUDA graph batch dimensions for expert parallelism.
All-reduce-max the token count and non-decode flag across the EP group.
If any rank has a prefill (non-decode) step, all ranks fall back to eager
mode (return None) — the non-CG path handles variable token counts via
use_allgather_v. Otherwise return adjusted dims with the max token count.
```

*Collapsible:* [`rl_config.py#L140-L141`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/config/rl_config.py#L140-L141) (rollout EP size)

```
rl_inference_expert_model_parallel_size: int | None = None
"""Degree of expert model parallelism for inference for RL."""
```

*Collapsible:* [`training.py#L1965-L1993`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/training.py#L1965-L1993) (separate inference model with its own parallelism)

```
if args.perform_rl_step:
    # RL inference doesn't support CP; when training uses CP>1, always build a
    # separate CP=1 inference model (CP ranks become extra DP replicas, dp*=cp).
    force_cp1_inference_model = args.context_parallel_size > 1
    if (
        args.rl_inference_tensor_model_parallel_size is not None
        or args.rl_inference_pipeline_model_parallel_size is not None
        or args.rl_inference_expert_model_parallel_size is not None
        or args.rl_inference_expert_tensor_model_parallel_size is not None
        or force_cp1_inference_model
    ):
        from megatron.core.inference.shards import build_inference_pg_collection
        print_rank_0(
            "Building separate RL inference model with custom parallelism: "
            f"TP={args.rl_inference_tensor_model_parallel_size}, "
            f"PP={args.rl_inference_pipeline_model_parallel_size}, "
            f"CP={1 if force_cp1_inference_model else None}, "
            f"EP={args.rl_inference_expert_model_parallel_size}, "
            f"ExptTP={args.rl_inference_expert_tensor_model_parallel_size}"
        )
        inference_pg_collection = build_inference_pg_collection(
            args.world_size,
            tp_size=args.rl_inference_tensor_model_parallel_size,
            pp_size=args.rl_inference_pipeline_model_parallel_size,
            cp_size=1 if force_cp1_inference_model else None,
            ep_size=args.rl_inference_expert_model_parallel_size,
            expt_tp_size=args.rl_inference_expert_tensor_model_parallel_size,
            use_tp_pp_dp_mapping=args.use_tp_pp_dp_mapping,
```

*Collapsible:* [`rl_utils.py#L810-L822`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/rl/rl_utils.py#L810-L822) (weights refit into it)

```
# If we have separate training and inference models we to refit weights from the training model to the inference model.
has_separate_inference_model = inference_model is not None
if has_separate_inference_model:
    # If the separate inference model weights were prefetched to CPU while idle, bring them
    # back to GPU before refit/copy and before any CUDA-graph'd inference.
    with nvtx_range("rl/prefetch-weights-to-gpu", time=True):
        inf_core = unwrap_model(inference_model[0])
        _maybe_prefetch_separate_inference_model_weights(inf_core, to_cpu=False)
    swap_model_weights(
        model,
        inference_model,
        args.refit_method,
        execution_batch_bytes=args.refit_execution_batch_bytes,
```

> **Watch:** DeepSeek credits wide EP's gain in decode partly to "good EPLB support"<sup>256</sup>, its expert-parallel load balancer, so track the slowest EP rank's load over the mean, which DeepSeek reports as `moe_lb`. With redundant copies of hot experts, DeepSeek holds it at 1.090 in decode<sup>71</sup>.

> **Recommendation:** Use it when decode speed is what you need and you have the GPUs for a wide deployment: serve decode at the widest expert parallelism your GPUs allow and prefill at the narrowest that fits in memory, as DeepSeek does for V4.1-Flash, and give the wide decode group redundant experts so its slowest rank stays close to the mean<sup>256,71</sup>.

A wider expert group changes how much expert work each GPU does, but each GPU still runs attention and the experts side by side, even though the two make different demands on it. At inference time, is sharing GPUs still the right way for you to place them?

#### Attention-FFN disaggregation

In a colocated layout, each GPU in an expert-parallel group runs both halves of each layer, attention and experts, but during decoding the two halves need different resources. Attention holds few parameters but has to keep the key-value cache of every request in flight, while the experts hold most of the parameters and keep no per-request state<sup>260</sup>. Serving can therefore put attention and experts on separate GPUs, one pool each, and pass micro-batches back and forth so that each pool computes while the other one works on the previous micro-batch. MegaScale-Infer, which disaggregates attention and FFN modules within each layer this way, reports up to 1.90× the per-GPU throughput of earlier serving systems<sup>261</sup>.

> *Margin note:* Megatron's `megatron/core/inference/disaggregation` splits along a different line: it hands KV and SSM state from prefill engines to decode engines.

*Collapsible:* Megatron source

*Collapsible:* [`mcore-inference-user-guide.md#L130`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/docs/mcore-inference-user-guide.md#L130) (Megatron's disaggregation: prefill to decode, not attention to FFN)

```
| **Disaggregation** | KV and SSM state handoff between prefill and decode engines over NIXL or NCCL, with resharding across mismatched TP/PP layouts. Refer to [Disaggregated Prefill and Decode](#disaggregated-prefill-and-decode) for what is and is not turnkey today |
```

The figure below draws FastAFD's deployment of Qwen3-235B-A22B, 28 attention GPUs plus 4 expert GPUs, next to colocated expert parallelism over 4 GPUs<sup>262</sup>. On the left, compare what one GPU holds in each layout: an attention GPU without experts has room for more requests' caches, but the expert GPUs hold no request's cache, and the requests-per-GPU bars count both pools. On the right, follow a decode step to see how a second micro-batch keeps the attention pool busy while the first is away at the experts. The colocated row overlaps its all-to-all with two micro-batches as well, which vLLM offers as dual-batch overlap<sup>263</sup>.

![attention-ffn-disaggregation](https://huggingface-moe-blogpost.hf.space/viz/posters/attention-ffn-disaggregation.webp)

*Figure caption:* Figure 4.4

How much this buys depends on what you compare it with. As published, FastAFD's layout gives 1.41× the per-GPU throughput of colocated EP4. Qiu et al. at Meituan reconstructed that gain with an analytical model, then re-provisioned both layouts in that model for the same budget of 72 GPUs, and the ratio fell to 0.99×. Across all their modelled settings, homogeneous AFD raised fixed-budget throughput in only a minority of them<sup>262</sup>. Step-3's headline number, 4,039 tokens per GPU per second against 2,324 for DeepSeek-V3 under the same decoding target of 20 tokens/s, sets two different models against each other, so it does not isolate the layout<sup>264</sup>.

Training decides one thing here: how sparse a model the expert pool has to serve. Step-3 measures sparsity as activated experts, shared included, over routed experts, and derives the sparsest MoE an expert pool can serve while staying compute-bound and overlapping communication with computation. The bound rises with the model's width and depth; at DeepSeek-V3's width and depth on H800 it is 0.058, and Step-3 trained at about 0.08<sup>265</sup>. A sparser model falls back on large expert parallelism or on routing restrictions such as the group-limited routing of 3.7<sup>266</sup>.

> **Recommendation:** Use it when your inference engine can run attention and the experts as separate GPU pools, as MegaScale-Infer and Step-3's serving system do, and when that layout beats a colocated expert-parallel layout re-provisioned for the same number of GPUs, since that is the comparison under which the published gain shrank to parity in Qiu et al.'s model<sup>262</sup>. If you plan to serve this way, compute Step-3's bound for your width, depth and hardware before you fix the expert count and top-k, and keep the activated fraction above it<sup>265</sup>.

Where attention and the experts run is a serving decision, but in RL post-training the serving engine also writes the rollouts the trainer learns from. Can you count on the trainer sending each token to the same experts the rollout engine did?

#### RL routing

RL post-training separates sample generation from gradient computation. A rollout engine generates the samples with its own kernels and, in off-policy or async RL, with weights one update or more behind the trainer's, and the trainer recomputes each token to take the gradient. These differences can shift token probabilities, but in an MoE they can also change which experts a token runs through, so the trainer differentiates a path the sample never took<sup>267,268</sup>.

Each cause has been measured on its own. Ma et al. generated responses with [SGLang](https://github.com/sgl-project/sglang) on Qwen3-30B-A3B and fed them through Megatron: about 10% of the routers chose different experts, and 94% of tokens differed in at least one layer<sup>267,269</sup>. Zheng et al., the authors of GSPO, measured the other cause on Qwen3-30B-A3B-Base: after one gradient update, about 10% of the experts activated for the same rollout had changed<sup>268</sup>. The two 10%s count different things: routers that disagree across engines, and activated experts that change in one update.

Ma et al.'s fix, R3, records the experts the rollout picked and replays them in the trainer. That removes the routing share of the gap but not the rest of it: the train-inference KL fell from 1.5e-3 to 7.5e-4, near the dense Qwen3-8B's 6.4e-4<sup>270</sup>. In Megatron, `--moe-enable-routing-replay` makes the inference engine record each request's top-k. Your RL framework then hands those indices back to the trainer with `set_replay_data` before a `REPLAY_FORWARD` pass. Record with the engine's async scheduling off, since the engine refuses the two together. Replay does not freeze the router: in `REPLAY_FORWARD` it gathers its own current scores at the replayed indices, so its gradient flows through the experts the rollout chose rather than the ones it would pick itself.

> *Margin note:* A third action, `REPLAY_BACKWARD`, replays the indices again when [activation recomputation](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=activation_recomputation) repeats the forward pass during backpropagation.

*Collapsible:* Megatron source

*Collapsible:* [`inference_request.py#L786-L787`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/inference/inference_request.py#L786-L787) (rollout's indices per request)

```
# routing_indices is reconstructed from per-block storage when a request finishes.
routing_indices: Optional[np.ndarray] = None
```

*Collapsible:* [`router_replay.md#L70-L80`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/docs/api-guide/router_replay.md#L70-L80) (`set_replay_data`, then `REPLAY_FORWARD`)

```
1.  **Enable & Instantiate**
    - Create one `RouterReplay` instance per MoE router layer when building the model.
    - Optionally use the global helpers to set/clear actions across all layers.
2.  **Record Routing Decisions**
    - Set action: `RouterReplay.set_global_router_replay_action(RouterReplayAction.RECORD)`.
    - Run the model; retrieve per-layer indices via `RouterReplay.get_recorded_data()` and persist.
3.  **Forward Replay**
    - Load indices and distribute: `RouterReplay.set_replay_data(list_of_tensors)`.
    - Set action: `RouterReplay.set_global_router_replay_action(RouterReplayAction.REPLAY_FORWARD)`.
    - Run the model; dynamic top‑k is bypassed and target indices are used.
4.  **Backward Replay**
```

*Collapsible:* [`router_replay.py#L13-L15`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router_replay.py#L13-L15) (`REPLAY_BACKWARD` under recomputation)

```
RECORD = "record"  # Record the topk indices for replay
REPLAY_FORWARD = "replay_forward"  # Replay the recorded topk indices for forward pass
REPLAY_BACKWARD = "replay_backward"  # Replay topk indices for re-compute during backward pass
```

*Collapsible:* [`router_replay.py#L161-L182`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router_replay.py#L161-L182) (record, or gather replayed indices)

```
if self.router_replay_action == RouterReplayAction.RECORD:
    probs, top_indices = default_compute_topk(
        scores, topk, num_groups=num_groups, group_topk=group_topk
    )
    self.record_indices(top_indices)
    return probs, top_indices
elif self.router_replay_action == RouterReplayAction.REPLAY_FORWARD:
    top_indices = self.target_topk_idx
    # Ensure indices are on the correct device
    top_indices = top_indices.to(scores.device)
    # Gather the scores for the replayed indices to get the probabilities
    probs = scores.gather(1, top_indices)
    return probs, top_indices
elif self.router_replay_action == RouterReplayAction.REPLAY_BACKWARD:
    top_indices = self.replay_backward_list.pop(0)
    # Ensure indices are on the correct device
    top_indices = top_indices.to(scores.device)
    # Gather the scores for the replayed indices to get the probabilities
    probs = scores.gather(1, top_indices)
    return probs, top_indices
else:
    return default_compute_topk(scores, topk, num_groups, group_topk)
```

*Collapsible:* [`moe_utils.py#L899-L907`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L899-L907) (top-k hands off to replay)

```
def compute_topk(scores, topk, num_groups=None, group_topk=None):
    # Default behavior if no replay is active
    if router_replay is None:
        return _compute_topk(scores, topk, num_groups=num_groups, group_topk=group_topk)
    else:
        return router_replay.get_replay_topk(
            scores, topk, num_groups, group_topk, _compute_topk
        )
```

*Collapsible:* [`dynamic_engine.py#L1863-L1864`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/inference/engines/dynamic_engine.py#L1863-L1864) (recording refused with async scheduling)

```
if model_config.moe_enable_routing_replay:
    raise ValueError("Async scheduling does not support routing replay.")
```

*Collapsible:* [`mcore-inference-user-guide.md#L133-L149`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/docs/mcore-inference-user-guide.md#L133-L149) (batch-invariant mode for the train-inference mismatch)

```
> **Batch-invariant kernels (training and inference log-prob consistency).** Standard
> GEMM, attention, and norm kernels can produce slightly different numerics depending
> on batch composition, which shows up as log-prob mismatch between training and
> inference. This mismatch is a real source of error and instability in RL. Megatron Inference
> offers *batch-invariant kernels* whose outputs do not depend on how requests are
> batched, so per-token log-probs match between the training and inference forward
> passes.
>
> Enable it with `batch_invariant_mode` on the model's `TransformerConfig` — it
> is *not* an `InferenceConfig` field, so it must be set when you build the
> model, not on the engine config. Two companion fields tune it:
> `batch_invariant_backend` (`te_native` by default, or `deepgemm` / `triton`)
> selects the GEMM backend, and `batch_invariant_collective` (`ordered` by
> default, or `multimem`) selects the cross-rank expert-combine reduction.
>
> Both dense and MoE models are supported. Batch-invariant MoE supports BF16 and
> MXFP8 squared-ReLU/SwiGLU experts, requires unfused permute/unpermute, and under
```

*Collapsible:* [`transformer_config.py#L3770-L3803`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L3770-L3803) (batch-invariant requirements)

```
assert self.params_dtype == torch.bfloat16, (
    "Batch invariant mode supports BF16 model parameters only; "
    f"got {self.params_dtype}."
)
assert (
    self.attention_backend == AttnBackend.flash
), "Batch invariant mode only supports FlashAttention (--attention-backend flash)"
# The training (TransformerEngine) and inference attention paths must run
# the same FlashAttention kernel, so the version cannot be left to each
# path's autodetection. FlashAttention-2 is excluded because it does not
# expose the fixed num_splits schedule the batch-invariant kernels require.
assert self.flash_attention_version in (3, 4), (
    "Batch invariant mode requires --flash-attention-version 3 or 4 so the "
    "training and inference attention paths run the same batch-invariant "
    f"FlashAttention kernel (got {self.flash_attention_version})."
)
# Context parallelism routes through TE's FA2 fwd/bwd kernels directly, which
# cannot be pinned to another version; dropout is not batch-invariant.
assert (
    self.context_parallel_size == 1
), "Batch invariant mode does not support context parallelism"
assert (
    self.attention_dropout == 0.0
), "Batch invariant mode does not support attention dropout"
if (self.num_moe_experts or 0) > 0:
    from megatron.core.transformer.custom_layers.batch_invariant_kernels import (
        HAVE_DEEPGEMM_BF16,
    )
    if self.transformer_impl != "inference_optimized":
        assert self.moe_token_dispatcher_type == "alltoall", (
            "Batch-invariant MoE training requires "
            "moe_token_dispatcher_type='alltoall'."
        )
```

*Collapsible:* [`transformer_config.py#L1337-L1341`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/transformer_config.py#L1337-L1341) ("will significantly affect speed")

```
batch_invariant_mode: bool = False
"""If true, uses batch-invariant kernels that provide deterministic forward execution regardless
   of batch size. This ensures bitwise identical results when the same inputs are processed
   in different batch configurations. This will significantly affect speed of 
   training and inference as the kernels are not full optimized.
```

*Collapsible:* [`rl_utils.py#L521-L533`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/rl/rl_utils.py#L521-L533) (train-inference probability metrics)

```
    group_stats: Statistics object to update with computed metrics
"""
n_elems = mask.sum()
if n_elems > 0:
    ratios = (old_logprobs - inference_logprobs).exp()[mask]
    abs_diffs = (old_logprobs.exp() - inference_logprobs.exp()).abs()[mask]
    group_stats.min_piold_to_inf_prob = ratios.min().item()
    group_stats.max_piold_to_inf_prob = ratios.max().item()
    group_stats.mean_piold_to_inf_prob = (ratios.sum() / n_elems).item()
    group_stats.min_inf_train_prob_abs_diff = abs_diffs.min().item()
    group_stats.max_inf_train_prob_abs_diff = abs_diffs.max().item()
    group_stats.mean_inf_train_prob_abs_diff = (abs_diffs.sum() / n_elems).item()
```

*Collapsible:* [`rl_utils.py#L1991-L2001`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/rl/rl_utils.py#L1991-L2001) (train-inference gap logged)

```
metrics = {
    'min_piold_to_inf_prob': group_stats.min_piold_to_inf_prob,
    'max_piold_to_inf_prob': group_stats.max_piold_to_inf_prob,
    'mean_piold_to_inf_prob': group_stats.mean_piold_to_inf_prob,
    'min_inf_train_prob_abs_diff': group_stats.min_inf_train_prob_abs_diff,
    'max_inf_train_prob_abs_diff': group_stats.max_inf_train_prob_abs_diff,
    'mean_inf_train_prob_abs_diff': group_stats.mean_inf_train_prob_abs_diff,
    'min_inf_prob': group_stats.min_inf_prob,
    'max_inf_prob': group_stats.max_inf_prob,
    'mean_inf_prob': group_stats.mean_inf_prob,
}
```

The figure below simulates one toy MoE layer, 4 of 16 experts over 512 tokens, whose rollout routes with its own numerics and one update behind the trainer, each cause scaled to match its measurement above. Between a trainer that routes on its own and one that replays, a middle row freezes the router matrix. On the left, compare the experts the trainer runs for a token with the rollout's picks; on the right, follow the share of tokens whose experts differ from the rollout's: in the toy it stays high when the trainer routes on its own, a frozen router still leaves the share that comes from numerics and from the router's changing input, and replay brings it to zero by construction.

![router-drift](https://huggingface-moe-blogpost.hf.space/viz/posters/router-drift.webp)

*Figure caption:* Figure 4.5

Released RL recipes sit on both sides of that choice. DeepSeek-V3.2, MiMo-V2-Flash and Instella-MoE replay the rollout's routing in the trainer<sup>271,272,273</sup>, while Kimi K2.5 and Mellum 2 describe no replay and handle the mismatch in the loss, by masking the gradient of tokens whose probability ratio drifts too far<sup>274,275</sup>.

Whether replay pays off in reward is still contested. In Ma et al.'s comparison on Qwen3-30B-A3B, GRPO without replay crashed in all three settings, GRPO with truncated importance sampling in one of two, and no run with replay crashed<sup>276</sup>, and they report significant improvements in training stability and performance<sup>267</sup>. A later Qwen study by Zheng et al. saw no gain from R3 in on-policy training<sup>277</sup>, and in He et al.'s runs replay scored below plain GRPO on Moonlight-16B-A3B, though not on Qwen's 30B-A3B model<sup>278</sup>. The overhead is small in rollout, under 3% added latency for storing the routing<sup>279</sup>. The GSPO authors, who had used replay, list extra memory and communication and a possible limit on the model's capacity, and dropped it for sequence-level importance ratios<sup>268</sup>.

TRL handles the same mismatch without replay. In its `GRPOConfig`, `importance_sampling_level="sequence"` gives GSPO's sequence-level ratios, and `vllm_importance_sampling_correction`, on by default, applies importance-sampling ratios between the trainer's and [vLLM](https://github.com/vllm-project/vllm)'s probabilities and masks out sequences whose ratio falls outside a set range<sup>280</sup>.

Part of what replay leaves is the kernels' own share of the gap, which Megatron targets with `--batch-invariant-mode`: it documents batch-invariant kernels as the fix for log-probability mismatch between training and inference, "a real source of error and instability in RL". It needs flash attention 3 or 4 and, for MoE training, the `alltoall` dispatcher, and Megatron warns that it "will significantly affect speed". On our 64-expert MoE, at an older Megatron commit, two runs with it printed identical losses and grad norms at all 12 iterations, and its cost in iteration time could not be separated from run-to-run spread. Rollout weights one update behind the trainer's are a separate cause, which batch-invariant mode leaves in place<sup>268</sup>.

DeepInfer, DeepSeek's production serving engine, ships the same option: it keeps model results identical across batch compositions when `DEEPINFER_BATCH_INVARIANT=1` is set, and with `DEEPINFER_ENABLE_MTP_VARLEN=0` and a fixed seed per request, it samples deterministically, on NVIDIA GPUs only<sup>281</sup>.

StepFun's RL for Step 5 Preview uses both remedies. With rollouts on the current weights, it aligned the training and inference operators until their log-probabilities matched bitwise, at under 10% overhead. With stale rollouts, it replays the routed experts, both their indices and their coefficients, with the router frozen, for the actor and the reference policy alike. That goes further than Megatron's replay, which recomputes the weights at the replayed indices from the router's current scores<sup>282</sup>.

NVIDIA's NeMo-RL recipes for Nemotron 3 Super and Ultra freeze the router matrix in async RL whose rollouts lag the trainer by at most one update, and keep updating the balancing bias that Megatron adds to the scores only to select experts<sup>283</sup>. That bias moves every step, so selection still changes under the frozen matrix, a drift the frozen row in the figure leaves out.

Quantized rollout activations widen the same gap. Zhuge et al. at Qwen ran NVFP4 rollouts, with weights and activations both in 4 bits, against a BF16 trainer, and training collapsed after about 150 steps. Comparing rollouts that quantized only the weights with rollouts that quantized only the activations, they traced the collapse to the quantized activations rather than the weights<sup>284</sup>.

> **Watch:** A mismatch that hurts shows up as an RL run that learns badly or crashes<sup>276</sup>. The signal is the train-inference probability gap, in two metrics Megatron's RL loop logs to W&B: `mean_inf_train_prob_abs_diff`, the mean absolute difference between trainer and rollout probabilities, and `max_piold_to_inf_prob`, the largest ratio of trainer over rollout probability. To see the routing share alone, compare the `routing_indices` that Megatron's inference engine records with the trainer's own top-k offline.

> **Recommendation:** Use it when the trainer and the rollout engine of an MoE's RL run disagree on routing, whether from separate engines or, in off-policy or async RL, from rollout weights that lag the trainer's. Replay removes that disagreement, but its reward gains are contested: Ma et al. report gains, while the Qwen on-policy study saw none. Measure how many routers disagree, then compare learning with and without replay before you keep it. If you also quantize the rollouts, try quantizing only the weights first, since in Zhuge et al.'s runs the quantized activations drove the collapse.

You have now carried an MoE from its first dense baseline through serving and into an RL loop. Which of the choices along the way can you take as settled, and which are still open?

### 5. Conclusion

We started from a dense run, took the MoE layer apart setting by setting, and then followed the trained model into serving and RL post-training. You can now test a cluster before trusting it, train a dense baseline and an MoE on the same data and launch script, and make two runs repeatable enough to compare. Chapter 3 paired each part of the layer, from the router's scores to the all-to-all, with a signal to watch and a recommendation. Appendix [A.2](#s-a-2) runs the other way, from a symptom on the dashboard back to the config behind it.

The block below gathers every flag the chapters recommend, each with a comment naming the section that argues for it: commented-out lines hold only under a condition or replace a line above them, and values in angle brackets are yours to choose. Start from your own launch script and bring the groups in one at a time, measuring each against the run before it, since each recommendation comes from its own setup and their gains need not add up.

*Collapsible:* Every recommended flag, by section

```
# 2.1 Test your hardware
--gpu-sniff-test-interval <n>               # 2.1: GPU and EP all-to-all check every n iters

# 2.2 Build your image (EFA on AWS P5)
# 2.2, 3.7: EFA libraries first, or NCCL quietly falls back to sockets
export LD_LIBRARY_PATH=/opt/amazon/ofi-nccl/lib:/opt/amazon/efa/lib:${LD_LIBRARY_PATH:-}
export NCCL_NET_PLUGIN=ofi                  # 2.2: by name; a path left NCCL on sockets
export FI_PROVIDER=efa                      # 2.2
export FI_EFA_USE_DEVICE_RDMA=1             # 2.2
export NCCL_SOCKET_IFNAME='^lo,docker0,veth_def_agent'  # 2.2: adapt to your interfaces
export NCCL_DEBUG=INFO                      # 2.2, 3.7: want "Using network Libfabric"

# 2.5 Your first MoE
# --deterministic-mode                      # 2.5: to compare runs or chase a NaN;
# export NVTE_ALLOW_NONDETERMINISTIC_ALGO=0 #   also drop --cross-entropy-loss-fusion

# 3.0 Monitoring
--moe-per-layer-logging                     # 3.0, 3.5: router losses per layer
--save <dir> --save-interval <m>            # 3.0: token counts and dumps go here
--save-tokens-per-expert-interval <n>       # 3.0, 3.3: tokens per expert, MaxVio
--log-throughput --log-params-norm          # 3.0: TFLOP/s, parameter norm
--log-num-zeros-in-grad --log-max-attention-logit  # 3.0: run health
# --moe-routing-trace-path <dir> --moe-routing-trace-max-training-iters <n>
# --cuda-graph-impl none                    # 3.0: bounded routing trace; hooks skip graphs
# --save-activations-interval <n>           # 3.0, 3.4: expert output norms; sample sparsely

# 3.1 Router scoring
--moe-router-dtype fp32                     # 3.1: bf16 ties can flip experts
# --moe-router-score-function sigmoid       # 3.1, 3.3: needed by the expert bias
# --moe-router-pre-softmax                  # 3.1: softmax at top-1, else no router gradient
# --moe-z-loss-coeff 1e-3                   # 3.1: softmax router whose logits drift up

# 3.2 Routing strategy
# --moe-num-hash-layers <n>                 # 3.2: only to reproduce DeepSeek-V4;
#                                           #   load a fixed table, not the placeholder

# 3.3 Load balancing
--moe-router-load-balancing-type aux_loss --moe-aux-loss-coeff 1e-3  # 3.3 Aux loss
# --moe-router-force-load-balancing         # 3.3, 3.7: control run only, never train
# --moe-router-load-balancing-type global_aux_loss  # 3.3 Scope: domain experts, +5.8% step
# 3.3 Loss-free bias, in place of the aux_loss line:
# --moe-router-enable-expert-bias --moe-router-score-function sigmoid
# --moe-router-bias-update-rate <rate>      # tune to expert count; 1e-3 coarse past 128
# --moe-router-load-balancing-type seq_aux_loss --moe-aux-loss-coeff 1e-4  # DeepSeek-V3
# --moe-router-load-balancing-type quantile_balancing  # 3.3 Quantile: no aux loss,
#                                           #   router fusion or group-limited routing

# 3.4 Experts
# 2.5 shape; 3.4 Count and size: finer experts help, up to a point
--num-experts 64 --moe-ffn-hidden-size 1024 --moe-router-topk 8
# --moe-latent-size <l>                     # 3.4 Latent MoE: more experts, same traffic
# --moe-use-norm-before-up-proj             # 3.4: Kimi K3's fix for latent blow-ups
# --moe-shared-expert-intermediate-size 1024  # 3.4: routed width, top-k one lower
# --activation-func-clamp-value 10          # 3.4 Activation: if expert norms diverge
# --activation-func-tanh-clamp-scale 4 --activation-func-tanh-clamp-scale-linear 25
#                                           # 3.4: Kimi K3's SiTU-GLU, Megatron Core v0.20 on

# 3.5 Block layout
# --moe-layer-freq "([0]+[1]*15)"           # 3.5: leading dense layer, fewer all-to-alls
# --moe-shortcut-connection --moe-shortcut-parallel  # 3.5 Block wiring: hybrid stack;
#                                           #   no FSDP, CUDA graphs or full recompute

# 3.6 Training
# --moe-use-upcycling --moe-upcycling-granularity 8  # 3.6: first run only, 2.5's two fixes
# --optimizer muon --muon-extra-scale-factor 0.2     # 3.6 Optimizer: 1.0 diverged; no FSDP
# --moe-router-skip-muon                    # 3.6: router on Adam, Megatron Core v0.20 on
# --mtp-num-layers 1 --mtp-loss-scaling-factor 0.1   # 3.6 MTP
# --pipeline-model-parallel-layout <layout> # 3.6: place the MTP layer under PP
# --timing-log-level 2 --timing-log-option all       # 3.6: find the slowest PP stage
--rerun-mode validate_results               # 3.6 Stability: the default; keep it

# 3.7 Systems
# --profile --profile-step-start <a> --profile-step-end <b> --profile-ranks <r>
#                                           # 3.7 Profiling: one step per new config
# --moe-permute-fusion                      # 3.7: if permute and copy kernels show
--expert-model-parallel-size 8              # 3.7 Interconnect: EP inside one node
# --overlap-moe-expert-parallel-comm --delay-wgrad-compute  # 3.7 Overlap: exposed
#                                           #   all-to-all; no full recompute, VPP under PP
# --recompute-granularity selective --recompute-modules layernorm moe_act
# --fine-grained-activation-offloading --offload-modules core_attn attn_proj expert_fc1
#                                           # 3.7 Memory: when the overlap does not fit
# --activation-offload-fraction <f>         # 3.7: lower it if step time grows
# --moe-token-dispatcher-type flex --moe-router-num-groups <nodes> --moe-router-group-topk <g>
#                                           # 3.7 Group-limited: EP across nodes, DeepEP
# --moe-expert-capacity-factor <cf> --moe-pad-expert-input-to-capacity
#                                           # 3.7 Capacity: memory short; dropless to fine-tune
# --fp8-format <fmt> --fp8-recipe blockwise # 3.7 Precision: Hopper; mxfp8 on Blackwell
# --moe-router-padding-for-quantization     # 3.7: aligned counts for quantized GEMMs
# --moe-dispatch-fwd-dtype mxfp8 --moe-combine-bwd-dtype mxfp8  # 3.7: ncclep, Blackwell

# 4 From training to serving
# --fp4-format e2m1                         # 4 Low-bit: NVFP4 on Blackwell, not with FP8
# --rl-inference-expert-model-parallel-size <n>  # 4: rollout engine's own EP size
# --moe-enable-routing-replay               # 4 RL routing: rollout and trainer disagree
# --batch-invariant-mode                    # 4: kernels' share of the mismatch; slow
```

Plenty remains open. Most of what we know about training MoEs at scale comes from the technical reports of open-weight models, and a report shows what a team shipped: rarely what it tried and dropped, or the run that settled a choice. Many of the recommendations above rest on one ablation in one lab's setup, and each is an experiment worth rerunning at another scale, on other data or on another cluster. If you run one, publish it with its configs and logs, the negative results included: that is how the next team starts from what you learned instead of from scratch. Share yours, or ask about ours, on the [discussion page](https://huggingface.co/spaces/huggingface/moe-blogpost/discussions) of this post.

We hope this post saves your next MoE run a few of the days it cost ours.

#### Acknowledgements

We thank [Antoine Bosselut](https://huggingface.co/atcbosselut), [Martin Jaggi](https://huggingface.co/mjaggi) and the Swiss AI team for providing part of the compute behind this post, and for insightful conversations along the way. We also thank [Thibaud Frere](https://huggingface.co/tfrere) for his help with the figures.

### Appendix

#### A.1 Monitoring in detail

This appendix gives the commands and calculations behind chapter 3's Watch callouts. Router statistics describe the distribution of work, routing traces retain individual expert selections, and activation dumps show what the experts produce. Run-level logs put those measurements alongside loss, timing and memory.

The recipes target [Megatron](https://github.com/NVIDIA/Megatron-LM) commit `d6316eb45`. Keep the configuration and rank layout with each capture: they determine how local expert ids, token positions and routing scores should be interpreted. Collect traces and activations in short diagnostic runs, separately from throughput measurements.

*Collapsible:* Code

*Collapsible:* [`router.py#L691-L700`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L691-L700) (aux loss, one slot per layer)

```
layer_number = self._get_metric_layer_number()
get_moe_metrics_tracker().record(
    aux_loss_name,
    aux_loss / aux_loss_coeff,
    layer_number,
    num_layers,
    reduce_group=reduce_group,
    needs_dp_avg=needs_dp_avg,
)
```

*Collapsible:* [`router.py#L805-L811`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router.py#L805-L811) (z-loss, one slot per layer)

```
get_moe_metrics_tracker().record(
    "z_loss",
    z_loss / moe_z_loss_coeff,
    layer_number,
    num_layers,
    avg_group=self.tp_dp_cp_group,
)
```

*Collapsible:* [`moe_logging.py#L392-L404`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_logging.py#L392-L404) (per-layer scalars)

```
for name in metric_names:
    if name not in self._metrics:
        continue
    values = self._metrics[name].values.float() * loss_scale
    is_sparse = percentiles is not None and name in percentiles
    for i, val in enumerate(values.tolist()):
        if is_sparse and val == 0:
            continue
        if writer is not None:
            writer.add_scalar(f"moe/{name}_layer_{i}", val, iteration)
        if wandb_writer is not None:
            wandb_writer.log({f"moe/{name}_layer_{i}": val}, iteration)
```

*Collapsible:* [`router_trace.py#L217-L221`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router_trace.py#L217-L221) (hook on every router)

```
for chunk in model:
    unwrapped = unwrap_model(chunk)
    for module_name, module in unwrapped.named_modules():
        if isinstance(module, TopKRouter):
            handle = module.register_forward_hook(self.make_hook(module_name))
```

*Collapsible:* [`router_trace.py#L353-L365`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router_trace.py#L353-L365) (routing map to top-k ids)

```
if second.dtype == torch.bool:
    topk = getattr(module, "topk", None)
    if topk is None:
        return
    num_tokens = second.shape[0]
    _, expert_idx = second.nonzero(as_tuple=True)
    if expert_idx.numel() != num_tokens * topk:
        return
    top_indices = expert_idx.view(num_tokens, topk)
else:
    top_indices = second
top_indices_cpu = top_indices.detach().to("cpu", torch.int32, non_blocking=True)
```

*Collapsible:* [`router_trace.py#L383-L395`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router_trace.py#L383-L395) (logits recomputed, saved bf16)

```
if self.capture_logits:
    hs_for_gating = self._extract_hidden_state(inputs, num_tokens)
    gating_fn = getattr(module, "gating", None)
    if hs_for_gating is not None and callable(gating_fn):
        try:
            with torch.no_grad():
                logits = gating_fn(hs_for_gating)
            if isinstance(logits, tuple):
                logits = logits[0]
        except Exception:
            logits = None
        if torch.is_tensor(logits) and logits.shape[0] == num_tokens:
            logits_cpu = logits.detach().to("cpu", dtype=torch.bfloat16).contiguous()
```

*Collapsible:* [`training.py#L5387-L5393`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/training.py#L5387-L5393) (params norm)

```
if _should_compute_params_norm(args, iteration, is_first_iteration):
    # Cross-rank param L2 norm (--log-params-norm): a full-model reduction
    # + all-reduce that BLOCKS the training loop -- exposed goodput cost
    # (~1.5s cold on the first iteration, ~10ms steady). Kept as a real
    # cost span (it stalls the critical path), unlike passive monitors.
    with _otel_managed_span('step', 'megatron.train.params_norm', is_goodput_span=True):
        params_norm = calc_params_l2_norm(model, pg_collection=pg_collection)
```

*Collapsible:* [`clip_grads.py#L282-L288`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/optimizer/clip_grads.py#L282-L288) (zeros in the gradient)

```
if grad_not_none and is_not_shared and is_not_tp_duplicate and is_not_gtp_duplicate:
    grad_obj = getattr(param, grad_attr)
    data_parallel_group = get_data_parallel_group_if_dtensor(grad_obj, data_parallel_group)
    grad = to_local_if_dtensor(grad_obj).detach()
    num_zeros = grad.numel() - torch.count_nonzero(grad)
    num_zeros -= _gtp_pad_zero_count(param, grad)  # exclude structural GTP padding
    total_num_zeros = num_zeros + total_num_zeros
```

*Collapsible:* [`qk_clip.py#L30-L40`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/optimizer/qk_clip.py#L30-L40) (max attention logit)

```
torch.distributed.all_reduce(
    transformer_layer.self_attention.core_attention.current_max_attn_logits,
    op=torch.distributed.ReduceOp.MAX,
    group=parallel_state.get_data_parallel_group(with_context_parallel=True),
)
log_max_attention_logit = max(
    log_max_attention_logit,
    torch.max(
        transformer_layer.self_attention.core_attention.current_max_attn_logits
    ).item(),
)
```

*Collapsible:* [`param_and_grad_buffer.py#L396-L406`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/distributed/param_and_grad_buffer.py#L396-L406) (NaN grad stops the run)

```
grad_norm = self.buckets[i].grad_data.norm(p=2)
# check for NaN, Inf and unexpectedly large grads
if check_for_nan_or_inf:
    rerun_state_machine.validate_result(
        result=grad_norm,
        rejection_func=torch.isnan,
        message=f"found NaN in local grad norm for bucket #{i} "
        f"in backward pass before data-parallel communication collective",
        tolerance=0.001,  # 0.1% tolerance to account for non-deterministic FA backward
        fatal=True,
    )
```

Our scripts: [`router_watch.py`](https://gist.github.com/nmntz/5de952d686f66d7bce5bce8cba9d7139#file-router_watch-py) reads token counts and routing traces and checks fp32 flips on a live router, [`expert_watch.py`](https://gist.github.com/nmntz/5de952d686f66d7bce5bce8cba9d7139#file-expert_watch-py) reads activation dumps, and [`expert_watch_hooks.py`](https://gist.github.com/nmntz/5de952d686f66d7bce5bce8cba9d7139#file-expert_watch_hooks-py) samples a live forward; their commands and capture recipes appear beside the relevant metric in the prose.

##### Router stats

###### Per-layer losses

Enable `--moe-per-layer-logging` with the [Trackio](https://huggingface.co/docs/trackio) launcher from [2.4](#s-2-4) to record the auxiliary loss and z-loss for each layer. Megatron logs the losses enabled in the configuration, with their coefficients divided out. A run using expert bias for balancing can still report a sequence-wise auxiliary loss or z-loss when those losses are enabled.

The auxiliary loss can read 1 with flat probabilities even when token counts are uneven ([3.3](#s-3-3)), so use token counts to measure load directly. Z-loss describes the scale of the logits: the square root of its logged value gives the RMS of logsumexp across tokens.

###### Expert counts and MaxVio

To save the number of tokens processed by each local expert, add these flags to the training command:

```
--save run/ \
--moe-grouped-gemm \
--save-tokens-per-expert-interval 100
```

The hook on the grouped linear layers writes `run/tokens_per_expert/rank*.jsonl`. Each record identifies an iteration and layer, with a `tpe` list containing a count vector for each captured micro-batch. Decoder layers and MTP layers have separate identities. The vectors describe local expert loads after dispatch ([`activation_logging.py`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/activation_logging.py)).

For an expert count vector c, MaxVio measures the busiest expert's excess load relative to the mean<sup>52</sup>:

*Calculation:*
```
MaxVio = max(c) / mean(c) - 1
```

For example, counts `[2, 2, 4, 0]` have a mean of 2 and MaxVio of 1: the busiest expert receives twice the average load. The zero-count expert contributes to that mean and must remain in the calculation. An even load gives 0; an all-zero vector has undefined MaxVio.

Choose the aggregation scope before computing the metric:

- **Micro-batch:** join the local expert vectors across one expert-parallel (EP) group, in global expert-id order.

- **Global batch:** sum each expert's counts over micro-batches and independent data replicas, then compute MaxVio from the resulting vector.

- **Sequence:** use individual routing selections and sequence boundaries, as described under Routing diagnostics.

Averaging micro-batch MaxVio values does not give global-batch MaxVio. Experts can be unevenly loaded within each micro-batch yet balanced over the batch ([3.3](#s-3-3)). The aggregation must also preserve layer identity: keep pipeline stages and MTP depths separate. [Interleaved pipeline](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=interleaving_stages) chunks reuse local layer ids, and the saved records do not distinguish them ([`activation_logging.py#L131-L134`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/training/activation_logging.py#L131-L134)), so disable interleaving for the capture. [Activation recomputation](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=activation_recomputation) can duplicate hook calls, so capture without recomputation or retain identifiers for the original forwards.

The [`router_watch.py`](https://gist.github.com/nmntz/5de952d686f66d7bce5bce8cba9d7139#file-router_watch-py) reader joins count files using an explicit map from rank to global expert ids. For two ranks holding four experts, save `{"0": [0, 1], "1": [2, 3]}` as `experts.json`, then run:

```
python3 scripts/router_watch.py counts run/tokens_per_expert \
    --num-experts 4 --ranks 0 1 \
    --expert-map experts.json --pool-ranks
```

`--pool-ranks` declares that the selected files contain independent work for the same layer, with tensor-parallel duplicates removed. For per-micro-batch measurements, retain the identities needed to match captured forwards across ranks.

###### Load per rank

Sum the counts of the experts placed on each EP rank, then compare the busiest rank with the mean. Read this alongside expert MaxVio: several busy experts placed on the same GPU can concentrate work there ([3.3](#s-3-3), [3.7](#s-3-7)).

With capacity limits or padding enabled, grouped GEMM counts describe the work after those operations. To measure the original demand, use the router's unpadded assignments.

##### Routing diagnostics

###### Capturing expert selections

For a short capture, add the following flags to the training command, replacing `trace_steps` with the number of iterations to capture:

```
--moe-routing-trace-path trace/ \
--moe-routing-trace-max-training-iters trace_steps \
--cuda-graph-impl none
```

The hook records selected expert ids before dispatch. Add `--moe-routing-trace-capture-logits` to save the logits file, or `--moe-routing-trace-capture-hidden-states --moe-routing-trace-dump-weights` to save hidden states and router weights. These captures write to disk, and the Python hooks require eager execution.

Expert ids follow the routing map's order, so sort by reconstructed weight when a metric needs the leading expert. Dropping can cause an entire record to be skipped. Treat such a gap as a missing observation ([`router_trace.py`](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/router_trace.py)).

###### Counts and MaxVio from a trace

The selected expert ids also give token counts and MaxVio, without a logits capture. To read these for one rank with 64 experts:

```
python3 scripts/router_watch.py trace trace/ --num-experts 64 --ranks 0
```

Each `trace_call` record contains `counts` and `maxvio` for one captured call. The `rank_captured_step` records sum those counts within each layer, rank and step, then compute MaxVio from the sum. These summaries cover the captured tokens; a global-batch measurement requires all of its original forwards and independent replicas, with tensor-parallel duplicates removed. Use the aggregation rules under Expert counts and MaxVio when joining captures. Records skipped because of dropped assignments remain missing from these totals.

###### Per-sequence balance

Per-sequence balance requires the sequence membership of each token row. For complete, unpartitioned inputs laid out as `[sequence, batch, hidden]`, with batch size B, row `s * B + b` belongs to sequence b. Pass `--sequence-length S --batch-size B` to the trace reader only when that layout holds.

Within each sequence, count assignments to each expert, including experts with zero assignments, then compute MaxVio from that vector. Summarize the per-sequence values by layer.

For packed sequences, replace the fixed-length layout with the actual sequence boundaries. Context or [sequence parallelism](https://huggingface.co/spaces/nanotron/ultrascale-playbook?section=sequence_parallelism) also requires token positions to join the pieces across ranks. Following a token across observations requires its identity as well, since the same row number at two training steps generally refers to different tokens.

###### Mixture weights

The logits file supports an approximate reconstruction of the weights applied to the selected experts. The hook recomputes these logits and stores them in bf16. Preserve the recorded selections, and use the run's score function, normalization and routed scaling factor when reconstructing the weights.

For a softmax capture with 64 experts and a scaling factor of 1:

```
python3 scripts/router_watch.py trace trace/ \
    --num-experts 64 --ranks 0 --score softmax --scale 1
```

Add `--pre-softmax` if the run applied softmax over all experts before selection. Otherwise, softmax applies over the selected logits. For sigmoid and sqrt(softplus), use the run's normalization of the selected scores. Expert bias affects selection; keep it out of the mixture weights.

Let w denote the final selected weights, including the scaling factor, and let q be w divided by its sum. Compute each metric per token before summarizing it by layer:

- **Largest weight:** `max(w)` is the largest multiplier on an expert output. Use `max(q)` to compare concentration across different scaling factors.

- **Selected-weight entropy:** `-sum(q * log(q))` ranges from 0 to `log(k)` and increases as the k selected weights become more equal. At top-1 it is 0.

- **Max1/Max2:** the largest weight divided by the second largest. Values near 1 indicate similar leading weights; the ratio is undefined at top-1.

- **Estimated mixture RMS:** `sqrt(sum(q*q))` estimates mixture RMS relative to one expert when expert outputs have equal RMS and are uncorrelated ([3.1](#s-3-1)). Using w includes the routed scaling factor.

- **Top-k probability mass:** for pre-softmax routing, sum the selected full-softmax probabilities before scaling. Raw sigmoid and sqrt(softplus) scores have a different interpretation because they are not probabilities over all experts.

For illustration, selected weights `[0.75, 0.25]` give a largest weight of 0.75, Max1/Max2 of 3 and entropy of about 0.562, using natural logarithms.

###### Nodes reached per token

To measure communication fan-out, map the selected expert ids to their destination nodes and count the distinct nodes for each token. Report the mean and maximum by layer ([3.7](#s-3-7)).

Pass `--node-map nodes.json` to the trace reader. The file maps global expert ids to node names, for example `{"0": "node-a", "1": "node-a", "2": "node-b"}`. For replicated experts, capture the destination actually chosen by the dispatcher. Counting remote nodes also requires the token's source node so it can be excluded.

Converting fan-out to bytes requires the hidden width, dtype and dispatcher's copy policy: one copy per expert and one copy per destination node give different traffic volumes.

###### Dropped assignments

With a capacity limit, measure drops from the router's final routing map. For N valid tokens and K surviving assignments:

*Calculation:*
```
dropped_fraction = 1 - K / (N * topk)
```

This counts lost token-expert assignments. A token may retain some of its experts. Exclude masked tokens and rows added for quantized GEMMs from the calculation. Use a live hook for this measurement, since the saved trace can skip records containing drops. The [`ExpertWatch`](https://gist.github.com/nmntz/5de952d686f66d7bce5bce8cba9d7139#file-expert_watch_hooks-py) helper captures this map; its setup and supported configurations appear under Shared and routed contributions.

###### Precision flips

The fp32 flip rate measures how often the selected expert set changes when the router calculation uses fp32. Both calculations must use the same forward's inputs, weights, biases and selection rules. Compare sets so that a change in ordering alone does not count as a flip.

For plain token-choice routing, [`install_fp32_flip_hook`](https://gist.github.com/nmntz/5de952d686f66d7bce5bce8cba9d7139#file-router_watch-py) performs this comparison on the live state. Attach it to the chosen MoE layer's router for one eager forward. Replace `moe_layer`, `model` and `tokens` with the objects in the training harness:

*Python:*
```
import torch
from scripts.router_watch import install_fp32_flip_hook

previous_tf32 = torch.backends.cuda.matmul.allow_tf32
handle = install_fp32_flip_hook(moe_layer.router, emit=print)
try:
    torch.backends.cuda.matmul.allow_tf32 = False
    output = model(tokens)
finally:
    handle.remove()
    torch.backends.cuda.matmul.allow_tf32 = previous_tf32
```

Disabling TF32 gives the reference matrix multiplication fp32 precision. The hook compares selected expert sets on a bounded sample of valid tokens. Its docstring lists the supported settings; routing transformations outside those settings are rejected. Run with CUDA graphs disabled and outside timed measurements.

Both calculations start from the live input's existing precision. The result isolates a routing disagreement at that input precision; assessing its effect on loss requires a separate experiment ([3.1](#s-3-1)).

For offline comparisons, retain the exact state and gating input of the captured forward, including jitter. The built-in weight dump snapshots each router on its first observed call, so it does not track subsequent updates to weights and balancing biases. Hidden states and recomputed logits are stored in bf16, and the snapshot omits the router's linear bias, if present. Reconstructions from these files should therefore be labeled approximate, with the capture step and missing state specified.

##### Expert activations

###### Capturing activations

Add `--save run/ --save-activations-interval 100` to capture inputs and outputs of supported linear modules, including grouped expert token counts. Each module's entry is overwritten on its next captured call, leaving the last captured micro-batch. The hook copies tensors to CPU on captured calls, so use a sparse interval and a short diagnostic run with CUDA graphs and activation recomputation disabled.

###### Per-expert output norms

The native dump's `experts.linear_fc2/output0` contains rows for the local experts. Split those rows using the module's `input1` token counts, convert to fp32, and calculate the L2 norm of each token's output vector. The mean of those norms describes the expert's output magnitude. Dividing each norm by the square root of the output width gives token RMS, useful for comparisons across widths.

The [`expert_watch.py`](https://gist.github.com/nmntz/5de952d686f66d7bce5bce8cba9d7139#file-expert_watch-py) reader performs these calculations. In an environment with PyTorch, run:

```
python3 scripts/expert_watch.py \
    --unpadded --expert-tp-size 1 activations.pth
```

These options assert that the captured rows contain no padding and expert tensor parallelism is 1. The reader reports each expert's token count, norm sum and mean norm. It also reports the largest and smallest mean norms relative to the median among experts that received tokens ([3.4](#s-3-4), [3.6](#s-3-6)).

An empty expert has no mean output norm, so the reader lists empty experts separately. The ratios are also undefined when the median is zero. Taking the norm of all an expert's rows concatenated would mix output magnitude with token count; averaging the per-token norms keeps those measurements separate.

The median used for these ratios covers the experts in one file. For a layer-wide comparison, join the EP shards before computing the median. Repeated observations can be merged by summing each expert's `sum_l2` and `rows`, then dividing to obtain its mean. With expert tensor parallelism above 1, first combine the partial output vectors; their individual norms cannot be added to recover the full vector's norm. Exclude padding rows from these calculations.

Grouped fc2 outputs can already include routing weights, depending on where the implementation applies them. A small norm can therefore reflect a small routing weight. Keep the point where weights are applied fixed across comparisons, and examine the mixture weights alongside the norms.

For live sampling, `ExpertWatch` reports the same per-expert norm statistics in its `routed_experts` output, including `local_max_to_median` and `local_min_to_median`. These ratios cover the local experts; join their statistics across EP ranks before computing a layer-wide median. The setup under Shared and routed contributions collects these statistics during the same forward.

###### Latent up-projection

To inspect the latent up-projection, read `fc2_latent_proj/output0` and compare its input and output RMS ([3.4](#s-3-4)). RMS accounts for the difference between latent width and model width. With `--moe-use-norm-before-up-proj`, also sample before the normalization to locate where the growth begins.

###### Shared and routed contributions

To compare the two branches, capture the shared output after its optional sigmoid gate and the routed output after unpermutation and combination. Include the latent up-projection when present. For each token, compute `norm(shared) / norm(routed)`, keeping zero denominators separate. This ratio compares branch magnitudes; the vectors can still reinforce or cancel one another when added.

The raw fc2 dumps occur earlier: shared fc2 is before the gate, and routed fc2 is before combination. For a live sample at the required points, attach [`ExpertWatch`](https://gist.github.com/nmntz/5de952d686f66d7bce5bce8cba9d7139#file-expert_watch_hooks-py) around one diagnostic forward:

*Python:*
```
from scripts.expert_watch_hooks import ExpertWatch

with ExpertWatch(moe_layer, emit=print):
    output = model(tokens)
```

This helper supports eager execution with the all-to-all dispatcher, tensor and expert-tensor parallel sizes of 1, and shared-expert overlap disabled. The sample must be unpadded, with quantization and expert padding disabled. Keep the hooks scoped to the diagnostic forward, as shown above, and save the JSON output per rank with the step and micro-batch identity.

For a standard MoE, the helper recovers the routed branch by subtracting the post-gate shared output from the total. The subtraction retains rounding error from the original addition, so a small routed contribution beside a large shared one calls for direct capture before addition. For a latent MoE, the helper captures the up-projection's output directly. Branch summaries include padding positions, which is why this comparison requires an unpadded sample.

To check the hooks on CPU before attaching them, run `python -m unittest scripts.test_router_watch scripts.test_expert_watch`.

##### Run health

###### Loss and gradient signals

Keep LM loss and gradient norm beside the router and expert measurements. The following flags add run-level signals:

- `--log-throughput`: training throughput.

- `--log-params-norm`: parameter norm.

- `--log-num-zeros-in-grad`: number of zero entries across model gradients.

- `--log-max-attention-logit`: largest attention logit; requires [Transformer Engine](https://github.com/NVIDIA/TransformerEngine) 2.9 or later.

To investigate expert-specific underflow ([3.7](#s-3-7)), count exact zeros in expert weight gradients after accumulation and before the optimizer update. Compare this expert-specific count with a BF16 run of the same configuration.

NaN checking is enabled by default. A detected NaN stops the step and invokes rerun handling ([3.6](#s-3-6)); `--no-check-for-nan-in-loss-and-grad` disables the check.

###### Timing and memory

Add `--timing-log-level 2 --timing-log-option all` for per-rank forward and backward timings. Group ranks by pipeline stage to locate a slow stage, including one holding MTP ([3.6](#s-3-6)). Then profile that stage using the tools in [3.7](#s-3-7).

Compare the same warmed-up interval across runs. For peak memory, reset CUDA peak statistics at the interval's start and read `torch.cuda.max_memory_allocated()` on each rank at its end. Take the maximum across ranks to report the highest peak allocated memory.

#### A.2 Debugging index

Chapter 3 went setting by setting, from a flag to what it does to the run. When a run misbehaves you travel the other way: you see a symptom on the dashboard and need the config behind it. This appendix is that reverse index, one row per symptom, each pointing back to the part of the post that explains it.

Before you blame a setting, though, rule out the stack itself with the two checks at the end of [2.5](#s-2-5).

##### Read the index

Each row carries a tag, the symptom with the first signal that moves, and the section to read. The tags sort runs by how they fail: `slow`, `OOM`, `blows up`, `learns badly`, and `won't start` for runs that stop before their first iteration. Find your tag, then the signal that moved first, and the row tells you where to go; the map in the introduction draws all of these rows but one, the `global_aux_loss` setting, which has no signal to start from.

*Collapsible:* Debugging index, 42 symptoms

| Tag | Symptom | Read |
| --- | --- | --- |
| `slow` | throughput drop | [3.3](#s-3-3), [3.7](#s-3-7) profiling |
| `slow` | half the single-node step is all-to-all | [3.3](#s-3-3) balance first, then [3.7](#s-3-7) overlap |
| `slow` | aux loss near 1 but one GPU slow | [3.3 Cost of imbalance](#s-3-3-cost-of-imbalance) (the aux loss equals 1 for flat router probabilities whatever the load; read MaxVio) |
| `slow`, `learns badly` | loss-free bias run still unbalanced after many steps | [3.3 Loss-free bias](#s-3-3-loss-free-bias) (fixed step lags; quantile balancing) |
| `slow`, `learns badly` | a few experts overloaded only in the first layers | [3.2](#s-3-2) hash layers, [3.5 Dense layers](#s-3-5-dense-layers) |
| `slow` | each token's all-to-all reaches every node | [3.7 Interconnect](#s-3-7-interconnect) and group-limited routing |
| `slow` | throughput drops after moving to more, smaller experts | [3.4](#s-3-4) count and size |
| `slow`, `OOM` | step much slower after turning on MTP, or OOM with more layers under pipeline parallelism | [3.6 MTP](#s-3-6-mtp) |
| `slow` | all-to-all exposed in the profile | [3.5 Block wiring](#s-3-5-block-wiring), [3.7 Overlap](#s-3-7-overlap) |
| `slow` | multi-node about 25x slower on our EP16 proxy and the NCCL log says 'Using network Socket' | [3.7 Interconnect](#s-3-7-interconnect) |
| `slow` | step slower after moving to `global_aux_loss` | [3.3 Scope](#s-3-3-scope) |
| `slow` | under quantile balancing, MaxVio per global batch low but per micro-batch high | [3.3 Quantile](#s-3-3-quantile) |
| `slow` | step slower with `--moe-latent-size` | [3.4 Latent MoE](#s-3-4-latent-moe), from the two d × ℓ projections and smaller expert GEMMs ([3.4](#s-3-4)); the throughput LatentMoE reports is serving, 12% lower at concurrency 1 |
| `slow` | slower inference after adding a shared expert on top of the routed top-k | [3.4 Shared experts](#s-3-4-shared-experts) |
| `slow` | full recompute still on | [3.7 Memory](#s-3-7-memory) |
| `slow` | TFLOP/s still short after balance, overlap and fusions | [3.7 Precision](#s-3-7-precision) |
| `OOM` | OOM on one rank | [3.3](#s-3-3) (imbalance), [3.7](#s-3-7) memory |
| `OOM` | peak memory looks fine but one rank OOMs | [3.7](#s-3-7) memory (Megatron logs data-parallel rank 0 only) |
| `blows up` | a NaN with nothing moving before it (grad norm, params norm, z-loss flat) | [3.6](#s-3-6) stability (no warning; the rerun on another GPU tells a faulty GPU from a reproducible NaN) |
| `blows up` | exit code 16 twice on one node | [3.6](#s-3-6) stability (the rerun needs a different GPU) |
| `blows up` | Muon run diverges in the first steps | [3.6](#s-3-6) optimizer (update scale, `--muon-extra-scale-factor`) |
| `blows up` | z-loss or router logits climbing before a spike | [3.1](#s-3-1) precision (a flat z-loss before a NaN points to [3.6](#s-3-6) stability instead) |
| `blows up` | expert output norms growing, or their max-to-median ratio climbing before a spike | [3.4](#s-3-4) activation (clamp) |
| `blows up` | exploding activations or a spike with a latent MoE | [3.4](#s-3-4) latent (norm before the up-projection) |
| `blows up` | grad norm and load-balancing loss jump a few iterations before a NaN | [3.6](#s-3-6) stability, [3.3](#s-3-3). Our 7B-A1B |
| `blows up` | loss spikes under Muon that resuming from a nearby checkpoint often avoids | [3.6](#s-3-6) optimizer (orthogonalization in bf16) |
| `learns badly` | RL reward stalls or collapses while the train-inference probability gap grows | 4 RL routing |
| `learns badly` | loss flat but MaxVio or an expert's output norm drifting from the layer median (collapse, dead or rogue expert) | [3.6](#s-3-6) stability, [3.3](#s-3-3) |
| `learns badly` | top-k weights all equal (flat gate) | [3.1](#s-3-1) sharpness |
| `learns badly` | dead experts with an aux loss on | [3.3 Aux loss](#s-3-3-aux-loss) (coefficient too small) |
| `learns badly` | `global_aux_loss` with more than 256 micro-batches per global batch | [3.3 Scope](#s-3-3-scope) Flags (bf16 counter) |
| `learns badly`, `blows up` | routing collapse or divergence in the first MoE layers | [3.5 Dense layers](#s-3-5-dense-layers) |
| `learns badly` | a capacity factor is set and the loss lags the dropless run | [3.7 Capacity and replicas](#s-3-7-capacity-and-replicas) (drops are not logged |
| `learns badly` | experts collapse layer by layer under Muon | [3.6](#s-3-6) optimizer |
| `learns badly` | with `--moe-router-pre-softmax` (top-k weights not renormalized), loss above a renormalized run | [3.1 Output scale](#s-3-1-output-scale) |
| `learns badly` | experts that do not specialize by domain | [3.3 Scope](#s-3-3-scope) |
| `learns badly` | LM loss rising with the aux coefficient | [3.3 Aux loss](#s-3-3-aux-loss) |
| `learns badly` | loss no longer improving as experts get smaller | [3.4 Count and size](#s-3-4-count-and-size) |
| `learns badly` | a model trained with expert choice routing differently at inference | [3.2 Who selects](#s-3-2-who-selects) |
| `learns badly` | an upcycled MoE that learns slowly after its head start | [3.6 Upcycling](#s-3-6-upcycling) |
| `won't start` | `--moe-use-upcycling` fails with "unexpected keyword argument 'model'" or a missing `pre_mlp_layernorm` key | [3.6](#s-3-6) upcycling (two upstream bugs) |
| `won't start` | assert about full recomputation after turning on `--overlap-moe-expert-parallel-comm` | [3.7](#s-3-7) overlap and memory |

The signal matters more than the symptom, because the same symptom can have causes in different parts. Before each of our NaNs, the signal we were watching (the grad norm, the params norm or the z-loss) stayed flat, and the one we traced was born in the backward pass of the grouped expert GEMM. For such a NaN, Megatron's rerun on another GPU tells a faulty GPU from a NaN that the data or the model really produced ([3.6 Stability](#s-3-6-stability)). A slow step with an aux loss near 1 sends you to MaxVio instead: [Megatron](https://github.com/NVIDIA/Megatron-LM)'s aux loss [equals 1](https://github.com/NVIDIA/Megatron-LM/blob/d6316eb45bf1bfbb6f1f848c0b56e55166564d80/megatron/core/transformer/moe/moe_utils.py#L147-L150) whenever the router's probabilities are flat, whatever the load, so a single overloaded GPU can hide behind it ([3.3 Cost of imbalance](#s-3-3-cost-of-imbalance)).

### References

1. `ref-2605.27605` Julien Abadji, Marah Abdin, Connor Adams, Eric Alcaide, Mustafa Altun et al. (2026). [Laguna M.1/XS.2 Technical Report](https://arxiv.org/abs/2605.27605). arXiv:2605.27605.

2. `ref-2604.12163` Chandan Akiti, Ajay Modukuri, Murali Nandan Nagarapu, Gunavardhan Akiti, Haozhe Liu (2026). [Nucleus-Image: Sparse MoE for Image Generation](https://arxiv.org/abs/2604.12163). arXiv:2604.12163.

3. `ref-2404.05019` Weilin Cai, Juyong Jiang, Le Qin, Junwei Cui, Sunghun Kim et al. (2024). [Shortcut-connected Expert Parallelism for Accelerating Mixture-of-Experts](https://arxiv.org/abs/2404.05019). arXiv:2404.05019.

4. `ref-doc-4` Jonathan Chang. [Causal Routing Bias for Aux-Loss-Free MoE Training](https://jonathanc.net/blog/causal-routing-bias). blog.

5. `ref-2605.27358` Yanbei Chen, Hanxian Huang, Ernie Chang, Jacob Szwejbka, Digant Desai et al. (2026). [MobileMoE: Scaling On-Device Mixture of Experts](https://arxiv.org/abs/2605.27358). arXiv:2605.27358.

6. `ref-2609.04575` Xing Chen, Hengshuai Yao (2026). [Training-Free Halving of Activated Experts in Fine-Grained Mixture-of-Experts Models](https://arxiv.org/abs/2609.04575). arXiv:2609.04575.

7. `ref-2204.09179` Zewen Chi, Li Dong, Shaohan Huang, Damai Dai, Shuming Ma et al. (2022). [On the Representation Collapse of Sparse Mixture of Experts](https://arxiv.org/abs/2204.09179). arXiv:2204.09179.

8. `ref-2202.01169` Aidan Clark, Diego de las Casas, Aurelia Guy, Arthur Mensch, Michela Paganini et al. (2022). [Unified Scaling Laws for Routed Language Models](https://arxiv.org/abs/2202.01169). arXiv:2202.01169.

9. `ref-2602.04870` Chenwei Cui, Rockwell Jackson, Benjamin Joseph Herrera, Ana María Tárano, Hannah Kerner (2026). [Multi-Head LatentMoE and Head Parallel: Communication-Efficient and Deterministic MoE Parallelism](https://arxiv.org/abs/2602.04870). arXiv:2602.04870.

10. `ref-2401.06066` Damai Dai, Chengqi Deng, Chenggang Zhao, R. X. Xu, Huazuo Gao et al. (2024). [DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models](https://arxiv.org/abs/2401.06066). arXiv:2401.06066.

11. `ref-doc-1` DeepSeek-AI. [DeepSeek V4.1 Flash 大规模推理部署实践 (the DeepInfer release post)](https://zhuanlan.zhihu.com/p/2095560295930508953). Zhihu.

12. `ref-doc-2` DeepSeek-AI. [DeepSeek V4.1 Flash Inference Deployment Q&A](https://github.com/deepseek-ai/DeepInfer/blob/main/doc/inference_deployment_qa.md). GitHub, deepseek-ai/DeepInfer.

13. `ref-doc-3` DeepSeek-AI. [DeepInfer](https://github.com/deepseek-ai/DeepInfer). GitHub.

14. `ref-2405.04434` DeepSeek-AI, Aixin Liu, Bei Feng, Bin Wang, Bingxuan Wang et al. (2024). [DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model](https://arxiv.org/abs/2405.04434). arXiv:2405.04434.

15. `ref-2412.19437` DeepSeek-AI, Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang et al. (2024). [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437). arXiv:2412.19437.

16. `ref-2606.19348` DeepSeek-AI, Anyi Xu, Bangcai Lin, Bing Xue, Bingxuan Wang et al. (2026). [DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence](https://arxiv.org/abs/2606.19348). arXiv:2606.19348.

17. `ref-2609.19969` DeepSeek-AI, Anyi Xu, B. Li, Bangcai Lin, Bing Xue et al. (2026). [DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression](https://arxiv.org/abs/2609.19969). arXiv:2609.19969.

18. `ref-2511.11505` Yonatan Dukler, Guihong Li, Deval Shah, Jiang Liu, Vikram Appia et al. (2025). [FarSkip-Collective: Unhobbling Blocking Communication in Mixture of Experts Models](https://arxiv.org/abs/2511.11505). arXiv:2511.11505.

19. `ref-2601.18089` Venmugil Elango, Nidhi Bhatia, Roger Waleffe, Rasoul Shafipour, Tomer Asida et al. (2026). [LatentMoE: Toward Optimal Accuracy per FLOP and Parameter in Mixture of Experts](https://arxiv.org/abs/2601.18089). arXiv:2601.18089.

20. `ref-doc-0` Hugging Face (2025). [The Smol Training Playbook](https://huggingfacetb-smol-training-playbook.hf.space/).

21. `ref-2101.03961` William Fedus, Barret Zoph, Noam Shazeer (2021). [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://arxiv.org/abs/2101.03961). arXiv:2101.03961.

22. `ref-2211.15841` Trevor Gale, Deepak Narayanan, Cliff Young, Matei Zaharia (2022). [MegaBlocks: Efficient Sparse Training with Mixture-of-Experts](https://arxiv.org/abs/2211.15841). arXiv:2211.15841.

23. `ref-2602.15763` GLM-5-Team, Aohan Zeng, Xin Lv, Zhenyu Hou, Zhengxiao Du et al. (2026). [GLM-5: from Vibe Coding to Agentic Engineering](https://arxiv.org/abs/2602.15763). arXiv:2602.15763.

24. `ref-2509.21892` Naibin Gu, Zhenyu Zhang, Yuchen Feng, Yilong Chen, Peng Fu et al. (2025). [Elastic MoE: Unlocking the Inference-Time Scalability of Mixture-of-Experts](https://arxiv.org/abs/2509.21892). arXiv:2509.21892.

25. `ref-2609.13058` Hongyi He, Zhenghao Lin, Xiao Liu, Peng Cheng, Yan Lu et al. (2026). [Expert-Space Exploration in MoE Reinforcement Learning](https://arxiv.org/abs/2609.13058). arXiv:2609.13058.

26. `ref-2203.15556` Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai et al. (2022). [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556). arXiv:2203.15556.

27. `ref-2512.16248` Qingguo Hu, Zhenghao Lin, Ziyue Yang, Yucheng Ding, Xiao Liu et al. (2025). [Sigma-MoE-Tiny Technical Report](https://arxiv.org/abs/2512.16248). arXiv:2512.16248.

28. `ref-2602.10604` Ailin Huang, Ang Li, Aobo Kong, Bin Wang, Binxing Jiao et al. (2026). [Step 3.5 Flash: Open Frontier-Level Intelligence with 11B Active Parameters](https://arxiv.org/abs/2602.10604). arXiv:2602.10604.

29. `ref-2605.25704` Peijie Jiang, Yuqi Feng, Cunyin Peng, Qian Zhao, Jia Liu et al. (2026). [PowLU: An Activation Function for Stable Pre-Training of LLMs](https://arxiv.org/abs/2605.25704). arXiv:2605.25704.

30. `ref-2609.39137` Peng Jin, Zihan Qiu, Zekun Wang, Bo Zheng, Yang Xu et al. (2026). [ID Balancing: Stable Training of Extremely Sparse MoE via PID-Based Load Control](https://arxiv.org/abs/2609.39137). arXiv:2609.39137.

31. `ref-2605.31268` Marko Kojic, Ivan Bondyrev, Aral de Moor, Joseph Shtok, Petr Borovlev et al. (2026). [Mellum2 Technical Report](https://arxiv.org/abs/2605.31268). arXiv:2605.31268.

32. `ref-2212.05055` Aran Komatsuzaki, Joan Puigcerver, James Lee-Thorp, Carlos Riquelme Ruiz, Basil Mustafa et al. (2022). [Sparse Upcycling: Training Mixture-of-Experts from Dense Checkpoints](https://arxiv.org/abs/2212.05055). arXiv:2212.05055.

33. `ref-2506.02890` Jakub Krajewski, Marcin Chochowski, Daniel Korzekwa (2025). [Scaling Fine-Grained MoE Beyond 50B Parameters: Empirical Evaluation and Practical Insights](https://arxiv.org/abs/2506.02890). arXiv:2506.02890.

34. `ref-doc-12` AWS Labs. [awsome-distributed-ai, NCCL test recipes](https://github.com/awslabs/awsome-distributed-ai/tree/main/micro-benchmarks/nccl-tests). GitHub.

35. `ref-2605.18106` Tim Tsz-Kit Lau, Weijie Su (2026). [Symmetry-Compatible Principle for Optimizer Design: Embeddings, LM Heads, SwiGLU MLPs, and MoE Routers](https://arxiv.org/abs/2605.18106). arXiv:2605.18106.

36. `ref-2605.11689` Margaret Li, Sneha Kudugunta, Danielle Rothermel, Luke Zettlemoyer (2026). [Slicing and Dicing: Configuring Optimal Mixtures of Experts](https://arxiv.org/abs/2605.11689). arXiv:2605.11689.

37. `ref-2601.08215` Seng Pei Liew, Kenta Shinzato, Yuyang Dong (2026). [Towards Principled Design of Mixture-of-Experts Language Models under Memory and Inference Constraints](https://arxiv.org/abs/2601.08215). arXiv:2601.08215.

38. `ref-2608.09119` Junghwan Lim, Joon Son Chung, Sungmin Lee, Wai Ting Cheung, Gihun Cho et al. (2026). [Motif 3: Technical Report](https://arxiv.org/abs/2608.09119). arXiv:2608.09119.

39. `ref-2502.16982` Jingyuan Liu, Jianlin Su, Xingcheng Yao, Zhejun Jiang, Guokun Lai et al. (2025). [Muon is Scalable for LLM Training](https://arxiv.org/abs/2502.16982). arXiv:2502.16982.

40. `ref-2609.00791` Jiang Liu, Sudhanshu Ranjan, Prakamya Mishra, Yonatan Dukler, Gowtham Ramesh et al. (2026). [Instella-MoE Technical Report](https://arxiv.org/abs/2609.00791). arXiv:2609.00791.

41. `ref-2510.11370` Wenhan Ma, Hailin Zhang, Liang Zhao, Yifan Song, Yudong Wang et al. (2025). [Stabilizing MoE Reinforcement Learning by Aligning Training and Inference Routers](https://arxiv.org/abs/2510.11370). arXiv:2510.11370.

42. `ref-2409.02060` Niklas Muennighoff, Luca Soldaini, Dirk Groeneveld, Kyle Lo, Jacob Morrison et al. (2024). [OLMoE: Open Mixture-of-Experts Language Models](https://arxiv.org/abs/2409.02060). arXiv:2409.02060.

43. `ref-2609.28053` Pit Neitemeier, Jiaze Li, Alessio Serra, Philipp Scholl, Sohir Maskey (2026). [Exact Quantile Balancing and Load-Error Injection for Mixture-of-Experts](https://arxiv.org/abs/2609.28053). arXiv:2609.28053.

44. `ref-doc-10` NVIDIA. [enroot](https://github.com/NVIDIA/enroot). GitHub.

45. `ref-doc-11` NVIDIA. [nccl-tests](https://github.com/NVIDIA/nccl-tests). GitHub.

46. `ref-doc-6` NVIDIA. [Megatron-LM PR #1913, feat(moe): Fine-grained activation offloading](https://github.com/NVIDIA/Megatron-LM/pull/1913). GitHub.

47. `ref-doc-7` NVIDIA. [DCGM Diagnostics](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html). DCGM documentation.

48. `ref-doc-9` NVIDIA. [pyxis](https://github.com/NVIDIA/pyxis). GitHub.

49. `ref-2509.25149` NVIDIA, Felix Abecassis, Anjulie Agrusa, Dong Ahn, Jonah Alben et al. (2025). [Pretraining Large Language Models with NVFP4](https://arxiv.org/abs/2509.25149). arXiv:2509.25149.

50. `ref-2604.12374` NVIDIA, Aakshita Chandiramani, Aaron Blakeman, Abdullahi Olaoye, Abhibha Gupta et al. (2026). [Nemotron 3 Super: Open, Efficient Mixture-of-Experts Hybrid Mamba-Transformer Model for Agentic Reasoning](https://arxiv.org/abs/2604.12374). arXiv:2604.12374.

51. `ref-2606.15007` NVIDIA, Aaron Blakeman, Aaron Thomas, Aastha Jhunjhunwala, Abhibha Gupta et al. (2026). [Nemotron 3 Ultra: Open, Efficient Mixture-of-Experts Hybrid Mamba-Transformer Model for Agentic Reasoning](https://arxiv.org/abs/2606.15007). arXiv:2606.15007.

52. `ref-2508.10925` OpenAI, Sandhini Agarwal, Lama Ahmad, Jason Ai, Sam Altman et al. (2025). [gpt-oss-120b & gpt-oss-20b Model Card](https://arxiv.org/abs/2508.10925). arXiv:2508.10925.

53. `ref-2601.07022` Sungrae Park, Sanghoon Kim, Jungho Cho, Gyoungjin Gim, Dawoon Jung et al. (2026). [Solar Open Technical Report](https://arxiv.org/abs/2601.07022). arXiv:2601.07022.

54. `ref-2501.11873` Zihan Qiu, Zeyu Huang, Bo Zheng, Kaiyue Wen, Zekun Wang et al. (2025). [Demons in the Detail: On Implementing Load Balancing Loss for Training Specialized Mixture-of-Expert Models](https://arxiv.org/abs/2501.11873). arXiv:2501.11873.

55. `ref-2608.04502` Chengyu Qiu, Xiao Fu, Fengcun Li, Yulei Qian, Yuchen Xie et al. (2026). [AFD-Ledger: Deployment Provisioning for Attention--FFN Disaggregation](https://arxiv.org/abs/2608.04502). arXiv:2608.04502.

56. `ref-2608.30320` Zihan Qiu, Zekun Wang, Xiao Li, Yanpeng Li, Yang Xu et al. (2026). [On the Design of Qwen3.8-Next Architecture: Evaluation, Efficiency, and Training Stability](https://arxiv.org/abs/2608.30320). arXiv:2608.30320.

57. `ref-2106.04426` Stephen Roller, Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston (2021). [Hash Layers For Large Sparse Models](https://arxiv.org/abs/2106.04426). arXiv:2106.04426.

58. `ref-2608.10605` Soumajyoti Sarkar, Yuxin Tang, Sheng Zha (2026). [Compute-Optimal Is Not Cluster-Optimal: Systems-Aware Scaling for Sparse Mixture-of-Experts](https://arxiv.org/abs/2608.10605). arXiv:2608.10605.

59. `ref-1701.06538` Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le et al. (2017). [Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://arxiv.org/abs/1701.06538). arXiv:1701.06538.

60. `ref-doc-8` StepFun. [Inside Step 5 Preview](https://platform.stepfun.ai/blog/inside-step-5-preview). blog.

61. `ref-2507.19427` StepFun, Bin Wang, Bojun Wang, Changyi Wan, Guanzhe Huang et al. (2025). [Step-3 is Large yet Affordable: Model-system Co-design for Cost-effective Decoding](https://arxiv.org/abs/2507.19427). arXiv:2507.19427.

62. `ref-2409.12210` Manxi Sun, Wei Liu, Jian Luan, Pengzhi Gao, Bin Wang (2024). [Mixture of Diverse Size Experts](https://arxiv.org/abs/2409.12210). arXiv:2409.12210.

63. `ref-2603.11535` Hanchi Sun, Yixin Liu, Yonghui Wu, Lichao Sun (2026). [Expert Threshold Routing for Autoregressive Language Modeling with Dynamic Computation Allocation and Load Balancing](https://arxiv.org/abs/2603.11535). arXiv:2603.11535.

64. `ref-2505.04519` Yehui Tang, Yichun Yin, Yaoyuan Wang, Hang Zhou, Yu Pan et al. (2025). [Pangu Ultra MoE: How to Train Your Big MoE on Ascend NPUs](https://arxiv.org/abs/2505.04519). arXiv:2505.04519.

65. `ref-2505.21411` Yehui Tang, Xiaosong Li, Fangcheng Liu, Wei Guo, Hang Zhou et al. (2025). [Pangu Pro MoE: Mixture of Grouped Experts for Efficient Sparsity](https://arxiv.org/abs/2505.21411). arXiv:2505.21411.

66. `ref-doc-5` Kimi Team. [Kimi K3 tech report](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf). GitHub, MoonshotAI/Kimi-K3.

67. `ref-2509.01322` Meituan LongCat Team, Bayan, Bei Li, Bingye Lei, Bo Wang et al. (2025). [LongCat-Flash Technical Report](https://arxiv.org/abs/2509.01322). arXiv:2509.01322.

68. `ref-2510.22115` Ling Team, Ang Li, Ben Liu, Binbin Hu, Bing Li et al. (2025). [Every Activation Boosted: Scaling General Reasoner to 1 Trillion Open Language Foundation](https://arxiv.org/abs/2510.22115). arXiv:2510.22115.

69. `ref-2607.24653` Kimi Team, Tongtong Bai, Yifan Bai, Yiping Bao, M. C. et al. (2026). [Kimi K3: Open Frontier Intelligence](https://arxiv.org/abs/2607.24653). arXiv:2607.24653.

70. `ref-2610.11959` Xiaomi LLM-Core Team, Zongming Qiao, Ziyue Hua, Zirui Ou, Zihao Yue et al. (2026). [MiMo-V2.6: Scaling Reinforcement Learning Towards Self-Improvement](https://arxiv.org/abs/2610.11959). arXiv:2610.11959.

71. `ref-2507.17702` Changxin Tian, Kunlong Chen, Jia Liu, Ziqi Liu, Zhiqiang Zhang et al. (2025). [Towards Greater Leverage: Scaling Laws for Efficient Mixture-of-Experts Language Models](https://arxiv.org/abs/2507.17702). arXiv:2507.17702.

72. `ref-2412.09952` Aditya Vavre, Ethan He, Dennis Liu, Zijie Yan, June Yang et al. (2024). [Llama 3 Meets MoE: Efficient Upcycling](https://arxiv.org/abs/2412.09952). arXiv:2412.09952.

73. `ref-2408.10681` An Wang, Xingwu Sun, Ruobing Xie, Shuaipeng Li, Jiaqi Zhu et al. (2024). [HMoE: Heterogeneous Mixture of Experts for Language Modeling](https://arxiv.org/abs/2408.10681). arXiv:2408.10681.

74. `ref-2408.15664` Lean Wang, Huazuo Gao, Chenggang Zhao, Xu Sun, Damai Dai (2024). [Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts](https://arxiv.org/abs/2408.15664). arXiv:2408.15664.

75. `ref-2602.04705` Haifeng Wang, Hua Wu, Tian Wu, Yu Sun, Jing Liu et al. (2026). [ERNIE 5.0 Technical Report](https://arxiv.org/abs/2602.04705). arXiv:2602.04705.

76. `ref-2406.06563` Tianwen Wei, Bo Zhu, Liang Zhao, Cheng Cheng, Biye Li et al. (2024). [Skywork-MoE: A Deep Dive into Training Techniques for Mixture-of-Experts Language Models](https://arxiv.org/abs/2406.06563). arXiv:2406.06563.

77. `ref-2508.07785` Haoyuan Wu, Haoxing Chen, Xiaodong Chen, Zhanchao Zhou, Tieyuan Chen et al. (2025). [Grove MoE: Towards Efficient and Superior MoE LLMs with Adjugate Experts](https://arxiv.org/abs/2508.07785). arXiv:2508.07785.

78. `ref-2608.27874` Weicheng Xue, Bingqiang Wang, Li Yuan, Huihui Zhou, Yonghong Tian (2026). [TerraceMoE: A Cost Model for Hierarchical MoE All-to-All Communication](https://arxiv.org/abs/2608.27874). arXiv:2608.27874.

79. `ref-2603.07685` Zijie Yan, Hongxiao Bai, Xin Yao, Dennis Liu, Tong Liu et al. (2026). [Scalable Training of Mixture-of-Experts Models with Megatron Core](https://arxiv.org/abs/2603.07685). arXiv:2603.07685.

80. `ref-2505.09388` An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui et al. (2025). [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388). arXiv:2505.09388.

81. `ref-2601.14327` YuanLab.ai, Shawn Wu, Jiangang Luo, Darcy Chen, Sean Wang et al. (2026). [Yuan3.0 Ultra: A Trillion-Parameter Enterprise-Oriented MoE LLM](https://arxiv.org/abs/2601.14327). arXiv:2601.14327.

82. `ref-2603.02731` Wuyue Zhang, Chongdong Huang, Chunbo You, Cheng Gu, Fengjuan Wang et al. (2026). [Practical FP4 Training for Large-Scale MoE Models on Hopper GPUs](https://arxiv.org/abs/2603.02731). arXiv:2603.02731.

83. `ref-2507.18071` Chujie Zheng, Shixuan Liu, Mingze Li, Xiong-Hui Chen, Bowen Yu et al. (2025). [Group Sequence Policy Optimization](https://arxiv.org/abs/2507.18071). arXiv:2507.18071.

84. `ref-2512.01374` Chujie Zheng, Kai Dang, Bowen Yu, Mingze Li, Huiqiang Jiang et al. (2025). [Stabilizing Reinforcement Learning with LLMs: Formulation and Practices](https://arxiv.org/abs/2512.01374). arXiv:2512.01374.

85. `ref-2202.09368` Yanqi Zhou, Tao Lei, Hanxiao Liu, Nan Du, Yanping Huang et al. (2022). [Mixture-of-Experts with Expert Choice Routing](https://arxiv.org/abs/2202.09368). arXiv:2202.09368.

86. `ref-2504.02263` Ruidong Zhu, Ziheng Jiang, Chao Jin, Peng Wu, Cesar A. Stuardo et al. (2025). [MegaScale-Infer: Serving Mixture-of-Experts at Scale with Disaggregated Expert Parallelism](https://arxiv.org/abs/2504.02263). arXiv:2504.02263.

87. `ref-2607.15810` Zhengyang Zhuge, Hao Yu, Xin Wang, Zheng Li, Yizhong Cao et al. (2026). [QUADS: Stabilizing NVFP4 Reinforcement Learning for MoE via QUantization-error Alignment across Dual Sides](https://arxiv.org/abs/2607.15810). arXiv:2607.15810.

88. `ref-2411.03884` Zhijian Zhuo, Ya Wang, Yutao Zeng, Xiaoqing Li, Xun Zhou et al. (2024). [Polynomial Composition Activations: Unleashing the Dynamics of Large Language Models](https://arxiv.org/abs/2411.03884). arXiv:2411.03884.

89. `ref-2202.08906` Barret Zoph, Irwan Bello, Sameer Kumar, Nan Du, Yanping Huang et al. (2022). [ST-MoE: Designing Stable and Transferable Sparse Expert Models](https://arxiv.org/abs/2202.08906). arXiv:2202.08906.

#### Code, configs and data

1. `ref-src-cfg-moe-every` An MoE in every layer, [Qwen3-30B-A3B](https://huggingface.co/Qwen/Qwen3-30B-A3B/blob/ad44e777bcd18fa416d9da3bd8f70d33ebb85d39/config.json).

2. `ref-src-trinity-centered` Arcee AI, 2026, *Arcee Trinity Large Technical Report*, arXiv:2602.17004, §2.3.

3. `ref-src-aa-open-top` Artificial Analysis Intelligence Index v5.0.1, [open-weights models](https://artificialanalysis.ai/models/open-source).

4. `ref-src-engram-s23` Cheng et al., 2026, *Conditional Memory via Scalable Lookup*, arXiv:2601.07372, §2.2 (suffix N-grams of canonical token ids, retrieved by hashing into embedding tables) and §2.3.

5. `ref-src-lexi-gate` Chitty-Venkata, Madireddy, Emani and Vishwanath, 2025, *LExI: Layer-Adaptive Active Experts for Efficient MoE Model Inference*, arXiv:2509.02753.

6. `ref-src-parallel-block` [`CohereLabs/North-Mini-Code-1.0`](https://huggingface.co/CohereLabs/North-Mini-Code-1.0/blob/d11e61a842617a22dc328552fa5bb86231ee4f37/config.json).

7. `ref-src-datatrove-skip` datatrove, `src/datatrove/executor/base.py` [L30](https://github.com/huggingface/datatrove/blob/2c895af7a95010a96fa53e2dc77cc0ce92799e3f/src/datatrove/executor/base.py#L30).

8. `ref-src-v32-keep-routing` DeepSeek-AI, 2025, *DeepSeek-V3.2*, arXiv:2512.02556.

9. `ref-src-deepep-readme` DeepSeek-AI, DeepEP README at tag v1.2.1.

10. `ref-src-cfg-dsv3` DeepSeek-V3 [`config.json`](https://huggingface.co/deepseek-ai/DeepSeek-V3/blob/e815299b0bcbac849fa540c768ef21845365c9eb/config.json).

11. `ref-src-cfg-v4flash-rs` DeepSeek-V4-Flash [`config.json`](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/60d8d70770c6776ff598c94bb586a859a38244f1/config.json).

12. `ref-src-dsv4-gate-code` DeepSeek-V4-Pro Hub `inference/model.py`, `Gate` ([L546](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/b5968e9190ef611bbf34a7229255be88a0e937c1/inference/model.py#L546)).

13. `ref-src-hub-dsv4pro-route` DeepSeek-V4-Pro's own inference code, [`model.py#L556`](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/b5968e9190ef611bbf34a7229255be88a0e937c1/inference/model.py#L556) (hash routing when `layer_id < n_hash_layers`).

14. `ref-src-hub-v41-engram` DeepSeek-V4.1-Flash on the Hub (rev 314113f), [`inference/engram.py#L90`](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/314113f8a7dadb388215396ba5fbee2c610a04d6/inference/engram.py#L90).

15. `ref-src-hub-dsv41` DeepSeek-V4.1-Flash's own inference code, [`model.py#L811`](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/2cba9e42aa026125f3ed06c6d98c1db82f7ca027/inference/model.py#L811) (router GEMM in fp32, divided by `gate_temp`, 1.0 by default).

16. `ref-src-emo-init` EMO, 2026, arXiv:2605.13247, §3.3.

17. `ref-src-expup-copy` Expert Upcycling, 2026, arXiv:2604.19835, Definition 3.1.

18. `ref-src-expup-drop` Expert Upcycling, arXiv:2604.19835, App. D, Tables 9 and 11.

19. `ref-src-shape-glm53` GLM-5.3 publisher [`config.json`](https://huggingface.co/zai-org/GLM-5.3/blob/main/config.json).

20. `ref-src-grok2-parallel` Grok 2, [`config.json`](https://huggingface.co/xai-org/grok-2/blob/main/config.json).

21. `ref-src-grok2-softcap` Grok 2, [`config.json`](https://huggingface.co/xai-org/grok-2/blob/daf4395a80ad177386cfe39641b64fc12b1d70ed/config.json).

22. `ref-src-hf-jobs-hardware` `hf jobs hardware`.

23. `ref-src-cfg-swiglu` `hidden_act: silu` with gated experts in [DeepSeek-V3](https://huggingface.co/deepseek-ai/DeepSeek-V3/blob/e815299b0bcbac849fa540c768ef21845365c9eb/config.json).

24. `ref-src-lowbit-all-cfg` Hub config.json `quantization_config`, [`Qwen/Qwen3-30B-A3B-GPTQ-Int4`](https://huggingface.co/Qwen/Qwen3-30B-A3B-GPTQ-Int4/blob/9b534e4318b7ebc3c961a839f13eb18b1833f441/config.json).

25. `ref-src-lowbit-experts-cfg` Hub config.json `quantization_config`, [`Zyphra/ZAYA1-8B-MXFP4-Experts`](https://huggingface.co/Zyphra/ZAYA1-8B-MXFP4-Experts/blob/d8602cda89e0f5f8ff268593778f4f27c8cbfe65/config.json).

26. `ref-src-hub-gated` Hugging Face Hub API, [`api/models/meta-llama/Llama-3.2-1B`](https://huggingface.co/api/models/meta-llama/Llama-3.2-1B).

27. `ref-src-hf-jobs-pricing` Hugging Face, [Jobs, Pricing and Billing](https://huggingface.co/docs/hub/jobs-pricing).

28. `ref-src-hf-jobs-guide` Hugging Face, [Run and manage Jobs](https://huggingface.co/docs/huggingface_hub/en/guides/jobs).

29. `ref-src-interns1pro-s21` Intern-S1-Pro, 2026, *Intern-S1-Pro: Scientific Multimodal Foundation Model at Trillion Scale*, arXiv:2603.25040, §2.1 Group Routing.

30. `ref-src-cfg-k3` Kimi K3 [`config.json`](https://huggingface.co/moonshotai/Kimi-K3/blob/f831ab66814297da540d832a5235f8e904f29d06/config.json).

31. `ref-src-hub-kimi-k3` Kimi K3's repo code, [`modeling_kimi_linear.py#L707-L712`](https://huggingface.co/moonshotai/Kimi-K3/blob/f831ab66814297da540d832a5235f8e904f29d06/modeling_kimi_linear.py#L707-L712) (router GEMM in fp32, sigmoid).

32. `ref-src-hub-kimi-k3-route` Kimi K3's repo code, [`modeling_kimi_linear.py#L724`](https://huggingface.co/moonshotai/Kimi-K3/blob/f831ab66814297da540d832a5235f8e904f29d06/modeling_kimi_linear.py#L724).

33. `ref-src-k25-mask` Kimi Team, 2026, *Kimi K2.5: Visual Agentic Intelligence*, arXiv:2602.02276.

34. `ref-src-kimivl-bias` Kimi-VL-A3B-Instruct publisher [`config.json`](https://huggingface.co/moonshotai/Kimi-VL-A3B-Instruct/blob/main/config.json).

35. `ref-src-kexaone-peak` LG AI Research, 2026, *K-EXAONE 2.0 Technical Report*, arXiv:2608.04505, §2.2 Training stability.

36. `ref-src-kexaone-grow` LG AI Research, 2026, *K-EXAONE 2.0 Technical Report*, arXiv:2608.04505, §2.2.

37. `ref-src-longcat-ngram-f2` Liu et al. (Meituan LongCat), 2026, *Scaling Embeddings Outperforms Scaling Experts in Language Models*, arXiv:2601.21204, Fig. 2 and §3.2.1, 280M active parameters, 300B tokens.

38. `ref-src-flashlite-ngram` Liu et al. (Meituan LongCat), 2026, *Scaling Embeddings Outperforms Scaling Experts in Language Models*, arXiv:2601.21204, §6, [`config.json`](https://huggingface.co/meituan-longcat/LongCat-Flash-Lite/blob/b62b68827ead0b7fef3ba98b57f18484acaaec06/config.json).

39. `ref-src-shape-mimo26` MiMo-V2.6-Pro-RL publisher [`config.json`](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL/blob/main/config.json), text configuration.

40. `ref-src-hub-mimo26` MiMo-V2.6-Pro-RL's repo code, [`modeling_mimo_v2.py#L155`](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL/blob/73875d00b30a89ef8cc353a0b60b0e9f9561952d/modeling_mimo_v2.py#L155) (router GEMM in fp32).

41. `ref-src-cfg-mistral-large3` `mistralai/Mistral-Large-3-675B-Instruct-2512` [`params.json`](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512/blob/383ffea2c7d60dfd44ca960e8e691709d4fdb9cd/params.json).

42. `ref-src-cfg-mixtral` `mistralai/Mixtral-8x7B-v0.1` [`config.json`](https://huggingface.co/mistralai/Mixtral-8x7B-v0.1/blob/fc7ac94680e38d7348cfa806e51218e6273104b0/config.json).

43. `ref-src-dropup-r` Nakamura et al., 2025, *Drop-Upcycling*, arXiv:2502.19261, §5.

44. `ref-src-shape-nemotron-ultra` Nemotron 3 Ultra publisher [`config.json`](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4/blob/main/config.json).

45. `ref-src-nemorl-freeze` NVIDIA NeMo-RL at fb121a00, [`examples/nemo_gym/nemotron-3-super/stage1_rlvr.yaml#L59-L61`](https://github.com/NVIDIA-NeMo/RL/blob/fb121a00d6b49cffd59e9e13e6c92215008b948e/examples/nemo_gym/nemotron-3-super/stage1_rlvr.yaml#L59-L61) (`async_grpo: enabled: true`, `max_trajectory_age_steps: 1`).

46. `ref-src-cfg-granularity` Publisher configs (hidden size / routed expert width, experts / top-k), [`config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/config.json).

47. `ref-src-cfg-latent` Publisher configs, [`config.json`](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16/blob/2dc98e2afe4face0e4ce40972a915c45368bd34a/config.json).

48. `ref-src-torch-topk` PyTorch `torch.topk` documentation.

49. `ref-src-cfg-qwen3next` `Qwen/Qwen3-Next-80B-A3B-Instruct` [`config.json`](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct/blob/9c7f2fbe84465e40164a94cc16cd30b6999b0cc7/config.json).

50. `ref-src-cfg-qwen35` Qwen3.5-397B [`config.json`](https://huggingface.co/Qwen/Qwen3.5-397B-A17B/blob/8472618112abcbd45acbcdc58436aff4233c23f7/config.json).

51. `ref-src-shape-qwen38` Qwen3.8-2.4T-A95B publisher [`config.json`](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B/blob/main/config.json).

52. `ref-src-hub-q38-ngram` Qwen3.8-Flash-Next on the Hub (rev de4b8e4), [`modeling_qwen4_exp.py#L1262`](https://github.com/huggingface/transformers/blob/a672eb5f474b8b30173e9f96eab66adf292da635/src/transformers/models/qwen4_exp/modeling_qwen4_exp.py#L1262).

53. `ref-src-ckpt-bias-means` Released weights, one tensor range-read per layer from each safetensors file, [DeepSeek-V3-Base](https://huggingface.co/deepseek-ai/DeepSeek-V3-Base).

54. `ref-src-fp32-router-code` Router GEMM cast to fp32 in inference code, [`modeling_deepseek_v32.py#L512`](https://github.com/huggingface/transformers/blob/ff704ffd47d800e31b31f2f81a5a2952fb0fbf71/src/transformers/models/deepseek_v32/modeling_deepseek_v32.py#L512).

55. `ref-src-shape-step5` Step 5 Preview publisher [`config.json`](https://huggingface.co/stepfun-ai/Step-5-Preview-BF16/blob/main/config.json), text configuration.

56. `ref-src-hub-step5-router` Step-5-Preview on the Hub (`stepfun-ai/Step-5-Preview`, rev 364b3b0), [`inference/model.py#L2020-L2030`](https://huggingface.co/stepfun-ai/Step-5-Preview/blob/364b3b03fed2477aa0953fe855a2c4c8c48ee3cc/inference/model.py#L2020-L2030).

57. `ref-src-hub-step5-route` Step-5-Preview on the Hub (`stepfun-ai/Step-5-Preview`, rev 364b3b0), [`inference/model.py#L2021-L2025`](https://huggingface.co/stepfun-ai/Step-5-Preview/blob/364b3b03fed2477aa0953fe855a2c4c8c48ee3cc/inference/model.py#L2021-L2025).

58. `ref-src-su-qb` Su Jianlin, kexue.fm post 11619, "MoE环游记：6、最优分配促均衡".

59. `ref-src-su-k3` Su Jianlin, kexue.fm post 11848, "简单谈谈K3的MoE和Attention".

60. `ref-src-cfg-clamp10` `swiglu_limit: 10` in [`ai-sage/GigaChat3.5-432B-A28B`](https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B/blob/d10dcaeccb04ca3186fdfa3bb3874b4474e6b41b/config.json).

61. `ref-src-trackio-readme` Trackio [`README.md`](https://github.com/gradio-app/trackio/blob/4bef24c5fd2db622c41cce7c763be504116281a2/README.md) at 4bef24c.

62. `ref-src-tf-cohere2-moe` transformers `cohere2_moe` at main ff704ff, [`modeling_cohere2_moe.py#L150-L160`](https://github.com/huggingface/transformers/blob/ff704ffd47d800e31b31f2f81a5a2952fb0fbf71/src/transformers/models/cohere2_moe/modeling_cohere2_moe.py#L150-L160).

63. `ref-src-tf-gemma4` transformers `gemma4` at main ff704ff, `Gemma4TextRouter`, [`modeling_gemma4.py#L1323`](https://github.com/huggingface/transformers/blob/ff704ffd47d800e31b31f2f81a5a2952fb0fbf71/src/transformers/models/gemma4/modeling_gemma4.py#L1323-L1324).

64. `ref-src-tf-glm-moe-dsa` transformers `glm_moe_dsa` at main ff704ff, [`modeling_glm_moe_dsa.py#L485`](https://github.com/huggingface/transformers/blob/ff704ffd47d800e31b31f2f81a5a2952fb0fbf71/src/transformers/models/glm_moe_dsa/modeling_glm_moe_dsa.py#L485).

65. `ref-src-tf-inkling` transformers `inkling` at main ff704ff, [`modeling_inkling.py#L360`](https://github.com/huggingface/transformers/blob/ff704ffd47d800e31b31f2f81a5a2952fb0fbf71/src/transformers/models/inkling/modeling_inkling.py#L360).

66. `ref-src-hub-llama4-route` transformers `llama4` at main ff704ff, [`modeling_llama4.py#L146-L148`](https://github.com/huggingface/transformers/blob/ff704ffd47d800e31b31f2f81a5a2952fb0fbf71/src/transformers/models/llama4/modeling_llama4.py#L146-L148).

67. `ref-src-tf-llama4` transformers `llama4` at main ff704ff, [`modeling_llama4.py#L150`](https://github.com/huggingface/transformers/blob/ff704ffd47d800e31b31f2f81a5a2952fb0fbf71/src/transformers/models/llama4/modeling_llama4.py#L150).

68. `ref-src-hf-qwen3moe` transformers main at a96730c8, [`qwen3_moe/modeling_qwen3_moe.py#L257-L264`](https://github.com/huggingface/transformers/blob/a96730c8c97b8efbf35bbaf7f5da33ec99231a49/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py#L257-L264).

69. `ref-src-tf-qwen4-exp` transformers `qwen4_exp` at main ff704ff, [`modeling_qwen4_exp.py#L964`](https://github.com/huggingface/transformers/blob/ff704ffd47d800e31b31f2f81a5a2952fb0fbf71/src/transformers/models/qwen4_exp/modeling_qwen4_exp.py#L964).

70. `ref-src-tf-zaya` transformers `zaya` at main ff704ff, [`modeling_zaya.py#L538`](https://github.com/huggingface/transformers/blob/ff704ffd47d800e31b31f2f81a5a2952fb0fbf71/src/transformers/models/zaya/modeling_zaya.py#L538).

71. `ref-src-trl-is` TRL, `trl/trainer/grpo_config.py` at 3749f2a, [`importance_sampling_level`](https://github.com/huggingface/trl/blob/3749f2a59fdcd3b6435243faa44eedf2903bc30e/trl/trainer/grpo_config.py#L208-L213).

72. `ref-src-cfg-maverick` `unsloth/Llama-4-Maverick-17B-128E-Instruct` [`config.json`](https://huggingface.co/unsloth/Llama-4-Maverick-17B-128E-Instruct/blob/86c5ecb6f2fbddf604c60120125fb202e09f2556/config.json), `text_config`.

73. `ref-src-vllm-dbo` vLLM at 790be385, [`vllm/config/parallel.py#L275-L276`](https://github.com/vllm-project/vllm/blob/790be385c8a69f45ec9a7a85ef00836d1684060f/vllm/config/parallel.py#L275-L276).

74. `ref-src-ultraep-f11` Wei et al., 2026, *UltraEP*, arXiv:2606.04101, §8.2 and Fig. 11 (training, resumed at global batch 3,500 for 20 more).

75. `ref-src-dsvl2-bias` Wu et al., 2024, *DeepSeek-V*, arXiv:2412.10302, §2.

76. `ref-src-mimo-r3` Xiaomi, 2026, *MiMo-V2-Flash Technical Report*, arXiv:2601.02780.

77. `ref-src-cfg-glm45air` `zai-org/GLM-4.5-Air` [`config.json`](https://huggingface.co/zai-org/GLM-4.5-Air/blob/a24ceef6ce4f3536971efe9b778bdaa1bab18daa/config.json).

78. `ref-src-zaya1-adamw` Zyphra, 2026, *ZAYA1-8B Technical Report*, arXiv:2605.05365, §II-A2.

### Footnote key

Superscript numbers in the article are assigned by the page's script; each maps to the reference entry with the ID shown.

- <sup>1</sup> → `ref-src-aa-open-top`
- <sup>2</sup> → `ref-doc-0`
- <sup>3,4</sup> → `ref-doc-9` (cites: pyxis-readme enroot-readme)
- <sup>5</sup> → `ref-src-hf-jobs-pricing`
- <sup>6</sup> → `ref-src-hf-jobs-hardware`
- <sup>7</sup> → `ref-src-hf-jobs-guide`
- <sup>3</sup> → `ref-doc-9`
- <sup>8</sup> → `ref-doc-7`
- <sup>9</sup> → `ref-doc-12`
- <sup>10,9</sup> → `ref-doc-10` (cites: enroot-import aws-nccl-image)
- <sup>11</sup> → `ref-doc-11`
- <sup>4</sup> → `ref-doc-10`
- <sup>12</sup> → `ref-src-hub-gated`
- <sup>13</sup> → `ref-src-datatrove-skip`
- <sup>14</sup> → `ref-src-trackio-readme`
- <sup>15</sup> → `ref-2602.10604`
- <sup>16</sup> → `ref-src-hub-dsv41`
- <sup>17</sup> → `ref-src-tf-gemma4`
- <sup>18</sup> → `ref-src-tf-glm-moe-dsa`
- <sup>19</sup> → `ref-src-tf-inkling`
- <sup>20</sup> → `ref-src-hub-kimi-k3`
- <sup>21</sup> → `ref-doc-5`
- <sup>22</sup> → `ref-src-hub-mimo26`
- <sup>23</sup> → `ref-src-tf-cohere2-moe`
- <sup>24</sup> → `ref-src-tf-qwen4-exp`
- <sup>25</sup> → `ref-src-hub-step5-router`
- <sup>26</sup> → `ref-src-tf-zaya`
- <sup>27</sup> → `ref-2606.19348`
- <sup>28</sup> → `ref-2408.15664`
- <sup>29</sup> → `ref-2506.02890`
- <sup>30</sup> → `ref-src-cfg-dsv3`
- <sup>31</sup> → `ref-src-tf-llama4`
- <sup>32</sup> → `ref-2406.06563`
- <sup>33</sup> → `ref-src-grok2-softcap`
- <sup>34</sup> → `ref-2406.06563`
- <sup>35</sup> → `ref-2406.06563`
- <sup>36</sup> → `ref-2204.09179`
- <sup>37</sup> → `ref-src-torch-topk`
- <sup>38</sup> → `ref-2202.08906`
- <sup>39</sup> → `ref-src-fp32-router-code`
- <sup>40</sup> → `ref-2101.03961`
- <sup>41</sup> → `ref-2202.08906`
- <sup>42</sup> → `ref-2412.19437`
- <sup>43</sup> → `ref-2202.09368`
- <sup>44</sup> → `ref-src-hub-dsv4pro-route`
- <sup>45</sup> → `ref-src-hub-v41-engram`
- <sup>46</sup> → `ref-src-hub-llama4-route`
- <sup>47</sup> → `ref-src-hub-q38-ngram`
- <sup>48</sup> → `ref-src-hub-step5-route`
- <sup>49</sup> → `ref-2408.15664`
- <sup>50</sup> → `ref-2603.11535`
- <sup>51</sup> → `ref-2603.11535`
- <sup>52</sup> → `ref-2408.15664`
- <sup>53</sup> → `ref-2606.19348`
- <sup>54</sup> → `ref-src-dsv4-gate-code`
- <sup>55</sup> → `ref-2106.04426`
- <sup>56</sup> → `ref-src-engram-s23`
- <sup>57,58</sup> → `ref-2609.19969` (cites: dsv41-s242 dsv41-engram)
- <sup>59</sup> → `ref-src-cfg-v4flash-rs`
- <sup>60</sup> → `ref-2202.01169`
- <sup>61</sup> → `ref-2106.04426`
- <sup>62</sup> → `ref-2412.19437`
- <sup>63</sup> → `ref-2609.19969`
- <sup>64</sup> → `ref-2607.24653`
- <sup>65</sup> → `ref-2509.01322`
- <sup>66</sup> → `ref-2610.11959`
- <sup>67</sup> → `ref-2505.09388`
- <sup>68</sup> → `ref-src-hf-qwen3moe`
- <sup>69</sup> → `ref-2401.06066`
- <sup>70</sup> → `ref-2405.04434`
- <sup>71</sup> → `ref-doc-1`
- <sup>72,73</sup> → `ref-2601.14327` (cites: yuan3-t1 yuan3-l144)
- <sup>74</sup> → `ref-2608.09119`
- <sup>75</sup> → `ref-2408.15664`
- <sup>76</sup> → `ref-2408.15664`
- <sup>77</sup> → `ref-2512.16248`
- <sup>72</sup> → `ref-2601.14327`
- <sup>78</sup> → `ref-2501.11873`
- <sup>79</sup> → `ref-2501.11873`
- <sup>80,81</sup> → `ref-2501.11873` (cites: qiu-s42 qiu-t5)
- <sup>82</sup> → `ref-2405.04434`
- <sup>81</sup> → `ref-2501.11873`
- <sup>83</sup> → `ref-2412.19437`
- <sup>84</sup> → `ref-2605.11689`
- <sup>85</sup> → `ref-2605.11689`
- <sup>86</sup> → `ref-2408.15664`
- <sup>87</sup> → `ref-src-zaya1-adamw`
- <sup>88,89</sup> → `ref-2502.16982` (cites: moonlight-centered trinity-centered)
- <sup>90</sup> → `ref-src-ckpt-bias-means`
- <sup>91</sup> → `ref-doc-4`
- <sup>92,93</sup> → `ref-src-dsvl2-bias` (cites: dsvl2-bias kimivl-bias)
- <sup>94</sup> → `ref-2609.39137`
- <sup>95</sup> → `ref-src-su-qb`
- <sup>96</sup> → `ref-src-su-k3`
- <sup>97</sup> → `ref-2609.28053`
- <sup>98</sup> → `ref-2609.28053`
- <sup>99</sup> → `ref-2609.39137`
- <sup>100</sup> → `ref-2609.19969`
- <sup>101</sup> → `ref-src-shape-glm53`
- <sup>102</sup> → `ref-2607.24653`
- <sup>103</sup> → `ref-2509.01322`
- <sup>104</sup> → `ref-src-shape-mimo26`
- <sup>105</sup> → `ref-src-shape-nemotron-ultra`
- <sup>106</sup> → `ref-src-shape-qwen38`
- <sup>107</sup> → `ref-src-shape-step5`
- <sup>108</sup> → `ref-2601.08215`
- <sup>109</sup> → `ref-src-cfg-granularity`
- <sup>110</sup> → `ref-src-longcat-ngram-f2`
- <sup>111</sup> → `ref-src-flashlite-ngram`
- <sup>112</sup> → `ref-2203.15556`
- <sup>113</sup> → `ref-2608.10605`
- <sup>114</sup> → `ref-2602.10604`
- <sup>115</sup> → `ref-2601.18089`
- <sup>116</sup> → `ref-2601.18089`
- <sup>117</sup> → `ref-2602.04870`
- <sup>118</sup> → `ref-src-cfg-latent`
- <sup>119</sup> → `ref-2601.18089`
- <sup>120</sup> → `ref-2601.18089`
- <sup>121</sup> → `ref-src-cfg-k3`
- <sup>122</sup> → `ref-2401.06066`
- <sup>123</sup> → `ref-2401.06066`
- <sup>124</sup> → `ref-2505.09388`
- <sup>125</sup> → `ref-src-cfg-qwen3next`
- <sup>126</sup> → `ref-src-cfg-qwen35`
- <sup>127,128</sup> → `ref-2505.04519` (cites: pangu-ultra-f2 et-t8)
- <sup>129,130</sup> → `ref-2409.02060` (cites: olmoe-f6 slicing-shared)
- <sup>131</sup> → `ref-2605.31268`
- <sup>132</sup> → `ref-src-grok2-parallel`
- <sup>133,134</sup> → `ref-src-cfg-glm45air` (cites: cfg-glm45air cfg-mistral-large3)
- <sup>135,136,137</sup> → `ref-2602.15763` (cites: shared-glm53 shared-k3 shared-dsv41)
- <sup>138</sup> → `ref-2610.11959`
- <sup>139</sup> → `ref-2509.01322`
- <sup>140</sup> → `ref-2509.01322`
- <sup>141</sup> → `ref-2409.12210`
- <sup>142</sup> → `ref-src-cfg-mixtral`
- <sup>143</sup> → `ref-2509.01322`
- <sup>141,144</sup> → `ref-2409.12210` (cites: modse-f2 hmoe-3b)
- <sup>145</sup> → `ref-2605.11689`
- <sup>146</sup> → `ref-2508.07785`
- <sup>138,135,136</sup> → `ref-2610.11959` (cites: shared-mimo26 shared-glm53 shared-k3)
- <sup>147</sup> → `ref-src-cfg-swiglu`
- <sup>148</sup> → `ref-2605.25704`
- <sup>149</sup> → `ref-2605.25704`
- <sup>150</sup> → `ref-src-kexaone-peak`
- <sup>151</sup> → `ref-2411.03884`
- <sup>152</sup> → `ref-2608.09119`
- <sup>153</sup> → `ref-2607.24653`
- <sup>154</sup> → `ref-2609.19969`
- <sup>155</sup> → `ref-src-cfg-clamp10`
- <sup>156</sup> → `ref-2602.10604`
- <sup>107,154,153</sup> → `ref-src-shape-step5` (cites: step5-activation dsv41-activation k3-appb)
- <sup>157</sup> → `ref-2412.19437`
- <sup>158</sup> → `ref-2609.19969`
- <sup>159</sup> → `ref-2607.24653`
- <sup>160</sup> → `ref-src-cfg-maverick`
- <sup>161</sup> → `ref-2509.01322`
- <sup>162</sup> → `ref-src-cfg-moe-every`
- <sup>163</sup> → `ref-2412.19437`
- <sup>164</sup> → `ref-2507.17702`
- <sup>165</sup> → `ref-2401.06066`
- <sup>166</sup> → `ref-2507.17702`
- <sup>167</sup> → `ref-2604.12163`
- <sup>168</sup> → `ref-2601.07022`
- <sup>169</sup> → `ref-2602.04705`
- <sup>165,166</sup> → `ref-2401.06066` (cites: dsmoe-early ling-early)
- <sup>170</sup> → `ref-src-parallel-block`
- <sup>171</sup> → `ref-2509.01322`
- <sup>172</sup> → `ref-2404.05019`
- <sup>173</sup> → `ref-2404.05019`
- <sup>174</sup> → `ref-2509.01322`
- <sup>175,176</sup> → `ref-2609.00791` (cites: instella-t13 farskip-t3)
- <sup>177</sup> → `ref-2609.00791`
- <sup>178</sup> → `ref-2509.01322`
- <sup>179</sup> → `ref-1701.06538`
- <sup>180</sup> → `ref-2609.19969`
- <sup>181</sup> → `ref-2607.24653`
- <sup>182</sup> → `ref-2509.01322`
- <sup>183</sup> → `ref-2602.10604`
- <sup>184</sup> → `ref-2212.05055`
- <sup>185</sup> → `ref-2212.05055`
- <sup>186</sup> → `ref-2409.02060`
- <sup>187</sup> → `ref-2212.05055`
- <sup>188</sup> → `ref-src-expup-copy`
- <sup>189</sup> → `ref-src-kexaone-grow`
- <sup>190,191</sup> → `ref-src-expup-drop` (cites: expup-drop dropup-r)
- <sup>192</sup> → `ref-src-emo-init`
- <sup>186,187</sup> → `ref-2409.02060` (cites: olmoe-upcycle sparse-upcycle)
- <sup>193</sup> → `ref-2606.19348`
- <sup>194</sup> → `ref-2502.16982`
- <sup>195</sup> → `ref-2608.30320`
- <sup>196</sup> → `ref-2605.18106`
- <sup>197</sup> → `ref-2605.27605`
- <sup>198</sup> → `ref-2605.31268`
- <sup>199</sup> → `ref-2412.19437`
- <sup>200</sup> → `ref-2605.31268`
- <sup>201</sup> → `ref-2510.22115`
- <sup>163,183</sup> → `ref-2412.19437` (cites: train-dsv3 train-step35)
- <sup>202</sup> → `ref-2608.30320`
- <sup>203</sup> → `ref-2412.19437`
- <sup>204</sup> → `ref-2606.19348`
- <sup>205,21</sup> → `ref-2607.24653` (cites: systems-k3 k3-qat)
- <sup>206</sup> → `ref-src-hub-kimi-k3-route`
- <sup>178,207</sup> → `ref-2509.01322` (cites: longcat-overlap systems-longcat)
- <sup>208</sup> → `ref-2603.07685`
- <sup>209</sup> → `ref-2412.19437`
- <sup>210</sup> → `ref-doc-6`
- <sup>211</sup> → `ref-doc-6`
- <sup>212</sup> → `ref-2603.07685`
- <sup>213</sup> → `ref-2505.21411`
- <sup>214</sup> → `ref-src-interns1pro-s21`
- <sup>215,216</sup> → `ref-2412.19437` (cites: dsv3-s322 deepep-readme)
- <sup>217</sup> → `ref-2608.27874`
- <sup>218</sup> → `ref-2505.04519`
- <sup>219</sup> → `ref-2202.08906`
- <sup>220</sup> → `ref-2412.09952`
- <sup>221</sup> → `ref-src-ultraep-f11`
- <sup>222</sup> → `ref-2603.07685`
- <sup>223</sup> → `ref-2412.19437`
- <sup>224</sup> → `ref-2211.15841`
- <sup>225</sup> → `ref-2412.09952`
- <sup>226</sup> → `ref-2605.27358`
- <sup>227</sup> → `ref-2202.08906`
- <sup>228</sup> → `ref-2405.04434`
- <sup>229</sup> → `ref-2603.07685`
- <sup>230</sup> → `ref-2412.19437`
- <sup>231</sup> → `ref-2603.07685`
- <sup>232</sup> → `ref-2603.07685`
- <sup>233,234</sup> → `ref-2412.19437` (cites: dsv3-fp8-tiles ling-fp8)
- <sup>235</sup> → `ref-2603.07685`
- <sup>236</sup> → `ref-2412.19437`
- <sup>237</sup> → `ref-2412.19437`
- <sup>234</sup> → `ref-2510.22115`
- <sup>238</sup> → `ref-2604.12374`
- <sup>239</sup> → `ref-2606.15007`
- <sup>240</sup> → `ref-2509.25149`
- <sup>241</sup> → `ref-2603.02731`
- <sup>242</sup> → `ref-2604.12374`
- <sup>237,234</sup> → `ref-2412.19437` (cites: dsv3-fp8-val ling-fp8)
- <sup>243</sup> → `ref-2609.04575`
- <sup>244</sup> → `ref-src-lexi-gate`
- <sup>245</sup> → `ref-2609.04575`
- <sup>246</sup> → `ref-2609.04575`
- <sup>247</sup> → `ref-2609.04575`
- <sup>248</sup> → `ref-2509.21892`
- <sup>249</sup> → `ref-2609.04575`
- <sup>250</sup> → `ref-2508.10925`
- <sup>251</sup> → `ref-2606.19348`
- <sup>252</sup> → `ref-2602.15763`
- <sup>253</sup> → `ref-src-lowbit-experts-cfg`
- <sup>254</sup> → `ref-src-lowbit-all-cfg`
- <sup>255</sup> → `ref-doc-2`
- <sup>256</sup> → `ref-doc-2`
- <sup>257</sup> → `ref-doc-2`
- <sup>258</sup> → `ref-doc-2`
- <sup>259</sup> → `ref-doc-1`
- <sup>256,71</sup> → `ref-doc-2` (cites: deepinfer-qa-par deepinfer-eplb)
- <sup>260</sup> → `ref-2507.19427`
- <sup>261</sup> → `ref-2504.02263`
- <sup>262</sup> → `ref-2608.04502`
- <sup>263</sup> → `ref-src-vllm-dbo`
- <sup>264</sup> → `ref-2507.19427`
- <sup>265</sup> → `ref-2507.19427`
- <sup>266</sup> → `ref-2507.19427`
- <sup>267,268</sup> → `ref-2510.11370` (cites: r3-engines gspo-drift)
- <sup>267,269</sup> → `ref-2510.11370` (cites: r3-engines r3-mismatch)
- <sup>268</sup> → `ref-2507.18071`
- <sup>270</sup> → `ref-2510.11370`
- <sup>271,272,273</sup> → `ref-src-v32-keep-routing` (cites: v32-keep-routing mimo-r3 instella-r3)
- <sup>274,275</sup> → `ref-src-k25-mask` (cites: k25-mask mellum2-icepop)
- <sup>276</sup> → `ref-2510.11370`
- <sup>267</sup> → `ref-2510.11370`
- <sup>277</sup> → `ref-2512.01374`
- <sup>278</sup> → `ref-2609.13058`
- <sup>279</sup> → `ref-2510.11370`
- <sup>280</sup> → `ref-src-trl-is`
- <sup>281</sup> → `ref-doc-3`
- <sup>282</sup> → `ref-doc-8`
- <sup>283</sup> → `ref-src-nemorl-freeze`
- <sup>284</sup> → `ref-2607.15810`
