import json
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("intents.json") as f:
    intents = json.load(f)["intents"]

sentences = []
tags = []
import json
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("intents.json") as f:
    intents = json.load(f)["intents"]

sentences = []
tags = []

for intent in intents:
    for pattern in intent["patterns"]:
        sentences.append(pattern)
        tags.append(intent["tag"])

embeddings = model.encode(sentences, show_progress_bar=True)

pickle.dump((embeddings, tags), open("intent_embeddings.pkl", "wb"))

print("✅ Transformer embeddings created")
print("Total sentences:", len(sentences))

for intent in intents:
    for pattern in intent["patterns"]:
        sentences.append(pattern)
        tags.append(intent["tag"])

embeddings = model.encode(sentences, show_progress_bar=True)

pickle.dump((embeddings, tags), open("intent_embeddings.pkl", "wb"))

print("✅ Transformer embeddings created")
print("Total sentences:", len(sentences))
