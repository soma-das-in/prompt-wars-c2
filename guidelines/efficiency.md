# Efficiency Strategy

The system is optimized to run within a $5 GCP credit budget.

---

## Lightweight Architecture

The system avoids:

- Databases
- Large frameworks
- Heavy frontend libraries

---

## Minimal Dependencies

Only essential libraries are used.

Example:

- FastAPI
- Uvicorn
- Vertex AI SDK

---

## Serverless Deployment

Cloud Run ensures:

- No idle server costs
- Automatic scaling
- Pay-per-use billing

---

## Token Optimization

Prompts are designed to be:

- Short
- Focused
- Structured

This reduces LLM cost.

---

## Static Content Usage

Information such as:

- Election process
- Voting steps
- FAQs

is stored locally using the structured JSON schema defined in `static_data_format.md` to reduce AI calls.

---

## Efficient API Calls

AI calls occur only when:

- User asks a question
- Explanation is required

Simple logic like eligibility checks run locally.