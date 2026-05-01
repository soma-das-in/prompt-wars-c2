# Backend Tech Stack

This document outlines the backend architecture and technology stack for VoteAssist.

## Core Technologies
- **Python (3.9+)**: The primary language for the backend service.
- **FastAPI**: A modern, high-performance web framework for building APIs.
- **Uvicorn**: An ASGI web server implementation for Python, used to serve the FastAPI application.
- **Google Vertex AI (Gemini Flash)**: The LLM used to process user queries and generate election-related guidance.

## Infrastructure & Deployment
- **Google Cloud Run**: For serverless, scalable, and stateless deployment of the containerized backend.
- **Docker**: For containerizing the application and its dependencies.

## Key Principles
1. **Stateless Operations**: No databases or persistent storage will be used for privacy and security reasons and for cost optimization.
2. **Cost-Effective AI**: Minimize LLM requests by handling logic like eligibility checks directly in the backend Python code using rule-based conditional statements.
3. **JSON REST API**: All communication with the frontend will happen over simple JSON-based REST endpoints.
