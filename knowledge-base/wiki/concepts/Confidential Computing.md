---
type: concept
created: 2026-10-30
updated: 2026-10-30
tags:
  - concept
  - security
  - privacy
  - infrastructure
source_ids:
  - src-2026-10-27-bytebytego-apple-on-device
  - src-2026-10-25-tinfoil-minimal-firmware
status: active
---

# Confidential Computing

## Definition

Confidential computing protects data during execution within a hardware-backed isolation
boundary, under a stated threat model that can include an untrusted host operator. Attestation
provides evidence about the measured execution environment so a client can decide whether to
send it data. Neither isolation nor a matching measurement proves the application is correct.

## Why it matters

An agent sandbox usually protects infrastructure from the agent. Confidential inference asks
the reverse question: how can a user send sensitive inputs to a service without giving its
operator unrestricted access? [[Agent Security and Governance]] still needs both directions;
protecting inputs from the host does not authorize what the agent may do with tools.

## Current synthesis

[[ByteByteGo - How Apple Fits an LLM on Your iPhone]] places this boundary inside a local-first
product. Tasks can leave the phone for Private Cloud Compute, where the account describes
verification of authorized software and encrypted request delivery. The privacy claim is
therefore about an enforced remote execution path, not a claim that all processing stays local.
The source is secondary and its closing claims about newer PCC hardware/platform placement
are not verified by claim-specific references in the capture.

[[Joe Lothan et al - Less Is More - From 1M Lines of Firmware to 300 of Assembly]] makes the
boot side explicit. Tinfoil treats its own host/operator as untrusted and prebuilds an IGVM
image containing the firmware, kernel, initramfs, command line, and boot structures. TDX or
SEV-SNP measures that image at launch, rather than relying on general firmware to load and
measure subsequent components while interpreting more host configuration.

Together the accounts separate three obligations:

1. **Identity and admission:** verify that the measured environment is one the client accepts
   before releasing its input.
2. **Runtime exposure:** minimize what the accepted environment still parses from an untrusted
   host. Tinfoil reports eight host-input parsing sites reduced to two bounded checks.
3. **Application authority and correctness:** separately constrain tools and test behavior.
   Running approved software privately does not make its answers true or its actions permitted.

## Smaller runtime trust does not remove build-time trust

Tinfoil's roughly 300 assembly lines replace over 1M lines of general-purpose OVMF C in its
boot path, not the whole trusted computing base. Linux and the image generator still require
trust and audit. Moving boot construction to a generator removes live adversarial host inputs
from that code's execution, but its output still decides what the guest runs.

The restriction buys simplicity by accepting fewer machine shapes. Memory-layout or QEMU
changes can require a new image; unsupported inputs fail boot. A line-count reduction is
therefore a scoped reduction in runtime exposure and audit surface, not formal verification
or a measured probability of compromise.

## Open questions

- Which hardware, firmware, kernel, build, and attestation-verification components remain
  trusted in a particular deployment, and how are their updates approved or revoked?
- How much flexibility and operational maintenance does a narrowly specified image trade for
  less host-controlled parsing?
- What independent evidence tests the confidentiality guarantee beyond matching a measurement?
  Neither captured source supplies a full independent security evaluation.

## Related pages

- [[Apple]]
- [[Tinfoil]]
- [[On-Device Reasoning]]
- [[Agent Security and Governance]]
- [[ByteByteGo - How Apple Fits an LLM on Your iPhone]]
- [[Joe Lothan et al - Less Is More - From 1M Lines of Firmware to 300 of Assembly]]
