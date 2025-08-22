#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "openai",
#     "python-dotenv",
# ]
# ///

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")
model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-5-nano")

print(f"API Key present: {bool(api_key)}")
print(f"API Base: {api_base}")
print(f"Model: {model_name}")

if api_base:
    client = OpenAI(api_key=api_key, base_url=api_base)
else:
    client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Please say 'Hello world!' exactly"}
        ],
        max_completion_tokens=100,
        temperature=1.0,
    )
    content = response.choices[0].message.content
    print(f"Success! Response: '{content}'")
    print(f"Response length: {len(content) if content else 0}")
except Exception as e:
    print(f"Error: {e}")