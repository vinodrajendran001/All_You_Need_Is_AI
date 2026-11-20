---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-11-openrouter-mcp-cli-skills
source_title: "MCP vs CLI vs Skills: What Each Costs in Context"
source_author: "OpenRouter"
source_url: "https://openrouter.ai/blog/insights/mcp-vs-cli-vs-skills/"
tags:
  - source/summary
  - mcp
  - tool-use
  - agent-skills
  - context-engineering
  - cost
source_ids:
  - src-2026-11-11-openrouter-mcp-cli-skills
status: active
---

# MCP vs CLI vs Skills - What Each Costs in Context

## Summary

A vendor blog post from OpenRouter that measures how many input tokens one GitHub task costs when a
model reaches GitHub through the GitHub MCP server, through the `gh` command-line tool, or through
`gh` plus a short skill file. It ran the task on Claude Haiku 5.5, Claude Sonnet 5.5, GPT-6 Luna, and
Gemini 3.8 Flash. On Sonnet 5.5 all three routes answered correctly, but the CLI used **1,421** input
tokens, the skill **3,315**, and the MCP server **59,417** with its default tools loaded.

The post then splits the MCP cost into two parts that are easy to confuse: the tool **definitions**
that ride along on every request, and the tool **results** that stay in the conversation once
returned. It ends by testing OpenRouter's own Tool Search server tool (in beta), which withholds
deferred definitions until the model searches for them. That part is promotional as well as
measured: Tool Search halved the whole-task cost on Sonnet 5.5 and raised it on Haiku 5.5. The
authors' own caveat is that they "tested one server on one task".

## Key claims

### Definitions cost depends on the model and even the provider

- The post counts tool cost by asking the model: send the same request with and without the tools
  and take the difference in `usage.prompt_tokens`, because each provider writes tool definitions
  into the prompt in its own format, "which a local tokenizer misses".
- The GitHub MCP server's **46** default tools added **19,436** tokens on Haiku 5.5, **8,903** on
  GPT-6 Luna, and **8,525** on Gemini 3.8 Flash through Google Vertex. Through Google AI Studio the
  same tools cost **13,010** on Gemini, so the script pins Gemini to Vertex.
- On Haiku 5.5, the issues toolset (**10** tools) adds **5,801** tokens and the users toolset (one
  tool) adds **619**.

### Same task, three routes (medians of three runs, October 20, 2026)

| Approach | Sonnet 5.5 tokens | Sonnet 5.5 cost per task | GPT-6 Luna tokens | Gemini 3.8 Flash tokens |
|---|---|---|---|---|
| CLI | 1,421 | $0.0075 | 627 | 5,292 |
| Skill | 3,315 | $0.0118 | 1,542 | 6,107 |
| MCP, 2 tools | 23,228 | $0.0552 | 14,479 | 17,267 |
| MCP, 46 default tools | 59,417 | $0.1274 | 116,282 | 35,409 |
| MCP, all 91 tools | 101,351 | $0.2113 | 135,238 | 53,289 |
| MCP, 2 tools, results capped at 4,000 characters | 5,357 | $0.0191 | 2,726 | 2,943 |

- "Every run in this table answered correctly." On Sonnet 5.5 the default MCP route used **42
  times** the CLI's input tokens and cost **17 times** as much, **$127 against $7.50 per 1,000
  tasks**. Output costs five times input on Sonnet 5.5, and the CLI run's **463** output tokens were
  **$0.0046** of its **$0.0075**, which is why the cost ratio is smaller than the token ratio.
- The skill (a one-line index pointing at a **1,492**-character SKILL.md) cost more than the bare CLI
  because the file stays in the conversation once read. "For a CLI tool the model knows well, a
  skill is optional. For your own CLI, the skill is how the model learns the commands."

### Results can cost as much as definitions

- `get_latest_release` returned GitHub's full release object, **42,182** characters, **87%** of it
  describing **22** download files; the model needed only the tag and date. On Sonnet 5.5 it added
  about **20,400** tokens, more than all 46 definitions, and was resent with every later request.
- Scoping the server to two tools cut the first request from **19,487** tokens to **1,406**, but the
  whole task still cost **23,228**. Capping results at 4,000 characters brought it to **5,357**, and
  worked "only because of where the fields happened to sit" (the tag and date are near the top).
- Asking `list_issues` for only number, title, and creation date cut its result from **8,336**
  characters to **714**. Without that, "the model decides the size": in **four of six** runs with 46
  or 91 tools loaded, GPT-6 Luna asked for **100** issues with full text and got **281,963**
  characters back.

