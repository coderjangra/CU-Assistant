import numpy as np
from query_classifier import classify_query

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def predict_intent(text, embedder,
                   general_tags, general_embeddings,
                   course_tags, course_embeddings):

    query_type = classify_query(text)
    vec = embedder.encode([text])[0]

    # GREETING
    if query_type == "GREETING":
        return "greeting"

    # GENERAL INTENTS ONLY
    if query_type == "GENERAL":
        sims = [cosine_sim(vec, e) for e in general_embeddings]
        best = np.argmax(sims)
        if sims[best] < 0.30:
            return "fallback"
        return general_tags[best]

    # COURSE INTENTS ONLY
    if query_type == "COURSE":
        sims = [cosine_sim(vec, e) for e in course_embeddings]
        best = np.argmax(sims)
        if sims[best] < 0.35:
            return "fallback"
        return course_tags[best]

    return "fallback"
