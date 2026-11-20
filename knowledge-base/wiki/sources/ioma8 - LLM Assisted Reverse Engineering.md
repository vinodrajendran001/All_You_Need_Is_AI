---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-18-ioma8-llm-reverse-engineering
source_title: "LLM assisted reverse engineering"
source_author: "ioma8"
source_url: "https://www.slowchronicle.com/posts/llm-assisted-reverse-engineering"
tags:
  - source/summary
  - reverse-engineering
  - agent-skills
  - agent-memory
  - agent-security
  - mcp
source_ids:
  - src-2026-11-18-ioma8-llm-reverse-engineering
status: active
---

# LLM Assisted Reverse Engineering

## Summary

A short personal blog post by ioma8, who says he has hacked hardware and software "for 2 decades"
and that in 2026 AI has greatly sped the process up. He describes his set-up, his working method,
three agent skills he relies on, his implementation languages, and a list of projects he credits to
the approach. The post reached **306** points on Hacker News, which the author mentions in an edit.

The method is less about clever prompting than about making a long investigation survivable for an
agent: write every finding to Markdown files, give the agent a skill that describes the specific
disassembly tooling, and, when it gets stuck, force it through a logged hypothesis-and-experiment
loop rather than letting it guess. Much of the text concerns hobby hardware work: mapping device
protocols, custom firmware for synthesizers and an e-reader, and a printer driver.

Reverse engineering is dual-use. The author's list of successes includes a claim to have "Cracked
tons of license-locked abandonware softwares from my youth". This summary records that only as a
claim and stays at the level of method; it omits anything aimed at defeating licensing or other
protections. All results are anecdotal and self-reported.

## Key claims

### Set-up

- Main agent: "DeepSeek Harness + Deepseek v4.1 Flash", described as "super performant, fast and
  cheap", with Codex on Luna or Terra used occasionally.
- Ghidra with an MCP bridge, "The best in the market, free, disassembler and decompiler. With the
  MCP bridge agents can use it very well". radare2 and kuna are faster command-line alternatives,
  "possibly better usable for AIs".

### Process

- "What I basically do nowadays is just point the agent at the binary to be analysed and use my set
  of dedicated agent skills. Rest usually takes care of itself."
- Identify the binary type and platform and choose a decompiler; he notes current models "do fairly
  well with just disassembly".
- **Have the agent document all findings to MD files.** He gives three reasons: they become the
  human's notes, "They help the agent not lose the track after compaction / handoff to different
  agent", and they keep it from getting "lost in circles".
- Ask for the basic structure (main functions, branching, imports) before anything else.
- When static analysis is not enough: let the agent run a debugger, add logging or a probe, give it
  outside access such as computer use or an API-controlled emulator, steer it to a specific
  alternative approach (for example following strings instead of cross-references), and read the
  whole agent conversation and thinking to spot a "blind path" early.

### Skills

- **Grill me** (from Matt Pocock's public skills repository, spelled "Matt Pottock" in the capture):
  used to have the agent ask up to five crucial questions, one at a time.
- **A tooling skill** describing the specific reverse-engineering tools and the Ghidra MCP bridge.
  "Without such a skill, agents often give up too quickly getting lost". His public version is
  described as an agent skill plus **22** Ghidra scripts.
- **Hypothesis debugging**, his own public skill: write a hypothesis to a CSV table on disk, design
  an experiment that "will definitively prove or disprove" it, record the result, repeat. "This is
  variation of scientific method"; it "Stops it going in circles". He calls it "crucial".

### Implementation languages

- Python with uv for fast, portable probes and helpers.
- Rust for the actual implementation, partly because the strict compiler "provides brutally good
  feedback loops to the agent when it iterates".

### Claimed results

- In "the last 6 months", results "which would take me years each on its own, if done by hands":
  mapping the protocols of a biofeedback device and two Sony cameras (including turning one into a
  wireless webcam), custom firmware for several synthesizers and an e-reader, a fixed macOS printer
  driver, a custom Evernote client, and the cracking claim above.
- "Sometimes its a thin boundary between reverse engineering and software development": decipher a
  proprietary file format, then build a new editor for it.

## Why it matters

The vault already records agent reverse engineering as a governance problem through REA in
[[@0xCodila - Reverse Engineering with REA and Opus 5.5 (Full Course)]]. This post is the
practitioner's view of the same capability, and its interesting parts are general agent practice. Its
notes files are external memory chosen specifically to survive compaction and handoff, the
file-backed persistence [[Agent Memory]] discusses. Its hypothesis loop and tooling skill are
examples of [[Agent Skill]] encoding method rather than facts: a procedure that stops a stuck agent
from guessing, and a description of tools without which the agent often gives up too quickly. For
[[Agent Security and Governance]], it is a second data point on dual use: an individual using a
cheap model and free tools, with no stated limit on targets beyond his own judgement, and a
licence-cracking claim listed alongside firmware hobby work.

## Tensions / open questions

- **No evidence beyond the author.** The time saving ("years each") is a personal estimate and the
  skills are not compared against working without them.
- **The skill's value is asserted.** The hypothesis loop is called crucial; no runs with and without
  it are reported.
- **Dual use without a boundary.** Unlike REA's post, this one states no lawful-use disclaimer. The
  only boundary is the author's account of his own projects.
- **Model naming.** "Deepseek v4.1 Flash" and "DeepSeek Harness" are the capture's names; the vault
  has other DeepSeek V4.1-Flash references, and this summary does not assume they are the same
  product version.

## Affected pages

- [[Agent Skill]]
- [[Agent Memory]]
- [[Agent Security and Governance]]

## Raw capture

- [[knowledge-base/raw/sources/LLM assisted reverse engineering]]

## Citations

- Canonical URL: <https://www.slowchronicle.com/posts/llm-assisted-reverse-engineering> (the
  captured link carried a `utm_source=tldrnewsletter` parameter, removed here).
- By ioma8 (the GitHub handle the post links for its skills and projects) on slowchronicle.com,
  published November 18, 2026; captured November 20, 2026. The Hacker News figure of 306 points is
  from the author's edit in the capture.

## Related pages

- [[Agent Skill]]
- [[Agent Memory]]
- [[Agent Security and Governance]]
- [[@0xCodila - Reverse Engineering with REA and Opus 5.5 (Full Course)]]
- [[Model Context Protocol]]
- [[Context Engineering]]
- [[Computer Use Agents]]
- [[Legacy Code Modernization with AI Agents]]
