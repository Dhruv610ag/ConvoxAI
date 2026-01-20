# All the Pydantic Models are here Whether it is used for the chatbot or the Output parser or the Fastapi Things.
from pydantic import BaseModel,Field
from typing import List,Literal,Annotated,Any,Dict

class SummaryResponse(BaseModel):
    summary: Annotated[str, Field(..., description="Write the Concise call summary From the Transcript")]
    duration_minutes: Annotated[int, Field(..., description="Calculate the Call duration in minutes")]
    no_of_participants: Annotated[int, Field(..., description="Count the number of participants")]
    key_aspects: Annotated[List[str], Field(..., description="List the key discussion points as bullet points")]
    sentiment: Annotated[Literal["Positive", "Negative", "Neutral"], Field(..., description="Mention the sentiment of the call")]


class APIResponse(BaseModel):
    status: Annotated[str,Field(...,description="What is the Status od the Model")]
    message: Annotated[str,Field(...,description="What is the Message")]
    model_info: Annotated[Dict[str, Any],Field(...,description="What is the Model Info")]

class ErrorResponse(BaseModel):
    error: Annotated[str,Field(...,description="What is the Error")]
    detail: Annotated[str,Field(...,description="What is the Detail")]

class ModelTestRequest(BaseModel):
    user_choice: Annotated[int, Field(..., description="Model choice: 1 for Google Gemini, 2 for Groq", ge=1, le=2)]
    query: Annotated[str, Field(..., description="Query to test the model with")]

