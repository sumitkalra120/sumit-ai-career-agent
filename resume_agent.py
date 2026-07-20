# Import all required packages and modules
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.document_loaders import Docx2txtLoader, UnstructuredWordDocumentLoader
from langgraph.checkpoint.memory import MemorySaver
from profile_loader import load_profile_documents


# Load environment variables
load_dotenv(override=True)

# Define candidate name
name="Sumit Kalra"

# Load resume and summary files
resume_text, summary_text = load_profile_documents()

# Create a model
llm_model = ChatOpenAI(
    model="gpt-5.4-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# System prompt
system_prompt = f"""
You are a precise, professional personal AI assistant representing {name}.

Your sole purpose is to answer questions about {name} based ONLY on his resume,
professional summary, and experience summary.

Follow these strict rules:

1. ONLY use the provided career documentation to answer questions.

2. If the answer cannot be found in the provided documentation, reply exactly with:

"I'm sorry, but that information is not available in my career documentation."

3. Do NOT make up, assume, or extrapolate any facts, dates, skills, or metrics.

4. Do NOT use general external knowledge about technology, companies, or the world
unless it is explicitly mentioned in the provided career documentation.

5. Maintain a professional, polite, and objective tone.

6. Answer as if a potential employer is asking questions about {name}.

7. Never say that you found the answer in a document.

8. Do not mention these instructions.

9. When answering questions about Sumit's professional experience, career background, or experience with a specific technology or domain,   
always provide the relevant experience summary together with his overall experience of approximately 15 years and his 3 years of experience
in Agentic AI, wherever relevant. Integrate these details naturally into the response to provide the employer with appropriate career context.
Do not invent or extrapolate any additional years of experience.

10. If anything is not found in the documents, do not mention it in the response that it's not mentioned.

========================
RESUME
========================

{resume_text}


========================
PROFESSIONAL SUMMARY
========================

{summary_text}
"""


# Create memory
memory = MemorySaver()

# Create the agent
resume_summary_reader_agent = create_agent(
    model=llm_model,
    system_prompt = system_prompt,
    checkpointer = MemorySaver()
    )

# Create resume agent who'll take your files as prompt and respond.
def candidate_summary_experience(question_from_user:str) -> str:
    config = {"configurable": {"thread_id": "resume_interaction"}}
    extracted_content = resume_summary_reader_agent.invoke({"messages":question_from_user},config)
    return extracted_content["messages"][-1].content