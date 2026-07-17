from langchain_community.document_loaders import Docx2txtLoader


def load_profile_documents():

    resume_loader = Docx2txtLoader(
        "SumitKalra_AgenticAIEngineer_Resume.docx"
    )

    summary_loader = Docx2txtLoader(
        "Sumit_Kalra_Background_Summary.docx"
    )

    resume_doc = resume_loader.load()
    summary_doc = summary_loader.load()

    resume_text = resume_doc[0].page_content
    summary_text = summary_doc[0].page_content

    return resume_text, summary_text