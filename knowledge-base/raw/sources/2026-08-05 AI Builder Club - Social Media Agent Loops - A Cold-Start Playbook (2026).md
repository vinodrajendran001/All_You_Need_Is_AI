---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-ai-agent-social-loop
title: 'Social Media Agent Loops: A Cold-Start Playbook (2026)'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/ai-agent-social-loop
published: '2026-07-28'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Social Media Agent Loops: A Cold-Start Playbook (2026)

On 2026-07-28 two runs of the same loop posted to the same Reddit account at 16:31 and 16:33 Sydney time. Our rule for that account is a gap of at least 21 minutes, jittered, because two comments a minute apart from one account is what a bot looks like.

Both runs checked. The 16:33 run read the shared ledger at 16:32 and the other run's line was not there yet, because that run was in the middle of posting. Both runs believed they were post 4 of 5 for the day. Neither run skipped a check, and neither did anything wrong by its own spec.

Here is what the account's ledger looked like afterwards, which is the file both runs were reading:

| Time (Sydney) | Sub | Gap since previous |
| --- | --- | --- |
| 12:38 | r/ClaudeCode | first of the day |
| 13:10 | r/ClaudeCode | 32 min |
| 13:59 | r/codex | 49 min |
| 16:31 | r/ClaudeCode | 152 min |
| 16:33 | r/codex | 2 min |

The loop's own post-mortem, written into its spec that day, states the conclusion better than I can: the ledger tail cannot close a window narrower than one post's own latency, and the durable fix is at the workflow layer rather than the agent layer, because no amount of re-reading closes a two-minute race between two live agents.

