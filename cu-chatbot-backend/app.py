from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import numpy as np
import os

# Set HuggingFace cache to a local directory so it persists in Render's build artifact
os.environ["HF_HOME"] = os.path.join(os.getcwd(), ".hf_cache")

# ---------------- APP SETUP ---------------- #

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "success", "message": "CU-Chatbot Backend is running!"}), 200

# ---------------- LOAD DATA ---------------- #

with open("intents.json", "r", encoding="utf-8") as f:
    intents_data = json.load(f)["intents"]

embedder = None
def get_embedder():
    global embedder
    if embedder is None:
        print("Loading SentenceTransformer model...")
        from sentence_transformers import SentenceTransformer
        embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return embedder

# ---------------- PREPARE EMBEDDINGS ---------------- #

tags = []
embeddings = None
responses_map = {}

for intent in intents_data:
    tag = intent["tag"]
    responses_map[tag] = intent["responses"]

EMBEDDINGS_FILE = "embeddings.npy"
TAGS_FILE = "tags.json"

if os.path.exists(EMBEDDINGS_FILE) and os.path.exists(TAGS_FILE):
    print("Loading pre-computed embeddings from disk...")
    embeddings = np.load(EMBEDDINGS_FILE)
    with open(TAGS_FILE, "r") as f:
        tags = json.load(f)
else:
    print("Computing and caching embeddings. This might take a few seconds...")
    embeddings_list = []
    for intent in intents_data:
        tag = intent["tag"]
        patterns = intent.get("patterns", [])
        if not patterns:
            continue

        # Create an averaged embedding for all patterns in an intent
        emb = get_embedder().encode(patterns).mean(axis=0)
        tags.append(tag)
        embeddings_list.append(emb)

    embeddings = np.array(embeddings_list)
    np.save(EMBEDDINGS_FILE, embeddings)
    with open(TAGS_FILE, "w") as f:
        json.dump(tags, f)
    print(f"Successfully loaded and encoded {len(tags)} intents.")

# ---------------- SIMILARITY ---------------- #

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ---------------- INTENT PREDICTOR ---------------- #

def predict_intent(text: str):
    text_l = text.lower().strip()
    
    if not text_l:
        return "fallback"

    vec = get_embedder().encode([text_l])[0]

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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
