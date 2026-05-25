# Examples

This repository intentionally does not include real course PDFs or copyrighted slide screenshots.

`demo.html` is a self-authored mock review page that shows the intended output style without using private course material. `demo-preview.png` is a public-safe preview image used by the repository README and social sharing.

Live demo:

```text
https://misakakuroko.github.io/bilingual-slide-study-kit/examples/demo.html
```

To create another public demo, use slides that you authored yourself or materials released under a license that permits redistribution.

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
