from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from convoxai.utils.audio import transcribe_audio_simple
from convoxai.utils.text_processing import split_extracted_text
from convoxai.utils.vector_store import get_or_create_index, ingest_text_chunks, get_retriever
from convoxai.core.prompts.templates import system_prompt
from convoxai.core.summarizer import generate_summary, create_llm


app=FastAPI()

@app.post('/getSummary')
def get_summary():
    pass