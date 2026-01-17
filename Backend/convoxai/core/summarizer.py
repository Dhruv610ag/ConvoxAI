import warnings
from typing import List, Literal, Annotated
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from convoxai.utils.audio import transcribe_audio_simple
from convoxai.core.prompts.templates import system_prompt
from convoxai.config import GEMINI_API_KEY, GEMINI_MODEL_NAME, GEMINI_TEMPERATURE

warnings.filterwarnings("ignore")

class SummaryResponse(BaseModel):
    summary: Annotated[str, Field(..., description="Write the Concise call summary From the Transcript")]
    duration_minutes: Annotated[int, Field(..., description="Calculate the Call duration in minutes")]
    no_of_participants: Annotated[int, Field(..., description="Count the number of participants")]
    key_aspects: Annotated[List[str], Field(..., description="List the key discussion points as bullet points")]
    sentiment: Annotated[Literal["Positive", "Negative", "Neutral"], Field(..., description="Mention the sentiment of the call")]

def create_llm():
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL_NAME,
        api_key=GEMINI_API_KEY,
        temperature=GEMINI_TEMPERATURE
    )

def generate_summary(audio_file_path: str | None = None) -> dict:
    if audio_file_path is None:
        raise ValueError("Provide the valid Audio File for processing")
    transcript = transcribe_audio_simple(audio_file_path)
    llm = create_llm()
    st_llm = llm.with_structured_output(SummaryResponse)
    final_prompt = system_prompt.format(transcript=transcript)
    response = st_llm.invoke(final_prompt)
    return response
