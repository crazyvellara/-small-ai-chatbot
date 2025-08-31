# -small-ai-chatbot
A simple AI chatbot built using Python, Gradio, and vector-based retrieval. This chatbot allows users to interact with AI and fetch context-based answers from uploaded documents or stored knowledge.

🔹 Features

Interactive chatbot interface using Gradio

Vector-based document retrieval for context-aware answers (FAISS / VectorStore)

Anonymous and offline-ready: stores knowledge locally

Supports multiple file formats (PDF, DOCX, etc.)

Clean and lightweight design suitable for personal AI assistant projects

🛠️ Technologies Used

Python – core programming language

Gradio – web-based user interface

FAISS – vector search for document-based queries

LangChain – chaining LLM prompts and context handling

Local Storage – stores uploaded data and vector embeddings

Git & GitHub – version control and project hosting

⚡ Setup Instructions

Clone the repository

git clone https://github.com/crazyvellara/-small-ai-chatbot.git
cd -small-ai-chatbot


Create a virtual environment

python -m venv .venv
.\.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Mac/Linux


Install dependencies

pip install -r requirements.txt


Run the chatbot

python tinyllama_chat.py


Open the Gradio interface in your browser:
http://localhost:7860

📝 Usage

Type your query in the input box.

The AI responds based on the knowledge in your uploaded documents.

Add more documents to extend the chatbot’s knowledge.

🔹 Project Structure
-small-ai-chatbot/
│
├─ tinyllama_chat.py      # Main chatbot script
├─ requirements.txt       # Python dependencies
├─ vectorstore/           # Stored vector database (FAISS)
├─ .gitignore
└─ README.md

📌 Future Improvements

Multi-turn memory for more natural conversations

Support for additional file types like XLSX

Integration with a cloud database for persistent storage

UI improvements and mobile-friendly design

Knowledge graph support for advanced queries

⚡ Notes

Ensure Python 3.10+ is installed

Keep the .venv folder hidden and do not push it to GitHub

Avoid running the project inside OneDrive to prevent Git object errors

🟢 Author

Ann Mariya Thomas – AI & Data Science Student
Team: The Chaotic 4 (Adhisree P A, Anirudh, Asna A, Ann Mariya Thomas 
