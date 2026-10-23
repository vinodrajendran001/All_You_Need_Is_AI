---
title: "Understanding Databricks: How to Structure a Databricks Project from Scratch"
source: "https://mbvyn.medium.com/understanding-databricks-how-to-structure-a-databricks-project-from-scratch-76de287671d6"
author:
  - "[[Mykola-Bohdan Vynnytskyi]]"
published: 2026-10-18
created: 2026-10-23
description: "From an empty workspace to a deployed, version-controlled project, with every command and screenshot. Updated October 2026."
tags:
  - "clippings"
---
## From an empty workspace to a deployed, version-controlled project, with every command and screenshot. Updated October 2026.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*WQBRRfOz2nhu2o8O-PQ7dw.png)

This one still makes me wince. Years ago a small client came to us wanting a data platform on Databricks. I was young and naive, AI assistants didn’t exist yet, nobody had agreed on how a Databricks project should look, and, most importantly, none of us had ever worked with Databricks. Fake it till you make it, right?

To be fair, an engineer with solid fundamentals and a real wish to make the client happy can get surprisingly far. We connected a dozen sources, set up Git, CI/CD, and infrastructure as code, everything by the book. The client was happy. But look inside the core of that project and it was chaos. There was no agreed structure, everyone wrote code the way they felt like, and most of it lived in kilometer-long notebooks. When the project ended up on my shoulders, I spent three more months refactoring it, with almost no visible benefit for the client.

Not the best story to open with, I know. But since then I’ve seen and consulted on a lot of projects, and the worst part is that mine wasn’t a one-off. Most teams run this huge, robust platform at maybe one percent of its potential.

That’s why Understanding Databricks moves from theory to practice, starting today: so you don’t repeat the mistakes I made, and you know how a Databricks project should actually be built.

In 2026 the platform finally has an official, opinionated answer to “how should my project look,” and it takes one command to get it. So instead of describing a structure in theory, I built one from zero on a fresh Databricks Free Edition workspace and recorded every step: the commands, the real output, what broke, and the three things in the official template I had to fix before I could make the repo public.

