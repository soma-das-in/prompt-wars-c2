#!/bin/bash

PROJECT_ID="prompt-wars-hackathon-493408"
DATABASE="(default)"
COLLECTION="faqs"

# Get access token from gcloud
ACCESS_TOKEN=$(CLOUDSDK_PYTHON=/opt/homebrew/bin/python3.13 /opt/homebrew/share/google-cloud-sdk/bin/gcloud auth print-access-token)

if [ -z "$ACCESS_TOKEN" ]; then
    echo "Error: Could not get access token."
    exit 1
fi

seed_doc() {
    local question="$1"
    local answer="$2"
    
    echo "Seeding: $question"
    
    curl -s -X POST \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        --data "{
            \"fields\": {
                \"question\": {\"stringValue\": \"$question\"},
                \"answer\": {\"stringValue\": \"$answer\"}
            }
        }" \
        "https://firestore.googleapis.com/v1/projects/$PROJECT_ID/databases/$DATABASE/documents/$COLLECTION"
}

seed_doc "How to register to vote?" "You can register online through the NVSP portal (nvsp.in) or by submitting Form 6 to your Electoral Registration Officer."
seed_doc "Am I eligible to vote?" "Any Indian citizen aged 18 or above on the qualifying date (usually Jan 1st of the year) is eligible to vote."
seed_doc "What is the voting process?" "Visit your assigned polling station, verify your ID, get your finger inked, and cast your vote on the EVM/VVPAT machine."
seed_doc "Do I need a Voter ID?" "While a Voter ID (EPIC) is preferred, you can use other valid IDs like Aadhaar, PAN card, or Driving License if your name is in the voter list."
seed_doc "How to find my polling booth?" "You can find your polling booth on the NVSP portal or the Voter Helpline App by entering your EPIC number or personal details."

echo -e "\nSeeding complete!"
