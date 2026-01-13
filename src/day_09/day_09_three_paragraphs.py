import os
import sys
import re
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "Write in the style of a 1920s newspaper reporter. "
    "Return exactly 3 paragraphs."
)
USER_PROMPT = "Describe what prompt engineering is and why it matters."

def call_openai_paragraphs(system_prompt, user_prompt):
    try:
        import openai # type: ignore
    except ImportError:
        raise ImportError("openai is not installed. Install with: pip install openai")
    if not OPENAI_API_KEY:
        print("[ERROR] OPENAI_API_KEY not set. Please add it to your .env file.")
        sys.exit(1)
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return resp.choices[0].message.content.strip()

def call_gemini_paragraphs(system_prompt, user_prompt):
    try:
        import google.genai as genai # type: ignore
    except ImportError:
        raise ImportError("google-genai is not installed. Install with: pip install google-genai")
    if not GEMINI_API_KEY:
        print("[ERROR] GEMINI_API_KEY not set. Please add it to your .env file.")
        sys.exit(1)
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

if __name__ == "__main__":
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "gemini").lower()
    if MODEL_PROVIDER == "openai":
        output = call_openai_paragraphs(SYSTEM_PROMPT, USER_PROMPT)
    elif MODEL_PROVIDER == "gemini":
        output = call_gemini_paragraphs(SYSTEM_PROMPT, USER_PROMPT)
    else:
        print(f"[ERROR] Unknown MODEL_PROVIDER: {MODEL_PROVIDER}. Use 'openai' or 'gemini'.")
        sys.exit(1)
    print(output)


    paragraphs = re.split(r"\n\s*\n", output)
    count = sum(1 for p in paragraphs if p.strip())
    print(f"\nParagraphs detected: {count}")
