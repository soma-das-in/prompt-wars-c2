# Google Services Integration

VoteAssist meaningfully integrates Google Cloud services.

---

## Cloud Run

Purpose:

- Host backend API
- Provide serverless execution

Benefits:

- Automatic scaling
- Low operational cost
- Simple deployment

---

## Vertex AI

Vertex AI provides the AI assistant capability.

Model used:

Gemini 2.5 Flash

Capabilities:

- Natural language understanding
- Question answering
- Multilingual responses

---

## Cloud Build

Cloud Build is used to:

- Build container images
- Deploy application to Cloud Run

---

## IAM

Identity and Access Management ensures:

- Secure service access
- Controlled API permissions

---

## Google Cloud Firestore

Firestore is used as a lightweight NoSQL database to store structured election education data.

Use cases:

- Voter FAQs
- Election process guides
- Official election resources

Firestore is used primarily for read operations to reduce AI calls and improve cost efficiency.

---

## Voice Capabilities

To stay within budget and improve performance, the application uses a hybrid voice approach:

### Browser-Native Speech-to-Text (STT)
The application utilizes the **Web Speech API** (`webkitSpeechRecognition`) for speech-to-text. This allows for zero-cost voice input processing on the client side without incurring GCP STT costs.

### Google Cloud Text-to-Speech (TTS)
Google Cloud Text-to-Speech is used to convert system responses into high-quality spoken audio. 
- **Multilingual Support:** Native voices for English, Hindi, and Bengali.
- **Cost Control:** Responses are strictly limited to ≤10 seconds and triggered only on user interaction.

---

## Why Google Services

Google services enable:

- Rapid development
- Low-cost infrastructure
- Reliable deployment