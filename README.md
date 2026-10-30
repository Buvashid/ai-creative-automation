# PaisaPath: One Template, Twenty Creatives

PaisaPath is a lightweight Python creative-automation project for the Yanisa
Execution assignment. It turns 20 CSV creative specifications into branded
personal-finance demonstration advertisements. The goal is to reduce repetitive
manual work while keeping supplied offers unchanged, validating input, and
making human QA explicit.

PaisaPath and all offers in this repository are fictional demonstration
material. They are not real financial products and are not financial advice.

## Features

- Reusable 1080 x 1080 Pillow template with consistent PaisaPath branding.
- CSV-driven generation for exactly 20 creative specifications.
- English, Hindi, and Marathi copy support.
- Required-field, duplicate-ID, language, blank-value, and row-count validation.
- Claim-safe copy preparation that preserves supplied offers exactly.
- Per-creative generation failure handling.
- Pytest coverage for loading, validation, copy generation, rendering, and the
  pipeline.
- CSV quality reporting with separate generation and QA statuses.
- Visual audit documenting programmatic checks and remaining human review.

Generated creatives are not automatically approved. Successful files receive
`qa_status=PENDING_REVIEW`; Hindi and Marathi files are also flagged for manual
language review.

## Pipeline

```text
data/creatives.csv
        |
        v
CSV loading and whitespace normalization
        |
        v
Whole-dataset validation
        |
        v
Claim-safe content generation
        |
        v
Pillow 1080 x 1080 PNG rendering
        |
        v
reports/quality_report.csv
```

Validation blocks the batch when required fields are invalid, IDs are
duplicated, languages are unsupported, or the row count is not exactly 20.
Individual rendering failures are recorded and do not stop later rows.

## Tech stack

- Python
- Pandas for CSV loading
- Pillow for image rendering
- pytest for automated tests

## Project structure

```text
app/
  config.py              Shared paths and canvas size
  content_generator.py   Structured, claim-safe copy generation
  data_loader.py         CSV loading and normalization
  generate_samples.py    Three-language sample generator
  main.py                End-to-end pipeline
  quality_checker.py     QA status values
  template_renderer.py   Pillow template renderer
  validator.py           Dataset validation
data/
  creatives.csv          The 20 creative specifications
assets/                  Reserved branding assets
output/                  Generated PNG files
reports/
  quality_report.csv     Generation and QA results
  visual_audit.md        Programmatic and human-review audit
tests/                   Automated tests
requirements.txt         Python dependencies
```

## Windows setup

From the project root in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

If PowerShell blocks activation, run the commands with the virtual
environment's interpreter instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the pipeline

With the virtual environment activated:

```powershell
py -m app.main
```

To generate the three small English, Hindi, and Marathi samples:

```powershell
py -m app.generate_samples
```

## Run tests

```powershell
py -m pytest
```

The current test suite result is **32 passed**.

## CSV schema

`data/creatives.csv` must contain these columns in this order:

```text
creative_id,product,audience,offer,language
```

Example:

```csv
creative_id,product,audience,offer,language
C001,Budgeting tools,Young professionals,Explore budgeting tools,English
```

The project expects IDs `C001` through `C020`, non-empty fields, and only
`English`, `Hindi`, or `Marathi`. Offers are copied exactly as supplied; the
application does not add rates, returns, guarantees, or other claims.

## Outputs and QA

- PNG advertisements: `output/C001.png` through `output/C020.png`
- Generation and QA report: `reports/quality_report.csv`
- Visual audit: `reports/visual_audit.md`

The report keeps generation status separate from QA status:

- `GENERATED` or `GENERATED_MANUAL_REVIEW`: rendering completed.
- `FAILED`: that creative could not be generated.
- `BLOCKED`: the batch could not start because validation failed.
- `PENDING_REVIEW`: generated output awaits human QA.
- `FIX_REQUIRED`: generation or validation requires correction.

The 20 images have passed basic file, dimension, and consistency checks, but
remain `PENDING_REVIEW`. Full-size readability, exact text verification, and
Hindi/Marathi linguistic accuracy still require human review. No creative is
fully approved by automated tests or file generation alone.

## Font configuration

English rendering searches common Windows fonts. Hindi and Marathi rendering
requires a Windows Devanagari-compatible font such as Nirmala UI or Mangal.
The renderer does not silently replace unsupported characters.

To configure a specific Devanagari TrueType font in PowerShell:

```powershell
$env:PAISAPATH_DEVANAGARI_FONT_PATH = "C:\Path\To\NirmalaUI.ttf"
py -m app.main
```

The code verifies that the configured file exists. If no suitable font is
available, Hindi and Marathi creatives are reported as failures with a clear
configuration message. Pillow RAQM shaping is used only when available;
Devanagari output still requires visual inspection.

## Known issue and handling

The pipeline encountered missing Devanagari fonts on Windows during Hindi and
Marathi generation. This is handled explicitly: the renderer supports
`PAISAPATH_DEVANAGARI_FONT_PATH` and reports a clear error instead of silently
rendering replacement boxes. Configure a compatible font before regenerating
those creatives; the repository does not claim that font configuration is
complete on every machine.
