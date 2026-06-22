import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from finance_agent.rag.embeddings import get_embeddings


DOCUMENTS_PATH = "finance_agent/rag/documents"

VECTOR_DB_PATH = "finance_agent/rag/faiss_index"


def load_documents():

    documents = []

    for file in os.listdir(DOCUMENTS_PATH):

        if file.endswith(".pdf"):

            path = os.path.join(
                DOCUMENTS_PATH,
                file
            )

            print(f"Loading {file}")

            loader = PyPDFLoader(path)

            documents.extend(
                loader.load()
            )

    return documents


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200

    )

    return splitter.split_documents(documents)


def create_vector_database(chunks):

    print("Creating embeddings...")

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(

        chunks,

        embeddings

    )

    vectorstore.save_local(

        VECTOR_DB_PATH

    )

    print("FAISS vector database saved successfully.")


def main():

    print("Loading PDF documents...")

    documents = load_documents()

    print(f"{len(documents)} pages loaded.")

    print("Splitting documents...")

    chunks = split_documents(documents)

    print(f"{len(chunks)} chunks created.")

    create_vector_database(chunks)

    print("RAG knowledge base is ready.")


if __name__ == "__main__":

    main()