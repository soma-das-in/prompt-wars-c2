# Testing Strategy

Testing ensures the assistant behaves correctly.

---

## Functional Testing

Verify key features.

| Feature | Test |
|------|------|
Eligibility Checker | Age ≥18 returns eligible |
Chat Assistant | Returns explanation |
Homepage | Loads successfully |

---

## Input Validation Tests

Examples:

| Input | Expected Result |
|------|------|
Age = 17 | Not eligible |
Age = 18 | Eligible |
Invalid text age | Error |

---

## Automated Unit Testing

Automated logic tests will be implemented using `pytest` to ensure backend stability and verify logic without manual intervention.

**Key Automated Logic Tests:**
- **Eligibility Logic (`/eligibility`):** Test boundary conditions (e.g., age 17 returns ineligible, age 18 returns eligible).
- **Firestore Integration:** Verify that static content retrieval from Firestore executes correctly and parses the expected schema.
- **Voice Constraints:** Verify that Voice STT/TTS endpoints strictly reject audio exceeding 10 seconds and gracefully handle empty audio.
- **API Routing & Validation:** Ensure endpoints reject malformed requests (e.g., empty chat queries, excessively long queries) with appropriate HTTP 422 errors.
- **Error Handling:** Verify that Vertex AI or Firestore API failures return generic, safe user-friendly errors without leaking stack traces.

---

## API Testing

Test endpoints:

- `/`
- `/chat`
- `/eligibility`

---

## Manual Testing

Perform manual checks for:

- UI usability
- Response clarity
- Mobile responsiveness

---

## Edge Cases

Examples:

- Empty query
- Very long question
- Non-English queries

---

## Performance Testing

Ensure response time remains acceptable (<2 seconds for most queries).