from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.api.utils import supabase  # Supabase client

load_dotenv()

router = APIRouter()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request and response schemas
class Message(BaseModel):
    role: str  # 'user', 'assistant', or 'system'
    content: str

class RespondRequest(BaseModel):
    user_id: str
    conversation: list[Message]

class RespondResponse(BaseModel):
    reply: str
    summary: str
    emotions: list[str]  # Include emotions in the response

@router.post("/respond", response_model=RespondResponse)
async def respond_to_conversation(request: RespondRequest):
    """
    Handles user conversation, generates GPT response, and stores a daily summary and emotions in the database.
    """
    try:
        # Detect emotions from the conversation
        detected_emotions = []
        for msg in request.conversation:
            if msg.role == "assistant" and "I noticed these emotions:" in msg.content:
                emotions = msg.content.replace("I noticed these emotions:", "").strip().split(",")
                detected_emotions.extend([emotion.strip() for emotion in emotions])

        # Remove duplicates and aggregate emotions
        aggregated_emotions = list(set(detected_emotions))

        # System prompt for GPT
        system_prompt = (
            "You are a compassionate, trustworthy AI journaling companion. "
            "Your job is to help users reflect on their thoughts, process their emotions, "
            "and gain insights through natural conversation. "
            "Ask thoughtful follow-up questions, identify emotional patterns, and encourage the user to explore their feelings and experiences more deeply. "
            "Always be supportive, non-judgmental, and help the user feel safe and understood."
        )
        if aggregated_emotions:
            system_prompt += f"\nThe user's current emotional state is: {', '.join(aggregated_emotions)}. Use this to guide your response."

        # Prepare messages for GPT
        messages = [{"role": "system", "content": system_prompt}] + [
            {"role": m.role, "content": m.content} for m in request.conversation
        ]

        # Generate AI response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()

        # Check if a daily summary already exists for the user
        today = datetime.utcnow().date()
        existing_summary = supabase.table("conversation_summaries").select("*").filter(
            "user_id", "eq", request.user_id
        ).filter(
            "date", "eq", today.isoformat()
        ).execute()

        # Generate daily summary using GPT
        daily_summary_prompt = (
            "Summarize all conversations for the day. "
            "Include emotional trends and key themes:\n\n"
            + "\n".join([f"{msg.role}: {msg.content}" for msg in request.conversation])
        )
        daily_summary_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a summarization assistant."}, {"role": "user", "content": daily_summary_prompt}],
            max_tokens=200,
            temperature=0.7
        )
        daily_summary = daily_summary_response.choices[0].message.content.strip()

        # Update or insert the daily summary in the database
        if existing_summary.data:
            # Update the existing summary
            supabase.table("conversation_summaries").update({
                "summary": daily_summary,
                "emotions": aggregated_emotions,
                "updated_at": datetime.utcnow().isoformat()
            }).filter(
                "user_id", "eq", request.user_id
            ).filter(
                "date", "eq", today.isoformat()
            ).execute()
        else:
            # Insert a new summary
            supabase.table("conversation_summaries").insert({
                "user_id": request.user_id,
                "summary": daily_summary,
                "emotions": aggregated_emotions,
                "date": today.isoformat(),  # Add the date field
                "created_at": datetime.utcnow().isoformat()
            }).execute()

        return RespondResponse(reply=reply, summary=daily_summary, emotions=aggregated_emotions)
    except Exception as e:
        print(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
