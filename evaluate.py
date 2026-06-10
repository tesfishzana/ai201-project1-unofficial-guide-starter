"""
Evaluation Script: Run all 5 test questions and document results.
Outputs formatted evaluation results for the README.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Check API key
if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "your_key_here":
    print("ERROR: Please set your GROQ_API_KEY in .env first.")
    print("Get a free key at: https://console.groq.com")
    sys.exit(1)

from query import ask
from retrieval import build_vector_store, get_embedding_model

# Build vector store fresh for evaluation
docs_dir = os.path.join(os.path.dirname(__file__), "documents")
persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")

print("Building vector store for evaluation...")
collection = build_vector_store(docs_dir, persist_dir)
model = get_embedding_model()

# 5 Evaluation questions with expected answers
EVAL_QUESTIONS = [
    {
        "question": "How much tuition assistance does Starbucks offer student employees?",
        "expected": "Starbucks offers a 42% CAP Scholarship up front plus covers remaining tuition at ASU's online program, valued at over $47,000 total. Employees must be working on their first bachelor's degree and complete FAFSA.",
    },
    {
        "question": "How many hours per week should a full-time student work before grades start to suffer?",
        "expected": "10-15 hours/week is generally manageable; 15-20 is doable but grades may dip slightly; 20-25 is the risk zone with high burnout potential; 25+ is not recommended for full-time students.",
    },
    {
        "question": "What are the hidden costs beyond rent that students should budget for when moving off-campus?",
        "expected": "Security deposit, first+last month's rent, utilities ($30-80 electric, $20-50 gas, $20-40 water, $40-60 internet), renter's insurance ($10-20/month), furniture, kitchen basics ($100-200), and laundry ($20-40/month).",
    },
    {
        "question": "What should a student do to stay safe when walking home from a late work shift?",
        "expected": "Share live location with a trusted person, walk in well-lit areas, keep headphones off/low volume, carry a flashlight, have keys in hand before reaching the door, use campus safety escort services, and trust your gut if something feels wrong.",
    },
    {
        "question": "What's a realistic weekly grocery budget and what staple items should a student buy?",
        "expected": "$25-40/week. Staples: rice (25lb bag), dried beans/lentils, eggs, bananas, frozen vegetables, bread, peanut butter, oats, chicken thighs (family pack). Shop at Aldi/Lidl/ethnic grocery stores for 30-50% savings.",
    },
]

# Also test an out-of-scope question
OUT_OF_SCOPE = {
    "question": "What are the best computer science courses to take at MIT?",
    "expected": "System should decline to answer — this topic is not covered in the documents.",
}

print(f"\n{'='*70}")
print("EVALUATION RESULTS")
print(f"{'='*70}")

results = []

for i, q in enumerate(EVAL_QUESTIONS, 1):
    print(f"\n{'─'*70}")
    print(f"Question {i}: {q['question']}")
    print(f"{'─'*70}")
    print(f"\nExpected: {q['expected']}")

    result = ask(q["question"], collection, model)

    print(f"\nSystem Response:\n{result['answer']}")
    print(f"\nSources: {', '.join(result['sources'])}")
    print(f"Top chunk distance: {result['chunks'][0]['distance']:.4f}")

    results.append({
        **q,
        "response": result["answer"],
        "sources": result["sources"],
        "distance": result["chunks"][0]["distance"],
    })

# Out-of-scope test
print(f"\n{'─'*70}")
print(f"OUT-OF-SCOPE: {OUT_OF_SCOPE['question']}")
print(f"{'─'*70}")

oos_result = ask(OUT_OF_SCOPE["question"], collection, model)
print(f"\nSystem Response:\n{oos_result['answer']}")
print(f"\nSources: {', '.join(oos_result['sources'])}")
print(f"Top chunk distance: {oos_result['chunks'][0]['distance']:.4f}")

print(f"\n{'='*70}")
print("EVALUATION COMPLETE")
print(f"{'='*70}")
print(f"\nTotal questions evaluated: {len(EVAL_QUESTIONS)} + 1 out-of-scope")
print("Review the outputs above and assess accuracy for the README.")
