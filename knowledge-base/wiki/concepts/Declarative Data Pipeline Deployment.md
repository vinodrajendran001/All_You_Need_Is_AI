---
type: concept
created: 2026-10-23
updated: 2026-10-23
tags:
  - concept
  - data-engineering
  - devops
  - tooling
source_ids:
  - src-2026-10-18-vynnytskyi-databricks-project-structure
  - src-2026-06-01-vynnytskyi-databricks-core-components
status: active
---

# Declarative Data Pipeline Deployment

## Definition

Treating data assets — jobs, pipelines, tables, endpoints, permissions — as **version-controlled
desired-state declarations** rather than as objects created by hand in a web UI. A manifest describes
what should exist; the tool computes the diff against reality and converges.

From [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - How to Structure a Databricks Project from Scratch]]:
**"The bundle compared the desired state in my files with what exists in the workspace."**

## Why it matters

Two distinct ideas get bundled under "declarative" here, and separating them is useful:

1. **Declarative deployment** — the infrastructure-as-code convergence model, where reapplying the same
   configuration is **idempotent** and produces no duplicates. The observed output `0 created,
   0 changed, 0 deleted, 2 unchanged` is the whole contract in one line.
2. **Declarative computation** — the distinction between **jobs** (orchestrate *when* and in *what
   order* tasks run) and **pipelines** (declare *which tables should exist and how they are computed*,
   letting the platform derive dependencies and refresh order). The second surrenders control of
   execution order in exchange for the platform maintaining the dependency graph.

## Current synthesis

### Why this matters for agent-assisted work

Two details in the vault's source have direct consequences beyond data engineering.

**Agent instructions have become scaffolded project files.** The official template now emits `AGENTS.md`
and `CLAUDE.md` alongside tests, manifests, and a package definition. Agent context has moved from
something a developer writes ad hoc into something a project generator produces by default — the same
pattern [[Agent Skill]] and [[Coding Agent Harness]] describe from the other side.

**Moving logic out of notebooks is what makes a codebase legible to an agent at all.** The source's
recommendation — notebooks as thin parameter-and-result entry points, reusable logic in importable
modules, and `%run` chains discouraged — is usually justified by testability. The stronger justification
is structural: a `%run` chain has **no import graph**, so neither a test runner nor a coding agent can
determine what depends on what. Notebook-first codebases are opaque to exactly the tooling
[[AI-Native Software Development Lifecycle]] assumes.

### Structure and parameter scopes

Recommended layout separates **resource definitions**, **application code**, **tests**, **test
fixtures**, and a **package manifest**, with a top-level bundle manifest connecting them.

Four parameter scopes resolve at different times, and conflating them is a common source of confusion:

| Scope | Resolves at |
|---|---|
| Bundle variables | Deployment time |
| Job parameters | Run time |
| Task values | Between tasks within a run |
| Widgets | Interactive notebook use |

### Environment separation and hygiene

Separation uses **distinct workspaces, environment-specific catalogs, deployment targets, and service
principals for production**. Development mode can prefix resources, pause schedules, and permit
concurrent runs; production mode is for controlled deployments.

A practical secret-hygiene lesson worth generalizing: the **generated scaffolding embedded the author's
workspace URL, email, and username**, which had to be scrubbed before the first commit. Workspace hosts
and identities belong in a Git-ignored local override with a committed example file, referenced through
substitutions.

## Open questions

- The project layout is **explicitly opinionated** and tied to one vendor's 2026 template; naming, CLI
  behaviour, and template contents are expected to change. The durable part is the desired-state model
  and the jobs-versus-pipelines distinction.
- **"If it's not in the bundle, it doesn't exist"** is a rhetorical CI/CD principle, not a platform
  guarantee — manual changes remain possible and will be silently reconciled or clobbered.
- The vault's only performance figures here are from **one demonstration on tiny tables** (22K and 128
  rows, three seconds each) and are not a general performance claim.
- Discouraging `%run` categorically is the author's position; the vault has no evidence about the
  migration cost for existing notebook-heavy codebases.
- When the platform derives refresh order, what is the debugging story when it derives it wrongly?

## Related pages

- [[Lakehouse Architecture]]
- [[Medallion Architecture]]
- [[Agent Skill]]
- [[Coding Agent Harness]]
- [[AI-Native Software Development Lifecycle]]
- [[All_You_Need_Is_AI/knowledge-base/wiki/entities/Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - How to Structure a Databricks Project from Scratch]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Core Components]]
