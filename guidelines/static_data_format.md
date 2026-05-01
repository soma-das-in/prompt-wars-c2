# Static Data Format Guide

To minimize unnecessary calls to the Vertex AI model and maintain low API usage costs, VoteAssist relies on local static data to provide standard information such as election process steps and frequently asked questions (FAQs).

This document defines the schema for the JSON file used to store this static content.

## Schema Definition

The static content should be stored in a `static_content.json` file on the server.

### Example JSON Structure

```json
{
  "election_process": [
    {
      "step": 1,
      "title": "Voter Registration",
      "description": "Eligible citizens register their names in the electoral roll."
    },
    {
      "step": 2,
      "title": "Election Announcement",
      "description": "The Election Commission announces the dates and schedules."
    }
  ],
  "faqs": [
    {
      "question": "What if I lose my voter ID?",
      "answer": "You can apply for a duplicate EPIC (Elector Photo Identity Card) online via the NVSP portal or at your local electoral office."
    },
    {
      "question": "Am I eligible to vote?",
      "answer": "You are eligible if you are an Indian citizen and 18 years of age or older as of the qualifying date."
    }
  ]
}
```

## Data Utilization

- The backend (FastAPI) will load this JSON data into memory on startup.
- The frontend can fetch the FAQs and election process via a REST endpoint (e.g., `/api/static-content`).
- This allows the application to instantly serve informational queries without invoking the Vertex AI Gemini model, significantly improving response times and reducing operational costs.
