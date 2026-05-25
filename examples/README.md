# Examples / 示例

This repository intentionally does not include real course PDFs or copyrighted slide screenshots.

本仓库有意不包含真实课程 PDF 或受版权保护的课件截图。

`demo.html` is a self-authored mock review page that shows the intended output style without using private course material. `demo-preview.png` is a public-safe preview image used by the repository README and social sharing.

`demo.html` 是一个自制模拟复习页，用来展示目标输出风格，不使用私人课程材料。`demo-preview.png` 是一个公开安全的预览图，用于仓库 README 和社交媒体分享。

## Case Gallery / 案例图

The README gallery uses these files in order:

README 中的案例图按以下顺序展示：

1. `case-01-overview.png` — module overview / 模块总览
2. `case-02-visual-explanation.png` — public-safe replacement for the real PPT screenshot / 替代真实 PPT 截图的公开安全图像精讲页
3. `case-03-terminology.png` — terminology cards / 术语卡片
4. `case-04-short-answers.png` — exam-ready short answers / 英文短答素材
5. `case-05-comparison.png` — method comparison cards / 方法对比卡片

Live demo / 在线示例：

```text
https://misakakuroko.github.io/bilingual-slide-study-kit/examples/demo.html
```

To create another public demo, use slides that you authored yourself or materials released under a license that permits redistribution.

如果要创建新的公开示例，请使用你自己制作的课件，或使用允许再分发的开放许可材料。

Suggested demo structure / 建议示例结构：

```text
examples/
└── demo-course/
    ├── demo-slides.pdf
    ├── demo_assets/
    └── DEMO_REVIEW.zh.html
```

Run / 运行：

```bash
python3 scripts/prepare_ppt_review_assets.py \
  --pdf examples/demo-course/demo-slides.pdf \
  --output-dir examples/demo-course/demo_assets \
  --prefix demo \
  --pages "1-5" \
  --clean
```

Then ask Codex / 然后让 Codex 执行：

```text
Use $course-ppt-review-html to create a bilingual exam review HTML page from examples/demo-course/demo-slides.pdf.
```

中文也可以这样说：

```text
使用 $course-ppt-review-html，基于 examples/demo-course/demo-slides.pdf 创建一个中英双语考试复习 HTML 页面。
```