### Tool Search helps some models and hurts others

- With all 46 tools deferred, the up-front cost before any search was **578** tokens on the Claude
  models, **144** on GPT-6 Luna, and **130** on Gemini 3.8 Flash.
- Whole task, 46 loaded / 46 deferred / 91 deferred: Sonnet 5.5 **59,417 / 30,334 / 31,615**; GPT-6
  Luna **116,282 / 25,544 / 57,975**; Gemini 3.8 Flash **35,409 / 37,568 / 38,445**; Haiku 5.5
  **99,319 / 154,623 / 31,781**. On Sonnet, 91 deferred tools cost **1,281** tokens more than 46,
  where loading all 91 cost "about 42,000 more".
- Haiku 5.5 cost more with deferral because in all three runs it asked `list_issues` for a field the
  tool does not offer, then retried three or four times with wrong argument types. In five runs of
  the demonstration script it used **2,134 to 13,225** tokens; GPT-6 Luna searched with phrases
  rather than patterns, made three to six searches, and once gave up without calling the tool.
- Combined with the 4,000-character cap, Tool Search left Gemini 3.8 Flash and Haiku 5.5 with one
  correct answer in three runs each, and Gemini once hit the loop's 12-request limit.
- Tool Search works by widening `tool_choice`, so a request that also forces a tool call fails with
  a 400; Chat Completions does not accept it at all. OpenRouter's docs suggest deferring once
  definitions pass "roughly 10,000 tokens or about 10 tools" and keeping the three to five most-used
  tools loaded.
- Prompt caching "lowers the price of those tokens but doesn't remove them": as of October 2026,
  cached input on OpenRouter costs a tenth of the normal rate on Haiku 5.5 and GPT-6 Luna, and still
  fills the window.

## Why it matters

The vault's [[Tool Roster Economics]] page has argued that MCP's cost is residency, not the
protocol, and has repeatedly noted that nobody prices a search-first roster against a resident one.
This is the first capture with whole-task token counts for that trade across four models. Its
answer is model-dependent: deferral roughly halved Sonnet's cost and cut GPT-6 Luna's sharply
(though Luna's loaded figure "includes the 100-issue request"), did little for Gemini, and raised Haiku's because of retries. It also adds the result side that a tool
count misses: one oversized result outweighed every definition, and output projection (asking for
fields) beat a character cap that worked by luck. Its recommendation ("Use a CLI when one exists and
your agent can run commands") gives [[Agent Skill]] a measured place as a cheap wrapper around a CLI
rather than a replacement for [[Model Context Protocol]].

## Tensions / open questions

- **A model-name inconsistency.** The TL;DR and FAQ say the 46 default tools add 19,436 tokens "on
  Claude Sonnet 5.5" / "on Claude", but the script that produced the figure measured Haiku 5.5. The
  post asserts that "Haiku 5.5 counts a prompt exactly as Sonnet 5.5 does"; it shows no Sonnet run of
  the script. The captured script output also prints " tools" with the count missing.
- **One server, one task, three runs.** Medians of three runs cannot show variance, and the Tool
  Search script's own five runs spread from 2,134 to 13,225 tokens on Haiku.
- **Vendor framing.** OpenRouter sells Tool Search, the Shell server tool, and the Agent SDK it
  recommends; no comparison with another provider's tool search is made.
- **Correctness is thin.** Every main-table run answered correctly, but quality was not measured
  beyond one factual question, and the CLI's advantage assumes a shell and a model that already
  knows `gh`.

## Affected pages

- [[Tool Roster Economics]]
- [[Model Context Protocol]]
- [[Agent Skill]]

## Raw capture

- [[knowledge-base/raw/sources/MCP vs CLI vs Skills What Each Costs in Context]]

## Citations

- Canonical URL: <https://openrouter.ai/blog/insights/mcp-vs-cli-vs-skills/> (the captured link
  carried a `utm_source=tldrai` parameter, removed here).
- By OpenRouter on its blog, published November 11, 2026; captured November 20, 2026. No individual
  author is named. Runs were made on October 20, 2026.

## Related pages

- [[Tool Roster Economics]]
- [[Model Context Protocol]]
- [[Agent Skill]]
- [[Context Engineering]]
- [[Programmatic Tool Calling]]
- [[Tool Use and Function Calling]]
- [[Factory Research - Droid 1.0 - Building a Frontier Harness]]
- [[Philipp Schmid - Why Agents Are Soon Only Going to Have 1 Tool]]
- [[ByteByteGo - How Uber Built a Gateway for AI Agents to Access Tools]]
- [[Semantic Caching]]