![Two agent runs and one shared account ledger drawn as a timeline: on the left both runs read the ledger tail at 16:29 and 16:32, both see the last entry at 13:59 with a gap of 152 minutes, both conclude the account is clear, and both post, producing entries at 16:31 and 16:33 that sit two minutes apart and break the account's 21-minute rule; on the right the same two runs call a claim gate first, the first run acquires the slot with an atomic mkdir and posts, the second run finds the claim already held and exits without posting, and the ledger gains one entry instead of two](/images/blog/ai-native-shared-account-race-diagram.png "Two agent runs and one shared account ledger drawn as a timeline: on the left both runs read the ledger tail at 16:29 and 16:32, both see the last entry at 13:59 with a gap of 152 minutes, both conclude the account is clear, and both post, producing entries at 16:31 and 16:33 that sit two minutes apart and break the account's 21-minute rule; on the right the same two runs call a claim gate first, the first run acquires the slot with an atomic mkdir and posts, the second run finds the claim already held and exits without posting, and the ledger gains one entry instead of two")

What this page carries instead of a fix is the rule, written out: an account-level gate that takes the posting slot instead of reading for it, refuses when the ledger cannot establish a gap, and prints the answer a ledger read would have given so the size of the difference is visible on every run. Including the three clauses our own version got wrong, where it let a post through that should have been blocked.

It also ships what our social loops have actually produced, which is thinner than the loop count suggests, and the channel we looked at and decided not to work. This goes past the pillar's [two failures that look like success](/blog/how-to-become-an-ai-native-company), which names two of these outages in a paragraph each and does not tell you what to do about either.

This page does not argue that you should automate distribution. The pillar's own selection rule puts customer-facing and irreversible work last, and posting from a real account under a real name is both.

---

## Where the Search Intent Is, and It Is Not Here

Before any of it, the honest note about why this page is titled the way it is.

A 90-day Search Console pull on 2026-07-28 across every query this domain drew, 25,000 rows at `dataState:"final"`, says our audience does not arrive here looking for distribution advice. Queries containing `social` returned 6 rows, 1 click and 68 impressions. `twitter` returned 62 rows and zero clicks. `linkedin` returned 29 rows and zero clicks. `distribution`, `audience`, `engagement` and `cold start` returned nothing at all. The `reddit` rows exist, 188 of them, and took 2 clicks.

Worse, the `twitter` and `linkedin` rows are mostly not people. They are queries carrying operators like `-site:reddit.com -site:twitter.com`, which is a machine reading the web rather than a reader with a problem.

Where our authority actually sits, in the same pull: `loop engineering` at 670 rows and 1,270 clicks, `agent` at 6,671 rows, `graph engineering` as the single biggest query on the property. So this page is named for the loop, not for the channel, the same call the [SEO spoke](/blog/ai-agent-seo-loop) made when it found six rows, 19 impressions and zero clicks for anything containing `seo`, and labelled its own intent unvalidated on the strength of it.

The intent for this page is **unvalidated**, and that word is doing real work. No keyword tool was run against any of these queries and no row on this property demonstrates demand for them. What is demonstrated is the problem, on our own fleet, on dated evidence, which is a different claim.

---

## What Actually Runs

As of 2026-07-28 our fleet is 29 loops. Seven of them touch social, read live from the fleet rather than from the copy of the specs in this repo. That distinction cost real time and is worth stating once: this repo carries a `loopany/` directory that is an older clone of the fleet, and grepping it returns confident zeros that are honest and completely wrong. Every row below came from the CLI against the live fleet.

What matters here is the split rather than the count.

Three of them put text on an account with no human in the moment. The Reddit value-comment loop, which fires in half-hour slots across the working day and escalates probabilistically to land somewhere between three and five comments. The X reply poster, which drips queued replies out through the day. And the LinkedIn repurposer on its tweet branch, which queues straight to the AI Builder Club company page through Buffer.

That third one is a **mixed loop**, and the mixing is the part worth copying down. It picks a branch each run. On the video branch it produces a paste-ready draft for a personal profile and its spec says never queue that one, because the only connected channel is the company page and the personal account is published by hand. On the tweet branch it queues to that company page unattended. One loop, two destinations, and only reading the spec tells you which. Its live record has both: four posts queued to the company page across eleven runs since 2026-07-06, one of which was gone from Buffer hours after the run that queued it verified it, and one draft handed over on 2026-07-28 with nothing queued.

A fourth reaches a live account without posting anything itself, and this is the one I had wrong in an earlier draft of this page. The X reply surfacer writes a daily queue file and flags each row `auto` or `hold`. The `hold` rows wait for a human. The `auto` rows are consumed by the poster above and sent unattended, capped at three to five a day, and its spec says so in place. So its output does land on the account and it does carry attribution: across seven live queue files sit 53 items, 6 `posted` and 2 `misposted`, and every one of those eight carries the URL it came back with.

Three end at a draft a human sends. The daily X post drafter, whose spec says review then publish and never auto-post. The X engagement drafter, five comments and five quote tweets a day, all drafts. And the Superdesign answer-engine loop, which builds a post-today shortlist and hands it over. Its spec says the loop drafts and presents and never posts, that it does not auto-post, and that only text a human has verified goes out. That loop had an auto-post gate once and it was retired on 2026-07-17.

So the split is four to three, not three to four, and both halves of it were wrong at some point in this page's drafting. An earlier version counted the surfacer as draft-only, which hid one loop's output going out unattended. A later version counted the answer-engine loop as a direct poster and the LinkedIn loop as draft-only, which had the right total by coincidence and the wrong two loops in it. The lesson is the boring one: read the spec, do not read the name, and do not assume a loop with an approval gate in its history still has an auto path.

### What They Have Earned

The brief for this page asked whether these loops have produced measurable results. One has a number. The rest do not, and the reason differs per loop.

| Loop | Runs, live count 2026-07-28 | Measurable outcome |
| --- | --- | --- |
| Reddit value comments | 159 | Comment karma roughly 0 to 90, 2026-07-17 to 07-28 |
| X reply poster | 140 | 6 replies posted, all on 2026-07-21 and 07-22, plus 2 to the wrong account |
| X reply surfacer | 15 | 53 replies written across 7 daily queues; 6 posted and 2 misposted through the poster, each with its returned URL, 45 still pending |
| X engagement drafter | 10 | Drafts only. No published-post attribution exists |
| Daily X post drafter | 19 | Drafts only. Spec forbids posting |
| LinkedIn repurposer (mixed) | 11 | 4 posts queued to the company page, one of which vanished from Buffer before publishing. 1 personal-profile draft handed over |
| Superdesign answer engine | 30 | Drafts only since 2026-07-17. 0 of 3 on its own head-query citation test, after six tests |

The one real number is the karma, and its shape is the most useful thing on this page.

u/jzdesign started at roughly zero comment karma, confirmed by the account's owner on 2026-07-17. A live read of the account on 2026-07-28 returns 90 comment karma and 5 post karma. In between, 41 comments are logged in the account's own ledger.

Now the part that matters. The loop's two weekly retros record where that karma came from. Week ending 2026-07-22: plus 43, of which a single comment in r/LocalLLaMA scored 32, and the other 15 comments sat at 1 to 4. Week ending 2026-07-26: plus 42, of which a single comment in r/ClaudeCode scored 36, and the other 9 scored 0 to 2.

Two comments account for 68 of the 89 points. Everything else is ones.

That shape is the cold-start distribution, on our account, on those dates, and multiplying it out by posts per day would describe nothing that happened. The loop's own retro says so in its own words, that a full four comments a day across the general AI subs is plus-ones rather than progress. What it argues for is a hunting rule rather than a volume rule, and ours is written as a gate: before writing anything, say in a sentence why the thread's best existing answer is weak and what our concrete fix is. If both halves cannot be filled in, there is no post.

The three loops with no outcome column are honest blanks rather than zeros. A drafting loop's output is a file a human may or may not use, and nothing in our fleet links a published post back to the draft it came from. That gap is the reason a results loop was specified on 2026-07-26 and deliberately not built, to be run by hand for a week first.

---

## The Channel We Decided Not to Work

The most useful thing we learned about cold-starting a social presence is where not to spend the loop.

On 2026-07-23 we looked hard at cold-commenting on X to grow awareness of a public skills repo, and judged it weak. The reason is about the topic rather than about the tactic, and it is the part worth carrying.

The AI coding agents conversation on X is dominated by two groups: creators selling content, and builders promoting their own tools. It is not dominated by people asking answerable questions. So the intersection we needed, a genuine problem crossed with real traffic crossed with a clean fit to something we ship, was close to empty.

Both halves failed separately. The high-traffic posts were promotional threads, and a reply that offers a competing tool under one of those reads as a reply guy and costs credibility rather than earning it. The genuine-pain posts did exist, and they ran tiny, in the tens of views rather than the thousands, and several of the ones we opened ended with the poster pitching their own product anyway. A plug-free asker with an audience barely appeared.

What we chose instead was mostly our own demo posts, what we ship matched against a problem it solves, short, in a real voice, with the repo linked. Plus a few genuine-asker replies where one skill is the exact answer, engaging what the person actually tried rather than dropping a link.

Scope, because this reads like a rule when it should not. That is one team reading one topic on one date. It supports no claim about cold outreach in general, about other topics, or about whether the same call would hold a quarter later. The transferable part is the test, not the verdict: before pointing a loop at a channel, go and count how many posts in a week clear all three of genuine problem, real traffic, and clean fit. Ours came back close to zero, and a loop cannot find what does not exist.

The Reddit comparison is the reason the test is worth running. The same three-way filter, applied to r/ClaudeCode and r/codex, kept finding threads worth answering, and the account has 41 logged comments to show for it against a count of qualifying X posts that came back near zero. Nobody counted the qualifying threads per day on the Reddit side, so I cannot give you a hit rate, only the two outcomes. Those rooms are full of stuck people rather than people selling. The operator, the voice rules and the effort were held constant across both, and the two channels came back nowhere near each other.

---

## The Failure

Now the one that cost us a rule violation on a real account.

### A Read Cannot Close the Window It Opens

The account rule is simple and the enforcement was not. At least 21 minutes between any two posts, jittered, with a combined cap of 5 per calendar day, counting every source: the value-comment loop, the answer-engine loop, and any interactive session. One account, several posters, one file as the source of truth.

The workflow pre-checks it. Before firing a slot it reads the ledger, returns silently with no agent run at all if the day is at the cap or the last post was under 21 minutes ago, and hands the escalated run a snapshot. The spec is careful about that snapshot, and says in place that it is a hint taken at slot-fire time rather than a substitute, and that the run must tail the ledger again immediately before posting.

Both of those checks ran on 2026-07-28 and both passed, correctly, and two comments went out two minutes apart.

The reason is structural. Posting takes time. Discovery took minutes, and the browser call plus the ledger append ran somewhere between 8 and 30 seconds on a slow-bridge day. So between the moment a run reads the ledger and the moment its own line lands on disk, there is a window in which the ledger is wrong, and it is wrong in the friendly direction. A second run arriving inside that window reads a file that does not yet contain the post that is happening.

Re-reading later does not help, because the window moves with you. Reading twice halves nothing.

The other guard on that account worked perfectly, and the contrast is what the incident is for. Before posting, each run also checks whether our account has already commented on that specific thread. That check held: the two comments went to different threads in different subs, so the placement guard did its job. What failed was the timing guard, and it failed because timing is a property of the account across runs while placement is a property of one thread, and only one of those can be established by reading.

### An Unknown Minute Is Not a Small Gap

The second half of this is quieter and it is in the data rather than in the incident.

That ledger holds 41 post entries as of 2026-07-28. **18 of them carry a time that cannot be read**: `time?` where the minute was not captured at the time, or `~16:xx` and `10:1x` where it was backfilled approximately. Nobody was being sloppy. That is what a backfilled row looks like when an interactive session posts and logs it afterwards, and the ledger's own format section tells you to write it that way.

The live workflow's rule for those rows is stated in the spec: if a line's time is fuzzy the workflow cannot measure the gap and will not gate on it, so the call falls to the human. Read that again with the incident in mind. An unreadable minute currently produces the same behaviour as a comfortably wide gap. Unknown is being treated as safe, on 18 of the 41 rows in the file.

The tempting fix is to skip unreadable lines and use the newest one that parses. That is worse, because it is confidently wrong: the newest parsing line on 2026-07-28 at 16:33 was 13:59, and a guard built that way would have reported a 152-minute gap two minutes after a post.

There is a precise version of the rule that keeps most of the file usable. The ledger is append-only and chronological. So an unreadable entry that is **followed** by a readable one is bounded by it and can be scored around. Only an unreadable entry at the **end** of the day's run blocks, because only that one leaves the gap genuinely unknown. That distinction is what stops the refusal from swallowing nearly half the ledger, and it is a clause in the rule written out below rather than an assurance in a paragraph.

---

## The Gate, Written Out

No script is attached to this page. What we run parses our ledger's format and our account's conventions, so handing it over would hand you our plumbing rather than the thing worth having. The rule is six clauses. Four of the six are here because our own version got them wrong and returned a green light on a post that should have been blocked.

### Take the Slot, Do Not Read for It

`fs.mkdirSync` with `recursive: false` either creates the directory or throws `EEXIST`, and exactly one of two concurrent callers can win. Any primitive with that property will do. Claim, post, release. The window between reading and writing still exists, and now it sits inside the claim, where it belongs to one run.

Re-reading the ledger later does not help, because the window moves with you. Both of our runs on 2026-07-28 read a file whose newest line was 13:59, both computed a 152-minute gap, and both were correct about the file in front of them. Reading twice halves nothing.

If you test this, race real operating-system processes. A same-process version of the test passes even when the atomic claim is replaced with a read followed by a create, because nothing interleaves inside one process, so the suite goes green over the exact bug the gate exists to fix.

### The Claim and the Recorded Post Are One Operation

This one is enforced rather than recommended, because our first version recommended the unsafe form in its own output. Releasing the slot without writing the ledger line frees it against a ledger that has not moved, so the next run reads the same stale trailing entry and goes. That is the original race with an extra step in it. A release has to carry the post it is recording, and a run whose post genuinely failed has to say so in as many words, or the first failed post wedges the account.

Check the line you are about to append against the parser that will read it back. The next run reads straight past any line the ledger's own format does not match, while your own output reports that it appended.

### Chronology Has to Be Checked Across the Whole File

An ordering check scoped to one day waves through a ledger whose dates run backwards, and then reads the gap off a row that is a day older than the row above it. Ours did exactly that. Rows `2026-07-28 16:30` then `2026-07-27 12:00`, a claim at 16:33, and it reported a 1,713-minute gap with a post three minutes old sitting in the file.

The same reasoning runs the other way for the day boundary. The cap is a calendar-day rule and the account lives in Sydney, so compute the day in a real IANA zone rather than in UTC or in whatever the runner's clock says. A post at 23:58 and a claim at 00:03 are five minutes apart, and a guard that only looks at today sees an empty day and fires.

### Refusing an Unknown Minute, Precisely

If the newest entry for the day has no readable minute, refuse, with no fallback to drop into. Skipping the unreadable line and using the newest one that parses is worse, because it is confidently wrong: the newest parsing line on 2026-07-28 at 16:33 was 13:59, and a guard built that way reports a 152-minute gap two minutes after a post.

The refusal needs a precise scope, and the scope is what keeps the file usable. The ledger is append-only and chronological, so an unreadable entry that is followed by a readable one is bounded by it and can be scored around. Only an unreadable entry at the end blocks, because only that one leaves the gap genuinely unknown. Without that distinction the refusal swallows 18 of the 41 rows in our real ledger, and a guard that blocks legitimate posts gets switched off.

### A Claim Nobody Released Is Evidence

We shipped this wrong twice and both times in the same direction. A claim past its time-to-live looks like litter, and the tempting move is to delete it and carry on. But a claim nobody released records a run that took the slot and never came back, and the documented way that happens is posting first and dying before the write.

With a 60-minute minimum gap and a 30-minute TTL: holder A claims at 16:00, posts, and dies before recording it. Holder B arrives at 16:31, finds a claim past its TTL, deletes it, re-reads a ledger that has not moved since 12:00, and authorises a post 31 minutes after a possible unlogged one, printing a 271-minute gap while it does so. So the claim's own timestamp counts as a possible post, and takeover waits for the minimum gap since the claim was taken rather than merely for the TTL.

The day cap needs the same treatment, which is the second version of the same mistake. The cap is counted from the ledger, and the ledger is the one place a crashed run's post is guaranteed not to be. Four logged posts plus an abandoned claim taken today is five against a cap of five.

The opposite case matters as much. Once the minimum gap has elapsed, the stale claim has to be takeable, or every crash wedges the account permanently and the gate gets removed.

Displacing a stale claim has to be atomic in itself, and this is the clause that is easiest to get wrong because the free-slot path next to it is already correct. Inspecting a stale claim, deleting it, then creating your own is a check-then-act sequence spread over separate syscalls, and two contenders working from the same stale read can each delete and each create, including one deleting the other's fresh claim. Displace the exact object you inspected atomically, with a rename or a dedicated takeover claim, so only the process that actually moved the stale claim may replace it.

### Print What a Ledger Read Would Have Said

Beside every verdict, on every run. Replayed against the real ledger as it stood at 16:29 that afternoon, the second run's verdict is `HELD` while the tail-read of the newest parseable line, 13:59, says 152.0 minutes and would have said go. Hours later the same ledger returns `DAY_CAP` while the tail-read, now 16:33, says 215.8 minutes and would have said go again. Two different reasons to hold, and the tail-read is wrong both times. Dropping it would be cleaner. It would also remove the one place a reader can see how far apart the two readings are, and that gap is what makes the rule stick.

### The Verdict States, All of Them

The defect being fixed is a guard whose permissive state looks like its healthy state, so every state is named and every one of them is distinguishable in the output.

| Verdict | When |
| --- | --- |
| `CLAIMED` | Gap and cap both clear, and the slot was acquired |
| `TOO_SOON` | The newest readable post is closer than the minimum gap, or an abandoned claim was taken inside the minimum gap and may have posted without recording it |
| `DAY_CAP` | The calendar day in the given zone is already at the cap |
| `MALFORMED_USAGE` | Settings unusable, including an unrecognised timezone, a release that records no post, and a ledger line the parser cannot read back |
| `REFUSED` | The ledger cannot establish the gap: trailing unreadable minute, entries out of order across days or within one, or an entry in the future |
| `LEDGER_UNREADABLE` | The ledger is missing or is not a file, which is unknown history |
| `HELD` | Another holder has a live claim |

`LEDGER_UNREADABLE` is the one worth arguing about, and it is the reason the list runs this long. If the ledger path is wrong, or the file has not been created yet, the friendly answer is that there are no posts today. That answer is indistinguishable from the truth on a genuinely quiet day, and it is the answer a guard with a typo in its path gives every single time. So a missing file is its own state and it blocks. A file that exists and holds no entries is a real zero and does not.

### The Limits, Said Out Loud

An abandoned claim leaves an unknown rather than a zero, and the rule above resolves that unknown in the conservative direction on purpose. A claim taken at 16:00 by a run that never came back might mean a post at 16:00, or it might mean a run that crashed before it opened the browser. Nothing in the claim can tell you which, so it counts as a post against the gap and against the cap alike, and the cost of that is a real post you could have made and did not. The alternative costs a rule violation on a live account, and we picked which of those two we would rather have.

The gap and the cap are also only as good as the ledger every poster writes to. Anything that posts from that account without appending is invisible to all of this, and the gate cannot see it. That is a property of the account rather than of the code, and it is why the limits sit on the account instead of inside any one loop.

One deliberate difference from what we run in production. Ours escalates through a workflow pre-check that returns silently and never spawns an agent, which is cheaper. The rule as written above always runs and always prints, which is louder and easier to debug while you are installing it.

Two rounds of review found two real defects in the takeover path, and a third found the check-then-act race in it. All three sat in the part we were already being careful about, which is worth more than the fixes: the TTL and the minimum gap were each validated on their own terms, and the interaction between them belonged to neither check.

---

## The Other Three Ways a Posting Loop Goes Quiet

The race is the one with a rule you can implement. These three have no fix to hand you, and each of them cost us a day before we understood it.

The channel drops while every loop reports `ok`. Our browser-driven loops post by driving Chrome through an extension bridge. When Chrome closes or the extension's background worker suspends, the bridge goes and the loops refuse to half-post, which is correct. A correct skip records as `ok`. On 2026-07-23 every browser loop across our three repos posted nothing all day and the fleet view showed a normal day, until a human asked why nothing had gone out. The [permissions canary](/blog/agent-tool-permissions-canary) makes the general version of this argument, that a control you cannot observe is a control you cannot trust, and this is the distribution-shaped instance of it.

The follow-up is the honest part and it is more interesting than the outage. We built a check that runs before the posting window, and it has since produced a reading the record cannot classify. On 2026-07-27 it recorded, in its own run message, that a healthy probe now took 25 seconds cold against a 20-second timeout added four days earlier, and that left alone it would eventually report a false outage. On 2026-07-28 at 10:25 Sydney it reported the bridge down, on exactly that condition, a timeout rather than a connection error. Two hours later the same bridge posted four comments.

I cannot tell you from the record which of those it was, whether a false alarm or a real drop that a human fixed without logging it. That ambiguity is what there is to take away. A channel check that cannot distinguish its own probe timing out from the channel being down reports on itself rather than on the channel. If you build one, make the two outcomes different states with different messages, the same way the rule above separates `REFUSED` from `TOO_SOON`.

A posting command has a bug that only bites one shape of content. Our X reply poster cannot post multi-line text. The CLI types the reply, reads the composer back, string-compares, and aborts because the site's editor normalises blank lines differently from the raw string. It fails cleanly and posts nothing, 6 attempts for 6 clean failures across two days, and every single-paragraph attempt succeeded.

The trap is that this interacts with a house rule. Replies here are deliberately written as two or three short beats with blank lines between them, because a dense four-sentence paragraph reads as a bot on that platform. So every draft the surfacer produces is multi-line, and the whole drip is blocked rather than some of it. Upgrading did not fix it; the machine was already on the version the fix was supposed to be in, and a live retest on that version still failed.

The result, live-checked on 2026-07-28: the poster has 140 runs, the surfacer has written 53 replies across seven daily queues, 6 have posted, 2 went to the wrong account, and 45 are still pending. The last reply that actually landed was on 2026-07-21, confirmed by the loop reading its own account's timeline rather than by trusting its own logs.

A read API changes shape, and the failure that comes back looks like a permissions problem. Our X CLI's search command returns HTTP 404 as of 2026-07-28 on version 0.8.5. The cause is in the warning it prints first: it derives a required per-request header by scraping the site's own JavaScript bundle. That bundle changed, so the pattern it looks for no longer matches anything. Reads of a user's posts still work fine on the same binary in the same session, which is what makes it confusing. That is a statement about one version on one day, and the fix is somebody else's.

What puts these together is that they produce the same row in a dashboard. Our fleet view distinguishes a failure from a success. It does not distinguish either of them from a loop that ran perfectly and had nothing it was able to do.

---

## What Else Goes in the Spec

The rest of what our social loop specs carry has nothing to do with mechanics.

The limits belong to the account rather than to the loop. Two loops post from u/jzdesign and interactive sessions do too. So spacing and the daily cap are tracked in one file that every poster appends to, and the cap counts all three sources. A loop that only knows its own posts will hit the combined limit without ever seeing it. The same file also carries a priority rule for the days both loops want to post, which is a policy question rather than a technical one and belongs somewhere a human can change it.

There is a hard content firewall between the two loops on that account. The value-comment loop is pure value: zero product mentions, zero links, no exception. Product mentions are the other loop's job. This came up for real on 2026-07-27, when a genuinely good thread appeared that would have suited a soft product mention, and two independent reviewers on a blind brief both ruled it out of scope for that loop. It was routed to the other loop's approval queue instead and nothing was posted. A firewall you route around once is not a firewall, and the cheapest time to find that out is when the thread is good.

Discovery is scoped to subreddits rather than to search. Our spec says the site-wide search returns unrelated high-karma noise and is near-useless for discovery, so the loop browses specific subreddits sorted by hot and by new instead. Quoted phrases do not help either, because that search does not do exact-phrase matching, so a quoted query silently becomes a loose one. If a discovery step is coming back with nothing relevant, check whether it is searching a ranked-by-popularity index before you tune the prompt.

The voice rules are written as a gate the loop has to pass rather than as guidance. Ours is a read-back before posting that kills specific tells: no em-dashes, straight quotes only, no bullet lists inside a comment, no opener that thanks anyone for the question. It is written that way because it is checkable, and a rule like "sound human" is not.

And one thing to know before you point a loop at a channel: the review queue is the ceiling, not the drafting. Three of our seven social loops end at a draft, a fourth ends at a queue whose held rows wait for a human, 45 replies sit pending in that queue right now, and none of that is a drafting shortage. The general version of that ceiling, as four files you can put in a repo, is [reviewing AI-generated pull requests](/blog/reviewing-ai-generated-pull-requests).

---

## Receipts

| Claim | Status |
| --- | --- |
| Two comments posted 16:31 and 16:33 Sydney on 2026-07-28, two minutes apart, breaking a 21-minute rule | Firsthand, dated. Both lines are in the account's own ledger with their thread and comment ids, and the loop's spec carries its own post-mortem of the incident written that day |
| The 16:33 run read the ledger at 16:32 and the other run's line was not yet on disk | Firsthand, from that post-mortem. One incident, one account. Supports "a read cannot close this window," not a rate at which it happens |
| The day's gaps: 32, 49, 152 and 2 minutes | Firsthand. Derived from the five dated ledger lines for 2026-07-28 by subtraction, re-derivable from the file |
| At least 21 minutes jittered, combined cap of 5 per Sydney day, counting every poster | Firsthand. The account's own rules, set 2026-07-19 after two comments went out about a minute apart. **Ours, not a recommendation.** The rule carries both as settings and the article says to set your own |
| 41 post entries in the ledger, 18 of them with an unreadable or approximate minute | Firsthand. Counted by script over the live file on 2026-07-28. A property of one file on one date, not a rate at which ledgers rot |
| Comment karma roughly 0 to 90 between 2026-07-17 and 07-28, across 41 comments | Firsthand. The starting point is the loop spec's own description of the account, confirmed by its owner on 2026-07-17. The 90 is a live read of the account on 2026-07-28. **One account, eleven days.** Not a rate and not a forecast |
| Two comments scored 32 and 36, and the rest scored 0 to 4 | Firsthand, from the loop's two weekly retro entries which record the per-comment scores. The 68-of-89 arithmetic follows from those two figures and the two karma deltas |
| 29 loops on the fleet, 7 touching social, 4 reaching a live account without a human in the moment and 3 draft-only | Firsthand, live CLI query 2026-07-28. Same 29 the pillar and spokes 2, 4 and 5 carry, re-derived rather than inherited. The split was read from each loop's **live task file**, resolved through the CLI, never from this repo's stale `loopany/` mirror. **This is the second correction to this row.** The first added the surfacer to the posting side: its spec points its `auto` rows at the unattended poster, and the seven live queue files carry 6 `posted` and 2 `misposted` items with their returned URLs. The second swapped the other two: the Superdesign answer-engine loop's task file says "loop drafts + presents, never posts" and "The loop DRAFTS and PRESENTS; it does NOT auto-post", with its auto-post gate retired 2026-07-17, so it is draft-only. The LinkedIn repurposer's task file has two branches and branch B "auto-queued to the **ai-builder-club** company page via Buffer", so it reaches an account. The total was right by coincidence and two of the named loops were on the wrong side |
| The LinkedIn repurposer is a mixed loop: branch A drafts for a personal profile, branch B auto-queues to a company page | Firsthand, from its live task file's own branch table plus its step 4 ("Hand Jason the draft, do NOT queue") and step 4b (the Buffer `createPost` mutation and channel id). **One loop, two destinations.** This is why the split had to be read per branch rather than per loop |
| The LinkedIn loop: 11 runs, 4 posts queued to the company page, one vanished from Buffer, 1 personal draft | Firsthand, live 2026-07-28. Run count from the CLI; the queue and draft outcomes from the task file's own dated timeline, which records each queued post and the run that found the 07-13 one gone (`NOT_FOUND`, zero pending posts org-wide) hours after the run that queued it had verified it. **Corrects an earlier count of 3 on this page** |
| The X reply poster: 140 runs, 6 posted, 2 to the wrong account, 45 pending, last landed 2026-07-21 | Firsthand, live 2026-07-28. Run count from the CLI; the item counts from the seven queue files it consumes. The last-landed date was confirmed by the loop reading the account's own timeline, not from its own logs. **This corrects a rounder claim in the pillar**, which said the loop had recorded 119 runs and posted nothing; it posted 6 before the block took hold, and the pillar now carries the exact figures |
| The Superdesign answer-engine loop is 0 of 3 on head-query citations after six tests | Firsthand, dated. The loop's own run metrics and its 2026-07-27 evolve message |
| Cold-commenting on X judged weak ROI on 2026-07-23, and why | Firsthand, dated, and it is a **judgement rather than a measurement.** It records what we looked at, what we concluded and what we did instead. No count of qualifying posts was taken, so the article states the test to run rather than a number |
| Every browser loop across three repos posted nothing on 2026-07-23 because an extension unloaded, and the skips recorded as `ok` | Firsthand, dated. Already published as a receipt in the pillar and in the canary spoke. Carried here as a single paragraph with links across, not re-derived |
| The bridge check recorded on 2026-07-27 that it would eventually report a false outage, then reported down on 2026-07-28 at 10:25 while the bridge posted two hours later | Firsthand, dated, and **deliberately not resolved.** Both run messages exist and the posting times exist. Nothing in the record says whether a human fixed the bridge in between, and the article says so instead of picking the reading that makes a better story |
| The multi-line reply bug: 6 clean failures for 6 attempts, single-paragraph succeeded, not fixed by the current version | Firsthand, dated 2026-07-21 to 07-22, retested on the installed version. **Evidence about one CLI on one machine on those dates** |
| The X CLI's search returns 404 on version 0.8.5 while reads work, and the cause is a scraped header pattern that no longer matches | Firsthand, reproduced live on 2026-07-28 on that version. **Version-scoped.** It is evidence about the version run and nothing else, and it may be fixed by the time you read this |
| The site-wide Reddit search returns noise, and quoted phrases do not do exact matching | Firsthand as our loop's operating rule, recorded in its spec as the reason discovery is subreddit-scoped. Not verified against that platform's published documentation |
| 90-day Search Console pull showing no social or distribution intent on this property | Firsthand. Live API pull 2026-07-28, 2026-04-29 to 07-27, `dimensions:["query"]`, `dataState:"final"`, 25,000 rows. The `dataState` qualifier is part of the claim: a same-day `dataState:"all"` pull had already moved to 6 rows and 2 clicks on the social side, which is preliminary data arriving rather than a contradiction. **A property of one domain**, which is exactly why the slug sits in the agent-loop lane instead |
| An atomic claim admits exactly one of eight concurrent OS processes | Firsthand, by execution against our own implementation on 2026-07-28, eight real processes racing one slot. **A same-process version of that test stays green when the atomic claim is replaced with a read followed by a create**, which is why the page says to race real processes |
| A stale claim could be taken over inside the minimum gap and authorise a post 31 minutes after a possible unlogged one | Firsthand, found by a review on 2026-07-28 against our own implementation in three commands. **The article's earlier hand-attack claim of "none produced a claim it should not have" was false when it shipped**, and this row says so rather than quietly dropping the sentence. Attacking the fix produced a second defect of the same shape against the day cap. Both clauses are written out on the page |
| Displacing a stale claim by inspect, delete, create is itself a race | Firsthand, found by a review on 2026-07-29 against our own implementation: 32 processes against one stale claim, 5 of 10 trials produced more than one winner and the worst produced 5. A control against a free slot produced one winner per trial every time, which is why an ordinary race test walks past it. **The page states the requirement rather than a fix**: displace the exact claim you inspected in one atomic step |

What is missing here, and why. There is no **conversion number for any of it**, because nothing in our fleet links a published post back to a signup, a click or a draft, and inventing an attribution chain would be worse than the blank. There is no **before-and-after showing the guard catching the race in production**, because the gate was written after the race rather than before it, so what exists is a replay against the real ledger rather than a save, and a replay does not count as a catch. And there is no **recommended posting frequency**, which is the single most quotable thing a page like this could offer and the one we have no evidence for at all: our numbers are one account's house rules set by its owner after one incident, and dressing them as a safe threshold would be the worst sentence here.

---

## Start Here

Do the counting exercise before you build anything. Take the channel you were going to point a loop at, open it, and go through one week of posts and ask of each whether there is a genuine problem in it, whether it has traffic, and whether something specific you ship is the exact answer. Count the posts that clear all of that. Our count came back near zero, and pointing a loop at that would have produced volume rather than replies, which is what turned our own answer from X to Reddit. It took us an evening.

If the channel survives, gate the account before you gate the loop. The smallest useful version is a claim directory per account, created with a call that fails when the directory already exists, and a release that will not run without the ledger line it is recording. Your minimum gap, your cap, and the timezone the cap counts in are settings on that gate rather than constants in it.

Before you write any of it, take whatever posting history you already have and compute both numbers over it: the gap the newest parseable ledger line implies, and the gap the claim record implies. Where those two disagree on a day you actually posted, something has been deciding on the wrong one.

After that, the order that worked here: put the spacing and cap rules on the account rather than in each loop, make every poster append to one file, write the firewall between two loops on one account before you need it, and give your channel check two different failure states so a probe timing out cannot be reported as a channel going down.

The tooling is open source. [AI Builder Club Skills](https://github.com/AI-Builder-Club/skills?utm_source=blog&utm_medium=article&utm_campaign=ai-agent-social-loop&utm_content=start-here) ships `new-loop` for the shared file-based memory a loop reads and writes. There is no social skill in it, and the gate on this page is written out as a rule rather than shipped as code.

If you want the full build layer by layer, the [Loop Engineering course](/courses/loop-engineering) goes from prompting an agent yourself to a loop that wakes on schedule, ships behind quality gates, and reports back.

---

## Related Content

- **[How to Become an AI-Native Company](/blog/how-to-become-an-ai-native-company)** - The pillar this hangs off. Its migration path has no distribution step, and its two-failures section names two of the outages here in a paragraph each.
- **[How to Build an SEO Agent Loop](/blog/ai-agent-seo-loop)** - The closest sibling. Same fleet, the other half of the growth function, and the loop that had a real number attached to it.
- **[Reviewing AI-Generated Pull Requests](/blog/reviewing-ai-generated-pull-requests)** - Spoke one. The review-bandwidth ceiling underneath 45 pending replies, as four files you can put in a repo.
- **[Why Your Agent Bill Is Wrong](/blog/ai-agent-runaway-cost)** - Spoke two. What these loops cost, and how to tell whether the figure your runner shows you is a total or a floor.
- **[A Role Label Is Not a Sandbox](/blog/agent-tool-permissions-canary)** - Spoke three. The general form of the outage above: a control you cannot observe is a control you cannot trust.
- **[Your Agents Have Production Credentials and No Owner](/blog/who-owns-your-ai-agents)** - Spoke four. Which of your loops is allowed to post without asking, as a ladder with demotion triggers rather than a sentence in a spec.
- **[Loop Engineering: Stop Writing Prompts, Start Writing Verifiers](/blog/loop-engineering-guide-2026)** - The mechanics of one loop, and why the verifier is the bottleneck. The guard here is a verifier for an account rather than for an output.
- **[Self-Improving Agent Loops](/blog/self-improving-agent-loops)** - The evolve step. Every spec rule quoted here arrived through one after something went wrong.
- **[Agent Memory Systems](/blog/agent-memory-systems-guide)** - The current-state and append-only-history split. The account ledger here is the append-only half, and the incident is what happens when two writers share it.
- **[How to Evaluate AI Agents](/blog/how-to-evaluate-ai-agents)** - Why self-evaluation skews optimistic. A drafting loop scoring itself on drafts produced is the same failure one layer up.

[Join AI Builder Club](/pricing?utm_source=blog&utm_medium=article&utm_campaign=ai-agent-social-loop)

Because both of them read a shared ledger and a read cannot close the window it opens. On 2026-07-28 two runs of our Reddit value-comment loop both believed they were post 4 of 5 for the day. The run that posted at 16:33 Sydney ran its ledger tail at 16:32, and the other run's line was not on disk yet because that run was mid-post. Our account rule is a gap of at least 21 minutes, so two minutes apart is exactly the machine-shaped pattern the rule exists to prevent. Neither run skipped a check and neither did anything wrong by its own spec. The loop's own post-mortem states the conclusion plainly: the ledger tail cannot close a window narrower than one post's own latency, and the fix belongs at the workflow layer rather than the agent layer, because no amount of re-reading closes a two-minute race between two live agents.

One of ours has a number and the rest do not, and the number is small and lumpy. u/jzdesign went from roughly zero comment karma on 2026-07-17 to 90 on 2026-07-28, read live from the account that day, across 41 logged comments. Two of those comments carried it: one scored 32 and one scored 36, which is 68 of the 89 points gained, and the loop's own weekly retros record the rest sitting at 0 to 4. So the honest shape of a cold start on our evidence is a couple of hits sitting inside a lot of ones, which is nothing you can multiply out. On the same fleet, our X reply poster has 140 runs and last landed a reply on 2026-07-21, and our Superdesign answer-engine loop is 0 of 3 on its head-query citation test after six tests.

We judged it not worth it for ours on 2026-07-23 and picked something else. The reason is specific to the topic rather than to the tactic: the AI coding agents conversation on X is dominated by creators selling content and builders promoting their own tools, not by people asking answerable questions. The intersection of a genuine problem, real traffic, and a clean fit with something we ship was close to empty. The high-traffic posts were promo threads, and replying to one with a competing tool reads as a reply guy and costs credibility. Genuine-pain posts existed but ran tiny, in the tens of views rather than the thousands, and several of the ones we opened ended with the poster pitching their own product. What we chose instead was mostly our own demo posts, one skill against one problem, plus occasional replies where something we ship is the exact answer. That is one team's read of one topic on one date, not a general finding about cold outreach.

We do not know what is safe generally and nothing here measures it. What we run is at least 21 minutes between any two comments, jittered so it is never exactly 21 minutes, with a combined cap of 5 per calendar day across every source that touches the account. Those numbers are ours, set by the account's owner on 2026-07-19 after two comments went out about a minute apart during a manual catch-up. Nothing derived those numbers. They are a house rule, and the rule on this page carries both as settings rather than baking them in. The part that does transfer is the shape: the limits belong to the account and count every poster, because a shared account sees the sum, and a loop that only knows its own posts will hit the sum without ever seeing it.

Because a correct skip and a successful run are the same row in a fleet view. Our browser-driven loops post by driving Chrome through an extension bridge, and when that bridge drops the loops refuse to half-post and skip instead, which is the right behaviour. The skip records as ok. On 2026-07-23 every browser loop across our three repos posted nothing all day for that reason and the fleet view showed a normal day until a human asked why nothing had gone out. We now run a bridge check before the posting window. The honest follow-up is that the check has since produced a reading nobody can classify: on 2026-07-27 it recorded that a healthy check had slowed past its own timeout and would eventually report a false outage, and on 2026-07-28 it reported the bridge down on exactly that condition, hours before the same bridge posted four comments. Whether that was the false alarm it predicted or a real drop somebody fixed without logging it, the record does not say, and a check that cannot tell its own probe timing out from the channel being down is reporting on itself.

We run seven that touch social, out of 29 loops on the fleet as of 2026-07-28, and what matters is the split rather than the count. Four of the seven put text on a live account without a human in the moment. Three of those post or queue directly: the Reddit value-comment loop, the X reply poster, and the LinkedIn repurposer on its tweet branch, which queues to a company page through Buffer unattended. The fourth is the X reply surfacer, which posts nothing itself but writes a daily queue whose auto-flagged rows the poster sends unattended, capped at three to five a day, so its output does land and does carry attribution. Three end at a draft a human sends: the daily X post drafter, the X engagement drafter, and the Superdesign answer-engine loop, whose spec says it drafts and presents and never posts and whose auto-post gate was retired on 2026-07-17. Getting that split right matters in both directions, and we got it wrong twice. Counting the surfacer as draft-only hid one loop's output going out unattended. Counting the answer-engine loop as a poster and the LinkedIn loop as draft-only produced the right total with the wrong two loops in it, because one loop can carry both behaviours on different branches and only the spec says which.

Firsthand. Every loop, run outcome, ledger line and karma figure below was read from the live fleet on 2026-07-28 through the loopany CLI and the account's own API, never from the copy of the fleet specs checked into this repo, which is a stale mirror. Where a loop has produced no measurable result, this page says so rather than reporting activity as outcome. See our [editorial standards](/about).
