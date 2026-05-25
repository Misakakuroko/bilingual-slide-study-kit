# bilingual-slide-study-kit

Turn lecture slides into exam-ready bilingual HTML study guides.

This project packages a reusable Codex skill and a deterministic slide-asset harness for students who need to review English lecture slides, especially when the exam requires technical vocabulary and short-answer responses.

It is not a generic PPT-to-HTML converter. The goal is to generate review pages that explain the slides, extract important terms, create bilingual exam sentences, and add detailed visual explanations for hard-to-understand diagrams.

## What It Creates

For each lecture module, the workflow can produce a standalone HTML review page with:

- slide-range logic map,
- selected PPT/PDF screenshots,
- detailed slide explanations,
- important terminology with Chinese support,
- English short-answer material with full Chinese sentence translations,
- method comparisons,
- common confusions,
- a memorization order for exam prep.

## Repository Layout

```text
bilingual-slide-study-kit/
├── README.md
├── LICENSE
├── .gitignore
├── scripts/
│   └── prepare_ppt_review_assets.py
├── skills/
│   └── course-ppt-review-html/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── references/review-page-criteria.md
│       └── scripts/prepare_ppt_review_assets.py
├── templates/
│   └── visual-card.html
├── examples/
│   └── README.md
└── tests/
    └── test_prepare_ppt_review_assets.py
```

## Requirements

- Python 3.10+
- Poppler command-line tools:
  - `pdfinfo`
  - `pdftotext`
  - `pdftoppm`

On macOS:

```bash
brew install poppler
```

On Ubuntu/Debian:

```bash
sudo apt-get install poppler-utils
```

`sips` is used for image resizing when available on macOS. The harness still works without it.

## Install The Codex Skill

Clone this repository, then copy the skill into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/course-ppt-review-html ~/.codex/skills/
```

Then start a new Codex session and invoke:

```text
Use $course-ppt-review-html to turn this lecture PDF into an exam-ready bilingual HTML review page with detailed slide explanations.
```

## Use The Harness

The harness prepares deterministic assets from a lecture PDF:

```bash
python3 scripts/prepare_ppt_review_assets.py \
  --pdf "/path/to/lecture.pdf" \
  --output-dir "./out/module_assets" \
  --prefix "module" \
  --pages "3,4,7-10,13,16-18,20-21" \
  --clean
```

Outputs:

- `module_slides_text.txt`
- `module_manifest.json`
- `module-slide-03.jpg` etc.
- `module_visual_snippets.html`

The skill then uses these assets to write a review page. The harness does not replace the reasoning step; it makes the extraction and screenshot work reliable.

## Example Prompt

```text
Use $course-ppt-review-html to generate final review HTML pages for these modules.

Course directory:
/path/to/course

Modules:
1. Recording Brain Activity: /path/to/recording.pdf
2. EMG: /path/to/emg.pdf
3. TMS: /path/to/tms.pdf

Requirements:
- Do not impose a fixed number of terms or short answers.
- Include every concept that helps exam performance.
- Add detailed explanations for important PPT images.
- For each slide image, explain what it teaches, how to read it, what to remember, an exam-ready English sentence, and one common misconception.
- English short answers must have full Chinese sentence translations.
- Prioritize slide-grounded content and label slide sources.
- Verify mobile readability and broken images.
```

## Copyright And Privacy

Do not commit course PDFs, copyrighted slide screenshots, generated review pages based on private course material, or personal paths. The `.gitignore` excludes common slide and generated asset files by default.

For a public demo, use self-authored or openly licensed slides.

## License

MIT License.
