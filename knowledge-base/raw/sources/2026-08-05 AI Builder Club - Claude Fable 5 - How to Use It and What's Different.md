---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-claude-fable-5-how-to-use-guide
title: 'Claude Fable 5: How to Use It and What''s Different'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/claude-fable-5-how-to-use-guide
published: '2026-06-11'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Claude Fable 5: How to Use It and What's Different

**Claude Fable 5 shipped on June 9, 2026.** Two days later: 2,561 points on Hacker News, 5,272 upvotes on r/ClaudeAI, 532K views on Anthropic's launch video. One builder burned 700 million tokens in a single day inside Cursor. Another one-shot an entire horror game live on stream. The consensus across every platform I checked: biggest capability jump since Claude 3.5 Sonnet, but with tradeoffs nobody expected.

> **TL;DR:** Claude Fable 5 is Anthropic's Mythos-class model (same as Mythos 5) with safety classifiers added. It scores 80.3% on SWE-Bench Pro (11 points above Opus 4.8), costs $10/$50 per million tokens (2x Opus), requires 30-day data retention, and is available via API (`claude-fable-5`), Claude.ai, Claude Code, and Cursor. Use it for hard, long-horizon tasks. Keep Opus 4.8 for everything else.

## What Is Claude Fable 5?

Claude Fable 5 is Anthropic's first **Mythos-class** model made available to the general public. Mythos was previously considered too capable in cybersecurity and biology to release broadly. Fable 5 is the same underlying model as Claude Mythos 5, but with safety classifiers layered on top that automatically block or reroute requests in high-risk areas.

The key facts:

| Spec | Claude Fable 5 |
| --- | --- |
| Model ID | `claude-fable-5` |
| Context window | 1,000,000 tokens |
| Max output | 128,000 tokens per request |
| Input price | $10 / million tokens |
| Output price | $50 / million tokens |
| Batch pricing | $5 input / $25 output per MTok |
| Prompt caching | 90% discount on cached input |
| Availability | Claude API, AWS Bedrock, Vertex AI, Microsoft Foundry |

Karpathy called it "a major-version-bump-deserving step change forward." On SWE-Bench Pro it scores 80.3% - 11 points ahead of Opus 4.8 and 22 points ahead of GPT-5.5.

## How to Access Claude Fable 5

Three paths, depending on how you work with AI:

### 1. Claude.ai (Chat Interface)

Open the model picker in any conversation and select Claude Fable 5. Available on Pro, Max, Team, and Enterprise plans through June 22 at no extra cost. After June 23, it requires usage credits.

### 2. API (For Builders Shipping Products)

Use the model string `claude-fable-5`:

code

```
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-fable-5",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Audit this function for edge cases: ..."}],
)

print(message.content[0].text)
```

### 3. Claude Code / Cursor (Agent Coding)

This is where Fable 5's long-horizon design pays off. Anthropic explicitly recommends running it inside an agent harness for multi-stage work.

- **Claude Code**: Run `/model` inside a session and select Fable 5, or launch with `claude --model claude-fable-5`
- **Cursor**: Select Claude Fable 5 from the model dropdown. It's the state-of-the-art model on CursorBench.

BridgeMind spent over 700 million tokens inside Cursor on launch day and said: "Fable 5 makes new things possible... this model is a massive leap in AI capabilities." DesignCourse ran 5 UI/UX one-shot tests and went "three for three" with award-worthy landing pages from a single prompt (189K views, 6,258 likes).

## Claude Fable 5 vs Opus 4.8 vs Mythos 5: The Real Differences

This is where most people get confused. Here is the actual relationship:

|  | Claude Fable 5 | Claude Opus 4.8 | Claude Mythos 5 |
| --- | --- | --- | --- |
| **What it is** | Mythos-class model + safety classifiers | Previous-gen top model | Same model as Fable without classifiers |
| **Access** | Everyone (API, chat, Bedrock, Vertex) | Everyone | Project Glasswing partners only |
| **Pricing** | $10 / $50 per MTok | $5 / $25 per MTok | $10 / $50 per MTok |
| **SWE-Bench Pro** | 80.3% | 69.2% | Same as Fable |
| **FrontierCode** | 29.3% | 13.4% | Same as Fable |
| **Safety** | Classifiers block cyber/bio, falls back to Opus | Standard moderation | No classifiers |
| **Data retention** | 30-day mandatory retention | Standard | 30-day mandatory retention |
| **Best for** | Long-running, complex, autonomous work | Routine tasks, cost-sensitive workloads | Cybersecurity research (approved partners) |

