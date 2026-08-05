---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-agent-skills-best-practices-guide
title: 'Anthropic''s 300+ Claude Code Skills: Lessons Learned'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/agent-skills-best-practices-guide
published: '2026-06-09'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Anthropic's 300+ Claude Code Skills: Lessons Learned

**Agent Skills** are self-contained folders of instructions, scripts, and reference files that Claude Code auto-discovers and executes. They are the most flexible extension point for Claude Code in 2026. I run 26 Skills across two directories. Anthropic maintains hundreds internally. This guide covers what actually works: which Skills are worth building, how to structure them, the mistakes that waste your time, and how to share them with a team.

Prefer to watch? Here's the full video on why Skills are eating MCP's lunch and what that means for your workflow:

## What Are Agent Skills and Why Should You Care?

A Skill is a folder. Not a Markdown file. That distinction matters.

The folder contains a `SKILL.md` file (the entry point the agent reads first), plus any combination of scripts, reference docs, config files, templates, and data. The agent discovers available Skills at session start, scans their descriptions to decide relevance, and reads the full `SKILL.md` only when it determines a Skill matches the current task.

The common misconception is that Skills are just prompt snippets. In practice, the best Skills use the entire folder as a context engineering surface. A `references/` subfolder with API docs. A `templates/` directory with scaffold files. A `config.json` the agent populates on first run. Scripts the agent can execute at runtime. The folder *is* the Skill.

Here is what my setup looks like:

| Location | Count | Purpose |
| --- | --- | --- |
| `~/.claude/skills/` | 14 | Platform Skills: PR babysitting, hook creation, canvas rendering, SDK guidance, PR splitting |
| `.claude/skills/` (project) | 12 | Domain Skills: SEO content pages, pricing pages, comparison pages, event landing pages |

That is 26 Skills the agent can reach for on any task. Not all fire on every session. The agent picks what is relevant based on descriptions and trigger words. More on that below.

Anthropic reports running "several hundred" active Skills internally for Claude Code. They cataloged them into 9 types. I mapped my own Skills against those types and the framework holds up.

## What Are the 9 Types of Skills Worth Building?

Anthropic categorized every internal Skill into 9 types. A good Skill fits exactly one. Skills that try to do everything end up confusing the agent because it cannot determine when to invoke them.

| # | Type | What It Does | My Examples |
| --- | --- | --- | --- |
| 1 | Library and API Reference | How to correctly use a specific library, CLI, or SDK | `billing-lib` (internal billing), `internal-platform-cli` (CLI subcommands) |
| 2 | Product Verification | How to test or validate that code works | - |
| 3 | Data Fetching and Analysis | Connect to data and monitoring systems | - |
| 4 | Business Process Automation | One-click repeatable workflows | `loop` (recurring task runner), `canvas` (data visualization) |
| 5 | Code Scaffolding and Templates | Generate framework templates for specific features | `seo-content-page`, `pricing-page`, `comparison-page`, all 12 landing page Skills |
| 6 | Code Quality and Review | Enforce code quality standards, assist reviews | `adversarial-review` (sub-agent code review), `testing-practices` |
| 7 | CI/CD and Deploy | Pull, push, deploy code | `babysit` (PR babysitter), `split-to-prs` (split work into reviewable PRs) |
| 8 | Runbooks | Accept a symptom, guide multi-tool investigation, output structured report | - |
| 9 | Infrastructure Ops | Day-to-day maintenance with guardrails | - |

The empty rows are not failures. They are opportunities. Verification Skills (type 2) are what Anthropic says deliver the biggest quality improvement to Claude's output. They recommend spending a full engineering week building one. I have not built one yet. That is next on my list.

Notice that 12 of my 26 Skills are type 5 (scaffolding). That is not an accident. Scaffolding Skills are the easiest to build and the most immediately useful. You already have templates and patterns you repeat. Encode them.

## How Should You Structure a Skill Folder?

Two real examples from my setup.

**Simple Skill: `babysit/`**

code

```
babysit/
  SKILL.md
```

One file. 15 lines. The entire Skill is a set of instructions: resolve merge conflicts, triage PR comments, fix CI, loop until merge-ready. No reference docs needed because the agent already knows how `git` and GitHub work. The Skill just tells it *what to do*, not *how to use the tools*.

**Complex Skill: `seo-content-page/`**

