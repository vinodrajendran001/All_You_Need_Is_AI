---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-18-vynnytskyi-databricks-project-structure
source_title: "Understanding Databricks: How to Structure a Databricks Project from Scratch"
source_author: Mykola-Bohdan Vynnytskyi
source_url: https://mbvyn.medium.com/understanding-databricks-how-to-structure-a-databricks-project-from-scratch-76de287671d6
tags:
  - source/summary
  - data-engineering
  - devops
  - series/understanding-databricks
source_ids:
  - src-2026-10-18-vynnytskyi-databricks-project-structure
status: active
---

# Mykola-Bohdan Vynnytskyi - Understanding Databricks - How to Structure a Databricks Project from Scratch

## Summary

Part thirteen builds a version-controlled project from an empty workspace. The central artifact is a
**Declarative Automation Bundle** (formerly Databricks Asset Bundles): a Git-versioned folder whose
`databricks.yml` manifest describes code, jobs, pipelines, artifacts, variables, and deployment targets.

The organizing principle: **"The foundation of a 2026 Databricks project is a Declarative Automation
Bundle"**, deployed idempotently — **"The bundle compared the desired state in my files with what exists
in the workspace."**

## Key claims

- **Jobs orchestrate; pipelines declare.** A job says when and in what order tasks run. A pipeline says
  **which tables should exist and how they are computed**, leaving dependency ordering and refresh order
  to the platform.
- **Idempotent deployment:** reapplying the same configuration converges without duplicating unchanged
  resources. The author's run reports `0 created, 0 changed, 0 deleted, 2 unchanged`.
- Recommended layout: `databricks.yml`, `resources/`, `src/`, `tests/`, `fixtures/`, `pyproject.toml`,
  plus `AGENTS.md` and `CLAUDE.md` emitted by the official template.
- **Notebooks are thin entry points** for parameters and results; reusable logic belongs in importable,
  testable Python modules. **`%run` chains are discouraged** in favour of module imports — the change
  that makes the code unit-testable.
- Four distinct parameter scopes: **bundle variables** resolve at deployment time, **job parameters** at
  run time, **task values** pass data between tasks, and **widgets** support interactive notebooks.
- Environment separation uses **distinct workspaces, environment-specific catalogs, bundle targets, and
  service principals for production**. Development mode can prefix resources, pause schedules, and allow
  concurrent runs.
- **Workspace-specific hosts and user identities must not be committed.** Use `${workspace.current_user.userName}`
  substitutions and a Git-ignored `databricks.local.yml` with a committed `.example`.
- CI/CD for data work is represented as Git-versioned declarative resources plus `databricks bundle
  validate`, `deploy`, and `run`.
- **[Measured, author's single run]** first public commit contained **22 files**; example materialized
  views held **22K and 128 rows**, each taking **three seconds** on serverless compute; Free Edition
  initially returned **403 PERMISSION_DENIED** for job deployment until identity verification.
- **[Self-reported, time-sensitive]** the DAB rename occurred **2026-03-16**; CLI **1.3+** required,
  author used **1.15**; the template uses `uv` and builds a wheel via `pyproject.toml`.

## Why it matters

[[Declarative Data Pipeline Deployment]] enters the vault here, and the transferable idea is the
**desired-state manifest**: the deployment artifact describes the end state, and the tool computes the
diff. That is the same convergence model this vault records in infrastructure-as-code practice, applied
to data assets.

Two details matter for agent-assisted work specifically. First, the template now ships **`AGENTS.md` and
`CLAUDE.md`** — agent instructions have become a scaffolded project file alongside tests and manifests,
which is the pattern [[Agent Skill]] and [[Coding Agent Harness]] describe from the other direction.
Second, **moving logic out of notebooks into modules is what makes a codebase legible to an agent at
all**: `%run` chains have no import graph to follow, so neither a test runner nor a coding agent can
reason about them.

The secret-hygiene point also generalizes: generated scaffolding embedded the author's workspace URL,
email, and username, and had to be scrubbed before the first commit.

## Tensions / open questions

- The layout is **explicitly opinionated** and tied to the 2026 official template; product naming, CLI
  behaviour, and template contents are expected to change.
- The performance figures come from **one demonstration on tiny tables** and are not a general
  performance claim.
- **"If it's not in the bundle, it doesn't exist"** is a rhetorical CI/CD principle, not a platform
  guarantee.
- Free Edition's job-deployment block and the one-workspace shortcut are acceptable for learning only.
- Discouraging `%run` categorically, and treating the official template as settled, are the author's
  positions rather than established practice.
- The capture contains a garbled duplicated command (`git statusgit status`), apparently a transcription
  artefact.

## Affected pages

- [[Declarative Data Pipeline Deployment]]
- [[Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]

## Raw capture

- [[Understanding Databricks How to Structure a Databricks Project from Scratch]]

## Citations

- Raw capture: [[Understanding Databricks How to Structure a Databricks Project from Scratch]]
- Canonical URL: <https://mbvyn.medium.com/understanding-databricks-how-to-structure-a-databricks-project-from-scratch-76de287671d6>
- Published 2026-10-18; captured 2026-10-23.

## Related pages

- [[Medallion Architecture]]
- [[Lakehouse Architecture]]
- [[Agent Skill]]
- [[Coding Agent Harness]]
- [[AI-Native Software Development Lifecycle]]