**The short version:** Fable 5 is 2x the price and meaningfully better on hard, long-horizon tasks. Opus 4.8 remains the smart default for 80% of everyday work. Mythos 5 is the same model without safety rails, but you can't get it unless you're in Project Glasswing.

A Hacker News user with 2,093 comments on the launch thread put it clearly: "Fable on 'high' is producing substantially better results than Opus 4.8 on xhigh for me... it 'feels' smarter and doesn't use nearly as many tokens running in circles."

## How to Prompt Claude Fable 5 (Tips from Anthropic + the Community)

Fable 5 behaves differently from previous Claude models. Anthropic published a dedicated prompting guide. The community found additional patterns. Here is what works:

### Use the effort Parameter

This is the primary control for the intelligence/cost/latency tradeoff:

- **`high`** (default): Use for most tasks. Still outperforms Opus 4.8 at xhigh.
- **`xhigh`**: Maximum capability. Use for the hardest problems.
- **`medium` / `low`**: Routine work. Lower effort on Fable 5 still exceeds prior-gen models at xhigh.

### Tell It to Be Brief

Fable 5 is verbose by default at higher effort levels. Anthropic's own docs acknowledge it will "elaborate beyond what the task needs, surveying options it won't pursue, explaining root causes at length." A short instruction fixes it:

code

```
Be concise. No preamble. Answer in the minimum words needed.
```

### Don't Ask for Internal Reasoning

Requesting the model's "internal reasoning" or "thinking process" can trigger a `reasoning_extraction` refusal. Use adaptive thinking blocks instead - they're built in and always active.

### Ground Long-Running Agents

For autonomous tasks running for hours or days, add explicit tool-based progress reports. Fable 5 can work for extended periods, but you need to track what it's doing:

code

```
After every major step, use the progress_report tool to summarize:
1. What you just completed
2. What you plan to do next
3. Any blockers or decisions needed
```

### State Boundaries Explicitly

Fable 5 is proactive - it will do things you didn't ask for if it thinks they're helpful. Set clear scope:

code

```
Only modify files in src/components/. Do not touch tests, configs, or documentation unless I explicitly ask.
```

### Alex Finn's "Plan Mode" Tip (129K views)

From the launch-day video: "This is an advanced plan mode where I'm going to have Claude Fable 5 ask me a bunch of questions to fully understand in depth what I want to build." Instead of prompting step-by-step, give Fable 5 the full goal and let it plan autonomously.

## The Safety Refusals: What Actually Happens

This is the most controversial aspect. Fable 5's safety classifiers automatically flag requests touching cybersecurity, biology, chemistry, and frontier LLM research. When triggered, it falls back to Opus 4.8.

Anthropic says 95% of sessions run entirely on Fable without hitting a fallback. The community's experience is more mixed:

- A GitHub issue titled "Saying 'hi' returns usage policy violation" got 23 reactions and 86 comments
- r/Anthropic user paying $200/month for Max: "Fable 5 feels too restricted to be useful for legitimate cybersecurity and forensics work"
- AI Explained spent nine hours reading the 319-page system card and noted: "It was a minute after the release of Fable 5, and I had just been having a conversation with Opus 4.8 about getting more fermented food for my gut bacteria" - even that triggered a classifier switch
- Wired reported that Anthropic walked back a policy that would have "covertly degraded performance for researchers training rival AI models"

**For builders shipping with the API:** You need to handle `stop_reason: "refusal"` responses. Here is the simplest implementation:

code

```
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-fable-5",
    max_tokens=4096,
    messages=[{"role": "user", "content": your_prompt}],
)

if response.stop_reason == "refusal":
    # Fable's safety classifier tripped - retry on Opus 4.8
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=4096,
        messages=[{"role": "user", "content": your_prompt}],
    )
```

Or use the built-in server-side fallback (beta) to handle this automatically:

code

```
response = client.messages.create(
    model="claude-fable-5",
    max_tokens=4096,
    fallbacks=["claude-opus-4-8"],
    messages=[{"role": "user", "content": your_prompt}],
)
```

You are not billed for refused requests. When you retry, a "fallback credit" refunds the prompt-cache cost of switching. The SDK middleware for TypeScript, Python, Go, Java, and C# handles all of this transparently if you prefer not to write the logic yourself.

## The Data Retention Issue

This caught many teams off guard. Claude Fable 5 requires a **30-day data retention policy** for all traffic. This means Anthropic retains your inputs and outputs for 30 days for safety monitoring.

The impact has been immediate:

