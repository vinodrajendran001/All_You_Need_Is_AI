---
type: source-summary
created: 2026-10-19
updated: 2026-10-19
source_id: src-2026-10-15-netflix-reliable-gpu-compute
source_title: "Reliable GPU compute for large training & inference jobs"
source_author: Nick Rutigliano, Argha C, and Samartha Chandrashekar (Netflix Technology Blog)
source_url: https://netflixtechblog.com/reliable-gpu-compute-for-large-training-inference-jobs-d62b03a96d7a
tags: [source/summary, gpu, reliability, distributed-training, kubernetes, systems]
source_ids: [src-2026-10-15-netflix-reliable-gpu-compute]
status: active
---

# Netflix - Reliable GPU Compute for Training and Inference

## Summary

Netflix's account of keeping a Kubernetes-native GPU fleet healthy for multi-week, gang-scheduled
training and a growing share of always-on inference. It treats hardware failure as normal at fleet
scale and organizes reliability into four layers: node and hardware health, scheduler and platform
remediation, training-loop survival, and observability. Two design commitments recur: checks must not
be able to pass silently, and a failure must be attributed before it is retried.

This is a first-party engineering report. Its results are stated without a measurement window, fleet
size, or metric denominators.

## Key claims

### Why basic checks miss the costly failures

- A large training job can run for weeks across hundreds of GPUs on many machines. It runs as a gang:
  ranks exchange data every step, so the job advances at the slowest participant's pace and stops
  entirely if one participant dies.
- Cloud instance checks (host and instance status, attached storage, scheduled maintenance events,
  automatic recovery) confirm that a machine is up, reachable, or slated for maintenance. Netflix uses
  all of them and feeds maintenance events into one of its own checks, but they do not verify that
  each GPU, its on-chip memory, its interconnect, and the network fabric can support distributed
  training.
- A "driver responds" check also misses the slow-to-diagnose cases: a GPU that answers status queries
  but faults once a job allocates memory or runs sustained compute; an Elastic Fabric Adapter (EFA)
  showing fewer links than expected, so collectives run at a fraction of bandwidth rather than crash;
  a diagnostic tool that hangs when the driver hangs; and a check whose dependency disappears after an
  upgrade so it stops reporting. "A check that can silently stop running is worse than no check."

### Detection

- A node agent built on the open-source Kubernetes node-problem-detector runs on every GPU machine
  every 30 seconds and turns results into Kubernetes node conditions; controllers decide from those
  conditions whether the machine may take work.
- Device checks use NVIDIA DCGM for driver error codes, uncorrectable memory errors, interconnect
  integrity, and thermal state. Adapter checks inspect the count and link state of EFA interfaces.
- Four rules: **fail closed** (an unresponsive driver or tool times out and marks the machine
  unhealthy); a **fallback path** (read the kernel log directly for Xid/SXid codes when the reading
  tool breaks); a **Netflix-maintained fatal-error map** per GPU family, because vendor catalogs lag
  newer generations and one generation emits a burst of normally fatal codes on every healthy boot;
  and **no silent no-ops** (a missing dependency fails the check). The last rule came from an upgrade
  that dropped a binary: machines with the wrong number of adapters shipped for days before slow jobs
  were traced back to them.

### Remediation

- A *problem* condition blocks new work while running jobs continue, since many problems clear on
  their own. If it persists beyond a tolerance window it escalates to a *failure* condition, which
  evacuates the machine, drains its tasks (overriding normal disruption limits), terminates it, and
  replaces it.
- Netflix customized Karpenter node auto-repair with a policy and controller mapping each condition to
  a tolerated duration, so a fast-fatal error is actioned within minutes while flaky signals get longer
  windows. A cap limits how much of a cluster can be disrupted at once, so a bad rollout of the checks
  themselves cannot tear a cluster down. Netflix plans to upstream the feature.
- Remediation is graded: kill the offending job for a software wedge, reset one GPU for many transient
  device faults, reboot for firmware state drifted over long uptime, and terminate/replace only for
  hardware failing a trusted test. The GPU's immutable hardware identifier is recorded, reported to
  the cloud provider, and kept on Netflix's own list so a repeatedly failing device cannot rejoin the
  pool under a new instance.
- Capacity is now held until checks have run and settled; previously a job could land just before a
  slow check flagged the machine. A new machine passes system checks, GPU and topology presence
  checks, and GPU diagnostics, then waits for the health checks to **run twice** before its startup
  taint is removed. Teardown runs deeper diagnostics that feed the same bad-hardware list.

### Jobs survive loss, but only attributed failures are retried

- Jobs checkpoint and resume from the last healthy checkpoint; workers are elastic and retryable; the
  scheduler retries platform-caused failures automatically.
- Each failure is classified as platform or application before retry, so genuine job bugs are not
  masked and GPU hours are not burned looping. Example: a class of NCCL timeouts that looked like a
  network fault was traced to data-loading stalls at high worker counts. Treated as hardware failures,
  they would have cycled healthy machines without fixing the cause.
