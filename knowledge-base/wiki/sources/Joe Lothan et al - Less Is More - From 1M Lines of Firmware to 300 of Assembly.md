---
type: source-summary
created: 2026-10-30
updated: 2026-10-30
source_id: src-2026-10-25-tinfoil-minimal-firmware
source_title: "Less Is More: From 1M Lines of Firmware to 300 of Assembly"
source_author: Joe Lothan, Jules Drean, and Mia Korennykh
source_url: https://tinfoil.sh/blog/2026-10-25-less-is-more
tags:
  - source/summary
  - security
  - privacy
  - infrastructure
source_ids:
  - src-2026-10-25-tinfoil-minimal-firmware
status: active
---

# Less Is More: From 1M Lines of Firmware to 300 of Assembly

## Summary

Tinfoil's engineers describe replacing general-purpose OVMF firmware with roughly 300 lines of
assembly for their supported confidential-VM fleet. The threat model treats Tinfoil's own host
operator as untrusted. The reduction comes from prebuilding a tightly specified boot image and
moving work out of the live host-facing boot path, not from making the entire system only
300 lines long.

## Key claims

- **Measure the initial image, not a chain of later loads.** An IGVM image contains firmware,
  kernel, initramfs, command line, page tables, and ACPI tables/templates. Hardware measures
  that initial state at launch through Intel TDX's `MRTD` or AMD SEV-SNP's launch digest.
  Firmware no longer has to load and measure the rest afterward.
- **Delete or relocate general-purpose boot machinery.** Work moves to the image generator,
  already-trusted Linux, or disappears because the fleet does not need it. Firmware has no
  dependencies and stops executing after handing off to Linux.
- **Constrain remaining host inputs.** The two remaining parsing sites validate memory-map
  shape/size and CPU count; unsupported layouts fail boot. The authors report host-input
  parsing sites falling from **eight to two**, alongside the reduction from over **1M lines
  of C** in OVMF to roughly **300 assembly lines**.
- **The audit and runtime trust sets differ.** The image generator still needs to be audited
  for correctness, but no longer interprets adversarial host inputs during guest boot.
  Moving code to build time reduces runtime exposure without removing its influence.
- **Stage0 was a different fit.** Tinfoil rejected it for this deployment because it still
  loads/measures later components and processes more host configuration. The comparison is
  deployment-specific, not proof that the alternative is universally inferior.

## Why it matters

[[Confidential Computing]] must ask what the hardware measurement covers and which host inputs
remain after measurement. [[Agent Security and Governance]] usually assumes the infrastructure
enforces limits on an untrusted agent; this source reverses the direction and asks how the
workload can remain protected from the infrastructure operator.

## Tensions / open questions

- The smaller firmware supports a restricted set of machine shapes. A QEMU layout change can
  require a new image or firmware version; this is not a general drop-in replacement for OVMF.
- Line count is an auditability indicator, not a vulnerability rate or a proof of confidentiality.
  Hardware, Linux, build artifacts, attestation verification, and the application remain trusted
  parts of the system under the stated model.
- Formal verification is presented as an aspiration, not a completed result. The post is
  first-party engineering evidence, not an independent security audit.
- The broader discussion of language-model-assisted exploitation and its estimated economics
  motivates the design; it does not measure the security improvement of this firmware.

## Affected pages

- [[Confidential Computing]]
- [[Agent Security and Governance]]
- [[Tinfoil]]

## Raw capture

- [[knowledge-base/raw/sources/Less Is More From 1M Lines of Firmware to 300 of Assembly]]

## Citations

- Canonical URL: <https://tinfoil.sh/blog/2026-10-25-less-is-more>
- By Joe Lothan, Jules Drean, and Mia Korennykh; published October 25, 2026 and captured
  October 29, 2026.

## Related pages

- [[Tinfoil]]
- [[Confidential Computing]]
- [[Agent Security and Governance]]
- [[ByteByteGo - How Apple Fits an LLM on Your iPhone]]
