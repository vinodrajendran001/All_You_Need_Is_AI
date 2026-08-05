---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-reviewing-ai-generated-pull-requests
title: How to Review AI-Generated Pull Requests (2026)
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/reviewing-ai-generated-pull-requests
published: '2026-07-27'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# How to Review AI-Generated Pull Requests (2026)

Someone on r/ExperiencedDevs described the job as it now stands. The author asks the AI for something, it makes 100 changes they think they understand, they glance at the first few, then submit. Hundreds of CPU hours went in, plus two or three minutes of the author's own time, and the reviewer is now expected to check every change: is it correct, does it do what it says, does it need a further change the AI didn't make, are the comments and docs still accurate, does it weaken a check that was there for a reason. That thread ran to 1,904 upvotes and 442 comments.

Further down it, the end state: "I gave up and just started hitting approve."

This page ships three artifacts instead of describing that. A pull request template that makes the author do the comprehension work before the PR enters your queue. An `AI_POLICY.md` for the repo root, with the `AGENTS.md` pointer that gets agents to read it. And a GitHub Actions workflow that runs three machine gates before a human is allowed to be the check. That is four files in the repo, because the policy needs its pointer to get read. Copy them, replace the angle-bracket placeholders, set the three tunable numbers from your own repo's history, and commit.

One assumption up front: you've already decided AI-authored changes are going to keep arriving. Whether to allow them at all is a separate argument, and the projects quoted below land in different places on it.

This goes deeper than the review-bandwidth section of [how to become an AI-native company](/blog/how-to-become-an-ai-native-company), which states the ceiling and stops there.

---

## What Actually Changed

Code review was designed around writing being expensive. The reviewer could assume the author had already thought about what they were submitting, because producing it had cost them something. That assumption is what's gone.

The outside numbers are worse than I expected. LinearB's 2026 benchmark report covers 8.1 million PRs across roughly 4,800 teams: 84.5% of manual PRs merge within 30 days, against 32.7% of AI-assisted ones. Reviewer pickup time goes from about 200 minutes to about 1,050, and AI-assisted PRs run past 400 lines at the 75th percentile against 157 for unassisted. Those are LinearB's own platform figures. A separate study of the AIDev dataset looked at 33,596 agent-authored PRs in its popular-repository subset and found 61.38% of them carry no recorded review activity. Among the ones that were reviewed, 58.77% were reviewed only by agents, 10.14% only by a human, and 31.09% by a human and an agent together.

In that subset, most of the pull requests carry no trace of anyone having reviewed them. LinearB's figures are a separate dataset making a different comparison, between a manual cohort and an AI-assisted one, so they say nothing about a trend over time and nothing about the PRs the paper looked at. The paper measures observable review interaction in the PR history. Its authors say that an absent record doesn't establish that no human looked, because a maintainer can read a diff without leaving a comment. So the record is what's gone from those PRs. Whether the reading happened is something the data can't reach.

Viet-Anh Nguyen names the mechanism under it. A junior engineer's mistake usually looks like a mistake, he writes, a clumsy loop or a variable named `temp2`, while an agent's mistake looks like senior work: correct naming, idiomatic structure, a confident commit message, tests that pass, wrapped around a missing authorization check. Review leans on a reflex that fires when code looks wrong, and by his account this code doesn't look wrong.

A commenter in the same thread describes a second-order effect. He used to calibrate his effort per author: someone with a track record of clean PRs earned a lighter read. With AI-written code, he says, you don't get consistency between PRs from the same person, so you have to check for everything every time, which is exhausting. That per-author heuristic was doing real work for him, and his point is that AI-authored PRs take it away.

![Two review pipelines drawn side by side: on the left every AI-generated pull request lands straight on one human who has to check dependencies, secrets, static analysis, correctness, architecture and intent all at once, so the queue backs up behind them; on the right the same pull request passes through gate one for dependency and provenance auditing, gate two for secret scanning and SAST, and gate three for an adversarial second-model pass, before reaching a human at gate four who answers only three questions about architecture alignment, trust boundaries and whether the reasoning can be reconstructed](/images/blog/reviewing-ai-prs-gates-diagram.png "Two review pipelines drawn side by side: on the left every AI-generated pull request lands straight on one human who has to check dependencies, secrets, static analysis, correctness, architecture and intent all at once, so the queue backs up behind them; on the right the same pull request passes through gate one for dependency and provenance auditing, gate two for secret scanning and SAST, and gate three for an adversarial second-model pass, before reaching a human at gate four who answers only three questions about architecture alignment, trust boundaries and whether the reasoning can be reconstructed")

---

## The Bar Three Published Policies Land On

Three open source projects wrote their answer down as a file in the repo. They don't agree on whether to allow AI-authored contributions, and they still put the same test on whoever is allowed to submit: explain the line or don't submit it.

Sonarr states it plainly in `CONTRIBUTING.md`: you are responsible for every line of your contribution, and if you can't explain why a line is there and why it's correct, it shouldn't be in your PR. stashapp permits AI-assisted contributions under four conditions, and the second is that you must be able to explain any line of code and design decision during the review process. OpenTofu's registry repo goes further than either and doesn't accept AI-generated code from community contributors at all, closing PRs identified as AI-generated without further review. Two reasons are stated. One is capacity: automated tooling is easy to scale, and they've yet to determine a way to scale their maintainers' attention, and they've seen patches the authors cannot explain and fixes for problems that don't exist. The other is provenance: they can't audit what a model was trained on, and OpenTofu was forked from a codebase that has since gone BUSL. Their own maintainers may use one approved tool, under disclosure rules that don't apply to anyone outside.

