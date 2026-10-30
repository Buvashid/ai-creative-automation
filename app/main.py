"""Run the PaisaPath creative generation pipeline."""

import csv
from pathlib import Path

from app.config import CREATIVES_CSV, OUTPUT_DIR, REPORTS_DIR
from app.content_generator import prepare_copy
from app.data_loader import load_creatives
from app.quality_checker import QA_FIX_REQUIRED, initial_qa_status
from app.template_renderer import render_creative
from app.validator import validate_creatives

REPORT_COLUMNS = (
    "creative_id",
    "language",
    "output_file",
    "status",
    "qa_status",
    "issues",
)
COUNT_WARNING_PREFIX = "WARNING: Creative count mismatch:"


def _write_report(report_path: Path, rows: list[dict[str, str]]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", newline="", encoding="utf-8") as report_file:
        writer = csv.DictWriter(report_file, fieldnames=REPORT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _is_blocking_issue(issue: str) -> bool:
    return issue.startswith("ERROR:") or issue.startswith(COUNT_WARNING_PREFIX)


def run_pipeline(
    csv_path: Path = CREATIVES_CSV,
    output_dir: Path = OUTPUT_DIR,
    reports_dir: Path = REPORTS_DIR,
) -> dict[str, int]:
    """Validate and render all creatives, returning a generation summary."""
    report_path = reports_dir / "quality_report.csv"
    try:
        creatives = load_creatives(str(csv_path))
    except ValueError as error:
        _write_report(
            report_path,
            [
                {
                    "creative_id": "",
                    "language": "",
                    "output_file": "",
                    "status": "BLOCKED",
                    "qa_status": QA_FIX_REQUIRED,
                    "issues": str(error),
                }
            ],
        )
        print(f"ERROR: {error}")
        return {"total": 0, "successful": 0, "failures": 1, "manual_review": 0}

    validation_issues = validate_creatives(creatives)
    if any(_is_blocking_issue(issue) for issue in validation_issues):
        report_rows = [
            {
                "creative_id": str(row.get("creative_id", "")),
                "language": str(row.get("language", "")),
                "output_file": "",
                "status": "BLOCKED",
                "qa_status": QA_FIX_REQUIRED,
                "issues": " | ".join(validation_issues),
            }
            for row in creatives.to_dict(orient="records")
        ]
        _write_report(report_path, report_rows)
        print("Validation blocked generation:")
        for issue in validation_issues:
            print(f"- {issue}")
        return {
            "total": len(creatives),
            "successful": 0,
            "failures": len(creatives),
            "manual_review": 0,
        }

    report_rows: list[dict[str, str]] = []
    successful = 0
    failures = 0
    manual_review = 0

    for row in creatives.to_dict(orient="records"):
        creative_id = str(row["creative_id"])
        language = str(row["language"])
        try:
            copy_data = prepare_copy(row)
            output_path = render_creative(copy_data, output_dir)
        except (OSError, ValueError, TypeError) as error:
            failures += 1
            report_rows.append(
                {
                    "creative_id": creative_id,
                    "language": language,
                    "output_file": "",
                    "status": "FAILED",
                    "qa_status": QA_FIX_REQUIRED,
                    "issues": str(error),
                }
            )
            print(f"FAILED {creative_id}: {error}")
            continue

        successful += 1
        needs_review = language in {"Hindi", "Marathi"}
        if needs_review:
            manual_review += 1
        status = "GENERATED_MANUAL_REVIEW" if needs_review else "GENERATED"
        report_rows.append(
            {
                "creative_id": creative_id,
                "language": language,
                "output_file": str(output_path),
                "status": status,
                "qa_status": initial_qa_status(True),
                "issues": (
                    "Manual language review required for Hindi/Marathi"
                    if needs_review
                    else ""
                ),
            }
        )
        print(f"GENERATED {creative_id}: {output_path}")

    _write_report(report_path, report_rows)
    summary = {
        "total": len(creatives),
        "successful": successful,
        "failures": failures,
        "manual_review": manual_review,
    }
    print(
        "Summary: "
        f"total rows={summary['total']}, "
        f"successful generations={summary['successful']}, "
        f"failures={summary['failures']}, "
        f"manual-review items={summary['manual_review']}"
    )
    print(f"Quality report: {report_path}")
    return summary


def main() -> None:
    """Run the pipeline using the project default paths."""
    run_pipeline()


if __name__ == "__main__":
    main()
