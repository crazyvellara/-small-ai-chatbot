import os
import json

print("Current working directory:", os.getcwd())  # debug line

# Try opening the file using absolute path
path = os.path.abspath("data/extracted_qna.json")
print("Looking for file at:", path)

with open(path, 'r') as file:
    qa_data = json.load(file)

print("\nAvailable Questions:")
for item in qa_data:
    print("Q:", item['question'])

# Take user input
import difflib

# Take user input
print("\nYou can ask me anything about MOSDAC. Type 'exit' to quit.\n")

while True:
    user_question = input("> ").lower()
    if user_question == 'exit':
        print("Goodbye! 👋")
        break

    # Find closest match
    questions = [item['question'].lower() for item in qa_data]
    best_match = difflib.get_close_matches(user_question, questions, n=1, cutoff=0.4)

    if best_match:
        for item in qa_data:
            if item['question'].lower() == best_match[0]:
                print("\nAnswer:", item['answer'], "\n")
    else:
        print("\nSorry, I couldn't find an answer to that.\n")


# Extract all stored questions
questions = [item['question'].lower() for item in qa_data]

# Use difflib to find best match
best_match = difflib.get_close_matches(user_question, questions, n=1, cutoff=0.4)

if best_match:
    for item in qa_data:
        if item['question'].lower() == best_match[0]:
            print("\nAnswer:", item['answer'])
else:
    print("\nSorry, I couldn't find an answer to that.")
