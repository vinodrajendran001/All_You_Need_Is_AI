---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-ai-agent-seo-loop
title: How to Build an SEO Agent Loop (2026)
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/ai-agent-seo-loop
published: '2026-07-28'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# How to Build an SEO Agent Loop (2026)

On 2026-07-27 one of our SEO loops finished its run and reported that the head term it owns was at position 2.75. The weekly scorecard that grades that loop read the same number and wrote `SCALE, confirmed`.

Here is what the term was actually doing, one day at a time, pulled from the Search Console API on 2026-07-28:

| Date | Position | Clicks | Impressions | CTR |
| --- | --- | --- | --- | --- |
| 2026-07-20 | 1.42 | 411 | 983 | 41.8% |
| 2026-07-21 | 1.56 | 553 | 1,459 | 37.9% |
| 2026-07-22 | 2.27 | 351 | 1,116 | 31.5% |
| 2026-07-23 | 3.70 | 231 | 1,353 | 17.1% |
| 2026-07-24 | 4.86 | 125 | 1,084 | 11.5% |
| 2026-07-25 | 5.33 | 84 | 982 | 8.6% |
| 2026-07-26 | 7.30 | 68 | 1,331 | 5.1% |

That last row is the earlier of two pulls made that day. 2026-07-26 was still preliminary when it was read, and by the re-pull at 2026-07-28T12:03Z it had firmed to position 7.2947 on 72 clicks and 1,337 impressions. The six rows above it are finalized and identical in both pulls. Both readings ship with their times, the same as the 3.11 further down, and the 12:03Z pair is what is retained in the repo. The score does not move either way: the 3-day median is 5.33 on both.

Six consecutive days of decline. Clicks from 411 a day to 68. And the monitor watching it said 2.75, which sits comfortably inside the band we call healthy.

The monitor was not broken and it did not fail. It returned a correct number. Request those same seven days from the API as one window instead of seven, which is what our loop was doing, and the answer is position 3.785. That is the true impression-weighted average of the window. It is also useless, and the reason it is useless is the point of this page.

![The same seven days of Search Console data drawn twice: on the left the request carries a date dimension and returns seven rows, position 1.42 then 1.56, 2.27, 3.70, 4.86, 5.33 and 7.30 with clicks falling from 411 a day to 68, which scores as a critical verdict on a three-day median of 5.33 plus a 5.74-place slide; on the right the same request with the dimensions field omitted returns a single row at position 3.785, the true impression-weighted average of all seven days, which our loop reported as 2.75 and the weekly scorecard recorded as confirmed, because the term went live on the first of those days so every window in the fortnight after contains its own launch days holding the average down](/images/blog/ai-native-seo-daily-vs-window-diagram.png "The same seven days of Search Console data drawn twice: on the left the request carries a date dimension and returns seven rows, position 1.42 then 1.56, 2.27, 3.70, 4.86, 5.33 and 7.30 with clicks falling from 411 a day to 68, which scores as a critical verdict on a three-day median of 5.33 plus a 5.74-place slide; on the right the same request with the dimensions field omitted returns a single row at position 3.785, the true impression-weighted average of all seven days, which our loop reported as 2.75 and the weekly scorecard recorded as confirmed, because the term went live on the first of those days so every window in the fortnight after contains its own launch days holding the average down")

What this page carries instead of a fix is the monitoring rule, written out so you can implement it against your own Search Console data: score a keyword on the daily series, refuse to produce a verdict from a window average at all, and drop the two kinds of row that carry no reading. Including the two clauses our own version got wrong, where it passed something it should have caught.

It also carries the rest of the loop around that monitor, because a monitor on its own will not do the job. This goes deeper than the Step 1 section of [how to become an AI-native company](/blog/how-to-become-an-ai-native-company), which says to build this loop first and then does not tell you what goes in it.

One assumption up front: you have decided to run search as a loop rather than as a person with a spreadsheet. Whether SEO is worth doing at all in 2026 is a different argument and this page does not make it.

And one note about the page itself, which the design brief behind it carries and this page should too. The intent for this page is **unvalidated**. A 90-day Search Console pull on 2026-07-28 across every query this domain drew, `dataState:"final"`, returns six rows containing `seo`, totalling 19 impressions and zero clicks, and the `rank` rows on the property are all "ai coding agent ranking" intent, which is a different topic. No keyword tool was run against any of the terms in this page's frontmatter, and nothing on this property demonstrates demand for them. The slug sits where our authority already is, in the agent-loop lane, rather than where the generic SEO-tooling volume is. What is demonstrated here is the problem, on our own fleet, on dated evidence, which is a different claim from demand. The [social spoke](/blog/ai-agent-social-loop) made the same call for the same reason.

---

## What Actually Runs

As of 2026-07-28 our fleet is 29 loops, and eight of them touch search: five running engines, a paused template, a weekly scorecard that grades two of the engines, and a blog enrichment engine. Eight loops covering four kinds of work, spread wider than the work is because two brands are involved and each brand needs its own engine.

