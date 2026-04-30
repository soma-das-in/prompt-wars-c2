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