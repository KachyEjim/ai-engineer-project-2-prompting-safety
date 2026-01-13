import os
from dotenv import load_dotenv
import openai

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("[ERROR] OPENAI_API_KEY not set. Please add it to your .env file.")
    exit(1)

client = openai.OpenAI(api_key=api_key)
prompt = "Summarize the Wikipedia entry for 'Transformer (machine learning)' in plain English."

print("=== NO MAX TOKENS ===")
resp1 = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
)
print(resp1.choices[0].message.content.strip())

print("\n=== MAX_TOKENS=50 ===")
resp2 = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=50,
)
print(resp2.choices[0].message.content.strip())
