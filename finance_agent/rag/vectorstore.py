from langchain_community.vectorstores import FAISS

from finance_agent.rag.embeddings import get_embeddings


VECTOR_DB_PATH = "finance_agent/rag/faiss_index"


def load_vectorstore():
    """
    Load the FAISS vector database.
    """

    embeddings = get_embeddings()

    vectorstore = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore