import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL_ID = os.getenv("HF_MODEL_ID", "meta-llama/Llama-3.2-1B-Instruct")

client = InferenceClient(
    model=HF_MODEL_ID,
    token=HF_API_KEY,
)

def hf_stream_reply(user_input, emotion, intent, history):
    """
    Streaming reply generator — SAFE VERSION
    Prevents NoneType chunks
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are an empathetic emotional-support assistant. "
                "Keep responses short, warm, supportive. Add emojis relevant to the mood."
            )
        },
        {"role": "system", "content": f"Emotion: {emotion}, Intent: {intent}"}
    ]

    for msg in history[-5:]:
        role = "assistant" if msg["sender"] == "bot" else "user"
        messages.append({"role": role, "content": msg["message"]})

    messages.append({"role": "user", "content": user_input})

    try:
        stream = client.chat_completion(
            messages=messages,
            max_tokens=150,
            temperature=0.9,
            stream=True
        )

        for chunk in stream:
            try:
                delta = chunk.choices[0].delta
                if delta and delta.get("content"):   # ONLY when content exists
                    yield delta["content"]
            except:
                continue

    except Exception as e:
        yield f"⚠ Network error: {str(e)}"
