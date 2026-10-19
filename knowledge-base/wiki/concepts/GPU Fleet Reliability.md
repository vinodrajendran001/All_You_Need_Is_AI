---
type: concept
created: 2026-10-19
updated: 2026-10-19
tags: [concept, gpu, reliability, distributed-training, infrastructure, systems]
source_ids:
  - src-2026-10-15-netflix-reliable-gpu-compute
  - src-2026-10-04-ben-tovim-ai21-kueue-gpu-fleet
  - src-2026-10-02-epoch-agent-population
  - src-2026-07-17-netflix-in-house-llm-serving
status: active
---

# GPU Fleet Reliability

## Definition

**GPU fleet reliability** is the work of keeping accelerator capacity fit for distributed training
and serving: detecting hardware that is degraded rather than merely dead, remediating it in proportion
to the fault, making the loss of a machine cheap for running jobs, attributing failures before
retrying them, and measuring the useful work the fleet completes rather than its uptime.

## Why it matters

GPU capacity is expensive, and synchronous distributed jobs make one bad device everyone's problem.
In the collectives described on [[Distributed Training Parallelism]], ranks exchange data every step,
so a gang-scheduled job moves at its slowest member's pace and stops when any member dies. Basic
infrastructure checks answer "is the machine up?"; the costly question is "will this machine run a
collective at full speed for the next three weeks?"

## Current synthesis

### Health is a different control from admission

[[Asaf Ben-Tovim - How AI21 Manages Its GPU Fleet with Kueue]] and
[[Netflix - Reliable GPU Compute for Training and Inference]] address adjacent layers that are easy to
merge. AI21's Kueue setup decides **which complete jobs may start and where they can be placed**: eight
free GPUs split 1+1+4+2 across four nodes cannot host an eight-GPU single-node job. Netflix decides
**whether the capacity being scheduled can be trusted**: a machine can pass cloud instance checks and
answer driver queries while a GPU faults under load. Netflix states that its loop works the same way
whether jobs arrive through its batch scheduler, Kueue, or Ray, which is consistent with treating
health as a layer below admission rather than a scheduler feature. Both accounts are first-party
operational reports.

The failure classes differ as well. AI21 notes that a queue guarantee against scheduler preemption does
not stop a cloud provider reclaiming spot capacity; Netflix handles devices and fabric that are present
but unfit. A fleet needs a policy for each, and neither substitutes for the other.

### Degraded is the expensive state

The failures that cost the most time do not crash anything. Netflix's examples are an Elastic Fabric
Adapter with fewer links than expected, so collectives run at a fraction of bandwidth, and a GPU that
answers status queries but faults once a job allocates memory or runs sustained compute. Its planned
policy of treating a GPU running ten to fifteen degrees hotter than its peers as a fault follows the
same logic: within healthy limits, the hot device still sets the pace for the gang. This is the
compute-versus-communication law of [[AI Accelerator Architecture]] seen as a failure mode, where a
weakened link or slow rank becomes the job's bottleneck.

Hence Netflix validates allocations with a short collective run and pairwise network tests before
admission, then looks for a single slow rank during the job instead of only for whole-machine failure.

### The observer can fail too

Netflix's most transferable rules concern the checks themselves: fail closed when a driver or tool
hangs, fall back to the kernel log when the error reader breaks, maintain a per-GPU-family fatal-error
map because vendor catalogs lag, and fail the check when a dependency is missing. The last rule exists
because an upgrade dropped a binary and machines with the wrong adapter count shipped for days.

The vault has the same failure shape at other layers. [[Netflix - In-House LLM Serving]] lost most
engine metrics at an integration boundary (Triton's bridge surfaced **9 of more than 40** vLLM metrics),
and [[LLM Application Resilience]] argues that the dangerous LLM failures return a success status. In
all three, the hazard is a monitor that reports health because it has stopped observing.

### Remediation is graded and blast-radius capped

Netflix separates a *problem* condition, which blocks new work while running jobs continue, from a
*failure* condition reached when the problem persists past a per-condition tolerance window. Actions
escalate from killing a wedged job to resetting one GPU, rebooting, and only then terminating and
replacing hardware that fails a trusted test. A cap on simultaneous disruption keeps a bad rollout of
the checks from tearing down a cluster, and immutable GPU identifiers keep repeatedly failing devices
from rejoining the pool under new instances.

### Retry needs attribution

Checkpoints and elastic workers make machine loss cheap, but automatic retry is only safe after a
failure is classified as platform or application. Netflix's example is a class of NCCL timeouts that
looked like network faults and turned out to be data-loading stalls at high worker counts: retrying them
as hardware failures would have cycled healthy machines and left the cause in place. A collective
library's timeout is a symptom surface shared by fabric faults, slow ranks, and input pipelines.

### Measure useful work, not uptime

Netflix optimizes **goodput**, "the useful work the fleet completes", and splits each of its three
objectives (availability, job-start success, job success) into hardware, driver, platform, and user
causes. That is not the request-level goodput on [[Serving Benchmarks and Goodput]], which counts
completions under per-request latency targets, and the two should not be compared numerically. Both
reject the flattering denominator: uptime for a fleet, raw throughput for a server.

The same layering appears in [[ML Systems at Scale]], where the AI21 account and
[[Jason Li - How Many AI Agents Could We Run]] together keep raw supply, allocatable capacity, delivered
goodput, and useful work distinct. Health adds a step between allocatable and delivered: capacity can
be allocatable and still unfit. AI21's headline makes
the parallel point for scheduling: an **83% time-to-start reduction** for hero jobs is not an 83%
training-throughput gain.

Netflix's reported results are **>99.95%** GPU-node availability and job success rising from **~98% to
above 99.5%**, with no measurement window, fleet size, or denominators, and no targets in the captured
text despite a sentence promising illustrative ones.

### Partitioning changes the unit of capacity, and possibly of failure

For small inference jobs, Netflix uses MIG partitions for memory-level isolation and reconfigures them
without restarting machines. With device-level allocation through Kubernetes Dynamic Resource
Allocation, once Karpenter supports it, one faulty GPU could be isolated while the rest of the machine
keeps serving. That capability is conditional in the source. Placement also has an internal topology:
a GPU paired with a network adapter or CPU on the wrong PCIe root pays a bandwidth penalty.

## Open questions

- How much immediately schedulable capacity does a fleet give up by holding new machines until checks
  run twice, and when does that trade stop paying for itself?
- How accurate is platform-versus-application attribution in practice, and what does a
  misclassification cost in each direction: masked job bugs or recycled healthy machines?
- Training survives loss through checkpoints; always-on inference does not checkpoint. Which of these
  controls carry over to serving fleets, and which belong to routing and replica management instead?
- Can fleet-level goodput and request-level serving goodput be connected for a fleet that both trains
  and serves on shared hardware?
- Should operators share immutable-device failure records across tenants or with providers by default?

## Related pages

- [[Netflix - Reliable GPU Compute for Training and Inference]]
- [[Asaf Ben-Tovim - How AI21 Manages Its GPU Fleet with Kueue]]
- [[Netflix]]
- [[Distributed Training Parallelism]]
- [[Serving Benchmarks and Goodput]]
- [[ML Systems at Scale]]
- [[Model Factory]]
- [[AI Accelerator Architecture]]
- [[Jason Li - How Many AI Agents Could We Run]]
- [[Netflix - In-House LLM Serving]]
- [[LLM Application Resilience]]
- [[Inference Serving Engines]]
- [[Google Cloud]]
- [[NVIDIA]]
