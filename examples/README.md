# Examples

This repository intentionally does not include real course PDFs or generated screenshots.

To create a public demo, use slides that you authored yourself or materials released under a license that permits redistribution.

Suggested demo structure:

```text
examples/
└── demo-course/
    ├── demo-slides.pdf
    ├── demo_assets/
    └── DEMO_REVIEW.zh.html
```

Run:

```bash
python3 scripts/prepare_ppt_review_assets.py \
  --pdf examples/demo-course/demo-slides.pdf \
  --output-dir examples/demo-course/demo_assets \
  --prefix demo \
  --pages "1-5" \
  --clean
```

Then ask Codex:

```text
Use $course-ppt-review-html to create a bilingual exam review HTML page from examples/demo-course/demo-slides.pdf.
```
