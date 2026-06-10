# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

Off-campus survival guides for college students who work part-time. This system covers budgeting, apartment hunting, meal prep, time management, commuting, safety, burnout prevention, and employer tuition benefits — the practical knowledge that working students need but is scattered across Reddit threads, personal finance blogs, and student life articles. University websites rarely address the reality of students who must work to afford school, making this knowledge hard to find through official channels.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Fastweb - College Housing Options | Article | https://www.fastweb.com/student-life/articles/how-to-pick-housing-for-college-students |
| 2 | Fastweb - Juggling Part-Time Work | Article | https://www.fastweb.com/student-life/articles/how-to-juggle-part-time-work-and-scholarship-applications |
| 3 | Fastweb - Fast Food Jobs Tuition | Article | https://www.fastweb.com/student-life/articles/four-fast-food-jobs-thatll-pay-your-college-tuition |
| 4 | CNBC Select - Student Budgeting | Article | https://www.cnbc.com/select/budgeting-tips-for-college-students/ |
| 5 | Budget Bytes - Meal Prep | Recipe/Guide | https://www.budgetbytes.com/category/extra-bytes/budget-friendly-meal-prep/ |
| 6 | Reddit r/personalfinance | Wiki/Forum | https://www.reddit.com/r/personalfinance/wiki/young_adult |
| 7 | Reddit r/college - Commuting | Forum thread | https://www.reddit.com/r/college/ |
| 8 | Reddit r/college - Apartment Hunting | Forum thread | https://www.reddit.com/r/college/ |
| 9 | Reddit r/college - Safety Tips | Forum thread | https://www.reddit.com/r/college/ |
| 10 | Reddit r/college - Burnout Prevention | Forum thread | https://www.reddit.com/r/college/ |
| 11 | Reddit r/LifeProTips - Time Management | Forum thread | https://www.reddit.com/r/LifeProTips/ |
| 12 | Reddit r/povertyfinance - Min Wage Survival | Forum thread | https://www.reddit.com/r/povertyfinance/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 500 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** My documents are structured guides averaging 4,000–7,000 characters each, organized with headers and bullet-pointed advice. A 500-character chunk captures one complete piece of advice (e.g., one budgeting tip, one safety strategy, or one meal prep idea) without mixing unrelated topics. The chunking function prefers breaking at sentence and paragraph boundaries rather than splitting mid-sentence. The 50-character overlap ensures advice split at section boundaries retains enough context in both chunks to be independently retrievable.

**Preprocessing:** Each document has a metadata header (Source, URL, Author, Date, Type) separated by `---`. The ingestion step strips this header before chunking. No HTML cleaning was needed since documents were collected as plain text.

**Final chunk count:** 134 chunks across 12 documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`. Produces 384-dimensional embeddings, runs locally with no API key or rate limits, and handles informal English text (Reddit-style writing, casual advice) well. Stored in ChromaDB with cosine similarity.

**Production tradeoff reflection:** For a real deployment serving students, I'd weigh:
- **`all-mpnet-base-v2`** (768-dim): ~10% higher accuracy on semantic similarity benchmarks but 2x slower/larger. Worth it if retrieval precision is the bottleneck.
- **OpenAI `text-embedding-3-small`**: Better on domain-specific text with 8191-token context window, but requires API calls ($0.02/1M tokens) and adds 100-300ms latency per query. Would be necessary for multilingual content.
- **Context length**: `all-MiniLM-L6-v2` handles up to 256 tokens (~500 characters), which fits my chunks well. Larger chunks or documents would require a model with a bigger window.
- **Local vs. API**: Local models give zero-cost, zero-latency embedding, critical for a student project. A production system with millions of queries might benefit from API models' superior accuracy despite the per-call cost.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The system prompt explicitly enforces grounding with these rules:
```
You answer questions using ONLY the information provided in the context documents below.
STRICT RULES:
1. Answer ONLY using information explicitly stated in the provided context documents.
2. Do NOT use your general knowledge or training data to supplement answers.
3. If the provided documents do not contain enough information to fully answer the question,
   say: "I don't have enough information in my sources to answer that question."
