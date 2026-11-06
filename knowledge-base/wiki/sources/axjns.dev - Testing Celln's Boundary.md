---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-11-04-axjns-celln-deepseek-benchmark
source_title: Testing Celln's Boundary
source_author: Alex Jones
source_url: https://axjns.dev/blog/celln-deepseek-benchmark
tags:
  - source/summary
  - sandboxing
  - agent-security
  - generated-code
source_ids:
  - src-2026-11-04-axjns-celln-deepseek-benchmark
status: active
---

# Testing Celln's Boundary

## Summary

This post reports a small demonstration of [[Celln]], which runs generated code inside isolated
microVMs called **cells**. DeepSeek generated **five** Rust programs:

- four probes of restricted or unavailable capabilities;
- one legitimate computation as a positive control.

All four probes failed to get what they asked for, and the positive control returned a correct
SHA-256 digest. The post is unusually careful about what those outcomes do and do not show. It is
"not a VM-escape benchmark". The excerpts come from one retained run, not a fresh execution. Several
results are attributed more narrowly than a reader might assume. The post also criticises its own
demo script's PASS/FAIL heuristic. For this vault, its value is as a worked example of testing
controls instead of inferring them from configuration.

## Key claims

### Setup and lifecycle

- Programs pass through a build pipeline ("forge"), then sealing, admission by a component called
  pilot, execution, and teardown. A program that fails to compile never reaches a cell.
- The original run records:
  - host "carbon";
  - kernel **7.1.3-200.fc44.x86_64**;
  - KVM available;
  - provider **deepseek-chat**.

  The post says these excerpts are "not a fresh execution or a statistically representative
  sample".

### Five results, each narrower than its label

| # | Attempt | Result | What the post says it shows |
| --- | --- | --- | --- |
| 1 | Open TCP socket | "socket refused" | This connection failed; guest had no ordinary IPv4 |
| 2 | Import `rand` crate | Build rejected (E0432/E0433) | Compile-gate rejection; no cell ran |
| 3 | Read `/etc/passwd` | ENOENT (os code 2) | Path absent from the guest view; not a Landlock denial |
| 4 | Run `whoami` | Permission denied (os code 13) | The process did not launch; the control is unidentified |
| 5 | SHA-256 of a test string | Correct digest | Positive control: useful work still runs |

- **Network.** The "socket refused" message is the program's own output, so it is "coarser evidence
  than a syscall trace". A vsock broker such as `pilot-fetch` can still mediate communication under
  host policy. "Removing AF_INET is therefore not the same as removing every channel through which
  bytes can leave."
- **Dependencies.** The forge used direct `rustc` with a sealed standard-library-only toolchain. The
  rejection "says nothing about whether a program that does compile is safe".
- **Filesystem.** The cell has a minimal guest filesystem, read-only tool content and an ephemeral
  writable workspace. It is "inaccurate to describe this as having no writable filesystem". Testing a
  denial would require a known-present forbidden file.
- **Execution.** Ordinary seccomp BPF inspects syscall numbers and numeric arguments. It does not
  read a pathname string and compare it with an allowlist. The result therefore "should not be
  described as proof that seccomp recognised and rejected the name `whoami`".
- **Positive control.** The build record shows the following:
  - a truncated `blake3` hash;
  - **451120** bytes;
  - `rustc 1.96.0`;
  - `"reproduced":true`;
  - pilot verdict `permitted:agent`.

  The output digest `db96068e…999914` is reported as correct for the input
  `celln-hermetic-seal-test`. The post says it does not establish correctness for every input.

### Timing is one observation

- The original account reports **about 3.3 seconds** from fork to dissolution. The post calls this
  "one lifecycle observation, not a startup benchmark or a measure of the hashing time". Model
  generation and build time also belong in end-to-end latency.

### What a stronger test would include

- The post lists what a stronger test would cover:
  - known-present forbidden files;
  - writable and executable paths;
  - direct syscall variants;
  - broker policy;
  - resource exhaustion;
  - recovery after interruption.

  Hypervisor and kernel vulnerabilities need their own threat model.
- The demo script "uses a coarse result heuristic". Any captured stdout can count as success,
  including a printed denial. "Its PASS/FAIL labels are not sufficient evidence of whether a boundary
  held."
- A reproducible report would keep several details:
  - the commit;
  - the guest configuration;
  - the toolchain;
  - the model version;
  - the generated sources;
  - the full logs.

  "Those details were not all pinned in the original post."

## Why it matters

- [[Agent Security and Governance]] gets a concrete case of separating an operation's failure from
  a denial by the intended control. Three of the four denials turn out to need a different
  explanation or a different probe.
- [[Celln]] gets the only runtime evidence in the vault for this system.

## Tensions / open questions

- **Methodology.** There is one run, five programs and no repetition.
  - The probes were generated by a model from prompts in the script. They are ordinary operations,
    not adversarial attempts.
  - Probe 2 never reached a cell. So only **three** probes exercised the runtime boundary, plus the
    positive control.
- **Naming.** The URL slug says "benchmark", but the post disclaims being one. DeepSeek's role is only
  to generate the programs. The results say nothing about DeepSeek's capability or safety.
- **The vsock broker.** It remains an untested channel, so the network result does not show a sealed
  cell.
- **Reproducibility.** The excerpts were retained from an earlier run, and the configuration was not
  fully pinned. `"reproduced":true` in the build record is a claim of the pipeline, not an
  independent rebuild.
- **Vault check.** During ingest, recomputing SHA-256 of `celln-hermetic-seal-test` without a
  trailing newline reproduced the reported digest. That checks the arithmetic only, not the run.

## Affected pages

- [[Agent Security and Governance]]
- [[Celln]]

## Raw capture

- [[knowledge-base/raw/sources/Testing Celln's Boundary]]

## Citations

- Canonical URL: https://axjns.dev/blog/celln-deepseek-benchmark
- Byline in the captured body: "Alex Jones · August 2026 · Revised September 2026". The capture's
  frontmatter author and published fields are empty. The site is axjns.dev.
- Repository: `sympozium-ai/celln`. The demo script is `scripts/hermetic-boundary-demo.sh`.
- Captured: 2026-11-04.

## Related pages

- [[axjns.dev - The Agent Environment Should Be a Lease]]
- [[axjns.dev - Post-Kubernetes Infrastructure for GenAI Workloads]]
- [[axjns.dev - The Synthetic Membrane - A Coordination Layer for Multi-Agent AI Systems]]
- [[axjns.dev - Agents Need Somewhere to Share Their Work]]
- [[axjns.dev - The Sticky-Note Problem]]
- [[Agent Security and Governance]]
- [[Celln]]
- [[DeepSeek]]
- [[Multi-Tenant Agent Architecture]]
