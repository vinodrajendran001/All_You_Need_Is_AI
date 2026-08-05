---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-google-skills-official-agent-skills-library
title: 'google/skills: Google''s Official Agent Skills Library'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/google-skills-official-agent-skills-library
published: '2026-06-09'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# google/skills: Google's Official Agent Skills Library

Google shipped something worth paying attention to: an official, open-source Agent Skills repository called [google/skills](https://github.com/google/skills).

It launched at Google Cloud Next 2026 on April 22, has 12,200+ stars on GitHub, and it's under active development. Here's what it is, what's in it, and why it matters.

## What Is google/skills?

`google/skills` is Google's official repository of [Agent Skills](https://agentskills.io) for Google Cloud products and technologies. Skills are "compact, agent-first documentation" - structured markdown knowledge packages that AI coding agents load on demand to gain expertise in specific tasks.

Instead of pasting Google Cloud documentation into your context window or hoping the model remembers the right `gcloud` incantations, you install the relevant skill and your agent just knows how to do it.

Install with:

code

```
npx skills add google/skills
```

Works with Claude Code, Codex, Cursor, Gemini CLI, Antigravity, and any Agent Skills-compatible host.

## Available Skills

The current library covers Google Cloud infrastructure and the Gemini Agent Platform:

### Gemini Agent Platform

- Gemini API on Agent Platform
- Gemini Interactions API
- Managed Agents API
- Skill Registry API

### Google Cloud Infrastructure

| Skill | What Your Agent Learns |
| --- | --- |
| AlloyDB Basics | PostgreSQL-compatible managed database setup, queries, migrations |
| BigQuery Basics | Data warehouse schema design, SQL patterns, cost optimization |
| Cloud Run Basics | Container deployment, scaling config, custom domains |
| Cloud SQL Basics | Managed MySQL/PostgreSQL provisioning and maintenance |
| Firebase Basics | Auth, Firestore, hosting, Cloud Functions setup |
| GKE Basics | Kubernetes cluster management, pods, services, ingress |

### Recipes (Step-by-Step Guides)

- Onboarding to Google Cloud
- Authenticating to Google Cloud
- Google Cloud Network Observability

### Well-Architected Framework

- Security
- Reliability
- Cost optimization
- Operational excellence
- Performance optimization
- Sustainability

The repository is under active development with more skills being added.

## Why This Matters

### Google is treating Agent Skills as a first-class distribution channel

This is the equivalent of Google publishing an official npm package - except instead of code libraries, they're publishing **AI knowledge**. When you install `google/skills`, your coding agent knows how to set up BigQuery, deploy to Cloud Run, configure GKE, and architect secure Google Cloud infrastructure.

You don't need to paste documentation into your context window. You don't need to remember the right authentication flow. The skill encodes all of that with proper error handling and common gotchas.

### Google launched this at their biggest developer event

This wasn't a quiet side project. Google announced `google/skills` on Day 1 of Google Cloud Next 2026, alongside a codelab showing how to build ADK (Agent Development Kit) agents that load skills dynamically. They built a `SkillToolset` class into ADK that discovers `SKILL.md` files from filesystem directories and exposes them as tools to agents.

## The Bigger Picture: Agent Skills as a Platform

`google/skills` is built on the open [Agent Skills](https://agentskills.io) standard - the same infrastructure that powers [last30days-skill](https://www.aibuilderclub.com/blog/last30days-skill-real-time-research) (34K+ stars) and the official skills from Vercel, Stripe, Cloudflare, Netlify, Sentry, Expo, and Hugging Face.

The pattern is clear: instead of giving AI agents better models, enterprises are giving them better *knowledge packages* - pre-built expertise that agents load on demand.

### For Claude Code users specifically

If you're using Claude Code with any Google Cloud infrastructure, installing `google/skills` means Claude already knows your environment. You tell it "deploy this to Cloud Run" and it knows what that means - the auth flow, the project structure, the common gotchas, the billing implications.

## How to Use It

code

```
# Install (Claude Code, Codex, Cursor, Gemini CLI, 30+ others)
npx skills add google/skills

# Update later
npx skills update google/skills
```

You'll be prompted to select which skills to install. For most teams, start with the skills that match your current Google Cloud stack.

The repository is open source under Apache 2.0 at [github.com/google/skills](https://github.com/google/skills). Contributions are welcome.

## What This Signals About 2026

The fact that Google shipped an official Agent Skills repo tells us something: the ecosystem has reached the threshold where major companies need an official presence in it.

The [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) directory already lists official skills from Google, Google Labs, Anthropic, Vercel, Stripe, Cloudflare, Netlify, NVIDIA, Redis, Red Hat, Trail of Bits, Sentry, Expo, Hugging Face, and Figma.

For AI builders, the implication is straightforward: the agents that win in enterprise will be the ones pre-loaded with the right skills for the infrastructure they're operating in. `google/skills` is Google's opening move in that race.

google/skills is Google's official repository of Agent Skills for Google Cloud products and technologies. It contains structured knowledge packages that AI coding agents can load on demand to work with BigQuery, Cloud Run, GKE, Firebase, AlloyDB, and other Google Cloud services.

Run npx skills add google/skills in your terminal. This works with Claude Code, Codex, Cursor, Gemini CLI, and 30+ other agent hosts. You will be prompted to select which specific skills to install based on your Google Cloud stack.

The repository includes skills for Gemini API, Cloud Run, Cloud SQL, BigQuery, AlloyDB, Firebase, GKE, plus recipe skills for onboarding and authentication, and Well-Architected Framework skills covering security, reliability, cost optimization, operational excellence, performance, and sustainability.

Yes. google/skills is released under Apache License 2.0. It is open source with contributions welcome. Google is actively asking for bug reports on skill inaccuracies and feature requests for new skills.

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
