import pandas as pd

from app.validator import validate_creatives


def make_creatives(row_count: int = 20) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "creative_id": range(1, row_count + 1),
            "product": ["Credit Card"] * row_count,
            "audience": ["Young adults"] * row_count,
            "offer": ["Verified offer"] * row_count,
            "language": ["English"] * row_count,
        }
    )


def test_valid_creatives_return_no_messages():
    assert validate_creatives(make_creatives()) == []


def test_missing_required_columns_produce_error():
    creatives = make_creatives().drop(columns=["offer"])

    messages = validate_creatives(creatives)

    assert any(message.startswith("ERROR:") for message in messages)
    assert any("offer" in message for message in messages)


def test_blank_offer_produces_error():
    creatives = make_creatives()
    creatives.loc[0, "offer"] = "   "

    messages = validate_creatives(creatives)

    assert any(
        message.startswith("ERROR:") and "offer" in message
        for message in messages
    )


def test_duplicate_creative_ids_produce_error():
    creatives = make_creatives()
    creatives.loc[1, "creative_id"] = creatives.loc[0, "creative_id"]

    messages = validate_creatives(creatives)

    assert any(
        message.startswith("ERROR:") and "Duplicate creative IDs" in message
        for message in messages
    )


def test_unsupported_language_produces_error():
    creatives = make_creatives()
    creatives.loc[0, "language"] = "French"

    messages = validate_creatives(creatives)

    assert any(
        message.startswith("ERROR:") and "French" in message
        for message in messages
    )


def test_fewer_than_20_rows_produce_warning_not_row_count_error():
    messages = validate_creatives(make_creatives(row_count=19))

    assert any(message.startswith("WARNING:") for message in messages)
    assert not any(
        message.startswith("ERROR:") and "Creative count mismatch" in message
        for message in messages
    )


def test_validation_does_not_modify_input_dataframe():
    creatives = make_creatives(row_count=2)
    original = creatives.copy(deep=True)

    validate_creatives(creatives)

    pd.testing.assert_frame_equal(creatives, original)


def test_missing_creative_id_produces_error():
    creatives = make_creatives()
    creatives.loc[0, "creative_id"] = None

    messages = validate_creatives(creatives)

    assert any(
        message.startswith("ERROR:") and "creative_id" in message
        for message in messages
    )
