
from typing import List
import os

MODERATION_MODEL = "omni-moderation-latest"
MODERATION_PROVIDER = os.getenv("MODERATION_PROVIDER", "gemini").lower()  # 'openai' or 'gemini'

class ModerationResult:
    flagged: bool
    categories: List[str]

    def __init__(self, flagged: bool, categories: List[str]):
        self.flagged = flagged
        self.categories = categories

    def __repr__(self):
        return f"ModerationResult(flagged={self.flagged}, categories={self.categories})"

def moderate_text(text: str) -> ModerationResult:
    if MODERATION_PROVIDER == "openai":
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package is required for moderation.")
        client = OpenAI()
        resp = client.moderations.create(model=MODERATION_MODEL, input=text)
        result = resp.results[0]
        flagged = result.flagged
        categories = [cat for cat, val in result.categories.items() if val] # pyright: ignore[reportAttributeAccessIssue]
        return ModerationResult(flagged, categories)
    elif MODERATION_PROVIDER == "gemini":
        try:
            import google.genai as genai # type: ignore
        except ImportError:
            raise ImportError("google-genai is required for Gemini moderation.")
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")
        client = genai.Client(api_key=GEMINI_API_KEY)
        moderation_prompt = (
            "You are a content moderation system. "
            "Categories: hate, violence, self-harm, sexual, harassment, dangerous, illegal, other. "
            "Does the following text violate any content policy? "
            "Reply with JSON: {\"flagged\": true/false, \"categories\": [list of categories or empty]}\nText: " + text
        )
        gen_config = {"temperature": 0.0}
        interaction = client.interactions.create(
            model=GEMINI_MODEL,
            input=moderation_prompt,
            generation_config=gen_config # pyright: ignore[reportArgumentType]
        )
        outputs = getattr(interaction, "outputs", [])
        response = ""
        for output in outputs:
            if hasattr(output, "text"):
                response = output.text
        import json
        try:
            data = json.loads(response)
            flagged = bool(data.get("flagged", False))
            categories = data.get("categories", [])
            if not isinstance(categories, list):
                categories = []
        except Exception:
            flagged = False
            categories = []
        return ModerationResult(flagged, categories)
    else:
        raise ValueError(f"Unknown MODERATION_PROVIDER: {MODERATION_PROVIDER}")