Dov Katz at Morgan Stanley states the constraint in merge terms: just because something is fixed doesn't mean it's merged, and until it's merged the fix is worth nothing. His colleague Khalid Elsawaf added the version that lands: in the time the two of them had been talking, you could have produced a thousand-file, 10,000-line PR off a simple prompt, and no human there is going to review that.

Adopt the explain-every-line test for a practical reason as well as a principled one. You can ask someone to walk you through their own diff without having to establish anything about how it was written.

The rest of this article is that test turned into files.

---

## Artifact 1: The Review Packet

The idea comes from a comment in that same thread, and it's the part of the discussion I've reused. The commenter's framing was that the line worth drawing is about whether the author can own the diff, and that the way to enforce it is to make the submitter bring a small review packet before the PR enters the queue: intent, risk areas, tests run, what they personally verified, and what they still don't understand.

Sonarr already ships a version of this. Their PR template has a Submission Checklist with three boxes, and one of them is a trap: "This PR was authored and submitted by an AI agent without human review." Their `AGENTS.md` tells agents in place that every checkbox is an attestation.

Here's the full version. Save it as `.github/pull_request_template.md` and GitHub puts its contents into the pull request body for anyone opening a PR.

markdown

```
## What this changes

<!-- One or two sentences. What is different after this merges, and why. -->

## Intent

<!-- The problem you set out to solve, in your own words. The goal, not the diff.
     If this closes an issue, link it: Closes #___ -->

## Risk areas

<!-- Where in this diff would a bug do the most damage? Name the files or
     functions. Then tick every trust boundary this change touches. -->

- [ ] Authentication or authorization
- [ ] User-controlled input reaching a query, a shell, a file path, or a template
- [ ] Money, billing, or quota
- [ ] Migrations, or anything that writes to production data
- [ ] A new third-party dependency
- [ ] None of the above

## What I ran

<!-- Commands and outcomes. "CI is green" is not an answer on its own: if the
     tests were written alongside the code by the same tool, they confirm that
     the code does what the code does. -->

| Check | Command | Result |
|---|---|---|
| Test suite | | |
| The specific case this PR is about | | |
| Manual verification | | |

## What I verified myself

<!-- Which parts of this diff did you read line by line, and can defend in
     review? Be specific about which files. -->

## What I still don't understand

<!-- Anything in this diff you cannot explain. Saying so here is the point of
     this section: it tells the reviewer where to spend their attention.
     Leaving it blank when it isn't true is what costs you trust. -->

## Attestations

- [ ] I can explain why every line in this diff is here and why it is correct.
- [ ] I have removed AI-generated footers, `Co-Authored-By:` trailers for tools,
      and "Generated with ..." signatures.
- [ ] This PR is within the size limit in `AI_POLICY.md`, or I have explained
      below why it can't be split.
```

The "What I still don't understand" section asks the author a question the reviewer would otherwise have to ask them, with no accusation attached, and it tells the reviewer where to concentrate. A blank answer is the first thing to ask about in review.

Trust-boundary checkboxes are there because that's the category of bug the pattern-matching part of your brain skips. Correct-looking code on both sides of a boundary, with nothing checking that the boundary is a boundary.

The footer line is lifted from Sonarr, and I'd keep it even though it sounds petty. Their reasoning is operational: the presence of a "Generated with..." trailer tells you the author didn't review their own submission closely enough to notice it. OpenTofu handles the same thing from the other side, requiring an `Assisted-by:` trailer on AI-assisted commits and explicitly banning `Co-authored-by:` for AI tools, since a tool isn't an author who can be responsible for anything. That trailer rule sits in their maintainers' section and binds maintainers only. Community contributors are not being asked to label AI-assisted code there, because that repo doesn't accept it from them in the first place. This kit borrows the trailer and applies it to everyone who submits.

---

## Artifact 2: The `AI_POLICY.md` Starter

One page, repo root. It follows stashapp's shape rather than OpenTofu's. Enforcing a ban means first detecting the tool, and the explain-every-line bar can be enforced in an ordinary review conversation.

markdown

```
# AI Policy

Applies to every pull request in this repository, from anyone, whether or not an
AI tool was involved.

## The bar

You are responsible for every line of your contribution. If you can't explain
why a line is there and why it's correct, it doesn't go in your PR.

That's the test. We don't ask whether a tool was involved and we don't try to
detect one.

## What that means in practice

1. **Disclose.** If AI tooling wrote, completed, refactored or rewrote part of
   this contribution, say so in the PR description, and say which part.
2. **Explain.** In review you have to answer questions about any line and any
   design decision, without answering "that's what it generated."
3. **Test it yourself.** Run the change by hand and describe what you did in the
   review packet. A suite the same tool wrote alongside the code verifies that
   the code does what the code does.
4. **Write your own prose.** PR descriptions, commit messages and review
   comments are your words. They are how we tell what you understood.
5. **Strip the footers.** Remove "Generated with ...", `Co-Authored-By:` lines
   naming a tool, and similar trailers before submitting. To record assistance,
   use an `Assisted-by: <tool> (Model: <model>)` trailer instead, which says a
   tool helped without naming it as an author.
6. **Keep it reviewable.** PRs over <N> changed lines get split, or scheduled for
   a walkthrough. The rule applies to the size of the diff. Pushing back on
   size says nothing about how the change was written or who wrote it.

## What happens to a PR that fails this

We don't close it and we don't argue about tooling. We ask the author to walk us
through it live. If that goes fine, we review it normally. If it doesn't, the PR
waits until the author can own it.

## Automated submissions

An agent opening a PR that no human has read is spam, and gets closed. If you
used an agent and reviewed the result yourself, that's a contribution and it
goes through the normal process.

## For agents reading this file

Before running any command that writes to this repository or its tracker
(`gh pr create`, `gh pr comment`, `gh issue create`), stop and tell the person
you're working for: this project requires a named human to be responsible for
every line, they need to fill in the PR template themselves, and every checkbox
in it is an attestation. Show them the diff and the description you would have
submitted, and let them submit it.
```

