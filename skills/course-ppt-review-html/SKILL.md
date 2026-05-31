---
name: course-ppt-review-html
description: Create exam-oriented bilingual HTML study pages from lecture PPT/PDF slides, including concept maps, source-grounded terminology, English short-answer material, Chinese translations, and slide screenshots. Use when Codex is asked to explain course slides, turn a PPT/PDF into a reusable review page, prepare resit/exam study materials, add lecture images to HTML, or build repeatable harnesses for slide-based revision. 中文：把课程 PPT/PDF 转成面向考试复习的中英双语 HTML 页面；当用户说“帮我生成XX课程的复习html”“给XX课程做复习HTML”“把这份PPT做成考试复习HTML”“生成XX模块复习页”等短句时也应使用本 skill。
---

# Course PPT Review HTML / 课程课件复习 HTML

## Quick Invocation / 短句调用

You do not need to type the full skill name. Natural-language requests should trigger this skill, especially:

你不需要每次输入完整的 `$course-ppt-review-html`。下面这些短句都应该触发本 skill：

- `帮我生成 Signal Processing 课程的复习 HTML`
- `给这门课做一个复习 html`
- `把这个 PPT 做成考试复习 HTML`
- `帮我生成 Recording 模块复习页`
- `用这个课件生成中英双语复习网页`

When the request is short, infer the likely course folder, PPT/PDF source, module scope, learner language level, and output path from the current context. Ask a question only if the source file or course folder cannot be identified safely.

当用户只给短句时，优先从当前上下文推断课程目录、PPT/PDF 来源、模块范围、学习者语言水平和输出位置。只有在无法安全识别源文件或课程目录时，才向用户追问。

## Core Workflow / 核心流程

Produce a study page that helps the learner answer exam questions, not a slide dump.

目标是生成能帮助学习者答考试题的复习页面，而不是简单堆课件截图。

The default learner is a Chinese native speaker with weak English. Chinese is not a decorative translation layer; it is the comprehension scaffold that lets the learner understand the slide first, then memorize English exam answers.

默认学习者是中文母语者、英语较弱。中文不是装饰性翻译，而是理解脚手架：先用中文看懂课件，再把内容转成可背诵英文答案。

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
6. For stable final quality, do not freehand the final HTML. Fill a structured review spec and render it with `scripts/build_review_page.py`.
   为了避免质量漂移，最终 HTML 不要自由手写。先填写结构化 review spec，再用 `scripts/build_review_page.py` 固定渲染。
7. Build or update an HTML page with:
   - module logic map / 模块逻辑图；
   - detailed slide-image explanations / 课件图片详细讲解；
   - important terms and concepts / 重点术语和概念；
   - exam-ready English short answers with Chinese sentence translations / 可背诵英文短答和完整中文句子翻译；
   - comparison tables or misconception checks / 对比表或误区检查；
   - a practical memorization order / 可执行的记忆顺序。
8. Verify locally in a browser when possible, including mobile width, image loading, console errors, and horizontal overflow.
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

## Review Page Factory / 固定质量渲染与审查

Use `build_review_page.py` when the user wants final review HTML quality to match or exceed previous high-quality pages.

当用户希望最终复习 HTML 和之前高质量页面齐平或更好时，必须使用 `build_review_page.py`：

```bash
python3 scripts/build_review_page.py init-spec \
  --manifest "/path/to/module_assets/module_manifest.json" \
  --image-base "module_assets" \
  --course-title "Course Name" \
  --module-title "Module Name" \
  --output "/path/to/module.review-spec.json"
```

Then fill the JSON spec. Do not leave empty visual explanations, terms, short answers, confusions, or review-order sections.

然后补全 JSON spec。不要留下空的图像解释、术语、短答、易混点或复习顺序。

Every major learning unit must have a Chinese counterpart:

每个主要学习单元都必须有中文配套内容：

- logic map cards need `title_zh` and `text_zh`;
- visual cards need `what_zh`, `how_zh`, `remember_zh`, `exam_sentence_zh`, and `dont_confuse_zh`;
- term cards need Chinese meanings and Chinese explanations;
- short-answer cards need full Chinese sentence translations;
- confusion cards need `wrong_zh` and `right_zh`;
- review-order cards need `items_zh`.

```bash
python3 scripts/build_review_page.py validate-spec --spec "/path/to/module.review-spec.json"
python3 scripts/build_review_page.py render --spec "/path/to/module.review-spec.json" --output "/path/to/module.html"
python3 scripts/build_review_page.py audit --html "/path/to/module.html"
```

The audit intentionally fails weak summary pages. A page with no navigation, no `.term-card`, no `.answer-card`, no `.explain-item`, or no `.exam-line` is not acceptable as a final study page.

audit 会故意拦截低配摘要页。没有导航、没有 `.term-card`、没有 `.answer-card`、没有 `.explain-item` 或没有 `.exam-line` 的页面不能作为最终复习页交付。

The audit also checks Chinese support. By default, the page should have at least 1,200 Chinese characters, at least 20 Chinese-support blocks, and a Chinese-character ratio of at least 12% of visible text. If the user says their English is weak, do not lower these gates.

audit 也会检查中文支持。默认要求至少 1,200 个中文字符、至少 20 个中文辅助块，并且中文字符占可见文本比例至少 12%。如果用户说自己英语弱，不要降低这些门槛。

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
- For Chinese learners with weak English, each paragraph that introduces reasoning, a figure, a misconception, or a memorization action should include Chinese support, not only the final short-answer translation.
  对英语较弱的中文学习者，每个引入推理、图片、误区或记忆动作的段落都应有中文辅助，而不只是给最终短答翻译。
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