code

```
seo-content-page/
  SKILL.md
  references/
    geo-ai-patterns.md
```

The `SKILL.md` is 274 lines covering brand discovery, content requirements, page architecture, GEO optimization rules, and technical specs. But the detailed content block templates (definition blocks, step-by-step blocks, evidence sandwich patterns) live in `references/geo-ai-patterns.md`. The SKILL.md tells the agent "For detailed content block templates, see references/geo-ai-patterns.md." The agent reads it when it needs it.

This is **progressive disclosure through the file system**. Your `SKILL.md` is always loaded when the Skill fires. Reference files are loaded on demand. Put the decision-making instructions in `SKILL.md`. Put the detailed reference material in subfolders. The agent manages its own context window this way.

Anthropic calls this out as the single most underused pattern. Most builders cram everything into one Markdown file because they think that is all a Skill is. Use the folder.

## What Makes a Skill Description Actually Work?

The description field is not documentation for humans. It is a trigger signal for the model.

When a session starts, the agent builds an index of all available Skills and their descriptions. When you make a request, the agent scans that index to decide: "Does any Skill match what this person is asking for?" The description determines whether the Skill fires or sits idle.

**Bad description:**

code

```
Creates SEO pages
```

Four words. No trigger signals. The agent might match it on "SEO" but will miss "blog post", "content article", "keyword-targeted page", or "GEO optimization."

**Good description (from my `seo-content-page` Skill):**

code

```
Build on-brand SEO content pages optimized for both traditional search
engines and AI search (ChatGPT, Gemini, Perplexity) with GEO (Generative
Engine Optimization), E-E-A-T signals, answer-first structure, and
hub-and-spoke internal linking. Use when the user wants to create an SEO
page, blog post, topic page, content article, spoke article,
keyword-targeted page, AI-optimized content page, GEO page, or any
organic search content piece.
```

Nine explicit trigger phrases. The model now matches on "blog post", "topic page", "spoke article", "keyword-targeted page", and "GEO page" in addition to "SEO." The "Use when the user wants to..." sentence is the most valuable part. It tells the model exactly when to activate.

Another good example from Anthropic's internal `sandbox-proxy` Skill:

code

```
Configure egress gateway for sandbox environments. Use when the user
mentions proxy settings, allowed hosts, connection debugging, allowlist,
sandbox networking, or egress rules.
```

It lists the specific terms an engineer would type when hitting a networking issue. That level of specificity is what separates a Skill that works from one that never gets invoked.

## What Is a Gotchas List and Why Does Every Skill Need One?

Anthropic says the highest-information-density section in any Skill is the gotchas list. I agree. This is where you capture the things the model gets wrong repeatedly when working in your domain.

The model already knows how to write code. It already knows most libraries. A Skill that just repeats what the model already knows adds context weight without adding value. The gotchas list is where you push the model out of its default assumptions.

Examples from Anthropic's internal Skills:

- "The `subscriptions` table is append-only. You want the row with the highest `version`, not the most recent `created_at`."
- "This field is called `@request_id` in the API gateway but `trace_id` in the billing service. They are the same value."
- "Staging returns 200 for Stripe webhooks even when they are not actually processed. Check the `payment_events` table for real status."

Each of these would cause a subtle bug if the model followed its default pattern. The gotchas list prevents that by injecting domain-specific knowledge at the exact moment the model needs it.

For my landing page Skills, the equivalent is design taste. The `seo-content-page` Skill includes specific GEO optimization rules that override the model's defaults:

