---
title: "Hardware Is Software"
source: "https://unchartedterritories.tomaspueyo.com/p/hardware-is-software?utm_source=tldrnewsletter"
author:
  - "[[Tomas Pueyo]]"
published: 2026-11-18
created: 2026-11-20
description: "What happens when silicon gods gobble up atoms too"
tags:
  - "clippings"
---
## 1\. Hardware Becomes Software

A US company is trying to bring back supersonic civilian flight, and to make their airplanes faster and cheaper than the Concorde.

![](https://substackcdn.com/image/fetch/$s_!oCDq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea67e615-0032-4766-9afc-dde2323f9dfd_2048x967.png)

You can’t call [Boom](https://boomsupersonic.com/)[^1] a simple hardware engineering company. They’re taking on one of the hardest engineering challenges out there. So I was surprised when its founder CEO, [Blake Scholl](https://x.com/bscholl), said [this](https://x.com/bscholl/status/2118524700796305669):

> *12 years ago I founded Boom, as a software engineer doing hardware for the first time.*
> 
> *More than a decade in, the most insane realization is that software is the key to reaccelerating hardware engineering. But in a way that I don’t think is widely understood or implemented, even in the burgeoning hard tech community.*
> 
> *Most hardware engineering is actually software engineering in disguise. It’s spreadsheet “code,” engineering calculations done as one-offs. Eg, wing structural loads in, spar sizing design out. Thermal loads in, air conditioning system sizing out.*
> 
> *Everything is a calculation, and calculation is software. But these calculations are done essentially by hand, as if we are doing arithmetic but have not yet discovered algebra.*
> 
> *Hardware engineers have baby software, built in spreadsheets, the kind of crappy software I wrote as a kid before I understood architecture, unit tests, APIs, version control, and everything else that makes modern software good.*
> 
> *Our airplanes and engines are built with the software sophistication of a script kiddie.*
> 
> *So what we tell our engineers: don’t design the hardware, design the \*algorithm\* for designing the hardware. And take the algorithm seriously—as an algorithm and as a first-class engineered software system.*
> 
> *Never design a piece of hardware, such that you couldn’t redesign it tomorrow with a different set of assumptions.*
> 
> *This all sounds obvious, yet our experience at Boom is that it changes everything.*
> 
> *Ten years ago we couldn’t afford to build much software. We had a small team—and there were few software engineers with the curiosity, brilliance, and vision required to learn hardware engineering.*
> 
> *But now AI changes the equation. Now everyone can code. The software engineers define the architecture. The hardware people bring the physics and engineering know-how.*
> 
> *We have a turbomachinery design tool that lets one engineer do in realtime what previously took 100 engineers six months. Another tool auto-generates 65% of entire aircraft structure. I’m sure we’ll figure out the other 35% too. Eventually these should not be multiple tools, but one integrated physics model of a complete vehicle, airframe and powertrain.*
> 
> *The results speak for themselves. A boomless supersonic airplane built by 50. A full scale supersonic turbine made by 150. And with this approach, I don’t think we’ll need that many more people to build and certify a supersonic airliner.*
> 
> *You don’t need a big team to build big things—not when everyone on the team is a software engineer.*

NASA proved this is the case: In [this 2022 paper](https://ntrs.nasa.gov/citations/20220012523), they used AI to design industrial parts, and they were 40% cheaper, 66% lighter, 85% faster to design, and more robust than human expert-designed parts. That was NASA in 2022, before AI got really good. Imagine putting a tool that’s one million times better in the hands of every manufacturer.

## 2\. Hardware = AI

So what happens when you don’t need a big hardware team when everybody is a software engineer, but AI replaces software engineers?

Here’s a side project of [Casey Handmer](https://www.caseyhandmer.com/), founder of Terraform (I’m an investor):

![](https://substackcdn.com/image/fetch/$s_!AdZR!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff5233267-f4c2-4227-8990-773d349ab06a_1200x1376.png)

The big golden rectangles are the antennas that emit microwaves (MW) that hit a person, and capture how these MW then return to them. The rest of the board creates the MWs and interprets the data. The top number on the display seems to be the heart rate and the bottom number the respiration rate.

According to him, he asked Claude:

> *Design a printed circuit board that can use radar to detect my heart rate*.

Claude designed the circuit and physical layout, the firmware, the software… I assume Casey sent the files to a board printing and assembly company, and got it back for a couple hundred bucks. Here’s what the device can do:

> *It can do range, angle, motion frequency. It can tell if I'm typing and guess what it is (not perfect). It can tell if I'm speaking but not what I'm saying.*

The only physical step in all of this was the board manufacture and assembly, but that’s already a commodity, because a lot of that process is automated today—and more will probably be.

So what happens when you push this thinking further? Casey has yet [another prediction](https://x.com/CJHandmer/status/2120994222035829082), after Jensen Huang stepped down from NVIDIA:

> *Nvidia is cooked either way. GPU* \[Graphics Processing Unit, the computers NVIDIA sells\] *design and CUDA* \[the software that lets programs use the GPU efficiently\] *were insurmountable moats 12 months ago, now a Fable-class model* \[Claude, basically\] *can independently rebuild both for <$1m token spend.*

Indeed, NVIDIA doesn’t manufacture its GPUs, TSMC does. NVIDIA just designs them and adds their software. People have [four trillion](https://www.google.com/search?q=market+cap+nvidia&oq=market+cap+nvidia&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBwgBEAAYgAQyBwgCEAAYgAQyBwgDEAAYgAQyBwgEEAAYgAQyBwgFEAAYgAQyBwgGEAAYgAQyBwgHEAAYgAQyBwgIEAAYgAQyBwgJEAAYgATSAQgzNTYzajBqN6gCALACAA&sourceid=chrome&source=chrome.ob&ie=UTF-8) reasons[^2] to reverse engineer that software and design. Google was [already doing this a decade ago](https://deepmind.google/blog/how-alphachip-transformed-computer-chip-design/), and it’s been using AI to do it [for years](https://deepmind.google/blog/how-alphachip-transformed-computer-chip-design/). That’s how they got their competing TPUs. Now, everybody can do it.

## 3\. Cutting Intelligence Costs in Manufacturing

You can see where this is going: R&D costs will soon be eliminated from manufacturing. Depending on the industry, they account for ~ [5-20%](https://www.ncses.nsf.gov/pubs/nsf25353) of a manufacturing company’s revenue. But AI won’t just reduce those; it will go well beyond. A lot of manufacturing costs go to designing requirements, documenting, detailed engineering, experimentation, measurement, certification, qualification—all tasks that can be automated. And of course, better design also means cheaper designs, so the cost of parts, transportation, and energy will also shrink with more AI.

Here’s one way to think about it. Look at solar panel costs over time:

![](https://substackcdn.com/image/fetch/$s_!7Kfh!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a3abaaf-1db1-496c-943e-25a62725eff5_1600x1098.png)

For 50 years, we’ve been shrinking their costs by 12% per year, learning how to produce more with less. If the learning pace was faster (thanks to AI), we might have been able to reduce costs by 20% year on year, and we would have gotten to the same point 20 years earlier. At a learning pace of 30% per year, we would have gotten there 32 years earlier.

As the panels got cheaper, they also got better though! So cost, materials, efficiency, and quality all improved together.

![](https://substackcdn.com/image/fetch/$s_!zKh2!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd4bd7f26-b0cd-4b98-b0c4-6c77b9613617_2048x884.png)

What’s the limit to this improvement?

## 4\. The Idiot Index

When Elon Musk wanted to buy a ballistic missile from the Russians to go to Mars, they quoted him such a ridiculous price that on the plane home, he took his computer out, opened a spreadsheet, started calculating the cost of the raw materials, and realized they were just [2%](https://www.wired.com/2012/10/ff-elon-musk-qa/) of the total price of a rocket.

He started calling that the *Idiot Index*: If a thing costs much more than its raw materials, it means there’s some idiot here that couldn’t make it cheaper, that there was too much waste caused by human intelligence—or lack thereof.

So how much could he reduce rocket costs? Falcon Heavy [reduced](https://unchartedterritories.tomaspueyo.com/p/space-industries-are-lifting-off) [costs](https://unchartedterritories.tomaspueyo.com/p/can-we-build-ai-in-space) by 98%. Starship will further reduce costs by 93%, for a total of ~99.9%.

Of course, space companies were not very efficient—in fact, many like Boeing are just a jobs program at best, and a grift at worst—so maybe they’re an outlier. But the logic stands: An intelligent designer can cut costs so radically that raw materials become a much bigger part of the end product

![](https://substackcdn.com/image/fetch/$s_!KJPr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcafb7040-2f52-4792-9039-51caa568f978_1700x1299.png)

But one thing is to eliminate white-collar workers, and the other is blue-collar ones. Much harder, right?

## 5\. Blue-Collar Too

Another chunk of human costs is not the R&D and other white-collar jobs, but blue-collar ones. Together, they account for 25% of manufacturing companies’ costs. Will AI reduce their cost too though? Yes.

The only reason blue collar work still exists is because we haven’t yet been able to use AI to automate the workers’ movements in a cost-effective way. Many more movements could be automated with better AI design of replacement machines. Industry experts definitely think physical AI will transform many industries:

![](https://substackcdn.com/image/fetch/$s_!B_M_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9ea4281-7e3c-4511-9aa5-6db7b3de0422_2048x977.png)

*[Source](https://www.capgemini.com/wp-content/uploads/2026/05/CRI_Physical-AI-Report-Final-web-version-2.pdf)*

But some human physical skills have been just too hard to automate so far (eg, hands), so that’s what the robot industry is working on. If humanoid robots succeed in the coming years, blue collar work is likely to fall.

![](https://substackcdn.com/image/fetch/$s_!SSvr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F385f0c9e-8156-4973-96c0-83c5d5d8c945_1182x888.png)

I think it will happen in the next 2-5 years. If that sounds pretty aggressive to you, you’ll want to read the upcoming article on the topic.

## 6\. Cutting Costs Across the Value Chain

Between blue- and white-collar workers, including contractors, humans account for ~26% of manufacturing companies’ budgets. Manufacturing company A still has to spend on:

- Parts, components, packaging, and raw materials: ~62%
- Machinery: ~3%
- Energy: ~1.8%
- Maintenance, repairs, waste removal: ~1.5%
- Land and buildings: ~1.4%

So by far the biggest cost is the parts and components from their providers… Who will *also* see a reduction in their costs of ~25% (from humans)! And of course, they will become more efficient with parts and raw materials, so that part of costs will be reduced further. Let’s say company A will reduce these 62% costs by 12 percentage points. Combined with the human cost reduction, we’re at ~37%.

And since company A is in a competitive market (as most manufacturing is), this improvement will be competed away, and prices to customers will shrink by 37% on average.

Only that? No! Company A will put pressure on its providers to reduce their prices too! So Provider B will also have a reduction in costs of 37%. And its own providers will also shrink by 37%! If you push this across the entire value chain, you end up with a total cost reduction of 74%!

The remaining 25% you end up paying for is raw materials, energy, and some human work here and there, at each step to keep the AIs and robots improving.

But are energy and mining safe from the AI onslaught? I just looked into mining and based on that, I changed my investments. I’ll cover it in the next (premium) article.

What will replace these human costs?

Capital.

Manufacturing companies will need to invest in:

- Intelligence to replace the white-collar workers—so, pay for inference.
- Intelligence, plus machines and humanoid robots, to replace the blue-collar workers.

This means robot and AI companies will employ people—just not enough, in my opinion, to make up for the jobs they’ll erase.

## Takeaways: Manufacturing Moats

People tend to say that hardware is safe from AI, but it isn’t. From what I can gather:

1. AI can cut ~20%-25% of human costs in every step of the value chain, plus an additional cut on parts and materials needed.
2. This adds up to ~65-75% of all the costs across the value chain. Not all these costs will be eliminated, as some will be replaced by the cost of capital for inference and robots, so employment in these companies will growth.
3. AI will attack first management, R&D, and all other intelligence tasks.
4. Blue collar work will also be automated with AI, and that will dramatically accelerate as humanoid robots become huge, which I’ll study in an upcoming article.
5. Competition will translate these lower costs into lower prices for customers.
6. But also higher quality manufactured products!
7. This will increase the demand for manufactured products.
8. But here we’re talking about an absolute carnage in the blue- and white-collar manufacturing jobs. I think it’s unlikely that the increase in the volume of sales will outweigh the job destruction.
9. Raw materials will then take a much bigger share of the cost of manufactured products—improving the idiot index—,which makes mining an extremely important industry to understand in a world of AI. We’ll explore it in the next article.

Is there a limit to this? Well, it’s all a matter of timelines, and there are two schools of thought here.

One thinks intelligence can only take us so far. There are lots of human decision-makers across the board, vested interests, politics, slow adoption… It will take years for humans to learn to harness AI well in manufacturing. Most existing companies won’t do it well, so we’re about to experience a golden age of startups taking over the manufacturing sector by using AI to work more efficiently. But it’s hard to create mining startups. And of course, intelligence is not the same as physical movement. Humanoid robots will take a few years to arrive, and then a few years to ramp up production to get them everywhere. And in any case, manufacturing is not only about intelligence. It hits the real world of atoms. You need to test things, and that takes time and money independently from the intelligence of AIs. According to this school of thought, it might take one or two decades to see a dramatic change in the manufacturing industry.

The other thinks that AI will be able to plow through all these issues. What prevents Anthropic from creating its own manufacturing companies? From buying out the worst managed ones and implementing change at the speed of its agents? What prevents clever Private Equity companies from buying dozens of these companies with the single purpose of firing everybody and replacing them with AIs? Why would there not be any company that automates atoms testing with AI?

This debate boils down to: How much faster will manufacturing productivity improve in the coming years? If the first school wins, it will take 5-20 years for this revolution to take place. If the second school wins, it will be in the next 1-4 years.

---

∙

[^1]: *I’m a very tiny investor.*

[^2]: *As I write this in November, 2026*