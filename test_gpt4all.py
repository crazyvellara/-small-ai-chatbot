from gpt4all import GPT4All

# ✅ This is a working model name as of now (July 2025)
model_name = "ggml-gpt4all-j-v1.3-groovy"

# It will download this model the first time and save it locally
model = GPT4All(model_name)

response = model.generate("What is GPT4All?")
print(response)

