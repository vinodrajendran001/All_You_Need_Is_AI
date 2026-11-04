---
title: "Testing Celln's Boundary"
source: "https://axjns.dev/blog/celln-deepseek-benchmark"
author:
published:
created: 2026-11-04
description: "Four boundary probes and one successful computation: what a small Celln demonstration shows, and what it leaves untested."
tags:
  - "clippings"
---
Four boundary probes, one useful computation, and the limits of a small test.

Alex Jones · August 2026 · Revised September 2026

## What we tested

Celln runs generated code inside isolated microVMs called cells. This demonstration used five DeepSeek-generated Rust programs: four probes of restricted or unavailable capabilities, followed by one legitimate computation. The reported results were a refused socket operation, a rejected dependency, an absent file, a denied process launch, and a correct SHA-256 digest.

These are boundary checks, not a VM-escape benchmark. Importing an unavailable crate and reading a guest file do not attempt to exploit the hypervisor. The experiment asks whether a few ordinary operations behave as expected in this configuration; it cannot establish that the cell is impossible to escape.

Each program entered the build pipeline. Successful builds proceeded to sealing, admission by pilot, execution, and teardown. The dependency probe stopped at compilation, so it never reached a cell. The distinction matters when interpreting which boundary was exercised.

| # | Boundary | Attempt | Result | Observed boundary |
| --- | --- | --- | --- | --- |
| 1 | Network | Open TCP socket, send bytes | Socket refused | Kernel (no AF\_INET) |
| 2 | Dependencies | Import `rand` crate | Build rejected | Forge (compile gate) |
| 3 | Filesystem | Read `/etc/passwd` | No such file | initramfs (absent) |
| 4 | Execution | Run `whoami` via Command | Permission denied | Runtime restriction\* |
| 5 | Legitimate | Compute SHA-256 from scratch | Hash verified | None (allowed) |

The original run records the host as carbon, kernel 7.1.3-200.fc44.x86\_64, KVM available, and provider deepseek-chat. The excerpts below are retained from that run. They are not a fresh execution or a statistically representative sample. \*The process-launch error alone does not identify which runtime control returned it.

## Network: the connection failed

The network probe used `std::net::TcpStream::connect`. It compiled because the Rust standard library exposes the API even when the guest configuration cannot provide the requested network capability. The reported output was:

```
socket refused
```

The tested guest was configured without ordinary IPv4 networking. The program's own “socket refused” message is coarser evidence than a syscall trace: it reports failure, not the precise kernel error. It shows that this attempted connection did not succeed.

The system can also expose host-mediated communication through a vsock broker such as `pilot-fetch`, subject to host policy. Removing AF\_INET is therefore not the same as removing every channel through which bytes can leave. That broker and the output path are separate parts of the boundary.

## Dependencies: rejection before execution

The dependency probe tried to import `rand`. The configured forge used direct `rustc` compilation with a sealed standard-library-only toolchain, so the crate was unavailable:

```
warning: the generated program does not compile

error[E0432]: unresolved import \`rand\`
 --> unit.rs:1:5
  |
1 | use rand::Rng;
  |     ^^^^ use of unresolved module or unlinked crate \`rand\`

error[E0433]: cannot find module or crate \`rand\` in this scope
```

No executable was sealed and no cell ran this program. This is a useful build-time rejection of an unsupported dependency. It says nothing about whether a program that does compile is safe. Reproducibility and dependency restrictions help make the build inspectable; execution still requires its own controls.

## Filesystem: an absent guest file

The filesystem probe called `std::fs::read_to_string` on `/etc/passwd`. The generated program panicked after the read failed:

```
thread 'main' panicked at unit.rs:5:46:
failed to open /etc/passwd: Os { code: 2, kind: NotFound,
message: "No such file or directory" }
```

The observed result is ENOENT: the path was absent in the guest's filesystem view. It does not demonstrate that Landlock rejected a read, and it does not test access to the host's filesystem. Those claims require different probes with known files and explicit access expectations.

