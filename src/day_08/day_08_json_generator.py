import os
import sys
import json
from dotenv import load_dotenv
import openai
from src.p2.json_utils import BOOK_RECOMMENDATION_SCHEMA_KEYS, validate_exact_keys

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("[ERROR] OPENAI_API_KEY not set. Please add it to your .env file.")
    sys.exit(1)

client = openai.OpenAI(api_key=api_key)

SYSTEM_PROMPT = (
    "You are a helpful assistant. You must reply ONLY with a valid JSON object containing exactly these keys: "
    f"{', '.join(BOOK_RECOMMENDATION_SCHEMA_KEYS)}. "
    "Do not include any extra keys. Do not include markdown or commentary. Return only the JSON object."
)

USER_PROMPT = "Recommend a book about AI engineering."

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ],
    temperature=0.2,
    response_format={"type": "json_object"},
)

raw = response.choices[0].message.content
try:
    if raw is None:
        raise ValueError("Response content is None.")
    obj = json.loads(raw)
    validate_exact_keys(obj, required_keys=BOOK_RECOMMENDATION_SCHEMA_KEYS)
    print(json.dumps(obj, indent=2, sort_keys=True))
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)