This is also the first hands-on article of the series. The project we create today is the one we’ll keep growing through the Bronze, Silver, and Gold layers, testing, and CI/CD, and it lives in a [public repo](https://github.com/mbvyn/understanding-databricks) you can clone.

This article is part of the Understanding Databricks series. If you’re new to the platform, start with [What Is Databricks](https://medium.com/@mbvyn/understanding-databricks-what-it-is-and-why-it-matters-b0c922760785).

> ***Key takeaways***
> 
> \- The foundation of a 2026 Databricks project is a Declarative Automation Bundle (DAB, renamed from “Databricks Asset Bundles” in March 2026): code, jobs, pipelines, and target environments in one deployable, version-controlled folder.
> 
> \- One command scaffolds it: `databricks bundle init default-python` generates `databricks.yml`, `resources/`, `src/`, `tests/`, a uv-built wheel, and even `AGENTS.md` instructions for AI coding agents.
> 
> \- The template hardcodes your workspace URL and email into the config. Strip them out before you push: `${workspace.current_user.userName}` plus a git-ignored local override file.
> 
> \- Deploys are idempotent: run `bundle deploy` twice and the second run reports `0 created, 0 changed`. That's the whole argument against clicking jobs together in the UI.
> 
> \- Jobs orchestrate, pipelines transform. The template’s job literally runs the pipeline as one of its tasks.
> 
> Everything here works on Free Edition, with one catch: jobs won’t deploy until you verify your identity.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*jn7Jc62gZCtHnPqfpuXRoA.png)

## Why This Is Suddenly a 2026 Topic

Project structure used to be a religious debate. Every team had its own layout, its own deploy scripts, its own opinion about notebooks. What changed is that Databricks picked a side and shipped it.

The center of gravity is the bundle. A Declarative Automation Bundle describes your whole project declaratively: source code, Lakeflow Jobs, pipelines, dashboards, even Genie Agents and Lakebase instances, plus which workspace each environment deploys to. The name is new since March 16, 2026 (the template now greets you with it, as you’ll see in a minute), but the tool matured over two years. You can define bundles in Python instead of YAML, edit and deploy them from the workspace UI, and the CLI, now in its 1.x versions, plans and deploys faster than ever.

And there’s a reason this stopped being optional, which I didn’t fully appreciate until I opened the generated files. The official template now ships an `AGENTS.md`, a set of instructions for AI coding agents working on your project, plus a `CLAUDE.md` that points to it. Databricks expects agents like Genie Code to read and change your project. Agents operate on what they can read: declarative, versioned files. A job that exists only as clicks in the UI is invisible to the tools that are about to matter most.

> ***Take Your Databricks Prep to the Next Level***
> 
> *If you are serious about mastering Databricks and preparing for certification, check out my practice exams on Udemy:*
> 
> [*Databricks Data Engineer Professional: 300+ Practice Questions*](https://www.udemy.com/course/databricks-data-engineer-professional-300-practice-question/?referralCode=04CA66473BF290882536) *— Exam-grade questions covering Delta Lake, Structured Streaming, and production data engineering scenarios*
> 
> [*Databricks Data Engineer Associate: 5 Practice Tests (2026)*](https://www.udemy.com/course/databricks-data-engineer-associate-5-practice-tests-2026/?referralCode=E930A2DCEDFBDCFA0374) *— Five full-length practice tests aligned to the latest exam blueprint with detailed explanations*
> 
> [*Databricks GenAI Engineer Associate: 5 Practice Tests (2026)*](https://www.udemy.com/course/databricks-genai-engineer-associate-5-practice-tests-2026/?referralCode=48CC75361435DC8F7F48) *— Five practice tests covering Mosaic AI, RAG, model serving, and GenAI workflows on Databricks*
> 
> *These tests are designed to challenge you in the same way the real exam will.*

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*vF1bTrK7OGIN4CrQ2jFAtw.png)

## One Command to Start

I started from a completely empty Free Edition workspace. If you want to follow along, [Free Edition](https://www.databricks.com/learn/free-edition) costs nothing and needs no credit card.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Bnb0pBmsxiRO9biBU02l2w.png)

You need two tools locally: the Databricks CLI (1.3 or newer; I used 1.15) and uv, the Python package manager the official template builds with.

```c
brew install databricks/tap/databricks uv
databricks -v
```
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*8L9oDUAdnripbkxRuR_BsA.png)

Then log in. The CLI opens your browser for OAuth, so there’s no personal access token to copy around and eventually leak. Naming the profile up front saves you from a prompt:

```c
databricks auth login --host https://<your-workspace>.cloud.databricks.com --profile hands-on
databricks auth profiles
```
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*BDXvAb34OlCs1DRa5mP2jA.png)

Now the one command that matters:

```c
databricks bundle init default-python
```
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*O9W4Aa8LE3Kki4vgrO_yUQ.png)

Look at the first line: “Welcome to the default Python template for Declarative Automation Bundles.” Then six questions. I said yes to the sample job, the ETL pipeline, the Python wheel, and serverless compute. The default catalog on Free Edition is `workspace`, so I kept it.

The last question deserves a pause: “Use a personal schema for each user working on this project?” The template recommends yes, and for a team it’s the right call, because every developer then gets their own schema and nobody overwrites anyone’s tables. I chose a shared `dev` schema to keep the screenshots readable for a solo project. If you're two or more people, say yes.

Notice what nobody asked you about: pip or Poetry. The template requires uv and generates a `pyproject.toml`. And notice that you didn't design this structure. Databricks did, which means every engineer who joins your team after 2026 will recognize it.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*O1KvQak8XEzKlnrFdgPQmg.png)

## The Anatomy

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*s6-WczY42-4tznQJeG1_mw.png)

What you get, folder by folder:

- `databricks.yml` is the manifest: bundle name, which files to include, the wheel artifact, variables, and the dev and prod targets
- `resources/` holds *what runs*: one YAML file per resource, here `sample_job.job.yml` and `understanding_databricks_etl.pipeline.yml`
- `src/` holds *what the code does*: a Python package, the pipeline's transformation code as its own package, and one notebook
- `tests/` already contains a `conftest.py` and a real sample test, so pytest works on day one
- `fixtures/` is an empty folder for test data
- `AGENTS.md` and `CLAUDE.md` are the instructions for AI agents mentioned earlier

The design principle is simple: definitions and code live apart. A pull request that changes a schedule touches one small YAML file in `resources/`, not your transformation logic.

The manifest ties it together. Here’s the version I ended up with (the next section explains what I changed from the generated one):

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*pIpyG0YOj3kHNZ7btR330Q.png)

Read the `targets` block twice. It quietly solves the oldest problem in data engineering: the same code deploying to different environments without a single copy-pasted notebook. The `dev` target uses `mode: development`, the `prod` target uses `mode: production`, and each sets its own catalog and schema through variables. We'll come back to what the modes actually do.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Kw8YDoCt_rveWMbMnRrB_Q.png)

