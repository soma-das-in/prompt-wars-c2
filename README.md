
# VoteAssist

VoteAssist is an AI-powered educational assistant designed to help Indian voters understand the election process in a simple, interactive, and accessible way.

The assistant provides clear explanations about voter registration, election procedures, voting steps, and common voter questions using official information from trusted election resources.

The goal is to improve voter awareness and make election information easier to understand, especially for first-time voters.

---

# Chosen Vertical

Civic Technology – Election Education

This project focuses on **Election Process Education for Indian voters**, helping users understand:

- How elections work in India
- How to register as a voter
- Eligibility requirements
- What happens on voting day
- Frequently asked voter questions

The assistant acts as a **digital guide for voters**, simplifying complex election information into easy-to-understand responses.

---

# Approach and Logic

The solution is designed as a **lightweight AI assistant** that combines:

- A simple web interface
- A backend API
- Google Vertex AI for natural language responses

The system follows these principles:

**Grounded Information**

Responses are based on official election resources such as:

- Election Commission of India
- National Voters’ Service Portal
- SVEEP voter awareness program

**Context-Aware Responses**

The assistant identifies the user's intent and provides relevant guidance for topics such as:

- voter registration
- voting process
- eligibility
- election timelines
- voter FAQs

**Lightweight MVP Design**

To meet privacy, security and performance goals:

- Google Cloud Firestore is used as a stateless, read-only database
- The application is stateless and does not store personal data
- The system relies on trusted information sources rather than storing large datasets

---

# How the Solution Works

## System Architecture

User Browser  
↓  
Frontend (HTML + JavaScript)  
↓  
Voice Input (Browser STT) → Backend API (FastAPI on Google Cloud Run)  
↓  
Firestore (FAQs and Guides)  
↓  
Vertex AI Gemini 2.5  
↓  
Text-to-Speech (Google TTS)

### Frontend

The frontend provides a simple and accessible chat interface where users can ask election-related questions.

Key characteristics:

- Lightweight HTML and JavaScript
- Simple UI for accessibility
- Mobile-friendly design

### Backend

The backend is implemented using **FastAPI**.

Responsibilities include:

- Receiving user queries
- Validating requests
- Sending prompts to Google Vertex AI
- Returning responses to the frontend

The backend remains **stateless and lightweight**.

### AI Layer

Google **Vertex AI Gemini 2.5 Flash** is used to generate natural language responses. This state-of-the-art model provides high-quality, nuanced answers while maintaining the speed required for a conversational interface.

Prompt rules ensure that the assistant:
- Provides educational guidance
- Uses trusted election information
- Remains strictly politically neutral
- Supports multiple languages (English, Hindi, Bengali)

### Deployment

The backend is containerized and deployed on **Google Cloud Run**, enabling scalable and cost-efficient hosting.

---

# Google Services Used

The project uses the following Google Cloud services:

| Service | Purpose |
|------|------|
Google Cloud Run | Hosts the backend API |
Google Vertex AI (Gemini 2.5) | Generates conversational responses |
Google Cloud Firestore | Stateless, read-only storage for FAQs and guides |
Google Cloud Text-to-Speech | Generates audio responses in English, Hindi, and Bengali |
Artifact Registry | Stores container images |

These services enable a **fully cloud-native deployment**
---

# Key Features

The MVP supports the following features:

**Election Process Guide**

Explains the stages of elections in India including nomination, campaigning, voting, counting, and results.

**Voter Registration Guidance**

Provides information about:

- eligibility criteria
- registration process
- required documents

**How to Vote Guide**

Explains the voting process at polling booths, including the use of Electronic Voting Machines (EVMs).

**Eligibility Explanation**

Clarifies who is eligible to vote in India using simple rule-based conditional checks (age and citizenship) on the backend to avoid unnecessary AI API calls.

**Voter FAQs**

Answers common voter questions related to election participation.

**Multilingual Voice Assistance**

Supports voice interaction via browser-native Speech-to-Text (STT) and backend Text-to-Speech (TTS). The assistant can speak back in:
- English
- Hindi
- Bengali

**Dynamic FAQ System**

Suggested questions are dynamically fetched from Google Cloud Firestore, allowing for easy updates to the knowledge base without redeploying the application.

**API Security & Rate Limiting**

Implemented security best practices including:
- **CORS Middleware:** Restricts API access to authorized origins.
- **Rate Limiting:** Protects against abuse and protects the hackathon budget.
- **Input Validation:** Strict Pydantic models for all API requests.

---

# Accessibility Considerations

The system is designed to be simple and accessible:

- Clear conversational interface with typing indicators
- Simple UI design with high-contrast elements
- **Voice Interaction:** Click-to-activate microphone for users with reading difficulties
- **Multilingual Support:** Fully conversational in English, Hindi, and Bengali
- Suitable for first-time voters and elderly users

---

# Security and Privacy

Vote Assist follows responsible design practices:

- No personal data is stored
- No authentication or user tracking
- Inputs are sanitized to prevent misuse
- The assistant does not provide political opinions or endorsements

The system is designed purely for **educational purposes**.

---

# Assumptions

The following assumptions were made for the MVP:

- The assistant provides **educational guidance only**, not official voter registration services.
- Users will visit official government portals for actions such as voter registration or polling booth lookup.
- Election information is sourced from trusted public resources.
- The system is designed as a **lightweight hackathon prototype**, not a production election system.

---

# Project Goal

The goal of VoteAssist is to make **election education simple, accessible, and interactive**, helping citizens better understand the democratic process in India.

