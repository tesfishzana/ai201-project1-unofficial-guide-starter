# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Off-campus survival guides for college students who work part-time. This domain covers the practical, day-to-day knowledge that working students need but can't find in one place: budgeting on minimum wage, finding apartments, balancing work shifts with class schedules, meal prepping on a tight budget, staying safe in off-campus housing, avoiding burnout, and navigating employer tuition benefits. This knowledge is valuable because it's scattered across dozens of Reddit threads, personal finance blogs, and student life articles — and university websites almost never address the reality of students who must work to survive.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Fastweb | College housing options: dorms vs off-campus decision guide | https://www.fastweb.com/student-life/articles/how-to-pick-housing-for-college-students |
| 2 | Fastweb | How to juggle part-time work and scholarship applications | https://www.fastweb.com/student-life/articles/how-to-juggle-part-time-work-and-scholarship-applications |
| 3 | Fastweb | Fast food jobs that pay for college tuition (tuition assistance programs) | https://www.fastweb.com/student-life/articles/four-fast-food-jobs-thatll-pay-your-college-tuition |
| 4 | CNBC Select | 5 budgeting tips for college students | https://www.cnbc.com/select/budgeting-tips-for-college-students/ |
| 5 | Budget Bytes | Budget-friendly meal prep ideas and strategies | https://www.budgetbytes.com/category/extra-bytes/budget-friendly-meal-prep/ |
| 6 | Reddit r/personalfinance | Personal finance guide for young adults and working students | https://www.reddit.com/r/personalfinance/wiki/young_adult |
| 7 | Reddit r/college | Tips for commuting students who work part-time | https://www.reddit.com/r/college/ |
| 8 | Reddit r/college | Off-campus apartment hunting tips for students | https://www.reddit.com/r/college/ |
| 9 | Reddit r/college | How to stay safe living off-campus | https://www.reddit.com/r/college/ |
| 10 | Reddit r/college & r/GetMotivated | Avoiding burnout as a working student | https://www.reddit.com/r/college/ |
| 11 | Reddit r/LifeProTips | Time management hacks for students with jobs | https://www.reddit.com/r/LifeProTips/ |
| 12 | Reddit r/povertyfinance & r/Frugal | Surviving on minimum wage while in school | https://www.reddit.com/r/povertyfinance/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
