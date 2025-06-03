from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import transcribe, analyze, respond, auth , reflect

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcribe.router, prefix="/api/v1")
app.include_router(analyze.router, prefix="/api/v1")
app.include_router(respond.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(reflect.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Hello from Render!"}

