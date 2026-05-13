---
type: source-summary
source_id: src-2026-05-12-vinod-expert-workshop-copilot-cli
source_title: "May Expert Workshop - Copilot CLI Setup Guide"
source_author: Vinod Rajendran
source_url: ""
created: 2026-05-13
updated: 2026-05-13
tags: [copilot, cli, setup, wsl, workshop, github]
status: active
---

# May Expert Workshop - Copilot CLI Setup Guide

## Summary

A step-by-step setup guide created for an internal expert workshop in May 2026 on using **GitHub Copilot CLI**. The guide walks through the full installation chain from WSL setup through Copilot CLI login and model selection.

## Key steps documented

1. **Prerequisites** — GitHub Copilot access and local Windows admin rights.
2. **WSL installation** — `wsl --install` from an elevated PowerShell.
3. **Dependency installation** — Node.js, npm, and the `@github/copilot` npm package inside WSL.
4. **Launching Copilot CLI** — Running `copilot` from the WSL terminal.
5. **Authentication** — `/login` command triggers a device-code flow via `github.com/login/device`.
6. **Model selection** — `/model` command to choose the backing LLM.

## Durable claims

- Copilot CLI can be installed globally via `sudo npm install -g @github/copilot`.
- Authentication uses GitHub's standard device-code OAuth flow.
- The `/model` command lets users switch between available LLMs inside a session.

## Affected pages

- [[GitHub Copilot CLI]] — new entity page for the tool.

## Raw capture

- [[2026-05-12 Vinod Rajendran - May Expert Workshop Copilot CLI Setup]]

## Related pages

- [[AI Knowledge Base Overview]]
- [[GitHub Copilot CLI]]
