"""
Query Module: End-to-end retrieval + grounded generation.
Connects the retrieval pipeline to Groq's LLM with strict grounding instructions.
"""

import os
from dotenv import load_dotenv
from groq import Groq
from retrieval import build_vector_store, retrieve, get_embedding_model

load_dotenv()

# System prompt enforcing grounding
SYSTEM_PROMPT = """You are a helpful assistant for college students who live off-campus and work part-time jobs. You answer questions using ONLY the information provided in the context documents below.

STRICT RULES:
1. Answer ONLY using information explicitly stated in the provided context documents.
2. Do NOT use your general knowledge or training data to supplement answers.
3. If the provided documents do not contain enough information to fully answer the question, say: "I don't have enough information in my sources to answer that question."
4. Always cite which source document(s) your answer comes from using the format: [Source: filename].
5. If information comes from multiple sources, cite all relevant ones.
6. Be specific and practical — these are real students looking for actionable advice.
7. Do not invent, assume, or extrapolate beyond what the documents state."""


def format_context(retrieved_chunks: list[dict]) -> str:
    """Format retrieved chunks into a context string for the LLM."""
    context_parts = []
    for i, chunk in enumerate(retrieved_chunks, 1):
        source = chunk["source"].replace(".txt", "").replace("_", " ")
        context_parts.append(
            f"[Document {i} - {chunk['source']}]\n{chunk['text']}"
        )
    return "\n\n---\n\n".join(context_parts)


def generate_answer(query: str, retrieved_chunks: list[dict]) -> str:
    """
    Generate a grounded answer using Groq's LLM.
    The LLM is instructed to answer only from the retrieved context.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    context = format_context(retrieved_chunks)

    user_message = f"""Context documents:

{context}

---

Question: {query}

Answer the question using ONLY the information in the context documents above. Cite your sources using [Source: filename] format."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    return response.choices[0].message.content


def ask(question: str, collection=None, model=None, k: int = 5) -> dict:
    """
    Full end-to-end pipeline: retrieve relevant chunks and generate a grounded answer.
    Returns a dict with 'answer', 'sources', and 'chunks'.
    """
    if model is None:
        model = get_embedding_model()

    if collection is None:
        # Load existing collection from persistent storage
        import chromadb
        persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
        client = chromadb.PersistentClient(path=persist_dir)
        collection = client.get_collection("offcampus_survival_guide")

    # Retrieve relevant chunks
    retrieved = retrieve(question, collection, model, k=k)

    # Generate grounded answer
    answer = generate_answer(question, retrieved)

    # Extract unique sources
    sources = list(dict.fromkeys(chunk["source"] for chunk in retrieved))

    return {
        "answer": answer,
        "sources": sources,
        "chunks": retrieved,
    }


if __name__ == "__main__":
    # Test end-to-end with evaluation queries
    print("Building vector store...")
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
    collection = build_vector_store(docs_dir, persist_dir)
    model = get_embedding_model()

    test_queries = [
        "How much tuition assistance does Starbucks offer student employees?",
        "What should a student do to stay safe when walking home from a late work shift?",
        # This question is NOT covered by our documents — should decline to answer
        "What are the best computer science courses to take at MIT?",
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"QUERY: {query}")
        print(f"{'='*60}")

        result = ask(query, collection, model)

        print(f"\nANSWER:\n{result['answer']}")
        print(f"\nSOURCES: {', '.join(result['sources'])}")
        print(f"\nTop chunk distance: {result['chunks'][0]['distance']:.4f}")
