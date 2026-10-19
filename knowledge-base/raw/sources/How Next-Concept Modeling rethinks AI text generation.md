
Researchers at Stanford University have introduced [Next-Concept Modeling](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=669a11ec0df5c83b&lid=oVzoj5GQClHBuBoO&mid=732612af-3729-46d1-aed2-7bd5bc306b47 "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=669a11ec0df5c83b&lid=oVzoj5GQClHBuBoO&mid=732612af-3729-46d1-aed2-7bd5bc306b47") (NCM), a new architecture that changes how AI models generate text. Instead of predicting text one token at a time, NCM learns to represent entire sequences as hierarchies of discrete codes, then generates those representations from coarse concepts to fine details.

In experiments with models of comparable scale, NCM produced text 10–31 times faster than strong diffusion language model baselines while achieving comparable or better quality. It also processed 4–5 times fewer training tokens in selected language modeling benchmarks.

While NCM is in its early stages, the architecture raises an important question for future AI systems: Can models generate better answers more efficiently by deciding on the overall representation before producing the final text?

**The autoregressive challenge**

Most language models today are autoregressive. They generate text by predicting the next token based on the input and everything they have generated so far. Each new token depends on the previous ones, creating a sequential process that becomes more expensive as outputs grow longer.

This also makes it difficult for the model to revise earlier decisions. Once the model generates a token, it cannot directly change that token within the same decoding pass. Techniques such as chain-of-thought reasoning help models plan before producing final answers, but they still depend on sequential token generation.

![alpha_signal_image_1](https://alphasignal.ai/image/1792334577142-ov71f0.png)

Diffusion language models (DLMs) offer one alternative. Instead of predicting tokens from left to right, they work on entire blocks simultaneously and refine the output through successive steps. However, this comes with several limitations:

- They often require many sampling steps to achieve good quality.
- They process the full output sequence at each step, making computation expensive.
- Strong diffusion models can require large training budgets, often involving repeated passes over the same data.

NCM takes a different approach. Instead of repeatedly refining predictions for individual text tokens, it builds an answer by generating representations at progressively finer levels of detail.

**How Next-Concept Modeling works**

Think about writing an article. You usually start by establishing the main idea and structure, then develop individual paragraphs and sentences. As you write, you might go back and edit earlier sentences and paragraphs.

This helps maintain consistency across the article instead of deciding what to write next without considering the overall direction and having no recourse. NCM follows a similar coarse-to-fine process. It learns latent representations that capture information about its answer at different levels of detail.

NCM first represents the answer as a hierarchy of discrete codes, which represent concepts at different levels of granularity. The early levels are short, containing a few codes that capture coarse information about the entire sequence. Later levels contain more codes and progressively add finer details.

The researchers illustrate this with a German-to-English translation example. At the earliest levels, the decoded text is incomplete and does not fully capture the original sentence. As NCM generates additional levels, the translation becomes more accurate and detailed. The intermediate outputs can contain mistakes, which later levels may correct.

![alpha_signal_image_2](https://alphasignal.ai/image/1792334653143-he31i8.png)

To learn this representation and generation process, NCM uses two training stages.

**Stage 1: Learning to represent text.** A multiscale autoencoder learns to compress text into hierarchical codes and reconstruct the original sequence from them. This helps the model learn representations that carry meaningful information at different levels of detail.

![alpha_signal_image_3](https://alphasignal.ai/image/1792334624831-f74unu.png)

**Stage 2: Learning to generate the hierarchy.** A transformer learns to predict the codes at each level, using reconstructions from earlier levels as context. During training, all levels can be predicted in a single forward pass because the correct earlier representations are available. (During inference, the model must generate levels sequentially, but it predicts all codes within each level in parallel.)

The prediction mechanism is key to NCM's efficiency. An autoregressive model needs a sequential generation step for each output token. NCM needs one step for each hierarchical level, typically far fewer than the total number of output tokens. The earlier levels also contain shorter sequences, reducing their computational cost.

![alpha_signal_image_4](https://alphasignal.ai/image/1792334599382-mx7hcw.png)

**NCM in action**

The researchers evaluated NCM on language modeling, translation, summarization, and Sudoku. They compared it with autoregressive and diffusion-based methods, generally using generators with around 100 million parameters.

The experiments highlight several findings:

**Faster generation at competitive quality:** On the LM1B language modeling benchmark, NCM generated text 21× faster than the strongest diffusion baseline while generating higher quality text. The gains come from fewer generation steps and lower computation per step. The researchers measured latency on an NVIDIA H100 GPU.

**Promising results for reasoning tasks:** On hard Sudoku puzzles, NCM outperformed the strongest competing method while requiring fewer model evaluations. Sudoku requires satisfying constraints across the entire board, making it a useful test of coarse-to-fine refinement.

![alpha_signal_image_5](https://alphasignal.ai/image/1792334678742-7h1nar.png)

**Lower training-token budgets:** In the experiments, NCM required 4–5× fewer training tokens than strong diffusion baselines.

The researchers also explored how faster generation can improve quality by allocating more compute at inference time. They tested minimum Bayes risk (MBR) decoding, where the model generates multiple candidate answers and selects the one with the highest average similarity to the others.

Because NCM produces samples quickly, it can explore more candidates within the same time budget. In summarization tasks, it outperformed the strongest baseline by an approximately 7% higher ROUGE-L, a measure of overlap with reference summaries.

This could be useful for applications where developers prefer to spend extra inference compute on improving response quality rather than minimizing latency. Similar selection methods can work with other architectures, but faster generation changes how many candidates an application can afford to examine.

**Availability and future outlook**

The researchers have released NCM's code under an MIT license, along with pretrained checkpoints for different tasks. You can download the models from [Hugging Face](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=669a11ec0df5c83b&lid=l2gKoEjQSkdBivI4&mid=732612af-3729-46d1-aed2-7bd5bc306b47 "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=669a11ec0df5c83b&lid=l2gKoEjQSkdBivI4&mid=732612af-3729-46d1-aed2-7bd5bc306b47") and use the code from [GitHub](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=669a11ec0df5c83b&lid=DepYaLttOQ5Tk9ed&mid=732612af-3729-46d1-aed2-7bd5bc306b47 "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=669a11ec0df5c83b&lid=DepYaLttOQ5Tk9ed&mid=732612af-3729-46d1-aed2-7bd5bc306b47") to reproduce evaluations and inspect generated outputs.

NCM remains an early-stage research architecture. Most experiments involve relatively small generators, although the researchers have tested scaling to 725 million parameters with encouraging results.

Future improvements could include jointly training the tokenizer and generator, scaling to larger models, and dynamically adjusting the number of hierarchical levels based on task difficulty. The current architecture uses a fixed hierarchy.

NCM is still far from replacing mainstream autoregressive LLMs. But its early results show that predicting individual tokens is not the only viable way to generate language. If its advantages hold at larger scales, hierarchical generation could provide another path toward AI systems that produce more consistent outputs while making better use of compute budgets.