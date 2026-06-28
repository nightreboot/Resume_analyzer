from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import shutil

CHROMA_DIR = "Chroma"

def embedding_model():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def chunk_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50
    )
    return splitter.split_text(text)


def vector_store(chunks: list) -> Chroma:
    if not chunks:
        raise ValueError(
            "vector_store() got no chunks to embed. "
            "extract_text() returned empty — check the file."
        )

    # ✅ Wipe old/corrupted Chroma data before writing fresh
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    embedding = embedding_model()
    docs = [Document(page_content=chunk) for chunk in chunks]
    vector = Chroma.from_documents(
        embedding=embedding,
        documents=docs,
        persist_directory=CHROMA_DIR
    )
    return vector


def vector_load():
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_model()
    )


def retrivers(vector_db: Chroma, k: int = 5):
    return vector_db.as_retriever(
        search_type='mmr',
        search_kwargs={"k": k}
    )