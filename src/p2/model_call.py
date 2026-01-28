from p2.config import OPENAI_API_KEY, GEMINI_API_KEY, P2_MODEL, GEMINI_MODEL
import openai
import requests
import google.genai as genai # type: ignore


def call_openai_model(prompt: dict) -> str:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=P2_MODEL,
        messages=[
            prompt # pyright: ignore[reportArgumentType]
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content # pyright: ignore[reportReturnType]


def call_gemini_model(prompt: dict) -> str:
    client = genai.Client(api_key=GEMINI_API_KEY)
    messages = [
        prompt # pyright: ignore[reportArgumentType]
    ]
    gen_config = {"temperature": 0.2}
    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        input=messages, # pyright: ignore[reportArgumentType]
        generation_config=gen_config # pyright: ignore[reportArgumentType]
    )
    outputs = getattr(interaction, "outputs", [])
    assistant_text = ""
    for output in outputs:
        if hasattr(output, "text"):
            assistant_text = output.text
    return assistant_text.strip()  

def call_model(prompt: dict) -> str:
    if P2_MODEL == "openai":
        return call_openai_model(prompt)
    elif P2_MODEL == "gemini":
        return call_gemini_model(prompt)
    else:
        raise ValueError(f"Unknown P2_MODEL: {P2_MODEL}")
