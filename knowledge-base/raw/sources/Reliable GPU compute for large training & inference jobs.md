---
title: "Reliable GPU compute for large training & inference jobs"
source: "https://netflixtechblog.com/reliable-gpu-compute-for-large-training-inference-jobs-d62b03a96d7a"
author:
  - "[[Netflix Technology Blog]]"
published: 2026-10-15
created: 2026-10-19
description: "Reliable GPU compute for large training & inference jobs How we detect failing GPUs and network fabric, remediate machines automatically, and let long-running jobs survive hardware loss. Authors …"
tags:
  - "clippings"
---
*How we detect failing GPUs and network fabric, remediate machines automatically, and let long-running jobs survive hardware loss.*

Authors: [Nick Rutigliano](https://www.linkedin.com/in/nick-rutigliano/), [Argha C](https://www.linkedin.com/in/argha-c/), [Samartha Chandrashekar](https://www.linkedin.com/in/samartha/)

Open Netflix, and the home screen is assembled for you: which rows appear, the order they appear in, the titles within them, and the artwork for each title are chosen by machine learning models trained on how hundreds of millions of members watch. Personalization is one of the most widely used things we build, and members feel it every time they open the app. Like a growing share of Netflix, it runs on GPUs, which train those models and increasingly serve them live.

Those GPUs have to stay healthy for that experience to hold up, and keeping them healthy is harder than it sounds. A single large training job can run for weeks across hundreds of GPUs spread over many machines. It runs as a gang: the ranks move in lockstep, exchanging data every step, so the job advances only as fast as its slowest participant and stops entirely if one participant dies. Every GPU, every high-speed network adapter, and every interconnect must keep working throughout the run. At the scale at which modern machine learning runs, individual GPUs and network links can fail during a run, so the underlying platform must be prepared for this and handle it without a person in the loop.

This post describes how we keep our GPU infrastructure healthy for training and inference. We cover how we detect failing hardware before and during jobs, how we automatically remediate a bad machine, and how we let a long job survive the loss of a machine. These training workloads run on our modern Kubernetes-native Compute platform.

## Why GPU reliability matters

Netflix aims to entertain the world, and machine learning has been part of how we do that for years, from the recommendations that help members find something to watch to the systems that help produce and promote titles. As generative AI advances, we are investing in it on both sides of the business: for members, through better recommendations and higher-quality promotional assets; and for storytelling, through creative tools for our production partners.

All of this runs on GPUs, for both training and inference, and GPU capacity is among the fastest-growing and most expensive parts of our infrastructure. That makes reliability a business concern on two fronts.

- Availability: a training run that loses a machine, or an inference service that cannot get healthy capacity, delays work that members and creators depend on.
- Cost efficiency: a GPU sitting idle behind a slow neighbor, or a whole machine pulled from the pool because one device is degraded, becomes capacity we paid for and are not using. Higher reliability and higher utilization mean more useful work per GPU, which is equivalent to spending less to do the same work.

Inference is a growing share of that GPU footprint as more of these AI features reach members, so the reliability and efficiency that matter for multi-week training runs increasingly matter for always-on serving too.

## Why basic health checks are not enough

We start from the baseline provided by the cloud provider. Cloud providers run instance status checks on virtual machines: a system status check for the underlying host’s power, network, and hardware reachability; an instance status check to verify that the operating system is up and reachable; and a check on attached storage. It emits scheduled maintenance events when it plans to retire or reboot a host, and it can automatically recover an instance that becomes impaired. We use all of these, and the maintenance events feed one of our own checks. They catch a machine that is down, unreachable, or slated for maintenance, and they stop at the instance level. They confirm the box is up and reachable. They do not verify that each GPU, its on-chip memory, its interconnect, and its network fabric are healthy enough to support distributed training.

The next step most teams take is a GPU-level check to confirm that the driver responds and that the GPUs are visible. That catches a dead or missing GPU, but misses the cases that take the most time.

- A GPU can answer a status query and still be faulty once a workload touches it. A fault in on-chip memory or in the firmware that manages the device can remain invisible until a job allocates memory or runs sustained compute, at which point the job fails or slows.
- A high-speed network adapter may be present but show fewer links than expected. Collective operations still run, at a fraction of the bandwidth, so the job does not crash. It crawls, and the cause is easy to miss.
- A check can fail in ways that leave a faulty machine looking healthy. The diagnostic tool can hang when the driver hangs, and a naive check that waits on it hangs too. A binary that the check depends on can go missing after a driver upgrade, causing the check to stop running and report nothing. A check that can silently stop running is worse than no check, because it gives false confidence while the machine keeps working.

Because a job runs as a gang, any one of these on any one machine can degrade or stop the whole job, and none of them shows up in an instance-level check or a driver-responds check. The health system has to assume the hardware can lie and the tools that inspect it can break.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*d15z8m06XjWnYeauK7iXfQ.png)

