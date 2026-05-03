# Implementation Scope Review

## Scope Cohesion & Realism
* **UI Checkbox Fix:** Fixing the quick eligibility check visibility issue is a minor CSS adjustment and is completely realistic and cohesive for the MVP.
* **Firestore Data Storage:** Realistic and cohesive if restricted to storing static, read-only content (like FAQs and guides), as defined in the architecture guidelines.
* **Multilingual Voice Assistance:** Introducing full voice support (Bengali, English, Hindi) is highly ambitious for a lightweight MVP and challenges the project's strict constraints.

## Ambiguity & Over-Engineering Risks
* **Database Ambiguity:** The `README.md` explicitly states "No database is used," whereas `architecture.md` outlines Firestore usage. This contradiction creates implementation ambiguity.
* **Scope Contradiction:** Voice interaction is currently listed as "Out of Scope for MVP" in both `product_requirements.md` and `assumptions.md`.
* **Budget and Size Risks:** Implementing real-time Speech-to-Text and Text-to-Speech via Google Cloud could push the project past the < $5 GCP budget limit and the strict < 1 MB repository size constraint.
* **Frontend Over-Engineering:** Handling multi-language audio recording and playback purely in Vanilla JS without frameworks risks over-engineering the lightweight UI.

## Additional Guidelines Required
* **Documentation Synchronization:** Existing guidelines (`README.md`, `assumptions.md`, `product_requirements.md`) need to be updated to reflect Firestore and Voice as "In Scope".
* **Voice Integration Strategy:** Specific technical guidelines are needed for implementing Google Cloud STT/TTS cleanly in Vanilla JS and FastAPI without bloating the repository.

## Proposed Clarifications
* **Firestore Usage:** Clarify whether Firestore will completely replace existing static JSON files and confirm it remains stateless and read-only (no user data stored).
* **Voice Capabilities:** Clarify if voice assistance must be fully functional via APIs for the demo, or if a simulated/mocked frontend approach is acceptable to ensure budget and size compliance.
