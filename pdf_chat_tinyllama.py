from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import Ollama
import os

# Load the PDF
pdf_path = "data/docs/product_catalogue.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# Create embeddings and vector store
embeddings = OllamaEmbeddings(model="tinyllama")
db = FAISS.from_documents(documents, embeddings)

# Search for relevant content
while True:
    query = input("\n🔍 Ask a question (or type 'exit'): ")
    if query.lower() == "exit":
        break
    docs = db.similarity_search(query)

    # Use LLM to answer based on relevant docs
    llm = Ollama(model="tinyllama")
    qa_chain = load_qa_chain(llm, chain_type="stuff")
    answer = qa_chain.run(input_documents=docs, question=query)

    print("\n🧠 Answer:", answer)
