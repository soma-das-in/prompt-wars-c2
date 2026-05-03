# Implementation Plan: VoteAssist MVP Scope Adjustments

## Goal Description
This plan outlines the steps required to implement the finalized MVP scope for VoteAssist. The scope includes migrating from static JSON to Google Cloud Firestore, integrating budget-conscious Voice Capabilities (STT/TTS), applying a UI bug fix, enhancing API security, and introducing automated unit testing for backend logic. The plan ensures that the project remains lightweight (under 1 MB repo size), cost-effective (< $5 budget), and strictly follows vanilla web principles and FastAPI best practices.

## User Review Required
> [!IMPORTANT]
> Please review the phasing and proposed changes to ensure they align with the timeline and budget expectations. Specifically, review the Voice API limits (strictly ≤10 seconds per request, click-to-activate only). 

## Open Questions
> [!NOTE]
> 1. Will the static data (FAQs, guides) be pre-seeded into Firestore via the Google Cloud Console, or should we include a one-off python script in the repository to populate Firestore initially?
> 2. For the STT implementation, should we handle audio recording via the native Web Audio API in vanilla JS and send the raw blob to the backend, or should we rely entirely on the browser's native `webkitSpeechRecognition` (which avoids GCP STT costs entirely, though backend TTS would still be used)?

## Proposed Changes

### Phase 1: Security and Code Quality Foundation
* **Dependencies & Tooling:** Add `pytest` for automated testing. Ensure standard linting with `flake8` and `black`.
* **API Security:** Configure FastAPI CORS middleware to strictly allow only the frontend origin.
* **Rate Limiting:** Implement basic in-memory rate limiting for the `/chat` and voice endpoints to prevent abuse and protect the $5 budget limit.
* **Secret Management:** Ensure Google Cloud credentials and Vertex AI parameters are strictly loaded from environment variables.

---

### Phase 2: Database Migration (Firestore)
* **Setup:** Configure the `google-cloud-firestore` client in the FastAPI backend.
* **Implementation:** Create a service module (`firestore_service.py`) to handle read-only queries from the `faqs` and `guides` collections.
* **Deprecation:** Remove the legacy `static_content.json` file and its parsing logic. Ensure the `/api/static-content` (or equivalent) endpoint serves data directly from Firestore.

---

### Phase 3: Voice Interaction Integration
* **Backend Audio Handling (`voice_service.py`):**
    * Implement an endpoint to receive audio blobs for Speech-to-Text.
    * Implement Text-to-Speech generation for assistant responses.
* **Constraint Enforcement:** 
    * Add backend validation to strictly reject STT audio payloads that exceed 10 seconds.
    * Add validation to keep AI text responses concise before sending them to TTS.

---

### Phase 4: Frontend UI and Logic Updates
* **UI Bug Fix:** Adjust CSS styling for the Quick Eligibility Check to ensure the "I am an Indian citizen" checkbox is perfectly visible and accessible.
* **Voice UI:** Add a microphone icon button to the chat interface. Ensure the button acts as a push-to-talk or click-to-activate trigger.
* **Audio Logic (Vanilla JS):** Implement the Web Audio API to record audio, send the Blob to the backend STT endpoint, and play the returned TTS audio buffer. Ensure robust error handling for browser microphone permissions.

---

### Phase 5: Automated Testing
* **Test Suite Creation:** Create a `tests/` directory and configure `pytest`.
* **Implement Tests (`test_logic.py`):**
    * Eligibility Logic: Boundary tests for ages `< 18` and `≥ 18`.
    * Firestore Integration: Mock and verify that Firestore data retrieval executes cleanly and matches the required schema.
    * Voice Constraints: Verify that endpoints explicitly return `422 Unprocessable Entity` or `400 Bad Request` if audio exceeds the 10-second limit.
    * API Routing: Validate error handling for malformed requests.

---

### Phase 6: Deployment & Verification
* **Cloud Run Update:** Rebuild the Docker container and deploy the updated stateless application to Google Cloud Run.
* **IAM Configuration:** Verify that the Cloud Run service account has the exact least-privilege roles required (`Cloud Datastore User` for Firestore, `Vertex AI User`, and optionally `Cloud Speech Client`/`Cloud Text-to-Speech Client`).

## Verification Plan

### Automated Tests
- Run `pytest` locally to verify 100% pass rate for Eligibility, Firestore reads, Voice limits, and API validation.

### Manual Verification
1. **UI Verification:** Open the site on mobile and desktop views to verify the eligibility checkbox visibility.
2. **Voice Interaction:** Click the microphone, speak a 5-second question, and verify the text appears, Vertex AI answers, and the TTS audio plays. Attempt an 11-second audio recording and verify the UI properly displays an error without crashing.
3. **Firestore Data:** Ask a known FAQ question and ensure the answer matches the seeded Firestore data instead of a generated AI hallucination.
