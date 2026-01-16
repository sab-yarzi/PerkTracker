import os
import logging
from models import PerkList
from regex_helper import parse_offer_fields
from llm_client import extract_perks_from_image

logger = logging.getLogger(__name__)


def process_screenshot(
        image_path: str,
        model: str,
        temperature: float = 0
) -> PerkList:
    """Load image, extract perks via LLM, parse fields."""
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")

    logger.info(f"Processing {image_path}")
    json_text = extract_perks_from_image(image_path, model, temperature)
    logger.debug(f"Raw JSON: {json_text}")

    perk_list = PerkList.model_validate_json(json_text)

    # Parse offer fields for each perk
    for perk in perk_list.perks:
        parse_offer_fields(perk)

    return perk_list
