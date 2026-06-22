from langchain_huggingface import HuggingFaceEmbeddings


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


print("Loading embedding model...")


embeddings = HuggingFaceEmbeddings(

    model_name=MODEL_NAME,

    model_kwargs={

        "device": "cpu"

    },

    encode_kwargs={

        "normalize_embeddings": True

    }

)


def get_embeddings():

    """
    Returns the embedding model used by the RAG pipeline.
    """

    return embeddings