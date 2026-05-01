from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import os
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load static content
with open("static_content.json", "r") as f:
    STATIC_CONTENT = json.load(f)

# Initialize Vertex AI
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "prompt-wars-hackathon-493408")
REGION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
try:
    vertexai.init(project=PROJECT_ID, location=REGION)
    # Using gemini-2.5-flash as requested
    model = GenerativeModel("gemini-2.5-flash")
except Exception as e:
    print(f"Warning: Failed to initialize Vertex AI: {e}")
    model = None

# Pydantic models for request validation
class EligibilityRequest(BaseModel):
    age: int
    is_citizen: bool

class ChatRequest(BaseModel):
    message: str

# Endpoints
@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/api/static-content")
def get_static_content():
    return STATIC_CONTENT

@app.post("/api/eligibility")
def check_eligibility(req: EligibilityRequest):
    if req.age >= 18 and req.is_citizen:
        return {"status": "eligible", "message": "You are eligible to register as a voter."}
    else:
        reasons = []
        if req.age < 18:
            reasons.append("you must be at least 18 years old")
        if not req.is_citizen:
            reasons.append("you must be an Indian citizen")
        reason_str = " and ".join(reasons)
        return {"status": "ineligible", "message": f"You are not eligible because {reason_str}."}

@app.post("/api/chat")
def chat_with_assistant(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=422, detail="Message cannot be empty")
        
    if not model:
        raise HTTPException(status_code=500, detail="AI Model not initialized")
        
    prompt = f"""
    You are VoteAssist, a civic education assistant helping Indian voters understand the election process.
    Rules:
    - Use simple language, short sentences, and explain concepts step-by-step.
    - Use clear formatting: Use bullet points for lists and bold key terms using **markdown**.
    - Remain strictly politically neutral. Do not promote or criticize any parties or candidates.
    - If the user asks a political opinion question, reply: "Vote Assist provides information about the election process but does not provide political opinions or recommendations."
    - If you do not understand the question, reply: "I can help explain the election process, voter registration, eligibility, or voting steps. Could you please rephrase your question?"
    - Do NOT request personal information.
    - Respond in the language of the user's question.
    
    User question: {req.message}
    """
    
    try:
        response = model.generate_content(prompt)
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
