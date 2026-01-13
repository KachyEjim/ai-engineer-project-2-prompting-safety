import os
from dotenv import load_dotenv
import openai
import re

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("[ERROR] OPENAI_API_KEY not set. Please add it to your .env file.")
    exit(1)

client = openai.OpenAI(api_key=api_key)
system_prompt = (
    "Write in the style of a 1920s newspaper reporter. "
    "Return exactly 3 paragraphs."
)
user_prompt = "Describe what prompt engineering is and why it matters."

resp = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
)
output = resp.choices[0].message.content.strip()
print(output)

# Count paragraphs (blocks separated by one or more blank lines)
paragraphs = re.split(r"\n\s*\n", output)
count = sum(1 for p in paragraphs if p.strip())
print(f"\nParagraphs detected: {count}")
