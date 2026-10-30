import pytest

from app.data_loader import load_creatives

REQUIRED_HEADER = "creative_id,product,audience,offer,language"


def test_load_creatives_returns_expected_columns_and_rows(tmp_path):
    csv_path = tmp_path / "creatives.csv"
    csv_path.write_text(
        f"{REQUIRED_HEADER}\n1,Card,Students,0% APR,en\n",
        encoding="utf-8",
    )

    creatives = load_creatives(str(csv_path))

    assert list(creatives.columns) == REQUIRED_HEADER.split(",")
    assert len(creatives) == 1
    assert creatives.iloc[0]["creative_id"] == 1


def test_load_creatives_rejects_missing_required_column(tmp_path):
    csv_path = tmp_path / "creatives.csv"
    csv_path.write_text(
        "creative_id,product,audience,language\n1,Card,Students,en\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing required columns: offer"):
        load_creatives(str(csv_path))


def test_load_creatives_rejects_empty_file(tmp_path):
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="Creative CSV file is empty"):
        load_creatives(str(csv_path))


def test_load_creatives_rejects_headers_without_data_rows(tmp_path):
    csv_path = tmp_path / "headers.csv"
    csv_path.write_text(f"{REQUIRED_HEADER}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="contains no data rows"):
        load_creatives(str(csv_path))


def test_load_creatives_rejects_nonexistent_file(tmp_path):
    with pytest.raises(ValueError, match="does not exist"):
        load_creatives(str(tmp_path / "missing.csv"))


def test_load_creatives_strips_whitespace(tmp_path):
    csv_path = tmp_path / "whitespace.csv"
    csv_path.write_text(
        " creative_id , product , audience , offer , language \n"
        " 1 , Card , Students , 0% APR , en \n",
        encoding="utf-8",
    )

    creatives = load_creatives(str(csv_path))

    assert list(creatives.columns) == REQUIRED_HEADER.split(",")
    assert creatives.iloc[0].to_dict() == {
        "creative_id": 1,
        "product": "Card",
        "audience": "Students",
        "offer": "0% APR",
        "language": "en",
    }
