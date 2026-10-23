---
type: social-post
created: 2026-10-23
updated: 2026-10-23
tags:
  - post
platforms:
  - linkedin
  - x
pages_used:
  - Text-to-SQL Agents
  - ByteByteGo - System Design and AI at Scale (May 2026 Batch)
  - Mykola-Bohdan Vynnytskyi - Understanding Databricks - Genie Explained
  - Agent Security and Governance
  - Benchmark Optimization
topics:
  - text-to-sql agents
  - guardrails vs correctness
  - data agents
  - pre-execution validation
covers_from: 2026-10-16
covers_through: 2026-10-23
status: draft
---

# A Safe Query Is Not a Correct Answer

> **Superseded on 2026-10-23:** Rejected editorially and replaced by
> [[2026-10-23 The Skyline Was the Message]]. Retained for history only; do not publish.
> Excluded from active topics and spine cooldown. Future Post runs exclude ByteByteGo.

## LinkedIn post

A safe query and a correct answer are not the same thing.

Companies are wiring language models to their data warehouses so anyone can ask a question in plain English - "how many active customers did we have last quarter?" - and get a number back instead of filing a ticket with the data team.

Almost all the engineering attention goes to making that safe. It should. But the safety work is quietly being mistaken for correctness work, and they are different problems.

ByteByteGo's write-up of Grab's analytics data warehouse team made this clear to me. That team maintains over 15,000 tables, which power roughly half of all queries in Grab's data lake and serve about 1,000 internal users every month. Their best engineers were losing two full days a week answering colleagues' questions.

So they automated it, with real guardrails in front. Before any query runs, a classifier drops requests for personal data and out-of-scope questions. Then every generated query is checked for access to personal-data columns, destructive commands like DELETE or DROP, missing partition filters that would scan an entire massive table instead of the slice you need, and whether the schema is valid. They report resolution time dropping by an order of magnitude - their own figure, with no controlled comparison.

Now notice what every one of those checks has in common: each is a property of the query text. That is why they can run before anything executes.

Correctness is not. Whether the answer is right depends on whether the model chose the right table and the right join, and a wrong join produces perfectly valid SQL. It is safe. It is cheap. It is fast. It is wrong. What comes back is a fluent sentence and a number, and nothing in the interface distinguishes a correct aggregation from a bad one.

The honest caveat: I cannot tell you how often this happens. The only accuracy figure I have for this category is a vendor benchmark, reported in Mykola-Bohdan Vynnytskyi's Databricks series: 84.5% first-attempt accuracy against 52.4% for "the strongest general-purpose coding agent", with no task distribution, no baseline description, and no independent replication. The author who reported it advises skepticism himself.

So keep the guardrails - they are doing a real job. Just don't let passing them count as evidence that the answer was right. Scope the agent to selected, curated tables rather than the whole catalog, because as Vynnytskyi puts it, "scoping is where the accuracy comes from". And build a separate way to check correctness, because execution success is not correctness.

If your data agent returned a confidently wrong number tomorrow, how would you find out?

#DataEngineering #TextToSQL #AIAgents #DataQuality #LLMEvaluation

## X post

**A) Standalone** (273 chars):

Teams wiring language models to their data warehouse check every query for destructive commands, personal data, and full-table scans before it runs.

All properties of the query text.

Whether it joined the right tables isn't. A wrong join is safe, cheap, fast - and wrong.

**B) Thread:**

1. (273 chars)
Teams wiring language models to their data warehouse check every query for destructive commands, personal data, and full-table scans before it runs.

All properties of the query text.

Whether it joined the right tables isn't. A wrong join is safe, cheap, fast - and wrong.

2. (252 chars)
The setup: ask a question in plain English, get a number back instead of filing a ticket with the data team.

The engineering attention goes almost entirely to making this safe. It should. But safety work is quietly being mistaken for correctness work.

3. (265 chars)
ByteByteGo wrote up how Grab's analytics warehouse team did it.

15,000+ tables, powering roughly half the queries in their data lake, serving ~1,000 internal users a month.

Their best engineers were losing two full days every week answering colleagues' questions.

4. (265 chars)
Their guardrails run before anything executes.

A classifier drops requests for personal data and out-of-scope questions. Then each query is checked for personal-data columns, DELETE/DROP, missing partition filters that would scan a whole table, and a valid schema.