A machine can pass a basic check and still be faulty. Layered checks, timeouts, a fallback path, and checks that fail when a dependency is missing close these gaps.

## Our approach

We treat reliability as four layers, each catching what the layer below cannot:

**1/ Node and hardware health:** find bad GPUs, network adapters, interconnects, memory errors, and thermal issues, then taint or recycle the machine.

**2/ Scheduler and platform:** retry at the task & job level, validate a machine before it takes work, and drain & recycle machines safely.

**3/ Training loop:** checkpoint and use elastic workers so a job survives losing a machine.

**4/ Observability:** metrics, service-level objectives, and failure attribution across the other three.

The first two layers keep hardware problems away from jobs. The third accepts that some loss is unavoidable and makes it cheap. The fourth tells us whether the first three are working.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*2lLAu7fFc5rqqiWY2QAbhA.png)

Four layers: Each catches what the layer below cannot.

## How the health checks work

Checks run in two tiers. Device-level checks look at each GPU. A node-level agent, built on the open-source Kubernetes [node-problem-detector](https://github.com/kubernetes/node-problem-detector), runs on every GPU machine every 30 seconds and turns check results into conditions on the Kubernetes node, the same mechanism Kubernetes uses to mark a node NotReady. Controllers watch those conditions and decide whether the machine can take on work.

GPU device checks are built on NVIDIA’s [DCGM](https://developer.nvidia.com/dcgm) for driver-reported error codes, uncorrectable memory errors, interconnect integrity, and thermal state, and networking adapter checks inspect the host state for the count and link state of the [Elastic Fabric Adapter](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html) interfaces that carry cross-machine traffic. A few of these checks deserve detail.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*73vlwnPR6M7b1cYx43QeGw.png)

Two-tier health checking. Device-level and node-level checks become Kubernetes node conditions, which controllers then turn into taints, drains, terminates, and replaces.

- *Failing closed:* if the driver or the diagnostic tool is unresponsive, the check times out and marks the machine unhealthy. A check that cannot reach the hardware reports a problem rather than passing, so a wedged driver takes the machine out of rotation rather than letting it hide behind a hung tool.
- *A fallback path:* driver error codes are the strongest signal that a GPU has faulted, but the tool that reads them can itself be broken in certain failure modes! When it does, we read the kernel log dmesg directly for those codes, so no Xid or SXid errors are missed.
- *Our own fatal-error map:* vendor driver error catalogs lag newer GPU generations and do not always match what we see in production, so we keep our own mapping of which codes are fatal for each GPU family. A code that means reset-the-GPU in one generation can be benign in another, and one GPU generation emits a burst of normally-fatal code on every healthy boot, which we learned to treat as noise rather than drain fresh machines.
- *No silent no-ops:* a check fails when a required dependency is missing. This one came from an upgrade that dropped a binary the network-adapter check relied on. The check quietly stopped running, and machines with the wrong number of adapters shipped for days before the slow jobs were traced back to them. Now a missing dependency fails the check.

## Turning a bad machine into healthy capacity, automatically

When a check fails, the machine’s node condition changes, and controllers take over. We distinguish two levels. A problem condition blocks new work from landing while jobs are running, because pulling a job off a machine is disruptive, and many problems clear on their own. If the condition persists beyond a tolerance window, it escalates to a failure condition, which evacuates the machine, drains its tasks (overriding the normal disruption limits to move quickly), terminates it, and replaces it.

## Get Netflix Technology Blog’s stories in your inbox

Join Medium for free to get updates from this writer.

[Karpenter](https://karpenter.sh/) node auto-repair is used on our compute stack. We have customized it with a policy and a controller that maps each node condition to the duration we tolerate it before acting, so a fast-fatal error is actioned within minutes. At the same time, a flaky signal gets a longer window, and a cap limits how much of a cluster we will disrupt at once, so a bad rollout of the checks themselves cannot cascade into tearing down a whole cluster. We plan to upstream this feature to all Karpenter users.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*E194fQZ3PRUDlq0AU5VQPg.png)

Graded remediation. A problem is tolerated and may clear; a persistent failure escalates to evacuation and draining, then to a fast in-place fix or termination for confirmed hardware faults.

Not every fault requires a full replacement, and replacement is the slowest way to restore capacity. We match the action to the fault. Killing the offending job clears a software wedge. Resetting a single GPU clears many transient device faults. Rebooting the machine clears the firmware state that has drifted over a long uptime. Terminating and replacing is reserved for hardware that fails a test we trust. For that last case, we record the GPU’s immutable hardware identifier, which stays with the physical device across reboots and relaunches even when the instance changes, report it to the cloud provider, and keep our own list, so a device that fails repeatedly does not quietly rejoin the pool under a new instance.

One subtlety sits between detection and scheduling. A freshly checked machine was handed to the scheduler just as its checks were still settling, so a job could land on it a moment before a slow check flagged it. We now hold capacity until the checks have run and settled, which closed that window.

## Validating a machine before it takes work

A machine that just booted is not trusted until it proves itself. Before we release its capacity, it passes system checks, confirms the GPUs and their topology are present, and runs a round of GPU diagnostics. We then wait for the health checks to run twice, because the longer checks, such as counting network adapters, take more than one cycle to fire, and releasing after a single pass would let work land before those checks are reported. Only then do we remove the startup taint. On teardown, we run deeper diagnostics and record the GPU identifiers, which feed the same bad-hardware list, so hardware that failed once does not silently cycle back into service.

## Letting long jobs survive machine loss

Even with all of the above, some machines are lost mid-job, so we make that cheap. Jobs checkpoint their state, and on a lost machine, they resume from the last healthy checkpoint rather than restarting from the beginning of a multi-week run. Workers are elastic and retryable, and the scheduler automatically retries platform-caused failures.

Attribution is what makes automatic retries safe. If we retried every failure, we would mask genuine bugs in a job and burn GPU hours looping on an error the platform cannot fix, so we classify each failure as platform or application before retrying. One example of why this matters: a class of timeouts in [NCCL](https://developer.nvidia.com/nccl), the collective communication library GPUs use to exchange data, appeared to be a network fault and was traced to data-loading stalls at high worker counts. The GPUs and the network were fine, and the fix was in the data pipeline. Treated as hardware failures, those timeouts would have cycled healthy machines without fixing the cause.

## Measuring whether it works

We track GPU reliability along three service-level objectives, each split by cause, so a miss points at the layer responsible:

- *Availability:* the amount of GPU capacity available for scheduling at any given moment.
- *Job-start success:* whether a job starts promptly once its capacity is available.
- *Job success:* whether a job finishes without a platform-caused failure.

Each objective is split into hardware, driver, platform, and user causes. Hence, an availability dip from bad hardware reads differently from one caused by a scheduler change or a user misconfiguration. We optimize for goodput, the useful work the fleet completes, because a job held back by one slow GPU can look healthy on an uptime chart while getting almost nothing done. Specific targets for each objective are provided here for illustrative purposes.

## A closed remediation loop

These pieces form a loop. Hardware is validated at allocation, before a job starts, with a short collective communication run and pairwise network tests. Hence, any machine that fails within the first minute fails before the job is admitted. During the job, we watch passively for driver errors, memory errors, thermal events, and more. We view each job as a distributed system, which lets us identify a single slow rank dragging the rest, rather than only whole-machine failures. When something is wrong, remediation is automatic and graded. The loop is the same whether a job runs through our batch scheduler, [Kueue](https://kueue.sigs.k8s.io/), or [Ray](https://www.ray.io/).

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*UpFBA2LWwDLkaujStvIq_g.png)

The reliability loop: validate, watch, actively check, view the job as a system, remediate, then repeat.

## Sharing GPUs safely

Not every workload needs a whole GPU, and leaving small inference jobs on dedicated GPUs wastes capacity. We partition GPUs with [MIG](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/) for memory-level isolation between tenants, so a fault or a memory hog in one partition does not affect another. We also reconfigure those partitions without restarting the machine, so that a pool can shift between many small slices and a few large ones as demand changes. GPU and network adapter allocation is device-plugin-based today, to move to Kubernetes Dynamic Resource Allocation once it is supported in Karpenter. This matters because a GPU talking to a network adapter or working with a CPU on the wrong PCIE root of the machine incurs a bandwidth penalty.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*1MA62iL5MCRimp5V1Fgmrw.png)

On a multi-GPU machine, we isolate a single faulty GPU, keep the rest in service, and partition healthy GPUs across multiple tenants with memory-level isolation.

Device-level allocation also changes how we handle a single bad GPU. With DRA support, instead of losing the whole machine, we could isolate the one faulty device and keep the others serving, which matters most for inference, where many small jobs share a machine. And because allocation is expressive, a job can request the capabilities it needs, such as memory or tensor-core support, and the platform matches a suitable GPU type, so users are not pinned to a model they had to choose in advance.

## Results

Moving from basic checks and manual draining to layered checks and automatic remediation changed two things users feel. More of the GPU fleet is available for scheduling at any time because bad machines are caught and cycled quickly, rather than sitting in the pool or waiting on an on-call engineer. And fewer jobs fail due to platform issues because most faults are caught before a job lands, and the rest are automatically remediated and retried. Graded remediation also returns capacity in minutes for faults that only require a job kill, a GPU reset, or a reboot, rather than the longer wait for a replacement machine.

Since the above improvements have landed, we’ve seen:

- Consistently achieving >99.95% availability of our GPU nodes
- Job success rate has gone from ~98% to above 99.5%

## What is next

We are extending active checks to cover additional failure modes under load, widening burn-in so more classes of failures can be cleared before a user encounters them, and making remediation more granular so more error types are cleared in place rather than requiring a full node replacement loop for certain Xid errors. Additionally, we want to do more periodic diagnostics between jobs.

We are working to make placement more topology-aware using Kubernetes Dynamic Resource Allocation (DRA) once it lands in Karpenter, for example, by aligning on Compute/IMEX Domains, PCIe roots, and NUMA nodes.

More on the performance side for multi-GPU training, we plan to run a custom Linux scheduler built on [sched\_ext](https://docs.kernel.org/scheduler/sched-ext.html). Firstly, we can prioritize processes during collective coordination, such as when GPUs exchange results before the next round of compute, thereby reducing overall GPU idle time by establishing a fleet-wide priority for these tasks. The effect is small on one machine but grows across hundreds of machines, where a few percent of throughput amounts to a large amount of capacity. Secondly, we can prioritize data-loading processes to minimize the bottleneck that sometimes occurs when data is not loaded onto GPUs quickly enough to maintain steady progress.

While we already monitor throttling events, GPUs do not have to report throttling for it to hurt a job. One running ten to fifteen degrees hotter than its peers, even within healthy limits, sets the pace for the gang, so we can treat a large temperature gap as a fault, stop the job, and move it to cooler GPUs.

Additionally, we plan to expand our NCCL RAS (reliability, availability, serviceability) monitoring to identify NCCL issues sooner, such as mismatched collectives or hangs, to more quickly resume work.

## Closing

Hardware fails, and at this scale, it fails often enough that the platform has to treat failure as normal. Detecting problems before and during jobs, automatically remediating machines, and allowing long jobs to resume after a loss lets teams run large-scale training and inference without babysitting the hardware. If you like these kinds of problems, we are hiring.