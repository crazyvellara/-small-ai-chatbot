import os
import spacy
from langchain_community.document_loaders import PyPDFLoader
from collections import defaultdict

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Folder with your MOSDAC PDFs
pdf_folder = "data/docs"

def extract_entities_from_text(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def build_knowledge_graph(pdf_folder):
    graph = defaultdict(list)

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            print(f"Processing: {filename}")
            loader = PyPDFLoader(os.path.join(pdf_folder, filename))
            pages = loader.load()
            for page in pages:
                entities = extract_entities_from_text(page.page_content)
                for i in range(len(entities)-1):
                    source, source_type = entities[i]
                    target, target_type = entities[i+1]
                    if target not in graph[source]:
                        graph[source].append(target)
    
    return graph

if __name__ == "__main__":
    kg = build_knowledge_graph(pdf_folder)
    print("\n📚 Sample Knowledge Graph:")
    for source, targets in list(kg.items())[:10]:
        print(f"{source} --> {targets}")
