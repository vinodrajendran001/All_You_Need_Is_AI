---
type: raw-source
source_id: src-2026-06-30-alisa-liu-ai-research-job-search
title: "Reflections on the AI research job search"
author: Alisa Liu (alisawuffles)
url: https://alisawuffles.github.io/blog/job-search/
captured: 2026-06-30
status: immutable
tags:
  - source/raw
  - careers
  - interview-prep
---

> Preserve the source body below this line as the canonical capture.
> Captured as clean markdown via web fetch on 2026-06-30. Author name "Alisa Liu" inferred from the alisawuffles handle and the alisa-s-book-of-llms Notion URL; the post itself self-describes a 6-year NLP PhD at the University of Washington focused (latterly) on tokenization.

# Reflections on the AI research job search

For most of my PhD, the job search in my mind was like a sorting hat: senior PhD students would disappear (for several months), then emerge with their fates decided. Even as my close friends began graduating and getting jobs, I knew little about what they were going through apart from the occasional proof of life. When it was finally my turn, I found the process to be far more demanding than I had imagined, and felt like I was learning the rules of the game while playing it.

In retrospect, a lot of my experiences were universal and many of the things I learned along the way now feel like common knowledge. I'm writing this post to share one data point for how the journey can look and hopefully make the job search a little less mysterious.

A bit of background on me. I applied for Research Scientist / Member of Technical Staff roles at the end of my 6-year PhD in NLP at the University of Washington. I spent most of my PhD not thinking much about what I would do afterwards, and I was compelled more by working on fun ideas than anything else. This led to a lot of pivoting, but fortunately I managed to keep a consistent thread in my last two years (on tokenization!), and I think establishing an area of expertise helped me stand out in the job search.

## My timeline

