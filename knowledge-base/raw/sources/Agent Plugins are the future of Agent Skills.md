---
title: "Agent Plugins are the future of Agent Skills"
source: "https://x.com/GoogleCloudTech/status/2087733334617063503"
author:
  - "[[@GoogleCloudTech]]"
published: 2026-08-13
created: 2026-08-17
description: "Agent Plugins is an open, vendor-neutral standard for packaging Agent Skills and the MCP servers they depend on into one portable folder tha..."
tags:
  - "clippings"
---
![Image](https://pbs.twimg.com/media/HPkeUsWXsAAgdAy?format=jpg&name=large)

[Agent Plugins](https://agent-plugins.org/) is an open, vendor-neutral standard for packaging Agent Skills and the MCP servers they depend on into one portable folder that any compatible client can load. Google is joining the Technical Steering Committee as a Core Maintainer. The [launch post](https://developers.googleblog.com/agent-plugins-package-your-skills-tools-and-more/) covers the announcement, and the [specification](https://agent-plugins.org/specification) carries the detail. This is what we learned putting real skills through it.

Agent Skills gave agents on-demand expertise. A folder of instructions the model pulls in only when a task matches, so your context window isn't carrying a deployment runbook while you fix a CSS bug. We've leaned on that hard, in the [google/skills](https://github.com/google/skills) repository and the seven skills that ship with [Agents CLI](https://google.github.io/agents-cli/guide/getting-started/).

What Skills never solved is distribution.

**By** [@lavinigam](https://x.com/@lavinigam)**, Developer Relations Engineer, Google Cloud**

![Image](https://pbs.twimg.com/media/HPkaks2XcAAhErQ?format=jpg&name=large)

A skill that needs a tool is two artifacts. Instructions live in SKILL.md, the tool lives in an MCP server, and nothing ties them together. So the binding lived in a README: copy this here, add that JSON block there, a different snippet per client. Every client invented its own bundle format to fix it, so authors picked one and rewrote for the next.

Agent Plugins standardizes the box. The components inside it were already portable.

Here's what changes when your skill becomes a plugin, and why you've already built most of one:

- **The one file you're missing.** Your folder is already the right shape.
- **Your tools travel with your expertise.** mcp.json, and paths that survive the trip.
- **Components fail independently.** A dead server doesn't take your skills down.
- **Client-specific behaviour without forking.** The extension namespace.
- **One folder, every client.** What we shipped, and where it actually runs.

## The one file you're missing

If you've written an [ADK skill](https://adk.dev/skills/), look at where it lives: skills/\<name>/SKILL.md, with scripts/, references/ and assets/ underneath. Agent Plugins asks for skills/\<dir>/SKILL.md and defers the inside of that folder to the [Agent Skills specification](https://agentskills.io/specification). It's the same tree.

Here's a skill we'd already written, unchanged by packaging:

```text
---
name: summarize-report
description: Summarize a quarterly revenue report into an executive brief.
  Use when the user asks to summarize, condense, or brief a financial report.
---

# Summarize a revenue report

## Steps

1. Fetch the report with the \`reports\` MCP server's \`fetch_report\` tool.
2. Load \`references/house-style.md\` and follow its tone rules.
3. Produce three sections: Headline, Numbers That Moved, Risks.
4. Keep the brief under 300 words.

## Rules

- Never estimate a figure the report does not state.
- Quote every percentage with its comparison period.
- If a quarter is missing, say so rather than interpolating.
```

Note what line 1 of the Steps assumes: a running MCP server. That dependency is the thing packaging fixes.

The migration is one file at the root:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "acme.reports"
}
```

Both fields are required, and that's the whole minimum. Names run 1 to 64 characters of lowercase alphanumerics, hyphens and periods, must start and end alphanumeric, and can't contain -- or ... So acme.reports is fine, while My-Plugin, -start and has--double are not.

When you're ready to publish rather than test, the manifest takes metadata too. The schema is closed: ten top-level fields are permitted and nothing else ([full field reference](https://agent-plugins.org/plugin-authors/manifest)).

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "acme.reports",
  "version": "1.2.0",
  "description": "Revenue reporting skills and the MCP server they call.",
  "author": { "name": "Acme Data", "url": "https://acme.example" },
  "homepage": "https://acme.example/reports-plugin",
  "repository": "https://github.com/acme/reports-plugin",
  "license": "Apache-2.0",
  "keywords": ["reports", "finance", "bigquery"]
}
```

That's nine of the ten. The last is extensions, for client-specific data, which comes later. author also takes an optional email.

version should be SemVer and license should be SPDX, though a client won't reject you for malformed strings. Wrong JSON types are a different matter: a number where a string belongs is fatal even on an optional field. Exactly two schema violations are non-fatal, an unknown top-level field and an extensions value that isn't an object. Both get reported and ignored, and the plugin still loads. Everything else is fatal and the client refuses the whole package.

One rule catches people migrating to a large skills library. Discovery goes exactly one level deep: clients read the immediate subdirectories of skills/ and don't recurse ([discovery rules](https://agent-plugins.org/client-implementers/loading-and-discovery)). If you've been grouping skills into category folders, those skills stop existing the moment you package them, with no error explaining why.

![Image](https://pbs.twimg.com/media/HPkaw9oWUAAeWgM?format=jpg&name=large)

## Your tools travel with your expertise

mcp.json sits beside your manifest and declares the servers your skill needs. It carries only two top-level keys, and every server declares its transport explicitly:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "reports": {
      "type": "stdio",
      "command": "./bin/reports-server",
      "args": ["--cache", "${PLUGIN_DATA}/cache"],
      "env": { "TEMPLATES": "${PLUGIN_ROOT}/templates" },
      "cwd": "${PLUGIN_DATA}"
    },
    "deployment-api": {
      "type": "streamable-http",
      "url": "https://deploy.example.com/mcp",
      "headers": { "X-Tenant": "public-tenant" }
    }
  }
}
```

Three transports exist, and the required fields differ ([MCP server reference](https://agent-plugins.org/plugin-authors/mcp-servers)):

```text
stdio             type, command      + optional args, env, cwd
streamable-http   type, url          + optional literal headers
sse               type, url          deprecated; client support optional
```

command is one executable token, not a shell command. Either a bare name resolved by platform search rules, or a plugin-relative path starting with ./. Placeholder expansion deliberately does not apply to it, so a bundled binary is found by that ./ path and nothing else.

The two placeholders are environment variables the client provides to stdio subprocesses, and the difference between them matters more than the names suggest:

```text
${PLUGIN_ROOT}    absolute path to the plugin. Read your templates,
                  configs and bundled assets from here.

${PLUGIN_DATA}    a writable directory that survives plugin updates.
                  Caches, indexes and local state go here
```

Write into PLUGIN\_ROOT and your state disappears the next time someone updates the plugin. Both expand in args, env values and cwd only. Not in environment keys, not in command, not in remote URLs, and not in headers. Expansion is textual and single-pass, so nothing nests.

Headers are literal package data that anyone who downloads your plugin can read, which is why the spec forbids putting credentials in them. Agent Plugins 1.0.0 defines [no portable OAuth or credential-reference field](https://agent-plugins.org/plugin-authors/mcp-servers) at all. Authentication stays client-managed.

![Image](https://pbs.twimg.com/media/HPkbSvhWkAAQp3S?format=jpg&name=large)

## Components fail independently

If your MCP server can't start, your skills still load. The spec requires the client to keep loading everything else, and says it should report the failure rather than swallow it. For an entry that is invalid or declares a transport the client doesn't support, the spec goes further: the client must skip that entry and carry on.

Failure is scoped at three levels ([failure boundaries](https://agent-plugins.org/specification)), and knowing which one you've hit is most of the debugging:

```text
Manifest invalid          → whole plugin rejected, nothing loads
mcp.json invalid          → all MCP disabled, skills still load
One server unreachable    → that entry disabled, other servers load
```

Absence is tolerated too. A plugin with no mcp.json isn't broken, because a missing component location is not an error. A location in the wrong form, like mcp.json as a directory, invalidates that component type while the rest keeps loading.

```text
reports-plugin/
├── plugin.json                  ✅ loads
├── skills/summarize-report/     ✅ loads
└── mcp.json
    ├── reports                  ✅ connected
    └── deployment-api           ❌ unreachable → reported, skipped
```

This is the difference between a bundle and a package format. A bundle is all-or-nothing. A package format degrades in parts, which is the only reason it's safe to hand someone a folder containing both your instructions and a server that has to reach the network.

![Image](https://pbs.twimg.com/media/HPkboxQXEAAO_NT?format=jpg&name=large)

## Client-specific behavior without forking

Hooks, commands, subagents and rules aren't in v1. They're too client-specific to standardise without freezing someone's roadmap. Rather than forcing a lowest common denominator, the spec hands each client a [namespace it owns](https://agent-plugins.org/plugin-authors/client-extensions).

A client namespace can appear as a reverse-domain directory at the root, as a key under extensions in the manifest, or both. Neither one requires the other.

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "acme.reports",
  "extensions": {
    "com.example.client": { "autoActivate": true }
  }
}
```

```text
reports-plugin/
├── plugin.json
├── skills/
├── mcp.json
└── com.example.client/
    └── hooks/
```

Clients ignore namespaces they don't recognise, so the portable core stays portable. The same mechanism could re-fragment plugins one directory down if every client leans on its own namespace instead of the core, which is the thing to watch as v2 gets debated.

![Image](https://pbs.twimg.com/media/HPkb5fDWYAARjuI?format=jpg&name=large)

## One folder, every client

Two Google products ship as Agent Plugins today. [Agents CLI](https://google.github.io/agents-cli/guide/getting-started/) packages our expert skills for agent building, evaluation, deployment, observability and publishing. The [Data Agent Kit](https://github.com/GoogleCloudPlatform/data-agent-kit) brings Spanner, Cloud SQL and AlloyDB plugins, plus a starter pack covering BigQuery, into whichever coding agent you already use.

In Antigravity CLI that is one command:

```shell
agy plugin install https://github.com/GoogleCloudPlatform/data-agent-kit
```

Every other client still has its own installer, which is the gap the spec is closing:

```shell
# Claude Code — marketplace, then plugin, then reload
claude plugin marketplace add GoogleCloudPlatform/data-agent-kit
claude
  /plugin install <plugin-name>@data-agent-kit   # in-session
  /reload-plugins                                # in-session

# Codex — marketplace, then plugin
codex plugin marketplace add GoogleCloudPlatform/data-agent-kit
codex plugin add <plugin-name>@data-agent-kit
```

The set of clients that read the portable format is growing, and it is published and kept current at [agent-plugins.org/compatible-clients](https://agent-plugins.org/compatible-clients).

One caution from doing this ourselves. Conformance permits partial implementations: a client must support at least one of stdio and streamable-http and should support both, while sse is optional. Build on either modern transport and you are safe across everything listed today, but test your plugin in a second client before you promise it works there.

## Deciding what to package

Not everything needs a plugin. A single skill with no tools is fine as a skill. One server for one client is simpler as a plain MCP config. Reach for a plugin when instructions and tools have to arrive together, in more than one place.

![Image](https://pbs.twimg.com/media/HPkcPJRWwAArEpx?format=jpg&name=large)

## When it doesn't load

Every failure we hit was silent in practice, though only the first is silent by design: a directory nested too deep is never discovered, so there's nothing for a client to report. For an invalid SKILL.md the spec says the client should report it, and the clients we tried didn't. Each has a distinct signature:

```text
Skill missing, no error          nested deeper than skills/<dir>/SKILL.md
Skill missing, still no error    SKILL.md lacks name or description frontmatter
No tools at all                  invalid top-level mcp.json disabled all MCP
One tool missing                 that server entry unreachable or invalid
Nothing loads                    wrong JSON type on a required manifest field
Binary not found                 placeholder used in command, which never expands
State lost on update             writes went to PLUGIN_ROOT instead of PLUGIN_DATA
```

There's no standard validator yet. The project's non-normative [future-considerations doc](https://github.com/agentplugins/agent-plugins-spec/blob/main/FUTURE_CONSIDERATIONS.md) floats a plugin linter, and conformance test suites aimed at client implementations, as things a future version may define. Nothing is committed. For now the check is loading the plugin in a real client and reading the diagnostics.

## What doesn't travel yet

Credentials are the first gap. Plugins must not embed secrets, and there's no portable field to reference them either, so anything behind an authenticated gateway still needs per-client setup. The folder moves; the authentication stays behind.

The second is naming collisions with formats that already exist. [Claude Code](https://docs.claude.com/en/docs/claude-code/plugins) uses .claude-plugin/plugin.json and .mcp.json. [Antigravity](https://antigravity.google/docs/cli/plugins) uses mcp\_config.json. These sit next to the portable layout rather than inside it. Expect a transition period where a repo carries both, and check which one a client is actually reading before you debug a plugin that was never loaded.

Two status notes worth carrying: [ADK's Skills support](https://adk.dev/skills/) is still experimental (Python v1.25.0, TypeScript v0.6.1, Go v1.2.0), and [Agent Plugins 1.0.0](https://agent-plugins.org/specification) is published as a Working Draft.

## Get started today

Build a valid plugin in about a minute:

```shell
mkdir -p acme-reports/skills/summarize-report
cd acme-reports

cat > plugin.json <<'JSON'
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "acme.reports"
}
JSON

cat > skills/summarize-report/SKILL.md <<'MD'
---
name: summarize-report
description: Summarize a quarterly revenue report into an executive brief.
  Use when the user asks to summarize, condense, or brief a financial report.
---
Produce three sections: Headline, Numbers That Moved, Risks.
Keep it under 300 words.
MD
```

Then work outward from there:

1. **Convert something real.** Point it at a skill you've already written. Check nothing sits deeper than one level under skills/.
2. **Add its tools.** Write mcp.json. Use a ./ path for a bundled binary, ${PLUGIN\_ROOT} for assets you ship, and ${PLUGIN\_DATA} for anything you write.
3. **Open it in a second client** and confirm what actually loaded, not what should have.
4. **Add publishing metadata** once it works: version, license, repository, keywords.
5. **Install ours**, [Agents CLI](https://google.github.io/agents-cli/guide/getting-started/) and the [Data Agent Kit](https://github.com/GoogleCloudPlatform/data-agent-kit), and read the [specification](https://agent-plugins.org/specification)

If you liked this article, don’t miss out on our previous article [7 rules for self-improving agent loops every AI engineer should know](https://x.com/GoogleCloudTech/status/2086874630032073142). And follow along for more.