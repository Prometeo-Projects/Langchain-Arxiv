from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

_DEFAULT_EMBEDDING_MODEL = None

def get_embedding_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> HuggingFaceEmbeddings:
    global _DEFAULT_EMBEDDING_MODEL
    if _DEFAULT_EMBEDDING_MODEL is None:
        _DEFAULT_EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name=model_name)
    return _DEFAULT_EMBEDDING_MODEL


def save_to_vdb(
    full_text: str,
    metadata: dict,
    persist_directory: str = "vdb",
    embedding_model: HuggingFaceEmbeddings | None = None,
) -> Chroma:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )
    chunks = splitter.split_text(full_text)

    metadatas = [{**metadata, "chunk_id": i} for i in range(len(chunks))]

    if embedding_model is None:
        embedding_model = get_embedding_model()

    # Load existing collection or create a new one
    vdb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model,
    )
    vdb.add_texts(texts=chunks, metadatas=metadatas)

    return vdb