Naming those four kinds of work is worth the paragraphs, because collapsing them into one loop is the mistake that costs the most.

A scout runs weekly and hunts for a term people are starting to search that nobody has ranked content for yet. Ours runs Tuesday mornings and its output is one article or nothing. It produced nothing on 2026-07-14, 07-21 and 07-28, which is a pass rather than a failure, because its spec carries an explicit valve: if no candidate passes the bar that week, that is a valid outcome, do not force a weak article.

The ship-mode engine sits on a term that has already proven itself, running daily or a few times a week, widening the cluster around it while competition is thin. It is the only one of the four that ships on a schedule, and the one that needs the most restraint written into it.

A bounded monitor has an end date. It points at a new bet, reads the day-7 result and either recommends scaling or drops it. Ours are cron entries that fire once. The graph engine in this article exists because a bounded monitor read a day-4 number, escalated, and a human said go.

The scorecard runs weekly, grades the engines and writes a report a human reads. It ships nothing and changes nothing, and its own spec puts it in those words: a monitor that produces a report and does not act.

Keeping them apart is about failure modes rather than about tidiness. The scout and the engine are scored differently, run on different cadences, and go wrong in opposite directions. A scout that ships every week is manufacturing articles. An engine that only ships when something is obviously worth shipping compounds nothing. One loop holding both ends up re-deriving which mode it is in on every run, which is expensive in tokens and produces a different answer each time.

The mechanics of a single one of these, the discover-plan-execute-verify cycle underneath, are in [loop engineering](/blog/loop-engineering-guide-2026), and this page does not restate them.

### Why This Function Goes First

The pillar's selection rule is that you automate the frequent, measurable, reversible and public before the infrequent, subjective, irreversible and customer-facing. SEO clears all four. The part worth adding here is the one that only becomes obvious once you have run it: **the success signal comes from a system you do not control.**

That property is doing more work than the other three combined. Search Console is not your database, so the loop cannot grade its own homework against it. The other candidate first functions we looked at all fail this test. A support loop scoring itself on resolution rate is scoring a number it produces, and so is a content loop scoring itself on articles shipped.

The catch, and this page is mostly about the catch, is that an external signal you read wrongly is worse than no signal, because it comes with authority.

---

## The Wedge, With Our Numbers

The strategy half of this is short, and the rest is execution.

Our domain has close to no authority, and on the established head terms we went after it did not rank. The incumbents hold the authority and the links and nothing we wrote moved that. What did work was landing on a term about a fortnight old, while nobody had built authority on it because it had not existed a month earlier.

That is one domain in one window and it is the whole of our evidence for it. It is a reason to go and test an emerging term on your own property, not a rule about emerging terms. The receipts table at the bottom scopes the same numbers the same way.

The consequence people get backwards is the clickthrough rate. On an emerging term your CTR runs high, not low, and it runs high for a boring reason: you are at position 1 to 3 because nothing else is, and position 1 to 3 is where clicks are. The high CTR is a symptom of thin competition, not of anything you did to the page.

Here is that contrast on one domain in one window, from a live pull on 2026-07-28 covering 2026-06-29 to 07-26:

| Page or query | Clicks | Impressions | CTR | Position |
| --- | --- | --- | --- | --- |
| The graph-engineering pillar (live ~7 of 28 days) | 2,978 | 27,252 | 10.93% | 4.54 |
| Exact query "graph engineering" | 1,823 | 8,308 | 21.94% | 3.79 |
| Exact query "loop engineering" | 145 | 5,321 | 2.73% | 9.02 |
| The whole site, all queries | 14,794 | 1,009,266 | 1.47% | 7.57 |

The pillar became the top page on the site by clicks in that window, having been live for about seven days of it. The exact head term ran a 21.94% clickthrough rate against 1.47% sitewide. The comparison row that matters most is the third one: same domain, same month, same team, a term we went after when it was already contested, sitting at position 9 and taking a 2.73% clickthrough.

Two scope notes, because this table invites two conclusions it does not support. These are our numbers on our domain in one 28-day window, and nothing here measures whether any of it transfers to yours. And the first row is not a rate: that page was live for roughly a quarter of the window, so it is a total for a partial period, not a monthly figure to extrapolate.

The scoring rule that falls out of this is the part worth copying whole. **Score an emerging term on position and footprint. Score a mature page on clicks.** Backwards in the first direction and the loop abandons the land grab exactly as the ground becomes valuable, because an emerging term has no clicks yet by construction. Backwards in the second and a page ranks respectably while converting nothing and nothing in the system ever marks it a failure.

Our two engines have literally opposite north stars for this reason, and both say so in their specs. The graph engine: north star is position plus footprint, not clicks. The loop engine, whose cluster matured: the score is cluster clicks, position is a diagnostic.

---

## The Failure

Now the part that cost us the term.

