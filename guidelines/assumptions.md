# Project Assumptions

The following assumptions guide the design of VoteAssist.

---

## User Assumptions

Users may include:

- First-time voters
- Citizens unfamiliar with the election process
- Elderly voters needing simplified guidance

Users may access the application from:

- Mobile browsers
- Desktop browsers

---

## Data Assumptions

The system assumes that:

- Official election procedures remain consistent
- Users may not know election terminology
- Users require simple explanations

The system will provide general guidance and redirect users to official portals 
when necessary.

---

## Data Storage Assumptions

The application uses Google Cloud Firestore to completely replace any existing static JSON files and store static educational content such as FAQs and election guides.

Firestore remains stateless and read-only, and is not used to store personal voter information or user interaction data.

---

## Technical Assumptions

As per privacy needs and resource constraints:

- The system will not store user data
- The system will not maintain session history
- Only lightweight libraries will be used
- Repository must remain under 1 MB

---

## API Usage Assumptions

Vertex AI usage will remain minimal because:

- Gemini Flash models are low cost
- Queries are short and informational

Expected cost: < $5.

---

## Legal and Neutrality Assumptions

The assistant will:

- Provide educational content only
- Avoid political bias
- Not promote political parties or candidates

The goal is civic education only.

---

## Feature Scope for MVP

The MVP will include:

- Election process guide
- Eligibility checker
- Voting process explanation
- Frequently asked questions
- Voice interaction (with usage constraints)

The following are **out of scope for MVP**:

- Polling booth lookup
- Candidate information
- Election notifications