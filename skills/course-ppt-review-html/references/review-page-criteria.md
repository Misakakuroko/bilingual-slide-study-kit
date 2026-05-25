# Review Page Criteria / 复习页面评审标准

## Coverage / 覆盖度

Use slide order to reconstruct the lecture logic before writing. A good review page should answer:

写作前先根据课件顺序重建课程逻辑。一个好的复习页面应该回答：

- What is the module about? / 这个模块讲什么？
- What are the major methods, signals, mechanisms, equations, or models? / 主要方法、信号、机制、公式或模型是什么？
- Which concepts are needed for compare/contrast questions? / 哪些概念适合比较题或辨析题？
- Which terms are low-frequency but useful for understanding figures or equations? / 哪些低频术语对理解图表或公式很重要？
- Which slide images make abstract content easier to remember? / 哪些课件图片能帮助记忆抽象内容？

Do not cap terminology or short answers unless the user explicitly asks for a fixed exam drill.

除非用户明确要求固定数量的练习，否则不要限制术语或短答数量。

## Sections / 页面结构

Recommended structure:

推荐结构：

1. Header with module name, source PDF/PPT, and coverage status.
   页头：模块名、来源 PDF/PPT 和覆盖状态。
2. Logic map by slide ranges.
   按课件页码范围组织的逻辑图。
3. Visual explanation section with selected slide screenshots.
   带关键课件截图的图像讲解区。
4. Terms grouped by slide range or concept group.
   按页码范围或概念组组织的术语区。
5. English short answers with Chinese sentence translations.
   配完整中文句子翻译的英文短答。
6. Method comparison cards.
   方法对比卡片。
7. Misconception or "do not confuse" cards.
   常见误区或“不要混淆”卡片。
8. Memorization sequence for two or three review passes.
   适合两到三轮复习的记忆顺序。

## Image Selection / 图片选择

Select images that explain something hard to memorize:

选择那些能解释难记内容的图片：

- method comparison figures / 方法对比图；
- system/block diagrams / 系统图或框图；
- signal traces / 信号轨迹；
- anatomical or device diagrams / 解剖图或设备图；
- tables that map concepts / 概念映射表；
- equations or model diagrams / 公式或模型图；
- parameter or mechanism timelines / 参数或机制时间线。

Skip pages that are only title, author biography, bibliography, or decorative context unless the user asks for completeness.

除非用户要求完整覆盖，否则跳过纯标题页、作者介绍、参考文献或装饰性背景页。

## Image Explanation / 图片讲解

For each important slide image, write more than a caption:

每张重要课件图片都不要只写一句 caption，应说明：

- what the slide is trying to teach / 这页想教什么；
- how to read the figure or table / 图或表应该怎么看；
- what the learner must remember / 学习者必须记住什么；
- one exam-ready English sentence / 一个可背诵的英文考试句；
- one common misconception to avoid / 一个需要避免的常见误区。

The goal is that a learner who cannot understand the PPT page alone can still follow the HTML explanation.

目标是：即使学习者单独看不懂 PPT 页面，也能通过 HTML 解释理解它。

## English Answer Quality / 英文答案质量

Each short answer should be:

每个英文短答都应该：

- grammatical and complete / 语法正确、句子完整；
- directly useful in an exam / 能直接用于考试；
- short enough to memorize / 足够短，便于背诵；
- grounded in slide content / 基于课件内容；
- translated into Chinese as a full sentence / 翻译成完整中文句子。

Prefer answer stems such as:

优先使用这类句型：

- "Compared with X, Y is more/less ..."
- "This method measures ..."
- "At the membrane level, ..."
- "The model explains ... by ..."
- "This matters because ..."

## Validation / 验证

Before delivery, check:

交付前检查：

- image files exist / 图片文件存在；
- image paths load through the same URL/file context as the HTML / 图片路径在 HTML 所处 URL 或文件上下文中能加载；
- every English short answer has a Chinese translation / 每个英文短答都有中文翻译；
- every slide-grounded answer has source slide labels / 每个基于课件的答案都有来源页标注；
- no placeholder text remains / 没有残留占位文本；
- no body-level horizontal overflow at mobile width / 移动端没有页面级横向溢出；
- local browser console has no errors / 本地浏览器控制台无错误。
