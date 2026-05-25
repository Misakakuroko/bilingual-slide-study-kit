# Contributing / 贡献指南

Thanks for considering a contribution.
感谢你考虑参与贡献。

This project is meant to help students turn lecture slides into bilingual, exam-ready study material. Contributions are especially welcome when they make the workflow easier to install, easier to verify, or safer for private course material.

这个项目希望帮助学生把课件整理成中英双语、面向考试复习的学习材料。尤其欢迎那些能让安装更简单、验证更可靠、处理私人课程材料更安全的贡献。

## Good First Contributions / 适合新贡献者的方向

- Improve Windows, Linux, or macOS setup instructions.
  改进 Windows、Linux 或 macOS 安装说明。
- Add examples using self-authored or openly licensed slides.
  使用自制或开放许可课件补充示例。
- Improve the HTML review-page template.
  改进 HTML 复习页模板。
- Add tests for the slide asset harness.
  为课件素材 harness 增加测试。
- Improve source-labeling and privacy guidance in the skill.
  改进 skill 中的来源标注和隐私说明。

## Development Setup / 开发环境

macOS/Linux:

```bash
git clone https://github.com/Misakakuroko/bilingual-slide-study-kit.git
cd bilingual-slide-study-kit
python3 -m unittest discover -s tests -v
```

Windows PowerShell:

```powershell
git clone https://github.com/Misakakuroko/bilingual-slide-study-kit.git
cd bilingual-slide-study-kit
py -3 -m unittest discover -s tests -v
```

## Contribution Rules / 贡献规则

- Do not commit private lecture PDFs, copyrighted slide screenshots, or generated pages based on private course material.
  不要提交私人课程 PDF、受版权保护的课件截图，或基于私人课程材料生成的页面。
- Do not commit personal paths, API keys, tokens, or local configuration files.
  不要提交个人本地路径、API key、token 或本地配置文件。
- Use self-authored or openly licensed material for public demos.
  公开示例必须使用自制或开放许可材料。
- Keep examples small enough to review quickly.
  示例应保持足够小，方便快速审查。
- Keep changes focused: one bug fix, feature, or documentation improvement per pull request is preferred.
  每个 pull request 尽量聚焦一个 bug 修复、功能或文档改进。

## Before Opening A Pull Request / 发起 Pull Request 前

Run tests / 运行测试：

```bash
python3 -m unittest discover -s tests -v
```

On Windows / Windows 上：

```powershell
py -3 -m unittest discover -s tests -v
```

Also check that no private course files or generated private assets were added:

同时检查没有误加入私人课件文件或私人生成资产：

```bash
git status --short
```
