import json
import os

# Load the knowledge graph file
path = os.path.abspath("data/knowledge_graph.json")
with open(path, 'r') as file:
    kg_data = json.load(file)

# Print each entity and its relationships
print("\n🔗 Knowledge Graph Preview:\n")
for entity in kg_data['entities']:
    print(f"🔸 Entity: {entity['name']} ({entity['type']})")
    for relation in entity['relations']:
        print(f"   └── {relation['relation']} → {relation['target']}")
print("\n✅ KG loaded successfully!")
