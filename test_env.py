from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(token=os.getenv("HF_API_KEY"))
model = os.getenv("HF_MODEL_ID")

print("Calling HF model:", model)

resp = client.chat_completion(
    model=model,
    messages=[{"role": "user", "content": "hello"}],
    max_tokens=20
)

print(resp.choices[0].message["content"])
