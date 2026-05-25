# Security Policy / 安全政策

## Supported Versions / 支持版本

Security fixes are currently handled on the latest `main` branch and the latest tagged release.

当前安全修复会优先处理最新的 `main` 分支和最新 tag release。

## Reporting A Vulnerability / 报告漏洞

Please open a GitHub issue if the report does not contain private data.

如果报告中不包含私人数据，请直接创建 GitHub issue。

If your report involves private course material, personal paths, API keys, tokens, or other sensitive information, do not paste the sensitive content into a public issue. Instead, describe the risk at a high level and offer to share a minimal sanitized reproduction.

如果报告涉及私人课程材料、个人路径、API key、token 或其他敏感信息，请不要把敏感内容贴到公开 issue。请只描述风险本身，并尽可能提供一个已脱敏的最小复现。

## Privacy Boundary / 隐私边界

This repository should not contain:

本仓库不应包含：

- private lecture PDFs / 私人课程 PDF；
- copyrighted slide screenshots from closed courses / 封闭课程中受版权保护的课件截图；
- generated HTML pages based on private course material / 基于私人课程材料生成的 HTML 页面；
- personal filesystem paths / 个人本地文件路径；
- API keys, tokens, or local environment files / API key、token 或本地环境文件。

The project is designed so that private course processing can happen locally while the reusable skill, harness, and templates remain public.

这个项目的设计边界是：私人课件可以在本地处理，而可复用的 skill、harness 和模板保持公开。
