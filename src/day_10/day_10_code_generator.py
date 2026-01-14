import os
import sys
import json
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from importlib import util as importlib_util
from importlib import import_module
from src.p2.json_utils import CODEGEN_SCHEMA_KEYS, validate_codegen_payload

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "gemini").lower()

SYSTEM_PROMPT = (
    "You are a helpful assistant. You must reply ONLY with a valid JSON object containing exactly these keys: "
    f"{', '.join(CODEGEN_SCHEMA_KEYS)}. "
    "Do not include any extra keys. Do not include markdown or commentary. "
    "Return only the valid JSON object that can be parsed with json.loads. "
    "Schema: {function_name: string, dependencies: [string], description: string, code: string}. "
    "Python 3.11+, include a docstring, no external dependencies unless listed in dependencies, do not use eval or exec."
)
USER_PROMPT = "Write a Python function to check if a string is a palindrome."


def call_openai_json(system_prompt, user_prompt):
    import openai # type: ignore
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content

def call_gemini_json(system_prompt, user_prompt):
    import google.genai as genai # type: ignore
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")
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

def main():
    if MODEL_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            print("[ERROR] OPENAI_API_KEY not set. Please add it to your .env file.")
            sys.exit(1)
        raw = call_openai_json(SYSTEM_PROMPT, USER_PROMPT)
    elif MODEL_PROVIDER == "gemini":
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            print("[ERROR] GEMINI_API_KEY not set. Please add it to your .env file.")
            sys.exit(1)
        raw = call_gemini_json(SYSTEM_PROMPT, USER_PROMPT)
    else:
        print(f"[ERROR] Unknown MODEL_PROVIDER: {MODEL_PROVIDER}")
        sys.exit(1)

    try:
        obj = json.loads(raw)
        validate_codegen_payload(obj)
    except Exception as e:
        print(f"[ERROR] {e}\nRaw response: {raw}")
        sys.exit(1)

    os.makedirs("generated/day_10", exist_ok=True)
    code_path = "generated/day_10/palindrome.py"
    with open(code_path, "w") as f:
        f.write(obj["code"])

    # Import and test the generated function
    spec = importlib_util.spec_from_file_location("palindrome", code_path)
    if spec is None:
        print(f"[ERROR] Could not load module spec from {code_path}")
        sys.exit(1)
    palindrome_mod = importlib_util.module_from_spec(spec)
    if spec.loader is None:
        print(f"[ERROR] Could not load module loader from {code_path}")
        sys.exit(1)
    spec.loader.exec_module(palindrome_mod)
    func_name = obj["function_name"]
    func = getattr(palindrome_mod, func_name)
    assert func("racecar") is True, "racecar should be palindrome"
    assert func("hello") is False, "hello should not be palindrome"
    print("PASS: palindrome tests")

if __name__ == "__main__":
    main()
