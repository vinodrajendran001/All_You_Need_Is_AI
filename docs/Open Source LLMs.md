
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
5. Contex Length
	1. Standard (2K-4K)
	2. Medium (8K)
	3. Long (32K+)
6. Inference Optimization
	1. KV Caching
	2. Flash Attention
	3. Quantization Friendly design


## Attention Mechanism

### Standard Attention

$$ 
z = \frac{}{}  

$$