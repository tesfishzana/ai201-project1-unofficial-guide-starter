"""Quick validation script for chunk quality."""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from pipeline import ingest_and_chunk

docs_dir = os.path.join(os.path.dirname(__file__), "documents")
chunks = ingest_and_chunk(docs_dir)

short_chunks = [c for c in chunks if len(c["text"]) < 50]
print(f"Chunks shorter than 50 chars: {len(short_chunks)}")
for c in short_chunks:
    print(f'  [{c["source"]}] ({len(c["text"])} chars): "{c["text"]}"')

print(f"\nChunks per document:")
for source, count in sorted(Counter(c["source"] for c in chunks).items()):
    print(f"  {source}: {count} chunks")

print(f"\nTotal: {len(chunks)} chunks")
