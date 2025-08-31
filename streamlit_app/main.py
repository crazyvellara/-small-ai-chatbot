import streamlit as st
import json
import os
import difflib
import re

# Load Q&A data
def load_qna():
    path = os.path.abspath("data/extracted_qna.json")
    with open(path, 'r') as file:
        return json.load(file)

# Intent detection setup
intent_keywords = {
    "registration": ["register", "sign up", "create account"],
    "data_access": ["download", "access", "get data", "retrieve", "view data"],
    "satellite_info": ["satellite", "INSAT", "SCATSAT", "megha", "payload", "resolution"],
    "general_info": ["what is", "MOSDAC", "help", "faq", "support"],
    "geospatial": ["india", "kerala", "tamil nadu", "delhi", "goa", "region", "location", "area", "coverage", "ocean", "bay of bengal", "map"]
}

def detect_intent(user_input):
    user_input = user_input.lower()
    for intent, keywords in intent_keywords.items():
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", user_input):
                return intent
    return "unsupported"

# Match best answer
def find_answer(user_question, qna_list):
    questions = [item['question'] for item in qna_list]
    matches = difflib.get_close_matches(user_question, questions, n=1, cutoff=0.4)
    
    if matches:
        for item in qna_list:
            if item['question'] == matches[0]:
                return item['answer']
    return "Sorry, I couldn't find an answer for that."

# Streamlit UI setup
st.set_page_config(page_title="MOSDAC Help Bot", layout="centered")
st.title("🛰️ ISRO - MOSDAC Help Bot")
st.write("Ask me anything about the MOSDAC portal, data, satellites, or registration!")

# Load Q&A
qna_data = load_qna()

# Initialize session history
if "history" not in st.session_state:
    st.session_state.history = []

# Input box
user_question = st.text_input("Type your question here:")

if user_question:
    # Detect intent
    intent = detect_intent(user_question)

    # Geospatial-specific reply
    if intent == "geospatial":
        answer = (
            "MOSDAC provides region-specific satellite data like Ocean Temperature, Wind Vector, and Rainfall "
            "for areas across India. Visit the Ocean or Weather data sections to explore data by location."
        )
    else:
        answer = find_answer(user_question, qna_data)
    
    # Store in chat history
    st.session_state.history.append({
        "question": user_question,
        "answer": answer,
        "intent": intent
    })

# Show chat history
if st.session_state.history:
    st.subheader("🧾 Chat History")
    for entry in reversed(st.session_state.history):
        st.markdown(f"**You:** {entry['question']}")
        st.markdown(f"**Bot:** {entry['answer']}")
        st.caption(f"🧠 Detected Intent: `{entry['intent']}`")
        st.markdown("---")



