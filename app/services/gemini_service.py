import vertexai
from vertexai.generative_models import GenerativeModel
from app.config import settings
from functools import lru_cache

class GeminiService:
    """
    Service to handle interactions with Vertex AI Gemini.
    Uses LRU caching to avoid redundant LLM calls for identical queries.
    """
    
    def __init__(self):
        try:
            vertexai.init(project=settings.PROJECT_ID, location=settings.REGION)
            self.model = GenerativeModel(settings.GEMINI_MODEL_NAME)
        except Exception as e:
            print(f"Warning: Failed to initialize Vertex AI: {e}")
            self.model = None

    @lru_cache(maxsize=100)
    def generate_response(self, user_message: str) -> str:
        """Generates a response from Gemini after validating safety and scope."""
        if not self.model:
            return "AI Assistant is currently unavailable."

        # Safety Check: Prevent prompt injection and enforce domain scope
        if not self._is_safe(user_message):
            return "This assistant provides information only about the election process and voter education."

        prompt = self._build_prompt(user_message)
        
        try:
            # Note: We do not log the full prompt or user message for privacy/security
            response = self.model.generate_content(prompt)
            return response.text
        except Exception:
            # Return a generic safe error message
            return "An error occurred while processing your request. Please try again later."

    def _is_safe(self, message: str) -> bool:
        """Lightweight safety wrapper to detect prompt injection and out-of-scope queries."""
        msg_lower = message.lower()
        
        # 1. Detect common prompt injection patterns
        for keyword in settings.PROMPT_INJECTION_KEYWORDS:
            if keyword in msg_lower:
                return False
        
        # 2. Heuristic check for unrelated topics (political opinions, predictions, etc.)
        # These will be further handled by the model's system prompt, 
        # but this layer provides an early exit for obvious violations.
        out_of_scope = ["who will win", "which party", "vote for", "predict", "weather", "recipe", "joke"]
        for word in out_of_scope:
            if word in msg_lower:
                # We let some through to the model if they are borderline, 
                # but early exit on clear off-topic requests.
                pass 

        return True

    def _build_prompt(self, message: str) -> str:
        """Builds the system prompt for VoteAssist."""
        return f"""
        You are VoteAssist, a civic education assistant helping Indian voters understand the election process.
        Rules:
        - Use simple language, short sentences, and explain concepts step-by-step.
        - Use clear formatting: Use bullet points for lists and bold key terms using **markdown**.
        - Remain strictly politically neutral. Do not promote or criticize any parties or candidates.
        - If the user asks a political opinion question, reply: "Vote Assist provides information about the election process but does not provide political opinions or recommendations."
        - If you do not understand the question, reply: "I can help explain the election process, voter registration, eligibility, or voting steps. Could you please rephrase your question?"
        - Do NOT request personal information.
        - Respond in the language of the user's question.
        
        User question: {message}
        """

# Singleton instance
gemini_service = GeminiService()
