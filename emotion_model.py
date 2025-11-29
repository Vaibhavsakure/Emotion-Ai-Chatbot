import pickle
import re

# Load trained ML model
with open("emotion_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Load TF-IDF vectorizer
with open("vectorizer.pkl", "rb") as vec_file:
    vectorizer = pickle.load(vec_file)

# Emotion label mapping
emotion_map = {
    0: "sad",
    1: "happy",
    2: "anger",
    3: "fear",
    4: "love",
    5: "surprise"
}

# Rule-based emotion keywords
rule_emotions = {
    "anger": ["scolding", "shouting", "yelling", "angry", "fight", "pissed", "mad"],
    "fear": ["scared", "afraid", "worried", "nervous", "terrified"],
    "sad": ["crying", "upset", "depressed", "lonely", "hurt"]
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

def rule_based_emotion(text):
    text = text.lower()
    for emotion, keywords in rule_emotions.items():
        if any(word in text for word in keywords):
            return emotion
    return None

def detect_emotion(text):
    # Step 1: Rule-based check
    rule_result = rule_based_emotion(text)
    if rule_result:
        return rule_result

    # Step 2: ML model prediction
    clean = clean_text(text)
    vec = vectorizer.transform([clean])
    pred = model.predict(vec)[0]
    return emotion_map[pred]