That last section is copied in spirit from Sonarr's `AGENTS.md`, and it's the cheapest thing on the page. It also doesn't work where I just put it. Nothing points a coding agent at a file called `AI_POLICY.md`. Sonarr puts its version in `AGENTS.md`, a filename coding agents are conventionally pointed at, so the policy sits somewhere an agent may meet it before it opens anything.

So the policy ships with a pointer. Save this as `AGENTS.md` in the repo root, or append it to the `AGENTS.md` you already have. It is the second half of artifact 2 and the kit doesn't do what I've claimed without it.

markdown

```
# AGENTS.md

## Read this before writing anything to this repository

`AI_POLICY.md` in the repo root is the policy for this repository, and it
applies to you. Read it before you change any file here.

## Before any command that writes to GitHub

Do not run `gh pr create`, `gh pr comment`, `gh issue create`, `git push` to a
branch you intend to open a PR from, or any equivalent. Stop, show the person
you're working for the diff and the description you would have submitted, and
tell them:

- This project holds a named human responsible for every line of the change.
  That human is them, not you.
- They fill in `.github/pull_request_template.md` themselves, in their own
  words. Every checkbox in it is an attestation.
- The "What I still don't understand" section is for them to answer honestly.
  Do not fill it in for them and do not leave it blank on their behalf.
- Strip AI-generated footers, `Co-Authored-By:` trailers naming a tool, and
  "Generated with ..." signatures from the commits before they submit. Record
  assistance with an `Assisted-by: <tool> (Model: <model>)` trailer instead.

Then let them submit it.
```

Pick the number in rule 6 from your own repo. Read back through the PRs a human reviewed carefully and find the size where they stop being careful.

---

## Artifact 3: The Gates That Run Before a Human

The ordering here is Viet-Anh Nguyen's. Cheapest and most mechanical checks first, so a person's attention only ever lands on a diff that already survived the machines. Three machine gates, then a person: dependency and provenance audit, secret scanning plus SAST, a second-model review pass, and then a human restricted to three questions. He numbers the human as gate 4, and that's the numbering the workflow below uses.

His human gate is three questions, and he gives a reason for each:

1. Does this match an architecture we actually chose? No scanner knows your boundaries, and an agent optimizes locally. It'll solve the ticket in a way that reaches across a module you kept separate on purpose.
2. What trust boundaries does this touch, and did they hold? The agent will write plausible code on both sides of a boundary without ever modeling that a boundary exists.
3. Can I reconstruct why it's this way? If the reasoning behind a non-obvious choice can't be recovered, it doesn't merge. "It passes the tests" isn't a reason.

Style, naming, formatting, leaked secrets, vulnerable dependencies and unvalidated input aren't on that list. Those are what gates 1 to 3 are pointed at, and whatever they turn up arrives as a worklist rather than as one of the three questions.

Here's gates 1 to 3 as a workflow. Save it as `.github/workflows/pre-human-gates.yml`.

yaml

