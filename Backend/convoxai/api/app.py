from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from modules.audio_extractor import transcribe_audio_simple
from modules.dataloading import split_extracted_text
from modules.vectorstore import get_or_create_index,ingest_text_chunks,get_retriever
from src.prompt import system_prompt
from src.summarizer import generate_summary,create_llm

app=FastAPI()

@app.post('/getSummary')
def get_summary():
    pass