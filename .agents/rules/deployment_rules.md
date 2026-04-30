---
trigger: always_on
---

# Deployment Rules

The application must be deployable to Google Cloud Run.

Requirements:

- Application must run inside a Docker container.
- FastAPI should run using Uvicorn.
- The container must expose port 8080.

Example startup command:

uvicorn app.main:app --host 0.0.0.0 --port 8080

Avoid system dependencies that increase container size.