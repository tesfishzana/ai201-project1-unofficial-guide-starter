"""
Embedding and Retrieval Module
Embeds document chunks using all-MiniLM-L6-v2 and stores them in ChromaDB.
Provides retrieval function for querying the vector store.
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer
from pipeline import ingest_and_chunk


# Collection name for our vector store
COLLECTION_NAME = "offcampus_survival_guide"


def get_embedding_model():
    """Load the sentence-transformers embedding model."""
    return SentenceTransformer("all-MiniLM-L6-v2")


def get_chroma_client(persist_dir: str = None):
    """Get a ChromaDB client. Uses persistent storage if persist_dir is provided."""
    if persist_dir:
        return chromadb.PersistentClient(path=persist_dir)
    return chromadb.Client()


def build_vector_store(docs_dir: str, persist_dir: str = None):
    """
    Full embedding pipeline:
    1. Load and chunk documents
    2. Embed all chunks with all-MiniLM-L6-v2
    3. Store in ChromaDB with source metadata
    Returns the ChromaDB collection.
    """
    # Load and chunk documents
    print("Loading and chunking documents...")
    chunks = ingest_and_chunk(docs_dir)
    print(f"  {len(chunks)} chunks ready for embedding")

    # Load embedding model
    print("Loading embedding model (all-MiniLM-L6-v2)...")
    model = get_embedding_model()

    # Embed all chunks
    print("Embedding chunks...")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    print(f"  Generated {len(embeddings)} embeddings of dimension {embeddings.shape[1]}")

    # Store in ChromaDB
    print("Storing in ChromaDB...")
    client = get_chroma_client(persist_dir)

    # Delete existing collection if it exists (for re-indexing)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    # Add chunks with metadata
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=[
            {"source": chunk["source"], "chunk_index": chunk["chunk_index"]}
            for chunk in chunks
        ],
    )
    print(f"  Stored {collection.count()} chunks in collection '{COLLECTION_NAME}'")

    return collection


def retrieve(query: str, collection=None, model=None, k: int = 5):
    """
    Retrieve the top-k most relevant chunks for a given query.
    Returns a list of dicts with 'text', 'source', 'chunk_index', and 'distance'.
    """
    if model is None:
        model = get_embedding_model()

    # Embed the query
    query_embedding = model.encode([query]).tolist()

    # Query ChromaDB
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    # Format results
    retrieved = []
    for i in range(len(results["documents"][0])):
        retrieved.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
            "distance": results["distances"][0][i],
        })

    return retrieved


if __name__ == "__main__":
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")

    # Build the vector store
    collection = build_vector_store(docs_dir, persist_dir)

    # Test retrieval with 3 evaluation questions
    model = get_embedding_model()

    test_queries = [
        "How much tuition assistance does Starbucks offer student employees?",
        "How many hours per week should a full-time student work before grades start to suffer?",
        "What should a student do to stay safe when walking home from a late work shift?",
    ]

    print(f"\n{'='*60}")
    print("RETRIEVAL TEST RESULTS")
    print(f"{'='*60}")

    for query in test_queries:
        print(f"\n{'─'*60}")
        print(f"QUERY: {query}")
        print(f"{'─'*60}")

        results = retrieve(query, collection, model, k=5)

        for i, result in enumerate(results, 1):
            print(f"\n  Result {i} (distance: {result['distance']:.4f})")
            print(f"  Source: {result['source']}")
            # Show first 200 chars of the chunk
            preview = result["text"][:200].replace("\n", " ")
            print(f"  Preview: {preview}...")
