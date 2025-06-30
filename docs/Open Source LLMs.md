
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
	2. 
