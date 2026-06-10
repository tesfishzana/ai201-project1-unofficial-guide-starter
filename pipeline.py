"""
Document Pipeline: Ingestion and Chunking
Loads .txt documents from the documents/ folder, strips metadata headers,
and splits content into 500-character chunks with 50-character overlap.
"""

import os
import glob


def load_documents(directory: str) -> list[dict]:
    """
    Load all .txt files from the given directory.
    Strips the metadata header (everything before the first '---' line).
    Returns a list of dicts with 'source' (filename) and 'text' (content).
    """
    documents = []
    txt_files = sorted(glob.glob(os.path.join(directory, "*.txt")))

    for filepath in txt_files:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()

        # Split on the first '---' separator to remove metadata header
        parts = raw_text.split("\n---\n", 1)
        if len(parts) == 2:
            content = parts[1].strip()
        else:
            # No metadata header found, use entire text
            content = raw_text.strip()

        filename = os.path.basename(filepath)
        documents.append({"source": filename, "text": content})

    return documents


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into chunks of approximately chunk_size characters with overlap.
    Tries to break at sentence or paragraph boundaries when possible.
    Ensures chunks don't start or end mid-word.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        # If we're not at the end, try to find a good break point
        if end < text_length:
            # Look for a sentence/paragraph boundary near the end
            search_start = max(start + chunk_size - 150, start)
            best_break = -1

            # Prefer paragraph breaks, then sentence breaks, then line breaks
            for sep in ["\n\n", ".\n", ". ", "!\n", "! ", "?\n", "? ", "\n- ", "\n"]:
                pos = text.rfind(sep, search_start, end + 50)
                if pos > best_break and pos > start:
                    best_break = pos + len(sep)

            if best_break > start:
                end = best_break
            else:
                # Fall back to nearest space to avoid cutting mid-word
                space_pos = text.rfind(" ", search_start, end)
                if space_pos > start:
                    end = space_pos + 1

        chunk = text[start:end].strip()
        if len(chunk) > 10:  # Only add substantive chunks
            chunks.append(chunk)

        # Calculate next start position with overlap
        next_start = end - overlap

        # Adjust to not start mid-word: find next space or newline
        if next_start < text_length and next_start > 0 and text[next_start] not in (" ", "\n"):
            space_pos = text.find(" ", next_start)
            newline_pos = text.find("\n", next_start)
            candidates = [p for p in (space_pos, newline_pos) if p != -1]
            if candidates:
                next_start = min(candidates) + 1

        # Ensure we always make progress
        start = max(next_start, start + 1)

    return chunks


def ingest_and_chunk(directory: str, chunk_size: int = 500, overlap: int = 50) -> list[dict]:
    """
    Full pipeline: load documents, chunk them, and return chunks with metadata.
    Returns a list of dicts with 'text', 'source', and 'chunk_index'.
    """
    documents = load_documents(directory)
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"], chunk_size, overlap)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": doc["source"],
                "chunk_index": i,
            })

    return all_chunks


if __name__ == "__main__":
    import random

    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    all_chunks = ingest_and_chunk(docs_dir)

    print(f"{'='*60}")
    print(f"PIPELINE RESULTS")
    print(f"{'='*60}")
    print(f"Total documents loaded: {len(set(c['source'] for c in all_chunks))}")
    print(f"Total chunks produced: {len(all_chunks)}")
    print(f"Average chunk length: {sum(len(c['text']) for c in all_chunks) / len(all_chunks):.0f} chars")
    print(f"Min chunk length: {min(len(c['text']) for c in all_chunks)} chars")
    print(f"Max chunk length: {max(len(c['text']) for c in all_chunks)} chars")

    # Print 5 random chunks for inspection
    print(f"\n{'='*60}")
    print(f"5 SAMPLE CHUNKS FOR INSPECTION")
    print(f"{'='*60}")

    sample_chunks = random.sample(all_chunks, min(5, len(all_chunks)))
    for i, chunk in enumerate(sample_chunks, 1):
        print(f"\n--- Chunk {i} (source: {chunk['source']}, index: {chunk['chunk_index']}) ---")
        print(f"Length: {len(chunk['text'])} chars")
        print(chunk['text'])
        print()
