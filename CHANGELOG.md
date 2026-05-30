# Changelog / 更新日志

All notable changes to this project will be documented in this file.
本文件记录项目的重要变更。

The format is inspired by Keep a Changelog, and this project uses semantic versioning for public releases.
格式参考 Keep a Changelog，公开发布版本采用语义化版本。

## [Unreleased] / 未发布

## [0.1.5] - 2026-05-30

### Added / 新增

- Added `build_review_page.py`, a fixed-quality review-page factory with `init-spec`, `validate-spec`, `render`, `metrics`, and `audit` commands.
  新增 `build_review_page.py` 固定质量复习页工厂，支持 `init-spec`、`validate-spec`、`render`、`metrics` 和 `audit` 命令。
- Added quality gates that reject summary-like pages without navigation, term cards, answer cards, detailed visual explanations, or exam sentences.
  新增质量门，拦截缺少导航、术语卡、短答卡、图像精讲或考试句的普通摘要页。
- Added tests for the review-page harness.
  新增 review-page harness 测试。

## [0.1.4] - 2026-05-30

### Changed / 变更

- Added short natural-language invocation examples to the skill metadata, skill body, and README pages.
  在 skill 元数据、skill 正文和 README 页面中加入短句自然语言调用示例。
- Updated the skill interface prompt so short review-HTML requests are shown as the default usage path.
  更新 skill 界面提示，让简短的复习 HTML 请求成为默认使用方式。

## [0.1.3] - 2026-05-25

### Changed / 变更

- Split the mixed-language README into separate English and Simplified Chinese pages with one-click language links.
  将中英混排 README 拆分为独立英文页和简体中文页，并提供顶部一键语言切换链接。

## [0.1.2] - 2026-05-25

### Added / 新增

- Added an ordered README case gallery using repository-safe screenshots.
  新增按顺序展示的 README 案例图库。
- Replaced the real PPT screenshot case with a public-safe self-authored visual-explanation image.
  使用公开安全的自制图像精讲页替代真实 PPT 截图。

## [0.1.1] - 2026-05-25

### Changed / 变更

- Repository documentation is now bilingual in English and Chinese.
  仓库文档已改为中英双语。

## [0.1.0] - 2026-05-25

### Added / 新增

- Initial `course-ppt-review-html` Codex skill.
  初始版本的 `course-ppt-review-html` Codex skill。
- Deterministic slide asset harness for PDF text extraction, slide screenshots, manifests, and HTML visual snippets.
  稳定生成课件文本、课件截图、manifest 和 HTML 图像片段的 slide asset harness。
- Cross-platform quick-start documentation for macOS, Linux, and Windows.
  macOS、Linux 和 Windows 的跨平台快速开始文档。
- Repository CI for Python unit tests.
  用于 Python 单元测试的仓库 CI。
- MIT license.
  MIT 许可证。
