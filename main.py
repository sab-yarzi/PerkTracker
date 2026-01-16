from ollama import chat
from pydantic import BaseModel
from typing import Optional
import os
import time

SELECTED_MODEL = 'openbmb/minicpm-v4.5'

class SingularPerk(BaseModel):
    company_name: str
    percentage_value: float
    expiry_date: Optional[str] = None
    conditions: Optional[str] = None
    confidence: float

class PerkList(BaseModel):
    perks: list[SingularPerk]
    overall_confidence: float


path = input("Enter the path to the file: ").strip()

if not os.path.isfile(path):
    raise FileNotFoundError(f"File not found: {path}")

start = time.perf_counter()

response = chat(
    model=SELECTED_MODEL,
    messages=[
        {
            "role": "system",
            "content": (
                "You are a data extraction tool. "
                "Extract perks from the screenshot. "
                "Return ONLY valid JSON matching the schema. "
                "Do not guess missing values; use null/empty string where appropriate. "
                "If there is something like get 20% back up to 100, extract only the 20 and in the conditions note the rest. "
                "Confidence must be 0 to 1."
            ),
        },
        {
            "role": "user",
            "content": (
                "Extract perks from this screenshot."
                   "Rules:\n"
                "- company_name: the brand/company offering the perk\n"
                "- percentage_value: number only (e.g. 10 for '10%')\n"
                "- expiry_date: string if shown else null\n"
                "- conditions: string if shown else null\n"
                "- confidence: 0..1\n"
                "- overall_confidence: 0..1\n"
                "Return JSON only."
            ),
            "images":[path]
        }
    ],
    format=PerkList.model_json_schema(),
    options={"temperature": 0},
    stream=True,
)

fullMessage = ""
for chunk in response:
    piece = chunk.message.content or ""
    fullMessage += piece
    print(piece, end="", flush=True)

elapsed = time.perf_counter() - start
print(f"\n\nDone in {elapsed:.2f}s")
perk_list = PerkList.model_validate_json(fullMessage)


for x in perk_list.perks:
    print(f"- {x.company_name}: {x.percentage_value}% (confidence: {x.confidence})")

