from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import firestore
from google.cloud import texttospeech
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import io

app = FastAPI()

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Firestore
db = firestore.Client()

# Initialize TTS
tts_client = texttospeech.TextToSpeechClient()

# Initialize Vertex AI
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "prompt-wars-hackathon-493408")
REGION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
try:
    vertexai.init(project=PROJECT_ID, location=REGION)
    model = GenerativeModel("gemini-2.5-flash")
except Exception as e:
    print(f"Warning: Failed to initialize Vertex AI: {e}")
    model = None

# Pydantic models
class EligibilityRequest(BaseModel):
    age: int
    is_citizen: bool

class ChatRequest(BaseModel):
    message: str

class TTSRequest(BaseModel):
    text: str

# Endpoints
@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/api/static-content")
@limiter.limit("10/minute")
async def get_static_content(request: Request):
    try:
        # Fetch FAQs from Firestore
        faqs_ref = db.collection("faqs")
        docs = faqs_ref.stream()
        faqs = []
        for doc in docs:
            faqs.append(doc.to_dict())
        return {"faqs": faqs}
    except Exception as e:
        print(f"Error fetching from Firestore: {e}")
        # Fallback if Firestore is empty or fails
        return {"faqs": []}

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
@limiter.limit("5/minute")
async def chat_with_assistant(request: Request, req: ChatRequest):
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

@app.post("/api/tts")
@limiter.limit("5/minute")
async def text_to_speech(request: Request, req: TTSRequest):
    # Constraint: Limit text length to keep audio short (<10s)
    # Roughly 15 characters per second, so 150 characters ~ 10s
    if len(req.text) > 150:
        req.text = req.text[:147] + "..."

    # Basic language detection for TTS
    lang_code = "en-IN"
    if any("\u0900" <= c <= "\u097F" for c in req.text):
        lang_code = "hi-IN"
    elif any("\u0980" <= c <= "\u09FF" for c in req.text):
        lang_code = "bn-IN"

    input_text = texttospeech.SynthesisInput(text=req.text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        response = tts_client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        return StreamingResponse(io.BytesIO(response.audio_content), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
