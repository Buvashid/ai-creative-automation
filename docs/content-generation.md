# Content Generation

This project uses deterministic Python templates to prepare advertising copy.
It does not call an external AI model or API.

## From CSV row to copy

The pipeline reads `data/creatives.csv` with
[`load_creatives`](../app/data_loader.py). Each row must contain:

```text
creative_id,product,audience,offer,language
```

The loader strips surrounding whitespace from column names and string values.
[`validate_creatives`](../app/validator.py) then checks required columns,
required values, duplicate IDs, supported languages, and the expected count of
20 rows. Any error or count mismatch blocks the batch before images are
generated.

For each valid row, [`prepare_copy`](../app/content_generator.py) validates the
required fields and selects a fixed template for the row's language. It returns
structured fields for the renderer:

- `creative_id`
- `product`
- `audience`
- `headline`
- `body`
- `offer`
- `language`
- `disclaimer`

## Language templates

The generator supports exactly English, Hindi, and Marathi:

- English uses a concise English headline and body.
- Hindi uses a Devanagari headline and body.
- Marathi uses a Devanagari headline and body.

Product and audience values come from the CSV row and are inserted into the
language-specific templates. The offer is passed through exactly as supplied;
the generator does not add financial figures, rates, returns, guarantees, or
other claims.

Hindi and Marathi output is flagged for manual language review. The templates
are deterministic, but competent human review is required for translation
quality, grammar, cultural appropriateness, and final glyph rendering.

## Branding, offers, and disclaimers

[`render_creative`](../app/template_renderer.py) uses a reusable 1080 x 1080
Pillow layout with:

- The fictional `PaisaPath` brand header.
- The product/topic and language label.
- The generated headline and body.
- A highlighted offer panel containing the supplied offer.
- The language-specific fictional-demonstration disclaimer.

The disclaimers are:

- English: `Fictional demonstration material. Not financial advice.`
- Hindi: `यह केवल काल्पनिक प्रदर्शन सामग्री है। यह वित्तीय सलाह नहीं है।`
- Marathi: `ही केवळ काल्पनिक प्रात्यक्षिक सामग्री आहे. हा आर्थिक सल्ला नाही.`

The renderer wraps text, reduces font sizes within configured limits, and
raises an error if content cannot fit. It does not silently clip text or
replace unsupported Devanagari characters.

## Automated checks

The current pipeline automates:

- CSV file loading and empty-input errors.
- Required columns and non-empty required values.
- Duplicate creative ID detection.
- Supported-language validation.
- The exact 20-row batch requirement.
- Output image creation and PNG dimensions through tests.
- Renderer filename safety, text-fit checks, and output-directory creation.
- Generation status and per-creative failures in
  `reports/quality_report.csv`.
- Default QA status of `PENDING_REVIEW` for generated images.

## Human review

Automated generation is not visual approval. Human reviewers must check:

- Full-size readability, spacing, clipping, and contrast.
- Exact visible offer and disclaimer text.
- Hindi and Marathi language accuracy and cultural appropriateness.
- Devanagari shaping and glyph quality on the target machine.

Hindi and Marathi rows are explicitly marked for manual language review. The
visual audit in [`reports/visual_audit.md`](../reports/visual_audit.md) records
the current programmatic checks and review limitations.

## Limitations and known issues

- Copy is based on fixed deterministic templates, not an external AI service.
- The generator does not verify the truth of supplied financial data.
- The renderer depends on an installed compatible font. Hindi and Marathi
  require a Devanagari-compatible Windows font such as Nirmala UI or Mangal.
- A custom font can be configured with
  `PAISAPATH_DEVANAGARI_FONT_PATH`.
- Pillow uses RAQM shaping only when that capability is available; Hindi and
  Marathi still require visual inspection.
- A missing Devanagari font causes those creatives to fail clearly rather than
  silently substituting characters.