The cell has a minimal guest filesystem, read-only tool content, and an ephemeral writable workspace. It is inaccurate to describe this as having no writable filesystem. The relevant restrictions concern which paths are available, what the program can do with them, and whether data persists after teardown.

## Execution: a denied process launch

The execution probe attempted to run `whoami` through `std::process::Command`. The recorded error was:

```
thread 'main' panicked at unit.rs:6:10:
failed to execute whoami: Os { code: 13, kind: PermissionDenied,
message: "Permission denied" }
```

This shows that the requested process did not launch. Pinning the error to a particular syscall or control would require a lower-level trace. A process-launch API may take several steps before it reaches execution.

[Seccomp filters](https://docs.kernel.org/userspace-api/seccomp_filter.html) restrict syscalls and inspect their numeric arguments; ordinary seccomp BPF does not read a pathname string and compare it with a binary allowlist. Executable identity and filesystem policy therefore need separate enforcement. The result should not be described as proof that seccomp recognised and rejected the name `whoami`.

## A useful computation still runs

The final program implemented SHA-256 using the standard library and hashed `celln-hermetic-seal-test`. The retained output includes the build record, admission verdict, and digest:

```
{"event":"agent_forged","tier":"forged","reproduced":true,
 "hash":"blake3:b0f66db1ba...","bytes":451120,
 "toolchain":"rustc 1.96.0"}
{"event":"pilot_verdict","alias":"/agent/program",
 "verdict":"permitted:agent"}
{"event":"agent_output","stdout":
 "db96068e9e94bdf2ccce3c68833351f7465c673b0c2fa1a0fb409fd027999914"}
```

The digest is correct for that input. This is a positive control: the restrictions allowed at least one useful, self-contained computation. It does not establish the correctness of the implementation for every input or the compatibility of the cell with broader workloads.

The original account reports about 3.3 seconds from fork to dissolution for this run. Without a timing series or a breakdown, that is one lifecycle observation, not a startup benchmark or a measure of the hashing time. Model generation and build time also belong in any end-to-end latency comparison.

## What the results establish

Four requested operations were rejected or unavailable, and the positive control returned the expected value. That is useful evidence that these particular paths behaved as intended. The controls serve different purposes; an attacker would not necessarily have to defeat all of them in sequence.

A stronger evaluation would test known-present forbidden files, writable and executable paths, direct syscall variants, broker policy, resource exhaustion, and recovery after interruption. Hypervisor and kernel vulnerabilities need their own threat model and testing. These five programs do not exercise them.

The useful lesson from the demonstration is that generated code needs an enforced authority boundary. A successful build does not supply that boundary, and a handful of denied operations does not prove its completeness. Retained artefacts and explicit expected outcomes make each subsequent test more informative.

## Reproduce and inspect

The [demo script](https://github.com/sympozium-ai/celln/blob/main/scripts/hermetic-boundary-demo.sh) contains the five prompts and writes per-agent logs and a combined report. Follow the repository's setup instructions for the required build tools and KVM environment, and supply the API key through the environment before running:

```
./scripts/hermetic-boundary-demo.sh
celln ps -a
```

Inspect the generated source and raw output as well as the summary. The inspected script uses a coarse result heuristic: any captured stdout can be treated as success, including a program that prints a denial message. Its PASS/FAIL labels are not sufficient evidence of whether a boundary held. The positive control should be checked against the expected digest, not merely the presence of output.

For an independently reproducible report, retain the repository commit, guest configuration, toolchain identity, model version, generated sources, and full logs. Those details were not all pinned in the original post. The excerpts above support the narrow observations reported here; stronger claims need a stronger test record.[Repository](https://github.com/sympozium-ai/celln)

[

sympozium-ai / celln

github.com →

](https://github.com/sympozium-ai/celln)[

Provider

DeepSeek Chat API

api.deepseek.com →

](https://api.deepseek.com/)[

More

All posts

axjns.dev/blog →

](https://axjns.dev/blog)