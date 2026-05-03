# Vote Assist – System Architecture

## Problem Statement Alignment

Vote Assist is architected to solve the primary challenge of **inaccessible and fragmented election information** in India. The system transforms static, complex official data into an interactive, voice-enabled conversational guide, specifically targeting:
- First-time voters who find official documents intimidating.
- Users with accessibility needs (literacy, language, vision).
- Citizens seeking a verified "source of truth" to combat misinformation.

The architecture is designed to meet the following constraints:

- Cloud Run deployment
- Repository size < 1 MB
- Maximum GCP credits: $5
- Simple maintainable implementation

---

## High Level Architecture

User Browser  
↓  
Frontend (HTML + JavaScript)  
↓  
Voice Input → Speech-to-Text  
↓  
Backend API (FastAPI on Google Cloud Run)  
↓  
Firestore (FAQs and guides)  
↓  
Vertex AI Gemini  
↓  
Text Response  
↓  
Text-to-Speech  
↓  
Voice Output

---

## Component Description

### 1. Frontend

Responsibilities:
- Simple user interface
- Accept user queries
- Display assistant responses

Technology:
- HTML
- CSS
- Vanilla JavaScript

Design goals:
- Minimal size
- No heavy frameworks
- Fast load time

---

### 2. Backend API

Responsibilities:
- Handle user queries
- Process eligibility checks
- Call the AI model
- Return responses to the frontend

Technology:
- Python
- FastAPI

Endpoints:

| Endpoint | Purpose |
|--------|--------|
| `/` | Loads UI |
| `/chat` | Handles user questions |
| `/eligibility` | Checks voting eligibility |

---
## Data Storage

The system uses Google Cloud Firestore for lightweight data storage.

Firestore stores:

- Frequently asked voter questions
- Election process guides
- Official election resource links

The database is read-heavy and stores only static or public information.

No personal voter data is collected or stored.

### Firestore Data Model

Collections:

**faqs**
- question
- answer
- category

**guides**
- title
- steps

**resources**
- name
- url
- description

These collections store publicly available election education information such as voter FAQs, election process guides, and official election resources.


---

### 3. AI Layer

Uses Google Vertex AI Gemini model to:

- Explain election procedures
- Answer voter questions
- Provide multilingual explanations

The prompt ensures:
- Neutral information
- Simple explanations
- Educational content

---

## Deployment Architecture

Cloud Run is used because it provides:

- Serverless execution
- Automatic scaling
- Low cost for small workloads
- Easy container deployment

---

## Data Handling

The system does not store personal data.

All requests are processed statelessly.

---

## Privacy Model

- No user accounts
- No personal information collected


---

## Future Architecture Improvements

Possible future extensions:

- Polling booth locator
- Real-time election timelines
- Integration with voter databases