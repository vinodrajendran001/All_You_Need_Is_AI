
Modern Retrieval-Augmented Generation (RAG) systems can expand to millions of document chunks encoded as high-dimensional embeddings that can store up to 3,072 values per chunk.

Yet, Lloyd’s k-means, the clustering algorithm that powers the vector search techniques used to match documents to prompts, has remained largely unchanged for nearly seven decades. The limits of this algorithm is showing itself when RAG systems are deployed at scale.

To solve this challenge, researchers at Meta FAIR and École nationale des ponts et chaussées have released “[e-means](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=980ea889d740a7b9&lid=JKOW5TcetmwRRgcW&mid=97701ce9-5439-4010-83cb-ae7d793f55e3 "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=980ea889d740a7b9&lid=JKOW5TcetmwRRgcW&mid=97701ce9-5439-4010-83cb-ae7d793f55e3"),” a drop-in replacement for k-means that works at the scale of modern RAG pipelines.

Across 24 benchmarks covering text, code, image, and multimodal embeddings, e-means beats Lloyd baseline in roughly one-tenth the passes while running 10-45X faster on GPUs than Flash-KMeans and 8-15X faster on CPUs than Faiss.

e-means is compatible with the embedding model and document chunking strategy, and it doesn’t affect your search queries. It lowers the cost and time of clustering your embedding collections, which will allow you to rebuild RAG indexes more frequently and prevent search quality from degrading over time.

**How clustering became a bottleneck for RAG pipelines**

When you have millions of records in your vector database, comparing every one of them against your prompt becomes prohibitively expensive. To speed up search, vector indexes break the embeddings into tens of thousands of clusters, each represented by a centroid.

Vector search happens in a multi-step search, where the query embedding is compared against the centroids first before choosing the subset of documents (the clusters) from which the final candidates should be chosen from.

To update the centroids of the document corpus, Lloyd’s k-means scans every vector in the dataset. To refine the centroids, Lloyds repeats the full-pass cycle (aka epoch) 20-25 times.

