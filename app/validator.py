"""Validate creative specifications before rendering."""

import pandas as pd

REQUIRED_COLUMNS = ("creative_id", "product", "audience", "offer", "language")
ALLOWED_LANGUAGES = {"English", "Hindi", "Marathi"}


def validate_creatives(creatives: pd.DataFrame) -> list[str]:
    """Return readable validation errors and warnings for creative specifications."""
    errors: list[str] = []
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in creatives.columns
    ]

    if missing_columns:
        errors.append(f"ERROR: Missing required columns: {', '.join(missing_columns)}")

    available_columns = [
        column for column in REQUIRED_COLUMNS if column in creatives.columns
    ]
    missing_values: list[str] = []
    for row_number, row in creatives.iterrows():
        for column in available_columns:
            value = row[column]
            if pd.isna(value) or (isinstance(value, str) and not value.strip()):
                missing_values.append(f"row {row_number + 2} ({column})")

    if missing_values:
        errors.append(
            "ERROR: Missing required values: " + ", ".join(missing_values)
        )

    if "creative_id" in creatives.columns:
        duplicate_ids = creatives.loc[
            creatives["creative_id"].duplicated(keep=False), "creative_id"
        ].dropna().unique().tolist()
        if duplicate_ids:
            formatted_ids = ", ".join(str(identifier) for identifier in duplicate_ids)
            errors.append(f"ERROR: Duplicate creative IDs: {formatted_ids}")

    if "language" in creatives.columns:
        unsupported_languages = set()
        for value in creatives["language"].dropna():
            if isinstance(value, str):
                language = value.strip()
            else:
                language = str(value)
            if language and language not in ALLOWED_LANGUAGES:
                unsupported_languages.add(language)
        if unsupported_languages:
            languages = ", ".join(sorted(unsupported_languages))
            errors.append(f"ERROR: Unsupported languages: {languages}")

    if len(creatives) != 20:
        errors.append(
            f"WARNING: Creative count mismatch: expected 20, found {len(creatives)}"
        )

    return errors
