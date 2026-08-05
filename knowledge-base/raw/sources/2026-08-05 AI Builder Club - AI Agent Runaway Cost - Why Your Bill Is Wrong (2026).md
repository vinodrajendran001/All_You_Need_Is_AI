---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-ai-agent-runaway-cost
title: 'AI Agent Runaway Cost: Why Your Bill Is Wrong (2026)'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/ai-agent-runaway-cost
published: '2026-07-27'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# AI Agent Runaway Cost: Why Your Bill Is Wrong (2026)

Someone on the `anthropics/claude-code` tracker went to dinner with his family. A batch classifier had been denied, and the agent started spawning monitors to get around it. He came back to a reported $900 in extra usage credits.

That story is easy to file under carelessness, so here's the one that isn't. A different operator asked Claude to plan the budget for the agent stack he was about to run. It projected $1.73 a month and told him a $2 hard cap was more than enough, with about 15% headroom. He hit the cap in four days and his crons stopped. When he went through the accounting himself, thinking tokens were 47% of his spend, the single largest line, and they had never come up in the budget planning at all.

Both of those are self-reported by users on a public tracker, so treat the dollar amounts as claims. The second one is the subject of this page. His agent did roughly what he asked it to. The number he planned against had three whole categories missing from it, and he only found that out from the invoice.

This page ships three things you can copy. A table of the cost categories that don't appear in session metrics, so you know what to ask your own runner about. `scripts/cost-reconcile.sh`, which counts priced runs against retained runs and refuses to print a total when they don't match. And an agent definition file plus the orchestration rule that together stop recursive fan-out, which is the failure with the largest numbers attached to it.

This is a measurement page. What to do about a bill you can already see is [agent reliability and cost control](/blog/ai-agent-reliability-cost-control), which covers the levers. This one is about whether the number you're looking at is real. It goes deeper than the cost section of [how to become an AI-native company](/blog/how-to-become-an-ai-native-company), which prices one well-behaved loop and stops there.

---

## Artifact 1: The Invisible-Categories Table

Your session view reports on a session. The invoice covers everything billed to the account, including work no session ever saw, and nothing in the session view flags the difference.

The first artifact is a table, because there's nothing to install here. It's the list of questions to put to whatever you run.

Here are four categories sitting in that gap. They come from two different operators, so the table names which one reported each. The first three are from the issue 49745 write-up: his figures, for his own stack, over his 69 sessions. The runtime he was budgeting was a small model on a cheap VPS, with Claude Code as the planner that produced the estimate. The fourth belongs to a different operator, from a thread on r/AI\_Agents, on his own stack, and it played no part in the $2 cap in the story above. None of these figures is a rate.

| Category | Who reported it | What that operator found | Why session metrics miss it |
| --- | --- | --- | --- |
| Thinking tokens | Issue 49745 | 47% of his total spend, the largest single line | Billed as output, not surfaced as its own line, and absent from the budget the model itself proposed |
| Silent auxiliary calls | Issue 49745 | 249 across 69 sessions, for title generation, auto-detect and vision auto-detect | The tool makes them, not the session, so no session records them |
| MCP tool bloat | Issue 49745 | One 29-tool server took his per-session input from about 12K to about 40K tokens | The tool definitions are in the context window before you type anything |
| Idle re-wakes | A different operator, on r/AI\_Agents | A run that exits without recording a disposition gets treated as incomplete and re-woken | The re-run is a new run, and looks like work |

