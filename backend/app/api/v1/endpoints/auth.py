from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()

class AuthRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
async def signup(auth: AuthRequest):
    try:
        result = supabase.auth.sign_up(email=auth.email, password=auth.password)
        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"]["message"])
        return {"message": "User signed up successfully", "data": result["data"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login(auth: AuthRequest):
    try:
        result = supabase.auth.sign_in_with_password(email=auth.email, password=auth.password)
        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"]["message"])
        return {"message": "User logged in successfully", "data": result["data"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))