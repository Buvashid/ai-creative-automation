# Creative Visual Audit

Audit scope: 20 CSV specifications, 20 PNG files in `output/`, and
`reports/quality_report.csv`.

## Programmatically verified

| Check | Result |
|---|---|
| CSV rows | 20 |
| Output PNG files | 20 of 20 present |
| Image dimensions | 20 of 20 are 1080 x 1080 |
| Image format | 20 of 20 are PNG/RGB |
| CSV/report IDs | Match in order: C001-C020 |
| Report output paths | All referenced files exist |
| Report QA status | All are `PENDING_REVIEW`; none are auto-approved |
| Language distribution | English 10, Hindi 5, Marathi 5 |

Offer values were compared against the CSV/report pipeline inputs. The
renderer receives the supplied offer unchanged, but this audit does not use
OCR to independently read offer text from pixels.

## Visual and linguistic review

- A contact-sheet review of all 20 images found a consistent PaisaPath header,
  language label, content area, offer panel, and disclaimer placement.
- No obvious clipping, overlap, or unsafe boundary placement was visible at
  the contact-sheet scale.
- Hindi and Marathi glyphs are visibly rendered in the reviewed images; no
  replacement boxes were observed.
- Full-size readability, exact glyph shaping, translation quality, disclaimer
  wording, and offer transcription still require human review.
- Hindi and Marathi rows require manual language review as already recorded
  in the quality report.

## QA decision

No creative is approved by this audit. Keep all 20 items at
`PENDING_REVIEW` until a reviewer checks the full-size images, supplied offer
text, disclaimer text, and Hindi/Marathi language quality.
