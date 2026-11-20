---
title: "LiquidCodec: High-Fidelity Audio Tokenization Optimized for Speed"
source: "https://www.liquid.ai/blog/liquidcodec?utm_source=tldrai"
author:
  - "[[Liquid AI]]"
published: 2026-11-12
created: 2026-11-20
description: "LiquidCodec is the ~74M-parameter audio codec behind LFM3-Audio and LFM3-Omni: high-fidelity reconstruction, easy-to-predict tokens, fast on-device decoding."
tags:
  - "clippings"
---
At the end of October, we released [LFM3-Audio-2B](https://huggingface.co/LiquidAI/LFM3-Audio-2B) and [LFM3-Omni-2B](https://huggingface.co/LiquidAI/LFM3-Omni-2B), our most powerful models to date for multimodal on-device intelligence. Essential to their performance is a new in-house streaming audio codec, [LiquidCodec](https://huggingface.co/LiquidAI/Liquid-Codec). An audio codec turns speech into tokens that language models can predict, and it converts those tokens back into audio. A codec’s quality is measured by the fidelity of its reconstruction. High fidelity means that when you convert a recording into tokens and back into audio, the result sounds nearly identical to the original.

We built LiquidCodec on the [LFM3 architecture](https://www.liquid.ai/blog/lfm3) \[1\] around two practical constraints: the audio tokens must be easy for our models to predict, and converting them back into speech must be extremely fast. The ~74M-parameter codec matches similarly sized models in both the quality of the audio it reconstructs and how much it can compress speech, while outperforming them in speech generation and token-to-waveform decoding speed. LiquidCodec combines traditional spectral processing with an exactly symmetric encoder and decoder in a compact architecture built to run on-device.

## Why we built our own audio codec

An audio codec has two components: a *tokenizer*, which translates audio waveforms into discrete tokens suitable for language-model processing and prediction, and a *detokenizer*, which translates these predicted tokens back into audio.

In Liquid AI’s first audio model, [LFM2-Audio-1.5B](https://huggingface.co/LiquidAI/LFM2-Audio-1.5B), we used the popular codec Mimi \[2\], which benefits from high compression (1.1 kbps bitrate) and a low parameter count (~96M). However, we wanted to push speech quality further and wanted a codec optimized for speed and low-precision inference. Therefore, we replaced only the detokenizer in its successor, [LFM2.5-Audio-1.5B](https://www.liquid.ai/blog/introducing-lfm2-5-the-next-generation-of-on-device-ai), and achieved 8× faster detokenization.

However, retaining the third-party tokenizer limited us by both the quality of its audio tokens and its underlying architectural decisions. In particular, the traditional quantization method used by Mimi, residual vector quantization (RVQ) \[3,4\], has since been challenged by newer approaches such as finite scalar quantization (FSQ) \[5\]. These minimize sequential dependencies between codebooks and enable more flexible, parallel prediction of audio tokens. That’s why, for our newest generation of audio models, we built our own codec to control both audio-token quality and how easily our models can predict them.

## Architecture

At its core, LiquidCodec follows the standard encode → quantize → decode pipeline: audio is first encoded into feature vectors, which a quantizer turns into tokens, and the tokens are then decoded back into audio.

Figure 1: LiquidCodec reconstruction (encode → quantize → decode) pipeline.

We designed LiquidCodec to focus on the two things we care most about: suitability for downstream audio generation models as well as encoding and decoding speed. Because we already had a heavily optimized detokenizer from LFM2.5-Audio-1.5B, we decided to keep its overall design, using blocks from the LFM3 architecture in both the encoder and decoder.

Instead, we focused on the tokenizer, which has a large impact on audio model training, as its produced tokens provide the learning supervision required for speech generation. To preserve the efficiency of our previous audio models, we kept the same frame rate of 12.5 Hz (yielding one frame every 80 ms). We also decided to model 24 kHz waveforms to strike a balance between high-fidelity reconstruction and computational efficiency. However, there were a number of other important decisions to be made.

The most important decision was the quantization algorithm. It decides how continuous feature vectors produced by the audio encoder are turned into tokens for language model prediction. Mimi, the tokenizer in LFM2.5-Audio-1.5B, uses RVQ. In RVQ, audio features are quantized using a sequence of *codebooks* (learned sets of representative vectors), where each codebook selects a vector that approximates the residual error left by the preceding codebooks. The selected vectors are then summed to reconstruct the original feature. Mimi supports up to 32 codebooks, and using eight gives a *bitrate* of 1.1 kbps.

Figure 2: Residual vector quantization (RVQ)

In contrast, FSQ independently rounds each dimension of a feature vector to one of a fixed number of values. It can be extended to grouped FSQ (GFSQ) \[6\], which splits features into independently quantized groups. Each group produces a token from a codebook defined by all possible combinations of those values, and the resulting quantized vectors are concatenated to reconstruct the feature.

Figure 3: Grouped finite scalar quantization (GFSQ)

The advantage of GFSQ is that it does not naturally introduce the same level of sequential dependencies between codebooks as in RVQ, where each codebook strongly influences its successor. This means that GFSQ allows parallel prediction: previous work has used MaskGIT-based transformer methods to iteratively predict multiple codebooks in parallel, which we adopt \[7,8\].

We also decided to make our encoder and decoder symmetric and the encoder fully causal. This not only simplifies the design but also optimizes our tokenizer to be just as lightweight and efficient as our detokenizer, making LiquidCodec particularly well suited for real-time, low-latency audio streaming.

Figure 4: Architecture of symmetric tokenizer and detokenizer.

LiquidCodec’s speed comes from a combination of its LFM3 architecture explicitly optimized for performance on the edge and its modeling choices. In particular, the decision to directly predict spectral coefficients allows us to avoid costly operations in similar codecs, such as progressive upsampling with learned transposed convolutions during decoding.

## How we trained LiquidCodec

As the LFM family focuses on multilingual capabilities, we put LiquidCodec through two stages of multilingual training: In the first stage, we expose the codec to a large amount of potentially noisy data, and in the second stage we fine-tune only on high-fidelity waveforms to ensure the highest possible reconstruction quality.

For the **first stage**, we collected 264,000 hours across 107 languages, combining web speech with audiobooks, crowd-sourced recordings, and smaller parliamentary and meeting collections. We pre-trained LiquidCodec using waveform and spectral losses to compare the reconstruction directly with the original. Importantly, in this first phase, we omitted the usual adversarial (GAN) losses used in codec training, focusing on learning robust audio representations before refining perceptual quality in the second stage.

This taught the model to restore the signal, but we still noticed that our reconstruction-only pretraining could leave “metallic” artifacts. We hypothesized that waveform and spectral losses alone were insufficient to capture the finer perceptual details of natural speech, leading to a sort of “averaging out” that produced this artifact.

In the **second stage**, we directly addressed this by narrowing the training pool to 55,000 hours of cleaner, full-band speech (all sources were natively sampled at 24 kHz or above), still covering multiple languages. We fine-tuned the model with adversarial critics that examine waveform patterns, spectral detail, and speech features. We noticed the artifacts we observed after pretraining gradually disappeared, leaving clean reconstructions of the underlying waveform.

Additionally, to improve LiquidCodec’s robustness to quantization for edge inference, we ran decoder-only fine-tuning via quantization-aware training (QAT) \[11\].

## Audio reconstruction and speech generation

A common way to evaluate a codec’s performance is by measuring the fidelity of its reconstruction. In this setting, an audio recording is encoded into discrete tokens and then decoded back into speech, with the reconstructed audio compared against the original.

Original from "Ramin Hasani: Meet the AI system inspired by the human brain."

<audio src="https://aypchzzf9pftwuto.public.blob.vercel-storage.com/original_24khz_trimmed-wWXHLVdWMsIsf3j7O2qk5wKtMB7M32.wav"></audio>

Reconstructed with LiquidCodec from “Ramin Hasani: Meet the AI system inspired by the human brain”.

<audio src="https://aypchzzf9pftwuto.public.blob.vercel-storage.com/reconstruction_liquidcodec_bf16_trimmed-lXZhbyEGYtDE7AOTirXogWtI81Yx4z.wav"></audio>

The more important question, however, is whether our codec produces tokens that a basic speech model can easily predict. During reconstruction, the detokenizer receives tokens from its own tokenizer. During text-to-speech (TTS) training, it receives predictions from a language model. Tokens that are good for reconstruction may still be difficult for the speech generation model to learn, and we wanted to ensure that the token space of our codec was robust enough for language modeling.

To compare audio codecs fairly, we fixed the training data (101,000 hours across six languages), TTS architecture, and training compute budget. We initialized each model’s backbone from pretrained [LFM3-1.7B](https://huggingface.co/LiquidAI/LFM3-1.7B) and added a six-layer, 1,024-dim autoregressive depth decoder to predict the codebooks within each audio frame. We trained the TTS models with identical batches in identical order. Only the token-specific embeddings and output heads changed to fit each tokenizer. At evaluation, each model received text without a reference speech prompt, and we used three generation seeds.

## Results

For evaluation, we picked LibriSpeech test-clean, one of the most common benchmarks for codec reconstruction, added Seed-TTS English and Mandarin, and extended the coverage with FLEURS in German, French, Mandarin, Japanese, and Korean, matching the languages we train TTS on.

### Reconstruction and speech generation

In addition to being much more computationally efficient than its competitors, LiquidCodec matches their reconstruction quality. It achieves the best perceived audio quality measured by ViSQOL and the lowest mel distance on all eight test sets while remaining competitive on the other metrics. Decoder-only QAT can also reduce its decoder footprint by a factor of 3.5 in Q4\_0 with minimal impact on audio reconstruction quality. Even quantized, LiquidCodec keeps its ViSQOL and mel-distance lead over the external codecs.

For zero-shot multilingual TTS, models trained on LiquidCodec tokens reach the highest naturalness score (UTMOSv2) on all eight test sets and the best intelligibility (WER/CER) on four out of the eight datasets. Notably, these findings are not LFM backbone-specific. Repeating the TTS experiment with a Qwen3-1.7B \[12\] backbone gives consistent results.

<table><tbody><tr><td rowspan="2"><p><strong>Test Set</strong></p></td><td rowspan="2"><p><strong>Codec</strong></p></td><td colspan="6"><p><strong>Reconstruction</strong></p></td><td colspan="2"><p><strong>TTS</strong></p></td></tr><tr><td><p><strong>SQMOS ↑</strong></p></td><td><p><strong>PESQ</strong></p><p><strong>(WB) ↑</strong></p></td><td><p><strong>Mel</strong></p><p><strong>Dist. ↓</strong></p></td><td><p><strong>SECS</strong></p><p><strong>(ECAPA2) ↑</strong></p></td><td><p><strong>ViSQOL</strong></p><p><strong>↑</strong></p></td><td><p><strong>CER</strong></p><p><strong>(%) ↓</strong></p></td><td><p><strong>WER/CER</strong></p><p><strong>(%) ↓</strong></p></td><td><p><strong>UTMOSv2</strong></p><p><strong>↑</strong></p></td></tr><tr><td rowspan="5"><p>LibriSpeech test-clean (English)</p></td><td><p>LiquidCodec BF16</p></td><td><p>4.442</p></td><td><p>2.640</p></td><td><p><strong>0.120</strong></p></td><td><p>0.785</p></td><td><p><strong>4.319</strong></p></td><td><p>0.89</p></td><td><p><strong>3.15</strong></p></td><td><p><strong>3.31</strong></p></td></tr><tr><td><p>LiquidCodec Q4_0</p></td><td><p>4.445</p></td><td><p>2.577</p></td><td><p>0.121</p></td><td><p>0.781</p></td><td><p>4.292</p></td><td><p>0.89</p></td><td><p>3.18</p></td><td><p>3.22</p></td></tr><tr><td><p>X-Codec 2</p></td><td><p>4.436</p></td><td><p>2.434</p></td><td><p>0.123</p></td><td><p>0.754</p></td><td><p>4.119</p></td><td><p>0.88</p></td><td><p>4.19</p></td><td><p>3.27</p></td></tr><tr><td><p>NanoCodec</p></td><td><p><strong>4.486</strong></p></td><td><p><strong>2.942</strong></p></td><td><p>0.122</p></td><td><p><strong>0.836</strong></p></td><td><p>4.219</p></td><td><p><strong>0.76</strong></p></td><td><p>3.32</p></td><td><p>3.19</p></td></tr><tr><td><p>Mimi (12 codebooks)</p></td><td><p>4.364</p></td><td><p>2.615</p></td><td><p>0.160</p></td><td><p>0.714</p></td><td><p>4.031</p></td><td><p>0.87</p></td><td><p>6.27</p></td><td><p>2.89</p></td></tr><tr><td rowspan="5"><p>Seed-TTS (English)</p></td><td><p>LiquidCodec BF16</p></td><td><p>4.463</p></td><td><p>2.326</p></td><td><p><strong>0.130</strong></p></td><td><p>0.751</p></td><td><p><strong>4.369</strong></p></td><td><p>0.86</p></td><td><p><strong>3.50</strong></p></td><td><p><strong>3.39</strong></p></td></tr><tr><td><p>LiquidCodec Q4_0</p></td><td><p>4.460</p></td><td><p>2.271</p></td><td><p>0.131</p></td><td><p>0.744</p></td><td><p>4.341</p></td><td><p>0.86</p></td><td><p>3.54</p></td><td><p>3.31</p></td></tr><tr><td><p>X-Codec 2</p></td><td><p>4.436</p></td><td><p>2.099</p></td><td><p>0.140</p></td><td><p>0.745</p></td><td><p>4.105</p></td><td><p>0.86</p></td><td><p>5.65</p></td><td><p>3.24</p></td></tr><tr><td><p>NanoCodec</p></td><td><p><strong>4.467</strong></p></td><td><p><strong>2.599</strong></p></td><td><p>0.136</p></td><td><p><strong>0.799</strong></p></td><td><p>4.304</p></td><td><p><strong>0.73</strong></p></td><td><p>3.95</p></td><td><p>3.29</p></td></tr><tr><td><p>Mimi (12 codebooks)</p></td><td><p>4.347</p></td><td><p>2.396</p></td><td><p>0.163</p></td><td><p>0.722</p></td><td><p>4.124</p></td><td><p>1.01</p></td><td><p>6.15</p></td><td><p>2.98</p></td></tr><tr><td rowspan="5"><p>Seed-TTS (Mandarin)</p></td><td><p>LiquidCodec BF16</p></td><td><p><strong>4.407</strong></p></td><td><p>2.429</p></td><td><p><strong>0.118</strong></p></td><td><p>0.776</p></td><td><p><strong>4.313</strong></p></td><td><p>6.93</p></td><td><p><strong>1.19</strong></p></td><td><p><strong>3.01</strong></p></td></tr><tr><td><p>LiquidCodec Q4_0</p></td><td><p>4.393</p></td><td><p>2.375</p></td><td><p>0.119</p></td><td><p>0.768</p></td><td><p>4.285</p></td><td><p>7.04</p></td><td><p>1.20</p></td><td><p>2.92</p></td></tr><tr><td><p>X-Codec 2</p></td><td><p>4.387</p></td><td><p>2.237</p></td><td><p>0.126</p></td><td><p><strong>0.823</strong></p></td><td><p>4.064</p></td><td><p>7.30</p></td><td><p>1.44</p></td><td><p>2.85</p></td></tr><tr><td><p>NanoCodec</p></td><td><p><strong>4.407</strong></p></td><td><p><strong>2.606</strong></p></td><td><p>0.122</p></td><td><p>0.811</p></td><td><p>4.189</p></td><td><p><strong>6.41</strong></p></td><td><p>1.27</p></td><td><p>2.88</p></td></tr><tr><td><p>Mimi (12 codebooks)</p></td><td><p>4.198</p></td><td><p>2.401</p></td><td><p>0.152</p></td><td><p>0.702</p></td><td><p>3.992</p></td><td><p>7.59</p></td><td><p>2.12</p></td><td><p>2.53</p></td></tr><tr><td rowspan="5"><p>FLEURS (German)</p></td><td><p>LiquidCodec BF16</p></td><td><p>4.237</p></td><td><p>2.434</p></td><td><p><strong>0.120</strong></p></td><td><p>0.807</p></td><td><p><strong>4.207</strong></p></td><td><p><strong>3.65</strong></p></td><td><p><strong>5.30</strong></p></td><td><p><strong>3.20</strong></p></td></tr><tr><td><p>LiquidCodec Q4_0</p></td><td><p>4.224</p></td><td><p>2.391</p></td><td><p>0.121</p></td><td><p>0.818</p></td><td><p>4.162</p></td><td><p>3.67</p></td><td><p>5.38</p></td><td><p>3.12</p></td></tr><tr><td><p>X-Codec 2</p></td><td><p><strong>4.256</strong></p></td><td><p>2.085</p></td><td><p>0.125</p></td><td><p>0.661</p></td><td><p>3.942</p></td><td><p>4.39</p></td><td><p>5.44</p></td><td><p>3.08</p></td></tr><tr><td><p>NanoCodec</p></td><td><p>4.202</p></td><td><p><strong>2.597</strong></p></td><td><p>0.129</p></td><td><p><strong>0.822</strong></p></td><td><p>4.009</p></td><td><p>3.74</p></td><td><p>5.36</p></td><td><p>3.01</p></td></tr><tr><td><p>Mimi (12 codebooks)</p></td><td><p>4.087</p></td><td><p>2.393</p></td><td><p>0.170</p></td><td><p>0.698</p></td><td><p>3.627</p></td><td><p>5.36</p></td><td><p>6.14</p></td><td><p>2.78</p></td></tr><tr><td rowspan="5"><p>FLEURS (French)</p></td><td><p>LiquidCodec BF16</p></td><td><p>4.301</p></td><td><p>2.315</p></td><td><p><strong>0.127</strong></p></td><td><p><strong>0.825</strong></p></td><td><p><strong>4.242</strong></p></td><td><p>5.27</p></td><td><p>6.91</p></td><td><p><strong>3.12</strong></p></td></tr><tr><td><p>LiquidCodec Q4_0</p></td><td><p>4.302</p></td><td><p>2.262</p></td><td><p>0.128</p></td><td><p>0.820</p></td><td><p>4.212</p></td><td><p>5.27</p></td><td><p><strong>5.26</strong></p></td><td><p>3.04</p></td></tr><tr><td><p>X-Codec 2</p></td><td><p><strong>4.317</strong></p></td><td><p>2.019</p></td><td><p>0.134</p></td><td><p>0.606</p></td><td><p>3.914</p></td><td><p>6.84</p></td><td><p>6.37</p></td><td><p>3.01</p></td></tr><tr><td><p>NanoCodec</p></td><td><p>4.305</p></td><td><p><strong>2.500</strong></p></td><td><p>0.137</p></td><td><p>0.824</p></td><td><p>4.072</p></td><td><p><strong>5.06</strong></p></td><td><p>7.72</p></td><td><p>3.02</p></td></tr><tr><td><p>Mimi (12 codebooks)</p></td><td><p>3.876</p></td><td><p>2.207</p></td><td><p>0.192</p></td><td><p>0.710</p></td><td><p>3.758</p></td><td><p>15.95</p></td><td><p>8.73</p></td><td><p>2.67</p></td></tr><tr><td rowspan="5"><p>FLEURS (Mandarin)</p></td><td><p>LiquidCodec BF16</p></td><td><p><strong>4.343</strong></p></td><td><p>2.479</p></td><td><p><strong>0.121</strong></p></td><td><p>0.794</p></td><td><p><strong>4.273</strong></p></td><td><p>7.60</p></td><td><p>8.82</p></td><td><p><strong>3.02</strong></p></td></tr><tr><td><p>LiquidCodec Q4_0</p></td><td><p>4.339</p></td><td><p>2.436</p></td><td><p>0.123</p></td><td><p>0.782</p></td><td><p>4.249</p></td><td><p>7.56</p></td><td><p>7.84</p></td><td><p>2.94</p></td></tr><tr><td><p>X-Codec 2</p></td><td><p>4.335</p></td><td><p>2.307</p></td><td><p>0.127</p></td><td><p>0.559</p></td><td><p>4.047</p></td><td><p>8.24</p></td><td><p>7.86</p></td><td><p>2.86</p></td></tr><tr><td><p>NanoCodec</p></td><td><p>4.334</p></td><td><p><strong>2.679</strong></p></td><td><p>0.133</p></td><td><p><strong>0.845</strong></p></td><td><p>4.164</p></td><td><p><strong>6.68</strong></p></td><td><p><strong>7.45</strong></p></td><td><p>2.91</p></td></tr><tr><td><p>Mimi (12 codebooks)</p></td><td><p>3.916</p></td><td><p>2.179</p></td><td><p>0.191</p></td><td><p>0.616</p></td><td><p>3.837</p></td><td><p>9.51</p></td><td><p>8.35</p></td><td><p>2.53</p></td></tr><tr><td rowspan="5"><p>FLEURS (Japanese)</p></td><td><p>LiquidCodec BF16</p></td><td><p>4.347</p></td><td><p>2.233</p></td><td><p><strong>0.122</strong></p></td><td><p><strong>0.766</strong></p></td><td><p><strong>4.162</strong></p></td><td><p>6.80</p></td><td><p>7.29</p></td><td><p><strong>3.05</strong></p></td></tr><tr><td><p>LiquidCodec Q4_0</p></td><td><p>4.327</p></td><td><p>2.188</p></td><td><p>0.123</p></td><td><p>0.756</p></td><td><p>4.120</p></td><td><p>6.83</p></td><td><p>7.32</p></td><td><p>2.98</p></td></tr><tr><td><p>X-Codec 2</p></td><td><p>4.354</p></td><td><p>2.045</p></td><td><p>0.130</p></td><td><p>0.497</p></td><td><p>3.805</p></td><td><p>7.02</p></td><td><p><strong>5.40</strong></p></td><td><p>2.94</p></td></tr><tr><td><p>NanoCodec</p></td><td><p><strong>4.378</strong></p></td><td><p><strong>2.415</strong></p></td><td><p>0.129</p></td><td><p>0.695</p></td><td><p>4.089</p></td><td><p><strong>6.02</strong></p></td><td><p>5.58</p></td><td><p>2.84</p></td></tr><tr><td><p>Mimi (12 codebooks)</p></td><td><p>4.332</p></td><td><p>2.232</p></td><td><p>0.166</p></td><td><p>0.658</p></td><td><p>3.982</p></td><td><p>12.13</p></td><td><p>6.27</p></td><td><p>2.49</p></td></tr><tr><td rowspan="5"><p>FLEURS (Korean)</p></td><td><p>LiquidCodec BF16</p></td><td><p><strong>4.217</strong></p></td><td><p><strong>2.637</strong></p></td><td><p><strong>0.117</strong></p></td><td><p><strong>0.803</strong></p></td><td><p><strong>4.176</strong></p></td><td><p>4.45</p></td><td><p>8.36</p></td><td><p><strong>2.97</strong></p></td></tr><tr><td><p>LiquidCodec Q4_0</p></td><td><p>4.214</p></td><td><p>2.599</p></td><td><p>0.118</p></td><td><p>0.800</p></td><td><p>4.146</p></td><td><p>4.30</p></td><td><p>6.71</p></td><td><p>2.88</p></td></tr><tr><td><p>X-Codec 2</p></td><td><p>4.214</p></td><td><p>2.299</p></td><td><p>0.128</p></td><td><p>0.591</p></td><td><p>3.870</p></td><td><p>5.08</p></td><td><p>6.22</p></td><td><p>2.87</p></td></tr><tr><td><p>NanoCodec</p></td><td><p>4.212</p></td><td><p>2.589</p></td><td><p>0.137</p></td><td><p>0.769</p></td><td><p>4.018</p></td><td><p><strong>3.41</strong></p></td><td><p><strong>5.96</strong></p></td><td><p>2.86</p></td></tr><tr><td><p>Mimi (12 codebooks)</p></td><td><p>3.843</p></td><td><p>2.165</p></td><td><p>0.178</p></td><td><p>0.543</p></td><td><p>3.530</p></td><td><p>9.37</p></td><td><p>9.81</p></td><td><p>2.54</p></td></tr></tbody></table>

Table: Reconstruction and zero-shot TTS results. Bold and underlined scores indicate the best and second-best results, respectively. TTS scores aggregate three generation trials.

### Speed

At FP32 precision with single-threaded CPU inference on a MacBook Pro with an Apple M4 Max, LiquidCodec encodes and decodes at approximately 361× and 87× real time, respectively, much faster than its competitors.

| Codec | Codebooks | Enc. RTF ↓ | Dec. RTF ↓ |
| --- | --- | --- | --- |
| LiquidCodec | 12 | 0.0028 ± 0.0001 | 0.0115 ± 0.0001 |
| [X-Codec 2](https://github.com/zhenye234/X-Codec-2.0) \[9\] | 1 | 0.7359 ± 0.0103 | 0.0379 ± 0.0009 |
| [NanoCodec](https://arxiv.org/abs/2508.05835) \[10\] | 13 | 0.2145 ± 0.0057 | 0.2543 ± 0.0061 |
| Mimi | 12 (truncated) | 0.0361 ± 0.0004 | 0.0329 ± 0.0005 |

Table 2: Encoding and decoding speed.

## Conclusion

LiquidCodec is a step toward making high-quality voice interaction a standard part of on-device AI. Faster speech generation with a smaller memory footprint makes it easier to build applications that can sustain a conversation while running locally.

Building the codec in-house also gives us control over a foundational part of our audio models. We can now evolve the speech representation alongside the models that use it. This opens up more possibilities for how future LFMs learn to generate and interact through speech.

LiquidCodec is available on [Hugging Face](https://huggingface.co/LiquidAI/Liquid-Codec) and loads directly with Transformers. To run it on-device, the [LFM3-Audio-2B](https://huggingface.co/LiquidAI/LFM3-Audio-2B-GGUF) and [LFM3-Omni-2B](https://huggingface.co/LiquidAI/LFM3-Omni-2B-GGUF) GGUFs include quantized Q4\_0, Q4\_K\_M, and Q8\_0 builds for llama.cpp.

## Acknowledgements

Research and development led by Anna Piunova and Calder Katyal, with development contributions by Ishwarya Ananthabhotla. Further contributions from Alexander Amini, Marc Härkönen, Tarek Dakhran, Samuel J. Broughton, Saniya Karwa, Farris Atif and Leonie Monigatti.

## Citation

Please cite this article as:

Liquid AI, "LiquidCodec: High-Fidelity Audio Tokenization Optimized for Speed", Liquid AI Blog, Nov 2026.

```
@article{liquidAI2026liquidcodec,
  author = {Liquid AI},
  title = {LiquidCodec: High-Fidelity Audio Tokenization Optimized for Speed},
  journal = {Liquid AI Blog},
  year = {2026},
  note = {www.liquid.ai/blog/liquidcodec},
}
```

## References

\[1\] Liquid AI (2026). Introducing LFM3: Every modality for specialized intelligence. Liquid AI Blog. [https://www.liquid.ai/blog/lfm3](https://www.liquid.ai/blog/lfm3)

\[2\] Défossez, A., Mazaré, L., Orsini, M., Royer, A., Pérez, P., Jégou, H., Grave, E., & Zeghidour, N. (2024). Moshi: A speech-text foundation model for real-time dialogue. arXiv preprint. [https://arxiv.org/abs/2410.00037](https://arxiv.org/abs/2410.00037)

\[3\] Juang, B.-H., & Gray, A. H. (1982). Multiple stage vector quantization for speech coding. ICASSP 1982. [https://doi.org/10.1109/ICASSP.1982.1171604](https://doi.org/10.1109/ICASSP.1982.1171604)

\[4\] Zeghidour, N., Luebs, A., Omran, A., Skoglund, J., & Tagliasacchi, M. (2022). SoundStream: An end-to-end neural audio codec. IEEE/ACM Transactions on Audio, Speech, and Language Processing, 30, 495–507. [https://arxiv.org/abs/2107.03312](https://arxiv.org/abs/2107.03312)

\[5\] Mentzer, F., Minnen, D., Agustsson, E., & Tschannen, M. (2024). Finite scalar quantization: VQ-VAE made simple. ICLR 2024. [https://arxiv.org/abs/2309.15505](https://arxiv.org/abs/2309.15505)

\[6\] Liao, S., Wang, Y., Li, T., Cheng, Y., Zhang, R., Zhou, R., & Xing, Y. (2024). Fish-Speech: Leveraging large language models for advanced multilingual text-to-speech synthesis. arXiv preprint. [https://arxiv.org/abs/2411.01156](https://arxiv.org/abs/2411.01156)

\[7\] Chang, H., Zhang, H., Jiang, L., Liu, C., & Freeman, W. T. (2022). MaskGIT: Masked generative image transformer. CVPR 2022. [https://arxiv.org/abs/2202.04200](https://arxiv.org/abs/2202.04200)

\[8\] Fejgin, R., Neekhara, P., Yang, X., Casanova, E., Langman, R., Kim, J., Ghosh, S., Hussain, S., & Li, J. (2025). Frame-stacked local transformers for efficient multi-codebook speech generation. arXiv preprint. [https://arxiv.org/abs/2509.19592](https://arxiv.org/abs/2509.19592)

\[9\] Ye, Z., Zhu, X., Chan, C.-M., Wang, X., Tan, X., Lei, J., Peng, Y., Liu, H., Jin, Y., Dai, Z., Lin, H., Chen, J., Du, X., Xue, L., Chen, Y., Li, Z., Xie, L., Kong, Q., Guo, Y., & Xue, W. (2025). Llasa: Scaling train-time and inference-time compute for Llama-based speech synthesis. arXiv preprint. [https://arxiv.org/abs/2502.04128](https://arxiv.org/abs/2502.04128)

\[10\] Casanova, E., Neekhara, P., Langman, R., Hussain, S., Ghosh, S., Yang, X., Jukić, A., Li, J., & Ginsburg, B. (2025). NanoCodec: Towards high-quality ultra fast speech LLM inference. Interspeech 2025. [https://arxiv.org/abs/2508.05835](https://arxiv.org/abs/2508.05835)

\[11\] Jacob, B., Kligys, S., Chen, B., Zhu, M., Tang, M., Howard, A., Adam, H., & Kalenichenko, D. (2018). Quantization and training of neural networks for efficient integer-arithmetic-only inference. CVPR 2018. [https://arxiv.org/abs/1712.05877](https://arxiv.org/abs/1712.05877)

\[12\] Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang, C., Lv, C., et al. (2025). Qwen3 technical report. arXiv preprint. [https://arxiv.org/abs/2505.09388](https://arxiv.org/abs/2505.09388)