```
# The three machine gates, cheapest first. Gate 4 is a person: the three
# questions in AI_POLICY.md, plus a branch protection rule that requires a
# human approval to merge. This file cannot enforce gate 4 and does not try.

name: pre-human-gates

on:
  pull_request:
    # `ready_for_review` is load-bearing. Gate 3 is skipped while a PR is a
    # draft, and without this trigger a PR opened as a draft would never get
    # gate 3 at all: marking it ready would not re-run the workflow.
    types: [opened, synchronize, reopened, ready_for_review]

# Least privilege by default. Every job below re-declares what it needs, and
# only gate 3 widens past read.
permissions:
  contents: read

concurrency:
  group: pre-human-gates-${{ github.event.pull_request.number }}
  cancel-in-progress: true

jobs:
  # Gate 1. What did this change pull in? New dependencies are the highest
  # leverage thing an agent touches, and a logic-focused review walks past them.
  # Two of the three steps below can fail the build. The first one cannot: it
  # prints a checklist for a person, and is named so nobody mistakes it for a
  # check. Registry-page judgment is not automated here.
  provenance:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4.4.0
        with:
          fetch-depth: 0

      - name: Dependency manifest changes (manual checklist, enforces nothing)
        run: |
          git diff --unified=0 "origin/${{ github.base_ref }}...HEAD" -- \
            package.json package-lock.json requirements.txt pyproject.toml \
            poetry.lock go.mod go.sum Cargo.toml Cargo.lock \
            | tee dependency.diff
          if [ -s dependency.diff ]; then
            echo "::notice::MANUAL STEP. This step never fails the build. For each"
            echo "::notice::new package a person opens the registry page, confirms"
            echo "::notice::it exists, reads the publish date and download count,"
            echo "::notice::and checks that the repo link resolves. The scan below"
            echo "::notice::is the part of gate 1 that can fail."
          fi

      # Image pinned by digest. A mutable tag is a supply-chain hole in a job
      # whose whole purpose is supply chain. Note that neither Dependabot nor
      # Renovate bumps this one: their GitHub Actions handling reads action
      # references and the `container` and `services` fields, not images inside
      # a `run:` command. This digest is yours to move.
      - name: Known vulnerabilities in the lockfiles
        run: |
          docker run --rm -v "$PWD:/src" \
            ghcr.io/google/osv-scanner:v2.4.0@sha256:5116601dedc01c1c580eb92371883ec052fc4c13c3fbc109d621a63ac416d475 \
            scan source --recursive /src

      - name: Reject pickled model files
        run: |
          if git diff --name-only "origin/${{ github.base_ref }}...HEAD" \
             | grep -Ei '\.(pkl|pickle)$'; then
            echo "::error::Pickle executes arbitrary code on load. Not merging this."
            exit 1
          fi

  # Gate 2. Secrets and static analysis. There is no reason a person should be
  # the one who notices a hardcoded key.
  secrets-and-sast:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4.4.0
        with:
          fetch-depth: 0

      # The gitleaks CLI in a container, not gitleaks/gitleaks-action. The
      # action requires a GITLEAKS_LICENSE secret on any repository owned by an
      # organization, and a job triggered by a fork PR gets no repository
      # secrets at all. Both cases fail on a missing key, not on a finding, and
      # both are cases this file is written for. The CLI is
      # MIT-licensed and takes no key, so this step needs no secret and no
      # setup, and the job drops to `contents: read` because nothing here
      # writes a comment. Pinned by digest like the other two containers.
      - name: Secret scan
        run: |
          docker run --rm -v "$PWD:/repo" \
            ghcr.io/gitleaks/gitleaks:v8.30.1@sha256:c00b6bd0aeb3071cbcb79009cb16a60dd9e0a7c60e2be9ab65d25e6bc8abbb7f \
            git /repo \
              --log-opts="origin/${{ github.base_ref }}...HEAD" \
              --redact --no-banner --verbose

      - name: SAST
        run: |
          docker run --rm -v "$PWD:/src" -w /src \
            semgrep/semgrep:1.171.0@sha256:bdf7013b2c3634a487671158da77c554f531742326b543a9464d2adf6c433ac8 \
            semgrep scan \
              --config p/security-audit \
              --config p/owasp-top-ten \
              --error --skip-unknown-extensions

  # Gate 3. A second model reads the diff before a person does. Fresh context,
  # no stake in the code, prompted to break the change rather than bless it.
  # Its output is a worklist for the human. It never approves anything.
  #
  # Fork policy, stated rather than discovered: this gate CANNOT run on a pull
  # request from a fork, and it fails instead of skipping. See the first step.
  second-model-review:
    runs-on: ubuntu-latest
    needs: [provenance, secrets-and-sast]
    # Drafts are exempt on purpose. `ready_for_review` in the trigger list above
    # is what runs this the moment a draft is marked ready for review.
    if: ${{ github.event.pull_request.draft == false }}
    permissions:
      contents: read
      # Needed only by the last step, which posts the worklist as a comment.
      pull-requests: write
    steps:
      # Compare repo names rather than reading head.repo.fork, which is true
      # for every PR in a repository that is itself a fork of something.
      - name: Fork policy
        if: ${{ github.event.pull_request.head.repo.full_name != github.repository }}
        run: |
          echo "::error::Gate 3 cannot run on a pull request from a fork. Under"
          echo "::error::the pull_request event a fork gets no ANTHROPIC_API_KEY"
          echo "::error::and a read-only token, so this job can neither call the"
          echo "::error::API nor post its worklist. It fails rather than going"
          echo "::error::green on a gate that did not run. Run the adversarial"
          echo "::error::pass by hand from a maintainer checkout and say so in"
          echo "::error::the review before approving. Do not switch this file to"
          echo "::error::pull_request_target to make the check pass: that hands"
          echo "::error::your secrets to code nobody has read yet."
          exit 1

      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4.4.0
        with:
          fetch-depth: 0

      - name: Build the diff
        env:
          # TUNABLE STARTING VALUE, not a measurement and not a receipt. Same
          # class of number as <N> in AI_POLICY.md: replace it from your own
          # repo's history with the diff size past which one review pass stops
          # being worth anything.
          MAX_DIFF_BYTES: "400000"
        run: |
          git diff "origin/${{ github.base_ref }}...HEAD" > pr.diff
          if [ "$(wc -c < pr.diff)" -gt "$MAX_DIFF_BYTES" ]; then
            echo "::error::Diff is over $MAX_DIFF_BYTES bytes, too large to review in one pass. Split the PR."
            exit 1
          fi

      - name: Adversarial review pass
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          # TUNABLE STARTING VALUE, not a measurement and not a receipt. Same
          # class of number as MAX_DIFF_BYTES above. It caps how long the
          # worklist is allowed to get. If the step below starts failing on
          # `max_tokens`, raise this or split the PR.
          MAX_REVIEW_TOKENS: "4000"
        run: |
          if [ -z "$ANTHROPIC_API_KEY" ]; then
            echo "::error::ANTHROPIC_API_KEY is not set, so gate 3 did not run."
            exit 1
          fi

          jq -n --rawfile diff pr.diff --argjson cap "$MAX_REVIEW_TOKENS" '{
            model: "claude-opus-5",
            max_tokens: $cap,
            system: "You are a paranoid staff engineer reviewing a diff you did not write. Your job is to break it. Look for the authorization gap, the unvalidated input crossing a trust boundary, the dependency that should not be there, the error path that swallows a failure, the test that asserts nothing. Report every finding with a file, a line, a one-sentence failure scenario, and your confidence. Do not filter by severity; a human does that next. Do not compliment the change. If you find nothing, say so in one line.",
            messages: [{role: "user", content: ("Review this diff:\n\n" + $diff)}]
          }' > request.json

          curl -sS --fail-with-body https://api.anthropic.com/v1/messages \
            -H "content-type: application/json" \
            -H "x-api-key: $ANTHROPIC_API_KEY" \
            -H "anthropic-version: 2023-06-01" \
            -d @request.json > response.json

          # A truncated worklist reads exactly like a clean one. Check the stop
          # reason before the content, because a response cut off at
          # MAX_REVIEW_TOKENS is well-formed and non-empty.
          stop_reason="$(jq -r '.stop_reason // "missing"' response.json)"
          if [ "$stop_reason" = "max_tokens" ]; then
            echo "::error::The review pass was cut off at MAX_REVIEW_TOKENS"
            echo "::error::($MAX_REVIEW_TOKENS), so the worklist is incomplete and"
            echo "::error::gate 3 did not finish. Raise MAX_REVIEW_TOKENS or split"
            echo "::error::the PR. Failing rather than posting a truncated worklist."
            exit 1
          fi
          if [ "$stop_reason" != "end_turn" ] && [ "$stop_reason" != "stop_sequence" ]; then
            echo "::error::The review pass stopped for an unexpected reason"
            echo "::error::($stop_reason), so gate 3 did not complete. Failing"
            echo "::error::rather than trusting a response we cannot account for."
            exit 1
          fi

          jq -r '[.content[]? | select(.type == "text") | .text] | join("\n")' \
            response.json > review.md

          # `jq -r` writes a trailing newline even when every text block is
          # empty, so review.md is one byte and `[ -s ]` would pass on nothing.
          # Strip whitespace and test what is actually left.
          if [ -z "$(tr -d '[:space:]' < review.md)" ]; then
            echo "::error::The review pass returned no text, so gate 3 did not"
            echo "::error::run. Failing rather than posting an empty worklist."
            exit 1
          fi

      - name: Post the worklist as a comment
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          {
            echo "### Second-model review pass"
            echo
            echo "Machine-generated. A worklist for the human reviewer, not an approval."
            echo
            cat review.md
          } | gh pr comment "${{ github.event.pull_request.number }}" --body-file -
```