4. Always cite which source document(s) your answer comes from using [Source: filename].
5. Do not invent, assume, or extrapolate beyond what the documents state.
```

Additionally, temperature is set to 0.3 to reduce creative generation, and the user message formats each retrieved chunk with its source filename label so the LLM has explicit provenance information.

**How source attribution is surfaced in the response:**

Source attribution is enforced at two levels:
1. **In the LLM prompt**: Each retrieved chunk is labeled `[Document N - filename.txt]` in the context, and the system prompt requires citing `[Source: filename]` in the response.
2. **Programmatically in the interface**: The Gradio UI displays a separate "Sources used" field listing all retrieved document filenames, independent of what the LLM chooses to cite. This guarantees source visibility even if the LLM forgets to cite.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How much tuition assistance does Starbucks offer student employees? | 42% CAP Scholarship + remaining tuition at ASU online, valued at $47,000+. Must be first bachelor's, complete FAFSA. | Correctly stated 42% CAP Scholarship, ASU online program, $47,000 value. Cited source document. | Relevant | Accurate |
| 2 | How many hours per week should a full-time student work before grades suffer? | 10-15 hrs manageable; 15-20 grades dip; 20-25 risk zone; 25+ not recommended. | Listed all hour ranges with correct impacts. Concluded 15 hrs/week as threshold. | Relevant | Accurate |
| 3 | What are the hidden costs beyond rent when moving off-campus? | Security deposit, first+last rent, utilities ($30-80 elec, $20-50 gas, $20-40 water, $40-60 internet), renter's insurance, furniture, kitchen basics, laundry. | Listed all hidden costs with exact dollar ranges matching source. Also added moving costs (truck rental, boxes). | Relevant | Accurate |
| 4 | What should a student do to stay safe walking home from a late work shift? | Share location, well-lit areas, headphones off, flashlight, keys ready, campus escorts, trust gut. | Provided comprehensive safety list including all expected points plus additional car/rideshare safety tips from related chunk. | Relevant | Accurate |
| 5 | What's a realistic weekly grocery budget and staple items? | $25-40/week. Staples: rice, beans, eggs, bananas, frozen veg, bread, PB, oats, chicken thighs. Shop at Aldi/Lidl. | Correctly stated $25-40/week, listed all staple items with prices, mentioned food pantries and SNAP benefits as bonus. | Relevant | Accurate |

**Out-of-scope test:** "What are the best computer science courses to take at MIT?" → System correctly responded: "I don't have enough information in my sources to answer that question." (Top chunk distance: 0.73, confirming no relevant content was retrieved.)

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

"What are the hidden costs beyond rent that students should budget for when moving off-campus?" — While the final answer was accurate, retrieval revealed a partial failure pattern: the second retrieved chunk (from `01_college_housing_options_off_campus.txt`, distance 0.48) discussed whether off-campus is more expensive than dorms in general terms but contained zero specific cost numbers. It was retrieved because it shared vocabulary ("off campus," "costs," "rent") with the query despite not actually answering it.

More critically, when I tested an additional query — "What's a good roommate agreement template?" — the system retrieved chunks about roommate cost-splitting and finding roommates, but the specific roommate agreement checklist (quiet hours, cleaning responsibilities, guest policies, temperature preferences) was split across a chunk boundary. The first chunk ended at "How to split utilities" and the second started at "Temperature preferences (heating/cooling battles are real)." The retrieval returned the first half but missed the second, so the generated answer omitted half the checklist items.

**What the system returned:**

For the roommate agreement query, the system listed utility splitting, quiet hours, and guest policies, but missed cleaning responsibilities, shared vs. personal groceries, early move-out procedures, and temperature preferences — all of which exist in the source document but were in the next chunk that wasn't retrieved.

**Root cause (tied to a specific pipeline stage):**

**Chunking stage**: The roommate agreements section in `08_apartment_hunting_guide_students.txt` is a long bulleted list (~400 characters) that falls right at the edge of the 500-character chunk boundary. The chunk_text function split it after "Quiet hours and guest policies" because it found a `\n- ` break point there. The remaining items ended up in a separate chunk that scored slightly lower on relevance (distance 0.52 vs 0.44) and was included at position 5 of the top-5 results — but with less context around it, the LLM gave it less weight in generation.

**What you would change to fix it:**

1. **Increase chunk size to 600-700 characters** for documents with long lists, or implement a "list-aware" chunker that detects bulleted lists and keeps them intact.
2. **Increase top-k from 5 to 7** to capture more related chunks, at the cost of potentially introducing off-topic noise.
3. **Add a deduplication step** that merges adjacent chunks from the same document when both are retrieved, reconstructing the original section before passing to the LLM.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The Chunking Strategy section in planning.md forced me to think about my document structure before writing any splitting code. Because I had already noted that my documents are "structured guides with headers and bullet-pointed advice," I built a chunk_text function that prioritizes paragraph and sentence boundaries rather than doing a naive fixed-character split. This decision directly prevented the most common RAG failure (mid-sentence splits producing meaningless fragments) and meant my first retrieval test already returned coherent, self-contained chunks. Without the spec, I likely would have used a simple `text[i:i+500]` approach and had to debug fragmented results later.

**One way your implementation diverged from the spec, and why:**

My planning.md specified a flat 50-character overlap applied uniformly. During implementation, I discovered that overlapping into the middle of a word created chunks starting with fragments like "egetarian" or "ommates." I modified the chunk_text function to find the nearest word boundary (space or newline) when calculating the overlap start position. This wasn't in the spec because I hadn't anticipated the word-boundary issue until I printed actual chunks and inspected them. The spec's overlap value (50 chars) stayed the same, but the implementation added logic the spec didn't describe.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* My planning.md Chunking Strategy section (500 chars, 50 overlap, section-based guides), the document structure description (12 .txt files with metadata headers separated by `---`), and the pipeline architecture diagram. I asked GitHub Copilot to implement `chunk_text()` and `ingest_documents()` functions matching my spec.
- *What it produced:* A chunking function that split text at fixed 500-character boundaries and searched backward for sentence-ending punctuation (`. `) to find natural break points. It also produced a document loader that split on the `---` separator to strip metadata.
- *What I changed or overrode:* The initial version produced chunks starting mid-word when the overlap calculation landed inside a word (e.g., "egetarian Meal Prep"). I added word-boundary detection logic that finds the nearest space or newline when calculating the next chunk's start position. I also expanded the break-point search to include paragraph breaks (`\n\n`), list items (`\n- `), and multiple punctuation types, and added a minimum chunk length filter (>10 chars) to prevent trailing fragments.

**Instance 2**

- *What I gave the AI:* My Retrieval Approach section (all-MiniLM-L6-v2, ChromaDB, top-k=5, cosine similarity), the pipeline diagram showing the Embedding + Vector Store stage, and the requirement that each chunk needs source metadata for attribution. I asked for embedding and retrieval code.
- *What it produced:* A `build_vector_store()` function that loads the embedding model, encodes all chunks, stores them in ChromaDB with metadata dictionaries containing `source` and `chunk_index`, and a `retrieve()` function that embeds the query and calls `collection.query()` with `n_results=k`. It used `chromadb.PersistentClient` for disk storage.
- *What I changed or overrode:* The initial code didn't handle re-indexing (running the build script twice would error on duplicate collection names). I added a `try/except` block that deletes the existing collection before creating a new one. I also added `metadata={"hnsw:space": "cosine"}` to the collection creation to explicitly set cosine distance (the default is L2), which better matches how sentence-transformers models are trained.

**Instance 3**

- *What I gave the AI:* My evaluation plan questions, the Groq SDK documentation, and the requirement for strict grounding (answer only from context, cite sources, decline out-of-scope questions). I asked for the generation function and Gradio interface.
- *What it produced:* A `generate_answer()` function with a system prompt, a `format_context()` function that labels chunks with document numbers, and a Gradio Blocks interface with textboxes for question/answer/sources.
- *What I changed or overrode:* I strengthened the system prompt's grounding rules — the initial version said "try to answer from the documents" which is too permissive. I rewrote it with explicit numbered rules including "Do NOT use your general knowledge" and "If documents don't contain enough information, say so explicitly." I also set temperature to 0.3 (it defaulted to 1.0) to reduce creative hallucination, and added the programmatic source display in the Gradio UI as a backup to the LLM's inline citations.
