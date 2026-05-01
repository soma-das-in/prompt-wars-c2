---
trigger: always_on
---

# Backend Development Rules

These rules define how the backend for the **VoteAssist** application must be implemented.

The backend must be lightweight, secure, and suitable for deployment on **Google Cloud Run**.

---

# Backend Technology Stack

The backend must use the following technologies:

- Python
- FastAPI
- Uvicorn (ASGI server)
- Google Vertex AI (Gemini) for AI responses

Avoid adding unnecessary frameworks or dependencies.

---

# Backend Responsibilities

The backend must:

1. Receive user queries from the frontend.
2. Process the request and validate inputs.
3. Generate responses using Google Vertex AI Gemini.
4. Return structured JSON responses to the frontend.

The backend must **not perform heavy computation** or maintain persistent state.

---

# API Design Rules

APIs must follow simple REST design.

Example endpoint:

POST /api/chat

Request Example

```json
{
  "message": "How do I register to vote in India?"
}
```

Response Example

```json

{
  "reply": "To register to vote in India you must..."
}
```

Rules:

- All responses must be JSON.
- Validate user inputs.
- Limit message length to avoid excessive AI token usage.



## Security Rules

The backend must follow basic security practices:

- Do not log sensitive user inputs.
- Sanitize and validate user inputs before processing.
- Limit request size to prevent abuse.
- Protect against prompt injection where possible.
- Do not store or transmit personal voter information.
- The application must operate without collecting personal data.

---

## Efficiency Rules

Because the project operates under **limited cloud credits**, the backend must be optimized for efficiency.

- Minimize calls to the AI model.
- Use short and simple prompt templates.
- Avoid maintaining long conversation histories.
- Process each request independently (stateless design).
- Avoid unnecessary backend processing or heavy computations.

---

## Code Quality Rules

Backend code must be **clean, readable, and maintainable**.

- Use a clear and simple folder structure.
- Separate API routes from AI service logic.
- Use meaningful variable and function names.
- Add comments for key functions and logic blocks.
- Keep functions small and focused.

## Recommended Project Structure

The backend should follow a simple and maintainable structure.

```
app/
   main.py
   routes/
      chat.py
   services/
      gemini_service.py
   config/
      settings.py
```
- Backend implementation must only support MVP features defined in the docs folder

