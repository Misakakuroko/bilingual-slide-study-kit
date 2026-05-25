# bilingual-slide-study-kit

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Misakakuroko/bilingual-slide-study-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Misakakuroko/bilingual-slide-study-kit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](pyproject.toml)

把英文课件转换成中英双语、面向考试复习的 HTML 学习包。

`bilingual-slide-study-kit` 是一个可复用的 Codex skill，加上一个稳定提取课件文字和截图的 Python harness。它面向用第二语言学习技术课程的学生：不只是总结课件，而是生成术语、基于来源的解释、考试风格英文短答、中文翻译，以及来自原始幻灯片的图像记忆材料。

它不是普通的 PPT 转 HTML 工具。它的目标是把一份课程 PDF 变成真正能帮助学生理解知识、记住术语、写出更好考试答案的复习页面。

![Bilingual Slide Study Kit demo preview](examples/demo-preview.png)

在线示例：
[misakakuroko.github.io/bilingual-slide-study-kit/examples/demo.html](https://misakakuroko.github.io/bilingual-slide-study-kit/examples/demo.html)

示例页面为自制内容，不包含任何私人课程材料。

## 案例图

下面的图片按复习页面的使用顺序展示。第 2 张“图像精讲”截图使用公开安全的自制示意图替代真实 PPT 页面。

### 1. 模块总览

![模块总览](examples/case-01-overview.png)

### 2. 图像精讲

![图像精讲卡片](examples/case-02-visual-explanation.png)

### 3. 术语卡片

![术语卡片](examples/case-03-terminology.png)

### 4. 英文短答素材

![英文短答素材](examples/case-04-short-answers.png)

### 5. 方法对比

![方法对比卡片](examples/case-05-comparison.png)

## 为什么做它

很多学生并不是因为学不会专业知识才挂科，而是因为课件、专业术语和考试表达都在第二语言里，理解成本被放大了。

这个项目把一套复习工作流整理成可复用工具：把课件转成可以在电脑和手机上复习的双语学习包。

## 它会生成什么

每个课程模块可以生成一个独立的 HTML 复习页面，包含：

- 按页码组织的知识逻辑图；
- 关键课件截图；
- 对重要图表的详细讲解；
- 带中文辅助的重点术语；
- 可直接背诵的英文短答素材；
- 英文答题句的完整中文翻译；
- 方法对比；
- 常见混淆点和误区；
- 面向期末或补考的记忆顺序。

## 支持平台

这个项目是跨平台的。它由 Python harness 和 Codex skill 组成，并不是只支持 macOS 的应用。

| 平台 | 状态 | 说明 |
| --- | --- | --- |
| macOS | 支持 | 测试最多；如果系统有 `sips`，会用于可选图片缩放。 |
| Linux | 支持 | Python harness 通过 CI 测试。 |
| Windows | 支持 | 需要 Python 和 Poppler 命令行工具在 `PATH` 中可用。 |

## 快速开始

### 1. 安装依赖

你需要 Python 3.10+ 和 Poppler 命令行工具：

- `pdfinfo`
- `pdftotext`
- `pdftoppm`

macOS:

```bash
brew install poppler
```

Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install poppler-utils
```

Windows PowerShell:

```powershell
winget install Python.Python.3.12
winget install oschwartz10612.Poppler
```

Windows 安装 Poppler 后，重新打开终端并检查：

```powershell
pdfinfo -v
pdftotext -v
pdftoppm -v
```

如果命令找不到，请把 Poppler 的 `Library\bin` 或 `bin` 文件夹加入 Windows `PATH`。

### 2. 安装 Codex Skill

克隆仓库：

```bash
git clone https://github.com/Misakakuroko/bilingual-slide-study-kit.git
cd bilingual-slide-study-kit
```

macOS/Linux:

```bash
mkdir -p ~/.codex/skills
cp -R skills/course-ppt-review-html ~/.codex/skills/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills"
Copy-Item -Recurse ".\skills\course-ppt-review-html" "$env:USERPROFILE\.codex\skills\"
```

新开一个 Codex 会话，然后这样调用：

```text
使用 $course-ppt-review-html，把这份课程 PDF 生成一个面向考试复习的中英双语 HTML 页面，并详细讲解关键课件图片。
```

英文也可以这样说：

```text
Use $course-ppt-review-html to turn this lecture PDF into an exam-ready bilingual HTML review page with detailed slide explanations.
```

### 3. 准备课件素材

harness 会提取课件文字、指定页截图、manifest 文件，以及可复用的 HTML 图像片段。

macOS/Linux:

```bash
python3 scripts/prepare_ppt_review_assets.py \
  --pdf "/path/to/lecture.pdf" \
  --output-dir "./out/module_assets" \
  --prefix "module" \
  --pages "3,4,7-10,13,16-18,20-21" \
  --clean
```

Windows PowerShell:

```powershell
py -3 .\scripts\prepare_ppt_review_assets.py `
  --pdf "C:\path\to\lecture.pdf" `
  --output-dir ".\out\module_assets" `
  --prefix "module" `
  --pages "3,4,7-10,13,16-18,20-21" `
  --clean
```

输出：

- `module_slides_text.txt`
- `module_manifest.json`
- `module-slide-03.jpg` 等；
- `module_visual_snippets.html`

Codex skill 会基于这些稳定生成的素材写出最终复习页面。harness 不替代推理和讲解，它负责把文字提取和课件截图这部分做稳定。

## 示例提示词

```text
使用 $course-ppt-review-html，为下面几个模块生成最终版复习 HTML 页面。

课程目录：
/path/to/course

模块：
1. Recording Brain Activity: /path/to/recording.pdf
2. EMG: /path/to/emg.pdf
3. TMS: /path/to/tms.pdf

要求：
- 不要固定术语和短答数量，重要内容都可以写进去。
- 只要有助于考试得分的概念都要覆盖。
- 对重要 PPT 图片做详细讲解。
- 每张图片都要说明它在讲什么、怎么看、必须记住什么、可背诵英文句子，以及常见误区。
- 英文短答必须配完整中文翻译。
- 优先基于课件内容，并标注来源页。
- 检查手机可读性和图片路径。
```

## 仓库结构

```text
bilingual-slide-study-kit/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── pyproject.toml
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
│   ├── README.md
│   ├── case-01-overview.png
│   ├── case-02-visual-explanation.png
│   ├── case-03-terminology.png
│   ├── case-04-short-answers.png
│   ├── case-05-comparison.png
│   ├── demo.html
│   └── demo-preview.png
└── tests/
    └── test_prepare_ppt_review_assets.py
```

## 设计原则

- 基于来源：标注内容来自课件、模型推理还是用户提供材料。
- 面向考试：每段解释都应该帮助记忆、比较或答题。
- 默认双语：英文考试句应配完整中文翻译。
- 优先图像记忆：重要图表要讲解，而不是只嵌入图片。
- 注意隐私：课程 PDF、受版权保护的截图和个人路径不应进入仓库。

## 版权与隐私

不要提交课程 PDF、受版权保护的课件截图、基于私人课程材料生成的复习页面，或个人本地路径。`.gitignore` 默认排除了常见课件和生成资产。

公开示例请使用自制课件或允许再分发的开放许可材料。

## 许可证

MIT License.
