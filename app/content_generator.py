"""Prepare simple, claim-safe advertising copy."""

from collections.abc import Mapping

REQUIRED_FIELDS = ("creative_id", "product", "audience", "offer", "language")
SUPPORTED_LANGUAGES = {"English", "Hindi", "Marathi"}
DISCLAIMERS = {
    "English": "Fictional demonstration material. Not financial advice.",
    "Hindi": "यह केवल काल्पनिक प्रदर्शन सामग्री है। यह वित्तीय सलाह नहीं है।",
    "Marathi": "ही केवळ काल्पनिक प्रात्यक्षिक सामग्री आहे. हा आर्थिक सल्ला नाही.",
}


def prepare_copy(specification: Mapping[str, object]) -> dict[str, object]:
    """Create structured advertising copy from one validated specification."""
    missing_fields = [
        field for field in REQUIRED_FIELDS if field not in specification
    ]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    values = {field: specification[field] for field in REQUIRED_FIELDS}
    for field in REQUIRED_FIELDS:
        if values[field] is None or (
            isinstance(values[field], str) and not values[field].strip()
        ):
            raise ValueError(f"Required field '{field}' cannot be empty")

    language = str(values["language"]).strip()
    if language not in SUPPORTED_LANGUAGES:
        supported = ", ".join(sorted(SUPPORTED_LANGUAGES))
        raise ValueError(
            f"Unsupported language '{language}'. Supported languages: {supported}"
        )

    product = str(values["product"]).strip()
    audience = str(values["audience"]).strip()
    offer = values["offer"]
    wording = {
        "English": (
            f"{product} for {audience}",
            f"Simple tools for {audience} to explore {product}.",
        ),
        "Hindi": (
            f"{audience} के लिए {product}",
            f"{product} के साथ रोज़मर्रा के पैसों की योजना बनाएं।",
        ),
        "Marathi": (
            f"{audience} साठी {product}",
            f"{product} सोबत रोजच्या पैशांचे नियोजन करा.",
        ),
    }
    headline, body = wording[language]

    result = {
        "creative_id": values["creative_id"],
        "product": values["product"],
        "audience": values["audience"],
        "headline": headline,
        "body": body,
        "offer": offer,
        "language": language,
        "disclaimer": DISCLAIMERS[language],
        "manual_review_required": language != "English",
    }
    if language != "English":
        result["review_note"] = "Review translated wording before publishing."
    return result
