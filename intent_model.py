import re

def detect_intent(text):
    text = text.lower().strip()

    # Helper function for clean word-boundary checking
    def match(words):
        return any(re.search(rf"\b{word}\b", text) for word in words)

    # ✅ Greeting
    if match(["hi", "hello", "hey", "sup", "yo", "whatsup", "what's up"]):
        return "greeting"

    # ✅ Farewell
    if match(["bye", "goodbye", "see you", "take care", "later"]):
        return "farewell"

    # ✅ Stress / Conflict
    if match(["scolding", "shouting", "fight", "arguing", "pressure", "stressed", "stress", "tension"]):
        return "stress"

    # ✅ Gaming / Hobby
    if match(["valo", "valorant", "pubg", "bgmi", "game", "gaming", "play", "match"]):
        return "gaming"

    # ✅ Advice Request
    if match(["what should i do", "help", "suggest", "advice", "guide", "what can i do"]):
        return "advice"

    # ✅ Sad / Emotional Venting
    if match(["cry", "crying", "upset", "hurt", "lonely", "depressed"]):
        return "venting"

    # ✅ Question (anything ending with '?')
    if text.endswith("?"):
        return "question"

    # ✅ Default
    return "casual"


# ✅ Emotion labels from your ML model
emotion_map = {
    0: "sad",
    1: "happy",
    2: "anger",
    3: "fear",
    4: "love",
    5: "surprise"
}
