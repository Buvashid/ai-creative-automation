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
    if language == "English":
        headline = f"{product} for {audience}"
        body = f"Simple tools for {audience} to explore {product}."
    elif language == "Hindi":
        headline, body = _hindi_copy(product, audience)
    else:
        headline, body = _marathi_copy(product, audience)

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


def _hindi_copy(product: str, audience: str) -> tuple[str, str]:
    """Return a simple topic-specific Hindi headline and body."""
    wording = {
        "बजट बनाने के साधन": (
            "बजट बनाना शुरू करें",
            "रोज़मर्रा के खर्चों की बेहतर योजना बनाने के लिए बजट बनाना सीखें।",
        ),
        "पैसों की योजना": (
            "अपने पैसों की योजना बनाएं",
            "पैसों की योजना बनाने के आसान तरीके समझें।",
        ),
        "व्यक्तिगत ऋण शिक्षा": (
            "व्यक्तिगत ऋण को समझें",
            "व्यक्तिगत ऋण की बुनियादी बातें सरल भाषा में जानें।",
        ),
        "बीमा शिक्षा": (
            "बीमा को आसान भाषा में समझें",
            "बीमा से जुड़ी बुनियादी बातें और जरूरी शब्दावली जानें।",
        ),
        "निवेश की जानकारी": (
            "निवेश की जानकारी, आसान भाषा में",
            "निवेश की बुनियादी बातें समझें और सोच-समझकर फैसले लेना सीखें।",
        ),
    }
    return wording.get(
        product,
        (f"{product} को समझें", f"{product} की सरल जानकारी जानें।"),
    )


def _marathi_copy(product: str, audience: str) -> tuple[str, str]:
    """Return a simple topic-specific Marathi headline and body."""
    wording = {
        "अर्थसंकल्पाची साधने": (
            "बजेटचे नियोजन सहज करा",
            "रोजच्या खर्चाचा हिशोब ठेवा आणि पैशांचे नियोजन करायला शिका.",
        ),
        "पैशांचे नियोजन": (
            "बचतीची सवय लावा",
            "नियमित बचतीच्या सोप्या पद्धती जाणून घ्या आणि त्या रोजच्या जीवनात वापरा.",
        ),
        "वैयक्तिक कर्ज शिक्षण": (
            "पैशांचे नियोजन करा",
            "तुमचे उत्पन्न आणि खर्च समजून घेऊन पैशांचे नियोजन करायला शिका.",
        ),
        "विमा शिक्षण": (
            "आर्थिक उद्दिष्टे ठरवा",
            "तुमच्या गरजांनुसार आर्थिक उद्दिष्टे ठरवा आणि ती साध्य करण्यासाठी नियोजन करा.",
        ),
        "गुंतवणुकीची माहिती": (
            "गुंतवणुकीच्या मूलभूत गोष्टी जाणून घ्या",
            "गुंतवणुकीचे विविध पर्याय समजून घ्या आणि आर्थिक निर्णय विचारपूर्वक घ्या.",
        ),
    }
    return wording.get(
        product,
        (f"{product} समजून घ्या", f"{product}बद्दलची सोपी माहिती जाणून घ्या."),
    )
