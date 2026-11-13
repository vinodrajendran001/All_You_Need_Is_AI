---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-03-willison-qwen-interprets-weights
source_title: "Qwen 3.8 27B on my laptop can interpret model weights, too"
source_author: Simon Willison
source_url: https://simonwillison.net/2026/Nov/3/qwen-can-interpret-model-weights/
tags:
  - source/summary
  - interpretability
  - weight-editing
  - local-llm
source_ids:
  - src-2026-11-03-willison-qwen-interprets-weights
status: active
---

# Qwen 3.8 27B on My Laptop Can Interpret Model Weights, Too

## Summary

Simon Willison's blog post is a third-party follow-up to
[[Rikiya Takehi et al - Sparks of Weight-Space Programming]], which he calls "yesterday's hot
paper". That paper bundles two questions, and Willison argues they should be kept apart:

- what a model can infer from raw weights *without* tools or code execution;
- how well a model armed with code can analyze and update another model.

He sets aside the second question and re-runs the paper's own first experiment, using its public
prompts. Each prompt gives a model the weights of one reinforcement-learning game policy and asks
which game it was trained on, with no tools allowed. Kimi K3.1 Pro, run via OpenRouter, identified
Breakout. Qwen 3.8 27B, running locally on his laptop, identified three of the four games and took
46 minutes to over an hour per answer.

He finds this impressive but bounded. A sufficiently experienced human with a notepad and pencil
could probably get there, and some of the commentary around the paper "does not feel justified". The
result is a small, informal replication: one run per game, no repeats and no baselines.

## Key claims

### The paper mixes two claims

- Willison quotes the paper's abstract. GPT-6 Astra "can tell what a network was trained to do"
  from raw weights. It writes small game networks that outplay PPO trained for 100 million steps.
  It fixes Qwen3.5-0.8B by "natively editing 0.016% of the weights", raising MATH-500 from 7.9% to
  48.1% and IFEval "by 3x".
- He separates the no-tools question from the code-armed one and calls the first "the more
  interesting of the two".
- He cites two critics:
  - spaCy author Matthew Honnibal, who called the paper misleading for conflating the two questions;
  - Sean Goedecke, who argued that the Qwen3.5-0.8B fix takes the steps a human ML researcher would.

  Their arguments are linked, not captured.

### The replication setup

- The prompts come from the paper's `RikiyaT/lm_understand-logs` repository, folder
  `exp1_which_game`. They cover four policies trained with reinforcement learning on "simplified
  10x10 grid versions" of Breakout, Pong, Pac-Man and Freeway.
- Willison checked that the four prompts are identical apart from the weights. Each says: "You have
  no tools: no code execution, no calculator, nothing to run. This is a single response."
- He ran the prompts with his `llm` command-line tool, which can take a remote text file as a
  prompt fragment.

### Results

| Model and setup | Game | Outcome | Time and tokens | Stated confidence |
| --- | --- | --- | --- | --- |
| Kimi K3.1 Pro via OpenRouter | Breakout | Correct | **9m 41s**, **19,493** reasoning tokens | not quoted |
| Qwen 3.8 27B, local | Pac-Man | Correct | **46m 12s**, **43,506** reasoning tokens | **72%** |
| Qwen 3.8 27B, local | Pong | Correct | **1h 4m 54s** | **75%** |
| Qwen 3.8 27B, local | Breakout | Correct | **52m 25s** | **88%** |
| Qwen 3.8 27B, local | Freeway | Wrong: "A simplified Pac-Man-like grid game" | not given | not quoted |

- **Local setup.** Qwen 3.8 27B ran as a **17GB** `Q4_K_M` GGUF in LM Studio, through the
  `llm-lmstudio` plugin. The default **8192**-token context "failed with errors", so a longer
  context window was loaded and the plugin timeout raised to **900** seconds.
- **Freeway.** Willison was not surprised by the failure, because Freeway is the most obscure of
  the four games.
- **Reasoning traces.** He calls them "fun to skim, and almost incomprehensible". The sample he
  quotes is the model hand-indexing weight lines into grid rows, columns and channels.

### His conclusion

- The result is "impressive", but "a sufficiently experienced human being armed with a notepad and
  a pencil could get there with enough effort".
- He is "not ready to declare that the age of source code is over".

## Why it matters

- [[Mechanistic Interpretability]]: the vault's first third-party check on reading weights without
  tools. Exp 1 of the Sparks paper was a single-model result for GPT-6 Astra. Here, a 27B
  open-weight model running on a laptop gets three of four games, which suggests the task does not
  need a frontier model. It shows nothing about the larger tool-assisted experiments.
- [[Qwen]]: Willison calls Qwen 3.8 27B "still my favorite model to run on my own laptop", and the
  vault already records his 17 GB local setup. Here it appears as an analyst of other networks'
  weights rather than as a coding or chat model.
- [[Rikiya Takehi et al - Sparks of Weight-Space Programming]]: the post narrows that paper's
  "natively read" claim to its cleanest case, small networks with no tools. It also records named
  objections to how the paper framed its tool-assisted results.

## Tensions / open questions

- **Anecdotal, with small n.** There is one run per game and per model, with no repeats, no
  sampling settings reported, and no guess-rate baseline. Only Breakout was tried on Kimi K3.1 Pro.
  The confidence percentages are the model's own statements, not calibrated probabilities.
- **Not a test of the tool-assisted claims.** Willison deliberately leaves aside the code-armed
  experiments, including the Qwen3.5-0.8B edit. He links Honnibal's and Goedecke's critiques of
  them without summarizing their full arguments.
- **Grid-size mismatch.** Willison describes "simplified 10x10 grid versions", while Qwen's answers
  describe an "8x8" maze, board or field. The capture does not resolve this. The 8x8 could be an
  interior inside a wall border, or an error in the model's reading.
- **The prompts may not reveal the options.** The Sparks paper says Astra was not shown the
  candidate games. Willison checked that his prompts differ only in their weights, but he does not
  say whether they list possible games. The quoted prompt text does not.
- **Undated capture.** The frontmatter has no published date. The ID's 2026-11-03 comes from the
  URL path (`2026/Nov/3`), consistent with "yesterday's hot paper" for a paper published 2026-11-02.
- **Reading is not the same as understanding.** Willison's own framing keeps open whether hour-long,
  "almost incomprehensible" traces are an alien skill or a slow version of what a human analyst
  would do by hand.

## Affected pages

- [[Mechanistic Interpretability]]
- [[Qwen]]

## Raw capture

- [[knowledge-base/raw/sources/Qwen 3.8 27B on my laptop can interpret model weights, too]]

## Citations

- Canonical URL: https://simonwillison.net/2026/Nov/3/qwen-can-interpret-model-weights/
- Byline: Simon Willison
- Published: not stated in the capture; the URL is dated 2026-11-03. Captured: 2026-11-10.
- Publisher: personal blog (simonwillison.net)
- Follows up: [[Rikiya Takehi et al - Sparks of Weight-Space Programming]]

## Related pages

- [[Rikiya Takehi et al - Sparks of Weight-Space Programming]]
- [[Mechanistic Interpretability]]
- [[Interpretability Evaluation]]
- [[Qwen]]
- [[Simon Willison - 2026 in LLMs (so far)]]
- [[Nous Research - Introducing Arete-27B - Qwen3.8-27B Post-Trained to Reinforce Western Values]]
- [[On-Device Reasoning]]
- [[DoubleAI - Can LLMs Redesign Themselves as They Train]]
