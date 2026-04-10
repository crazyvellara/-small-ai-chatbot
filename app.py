# tinyllama_chat.py

import os
import gradio as gr
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# ==== CONFIGURATION ====
PDF_FOLDER = "./pdfs"
VECTOR_DB_PATH = "faiss_index"

# ==== LOAD PDFs ====
def load_documents(pdf_folder):
    docs = []
    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(pdf_folder, file))
            docs.extend(loader.load())
    return docs

# ==== CREATE / LOAD VECTOR DB ====
def get_vectorstore():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")  # embeddings
    if os.path.exists(VECTOR_DB_PATH):
        vectorstore = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        docs = load_documents(PDF_FOLDER)
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local(VECTOR_DB_PATH)
    return vectorstore

# ==== CREATE LLM ====
def get_llm():
    return OllamaLLM(model="tinyllama")

# ==== PROMPT TEMPLATE (must have {context} and {question}) ====
prompt_template = """
You are an AI assistant answering questions based only on the provided context.

Context:
{context}

Question:
{question}

Answer in a clear and concise way. If the answer is not in the context, say "I don't know based on the provided documents."
"""

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# ==== QA CHAIN ====
def get_qa_chain():
    vectorstore = get_vectorstore()
    llm = get_llm()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff",
        chain_type_kwargs={"prompt": PROMPT}
    )
    return qa_chain

qa_chain = get_qa_chain()

# ==== CHATBOT FUNCTION ====
def chatbot(message, history):
    response = qa_chain.run(message)
    return response

# ==== GRADIO INTERFACE ====
with gr.Blocks() as demo:
    gr.Markdown("## 🚀 MOSDAC BOT — Powered by TinyLlama")
    chatbot_ui = gr.ChatInterface(fn=chatbot, chatbot=gr.Chatbot(height=400))

print("🚀 Chatbot running at http://localhost:7860")
demo.launch()













