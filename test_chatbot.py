from emotion_model import detect_emotion
from reply_logic import generate_reply

while True:
    text = input("You: ")
    emotion = detect_emotion(text)
    reply = generate_reply(emotion)
    print(f"Emotion: {emotion}")
    print(f"Bot: {reply}\n")
