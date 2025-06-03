from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.api.utils import supabase  # Supabase client
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request and response schemas
class ReflectRequest(BaseModel):
    user_id: str  # User ID for fetching data

class ReflectResponse(BaseModel):
    summary: str
    emotional_trends: dict  # Example: {"joy": 5, "sadness": 3, "anger": 2}
    insights: list[str]  # Example: ["You tend to feel anxious mid-week", "Outdoor activities improve your mood"]
    reflection_image_url: str = None  # Optional: URL to DALL·E-generated image

@router.post("/reflect", response_model=ReflectResponse)
async def reflect_on_journals(request: ReflectRequest):
    """
    Provides weekly insights based on past journal entries.
    """
    try:
        # Calculate the date range for the past week
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)

        # Fetch journal summaries and emotions from the database
        response = supabase.table("conversation_summaries").select("*").filter(
            "user_id", "eq", request.user_id
        ).filter(
            "date", "gte", start_date.isoformat()
        ).filter(
            "date", "lte", end_date.isoformat()
        ).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="No journal entries found for the past week.")

        # Aggregate summaries and emotions
        summaries = [entry["summary"] for entry in response.data]
        emotions = [emotion for entry in response.data for emotion in entry["emotions"]]
        emotional_trends = {emotion: emotions.count(emotion) for emotion in set(emotions)}

        # Generate weekly summary using GPT
        summary_prompt = (
            "Summarize the user's journal entries for the past week. "
            "Include emotional trends and key themes:\n\n"
            + "\n".join(summaries)
        )
        summary_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a summarization assistant."}, {"role": "user", "content": summary_prompt}],
            max_tokens=200,
            temperature=0.7
        )
        summary = summary_response.choices[0].message.content.strip()

        # Generate insights using GPT
        insights_prompt = (
            "Based on the user's journal entries and emotional trends, generate actionable insights. "
            "For example, 'You tend to feel anxious mid-week' or 'Outdoor activities improve your mood'. "
            "Provide 3-5 insights."
        )
        insights_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an insights assistant."}, {"role": "user", "content": insights_prompt}],
            max_tokens=150,
            temperature=0.7
        )
        insights = insights_response.choices[0].message.content.strip().split("\n")

        # Optional: Generate reflection image using DALL·E
        reflection_image_url = None
        try:
            image_response = client.images.create(
                prompt=f"Create an artistic representation of the user's week based on the theme: {summary}",
                n=1,
                size="512x512"
            )
            reflection_image_url = image_response["data"][0]["url"]
        except Exception as e:
            print(f"Error generating reflection image: {e}")

        return ReflectResponse(
            summary=summary,
            emotional_trends=emotional_trends,
            insights=insights,
            reflection_image_url=reflection_image_url
        )
    except Exception as e:
        print(f"Error reflecting on journals: {e}")
        raise HTTPException(status_code=500, detail=f"Error reflecting on journals: {str(e)}")