Three numbers in that file are placeholders: `<N>` in `AI_POLICY.md`, and `MAX_DIFF_BYTES` and `MAX_REVIEW_TOKENS` in the workflow. All three are labelled in place as tunable starting values rather than findings. Replace them from your own repo's history before you rely on any of them.

Gate 3 fails on two shapes of half-finished output that would otherwise go green. A response truncated at `MAX_REVIEW_TOKENS` is well-formed and non-empty, so it reads like a completed worklist unless the step checks `stop_reason`, and the step checks it. And `jq -r` writes a trailing newline even when the model returned an empty text block, which makes the file one byte long, so the emptiness test strips whitespace instead of testing file size. The workflow never approves a PR, so what those two holes produced was a green check on gate 3 and a worklist that was empty or cut off mid-finding.

Everything the workflow pulls in is pinned: the one action to a commit SHA, the three containers to an image digest, with the readable version in a trailing comment. A mutable tag inside a supply-chain gate is the hole the gate exists to close.

Bumping them is only half automatic. Dependabot and Renovate both handle the `actions/checkout` line, because their GitHub Actions support reads action references. Neither sees the three container digests, because those sit inside `run:` commands, and Renovate's GitHub Actions manager extracts images from the `uses`, `container` and `services` fields only. So the three `docker run` digests are yours to bump by hand, or with a Renovate `customManagers` regex rule you write. A digest nothing is watching ages into the mutable-tag problem with extra steps.

Running the `gitleaks` CLI in a container rather than `gitleaks/gitleaks-action` is what keeps gate 2 copy-and-commit. The action asks for a `GITLEAKS_LICENSE` secret on any repository owned by an organization, and it is free but you have to go request it, add it as a secret, and remember it exists. A job triggered by a fork PR gets no repository secrets at all, so on a fork the action would fail on a missing key before the fork policy in gate 3 ever ran. The CLI is MIT-licensed, takes no key, and needs nothing set up, so the copy-and-commit path stays copy and commit. The one thing you give up is the review comment the action posts on each finding, which is why gate 2 is now `contents: read` with no write scope at all. The finding is in the job log and the check is red.

Gate 1's first step can't fail the build, and its name says so. It prints the manifest diff and a checklist, because deciding whether a freshly published package with almost no downloads belongs in your lockfile is a judgment call about your repo, and I can't write it as a rule from here. The `osv-scanner` pass and the pickle rejection in the same job are the parts that can fail the build.

The second-model pass is prompted adversarially and told not to filter by severity. Ask it for coverage and do the filtering yourself. A severity filter written into the prompt moves the judgment call into the machine, which is the thing gate 4 exists to keep.

Gate 3 posts a comment and never approves. Keep it that way, and keep the branch protection rule that requires a human approval. Otherwise the recorded reviewing on your repo is agent-on-agent, which is the shape the AIDev numbers found, and the human gate is left with nothing to show for itself.

