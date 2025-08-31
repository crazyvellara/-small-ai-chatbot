import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag

# Sample question
question = input("Enter a question:\n> ")

# Tokenize and remove stopwords
stop_words = set(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')
words = tokenizer.tokenize(question.lower())
filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

# Part-of-speech tagging
tagged_words = pos_tag(filtered_words)

# Show nouns and important terms
entities = [word for word, tag in tagged_words if tag.startswith('NN')]

print("\n🧠 Detected Entities/Keywords:")
for e in entities:
    print("🔹", e)
