"""
Gradio Web Interface for the Off-Campus Survival Guide.
Run with: python app.py
Open: http://localhost:7860
"""

import gradio as gr
from query import ask


def handle_query(question):
    """Process a user question and return the answer with sources."""
    if not question.strip():
        return "Please enter a question.", ""

    try:
        result = ask(question)
        sources = "\n".join(f"• {s}" for s in result["sources"])
        return result["answer"], sources
    except Exception as e:
        return f"Error: {str(e)}", ""


with gr.Blocks(title="Off-Campus Survival Guide") as demo:
    gr.Markdown(
        """
        # 🏠 The Unofficial Off-Campus Survival Guide
        ### For college students who work part-time

        Ask questions about budgeting, housing, meal prep, time management,
        safety, avoiding burnout, and more. Answers are grounded in real
        student advice and guides — not general AI knowledge.
        """
    )

    with gr.Row():
        inp = gr.Textbox(
            label="Your question",
            placeholder="e.g., How much tuition assistance does Starbucks offer?",
            lines=2,
        )

    btn = gr.Button("Ask", variant="primary")

    answer = gr.Textbox(label="Answer", lines=10, interactive=False)
    sources = gr.Textbox(label="Sources used", lines=4, interactive=False)

    gr.Markdown(
        """
        ---
        **Example questions:**
        - How many hours per week should a student work before grades suffer?
        - What are the hidden costs of off-campus living beyond rent?
        - What's a realistic weekly grocery budget for a student?
        - What safety precautions should I take walking home from late shifts?
        - Which fast food jobs offer tuition assistance programs?
        """
    )

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()
