---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-24-antithesis-nightmare-mode
source_title: "Nightmare mode: simulating disk failures"
source_author: Anjana Ratnayake and Teymour Aldridge
source_url: https://antithesis.com/blog/2026/nightmare-mode/
tags:
  - source/summary
  - testing
  - fault-injection
  - distributed-systems
  - storage
source_ids:
  - src-2026-11-24-antithesis-nightmare-mode
status: active
---

# Nightmare Mode: Simulating Disk Failures

## Summary

Anjana Ratnayake and Teymour Aldridge of Antithesis's Forward Deployed Engineering team describe the
disk fault injector the company built for customers whose distributed systems must store data and never
lose it. After running a patched version of the open-source LazyFS, Antithesis wrote its own FUSE
filesystem, Amnesia, in Rust. It emulates power loss by holding unsynced writes in its own cache and
discarding them when the container is killed, and it adds disk I/O errors (including the fsyncgate
behaviour) and latency faults that reorder or split operations to expose races. Power failures are tied
to individual disk operations so the fuzzer spends less effort finding vulnerable moments. The one
shareable result is a bbolt bug that needed an I/O error followed by a power failure. **The post
contains no AI content**; it is in the vault as a testing and reliability reference, and it is a
first-party vendor post that ends in a sales invitation.

## Key claims

### Storage faults are varied, and customers expect different guarantees

A single write can fail and force a retry-or-give-up decision; a full disk can require compaction; file
creation can fail when inodes run out. A slow disk can stretch operations so a concurrent reader sees old
data, new data, or an interleaving. After power loss a read may see all, part, or none of a write that had
succeeded. Customers had "vastly different expectations" of their storage and ran ext4, XFS, or ZFS, each
with its own failure behaviour, so Antithesis first built per-customer solutions (for example, filling the
filesystem to test space reclamation) before combining them into one injector.

### Power loss is not a process kill

Writes go to the kernel page cache and reach disk through writeback or an explicit fsync. Antithesis's
existing node-kill fault SIGKILLs a container, but the kernel keeps running, so completed writes still
reach disk "fsync or no fsync"; a SIGKILL "is a fairly polite way to die". A power failure loses everything
written but not yet fsynced. Because the kernel offers no way to forget its cache or stop writeback, the
team used LazyFS, a FUSE filesystem from INESC TEC and Jepsen that keeps written data in its own cache
until fsync. Clearing that cache at the moment the application is killed is, the authors say,
"indistinguishable from a real power loss". They rejected eBPF, which can observe and tweak calls but
cannot hold data and release or lose it later, and a custom block device, which sees blocks rather than
syscalls and cannot tell fsynced data from writeback, losing "the strictness that catches missing fsyncs".

### From LazyFS to Amnesia

A patched LazyFS with extra fault types ran on a number of customer tenants and "found some subtle data
loss bugs". Amnesia was then written in Rust for memory safety and a simpler, faster model. It works on
inodes rather than paths, which removes the awkwardness of tracking renames, hard links, and deletion of
open files, and it keeps both volatile and "durable" state in memory, so an fsync is a bookkeeping update
rather than real I/O. LazyFS also taught the team about torn writes and torn sequences of writes, and the
FUSE settings needed so the kernel page cache in front of FUSE does not serve data that was supposedly lost.

### I/O errors, including fsyncgate

Returning an error code alone found some bugs, but emulating the page cache allows higher fidelity. The
key case is EIO on fsync. The kernel clears a page's dirty flag before submitting it; if the device write
fails, fsync returns EIO but nothing marks the page dirty again, so neither the next fsync nor writeback
resubmits it, and the next fsync succeeds. The post quotes Craig Ringer's fsyncgate report: success means
"all writes since the last fsync have hit disk", not since the last *successful* one. PostgreSQL now
crashes and recovers from its log instead of retrying. Amnesia reproduces this by marking the affected
pages clean without persisting them, so the data is lost at the next emulated power failure unless
rewritten and fsynced.

### Latency faults are concurrency tests

Two kinds are supported. Out-of-order completion lets the fuzzer choose when a parked operation completes,
with a deadline as a backstop. Partially completed operations split a write into chunks, some applied and
some held, so a concurrent read sees a mix of old and new data; reads can likewise be split across moments.
The authors say every interleaving the fuzzer tries is one "the kernel page cache or disk could have
produced".

### Faults correlated with operations

The filesystem works with the Antithesis fault injector and fuzzer, so disk faults are controlled like
other faults and gain the benefits of swarm testing. Within the "before" or "after" window of a disk
operation, the exact timing of a power failure does not change the outcome, while the interesting
"during" states are short and rare. The injector therefore decides on each syscall and can fire a power
failure at three points: before any of the operation has been applied to the internal cache, after part
of it, or after all of it but before the syscall returns. The authors call these **correlated faults**
and say this "decreas[es] the uninteresting state space" the fuzzer explores.

### A bug that needed two faults in sequence

bbolt, the storage engine behind etcd, commits in two fsynced steps: data pages, then a meta page pointing
to them. When the meta page's fsync failed with EIO, etcd exited, which is correct. On restart bbolt read
the unpersisted meta page back through the kernel page cache, treated the transaction as committed, and
rebuilt its free list so later commits reused pages the on-disk meta page still referenced. After the
cached page was evicted (by emulated memory pressure or power loss), bbolt panicked at every open, and the
etcd write-ahead log could not help because the node never got past opening. The authors say this "could
only be found by an I/O error followed by a power failure".

## Why it matters

[[Agentic Testing]] gains a testing method with no model in it: the environment, not an agent, is the
adversary, and the oracle is the system's own durability invariants. Correlating faults with operations
is a concrete way to shrink a search space, and the bbolt case is, by the authors' account, a defect
that only a compound fault exposes. [[Antithesis]] gains its own first-party account, beside the
property-testing libraries Geoffrey Huntley promotes.

## Tensions / open questions

- **First-party vendor post.** "A number of bugs in customer software" is not counted; only the bbolt bug is
  shared. No detection rate, run time, overhead, or comparison with other fault-injection tools is given.
- **Fidelity is asserted, not measured.** The claim that cache clearing plus a kill is indistinguishable
  from real power loss, and that every split interleaving is legal, is the authors'; no validation against
  real hardware failures is reported, and filesystem-specific differences (ext4, XFS, ZFS) are named but not
  shown to be modelled.
- **No published date in the capture.** The date was recovered outside it (see Citations).
- **Off-domain for this vault.** There is no AI system, model, or agent in the post; connections to agent
  testing are the vault's synthesis.

## Affected pages

- [[Agentic Testing]]
- [[Antithesis]]

## Raw capture

- [[knowledge-base/raw/sources/Nightmare mode simulating disk failures]]

## Citations

- Canonical URL: <https://antithesis.com/blog/2026/nightmare-mode/> (the captured link carried a
  `utm_source=tldrnewsletter` parameter, removed here).
- Byline in the capture: Anjana Ratnayake and Teymour Aldridge, on the Antithesis blog. The capture's
  `published` field is empty; the 2026-11-24 publication date was recovered outside the capture from the
  live page. Captured 2026-11-26.
- The bbolt issue (etcd-io/bbolt issue 1335), the LazyFS paper by Ramos et al., and Dan Luu's fsyncgate page
  are linked from the capture but were not read.

## Related pages

- [[Agentic Testing]]
- [[Antithesis]]
- [[Geoffrey Huntley - The Answer to AI Is Engineering]]
- [[Nikolas Göbel - Informal Verification]]
- [[Federico Tomassetti - Legacy Modernization with LLMs, Measured]]
