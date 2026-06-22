from langchain.tools import tool

from finance_agent.rag.retriever import retrieve_documents


@tool
def search_financial_documents(
    query: str
) -> str:
    """
    Search company annual reports, quarterly reports,
    earnings reports and other financial documents
    to answer questions about a company.
    """

    try:

        documents = retrieve_documents(
            query=query,
            k=8
        )

        if not documents:

            return "No relevant financial documents were found."

        context = ""

        for i, doc in enumerate(documents, start=1):

            context += (
                f"\nDocument {i}\n"
                f"\nSource: {doc.metadata.get('source', 'Unknown')}\n"
                f"{'-'*40}\n"
                f"{doc.page_content}\n\n"
            )

        return context

    except Exception as e:

        return f"Error retrieving financial documents: {e}"