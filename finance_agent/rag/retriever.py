from finance_agent.rag.vectorstore import load_vectorstore


def retrieve_documents(query: str, k: int = 4):
    """
    Retrieve the most relevant document chunks
    for a user query.
    """

    vectorstore = load_vectorstore()

    documents = vectorstore.similarity_search(

        query,

        k=k

    )

    return documents


def retrieve_context(query: str, k: int = 4):
    """
    Returns the retrieved chunks as one
    formatted context string.
    """

    documents = retrieve_documents(

        query,

        k

    )

    context = "\n\n".join(

        doc.page_content

        for doc in documents

    )

    return context