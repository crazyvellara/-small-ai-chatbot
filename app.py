import os
import gradio as gr
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings

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

# ==== VECTOR STORE ====
def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if os.path.exists(VECTOR_DB_PATH):
        vectorstore = FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        docs = load_documents(PDF_FOLDER)
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local(VECTOR_DB_PATH)

    return vectorstore


# ==== LLM ====
def get_llm():
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )


prompt_template = """
You are an AI assistant answering questions based only on the provided context.

Context:
{context}

Question:
{question}

Answer in a clear and concise way. If the answer is not in the context, say "I don't know based on the provided documents."
"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)


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


def chatbot(message, history):
    response = qa_chain.run(message)
    return response


with gr.Blocks() as demo:
    gr.Markdown("## 🚀 MOSDAC BOT — Cloud Version")
    gr.ChatInterface(fn=chatbot, chatbot=gr.Chatbot(height=400))


demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)