COURSE_KEYWORDS = [
    "bba", "mba", "cse", "computer", "engineering",
    "data science", "ai", "mechanical", "civil",
    "electrical", "law", "pharmacy"
]

GENERAL_KEYWORDS = [
    "admission", "fees", "fee", "campus", "life",
    "hostel", "placement", "library", "sports",
    "food", "mess", "exam", "attendance"
]

def classify_query(text: str):
    text = text.lower()
    words = text.split()

    # Greetings
    if text in ["hi", "hello", "hey", "good morning", "good evening"]:
        return "GREETING"

    # Explicit course mention
    if any(c in text for c in COURSE_KEYWORDS):
        return "COURSE"

    # General CU queries
    if any(g in text for g in GENERAL_KEYWORDS):
        return "GENERAL"

    # Short vague queries → GENERAL
    if len(words) <= 3:
        return "GENERAL"

    return "GENERAL"
