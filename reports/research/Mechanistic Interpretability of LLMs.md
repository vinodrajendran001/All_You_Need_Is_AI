
# Mechanistic interpretability of LLMs

Mechanistic interpretability seeks to explain the internal workings of large language models (LLMs) by decomposing their computations into human‐understandable components such as neurons, circuits, and representations, and recent research has produced a wealth of methodologies to formalize, test, and apply such explanations (1.1)


## Introduction

Transformer‐based LLMs have achieved remarkable performance across diverse language tasks, yet their internal operations remain opaque despite extensive research efforts; mechanistic interpretability aims to render these operations transparent by reverse‐engineering models into discrete, interpretable components (1.1). Existing studies emphasize understanding internal computations at multiple granularities—from individual neurons that detect specific semantic features to entire subnetworks or “circuits” that orchestrate complex functions—and have developed rigorous methodologies to test hypotheses about these internal mechanisms (2.2). In addition to enhancing our scientific understanding, these mechanistic explanations are crucial for AI safety, debugging, alignment, and for devising interventions that can mitigate undesirable behaviors (3.1).

### Foundational Concepts in Mechanistic Interpretability

Mechanistic interpretability is grounded in the idea that LLMs learn to represent and process information through internal features that are at least partially decoupled and structured; early work in this domain introduced the concept of `features` (vectors in hidden representations associated with human‐interpretable properties) and “circuits” (subgraphs of interconnected neurons implementing specific functions) (1.1). Researchers have drawn analogies between dissecting neural networks and reverse engineering traditional computational systems, where each neuron is likened to a variable in a program and circuits represent algorithmic subroutines (4.1). Foundational surveys and theoretical frameworks have converged on the idea that the residual streams, multi‐head attention, and feed‐forward layers of transformers jointly contribute to emergent phenomena such as in‐context learning and language generation, and these are now being analyzed using methods from sparse autoencoders, causal mediation analysis, and activation patching (1.2, 2.3).

### Neuron‐Level Analysis and Sparse Feature Discovery 

A central line of research in mechanistic interpretability focuses on the identification and dissection of individual neurons or small groups of neurons to determine their role in language processing. Early studies revealed that neurons often exhibit polysemy—activating for multiple, sometimes unrelated, features—and that models represent several concepts in overlapping high‐dimensional superpositions rather than as isolated `monosemantic` units (1.3). Sparse autoencoder approaches have been developed to disentangle such overlapping features by forcing the model to represent distinct concepts using sparse activations, thereby yielding more interpretable and distinct neuron representations (5.1, 1.4). Recent work leveraging sparse probing methods has been successful in isolating neurons critical for functions such as factual recall or sentiment detection, offering a granular view of how language models encode linguistic and semantic information (2.4).

### Circuit Analysis and Causal Mediation Approaches 

Beyond the analysis of individual neurons, research has increasingly turned its attention to `circuits`— interconnected groups of neurons that jointly implement a computational subroutine such as negation, sequence continuation, or even complex tasks like arithmetic reasoning. Circuit analysis involves both localization techniques, such as knockout experiments and causal mediation analysis, and detailed visualization methods that help researchers map and interpret the flow of information through the network (1.4, 2.5). For instance, studies have identified specific attention head pairs, known as induction heads, that play a key role in in‐context learning by copying and predicting sequences, and circuit‐level interventions have shown that perturbing these components can lead to marked changes in model behavior (6.1, 7.1). Advanced methods such as weights-based circuit analysis with transcoders allow researchers to separate input-dependent from input-invariant features, thereby providing a more stable and interpretable basis for understanding the computations within MLP layers (5.2).