- **Microsoft restricted employees** from using Fable 5 (1,443 upvotes on r/ClaudeAI). Top comment (453 upvotes): "This is just common sense, mature governance. It'd be insane for any organization to enable Fable during the data retention phase."
- r/singularity user (126 upvotes): "Fable is the only model with data retention for all traffic so that's a red flag for any company that wants to prevent data from flowing out"
- One commenter admitted: "It's enabled by default in Enterprise subscription. Our management is not aware of the changes in policy and I don't want to tell them"

**Bottom line for enterprise teams:** If you handle sensitive data (patient records, proprietary code, internal communications), evaluate whether the 30-day retention is compatible with your compliance requirements before enabling Fable 5.

## Pricing: The Real Cost and How to Manage It

The sticker shock is real. At $50/MTok output, Fable 5 is 2x Opus 4.8 and 67% more than GPT-5.5. But raw token price is not the full picture.

**Three levers that change the math:**

1. **Prompt caching** - 90% discount on cached input. If your system prompt is 10K tokens and you're sending 100 requests, that's $0.10 total for inputs instead of $1.00. Essential.
2. **Batch API** - 50% off. Fable 5 batch pricing ($5/$25) is identical to Opus 4.8's standard pricing. If latency doesn't matter, batch is free capability upgrade.
3. **Effort routing** - Fable 5 on `medium` effort for routine tasks uses fewer tokens than Opus 4.8 on `xhigh` and still outperforms it. Not every request needs `high`.

**What the community says:**

- r/ClaudeAI: "Claude Fable 5 pricing is $50/Million tokens... are we reaching enterprise-only AI?"
- r/Anthropic (93 upvotes): "Paying $200/mo just for the model it's all about to be locked behind usage credits after June 20th. Seriously not seeing the value anymore compared to my Codex subscription."
- Counterpoint from r/claude: "Drains tokens like crazy but output quality is at 4x compared to Opus 4.8, at least that's what my stomach tells me."

**The cost-discipline strategy:** Route by task complexity. Reserve Fable 5 for problems where its capability gap matters (migrations, multi-day agents, complex debugging). Keep Opus 4.8 as default. The benchmarks confirm Fable 5's lead widens on long/complex tasks but narrows on shorter, well-scoped work - so the routing actually saves money without sacrificing quality on the hard stuff.

## What Builders Are Actually Making (48 Hours In)

The pattern that keeps repeating: tasks that required 10+ iterations with Opus now complete in one shot.

- **Full games from a single prompt** - Horror games, Minecraft clones, Backrooms escape rooms, even crude Fortnite and GTA recreations. r/singularity's "It's over. Claude Fable 5 one-shots horror game live" hit 1,893 upvotes. Top comment (570 upvotes): "Holy, I still remember the first time I made a game with Claude 2 years ago, we've come a long way."
- **Production websites in minutes** - Luke Carter built 6 websites in 17 minutes (landing page to full 3D immersive experience, one prompt each). AM Design, a professional agency, said: "This is the first model whose output didn't look AI-made. Real hierarchy, intentional whitespace, actual restraint."
- **50-million-line codebase migration** - Completed in a single day during Anthropic's early-access period. Not a toy demo.
- **tef's viral demo** (10K views, 2,845 likes): Minecraft, Fortnite, and GTA built one prompt at a time. The comment section treated it like a magic show.

The GitHub ecosystem moved fast too. OmniRoute shipped `claude-fable-5` support within hours. Kiro's issue tracker filled with "When is Fable coming?" requests (15 reactions, 12 comments on the feature request).

## When to Use Fable 5 vs. Stay on Opus 4.8

**Use Claude Fable 5 when:**

- Large codebase migrations (it completed a 50-million-line migration in a day)
- Multi-day autonomous coding sessions
- Complex debugging that previous models couldn't solve
- Agent workflows that require planning across stages and self-verification
- You need the model to write its own tests and check its own work

**Stay on Opus 4.8 when:**

- Routine coding (classification, summarization, simple edits)
- High-volume, latency-sensitive workloads
- You handle sensitive/regulated data (data retention concern)
- Budget-constrained development (2x cheaper)
- Tasks that are well-scoped and don't need multi-step reasoning

**Consider GPT-5.5 when:**

- Terminal-heavy DevOps and shell automation (strong via Codex CLI)
- Batch workloads at scale (40% cheaper at batch pricing)
- You're embedded in the OpenAI ecosystem

## Common Mistakes (and How to Avoid Them)

Based on what I found across GitHub issues, Reddit threads, and HN comments in the first 48 hours:

