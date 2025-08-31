import re

# Define basic intents and their keywords
intent_keywords = {
    "registration": ["register", "sign up", "create account"],
    "data_access": ["download", "access", "get data", "retrieve", "view data"],
    "satellite_info": ["satellite", "INSAT", "SCATSAT", "megha", "payload", "resolution"],
    "general_info": ["what is", "MOSDAC", "help", "faq", "support"]
}

# Function to detect intent
def detect_intent(user_input):
    user_input = user_input.lower()
    
    for intent, keywords in intent_keywords.items():
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword.lower())}\b", user_input):
                return intent
    return "unsupported"

# --- TESTING ---

while True:
    q = input("\nAsk a question (or type 'exit' to quit):\n> ")
    if q.lower() == 'exit':
        break
    intent = detect_intent(q)
    print("🧠 Detected Intent:", intent)