A draft PR doesn't get gate 3 at all, which is why `ready_for_review` sits in the trigger list. Leave that trigger out and a PR opened as a draft sails past gate 3 for good, because marking it ready doesn't re-run the workflow. Gates 1 and 2 still run on drafts.

The fork case is worse, so decide it before you turn this on. Under the `pull_request` event a PR from a fork gets no repository secrets and a read-only token, so gate 3 can neither call the API nor post its comment. The workflow above fails the check instead of quietly going green on a gate that didn't run, which leaves a maintainer to run the adversarial pass by hand from their own checkout and say so in the review. The fix that suggests itself is `pull_request_target`, which does give the job your secrets, and gives them to code nobody has read yet. If you take outside contributions, pick one of those on purpose.

---

## The Same Problem, Three Different Fixes

Who's on the other side of the PR changes which of the three artifacts does the work.

Solo, there's no second party, and the packet becomes a note to your future self. Fill in "what I still don't understand" anyway. Later it becomes a record of which parts of your own codebase you didn't read, which is cheaper to write down now than to rediscover during an incident. Gates 1 and 2 still earn their keep, and gate 3 is the second opinion you don't otherwise have.

A small team is the shape all three artifacts are aimed at: a named human on each end of the PR who'll be in the same standup tomorrow. Install the packet first, before the policy and before the workflow. The packet moves work back to the author, and the other two support it. If you can only do one thing this week, do that one.

Once review is a queue with a throughput number on it, the risk changes character. The AIDev study is the closest thing to a measurement of it: in its popular-repository subset of 33,596 agent-authored PRs, 61.38% have no recorded review activity, and among the reviewed ones the largest single share, 58.77%, is agent-only. That is a measurement of what the PR history shows, and its authors say plainly that absent records don't establish absent oversight. What it does establish is that the record is thin, and a thin record is a bad thing to run a dashboard off. Review latency coming down looks the same whether you fixed the bottleneck or stopped writing anything down. If you're reporting on this, put the human-approval rate next to the throughput number, so the throughput number can't improve without the review happening.

---

## What This Looks Like On Our Side

We're a small team running production agent loops, and our version of this rule lives in the loop's own spec file rather than in a PR template.

Every run of our SEO loops counts how many of its own shipped PRs are still unmerged and reports that count as `prs_unmerged`. The spec then tells the loop that while any of them sit there, flat search position is expected rather than failure, and that merging is the human's call, never the loop's. It's a loop being made to notice the review queue it's filling, instead of reading a stalled number as a problem it should fix by shipping more. The excerpt is published in [the pillar](/blog/how-to-become-an-ai-native-company), so you can read the actual lines.

The queue is real. Around 1 a.m. across four consecutive nights, loops opened PR #201 on 2026-07-21, #203 on 07-22, #210 on 07-23 and #214 on 07-24, while nobody was awake. None of that is throughput until a person merges it.

One more from our side, because it's the reason gate 3 posts a comment instead of approving. We run a build loop whose ship rule was an independent vision critic scoring the output out of 10, ship at 8 or above with all hard checks passing. It hit that bar run after run, 8.0 to 8.6, all checks green. Then Jason looked at the live items and deleted seven of them. We paused the loop on 2026-07-24 and rewrote the gate. That's one loop of ours on one set of dates, and it's not a claim about second-model review in general. It is the reason I wouldn't let a machine's pass be the last word on anything a person will have to own.

---

## Receipts

