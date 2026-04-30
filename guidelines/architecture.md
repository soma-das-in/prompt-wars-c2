# Vote Assist – System Architecture

## Overview

Vote Assist is an AI-powered assistant designed to help Indian voters understand the election process in a simple, interactive way.

The system focuses on:
- Election process education
- Voter Registration Help
- Voter eligibility guidance
- Voting process explanation 
- Frequently asked questions about elections

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
Cloud Run Service (FastAPI backend)  
↓  
Vertex AI Gemini Model

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
- No database required

---

## Future Architecture Improvements

Possible future extensions:

- Polling booth locator
- Real-time election timelines
- Integration with voter databases
- Voice interaction