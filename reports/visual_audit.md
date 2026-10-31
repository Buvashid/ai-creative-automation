# Creative Visual Audit

**Audit scope:** 20 CSV specifications, 20 PNG files in `output/`, `reports/quality_report.csv`, and `reports/qa_log.csv`.

## 1. Automated Checks

| Check | Result |
|---|---|
| CSV rows | 20 |
| Output PNG files | 20 of 20 present |
| Image dimensions | 20 of 20 are 1080 × 1080 |
| Image format | 20 of 20 are PNG/RGB |
| CSV/report IDs | Match in order: C001–C020 |
| Report output paths | Relative and point to expected files |
| Generation failures | 0 |
| Language distribution | English 10, Hindi 5, Marathi 5 |
| Supplied offers | Preserved by the source-to-render pipeline |

Offer preservation was checked by comparing CSV values with the structured copy passed to the renderer. This check does not use OCR to independently verify every visible offer in the final images.

## 2. Visual Inspection

The following checks are recorded from the project's visual audit:

- A contact-sheet inspection covered all 20 PNGs.
- Full-size inspection covered C001, C011, C016, and C020.
- The PaisaPath header, language label, content area, offer panel, colors, and disclaimer placement were consistent.
- No obvious clipping, overlap, or unsafe boundary placement was observed during the recorded inspection.
- C020's two-line Marathi body remained inside its content area.
- The inspected Hindi and Marathi images displayed Devanagari glyphs without visible replacement boxes.
- The recorded visual screening identified no source defect requiring correction.

A contact sheet is useful for screening consistency but cannot establish that every small text detail is readable or correct.

## 3. Language Review

The project's `reports/qa_log.csv` records a `PASS` disposition for all 20 creatives, including the Hindi and Marathi creatives.

The regional-language review was performed by the project author. It should not be represented as independent linguistic certification.

The review record documents the checks performed for this assignment. Automated tests and visual inspection alone cannot prove linguistic accuracy, cultural appropriateness, or suitability for real-world financial advertising.

## 4. QA Disposition

The per-creative QA record is maintained in `reports/qa_log.csv`.

According to the committed QA log, all 20 creatives have `final_disposition=PASS`.

The generation report, `reports/quality_report.csv`, separately records generation outcomes and QA statuses. Its `PENDING_REVIEW` values should not be interpreted as overriding the separate manual QA log; the two reports track different stages of the workflow.

## 5. Review Checklist

The project's review process covers:

- Confirming headline and body wording at full size.
- Checking that each visible offer matches its CSV value.
- Confirming the correct language disclaimer is present and readable.
- Checking for clipping, overlap, and low-contrast text.
- Reviewing English, Hindi, and Marathi spelling and meaning.
- Checking for unsupported glyphs and rendering problems.
- Ensuring no unsupported or misleading financial claims were introduced.

## 6. Limitations

- The documented visual inspection does not establish that every pixel or text element was independently verified.
- Offer-preservation checks compare structured source data with the copy passed to the renderer; they are not a substitute for independently checking all visible text.
- Regional-language review was performed by the project author and was not independently certified.
- A passing QA record does not constitute regulatory approval or approval to publish fictional offers as real financial products.
- Automated tests verify technical behavior but cannot guarantee creative effectiveness or complete linguistic accuracy.

**Conclusion:** The recorded checks cover all 20 generated creatives. The manual QA log records PASS for every creative, while the generation report retains its separate status values. These records should be interpreted according to their respective purposes.