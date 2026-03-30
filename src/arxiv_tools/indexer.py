from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def save_to_vdb(full_text: str, metadata: dict, persist_directory="vdb"):
    """
    Guarda un documento en una Vector DataBase usando chunking y embeddings.

    Parameters
    ----------
    full_text : str
        Texto completo del documento.
    metadata : dict
        Metadatos asociados al documento (ej: autor, fuente, tema).
    persist_directory : str
        Carpeta donde se guarda la VDB.
    """

    # Fragmentar el texto
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.split_text(full_text)

    # Crear metadatos por chunk
    metadatas = [
        {**metadata, "chunk_id": i}
        for i in range(len(chunks))
    ]

    # Embeddings
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Guardar en ChromaDB
    vdb = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        metadatas=metadatas,
        persist_directory=persist_directory
    )

    vdb.persist()

    return vdb