## Before You Push: Take Yourself Out of the Config

The template does something you only notice if you read the generated files carefully: it writes *you* into them. My workspace URL appeared in both targets, my email in the prod target’s `root_path` and `permissions`, my email again in `pyproject.toml` as the author, and my username inside the sample notebook's widget metadata. Commit that to a public repo and you've published your workspace address and your identity. Commit it to a team repo and the prod config only works for you.

The fix takes three small changes. First, identity becomes a substitution that Databricks resolves at deploy time for whoever is deploying:

```c
prod:
  mode: production
  workspace:
    root_path: /Workspace/Users/${workspace.current_user.userName}/.bundle/${bundle.name}/${bundle.target}
  permissions:
    - user_name: ${workspace.current_user.userName}
      level: CAN_MANAGE
```

Second, the workspace URL moves into a local override file that the bundle includes but Git ignores:

```c
# databricks.yml
include:
  - resources/*.yml
  - databricks.local.yml   # git-ignored, holds your workspace host
```
```c
# databricks.local.yml (copy from databricks.local.yml.example)
targets:
  dev:
    workspace:
      host: https://<your-workspace>.cloud.databricks.com
```

I first tried deleting the host entirely and relying on the CLI profile. The CLI was fine with it; the VS Code extension wasn’t, and showed “Invalid host for target dev.” The local file satisfies both, and anyone who clones the repo just copies the `.example` file and fills in their own workspace.

Third, add `databricks.local.yml` and `.DS_Store` to `.gitignore` (the template's `.gitignore` already covers `.databricks/`, `.venv/`, `build/`, and `dist/`). Then check what Git is about to publish before the first commit:

```c
git init -b main && git add .
git statusgit status
```

My first commit had 22 files, none of them containing a host or an email:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ofwKqZSUv1t9gmqxwZ4P0Q.png)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*3qLAUyvDqJTPB1TWWwvV4Q.png)

## Validate, Deploy, Run

The loop you’ll live in from now on has three commands. First, validate:

```c
databricks bundle validate
```
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Zh-CLRh_6UOyXM2MqFVwCg.png)

Then deploy to dev. This is where Free Edition taught me something:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*HABmjCMuCYiGegSSTm8XyQ.png)

The wheel built, the files uploaded, the pipeline was created, and then the job failed with `403 PERMISSION_DENIED` and a message claiming my organization "has been cancelled or is not active yet." It hadn't been cancelled. The fix was the "Verify identity" button in the workspace's top bar: on Free Edition, an unverified account can create pipelines but not jobs. After verifying, I ran the exact same command again.

I’ll admit I was a bit shocked. It turns out the free version wants you to verify your account (I did it through LinkedIn), and until you do, you get exactly this misleading error. A small price for learning on a real platform for free, so don’t panic: verify the account and carry on.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*xNp6HPcoSszhyySTbNgiOg.png)

`0 created, 0 changed, 0 deleted, 2 unchanged`. This line is the best argument for bundles I know. The deploy compared the desired state in my files with what exists in the workspace and found nothing to do (the job had been created by the run before this screenshot). You can run it ten times; it converges, it doesn't duplicate. Try getting that guarantee from a job you clicked together in the UI.

Where does the CLI keep track? In the workspace, inside your user folder under `.bundle/<project>/<target>`:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*AqLEHR4VHdgK3Tf_nThmRA.png)

Three folders: `files` holds your synced code, `artifacts` the built wheel, and `state` the deployment state that made the `2 unchanged` possible. Treat all of it as build output. The code in the workspace is an artifact of a deploy, not a place to edit; edit locally, commit, deploy again.

Finally, run something. `bundle run` takes the resource *key* from your YAML, not a display name and not an ID, which is exactly why the command is reproducible for anyone who clones the repo:

```c
databricks bundle run --target dev understanding_databricks_etl
```
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*yBQUZH8sR1Tj_Y5IV7d7jw.png)

Two materialized views built from the `samples.nyctaxi.trips` dataset, 22K and 128 rows, three seconds each, on serverless compute nobody had to configure.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*nKnfkpbY5l4HTbwxGjdjZQ.png)

## Jobs vs Pipelines: Two Different Ideas

After the deploy, Jobs & Pipelines shows two resources side by side, and if you’re new to Databricks this is where it gets confusing:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*4DiYgquUGqRkHAhu7XCZqQ.png)

