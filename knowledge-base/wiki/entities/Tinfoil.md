---
type: entity
created: 2026-10-30
updated: 2026-10-30
entity_kind: organization
tags:
  - entity
  - security
  - privacy
source_ids:
  - src-2026-10-25-tinfoil-minimal-firmware
status: active
---

# Tinfoil

## What it is

Tinfoil is a confidential-inference provider represented in this vault by its engineers'
account, [[Joe Lothan et al - Less Is More - From 1M Lines of Firmware to 300 of Assembly]].
Its stated threat model includes Tinfoil's own host/operator as an adversary.

## Why it matters here

The company gives [[Confidential Computing]] a concrete build-versus-runtime distinction.
Its restricted fleet replaces general-purpose OVMF with roughly **300 assembly lines** and
prebuilds the kernel, initramfs, and boot structures into a hardware-measured IGVM image.
Only bounded memory-map and CPU-count inputs remain in the firmware's host-facing path.

This is not simply a shorter implementation of every OVMF feature. Work moves to the image
generator or already-trusted Linux, or is removed because those machine shapes do not need it.
The generator still requires audit, and host-layout changes can require a new image.

## Evidence boundary

The **eight-to-two** reduction in host-input parsing sites is vendor-reported. Neither that
count nor the firmware line count establishes a vulnerability rate; formal verification is
future work. The narrow boot design does not itself enforce agent tool permissions or guarantee
correct model output.

## Related pages

- [[Joe Lothan et al - Less Is More - From 1M Lines of Firmware to 300 of Assembly]]
- [[Confidential Computing]]
- [[Agent Security and Governance]]
- [[Apple]]
