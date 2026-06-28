
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from core.vectore_db import vector_load, retrivers
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()


def get_model():
    return ChatMistralAI(
        api_key=os.getenv("MISTRAL_API_KEY"),
        model="mistral-small-2603"
    )


def user_input(job_description: str) -> str:
    llm = get_model()
    vector_data = vector_load()
    retriever = retrivers(vector_data)

    docs = retriever.invoke(job_description)
    if not docs:
        raise ValueError(
            "No resume content found in the vector store. "
            "Make sure a resume has been extracted, chunked, and stored "
            "via vector_store() before calling user_input()."
        )

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = ChatPromptTemplate.from_template("""
You are an expert AI Resume Analyzer and ATS Evaluator.
Analyze the given resume against the provided job description and act like a professional hiring manager + ATS system.
Resume Content:
{resume}

Job Description:
{job_description}

Your tasks:

1. Evaluate the resume based on:
   - Skills match
   - Experience relevance
   - Projects alignment
   - Education fit
   - Keywords optimization
   - Achievements impact

2. Generate an ATS Match Score (0-100%) based on how well the resume matches the job description.

3. Identify:
   - Missing important skills
   - Missing keywords
   - Weak sections
   - Irrelevant information

4. Provide detailed improvement suggestions to increase ATS score.

5. Suggest exact keywords from the job description that should be added.

6. Highlight strengths of the resume.

Output format:

ATS Score: XX%

Matched Skills:
- ...

Missing Skills:
- ...

Strengths:
- ...

Weaknesses:
- ...

Improvement Suggestions:
- ...

Final Verdict:
(Short summary on whether the candidate is a strong fit or needs improvement)
""")

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({
        "resume": context,
        "job_description": job_description,
    })

    return response

