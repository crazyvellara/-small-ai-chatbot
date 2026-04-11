import os
import gradio as gr
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

PDF_FOLDER = "./mosdac_pdfs"
VECTOR_DB_PATH = "faiss_index"

# Load PDFs
def load_documents(pdf_folder):
    docs = []
    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(pdf_folder, file))
            docs.extend(loader.load())
    return docs

# Vector DB
def get_vectorstore():
    embeddings = OpenAIEmbeddings()

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


def get_llm():
    return ChatOpenAI(model="gpt-3.5-turbo")


prompt_template = """
You are an AI assistant answering questions based only on the provided context.

Context:
{context}

Question:
{question}

Answer clearly. If not found in context say "I don't know based on the documents."
"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context","question"]
)


def get_qa_chain():
    vectorstore = get_vectorstore()
    llm = get_llm()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff",
        chain_type_kwargs={"prompt":PROMPT}
    )

    return qa_chain


qa_chain = get_qa_chain()


def chatbot(message,history):
    return qa_chain.run(message)


with gr.Blocks() as demo:
    gr.Markdown("## 🚀 MOSDAC BOT")
    gr.ChatInterface(fn=chatbot)


demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT",10000))
)