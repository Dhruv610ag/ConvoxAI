from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate
from core.prompts.templates import CHATBOT_PROMPT
from utils.vector_store import get_retriever
from typing import List, Dict, Optional
from config import (
    GEMINI_API_KEY, 
    GEMINI_MODEL_NAME, 
    GEMINI_TEMPERATURE,
    GROQ_API_KEY,
    GROQ_MODEL_NAME,
    GROQ_TEMPERATURE
)

chatbot_prompt_template = PromptTemplate(
    input_variables=["question", "chat_history", "context"],
    template=CHATBOT_PROMPT
)

def create_chatbot_llm(model_choice: str = "gemini"):
    if model_choice.lower() == "groq":
        return ChatGroq(
            model=GROQ_MODEL_NAME,
            api_key=GROQ_API_KEY,
            temperature=GROQ_TEMPERATURE
        )
    else:
        return ChatGoogleGenerativeAI(
            model=GEMINI_MODEL_NAME,
            api_key=GEMINI_API_KEY,
            temperature=GEMINI_TEMPERATURE
        )


def create_chatbot_chain(model_choice: str = "gemini"):
    llm = create_chatbot_llm(model_choice)
    retriever = get_retriever()
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": chatbot_prompt_template},
        verbose=False
    )
    
    return chain

def process_query(
    question: str,
    chat_history: Optional[List[Dict[str, str]]] = None,
    model_choice: str = "gemini"
) -> Dict[str, any]:
    try:
        chain = create_chatbot_chain(model_choice)
        formatted_history = []
        if chat_history:
            for msg in chat_history:
                if msg["role"] == "user":
                    formatted_history.append(("human", msg["content"]))
                elif msg["role"] == "assistant":
                    formatted_history.append(("ai", msg["content"]))
        result = chain({
            "question": question,
            "chat_history": formatted_history
        })
        sources = []
        if "source_documents" in result:
            for doc in result["source_documents"]:
                sources.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata if hasattr(doc, 'metadata') else {}
                })
        
        return {
            "answer": result["answer"],
            "sources": sources,
            "model_used": model_choice
        }
        
    except Exception as e:
        raise


def query_without_history(question: str, model_choice: str = "gemini") -> Dict[str, any]:
    return process_query(question, chat_history=None, model_choice=model_choice)