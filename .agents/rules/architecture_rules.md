---
trigger: always_on
---

# Architecture Rules

The system must follow a lightweight architecture suitable for a MVP

Architecture Flow

User Browser  
↓  
Frontend (HTML + JavaScript)  
↓  
FastAPI Backend (Containerized)  
↓  
Google Cloud Run  
↓  
Google Vertex AI (Gemini)

Description

- The frontend is served as static files.
- The backend API is implemented using FastAPI.
- The backend runs inside a Docker container deployed on Google Cloud Run.
- The backend communicates with Google Vertex AI to generate assistant responses.

Rules

- The system must remain stateless.
- No database should be used.
- All data should be processed in memory.
- The backend must expose simple REST endpoints.
- The frontend must communicate with the backend using the fetch API.

Infrastructure Constraints

- The backend must be deployable to Google Cloud Run.
- The container must listen on port 8080.
- The application must be lightweight to stay within the hackathon cost limits.

Avoid complex architecture patterns.

Do not introduce:

- microservices
- message queues
- external databases
- heavy frontend frameworks

The architecture must remain simple, maintainable, and easy to deploy.