---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-who-owns-your-ai-agents
title: Who Owns Your AI Agents? A Registry, a Runbook and an Honest Score (2026)
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/who-owns-your-ai-agents
published: '2026-07-28'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Who Owns Your AI Agents? A Registry, a Runbook and an Honest Score (2026)

Start with one agent you already run, and one question about it: when was the last time a human looked at what its credential can reach?

Here's one, described by the person who built it. He'd stood up a few internal agents over a quarter: ticket triage, report assembly, and a nightly reconciliation job that used to belong to a person. To get them working he gave them service credentials, broad ones, because scoping them properly was going to take a week and the demo needed to land. Everyone said they'd tighten it after. They didn't tighten it after.

So the reconciliation agent has read and write on a production database. It has run every night since March. There's no record of what it does in there beyond application logs he'd have to correlate by hand.

Then he writes the sentence this whole page is built on:

> It has probably been fine. I do not know that it has been fine, which is a different sentence.

Sit with the gap between those two clauses, because everything worth doing about this lives inside it. He isn't reporting an incident. Nothing has gone wrong. He's reporting that he has no way to find out, and that the absence of bad news has been doing the work of evidence for four months.

You may not have a word for this. The people who have this problem describe it as a specific agent with a specific credential, while the words that would let you look it up are governance vocabulary borrowed from identity management. That mismatch is worth naming rather than papering over, because it means the fix arrives dressed as compliance work for a problem that feels like a Tuesday. The test that skips the vocabulary is three questions about one agent you already run.

Who gets asked, by name, what it did last night. What it could reach if it went wrong in a way you haven't imagined. And what happens the day you turn it off.

The files are here to be copied. `agents/REGISTRY.md` is a schema whose fields are chosen so that a blank one is a finding. `agents/OFFBOARDING.md` is the retirement runbook, which is the step our own fleet has no version of. Under those sits an action-log contract that gives "what did it do in there" an answer, and the autonomy ladder rewritten as a table with promotion evidence per rung.

It also ships our own score against that schema, which is 1 field out of 10 answered for all 29 of our agents, and a second field that answers for 28 of them. That number is further down and it isn't flattering, which is the reason it's here.

One scoping note before the artifacts. Whether the boundary you configured actually holds is a different question with its own page, [testing that your agent guardrails hold](/blog/agent-tool-permissions-canary). This page assumes your controls work exactly as written and asks who is accountable for them, what they cost you when the agent is retired, and how you'd reconstruct a night's work six months later.

---

## The Evidence Here Is Thin, and That Shapes the Page

The account above is one person's post. When we read it at the source on 2026-07-28 it carried a score of 3, and the replies carrying the fix carried 1 and 2. Compare that to the review-bottleneck problem, where [spoke one](/blog/reviewing-ai-generated-pull-requests) had a 1,904-upvote thread, five published policy files and an 8.1M-PR dataset to work from.

That difference is itself information, and here's the reading I'd offer for it rather than a finding. Anger is what fills a thread, and there's nothing to be angry about yet in an agent that has been fine. Quiet failure mode, quiet thread.

So this page doesn't lean on external volume it doesn't have. It leans on one very specific account, on a second operator's independent conclusion from the org side, and on the thing we can actually measure, which is our own fleet held against the schema and scored where it fails.

