from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import LlamaCpp
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
import os

# === Load PDF ===
pdf_path = "data/docs/product_catalogue.pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load()

# === Embeddings ===
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(pages, embeddings)

# === Load Local LLM ===
model_path = "models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"
llm = LlamaCpp(
    model_path=model_path,
    temperature=0.7,
    max_tokens=512,
    top_p=1,
    n_ctx=2048,
    verbose=True,
)

# === QA Chain ===
qa_chain = load_qa_chain(llm, chain_type="stuff")

# === Ask user ===
while True:
    question = input("💬 Ask a question (or type 'exit'): ")
    if question.lower() == "exit":
        break

    docs = db.similarity_search(question)
    answer = qa_chain.run(input_documents=docs, question=question)
    print(f"🧠 Answer: {answer}\n")










