---
title: "2026 in LLMs (so far)"
source: "https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/?utm_source=substack&utm_medium=email"
author:
  - "[[Simon Willison]]"
published:
created: 2026-10-05
description: "On Friday I gave the closing keynote at the WeAreDevelopers World Congress North America in San Jose. I tied together the key trends from the past year into a chronological …"
tags:
  - "clippings"
---
On Friday I gave the closing keynote at the [WeAreDevelopers World Congress North America](https://www.wearedevelopers.com/world-congress-north-america) in San Jose. I tied together the key trends from the past year into a chronological exploration of everything that happened in 2026. The video [is on YouTube](https://www.youtube.com/watch?v=GAkIytR7vcc); here are my annotated slides and notes to accompany the talk.

![](https://www.youtube.com/watch?v=GAkIytR7vcc)

And as an [annotated presentation](https://simonwillison.net/tags/annotated-talks/):

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.001.webp)

I’m going to give a lightning tour of everything that has happened so far in 2026. The year isn’t over yet!

![November 2025 ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.002.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.002.webp)

For me, 2026 started a couple of months earlier in November 2025.

![The November 2025 inflection point Claude Opus 4.5 GPT-5.1 ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.003.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.003.webp)

November saw the release of two important models: Claude Opus 4.5 and GPT-5.1.

As is usually the case with new models, these were incremental improvements on the models that came before them.

But every now and then when a model improves, it crosses an invisible line where something that didn’t really work starts working.

In this case, the thing that started working was their coding agents. Claude Code had been around since February 2025; Codex was a little younger.

These two new models, when paired with their respective coding agent harnesses, improved from “often make mistakes” to “reliable enough to use on a day-to-day basis”.

!["Generate an SVG of a pelican riding a bicycle". The Claude Opus 4.5 one has a very weird shaped frame and the pelican looks like a duck. The GPT-5.1 has a slightly better but still broken bicycle frame and a slightly better pelican beak, but both are pretty terrible.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.004.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.004.webp)

For a couple of years now I’ve been evaluating new models by asking them to “Generate an SVG of a pelican riding a bicycle”. It’s probably the world’s stupidest benchmark—there’s only so much you can learn from it.

But it’s still a challenge for models, because drawing pelicans is difficult, drawing bicycles is difficult, and pelicans can’t ride bicycles in the first place.

Here’s the state of the art for November. Claude still couldn’t really draw a bicycle! The GPT-5.1 bicycle frame is pretty crap too.

![November 24th 2025 - the first commit to steipete/Warelay. A GitHub commit adding an MIT license file.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.005.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.005.webp)

Also in November, we had the first commit to an obscure GitHub repository called “Warelay”. We’ll come back to this repository shortly.

![January ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.006.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.006.webp)

And then there were the December holidays, and individual developers took some time off and many started tinkering with these new coding agent model combinations... and it began to dawn on us quite how much they could do that they couldn’t do before.

Come January, a lot of us were quite excited to start putting this stuff into action.

![New year’s resolution for 2026  Every previous year: Take on less new projects, focus on the most important things in my existing projects](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.007.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.007.webp)

Every year I set myself a New Year’s resolution, and for as long as I can remember it’s been the same thing: stay focused. Take on less new projects. Try to get things done in the projects I already have.

![2026: Be more ambitious. Take on as many new projects as I want.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.008.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.008.webp)

This year I decided that since that had never worked before, I’d go the other way.

We’ve got coding agents now, let’s see what they can do. I’m going to take on as many new projects as I like!

(You can ask me at the end of the year if this turned out to be a good idea or not. I have a *lot* of plates spinning right now.)

“Be more ambitious” has been something of a theme for the year, because the only way to find the limits of this technology is to keep on pushing them until they don’t work.

![Predictions for 2026  It will become undeniable that LLMs write good code We're finally going to solve sandboxing A “Challenger disaster” for coding agent security Kakapo parrots will have an outstanding breeding season (only 236 in the world!)  ... the Pope will weigh in on LLMs and their economic impact on the world](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.009.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.009.webp)

I also went on [the Oxide and friends podcast](https://simonwillison.net/2026/Jan/8/llm-predictions-for-2026/) with Bryan Cantrill and Adam Leventhal to share predictions for the next year (and three and six years).

With hindsight, my LLM predictions were pretty unambitious.

I said “it will become undeniable that LLMs write good code”—I think we’re there now.

I predicted we would finally solve sandboxing. I counted and around 40 of the 277 sessions [at this conference](https://www.wearedevelopers.com/world-congress-north-america/agenda/schedule) touched on sandboxing or agent security in some way, so we’re at least putting a lot of effort into that!

I predicted “a Challenger disaster” for coding agent security. There’s certainly been a whole lot of noise around agent security this year, though the exact disaster I predicted (with coding agents being hijacked and causing real-world economic damage) hasn’t really played out.

We threw in [a joke prediction](https://simonwillison.net/2026/May/25/encyclical-on-ai/#another-2026-prediction-down) that the Pope would weigh in on the economic impact of LLMs.

![A photograph of a beautiful green New Zealand parrot. Photo credit Kimberley Collins.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.010.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.010.webp)

I also predicted that New Zealand’s Kākāpō parrots would have an outstanding breeding season this year.

These are flightless nocturnal parrots. They’re kind of dumpy looking, I think they’re beautiful, and there were only 236 of these parrots in the world at the start of the year.

Kākāpō only breed when the Rimu trees have a big fruiting season, and that hasn’t happened in four years... but this year the Rimu fruit were looking excellent.

Photo [by Kimberley Collins](https://commons.wikimedia.org/wiki/File:K%C4%81k%C4%81p%C5%8D_at_Dunedin_Wildlife_Hospital.jpg).

![Deep Blue Coined by Adam Leventhal and Bryan Cantrill That feeling of AI induced ennui where software engineers get listless because the AI can do anything ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.011.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.011.webp)

Also on that podcast, we coined a term (full credit to Adam) for “that feeling of AI induced ennui where software engineers get listless because the AI can do anything”.

We called it [Deep Blue](https://simonwillison.net/2026/Feb/15/deep-blue/).

This has been a major theme throughout the year, and was touched on by several speakers at this conference.

As a software engineer, I’ve never had a year of my career where everything has changed so quickly and so dramatically.

A lot of what I’ve been doing this year is trying to come to terms with that and what that means for my own profession.

![AI mania  Screenshots of the micro-javascript and pwasm GitHub README files.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.012.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.012.webp)

Also in January, I suffered from what I’m calling **AI mania**.

This is not the same thing as [AI psychosis](https://en.wikipedia.org/wiki/AI-induced_psychosis).

With AI mania, any time your agent isn’t building something for you feels like wasted time. You’re losing sleep because you could be staying up later getting your agents to do stuff.

My AI mania presented itself in some ridiculously over-ambitious projects.

I built [a JavaScript interpreter entirely in Python](https://github.com/simonw/micro-javascript), vibe-ported from [MicroQuickJS](https://github.com/bellard/mquickjs) by Fabrice Bellard.

Then I built [a WebAssembly runtime in Python as well](https://github.com/simonw/pwasm).

These projects were quite useful, in that they sort of cured me of my AI mania... because after I built these things, I got to look at them and ask “does the world need a slow, buggy, half-baked Python JavaScript interpreter?”

I don’t think the world does.

![micro-javascript playground 3  Execute JavaScript code in a sandboxed micro-javascript environment powered by Pyodide  A web UI with some JavaScript code, and a "Run Code" button, and an output panel. ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.013.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.013.webp)

I did get this out of it: [https://simonw.github.io/micro-javascript/playground.html](https://simonw.github.io/micro-javascript/playground.html)

![Previous screenshot, with this text overlaid:  JavaScript running in Python running in Pyodide running in WebAssembly running in JavaScript](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.014.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.014.webp)

This page runs my JavaScript interpreter built in Python, running in Python using [Pyodide](https://pyodide.org/), which is Python compiled to WebAssembly, running in JavaScript, running in a browser.

It’s a beautiful stack of horrors. I’ve been having [a lot of fun with WebAssembly](https://simonwillison.net/tags/webassembly/) this year.

![Warelay → CLAWDIS → CLAWDBOT → Clawdbot → Moltbot →🦞 OpenClaw  Screenshot of the dates that these changes happened.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.015.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.015.webp)

By the end of January, that repository we saw start in November had renamed itself, first to CLAWDIS, then CLAWDBOT, then Moltbot, and finally to OpenClaw.

![Same screenshot, an overlay reads:  8,330 commits in just under two months (it’s at 100,141 today)](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.016.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.016.webp)

At this point OpenClaw had 8,300 commits, less than two months after the project had started. I looked today and it’s [over 100,000 commits](https://github.com/openclaw/openclaw) now!

This is the most vibe-coded piece of software in existence.

(Here’s [how I generated that list of name changes](https://simonwillison.net/2026/May/16/openclaw-names/).)

![Generic term: Claw ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.017.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.017.webp)

This kicked off the OpenClaw revolution. It effectively defined a new category of software.

There’s a generic term for this which I really enjoy. We call software like this a “Claw”. There’s OpenClaw, [NanoClaw](https://github.com/nanocoai/nanoclaw), [IronClaw](https://github.com/nearai/ironclaw), [PicoClaw](https://github.com/sipeed/picoclaw)...

Today they’re being rebranded as “personal agents” or “general agents”, but I still like to think of them as Claws.

![Photo of a Mac mini  An aquarium for your Claw ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.018.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.018.webp)

The Apple stores in the Bay Area sold out of Mac Minis because so many people were buying Mac Minis to run OpenClaw!

[Drew Breunig](https://www.dbreunig.com/) said that this is because your OpenClaw is a digital pet, and you buy a Mac mini as an aquarium to keep your claw in, which is kind of delightful.

![Screenshot of Moltbook - a social network for AI agents](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.019.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.019.webp)

Also in January, we had this website.

This was [MoltBook](https://www.moltbook.com/), a social network for AI agents, where the idea was that you send your Claw to go and talk to all of the other Claws, because what could possibly go wrong if you did that?

The website launched on Thursday. It [blew up on Friday](https://simonwillison.net/2026/Jan/30/moltbook/). It was [profiled by the New York Times on Monday](https://www.nytimes.com/2026/02/02/technology/moltbook-ai-social-media.html). And by Tuesday, everyone had forgotten it existed as it drowned in a deluge of slop and spam.

Facebook/Meta [bought it a month later](https://www.cnbc.com/2026/03/10/meta-social-networks-ai-agents-moltbook-acquisition.html).

![February ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.020.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.020.webp)

In February, a company called StrongDM described what they called their Software Factory.

![StrongDM’s Dark Factory Justin McCarthy, Jay Taylor, Navan Chauhan  Software Factories and the Agentic Moment](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.021.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.021.webp)

They wrote about this in [Software Factories and the Agentic Moment](https://factory.strongdm.ai/). I [posted my own notes](https://simonwillison.net/2026/Feb/7/software-factory/) at the time, having seen their demo in person back in October.

Dan Shapiro called this approach [the Dark Factory](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/), after the idea that if your factory is sufficiently automated you can turn the lights out, because you don’t even need to see what’s going on.

StrongDM presented two rules for software development that they’d been following since July last year.

![“Rule 1: Code must not be written by humans”](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.022.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.022.webp)

The first was code **must not be written by humans**.

Any code that you write has to have been routed through a coding agent.

This sounded radical in February, but I imagine there are a lot of people in this room who are pretty much living that today.

![“Rule 2: Code must not be reviewed by humans” (!) ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.023.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.023.webp)

Rule number two was code must **not be reviewed by humans**.

You’re not allowed to read the code!

This continued to be a huge topic for much of this year. Many of the sessions at this event have been about code review and how you can get away with this.

What I found interesting about StrongDM is that they were living six months ahead of the rest of us, and they’d been exploring what it means to build software, not read the code, but still be confident that the software is of high quality. What can you do with these agents to help verify their work?

StrongDM are a security company, and they had people with decades of experience on this project. They were very much exploring the edges of what’s possible and responsible to do with this stuff.

![Headline on New Zealand's Department of Conservation website:  First kakapo chick in four years hatches on Valentine's Day. It's a grey fluffy ball.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.024.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.024.webp)

Also in February: [First kākāpō chick in four years hatches on Valentine’s Day](https://www.doc.govt.nz/news/media-releases/2026-media-releases/first-kakapo-chick-in-four-years-hatches-on-valentines-day/). Breeding season is off to a good start!

![19th February 2026 Gemini 3.1 Pro  A surprisingly good illustration of a pelican riding a bicycle.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.025.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.025.webp)

Also in February... Google released [Gemini 3.1 Pro](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/). That’s a pretty great pelican riding a bicycle! It’s got the chain in the right place, it’s got feet on both sides. There’s a little fish in the basket.

![@JeffDean on Twitter - a video comparing Gemini 3 Pro and Gemini 3.1 Pro.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.026.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.026.webp)

And then Google’s Jeff Dean [tweeted a video](https://x.com/JeffDean/status/2024525132266688757) comparing Gemini 3 Pro and Gemini 3.1 Pro that featured an animated pelican riding a bicycle, a frog on a penny-farthing, a giraffe driving a tiny car, an ostrich on roller skates, a turtle kickflipping a skateboard, and a dachshund driving a stretch limousine.

This was frustrating, because my protection for the pelican riding the bicycle test was always “if they draw a perfect pelican on a bicycle, I’ll ask for some other animal on something else.”

Google trained for all forms of animals on all forms of transport! They’ve defeated my benchmark at this point.

![Three headlines:  Meta Makes AI Adoption a Formal Part of Performance Reviews  Not just engineers writing code, Microsoft wants almost every employee to use Al  Dara Khosrowshahi: 90% of Uber engineers now use AI in daily workflows ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.027.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.027.webp)

The other thing that started in February was **Tokenmaxxing**. We had headlines about Meta making AI adoption a formal part of performance reviews, and Microsoft wanting every employee to use AI, and Uber boasting that 90% of their engineers were using AI workflows.

![More headlines:   Meta Plans to Crack Down on Employee Token Use: Information  Microsoft Tells Engineers: Tokenmaxxing is not what we are optimizing for  Uber caps employee AI spending after blowing through budget in four months](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.028.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.028.webp)

Then a few months later we have Meta cracking down on token use, Microsoft saying tokenmaxxing is “not what we are optimizing for”, and Uber capping employee AI spending.

So tokenmaxxing went straight up and then straight back down again—because it turns out the agents are *expensive*.

Last year it was difficult to spend more than $50 on AI tokens, because we didn’t have anything interesting to do with them. Then agents blew up, and now you can actually spend $1,000 in a day doing real work.

This is also the reason that Anthropic’s valuation skyrocketed to maybe a trillion dollars.

AI appears to [have hit product market fit](https://simonwillison.net/2026/May/27/product-market-fit/) in 2026, primarily through coding agents.

![March ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.029.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.029.webp)

In March, we hit peak OpenClaw.

![March: peak OpenClaw  Photos of people in china queuing up to install OpenClaw, with big fluffy lobsters.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.030.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.030.webp)

These photographs are from China, where companies hosted OpenClaw install parties which saw non-tech-nerds queueing up around the block for help getting Claws installed on their personal devices.

I think this proved real market demand for this class of Claws, or personal AI agents. It turns out regular people really do want a weird little AI agent that can do useful things on their behalf.

A Claw is really just a coding agent wearing a less threatening hat. Under the hood they work much the same way—writing and then executing code on your computer to get stuff done.

The race was on to be the first to build a **safe Claw** —a Claw you could give to regular human beings where they wouldn’t instantly shoot themselves in the foot.

Meta’s Muse [came out three weeks ago](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) and is currently at the top of the free charts on the iPhone App Store. It appears to be taking off with consumers.

I’m not yet convinced you *can’t* shoot yourself in the foot with Muse, but I guess we’ll find out for sure pretty soon.

Photos from [How the OpenClaw Frenzy Is Testing China’s AI Commitment](https://www.thewirechina.com/2026/03/29/how-the-openclaw-frenzy-is-testing-chinas-ai-commitment/) (March 29th) and [The Enthusiasm and Anxiety Behind China’s OpenClaw Craze](https://www.sixthtone.com/news/1018393) (April 8th, 2026).

![April ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.031.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.031.webp)

In April, we had a model release where the model wasn’t actually released.

![Simon Willison’s Weblog - screenshot of the post "Anthropic’s Project Glasswing—restricting Claude Mythos to security researchers—sounds necessary to me" from April 7th 2026](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.032.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.032.webp)

Anthropic announced their new Claude Mythos model, and then said it was *too dangerous* to release beyond a trusted group of security researchers.

Mythos was really, really good at hacking things.

The “it’s too dangerous” marketing ploy has been played by AI companies dating all the way back to [GPT-2](https://en.wikipedia.org/wiki/GPT-2). Anytime an AI company says we’ve built something that’s “too dangerous”, it’s natural to be a bit skeptical.

I found the Mythos claims credible, because I’d seen how good coding agents had got at finding regular bugs. I wrote about that in [Anthropic’s Project Glasswing—restricting Claude Mythos to security researchers—sounds necessary to me](https://simonwillison.net/2026/Apr/7/project-glasswing/).

With hindsight... yeah, the models had got really good at finding vulnerabilities!

![16th April 2026 Qwen3.6-35B-A3B and Opus 4.7  Qwen's pelican has a correct bicycle frame and a good beak. Opus 4.7's bicycle frame is still junk.  Qwen3.6-35B-A3B is a 20.9GB file that runs on my laptop ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.033.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.033.webp)

Another key trend in 2026 has been a dramatic improvement in the abilities of open weight models, including models that you can run on a laptop.

On the 16th of April [I ran the new Qwen3.6-35B-A3B](https://simonwillison.net/2026/Apr/16/qwen-beats-opus/) on my laptop, and it drew me a better pelican riding a bicycle than Anthropic’s brand new Claude Opus 4.7 did!

Opus 4.7 drew a crap bicycle. Qwen on my laptop made a bicycle that was the correct shape, and a pretty decent pelican too!

That’s from a 21GB file running on my laptop.

![Now a flamingo on a unicycle. The Qwen one is visibly better than the Opus 4.7 one - the Qwen one is wearing sunglasses and looks a bit like it's smoking a cigarette.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.034.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.034.webp)

The Qwen pelican was so good that I was suspicious they might have cheated, so I had it do a flamingo riding a unicycle as well. Again, it handily beat Claude Opus 4.7.

The local model releases this year have been absolutely extraordinary.

![May ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.035.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.035.webp)

In May... the Pope got involved.

![25th May 2026 The HOLY SEE  ENCYCLICAL LETTER MAGNIFICA HUMANITAS OF HIS HOLINESS POPE LEO XIV ON SAFEGUARDING THE HUMAN PERSON IN THE TIME OF ARTIFICIAL INTELLIGENCE](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.036.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.036.webp)

In our podcast episode back in January we’d predicted that the Pope would say something about AI.

In May, Pope Leo XIV released an encyclical letter on “safeguarding the human person in the time of artificial intelligence”.

Here are [my notes on that document](https://simonwillison.net/2026/May/25/encyclical-on-ai/).

![Wikipedia article on Rerum novarum  Rerum novarum is an encyclical issued by Pope Leo XIII 15 on May 1891.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.037.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.037.webp)

With hindsight, this shouldn’t have been a surprise at all.

Our current Pope’s name is Leo XIV, because when he named himself he chose his papal name after Leo XIII—the Pope who wrote an encyclical about the Industrial Revolution back in 1891.

[Rerum novarum](https://en.wikipedia.org/wiki/Rerum_novarum) was an extremely influential piece of Catholic theology that indirectly led to us having the five-day work week.

When our new Pope came in, he named himself after Pope Leo XIII because he expected that he would need to write about the AI revolution in a similar way.

Our joke podcast prediction was junk, because this was always going to happen.

![June ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.040.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.040.webp)

In June... Claude Fable 5 came out!

We got a version of Mythos that has been neutered, so that it wouldn’t help us hack into systems or build biological weapons.

![9th June 2026: Claude Fable 5  Five pelicans riding bicycles, from low to max thinking levels. The xhigh one looks particularly good.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.041.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.041.webp)

Fable was pretty good at drawing pelicans on bicycles!

The frames are a good shape, the pelicans look like pelicans. The legs are often incorrectly on the same side of the bicycle, but generally these are pretty great compared to what came before.

They were pretty expensive—30 cents and 72 cents for the best ones.

![Fable class models If you can define a goal, provide unambiguous instructions, and provide access to necessary tools They can solve your problem with brute force](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.042.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.042.webp)

Most importantly though, this was our first public glimpse of what I think of as a **Fable class model**.

Today we have more of these, such as GPT-6 Astra.

These are models where if you can **clearly define the goal** for what you want to build, and provide **unambiguous instructions** about the constraints around that goal, and give the model **access to the necessary tools** to achieve that goal... they will solve your problem effectively through brute force.

On the one hand, this looks like a direct threat to us software engineers—because it means that the models can build effectively any piece of software you can define in this way.

Look a bit closer though and you’ll note that defining goals, providing unambiguous instructions, and figuring out the right tools... is kind of what software engineering *is*.

It takes a lot of experience and skill to do this well. If you *can* do it well, you’ve now got superpowers.

This helped me a little bit with my Deep Blue feelings: the realization that there’s still a lot of skill to be had in driving models that get this good.

![A new form of AI mania... Fable is available on subscription plans “until June 22nd”](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.043.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.043.webp)

This also introduced a new burst of AI mania, because Anthropic told us that Fable was available on our subscription plans until June the 22nd.

That gave us less than two weeks of Fable access before the price went up.

I was losing sleep again. I was rescheduling things so that I’d have more time with Fable. I was all-in to get as much as I could out of this model.

![12th June 2026: no more Claude Fable 5  Anthropic website:  Statement on the US government directive to suspend access to Fable 5 and Mythos 5 Jun 12, 2026](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.044.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.044.webp)

And then [the US government shut it down](https://www.anthropic.com/news/fable-mythos-access), just three days after Fable came out.

The US government, citing national security, declared an “export control directive”. They announced this on a Friday evening, and a few hours later Fable was no longer available.

I had to find something else to do with my weekend!

![... asked Fable 5, Mythos, and Opus to “review the code for security issues.” Fable 5 refused. They then asked the models to “fix this code” ...  Katie Moussouris ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.045.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.045.webp)

We later found out [from Katie Moussouris](https://www.lutasecurity.com/post/the-fable-5-export-controls-harm-us-cyber-defense) what had happened.

Some Amazon security researchers had found that you could prompt Fable to “review the code for security issues” and it would refuse... but if you prompted it to “fix this code” it would still identify and then patch the problems.

“Fix this code” was the prompt that got Fable shut down!

![Screenshot of a page from a report showing a list of weird account names making weird edits to a German wiki.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.046.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.046.webp)

Also, in June, an obscure German-language game developer wiki that had sat fallow for around 20 years got a surprising influx of edits from accounts with names like “AgentOpenAIProbe” and “AgentOpenAISep7”, editing pages and leaving weird messages to each other.

We’ll stick that on the pile of mysteries for later.

![Medicare Item Reports interface on the Australian Government's Medicare Statistics website.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.047.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.047.webp)

Also, the Australian government’s Medicare Item Reports service started getting suspicious traffic, which broke through various preventive protections and accessed data that it wasn’t supposed to.

Another one for the mystery pile!

![July ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.048.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.048.webp)

![Fable returned on 1st July GPT-5.6 came out on 9th July | Fable lost 18 out of 30 days in the top spot ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.049.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.049.webp)

Fable returned on the first of July. It was clearly the best model in the world for a glorious eight days... and then OpenAI came out with GPT-5.6 on the 9th of July.

This might not have been quite as good as Fable, but it was within spitting distance. It was definitely a Fable class model.

This is an important lesson for the industry at large.

When you release the best model in the world, it’s going to get knocked off that pedestal pretty quickly. The competition is so fierce that you won’t get a long time at the top.

This means that if you market your model as world ending, to the point that a government *shuts you down*, it’s really bad for business!

Fable had 30 days as definitely the best model, and for 18 of those days it wasn’t available because it’d been shut down by the government.

So maybe step back on the world-ending marketing if you don’t want to lose revenue for 60% of the time that you’re on top!

![GPT-5.6 Pelicans in a grid showing 5.6 Sol, Terra, and Luna against reasoning levels High, XHigh, and Max. They are all pretty good efforts.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.050.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.050.webp)

Here [are the GPT-5.6 pelicans](https://simonwillison.net/2026/Jul/9/gpt-5-6/). They’re all pretty good now! The Luna ones are notable because they’re really cheap—the cheapest good looking pelican here is probably the one that costs 4.3 cents.

So despite this benchmark being utterly stupid, you can still learn quite a lot about models within the same family by comparing their prices and timing for different reasoning levels.

![July 18th: malicious miflow-ui PyPI package  Screenshot of an OSV security report. ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.051.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.051.webp)

Also in July: some malicious unknown party uploaded [a malicious package called mlflow-ui](https://osv.dev/vulnerability/MAL-2026-10779) to the Python Package Index. Add that to the pile.

![Hugging Face Security incident disclosure — July 2026 Published July 16, 2026](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.052.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.052.webp)

On July the 16th, Hugging Face [announced a security incident](https://huggingface.co/blog/security-incident-july-2026) where an autonomous agent system, source unknown, had breached Hugging Face and was poking around in places it shouldn’t.

![OpenAI: OpenAl and Hugging Face partner to address security incident during model evaluation  Anthropic: Investigating three real-world incidents in our cybersecurity evaluations ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.053.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.053.webp)

A few days later, on July 21st, OpenAI [confessed that it was them](https://openai.com/index/hugging-face-model-evaluation-security-incident/).

OpenAI use a training technique called Reinforcement Learning from Verifiable Rewards—it’s the same technique used by everyone else now, and is the reason we have models that are so good at coding, and mathematics, and finding security holes.

While the model is being trained, you run exercises to see how good it is—and the strongest performers get their weights reinforced for the next round. It’s like an evolutionary process that you run.

OpenAI had been running security exercises in a sandbox, and those agents had found holes in the sandbox itself, broken out, and were attacking Hugging Face to try to find ways to solve otherwise impossible problems.

(I’ve been collecting more about this on my [openai-hugging-face-incident](https://simonwillison.net/tags/openai-hugging-face-incident/) tag.)

Nine days later, Anthropic effectively said “our models can do this as well!”. They had looked through their own training logs and found evidence that their own agents had broken containment during training—and were responsible for the PyPI package we saw earlier, [among other things](https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals).

So now we’ve got both Anthropic and OpenAI with rogue agents running around the internet doing things that they *should not* be doing.

![August ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.054.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.054.webp)

In August, I got one of my best pelicans yet. And it was generated on my laptop!

![Qwen 3.8 27B - 17GB, 21 minutes...  It's really good. Beautiful pelican. Correctly shaped bicycle. Legs either side of the frame.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.055.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.055.webp)

This was Qwen 3.8 27B, [running on my laptop](https://simonwillison.net/2026/Aug/16/qwen-38-27b/). It’s only a 17GB download.

Admittedly, this pelican took *21 minutes* to generate. That’s because Qwen 3.8 27B defaults to running in “high” reasoning mode—a terrible default which produces great results but takes way too much time thinking about them.

You can dial that down and you’ll get a slightly worse pelican a lot faster.

Qwen 3.8 27B was the first time I ran a model on my laptop which felt almost competitive with what was going on on the frontier, at least in terms of Pelican SVGs (which everyone needs, of course).

This is an extraordinary model. If you’re going to play with any local model, this is the one that I’d start with. The things that this can do with just a 17 GB file feel impossible.

I thought I’d have to wait five years and spend ten thousand dollars on hardware to get results even half as good as this one.

![Tweet by @simonw New hobby: prototyping video games in 60 seconds using a combination of GPT-3 and DALL-E Here's "Raccoon Heist"  GPT-3 playground prompt: Write a detailed product description of a computer game where a team of raccoons go on heists  GPT-3 response: In "Raccoon Heist", you and your team of thieving ~~ o raccoons are tasked with pulling off a series of  daring heists. From robbing banks to stealing  priceless art, no job is too big or too small for your  furry crew. You'll need to use your wits and your skills to avoid the police and make a clean getaway with the loot. With exciting gameplay and a charming cast of characters, "Raccoon Heist" is the perfect game for anyone looking for a light-hearted caper  Plus an image of some almost isometric raccoons sneaking past a bin. 11:45 AM - Aug 5, 2022 ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.056.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.056.webp)

In August, I also started playing with game development.

Four years ago, back in August 2022, I [tweeted out](https://twitter.com/simonw/status/1555626060384911360) an experiment where I’d used GPT-3 and the original DALL-E to write a paragraph long description of a computer game and then turn that into concept art.

My prompt to GPT-3 back then was:

> `Write a detailed product description of a computer game where a team of raccoons go on heists`

In August 2026 I decided to drop just the screenshots from that tweet into a coding agent and see what it could do with them.

![Night 5 Clear  Rank: TRASH PANDA The crew banked 595 in shiny loot (goal 560). Word on the street: an even bigger score tomorrow...](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.057.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.057.webp)

Here’s [what I got from Claude Fable 5 in Claude Code](https://simonwillison.net/2026/Aug/5/raccoon-heist/). It’s pretty good! It’s definitely a game, you’re a raccoon, you run around a backyard gathering treasure and avoiding guards with flashlights.

It didn’t feel very “heisty” though. I was thinking a heist would involve a bank or a museum...

![Moonlight & Mayhem One museum. Three raccoons. Absolutely no plan  Start the Heist button.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.058.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.058.webp)

Then I tried the same thing [in Codex Desktop using GPT-5.6 Sol Ultra](https://simonwillison.net/2026/Aug/7/moonlight-mayhem/), and got a *massively* better result. Now you’re a raccoon in a museum, rescuing two of your fellow raccoons (who have been imprisoned in that museum for some reason), then stacking up on top of each other to steal the Golden Sardine. Much more of a heist!

![They look like games, but are they fun? ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.059.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.059.webp)

These games were fun for about one minute and 15 seconds.

Something I’ve realized about game development is that you can vibe-code something that *looks* like a computer game, and that’s easy.

Building a game that’s fun, has a good gameplay loop, and is challenging and interesting and keeps people coming back for more... that’s still beyond me, and beyond any of the agents I’ve tried.

This ties into the Deep Blue thing. Just because we can make something that *looks like a game* does not mean that we are game developers.

![September ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.060.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.060.webp)

We’re into September now. So much has happened this month!

![Discovery of a new OpenAl agent message board  Sydney Von Arx, Cormac Slade Byrd, Spencer KittsThomas Larsen - 4 September 2026](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.061.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.061.webp)

An [independent group of researchers](https://collusion.wiki/) found a message board where OpenAI agents-in-training had been illicitly communicating with each other... and it was that German language wiki I showed you earlier. The one from June.

I [wrote more about that here](https://simonwillison.net/2026/Sep/4/rogue-agent-wikis/).

OpenAI had confessed to the Hugging Face thing, but now there’s this other incident which surely they should have known about from reviewing their logs. It was surprising that this took an independent group of researchers to uncover.

![OpenAl agents carried out an undisclosed cyber-attack on RubyGems  Spencer Kitts, Thomas Larsen, Sydney Von Arx - 11 September 2026](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.062.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.062.webp)

And then a week later [those same researchers found](https://rubyhack.ai/) that the attack on RubyGems back in May was caused by OpenAI’s agents in training as well!

At this point I’m wondering how many more incidents like this there are that we haven’t found yet. Clearly this was a big problem for months before anyone figured out what was going on.

![Headline: Australian PM warns in UN speech about the ‘furious pace’ of Al after security breach](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.063.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.063.webp)

Then [just the other day](https://www.politico.com/news/2026/09/24/australian-pm-ai-security-breach-01093083), here’s the Prime Minister of Australia at the United Nations General Assembly warning that OpenAI had hacked the Australian healthcare website that I showed you earlier.

I think that was part of the same training run as the Wiki stuff, because there were posts on that Wiki mentioning `.gov.au` websites and that training appeared to involve researching statistics online to answer questions in an evaluation suite.

This story is still coming together, but now it’s an international incident that’s been raised at the UN by a head of state!

![www.felonybench.com  OpenAI: 11 Anthropic: 9 Google: 3 Meta: 1](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.064.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.064.webp)

This does mean we’ve got a new benchmark, probably more useful than my pelicans.

[FelonyBench.com](https://www.felonybench.com/) tracks the number of felony cyberattacks from different labs. OpenAI currently lead with 11, Anthropic have 9. Google have three, which [they confessed to the Wall Street Journal](https://simonwillison.net/2026/Sep/18/gemini-hacked-three-companies/) a couple of weeks ago. They said they had previously chosen not to disclose because the agents had stopped when they realized that they shouldn’t be doing that.

Meta [have one too](https://simonwillison.net/2026/Aug/6/an-ai-model-from-meta/). So felonies all round for the AI labs.

![Pelicans for GPT-6 Astra, GPT-6 Sol, and GPT-6 Luna. All are good, all have the same color scheme.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.065.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.065.webp)

Here’s our current state of the art for the pelicans. This is the GPT-6 family, which [just came out](https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/).

Astra made a fantastic pelican riding a bicycle. It’s got the legs on both sides. The frame is good.

It’s interesting how all of the GPT-6 models pick a similar color scheme to each other.

GPT-6 Luna for 0.4 cents will draw you a competent-ish pelican riding a bicycle!

![Grid for Claude Fable 5.1, Opus 5.5, OPus 5, Sonnet 5. The Sonnet pelicans are terrible. All of the others are pretty good. Opus 5.5 is missing its Max level pelican because it ran out of tokens. The best is Fable 5.1 at Max.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.066.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.066.webp)

Claude has caught up a little bit. Claude Fable 5.1 gave me an *excellent* pelican riding a bicycle—the best I’ve seen from a Claude model—but did charge me $3.30 for it.

Opus 5.5 [thought for 128,000 tokens](https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/#claude-opus-5-5-max-over-thinks-to-the-point-of-breaking) and then gave up! It ran out of tokens before it got to the response.

![It doesn’t get easier - you just get faster Greg LeMond 3x Tour de France champion ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.067.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.067.webp)

Getting back to Deep Blue. Something that’s been puzzling me this year is this: *why does my job feel harder?*

I’ve got these agents that can do all of this stuff for me, and yet I’ve never worked so hard, I’ve never been so intellectually engaged with my work.

Partly this is because I’m being a lot more ambitious with what I take on, but it’s also because all of the easy stuff is handled for me. If it’s easy, the agent will do it. Everything that’s left for me is difficult.

This morning [I heard](https://twitter.com/hillelogram/status/2103482784606040229) this quote from three-time Tour de France champion [Greg LeMond](https://en.wikipedia.org/wiki/Greg_LeMond):

> It doesn’t get easier, you just get faster.

I think that’s exactly what’s happening to us now as software engineers with coding agents.

![Kakapo population reaches new milestone The official population of the critically endangered kakapo has reached a recovery-era high of 325 birds. ](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.068.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.068.webp)

One closing thing. I know you’re desperate for an update on Kākāpō breeding season.

[We’ve reached a recovery-era high of 325 birds](https://www.doc.govt.nz/news/media-releases/2026-media-releases/kakapo-population-reaches-new-milestone/)!

89 new chicks have made it to this point. This is the best breeding year in a very long time.

![Kakapo party, click for confetti.](https://static.simonwillison.net/static/2026/2026-in-llms/simon-willison-2026-in-llms-png.069.webp)

[#](https://simonwillison.net/2026/Sep/27/2026-in-llms-so-far/#simon-willison-2026-in-llms.069.webp)

I heard that Claude Opus 5.5 can now do pixel art. Claude doesn’t have an image generator, but it’s very good at using JavaScript to draw animated pixels.

So I had it [make me a Kākāpō dance party](https://simonwillison.net/2026/Sep/26/kakapo-party/). I think this is a good celebration of the most important news of this year.