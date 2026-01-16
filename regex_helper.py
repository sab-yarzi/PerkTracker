import re
from typing import Optional
from models import SingularPerk

MONEY_RE = r"£\s*([0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?)"
PCT_RE = r"([0-9]+(?:\.[0-9]+)?)\s*%"

def to_float(s: str) -> float:
    """Convert '1,200.50' -> 1200.5"""
    return float(s.replace(",", "").strip())

def norm_text(s: Optional[str]) -> str:
    """Lowercase + normalize whitespace"""
    if not s:
        return ""
    return re.sub(r"\s+", " ", s.strip()).lower()


def parse_offer_fields(perk: SingularPerk) -> SingularPerk:
    """
    Extract structured fields from offer_text + conditions_text.
    Does NOT change offer_text itself.
    """
    offer = norm_text(perk.offer_text)
    conds = norm_text(perk.conditions_text)
    text = f"{offer} {conds}".strip()

    # Reset parsed fields to avoid stale values if re-running
    perk.percentage_value = None
    perk.minimum_spend = None
    perk.money_back = None
    perk.cap_amount = None

    # ---- Pattern A: Spend £X or more, get £Y back ----
    # "Spend £100 or more, get £10 back"
    # "Spend £500 or more, get £150 back"
    m = re.search(rf"spend\s*{MONEY_RE}.*?get\s*{MONEY_RE}\s*back", text, re.IGNORECASE)
    if m:
        perk.minimum_spend = to_float(m.group(1))
        perk.money_back = to_float(m.group(2))
        return perk

    # ---- Pattern B: Get X% back up to £Y ----
    # "Get 20% back up to £200"
    # "Get 10% back every time up to £750"
    m = re.search(rf"get\s*{PCT_RE}\s*back.*?up\s*to\s*{MONEY_RE}", text, re.IGNORECASE)
    if m:
        perk.percentage_value = to_float(m.group(1))
        perk.cap_amount = to_float(m.group(2))
        return perk

    # ---- Pattern C: SAVE X% (common gift card screens) ----
    # "SAVE 9%"
    m = re.search(rf"save\s*{PCT_RE}", text, re.IGNORECASE)
    if m:
        perk.percentage_value = to_float(m.group(1))
        return perk

    # ---- Pattern D: Generic percent anywhere ----
    # "10% off" / "Get 5% back"
    m = re.search(rf"{PCT_RE}", text, re.IGNORECASE)
    if m:
        perk.percentage_value = to_float(m.group(1))
        return perk

    # ---- Pattern E: Generic money offer (fallback) ----
    # If it says "get £10 back" without spend threshold
    m = re.search(rf"get\s*{MONEY_RE}\s*back", text, re.IGNORECASE)
    if m:
        perk.money_back = to_float(m.group(1))
        return perk

    # Nothing matched
    return perk