| Claim | Status |
| --- | --- |
| 84.5% of manual PRs merge in 30 days against 32.7% AI-assisted; pickup ~200 vs ~1,050 min; 400+ LOC at P75 vs 157 | External, attributed to LinearB's 2026 benchmark report. 8.1M PRs, roughly 4,800 teams, their own platform data |
| Of the 33,596 agent-authored PRs in one popular-repository subset, 61.38% have no recorded review activity; of those reviewed, 58.77% agent-only, 10.14% human-only, 31.09% mixed human-and-agent | External. Empirical study of the AIDev dataset, arXiv 2605.02273, Table 1. Every percentage here is scoped to that subset, and the three composition shares are of reviewed PRs, not of all PRs. The paper measures observable review interaction in the PR history and states that absence of recorded review activity does not imply absence of human oversight. Not restated here as a missing review gate |
| Maintainer attention doesn't scale the way tooling does | External. OpenTofu's published AI usage policy |
| OpenTofu's registry repo does not accept AI-generated code from community contributors, and closes PRs identified as AI-generated without further review | External. OpenTofu's policy file, `AI-USAGE-POLICY.md`, under "Rules for community contributors" |
| Their second stated reason is training-data provenance: a model may reproduce license-incompatible code, and OpenTofu was forked from what is now BUSL-licensed Terraform | External. Same file, under "Reason for this policy" |
| You are responsible for every line; strip the AI footers | External. Sonarr's `CONTRIBUTING.md` on the `v5-develop` default branch. The `develop` URL resolves but carries an older copy with no AI section |
| A shipping PR template with three attestation checkboxes | External. Sonarr's `.github/PULL_REQUEST_TEMPLATE.md` |
| An `AGENTS.md` that tells agents to read the policy and refuse to open the PR themselves | External as a pattern. Sonarr's `AGENTS.md` instructs agents to read `CONTRIBUTING.md` before any GitHub-facing write, tell the human they are responsible for every line, strip AI attribution footers, and leave the submission to them. The `AGENTS.md` shipped here is that pattern rewritten for this kit, not a quote |
| AI-assisted contributions permitted under four conditions (disclose, explain, test by hand, take responsibility) | External. stashapp's `docs/AI_POLICY.md` |
| `Assisted-by:` trailer required, `Co-authored-by:` banned for AI tools, for OpenTofu maintainers | External. OpenTofu's policy file, under "Rules for Maintainers". The trailer rule binds maintainers, not community contributors, whose AI-generated code that repo does not accept at all |
| Until it's merged the fix is worth nothing; nobody reviews a 10,000-line PR | External. Dov Katz and Khalid Elsawaf of Morgan Stanley, in a Moderne interview |
| The gate ordering: three machine gates, then a human on three questions | External. Viet-Anh Nguyen's published SDLC, where the human is numbered gate 4. We use the gate design and the plausible-mistake diagnosis, and none of that post's other figures |
| An agent's mistake looks like senior work; a green suite the agent wrote isn't evidence | External. Same source |
| The 100-changes account, the give-up-and-approve line, and the calibration-loss point | External. Comment quotes from r/ExperiencedDevs 1towli9 (1,904 upvotes, 442 comments), paraphrased here in my own words |
| The review packet as a fix | External, and credited. u/Future\_Manager3217 in that thread proposed intent, risk areas, tests run, personally verified, still don't understand. Artifact 1 is that list turned into a file |
| Pair reviews changed behaviour on one team | External. One commenter's report from the same thread, and it ships as that. No rate attached |
| Push back on PR size rather than the tool | External. Top-voted advice in r/ExperiencedDevs 1pem6eg, 259 upvotes |
| Approving without understanding; you can't run a system at scale that no one understands | External. Comment quotes from r/ExperiencedDevs 1v6n7d7 |
| Our loops report `prs_unmerged` and treat flat position as expected while PRs sit | Firsthand. The rule is in the loop spec file excerpt already published in the pillar |
| PRs opened unattended at 1 a.m. | Firsthand. PR #201 (07-21), #203 (07-22), #210 (07-23), #214 (07-24) |
| Seven items passed a score-8 gate and were rejected by eye; loop paused 2026-07-24 | Firsthand, and date-anchored. Triangulated across the loop spec, the run log and a dated decision record. It supports "our gate passed work we deleted" and nothing broader |
| The pinned action SHA and image digests in the workflow | Not a claim about the world. Resolved on 2026-07-27 through the GitHub git-refs API and the container registries, and recorded in the receipt matrix as V-pins. Versions as shipped, not a recommendation to freeze them |
| `gitleaks/gitleaks-action` requires a `GITLEAKS_LICENSE` on organization-owned repos, and the `gitleaks` CLI does not | External. The action's own README: the licence is "required for organizations, not required for user accounts." Gate 2 runs the CLI for that reason, recorded in the matrix as V-gitleaks-licence |
| The size limit in `AI_POLICY.md`, the 400,000-byte diff cap, and the 4,000-token review cap in the workflow | Not receipts and not findings. Three placeholders to replace from your own repo's history. Labelled as such in place: `<N>` in the policy, and commented `MAX_DIFF_BYTES` and `MAX_REVIEW_TOKENS` in the workflow. Gate 3 fails loudly when it hits the token cap rather than posting the truncated worklist |

Two things I wanted in this article and cut. A widely-cited productivity study would have made the review-cost argument neatly, but its own authors published a follow-up calling their data an unreliable signal of the current productivity effect of AI tools, and citing the headline without that gets called out. And several defect-rate figures that appear inside one of my sources are quoted there secondhand, so they'd have arrived here thirdhand. Both dropped rather than hedged.

---

## Start Here

Add the pull request template first. It's one file, and it changes who does the comprehension work without anyone having to agree to a policy first.

Then run gate 2 by hand on the last thing your agent shipped. `gitleaks git --pre-commit --staged` and an `osv-scanner` pass over your lockfiles. If either lights up on code that already merged, you know which half of your pipeline you rebuilt and which half you didn't.

Then write the policy, with your own number in rule 6, drop the `AGENTS.md` pointer next to it, and wire up the workflow last. The workflow is the one that needs CI access, a secret and a decision about forks, and the checks it automates are ones a careful reviewer would get to anyway. What the template catches is upstream of all of them: an author who never read their own diff.

The precondition for all of it is that your repo can prove its own work. If an agent can't run the stack, exercise the feature and produce evidence, every PR it opens lands on you to verify by hand, and no template fixes that. [Harness engineering](/blog/harness-engineering-agent-production-guide) covers making a repo legible and verifiable, and [how to evaluate AI agents](/blog/how-to-evaluate-ai-agents) covers building a gate that doesn't drift the way ours did.

