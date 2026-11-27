---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-24-uncensored-ai-free-model-catalog
source_title: "Every free uncensored AI model on the internet (103)"
source_author: Unattributed in capture
source_url: https://uncensored-ai-free.pages.dev/
tags:
  - source/summary
  - open-models
  - model-safety
  - safety-removal
source_ids:
  - src-2026-11-24-uncensored-ai-free-model-catalog
status: active
---

# Every Free Uncensored AI Model on the Internet (103)

## Summary

An unattributed, undated catalog site lists **103** open-weight models whose refusal behavior has
been removed, promising "No filters, no refusals". It is pitched mainly at traders. Each model card
shows a name, uploader and base model, a rank, three scores the site attributes to the public UGI
Leaderboard, a one-line use blurb, a memory and download size, a local-run command, and a link to
the model's hosting page. For the vault it is evidence of scale and normalization: safety-removed
derivatives of most major open families are packaged as a consumer catalog with no hazard
evaluation. This summary stays at catalog level and deliberately omits every command, link and
setup step.

## Key claims

### What the catalog lists

- **103** cards, ranked #1 to #103. The top card is gemma-4-31B-it-heretic: Uncensored IQ **65.7**,
  Reasoning **36.5**, Answers **10/10**.
- Base models named in "built on" lines span most open families. These include Gemma 4 and Gemma 3,
  Qwen3.5, Qwen3.6, Qwen3 VL and Qwen2.5, Llama 3.1 and 3.3, Mistral Large, Mistral Small and
  Magistral Small, GLM 4, GLM 4.5 Air and GLM 4.7 Flash, gpt oss 20B and 120B, Command A, Seed OSS 36B,
  Phi 4 and Apriel. Some cards stack on earlier community fine-tunes. Derived count: 15 cards give
  no base. Of the 88 that do, 17 name a Qwen checkpoint directly, from Qwen3.5 4B to Qwen3 VL 235B
  A22B, including Qwen3.5 9B.
- The bases include Qwen3.5 35B A3B, Qwen3.6 35B A3B and Gemma 4 26B A4B, the same small-active MoE
  checkpoints that [[Modaic - Latency Doesn't Lie - Jev Is (Probably) Qwen3.5-35B-A3B]] weighs as
  candidate backbones for a commercial model. Further examples are GLM-4.5-Air-Derestricted and
  Llama-3.3-70B-Instruct-abliterated.
- Model names carry the removal method as a label: heretic or heresy, abliterated, derestricted,
  lorablated, decensored, uncensored, MPOA, ARA, and norm-preserving or biprojected variants.
  Derived count: 62 of 103 names contain one of these terms.
- Memory needs run from about **5 GB** to about **144 GB**.

### How it defines removal and its scores

- The site defines an uncensored model as "An open AI model with its refusals removed." Some are
  retrained on new data. In others the part that refuses is "surgically cut out", and the name then
  says "abliterated" or "heretic". Such a model answers "directly instead of hedging".
- Its score definitions: "Uncensored IQ is how much it knows and how freely it answers. Reasoning is
  how well it thinks things through. Answers is how often it agrees to answer, out of 10." The site
  attributes the scores to the public UGI Leaderboard, but it does not describe that leaderboard's
  method or say how cards are ranked.
- *Derived observation:* the order follows the sum of Uncensored IQ and Reasoning, not Uncensored IQ
  alone. For example, #102 phi-4-heretic (IQ **36.6**) ranks above #103 (IQ **36.9**).
- The FAQ says "Every command uses the Q4 size", but some cards use a lower-bit quantization and one
  card has no command (derived counts: 5 and 1). The details are omitted here.

### Audience and the safety framing it offers

- Every blurb is about trading. Derived counts: 54 cards say "strategy ideas and trade reviews" and
  49 say "quick market summaries".
- The FAQ's case for traders is privacy ("strategies, positions and keys never leave it"), no
  "not financial advice" filler, and no API bill or rate limits, "so it can sit inside a bot all
  day".
- Its only safety answer is about trading losses: "Any AI can be confidently wrong: test on paper
  first and never let it trade without hard limits. Use the models within the law and each model's
  licence."

## Why it matters

- [[Defensive Deception for Open Models]]: its threat model treats safety removal after release as
  routine. The catalog shows removal operating as a public, labelled market across most open
  families, not as an occasional attack.
- [[Open Model Ecosystems]]: the derivative layer of open weights includes repackaged
  safety-removed models with their own leaderboard, naming conventions and audience.
- [[Qwen]]: Qwen checkpoints, including the 35B-A3B MoE line, are among the most-used bases for
  safety-removed derivatives.

## Tensions / open questions

- **No author, no date, promotional.** The site's operator is not named, and its framing ("run it
  offline for $0") is marketing. It was reached through a newsletter link with tracking parameters,
  removed here.
- **Scores are relayed, not checked.** The UGI Leaderboard is cited but not described. Uncensored IQ
  folds knowledge and willingness to answer into one number, so a high score does not mean a capable
  model. No card compares a derivative with its base model's capability.
- **No hazard evaluation.** "Answers" measures compliance, not harm. The FAQ's safety answer covers
  trading losses, the law and licences. It does not cover dangerous-content risk or say what the
  removal methods change beyond refusal.
- **Internal inconsistency.** The "Q4" claim does not hold for every card.
- **Legal and licence caveats.** These are left to the user ("within the law and each model's
  licence"). Whether every derivative's licence permits redistribution is not addressed.
- **Deliberately left out.** Run commands, download links, hardware-matching instructions and the
  "How do I start in 2 minutes?" section are not reproduced. Only a handful of model names are given
  as examples.

## Affected pages

- [[Defensive Deception for Open Models]]
- [[Open Model Ecosystems]]
- [[Qwen]]

## Raw capture

- [[knowledge-base/raw/sources/Every free uncensored AI model on the internet (103)]]

## Citations

- Canonical URL: https://uncensored-ai-free.pages.dev/ (newsletter `utm_*` and `_bhlid` parameters
  removed).
- No byline and no published date in the capture; the source ID uses the capture date. Captured
  2026-11-24. Publisher: the catalog site itself, reached through a newsletter link whose tracking
  parameters name theaivalley.com.

## Related pages

- [[Defensive Deception for Open Models]]
- [[Open Model Ecosystems]]
- [[Qwen]]
- [[Mark Russinovich - Fool's Gold]]
- [[Modaic - Latency Doesn't Lie - Jev Is (Probably) Qwen3.5-35B-A3B]]
- [[Agent Security and Governance]]
- [[Emergent Misalignment]]
- [[Model Quantization and Efficiency]]
