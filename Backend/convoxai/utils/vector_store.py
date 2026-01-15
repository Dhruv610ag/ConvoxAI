from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from convoxai.utils.embeddings import load_embeddings
from convoxai.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    PINECONE_DIMENSION,
    PINECONE_METRIC,
    PINECONE_CLOUD,
    PINECONE_REGION,
    RETRIEVER_SEARCH_TYPE,
    RETRIEVER_TOP_K
)

pc = Pinecone(api_key=PINECONE_API_KEY)

def get_or_create_index():
    if not pc.has_index(PINECONE_INDEX_NAME):
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=PINECONE_DIMENSION,
            metric=PINECONE_METRIC,
            spec=ServerlessSpec(
                cloud=PINECONE_CLOUD,
                region=PINECONE_REGION
            )
        )
    return PINECONE_INDEX_NAME

def ingest_text_chunks(chunks):
    embeddings = load_embeddings()
    index_name = get_or_create_index()
    vectorstore = PineconeVectorStore.from_texts(
        texts=chunks,
        embedding=embeddings,
        index_name=index_name
    )
    return vectorstore

def get_retriever():
    embeddings = load_embeddings()
    vectorstore = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings
    )
    return vectorstore.as_retriever(
        search_type=RETRIEVER_SEARCH_TYPE,
        search_kwargs={"k": RETRIEVER_TOP_K}
    )