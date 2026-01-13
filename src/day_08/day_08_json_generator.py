import os
import sys
import json
from dotenv import load_dotenv # type: ignore
from src.p2.json_utils import BOOK_RECOMMENDATION_SCHEMA_KEYS, validate_exact_keys
from src.p2.config import P2_MODEL, OPENAI_API_KEY, GEMINI_API_KEY, GEMINI_MODEL

load_dotenv()

def call_openai_json(system_prompt, user_prompt):
    import openai # type: ignore
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

def call_gemini_json(system_prompt, user_prompt):
    # Gemini does not have a strict JSON mode, but we can prompt for it
    try:
        import google.genai as genai    # type: ignore
    except ImportError:
        raise ImportError("google-genai is not installed. Install with: pip install google-genai")
    client = genai.Client(api_key=GEMINI_API_KEY)
    messages = [
        {"role": "user", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    gen_config = {"temperature": 0.2}
    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        input=messages,
        generation_config=gen_config
    )
    outputs = getattr(interaction, "outputs", [])
    assistant_text = ""
    for output in outputs:
        if hasattr(output, "text"):
            assistant_text = output.text
    assistant_text = assistant_text.strip()
    if assistant_text.startswith('```'):
        assistant_text = assistant_text.lstrip('`')
        if assistant_text.startswith('json'):
            assistant_text = assistant_text[4:]
        assistant_text = assistant_text.strip('`\n ')
    return assistant_text

SYSTEM_PROMPT = (
    "You are a helpful assistant. You must reply ONLY with a valid JSON object containing exactly these keys: "
    f"{', '.join(BOOK_RECOMMENDATION_SCHEMA_KEYS)}. "
    "Do not include any extra keys. Do not include markdown or commentary. Return only the valid JSON object that can be parsed with json.loads., do not include triple backticks and the language tag (like json)"
)

USER_PROMPT = "Recommend a book about AI engineering."

if P2_MODEL == "openai":
    if not OPENAI_API_KEY:
        print("[ERROR] OPENAI_API_KEY not set. Please add it to your .env file.")
        sys.exit(1)
    response = call_openai_json(SYSTEM_PROMPT, USER_PROMPT)
    raw = response.choices[0].message.content
elif P2_MODEL == "gemini":
    if not GEMINI_API_KEY:
        print("[ERROR] GEMINI_API_KEY not set. Please add it to your .env file.")
        sys.exit(1)
    raw = call_gemini_json(SYSTEM_PROMPT, USER_PROMPT)
else:
    print(f"[ERROR] Unknown model: {P2_MODEL}")
    sys.exit(1)

try:
    if raw is None:
        raise ValueError("Response content is None.")
    obj = json.loads(raw)
    validate_exact_keys(obj, required_keys=BOOK_RECOMMENDATION_SCHEMA_KEYS)
    print(json.dumps(obj, indent=2, sort_keys=True))
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)


