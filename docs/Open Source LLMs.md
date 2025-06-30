
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
	3. Absolute Positional Encoding
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


In a text generation scenario with MQA:

1. When processing "The cat sat on the":
    - We compute one key and one value vector per token
    - We compute multiple query vectors for each token
2. For the next token prediction:
    - Multiple query vectors from the last token ("the") each focus on different aspects
    - But all query heads use the same set of key and value vectors
3. During KV caching:
    - We only store ONE key and ONE value per token
    - This drastically reduces memory requirements

### Grouped-Query Attention (GQA)

GQA finds a middle ground between MHA and MQA by creating groups of query heads that share key and value projections:

- Multiple Q projection matrices (e.g., 32 of them)
- Multiple K projection matrices (e.g., 8 of them)
- Multiple V projection matrices (e.g., 8 of them)
- Each K/V projection is shared among a group of Q projections

In a text generation scenario with GQA:

1. When processing "The cat sat on the":
    - We compute 8 different key vectors and 8 different value vectors per token
    - We compute 32 query vectors (8 groups with 4 queries each)
2. For next token prediction:
    - Queries in the same group attend to the same key and value projections
    - Different groups attend to different key and value projections
    - This preserves some diversity while reducing memory requirements
3. During KV caching:
    - We store 8 keys and 8 values per token (instead of 32)
    - This gives a 4x memory reduction compared to MHA

### Sliding Window Attention (SWA)

Sliding Window Attention (SWA) limits each token to attend only to a fixed window of surrounding tokens, rather than the entire sequence:

- Each token attends only to tokens within a fixed window (e.g., 4096 tokens)
- Tokens outside this window are ignored
- This creates a "sliding window" of attention as we move through the sequence

In a long document analysis with SWA:

1. When processing a 10,000-token document with window size 4096:
    
    - For token at position 5000, attention is limited to tokens 903-5000
    - For token at position 9000, attention is limited to tokens 4904-9000
2. Next token prediction with window size 4096:
    
    - The last token only attends to the previous 4095 tokens
    - Older information isn't directly accessible but can still influence prediction through cascading attention layers
3. During KV caching:
    
    - We only need to store the most recent window of keys and values
    - This allows processing sequences longer than model's training length


## Positional Encoding


### Absolute Positional Encoding

Absolute positional encoding assigns a unique vector to each position in a sequence. This vector is added to the token embedding before it enters the transformer layers.

In the original transformer paper, sinusoidal functions with different frequencies create these position vectors:

```
PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

```
Position: 0       1      2     3    4     5
          ↓       ↓      ↓     ↓    ↓     ↓
Tokens:   "The"  "cat"  "sat"  "on" "the" "mat"
          +      +      +      +    +     +
PE:       PE₀    PE₁    PE₂    PE₃  PE₄   PE₅
          ↓      ↓      ↓      ↓    ↓     ↓
Result:   "The"  "cat"  "sat"  "on" "the" "mat"
          +pos0  +pos1  +pos2  +pos3 +pos4 +pos5
```

#### Limitations

- Limited to a fixed maximum sequence length
- Position 1000 has a completely different encoding than position 999 with no notion of them being close
- Struggles to generalize to positions beyond training length


### Rotatory Position Embeddings (RoPE)

RoPE encodes position by rotating token vectors in a high-dimensional space. The rotation angle is proportional to the position and varies across dimensions.

Unlike absolute encodings that add position information, RoPE applies a position-dependent rotation to query and key vectors:

1. Split embedding dimensions into pairs (dim0, dim1), (dim2, dim3), etc.
2. For each pair, apply a 2D rotation where the angle depends on:
    - The token's position in the sequence
    - The dimension pair (different dimension pairs rotate at different rates)

For a token at position m, the rotation for dimension pair j is:
```
θⱼ(m) = m × base^(-2j/d)
```

Where `base` is typically 10000, similar to absolute positional encoding.

For the word "cat" at position 2:
```
Original embedding dimensions: [0.5, 0.8, 0.3, 0.2, ...]

After RoPE (with simplified numbers):
- Dimensions 0-1: Rotate by 2θ₀ = 2 radians
  [0.5, 0.8] → [-0.8, 0.5]
  
- Dimensions 2-3: Rotate by 2θ₁ = 0.2 radians
  [0.3, 0.2] → [0.27, 0.24]
  
- And so on for other dimension pairs
```

The key insight is that these rotations create a specific pattern when computing attention:
```
When comparing positions m and n in attention:
Dot product becomes influenced by (m-n)
```

#### Practical Impact

RoPE enables the model to understand relative positions naturally:

1. For self-attention:
    - The dot product between query and key naturally encodes their relative distance
    - Tokens at similar relative distances have similar attention patterns
2. For token "cat" at position 2 attending to other tokens:
    - Its attention to position 0 ("The") is influenced by relative distance 2
    - Its attention to position 1 ("sat") is influenced by relative distance 1
    - The attention mechanism inherently understands these distances

#### Key Advantages

- Seamlessly encodes relative positions in the attention mechanism
- Better generalization to unseen sequence lengths
- Can be extended to longer contexts through frequency scaling
### Attention with Linear Biases (ALiBi)

ALiBi takes a completely different approach: instead of modifying token representations, it directly adds a position-dependent penalty to attention scores based on distance between tokens.

#### How It Works

1. Compute standard attention scores between query and key vectors
2. Apply a distance-based penalty that grows linearly with the distance between tokens
3. Different attention heads get different penalty slopes

```
Attention_Score(i, j) = (Qᵢ · Kⱼ) - m × |i-j|
```

Where:
- `i` is the query position
- `j` is the key position
- `m` is a head-specific negative slope

For a sentence "The cat sat":

```
Token "cat" (position 1) computing attention:

Standard attention scores (without positional information):
"The" (pos 0): 0.8
"cat" (pos 1): 1.0
"sat" (pos 2): 0.7

With ALiBi (assuming m = 0.2):
"The" (pos 0): 0.8 - 0.2×|1-0| = 0.8 - 0.2 = 0.6
"cat" (pos 1): 1.0 - 0.2×|1-1| = 1.0 - 0 = 1.0
"sat" (pos 2): 0.7 - 0.2×|1-2| = 0.7 - 0.2 = 0.5

After softmax, "cat" pays more attention to itself, less to distant tokens
```

Each attention head gets a different slope:
```
Head 1: m₁ = 2⁻⁸
Head 2: m₂ = 2⁻⁷
...
Head h: mₕ = 2⁻⁸⁽ʰ⁻¹⁾ʰ
```

This allows different heads to focus on different distance ranges.



