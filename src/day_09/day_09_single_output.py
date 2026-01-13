import os
from dotenv import load_dotenv
import openai

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("[ERROR] OPENAI_API_KEY not set. Please add it to your .env file.")
    exit(1)

client = openai.OpenAI(api_key=api_key)
system_prompt = (
    "You must answer with only the city name. No punctuation, no explanation, no leading or trailing whitespace."
)
user_prompt = "What is the capital of Canada?"

resp = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    max_tokens=10,
)
output = resp.choices[0].message.content.strip()
print(output)
if output != "Ottawa":
    raise ValueError("Output constraint failed: expected Ottawa")
