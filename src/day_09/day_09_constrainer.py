import os
import sys
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PROMPT = "Summarize the Wikipedia entry for 'Transformer (machine learning)' in plain English."

def call_openai_summary(prompt, max_tokens=None):
    try:
        import openai # type: ignore
    except ImportError:
        raise ImportError("openai is not installed. Install with: pip install openai")
    if not OPENAI_API_KEY:
        print("[ERROR] OPENAI_API_KEY not set. Please add it to your .env file.")
        sys.exit(1)
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    kwargs = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
    }
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens
    resp = client.chat.completions.create(**kwargs)
    return resp.choices[0].message.content.strip()

def call_gemini_summary(prompt, max_tokens=None):
    try:
        import google.genai as genai # type: ignore
    except ImportError:
        raise ImportError("google-genai is not installed. Install with: pip install google-genai")
    if not GEMINI_API_KEY:
        print("[ERROR] GEMINI_API_KEY not set. Please add it to your .env file.")
        sys.exit(1)
    client = genai.Client(api_key=GEMINI_API_KEY)
    messages = [
        {"role": "user", "content": prompt},
    ]
    gen_config = {"temperature": 0.2}
    if max_tokens is not None:
        gen_config["max_output_tokens"] = max_tokens
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
        print("=== OPENAI: NO MAX TOKENS ===")
        summary1 = call_openai_summary(PROMPT)
        print(summary1)

        print("\n=== OPENAI: MAX_TOKENS=50 ===")
        summary2 = call_openai_summary(PROMPT, max_tokens=50)
        print(summary2)
    elif MODEL_PROVIDER == "gemini":
        print("=== GEMINI: NO MAX TOKENS ===")
        summary1 = call_gemini_summary(PROMPT)
        print(summary1)

        print("\n=== GEMINI: MAX_TOKENS=50 ===")
        summary2 = call_gemini_summary(PROMPT, max_tokens=50)
        print(summary2)
    else:
        print(f"[ERROR] Unknown MODEL_PROVIDER: {MODEL_PROVIDER}. Use 'openai' or 'gemini'.")
        sys.exit(1)