5. (247 chars)
Notice what those checks share: every one is a property of the query text, so you can check it without running anything.

Correctness isn't. It depends on whether the model picked the right table and join - and a wrong join is perfectly valid SQL.

6. (273 chars)
The caveat: I can't tell you how often this happens.

Grab's reported order-of-magnitude drop in resolution time is first-party with no controlled comparison. The only accuracy figure I have is a vendor benchmark - 84.5% vs 52.4% - with no task distribution or replication.

7. (258 chars)
So keep the guardrails. They do a real job. Just don't let passing them count as evidence the answer was right.

Scope agents to curated tables, and check correctness separately. Execution success isn't correctness.

via ByteByteGo + Mykola-Bohdan Vynnytskyi

**Ship:** Thread. The claim needs the Grab setup and the mechanism to land; the standalone works as a
quote-post but drops the worked example. Post 1 is identical in both, so the standalone can be shipped
first and the thread built from it if it performs.

## Hook variants

1. **The distinction** - "A safe query and a correct answer are not the same thing."
2. **The counterexample** - "A wrong join is safe, cheap, fast, and wrong."
3. **The myth-correction** - "Your data agent's guardrails prove the query wouldn't hurt you. Not that the answer was right."

**Recommended:** 1 for LinkedIn - it states the whole claim in nine words and sets up the two-category
structure the post depends on. X should lead with 2, which is concrete and provocative enough to survive
a feed; the distinction then arrives as the payoff in post 5 rather than the opener.

## Why this topic

Window 2026-10-16 → 2026-10-23, covering the October 19 ingest (8 sources), the October 19 lint, the
October 23 ingest (25 sources), and the October 23 lint.

| Angle | Clarity | Completeness | Surprise | Concreteness | Reach | Freshness | Total |
|---|---|---|---|---|---|---|---|
| **Text-to-SQL: guardrails aren't correctness** | 5 | 4 | 4 | 5 | 5 | 5 | **28** |
| Semantic caching: similarity isn't correctness | 5 | 5 | 4 | 4 | 4 | 5 | 27 |
| More agents buy speed, not intelligence (Naam) | 4 | 4 | 5 | 4 | 5 | 5 | 27 |
| Decision models vs LLM judges (Husain) | 4 | 4 | 4 | 5 | 4 | 5 | 26 |
| Summarization drops the hedge that prevents the misreading | 5 | 3 | 5 | 4 | 3 | 5 | 25 |

Selected the winner. "Chat with your data" is the most widely attempted agent deployment in ordinary
companies, and the vault gained both a vendor account and a production account of it in the same week,
which is exactly the pairing that makes a claim teachable.