- Hardware is validated at allocation with a short collective-communication run and pairwise network
  tests, so a machine that fails within the first minute fails before the job is admitted. During the
  job, Netflix watches passively for driver, memory, and thermal events and treats the job as a
  distributed system to find a single slow rank. The loop is the same through its batch scheduler,
  Kueue, or Ray.

### Measurement, sharing, and reported results

- Three service-level objectives — **availability** (capacity available for scheduling), **job-start
  success**, and **job success** (no platform-caused failure) — are each split into hardware, driver,
  platform, and user causes. Netflix optimizes **goodput**, "the useful work the fleet completes",
  because a job held back by one slow GPU can look healthy on an uptime chart.
- The capture says specific targets are "provided here for illustrative purposes", but no targets
  follow in the captured text.
- MIG partitions give memory-level isolation between small inference tenants and are reconfigured
  without restarting the machine. GPU and adapter allocation is device-plugin-based today; isolating
  one faulty device while the rest keep serving, capability-based requests, and topology-aware
  placement are framed as possible once Kubernetes Dynamic Resource Allocation (DRA) is supported in
  Karpenter. A GPU paired with an adapter or CPU on the wrong PCIe root incurs a bandwidth penalty.
- Reported outcomes after moving from basic checks and manual draining to layered checks and automatic
  remediation: "**>99.95% availability of our GPU nodes**" and job success "**from ~98% to above
  99.5%**"; graded remediation returns capacity in minutes for faults needing only a job kill, GPU
  reset, or reboot.
- Planned work: wider active checks and burn-in, more in-place remediation for certain Xid errors,
  periodic between-job diagnostics, topology-aware DRA placement (Compute/IMEX domains, PCIe roots,
  NUMA nodes), a sched_ext Linux scheduler prioritizing collective coordination and data loading,
  treating a GPU running **ten to fifteen degrees hotter** than its peers as a fault, and expanded NCCL
  RAS monitoring.

## Why it matters

This is the vault's first operational account of hardware health in a GPU fleet.
[[Asaf Ben-Tovim - How AI21 Manages Its GPU Fleet with Kueue]] decides which jobs may start and where
they fit; Netflix decides whether the capacity being scheduled is fit to use and what to do when it is
not. Its goodput is fleet-level useful work, a different quantity from the request-level goodput on
[[Serving Benchmarks and Goodput]]. See [[GPU Fleet Reliability]].

## Tensions / open questions

- **Undefined denominators.** The availability SLO is defined as capacity available for scheduling,
  while the result reports availability "of our GPU nodes"; the capture does not say whether these are
  the same metric, how it is time-weighted, or whether held or quarantined capacity counts. The
  job-success change has no window, job count, or statement of whether user-caused failures are
  excluded.
- **Attribution is a classifier.** Automatic retry is safe only as far as platform/application
  classification is right. The NCCL example shows the misclassification risk, but no classification
  error rate is reported.
- **Held capacity is a trade.** Holding capacity until checks settle and requiring two check passes
  should raise job-start reliability at some cost in immediately schedulable capacity. That trade is
  the vault's reading; the source does not quantify it.
- **Present tense versus conditional.** A figure caption describes isolating a single faulty GPU while
  keeping the rest in service; the prose makes that capability conditional on DRA support in
  Karpenter. The conditional reading is kept here.
- The temperature-gap fault policy, sched_ext scheduler, and upstreamed Karpenter feature are plans,
  not results.

## Affected pages

- [[GPU Fleet Reliability]]
- [[Distributed Training Parallelism]]
- [[ML Systems at Scale]]
- [[Serving Benchmarks and Goodput]]
- [[Model Factory]]
- [[AI Accelerator Architecture]]
- [[Netflix]]
- [[NVIDIA]]

## Raw capture

- [[Reliable GPU compute for large training & inference jobs]]

## Citations

- Canonical article:
  <https://netflixtechblog.com/reliable-gpu-compute-for-large-training-inference-jobs-d62b03a96d7a>
- Published October 15; captured October 19, 2026.
- The capture includes a Medium subscription prompt inside the article body; it is not part of the
  technical account.

## Related pages

- [[GPU Fleet Reliability]]
- [[Netflix]]
- [[Asaf Ben-Tovim - How AI21 Manages Its GPU Fleet with Kueue]]
- [[Distributed Training Parallelism]]
- [[Serving Benchmarks and Goodput]]
- [[ML Systems at Scale]]
- [[Model Factory]]
- [[AI Accelerator Architecture]]
- [[NVIDIA]]
- [[Netflix - In-House LLM Serving]]
- [[Sunita Nadampalli and Nicolò Lucchesi - Push-Based KV Transfer in vLLM]]
- [[LLM Application Resilience]]