![alpha_signal_image_1](https://alphasignal.ai/image/1795358712779-fhs6up.png)

The compute cost of Lloyd’s k-means becomes prohibitive as documents grow to millions. Consequently RAG teams are forced to postpone index rebuilds in stores with shifting corpora, such as support tickets, product docs, or news feeds.

Meanwhile, appending new documents without recalculating the clusters causes the centroids to lose their accuracy. As a result, the clusters can become lopsided (some containing too many documents and some too few), resulting in higher latency and lower recall accuracy.

In LLM data pipelines, slow clustering also drags down semantic deduplication, where oversized clusters inflate the pairwise similarity checks performed inside each bucket.

The obvious fix to scanning every document is to update centroids incrementally on small slices of data. That is how mini-batch k-means works. Built on James MacQueen’s 1967 update rule, mini-batch k-means replaces full-dataset passes with faster partial updates.

![alpha_signal_image_2](https://alphasignal.ai/image/1795358743577-8zsvbd.png)

Mini-batch k-means has three key challenges:

- It requires manual tuning of the clustering parameters for every new dataset
- It generates a lot of empty "dead" clusters that waste index capacity
- It can generate unbalanced clusters that hurt both vector search recall and deduplication runtime

Engineers were stuck choosing between Lloyd’s reliable-but-slow algorithm and mini-batch’s fast-but-unstable shortcuts and frustrating tuning. e-means challenged this decades-long tradeoff.

**How e-means works**

At a high level, e-means combines the best of both worlds: the speed of mini-batch updates with the zero-tuning reliability of Lloyd’s algorithm. It has three practical outcomes:

- **Lower compute and memory costs:** e-means needs fewer passes over the data and uses custom GPU code that reduces memory requirements.
- **Higher clustering accuracy:** It has better accuracy than 25-epoch Lloyd across datasets.
- **No classic mini-batch pitfalls:** It requires no per-dataset tuning, produces almost no dead clusters, and keeps cluster sizes balanced.

![alpha_signal_image_3](https://alphasignal.ai/image/1795358649254-lnknib.png)

Three core design choices drive these results:

- **Moving averages that forget early mistakes:** Instead of storing every historical assignment, e-means updates each centroid with an exponential moving average (EMA). Centroids track recent data while gradually fading out outdated early guesses. The mild noise from small batches also helps centroids escape bad groupings that happen in Lloyd’s method.
- **Zero-tuning scaling rules:** In classic mini-batch methods, engineers have to find batch and step sizes by trial and error. Meta’s team derived scaling laws that automatically set both parameters from three inputs you already have: dataset size, cluster count, and epoch budget.
- **Reviving dead clusters by splitting crowded ones:** When a cluster goes empty, e-means picks a large active cluster and splits it in two. This reduces dead clusters considerably in comparison to baseline methods.

Two additional engineering touches convert fewer passes into wall-clock speed. First, e-means gradually shrinks its update step size as training progresses (cosine annealing) and ends with a near-zero-cost finalization step that snaps centroids to their exact last-epoch averages.

Second, it uses fused GPU kernels to combine distance calculation and cluster assignment into a single pass without filling GPU memory. On an H100 GPU with 10 million vectors and 65,536 clusters, 25 epochs of plain PyTorch Lloyd take 142 to 155 seconds and Flash-KMeans takes 14 to 22 seconds. Meanwhile, e-means cuts Flash-KMeans’ end-to-end GPU runtime by 10 to 45 times.

![alpha_signal_image_4](https://alphasignal.ai/image/1795358681651-c9h7ja.png)

In practice, these gains change how teams schedule routine index and data-pipeline work:

- **Dynamic RAG indexing:** With a 50-million-document index of live support tickets or internal docs, a 25-pass Lloyd reindexing would tie up GPUs or stall CPU batch jobs, pushing teams to delay re-clustering for months. With e-means, rebuilding the cluster map becomes fast enough to run as a scheduled weekly or nightly job, preserving search quality without touching embeddings or query-time retrieval.
- **LLM data curation:** Before e-means, teams running semantic deduplication or diversity sampling for supervised fine-tuning (SFT) over large text corpora faced steep full-batch compute bills or lopsided mini-batch buckets that slowed intra-cluster similarity checks. After e-means, they can partition large datasets quickly and evenly, iterating on curation sweeps far more often.

**Where you can use e-means today and where you cannot**

Meta shipped [the code for e-means](https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=980ea889d740a7b9&lid=1DuxR41PAUJx6AHBe&mid=97701ce9-5439-4010-83cb-ae7d793f55e3 "https://app.alphasignal.ai/c?uid=12PIFGaVBFKQnaUyy&cid=980ea889d740a7b9&lid=1DuxR41PAUJx6AHBe&mid=97701ce9-5439-4010-83cb-ae7d793f55e3") in Faiss 1.16.0, offering both PyTorch GPU and NumPy CPU versions under Faiss’s commercial-friendly MIT license. Standalone clustering with e-means can be done in three lines of Python.

Passing those centroids into a Faiss Inverted File (IVF) search index (the structure that uses clusters to narrow down which vectors to scan at search time) requires only light glue code.

e-means has a few operational boundaries:

- Teams running self-hosted Faiss IVF pipelines, or custom PyTorch and NumPy clustering scripts for LLM deduplication and dataset curation, can test it immediately.
- Teams on managed or third-party vector databases (e.g., Pinecone, Milvus, Qdrant) cannot plug e-means in themselves today because clustering is hidden inside the storage engine.
- e-means only affects offline indexing and curation, not live search. It also applies to static dataset snapshots rather than continuous streaming updates.

Frontier model launches draw most of the spotlight in AI. Yet modernizing a 70-year-old primitive like k-means quietly removes real operational friction across the infrastructure that feeds, cleans, and grounds those models.