A pipeline (Lakeflow Spark Declarative Pipelines) answers *what tables should exist*. You declare the tables and how each is computed; Databricks works out the order, the dependencies, and what needs refreshing. A job (Lakeflow Jobs) answers *when, and in what order, should things run*. It’s an orchestrator: schedules, retries, and tasks of any type, from notebooks and Python wheels to SQL and, yes, pipelines.

The template shows the relationship better than any diagram. Its sample job has three tasks: a notebook, a Python wheel, and a task called `refresh_pipeline` that runs the very pipeline we just looked at. The job orchestrates; the pipeline transforms. We'll go deep on pipelines later in the series. For now, keep the one-line version.

Look at the Trigger column too: `Paused - Scheduled`. That's `mode: development` at work, more on it in a moment.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*-F0ctiSOnTHccFu_a_Y7sA.png)

## Notebooks Are Entry Points, Not Homes

The oldest structural question on this platform: where does the code live? The 2026 answer is settled, and the template shows it if you look at that sample job in the VS Code extension:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*3KclHOb-MNdBN1fTiMAyfQ.png)

A `notebook_task`, a `python_wheel_task`, and a pipeline. Notebooks are for exploring and for being the thin entry point of a job: read parameters, call functions, show results. The logic lives in plain Python modules under `src/`, imported with a normal `import`, packaged as a wheel when the bundle deploys. That's the code you can unit test, review in a pull request, and reuse across jobs (testing gets its own article later in this series).

Which makes the `%run` chain, one notebook pulling in another pulling in another, officially outdated advice. Databricks' own guidance says to migrate `%run` -based code sharing to module imports. The chain breaks silently, can't be tested, and confuses every tool that tries to analyze your project, agents included.

One more detail for your Git reviews: the template’s notebook is an `.ipynb`, now the default format, which GitHub renders with rich diffs. The older `.py` source format still works, and some teams prefer it for cleaner pull requests. Pick one per repo and write it down.

For local work, the VS Code extension (it also works in Cursor) reads your bundle, shows every job and pipeline before they’re even deployed, and lets you run code against serverless via Databricks Connect. You edit in a real IDE with a real linter; the platform just executes.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*rIstExxG6Gk9BJgdvoa-Nw.png)

## Dev and Prod Without Copy-Paste

Environment separation in 2026 has three layers.

Start with workspaces. The official recommendation is separate workspaces per stage: at least dev and prod, ideally with staging in between. Free Edition gives you exactly one workspace, which is why my two targets point at the same host and differ by schema instead. Good enough for learning; in a company, don’t.

Then catalogs. Unity Catalog separates environments at the catalog level, with the environment prefix first: `dev_sales`, `prod_sales`, lowercase with underscores. Workspace-catalog binding then makes `prod_*` catalogs reachable only from the prod workspace, so no notebook in dev can even see production data. On Free Edition everything lives in the `workspace` catalog, and the bundle created the `dev` schema with its two tables on the first run:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*R6OkQdWEuO48-C8IwDoZqA.png)

Finally, targets and modes. This is where the bundle earns its keep. In `mode: development`, every deployed resource gets a `[dev your_username]` prefix, schedules deploy paused (you saw `Paused - Scheduled` above), and concurrent runs are allowed, so several engineers can deploy the same bundle into one workspace without colliding. In `mode: production`, the deploy checks that pipelines aren't in development state, can require you to deploy from the `main` branch, and should run as a service principal instead of a person. Nobody's personal account owns a production job, so nobody's departure breaks a schedule.

I learned this one the hard way. On one project we had a superuser account, and during testing someone deployed a production job through it. The catch: jobs deployed by that user weren’t visible to regular users. After testing we set up a proper bundle deploy and moved on. A while later we noticed that some tables were being written twice on every run, and nobody could explain why, until we logged in as the power user and found the forgotten job, still running on its schedule next to the bundle-deployed one. Production runs as a service principal and deploys through the bundle. No exceptions, not even “just for testing.”

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*VTyLpre6W-U8ib0X3hUJig.png)

## Config, Parameters, and Secrets

Configuration on Databricks confuses people because there are four mechanisms, and they answer different questions:

- Bundle variables resolve at *deploy* time. Anything environment-shaped (catalog, schema, warehouse) is a bundle variable, like `catalog` and `schema` in our `databricks.yml`
- Job parameters resolve at *run* time. The clean pattern is a job parameter whose default is a bundle variable, so you can override a single run without redeploying
- Task values pass data between tasks inside one run
- Widgets (`dbutils.widgets`) are for interactive notebook sessions. In a job, `dbutils.widgets.get()` is simply how a notebook reads its parameters; a widget as your *source* of production config is an anti-pattern

