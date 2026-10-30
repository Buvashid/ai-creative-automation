# Creative Visual Audit

Audit scope: 20 CSV specifications, 20 PNG files in `output/`, and
`reports/quality_report.csv`.

## Automated checks

| Check | Result |
|---|---|
| CSV rows | 20 |
| Output PNG files | 20 of 20 present |
| Image dimensions | 20 of 20 are 1080 x 1080 |
| Image format | 20 of 20 are PNG/RGB |
| CSV/report IDs | Match in order: C001-C020 |
| Report output paths | Relative and point to expected files |
| Generation failures | 0 |
| Report QA status | All are `PENDING_REVIEW`; none are auto-approved |
| Language distribution | English 10, Hindi 5, Marathi 5 |
| Supplied offers | Preserved by the source-to-render pipeline |

Offer preservation is verified by comparing each CSV row with the structured
copy passed to the renderer. The audit does not use OCR to independently
verify every offer pixel.

## Actual visual inspection

- A contact-sheet inspection covered all 20 current PNGs.
- Full-size inspection covered C001, C011, C016, and C020.
- The PaisaPath header, language label, content area, offer panel, colors, and
  disclaimer placement are consistent.
- No obvious clipping, overlap, or unsafe boundary placement was observed.
- C020's two-line Marathi body remains inside its content area.
- The reviewed Hindi and Marathi images show rendered Devanagari glyphs and no
  replacement boxes.
- The visual screening found no source defect requiring a correction.

The contact sheet is suitable for screening consistency, not for final
approval of every small text detail.

## Language review

All Hindi and Marathi creatives remain `PENDING_REVIEW`. A competent reviewer
must confirm grammar, natural phrasing, intended meaning, cultural
appropriateness, and Devanagari shaping at full size. Automated tests and this
visual screening do not prove language accuracy.

## QA disposition

The detailed per-creative record is in `reports/qa_log.csv`. All 20 creatives
have `final_disposition=PENDING_REVIEW`; none are marked fully approved.

Human reviewer checklist:

- Confirm headline and body wording at full size.
- Confirm each visible offer exactly matches its CSV value.
- Confirm the correct language disclaimer is present and readable.
- Confirm no clipping, overlap, or low-contrast text.
- Complete Hindi and Marathi language review.
