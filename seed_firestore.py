from google.cloud import firestore

def seed_data():
    db = firestore.Client(project="prompt-wars-hackathon-493408")
    
    faqs = [
        {"question": "How to register to vote?", "answer": "You can register online through the NVSP portal or by submitting Form 6 to your Electoral Registration Officer."},
        {"question": "Am I eligible to vote?", "answer": "Any Indian citizen aged 18 or above on the qualifying date is eligible to vote."},
        {"question": "What is the voting process?", "answer": "Visit your polling station, verify your ID, get your finger inked, and cast your vote on the EVM."},
        {"question": "Do I need a Voter ID?", "answer": "While a Voter ID is preferred, you can also use other valid ID proofs like Aadhaar, PAN card, or Driving License if your name is in the rolls."},
    ]

    print("Seeding FAQs...")
    for faq in faqs:
        # Using the question as a slug-like ID or just auto-ID
        db.collection("faqs").add(faq)
    
    print("Seeding successful!")

if __name__ == "__main__":
    seed_data()
