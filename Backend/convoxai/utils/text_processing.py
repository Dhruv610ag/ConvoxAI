from modules.audio_extractor import transcribe_audio_simple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from convoxai.config import CHUNK_SIZE, CHUNK_OVERLAP, TEXT_SEPARATORS

def text_extractor(audio_file_path):
    transcript = transcribe_audio_simple(audio_file_path)
    return transcript

def split_extracted_text(transcript):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=TEXT_SEPARATORS
    )
    chunks = text_splitter.split_text(transcript)
    return chunks

