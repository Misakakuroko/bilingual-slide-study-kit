---
name: course-ppt-review-html
description: Create exam-oriented bilingual HTML study pages from lecture PPT/PDF slides, including concept maps, source-grounded terminology, English short-answer material, Chinese translations, and slide screenshots. Use when Codex is asked to explain course slides, turn a PPT/PDF into a reusable review page, prepare resit/exam study materials, add lecture images to HTML, or build repeatable harnesses for slide-based revision.
---

# Course PPT Review HTML

## Core Workflow

Produce a study page that helps the learner answer exam questions, not a slide dump.

1. Identify the course folder, source PPT/PDF, module name, exam scope, learner language level, and output target.
2. If the source is PPT/PPTX, first export or convert it to PDF with the best local tool available; then extract slide text with structured tools (`pdftotext -layout` for PDF when available).
3. Read enough extracted text to reconstruct the lecture logic before writing.
4. Select screenshot pages by learning value: diagrams, tables, workflows, mechanisms, equations, comparison figures, and dense visual summaries.
5. Use `scripts/prepare_ppt_review_assets.py` to create slide screenshots, extracted text, a manifest, and starter HTML figure snippets.
6. Build or update an HTML page with:
   - module logic map,
   - detailed slide-image explanations,
   - important terms and concepts,
   - exam-ready English short answers with Chinese sentence translations,
   - comparison tables or misconception checks,
   - a practical memorization order.
7. Verify locally in a browser when possible, including mobile width, image loading, console errors, and horizontal overflow.

## Harness

Use the bundled helper from this skill folder:

```bash
python3 skills/course-ppt-review-html/scripts/prepare_ppt_review_assets.py \
  --pdf "/path/to/lecture.pdf" \
  --output-dir "/path/to/course/module_review_assets" \
  --prefix "module-name" \
  --pages "3,4,7-10,13,16-18,20-21"
```

The script writes:

- `<prefix>_slides_text.txt` extracted with `pdftotext -layout`
- `<prefix>_manifest.json` with page and image metadata
- `<prefix>-slide-03.jpg`-style rendered slide images
- `<prefix>_visual_snippets.html` starter figure markup

Read `references/review-page-criteria.md` when judging coverage, source discipline, bilingual explanations, or mobile/offline delivery.

## Source Discipline

- Prefer course slides as the primary source. If a slide only contains fragments, write a coherent paraphrase directly grounded in that slide and label the slide number.
- Do not invent fake source excerpts. If using external sources, cite them clearly and keep them separate from course-slide material.
- For English short answers, provide a Chinese translation of the whole answer sentence, not merely the term meaning.
- Distinguish direct slide facts from exam-helpful synthesis. Use wording such as `Course source: slides 9-10` for slide-grounded content.

## Content Standards

- Do not impose arbitrary counts. Include all concepts that help the learner explain, compare, or apply the module.
- Prioritize definitions, mechanisms, causal chains, equations, method comparisons, model assumptions, parameter meanings, and common confusions.
- For non-native English learners, include:
  - English term,
  - Chinese meaning,
  - short English explanation usable in an answer,
  - Chinese explanation or translation,
  - source slide range.
- For slide images, prefer detailed explanation over one-line captions:
  - what the slide is about,
  - how to read the diagram,
  - what must be remembered,
  - an exam-ready English sentence,
  - one common misconception.

## HTML Standards

- Keep the page usable as the first screen; do not create marketing filler.
- Use responsive layouts and stable card dimensions; on mobile, avoid horizontal body overflow.
- Use local image paths when the HTML stays beside an asset folder.
- If the user needs phone/offline sharing, package the HTML with the asset folder or inline images as base64.
- Do not rely on external CDNs for core display.
- Validate counts and broken images with a script or browser check before finishing.
