---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-25-goofyfish-make-your-own-game
source_title: Make your own game
source_author: Goofy Fish (site; no personal byline)
source_url: https://goofyfish.com/make
tags:
  - source/summary
  - coding-agents
  - end-user-programming
  - open-source
source_ids:
  - src-2026-11-25-goofyfish-make-your-own-game
status: active
---

# Make Your Own Game

## Summary

The "Make your own game" page on the Goofy Fish games site invites visitors to "Describe a game to
Claude Code. It builds it in our style and sends it in." The contribution path has four steps. A
visitor clones the site's public repository (github.com/nilbuild/goofyfish) and installs its
dependencies. They then open Claude Code in that folder and type a `/game` command with an idea; the
page's example is "a game where you keep a balloon in the air". The agent "builds the game, tests it
and draws the thumbnail", and the visitor plays it and asks for changes. Finally, "Say the word and it
walks you through the pull request. We play it and put it on the site." The page is short, but it is
a concrete case of a repository that ships its own agent command, so that a contributor's coding
agent produces work in the project's style and submits it through the normal pull-request route.

## Key claims

- **The repository carries the workflow.** The style rules, build, test, and thumbnail steps sit
  behind a `/game` command in the repository, not in the contributor's own setup. The page does not
  show the command's contents.
- **The contributor describes; the agent implements.** The human role on the page is to describe an
  idea, play the result, and ask for changes.
- **Submission stays a pull request.** The agent walks the contributor through a pull request, and
  the site's maintainers "play it" before publishing, so a human gate remains at intake.

## Why it matters

- [[Coding Agent Harness]]: harness configuration (a custom command) distributed with a repository
  so that every contributor's agent follows the same build and test path.
- [[AI-Native Software Development Lifecycle]]: an intake path where a visitor's description becomes
  a pull request, with review moved to the maintainers playing the result. The page does not say
  whether contributors need any programming experience.
- Proposed for [[Agent Skill]] and [[LLM-Native Extensible Software]].

## Tensions / open questions

- The capture has no personal byline and no published date; the site title comes from the parent's
  live check, not from the capture.
- No numbers are given: how many games arrived this way, how many were accepted, or how often the
  agent's tests caught problems.
- What "tests it" means for a game, and what the maintainers check when they "play it", is unstated.
- The page names Claude Code only; whether the command works in other harnesses is not said.

## Affected pages

- [[Coding Agent Harness]]
- [[AI-Native Software Development Lifecycle]]
- [[Agent Skill]]
- [[LLM-Native Extensible Software]]

## Raw capture

- [[knowledge-base/raw/sources/Make your own game]]

## Citations

- Canonical URL: https://goofyfish.com/make
- Byline: none in the capture (the frontmatter author field is empty). The site title "Goofy Fish"
  was verified on the live page by the parent agent, outside the capture.
- Published: not stated. Captured: 2026-11-25.

## Related pages

- [[Coding Agent Harness]]
- [[AI-Native Software Development Lifecycle]]
- [[Agent Skill]]
- [[LLM-Native Extensible Software]]
- [[Frank Rousseau - Agentic Coding on an Open-Source Project]]
