---
type: raw-source
source_id: src-2026-08-18-alireza-diri-aiml-interviews-feature-engineering
title: AIML Interviews - Feature Engineering
author: Alireza Diri
url: https://github.com/alirezadir/AIMLInterviews/blob/main/src/MLSD/mlsd-feature-eng.md
captured: 2026-08-18
status: immutable
tags:
  - source/raw
  - interview-prep
  - machine-learning
  - system-design
---

> Preserve the source body below this line as the canonical capture.
## Feature preprocessing

## Text preprocessing

normalization -> tokenization -> token to ids

## Text encoders:

Text -> Vector (Embeddings) Two approaches:

- Statistical
	- BoW: converts documents into word frequency vectors, ignoring word order and grammar
		- TF-IDF: evaluates the importance of a word (term) in a document relative to a collection of documents. It is calculated as the product of two components:
		- Term Frequency (TF): This component measures how frequently a term occurs in a specific document and is calculated as the ratio of the number of times a term appears in a document (denoted as "term\_count") to the total number of terms in that document (denoted as "total\_terms"). The formula for TF is:
			TF(t, d) = \\frac{\\text{term\_count}}{\\text{total\_terms}}
				- Inverse Document Frequency (IDF): This component measures the rarity of a term across the entire collection of documents and is calculated as the logarithm of the ratio of the total number of documents in the collection (denoted as "total\_documents") to the number of documents containing the term (denoted as "document\_frequency"). The formula for IDF is:
			IDF(t) = \\log\\left(\\frac{\\text{total\_documents}}{\\text{document\_frequency}}\\right)
		The final TF-IDF score for a term "t" in a document "d" is obtained by multiplying the TF and IDF components: TF-IDF(t,d)=TF(t,d)×IDF(t)
- ML encoders
	- Embedding (look up) layer: a trainable layer that converts categorical inputs, such as words or IDs, into continuous-valued vectors, allowing the network to learn meaningful representations of these inputs during training.
		- Word2Vec: based on shallow neural networks and consists of two main approaches: Continuous Bag of Words (CBOW) and Skip-gram.
		- CBOW (Continuous Bag of Words):
			In CBOW, the model predicts a target word based on the context words (words that surround it) within a fixed window. It learns to generate the target word by taking the average of the embeddings of the context words. CBOW is computationally efficient and works well for smaller datasets.
				- Skip-gram:
			In Skip-gram, the model predicts the context words (surrounding words) given a target word. It learns to capture the relationships between the target word and its context words. Skip-gram is particularly effective for capturing fine-grained semantic relationships and works well with large datasets.
		Both CBOW and Skip-gram use shallow neural networks to learn word embeddings. The resulting word vectors are dense and continuous, making them suitable for various NLP tasks, such as sentiment analysis, language modeling, and text classification.
		- transformer based e.g. BERT: consider context, different embeddings for same words in different context

## Video preprocessing

Frame-level: Decode frames -> sample frames -> resize -> scale, normalize, color correction

### Video encoders:

- Video-level
- Frame-level (from sampled frames and aggregate frame embeddings)
	- less expensive (training and serving speed, compute power)
		- Example: ViT (Vision Transformer)
		- by dividing images into non-overlapping patches and processing them through a self-attention mechanism, enabling it to analyze image content; it differs from the original Transformer, which was initially designed for sequential data, like text, and relied on 1D positional encodings.