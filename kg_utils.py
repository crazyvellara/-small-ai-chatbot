import os
import spacy
from langchain_community.document_loaders import PyPDFLoader
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

def extract_entities_from_text(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents]

def build_knowledge_graph(pdf_folder):
    graph = defaultdict(list)

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(pdf_folder, filename))
            pages = loader.load()
            for page in pages:
                entities = extract_entities_from_text(page.page_content)
                for i in range(len(entities) - 1):
                    source = entities[i]
                    target = entities[i + 1]
                    if target not in graph[source]:
                        graph[source].append(target)

    return graph
