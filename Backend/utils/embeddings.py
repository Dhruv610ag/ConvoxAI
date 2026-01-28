from langchain_community.embeddings import HuggingFaceEmbeddings
from config import EMBEDDINGS_MODEL_NAME

def load_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDINGS_MODEL_NAME,
    )
    return embeddings
