---
type: social-post
created: 2026-09-05
updated: 2026-09-05
tags:
  - post
platforms:
  - linkedin
  - x
pages_used:
  - "[[Context Engineering]]"
  - "[[Addy Osmani - Audit your Agent files]]"
  - "[[Meta - An Organizational Second Brain]]"
  - "[[Institutional Knowledge Agents]]"
  - "[[Agent Skill]]"
topics:
  - agent context files
  - instruction bloat
  - negative results
  - evaluating prompts
covers_from: 2026-08-29
covers_through: 2026-09-05
status: ready
---

# 2026-09-05 Nobody Tests the Instructions

## LinkedIn post

Your CLAUDE.md might be doing nothing. There's finally a number on it.

A study of 288 runs across 17 tasks found that the presence of an AGENTS.md or CLAUDE.md made no clear difference to correctness. Anthropic separately removed more than 80% of Claude Code's own system prompt with no measurable loss on evals. A 100-repo audit found context bloat in 42%.

Then the same week, Meta published the opposite result: a compliance agent running on 200+ text instruction files, no model retraining, roughly 80% fewer tokens per turn.

So the files can work. What separates them?

Meta's files sit under regression suites, a deterministic linter that passes or fails, and a hard rule that procedures never contain facts. Most repos' agent files have never been evaluated once — not badly, just never.

An untested instruction file isn't documentation. It's a drawer of sticky notes everyone stopped reading and nobody feels authorized to throw away.

Both sides are messy. The null result only measures correctness, and agents with context files did write more targeted tests, which a per-task score can't see. Meta's figures are qualitative, and its "zero regressions" was scored by a suite the same loop wrote.

The rule that survives both: an instruction must justify itself against an eval, and the default action for an unjustified rule is deletion.

When did you last delete a rule from your agent file and measure what happened?

(Via Addy Osmani, "Audit your Agent files" — https://addyo.substack.com/p/audit-your-agent-files)

#ContextEngineering #AIAgents #DeveloperTooling #LLMEvaluation #PromptEngineering

## X post

<!-- URLs count as 23 characters on X regardless of length; counts below include that. -->

**A) Standalone** (276 chars):

```
288 runs across 17 tasks: having an AGENTS.md or CLAUDE.md made no clear difference to correctness.

Anthropic cut >80% of Claude Code's own system prompt with no measurable eval loss.

Files like these can work. Most have just never been tested once.

https://addyo.substack.com/p/audit-your-agent-files
```

**B) Thread:**

1. (209 chars)
```
288 runs across 17 tasks: the presence of an AGENTS.md or CLAUDE.md made no clear difference to correctness.

It changed how the agents worked — they wrote more targeted tests. The outcome measure didn't move.
```

2. (221 chars)
```
Worse for the "more context is better" crowd: Anthropic removed more than 80% of Claude Code's own system prompt with no measurable loss on evals.

An audit of 100 repos found lint leakage in 62% and context bloat in 42%.
```

3. (221 chars)
```
But the same week, Meta shipped the opposite result: a compliance agent running on 200+ text instruction files, no retraining, ~80% fewer tokens per turn.

So the files can work. The question is what makes the difference.
```

4. (236 chars)
```
Meta's files sit under regression suites, a deterministic linter that passes or fails, and a hard split between procedures and facts.

Your repo's agent file has probably never been evaluated once. That's the variable — not the writing.
```

5. (213 chars)
```
Both sides are messy. The null measures correctness only, and agents with context files did write better tests. Meta's numbers are qualitative, and its "zero regressions" was scored by a suite the same loop wrote.
```

6. (193 chars)
```
Working rule: an instruction must justify itself against an eval, and the default action for an unjustified rule is deletion.

Via Addy Osmani, "Audit your Agent files": https://addyo.substack.com/p/audit-your-agent-files
```

**Ship: B.** Post 5 is the reason — it carries both sides' caveats, and this is a topic where a confident null
result will draw people who have read the underlying studies. The standalone is the fallback: it makes no claim
about *why* the files fail, only that they were never tested, so nothing in it depends on the caveat it has no
room for. No hashtags on either.

## Hook variants

1. **The number.** "288 runs across 17 tasks. Having an AGENTS.md or CLAUDE.md made no clear difference to correctness."
2. **The analogy.** "An untested instruction file isn't documentation. It's a drawer of sticky notes everyone stopped reading and nobody feels authorized to throw away."
3. **The myth-correction.** "Your CLAUDE.md might be doing nothing. There's finally a number on it."

**Recommended:** 3 for LinkedIn. It targets an artifact most of the audience personally maintains and puts it in doubt in nine words, which is what survives feed truncation. Variant 2 is the better sentence but the post needs it as the mid-point turn, and spending it first leaves the argument without a landing. Variant 1 is the most defensible opening but front-loads methodology to readers who don't yet know why they should care.

**On X, lead with variant 1.** That audience wants the study before the framing, and "your file might be doing nothing" reads as bait there while the raw n reads as evidence. Both shipped X forms therefore open on the 288-run number.

## Why this topic

Window: 2026-08-29 → 2026-09-05. Three ingests (2026-08-30, 09-03, 09-04) adding 22 source IDs, plus three lint passes.