If you are going to score an emerging term on position, position has to be a number you can trust. Ours was not, and the way it was wrong is not obvious, which is why it survived several weeks of daily runs and a weekly review.

### A Window Average of a Young Term Contains Its Own Launch

Our engine pulled position like this, and the shape of the request is the whole bug:

json

```
{
  "startDate": "<21 days ago>",
  "endDate": "<yesterday>",
  "dimensions": ["query"],
  "dimensionFilterGroups": [{ "filters": [
    { "dimension": "query", "operator": "equals", "expression": "graph engineering" }
  ]}],
  "rowLimit": 100
}
```

Read `dimensions`. It says `query`. There is no `date` in it, so the API returns **one row for the whole window**, and the position on that row is the impression-weighted average of every day inside it. There is no way to recover a series from that response, because the series was averaged away before it was sent.

The part that took us a while to see is arithmetic rather than a finding: our term was younger than the window, so **the term's own launch days were inside the average, holding it down.** Our page went live 2026-07-20. Every window ending in the following fortnight contained the pos-1.42 and pos-1.56 days at the top of it. The average could not go bad quickly because its best days were permanently in scope. How much that matters on a term older than the window, we did not measure, and it is not the case this page is about.

The instinct is to shorten the window. That does not fix it, and we have the receipt: the weekly scorecard was already reading a 7-day blend and it reported 2.75 and `SCALE, confirmed` on the same day. Seven days was still longer than the term's whole life. Any window long enough to be stable is long enough to contain the launch.

There is a second half to the same mistake and it is the one that made the report read as good news rather than as neutral. The **family footprint kept growing** through the slide, from 35 ranking queries to 83, and that got reported as health. It was the long tail filling in while the head bled. Two numbers going in opposite directions, and the run message led with the friendly one.

### Two Rows That Are Not Readings

Two smaller things fall out of moving to a daily series, and both of them will silently produce a friendly number if you skip them.

The first is a zero-impression day, which the API reports at position 0.0. That 0.0 records the absence of a reading rather than a rank. On our own pull for this term over 2026-06-15 to 07-28, 36 of the 44 rows returned were zero-impression days at position 0.0. Leave them in a median or a mean and they drag it toward zero, which reads as first place. A term that has stopped ranking entirely will look like it is winning.

This is the same rule the pillar's loop-spec excerpt already carries in one line, and it is in three of our SEO specs in the same words: a missing day is missing, never 0. Never write 0 for a failed read.

The second one is a partly-collected day. Search Console finalizes with a lag of a couple of days, so the trailing days of any window are partial, and a day that is 5% collected can report almost any position off a handful of impressions. On our sibling loop-engineering term, two consecutive thin days reported 21.9 and then 10.5.

What we test on is volume rather than the date. A preliminary day counts only if it carries a real share of a typical day's impressions, and ours uses half the median of the days before it. Testing on the date instead does not work here, because how preliminary a day is depends on when you asked.

The trap underneath that rule is that **the test is only valid where preliminary rows can exist.** A finalized series losing impressions is a term losing reach rather than a series still being collected, and the two look the same in the response because the difference lives in the request. We ran the volume test over both for weeks, which meant it ate exactly the days carrying the bad news. What closes it is a field in the response itself, and the rule written out below states the clause and what skipping it costs.

Those two pull against each other and it is worth saying so rather than hiding it. Waiting for finalized days only is the same blindness two to three days slower. Using a preliminary day means using a reading that might be off a handful of impressions, as the 21.9 above was. What we do with that tension is a preference and not a finding: a preliminary day counts only after it clears the volume test, and when both a finalized and an including-preliminary series are available we score the worse of the two. That escalates early, and it can escalate on a thin day. We would rather look twice than find out late. Clicks are a different matter, because a partly-collected day undercounts them by construction, so we do not score clicks on one at all.

---

## The Monitoring Rule, Written Out

There is no script attached to this page. The one we run reads Search Console responses in our pull shape, carries our band settings, and assumes our conventions about missing data, so handing it over would hand you our plumbing. The rule underneath is what travels, and it is short enough to state and implement in whatever your loop already speaks.

Two of the clauses below exist because our own implementation got them wrong and reported a healthy term while the term was sliding. Both are called out where they sit.

### What The Input Has To Be

Refuse anything other than a daily series. A response requested without a `date` dimension carries the impression-weighted average of the whole period on one row, and that cannot be un-averaged afterwards, so declining is the only honest answer to being handed one. There is no safe fallback to drop into.

The same refusal covers a response keyed on a date plus something else. `dimensions:["date","query"]` returns a row per date per query, every row's first key is still a date, so a check that reads only the first key waves it through and the median then runs across a mixture of terms. Refuse two rows carrying the same date, which is what concatenating two pulls produces.

### Which Rows Carry No Reading

A zero-impression day comes back at position 0.0, and that 0.0 records the absence of a reading. Left in a median it drags the score toward zero, which reads as first place, so a term that has stopped ranking entirely looks like it is winning. On our own pull for this term over 2026-06-15 to 07-28, 36 of the 44 rows were that shape. Drop them, and say how many you dropped.

