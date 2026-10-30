import csv
from pathlib import Path

import pandas as pd

from app import main


def valid_creatives() -> pd.DataFrame:
    row_count = 20
    return pd.DataFrame(
        {
            "creative_id": [f"C{index:03d}" for index in range(1, row_count + 1)],
            "product": ["Budgeting tools"] * row_count,
            "audience": ["Students"] * row_count,
            "offer": ["Example offer for demonstration only"] * row_count,
            "language": ["English"] * row_count,
        }
    )


def test_run_pipeline_generates_report_and_outputs(tmp_path: Path, monkeypatch):
    creatives = valid_creatives()
    creatives.loc[1, "language"] = "Hindi"
    monkeypatch.setattr(main, "load_creatives", lambda _: creatives)
    monkeypatch.setattr(
        main,
        "render_creative",
        lambda copy_data, output_dir: output_dir / f"{copy_data['creative_id']}.png",
    )

    summary = main.run_pipeline(
        csv_path=tmp_path / "input.csv",
        output_dir=tmp_path / "output",
        reports_dir=tmp_path / "reports",
    )

    assert summary == {
        "total": 20,
        "successful": 20,
        "failures": 0,
        "manual_review": 1,
    }
    with (tmp_path / "reports" / "quality_report.csv").open(
        encoding="utf-8", newline=""
    ) as report_file:
        rows = list(csv.DictReader(report_file))
    assert [row["status"] for row in rows[:2]] == [
        "GENERATED",
        "GENERATED_MANUAL_REVIEW",
    ]
    assert [row["qa_status"] for row in rows[:2]] == [
        "PENDING_REVIEW",
        "PENDING_REVIEW",
    ]
    assert rows[0]["issues"] == ""
    assert rows[1]["issues"] == "Manual language review required for Hindi/Marathi"
    assert len(rows) == 20


def test_run_pipeline_blocks_validation_failure(tmp_path: Path, monkeypatch):
    creatives = valid_creatives().drop(columns=["offer"])
    monkeypatch.setattr(main, "load_creatives", lambda _: creatives)
    render_called = False

    def fail_if_called(*args, **kwargs):
        nonlocal render_called
        render_called = True

    monkeypatch.setattr(main, "render_creative", fail_if_called)

    summary = main.run_pipeline(
        output_dir=tmp_path / "output",
        reports_dir=tmp_path / "reports",
    )

    assert summary["successful"] == 0
    assert render_called is False
    report = (tmp_path / "reports" / "quality_report.csv").read_text(
        encoding="utf-8"
    )
    assert "BLOCKED" in report
    assert "FIX_REQUIRED" in report
    assert "Missing required columns" in report


def test_run_pipeline_records_individual_failure(tmp_path: Path, monkeypatch):
    creatives = valid_creatives()
    monkeypatch.setattr(main, "load_creatives", lambda _: creatives)

    def render_with_one_failure(copy_data, output_dir):
        if copy_data["creative_id"] == "C002":
            raise ValueError("Text cannot fit")
        return output_dir / "C001.png"

    monkeypatch.setattr(main, "render_creative", render_with_one_failure)

    summary = main.run_pipeline(
        output_dir=tmp_path / "output",
        reports_dir=tmp_path / "reports",
    )

    assert summary == {
        "total": 20,
        "successful": 19,
        "failures": 1,
        "manual_review": 0,
    }
    report = (tmp_path / "reports" / "quality_report.csv").read_text(
        encoding="utf-8"
    )
    assert "C002" in report
    assert "FAILED" in report
    assert "FIX_REQUIRED" in report
    assert "Text cannot fit" in report
