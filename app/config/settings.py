import os

# Google Cloud Settings
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "prompt-wars-hackathon-493408")
REGION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

# Model Settings
GEMINI_MODEL_NAME = "gemini-2.5-flash"

# Rate Limiting Settings
CHAT_LIMIT = "5/minute"
CONTENT_LIMIT = "10/minute"
TTS_LIMIT = "5/minute"

# Security Settings
MAX_QUERY_LENGTH = 500  # Maximum characters for user queries
ALLOWED_DOMAINS = ["*"] # In production, this should be specific domains
PROMPT_INJECTION_KEYWORDS = ["ignore previous instructions", "reveal system prompt", "system instructions", "you are now"]