A thin trailing day is unusable for a different reason. Search Console finalizes with a lag of a couple of days, and a day that is 5% collected can report almost any position off a handful of impressions: two consecutive thin days on our sibling term reported 21.9 and then 10.5. Test on volume rather than on the date, because how preliminary a day is depends on when you asked. Ours drops a trailing day carrying under half the median of the days before it, recomputing that median at each step so a run of thin days is eaten one at a time from the end rather than stopping at the first.

### The Clause That Decides Whether The Drop Is Allowed

This is the one we shipped wrong. The volume test is valid only where a preliminary row can exist. A finalized series losing impressions is a term losing reach, and in the rows alone it looks exactly like a series still being collected, because the difference lives in the request. Run the drop over finalized data and it eats the days carrying the bad news and scores the old good ones. Take a term at 1,000 impressions and position 2 for three days, then four finalized days at 400, 200, 100 and 50 impressions at position 9. That is a term being pushed off the page, and a cascading volume filter reports it as healthy. It is this page's own headline failure, produced by the rule written to stop it.

The response tells you where the boundary is, and we were throwing the field away. A `dataState:"all"` response carries `metadata.firstIncompleteDate`, and every row dated before that day is finalized. The retained `all` pull behind this page carries `"firstIncompleteDate": "2026-07-27"`. So: read it, and never drop a row dated before it, however thin that day looks. When the field is absent and a drop would change the verdict, refuse rather than guess. Pushing the question back at the caller costs a rerun. Guessing costs the collapse.

### What To Score

Score a short median of the daily series, three days on ours, rather than the latest day. A single day is reactive enough to be scored on noise, and a monitor that fires on noise gets muted. Check the absolute band and the slide separately, so a term falling fast from a still-respectable position escalates on the slide alone. Ours sets bands at 3, 4.5 and 7 and treats a slide of 1.5 places over 5 days as an escalation on its own. Those numbers are ours and they are tuned to a standing top-3 objective, so set your own. Cap the median window at about a week: past that the score is a median of a period rather than of recent days, which is the trailing window this rule exists to refuse wearing different arithmetic.

Print the window average beside the verdict, labelled as the number you declined to score on. Deleting it would be cleaner. It would also remove the one place a reader can see how big the gap between the two readings is, and that gap is what makes the rule stick. On the pull behind this page the daily verdict is `CRITICAL` on a 3-day median of 5.33, and the trailing 7-day impression-weighted average sits at 3.79, which lands in the band we call watch.

Both of those figures carry a pull time rather than a date, 2026-07-28T12:03Z, and that is load-bearing for this page's own subject. An earlier pull the same day, taken while the finalized window still ended 2026-07-25, gave six usable days and a declined average of **3.11**. By 12:03Z 2026-07-26 had finalized, the usable window was seven days, and the declined average was **3.79**, which is the same 3.785 the aggregate request at the top of this page returns. The score of 5.33 and the verdict did not move. The number nobody should be scoring on moved by 0.68 of a place in a few hours, because the data firmed underneath it. Both API responses are retained in this repo under `campaigns/content-plan/gsc/`, and a pull made today gives a third set of numbers again, which is the behaviour rather than a defect.

If you have both a finalized pull and an `all` pull of the same window, score the worse of the two medians. That escalates early and it can escalate on a thin day. We would rather look twice than find out late. Clicks are a different matter, because a partly-collected day undercounts them by construction, so do not score clicks on one at all.

### The Verdict States, All Of Them

The failure being fixed is a monitor whose broken state looks like its healthy state, so enumerate the states and give each one its own name in the output.

| Verdict | When |
| --- | --- |
| `OK` | Score inside the first band, and no qualifying slide |
| `WATCH` | Second band, or first band with a qualifying slide |
| `SLIPPING` | Third band, or escalated into it |
| `CRITICAL` | Past the last band, or escalated into it |
| `INSUFFICIENT_DATA` | Fewer than two usable days survived filtering |
| `REFUSED` | The input is an aggregate, keyed on something other than a date, keyed on a date plus another dimension, or carrying two rows for one date. Also: a series whose data state cannot be established and whose trailing days the volume rule wants to drop, and a two-series pair that shares no date or disagrees on one it does share |
| Malformed input | Unparseable, `rows` present and not an array, or a setting outside its documented range |

`INSUFFICIENT_DATA` is the one worth arguing about, and it is why the list is this long. If every row gets dropped, you have no idea where the term ranks. The tempting answer is to say nothing and report healthy, which is what a monitor with a bug does, and a run that found nothing wrong looks the same as a run that could not look. Give it a name of its own and say in words that no verdict was produced.

### The Limits, Said Out Loud

