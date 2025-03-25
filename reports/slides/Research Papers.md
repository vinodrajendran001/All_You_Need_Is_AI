
# This Week's Top AI/ML Research Papers

#### Vinod

---
<section>
    <h4>Transformers without Normalization</h4>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: center;">
        <div>
            <p>Transformers can achieve or surpass normalized performance using a simple technique called Dynamic Tanh (DyT), replacing normalization layers with an element-wise operation inspired by tanh-like mappings observed in layer norm, validated across various tasks in computer vision and LLMs.</p>
            <p>
                🔗 <a href="https://arxiv.org/abs/2503.10622">Transformers without Normalization</a>
            </p>
        </div>
        <div>
            <img src="Pasted image 20250325101836.png" alt="Transformers without Normalization" style="width: 100%; max-height: 400px;">
        </div>
    </div>
</section>
---
<section>
    <h4>Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models</h4>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: center;">
        <div>
            <p>Block diffusion language models, merge discrete denoising diffusion with autoregressive models, addressing fixed-length generation limitations and enhancing inference efficiency via KV caching and parallel token sampling. This model introduces a training algorithm, gradient variance estimators, and data-driven noise schedules for minimized variance, achieving state-of-the-art results among diffusion models on benchmarks and enabling flexible-length sequence generation.</p>
            <p>
                🔗 <a href="https://arxiv.org/abs/2503.09573">Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models</a>
            </p>
        </div>
        <div>
            <img src="Pasted image 20250325104949.png" alt="Block Diffusion" style="width: 100%; max-height: 400px;">
        </div>
    </div>
</section>
---
<section>
    <h4>Compute Optimal Scaling of Skills: Knowledge vs Reasoning</h4>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: center;">
        <div>
            <p>This paper investigates whether compute-optimal scaling laws in LLM development are skill-dependent by examining knowledge-based tasks and reasoning skills, affirming that they indeed are. Through extensive ablation studies on various pretraining datamixes, it is shown that knowledge and reasoning skills like code generation fundamentally differ in scaling behavior, independent of datamix composition. Using a misspecified validation set can significantly misalign compute-optimal parameter counts by nearly 50% based on skill composition.</p>
            <p>
                🔗 <a href="https://arxiv.org/abs/2503.10061">Compute Optimal Scaling of Skills: Knowledge vs Reasoning</a>
            </p>
        </div>
        <div>
            <img src="Pasted image 20250325105456.png" alt="Compute Optimal Scaling of Skills: Knowledge vs Reasoning" style="width: 100%; max-height: 400px;">
        </div>
    </div>
</section>





