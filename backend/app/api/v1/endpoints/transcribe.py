from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from pydub import AudioSegment
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
# Define the response schema
class TranscribeResponse(BaseModel):
    text: str
router = APIRouter()

@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribes uploaded audio file using OpenAI's Whisper API.
    """
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"/tmp/{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Convert the file to .mp3 format if necessary
        mp3_file_path = f"/tmp/{os.path.splitext(file.filename)[0]}.mp3"
        if not file.filename.endswith(".mp3"):
            audio = AudioSegment.from_file(temp_file_path, format=file.content_type.split("/")[-1])
            audio.export(mp3_file_path, format="mp3")
            os.remove(temp_file_path)  # Remove the original file
        else:
            mp3_file_path = temp_file_path

        # Use OpenAI Whisper API for transcription
        with open(mp3_file_path, "rb") as audio_file:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            print("OpenAI Whisper API response:", response.text)  # Log the response

        # Clean up the temporary file
        os.remove(mp3_file_path)

        # Return the transcribed text
        return TranscribeResponse(text=response.text)

    except Exception as e:
        print(f"Error during transcription: {e}")  # Log the error
        raise HTTPException(status_code=500, detail=f"Error transcribing audio: {str(e)}")