A Search Console response carries no copy of the request that produced it, which means it does not tell you the query or the property or the data state. Everything a two-series comparison can check is therefore structural: that both series share at least one date, that the `all` series contains every finalized date, and that the shared dates agree on impressions and on position, because a finalized day does not change when you re-request it with a different `dataState`. That catches a mix-up, and we needed it, because our own implementation happily scored a finalized file for one term against an `all` file for another and reported the two as one term at position 1.

What it cannot do is prove that both files describe the same term, and nothing in the payload can. Two different terms whose daily numbers fall inside whatever tolerance you allow will pass. Choose that tolerance deliberately and print it, because "the shared dates agree" means whatever slack you built in, and ours allowed 0.1 of a place and 5% of the impressions until a review said so out loud. Print the limit next to the verdict rather than leaving it in a comment.

The second limit is the first one wearing a different hat. A day that is 5% collected and a day on which your term is dying look the same in the rows. `firstIncompleteDate` settles it when the response carries it. When it does not, the caller has to declare the data state, and a caller who declares it wrong gets a wrong answer with a green light on top.

One honest delta from what we run. Our production pre-stage escalates on a two-step ladder, from ok to watch at 1.5 places and from watch to slipping at 3. The rule as written above escalates one band at a single threshold from any band, which is stricter, so a term already slipping that keeps falling reaches critical here where ours would not.

The thing to try if you are implementing this. Build it without the zero-impression drop and run one of your own real series through it, one where the term has genuinely stopped ranking. It comes back healthy. That is what the bug looks like from the inside, and it is the cheapest way to convince yourself the clause is load-bearing.

---

## What Else Goes In The Spec

The monitor is the part that was hard-won. Four other things in our SEO loop specs are worth stating, and all four are about when the loop is allowed to do nothing.

Start with a quality valve, written before the happy path. Every one of our SEO specs has a branch that says ship nothing and log why, with the rejected candidates and the reason. The graph engine states its rationale in place: thin cluster pages actively hurt the pillar. Our scout used its valve on 2026-07-14, 07-21 and 07-28, three scheduled runs in a row that shipped nothing. A spec with no way to say no-op has given the loop no way to tell you there was nothing worth doing, and what arrives instead is an article.

Then external grounding, checked every run. The failure mode here is a loop that reads only your own pages and your own Search Console data. That is a closed circle: it produces internal link reshuffles, reports progress, and cannot move a term you do not already own. Our loop-engineering engine did exactly this from 2026-07-14 to 07-23 and the head term went to page two, while the answer sat unread in the owner's own bookmarks. The spec now names a sourcing order and puts an outside source first.

After that a cooldown, per page. One edit per page per window, or two changes inside a fortnight and neither result is readable. Our Superdesign engine runs 14 days on the page that earns the largest share of that site's clicks and 7 on everything else, with the reasoning stated in its spec: it is correct to leave clicks on the table rather than perturb the page that earns the largest share of them.

And merging stays the human's call. Every run counts its own unmerged PRs and reports the count, and the spec tells the loop that while any of them sit there, flat position is expected rather than failure. Without that line a loop reads its own review queue as a performance problem and ships more to fix it. The review-bandwidth ceiling underneath this, as four files you can put in a repo, is [reviewing AI-generated pull requests](/blog/reviewing-ai-generated-pull-requests).

And one thing to know before you cost this out. Our graph engine's complete metered history over four days was $19.06, of which $6.65 went on two runs that failed on infrastructure and produced nothing. Whether the number your runner shows you is a total or a floor is the subject of [why your agent bill is wrong](/blog/ai-agent-runaway-cost).

---

## What The Skill Covers, And What It Does Not

