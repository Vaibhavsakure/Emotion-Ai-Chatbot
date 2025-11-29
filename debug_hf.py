# debug_hf.py - Complete Debugging Script for HuggingFace API Issues

import os
import sys
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

print("=" * 60)
print("HUGGINGFACE API DEBUGGING SCRIPT")
print("=" * 60)

# Load environment variables
load_dotenv()

# Step 1: Check API Key
print("\n1. Checking API Key...")
HF_TOKEN = os.getenv("HF_API_KEY")
if not HF_TOKEN:
    print("❌ ERROR: HF_API_KEY not found in environment variables!")
    print("   Fix: Add HF_API_KEY=your_token_here to your .env file")
    sys.exit(1)
else:
    print(f"✅ API Key found: {HF_TOKEN[:10]}...{HF_TOKEN[-10:]}")

# Step 2: Check Model ID
print("\n2. Checking Model ID...")
MODEL_ID = os.getenv("HF_MODEL_ID", "microsoft/Phi-3.5-mini-instruct")
print(f"✅ Model ID: {MODEL_ID}")

# Step 3: Initialize Client
print("\n3. Initializing HuggingFace Client...")
try:
    client = InferenceClient(token=HF_TOKEN)
    print("✅ Client initialized successfully")
except Exception as e:
    print(f"❌ ERROR initializing client: {e}")
    sys.exit(1)

# Step 4: Test Simple Message
print("\n4. Testing Simple Message (Non-Streaming)...")
try:
    test_messages = [
        {"role": "user", "content": "Say hi"}
    ]
    
    response = client.chat_completion(
        model=MODEL_ID,
        messages=test_messages,
        max_tokens=20,
        stream=False,
    )
    
    if response and response.choices:
        reply = response.choices[0].message.content
        print(f"✅ Simple test successful!")
        print(f"   Response: {reply}")
    else:
        print("❌ Empty response from API")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\nCommon Issues:")
    print("1. Invalid API Token - Check your token at https://huggingface.co/settings/tokens")
    print("2. Model not accessible - Try a different model")
    print("3. Rate limiting - Wait a few minutes")
    print("4. Network issues - Check your internet connection")

# Step 5: Test with System Prompt
print("\n5. Testing with System Prompt...")
try:
    test_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's 2+2?"}
    ]
    
    response = client.chat_completion(
        model=MODEL_ID,
        messages=test_messages,
        max_tokens=50,
        temperature=0.7,
        stream=False,
    )
    
    if response and response.choices:
        reply = response.choices[0].message.content
        print(f"✅ System prompt test successful!")
        print(f"   Response: {reply}")
    else:
        print("❌ Empty response from API")
        
except Exception as e:
    print(f"❌ ERROR: {e}")

# Step 6: Test Streaming
print("\n6. Testing Streaming...")
try:
    test_messages = [
        {"role": "user", "content": "Count to 5"}
    ]
    
    stream = client.chat_completion(
        model=MODEL_ID,
        messages=test_messages,
        max_tokens=50,
        stream=True,
    )
    
    print("✅ Streaming chunks: ", end="")
    chunk_count = 0
    for chunk in stream:
        if chunk and chunk.choices and len(chunk.choices) > 0:
            delta = chunk.choices[0].delta
            if delta and hasattr(delta, 'content') and delta.content:
                print(delta.content, end="", flush=True)
                chunk_count += 1
    
    print(f"\n   Total chunks received: {chunk_count}")
    
    if chunk_count == 0:
        print("❌ No chunks received during streaming")
    else:
        print("✅ Streaming test successful!")
        
except Exception as e:
    print(f"\n❌ Streaming ERROR: {e}")

# Step 7: Alternative Models Test
print("\n7. Testing Alternative Models...")
alternative_models = [
    "meta-llama/Llama-3.2-3B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "HuggingFaceH4/zephyr-7b-beta"
]

print("If your current model isn't working, try these alternatives:")
for model in alternative_models:
    print(f"   - {model}")

# Step 8: Check Rate Limits
print("\n8. Checking for Rate Limiting...")
print("   If you're seeing errors, you might be rate limited.")
print("   Solutions:")
print("   - Wait a few minutes between requests")
print("   - Upgrade to HuggingFace Pro for higher limits")
print("   - Use a different model endpoint")

# Step 9: Final Recommendations
print("\n" + "=" * 60)
print("SUMMARY & RECOMMENDATIONS")
print("=" * 60)
print("""
If tests failed, try these fixes:

1. INVALID TOKEN:
   - Go to: https://huggingface.co/settings/tokens
   - Create a new token with 'inference' permission
   - Update your .env file: HF_API_KEY=hf_xxxxx

2. MODEL NOT ACCESSIBLE:
   - Some models require acceptance of terms
   - Try a different model (see alternatives above)
   - Check model card: https://huggingface.co/{MODEL_ID}

3. RATE LIMITING:
   - Free tier: 1000 requests/day
   - Wait 1-2 minutes between requests
   - Consider HuggingFace Pro

4. NETWORK ISSUES:
   - Check your internet connection
   - Try from a different network
   - Check if huggingface.co is accessible

5. MODEL SPECIFIC ISSUES:
   - Some models don't support streaming
   - Some require specific prompt formats
   - Check model documentation
""")

print("\n✅ Debug script completed!")
print("Run this script to diagnose issues: python debug_hf.py")