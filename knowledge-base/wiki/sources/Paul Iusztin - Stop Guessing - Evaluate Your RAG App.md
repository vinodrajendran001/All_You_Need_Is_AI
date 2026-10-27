---
type: source-summary
created: 2026-10-27
updated: 2026-10-27
source_id: src-2026-10-06-iusztin-rag-evals
source_title: "Stop Guessing. Evaluate Your RAG App."
source_author: Paul Iusztin
source_url: https://www.decodingai.com/p/rag-evals-change-prompts
tags: [source/summary, rag, evaluation, llm-as-a-judge, observability]
source_ids:
  - src-2026-10-06-iusztin-rag-evals
status: active
---

# Paul Iusztin - Stop Guessing - Evaluate Your RAG App

## Summary

A Decoding AI article by Paul Iusztin, published 6 October 2026 and sponsored by Opik, the tracing
and evaluation platform it uses throughout. It is based on an interview with Alexey Grigorev about
adding evaluations to the FAQ system of DataTalks.Club, whose free Zoomcamp courses serve 100k+
learners. The app has two parts:

- an ingestion automation that classifies each contributed question as `NEW`, `UPDATE`,
  `DUPLICATE`, or `WRONG_COURSE`, after a minsearch lookup merged with Reciprocal Rank Fusion
  (RRF);
- a Slack assistant that answers questions from the FAQ index.

The article's five steps are collect data, build the eval set, build the evaluators, run them, and
close the loop. They carry three durable ideas:

- When no traces exist, earlier human corrections can label an eval set.
- Replaying a RAG case needs the knowledge base as it was when the input arrived: "install your
  data".
- Most checks can be deterministic, leaving an LLM judge only for free-text answers.

The numbers come from one practitioner's community project, and the practitioner describes the
setup as "not very scientific" yet.

## Key claims

**No traces? Use corrections as labels.** Grigorev shipped without recording interactions: "My goal
was to just get this out and test how it works." The first eval set was therefore built from proxy
data. Each FAQ contribution was a GitHub issue, which supplied the input. Each correction was a
commit on a pull request, which showed the expected output. A pull request accepted unchanged
became a pass. One he altered became a fail, with a one-sentence critique. The general advice is to
look for "any place a human already judged your output", such as edited pull requests, support
tickets, corrected answers, or thumbs-down ratings, and to trace everything from then on.

**Weight the set toward the silent errors.** A false `DUPLICATE` or `WRONG_COURSE` closes the issue
automatically and opens no pull request, "so I would never discover it". Only two of the four
outcomes ever reach a human.

**Replay against the corpus as it was.** A question that was new when its issue arrived is now in
the FAQ. Replaying it unchanged produces a correct `DUPLICATE`, so the case fails for the wrong
reason. The fix is leave-one-out. With 200 records, remove record D, which the issue under test
created, replay the issue against the other 199, and expect `NEW`. Each case is a few lines of
Python in Git. The case ID is the GitHub issue number, and the case also holds the question,
answer, expected action and section, and the ID of the document to remove.

**Most of the evaluation needs no judge.**

| Suite | Cases | Check | Run time |
| --- | --- | --- | --- |
| Retrieval | 25 | recall@5 against the expected chunks | about 2 seconds |
| Generation (curation decisions) | 61 | Action match, placement (section) match, cost per case | about 2 minutes |
| Slack answers | Not stated | LLM judge aligned with 10 to 15 self-labeled examples | Not stated |

Every run costs money, so the core set was trimmed to 61 cases. It holds 38 `NEW`, 10 `DUPLICATE`,
7 `WRONG_COURSE`, 4 not `WRONG_COURSE`, and 2 `UPDATE`. Trace analysis found that the most common
error was wrong section placement, such as a projects question filed under "General", rather than a
wrong decision. The article's rule is to "use code checks wherever the right answer is known",
check retrieval separately from generation, and "save LLM judges for free-text answers".

**A baseline that must not fall, not a target of 100%.** The generation set passes 42 of 61 cases
on GPT-5.4 nano. "I never needed 100 percent," Grigorev says, because his AI assistant still
reviews every pull request. When new cases lower the score, he changes nothing else and takes the
result as the new baseline. Hard cases can stay failing, so the prompt does not grow to cover every
corner case. Evals also chose the model. GPT-4o mini was "very cheap but stupid" for this decision,
and GPT-5.4 nano was the cheapest model that still did well. According to Opik's metrics, each
query costs "on average less than one cent".

**Failures become cases first.** When the automation misbehaves, the failure is first captured as
an eval case. The prompt is changed until that case passes, then the whole set is re-run: "It's
kind of test-driven development, but like eval-driven development." A bad Slack reply or a user
correction now becomes a case: a coding agent pulls the trace from Opik into the eval set. Fixes
usually go into the FAQ, the docs, or the course repository rather than into a stronger model.

## Why it matters

[[Retrieval-Augmented Generation]]: a RAG regression case is only valid against the knowledge base
as it stood when the input arrived, and leave-one-out replay is a concrete way to rebuild that
state. Once again, the evaluation loop sends fixes back into the corpus.

[[Multi-Turn Evaluation]]: this partly answers the cold-start question. Before any traffic is
traced, existing human corrections can supply labeled cases. A production eval can also serve as a
floor rather than as a target.

[[Paul Iusztin]]: his presence in the vault extends from subagent context engineering to
evaluation practice.

## Tensions / open questions

- **Sponsored, single project.** The article is sponsored by Opik. Its Opik claims are the author's
  and the vendor's: integration takes about 5 minutes, and the free tier covers 25k spans a month,
  although Iusztin adds that "a serious production app might burn that in a day".
- **Proxy labels inherit reviewer behavior.** Any edit to a pull request counts as a fail, so a
  cosmetic edit and a real error get the same label. Nothing estimates the resulting label noise.
- **Leave-one-out removes one record.** It rebuilds the corpus minus the record the issue created,
  not the full corpus as it stood then. Later edits to other records remain.
- **Small numbers.** There are 61 and 25 cases, no confidence intervals, and a model comparison
  reported in words. The practitioner himself calls the runner "not very scientific".
- **Two gaps in Opik.** Per-case record removal could not be run straightforwardly inside Opik. The
  zero-dependency Lambda function used plain HTTP requests instead of Opik's Python client.

## Affected pages

- [[Retrieval-Augmented Generation]]
- [[Multi-Turn Evaluation]]
- [[Paul Iusztin]]

## Raw capture

- [[Stop Guessing. Evaluate Your RAG App]]

## Citations

- Canonical URL: https://www.decodingai.com/p/rag-evals-change-prompts (email tracking parameters
  removed).
- Published 6 October 2026. The case-study figures (61 cases, 42 passing, suite run times) are the
  practitioner's, relayed by the author. The FAQ system's companion write-up on aishippingblog.com
  is cited by the article but was not ingested.

## Related pages

- [[Retrieval-Augmented Generation]]
- [[Multi-Turn Evaluation]]
- [[Paul Iusztin]]
- [[LLM-as-a-Judge]]
- [[Agentic Testing]]
- [[Agent Observability]]
- [[ByteByteGo - How Uber Built a Genie to Answer Questions Correctly]]
- [[Lance Martin - Automating Eval Design and Hillclimbing with Claude]]
- [[Paul Iusztin - From 1 Bloated Context Window to 6 Scoped Subagents]]
- [[AI Knowledge Base Overview]]
