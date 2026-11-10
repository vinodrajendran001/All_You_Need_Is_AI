---
title: "Getting Data to Grow in a Dish"
source: "https://deepphenotype.substack.com/p/getting-data-to-grow-in-a-dish?utm_source=tldrnewsletter"
author:
  - "[[Daphne Koller]]"
published: 2026-11-06
created: 2026-11-10
description: "Biology doesn't come with standard parts. We had to build them."
tags:
  - "clippings"
---
![](https://substackcdn.com/image/fetch/$s_!-n0d!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3a06ced-60e8-490d-9166-50a093e3f1e3_1512x1008.png)

*Suppose you were handed the recipes of Joël Robuchon, who earned more Michelin stars than any chef in history, along with his equipment and a skilled crew. Could you serve his dishes at his standard, night after night? The recipes would quickly prove insufficient. Dairy varies by season, ovens drift from their set temperatures, and a reduction thickens while the fish it was meant for still has four minutes to go. A great kitchen runs on constant tasting and adjustment, and Robuchon himself walked away from that kind of cooking in 1996, worn down by it. When he returned seven years later, it was with L’Atelier: an open, modular kitchen, with precision and reproducibility built into the design.*

*In the first essay of this series, I explained why fulfilling AI’s promise in drug discovery requires identifying biological mechanisms with disease-transforming clinical benefit. In the second, I described how our Virtual Human™ integrates human genetics with perturbation experiments in human cells to connect a desired clinical outcome to a druggable mechanism.*

*Knowing which experiments to conduct is only the beginning. We also have to build a physical platform capable of conducting them, measuring their outcomes reliably, and generating evidence at the scale AI requires. And if a baguette, which is nothing but flour, water, salt and yeast, cannot be counted on to come out the same in a different kitchen on a different day, a human neuron grown in a dish certainly cannot. This essay is about what it took to build that platform: a production kitchen for cells, with ingredients that are alive.*

## 1\. Building a data factory

With growing regularity, AI companies are announcing internal wet labs. In 2018, when we started building ours, the idea struck many people as strange. Why would an AI company invest so heavily in the physical world? Most AI research happened in bits: the data already existed as text, images or code, waiting to be collected, cleaned and used to train a model. Why not do the same for biology?

My answer was that the data we needed did not exist.

In mathematics and software, we can sometimes generate data *in silico*, from first principles. Biology doesn’t work that way. It is the product of billions of years of evolution, with no designer and no documentation. To learn what a cell does when we perturb a gene, we have to perform the experiment and look. We cannot reliably reason our way to the answer, and nobody had measured these relationships at anything approaching the fidelity and scale an AI model needs. If we wanted to unravel causal human biology, we would have to generate the data ourselves, in our own laboratories. (That is where the name insitro comes from: the seamless integration of *in silico* and *in vitro*.)

That decision turned out to be both more rewarding and more difficult than I anticipated.

The reward came in the form of novel therapeutic targets. [In ALS](https://www.insitro.com/news/rewriting-the-playbook-for-als-drug-development/), we produced six billion motor neurons carrying the genetic backgrounds of a diverse population of people living with ALS. We characterized those cells through imaging and transcriptomics, then used AI to identify a new axis of ALS biology. The work led to three novel targets, including ALS-1, the target of our CTRO-2018 program.

The difficulty is the subject of this essay. Building a wet lab is not, in itself, especially hard. You buy benches, recruit good biologists, and run experiments. (This is more akin to cooking a home-made meal from a family recipe.) Building a laboratory that produces reliable, high-quality data at the scale AI needs is something else entirely. It is Robuchon’s problem at a different scale. Every step has to come out the same way thousands of times, with no chef tasting: cells must grow to the right density, enzymes must stay cold, the thin glass beneath a plate must survive robotic handling, and the microscope must capture hundreds of thousands of images in focus.

Our kitchen also has to change its menu. We work with different cell types, disease models, stressors and readouts, each with its own requirements. It is as if the restaurant served a different cuisine with different ingredients every month.

And the ingredients are alive. Two batches of cells, even from the same lineage, behave differently, and the more complex the cell type, the greater the variation. A chef can taste when a sauce has gone wrong. A model has no way to tell biology from experimental drift, so it latches onto the strongest signal it can find, and an unmeasured change in temperature or nutrient batch can masquerade as a discovery. The factory has to accommodate that variation without obscuring the very differences we want to study.

We have spent the better part of eight years learning what published protocols leave out. Some timelines are unyielding: neurons take weeks to mature in culture, much as dough takes its own time to rise, and neither capital nor compute can hurry them. And a protocol can be followed, but the edge cases it doesn’t mention have to be met one at a time. What follows is what we learned meeting them.

## 2\. The POSH platform

Our laboratories run several industrialized workflows, each with its own combination of hardware, software, and wetware. One of the most important is [POSH](https://www.nature.com/articles/s41467-025-66778-6), or Pooled Optical Screening in Human cells, which generates much of our experimental evidence about gene function in human cells.

In a POSH screen, millions of cells grow together in a single pool. Each receives a construct carrying a CRISPR guide RNA that directs gene-editing machinery to a particular gene, usually knocking it out. A library can target thousands of genes or extend across the genome, and we also use other kinds of perturbation. Each construct carries a molecular barcode, a short sequence of nucleotides that identifies its guide.

We then stain the cells and image them under a high-resolution microscope. Some stains come from [Cell Painting](https://www.nature.com/articles/nprot.2016.105), a panel that labels nuclei, membranes, and other cellular structures. Others mark particular proteins or RNA molecules relevant to the biological question. The images let us measure how each cell responds to losing a gene, but they do not tell us which gene it lost. For that, we have to read its barcode.

We use *in situ* sequencing, reading the barcode while the cells remain fixed in the plate. Roughly thirteen rounds of chemistry reveal successive nucleotides in four fluorescent colors, each followed by imaging. A plate goes on and off the microscope more than a dozen times over several days, producing more than 200,000 images. Software aligns those images to within microns so that each cell’s barcode can be connected to its phenotype. Millions of cells per screen, across dozens of screens a year, become the training data for our models.

![](https://substackcdn.com/image/fetch/$s_!zF2t!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9ddaa72b-106e-4244-ba17-1b248948149b_2400x2191.png)

##### POSH screen in four steps. Millions of cells grow in one pool, each then transfected by a CRISPR guide and a molecular barcode. We image the phenotype, then read the barcode, in place, over roughly thirteen rounds of sequencing. The result is one row per cell: what we did to it, and what happened.

We chose to build POSH because it [complements human genetics](https://deepphenotype.substack.com/p/mapping-causal-human-biology-9e7). Genetic studies implicate genes in disease; perturbation experiments show what happens when we alter those genes in a particular cellular context. Together, these measurements help our Virtual Human identify hypotheses worth pursuing. A change in a cultured cell does not establish that an intervention will benefit a patient. But it suggests a mechanistic hypothesis that we can align to human clinical data, and subsequently assess in other models.

Images also reveal consequences to cellular function that gene expression alone may miss: the shape of a neuron, the location of a protein, the state of a signaling pathway. AI can read those images better than people can, and imaging costs about 100x less per cell than other high-content, single-cell measurements.

Pooled screening reduces batch effects because cells carrying different perturbations share an experimental environment. This is particularly useful when comparing subtle phenotypes across many perturbations. If each guide were tested in a separate well, differences in cell density, reagent exposure, or timing might confound the effects of the gene. Pooling mitigates that impact. So in an arrayed screen, your N is a well; in a pooled screen, your N is a cell.

## 3\. Things that go bump in the night

One morning, the robotic arm in one of our workcells picked up a plate of cells and threw it across the deck. The plate held a week’s work and several million cells, and the arm was operating inches above a microscope that costs more than a Porsche.

<video controls=""></video>

##### Footage of our automation systems during early prototyping phases. A single sub-millimeter displacement, or a failure in grip pressure sensing, can lead to catastrophic failure if not properly controlled for. Each system has several cameras monitoring them 24/7 so that when these events do occur, the root cause can be identified and fixed.

The arm was supposed to lift the lid so a liquid handler could reach the wells. When we aligned the camera footage with our timestamped protocol logs, we found that every throw occurred during that operation. The lid was coming up with the plate stuck to it.

The cause was a fix for an earlier problem. Our plates had been cracking unpredictably. Their bottoms are coverslip glass, 170 microns thick, bonded to a plastic frame. During a single screen, they may undergo more than a hundred heating and cooling cycles and two hundred robotic handling steps. After weeks of investigation, we traced the cracks to an automated sealer that pressed hard enough to leave microfractures in the glass. We replaced it. The new seals, however, left enough adhesive around the rim to occasionally glue the lid to the plate. When the arm lifted the lid, the plate came with it.

This is what building in the physical world is like. Glass, glue, heat, enzymes, motors and cells interact in ways no one planned for. Fixing one failure can create the next.

Worse than things that go bump are those that go bump in the night. Networks drop connections, power supplies flicker, and computers install updates at 1 a.m. because nobody is using them — unless, of course, they are running a screen. An operator can often resolve such interruptions during the day. Over a holiday weekend, the same interruption can ruin an experiment. A collection of bits on a disk can wait for someone to restart a process. Cells and time-sensitive reagents often cannot. We had to work through a long list of rare but consequential events using buffering, local processing, recovery mechanisms, and uninterruptible power supplies.

And even worse are those that don’t go bump at all — the silent failures that announce themselves only after the fact, often through bad data. After a change in oligonucleotide supply, our sequencing stopped producing readable fluorescent dots. Nothing reported an error; it took weeks to find a single mislabeled primer. Our imaging systems sometimes froze without warning, leaving a laser illuminating one spot long enough to burn through a plate lid. The cause was a faulty USB port. A third-party camera driver silently shifted successive images by one frame. An experiment that fails visibly costs time and material. One that appears to succeed while recording the wrong thing can mislead the science. We needed to make silent failures loud before they entered the dataset.

## 4\. Measure, stabilize, optimize

![](https://substackcdn.com/image/fetch/$s_!sb0l!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b08a59e-4c81-4a98-81b2-63ff568e49c1_2400x1410.png)

##### Every A549 plate we have run, and what moved the number. Each mark is a single plate across three and a half years. The early scatter is the problem: runs landing anywhere between the floor and the 45% threshold, with no way to tell a real gain from a good week. Four interventions — training and scaling, software, automation hardening, and second-generation chemistry — carried the mean to 71%, and tightened it.Once a process appears to work, the temptation is to scale it: more instruments, more plates, more throughput. But scaling an unstable process may simply multiply the measurements you cannot trust. A Michelin star chef wouldn’t release a dish that has not been taste-tested; nor should a scientist trust data from a process that has not been validated. We learned to do things in a particular order: measure the process, stabilize it, and then optimize it. Only then does it make sense to scale.

### Measure everything

Similar to a chef tasting a dish while cooking it, a scientist running an experiment by hand makes countless assessments, often without realizing it. Are the cells healthy? Is the microscope in focus? Did that dispense look right? An automated system makes none of these judgments unless we build in the means to do so. We realized quickly that we needed to instrument and measure as much as possible: the mislabeled primer, faulty USB port, and camera-driver error had produced no warning. The platform had to tell us what was actually happening, not merely what it had been instructed to do.

Cameras and timestamped logs allowed us to connect the thrown plates with the adhesive. Temperature records let us check whether a refrigerator, freezer, or reservoir contributed to a failure. One of the most useful sensors in the workcell is also among the cheapest: a scale. We weigh plates throughout the workflow. Pumps fail, tubing clogs, O-rings wear out, and plates crack or leak. The scale cannot tell us which failure occurred, but it can tell us when the volume changed, often enough to narrow the search considerably.

The biology needs equal attention. We sequence the CRISPR guide library after synthesis, examine its representation after introduction into cells, and monitor the population during a screen. This reveals whether some guides are becoming overrepresented before the experiment is finished. We test guide-editing activity in new cell lines and check every sequencing-chemistry change against both the phenotype stains and the barcode readout. A change that improves one can quietly damage the other.

Measuring the output is harder, because the input never holds still. In manufacturing, you can assess an instrument by giving it the same part repeatedly and measuring the variation. Biology does not offer identical parts. When a screen performs poorly, was the biological effect small, or was the measurement unreliable? We developed the closest thing to standardized parts that we could: reference cells with well-characterized barcodes and synthesized barcoded beads that remove living cells from portions of the process. Running them regularly allows us to measure the platform independently of the biology under study. Much of the variation in our early results, we discovered, came from the platform itself. Until we could measure that contribution, a disappointing screen left us with dozens of possible causes and no principled way to choose among them.

### Stabilize the process

Once we could measure the platform, we set about making it behave consistently. We added checks at every handoff: was the plate present, was the lid removed, had the microscope stage returned to position, had the focus system settled? We recalibrated robot positions, qualified liquid-handling performance, and replaced reactive repairs with preventive maintenance. Each check became a timestamped record we could examine over time.

Much of the harder work was software. A workcell combines instruments from numerous manufacturers, with different interfaces and assumptions about how they communicate. The robot must not move a plate until the liquid handler has finished, or place one on a microscope before the stage is ready. We wrote software to coordinate those handoffs, verify instrument states, and keep checking during acquisition.

Our microscopes presented a related challenge. Capturing an image requires coordinating more than twenty components and actuators, while each imaging system can generate about 80 megabytes of raw data per second. Commercial control software was not designed for the combination of flexibility, throughput, and continuous operation we needed, so we built our own acquisition package, Pyxscope. It now captures more than 95% of our imaging data, operating around the clock and sending individual images to the cloud within seconds of acquisition. Streaming also changed what we could do while a screen was running. An empty well, focus error, or exposure problem could be detected while the screen was still running, rather than discovered after the images had been collected. We could stop wasting microscope time on a run that had already gone wrong.

The images then have to be analyzed. Our early tools were long-running notebooks on large cloud computers. Over time, common components became Pyxcell, our image-analysis platform. We moved demanding workloads to batch computing and extended analysis from individual fields of view to stitched wells, recovering cells otherwise lost at image boundaries. Making those features reliable in production took more engineering than building the first versions, including checks that separate defective images from failures in the analysis software.

The reward was a system we could measure end to end. With those records, we adopted statistical process control, the set of methods manufacturers use to separate ordinary process variation from exceptional events. A result outside established control limits calls for investigation. A process that stays within its limits, even at a level we dislike, is behaving consistently. Adjusting it in response to every fluctuation can make matters worse.

![](https://substackcdn.com/image/fetch/$s_!8Ae9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff81be52-7948-4463-9bc3-a47d35563df7_1652x890.gif)

##### The same readout before and after: dim, scattered signal on a hazy field becomes bright punctate dots on a dark one. Each dot is one round of sequencing chemistry reading one nucleotide of a cell's barcode.

Our main measure is barcode efficiency: the fraction of cells for which we can identify the genetic perturbation. Before stabilization, it varied from approximately 25% to 50% between runs, averaging 34%. Afterward, the average had risen to 47%. Measured by yield alone, that looked like an enormous amount of engineering for 13 percentage points. But the standard deviation fell from 11.2 to 2.5 percentage points. The process had become predictable. We could finally tell whether a change had improved the system or whether we were simply having a good week.

### Optimize the signal

With the process under control, the remaining gap between 47% barcode efficiency and our target was no longer principally an automation problem. We now had a reliable method of measuring our progress, and could have spent another year adjusting robots for marginal improvements. Instead, we knew to focus our energy towards software and chemistry changes that would have the greatest impact.

We found and corrected a fluorescence artifact that accumulated in one color channel across thirteen sequencing rounds, biasing the base caller toward that color. More importantly, we adopted chemistry that amplifies each barcode, producing much brighter sequencing dots that can be read much more quickly, and manifest in many more cells. Together with other improvements, those changes raised barcode efficiency above 71%, with the standard deviation remaining at a reliable 7 percentage points.

---

![](https://substackcdn.com/image/fetch/$s_!Hnm4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F12439262-263e-44ee-a86c-8f8a246f969e_2400x1170.png)

##### The compounding return on a stable process: The same whole-genome screen now takes 4 FTE-weeks instead of 52, 10 plates instead of 27.5, and $50,000 in reagents instead of $200,000. By simultaneously optimizing time, cost, and effort, it has now become possible for the platform to regularly conduct frequent genome-wide screens.

A platform never has a single bottleneck. It has a succession of them, and solving one exposes the next. The limiting step is not necessarily the slowest; it is the one that most constrains our ability to produce reliable data at the scale we need. A stable process lets us identify it.

## 5\. Use the tool that fits the problem

Nearly every problem in a platform like POSH can be approached in multiple ways: through computation, hardware, or chemistry. The right choice depends on where the information was lost, and whether it can still be recovered.

Take image alignment. The phenotype images and thirteen rounds of sequencing images must be matched cell by cell, to within microns, although they are acquired days apart with the plate repeatedly removed and replaced. A robot returns a plate to within roughly 100 microns; the microscope clamp improves its repeatability but cannot place every cell in exactly the same position. We could have invested in submicron robotics. Instead, every acquisition includes a nuclear stain, and software uses the nuclei as landmarks to align images and assign each barcode to the correct phenotype.

Focus is different. If an image is displaced sideways, software can realign it. If the microscope is a few microns out of focus, fine cellular detail was never recorded. While generating ground truth data, no algorithm can recover detail that was never captured. We therefore combine measurements from five autofocus routines per well to establish the focal plane, then maintain focus with an infrared sensor and software that waits for focus to settle before imaging.

Other problems belong in chemistry. The standard Cell Painting stain for mitochondria uses a dye whose fluorescence persists into sequencing and interferes with base calling. Rather than trying to untangle those signals afterward, we designed MitoProbe to bind accessible regions of mitochondrial RNA, guided by the structure of the mitochondrial ribosome. It works in fixed cells and washes away before sequencing begins.

Others are best prevented in the experimental design. We construct our guide libraries so that every pair of barcodes differs in at least three positions. A barcode with one misread nucleotide can still be assigned to the right guide, recovering between 5% and 35% more cells, depending on the screen.

The point isn’t to make every part of the platform more sophisticated. It is to measure biology as faithfully as we can, while keeping the link between the intervention and the observation intact.

## 6\. Intelligence inside the machine

We built POSH to generate training data for AI. Along the way, AI became a useful tool for building POSH itself. Equally important was deciding where to use the judgment of a scientist, and where a model could do the work better or at a scale no person could manage.

### Artificial intelligence

Consider base calling. The conventional approach uses hand-tuned image-processing rules that need adjustment as experimental conditions change. We replaced it with a small convolutional neural network, trained initially on predictions from the older method after filtering out invalid barcodes. The network ultimately outperformed the method it learned from. The fraction of cells assigned a valid barcode rose from 66.6% to 78.8%, without manual tuning. (Sivanandan et al., *[Nature Communications](https://www.nature.com/articles/s41467-025-66778-6)*, 2025).

Cell segmentation posed a different challenge. Every image-based measurement depends on identifying the boundary of each cell. A misplaced boundary can assign a barcode to the wrong cell, contaminating the data without an obvious warning. Our early screens used Cellpose, a deep learning model that performed reasonably well on simple shapes but poorly on complex or three-dimensional cells. Training a model for a new cell type could take months of manual annotation.

Our active learning framework, iALDE, changed the allocation of that effort. A model proposes boundaries, identifies cases it is least certain about, and asks an expert to correct them. The model retrains and the cycle repeats. Instead of outlining thousands of cells indiscriminately, scientists concentrate on examples that teach the model something new. Annotation time fell more than fiftyfold.

![](https://substackcdn.com/image/fetch/$s_!r8Jn!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F277feb55-a130-4356-aa18-15382230cc11_3200x2240.png)

##### Spending expert attention where it teaches the model something: The model proposes cell boundaries, flags the cases it is least sure about, and a scientist corrects only those. Each cycle, its agreement with expert consensus climbs.

Quality control was harder still. Images can be out of focus, overexposed, obscured by debris or compromised by cell density. Reviewing tens of thousands of phenotyping images per plate by eye would take days, and a screen can include twelve plates. For years, most images went uninspected, allowing technical artifacts into analyses where they could resemble biological effects.

![](https://substackcdn.com/image/fetch/$s_!ZQaC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd8acd263-3465-4e87-9c10-98a247df589a_3200x2300.png)

##### What the reviewer is looking for. Underexposure and noise, high background, overexposure, loss of focus, debris, overlapping cells. For years most images like these went uninspected.

Conventional image-quality metrics were confounded by differences in cell type and density. Supervised classifiers did better, until we changed the cell type. What we needed was a reviewer with enough general microscopy knowledge to recognize different failures in unfamiliar conditions. Multimodal language models offered a way forward: agentic QC.

Two engineers took agentic QC from prototype to production in about six weeks. It evaluates seven failure modes, explains its assessments, agrees with expert reviewers 82% of the time, and increased coverage more than eightyfold. Among its first catches was the camera-driver bug that shifted images by a frame, identified the evening the affected quantitative phase images were acquired.

### Human intelligence

When building automation and AI, it is tempting to treat the scientist as the component to be engineered out. That would be a mistake. The question is where their judgment belongs.

In iALDE, the model draws the boundaries and the expert corrects the difficult ones. In quality control, the model examines images at a scale no human team could sustain, but scientists define the standards, qualify the system, and decide what to do with its findings. The explanation accompanying each flag matters because it gives the scientist a basis for evaluating the model’s assessment. An unusual image might reflect a failed acquisition or the most interesting cellular response in the screen. The model can bring it to someone’s attention. Determining which explanation the experiment supports requires scientific judgment.

Scientists can spend less time on rote tasks such as inspecting images and more time choosing experiments, investigating anomalies, and deciding what the measurements mean. The models extend their reach, allowing them to apply scarce expertise where it has the most consequence.

## 7\. The platform flywheel

POSH is one platform, and the reason we built it is the reason we keep building others. Understanding causal human biology at scale requires new cell types, perturbations, and measurement methods, each with different demands. Scale rewards standardization, while discovery requires change. We have learned to engineer for both.

Part of the answer is modularity. We use standard equipment that can be expanded and reconfigured, with interchangeable plate formats, lasers, filters, and cameras. Adding quantitative phase imaging required a camera change rather than a new microscope. Our perturbation vectors are similarly adaptable across imaging and sequencing readouts.

Much of our progress derives from the unique composition of our team. Reference cells and beads emerged from molecular biologists working with process engineers. MitoProbe arose from structural biology applied to an imaging problem. The base caller came from machine learning scientists working with microscopists. A biologist looking at poor barcode recovery might suspect chemistry. An automation engineer might suspect focus. A machine learning scientist might suspect the base caller. A statistician asks whether the apparent change exceeds ordinary variation. Each has been right at different times. The advantage comes from giving them the same problem and having them work through it while sitting in the same room.

At first, every failure felt like a separate problem. Gradually, we recognized that the solutions had something in common. We needed to measure what was happening, distinguish routine variation from a real change, choose the appropriate intervention, and apply scientific judgment at the points where it was needed. We began engineering how we build platforms as carefully as we engineered the platforms themselves. None of the principles in this essay are secret. Measure, stabilize, then optimize is process engineering as any competent engineer would practice it. What is hard, and what took us years, is the layer below: knowing what to measure in a living system, how to separate its variation from the machine’s, when a process is stable enough to be worth improving, and how to do all of that quickly in a laboratory that keeps changing underneath you. That layer does not come from a textbook or a protocol. It comes from having done it.

A lot of work went into POSH, but the effort left behind more than individual fixes: instruments, software, statistical methods, screens, and other workflows. Each one was faster to build than the last, partly because more of the machinery was already in place, and partly because we had gotten better at the building itself. A segmentation model that once took six to twelve months of annotation and training can now be developed in about a month. The same framework has supported images of lipid droplets in fat cells, liver tissue, body MRI, and retinal scans. The machinery for selecting informative examples, training new models, and qualifying their performance no longer has to be invented from scratch each time. More broadly, process-control tools, data streaming, Pyxcell, active learning, and image quality control have all been reused in workflows with very different experimental requirements.

People often ask me whether the platform we have built can provide insight into every disease. The answer is no. A disease is only as tractable as our ability to measure what has gone wrong in it, and the measurements we can make today do not reach all of human biology. The good news is that they reach a great deal of it, enough to have delivered the targets described above and many more. The better news is that technologists keep inventing new ways to perturb and measure biology, and each one brings diseases within reach that were beyond it before. But a new method is not a capability until it runs at scale, with measurements we can trust, alongside everything that already works.

The most important thing we have built is not any single platform. It is the ability to build the next one.