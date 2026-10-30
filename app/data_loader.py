"""Load and normalize creative specifications from CSV files."""

import pandas as pd

REQUIRED_COLUMNS = ("creative_id", "product", "audience", "offer", "language")


def load_creatives(csv_path: str) -> pd.DataFrame:
    """Load a non-empty creative CSV and strip surrounding whitespace."""
    try:
        creatives = pd.read_csv(csv_path)
    except FileNotFoundError as error:
        raise ValueError(f"Creative CSV file does not exist: {csv_path}") from error
    except pd.errors.EmptyDataError as error:
        raise ValueError(f"Creative CSV file is empty: {csv_path}") from error
    except (OSError, pd.errors.ParserError) as error:
        raise ValueError(
            f"Could not read creative CSV file '{csv_path}': {error}"
        ) from error

    creatives.columns = creatives.columns.str.strip()
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in creatives.columns
    ]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Creative CSV is missing required columns: {missing}")

    if creatives.empty:
        raise ValueError("Creative CSV contains no data rows")

    for column in creatives.select_dtypes(include=["object", "string"]).columns:
        creatives[column] = creatives[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )

    return creatives
