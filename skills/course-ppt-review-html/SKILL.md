---
name: course-ppt-review-html
description: Create exam-oriented bilingual HTML study pages from lecture PPT/PDF slides, including concept maps, source-grounded terminology, English short-answer material, Chinese translations, and slide screenshots. Use when Codex is asked to explain course slides, turn a PPT/PDF into a reusable review page, prepare resit/exam study materials, add lecture images to HTML, or build repeatable harnesses for slide-based revision. 中文：把课程 PPT/PDF 转成面向考试复习的中英双语 HTML 页面，包含知识图谱、基于来源的术语、英文短答、中文翻译和课件截图讲解。
---

# Course PPT Review HTML / 课程课件复习 HTML

## Core Workflow / 核心流程

Produce a study page that helps the learner answer exam questions, not a slide dump.

目标是生成能帮助学习者答考试题的复习页面，而不是简单堆课件截图。

1. Identify the course folder, source PPT/PDF, module name, exam scope, learner language level, and output target.
   确认课程目录、源 PPT/PDF、模块名称、考试范围、学习者语言水平和输出目标。
2. If the source is PPT/PPTX, first export or convert it to PDF with the best local tool available; then extract slide text with structured tools (`pdftotext -layout` for PDF when available).
   如果源文件是 PPT/PPTX，先用本地可用工具导出或转换为 PDF；再用结构化工具提取课件文本，例如 PDF 可优先使用 `pdftotext -layout`。
3. Read enough extracted text to reconstruct the lecture logic before writing.
   写作前先阅读足够多的提取文本，重建课程讲解逻辑。
4. Select screenshot pages by learning value: diagrams, tables, workflows, mechanisms, equations, comparison figures, and dense visual summaries.
   按学习价值选择截图页：图示、表格、流程、机制、公式、对比图和高密度总结页优先。
5. Use `scripts/prepare_ppt_review_assets.py` to create slide screenshots, extracted text, a manifest, and starter HTML figure snippets.
   使用 `scripts/prepare_ppt_review_assets.py` 生成课件截图、提取文本、manifest 和初始 HTML 图片片段。
6. Build or update an HTML page with:
   - module logic map / 模块逻辑图；
   - detailed slide-image explanations / 课件图片详细讲解；
   - important terms and concepts / 重点术语和概念；
   - exam-ready English short answers with Chinese sentence translations / 可背诵英文短答和完整中文句子翻译；
   - comparison tables or misconception checks / 对比表或误区检查；
   - a practical memorization order / 可执行的记忆顺序。
7. Verify locally in a browser when possible, including mobile width, image loading, console errors, and horizontal overflow.
   尽可能在本地浏览器验证，包括移动端宽度、图片加载、控制台错误和横向溢出。

## Harness / 素材提取工具

Use the bundled helper from this skill folder:

使用 skill 文件夹内置 helper：

```bash
python3 skills/course-ppt-review-html/scripts/prepare_ppt_review_assets.py \
  --pdf "/path/to/lecture.pdf" \
  --output-dir "/path/to/course/module_review_assets" \
  --prefix "module-name" \
  --pages "3,4,7-10,13,16-18,20-21"
```

The script writes / 脚本会输出：

- `<prefix>_slides_text.txt` extracted with `pdftotext -layout` / 使用 `pdftotext -layout` 提取的文本；
- `<prefix>_manifest.json` with page and image metadata / 页码和图片元数据；
- `<prefix>-slide-03.jpg`-style rendered slide images / 渲染出的课件图片；
- `<prefix>_visual_snippets.html` starter figure markup / 初始图片 HTML 片段。

Read `references/review-page-criteria.md` when judging coverage, source discipline, bilingual explanations, or mobile/offline delivery.

判断覆盖度、来源纪律、双语解释和移动端/离线交付质量时，请阅读 `references/review-page-criteria.md`。

## Source Discipline / 来源纪律

- Prefer course slides as the primary source. If a slide only contains fragments, write a coherent paraphrase directly grounded in that slide and label the slide number.
  优先以课程课件为主要来源。如果课件只有碎片信息，可以写基于该页的连贯转述，并标注页码。
- Do not invent fake source excerpts. If using external sources, cite them clearly and keep them separate from course-slide material.
  不要编造来源摘录。如果使用外部来源，必须清楚引用，并与课件来源内容区分开。
- For English short answers, provide a Chinese translation of the whole answer sentence, not merely the term meaning.
  英文短答必须翻译完整句子，而不是只翻译术语含义。
- Distinguish direct slide facts from exam-helpful synthesis. Use wording such as `Course source: slides 9-10` for slide-grounded content.
  区分课件直接事实和有助考试的综合解释。基于课件的内容可使用 `Course source: slides 9-10` 这类标注。

## Content Standards / 内容标准

- Do not impose arbitrary counts. Include all concepts that help the learner explain, compare, or apply the module.
  不要强行限制数量。凡是有助于解释、比较或应用该模块的概念，都可以纳入。
- Prioritize definitions, mechanisms, causal chains, equations, method comparisons, model assumptions, parameter meanings, and common confusions.
  优先覆盖定义、机制、因果链、公式、方法对比、模型假设、参数含义和常见混淆点。
- For non-native English learners, include:
  - English term / 英文术语；
  - Chinese meaning / 中文含义；
  - short English explanation usable in an answer / 可用于答题的简短英文解释；
  - Chinese explanation or translation / 中文解释或翻译；
  - source slide range / 来源页码范围。
- For slide images, prefer detailed explanation over one-line captions:
  - what the slide is about / 这页在讲什么；
  - how to read the diagram / 这张图怎么看；
  - what must be remembered / 必须记住什么；
  - an exam-ready English sentence / 可背诵英文考试句；
  - one common misconception / 一个常见误区。

## HTML Standards / HTML 标准

- Keep the page usable as the first screen; do not create marketing filler.
  第一屏应直接可用，不要做营销式空内容。
- Use responsive layouts and stable card dimensions; on mobile, avoid horizontal body overflow.
  使用响应式布局和稳定卡片尺寸；移动端避免页面横向溢出。
- Use local image paths when the HTML stays beside an asset folder.
  如果 HTML 与素材文件夹放在一起，使用本地图片路径。
- If the user needs phone/offline sharing, package the HTML with the asset folder or inline images as base64.
  如果用户需要手机或离线分享，应把 HTML 和素材文件夹一起打包，或将图片转为 base64 内联。
- Do not rely on external CDNs for core display.
  核心显示不要依赖外部 CDN。
- Validate counts and broken images with a script or browser check before finishing.
  交付前用脚本或浏览器检查数量和坏图。