The strategy half of this page is published as a skill. `seo-growth` in the [AI Builder Club skills repo](https://github.com/AI-Builder-Club/skills?utm_source=blog&utm_medium=article&utm_campaign=ai-agent-seo-loop&utm_content=skill) is free and installs as a Claude Code plugin.

Checked on 2026-07-28, here is what is actually in it. Two playbooks, `cold-start.md` for a property with no rankings and `with-data.md` for one with a page that already earns, on the argument that those two situations need opposite behaviour and most bad SEO advice is given to the wrong one. Plus `emerging-terms.md`, which is the wedge above with the seven gates a candidate has to clear; `measurement.md`, which carries the position-versus-clicks rule, the four query families that score zero clicks by design, and a table of six Search Console traps; `operationalize.md`, which is the four loop roles; and `why-these-rules.md`. The property names and most of the traffic figures are stripped from the published version.

What is not in it: **the failure this page is about.** The six traps in its table are data lag, impression-weighted position, query clicks undercounting page clicks, apex versus www, metric mis-binding and cached reports. The trailing-window blind spot is not one of them, the daily-series rule is not in the skill, and neither zero-impression days nor the preliminary-day volume test appear anywhere in it. That gap is real and dated: the skill and its published copy were written the morning of 2026-07-27, and the rewire landed on our loops later the same day and has not propagated back.

So install it for the strategy and take the monitoring rule from this page. If you install it expecting that rule to be in there, it is not, and I would rather say so than let you find out from a chart.

---

## Receipts

| Claim | Status |
| --- | --- |
| The daily series 1.42 / 1.56 / 2.27 / 3.70 / 4.86 / 5.33 / 7.30 for "graph engineering", 2026-07-20 to 07-26 | Firsthand. Pulled live from the Search Console API on 2026-07-28 against `sc-domain:aibuilderclub.com`, `dimensions:["date"]`, `dataState:"all"`. Identical to the values our own engine's 2026-07-28 run report recorded. **The 07-26 row is the earlier of that day's two pulls**, taken while the day was still preliminary. In the retained 12:03Z responses it reads 7.2947 on 72 clicks and 1,337 impressions, which the article prints beside the table. The six rows before it are identical in both pulls, and the 3-day median of 5.33 is the same either way |
| The same seven days as one window return position 3.785 | Firsthand. Same API, same filter, same dates, `dimensions` omitted. The request is printed on the page so it can be re-run |
| Our loop reported head position 2.75 on 2026-07-27 and the scorecard wrote `SCALE, confirmed` | Firsthand, dated. The engine's own run report and the scorecard's report for that date. The scorecard has since recorded a correction retracting the top-3 evidence behind that call |
| Family footprint grew 35 to 83 ranking queries during the slide | Firsthand, from the same two run reports. Used only to show that two numbers moved in opposite directions and the friendly one led the report |
| Shortening the window does not fix it: the scorecard was on a 7-day read and still said 2.75 | Firsthand, dated 2026-07-27. One term, one fleet. It supports "a window shorter than the term's life did not help here," not a general claim about window lengths |
| 36 of 44 rows were zero-impression days at position 0.0 | Firsthand. One live pull, 2026-07-28, 2026-06-15 to 07-28, that term. A property of that response, not a rate |
| Two consecutive thin preliminary days reported 21.9 and then 10.5 | Firsthand, from the loop-engineering engine's spec, which records it as the reason for the volume test |
| The graph pillar at 2,978 clicks / 27,252 impressions / 10.93% CTR, top page on the site, 2026-06-29 to 07-26 | Firsthand. Live page-dimension pull, 2026-07-28. Live for roughly 7 of those 28 days, so it is a total for a partial period and not a monthly rate |
| Exact query "graph engineering" 21.94% CTR vs "loop engineering" 2.73% vs 1.47% sitewide, same window | Firsthand. Three live pulls, 2026-07-28, same window and same property. A comparison within one domain in one window and nothing wider |
| Eight dedicated articles on the term existed on 2026-07-28 that did not exist at launch | Firsthand, as a dated observation recorded in the engine's own 2026-07-28 report from a live search check. It is a count someone made on one day, not a market measurement |
| 29 loops, 8 touching search, 2026-07-28 | Firsthand. `loopany loops` and `loopany loops --json` on the machine that runs the fleet. Same count spokes 2 and 4 carry, re-derived |
| This property draws no SEO intent today: six `seo` rows, 19 impressions, zero clicks, 90 days to 2026-07-27 | Firsthand. Live GSC pull 2026-07-28, `dimensions:["query"]`, `dataState:"final"`, `sc-domain:aibuilderclub.com`. **The intent for this page's terms is unvalidated** and the article says so in place. The `dataState` qualifier is part of the claim: a same-day `dataState:"all"` pull had already moved to 8 rows and 21 impressions, which is preliminary data arriving rather than a contradiction |
| The quality valve, the sourcing order, the cooldowns, the `prs_unmerged` rule | Firsthand. Quoted in substance from the live loop specs. The pillar already publishes a redacted excerpt of one of them |
| The loop-engineering head term slipped to page two while grounding only on our own pages | Firsthand, dated to 2026-07-14 through 07-23 in the engine's own record. One loop, one term |
| $19.06 over four days, $6.65 of it on two failed runs | Firsthand. Metered per-run cost, 6 of 6 runs priced. Carried from the pillar, not re-derived here |
| The 3-day median of 5.33 matches the figure our own engine published for that term | Firsthand. Derived from a two-series pull taken 2026-07-28T12:03Z, checked against a run report written that morning. **Both API responses are retained** in `campaigns/content-plan/gsc/`, so the medians re-derive from the files with no network and no key |
| The declined window average was 3.11 at one pull that day and 3.79 at the next | Firsthand, and **the drift is the claim**. The finalized API advanced to include 2026-07-26 between the two pulls, so the usable window went from six days to seven. The verdict and the score of 5.33 are the same in both. **The 3.11 is not reproducible from any request made now**, which is why the article labels each transcript with a pull time rather than a date and retains the response behind the current one |
| A two-series comparison cannot prove both series describe the same term | Firsthand, found by a review on 2026-07-28 against our own implementation, which scored a finalized file for one term against an `all` file for another and reported the pair as one term at position 1. **The residual limit is stated as a limit**: the payload carries no query identity, a structural cross-check can only compare shared dates within whatever tolerance it allows, and ours allowed 0.1 of a place and 5% of the impressions. Two terms inside that tolerance still pass |
| A finalized volume decline can be dropped as preliminary collection and read as healthy | Firsthand, found by a review on 2026-07-28 against our own implementation. 1,000 impressions at position 2 for three days, then 400, 200, 100 and 50 at position 9, every row finalized. **This is the page's own headline failure produced by the rule written to stop it.** The clause that closes it is written out on the page: `metadata.firstIncompleteDate` marks where incomplete data starts, and rows dated before it are never dropped. That field is present in the retained `all` response on this page |
| What `seo-growth` contains and does not contain | Firsthand, dated. The published repo's file list and the contents of `measurement.md` read at `raw.githubusercontent.com` on 2026-07-28. The absence is stated as an absence in that file on that date |
| Position bands at 3, 4.5 and 7, and a 1.5-place slide in 5 days | Firsthand. Our own thresholds, live in three loop specs and their pre-stages. **Not a recommendation and not a finding.** They are tuned to a standing top-3 objective on our terms. The spec carries them as settings and the article says to set your own |
| The 3-day median, the half-a-typical-day preliminary threshold | Same. Ours, and the shape of the rule rather than evidence about what your numbers should be. The median window is capped at about a week for a stated reason rather than a tuned one: past that the score is a median of a period rather than of recent days, which is the window average this page is about wearing different arithmetic |

What is missing, and why. A tidy before-and-after showing the rewired monitor catching the slide in production was not available, because the rewire landed on 2026-07-27 and the slide had already happened, so what exists is a replay over data from before the fix rather than a live catch, and I am not presenting a replay as a save. A figure for how much traffic the delay cost us would have been the most quotable number here, but separating the loss caused by noticing late from the loss caused by eight competitors arriving is beyond what the data supports, so there is no number.

---

## Start Here

Pull one term as a daily series and look at it. That is the whole first step, and it takes one request body against the Search Analytics endpoint, however you talk to it:

json

```
{
  "startDate": "2026-06-28",
  "endDate": "2026-07-28",
  "dimensions": ["date"],
  "dimensionFilterGroups": [{ "filters": [
    { "dimension": "query", "operator": "equals", "expression": "your term" }
  ]}],
  "rowLimit": 100,
  "dataState": "all"
}
```

Then look at `metadata.firstIncompleteDate` in the response before you look at the rows, because that one field is what separates a day still arriving from a day your term lost, and those are opposite verdicts off the same shape of numbers. It is easy to skip. If it is absent, pull the window twice with only `dataState` changed, score the worse of the two medians, and cross-check that the pair agrees on every date they share.

Take the 3-day median of what survives, then take the impression-weighted average of the whole window and compare the two. If they land in different bands, you have been reading the wrong number, and you now know by how much. If they agree, you have lost nothing and you have a monitor.

Then go and look at whatever your loop or your dashboard currently reports as position, and check the request behind it for a `date` dimension. If it is not there, the number is an average of a period, and how misleading that is depends entirely on whether the term is older than the period.

After that, the order that worked for us: write the quality valve before the happy path, name an outside source the loop must read every run, put a cooldown on the page that earns the most, and make the loop count its own unmerged PRs so it stops reading your review queue as a ranking problem.

The tooling is open source. [AI Builder Club Skills](https://github.com/AI-Builder-Club/skills?utm_source=blog&utm_medium=article&utm_campaign=ai-agent-seo-loop&utm_content=start-here) ships `seo-growth` for the strategy and `new-loop` for the shared file-based memory a loop reads and writes. The engine itself you build by hand, and the monitoring rule is on this page.

If you want the full build layer by layer, the [Loop Engineering course](/courses/loop-engineering) goes from prompting an agent yourself to a loop that wakes on schedule, ships behind quality gates, and reports back.

---

## Related Content

- **[How to Become an AI-Native Company](/blog/how-to-become-an-ai-native-company)** - The pillar this hangs off. Step 1 says build this loop first; this page is what goes in it.
- **[Loop Engineering: Stop Writing Prompts, Start Writing Verifiers](/blog/loop-engineering-guide-2026)** - The mechanics of one loop, and why the verifier is the bottleneck. The monitor on this page is a verifier that was wrong.
- **[Graph Engineering](/blog/graph-engineering-guide-2026)** - The pillar whose collapse this page is about, and the one that earned the traffic in the wedge table.
- **[How to Evaluate AI Agents](/blog/how-to-evaluate-ai-agents)** - Why self-evaluation skews optimistic, and how to build a gate that does not drift. A loop scoring itself on a number it also produces is the same failure one layer up.
- **[Why Your Agent Bill Is Wrong](/blog/ai-agent-runaway-cost)** - What a loop costs, and how to tell whether the figure your runner gives you is a total or a floor.
- **[Reviewing AI-Generated Pull Requests](/blog/reviewing-ai-generated-pull-requests)** - The review-bandwidth ceiling every shipping loop runs into, as four files.
- **[A Role Label Is Not a Sandbox](/blog/agent-tool-permissions-canary)** - Testing that the guardrails you wrote for a loop actually hold.
- **[Your Agents Have Production Credentials and No Owner](/blog/who-owns-your-ai-agents)** - The registry and the autonomy ladder, for when the fleet is more loops than you can hold in your head.
- **[Self-Improving Agent Loops](/blog/self-improving-agent-loops)** - The evolve step. The rewire described here arrived through one.
- **[AI Agent Reliability and Cost Control](/blog/ai-agent-reliability-cost-control)** - Cheap triggers and model routing, which is how a daily loop stays cheap.
- **[Agent Memory Systems](/blog/agent-memory-systems-guide)** - The current-state and append-only-history split every loop spec here uses.
- **[How to Cold-Launch a Social Presence With Agent Loops](/blog/ai-agent-social-loop)** - The other half of the growth function on the same fleet, and the account-level gate a shared posting handle needs.

[Join AI Builder Club](/pricing?utm_source=blog&utm_medium=article&utm_campaign=ai-agent-seo-loop)

Because it scored position on a trailing window. On 2026-07-27 our graph-engineering loop reported a head-term position of 2.75 from a 21-day blend and the weekly scorecard called the day-7 read SCALE, confirmed. The finalized daily series for the same term ran 1.42, 1.56, 2.27, 3.70, 4.86 on 2026-07-20 through 24, and the two days after that came in at 5.33 and 7.30. Six straight days of decline averaged out to a number that sits in a healthy band. Two things made the blend lie. The term was younger than the window, so its own pos-1.4 launch days were inside the average holding it down. And family footprint kept growing, 35 queries to 83, because the long tail was filling in while the head bled, which reads as health if you report it as health. Shortening the window is not the fix: the scorecard was already on a 7-day read and still said 2.75.

On position while the term is emerging, on clicks once it is mature, and getting that backwards is expensive in both directions. Scoring an emerging term on clicks tells the loop to abandon the land grab exactly as the ground becomes valuable, because an emerging term has no click volume yet by definition. Scoring a mature page on position lets a page sit at a healthy-looking rank while converting almost nothing, with nothing in the system marking it a failure. Our graph engine's spec says north star is position plus footprint and not clicks, in those words. Our loop-engineering engine says the opposite, because that cluster matured: its score is cluster clicks and position is labelled a diagnostic.

Score a short median of the daily series rather than any single day, and check the slide separately from the absolute band. One day is reactive enough to be scored on noise. Our loops score a 3-day median with bands at 3, 4.5 and 7, and treat a slide of 1.5 places or more in 5 days as an escalation on its own, so a term falling fast from a good absolute position still alarms. Both halves have to be there, and so does the check in the other direction: a term holding around position 2 with ordinary day-to-day wobble must not alarm, and a term climbing back from 7.30 to 2.10 must not read as a slide, which is what a slide check that reads magnitude instead of sign does. A monitor that cries on noise gets muted, and a muted monitor is the same as no monitor.

The Search Console API returns those days as position 0.0, which records the absence of a reading rather than a rank. Left in a series, they pull a mean or a median toward zero, which reads as first place. On our own pull for the graph-engineering term over 2026-06-15 to 07-28, 36 of the 44 rows were zero-impression days. The rule that travels with this in our loop specs is stated the same way in three of them: a missing day is missing, never 0, and never write 0 for a failed read.

Four roles, and on our fleet those roles are spread across more than four loops. As of 2026-07-28 we run 29 loops in total and eight of them touch search: five running engines, a paused template, a weekly scorecard that grades two of the engines, and a blog enrichment engine. The roles are a scout that hunts terms weekly, a ship-mode engine per term that has proven itself, a bounded monitor that reads the day-7 result on a new bet, and a scorecard that grades the engines and reports to a human. The reason to split them is that they have different scores and different cadences, and one loop carrying all four ends up re-arguing its own strategy every run.

Not the established ones, on our evidence. What worked on our domain was landing on a term while it was days old and competition was still thin. Over 2026-06-29 to 07-26 our graph-engineering pillar took 2,978 clicks from 27,252 impressions, a 10.93% clickthrough rate, against a sitewide 1.47% over the same window, and it became the site's top page by clicks having been live for about seven of those days. The high clickthrough is a consequence of ranking 1 to 3, not of anything about the page. The other half of that story is on the same page: seven days later eight dedicated articles on the same term existed that had not existed at launch, and our position went to 7.30. The window closes.

Firsthand: the loop roles, the wedge, the failure and the fix come from eight search loops running at AI Builder Club and SuperDesign through July 2026. Every GSC figure on this page was pulled live from the Search Console API on 2026-07-28 against sc-domain:aibuilderclub.com, and the query that produced it is printed on the page. Where our own run reports and a live re-pull disagree, both are shown with their dates. See our [editorial standards](/about).
