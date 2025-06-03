from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
import re
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

class AnalyzeRequest(BaseModel):
    text: str
    user_id: str
    conversation: list

class AnalyzeResponse(BaseModel):
    chunks: list
    emotions: list
    colors: list

EMOTION_COLOR_MAP = {
    "joy": "yellow",
    "anger": "red",
    "sadness": "blue",
    "fear": "purple",
    "neutral": "gray",
}

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_emotion(chunk: str) -> str:
    """
    Analyze the emotion of a text chunk using OpenAI's API.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are an empathetic AI for a journaling app. "
                    "Classify the primary emotion in each journal entry or sentence. "
                    "Only respond with one of: joy, anger, sadness, fear, or neutral."
                )},
                {"role": "user", "content": f"Classify the emotion of this text: '{chunk}'. Respond with only one of: joy, anger, sadness, fear, or neutral."}
            ],
            max_tokens=10,
            temperature=0
        )
        emotion = response.choices[0].message.content.strip().lower()
        return emotion if emotion in EMOTION_COLOR_MAP else "neutral"
    except Exception as e:
        print(f"Error analyzing emotion: {e}")  # Log the error
        raise HTTPException(status_code=500, detail=f"Error analyzing emotion: {str(e)}")

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest):
    """
    Break text into chunks, analyze emotions, and map to colors.
    """
    print("Received text to analyze:", request.text)
    text = request.text
    chunks = re.split(r'(?<=[.!?]) +', text.strip())
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    
    emotions = []
    colors = []

    for chunk in chunks:
        emotion = analyze_emotion(chunk)
        emotions.append(emotion)
        colors.append(EMOTION_COLOR_MAP.get(emotion, "gray"))

    return AnalyzeResponse(chunks=chunks, emotions=emotions, colors=colors)