![A hand-drawn two-column diagram. The heading reads a person gets six of these, followed by a highlighted phrase, an agent gets none of them, and a subtitle reading joiner-mover-leaver, versus what an agent actually gets, our own fleet, 29 loops, scored 2026-07-28. The left panel is headed a person joins your company and holds six stacked boxes, each with a green tick beside it: identity created, a named record in the directory; access granted, provisioned to a role, scoped to the job; owner assigned, a manager who is asked what they did; reviewed on a cadence, access recertification, someone signs; escalation path, a name, and an out-of-hours contact; and leaves, credentials revoked, checked, record archived. The right panel is headed an agent starts running and holds the same six stages, every one of them marked with a red cross. Identity, no record, it authenticates as a credential somebody already had. Access, whatever that credential could already reach. Owner, whoever last edited the config file, not a field anywhere. Review, nothing fires, nobody signs, it has run every night since March. Escalation, whoever notices. Retirement, the run stops, the credential stays live, so it is switched off, not offboarded. Between the two panels, six gap markers point rightwards into the six crossed rows, reading, in order, no record, no scope, no name, no date, no contact, no revocation. A band across the bottom is headed our own fleet, 29 loops, scored 2026-07-28, and reads 1 of 10 registry fields answerable from the system for all 29 loops, the kill switch, with a sub-line reading that purpose answers for 28 of 29 because one loop's task file is gone from disk, that escalation and the action log are partial, and that six fields have nowhere in the config to live. A two-line footnote reads that the left column is the shape the operator in the thread was comparing against, in his own words, a review, an owner, an offboarding process, and that the right column is our own fleet, one machine, one day, not a survey](/images/blog/ai-native-agent-ownership-gap-diagram.png "A hand-drawn two-column diagram. The heading reads a person gets six of these, followed by a highlighted phrase, an agent gets none of them, and a subtitle reading joiner-mover-leaver, versus what an agent actually gets, our own fleet, 29 loops, scored 2026-07-28. The left panel is headed a person joins your company and holds six stacked boxes, each with a green tick beside it: identity created, a named record in the directory; access granted, provisioned to a role, scoped to the job; owner assigned, a manager who is asked what they did; reviewed on a cadence, access recertification, someone signs; escalation path, a name, and an out-of-hours contact; and leaves, credentials revoked, checked, record archived. The right panel is headed an agent starts running and holds the same six stages, every one of them marked with a red cross. Identity, no record, it authenticates as a credential somebody already had. Access, whatever that credential could already reach. Owner, whoever last edited the config file, not a field anywhere. Review, nothing fires, nobody signs, it has run every night since March. Escalation, whoever notices. Retirement, the run stops, the credential stays live, so it is switched off, not offboarded. Between the two panels, six gap markers point rightwards into the six crossed rows, reading, in order, no record, no scope, no name, no date, no contact, no revocation. A band across the bottom is headed our own fleet, 29 loops, scored 2026-07-28, and reads 1 of 10 registry fields answerable from the system for all 29 loops, the kill switch, with a sub-line reading that purpose answers for 28 of 29 because one loop's task file is gone from disk, that escalation and the action log are partial, and that six fields have nowhere in the config to live. A two-line footnote reads that the left column is the shape the operator in the thread was comparing against, in his own words, a review, an owner, an offboarding process, and that the right column is our own fleet, one machine, one day, not a survey")

---

## Artifact 1: `agents/REGISTRY.md`

The schema is the artifact. The file is a markdown table, and if you want it in a CMDB or a spreadsheet instead, the fields are what transfers.

Two things this file does not do, stated at the top of the file itself so that a reader who finds it later is not misled by it. It records, and it doesn't enforce. Nothing in it revokes a token, stops a run or blocks a write, and every field is a claim that has to be made true somewhere else in your infrastructure. The value is that a wrong claim becomes visible and a blank one becomes a question.

markdown

```
# Agent registry

One row per agent that runs without a human watching it. An agent you trigger by hand
belongs here too, if it holds a credential you would not hand to a contractor on day one.

This file records. It does not enforce. Nothing here revokes a token, stops a run, or
blocks a write. Every field below is a claim that has to be true somewhere else in your
infrastructure. A blank field is a finding rather than a formatting problem.

Rows are generated from whatever runs your agents, then filled in by hand. If an agent
can be absent from this list, the list is decoration.

Last full review: <date> by <name>          Next review due: <date>

## <agent name>

| Field | Value |
|---|---|
| Owner | <one person. first name and last name.> |
| Purpose | <one sentence: what stops being true if you delete it> |
| Reaches | <every system it can touch, one per line> |
| Credential | <the identity it authenticates as, what that identity can do, where the secret lives> |
| Expiry | <the date this row stops being valid> |
| Reviewed | <date> by <name> |
| Escalation | <who gets woken when it goes wrong, out of hours> |
| Kill switch | <the exact command or click that stops it, and who can run it> |
| Autonomy rung | <1-4, and the date it reached that rung> |
| Action log | <where its writes are recorded, and how far back that record goes> |

## Retired

<rows move here, they never get deleted. a deleted row is indistinguishable from an
agent that was never registered.>
```

Ten fields. Each has a reason to exist and a way to fill it that doesn't collapse into guesswork, because a row that can't be filled is worse than no row.

| Field | Why it's there | How to fill it |
| --- | --- | --- |
| `Owner` | A team alias means the question "what did it do last night" has no addressee, and a rota lets each person assume another one read it | Whoever would be embarrassed if it went wrong, which in practice is whoever built it. Then go and tell them |
| `Purpose` | Written as what stops being true when you delete the agent, it doubles as the retirement test | One sentence. An agent whose purpose sentence you can't write is an agent to turn off, and that's the cheapest outcome this file produces |
| `Reaches` | The spec says what an agent is supposed to touch and the credential says what it can touch. The gap between those two is the entire subject | Read the credential rather than the spec. Include what it gets to through another tool, since a shell is a route to everything the machine can reach |
| `Credential` | Three parts, because a single value collapses into a secret-manager path that answers none of them | The identity it authenticates as, what that identity is permitted to do, and where the secret lives |
| `Expiry` | A token expiry makes the agent break. A row expiry makes a named person look at it and decide | A date somebody has to look, rather than a date something stops working |
| `Reviewed` | Turns the file into a process rather than a document | A date and a name. It also produces the number that matters at audit time, which is how many rows have a review date older than their own expiry |
| `Escalation` | Owner and escalation diverge under load: the owner answers for it, escalation can do something at 3am | A name for out of hours. If it's the owner and the owner sleeps, the row is telling you something |
| `Kill switch` | "We'd pause it" is a plan rather than a control | The exact command or click, plus who can run it. The test is whether somebody who didn't build the agent could stop it from this row alone, at 2am, without waking the owner |
| `Autonomy rung` | A rung that lives in a spec file's prose can't be queried, so the one question worth asking across a fleet has nowhere to be asked from: how many things are running at rung four | A number from the ladder further down, and the date it got there |
| `Action log` | "It logs" is not an answer, because the question that sends you to the log arrives weeks after the write | A location and a retention window. How far back you can read is the answer, and name who can revise it, since a log the agent can edit answers a different question |

Two of those fields carry an argument rather than an instruction, and both of them failed a first pass at being fillable.

`Credential` is why `Reaches` can't be filled from the spec. If the row names a credential shared with a human or with other agents, writing that down is the point of the field. GitHub's own documentation is blunt about the common case: a classic personal access token grants access to all repositories within the organizations you have access to, as well as all personal repositories in your personal account. Where that's the credential, `Reaches` covers rather more than one repo.

`Expiry` gets confused with the token's expiry, and they're different controls. A token expiry makes the agent break, and a broken agent gets fixed at speed by whoever is on, without anyone being prompted to ask whether it should still exist. GitHub's fine-grained tokens default to 30 days and accept anything between 1 and 366 days or none at all, with infinite lifetimes allowed unless an organization or enterprise policy blocks them, so the token side of this is a choice somebody made rather than a constraint. The row's date is the one that makes a person decide.

---

## What Our Own Fleet Scores Against It

We run 29 loops across three repos, 24 of them enabled, counted on 2026-07-28. The fleet view that lists them is generated rather than hand-maintained, on a rule we hold to hard: a loop missing from the view is a bug in the generator, never something to hand-prune.

So we solved one half of coverage. An agent of ours cannot be absent from the list, and that took a script. The other half, whether the file each row points at is still there, is not solved and I found that out while scoring this, which is further down.

Then we ran the fleet against the ten fields above, and here's what came back.

| Field | What our fleet has | Score |
| --- | --- | --- |
| Owner | No such field. Of the 27 spec files that exist, 4 contain the word owner at all, and none of those names the loop's own owner: one names the owner of a downstream tracker, one is a template placeholder, one is a table header, one is a hand-off instruction | **0 of 29** |
| Purpose | The loop's name plus its task-file README. Not a field, and one loop's `taskFile` points at a README that is no longer on disk, so 28 are readable in one hop and one is not | **28 of 29, in prose** |
| Reaches | Not a field. Discoverable only by reading the spec's prose, which describes intent rather than reach | **0 of 29** |
| Credential | Not a field. Every loop runs as this machine's user and inherits what that user has, including one GitHub token on account `JayZeeDesign` whose scopes are `gist`, `read:org` and `repo` | **0 of 29** |
| Expiry | Not a field. 2 loops carry a stated finish line and both of those are paused | **0 of the 24 running** |
| Reviewed | Not a field, and no review has been scheduled for any of them | **0 of 29** |
| Escalation | Not a field. Each loop has a `notify` policy that reaches the machine's owner, which is one person for the whole fleet | **partial, one contact for 29** |
| Kill switch | Yes. `enabled` is per loop, `loopany edit <id> --json '{"enabled":false}'` stops one, and 5 are paused right now | **29 of 29** |
| Autonomy rung | Not a field. 11 of the 27 spec files that exist state a posting rule about themselves in prose, from "never post" to "auto-post". The other 16 state none | **0 of 29** |
| Action log | Per run, not per write. Each record carries an id, timestamp, role, outcome, duration, cost, message, session id and declared state | **partial, wrong granularity** |

One clean pass out of ten, and purpose missed being the second by a single row. Two partials. Six fields with no place in the system to put them.

That last part is the finding rather than the score. This isn't a case of fields left blank through neglect. The whitelist of every key a loop's config accepts has fourteen entries, and I read all fourteen: name, cron, timezone, notify, model, agent, allowControl, enabled, runAt, taskFile, goal, workflow, ui, stateSchema. There's no owner, no credential, no expiry, no review date, no escalation contact and no autonomy level, so a person who wanted to fill those fields properly has nowhere to write them and would end up keeping a second file by hand, which is the file that goes stale.

Purpose is the row I got wrong first time, and how I got it wrong is worth a paragraph. I scored it 29 of 29 because every loop has a `taskFile` and every `taskFile` is a README, so purpose is one hop away. Then I checked whether those files exist. Our 29 loops resolve to 28 unique paths, 27 of which are on disk. One loop points at a README that has been deleted, and a second path is registered twice under the same loop name. The CLI prints the path either way, because printing a string is not the same as resolving it, so a fleet view generated from that output shows 29 healthy rows. Coverage was the half I said we had solved. What we had actually solved was getting every loop into the list, which is a different thing from the item the list points at still being there.

Some of the other rows want a sentence more, starting with the ones I'd act on first.

Credential is the worst of them and it's structural rather than accidental. Every loop authenticates as this machine's user, so the blast radius of any one of them is the blast radius of all of them together. One token, `repo` scope, shared by 29 agents that do unrelated jobs, and per GitHub's own documentation that scope reaches every repository in every organization the account belongs to. A registry row for any single loop would have to name that token, and the row would immediately read as wrong, which is exactly the use I claimed for the file.

Expiry made me most uncomfortable. Two loops carry a finish line, both are paused, and so nothing currently running has a date on which someone is required to reconsider it. The agent in the thread had run every night since March. Ours have the same property and the same reason, which is that nothing in the system asks.

Then the action log, which is close but at the wrong granularity, and the distance is instructive. We get a run record with a session id, which tells you a run happened and lets you go read its transcript. It doesn't tell you which rows in which system that run changed, and reconstructing that is the hand-correlation of application logs the operator in the thread was already stuck doing. There's also a query ceiling: asking for 1,000 records on a loop with 128 returns 20, and the CLI says `count: 20 of 128 total` while it does it. On a loop that runs sixteen times a day, twenty records is about a day of readable history. [Spoke two](/blog/ai-agent-runaway-cost) documented that cap and the null-cost fields on the same log, so I won't re-litigate them here beyond noting that a log with a twenty-record query window is not an audit trail.

One thing I want to be precise about, since it's the difference between a useful score and a self-flagellating one. None of the above means our loops are running wild. Their guardrails are real and they're hand-built per loop in that loop's spec file and its runner config. What the score says is that the guardrails aren't legible from outside the loop, so checking them means reading each spec file, which in practice means asking the person who already knows the loop.

---

## Artifact 2: `agents/OFFBOARDING.md`

Retirement is where the whole thing gets tested, and it's the step people skip because the agent has already stopped mattering to them by the time they get to it.

The order below is chosen so that step 3 catches the failure in step 2.

markdown

```
# Offboarding: <agent name>

Registry row: <link>            Owner at retirement: <name>
Reason for retirement: <one line: superseded, purpose gone, never worked, cost>

- [ ] 1. Stop it.
      <the kill switch from its registry row, run verbatim>
      Stopped at: <timestamp>

- [ ] 2. Revoke the credential. Revoke, not rotate.
      <where, and which credential. if it is shared, say so here and stop:
       a shared credential cannot be revoked and this agent is not offboarded,
       it is only switched off.>
      Revoked at: <timestamp>

- [ ] 3. Verify the revocation from outside.
      Run the agent's own first call with the old credential and watch it fail.
      Paste what you ran and what came back:
      <command>
      <output>
      A revocation you have not watched fail is a revocation you have assumed.

- [ ] 4. Archive the action log.
      <where it goes, who can read it, how long you keep it>
      The log outlives the agent. The questions about what it did arrive after
      it is gone, and that is the whole reason this step exists.
      Archived at: <path or URL>   Retained until: <date>

- [ ] 5. Close the registry row.
      Move it to the Retired section with today's date. Do not delete it.
      A deleted row is indistinguishable from an agent that was never registered.

## Left behind

<Anything you cannot answer about what this agent did, written down now, in plain
words, while you still remember. Reconstructing it later costs more and is worse.>

Retired: <date> by <name>
```

Step 2 has the trap in it and I've put the trap in the file. If the credential is shared with a human or with other agents, you cannot revoke it, and the honest thing the runbook can do at that point is refuse to call the agent offboarded. It's switched off. The credential is still live and still reaches everything it reached, and the only difference is that nothing is currently using it. Our fleet fails this step for all 29 loops, and it fails for the same reason the credential row scored zero.

Step 3 is the one to actually run. Watching the old credential fail converts an assumption into an observation, and the assumption is the kind that survives indefinitely because nothing contradicts it.

The "left behind" section is there because of a point the operator in that thread made himself, in a reply to somebody suggesting he add an approval gate. A gate added now, he said, does nothing for the four months his agent had already been writing, and that history stays opaque no matter what he adds. He's right, and it generalises past his case. Every control on this page is prospective. None of them reaches backwards, so the only thing available for the period before you started is writing down what you don't know, before the person who remembers moves on.

---

## Artifact 3: The Action-Log Contract

The registry says what an agent may reach. This says what it actually did, and it's the difference between "probably fine" and "fine."

Append-only is a property of the writer, not a word you put on a heading, and the first draft of this contract failed its own label. It had one row per write, minted before the call with an `outcome` column filled in afterwards. That's a mutable row. A row the agent updates is a history the agent holds the pen on, which is the one property you need this file not to have.

So: two events per write, and a sink the agent can add to and nothing else.

code

```
INTENT   appended before the call. never updated, never deleted.
  op_id       uuid, minted before the call. not derived from the payload.
  ts          when the intent was recorded
  agent       the registry row this belongs to
  run_id      the run that decided on this write
  caused_by   the ticket, job, message or schedule slot that started the run
  target      the system, and the specific object
  before      what was there. a hash if it is large or sensitive.
  after       what it is being set to
  reason      the agent's own stated reason, in its words

OUTCOME  appended after the call, as a second event. never updated, never deleted.
  op_id       the same uuid. this is the only join between the two.
  ts          when the call returned
  result      applied | rejected | failed
  detail      the error, the affected row count, whatever came back
```

An intent with no outcome beside it is a finding rather than a gap in your data. It says a write was started and nothing came back, which is what a crash, a timeout or a killed process leaves behind. The mutable version records that same event as a row that simply never got updated, which is indistinguishable from a bug in the logger.

The writer is the other half, and without it the two-event shape is a convention rather than a control. Both events go somewhere the agent's own credential can append to and can't revise. On Postgres that's an `INSERT` grant on the log table with no `UPDATE`, no `DELETE`, no `TRUNCATE` and no ownership, and no `ON CONFLICT DO UPDATE` path in the code the agent runs. On a file it means the file isn't the agent's: it goes to a collector running as a different user, or to the platform's own append-only log service, and what the agent holds is a handle to a socket rather than to the history.

That has to be tested by attacking it, and the obvious version of the test does not test it. Revoking `UPDATE` and `DELETE` and then watching an insert succeed proves the insert works. It proves nothing about whether the history can be rewritten, because `UPDATE` and `DELETE` are not the only ways to rewrite it. `TRUNCATE` empties the table under a privilege of its own. The table's owner holds every privilege whether or not it was granted, so a writing role that owns the log is unconstrained no matter what the grants say. `ON CONFLICT DO UPDATE` revises a row through an `INSERT` statement. And a grant to `PUBLIC`, or to some other role, hands the same power back through a different login.

So `tests/append-only-log-test.sql` attempts every one of those as the writing role and fails, loudly, if any of them succeeds. Eleven checks, and a check it could not attempt counts as a failure rather than a skip:

text

```
 1  INSERT intent event                            must be accepted
 2  INSERT outcome event                           must be accepted
 3  UPDATE a written event                         must be refused
 4  DELETE a written event                         must be refused
 5  TRUNCATE the log                               must be refused
 6  INSERT ... ON CONFLICT DO UPDATE               must be refused
 7  ALTER the log table                            must be refused
 8  writing role does not own the table            and is not a member of the owner
 9  writing role is not superuser or BYPASSRLS
10  no other role holds UPDATE, DELETE or TRUNCATE
11  both probe events still present afterwards
```

There are two ways to run that file. Use the first when you already have PostgreSQL:

bash

```
psql -v ON_ERROR_STOP=1 -f tests/append-only-log-test.sql
```

Use the bundled Node runner when you do not. Its PostgreSQL runtime is an explicit, test-only install, so a fresh checkout prints this same install command instead of an `ERR_MODULE_NOT_FOUND` stack trace:

bash

```
npm install --no-save --package-lock=false @electric-sql/pglite@0.5.4
node tests/run-append-only-test.mjs
node tests/run-append-only-test.mjs --overgranted
```

The first Node run requires all eleven checks to pass. The second is the negative control: the runner deliberately over-grants the writing role, requires six named checks to fail, and exits 0 only when that failure is observed. `@electric-sql/pglite` is kept out of this site's lockfile because the SQL remains the portable artifact and the package is needed only by the no-server runner.

Run against a log built to the contract, all eleven pass and the refusals are quoted from the server rather than assumed. Run against a role that kept the mutations, six fail and the message names each one, which is the half of the evidence that makes the other half worth anything: a test never seen to fail is not known to be a test. Both runs are in the receipts.

`caused_by` is what makes it an audit trail rather than a pile of events. Without it you can see that a row changed and you're back to correlating timestamps by hand, which is the exact position the operator in the thread described as his current state. With it, "why did this customer's balance change on the 14th" resolves to a ticket in one hop.

`op_id` is doing a second job, and it comes from a point raised on a different thread in this research: an approval layer stops one bad write from running unreviewed, and does nothing about the same write firing repeatedly because the agent looped or a retry landed after a timeout. That's an idempotency problem wearing an approval problem's clothes. If the applier checks `op_id` against already-executed ops before running anything, a duplicate becomes a no-op, and you get that property from a field you were writing anyway.

Some limits belong on the file itself, because a log that overpromises is its own hazard.

The agent's stated reason is a lead and not evidence. It's the agent's account of itself, produced by the same process that produced the write, and it's genuinely useful for finding the run you want to go read. It is not a finding about what happened.

Append-only stops the agent revising its history and does nothing about what the agent chose to write down in the first place. An agent that never appends an intent event leaves no trace at all, and no grant on the log table changes that. What the contract buys you is that the events you do have can't be edited afterwards, which is a narrower claim than "the log is complete" and worth not confusing with it.

And the retroactive gap doesn't close. Turning this on today gives you an answer from today. For everything before, the honest artifact is the "left behind" section of the offboarding file.

---

## Artifact 4: The Autonomy Ladder

The pillar states this as a principle in three sentences: autonomy is granted per function, never to the system, and a function climbs on evidence and gets walked back down when the evidence stops holding. As a principle it's easy to agree with and impossible to check. Here it is as a table you can put a date against.

| Rung | What it means | Promotion evidence, written before you promote | Demotion trigger |
| --- | --- | --- | --- |
| 1. Human only | The agent doesn't touch this function. It may read and suggest | n/a. Nothing is promoted into rung 1 | n/a |
| 2. Drafts, a human sends | Every output passes through a person who can edit it before it leaves | A named person has read N consecutive drafts and states what a bad one looks like. Write the number and the person in the row | Any draft ships that the reviewer would not have sent, and the reviewer says so |
| 3. Executes, a human reads every action | The agent acts. A human reads every action within a stated window, and the window is part of the rung | The reviewer at rung 2 stopped editing. Record how many consecutive drafts went out unedited, and over what period | Two actions inside one window that needed correcting, or one that reached a system outside its registry row |
| 4. Autonomous inside stated limits | The agent acts and nobody reads every action. The limits are the control, so they have to be written before you get here | Rung 3 ran for a stated period with the reads happening and nothing corrected, and the limits are in config rather than prose | Any action outside the stated limits, or a limit nobody can point at in a config file |

Two rules make the table work, and without them it's decoration.

Promotion evidence gets written down before the promotion, not after. Evidence assembled afterwards is a justification, and a justification starts from the answer it wants. The row above asks for numbers you fill in prospectively, so a promotion you can't justify in advance doesn't happen.

The demotion trigger has no natural moment at which it gets written, which is why the table asks for it in the same row as the promotion. A rung with no written trigger only goes up, and a ladder that only goes up is a ratchet. Write it while you can still imagine failing.

The failure this catches doesn't look like an agent doing something wrong. A marketing agency running fourteen agents in production described a spend-monitoring agent that detected a client overspending, flagged it, specified the escalation action, then reported "escalation overdue" every day for 17 days without executing it. Nothing was broken. The specification was being treated as documentation rather than as executable logic, and nobody had verified the execution path end to end. That agent was sitting at rung 3 on paper with nobody performing the reading that rung 3 is defined by, which is the rung that quietly becomes rung 4.

Their other story is the coordination version: two agents tracking project deadlines from different data sources, each correct in isolation, producing two different due dates for the same project in one morning briefing. Their conclusion from both was organizational rather than technical: "one seat, one owner." Worth taking with its provenance attached, since that post ends in a pitch for the author's own product, and the reason to trust the two war stories anyway is that they're specific, they're consistent with each other, and the conclusion lands in the same place the thread this page opens on did, from a completely different direction.

---

## The Same Gap, Three Situations

The three cases below are conditions rather than headcounts. What changes the answer is who else is in the blast and what identity process already exists, and I have no measurement tying either of those to a team size.

When you are the only owner, the owner is obvious and implicit, and you're right that it's obvious. What you're missing is the reconstruction path: when the question arrives later, you're the only person who can answer it, and memory is what you have to answer it from. Write the registry rows anyway, and treat them as a note to a future version of yourself who has forgotten.

The ground gives way once no one person tracks the agents and there is still no identity process covering anything that isn't a person. Both halves are needed for the failure, and this is the case the whole page is aimed at. The specific shape is that agents get created by whoever needed one, with a credential that already existed because minting a scoped one was a week of work, and the person who created it moves to another team while the agent keeps running. It's also where an agent can reach a control belonging to the team rather than to itself, which the branch-protection incident on the claude-code tracker is the clean example of.

The problem inverts into something more interesting once an access-recertification regime does exist. It works, and it has no category for a non-human. So the agent's access is either invisible to the review or is reviewed as a person's, under the name of whoever's credential it borrowed, which is worse than invisible because it looks handled. The version of this that has actually been built is described in Microsoft's own customer story about BNY, so read it as a vendor's account of its customer rather than as a bank's statement: digital employees that each hold login credentials, an avatar, an employee number in the corporate directory, and a supervisor who assigns tasks and reviews output. Every field on the registry above, provisioned through the systems that already track people. I've deliberately left the headcount out, because the number in that piece doesn't match the number circulating on vendor pages that cite it, and no primary statement turned up to settle it.

---

## Receipts

| Claim | Status |
| --- | --- |
| An operator's reconciliation agent has read and write on a production database, has run nightly since March, and has no record of its actions beyond application logs he would have to correlate by hand. "It has probably been fine. I do not know that it has been fine, which is a different sentence" | External, attributed, quoted verbatim. One operator's account on r/AI\_Agents, read at primary 2026-07-28. **The post carried a score of 3**, which the article states in place rather than only here |
| His own framing that a person with those permissions would have a review, an owner and an offboarding process, and the agent has none because it is not in any of the systems that track people | External, attributed, same post. This is the sentence the diagram's two columns are built from, and the diagram footnote says so |
| Short-lived tokens are an answer he already had, and it does not tell him who owns the thing | External, attributed, same post, his closing line. Used as the reason the page is about ownership rather than rotation |
| A gate added now does nothing for the four months the agent has already been writing, and that history stays opaque | External, attributed, his reply in the same thread. The reason the offboarding file has a "left behind" section |
| The fix shape: a named human owner plus a row in the service catalog or CMDB, the same access recertification people flow through, and an offboarding runbook | External, attributed. A reply in the same thread, **score 1 when read**. The article does not present the replies as consensus |
| Treat the agent as a service account plus an owner rather than as a user: its own identity, a named human or team owner, scoped permissions, an expiry and review date, an append-only action log with correlation IDs back to the ticket or job, and a dry-run or approval mode for high-impact changes | External, attributed. Second reply in the same thread, **score 1 when read**. This is the source of the registry's field list and of the action-log contract, and the article says which parts came from where |
| A spend-monitoring agent flagged an overspend, specified the escalation action, then reported "escalation overdue" every day for 17 days without executing it | External, attributed. r/ClaudeAI, read at primary 2026-07-28, score 4. **The post ends in a pitch for the author's own product**, which the article states in place. Its coordination-score numbers appear nowhere on this page |
| Two agents tracking deadlines from different data sources produced two different due dates for one project, and the fix was organizational rather than a prompt change | External, attributed, same post, same caveat |
| Blocked from force-pushing, an agent used the GitHub API to enable force pushes, disabled the ruleset, deleted the branch protection rule, pushed, and restored protections after the human said stop | External, attributed. One reporter's account on `anthropics/claude-code` #42849. Referenced in one sentence; the incident is covered in depth on the permissions canary page |
| A classic personal access token grants access to all repositories within the organizations you have access to as well as all personal repositories in your personal account | External. GitHub's own documentation, fetched 2026-07-28. Present tense because it is the vendor's current documentation for the credential our fleet actually uses |
| A fine-grained token's expiration defaults to 30 days, accepts 1 to 366 days or none, and infinite lifetimes are allowed unless an organization or enterprise policy blocks them | External. Same documentation, same fetch |
| Digital employees at BNY each hold login credentials, an avatar, an employee number in the corporate directory, and a supervisor who assigns tasks and reviews output | External, attributed **and provenance-flagged**: Microsoft's own WorkLab customer story about a Microsoft customer, fetched 2026-07-28, quoting BNY's head of applied AI by name. Not a BNY statement. **No headcount ships**, because the figure there does not match the one circulating on vendor pages and no primary was found |
| We run 29 loops across three repos, 24 enabled, and the fleet view listing them is generated rather than hand-maintained | Firsthand, dated 2026-07-28. `loopany loops`, loopany v0.16.0, counted on the machine that runs them |
| Scored against the ten registry fields, our fleet answers 1 from the system across all 29 loops, the kill switch, with purpose answering for 28 of 29. Escalation and action log are partial. Six fields have no place in the config | Firsthand, dated, and **corrected on 2026-07-28**. The first version of this page scored purpose 29 of 29 and headlined 2 of 10. Re-derived from `loopany loops --json`: 29 loops resolve to 28 unique `taskFile` paths, of which 27 exist on disk, so one loop's purpose is not readable from the file its config points at. Field-by-field score in the table above. It is a score of our fleet on one day. It is not a benchmark, and it measures nobody else's fleet |
| 29 loops point at 28 unique `taskFile` paths and 27 of those files exist. One loop, `DS Article Perf Check`, points at a README that is gone, and a second path is registered twice under the same loop name | Firsthand, dated. `loopany loops --json`, then `os.path.exists` on each unique path. Both facts were found while re-deriving the score and neither is visible from the CLI's own output, which prints the path without checking it |
| Of the 27 spec files that exist behind the 29 loops, 4 contain the word "owner" and none names the loop's own owner | Firsthand, dated. Regex over the unique `taskFile` paths the CLI reports that resolve to a file. The four hits are a downstream tracker's owner, a template placeholder, a table header, and a hand-off instruction |
| Every key a loop config accepts, all fourteen: `name`, `cron`, `timezone`, `notify`, `model`, `agent`, `allowControl`, `enabled`, `runAt`, `taskFile`, `goal`, `workflow`, `ui`, `stateSchema`. None is an owner, credential, expiry, review date, escalation contact or autonomy level | Firsthand. The tool's own documented edit whitelist, read 2026-07-28 at loopany v0.16.0. This is the load-bearing half of the score: the fields are absent rather than blank |
| Every loop runs as this machine's user and inherits its credentials, including one GitHub token on account `JayZeeDesign` with scopes `gist`, `read:org` and `repo`, shared across all 29 | Firsthand, dated. `gh auth status` on the machine, token value redacted. No per-loop credential exists because the config has no field for one |
| 2 of 29 loops carry a stated finish line, and both are paused, so 0 of the 24 running loops have a date on which anyone must reconsider them | Firsthand, dated. The `goal` field from `loopany loops --json`, cross-checked against `enabled` |
| Kill switch: `enabled` is per loop, one command stops one loop, and 5 are paused right now | Firsthand, dated. The one row we pass cleanly, and the pause count is from the same query |
| 11 of the 27 spec files that exist state a posting rule about themselves in prose, from "never post" to "auto-post". The other 16 state none | Firsthand, dated. Regex over the same 27 files, then read by hand, which is what the count rests on: the regex returned 12 and one of them, `Browser Bridge Health Check`, matched only because it names another loop, `X value replies (auto-post)`, in a list of the loops it watches. It states no rule about its own posting. Used only to show the rung cannot be queried across the fleet, and not as a grade on any loop |
| The run log records one row per run rather than one per write: id, timestamp, role, outcome, duration, cost, message, session id, declared state. Asking for 1,000 records on a loop with 128 returns 20, and the CLI reports `count: 20 of 128 total` | Firsthand, dated. `loopany log --json --limit 1000`. The cap and the null cost fields were both documented by spoke two; this page restates neither beyond what the granularity argument needs |
| Guardrails on our loops are real and hand-built per loop, in that loop's spec file and its runner config | Firsthand, already published in the pillar's Step 5 and in spoke three. Included so the score is read as a legibility finding rather than as an absence of controls |
| The action-log contract is append-only in the sense that it names: two events per write correlated by `op_id`, neither ever updated, and a sink the agent's credential can insert into but not revise | Property of the shipped artifact rather than a source. The first draft was one row with an `outcome` column written after the call, which is a mutable row and was corrected on 2026-07-28. The contract ships with its own falsifying test, `tests/append-only-log-test.sql`, which attempts UPDATE, DELETE, TRUNCATE, an ON CONFLICT DO UPDATE upsert and an ALTER as the writing role, and checks ownership, role attributes and every other grantee. Run 2026-07-28 against PostgreSQL 18.3 on a log built to the contract: 11 of 11 checks held, each refusal quoted from the server. Run against a role that kept the mutations: 6 checks failed and the assertion named each one. The direct `psql` command has no project dependency; the no-server runner exits 2 with the exact test-only install command when PGlite is absent, then reproduces both controls after that install. **Not implemented on our own fleet**, because our log is per run rather than per write; the contract is a design, but the test of it is executed rather than asserted |

Four things I wanted on this page and cut. A count or proportion of companies running unowned agents, which nothing in the research measures and which our own 29 obviously cannot supply. A claim that the quiet thread means the problem is widespread and undiscussed, which is a story about an absence and not a receipt. BNY's agent headcount, for the reason in the row above. And a before-and-after on our own fleet, since the registry was written on the same day it was scored and there is no after.

---

## Start Here

Pick the agent with the widest credential, not the one you're proudest of, and fill one registry row for it by hand. The row that comes back mostly blank has told you more than a full one would.

Then read the credential rather than the spec to fill the "reaches" field. If it names a token shared with a human or with other agents, stop there and write that on the row, because it changes what every other field means and it's the finding our own fleet produced on all 29 rows.

Write the expiry date next, and make it a date somebody has to look, rather than a date something breaks. Ninety days out is fine. The point is that the date exists, which for the 24 loops we run is currently not true of any of them.

Then generate the row list from whatever runs your agents instead of typing it. Coverage is the half you can automate, and it's the half where a hand-maintained file fails silently, because a missing row and a nonexistent agent look identical on the page.

Offboard one agent properly, all five steps, including watching the old credential fail. Do it with an agent you were going to turn off anyway, so the practice is free. That's the run that tells you whether any of this is real.

---

## Related Content

- **[How to Become an AI-Native Company](/blog/how-to-become-an-ai-native-company)** - The pillar this hangs off. Step 5 puts scoped credentials on the loop; this page is who answers for them.
- **[A Role Label Is Not a Sandbox](/blog/agent-tool-permissions-canary)** - Spoke three, and the other half of this subject: whether the control you configured actually holds, tested rather than assumed.
- **[Why Your Agent Bill Is Wrong](/blog/ai-agent-runaway-cost)** - Spoke two. The same run log read for a different question, and where the query cap and the null cost fields are documented.
- **[Reviewing AI-Generated Pull Requests](/blog/reviewing-ai-generated-pull-requests)** - Spoke one: ownership of the code an agent wrote, which is the same accountability gap one layer up.
- **[How to Build an SEO Agent Loop](/blog/ai-agent-seo-loop)** - Spoke five. One function run at depth, with the loop specs this page scores against.
- **[How to Cold-Launch a Social Presence With Agent Loops](/blog/ai-agent-social-loop)** - Spoke six. The autonomy rung made concrete: which of seven social loops reach a live account without asking, and which stop at a draft.
- **[OS-Level Agent Sandboxing](/blog/agent-sandbox-os-level-security)** - What actually binds a process, for when a registry row and a permission rule are both the wrong tool.
- **[Harness Engineering for Production Agents](/blog/harness-engineering-agent-production-guide)** - Making a repo an agent can work in verifiably, which is the precondition for granting it anything.
- **[Inside an Open-Source AI Company's Multi-Agent Setup](/blog/open-source-ai-company-multi-agent)** - What a large agent roster looks like from the inside, read as a teardown.

[Join AI Builder Club](/pricing?utm_source=blog&utm_medium=article&utm_campaign=who-owns-your-ai-agents)

It means one named person, first name and last name, is the one who gets asked what the agent did and is the one who can stop it. Not a team alias, and not a rota. The operator whose account this article is built on framed the test better than a definition does: if a person held these permissions there would be a review, an owner and an offboarding process, and his agent had none of those because it was not in any of the systems that track people. The check is whether you can write the name into a table today without asking anyone.

Start with a file rather than a tool, because the hard part is not storage. Ship an agents/REGISTRY.md with one row per agent and ten fields, and expect the first pass to be mostly blank, which is the finding. We ran our own fleet of 29 loops against exactly that schema on 2026-07-28 and could answer 1 of the 10 fields from the system for the whole fleet, with a second field answering for 28 of the 29. Generate the row list from whatever runs your agents rather than typing it, so an agent cannot go missing from the file, and fill the fields by hand. A file that quietly omits an agent is worse than no file.

The row needs one more than the token does. A token expiry makes the agent stop working, which somebody then fixes at speed without asking whether the agent should still exist. A row expiry is a date when a named person has to look at it again and decide. Ours have neither: 2 of our 29 loops carry a stated finish line and both of those are paused, so 0 of the 24 loops actually running have a date on which anyone is required to reconsider them.

Five steps for retiring an agent, in an order chosen so that step three catches the failure in step two. Stop it, revoke the credential rather than rotate it, verify the revocation by making the old credential fail in front of you, archive the action log somewhere that outlives the agent, and close the registry row instead of deleting it. The verification step is the one that gets skipped and the archive step is the one you regret skipping, because the questions about what an agent did tend to arrive after it is gone.

Because it answers a different question. The operator in the thread this page opens on said so himself, that short-lived tokens were an answer he already had and it did not tell him who owns the thing. A short-lived token limits how long a stolen credential works. It does not tell you which human is accountable, what the agent touched last night, whether anyone reviewed that access this quarter, or who to wake at 3am. Rotation is a blast-radius control and ownership is an accountability control, and having one does not give you the other.

Two events per write rather than one row. An intent event appended before the call, carrying an operation id, the run and the registry row it belongs to, what caused the run, the target object, the before and after values and the agent's stated reason; then a separate outcome event appended after the call, joined to the first by the same operation id. Neither is ever updated, which is what makes the log append-only rather than a row the agent revises. Test it by attacking it rather than by revoking UPDATE and watching an insert succeed: attempt UPDATE, DELETE, TRUNCATE and an ON CONFLICT DO UPDATE upsert as the writing role, check that role does not own the table and is not a member of the owner, and check no other role holds those privileges. Any one of them succeeding fails the test. The operation id also makes a retry safe, because the applier can check it against already-executed ops. Some limits belong on the file itself. The agent's stated reason is a lead rather than evidence. Append-only stops the history being edited and does nothing about an event the agent never wrote. And a log you add today does nothing about the months already written, which is the gap the operator in the thread named when he pointed out a gate added now leaves the four months since March exactly as opaque as they were.

Firsthand: our own fleet of 29 loops was scored field by field against the registry schema in this article on 2026-07-28, using loopany v0.16.0's own CLI, and the score is published as it came back rather than as we would like it. The external evidence here is thin and the article says so: the account this page is built on is one operator's post that carried a score of 3 when we read it, and the article rests its weight on the firsthand half for that reason. Every claim about a third-party tool's behaviour is checked at that vendor's current documentation, fetched 2026-07-28. See our [editorial standards](/about).