The figure (inspired by Nathan Lambert's post) shows interviews as gray icons and outcomes as colored circles. *Ghosted* means the recruiter never informed me about an outcome; *withdrawn* means I politely told the company I was no longer interested after receiving offers I was excited about. In total, I interviewed at 11 companies over 57 interviews. Not pictured: 46 additional recruiter calls and 16 post-offer chats, plus myriad informal networking conversations.

**Company order.** I decided when to begin each interview process through some combination of whether I felt ready, pressure from the company, how quickly I expected them to move, how excited I was, and procrastination. The common wisdom: use a few companies for practice, then time the other processes so all offers arrive at roughly the same time for negotiation. Additions to that wisdom:

- Practice interviews are helpful, but your stamina is finite — be careful not to burn out before the places you really care about.
- External factors to timing matter (whether the company has headcount, which teams are actively hiring) and can matter more than your preparation. Friends and recruiters give insight here.
- Deadlines come with flexibility, so offer timing need not be precise. But watch for "exploding" offers — investigate how much time candidates usually get to sign.

**Getting the first interview.** Do good work during the PhD, make friends, collaborate a lot. To get the first interview, sometimes you need someone inside the company vouching for you. Be social at conferences, collaborate widely, attend networking events. During the search, reach out to people you know (or don't know) and ask about opportunities — reconnecting with people you haven't talked to in years is okay, expected, and a wonderful side effect.

## Interview types

Roughly these categories. Overall, technical skills and knowledge are evaluated much more than research experience, though the latter probably gets you the interview in the first place.

**ML coding.** By far the most common. Implement a given architecture, a decoding strategy, a traditional ML algorithm, or more creative things. Being fluent in `PyTorch` is a must; in rare cases asked to use only `numpy` (e.g., writing the backward pass from scratch), but not expected to know numpy syntax.

**General coding.** Basically LeetCode, sometimes with extra flavor. Strong foundations help because the concepts show up in ML coding too.

**Technical discussion.** No coding but very technical. Sometimes an extended discussion around one topic (e.g., how you'd design experiments to answer a research question); the interviewer presses you on design choices, asks you to comment on hypothetical results, design follow-ups. In other cases, rapid-fire questions *(What are some different ways of encoding positional information? What is 5D parallelism? What is the difference between PPO and GRPO?)* to signal you know your stuff. The former tests how you think; the latter checks breadth.

**Research discussion.** The kind practiced most in the PhD. Start by telling them about a past project, the rest flows from there; they may ask about other papers on your CV. Prepare by thinking about why you worked on things, insights and opinions developed along the way, and promising future directions. Tailor the research pitch to the role; interviewers are tired, so hitting the right keywords helps them believe your profile is relevant.

**Behavioral.** Totally textbook, apart from occasional questions about AI safety or societal impacts. Enumerate memorable PhD stories and map them onto common behavioral questions so you can retrieve the right anecdote instantly. I failed my first behavioral interview because I assumed I'm obviously well-"behaved" and came up blank — it is uniquely painful to reconstruct hazy memories while delivering them, only to be told "You didn't answer the question."

**Math.** Some companies have a math interview, from fun logic puzzles to serious pen-and-paper derivations. Brush up on probability, linear algebra, and calculus.

**Job talk.** Shorter than an academic one and focused on a single paper or direction. My job talk was all about tokenizers: mostly a first-author work, then a few second-author and ongoing works briefly.

## Preparation

There is truly no better use of your time than studying for interviews. Like being back in undergrad: I took notes (see my LLM notes, worked on continuously, and my math notes, all for a single fateful interview), drew diagrams, did practice problems, and spent entire days in coffee shops understanding fundamental ML concepts inside-and-out. The job search is a full-time job.

I started by watching all the lectures from Stanford's **Language Modeling from Scratch (CS336)**, which illustrates the breadth of topics and organizes scattered concepts into one coherent picture. After the basics, I deep-dived concepts one at a time by reading blog posts & papers, talking to ChatGPT & Claude *a lot*, and practicing implementing from scratch. **Homework 1 is crucial**: implementing/debugging a transformer comes up so often that turning it into muscle memory pays off massively. **Practice coding with AI assistance completely off** to mimic interview settings (you will underestimate your reliance otherwise).

Each interview is unique and benefits from dedicated prep. Build an intuitive understanding of an interview's scope from the description, the company's interests, recruiter hints, and reputation. "Each interview is a slightly different math or CS class, you never went to lectures, and now you have ~3 days to cram for the midterm."

**Day of interview.** Nothing beats enough sleep. I did my first technical interview on 2 hours of sleep after cramming LLM inference — none of it came up, and I spent 10 minutes on an off-by-one error. Afterward, record notes for future studying and reflection.

**Side benefits.** Studying widened my breadth, improved confidence as a researcher, made me more secure in conversations, and — amazingly — made me enormously more effective at my ongoing project, unlocking technical ideas I couldn't access before.

## Negotiation

The work is not done after offers. There is a (potentially extended) period to learn more and negotiate: conversations with future teammates/managers, lunch visits, recruiter calls. Negotiating is hard; nothing in the PhD prepared us, and unlike interviews it can't be conquered by studying. You are outmatched in market knowledge and negotiation skill. Even if you'd be happy with your offer independent of comp, you'd be doing yourself a disservice not to negotiate — initial offers leave room by design ("I don't expect you to take our first offer"). A few weeks of energy here can equal years of work at the initial offer. Lean on friends for know-how and data points. Before every recruiter call, write down what you will and won't share, plus verbatim quotes; anticipate their questions and construct comfortable responses that still advocate for yourself.

## Concluding words

A huge part of the experience is managing the emotions of being on the market: social perception, comparing yourself to peers, everyone having opinions, a huge decision space with incomplete information where small choices have outsized impact. I was stressed and miserable for several months — if that's you, you are not alone. Cherish the PhD for the unique time it is; I consistently did my best work when having fun and chasing questions my mind would not lay to rest.

## Appendix: learning resources

- LeetCode 75 / Neetcode Blind 75
- Stanford CS336: Language Modeling from Scratch
- Self-Attention & Transformers (CS224n reading)
- The Illustrated GPT-2 (Jay Alammar)
- Backpropagation (CS231n optimization-2)
- Introduction to Policy Gradient for LMs (Hamish Ivison)
- Lightweight Guide to understanding GRPO and RL principles
- How to Scale Your Model (JAX scaling book)