| Mistake | What happens | Fix |
| --- | --- | --- |
| Passing `thinking: {"type": "disabled"}` | Returns 400 error. Fable 5 always uses adaptive thinking. | Remove the `thinking` parameter entirely. |
| Not using streaming for long outputs | SDK raises `ValueError` for max\_tokens above ~16K | Set `stream=True` for any substantive generation. |
| No refusal fallback logic | Your app breaks silently when safety classifiers fire | Add `fallbacks=["claude-opus-4-8"]` or handle `stop_reason: "refusal"`. |
| Giving vague scope on agent tasks | Fable 5 proactively modifies files you didn't ask about | State boundaries explicitly: "Only modify X. Do not touch Y." |
| Using Fable 5 for simple tasks | Burning 2x the budget with no quality difference | Route by complexity. Fable 5 on `medium` effort for routine work, or just use Opus 4.8. |
| Sending sensitive data without checking retention policy | 30-day retention means Anthropic stores your inputs/outputs | Audit compliance requirements first. Consider Opus 4.8 for sensitive workloads. |

## Quick-Start Checklist

1. **Access the model**: Use `claude-fable-5` as the model string in API, or select from the picker in Claude.ai/Cursor/Claude Code
2. **Set effort level**: Start with `high`, drop to `medium` for routine tasks, use `xhigh` only for the hardest problems
3. **Handle refusals**: Implement fallback logic to Opus 4.8 for API integrations (SDK middleware or `fallbacks` parameter)
4. **Use streaming**: Required for requests with max\_tokens above ~16K. With 128K max output, you'll almost always be streaming.
5. **Cache system prompts**: 90% discount on cached input tokens. Essential for cost management.
6. **Set boundaries**: Tell the model what NOT to touch. It's proactive and will modify things outside your scope otherwise.
7. **Evaluate data retention**: 30-day retention is mandatory. Check compliance requirements before enabling for production.

## Timeline and Availability

| Date | Event |
| --- | --- |
| June 9, 2026 | Launch. Available on Pro, Max, Team, Enterprise at no extra cost. |
| June 22, 2026 | Last day of free access on subscription plans. |
| June 23, 2026 | Moves to usage credits only. |
| TBD | Anthropic aims to restore Fable 5 on subscription plans when capacity allows. |

The model is live today on: Claude API (direct), Claude Platform on AWS, Amazon Bedrock, Google Cloud Vertex AI, and Microsoft Foundry.

## Final Take

Claude Fable 5 is the strongest coding and reasoning model publicly available right now. The benchmarks back it up (80.3% SWE-Bench Pro, 29.3% FrontierCode Diamond - nobody else is close). The community confirms it in practice: builders are one-shotting entire games, shipping websites in minutes, and running multi-day autonomous sessions that previously required constant hand-holding.

The tradeoffs are real. Safety classifiers will trip you on legitimate cybersecurity and biology work. The data retention policy makes it a non-starter for some enterprise teams. The pricing (2x Opus) means you should route by task complexity, not switch wholesale.

The smart move: use Fable 5 for the hard jobs. Keep Opus 4.8 for everything else. Try problems you weren't able to solve with other models - that's literally what Anthropic built it for.

On Anthropic's published benchmarks, yes - Fable 5 leads GPT-5.5 on every shared benchmark. SWE-Bench Pro: 80.3% vs 58.6%. FrontierCode Diamond: 29.3% vs 5.7%. But GPT-5.5 costs 40% less at batch pricing and is stronger in terminal-centric coding via Codex CLI. For raw capability, Fable 5 wins. For cost-sensitive batch workloads, GPT-5.5 is the sharper value.

Same underlying model. Fable 5 has safety classifiers that block cybersecurity, biology, and chemistry requests (falling back to Opus 4.8). Mythos 5 does not have those classifiers. You cannot access Mythos 5 unless you are an approved partner in Anthropic's Project Glasswing program.

Through June 22, 2026, Fable 5 is included at no extra cost on Claude Pro ($20/mo), Max ($100-200/mo), Team, and Enterprise plans. After June 23, it requires usage credits. On the API, it costs $10 per million input tokens and $50 per million output tokens from day one.

Fable 5 includes safety classifiers for cybersecurity, biology, chemistry, and frontier AI research topics. These trigger in under 5% of sessions according to Anthropic. When triggered, your request is either refused or automatically rerouted to Opus 4.8. You can implement fallback logic in your API calls to handle this gracefully.

Yes. Select Claude Fable 5 from the model dropdown. It is the top-scoring model on CursorBench. Anthropic specifically recommends running Fable 5 inside agent harnesses like Cursor and Claude Code for long-horizon coding work.

Yes. Anthropic requires a 30-day data retention period for all Fable 5 and Mythos 5 traffic for safety monitoring purposes. This has led multiple companies (including Microsoft) to restrict employee access. Evaluate your compliance requirements before enabling.

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