| Candidate | Surprise | Concrete | Reach | Fresh | Total |
|---|---|---|---|---|---|
| **Agent context files show no correctness gain; the ones that work are tested** | 5 | 5 | 5 | 5 | **20** |
| pass@k is the wrong metric (pass@3 = 0.6 vs pass^3 = 0.4); temperature 0 isn't deterministic | 4 | 5 | 4 | 5 | 18 |
| The local metric trap — GitHub cut per-response tokens and raised total cost | 4 | 5 | 4 | 5 | 18 |
| Unsolvable eval tasks teach misbehaviour: 198 of 898 generated 93% of illicit coordination | 5 | 5 | 4 | 3 | 17 |
| Agentic kernel optimization pays inversely to prior human effort (42.3% / 15.2% / ~5.5%) | 4 | 5 | 3 | 5 | 17 |
| 78 official extension examples audited: 60 stateless, and of the 17 stateful only 2 correct | 4 | 5 | 3 | 5 | 17 |

Chose the context-files angle because the vault holds **both halves of a contradiction that landed five days apart**
and neither source knows about the other. Osmani's null result arrived 2026-08-30; Meta's working 200+ file system
arrived 2026-09-04. The reconciliation — that the discriminator is evaluation, not authorship — is the vault's, not
either source's, which is what the workflow asks for. It also has the widest reach of anything in the window: the
artifact under discussion is one most of the audience personally maintains.

The unsolvable-tasks angle scored lower only on freshness. It is the strongest *idea* in the window, but it sits in
the same post-training territory as last week's KL post and would make two consecutive RL-training posts. Held for
a later run, where it will still be good.

## Fact check

| Claim in post | Traced to | Verdict |
|---|---|---|
| 288 runs across 17 tasks; no clear difference to correctness | [[Addy Osmani - Audit your Agent files]], "Key claims"; restated on [[Context Engineering]] | ✅ verbatim |
| Agents with context files wrote more targeted tests | Same, both pages | ✅ included because omitting it would overstate the null |
| Anthropic removed >80% of Claude Code's system prompt, no measurable eval loss | Same | ✅ verbatim, incl. "more than" |
| 100 repositories: context bloat 42% | Same ("A June study of 100 repositories") | ✅ verbatim. Lint leakage 62% was cut from the LinkedIn body for length and is retained in X thread post 2; skill leakage 35% appears in neither variant. Nothing contradicted |
| Meta: 200+ text files, no model retraining, ~80% fewer tokens per turn | [[Meta - An Organizational Second Brain]]; [[Institutional Knowledge Agents]] | ✅ "roughly/~80%" hedge preserved; the vault records the 80% as unattributed across several simultaneous changes |
| Meta's regression suites, pass/fail deterministic linter, procedures-vs-facts separation | Same: "recipes reference knowledge files but contain no domain facts; knowledge files state positions but prescribe no procedures"; linter "passes or fails" | ✅ |
| "Zero regressions" scored by a suite the same loop wrote | [[Meta - An Organizational Second Brain]], recorded limits | ✅ hedged in both post bodies |
| Null result measures correctness only; may be a measurement limit | [[Addy Osmani - Audit your Agent files]], "Tensions / open questions" | ✅ hedged in body |
| "Instructions must justify themselves against an eval; default action is deletion" | [[Context Engineering]], "The null result this page has to answer" | ✅ vault's own formulation |
| Attribution: Addy Osmani; URL | Same, `source_author` / `source_url` | ✅ |

**Cut during fact-check:**

- A line reading "context files make agents worse" was cut. No source claims harm to correctness; the finding is a
  null, and bloat findings concern token cost and constraint, not accuracy.
- "Meta proved instruction files work" was cut. The vault files that report as a **design report, not evidence of
  effectiveness** — no baselines, no task counts, no comparison against fine-tuning. Rewritten to "shipped the
  opposite result," which claims a published outcome rather than a proof.
- A causal claim that Meta's linter is *why* its files work was cut. The two sources were never compared under
  controlled conditions; the post presents evaluation as the visible difference, not as a demonstrated cause.
- The 4/45 vs 27/45 prose-summaries-versus-source-code finding was cut for length. It is the window's second-best
  detail and is logged below rather than squeezed in.

**Compression check (X variant):**

- Thread post 5 exists solely to carry both caveats, and is placed second-to-last per the template rule. Nothing
  was shortened by dropping a qualifier.
- The standalone cannot carry the measurement-limit caveat, so it was written to need none: it states the null and
  the untested-files observation, and makes **no claim about why** the files underperform. The first draft ended
  "The files aren't the problem. Nobody tests them," which asserts a cause the vault does not establish; replaced
  with "Files like these can work. Most have just never been tested once."
- "More than 80%" compresses to ">80%" in the standalone — a notation change, not a weakening.
- Attribution survives both forms: the standalone links the source, thread post 6 names Osmani and links it.
- Counts computed, not estimated, with URLs at X's fixed 23 characters. All 7 blocks under 280.

## Attribution

- **Addy Osmani**, *Audit your Agent files* — https://addyo.substack.com/p/audit-your-agent-files
- **Meta Engineering**, *An Organizational Second Brain: Building an AI That Learns From Experts* —
  https://engineering.fb.com/2026/09/02/ml-applications/organizational-second-brain-ai-learns-from-experts/
- Osmani is credited inline in both post bodies; Meta is named inline in both. The 288-run and Anthropic findings
  are studies Osmani reports rather than his own work, which is why both bodies say "via".

## Hashtags

**LinkedIn:** `#ContextEngineering #AIAgents #DeveloperTooling #LLMEvaluation #PromptEngineering`

**X:** none.

## Related pages

- [[Context Engineering]] - spine page; carries the null result this post is built on
- [[Addy Osmani - Audit your Agent files]] - source summary for the negative results
- [[Meta - An Organizational Second Brain]] - source summary for the counterweight
- [[Institutional Knowledge Agents]] - the concept page for Meta's file architecture
- [[Agent Skill]] - skill-specific findings from the same source
- [[Post Archive]] - ledger of posts and spine-page cooldowns
