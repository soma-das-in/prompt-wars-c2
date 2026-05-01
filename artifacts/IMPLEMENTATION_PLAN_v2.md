# VoteAssist MVP Implementation Plan (v2)

This high-level project plan outlines the implementation of the VoteAssist MVP based on the validated scope and the finalized Vanilla HTML/JS/FastAPI technology stack.

## User Review Required

- Please review the phased implementation steps to ensure they align with your expectations for the hackathon MVP.
- Verify the newly added automated unit testing scope.

## Proposed Changes

The implementation will be divided into the following sequential phases:

---

### Phase 1: Project Initialization & Data Layer
- **Directory Structure:** Create the base project layout separating backend logic and frontend assets (e.g., `app/`, `app/routes/`, `app/services/`, `static/`).
- **Dependencies:** Define `requirements.txt` with the minimal necessary packages (`fastapi`, `uvicorn`, `google-cloud-aiplatform`, `pytest`, `httpx`).
- **Static Content:** Generate `static_content.json` following the schema defined in `guidelines/static_data_format.md` to store FAQs and election process steps locally.

---

### Phase 2: Backend Development (FastAPI)
- **Core App Setup:** Initialize the FastAPI application and configure middleware to serve static frontend files.
- **Eligibility Endpoint (`POST /api/eligibility`):** Implement standard rule-based conditional logic (checking for age $\ge$ 18 and Indian citizenship) to determine eligibility without invoking the LLM.
- **Static Content Endpoint (`GET /api/static-content`):** Create a route to serve the in-memory `static_content.json` to the frontend.
- **Chat API (`POST /api/chat`):** 
  - Integrate Google Vertex AI (Gemini Flash).
  - Enforce the system prompts from `prompt_rules.md` to ensure neutral, educational, and safe responses.
  - Ensure the endpoint returns structured JSON.
- **Statelessness & Security:** Implement input validation on all routes and verify no session state or personal data is stored.

---

### Phase 3: Frontend Development (Vanilla UI)
- **Markup (`index.html`):** Build a semantic, accessible HTML structure matching the layout in `ui_design.md` (Header, Suggested Questions, Chat Window, Input Box).
- **Styling (`styles.css`):** Implement a custom, mobile-first CSS design focusing on readability, large fonts, and high contrast (strictly avoiding frameworks like Tailwind).
- **Logic (`app.js`):** 
  - Fetch and render suggested questions from the backend static endpoint.
  - Handle user input and chat interface interactions.
  - Implement visual loading indicators while waiting for Vertex AI responses.
  - Add graceful error handling and user-friendly fallback messages.

---

### Phase 4: Containerization & Cloud Run Prep
- **Dockerization:** Create a minimal `Dockerfile` using a lightweight Python base image (e.g., `python:3.9-slim`).
- **Server Config:** Configure Uvicorn to bind to `0.0.0.0` and expose port `8080`.
- **Environment:** Prepare deployment scripts or instructions to handle GCP Project ID and Region configuration.

---

### Phase 5: Automated Logic Testing
- **Test Setup:** Configure `pytest` and `httpx` for testing the FastAPI application.
- **Eligibility Logic Verification:** Create automated test cases to assert that boundary conditions (e.g., age 17 vs 18) are correctly handled by the backend conditional statements.
- **Data & Routing Tests:** 
  - Validate that `static_content.json` is correctly parsed.
  - Ensure API endpoints correctly reject malformed payloads with HTTP 422 errors.

---

### Phase 6: Deployment & Verification
- **Deployment:** Push the container and deploy the service to Google Cloud Run.
- **IAM Configuration:** Ensure the Cloud Run service account has the necessary permissions to invoke Vertex AI.

## Verification Plan

### Local Verification
- Run the backend locally (`uvicorn app.main:app`) and verify the REST endpoints (`/api/chat`, `/api/eligibility`) using sample payloads.
- Run the automated test suite (`pytest`) to verify all backend logic tests pass.
- Check the repository size locally to guarantee it remains well under the 1 MB constraint.

### Manual Live Verification
- Access the public Cloud Run URL.
- Test the chat UI with both English and regional language queries to confirm that Vertex AI handles multilingual responses correctly.
- Test the eligibility form with boundary cases on the live UI to verify the static backend logic works end-to-end.
- Verify mobile responsiveness and general accessibility on a live browser.