- Lead every section with a direct answer in the first 40-60 words (the model's default is to build up to the answer)
- Structure H2s as questions, not statements (maps to People Also Ask and AI query patterns)
- Keyword stuffing actively reduces AI visibility by 10% (the model sometimes defaults to keyword-heavy copy)

Without these, the model produces generic SEO content. With them, it produces content optimized for AI citation.

## What Are the Most Common Mistakes When Building Skills?

**1. Telling the model what it already knows.**

Do not write a Skill that says "Use TypeScript for type safety" or "Follow REST conventions for API endpoints." The model already does this. Every line of your Skill that repeats default model behavior is wasted context and diluted signal.

Focus on what makes *your* codebase, *your* workflow, or *your* domain different from the default.

**2. Over-constraining the agent.**

Skills are highly reusable. A Skill written for one specific scenario breaks when the context shifts. Give the agent the information it needs, then let it adapt. Write rules, not scripts. Write principles, not step-by-step instructions for every edge case.

My `babysit` Skill is 15 lines. It says "resolve merge conflicts preserving intent on both branches" and "fix CI issues within this PR's scope." It does not specify *how* to resolve any particular conflict. The agent figures that out from context.

**3. Cramming everything into one Markdown file.**

Use the folder. Put reference docs in `references/`. Put templates in `templates/`. Put scripts in `scripts/`. The agent navigates file systems. Let it.

**4. Skipping the initialization flow.**

Some Skills need user context before they work. My `seo-content-page` Skill starts with a brand discovery phase: "Do you have an existing website? Share the URL so I can match your brand." Without this, the Skill generates generic output.

A good pattern is storing configuration in a `config.json` inside the Skill directory. If the config does not exist yet, the agent asks the user for the missing information and creates it. Next time, it reads the config and skips the questions.

**5. Writing descriptions for humans instead of models.**

Your description is not a README summary. It is a trigger function. Load it with the exact words and phrases a user would type when they need this Skill. "Use when the user wants to..." followed by a list of trigger phrases. This is the difference between a Skill that fires reliably and one that never activates.

## How Do On-Demand Hooks Make Skills More Powerful?

Skills can register Hooks that only activate when the Skill is invoked, and only for the current session. This is the "paranoid mode" pattern. You do not want these running all the time. But when you need them, they are invaluable.

Anthropic gives two examples:

**`/careful` mode** - A PreToolUse hook that intercepts destructive operations: `rm -rf`, `DROP TABLE`, `force-push`, `kubectl delete`. You only activate this when touching production infrastructure. The rest of the time, it is off.

**`/freeze` mode** - A hook that blocks all Edit/Write operations outside a specified directory. Useful for debugging: "I want to add a log statement, but the agent keeps 'fixing' unrelated code in other files." Freeze locks the agent to the directory you care about.

In Claude Code, Skills can include Hooks that register dynamically when invoked. These are triggered by agent events like `PreToolUse` and `PostToolUse`. The Skill activates its hooks at invocation time, scoped to the current session only.

## How Should You Share Skills With a Team?

Two distribution paths depending on your team size.

**Path 1: Commit to the repository.**

Place Skills in `.claude/skills/` inside your repo. Everyone who clones the repo gets the Skills. Simple. Works for small teams with a handful of shared repositories.

**Path 2: Plugin marketplace.**

Claude Code has a plugin marketplace where you can publish Skills for anyone on your team to install. This scales better because each engineer chooses which Skills to install, and you can add onboarding flows (initial configuration, credential setup).

The trade-off is context budget. Every installed Skill adds to the index the model scans at session start. More Skills means more noise in that index. For a small team, 20-30 well-described Skills is fine. At scale, curation matters.

Anthropic's internal approach: no central gatekeeper. Anyone can upload a Skill to a sandbox directory and share it in Slack. When a Skill accumulates enough usage (author's judgment), it gets promoted to the marketplace via a PR. The best Skills surface naturally.

For personal Skills that should not be shared (your own workflow shortcuts, personal preferences), use `~/.claude/skills/`. These are local to your machine and never committed to a repo.

## How Do You Measure Whether Skills Are Working?

Anthropic uses a PreToolUse Hook to log every Skill invocation across their org. This surfaces which Skills are popular, which ones have low trigger rates (bad descriptions), and which ones are never used (candidates for removal).

You can implement the same pattern. A simple approach:

1. Create a Hook that fires on Skill invocation
2. Append a line to a log file: timestamp, Skill name, session ID
3. Review the log weekly

If a Skill you expected to fire frequently is not showing up, the problem is almost always the description. Add more trigger phrases. If a Skill fires but users report bad output, the problem is in the instructions or the gotchas list.

For individual use, a lighter approach works: check your Skill folder's `SKILL.md` access patterns. If you have 26 Skills and only 8 fire regularly, the other 18 either have description problems or solve problems you do not actually encounter.

## How Do You Combine Multiple Skills?

You might want one Skill to reference another. There is no native dependency management for this yet. The workaround is simple: mention the other Skill by name in your `SKILL.md`. If it is installed, the model will invoke it.

