import csv
from pathlib import Path

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


@pytest.mark.parametrize(
    ("language", "product", "audience", "topic_words"),
    [
        ("Hindi", "बजट बनाने के साधन", "युवा पेशेवर", ("बजट", "खर्चों")),
        ("Hindi", "निवेश की जानकारी", "नए निवेशक", ("निवेश", "जानकारी")),
        ("Marathi", "अर्थसंकल्पाची साधने", "तरुण व्यावसायिक", ("बजेट", "खर्चाचा")),
        ("Marathi", "गुंतवणुकीची माहिती", "नवीन गुंतवणूकदार", ("गुंतवणुकी", "मूलभूत")),
    ],
)
def test_non_english_copy_is_topic_specific(
    language, product, audience, topic_words
):
    result = prepare_copy(
        creative_specification(language).copy()
        | {"product": product, "audience": audience}
    )

    assert all(word in f"{result['headline']} {result['body']}" for word in topic_words)


def test_non_english_headlines_are_not_repeated():
    hindi_products = [
        "बजट बनाने के साधन",
        "पैसों की योजना",
        "व्यक्तिगत ऋण शिक्षा",
        "बीमा शिक्षा",
        "निवेश की जानकारी",
    ]

    headlines = {
        prepare_copy(
            creative_specification("Hindi").copy() | {"product": product}
        )["headline"]
        for product in hindi_products
    }

    assert len(headlines) == len(hindi_products)


@pytest.mark.parametrize(
    ("product", "headline", "body"),
    [
        (
            "अर्थसंकल्पाची साधने",
            "बजेटचे नियोजन सहज करा",
            "रोजच्या खर्चाचा हिशोब ठेवा",
        ),
        (
            "पैशांचे नियोजन",
            "बचतीची सवय लावा",
            "नियमित बचतीच्या",
        ),
        (
            "वैयक्तिक कर्ज शिक्षण",
            "पैशांचे नियोजन करा",
            "तुमचे उत्पन्न आणि खर्च",
        ),
        (
            "विमा शिक्षण",
            "आर्थिक उद्दिष्टे ठरवा",
            "तुमच्या गरजांनुसार आर्थिक उद्दिष्टे",
        ),
        (
            "गुंतवणुकीची माहिती",
            "गुंतवणुकीच्या मूलभूत गोष्टी जाणून घ्या",
            "गुंतवणुकीचे विविध पर्याय",
        ),
    ],
)
def test_marathi_templates_include_expected_topic_copy(product, headline, body):
    result = prepare_copy(
        creative_specification("Marathi").copy() | {"product": product}
    )

    assert result["headline"] == headline
    assert body in result["body"]
    assert result["manual_review_required"] is True


@pytest.mark.parametrize(
    ("creative_id", "headline", "body"),
    [
        (
            "C016",
            "बजेटचे नियोजन सहज करा",
            "रोजच्या खर्चाचा हिशोब ठेवा आणि पैशांचे नियोजन करायला शिका.",
        ),
        (
            "C020",
            "गुंतवणुकीच्या मूलभूत गोष्टी जाणून घ्या",
            "गुंतवणुकीचे विविध पर्याय समजून घ्या आणि आर्थिक निर्णय विचारपूर्वक घ्या.",
        ),
    ],
)
def test_csv_creatives_generate_revised_marathi_copy(
    creative_id, headline, body
):
    csv_path = Path(__file__).parents[1] / "data" / "creatives.csv"
    with csv_path.open(encoding="utf-8", newline="") as csv_file:
        rows = csv.DictReader(csv_file)
        specification = next(row for row in rows if row["creative_id"] == creative_id)

    result = prepare_copy(specification)

    assert result["headline"] == headline
    assert result["body"] == body
    assert result["offer"] == specification["offer"]
    assert result["manual_review_required"] is True
