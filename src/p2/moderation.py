from typing import List

MODERATION_MODEL = "omni-moderation-latest"

class ModerationResult:
    flagged: bool
    categories: List[str]

    def __init__(self, flagged: bool, categories: List[str]):
        self.flagged = flagged
        self.categories = categories

    def __repr__(self):
        return f"ModerationResult(flagged={self.flagged}, categories={self.categories})"

def moderate_text(text: str) -> ModerationResult:
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("openai package is required for moderation.")
    client = OpenAI()
    resp = client.moderations.create(model=MODERATION_MODEL, input=text)
    result = resp.results[0]
    flagged = result.flagged
    categories = [cat for cat, val in result.categories.items() if val] # type: ignore
    return ModerationResult(flagged, categories)
