---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-last30days-skill-real-time-research
title: 'last30days-skill: Real-Time Research for AI Agents'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/last30days-skill-real-time-research
published: '2026-06-09'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# last30days-skill: Real-Time Research for AI Agents

A GitHub repo called [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) hit 34,700+ stars and landed as the #1 trending repository on all of GitHub.

If you build with AI agents, you need to know what this is.

## What Is last30days-skill?

last30days-skill is a Claude Code skill (also works with Codex, Cursor, Copilot, Gemini CLI, and 50+ other agent hosts) that turns any AI agent into a real-time research engine.

Give it a topic. It searches Reddit, X/Twitter, YouTube, HackerNews, Polymarket, GitHub, TikTok, Instagram, and Bluesky - all at once, in parallel - then synthesizes everything into one grounded brief ranked by what real people actually engaged with.

The core insight: **Google ranks editors. last30days ranks people.**

code

```
/last30days Andrej Karpathy
```

That single command gives you what Karpathy has been doing in the last 30 days: his recent tweets, GitHub commits, YouTube appearances, Reddit discussions about his work, and Polymarket odds on anything related to him. None of that is on Google.

## Why It Blew Up

Every major AI platform is a walled garden. Google can't touch Reddit comments. ChatGPT has a Reddit deal but can't search X. Gemini has YouTube but not Reddit. Claude has none of them natively.

last30days-skill solves this by bridging all of them through a single agent command. You bring your own API keys and browser sessions, and suddenly your AI can search every platform simultaneously.

As the README puts it: "You can't get this search anywhere else because no single AI has access to all of it."

## How to Install

### Claude Code (recommended - auto-updates via marketplace)

code

```
/plugin marketplace add mvanhorn/last30days-skill
/plugin install last30days
```

### Codex, Cursor, Copilot, Gemini CLI, or any Agent Skills host

code

```
npx skills add mvanhorn/last30days-skill -g
```

The `-g` flag installs globally so it's available across all your projects.

Reddit, HackerNews, Polymarket, and GitHub work immediately with zero configuration. Run it once and the setup wizard unlocks X, YouTube, TikTok, and more in about 30 seconds.

## What People Actually Use It For

### Before a sales call or meeting

Run `/last30days [person's name]` before you meet with someone. Instead of their outdated LinkedIn, you get what they've actually been doing this month: recent tweets, GitHub commits, podcast appearances, and what communities are saying about them.

### Competitive research

`/last30days OpenAI vs Anthropic vs xAI` runs three full research pipelines in parallel, merges them, and gives you a side-by-side comparison grounded in community engagement - not press releases.

### Staying current on fast-moving topics

AI tooling changes daily. `/last30days Claude Code` tells you what the community is actually talking about right now: the bugs people are hitting, the prompts that are working, the integrations they're shipping.

### Before a purchase or trip

`/last30days Universal Epic Universe` - current wait times, what's under construction, what the community says. Real-time community knowledge, not stale blog posts.

## What's in v3 (Current Version)

The version that drove the trending spike is v3.3, with several major upgrades:

| Feature | What It Does |
| --- | --- |
| **Intelligent pre-search** | Resolves X handles, GitHub repos, subreddits, TikTok hashtags *before* searching. Type "OpenClaw" and it finds the right accounts automatically. |
| **Cross-source cluster merging** | Same story on Reddit, X, and YouTube? Merged into one result instead of three. |
| **Shareable HTML briefs** | Self-contained dark-mode HTML file you can drop into Slack or email. |
| **Best Takes** | A second AI judge scores results for humor, wit, and virality. Cleverest community one-liners surface in every brief. |
| **Single-pass comparisons** | "A vs B" runs in 3 minutes with one parallel pass (down from 12 minutes). |

## Sources It Covers

| Source | Config Required | Notes |
| --- | --- | --- |
| Reddit | None (free via public JSON) | Full comments and engagement data |
| HackerNews | None | Posts, comments, karma |
| Polymarket | None | Prediction market odds backed by real money |
| GitHub | None | Repos, PRs, issues, star counts |
| Web search | Brave API key (free tier) | General web results |
| X/Twitter | Browser session | Free via your logged-in session |
| YouTube | yt-dlp (free) | Full transcripts |
| TikTok | ScrapeCreators API | Video content and engagement |
| Instagram | ScrapeCreators API | Posts and stories |
| Bluesky | Handle + app password | AT Protocol posts |
| Perplexity Sonar | OpenRouter key | AI-enhanced web search |

## Why This Matters for AI Builders

Most AI agents have a knowledge cutoff. They can reason brilliantly about information they were trained on, but they're blind to what happened last week.

last30days-skill closes that gap not by giving the AI internet access (lots of tools do that) but by giving it *community* access - the Reddit threads where real users are venting about real problems, the X posts where builders are sharing what's actually working, the Polymarket odds where people are betting real money on outcomes.

For anyone building products in the AI space, this is the difference between knowing the official announcements and knowing what the community actually thinks.

## How to Try It Now

code

```
# Claude Code
/plugin marketplace add mvanhorn/last30days-skill

# Then run
/last30days [any topic you care about]
```

Start with something you already know well - a tool you use daily, a competitor, a trend you've been watching. See how the community signal compares to what you thought you knew.

The repo is at [github.com/mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill), MIT licensed, 34,700+ stars and climbing.

last30days-skill is an open-source Agent Skill that turns any AI coding agent into a real-time research engine. It searches Reddit, X/Twitter, YouTube, HackerNews, Polymarket, GitHub, TikTok, Instagram, and Bluesky in parallel, then synthesizes everything into a grounded brief ranked by real engagement.

In Claude Code: /plugin marketplace add mvanhorn/last30days-skill. For Codex, Cursor, Copilot, and 50+ other hosts: npx skills add mvanhorn/last30days-skill -g. Reddit, HackerNews, Polymarket, and GitHub work immediately with zero configuration.

Reddit, HackerNews, Polymarket, GitHub, and basic web search work with zero configuration. X/Twitter, YouTube transcripts, TikTok, and Instagram unlock progressively as you add optional API keys. The setup wizard guides you through in about 30 seconds.

Google ranks editors and SEO content. ChatGPT has limited Reddit access and cannot search X. No single AI has access to all social platforms simultaneously. last30days-skill bridges all of them through your agent, searching every platform in parallel and ranking results by real human engagement rather than SEO signals.

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