![A diagram titled one box he saw, four he paid for, split into two labelled sources. The upper section is marked source A, claude-code issue 49745, one operator's accounting of his own stack, and holds two panels. The left panel, what his session metrics showed, holds a single box for session tokens, input plus output, and a readout of a projected 1.73 dollars per month labelled the number his session view gave him, then a stretch of empty space marked nothing else was reported here, closing on one category, it looked complete. The right panel, what his bill actually contained, repeats that same session tokens box, marked as the only category his session view showed, and stacks three more categories under it that his session metrics never surfaced, thinking tokens at 47 percent of his spend and the largest single line, 249 silent auxiliary API calls across 69 sessions covering title generation, auto-detect and vision auto-detect, and MCP tool bloat taking one 29 tool server from about 12K to about 40K input tokens per session, with an arrow running down the side to a bar reading he hit the 2 dollar hard cap in 4 days, and a footer reading four lines on his bill, every one of them from issue 49745. A separate band underneath is marked source B, r slash AI_Agents 1v1wehd, a different operator, a different stack, a different bill, and holds one box, idle re-wakes, where a run that exits with no recorded disposition gets re-woken and re-runs, his own figure being an idle heartbeat going from about 0.40 dollars to about 0.06 dollars, with a line stating this is not a line on the bill above and not counted toward that 2 dollar cap. A footnote reads both operators self-report their own figures, neither set was measured by us](/images/blog/ai-native-invisible-cost-categories-diagram.png "A diagram titled one box he saw, four he paid for, split into two labelled sources. The upper section is marked source A, claude-code issue 49745, one operator's accounting of his own stack, and holds two panels. The left panel, what his session metrics showed, holds a single box for session tokens, input plus output, and a readout of a projected 1.73 dollars per month labelled the number his session view gave him, then a stretch of empty space marked nothing else was reported here, closing on one category, it looked complete. The right panel, what his bill actually contained, repeats that same session tokens box, marked as the only category his session view showed, and stacks three more categories under it that his session metrics never surfaced, thinking tokens at 47 percent of his spend and the largest single line, 249 silent auxiliary API calls across 69 sessions covering title generation, auto-detect and vision auto-detect, and MCP tool bloat taking one 29 tool server from about 12K to about 40K input tokens per session, with an arrow running down the side to a bar reading he hit the 2 dollar hard cap in 4 days, and a footer reading four lines on his bill, every one of them from issue 49745. A separate band underneath is marked source B, r slash AI_Agents 1v1wehd, a different operator, a different stack, a different bill, and holds one box, idle re-wakes, where a run that exits with no recorded disposition gets re-woken and re-runs, his own figure being an idle heartbeat going from about 0.40 dollars to about 0.06 dollars, with a line stating this is not a line on the bill above and not counted toward that 2 dollar cap. A footnote reads both operators self-report their own figures, neither set was measured by us")

The last row travels furthest, and it came from somewhere else. A second operator, running six agents on his own stack, traced his bill to an orchestrator that woke, read the plan, queried assignments, extracted facts, concluded there was nothing to do, and exited without recording an explicit disposition of done, blocked or handoff. The system read the missing disposition as an incomplete run and woke it again. Nothing-to-do could re-fire and re-run. He reports an idle heartbeat going from about $0.40 to about $0.06, which is his figure for his six agents, and he attributes it to fixing the exit logic and right-sizing the model together rather than to the disposition alone. His numbers and the $2 cap above belong to two separate bills.

That's why the guardrail config in the pillar carries a `disposition: required: true` line. Whether your own runner does something similar with a run that exits saying nothing is a question worth putting to it before you plan a budget around its numbers.

---

## Artifact 2: The Reconciliation Script

The categories above are what your vendor doesn't show you. This next part is what your own runner doesn't show you, and it's worse, because you built that part.

Our loop runner's log lies in three specific ways. All three are reproducible on this machine as of 2026-07-27, against `loopany v0.16.0`, and all three have the same shape: a query that returns less than you asked for and exits 0.

Runs can carry no price at all. The `costUsd` field is nullable, and a null is not a zero. On our fleet on 2026-07-27 the CLI returned 255 run records across 29 loops, and 85 of them had no cost recorded. 38 of those 85 had run for longer than five minutes. What those 38 cost is an open question, because a duration is not a price and the log declines to give one. The sharpest single case is a visibility-check run on 2026-07-27 that ran for 7,800,589 milliseconds, about two hours ten minutes, collected 257 records by its own report, and carries `costUsd: null`. Its own run message explains why. The server had already reclaimed the run by the time the terminal tried to report, so every CLI verb returned a conflict. Two hours of metered model work, and no price on the record for any of it.

Then the window caps itself. `loopany log <id> --json --limit 1000` returns 20 rows, and so do `--limit 100` and `--limit 21`. The JSON carries no total anywhere in it, so a 20-element array is what a complete history and a truncated one both look like. Only the human-readable output says `count: 20 of 71 total`. Sum the JSON for that loop and you've priced 20 runs out of 71 while your script reports a clean number.

The third one took me longest to pin down, because it refuses to hold still. `loopany log <id> --json > file.json` writes 74,017 bytes for one of our loops, 8 records. Piped into anything, that same command came back cut to 65,536 bytes on 28 of 40 attempts and came back whole on the other 12. Ask for more history and it gets worse. At `--limit 1000` the file redirect writes 190,249 bytes and 20 records, while 40 piped attempts came back at either 65,536 or 131,072 bytes, and not one of them came back whole. Every attempt exited 0, cut or not.

Those two cut points are pipe-buffer multiples, 64KiB and 128KiB, so what's happening is a write that stops on a buffer boundary and reports success. Every truncated result across those 80 reads was invalid JSON rather than a shorter valid array, which is the one piece of luck in it: `jq` fails loudly instead of quietly pricing 3 runs out of 8. Put `2>/dev/null` on the pipeline and you've taken the loud failure away and left yourself an empty variable that arithmetic treats as zero. The intermittency is what makes this worth a check rather than a workaround. A pipeline that always cut at 64KiB is one you'd notice in an afternoon and design around. One that hands you the whole history 12 times out of 40 is one you'll come to trust.

So the script never pipes the JSON, and it checks five things before it prints anything. The first is the plain one that's easiest to skip: both fetches have to have exited 0. A runner that dies partway can leave a complete, well-formed JSON array on stdout describing a fraction of the history, and every later check will wave that through.

bash

```
#!/usr/bin/env bash
#
# cost-reconcile.sh - print a loop's true metered cost, or refuse.
#
# The point of this script is the refusal. Summing the cost column of a run log
# gives you a number whether or not the log is complete, and a partial total
# looks exactly like a complete one. This checks five things before it prints
# anything, and exits non-zero if any of them fail:
#
#   1. Both fetches exited 0. A producer that failed never yields a total, no
#      matter how much well-formed JSON it managed to write before it died.
#   2. The runner answered, and answered with a run log rather than an error.
#   3. The JSON parses completely. A stream cut off mid-record is rejected,
#      not silently re-parsed as fewer runs.
#   4. The number of runs returned equals the number of runs the runner says it
#      is retaining. Not "at least": equal. Fewer means a capped window, more
#      means the two answers disagree and neither is trustworthy.
#   5. Every run in that window carries a price. One unpriced run means the sum
#      is a floor, not a total.
#
# Written against loopany v0.16.0. Two behaviours of that CLI are the reason
# checks 3 and 4 exist, and both are reproducible on this machine:
#
#   - `loopany log <id> --json` truncates intermittently when stdout is a pipe,
#     and exits 0 when it does. On one loop whose file redirect writes 74,017
#     bytes, 28 of 40 piped reads came back cut to 65,536 bytes and the other 12
#     came back whole. At `--limit 1000`, where the file redirect writes 190,249
#     bytes, 40 piped reads came back at either 65,536 or 131,072 bytes and not
#     one came back whole. The cuts land on pipe-buffer boundaries, 64KiB and
#     128KiB, and every truncated result was invalid JSON rather than a shorter
#     valid array. So `loopany log <id> --json | jq ...` corrupts some of the
#     time, at a boundary that moves, with nothing in the exit status to say so.
#     This script never pipes the JSON.
#   - `--limit` is capped at 20 rows and the JSON carries no total, so a loop
#     with more retained runs than that returns a short array that looks whole.
#     Only the human-readable output declares "count: N of M total", so this
#     script reads both and compares them.
#
# Usage:  scripts/cost-reconcile.sh <loop-id> [<loop-id> ...]
#
# Exit:   0  every named loop reconciled, totals printed
#         1  at least one loop refused
#         2  bad usage or a missing dependency
#
# Porting it: LOOPANY_BIN swaps the runner binary. If your runner is not
# loopany, the two functions to rewrite are fetch_json and fetch_declared_total.
# Both must return the producer's own exit status. Keep the five checks.

set -euo pipefail

LOOPANY_BIN="${LOOPANY_BIN:-loopany}"
FETCH_LIMIT="${FETCH_LIMIT:-1000}"

die() {
  printf 'cost-reconcile: %s\n' "$1" >&2
  exit "${2:-2}"
}

require() {
  command -v "$1" >/dev/null 2>&1 || die "$1 is required and was not found on PATH"
}

# Fetch the run log as JSON into a file. Never into a pipe: see the header.
# Returns the runner's own exit status. Do not swallow it.
fetch_json() {
  local loop="$1" dest="$2" rc=0
  "$LOOPANY_BIN" log "$loop" --json --limit "$FETCH_LIMIT" >"$dest" 2>"$dest.err" || rc=$?
  return "$rc"
}

# Fetch the human-readable header, which is the only place the runner states
# how many runs it is retaining in total. Returns the runner's exit status too.
fetch_declared_total() {
  local loop="$1" dest="$2" rc=0
  "$LOOPANY_BIN" log "$loop" --limit "$FETCH_LIMIT" >"$dest" 2>"$dest.err" || rc=$?
  return "$rc"
}

# Print up to four lines of whatever the runner said, indented, from stdout if
# it wrote anything there and from stderr otherwise.
echo_runner_output() {
  local out="$1"
  if [ -s "$out" ]; then
    head -4 "$out" | sed 's/^/         > /'
  elif [ -s "$out.err" ]; then
    head -4 "$out.err" | sed 's/^/         > /'
  fi
}

reconcile_one() {
  local loop="$1"
  local workdir json text
  local json_rc=0 text_rc=0
  workdir="$(mktemp -d)"
  # shellcheck disable=SC2064
  trap "rm -rf '$workdir'" RETURN
  json="$workdir/runs.json"
  text="$workdir/runs.txt"

  fetch_json "$loop" "$json" || json_rc=$?
  fetch_declared_total "$loop" "$text" || text_rc=$?

  # Check 1: did both fetches exit 0?
  # This is first because it is the only check that cannot be fooled by
  # well-formed output. A runner that dies partway through can leave a complete
  # JSON array on stdout describing a fraction of the history, and every later
  # check would pass it. A non-zero exit means no total, whatever was written.
  if [ "$json_rc" -ne 0 ] || [ "$text_rc" -ne 0 ]; then
    printf 'REFUSED  %s\n' "$loop"
    printf '         the runner exited non-zero (json %s, text %s). Whatever it wrote before\n' \
      "$json_rc" "$text_rc"
    printf '         exiting is not a run log. No total.\n'
    if [ "$json_rc" -ne 0 ]; then
      echo_runner_output "$json"
    else
      echo_runner_output "$text"
    fi
    return 1
  fi

  # Check 2: did we get anything, and is it a run log rather than an error?
  # On loopany v0.16.0 an unknown loop id exits 1 and prints `error: "..."` plus
  # `code: NOT_FOUND` on stdout, so check 1 already catches that case. The grep
  # stays for the case an exit code cannot catch: a runner that reports a
  # failure in its output while still exiting 0.
  if [ ! -s "$json" ]; then
    printf 'REFUSED  %s\n' "$loop"
    printf '         the runner exited 0 and returned nothing. No total.\n'
    return 1
  fi
  if grep -qE '^(error|code):' "$json"; then
    printf 'REFUSED  %s\n' "$loop"
    printf '         the runner exited 0 but reported an error instead of a run log:\n'
    echo_runner_output "$json"
    printf '         No total.\n'
    return 1
  fi

  # Check 3: does the whole document parse? A truncated array fails here, which
  # is the entire reason this is a separate check from the count.
  if ! jq -e 'type == "array"' "$json" >/dev/null 2>&1; then
    printf 'REFUSED  %s\n' "$loop"
    printf '         the run log did not parse as a complete JSON array (%s bytes read).\n' \
      "$(wc -c <"$json" | tr -d ' ')"
    printf '         A truncated stream is not a short history. No total.\n'
    return 1
  fi

  local returned priced unpriced sum declared
  returned="$(jq 'length' "$json")"

  if [ "$returned" -eq 0 ]; then
    printf 'REFUSED  %s\n' "$loop"
    printf '         the run log is an empty array. Either the loop has never run or the\n'
    printf '         query returned nothing. Both are indistinguishable from here. No total.\n'
    return 1
  fi

  # Reject records that are not shaped like runs before trusting the cost field.
  if ! jq -e 'all(.[]; type == "object" and has("costUsd"))' "$json" >/dev/null 2>&1; then
    printf 'REFUSED  %s\n' "$loop"
    printf '         at least one record is not a run object with a costUsd field.\n'
    printf '         The log is not the shape this script knows how to price. No total.\n'
    return 1
  fi

  priced="$(jq '[.[] | select(.costUsd != null and (.costUsd | type) == "number")] | length' "$json")"
  unpriced=$((returned - priced))
  sum="$(jq -r '[.[] | select(.costUsd != null and (.costUsd | type) == "number") | .costUsd] | add // 0 | . * 100 | round / 100' "$json")"

  # Check 4: is the window we read exactly the whole retained window?
  declared="$(sed -n 's/^count: [0-9][0-9]* of \([0-9][0-9]*\) total$/\1/p' "$text" | head -1)"
  if [ -z "$declared" ]; then
    printf 'REFUSED  %s\n' "$loop"
    printf '         could not read a "count: N of M total" line, so there is no way to tell\n'
    printf '         whether the %s runs returned are the whole history. No total.\n' "$returned"
    return 1
  fi
  if [ "$returned" -lt "$declared" ]; then
    printf 'REFUSED  %s\n' "$loop"
    printf '         %s of %s retained runs returned. The runner caps the page below its own\n' \
      "$returned" "$declared"
    printf '         history, so the visible rows are a window, not the log.\n'
    printf '         Priced rows in the window sum to $%s. That is a floor for the window\n' "$sum"
    printf '         alone, and no bound at all on the loop. No total.\n'
    return 1
  fi
  if [ "$returned" -gt "$declared" ]; then
    printf 'REFUSED  %s\n' "$loop"
    printf '         %s runs returned against %s the runner says it retains. The two answers\n' \
      "$returned" "$declared"
    printf '         disagree, so neither one describes the history. No total.\n'
    return 1
  fi

  # Check 5: is every run in that window priced?
  if [ "$priced" -eq 0 ]; then
    printf 'REFUSED  %s\n' "$loop"
    printf '         %s runs, and the log records a price for none of them. A null is the runner\n' "$returned"
    printf '         declining to say, so there is nothing here to add up and nothing to bound it\n'
    printf '         with either. No total.\n'
    return 1
  fi
  if [ "$unpriced" -gt 0 ]; then
    printf 'REFUSED  %s\n' "$loop"
    printf '         %s of %s runs priced, %s with no cost recorded.\n' "$priced" "$returned" "$unpriced"
    printf '         Priced rows sum to $%s, which is a floor, not a total. A null price is the\n' "$sum"
    printf '         runner declining to say what a run cost, not a record of zero, so what sits\n'
    printf '         above that floor is unknown here rather than small. No total.\n'
    return 1
  fi

  printf 'OK       %s\n' "$loop"
  printf '         %s of %s runs priced. Metered total: $%s\n' "$priced" "$declared" "$sum"
  jq -r '.[] | "         \(.ts[0:16] | sub("T"; " "))  \(.role)  \(.outcome // "-")  $\(.costUsd)"' "$json"
  return 0
}

main() {
  [ "$#" -ge 1 ] || die "usage: cost-reconcile.sh <loop-id> [<loop-id> ...]"
  require jq
  require "$LOOPANY_BIN"

  local failures=0
  for loop in "$@"; do
    reconcile_one "$loop" || failures=$((failures + 1))
    printf '\n'
  done

  if [ "$failures" -gt 0 ]; then
    printf '%s of %s loops refused. Do not add the printed floors together.\n' "$failures" "$#" >&2
    exit 1
  fi
  exit 0
}

main "$@"
```

Save it as `scripts/cost-reconcile.sh`, `chmod +x`, and pass it loop ids. It needs `jq` and your runner on `PATH`, no key and no account anywhere. `shellcheck` is clean on it.

On a loop whose history is whole, it prints the total and the rows behind it:

text

```
OK       loop-mry8g8f2-5daaf53d
         6 of 6 runs priced. Metered total: $19.06
         2026-07-27 00:29  evolve  evolve  $3.102419
         2026-07-27 00:21  exec  exec  $4.0711485
         2026-07-26 03:23  exec  error  $3.2364104
         2026-07-25 04:03  exec  error  $3.4116462
         2026-07-24 01:14  evolve  evolve  $0.953405
         2026-07-24 01:12  exec  exec  $4.28062
```

On one whose history isn't, it says what's missing and exits 1:

text

```
REFUSED  loop-mr8hfir9-a47fa334
         3 of 6 runs priced, 3 with no cost recorded.
         Priced rows sum to $10.68, which is a floor, not a total. A null price is the
         runner declining to say what a run cost, not a record of zero, so what sits
         above that floor is unknown here rather than small. No total.
```

The refusal is the feature. The obvious one-liner, `loopany log <id> --json | jq '[.[].costUsd // 0] | add'`, prints `10.683629` for that same loop, to seven decimal places, with nothing anywhere to tell you it's short by half the history.

Two design choices worth stating, because without them I'd have stopped running the thing.

The script prints a floor when it refuses, and labels it a floor in the same sentence. A refusal with no number at all is a script I'd have abandoned by the third loop. A floor you can't mistake for a total is still worth having, and the closing line tells you not to add several of them together, because a sum of floors isn't a floor on the sum in any way you'd want to rely on.

The second choice is that `costUsd: 0` counts as priced and `costUsd: null` doesn't. Those look similar and mean opposite things. One of our runs failed on an expired OAuth session and recorded exactly `0`, which is a real and correct price for a run that never reached the model. A null is the runner declining to say.

---

## Artifact 3: The File That Stops the Fan-Out

The first two artifacts deal with measurement. Recursive fan-out is a different kind of failure, the one incident class in this set where the money arrives faster than a person can react to it, and four operators filed it on the same issue in July 2026.

One asked for research on a payment integration and got 48 or more background agents running at once, about 1.5M tokens, with the useful research complete inside the first three or four. One reported 905 agents, his five-hour limit gone in two minutes and $87 in the minute after that, and unplugged the machine to stop it. One reported over 900 agents and roughly $700 in 30 minutes on a company AWS Bedrock account. A fourth posted the tree by depth: 3 calls at the top, then 19, 38, 37 and 2, for 99 subagents across five levels, 241,679,793 tokens, 98% of it subagent traffic. Those dollar figures are self-reported by users seeking refunds.

The mechanism is what made it structural rather than careless. A fifth commenter went through the shipped binary at the version they were running and reported that the spawn tool stayed in a subagent's toolset while depth was under 5, and that nothing anywhere bounded how many children a level could produce. A depth limit says how deep the tree goes and nothing about how wide, so five levels with unbounded width is arithmetic that ends in four figures. He also reported that the built-in agent types shipped a wildcard tool list, which included the spawn tool, so recursion was opt out rather than opt in.

Check the version before you copy any of that forward, because the harness has moved. Anthropic's current subagent documentation gives a nesting depth that defaults to three layers and is settable through `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, with `1` turning nesting off, and it documents a per-session ceiling, `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`, defaulting to 200 subagents in a session. The uncapped-width version of this is closed. What survives is that 200 subagents in one session is still a bill, that both numbers are defaults rather than decisions, and that neither one is your runner's cap if your runner isn't Claude Code.

Two fixes came out of that thread and they work at different layers. Both still hold.

The first is a tool grant. A subagent definition whose `tools` frontmatter leaves out the spawn tool can't spawn children, so the tree stops at one level. Anthropic's documentation is explicit on both halves of this: `tools` inherits every tool available to subagents when it's omitted, and to keep a subagent from spawning you leave `Agent` out of its `tools` list or put it in `disallowedTools`. The tool is called `Agent`; it was renamed from `Task` in v2.1.63 and the old name still resolves as an alias. Save this as `.claude/agents/research-worker.md`:

markdown

```
---
name: research-worker
description: Reads and searches. Cannot write, cannot shell out, cannot spawn children.
tools: [Read, Grep, Glob, WebSearch, WebFetch]
---

You are a research worker. You have been given one question and you answer that
one question.

You do not have a tool that spawns other agents, and this is deliberate. If the
question is bigger than you can answer, say so in your result and stop. Do not
work around it, and do not ask for it to be granted. Deciding that more workers
are needed is the orchestrator's call, and the orchestrator has already made it.

Return: the answer, the sources you actually read, and anything you could not
determine. Say what you did not find.
```

Read that `tools` list for what's absent. No `Agent`, so the fan-out stops at one level. No `Bash`, so read-only means read-only rather than meaning it politely. The commenter who wrote the concrete version of this fix says plainly that the prompt-only version isn't a real solution, because a sufficiently creative model will sometimes ignore it, and by his account it reduces how often the problem happens rather than removing it. The prose in the file above is there to make an ignored instruction survivable, not to be the control.

The second fix is the orchestration shape, and it's the one that generalizes past any particular harness. The orchestrator spawns exactly N workers, waits for all N, and aggregates. No worker ever decides whether more workers are needed. The reason given in the thread is that the orchestrator has no completion signal back from parallel workers, so it keeps spawning to compensate, and a fixed count removes the question rather than answering it.

Then put a ceiling in your own config, counted by children. A depth limit leaves width unbounded, and a vendor default is a number you inherited rather than chose:

yaml

```
# In the runner config, per loop. Not in the prompt.
# These are starting values chosen so the file runs, not measurements.
fanout:
  max_depth: 3                 # starting value
  max_children_total: 8        # starting value. count, not depth
  on_exceed: fail_run          # fail, not warn. a warned run keeps spawning.
```

Set both from your own run log in the first week, and set `on_exceed` to fail, because a run that warns and continues is a run that finishes the job you're trying to stop.

---

## The Same Bill, Read Three Ways

Who's paying decides what the number means. Past a certain headcount the problem changes sign.

Solo, the bill is the alarm and the alarm is cheap. $87 and $900, both self-reported, both noticed within days because one person sees the invoice and that person also wrote the agent. The reconciliation script has the least to do here, because at this scale the invoice is the reconciliation. The categories table is where I'd start instead, since that's the gap between what you planned for and what you're charged.

Put several people behind one key and the invoice stops being anybody's alarm in particular. One of the fan-out reports on that GitHub thread is exactly this case: roughly $700 in 30 minutes on a company AWS Bedrock account, and the reporter's follow-up question in the thread is about how to get a refund. A monthly invoice arrives attributing nothing to anything, which is the gap per-run reconciliation fills.

At organization scale it inverts. Forbes reported Uber exhausting its entire 2026 AI budget by April, four months in, after Claude Code spread across roughly 5,000 engineers faster than its finance models expected, at $150 to $250 a month per engineer with power users between $500 and $2,000. Uber compounded it by ranking engineers on internal leaderboards by usage. Andrew Macdonald, Uber's President and COO, told Fortune the link between that spend and output isn't there yet, and that it's very hard to draw a line from one of those stats to actually producing more useful consumer features. Once usage is the visible proxy for productivity and the leaderboard is public, spending less looks like doing less, and the control you built to hold spend down is competing with an incentive to push it up. Simon Willison logged the response: $1,500 a month per person per AI coding tool, with each tool getting its own allowance, so spend on one has no bearing on the budget for another.

A cap like that is an org-level control and it can't do the job of the run-level ones. It fires monthly and per person, which means it fires once the money has already gone. The `fanout` block above, a retry limit, a per-task token budget and a step timeout all fire inside a single run, which is the only place a runaway is still cheap.

---

## What This Looks Like On Our Side

We run 29 loops across three repos. On 2026-07-27 I pointed the script at every one of them.

Five reconciled. Twenty-four refused. Nineteen of the refusals were unpriced runs and five were the capped window. Across those 29 loops the CLI returned 255 run records, 170 of them priced and 85 not, and 38 of the unpriced ones had durations over five minutes.

That's one fleet on one day, and I'm not offering it as a rate for anyone else's runner. What it does establish is that the incomplete case is the ordinary case here rather than the exception, and that our own cost reporting had been summing whatever the log handed it.

The loop I can price completely is the daily graph SEO engine, six of six runs priced, $19.06 across four days. $6.65 of that went on two runs that failed and produced nothing, one on an API connection closing mid-response and one on an expired OAuth session. A failed run can bill, and those two did. On a different loop a run that failed on an expired OAuth session recorded exactly $0, so failure on its own tells you nothing about the price.

Beside it, the two loops that motivated the script in the first place. Our Tuesday SEO Scout has three of six runs priced, summing to $10.68. Our weekly AI Visibility Check has two of five, summing to $6.34, and one of those two priced runs burned $5.74 before failing on a monthly spend limit, which is a cap firing correctly on a run that returned nothing. Neither of those loops has a total, and neither did before the script existed. What changed is that we now know it.

The two-hour run from earlier belongs to that same visibility loop. It ran, did the work, wrote 257 records, and the server reclaimed it before the terminal could report, so it carries no price at all. Nothing in the JSON marks that record as different from a cheap one.

The pillar quotes the $19.06 history as what a loop costs. That figure is still right, and it's the only one of our loops I'd have been able to say it about.

---

## Receipts

| Claim | Status |
| --- | --- |
| Thinking tokens at 47% of spend; 249 auxiliary calls across 69 sessions; a 29-tool MCP server taking per-session input from about 12K to about 40K; a $1.73 projection with a $2 cap that blew in four days | External, attributed. One operator's own accounting on `anthropics/claude-code` #49745, over his 69 sessions. His figures for his own stack, not a rate, and not measured by us. The article also states what the issue states, that the budgeted runtime was not Claude Code |
| Idle re-wakes: a run exiting with no recorded disposition of done, blocked or handoff gets treated as incomplete and re-woken | External, attributed. A **different** operator's report on r/AI\_Agents, not the one in #49745, which carries no idle or disposition claim. The table and the diagram both name the source per row for this reason. The mechanism is the transferable part. His idle heartbeat went from about $0.40 to about $0.06, and he credits the exit-logic fix and model right-sizing together, which is how it ships here rather than as a 6x attributed to the disposition |
| $900 in extra usage credits after a denied classifier led to dozens of monitors | External. `anthropics/claude-code` #67323. Self-reported by a user seeking a refund |
| 48+ agents on one research call at about 1.5M tokens; 905 agents with a five-hour limit gone in two minutes and $87 in the next; 900+ agents and roughly $700 in 30 minutes on Bedrock; 99 subagents across five levels from 3 initial calls, 241,679,793 tokens, 98% subagent traffic | External. Four operators on `anthropics/claude-code` #68110, July 2026. Dollar figures self-reported by users seeking refunds, so they ship as claims. The depth-by-depth counts are one commenter's posted table |
| At the version those operators ran, the spawn tool stayed in a subagent's toolset while depth was under 5, nothing bounded width, and the built-in agent types shipped a wildcard tool list | External. A fifth commenter's inspection of the shipped binary at v2.1.195, in the same thread. Ships in past tense and version-scoped, because the row below supersedes it |
| Nesting depth now defaults to three layers and is settable through `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, with `1` disabling nesting, and a per-session ceiling `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION` defaults to 200 subagents | External. Anthropic's current subagent documentation, fetched 2026-07-27 at `code.claude.com/docs/en/sub-agents`, which is where `docs.claude.com/en/docs/claude-code/sub-agents` now redirects. This is why the uncapped-width claim is not made in the present tense anywhere on this page |
| `tools` inherits every tool available to subagents when omitted; a subagent is kept from spawning by leaving `Agent` out of `tools` or adding it to `disallowedTools`; the tool was renamed from `Task` in v2.1.63 | External. Anthropic's subagent documentation, same fetch. The fix comes from #68110; the behaviour it depends on is checked at the vendor's own docs rather than inherited from the thread |
| Fixed fan-out: the orchestrator spawns exactly N, waits for all N, aggregates, and no worker decides | External. #68110, from the commenter who also states that the prompt-only version is not a real solution because a sufficiently creative model will sometimes ignore it |
| Uber exhausted its 2026 AI budget by April, four months in, across roughly 5,000 engineers; $150 to $250 per engineer per month, power users $500 to $2,000, usage leaderboards | External. Forbes |
| Uber's President and COO: the link is not there yet, and it is very hard to draw a line from those stats to producing more useful consumer features | External. Andrew Macdonald, in Fortune |
| Uber's cap: $1,500 a month per person per AI coding tool, each tool with its own allowance | External. Simon Willison's write-up, which is the source for the cap itself rather than the Forbes piece |
| `costUsd` is nullable, and 85 of 255 visible run records across our 29 loops carried no price on 2026-07-27, 38 of them with durations over five minutes | Firsthand, and dated. Read from the runner's own JSON on that date. One fleet, one day. Not a rate for any other runner |
| A single run of ours ran 7,800,589 ms, reported 257 records collected, and carries `costUsd: null` because the server reclaimed it before the terminal reported | Firsthand, and dated 2026-07-27. The run's own message states the reclaim |
| `--limit 1000`, `--limit 100` and `--limit 21` all return 20 rows; the JSON carries no total; the text output declares `count: 20 of 71 total` for the same loop | Firsthand, reproducible against `loopany v0.16.0` on 2026-07-27. A statement about this CLI at this version, not about run logs in general |
| Piped, the same command truncates some of the time and at a boundary that moves. One loop, file redirect 74,017 bytes: 28 of 40 piped reads cut to 65,536, 12 whole. Same loop at `--limit 1000`, file redirect 190,249 bytes: 40 of 40 piped reads cut, at 65,536 or 131,072. Exit 0 on all 80. Every truncated result invalid JSON, never a shorter valid array | Firsthand, reproducible on this machine on 2026-07-27, one loop's log, 80 piped reads. A statement about this CLI at this version, not about pipes in general. Round 3 published this as a flat "exactly 65,536 bytes, on eight consecutive attempts", which a wider sample disproved |
| 5 of our 29 loops reconciled and 24 refused, 19 on unpriced runs and 5 on the capped window | Firsthand, dated 2026-07-27, our fleet. Not a prevalence claim about anyone else |
| $19.06 over four days on one daily loop, six of six runs priced, $6.65 of it on two failed runs | Firsthand. Metered per-run cost, already published in the pillar |
| A run on another loop failed on an expired OAuth session and recorded `costUsd: 0`, not null | Firsthand, dated 2026-07-26. This is why the page says a failed run can bill rather than that failed runs bill, and why the script counts 0 as priced |
| Tuesday SEO Scout at 3 of 6 priced summing to $10.68; AI Visibility Check at 2 of 5 summing to $6.34, one of them a $5.74 run that failed on a monthly spend limit | Firsthand, dated 2026-07-27. The floors are labelled as floors here and in the script's own output |
| The `fanout` block's numbers (depth 3, 8 children) | Not a receipt and not a finding. Starting values, labelled in place. Set yours from your own run log |

Four things I wanted in this article and cut. The best-told runaway story in the research came with a top comment accusing the post itself of being machine-written, and this article's own rule is to prefer a scored comment over a disputed original, so none of its numbers appear anywhere on this page, including here. A set of enterprise token figures reaches the research through a summary of two paywalled reports rather than through either report. A tempting figure about a company running its whole operation for the price of a dinner traces back to a garbled transcript and isn't in the primary source. And I couldn't put a number on how much the unpriced runs on our own fleet actually cost, because the whole point of this page is that the log doesn't say, and estimating it would be the exact move the script exists to refuse.

---

## Start Here

Run the reconciliation on one loop today, before you change anything. If it refuses, you've learned that the number you've been quoting was a floor, and that's the finding.

Then ask your runner what a failed run costs on its books, and whether a thinking or reasoning budget gets a line of its own or folds into output. Ask what the tool calls on your key outside a session too. The reconciliation answers none of those, and on our own runner the log didn't either.

After that, read your agent definitions for what's absent from the `tools` list rather than what's present, and check what your harness currently caps and at what number. A depth limit and a width limit bound different things, and the operators on that thread found out which one they had the hard way.

Put the account-level cap in last, once the run-level ones are there. A cap is the control that tells you the least, because by the time it fires you've already spent the money, and you find out at whatever moment it picks.

---

## Related Content

- **[How to Become an AI-Native Company](/blog/how-to-become-an-ai-native-company)** - The pillar this hangs off: which loop to build first, what a well-behaved one costs, and what breaks.
- **[AI Agent Reliability and Cost Control](/blog/ai-agent-reliability-cost-control)** - The other half of this. That page is the levers that move the bill down; this one is whether the bill you're reading is the bill.
- **[Self-Improving Agent Loops](/blog/self-improving-agent-loops)** - The evolve step, which is a cost line of its own. Two of the six runs in the metered history above are evolve runs.
- **[Types of Agentic Loops](/blog/types-of-agentic-loops)** - Open monitors against closed loops, and which shape wakes on a schedule whether or not there's work.
- **[Reviewing AI-Generated Pull Requests](/blog/reviewing-ai-generated-pull-requests)** - Spoke one: the review packet and the AI policy, plus the machine gates that run before a human sees the diff.
- **[A Role Label Is Not a Sandbox](/blog/agent-tool-permissions-canary)** - Spoke three, and the other half of the `tools` grant above: a canary suite that proves a deny rule denies, rather than assuming the absent tool did its job.
- **[Your Agents Have Production Credentials and No Owner](/blog/who-owns-your-ai-agents)** - Spoke four. The same run log read for a different question, plus what a per-run record cannot tell you about which rows an agent changed.
- **[How to Build an SEO Agent Loop](/blog/ai-agent-seo-loop)** - Spoke five. A daily loop priced in this article's terms, and the monitor it needed.
- **[How to Cold-Launch a Social Presence With Agent Loops](/blog/ai-agent-social-loop)** - Spoke six. Seven more loops on the same fleet, and an honest account of what they have earned.
- **[Claude Code Agent Teams](/blog/claude-code-agent-teams-guide)** - Orchestrators and workers, which is where the fan-out rule above gets applied.

[Join AI Builder Club](/pricing?utm_source=blog&utm_medium=article&utm_campaign=ai-agent-runaway-cost)

Because the estimate is built from session metrics and the bill isn't. One operator wrote up the gap on the claude-code tracker after a $1.73 monthly projection hit a $2 hard cap in four days and stopped his crons. His own accounting put thinking tokens at 47% of spend, the largest single category, never mentioned in the budget planning. He also counted 249 auxiliary API calls across 69 sessions for things like title generation and auto-detect, none of which appeared in session metrics, and found that adding a 29-tool MCP server took his per-session input from about 12K to about 40K tokens. Those are his figures for his own stack, not a rate for yours, and the runtime he was budgeting wasn't Claude Code. What travels is the shape: ask your runner what categories its number excludes before you plan against it.

Count the priced runs against the total runs your runner says it's retaining, and refuse to add anything up when those two numbers differ. On our own fleet on 2026-07-27, 85 of the 255 visible run records carried no cost at all, and 38 of those 85 had run for more than five minutes. A null there is the runner declining to say, not a recorded zero, so summing the visible rows gives you a floor that reads like a total. The script in this article does that count and exits non-zero rather than printing a total it can't stand behind.

Leaving the spawn tool out of the worker's grant, and structuring the orchestration so no worker gets to make the call. On claude-code issue 68110 in July 2026, five operators reported the same fan-out, one of them going through the shipped binary and reporting that the spawn tool stayed available while depth was under 5 with nothing bounding width at all. Check your version before carrying that forward: Anthropic's current subagent documentation gives a nesting depth defaulting to three layers, settable through CLAUDE\_CODE\_MAX\_SUBAGENT\_SPAWN\_DEPTH, and a per-session ceiling of 200 subagents through CLAUDE\_CODE\_MAX\_SUBAGENTS\_PER\_SESSION. The two fixes from that thread still stand under either version: a subagent definition whose tools frontmatter leaves out Agent, and fixed fan-out, where the orchestrator spawns exactly N workers, waits for all N, and aggregates. The commenter who wrote the concrete version says the prompt-only version isn't a real solution, because a sufficiently creative model will sometimes ignore it.

It bounds the damage and it tells you nothing. A cap is the last control in the chain, and when it fires you find out at the worst moment. One of our own loops burned $5.74 on a single run on 2026-07-13 and then failed on a monthly spend limit, which is a cap doing its job and a run producing nothing. Put the cap in, then put the controls that fire earlier in front of it: a retry limit, a per-task token budget, a step timeout, and a fan-out limit counted by children rather than by depth.

Some of ours have. In the four-day metered history of one of our daily SEO loops, six of six runs priced, and two runs that failed on infrastructure billed $6.65 between them out of $19.06 total. One failed on an API connection closing mid-response and one on an expired OAuth session. Neither produced anything. A failure is not automatically a charge, though: on another loop a run that failed on an expired OAuth session recorded exactly $0, which is the correct price for work that never reached the model. That's one fleet rather than a rate to plan against, and the reason to put the question to your own runner instead of assuming it either way.

Because at organization scale the meaning of the number changes. Forbes reported Uber exhausting its entire 2026 AI budget by April, four months in, after Claude Code spread across roughly 5,000 engineers, at $150 to $250 a month per engineer with power users between $500 and $2,000, while Uber ranked engineers on internal leaderboards by usage. Andrew Macdonald, Uber's President and COO, told Fortune the link to output isn't there yet and that it's very hard to draw a line from one of those stats to producing more useful consumer features. Once usage is the visible proxy for productivity, low spend reads as low effort, and the incentive points the wrong way. Simon Willison logged what Uber did about it: $1,500 a month per person per AI coding tool, each tool with its own allowance.

Firsthand: the run-log defects, the reconciliation counts and the per-run costs come from the loop runner we use in production at SuperDesign and AI Builder Club, read on 2026-07-27. Every firsthand figure is scoped in the sentence that carries it. Dollar amounts attributed to other operators are self-reported on public issue trackers, unverified by us, and labelled as claims where they appear. See our [editorial standards](/about).
