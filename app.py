# Import all the packages and modules
import os
import gradio as gr
from resume_agent import candidate_summary_experience   


def ai_assistant(user_prompt):

    if not user_prompt.strip():
        return "Please enter a research question."

    try:
        result = candidate_summary_experience(user_prompt)
        return result

    except Exception as e:
        return f"Error: {str(e)}"


with gr.Blocks() as demo:

    gr.Markdown(
        """
        # 🤖 Sumit's AI Career Agent

        Ask me anything about Sumit's professional background,
        experience, skills, and career.
        """
    )

    user_input = gr.Textbox(
        label="Ask anything about me",
        placeholder="Type your message here...",
        lines=3
    )

    submit_button = gr.Button(
        "Ask me",
        variant="primary"
    )

    chatbot_output = gr.Textbox(
        label="Response",
        lines=10
    )

    submit_button.click(
        fn=ai_assistant,
        inputs=user_input,
        outputs=chatbot_output
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    demo.launch(
        server_name="0.0.0.0",
        server_port=port
    )