Rejected: the summarization angle **fails the completeness gate at 3** - it rests on a single incident
from this vault's own lint pass, not on vault-derived evidence across sources, so it cannot be published
regardless of its surprise score. The Naam angle scored well but needed two layers of hedging (a synthesis
of third-party results, carrying the author's own caveat about thin real-world data) and sits on a page
whose attribution I corrected in the same lint pass - too fresh a repair to build a public claim on.
Semantic caching was the closest contender and is held for a future run; its "similarity is not
probability of correctness" framing is the same shape of argument as this post, so shipping both in one
window would repeat the angle.

No spine conflict: [[Text-to-SQL Agents]] is new and not in cooldown, and no archive topic covers
text-to-SQL, data agents, or guardrails.

## Reader check

Reading only the public bodies:

1. **Problem?** Companies let people ask their data warehouse questions in plain English and get numbers
   back without going through the data team.
2. **Single claim?** The guardrails on these systems prove a query was safe, not that its answer was
   correct - and those are different problems.
3. **Supporting example?** Grab's analytics data warehouse team: 15,000+ tables, two days a week lost to
   questions, guardrails checking for personal data, destructive commands, full-table scans, and schema
   validity before execution.
4. **Why did it happen?** Every one of those checks is a property of the query text, so it can be verified
   before running. Correctness depends on table and join choice, and a wrong join is still valid SQL.
5. **What the evidence doesn't prove?** How often these systems are wrong. Grab's improvement is
   first-party with no controlled comparison, and the one accuracy figure is a vendor benchmark with no
   task distribution, baseline, or replication.
6. **What to do differently?** Keep the guardrails but stop treating them as correctness evidence; scope
   agents to curated tables; build separate correctness checking.

Acronyms and terms: SQL appears once in each variant, in a sentence ("a wrong join produces perfectly
valid SQL") whose meaning survives without knowing the acronym. DELETE and DROP are glossed as
"destructive commands". "Partition filters" is explained inline as scanning an entire table instead of
the slice needed. "Classifier" is described by what it does. No unexplained metric names.

Paragraph connection: situation → the mistaken equivalence → worked example → the shared property of the
checks → why correctness differs → caveat → action → question. The argument completes at "execution
success is not correctness" before the question is asked.

## Fact check

Every factual sentence traced to `pages_used`:

- **"over 15,000 tables... roughly half of all queries in Grab's data lake... about 1,000 internal users
  every month"** - verbatim from the raw capture via
  [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]: "over 15,000 tables that power roughly
  half of all queries in Grab's data lake, and about 1,000 people across the company query those tables
  every month". ✓
- **"two full days a week"** - raw: "spending two full days every week answering quick questions from
  colleagues". ✓
- **Guardrail list** - raw: "checked for PII column access, dangerous operations like DELETE or DROP,
  missing partition filters, and schema validity"; "Without these partition filters, a query might scan an
  entire massive table instead of just the relevant slice". "PII" rendered as "personal data" for a general
  reader, which preserves meaning. ✓
- **"resolution time dropping by an order of magnitude"** - raw: "Resolution time dropped by an order of
  magnitude". Hedged in both variants as first-party with no controlled comparison, matching the vault's
  "first-party and unablated" label. ✓
- **"84.5% first-attempt accuracy against 52.4% for 'the strongest general-purpose coding agent'"** -
  verbatim from [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Genie Explained]], which carries
  the vendor-claim label and "No methodology, task distribution, or independent replication is supplied".
  The post states all three absences and the author's own advice to be skeptical. ✓
- **"scoping is where the accuracy comes from"** - verbatim quoted claim on
  [[Text-to-SQL Agents]], attributed to Vynnytskyi. ✓
- **Mechanism (pre-execution checks vs correctness)** - the distinction is the vault's own, stated on
  [[Text-to-SQL Agents]]: "Grab's layers prevent dangerous and expensive queries; none of them establish
  that a permitted query returns the right number." The "fluent sentence and a number... nothing
  distinguishes a correct aggregation from a wrong join" line is also from that page. ✓

Attributions match the source summaries' `source_author`: **ByteByteGo** for the Grab material,
**Mykola-Bohdan Vynnytskyi** for the Databricks material. Both are credited inside both post bodies.

**Compression check.** The X variant keeps every qualifier that carries truth value: post 6 retains both
hedges (Grab's figure is first-party with no controlled comparison; the accuracy benchmark is vendor-run
with no task distribution or replication). The 84.5%/52.4% pair appears only alongside its vendor label,
never as a measured capability.

**Comprehension check.** The thread keeps the full chain: setup (post 2), worked example (post 3),
guardrail detail (post 4), mechanism (post 5), caveat (post 6), conclusion (post 7). Nothing load-bearing
was traded for length.

**Cut as unverifiable:** Grab's "several full-time equivalents worth of engineering bandwidth" and
"hundreds of hours" - both real in the capture but unablated self-reports that add no argumentative work.
Also cut: any estimate of how often text-to-SQL answers are wrong, because the vault holds no such figure
and the post says so explicitly rather than guessing. The Databricks Genie product status was deliberately
left out entirely, having just been corrected during the October 23 lint pass.

## Attribution

- **ByteByteGo**, "How Grab is Using AI Agents to Boost Team Productivity", in the May 2026 batch -
  https://blog.bytebytego.com - via [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- **Mykola-Bohdan Vynnytskyi**, "Understanding Databricks: Genie Explained — Genie One, Agents, and the
  Ontology" -
  https://mbvyn.medium.com/understanding-databricks-genie-explained-genie-one-agents-and-the-ontology-710792b66c5a
  - via [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Genie Explained]]

## Hashtags

**LinkedIn:** #DataEngineering #TextToSQL #AIAgents #DataQuality #LLMEvaluation

**X:** none - the thread's opening line carries the hook, and the audience for this topic is reached by
the claim rather than by tags.

## Related pages

- [[Text-to-SQL Agents]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Genie Explained]]
- [[Agent Security and Governance]]
- [[Benchmark Optimization]]
- [[Post Archive]]