Secrets got a 2026 upgrade too: they’re now Unity Catalog objects with a three-level name (`catalog.schema.secret`) and per-secret permissions, instead of the old all-or-nothing scope grants. We'll cover secrets and config properly in the next article.

Whatever mechanism you use, the rule is the same: the moment a path, catalog name, or credential appears as a string literal inside a notebook, you’ve planted the bug that pages someone at 2am in eight months.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*_cJANPBpfQ67myJ7OgxzEA.png)

## Common Mistakes to Avoid

- ClickOps. Creating jobs by hand in the UI works until you need a second environment, an audit, or an agent’s help. If it’s not in the bundle, it doesn’t exist
- Pushing the template as generated. It contains your workspace URL and email. Replace identity with `${workspace.current_user.userName}` and move the host to a git-ignored file
- The `%run` chain. Officially superseded by module imports. Move shared code to `src/` and let the wheel do its job
- Widgets as production config. Bundle variables and job parameters are the config mechanisms
- One workspace for everything. Fine on Free Edition, wrong in a company. Minimum: dev and prod
- A shared dev schema in a team. Say yes to the template’s personal-schema option when more than one person works on the project
- A person running production. Production targets run as a service principal. People go on vacation; service principals don’t
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*MJipmHfSIjYMYmgU6kERlQ.png)

## Frequently Asked Questions

### What are Declarative Automation Bundles (DABs)?

The infrastructure-as-code standard for Databricks projects, renamed from “Databricks Asset Bundles” in March 2026 (the acronym stayed). A bundle is a folder with a `databricks.yml` manifest describing your code, jobs, pipelines, and target workspaces; the CLI validates, deploys, and runs it. You can also author bundles in Python and manage them from the workspace UI.

### What is the recommended folder structure for a Databricks project?

The one the official `default-python` template generates: `databricks.yml` (manifest with targets), `resources/` (one YAML per job or pipeline), `src/` (Python packages plus notebook entry points), `tests/` (pytest), `fixtures/` (test data), and `pyproject.toml` (wheel build via uv). Since 2026 it also includes `AGENTS.md` for AI coding agents.

### What is the difference between a Databricks job and a pipeline?

A pipeline (Lakeflow Spark Declarative Pipelines) declares which tables should exist and how each is computed, and Databricks works out the order and dependencies. A job (Lakeflow Jobs) orchestrates when and in what order tasks run, and a pipeline can be one of those tasks.

### Can I use Declarative Automation Bundles on Databricks Free Edition?

Yes. Validation, deployment, pipelines, and serverless runs all work. One catch from my own setup: jobs failed to deploy with a 403 “organization has been cancelled or is not active yet” error until I completed the “Verify identity” step in the workspace.

### How do I separate dev and prod in Databricks?

Three layers: separate workspaces (dev and prod at minimum), environment-prefixed catalogs (`dev_sales`, `prod_sales`) with workspace-catalog binding, and bundle targets that map the same code to each. `mode: development` adds per-user prefixes and pauses schedules; `mode: production` enforces clean deployment state and should run as a service principal.

### How do I keep my workspace URL and email out of a public Databricks repo?

Replace user-specific values in `databricks.yml` with `${workspace.current_user.userName}`, move the workspace host into a git-ignored `databricks.local.yml` that the bundle includes, and commit a `databricks.local.yml.example` for others to copy. Check `pyproject.toml` and notebook metadata too; the template writes your identity there as well.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*wFdImzzS_ktFTnL7B-SjuQ.png)

## What Is Next

The skeleton is standing, it deploys, and it’s [on GitHub](https://github.com/mbvyn/understanding-databricks), ready to grow with this series. Next we give the project its nervous system: secrets, environment variables, and logging, including the new Unity Catalog secrets and what good logging even means when your compute is serverless.

Make sure to bookmark this series so you don’t miss any upcoming articles.

*Want more? Visit* [*mbvyn.com*](https://mbvyn.com/) *for mentorship, consulting, and all my content in one place. And if you work with Parquet files, try* [*parquetreader.app*](https://parquetreader.app/)*, my free tool for exploring them in the browser.*

*Follow me on* [*Medium*](https://medium.com/@mbvyn) *and subscribe on* [*Substack*](https://mbvyn.com/insights) *so you don’t miss the next article.*

*Reviewed by Coconut and Whiskey. Coconut insists on a place for everything and everything in its place. Whiskey keeps it all in one big pile and calls it a lakehouse.*