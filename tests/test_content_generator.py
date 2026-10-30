import pytest

from app.content_generator import prepare_copy


def creative_specification(language: str = "English", offer: object = "Verified offer"):
    return {
        "creative_id": "creative-1",
        "product": "Credit Card",
        "audience": "Young adults",
        "offer": offer,
        "language": language,
    }


@pytest.mark.parametrize(
    ("language", "disclaimer"),
    [
        ("English", "Fictional demonstration material. Not financial advice."),
        ("Hindi", "यह केवल काल्पनिक प्रदर्शन सामग्री है। यह वित्तीय सलाह नहीं है।"),
        ("Marathi", "ही केवळ काल्पनिक प्रात्यक्षिक सामग्री आहे. हा आर्थिक सल्ला नाही."),
    ],
)
def test_prepare_copy_supports_all_languages(language, disclaimer):
    result = prepare_copy(creative_specification(language))

    assert result["language"] == language
    assert result["headline"]
    assert result["body"]
    assert result["disclaimer"] == disclaimer


def test_prepare_copy_preserves_offer_exactly():
    offer = "  Verified offer: 0% APR  "

    result = prepare_copy(creative_specification(offer=offer))

    assert result["offer"] == offer


def test_prepare_copy_requires_all_fields():
    specification = creative_specification()
    del specification["offer"]

    with pytest.raises(ValueError, match="Missing required fields: offer"):
        prepare_copy(specification)


def test_prepare_copy_rejects_empty_field():
    specification = creative_specification()
    specification["audience"] = "   "

    with pytest.raises(ValueError, match="Required field 'audience' cannot be empty"):
        prepare_copy(specification)


def test_prepare_copy_rejects_unsupported_language():
    with pytest.raises(ValueError, match="Unsupported language 'French'"):
        prepare_copy(creative_specification("French"))


def test_non_english_copy_is_flagged_for_manual_review():
    result = prepare_copy(creative_specification("Hindi"))

    assert result["manual_review_required"] is True
    assert result["review_note"]
