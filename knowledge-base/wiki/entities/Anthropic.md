---
type: entity
created: 2026-08-25
updated: 2026-08-26
entity_kind: organization
tags:
  - entity
  - organization
  - ai-lab
  - claude
  - coding-agents
source_ids:
  - src-2026-08-21-anthropic-ai-native-sdlc
  - src-2026-08-25-bytebytego-stealing-reasoning-traces
status: active
---

# Anthropic

## What it is

AI research company, developer of the Claude model family and of Claude Code, the coding agent harness that appears across much of this vault's agent material.

## Why it matters here

Anthropic has been an ambient presence in this knowledge base for a long time — Claude Code is one of the reference harnesses in [[Coding Agent Harness]], `CLAUDE.md` is the canonical example of versioned institutional knowledge, and Claude skills recur throughout [[Agent Skill]]. This page exists so that presence has a home.

Its first directly ingested source, [[Anthropic - The AI-Native SDLC Playbook]], is also the vault's anchor for [[AI-Native Software Development Lifecycle]]. What makes it distinctive is scope: rather than describing how to make one agent work well, it describes what happens to an organisation's approval, review, and audit machinery when agents write most of the diff — and proposes rebuilding the lifecycle as a loop of committed artifacts with governance enforced as the agent acts.

Anthropic also appears indirectly on the hardware side. [[Jacob Peake - AI Chip Architectures]] records it as the anchor tenant validating AWS Trainium at frontier scale (over a million Trainium2 chips) and as a Google TPU customer contracted for up to a million chips — one of the clearest examples in the vault of a frontier lab deliberately spreading across non-NVIDIA silicon.

## Notes

- Vault sources are vendor material and should be read as such: the SDLC playbook consolidates the Applied AI team's consulting practice, with no baselines or measured outcomes.
- The playbook credits Jim Blackhurst, Will Steuk, and Jamal Arif for prior work it builds on.

## Reasoning-block exposure

[[ByteByteGo - How to Steal an AI Model's Private Thoughts]] reports that Anthropic returns encrypted reasoning state to clients in a field named `signature`, and that in July 2026 testing **Claude accepted almost every source/target block combination** — the exception being Fable 5, whose blocks only Fable 5 accepted. Claude was also the easiest family to extract from: a single fixed prompt sufficed, where GPT required up to 50 candidate extractions per block.

The mechanism is not a Claude-specific weakness so much as a design shared across providers — the envelope authenticates the model but not the account or conversation. It does, however, mean that anti-distillation training on Claude Opus 4.8 is undercut by Claude Haiku 4.5 accepting the same blocks and transcribing them. See [[Reasoning Trace Privacy]].

## Related pages

- [[Anthropic - The AI-Native SDLC Playbook]]
- [[AI-Native Software Development Lifecycle]]
- [[Coding Agent Harness]]
- [[Agent Skill]]
- [[Agent Security and Governance]]
- [[AI Accelerator Architecture]]
- [[AI Knowledge Base Overview]]
- [[ByteByteGo - How to Steal an AI Model's Private Thoughts]]
- [[Reasoning Trace Privacy]]
