# All the Pydantic Models are here Whether it is used for the chatbot or the Output parser or the Fastapi Things.

from pydantic import BaseModel,Field
from typing import List,Literal,Annotated

class SummaryResponse(BaseModel):
    summary: Annotated[str, Field(..., description="Write the Concise call summary From the Transcript")]
    duration_minutes: Annotated[int, Field(..., description="Calculate the Call duration in minutes")]
    no_of_participants: Annotated[int, Field(..., description="Count the number of participants")]
    key_aspects: Annotated[List[str], Field(..., description="List the key discussion points as bullet points")]
    sentiment: Annotated[Literal["Positive", "Negative", "Neutral"], Field(..., description="Mention the sentiment of the call")]

