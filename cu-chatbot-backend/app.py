from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# ---------------- APP SETUP ---------------- #

app = Flask(__name__)
CORS(app)

# ---------------- LOAD DATA ---------------- #

with open("intents.json", "r", encoding="utf-8") as f:
    intents_data = json.load(f)["intents"]

embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- PREPARE EMBEDDINGS ---------------- #

tags = []
embeddings = []
responses_map = {}

print("Loading and encoding intents. This might take a few seconds...")
for intent in intents_data:
    tag = intent["tag"]
    responses_map[tag] = intent["responses"]

    patterns = intent.get("patterns", [])
    if not patterns:
        continue

    # Create an averaged embedding for all patterns in an intent
    emb = embedder.encode(patterns).mean(axis=0)
    tags.append(tag)
    embeddings.append(emb)

embeddings = np.array(embeddings)
print(f"Successfully loaded and encoded {len(tags)} intents.")

# ---------------- SIMILARITY ---------------- #

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ---------------- INTENT PREDICTOR ---------------- #

def predict_intent(text: str):
    text_l = text.lower().strip()
    
    if not text_l:
        return "fallback"

    vec = embedder.encode([text_l])[0]

    # Calculate similarity against ALL intents globally
    sims = [cosine_sim(vec, e) for e in embeddings]
    best_idx = int(np.argmax(sims))
    best_score = sims[best_idx]
    
    # Debug info
    print(f"Query: '{text}' | Best Match: '{tags[best_idx]}' | Score: {best_score:.3f}")

    if best_score < 0.35:
        return "fallback"
        
    return tags[best_idx]

# ---------------- RESPONSE ---------------- #

def get_response(intent_tag):
    responses = responses_map.get(intent_tag)
    if not responses:
        return "Sorry, I couldn't understand that. Please ask something related to Chandigarh University."
    return np.random.choice(responses)

# ---------------- API ---------------- #

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"reply": "Please enter a message."})

    intent = predict_intent(message)
    reply = get_response(intent)

    return jsonify({
        "intent": intent,
        "reply": reply
    })

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)
