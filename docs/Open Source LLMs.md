
## Architecture Commonalities

1. Pre-training objective: Next-token prediction
2. Transformers architecture: decoder-only transformer as their foundation
3. Tokenization: Subword tokenization methods like BPE, sentence-piece, word-piece
4. Self-attention mechanism: Core component of transformer architecture to allow models to weigh importance of different input tokens
5. Layer Normalization: Stabilize training
6. Fully-Feed forward network: Interleaved with attention layers in transformer blocks
7. Residual connections: facilitate gradient flow during training
8. Training pipeline: two stage approach: pretraining on large corpora followed by instruction tuning

## Key Differentiators

1. Attention Mechanism
	1. Standard Attention
	2. Grouped-Query Attention (GQA)
	3. Multi-Query Attention (MQA)
	4. Sliding Window Attention (SWA)
2. Positional Encoding
	1. Rotational Positional Encoding (RoPE)
	2. Attention with Linear Biases (ALiBi)
	3. Absolution Positional Encoding
3. Parameter Efficiency
	1. Dense Models
	2. Mixture-of-Experts
4. Activation Function
	1. SwiGLU
	2. GeGLU
	3. ReLU variants
5. Context Length
	1. Standard (2K-4K)
	2. Medium (8K)
	3. Long (32K+)
6. Inference Optimization
	1. KV Caching
	2. Flash Attention
	3. Quantization Friendly design


## Attention Mechanism

In self-attention:

- Query (Q): What the current token is "looking for"
- Key (K): What each token "advertises" or "offer" about itself
- Value (V): The actual information content each token contributes

Standard Self-Attention Calculation

$$ 
z = softmax\bigg(\frac{qk^{T}}{\sqrt{d_{k}}}\bigg)v 
$$


```
Token embeddings:
"The"    : E1
"dog"    : E2 
"chases" : E3
"the"    : E4

1. Generate Q, K, V for each position:
   Q1, K1, V1 = E1 × WQ, E1 × WK, E1 × WV  # for "The"
   Q2, K2, V2 = E2 × WQ, E2 × WK, E2 × WV  # for "dog"
   Q3, K3, V3 = E3 × WQ, E3 × WK, E3 × WV  # for "chases"
   Q4, K4, V4 = E4 × WQ, E4 × WK, E4 × WV  # for "the"

2. For next token prediction, use Q4 (query from "the"):
   
   Attention scores from position 4:
   - Score between "the" and "The": Q4 · K1 = 0.7
   - Score between "the" and "dog": Q4 · K2 = 0.5
   - Score between "the" and "chases": Q4 · K3 = 0.3
   - Score between "the" and "the": Q4 · K4 = 0.9
   
   After softmax:
   Attention weights = [0.2, 0.15, 0.1, 0.55]
   
   Weighted sum:
   Context vector = 0.2×V1 + 0.15×V2 + 0.1×V3 + 0.55×V4
   
3. This context vector (after feed-forward processing) informs 
   the prediction of the next token, likely "cat"
```


#### Causal Attention Mask 

In autoregressive models like GPT, we use a causal mask to ensure tokens can only attend to themselves and previous tokens (not future ones):

```
Attention Mask:
[1, 0, 0, 0]  # "The" can only see itself
[1, 1, 0, 0]  # "dog" can see "The" and itself
[1, 1, 1, 0]  # "chases" can see "The", "dog", and itself
[1, 1, 1, 1]  # "the" can see all previous tokens and itself
```

### Cross Attention

- Queries (Q): Come from the decoder's current sequence
- Keys (K) and Values (V): Come from the encoder's processed input sequence

```
ENCODER SIDE                         DECODER SIDE
(English Input)                      (Spanish Output)

  "The"    → H1                         "El" → Z1
  "black"  → H2                        "gato" → Z2
  "cat"    → H3                        "negro" → Z3
  "sleeps" → H4                        ...
  "on"     → H5
  "the"    → H6
  "mat"    → H7
            |                            |
            |                            |
            v                            v
        Keys & Values                  Queries
            |                            |
            |                            |
            +------------+---------------+
                         |
                         v
                    Cross-Attention
                         |
                         v
              Contextual information
              from input sequence
                         |
                         v
                  Output prediction
```

In models like CLIP, DALL-E, and LLaVA, cross-attention plays a crucial role in connecting different modalities:

```
IMAGE ENCODER                      TEXT DECODER
(Visual features)                 (Text generation)

  Image patch 1 → V1                 Text token 1 → T1
  Image patch 2 → V2                 Text token 2 → T2
  Image patch 3 → V3                 Text token 3 → T3
  ...                                ...
            |                            |
            |                            |
            v                            v
        Keys & Values                  Queries
            |                            |
            |                            |
            +------------+---------------+
                         |
                         v
                    Cross-Attention
                         |
                         v
              Text referring to visual
                    elements

```

### Multi-Head Attention (MHA)

- Each head has its own query (Q), key (K), and value (V) projection matrices
- Each head produces its own attention output
- These outputs are concatenated and projected to produce the final output

In a model with 32 attention heads, MHA uses:

- 32 different Q projection matrices
- 32 different K projection matrices
- 32 different V projection matrices

### Multi-Query Attention (MQA)

Multi-Query Attention (MQA) maintains multiple query heads but uses a **single shared key and value head**:

- Multiple different Q projection matrices (e.g., 32 of them)
- Just ONE K projection matrix
- Just ONE V projection matrix

### Grouped-Query 