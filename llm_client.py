from ollama import chat
from models import PerkList

SYSTEM_PROMPT = """
You are a data extraction tool.
Extract perks from the screenshot.

Return ONLY valid JSON matching the schema.

Rules:
- Create ONE item per offer shown.
- company_name: brand/company name shown next to the offer
- offer_text: exact offer headline text (verbatim)
- expiry_text: exact expiry text shown (verbatim) or null
- conditions_text: any other constraints shown (verbatim) or null
- DO NOT compute numbers. Do NOT fill minimum_spend/money_back/percentage_value/cap_amount.
- confidence: 0..1 (how sure you captured the text correctly)
- overall_confidence: 0..1
"""

def extract_perks_from_image(
    image_path: str,
    model: str,
    temperature: float = 0
) -> str:
    """Call LLM with image and return raw JSON string."""
    response = chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": "Extract perks from this screenshot. Return JSON only.",
                "images": [image_path]
            }
        ],
        format=PerkList.model_json_schema(),
        options={"temperature": temperature},
        stream=False,
    )
    return response["message"]["content"]