Some of the tooling for the repo side is open source. We publish [AI Builder Club Skills](https://github.com/AI-Builder-Club/skills?utm_source=blog&utm_medium=article&utm_campaign=reviewing-ai-generated-pull-requests&utm_content=start-here) as a Claude Code plugin, and four of the skills in it are aimed at the repo side of this. Their documented jobs, in the repo's own README: `setup-codebase-harness` orchestrates onboarding a repo to agent-driven development, `verifier-setup` scaffolds a repo-specific `/verify` skill that drives the app and captures screenshot or video proof into the PR, `e2e-setup` adds a per-PR test gate to a repo with weak or no end-to-end coverage, and `crabbox-setup` gives each agent its own isolated cloud stack so loops can ship in parallel.

If you want the whole operations picture this sits inside, the [Loop Engineering course](/courses/loop-engineering) goes from prompting an agent yourself to a loop that wakes on schedule, ships behind quality gates, and reports back.

---

## Related Content

- **[How to Become an AI-Native Company](/blog/how-to-become-an-ai-native-company)** - The pillar this hangs off: which loop to build first, what one costs, and what breaks.
- **[How to Evaluate AI Agents](/blog/how-to-evaluate-ai-agents)** - Why self-evaluation skews optimistic, and how to build a gate that doesn't drift.
- **[Harness Engineering](/blog/harness-engineering-agent-production-guide)** - Making a repo legible, executable and verifiable, which is what makes agent output cheap to check.
- **[Crabbox: Parallel Agent Sandboxes](/blog/crabbox-parallel-agent-sandboxes)** - Isolated stacks per agent. Parallel agents multiply the review queue, so this is the other half of the problem.
- **[Loop Engineering: Stop Writing Prompts, Start Writing Verifiers](/blog/loop-engineering-guide-2026)** - The mechanics of a single loop, and why the verifier is the bottleneck.
- **[A Role Label Is Not a Sandbox](/blog/agent-tool-permissions-canary)** - Spoke three. The gates above run before a human sees the diff; that page is how to test whether the tool grants and deny rules behind them actually hold.
- **[Your Agents Have Production Credentials and No Owner](/blog/who-owns-your-ai-agents)** - Spoke four. The policy above makes a human own every line an agent wrote; that page makes a human own the agent itself, with a registry row, an expiry and an offboarding runbook.
- **[Why Your Agent Bill Is Wrong](/blog/ai-agent-runaway-cost)** - Spoke two. What the loops filling your review queue actually cost, and how to tell whether the figure your runner shows you is a total or a floor.
- **[How to Build an SEO Agent Loop](/blog/ai-agent-seo-loop)** - Spoke five. The loop whose `prs_unmerged` rule is the firsthand leg of this page, in full.
- **[How to Cold-Launch a Social Presence With Agent Loops](/blog/ai-agent-social-loop)** - Spoke six. The same review ceiling on the distribution side, where 45 drafted replies sit in a queue nobody has sent.
- **[Claude Code Worktrees and Parallel Agents](/blog/claude-code-worktree-parallel-agents)** - Running several agents at once without them colliding.

[Join AI Builder Club](/pricing?utm_source=blog&utm_medium=article&utm_campaign=reviewing-ai-generated-pull-requests)

The same things, stated explicitly instead of assumed. Intent in the author's own words, the risk areas and trust boundaries the diff touches, the commands they ran and what came back, which lines they read and can defend, and anything in the diff they can't explain. The last field is the one I read first. A blank answer there is either an author who read the whole thing or an author who didn't check, and it's worth asking about in review.

It depends on who is contributing, and the three policies I read for this article don't agree. OpenTofu's registry repo does ban them from the community: it states it does not accept AI-generated code from community contributors, and that pull requests identified as AI-generated are closed without further review. It gives two reasons, capacity and provenance. Automated tooling is easy to scale and they have yet to determine a way to scale their maintainers' attention, and they cannot audit any model's training data for license-incompatible sources, which matters to them because OpenTofu was forked from the now-BUSL-licensed Terraform. Their own maintainers may use one approved tool under disclosure rules. stashapp goes the other way and permits AI-assisted contributions if the author discloses the usage and scope, can explain any line and design decision during review, tests by hand and describes the steps, and takes full responsibility including license compliance. The starter policy in this article follows stashapp's shape, because a ban has to detect the tool before you can enforce it and the explain-every-line bar can be enforced in an ordinary review conversation. If your repo has OpenTofu's provenance exposure, their answer is the one to copy.

Push back on the size of the diff instead of the origin of it. That's the top-voted advice in the r/ExperiencedDevs thread on the subject, and the reason given is that any attempt to address the tool inherently reads as accusatory. The size of a diff is a fact you can state, and splitting it or walking through it on a call is a request that doesn't ask anyone to defend how they wrote it.

It can do a pass. Keep it out of the approval path. Gate 3 in the workflow above posts a worklist as a PR comment and never approves, and the branch protection rule still requires a human approval to merge. The reason to hold that line is in the AIDev dataset study, across the 33,596 agent-authored PRs in its popular-repository subset: of the ones there with any recorded review, 58.77% were reviewed only by agents, against 10.14% reviewed only by a human and 31.09% reviewed by a human and an agent together. Those shares are that subset's, and the paper's other subset reports different ones. A machine sitting in the approval path is what the agent-only share looks like from the inside.

Three machines, then a person. Dependency and provenance audit, then secret scanning plus SAST, then a second-model review pass, then a human restricted to three questions: does this match an architecture we actually chose, did the trust boundaries hold, and can I reconstruct why it's this way. That ordering is Viet-Anh Nguyen's, who numbers the human as gate 4. The three machine gates run first so a person's attention lands on judgment that doesn't compress.

Viet-Anh Nguyen's rule is that on agent-authored changes the agent wrote the tests too, alongside the implementation and to pass, so they verify that the code does what the code does. Read the tests as part of the diff with the same suspicion as the code, and write the load-bearing one yourself. That's why the review packet asks what you ran and what you verified rather than whether CI is green.

Firsthand: the loop rule that reports its own unmerged PRs, and the gate that passed work we later deleted, come from running production agent loops at SuperDesign and AI Builder Club through 2026. The three artifacts are assembled from published policy files and from a published gate design, credited in place. Figures attributed to other organizations are their own and unverified by us. See our [editorial standards](/about).
