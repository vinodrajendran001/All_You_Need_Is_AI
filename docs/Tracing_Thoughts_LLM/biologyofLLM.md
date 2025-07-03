---
footer: Vinod
theme: aumovio
title: Tracing the Thoughts of LLMs
paginate: true
size: 16:9
marp: true
---



<!-- _class: title -->
<!-- _class: summary-->

![bg opacity:.3](images/title_bg.png)
# Tracing the thoughts of an LLM





**Vinod**
*Generative AI Expert*

---
<!-- _class: summary-->

## How does a Large Language Model produce one token?



---
<!-- _class: picture-->

![LLM working](images/llm_one_token.png)

---
<!-- _class: picture-->

![LLM Intrep](images/llm_intrep.png)

---
<!-- _class: two-columns-centered -->
## Language model neurons are polysemantic

![bg right fit](images/polysemantic.png)

---


<!--_class: two-columns-centered-->

## But combination of neurons can be interpretable


![bg1](images/llm_feature.png)

![bg1](images/llm_feature_2neurons.png)

---

<!-- _class: two-columns-centered -->

## Feature : Golden Gate Bridge

![bg right fit](images/golden_gate_bridge.png)

---
<!-- _class: picture-->

![gg_bridge example](images/gg_lingual_modal.png)

---
<!-- _class: two-columns-centered -->
## Influence on Behavior

![bg right fit](images/inf_behavior.png)


---
<!-- _class: picture-->

![influence example](images/influence_example.png)

---
<!-- _class: picture-->

![](images/gg_nn.png)

---
<!-- _class: normal-slide -->
### Abstract Features
- Sycophantic phrase
- Secrecy
- Code error
- Bias
- Deception
- Power-seeking
- Criminal
- ...  

![bg right fit](images/abstract.png)

---
<!-- _class: picture-->

![trump](images/DonaldTrump.png)



---
<!-- _class: picture-->
# LLM: What’s Misunderstood vs. What’s True
![bg opacity:.6](images/mis_bg.png)

---

<!-- _class: two-columns-centered -->

## Misconception #1: LLM Simply Predicts the Next Word

![bg right fit](images/mis1_begining.png)


---
<!-- _class: picture-->

![mis1](images/mis1.png)

---
<!-- _class: two-columns-centered -->

## Reality: LLMs Plans Ahead 

![bg left fit](images/mis1_ending.png)

---


<!-- _class: two-columns-centered -->

## Misconception #2: LLM Processes Different Languages Separately


![bg right fit](images/mis2_begining.png)



---

<!-- _class: picture-->

![mis2](images/mis2.png)

---

<!-- _class: two-columns-centered -->

## Reality: LLMs Uses Universal Concepts


![bg left fit](images/mis2_ending.png)


---

<!-- _class: two-columns-centered -->

## Misconception #3: LLM Reasoning Matches its Explanations

![bg right fit](images/mis3_begining.png)

---

<!-- _class: picture-->

![mis3_1](images/mis3_1.png)


---
<!-- _class: picture-->

![mis3 fit](images/mis3.png)

---
<!-- _class: two-columns-centered -->

## Reality: LLMs Internal Process Differs from its Explanations 

![bg left fit](images/mis3_ending.png)

---

<!-- _class: two-columns-centered -->

## Misconception #4: LLMs Just Memorize Answers

![bg right fit](images/mis4_begining.png)

---
<!-- _class: picture-->

![mis4](images/mis4.png)

---

<!-- _class: two-columns-centered -->

## Reality: LLMs Uses Multi-Step Reasoning

![bg left fit](images/mis4_ending.png)

---

<!-- _class: two-columns-centered -->

## Misconception #5: Hallucinations and Jailbreaks are Random Failures

![bg right fit](images/mis5_begining.png)

---
<!-- _class: picture-->

![mis5_1](images/mis5_1.png)

---
<!-- _class: picture-->

![mis5_2](images/mis5_2.png)

---

<!-- _class: two-columns-centered -->

## Reality: They’re the Result of Specific, Understandable Mechanisms

![bg left fit](images/mis5_ending.png)

---
### How Researchers Proved These Findings

- **Attribution Graphs** : Mapping computational pathways in Claude’s reasoning processes by grouping related neural features into interpretable steps.

- **Intervention Experiments**:  Measuring output changes when specific features were inhibited or activated.

- **Cross-layer Transcoders**: Decomposing neural activity into sparse features to link concepts across model layers.


Read the full paper: https://transformer-circuits.pub/2025/attribution-graphs/biology.html

---
# Final Thought

- Interpretable features in LLMs are **highly abstract** and capable of **influencing large models**.

- LLMs can **plan ahead**, **navigate meaning across languages**, and sometimes **generate explanations that diverge from their actual reasoning**.

- Understanding LLM is **foundational for safety, trust, and impactful applications**.



---

<!-- _class: quote-->

![bg opacity:.6](images/hinton.png)


> People understand very little about how LLMs actually work, so they still think LLMs are very different from us. But actually, it's very important for people to understand that they're very like us.

---
## References

1. [Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html)
2. [Mapping the Mind of a Large Language Model \ Anthropic](https://www.anthropic.com/research/mapping-mind-language-model)
3. [Tracing the thoughts of a LLM](https://www.anthropic.com/news/tracing-thoughts-language-model)
4. [Mechanistic Interpretability: A Look Inside an AI's Mind + The Latest AI Research from Anthropic](https://www.youtube.com/watch?v=Y5l6VD9s4Lw)
5. [Mechanistic Interpretability explained | Chris Olah and Lex Fridman](https://www.youtube.com/watch?v=riniamTdUSo)
6. [Inside the Mind of Claude: How Large Language Models Actually "Think"](https://blog.typingmind.com/ai-misconceptions/)
