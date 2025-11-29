import random

def generate_reply(user_input, emotion, intent):
    user_input = user_input.lower()

    # Intent-based replies
    intent_replies = {
        "greeting": ["Hey! 😊", "Hi there!", "Hello! How are you feeling today?"],
        "farewell": ["Goodbye! Take care ❤️", "See you soon!", "Bye! Stay positive 😊"],
        "stress": [
            "That sounds stressful. Want to tell me more?",
            "Conflicts can be tough. I'm here for you.",
            "I'm sorry you're going through that. What happened?"
        ],
        "gaming": [
            "Gaming can be fun! Is Valorant your favorite?",
            "Nice! What game mode do you play?",
            "Sounds exciting! Do you play daily?"
        ],
        "advice": [
            "I understand. What outcome are you hoping for?",
            "Let’s think this through—what options do you have?",
            "I'm here to help. Tell me a bit more."
        ],
        "question": [
            "That's an interesting question.",
            "What do *you* think about it?",
            "Hmm, tell me more so I can help better."
        ],
        "casual": [
            "I get you. Go on!",
            "Interesting! Tell me more.",
            "I'm listening 😊"
        ]
    }

    # Emotion-based replies
    emotion_replies = {
        "sadness": [
            "I'm here for you.",
            "That sounds tough. Want to talk about it?",
            "It's okay to feel sad sometimes."
        ],
        "anger": [
            "I get that you're frustrated. What triggered it?",
            "It's okay to feel angry.",
            "I'm listening—let it out."
        ],
        "fear": [
            "Feeling scared is normal. What's worrying you?",
            "You're safe talking to me.",
            "I’m here with you."
        ],
        "joy": [
            "That's awesome! Tell me more! 😄",
            "I love hearing that!",
            "Wow! That made my day too! 😊"
        ]
    }

    # Priority: Intent first
    if intent in intent_replies:
        return random.choice(intent_replies[intent])

    # Then emotion fallback
    if emotion in emotion_replies:
        return random.choice(emotion_replies[emotion])

    # Default
    return "I'm here to listen. Tell me more."