For example, a deploy Skill might reference a verification Skill: "After deployment, run the `checkout-verifier` Skill to confirm the payment flow works." The model reads this, checks if `checkout-verifier` is available, and invokes it.

This is fragile in the sense that it breaks silently if the referenced Skill is not installed. Document the dependency clearly so engineers know what to install.

## How Do You Give Skills Memory?

Some Skills benefit from remembering past executions. The simplest pattern: write a log file inside the Skill directory.

Anthropic's example is a `standup-post` Skill that maintains a `standups.log`. Each time it runs, it appends the generated standup. Next invocation, it reads the log to understand what changed since yesterday.

Any format works:

- Append-only text log (simplest)
- JSON file (structured, queryable)
- SQLite database (complex queries, multiple tables)

The agent reads and writes these files like any other file operation. No special API needed. The Skill's `SKILL.md` just tells the agent where the log lives and how to use it.

## Key Takeaways

- **A Skill is a folder, not a Markdown file.** Use the file system for progressive disclosure. Put instructions in `SKILL.md`, reference material in subfolders.
- **Good Skills fit exactly one of the 9 types.** Multi-category Skills confuse the agent. Scaffolding Skills (type 5) are the easiest to start with.
- **The description is a trigger signal, not a summary.** Load it with the exact phrases users type. "Use when the user wants to..." is the most important sentence.
- **Gotchas lists are the highest-value section.** Capture what the model gets wrong in your domain. Skip everything the model already knows.
- **Do not over-constrain.** Give the agent rules and principles, not rigid step-by-step scripts. Let it adapt to context.
- **On-demand Hooks add paranoid-mode safety.** Register them per-session for destructive operations or directory freezing.
- **Share via repo for small teams, marketplace for large ones.** Every Skill adds to the context budget. Curate as you scale.

## Start Building Your First Skill

The fastest way to start: pick a workflow you repeat weekly. Write a `SKILL.md` that encodes the steps, gotchas, and decision points. Drop it in `~/.claude/skills/your-skill-name/`. Test it in your next session.

For more patterns, teardowns, and production examples, join the AI Builder Club. We cover agent customization, Skills architecture, and workflow automation in weekly workshops.

[Join AI Builder Club](https://www.aibuilderclub.com)

An Agent Skill is a folder containing a SKILL.md file plus optional scripts, templates, and reference documents. Claude Code auto-discovers Skills at session start and invokes them when they match the current task. They extend the agent's capabilities with domain-specific knowledge, workflows, and tooling.

Place personal Skills in ~/.claude/skills/ and project-level Skills in .claude/skills/ inside your repo. Claude Code scans both directories automatically at session start. Personal Skills are local to your machine. Project Skills are shared with anyone who clones the repo.

There is no hard limit, but each Skill adds to the index the model scans. At 20-30 well-described Skills, the system works well. Beyond that, description quality becomes critical because the model needs to quickly differentiate between similar Skills. Anthropic runs hundreds internally, but they use a marketplace model where engineers install only the ones they need.

CLAUDE.md is always-on project context loaded into every session. Skills are invoked on-demand when the agent determines they match the current task. Use CLAUDE.md for coding standards, project conventions, and facts that apply everywhere. Use Skills for workflows, scaffolding, and multi-step processes the agent should run only when asked.

Yes. Skills can include executable scripts in their folder, and the agent can run them. Skills can also reference MCP servers, CLI tools, and external APIs. Anthropic's verification Skills use Playwright for browser testing and tmux for interactive CLI sessions. The folder structure means you can bundle any supporting files the agent needs.

The SKILL.md format has been adopted across multiple tools. Cursor uses a similar skills system with its own discovery mechanism, and OpenAI Codex has adopted the SKILL.md spec. The skills themselves are portable Markdown folders. Claude Code has the richest feature set with Hooks registration and a plugin marketplace.

Start with a scaffolding Skill (type 5). Pick a template or boilerplate you create repeatedly, encode it as a Skill with a clear description and a gotchas list, and test it. Then build a verification Skill (type 2) for your most critical user flow. Anthropic says verification Skills deliver the biggest quality improvement to agent output.

The problem is almost always the description. Add more trigger phrases, especially the exact words users type when they need the Skill. Test by explicitly asking the agent to use the Skill by name, then check if it reads the SKILL.md. If it reads the file but produces bad output, the issue is in the instructions or missing gotchas.

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
